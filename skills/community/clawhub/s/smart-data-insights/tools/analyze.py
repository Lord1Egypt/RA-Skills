#!/usr/bin/env python3
"""
Data Analyst - Main Analysis Tool
Automatically analyze data files and generate insights.
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("Error: pandas not installed. Run: pip3 install pandas")
    sys.exit(1)


def load_data(file_path):
    """Load data from various formats."""
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    
    ext = file_path.suffix.lower()
    
    try:
        if ext == '.csv':
            df = pd.read_csv(file_path)
        elif ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif ext == '.json':
            df = pd.read_json(file_path)
        elif ext == '.tsv':
            df = pd.read_csv(file_path, sep='\t')
        else:
            print(f"Error: Unsupported format: {ext}")
            sys.exit(1)
        
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)


def generate_summary(df):
    """Generate statistical summary."""
    summary = {
        'rows': len(df),
        'columns': len(df.columns),
        'column_names': list(df.columns),
        'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
        'missing_values': df.isnull().sum().to_dict(),
        'missing_percentage': (df.isnull().sum() / len(df) * 100).to_dict(),
    }
    
    # Numeric columns statistics
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        summary['numeric_stats'] = {}
        for col in numeric_cols:
            summary['numeric_stats'][col] = {
                'mean': float(df[col].mean()) if not df[col].isna().all() else None,
                'median': float(df[col].median()) if not df[col].isna().all() else None,
                'std': float(df[col].std()) if not df[col].isna().all() else None,
                'min': float(df[col].min()) if not df[col].isna().all() else None,
                'max': float(df[col].max()) if not df[col].isna().all() else None,
            }
    
    # Categorical columns statistics
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    if len(cat_cols) > 0:
        summary['categorical_stats'] = {}
        for col in cat_cols:
            value_counts = df[col].value_counts()
            summary['categorical_stats'][col] = {
                'unique_count': int(df[col].nunique()),
                'top_values': value_counts.head(5).to_dict(),
            }
    
    return summary


def detect_issues(df):
    """Detect data quality issues."""
    issues = []
    
    # Check for duplicates
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        issues.append({
            'type': 'duplicates',
            'count': int(duplicates),
            'percentage': round(duplicates / len(df) * 100, 2),
            'suggestion': f'Found {duplicates} duplicate rows. Consider removing them.'
        })
    
    # Check for missing values
    missing = df.isnull().sum()
    cols_with_missing = missing[missing > 0]
    if len(cols_with_missing) > 0:
        for col, count in cols_with_missing.items():
            pct = round(count / len(df) * 100, 2)
            if pct > 50:
                suggestion = f'Column "{col}" has {pct}% missing. Consider dropping it.'
            elif pct > 10:
                suggestion = f'Column "{col}" has {pct}% missing. Consider filling with median/mode.'
            else:
                suggestion = f'Column "{col}" has {pct}% missing. Minor issue.'
            
            issues.append({
                'type': 'missing_values',
                'column': col,
                'count': int(count),
                'percentage': pct,
                'suggestion': suggestion
            })
    
    # Check for outliers in numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isna().all():
            continue
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = ((df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)).sum()
        if outliers > 0:
            issues.append({
                'type': 'outliers',
                'column': col,
                'count': int(outliers),
                'percentage': round(outliers / len(df) * 100, 2),
                'suggestion': f'Column "{col}" has {outliers} potential outliers.'
            })
    
    return issues


def generate_insights(df, summary, issues):
    """Generate actionable insights."""
    insights = []
    
    # Data quality insights
    if issues:
        high_priority = [i for i in issues if i.get('percentage', 0) > 20]
        if high_priority:
            insights.append({
                'priority': 'high',
                'category': 'data_quality',
                'message': f'Found {len(high_priority)} significant data quality issues that need attention.',
                'details': [i['suggestion'] for i in high_priority]
            })
    
    # Trend insights for time series
    date_cols = df.select_dtypes(include=['datetime64']).columns
    if len(date_cols) > 0:
        insights.append({
            'priority': 'medium',
            'category': 'time_series',
            'message': 'Time series data detected. Consider trend analysis.',
            'details': [f'Date column: {col}' for col in date_cols]
        })
    
    # Correlation insights
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) >= 2:
        corr_matrix = df[numeric_cols].corr()
        high_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr = corr_matrix.iloc[i, j]
                if abs(corr) > 0.8:
                    high_corr.append({
                        'cols': [corr_matrix.columns[i], corr_matrix.columns[j]],
                        'correlation': round(corr, 3)
                    })
        
        if high_corr:
            insights.append({
                'priority': 'medium',
                'category': 'correlation',
                'message': f'Found {len(high_corr)} strong correlations between variables.',
                'details': [f"{c['cols'][0]} <-> {c['cols'][1]}: {c['correlation']}" for c in high_corr]
            })
    
    # Size insights
    if len(df) > 100000:
        insights.append({
            'priority': 'low',
            'category': 'performance',
            'message': f'Large dataset ({len(df)} rows). Consider sampling for quick exploration.',
            'details': ['Use --sample 0.1 for 10% sample']
        })
    
    return insights


def save_summary(summary, output_path):
    """Save summary to file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)


