import argparse
import pandas as pd
import numpy as np
import lightgbm as lgb
import yfinance as yf
from datetime import datetime, timedelta
import warnings
import sys

warnings.simplefilter('ignore')

def add_advanced_features(df):
    df['ret_1'] = df['Close'].pct_change(1)
    df['ret_3'] = df['Close'].pct_change(3)
    df['ret_5'] = df['Close'].pct_change(5)
    df['ret_10'] = df['Close'].pct_change(10)
    
    df['ma_10'] = df['Close'].rolling(10).mean()
    df['ma_20'] = df['Close'].rolling(20).mean()
    df['ma_50'] = df['Close'].rolling(50).mean()
    df['ma_dist'] = df['Close'] / df['ma_20'] - 1
    
    df['vol_20'] = df['ret_1'].rolling(20).std() * np.sqrt(252)
    
    df['h_l'] = df['High'] - df['Low']
    df['h_c'] = (df['High'] - df['Close'].shift(1)).abs()
    df['l_c'] = (df['Low'] - df['Close'].shift(1)).abs()
    df['tr'] = df[['h_l', 'h_c', 'l_c']].max(axis=1)
    df['atr_14'] = df['tr'].rolling(14).mean()
    
    delta = df['ret_1']
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / (loss + 1e-9)
    df['rsi_14'] = 100 - (100 / (1 + rs))
    
    ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['macd'] = ema_12 - ema_26
    df['macdsignal'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['macdhist'] = df['macd'] - df['macdsignal']
    
    df['bb_mid'] = df['Close'].rolling(20).mean()
    df['bb_std'] = df['Close'].rolling(20).std()
    df['bb_upper'] = df['bb_mid'] + (df['bb_std'] * 2)
    df['bb_lower'] = df['bb_mid'] - (df['bb_std'] * 2)
    df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / df['bb_mid']
    
    low_min = df['Low'].rolling(9).min()
    high_max = df['High'].rolling(9).max()
    rsv = (df['Close'] - low_min) / (high_max - low_min + 1e-9) * 100
    df['kdj_k'] = rsv.ewm(com=2, adjust=False).mean()
    df['kdj_d'] = df['kdj_k'].ewm(com=2, adjust=False).mean()
    df['kdj_j'] = 3 * df['kdj_k'] - 2 * df['kdj_d']
    
    df['obv'] = (np.sign(df['Close'].diff()) * df['Volume']).fillna(0).cumsum()
    df['mom_10'] = df['Close'] / df['Close'].shift(10) - 1
    
    return df.dropna()

def prepare_data(symbols, years=8):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*years)
    print(f"📡 [Downloading Data] {len(symbols)} tickers for {years} years history to rebuild indicators...")
    data = yf.download(symbols, start=start_date, end=end_date, progress=False)
    
    close_df = data.xs('Close', axis=1, level=0) if len(symbols) > 1 else data['Close'].to_frame()
    open_df = data.xs('Open', axis=1, level=0) if len(symbols) > 1 else data['Open'].to_frame()
    high_df = data.xs('High', axis=1, level=0) if len(symbols) > 1 else data['High'].to_frame()
    low_df = data.xs('Low', axis=1, level=0) if len(symbols) > 1 else data['Low'].to_frame()
    vol_df = data.xs('Volume', axis=1, level=0) if len(symbols) > 1 else data['Volume'].to_frame()
    
    if len(symbols) == 1:
        close_df.columns = symbols
        open_df.columns = symbols
        high_df.columns = symbols
        low_df.columns = symbols
        vol_df.columns = symbols

    df_dict = {}
    for sym in symbols:
        if sym not in close_df.columns or close_df[sym].isnull().all():
            continue
            
        df = pd.DataFrame({'Open': open_df[sym], 'High': high_df[sym], 'Low': low_df[sym], 'Close': close_df[sym], 'Volume': vol_df[sym]})
        df = df.dropna()
        if len(df) < 250:
            continue
            
        df = add_advanced_features(df)
        
        # Next-day targets for training
        df['target_high_pct'] = (df['High'].shift(-1) / df['Close']) - 1
        df['target_low_pct'] = (df['Low'].shift(-1) / df['Close']) - 1
        
        # We must SAVE the LAST ROW (today's close) before dropping NA (which drops the unknown tomorrow's target)
        last_row = df.iloc[-1:].copy()
        
        df = df.dropna()
        df_dict[sym] = {'train': df, 'last': last_row}
            
    return df_dict

