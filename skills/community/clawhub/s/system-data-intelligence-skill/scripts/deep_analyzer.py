#!/usr/bin/env python3
"""
Deep Data Analysis Engine — 4-level analysis pipeline.
Usage: python deep_analyzer.py <csv_or_excel_path> [date_col] [value_col]
"""

import sys
import json
import logging
from pathlib import Path

import pandas as pd
import numpy as np
from scipy import stats

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class DeepAnalyzer:
    """4-level data analysis: descriptive → diagnostic → predictive → prescriptive."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.report: dict = {}

    def run_full_analysis(self) -> dict:
        logger.info(f"Analyzing {self.df.shape[0]} rows x {self.df.shape[1]} columns")
        self.report['overview'] = self._overview()
        self.report['quality'] = self._data_quality()
        self.report['distributions'] = self._distributions()
        self.report['correlations'] = self._correlations()
        self.report['anomalies'] = self._detect_anomalies()
        self.report['insights'] = self._generate_insights()
        return self.report

    def _overview(self) -> dict:
        return {
            'shape': list(self.df.shape),
            'columns': list(self.df.columns),
            'dtypes': {k: str(v) for k, v in self.df.dtypes.items()},
            'memory_mb': round(self.df.memory_usage(deep=True).sum() / 1e6, 3),
        }

    def _data_quality(self) -> dict:
        missing = (self.df.isnull().sum() / len(self.df)).round(4)
        return {
            'missing_rate': missing.to_dict(),
            'duplicate_rows': int(self.df.duplicated().sum()),
            'unique_counts': self.df.nunique().to_dict(),
            'completeness': round(1 - missing.mean(), 4),
        }

    def _distributions(self) -> dict:
        result = {}
        for col in self.df.select_dtypes(include=[np.number]).columns:
            s = self.df[col].dropna()
            if len(s) == 0:
                continue
            result[col] = {
                'mean': round(float(s.mean()), 4),
                'median': round(float(s.median()), 4),
                'std': round(float(s.std()), 4),
                'min': round(float(s.min()), 4),
                'max': round(float(s.max()), 4),
                'q25': round(float(s.quantile(0.25)), 4),
                'q75': round(float(s.quantile(0.75)), 4),
                'skewness': round(float(s.skew()), 4),
                'kurtosis': round(float(s.kurtosis()), 4),
            }
        return result

    def _correlations(self) -> dict:
        numeric_df = self.df.select_dtypes(include=[np.number])
        if numeric_df.shape[1] < 2:
            return {}
        corr = numeric_df.corr().round(4)
        strong = {}
        cols = list(corr.columns)
        for i, c1 in enumerate(cols):
            for c2 in cols[i+1:]:
                r = corr.loc[c1, c2]
                if abs(r) > 0.5:
                    strong[f"{c1} x {c2}"] = round(float(r), 4)
        return {'full_matrix': corr.to_dict(), 'strong_correlations': strong}

    def _detect_anomalies(self) -> dict:
        anomalies = {}
        for col in self.df.select_dtypes(include=[np.number]).columns:
            s = self.df[col].dropna()
            if len(s) < 10:
                continue
            z = np.abs(stats.zscore(s))
            mask = z > 3
            anomalies[col] = {
                'outlier_count': int(mask.sum()),
                'outlier_pct': f"{mask.mean():.1%}",
                'outlier_indices': s[mask].index.tolist()[:20],
            }
        return anomalies

    def _generate_insights(self) -> list:
        insights = []
        quality = self.report['quality']
        high_missing = {k: v for k, v in quality['missing_rate'].items() if v > 0.1}
        if high_missing:
            insights.append(f"[WARNING] High missing rate fields (>10%): {list(high_missing.keys())}")
        if quality['duplicate_rows'] > 0:
            insights.append(f"[WARNING] Found {quality['duplicate_rows']} duplicate rows")
        for col, info in self.report['anomalies'].items():
            if info['outlier_count'] > 0:
                insights.append(f"[ANOMALY] [{col}] detected {info['outlier_count']} outliers ({info['outlier_pct']})")
        for pair, r in self.report['correlations'].get('strong_correlations', {}).items():
            direction = "positive" if r > 0 else "negative"
            insights.append(f"[CORRELATION] {pair}: strong {direction} correlation (r={r})")
        if not insights:
            insights.append("[OK] Data quality is good, no significant issues detected")
        return insights


def analyze_time_series(df: pd.DataFrame, date_col: str, value_col: str) -> dict:
    """Time series analysis: trend, seasonality, and rate-of-change."""
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=[date_col]).sort_values(date_col)
    series = df.set_index(date_col)[value_col].dropna()

    if len(series) < 3:
        return {'error': 'Insufficient data for time series analysis'}

    result = {
        'period': {'start': str(series.index[0]), 'end': str(series.index[-1]), 'points': len(series)},
        'trend_7d': {str(k): round(float(v), 4) for k, v in
                     series.rolling(min(7, len(series))).mean().dropna().items()},
        'trend_30d': {str(k): round(float(v), 4) for k, v in
                      series.rolling(min(30, len(series))).mean().dropna().items()},
    }
    if len(series) > 21:
        result['mom_latest'] = round(float(series.pct_change(21).iloc[-1]), 4)
    if len(series) > 252:
        result['yoy_latest'] = round(float(series.pct_change(252).iloc[-1]), 4)
    if len(series) >= 24:
        try:
            from statsmodels.tsa.seasonal import seasonal_decompose
            decomp = seasonal_decompose(series, model='additive', period=12, extrapolate_trend='freq')
            result['seasonality_strength'] = round(float(decomp.seasonal.std() / series.std()), 4)
        except Exception as e:
            result['seasonality_error'] = str(e)
    return result


def load_data(filepath: str) -> pd.DataFrame:
    suffix = Path(filepath).suffix.lower()
    if suffix in ('.xlsx', '.xlsm', '.xls', '.et'):
        return pd.read_excel(filepath)
    elif suffix == '.csv':
        return pd.read_csv(filepath, encoding='utf-8-sig')
    elif suffix == '.json':
        return pd.read_json(filepath)
    raise ValueError(f"Unsupported format for analysis: {suffix}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python deep_analyzer.py <filepath> [date_col] [value_col]")
        sys.exit(1)

    filepath = sys.argv[1]
    date_col = sys.argv[2] if len(sys.argv) > 2 else None
    value_col = sys.argv[3] if len(sys.argv) > 3 else None

    df = load_data(filepath)
    analyzer = DeepAnalyzer(df)
    report = analyzer.run_full_analysis()

    if date_col and value_col:
        report['time_series'] = analyze_time_series(df, date_col, value_col)

    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)

    result_path = out_dir / "analysis_result.json"
    result_path.write_text(json.dumps(report, ensure_ascii=False, default=str, indent=2), encoding='utf-8')
    logger.info(f"Analysis saved to: {result_path}")

    summary_path = out_dir / "summary.md"
    summary_path.write_text("# Data Analysis Summary\n\n" + "\n".join(f"- {i}" for i in report['insights']), encoding='utf-8')
    logger.info(f"Summary saved to: {summary_path}")

    print(json.dumps(report['insights'], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
