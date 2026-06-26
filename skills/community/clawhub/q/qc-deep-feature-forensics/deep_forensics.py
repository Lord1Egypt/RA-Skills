"""
Deep Feature Forensics Engine
=============================
Iterates over all trade records, combines YFinance historical daily data,
extracts micro-level price/volume features at the moment of entry (moving average
deviation, gap %, volume anomaly, RSI, MACD, Bollinger Band, etc.), then performs
statistical dual-sample comparison between winners and losers to generate a
Deep Feature Attribution Report.

Optimizations:
- Batch download by ticker (one request per ticker), drastically reducing network calls
- Uses yf.Ticker().history() instead of yf.download() to avoid MultiIndex / NoneType issues
- Daily data persisted to local CSV; subsequent runs hit cache directly
- 12-dimensional feature factors (including RSI, Bollinger Band, MACD, etc.)
"""
import os
import sys
import time
import warnings
import pandas as pd
import numpy as np
import yfinance as yf
import datetime
from typing import List, Dict, Optional

# Suppress yfinance FutureWarning noise
warnings.filterwarnings("ignore", category=FutureWarning, module="yfinance")


class FeatureForensics:
    def __init__(self, orders_csv: str):
        self.orders_csv = orders_csv
        self.csv_dir = os.path.dirname(os.path.abspath(orders_csv))
        self.cache_dir = os.path.join(self.csv_dir, "yfinance_cache")

        self.df = pd.read_csv(orders_csv)

        # Support alternative CSV header formats (e.g. capitalized column names)
        rename_map = {
            'Symbol': 'symbol',
            'Price': 'fillPrice',
            'Quantity': 'quantity',
            'Status': 'status',
            'Time': 'fillTime',
        }
        self.df.rename(columns=rename_map, inplace=True)

        if 'direction' not in self.df.columns and 'quantity' in self.df.columns:
            self.df['direction'] = np.where(
                pd.to_numeric(self.df['quantity'], errors='coerce') > 0, 'buy', 'sell'
            )

        self.df['fillPrice'] = pd.to_numeric(self.df['fillPrice'], errors='coerce')
        self.df['quantity'] = pd.to_numeric(self.df['quantity'], errors='coerce')

        self.df['underlying'] = self.df['symbol'].apply(self._get_underlying)
        time_col = (
            'fillTime' if 'fillTime' in self.df.columns
            else ('submitTime' if 'submitTime' in self.df.columns else 'time')
        )
        self.df['time'] = pd.to_datetime(self.df[time_col], errors='coerce')

    @staticmethod
    def _get_underlying(sym: str) -> str:
        try:
            return str(sym).split()[0].strip()
        except Exception:
            return str(sym)

    # ------------------------------------------------------------------
    # Order reconstruction
    # ------------------------------------------------------------------
    def group_trades(self) -> List[Dict]:
        """Group orders by option contract and reconstruct closed trades."""
        trades = []
        df_filled = self.df[self.df['status'] == 'Filled'].copy()
        for sym, group in df_filled.groupby('symbol'):
            buys = group[group['direction'] == 'buy']
            sells = group[group['direction'] == 'sell']

            if buys.empty:
                continue

            buy_cost = (buys['quantity'] * buys['fillPrice']).sum() * 100
            sell_return = (sells['quantity'].abs() * sells['fillPrice']).sum() * 100
            net_profit = sell_return - buy_cost
            roi = net_profit / buy_cost if buy_cost > 0 else 0

            entry_time = buys['time'].min()

            trade = {
                'symbol': sym,
                'underlying': buys.iloc[0]['underlying'],
                'entry_time': entry_time,
                'cost': buy_cost,
                'net_profit': net_profit,
                'roi': roi,
                'status': 'Closed' if not sells.empty else 'Open',
                'is_winner': net_profit > 0,
            }
            trades.append(trade)

        return [t for t in trades if t['status'] == 'Closed' and t['cost'] > 0]

    # ------------------------------------------------------------------
    # Batch data download + local CSV cache
    # ------------------------------------------------------------------
    def _download_ticker(self, ticker: str, start: str, end: str, retries: int = 2) -> Optional[pd.DataFrame]:
        """Download a single ticker using yf.Ticker().history(), with retries."""
        for attempt in range(retries + 1):
            try:
                t = yf.Ticker(ticker)
                data = t.history(start=start, end=end, auto_adjust=False)
                if data is not None and not data.empty:
                    data = data.reset_index()
                    # history() returns tz-aware Date column; strip timezone
                    data['Date'] = pd.to_datetime(data['Date']).dt.tz_localize(None).dt.date
                    return data
                return None
            except Exception as e:
                if attempt < retries:
                    time.sleep(2)
                else:
                    print(f"  [!] {ticker} download failed: {e}")
                    return None
        return None

    def bulk_download(self, trades: List[Dict]) -> Dict[str, pd.DataFrame]:
        """Aggregate date ranges by ticker and download once per ticker, using local cache first."""
        os.makedirs(self.cache_dir, exist_ok=True)

        # Compute required date range per ticker
        ticker_ranges: Dict[str, Dict] = {}
        for t in trades:
            if pd.isnull(t['entry_time']):
                continue
            tk = t['underlying']
            entry = t['entry_time']
            need_start = entry - datetime.timedelta(days=45)
            need_end = entry + datetime.timedelta(days=5)
            if tk not in ticker_ranges:
                ticker_ranges[tk] = {'start': need_start, 'end': need_end}
            else:
                if need_start < ticker_ranges[tk]['start']:
                    ticker_ranges[tk]['start'] = need_start
                if need_end > ticker_ranges[tk]['end']:
                    ticker_ranges[tk]['end'] = need_end

        total = len(ticker_ranges)
        cache_hit = 0
        downloaded = 0
        failed = 0
        ticker_data: Dict[str, pd.DataFrame] = {}

        for i, (ticker, rng) in enumerate(ticker_ranges.items(), 1):
            start_str = rng['start'].strftime('%Y-%m-%d')
            end_str = rng['end'].strftime('%Y-%m-%d')
            cache_file = os.path.join(self.cache_dir, f"{ticker}.csv")

            # Try loading from local cache
            if os.path.exists(cache_file):
                try:
                    cached = pd.read_csv(cache_file)
                    cached['Date'] = pd.to_datetime(cached['Date']).dt.date
                    cached_min = cached['Date'].min()
                    cached_max = cached['Date'].max()
                    # Cache covers required range (7-day tolerance for weekends/holidays)
                    need_start = rng['start'].date()
                    need_end = (rng['end'] - datetime.timedelta(days=7)).date()
                    if cached_min <= need_start + datetime.timedelta(days=7) and cached_max >= need_end:
                        ticker_data[ticker] = cached
                        cache_hit += 1
                        print(f"  [{i}/{total}] {ticker} -- cache hit")
                        continue
                except Exception:
                    pass  # Corrupted cache file, re-download

            # Download
            print(f"  [{i}/{total}] {ticker} -- downloading ({start_str} ~ {end_str})...")
            data = self._download_ticker(ticker, start_str, end_str)
            if data is not None and not data.empty:
                # Persist to local CSV
                data.to_csv(cache_file, index=False)
                ticker_data[ticker] = data
                downloaded += 1
            else:
                failed += 1

        print(f"\n  Download stats: {total} tickers | cache hit {cache_hit} | downloaded {downloaded} | failed {failed}")
        return ticker_data

    # ------------------------------------------------------------------
    # Technical indicator computation (pre-computed on full ticker data)
    # ------------------------------------------------------------------
    @staticmethod
    def _compute_indicators(data: pd.DataFrame) -> pd.DataFrame:
        """Pre-compute all technical indicators on full daily data."""
        df = data.copy()
        c = df['Close']
        h = df['High']
        l = df['Low']
        v = df['Volume']

        # Moving averages
        df['MA5'] = c.rolling(window=5, min_periods=1).mean()
        df['MA20'] = c.rolling(window=20, min_periods=1).mean()

        # Volume average
        df['Vol10'] = v.rolling(window=10, min_periods=1).mean()

        # ATR
        df['Range'] = h - l
        df['ATR5'] = df['Range'].rolling(window=5, min_periods=1).mean()

        # RSI-14
        delta = c.diff()
        gain = delta.clip(lower=0)
        loss = (-delta).clip(lower=0)
        avg_gain = gain.rolling(window=14, min_periods=1).mean()
        avg_loss = loss.rolling(window=14, min_periods=1).mean()
        rs = avg_gain / avg_loss.replace(0, np.nan)
        df['RSI14'] = 100 - (100 / (1 + rs))

        # Bollinger Bands (20-day, 2 std dev)
        df['BB_mid'] = df['MA20']
        bb_std = c.rolling(window=20, min_periods=1).std()
        df['BB_upper'] = df['BB_mid'] + 2 * bb_std
        df['BB_lower'] = df['BB_mid'] - 2 * bb_std

        # MACD (12, 26, 9)
        ema12 = c.ewm(span=12, min_periods=1).mean()
        ema26 = c.ewm(span=26, min_periods=1).mean()
        df['MACD_line'] = ema12 - ema26
        df['MACD_signal'] = df['MACD_line'].ewm(span=9, min_periods=1).mean()
        df['MACD_hist'] = df['MACD_line'] - df['MACD_signal']

        # Consecutive up days
        up = (c.diff() > 0).astype(int)
        streak = up.copy()
        for i in range(1, len(streak)):
            if streak.iloc[i] == 1:
                streak.iloc[i] = streak.iloc[i - 1] + 1
        df['ConsecUp'] = streak

        # 20-day rolling high
        df['High20'] = h.rolling(window=20, min_periods=1).max()

        # Previous day return
        df['PrevDayReturn'] = c.pct_change()

        df = df.ffill().bfill()
        return df

    # ------------------------------------------------------------------
    # Per-trade feature extraction (slice from pre-computed ticker data)
    # ------------------------------------------------------------------
    @staticmethod
    def _safe_float(val, default=np.nan):
        try:
            return float(val)
        except Exception:
            return default

    def extract_features_for_trade(self, trade: Dict, ticker_data: Dict[str, pd.DataFrame]) -> Dict:
        """Extract cross-section feature vector for a single trade from pre-computed ticker data."""
        ticker = trade['underlying']
        entry_time = trade['entry_time']

        if pd.isnull(entry_time) or ticker not in ticker_data:
            return {}

        data = ticker_data[ticker]
        entry_date = entry_time.date()

        past_data = data[data['Date'] <= entry_date]
        if len(past_data) < 2:
            return {}

        T0 = past_data.iloc[-1]
        T1 = past_data.iloc[-2]

        sf = self._safe_float
        c0 = sf(T0['Close'])
        o0 = sf(T0['Open'])
        h0 = sf(T0['High'])
        l0 = sf(T0['Low'])
        v0 = sf(T0['Volume'])
        ma5 = sf(T0['MA5'])
        ma20 = sf(T0['MA20'])
        vol10 = sf(T1['Vol10'])
        c_prev = sf(T1['Close'])
        atr5_prev = sf(T1['ATR5'])
        rsi14 = sf(T0['RSI14'])
        bb_upper = sf(T0['BB_upper'])
        bb_lower = sf(T0['BB_lower'])
        macd_hist = sf(T0['MACD_hist'])
        consec_up = sf(T0['ConsecUp'])
        high20 = sf(T0['High20'])
        prev_ret = sf(T1['PrevDayReturn'])

        try:
            bb_range = bb_upper - bb_lower
            features = {
                # Original 6 factors
                'gap_pct': (o0 - c_prev) / c_prev if c_prev else np.nan,
                'volume_surge': v0 / vol10 if vol10 else np.nan,
                'ma5_deviation': (c0 - ma5) / ma5 if ma5 else np.nan,
                'ma20_deviation': (c0 - ma20) / ma20 if ma20 else np.nan,
                'volatility_expansion': (h0 - l0) / atr5_prev if atr5_prev else np.nan,
                'intraday_return': (c0 - o0) / o0 if o0 else np.nan,
                # Additional 6 factors
                'rsi_14': rsi14,
                'bb_position': (c0 - bb_lower) / bb_range if bb_range and bb_range > 0 else np.nan,
                'macd_hist_norm': macd_hist / c0 if c0 else np.nan,
                'consecutive_up_days': consec_up,
                'distance_from_20d_high': (c0 - high20) / high20 if high20 else np.nan,
                'prev_day_return': prev_ret,
            }
            return features
        except Exception:
            return {}

    # ------------------------------------------------------------------
    # Main analysis pipeline
    # ------------------------------------------------------------------
    def analyze(self) -> str:
        """Main entry point: iterate trades, extract features, compare pools, generate report."""
        print("Phase 1: Parsing and reconstructing trade chains...")
        trades = self.group_trades()
        if not trades:
            return "ERROR: No complete closed trades found."

        unique_tickers = set(t['underlying'] for t in trades if not pd.isnull(t.get('entry_time')))
        print(f"  Found {len(trades)} closed trades across {len(unique_tickers)} tickers\n")

        print("Phase 2: Batch downloading YFinance OHLCV data...")
        raw_data = self.bulk_download(trades)
        if not raw_data:
            return "ERROR: All ticker data downloads failed."

        print("\nPhase 3: Pre-computing technical indicators...")
        ticker_data: Dict[str, pd.DataFrame] = {}
        for ticker, data in raw_data.items():
            ticker_data[ticker] = self._compute_indicators(data)
        print(f"  Computed indicators for {len(ticker_data)} tickers\n")

        print("Phase 4: Extracting entry cross-section features...")
        features_list = []
        for i, t in enumerate(trades, 1):
            feats = self.extract_features_for_trade(t, ticker_data)
            if feats:
                row = {**t, **feats}
                features_list.append(row)
            if i % 50 == 0 or i == len(trades):
                print(f"  Processing progress: {i}/{len(trades)}")

        df_feat = pd.DataFrame(features_list)
        if df_feat.empty:
            return "ERROR: Feature extraction failed (possibly due to network issues downloading yfinance data)."

        # Save feature matrix
        feat_out_path = self.orders_csv.rsplit('.', 1)[0] + "_features.csv"
        df_feat.to_csv(feat_out_path, index=False)
        print(f"Feature matrix saved to: {feat_out_path}\n")

        print("Phase 5: Multi-dimensional attribution analysis and report generation...")
        report = self._generate_report(df_feat)
        return report

    def _generate_report(self, df_feat: pd.DataFrame) -> str:
        """Generate the complete feature attribution report."""
        winners = df_feat[df_feat['is_winner'] == True]
        losers = df_feat[df_feat['is_winner'] == False]

        report = []
        report.append("# Deep Feature Attribution Report")
        report.append(
            "> This report analyzes all closed trades from the backtest, extracts "
            "12-dimensional technical features from underlying stock price history, "
            "and compares winner vs loser entry conditions through dual-sample "
            "statistical comparison.\n"
        )

        report.append(
            f"**Total samples**: {len(df_feat)} closed trades "
            f"(winners: {len(winners)}, losers: {len(losers)})"
        )
        win_rate = len(winners) / len(df_feat) if len(df_feat) else 0
        avg_win = winners['roi'].mean() if not winners.empty else 0
        avg_loss = losers['roi'].mean() if not losers.empty else 0
        report.append(
            f"**Overall win rate**: {win_rate:.2%} | "
            f"**Avg winner ROI**: {avg_win:.2%} | "
            f"**Avg loser ROI**: {avg_loss:.2%}\n"
        )

        # All 12 factor definitions
        metrics = [
            {'key': 'gap_pct', 'name': 'Gap open %', 'format': '{:.2%}'},
            {'key': 'volume_surge', 'name': 'Volume surge (vs 10d avg)', 'format': '{:.2f}x'},
            {'key': 'ma5_deviation', 'name': 'MA5 deviation', 'format': '{:.2%}'},
            {'key': 'ma20_deviation', 'name': 'MA20 deviation', 'format': '{:.2%}'},
            {'key': 'volatility_expansion', 'name': 'Intraday range / 5d ATR', 'format': '{:.2f}x'},
            {'key': 'intraday_return', 'name': 'Intraday return (Close-Open)', 'format': '{:.2%}'},
            {'key': 'rsi_14', 'name': 'RSI(14)', 'format': '{:.1f}'},
            {'key': 'bb_position', 'name': 'Bollinger Band position (0=lower, 1=upper)', 'format': '{:.2f}'},
            {'key': 'macd_hist_norm', 'name': 'MACD histogram (normalized)', 'format': '{:.4f}'},
            {'key': 'consecutive_up_days', 'name': 'Consecutive up days', 'format': '{:.1f}'},
            {'key': 'distance_from_20d_high', 'name': 'Distance from 20d high', 'format': '{:.2%}'},
            {'key': 'prev_day_return', 'name': 'Previous day return', 'format': '{:.2%}'},
        ]

        # -- Dimension 1: Core Feature Mean Comparison --
        report.append("## Dimension 1: Core Feature Mean Comparison (Winners vs Losers)\n")
        report.append("| Feature Factor | Winner Mean | Loser Mean | Delta | Diagnostic Significance |")
        report.append("|----------------|-------------|------------|-------|------------------------|")

        for m in metrics:
            k, name, fmt = m['key'], m['name'], m['format']
            w_mean = winners[k].mean() if not winners.empty and k in winners.columns else np.nan
            l_mean = losers[k].mean() if not losers.empty and k in losers.columns else np.nan

            w_str = fmt.format(w_mean) if not pd.isnull(w_mean) else "N/A"
            l_str = fmt.format(l_mean) if not pd.isnull(l_mean) else "N/A"

            insight = ""
            d_str = "N/A"

            if not pd.isnull(w_mean) and not pd.isnull(l_mean):
                delta = w_mean - l_mean
                d_str = fmt.format(delta)
                if delta > 0:
                    d_str = "+" + d_str

                insight = self._diagnose(k, w_mean, l_mean, delta)
            else:
                insight = "Insufficient samples"

            report.append(f"| {name} | {w_str} | {l_str} | **{d_str}** | {insight} |")

        # -- Dimension 2: What-If Filter Simulation --
        report.append("\n## Dimension 2: What-If Filter Simulation\n")
        report.append(
            "To validate filter effectiveness (avoiding losers without accidentally "
            "killing too many winners), we performed a retrospective simulation on "
            "the full sample set:\n"
        )

        trap_count = 0
        if not df_feat.empty and not losers.empty:
            n_total = len(df_feat)
            n_winners = len(winners)
            n_losers = len(losers)
            base_win_rate = n_winners / n_total if n_total > 0 else 0

            traps = [
                ('gap_pct', 0.02, '>', 0.3,
                 "Gap chase", "gap_pct > 2%"),
                ('volume_surge', 2.0, '>', 0.3,
                 "Volume spike", "volume_surge > 2.0x"),
                ('ma20_deviation', 0, '<', 0.3,
                 "Catching falling knife", "ma20_deviation < 0"),
                ('rsi_14', 70, '>', 0.3,
                 "RSI overbought", "RSI(14) > 70"),
                ('bb_position', 0.95, '>', 0.3,
                 "Bollinger upper pressure", "BB_position > 0.95"),
                ('consecutive_up_days', 2.5, '>', 0.25,
                 "Chasing after streak", "ConsecUp >= 3"),
                ('distance_from_20d_high', -0.005, '>', 0.3,
                 "Top entry", "distance_from_20d_high > -0.5%"),
                ('intraday_return', 0, '<', 0.25,
                 "Gap-up reversal", "intraday_return (Close-Open) < 0"),
            ]

            report.append(
                "| Filter | Losers avoided | Winners killed | Remaining | "
                "New win rate | Win rate change | Filtered net ROI | "
                "Net PnL impact | Verdict |"
            )
            report.append(
                "|--------|----------------|----------------|-----------|"
                "-------------|-----------------|------------------|"
                "----------------|---------|"
            )

            combined_mask = pd.Series(True, index=df_feat.index)
            base_total_roi = df_feat['roi'].sum() if not df_feat.empty else 0

            for key, threshold, direction, min_ratio, trap_name, description in traps:
                if key not in df_feat.columns:
                    continue

                # Evaluate condition
                if direction == '>':
                    filter_mask = df_feat[key] > threshold
                else:
                    filter_mask = df_feat[key] < threshold

                # Caught (will be filtered out)
                caught_df = df_feat[filter_mask]
                caught_losers = len(caught_df[caught_df['is_winner'] == False])
                caught_winners = len(caught_df[caught_df['is_winner'] == True])

                # Remaining after filter
                remain_df = df_feat[~filter_mask]
                remain_total = len(remain_df)
                remain_winners = len(remain_df[remain_df['is_winner'] == True])
                new_win_rate = remain_winners / remain_total if remain_total > 0 else 0
                win_rate_diff = new_win_rate - base_win_rate

                # Compute overall ROI impact (core logic: did total net profit increase?)
                filtered_net_roi = caught_df['roi'].sum() if not caught_df.empty else 0
                new_total_roi = remain_df['roi'].sum() if not remain_df.empty else 0
                roi_impact = new_total_roi - base_total_roi

                ratio = caught_losers / n_losers if n_losers > 0 else 0

                # Relaxed display threshold: show all factors with significant impact
                if ratio > 0.1 or roi_impact > 0.5 or roi_impact < -0.5 or (key == 'intraday_return' and caught_losers > 0):
                    trap_count += 1
                    sign = "+" if win_rate_diff > 0 else ""
                    roi_sign = "+" if roi_impact > 0 else ""

                    # Verdict classification
                    if roi_impact > 0:
                        verdict = "Shield (improves total PnL)"
                    elif roi_impact < -0.5:
                        verdict = "Toxic (kills outlier wins)"
                    else:
                        verdict = "Marginal/slightly negative"

                    report.append(
                        f"| **{trap_name}** ({description}) | {caught_losers} | "
                        f"{caught_winners} | {remain_total} | {new_win_rate:.2%} | "
                        f"**{sign}{win_rate_diff:.2%}** | {filtered_net_roi:.2%} | "
                        f"**{roi_sign}{roi_impact:.2%}** | {verdict} |"
                    )

                    # Combined effect: only stack filters that truly improved total ROI
                    if roi_impact > 0:
                        combined_mask = combined_mask & (~filter_mask)

            if trap_count > 0:
                # Evaluate combined effect
                remain_combo = df_feat[combined_mask]
                combo_total = len(remain_combo)
                combo_winners = len(remain_combo[remain_combo['is_winner'] == True])
                combo_losers = len(remain_combo[remain_combo['is_winner'] == False])
                combo_win_rate = combo_winners / combo_total if combo_total > 0 else 0
                combo_diff = combo_win_rate - base_win_rate

                combo_filtered_net_roi = df_feat[~combined_mask]['roi'].sum() if not df_feat[~combined_mask].empty else 0
                combo_total_roi = remain_combo['roi'].sum() if not remain_combo.empty else 0
                combo_roi_impact = combo_total_roi - base_total_roi

                report.append(
                    f"| **Combined [Shield] filters** | {n_losers - combo_losers} | "
                    f"{n_winners - combo_winners} | {combo_total} | "
                    f"**{combo_win_rate:.2%}** | "
                    f"**{'+' if combo_diff > 0 else ''}{combo_diff:.2%}** | "
                    f"{combo_filtered_net_roi:.2%} | "
                    f"**{'+' if combo_roi_impact > 0 else ''}{combo_roi_impact:.2%}** | "
                    f"Final strategy pool |"
                )

        if trap_count == 0:
            report.append("- No highly distributed extreme traps detected, or no factor effectively improved win rate.")

        # -- Dimension 3: Winner Entry Profile --
        report.append("\n## Dimension 3: Winner Entry Profile\n")
        report.append(
            "Based on statistical distribution of winning trades, the following "
            "are reference ranges for the ideal entry environment (25th-75th percentile):\n"
        )

        if not winners.empty:
            report.append("| Feature Factor | Median | 25th pctl | 75th pctl |")
            report.append("|----------------|--------|-----------|-----------|")
            for m in metrics:
                k, name, fmt = m['key'], m['name'], m['format']
                if k not in winners.columns:
                    continue
                col = winners[k].dropna()
                if col.empty:
                    continue
                med = col.median()
                q25 = col.quantile(0.25)
                q75 = col.quantile(0.75)
                report.append(f"| {name} | {fmt.format(med)} | {fmt.format(q25)} | {fmt.format(q75)} |")
        else:
            report.append("No winning trades found; cannot generate profile.")

        report.append(
            f"\n---\n*Generated by Deep Feature Forensics Engine | "
            f"Cache directory: `{self.cache_dir}`*"
        )

        return "\n".join(report)

    @staticmethod
    def _diagnose(key: str, w_mean: float, l_mean: float, delta: float) -> str:
        """Generate qualitative diagnostic based on factor type."""
        if key == 'gap_pct':
            if delta > 0.01:
                return "Winners tend to occur in gap-up environments"
            elif delta < -0.01:
                return "Losers often accompany gap-up reversals"
        elif key == 'volume_surge':
            if delta > 0.3:
                return "Volume confirmation helps trend establishment"
            elif delta < -0.3:
                return "Losses often occur in low-volume / false-signal environments"
        elif key == 'ma5_deviation':
            if w_mean > 0 and l_mean < 0:
                return "Entering only above the 5-day MA is safer"
            elif delta > 0.02:
                return "Trend-following near short-term MA is effective"
        elif key == 'ma20_deviation':
            if w_mean > 0 and l_mean < 0:
                return "Entering only above the 20-day MA is safer"
            elif w_mean < l_mean - 0.02:
                return "Excessive MA deviation leads to losses (mean reversion)"
        elif key == 'volatility_expansion':
            if delta > 0.3:
                return "Expanded volatility environment favors winners"
            elif delta < -0.3:
                return "Low volatility environments make profits difficult"
        elif key == 'intraday_return':
            if delta > 0.005:
                return "Winners entered on days with stronger underlying performance"
            elif delta < -0.005:
                return "Losers entered on days with weaker underlying performance"
        elif key == 'rsi_14':
            if w_mean < l_mean - 3:
                return "Entering at lower RSI is safer (avoids overbought)"
            elif w_mean > l_mean + 3:
                return "Strong momentum entry is effective"
        elif key == 'bb_position':
            if delta < -0.1:
                return "Winners tend to enter in the lower-mid Bollinger zone"
            elif delta > 0.1:
                return "Entering near upper Bollinger Band is also effective for winners"
        elif key == 'macd_hist_norm':
            if delta > 0:
                return "Positive MACD momentum confirmation is effective"
            elif delta < 0:
                return "Entering on negative MACD is paradoxically more profitable"
        elif key == 'consecutive_up_days':
            if delta < -0.5:
                return "Winners tend to enter when not on a winning streak"
            elif delta > 0.5:
                return "Chasing momentum is effective in this strategy"
        elif key == 'distance_from_20d_high':
            if delta < -0.02:
                return "Winners tend to enter at relatively lower positions"
            elif delta > 0.02:
                return "Chasing near 20-day highs is still effective"
        elif key == 'prev_day_return':
            if delta > 0.005:
                return "Entering after a prior-day up move is more profitable"
            elif delta < -0.005:
                return "Entering after a prior-day decline is paradoxically better"
        return ""


if __name__ == "__main__":
    import sys, time
    if len(sys.argv) < 2:
        print("Usage: python deep_forensics.py <orders.csv>")
        sys.exit(1)
    csv_path = sys.argv[1]
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} does not exist.")
        sys.exit(1)
    t_start = time.time()
    engine = FeatureForensics(csv_path)
    report = engine.analyze()
    out_path = os.path.join(os.path.dirname(os.path.abspath(csv_path)), "feature_diagnosis.md")
    with open(out_path, 'w') as f:
        f.write(report)
    elapsed = time.time() - t_start
    print(f"\nDeep Feature Diagnosis saved to {out_path}")
    print(f"Total time: {elapsed:.1f}s")