def main():
    parser = argparse.ArgumentParser(description="Unbeatable Option Condor Signal Generator")
    parser.add_argument('symbols', metavar='S', type=str, nargs='+', help='Target stock symbols to scan (e.g. AAPL NVDA 0700.HK)')
    args = parser.parse_args()
    
    target_stocks = [s.upper() for s in args.symbols]
    
    # Reference Stocks that the AI was optimized on (Top 50B cap)
    train_symbols = [
        'AAPL', 'MSFT', 'NVDA', 'AMZN', 'GOOGL', 'META', 'TSLA', 
        'BRK-B', 'LLY', 'V', 'JPM', 'UNH', 'WMT', 'MA', 'XOM', 'JNJ', 'PG', 'HD', 'ORCL', 'COST',
        '0700.HK', '9988.HK', '3690.HK', '0941.HK', '1398.HK', '0883.HK', '1299.HK', '0939.HK', '3988.HK', '1810.HK'
    ]
    
    all_symbols = list(set(train_symbols + target_stocks))
    df_dict = prepare_data(all_symbols, years=8)
    
    print("\n🧠 [Training Daily Model] Extracting LightGBM 10% & 90% Probability Horizons...")
    feature_cols = ['ret_1', 'ret_3', 'ret_5', 'ret_10', 'ma_dist', 'vol_20', 'atr_14', 'rsi_14', 'macdhist', 'bb_width', 'kdj_k', 'kdj_d', 'kdj_j', 'obv', 'mom_10']
    
    all_train_features, all_train_target_h, all_train_target_l = [], [], []
    
    for sym in train_symbols:
        if sym not in df_dict: continue
        train_df = df_dict[sym]['train']
        all_train_features.append(train_df[feature_cols])
        all_train_target_h.append(train_df['target_high_pct'])
        all_train_target_l.append(train_df['target_low_pct'])
        
    X_train = pd.concat(all_train_features)
    p_train_h = pd.concat(all_train_target_h)
    p_train_l = pd.concat(all_train_target_l)
    
    # Fast GPU-ready params for real-time inference
    lgb_params = {'n_estimators': 300, 'learning_rate': 0.05, 'num_leaves': 16, 'random_state': 42, 'verbose': -1}
    
    m_low = lgb.LGBMRegressor(objective='quantile', alpha=0.1, **lgb_params).fit(X_train, p_train_l)
    m_high = lgb.LGBMRegressor(objective='quantile', alpha=0.9, **lgb_params).fit(X_train, p_train_h)
    
    print(f"\n========================================================")
    print(f" 🦅 CONDOR OPTION STRATEGY SIGNAL REPORT ")
    print(f"========================================================")
    
    for sym in target_stocks:
        if sym not in df_dict:
            print(f"❌ [ERROR] Could not fetch sufficient data for {sym}.")
            continue
            
        last_row = df_dict[sym]['last']
        features = last_row[feature_cols].values.reshape(1, -1)
        close_px = last_row['Close'].values[0]
        
        # Infer margins
        p_l = m_low.predict(features)[0]
        p_h = m_high.predict(features)[0]
        width = p_h - p_l
        
        put_strike = close_px * (1 + p_l)
        call_strike = close_px * (1 + p_h)
        
        print(f"\n[{sym}] Current Price: ${close_px:.2f} | Expected 1-Day Range: [{p_l*100:+.2f}%, {p_h*100:+.2f}%]")
        
        if width >= 0.04:
            print(f"✅ [SIGNAL TRIGGERED] Volatility width is {width*100:.2f}% (>= 4.00%). The market is overpaying for fear!")
            print(f"💰 ACTION REQUIRED:")
            print(f"     => SELL OTM PUT at roughly Strike ${put_strike:.2f}")
            print(f"     => SELL OTM CALL at roughly Strike ${call_strike:.2f}")
            print(f"     => (Optional: Buy further-out wings to cap risk at 3x collected premium)")
        else:
            print(f"🚫 [NO SIGNAL] Volatility width is only {width*100:.2f}%. Too narrow (< 4.00%).")
            print(f"     => Do not execute Condor. Premium is not worth the risk of a technical breakout.")
            
    print(f"\n--------------------------------------------------------")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python condor_signals.py [SYMBOLS...]")
        sys.exit(1)
    main()
