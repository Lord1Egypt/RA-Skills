#!/usr/bin/env python3
"""
Data Analyzer - Analyze CSV/Excel/JSON data and generate reports

Usage:
    python analyze_data.py --input sales.csv --output report.html --group-by date
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("Warning: pandas not installed. Install with: pip install pandas")

class DataAnalyzer:
    def __init__(self, input_file):
        self.input_file = Path(input_file)
        self.data = None
        self.results = {}
        
    def load_data(self):
        """Load data from file."""
        if not self.input_file.exists():
            print(f"Error: File not found: {self.input_file}")
            return False
        
        ext = self.input_file.suffix.lower()
        
        if ext == '.csv':
            if HAS_PANDAS:
                self.data = pd.read_csv(self.input_file)
            else:
                self.data = self._load_csv_manual()
        elif ext in ['.xlsx', '.xls']:
            if HAS_PANDAS:
                self.data = pd.read_excel(self.input_file)
            else:
                print("Error: Excel files require pandas")
                return False
        elif ext == '.json':
            if HAS_PANDAS:
                self.data = pd.read_json(self.input_file)
            else:
                self.data = self._load_json_manual()
        else:
            print(f"Error: Unsupported format: {ext}")
            return False
        
        print(f"Loaded {len(self.data)} records from {self.input_file}")
        return True
    
    def _load_csv_manual(self):
        """Load CSV without pandas."""
        data = []
        with open(self.input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data
    
    def _load_json_manual(self):
        """Load JSON without pandas."""
        with open(self.input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return [data]
    
    def basic_stats(self):
        """Calculate basic statistics."""
        if HAS_PANDAS and isinstance(self.data, pd.DataFrame):
            self.results['basic_stats'] = {
                'count': len(self.data),
                'columns': list(self.data.columns),
                'numeric_summary': self.data.describe().to_dict()
            }
        else:
            # Manual calculation
            if self.data:
                self.results['basic_stats'] = {
                    'count': len(self.data),
                    'columns': list(self.data[0].keys()) if self.data else []
                }
        
        return self.results['basic_stats']
    
    def group_by(self, field, metrics=None):
        """Group data by field and calculate metrics."""
        if HAS_PANDAS and isinstance(self.data, pd.DataFrame):
            if metrics:
                grouped = self.data.groupby(field)[metrics].agg(['sum', 'mean', 'count'])
            else:
                grouped = self.data.groupby(field).size()
            self.results['grouped'] = grouped.to_dict()
        else:
            # Manual grouping
            groups = defaultdict(list)
            for row in self.data:
                key = row.get(field, 'Unknown')
                groups[key].append(row)
            
            self.results['grouped'] = {
                key: len(rows) for key, rows in groups.items()
            }
        
        return self.results['grouped']
    
    def generate_html_report(self, output_file):
        """Generate HTML report."""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Data Analysis Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        .summary {{ background: #f9f9f9; padding: 20px; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>📊 Data Analysis Report</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p>Source: {self.input_file}</p>
    
    <div class="summary">
        <h2>Summary</h2>
        <p>Total Records: {self.results.get('basic_stats', {}).get('count', 'N/A')}</p>
        <p>Columns: {', '.join(map(str, self.results.get('basic_stats', {}).get('columns', [])))}</p>
    </div>
    
    <h2>Grouped Analysis</h2>
    <table>
        <tr><th>Group</th><th>Count</th></tr>
"""
        
        # Add grouped data
        grouped = self.results.get('grouped', {})
        for key, value in grouped.items():
            html += f"        <tr><td>{key}</td><td>{value}</td></tr>\n"
        
        html += """
    </table>
</body>
</html>
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"Report saved to: {output_path}")
        return output_path

def main():
    parser = argparse.ArgumentParser(description='Data Analyzer')
    parser.add_argument('--input', required=True, help='Input data file (CSV/Excel/JSON)')
    parser.add_argument('--output', help='Output report file')
    parser.add_argument('--group-by', help='Field to group by')
    parser.add_argument('--metrics', help='Metrics to calculate (comma-separated)')
    parser.add_argument('--format', choices=['html', 'csv', 'json'], default='html',
                        help='Output format')
    args = parser.parse_args()
    
    # Load and analyze
    analyzer = DataAnalyzer(args.input)
    
    if not analyzer.load_data():
        return 1
    
    # Basic stats
    analyzer.basic_stats()
    
    # Group by if specified
    if args.group_by:
        metrics = args.metrics.split(',') if args.metrics else None
        analyzer.group_by(args.group_by, metrics)
    
    # Generate report
    if args.output:
        if args.format == 'html':
            analyzer.generate_html_report(args.output)
        elif args.format == 'json':
            with open(args.output, 'w') as f:
                json.dump(analyzer.results, f, indent=2)
            print(f"JSON saved to: {args.output}")
    
    print("\n✅ Analysis complete!")
    return 0

if __name__ == '__main__':
    sys.exit(main())
