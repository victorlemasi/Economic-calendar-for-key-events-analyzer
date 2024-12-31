import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import time
from typing import Dict, List, Optional, Tuple

class MultiSymbolTradingSystem:
    def __init__(self, 
                investing_api_key: str,
                mt5_account: int,
                mt5_password: str,
                mt5_server: str):
        """Initialize trading system with required credentials"""
        self.investing_api_key = investing_api_key
        self.mt5_account = mt5_account
        self.mt5_password = mt5_password
        self.mt5_server = mt5_server
        
        # Define trading symbols and their parameters
        self.symbols = {
            "XAUUSD": {  # Gold
                "description": "Gold",
                "pip_value": 0.1,
                "base_lot": 0.1,
                "max_spread": 35,
                "correlation": {"USD": -0.8, "SPX": -0.3}
            },
            "EURUSD": {
                "description": "Euro",
                "pip_value": 0.0001,
                "base_lot": 0.1,
                "max_spread": 2,
                "correlation": {"USD": -1.0, "Gold": 0.3}
            },
            "US30": {  # Dow Jones
                "description": "US30 Index",
                "pip_value": 1.0,
                "base_lot": 0.1,
                "max_spread": 4,
                "correlation": {"SPX": 0.95, "USD": 0.4}
            },
            "USDJPY": {
                "description": "USD/JPY",
                "pip_value": 0.01,
                "base_lot": 0.1,
                "max_spread": 2,
                "correlation": {"USD": 1.0, "SPX": 0.3}
            }
        }
        
        # Trading parameters
        self.risk_percent = 0.02  # 2% risk per trade
        self.min_impact_strength = 0.6
        
    def initialize_mt5(self) -> bool:
        """Initialize MT5 connection and select symbols"""
        if not mt5.initialize():
            print("MT5 initialization failed")
            return False
            
        authorized = mt5.login(self.mt5_account, self.mt5_password, self.mt5_server)
        if not authorized:
            print("MT5 login failed")
            mt5.shutdown()
            return False
            
        # Enable all symbols
        for symbol in self.symbols:
            selected = mt5.symbol_select(symbol, True)
            if not selected:
                print(f"Failed to select {symbol}")
                return False
                
        return True
        
    def get_market_analysis(self, symbol: str) -> Dict:
        """Analyze current market conditions for a symbol"""
        try:
            # Get recent prices
            rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H1, 0, 100)
            if rates is None:
                return {}
                
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            
            # Calculate technical indicators
            df['SMA20'] = df['close'].rolling(window=20).mean()
            df['SMA50'] = df['close'].rolling(window=50).mean()
            df['RSI'] = self._calculate_rsi(df['close'])
            df['ATR'] = self._calculate_atr(df)
            
            # Calculate additional indicators
            df['Upper_BB'], df['Lower_BB'] = self._calculate_bollinger_bands(df['close'])
            df['MACD'], df['Signal'] = self._calculate_macd(df['close'])
            
            current_price = df['close'].iloc[-1]
            current_data = df.iloc[-1]
            
            # Determine trend strength
            trend_strength = self._calculate_trend_strength(df)
            
            return {
                "current_price": current_price,
                "trend": self._determine_trend(current_data),
                "rsi": current_data['RSI'],
                "macd_signal": "BUY" if current_data['MACD'] > current_data['Signal'] else "SELL",
                "bb_position": self._check_bb_position(current_price, current_data),
                "trend_strength": trend_strength,
                "atr": current_data['ATR'],
                "volatility": self._calculate_volatility(df)
            }
            
        except Exception as e:
            print(f"Error in market analysis for {symbol}: {e}")
            return {}
            
    def _calculate_rsi(self, prices: pd.Series, periods: int = 14) -> pd.Series:
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
        
        rs = gain / loss
        return 100 - (100 / (1 + rs))
        
    def _calculate_atr(self, df: pd.DataFrame, periods: int = 14) -> pd.Series:
        """Calculate Average True Range"""
        high = df['high']
        low = df['low']
        close = df['close']
        
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return tr.rolling(window=periods).mean()
        
    def _calculate_bollinger_bands(self, prices: pd.Series, periods: int = 20) -> Tuple[pd.Series, pd.Series]:
        """Calculate Bollinger Bands"""
        sma = prices.rolling(window=periods).mean()
        std = prices.rolling(window=periods).std()
        upper_bb = sma + (std * 2)
        lower_bb = sma - (std * 2)
        return upper_bb, lower_bb
        
    def _calculate_macd(self, prices: pd.Series) -> Tuple[pd.Series, pd.Series]:
        """Calculate MACD indicator"""
        exp1 = prices.ewm(span=12, adjust=False).mean()
        exp2 = prices.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        return macd, signal
        
    def _determine_trend(self, data: pd.Series) -> str:
        """Determine current trend based on multiple indicators"""
        trend_signals = []
        
        # SMA trend
        if data['SMA20'] > data['SMA50']:
            trend_signals.append(1)
        else:
            trend_signals.append(-1)
            
        # RSI trend
        if data['RSI'] > 50:
            trend_signals.append(1)
        else:
            trend_signals.append(-1)
            
        # MACD trend
        if data['MACD'] > data['Signal']:
            trend_signals.append(1)
        else:
            trend_signals.append(-1)
            
        # Average trend signals
        avg_signal = sum(trend_signals) / len(trend_signals)
        
        if avg_signal > 0.3:
            return "Bullish"
        elif avg_signal < -0.3:
            return "Bearish"
        else:
            return "Neutral"
            
    def analyze_economic_impact_on_symbol(self, event: Dict, symbol: str) -> Dict:
        """Analyze economic event impact on specific symbol"""
        event_name = event['event_name'].lower()
        actual = float(event.get('actual', 0))
        forecast = float(event.get('forecast', 0))
        
        impact = {
            "direction": "NEUTRAL",
            "strength": 0.0,
            "hold_hours": 24
        }
        
        # Get symbol correlation factors
        correlations = self.symbols[symbol]['correlation']
        
        # Fed related events
        if 'fed' in event_name or 'fomc' in event_name:
            base_impact = self._analyze_fed_impact(actual, forecast)
            impact = self._adjust_impact_by_correlation(base_impact, correlations, 'USD')
            
        # Inflation related events
        elif 'cpi' in event_name or 'pce' in event_name:
            base_impact = self._analyze_inflation_impact(actual, forecast)
            impact = self._adjust_impact_by_correlation(base_impact, correlations, 'USD')
            
        # PMI and economic health events
        elif 'pmi' in event_name:
            base_impact = self._analyze_pmi_impact(actual, forecast)
            impact = self._adjust_impact_by_correlation(base_impact, correlations, 'SPX')
            
        return impact
        
    def _adjust_impact_by_correlation(self, base_impact: Dict, correlations: Dict, factor: str) -> Dict:
        """Adjust impact based on symbol correlations"""
        if factor in correlations:
            correlation = correlations[factor]
            
            # Adjust direction based on correlation
            if correlation < 0:
                base_impact['direction'] = "SELL" if base_impact['direction'] == "BUY" else "BUY"
                
            # Adjust strength based on correlation magnitude
            base_impact['strength'] *= abs(correlation)
            
        return base_impact
        
    def execute_trade(self, 
                     symbol: str,
                     direction: str, 
                     impact_strength: float,
                     analysis: Dict) -> bool:
        """Execute trade based on analysis and market conditions"""
        try:
            if direction not in ["BUY", "SELL"] or impact_strength < self.min_impact_strength:
                return False
                
            # Get symbol info
            symbol_info = mt5.symbol_info(symbol)
            if symbol_info is None:
                return False
                
            # Check spread
            if symbol_info.spread > self.symbols[symbol]['max_spread']:
                print(f"Spread too high for {symbol}: {symbol_info.spread} points")
                return False
                
            # Calculate stop loss based on ATR
            atr = analysis['atr']
            stop_loss_points = atr * 2  # 2 ATR for stop loss
            
            # Calculate entry price
            if direction == "BUY":
                price = symbol_info.ask
                sl = price - (stop_loss_points * symbol_info.point)
                tp = price + (stop_loss_points * 2 * symbol_info.point)  # 1:2 risk/reward
                order_type = mt5.ORDER_TYPE_BUY
            else:
                price = symbol_info.bid
                sl = price + (stop_loss_points * symbol_info.point)
                tp = price - (stop_loss_points * 2 * symbol_info.point)
                order_type = mt5.ORDER_TYPE_SELL
                
            # Calculate position size
            volume = self._calculate_position_size(symbol, stop_loss_points)
            
            # Place order
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": volume,
                "type": order_type,
                "price": price,
                "sl": sl,
                "tp": tp,
                "deviation": 10,
                "magic": 234000,
                "comment": f"Economic event trade",
                "type_time": mt5.TIMEFRAME_H4,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            result = mt5.order_send(request)
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print(f"Order failed for {symbol}, retcode: {result.retcode}")
                return False
                
            print(f"Order executed: {symbol} {direction} {volume} lots at {price}")
            return True
            
        except Exception as e:
            print(f"Error executing trade for {symbol}: {e}")
            return False
            
    def run_trading_system(self):
        """Main method to run the trading system"""
        try:
            if not self.initialize_mt5():
                return
                
            # Initialize calendar analyzer
            calendar_analyzer = InvestingCalendarAnalyzer(self.investing_api_key)
            
            # Get important US events
            events = calendar_analyzer.get_specific_events()
            
            if events.empty:
                print("No important economic events found")
                return
                
            # Analyze each symbol
            for symbol in self.symbols:
                print(f"\nAnalyzing {self.symbols[symbol]['description']} ({symbol})")
                
                # Get market analysis
                market_analysis = self.get_market_analysis(symbol)
                if not market_analysis:
                    continue
                    
                print(f"\nCurrent Market Conditions for {symbol}:")
                print(f"Price: {market_analysis['current_price']}")
                print(f"Trend: {market_analysis['trend']}")
                print(f"RSI: {market_analysis['rsi']:.2f}")
                print(f"MACD Signal: {market_analysis['macd_signal']}")
                
                # Analyze each economic event's impact on the symbol
                for _, event in events.iterrows():
                    print(f"\nAnalyzing event impact on {symbol}: {event['event_name']}")
                    
                    impact = self.analyze_economic_impact_on_symbol(event, symbol)
                    print(f"Impact Analysis:")
                    print(f"Direction: {impact['direction']}")
                    print(f"Strength: {impact['strength']:.2f}")
                    
                    # Check if we should trade
                    if impact['strength'] >= self.min_impact_strength:
                        if (impact['direction'] == "BUY" and 
                            market_analysis['trend'] == "Bullish" and 
                            market_analysis['macd_signal'] == "BUY"):
                            
                            print(f"\nExecuting BUY trade for {symbol}")
                            self.execute_trade(symbol, "BUY", impact['strength'], market_analysis)
                            
                        elif (impact['direction'] == "SELL" and 
                              market_analysis['trend'] == "Bearish" and 
                              market_analysis['macd_signal'] == "SELL"):
                              
                            print(f"\nExecuting SELL trade for {symbol}")
                            self.execute_trade(symbol, "SELL", impact['strength'], market_analysis)
                            
                        else:
                            print(f"\nConflicting signals for {symbol} - no trade")
                    else:
                        print(f"\nImpact strength {impact['strength']:.2f} below threshold")
                
        except Exception as e:
            print(f"Error in trading system: {e}")
            
        finally:
            mt5.shutdown()

def main():
    # Trading system configuration
    config = {
        "investing_api_key": "YOUR_INVESTING_COM_API_KEY",
        "mt5_account": 12345,  # Your MT5 account number
        "mt5_password": "YOUR_MT5_PASSWORD",
        "mt5_server": "YOUR_BROKER_SERVER"
    }
    
    # Initialize and run trading system
    trading_system = MultiSymbolTradingSystem(
        investing</antArtifact>
