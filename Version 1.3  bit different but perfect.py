class EconomicAnalysis:
    def __init__(self, investing_api_key: str):
        self.api_key = investing_api_key
        self.event_impact_weights = {
            "HIGH": 1.0,
            "MEDIUM": 0.6,
            "LOW": 0.3
        }
        
        # Define economic indicators and their impact on currencies
        self.indicator_impacts = {
            "GDP": {
                "impact_type": "HIGH",
                "currencies": ["USD", "EUR", "GBP", "JPY", "AUD", "CAD"],
                "interpretation": {
                    "higher": "bullish",
                    "lower": "bearish",
                    "threshold": 0.2  # % difference from forecast
                }
            },
            "Interest Rate": {
                "impact_type": "HIGH",
                "currencies": ["USD", "EUR", "GBP", "JPY", "AUD", "CAD"],
                "interpretation": {
                    "higher": "bullish",
                    "lower": "bearish",
                    "threshold": 0.25  # % points difference
                }
            },
            "NFP": {
                "impact_type": "HIGH",
                "currencies": ["USD"],
                "interpretation": {
                    "higher": "bullish",
                    "lower": "bearish",
                    "threshold": 50000  # jobs difference
                }
            },
            "CPI": {
                "impact_type": "HIGH",
                "currencies": ["USD", "EUR", "GBP", "JPY", "AUD", "CAD"],
                "interpretation": {
                    "higher": "bullish",
                    "lower": "bearish",
                    "threshold": 0.2  # % difference from forecast
                }
            },
            "Retail Sales": {
                "impact_type": "MEDIUM",
                "currencies": ["USD", "EUR", "GBP", "AUD"],
                "interpretation": {
                    "higher": "bullish",
                    "lower": "bearish",
                    "threshold": 0.3  # % difference from forecast
                }
            },
            "PMI": {
                "impact_type": "MEDIUM",
                "currencies": ["USD", "EUR", "GBP", "CNH"],
                "interpretation": {
                    "higher": "bullish",
                    "lower": "bearish",
                    "threshold": 1.0  # points difference
                }
            }
        }
        
        # Initialize database connection for historical data
        self.initialize_database()
        
    def initialize_database(self):
        """Initialize SQLite database for storing historical economic data"""
        import sqlite3
        self.conn = sqlite3.connect('economic_data.db')
        self.cursor = self.conn.cursor()
        
        # Create tables if they don't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS economic_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_name TEXT,
                country TEXT,
                date TEXT,
                actual REAL,
                forecast REAL,
                previous REAL,
                impact TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS event_impacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER,
                symbol TEXT,
                price_impact REAL,
                volatility_impact REAL,
                duration_hours INTEGER,
                FOREIGN KEY (event_id) REFERENCES economic_events (id)
            )
        ''')
        
        self.conn.commit()
        
    def fetch_economic_events(self) -> pd.DataFrame:
        """Fetch economic events from Investing.com and store in database"""
        try:
            # API endpoint for economic calendar
            url = "https://api.investing.com/economic-calendar"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Get events for past week and upcoming week
            end_date = datetime.now() + timedelta(days=7)
            start_date = datetime.now() - timedelta(days=7)
            
            params = {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "importance[]": ["1", "2", "3"]  # High, Medium, Low importance
            }
            
            response = requests.get(url, headers=headers, params=params)
            events_data = response.json()
            
            # Process and store events
            events = []
            for event in events_data['data']:
                event_info = {
                    "event_name": event['event_name'],
                    "country": event['country'],
                    "date": event['date'],
                    "actual": event.get('actual', None),
                    "forecast": event.get('forecast', None),
                    "previous": event.get('previous', None),
                    "impact": event['importance']
                }
                events.append(event_info)
                
                # Store in database
                self.store_event(event_info)
                
            return pd.DataFrame(events)
            
        except Exception as e:
            print(f"Error fetching economic events: {e}")
            return pd.DataFrame()
            
    def store_event(self, event: Dict):
        """Store economic event in database"""
        try:
            self.cursor.execute('''
                INSERT INTO economic_events 
                (event_name, country, date, actual, forecast, previous, impact)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                event['event_name'],
                event['country'],
                event['date'],
                event['actual'],
                event['forecast'],
                event['previous'],
                event['impact']
            ))
            self.conn.commit()
            
        except Exception as e:
            print(f"Error storing event: {e}")
            
    def analyze_event_impact(self, event: Dict, symbol: str) -> Dict:
        """Analyze impact of economic event compared to historical patterns"""
        try:
            # Get event history
            historical_impacts = self.get_historical_impacts(
                event['event_name'],
                event['country'],
                symbol
            )
            
            # Calculate deviation from forecast
            if event['actual'] is not None and event['forecast'] is not None:
                deviation = (event['actual'] - event['forecast']) / event['forecast']
            else:
                deviation = 0
                
            # Get indicator parameters
            indicator = self.get_indicator_type(event['event_name'])
            if indicator in self.indicator_impacts:
                impact_params = self.indicator_impacts[indicator]
                threshold = impact_params['interpretation']['threshold']
                
                # Determine impact direction
                if abs(deviation) > threshold:
                    direction = impact_params['interpretation']['higher'] if deviation > 0 else impact_params['interpretation']['lower']
                    strength = min(abs(deviation / threshold), 1.0) * self.event_impact_weights[impact_params['impact_type']]
                else:
                    direction = "neutral"
                    strength = 0
                    
                # Compare with historical impact
                if historical_impacts:
                    avg_historical_impact = historical_impacts['price_impact'].mean()
                    avg_historical_volatility = historical_impacts['volatility_impact'].mean()
                    expected_duration = int(historical_impacts['duration_hours'].mean())
                else:
                    avg_historical_impact = 0
                    avg_historical_volatility = 0
                    expected_duration = 24
                    
                return {
                    "direction": direction,
                    "strength": strength,
                    "deviation_from_forecast": deviation,
                    "historical_impact": avg_historical_impact,
                    "expected_volatility": avg_historical_volatility,
                    "expected_duration": expected_duration,
                    "notes": f"Historical average impact: {avg_historical_impact:.2f}%"
                }
                
            return {
                "direction": "neutral",
                "strength": 0,
                "deviation_from_forecast": 0,
                "historical_impact": 0,
                "expected_volatility": 0,
                "expected_duration": 24,
                "notes": "Unknown event type"
            }
            
        except Exception as e:
            print(f"Error analyzing event impact: {e}")
            return {}
            
    def get_historical_impacts(self, event_name: str, country: str, symbol: str) -> pd.DataFrame:
        """Get historical impact data for similar events"""
        try:
            query = '''
                SELECT ei.*
                FROM event_impacts ei
                JOIN economic_events ee ON ei.event_id = ee.id
                WHERE ee.event_name = ? 
                AND ee.country = ?
                AND ei.symbol = ?
                ORDER BY ee.date DESC
                LIMIT 10
            '''
            
            return pd.read_sql_query(
                query,
                self.conn,
                params=(event_name, country, symbol)
            )
            
        except Exception as e:
            print(f"Error getting historical impacts: {e}")
            return pd.DataFrame()
            
    def get_indicator_type(self, event_name: str) -> str:
        """Determine indicator type from event name"""
        event_lower = event_name.lower()
        
        if "gdp" in event_lower:
            return "GDP"
        elif "interest rate" in event_lower:
            return "Interest Rate"
        elif "nonfarm payrolls" in event_lower or "nfp" in event_lower:
            return "NFP"
        elif "cpi" in event_lower or "consumer price" in event_lower:
            return "CPI"
        elif "retail sales" in event_lower:
            return "Retail Sales"
        elif "pmi" in event_lower or "purchasing manager" in event_lower:
            return "PMI"
        else:
            return "Unknown"
            
    def update_impact_history(self, event_id: int, symbol: str, 
                            price_impact: float, volatility_impact: float,
                            duration_hours: int):
        """Store actual impact of event for future reference"""
        try:
            self.cursor.execute('''
                INSERT INTO event_impacts 
                (event_id, symbol, price_impact, volatility_impact, duration_hours)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                event_id,
                symbol,
                price_impact,
                volatility_impact,
                duration_hours
            ))
            self.conn.commit()
            
        except Exception as e:
            print(f"Error updating impact history: {e}")
            
    def analyze_combined_impact(self, events: pd.DataFrame, symbol: str) -> Dict:
        """Analyze combined impact of multiple events"""
        try:
            total_impact = 0
            max_volatility = 0
            relevant_events = []
            
            for _, event in events.iterrows():
                impact = self.analyze_event_impact(event, symbol)
                
                if impact['direction'] != "neutral":
                    impact_score = impact['strength']
                    if impact['direction'] == "bearish":
                        impact_score *= -1
                        
                    total_impact += impact_score
                    max_volatility = max(max_volatility, impact['expected_volatility'])
                    relevant_events.append({
                        "event": event['event_name'],
                        "impact": impact
                    })
                    
            # Normalize combined impact to -1 to 1 range
            if relevant_events:
                normalized_impact = np.tanh(total_impact)
                
                return {
                    "direction": "bullish" if normalized_impact > 0 else "bearish",
                    "strength": abs(normalized_impact),
                    "expected_volatility": max_volatility,
                    "relevant_events": relevant_events,
                    "notes": f"Combined impact based on {len(relevant_events)} events"
                }
                
            return {
                "direction": "neutral",
                "strength": 0,
                "expected_volatility": 0,
                "relevant_events": [],
                "notes": "No significant events found"
            }
            
        except Exception as e:
            print(f"Error analyzing combined impact: {e}")
            return {}

# Add this method to the MultiSymbolTradingSystem class
def analyze_economic_calendar(self) -> Dict[str, Dict]:
    """Analyze economic calendar for all symbols"""
    economic_analyzer = EconomicAnalysis(self.investing_api_key)
    events = economic_analyzer.fetch_economic_events()
    
    symbol_impacts = {}
    for symbol in self.symbols.keys():
        # Get currency pairs from symbol
        currencies = self.get_symbol_currencies(symbol)
        
        # Filter events for relevant currencies
        relevant_events = events[events['country'].isin(currencies)]
        
        # Analyze combined impact
        impact = economic_analyzer.analyze_combined_impact(relevant_events, symbol)
        symbol_impacts[symbol] = impact
        
    return symbol_impacts

def get_symbol_currencies(self, symbol: str) -> List[str]:
    """Extract currencies from symbol"""
    if symbol == "XAUUSD":
        return ["USD"]  # Gold is primarily affected by USD
    else:
        # For currency pairs, split into base and quote currencies
        return [symbol[:3], symbol[3:]]
