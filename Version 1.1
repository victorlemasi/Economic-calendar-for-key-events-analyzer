import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import time
from typing import Optional, Dict, List
import MetaTrader5 as mt5

class InvestingCalendarAnalyzer:
    def __init__(self, api_key: str):
        """
        Initialize with your Investing.com API key
        """
        self.base_url = "https://api.investing.com/economic-calendar"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Economic Calendar Bot"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def get_economic_calendar(self, 
                            start_date: Optional[datetime] = None,
                            end_date: Optional[datetime] = None,
                            countries: List[str] = ["US"],
                            importance: List[str] = ["high"]) -> pd.DataFrame:
        """
        Fetch economic calendar events from Investing.com
        
        Parameters:
        - start_date: Start date for calendar events
        - end_date: End date for calendar events
        - countries: List of country codes
        - importance: List of event importance levels
        """
        if start_date is None:
            start_date = datetime.now()
        if end_date is None:
            end_date = start_date + timedelta(days=7)
            
        params = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "countries": ",".join(countries),
            "importance": ",".join(importance)
        }
        
        try:
            response = self.session.get(
                f"{self.base_url}/events",
                params=params
            )
            response.raise_for_status()
            
            data = response.json()
            return pd.DataFrame(data['events'])
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching calendar data: {e}")
            return pd.DataFrame()
            
    def get_specific_events(self) -> pd.DataFrame:
        """
        Get specific important US economic events
        """
        important_events = {
            "Fed Interest Rate Decision": "fed_rate",
            "CPI": "cpi",
            "Core CPI": "core_cpi",
            "Manufacturing PMI": "pmi_manufacturing",
            "Services PMI": "pmi_services",
            "PCE Price Index": "pce",
            "Core PCE Price Index": "core_pce",
            "FOMC Meeting Minutes": "fomc_minutes"
        }
        
        events_df = self.get_economic_calendar(
            countries=["US"],
            importance=["high"]
        )
        
        if events_df.empty:
            return pd.DataFrame()
            
        mask = events_df['event_name'].str.contains('|'.join(important_events.keys()), case=False)
        return events_df[mask].copy()
        
    def analyze_event_impact(self, event_data: pd.DataFrame) -> Dict:
        """
        Analyze the potential market impact of economic events
        """
        impact_analysis = {}
        
        for _, event in event_data.iterrows():
            event_name = event['event_name']
            actual = event.get('actual')
            forecast = event.get('forecast')
            previous = event.get('previous')
            
            impact = self._calculate_impact(event_name, actual, forecast, previous)
            impact_analysis[event_name] = impact
            
        return impact_analysis
        
    def _calculate_impact(self, event_name: str, actual, forecast, previous) -> Dict:
        """
        Calculate the potential market impact of an event
        """
        if actual is None or forecast is None:
            return {
                "impact": "Unknown",
                "direction": "Neutral",
                "strength": 0.0,
                "notes": "Insufficient data"
            }
            
        try:
            actual = float(actual)
            forecast = float(forecast)
            previous = float(previous) if previous is not None else None
            
            surprise = actual - forecast
            trend = actual - previous if previous is not None else 0
            
            # Impact calculation based on event type
            if "Fed" in event_name or "FOMC" in event_name:
                return self._analyze_fed_impact(surprise, trend)
            elif "CPI" in event_name or "PCE" in event_name:
                return self._analyze_inflation_impact(surprise, trend)
            elif "PMI" in event_name:
                return self._analyze_pmi_impact(surprise, trend, actual)
            else:
                return self._analyze_generic_impact(surprise, trend)
                
        except ValueError:
            return {
                "impact": "Unknown",
                "direction": "Neutral",
                "strength": 0.0,
                "notes": "Data conversion error"
            }
            
    def _analyze_fed_impact(self, surprise: float, trend: float) -> Dict:
        """Analyze Fed-related events"""
        impact = abs(surprise) * 2  # Fed surprises have doubled impact
        
        return {
            "impact": "High" if impact > 0.5 else "Medium",
            "direction": "Hawkish" if surprise > 0 else "Dovish",
            "strength": min(impact, 1.0),
            "notes": f"{'Above' if surprise > 0 else 'Below'} expectations by {abs(surprise):.2f}"
        }
        
    def _analyze_inflation_impact(self, surprise: float, trend: float) -> Dict:
        """Analyze inflation indicators"""
        impact = abs(surprise) * 1.5
        
        return {
            "impact": "High" if impact > 0.3 else "Medium",
            "direction": "Higher" if surprise > 0 else "Lower",
            "strength": min(impact, 1.0),
            "notes": f"Inflation {('rising' if trend > 0 else 'falling')} trend"
        }
        
    def _analyze_pmi_impact(self, surprise: float, trend: float, actual: float) -> Dict:
        """Analyze PMI data"""
        expansion = actual > 50
        impact = abs(surprise)
        
        return {
            "impact": "High" if impact > 2 else "Medium",
            "direction": "Expansion" if expansion else "Contraction",
            "strength": min(impact / 2, 1.0),
            "notes": f"Economy {'expanding' if expansion else 'contracting'}"
        }
        
    def _analyze_generic_impact(self, surprise: float, trend: float) -> Dict:
        """Analyze other economic indicators"""
        impact = abs(surprise)
        
        return {
            "impact": "Medium" if impact > 0.5 else "Low",
            "direction": "Positive" if surprise > 0 else "Negative",
            "strength": min(impact, 1.0),
            "notes": "General economic indicator"
        }

def connect_mt5(username: int, password: str, server: str) -> bool:
    """Connect to MetaTrader 5 platform"""
    if not mt5.initialize():
        print("MT5 initialization failed")
        return False
        
    authorized = mt5.login(username, password, server)
    if not authorized:
        print("MT5 login failed")
        mt5.shutdown()
        return False
        
    return True

def main():
    # Initialize with your API key
    api_key = "YOUR_INVESTING_COM_API_KEY"
    analyzer = InvestingCalendarAnalyzer(api_key)
    
    # MT5 credentials
    mt5_username = 12345
    mt5_password = "your_password"
    mt5_server = "your_broker_server"
    
    try:
        # Connect to MT5
        if not connect_mt5(mt5_username, mt5_password, mt5_server):
            return
            
        # Get important US events
        events = analyzer.get_specific_events()
        
        if events.empty:
            print("No important events found")
            return
            
        # Analyze events
        impact_analysis = analyzer.analyze_event_impact(events)
        
        # Print analysis
        print("\nEconomic Calendar Analysis:")
        print("-" * 50)
        
        for event_name, analysis in impact_analysis.items():
            print(f"\nEvent: {event_name}")
            print(f"Impact: {analysis['impact']}")
            print(f"Direction: {analysis['direction']}")
            print(f"Strength: {analysis['strength']:.2f}")
            print(f"Notes: {analysis['notes']}")
            
    except Exception as e:
        print(f"Error in main execution: {e}")
        
    finally:
        mt5.shutdown()

if __name__ == "__main__":
    main()
