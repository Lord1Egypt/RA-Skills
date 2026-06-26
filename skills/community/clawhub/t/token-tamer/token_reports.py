#!/usr/bin/env python3
"""
Token Reports — Cost report generation
Part of Token Tamer — AI API Cost Control

Author: Shadow Rose
License: MIT
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict

# Import config
try:
    import token_config as config
except ImportError:
    print("ERROR: token_config.py not found. Copy config_example.py to token_config.py and configure it.")
    sys.exit(1)

# Import from main module
from token_tamer import UsageStore, UsageRecord


class ReportGenerator:
    """Generate cost reports."""
    
    def __init__(self, config_obj):
        self.config = config_obj
        self.storage = UsageStore(Path(config_obj.USAGE_FILE))
    
    def generate_daily_report(self, date: Optional[datetime] = None) -> Dict:
        """Generate report for a specific day."""
        if date is None:
            date = datetime.now()
        
        start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        
        records = self.storage.get_records(start_date=start, end_date=end)
        
        return self._aggregate_records(records, f"Daily Report: {date.date()}")
    
    def generate_weekly_report(self, week_start: Optional[datetime] = None) -> Dict:
        """Generate report for a week."""
        if week_start is None:
            now = datetime.now()
            week_start = now - timedelta(days=now.weekday())
        
        start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=7)
        
        records = self.storage.get_records(start_date=start, end_date=end)
        
        return self._aggregate_records(records, f"Weekly Report: {start.date()} to {end.date()}")
    
    def generate_monthly_report(self, year: Optional[int] = None, month: Optional[int] = None) -> Dict:
        """Generate report for a month."""
        if year is None or month is None:
            now = datetime.now()
            year = now.year
            month = now.month
        
        start = datetime(year, month, 1)
        if month == 12:
            end = datetime(year + 1, 1, 1)
        else:
            end = datetime(year, month + 1, 1)
        
        records = self.storage.get_records(start_date=start, end_date=end)
        
        return self._aggregate_records(records, f"Monthly Report: {year}-{month:02d}")
    
    def generate_by_provider_report(self, start_date: Optional[datetime] = None,
                                   end_date: Optional[datetime] = None) -> Dict:
        """Generate report grouped by provider."""
        records = self.storage.get_records(start_date, end_date)
        
        by_provider = defaultdict(list)
        for record in records:
            by_provider[record.provider].append(record)
        
        report = {
            'title': 'Report by Provider',
            'period': f"{start_date or 'beginning'} to {end_date or 'now'}",
            'providers': {}
        }
        
        for provider, provider_records in by_provider.items():
            report['providers'][provider] = self._aggregate_records(provider_records, provider)
        
        # Add totals
        report['total_cost'] = sum(p['total_cost'] for p in report['providers'].values())
        report['total_tokens'] = sum(p['total_tokens'] for p in report['providers'].values())
        report['call_count'] = sum(p['call_count'] for p in report['providers'].values())
        
        return report
    
    def generate_by_task_report(self, start_date: Optional[datetime] = None,
                               end_date: Optional[datetime] = None) -> Dict:
        """Generate report grouped by task."""
        records = self.storage.get_records(start_date, end_date)
        
        by_task = defaultdict(list)
        for record in records:
            by_task[record.task].append(record)
        
        report = {
            'title': 'Report by Task',
            'period': f"{start_date or 'beginning'} to {end_date or 'now'}",
            'tasks': {}
        }
        
        for task, task_records in by_task.items():
            report['tasks'][task] = self._aggregate_records(task_records, task)
        
        # Add totals
        report['total_cost'] = sum(t['total_cost'] for t in report['tasks'].values())
        report['total_tokens'] = sum(t['total_tokens'] for t in report['tasks'].values())
        report['call_count'] = sum(t['call_count'] for t in report['tasks'].values())
        
        # Sort tasks by cost
        report['top_tasks'] = sorted(
            [(task, data['total_cost']) for task, data in report['tasks'].items()],
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        return report
    
    def generate_by_model_report(self, start_date: Optional[datetime] = None,
                                end_date: Optional[datetime] = None) -> Dict:
        """Generate report grouped by model."""
        records = self.storage.get_records(start_date, end_date)
        
        by_model = defaultdict(list)
        for record in records:
            key = f"{record.provider}/{record.model}"
            by_model[key].append(record)
        
        report = {
            'title': 'Report by Model',
            'period': f"{start_date or 'beginning'} to {end_date or 'now'}",
            'models': {}
        }
        
        for model, model_records in by_model.items():
            report['models'][model] = self._aggregate_records(model_records, model)
        
        # Add totals
        report['total_cost'] = sum(m['total_cost'] for m in report['models'].values())
        report['total_tokens'] = sum(m['total_tokens'] for m in report['models'].values())
        report['call_count'] = sum(m['call_count'] for m in report['models'].values())
        
        # Sort models by cost
        report['top_models'] = sorted(
            [(model, data['total_cost']) for model, data in report['models'].items()],
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        return report
    
    def _aggregate_records(self, records: List[UsageRecord], title: str = "") -> Dict:
        """Aggregate statistics from a list of records."""
        if not records:
            return {
                'title': title,
                'call_count': 0,
                'total_tokens': 0,
                'input_tokens': 0,
                'output_tokens': 0,
                'total_cost': 0.0,
                'avg_cost_per_call': 0.0,
                'avg_tokens_per_call': 0.0
            }
        
        total_cost = sum(r.cost for r in records)
        total_tokens = sum(r.total_tokens for r in records)
        input_tokens = sum(r.input_tokens for r in records)
        output_tokens = sum(r.output_tokens for r in records)
        call_count = len(records)
        
        return {
            'title': title,
            'call_count': call_count,
            'total_tokens': total_tokens,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'total_cost': total_cost,
            'avg_cost_per_call': total_cost / call_count,
            'avg_tokens_per_call': total_tokens / call_count
        }
    
    def print_report(self, report: Dict, format: str = 'text'):
        """Print report in specified format."""
        if format == 'json':
            print(json.dumps(report, indent=2))
        else:
            self._print_text_report(report)
    
    def _print_text_report(self, report: Dict):
        """Print report in human-readable text format."""
        print(f"\n{'=' * 60}")
        print(f"{report.get('title', 'Report').center(60)}")
        print(f"{'=' * 60}\n")
        
        if 'period' in report:
            print(f"Period: {report['period']}\n")
        
        # Simple aggregation report
        if 'call_count' in report:
            print(f"Total calls:       {report['call_count']:8,}")
            print(f"Total tokens:      {report['total_tokens']:8,}")
            print(f"  Input:           {report['input_tokens']:8,}")
            print(f"  Output:          {report['output_tokens']:8,}")
            print(f"Total cost:        ${report['total_cost']:8.2f}")
            print(f"Avg cost/call:     ${report['avg_cost_per_call']:8.4f}")
            print(f"Avg tokens/call:   {report['avg_tokens_per_call']:8.0f}")
        
        # Provider breakdown
        if 'providers' in report:
            print("\n" + "─" * 60)
            print("BY PROVIDER".center(60))
            print("─" * 60 + "\n")
            
            for provider, data in sorted(report['providers'].items(), 
                                        key=lambda x: x[1]['total_cost'], 
                                        reverse=True):
                print(f"{provider:20} ${data['total_cost']:8.2f}  {data['call_count']:6,} calls  {data['total_tokens']:10,} tokens")
        
        # Task breakdown
        if 'tasks' in report:
            print("\n" + "─" * 60)
            print("BY TASK".center(60))
            print("─" * 60 + "\n")
            
            for task, cost in report.get('top_tasks', [])[:10]:
                print(f"{task:30} ${cost:8.2f}")
        
        # Model breakdown
        if 'models' in report:
            print("\n" + "─" * 60)
            print("BY MODEL".center(60))
            print("─" * 60 + "\n")
            
            for model, cost in report.get('top_models', [])[:10]:
                print(f"{model:40} ${cost:8.2f}")
        
        print()


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Token Reports — Cost report generation")
    parser.add_argument('--daily', action='store_true', help='Generate daily report')
    parser.add_argument('--weekly', action='store_true', help='Generate weekly report')
    parser.add_argument('--monthly', action='store_true', help='Generate monthly report')
    parser.add_argument('--by-provider', action='store_true', help='Report by provider')
    parser.add_argument('--by-task', action='store_true', help='Report by task')
    parser.add_argument('--by-model', action='store_true', help='Report by model')
    parser.add_argument('--date', type=str, help='Date for daily report (YYYY-MM-DD)')
    parser.add_argument('--from', dest='date_from', type=str, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--to', dest='date_to', type=str, help='End date (YYYY-MM-DD)')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='Output format')
    
    args = parser.parse_args()
    
    generator = ReportGenerator(config)
    
    # Parse dates
    date = None
    date_from = None
    date_to = None
    
    if args.date:
        try:
            date = datetime.strptime(args.date, '%Y-%m-%d')
        except ValueError:
            print(f"Invalid date format: {args.date}", file=sys.stderr)
            sys.exit(1)
    
    if args.date_from:
        try:
            date_from = datetime.strptime(args.date_from, '%Y-%m-%d')
        except ValueError:
            print(f"Invalid date format: {args.date_from}", file=sys.stderr)
            sys.exit(1)
    
    if args.date_to:
        try:
            date_to = datetime.strptime(args.date_to, '%Y-%m-%d')
        except ValueError:
            print(f"Invalid date format: {args.date_to}", file=sys.stderr)
            sys.exit(1)
    
    # Generate report
    if args.daily:
        report = generator.generate_daily_report(date)
    elif args.weekly:
        report = generator.generate_weekly_report(date)
    elif args.monthly:
        if date:
            report = generator.generate_monthly_report(date.year, date.month)
        else:
            report = generator.generate_monthly_report()
    elif args.by_provider:
        report = generator.generate_by_provider_report(date_from, date_to)
    elif args.by_task:
        report = generator.generate_by_task_report(date_from, date_to)
    elif args.by_model:
        report = generator.generate_by_model_report(date_from, date_to)
    else:
        parser.print_help()
        return
    
    generator.print_report(report, format=args.format)


if __name__ == '__main__':
    main()