def print_report(summary, issues, insights):
    """Print analysis report to console."""
    print("\n" + "="*60)
    print("📊 DATA ANALYSIS REPORT")
    print("="*60)
    
    print(f"\n📁 Dataset Overview:")
    print(f"   Rows: {summary['rows']:,}")
    print(f"   Columns: {summary['columns']}")
    print(f"   Column names: {', '.join(summary['column_names'][:5])}{'...' if len(summary['column_names']) > 5 else ''}")
    
    print(f"\n📈 Data Quality:")
    print(f"   Missing values: {sum(summary['missing_values'].values()):,} total")
    print(f"   Issues found: {len(issues)}")
    
    if issues:
        print(f"\n⚠️  Issues:")
        for issue in issues[:5]:  # Show top 5
            print(f"   - {issue['suggestion']}")
    
    if insights:
        print(f"\n💡 Insights:")
        for insight in insights[:3]:  # Show top 3
            print(f"   [{insight['priority'].upper()}] {insight['message']}")
    
    print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(description='Analyze data files')
    parser.add_argument('file', help='Path to data file (CSV, Excel, JSON)')
    parser.add_argument('--clean', action='store_true', help='Clean data before analysis')
    parser.add_argument('--visualize', action='store_true', help='Generate visualizations')
    parser.add_argument('--report', action='store_true', help='Generate full report')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--sample', type=float, help='Sample fraction (e.g., 0.1 for 10%)')
    parser.add_argument('--columns', help='Specific columns to analyze (comma-separated)')
    parser.add_argument('--encoding', default='utf-8', help='File encoding')
    parser.add_argument('--chunk-size', type=int, help='Process in chunks for large files')
    
    args = parser.parse_args()
    
    print(f"Loading data from: {args.file}")
    df = load_data(args.file)
    
    # Sample if requested
    if args.sample and 0 < args.sample < 1:
        df = df.sample(frac=args.sample, random_state=42)
        print(f"Sampled {args.sample*100:.0f}% of data: {len(df)} rows")
    
    # Select specific columns
    if args.columns:
        cols = [c.strip() for c in args.columns.split(',')]
        missing_cols = [c for c in cols if c not in df.columns]
        if missing_cols:
            print(f"Warning: Columns not found: {missing_cols}")
        df = df[[c for c in cols if c in df.columns]]
    
    print(f"✅ Data loaded: {len(df):,} rows, {len(df.columns)} columns")
    
    # Generate analysis
    summary = generate_summary(df)
    issues = detect_issues(df)
    insights = generate_insights(df, summary, issues)
    
    # Print report
    print_report(summary, issues, insights)
    
    # Save outputs
    base_name = Path(args.file).stem
    output_dir = Path(args.file).parent
    
    # Save summary
    summary_path = output_dir / f"{base_name}_summary.json"
    save_summary(summary, summary_path)
    print(f"\n📄 Summary saved: {summary_path}")
    
    # Clean data if requested
    if args.clean:
        from clean import clean_data
        df_cleaned = clean_data(df)
        cleaned_path = output_dir / f"{base_name}_cleaned.csv"
        df_cleaned.to_csv(cleaned_path, index=False)
        print(f"🧹 Cleaned data saved: {cleaned_path}")
    
    # Generate visualizations if requested
    if args.visualize:
        try:
            from visualize import generate_charts
            chart_paths = generate_charts(df, output_dir, base_name)
            print(f"📈 Charts generated: {len(chart_paths)} files")
            for path in chart_paths:
                print(f"   - {path}")
        except ImportError:
            print("⚠️  matplotlib not installed. Skipping visualizations.")
    
    # Generate report if requested
    if args.report:
        try:
            from report import generate_report
            report_path = output_dir / f"{base_name}_report.md"
            generate_report(summary, issues, insights, report_path)
            print(f"📝 Report saved: {report_path}")
        except ImportError:
            print("⚠️  Report module not available.")
    
    print("\n✅ Analysis complete!")


if __name__ == '__main__':
    main()
