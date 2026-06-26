#!/usr/bin/env python3
"""
TokenBooks - Cost Aggregation Engine
Unified AI spend analysis and tracking.

Author: Shadow Rose
License: MIT
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict
from token_import import UsageRecord


@dataclass
class CostBreakdown:
    """Cost breakdown for a specific dimension."""
    total_cost: float
    total_tokens: int
    input_tokens: int
    output_tokens: int
    request_count: int


@dataclass
class TimeSeries:
    """Time series data point."""
    date: str
    cost: float
    tokens: int


class CostAggregator:
    """Aggregate and analyze AI spending."""
    
    def __init__(self, records: List[UsageRecord]):
        """
        Initialize aggregator.
        
        Args:
            records: List of usage records
        """
        self.records = records
    
    def get_total_cost(self) -> float:
        """Get total cost across all records."""
        return sum(r.cost_usd for r in self.records)
    
    def get_total_tokens(self) -> int:
        """Get total tokens across all records."""
        return sum(r.total_tokens for r in self.records)
    
    def by_provider(self) -> Dict[str, CostBreakdown]:
        """Break down costs by provider."""
        breakdown = defaultdict(lambda: {
            'cost': 0.0,
            'total_tokens': 0,
            'input_tokens': 0,
            'output_tokens': 0,
            'count': 0
        })
        
        for record in self.records:
            breakdown[record.provider]['cost'] += record.cost_usd
            breakdown[record.provider]['total_tokens'] += record.total_tokens
            breakdown[record.provider]['input_tokens'] += record.input_tokens
            breakdown[record.provider]['output_tokens'] += record.output_tokens
            breakdown[record.provider]['count'] += 1
        
        return {
            provider: CostBreakdown(
                total_cost=data['cost'],
                total_tokens=data['total_tokens'],
                input_tokens=data['input_tokens'],
                output_tokens=data['output_tokens'],
                request_count=data['count']
            )
            for provider, data in breakdown.items()
        }
    
    def by_model(self) -> Dict[str, CostBreakdown]:
        """Break down costs by model."""
        breakdown = defaultdict(lambda: {
            'cost': 0.0,
            'total_tokens': 0,
            'input_tokens': 0,
            'output_tokens': 0,
            'count': 0
        })
        
        for record in self.records:
            breakdown[record.model]['cost'] += record.cost_usd
            breakdown[record.model]['total_tokens'] += record.total_tokens
            breakdown[record.model]['input_tokens'] += record.input_tokens
            breakdown[record.model]['output_tokens'] += record.output_tokens
            breakdown[record.model]['count'] += 1
        
        return {
            model: CostBreakdown(
                total_cost=data['cost'],
                total_tokens=data['total_tokens'],
                input_tokens=data['input_tokens'],
                output_tokens=data['output_tokens'],
                request_count=data['count']
            )
            for model, data in breakdown.items()
        }
    
    def by_task(self) -> Dict[str, CostBreakdown]:
        """Break down costs by task."""
        breakdown = defaultdict(lambda: {
            'cost': 0.0,
            'total_tokens': 0,
            'input_tokens': 0,
            'output_tokens': 0,
            'count': 0
        })
        
        for record in self.records:
            task = record.task or 'untagged'
            breakdown[task]['cost'] += record.cost_usd
            breakdown[task]['total_tokens'] += record.total_tokens
            breakdown[task]['input_tokens'] += record.input_tokens
            breakdown[task]['output_tokens'] += record.output_tokens
            breakdown[task]['count'] += 1
        
        return {
            task: CostBreakdown(
                total_cost=data['cost'],
                total_tokens=data['total_tokens'],
                input_tokens=data['input_tokens'],
                output_tokens=data['output_tokens'],
                request_count=data['count']
            )
            for task, data in breakdown.items()
        }
    
    def time_series(self, period: str = 'day') -> List[TimeSeries]:
        """
        Generate time series data.
        
        Args:
            period: 'day', 'week', or 'month'
        
        Returns:
            List of TimeSeries data points
        """
        series = defaultdict(lambda: {'cost': 0.0, 'tokens': 0})
        
        for record in self.records:
            try:
                dt = datetime.fromisoformat(record.timestamp.replace('Z', '+00:00'))
            except:
                continue
            
            if period == 'day':
                key = dt.strftime('%Y-%m-%d')
            elif period == 'week':
                # Week start (Monday)
                start_of_week = dt - timedelta(days=dt.weekday())
                key = start_of_week.strftime('%Y-%m-%d')
            elif period == 'month':
                key = dt.strftime('%Y-%m')
            else:
                raise ValueError(f"Invalid period: {period}")
            
            series[key]['cost'] += record.cost_usd
            series[key]['tokens'] += record.total_tokens
        
        # Convert to sorted list
        result = [
            TimeSeries(date=date, cost=data['cost'], tokens=data['tokens'])
            for date, data in sorted(series.items())
        ]
        
        return result
    
    def detect_waste(self, threshold_ratio: float = 0.1) -> List[Dict]:
        """
        Detect potential waste (expensive models for simple tasks).
        
        Args:
            threshold_ratio: Cost-to-token ratio threshold
        
        Returns:
            List of potential waste cases
        """
        waste_cases = []
        
        # Group by model
        by_model = self.by_model()
        
        for model, breakdown in by_model.items():
            if breakdown.total_tokens == 0:
                continue
            
            cost_per_1k_tokens = (breakdown.total_cost / breakdown.total_tokens) * 1000
            
            # Flag if cost per 1k tokens is high and there are many requests
            if cost_per_1k_tokens > threshold_ratio and breakdown.request_count > 10:
                waste_cases.append({
                    'model': model,
                    'cost_per_1k_tokens': cost_per_1k_tokens,
                    'total_cost': breakdown.total_cost,
                    'request_count': breakdown.request_count,
                    'suggestion': 'Consider using a cheaper model for simple tasks'
                })
        
        return sorted(waste_cases, key=lambda x: x['total_cost'], reverse=True)
    
    def budget_analysis(self, monthly_budget: float) -> Dict:
        """
        Analyze spending against monthly budget.
        
        Args:
            monthly_budget: Monthly budget in USD
        
        Returns:
            Budget analysis dict
        """
        # Get current month spending
        current_month = datetime.now().strftime('%Y-%m')
        
        monthly_series = self.time_series(period='month')
        current_month_cost = next(
            (s.cost for s in monthly_series if s.date.startswith(current_month)),
            0.0
        )
        
        remaining = monthly_budget - current_month_cost
        utilization = (current_month_cost / monthly_budget * 100) if monthly_budget > 0 else 0
        
        return {
            'budget': monthly_budget,
            'spent': current_month_cost,
            'remaining': remaining,
            'utilization_percent': utilization,
            'status': 'over_budget' if remaining < 0 else ('warning' if utilization > 80 else 'ok')
        }


def main():
    """CLI interface for TokenBooks."""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(
        description='TokenBooks - AI Spend Analysis'
    )
    parser.add_argument(
        'data',
        help='Input JSON data file (from token_import.py)'
    )
    parser.add_argument(
        '--budget',
        type=float,
        help='Monthly budget in USD'
    )
    parser.add_argument(
        '--output',
        default='text',
        choices=['text', 'json'],
        help='Output format'
    )
    
    args = parser.parse_args()
    
    try:
        # Load data
        with open(args.data, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        records = [
            UsageRecord(**record) for record in data
        ]
        
        # Analyze
        aggregator = CostAggregator(records)
        
        total_cost = aggregator.get_total_cost()
        total_tokens = aggregator.get_total_tokens()
        by_provider = aggregator.by_provider()
        by_model = aggregator.by_model()
        waste = aggregator.detect_waste()
        
        if args.output == 'json':
            output = {
                'total_cost': total_cost,
                'total_tokens': total_tokens,
                'by_provider': {k: asdict(v) for k, v in by_provider.items()},
                'by_model': {k: asdict(v) for k, v in by_model.items()},
                'waste_detection': waste
            }
            
            if args.budget:
                output['budget_analysis'] = aggregator.budget_analysis(args.budget)
            
            print(json.dumps(output, indent=2))
        else:
            print(f"\n=== TokenBooks Analysis ===\n")
            print(f"Total cost: ${total_cost:.2f}")
            print(f"Total tokens: {total_tokens:,}\n")
            
            print(f"By Provider:")
            for provider, breakdown in sorted(by_provider.items(), key=lambda x: x[1].total_cost, reverse=True):
                print(f"  {provider}: ${breakdown.total_cost:.2f} ({breakdown.total_tokens:,} tokens, {breakdown.request_count} requests)")
            
            print(f"\nBy Model:")
            for model, breakdown in sorted(by_model.items(), key=lambda x: x[1].total_cost, reverse=True)[:10]:
                print(f"  {model}: ${breakdown.total_cost:.2f} ({breakdown.total_tokens:,} tokens)")
            
            if waste:
                print(f"\n💡 Potential Waste Detected:")
                for case in waste[:3]:
                    print(f"  {case['model']}: ${case['total_cost']:.2f} ({case['request_count']} requests)")
                    print(f"    → {case['suggestion']}")
            
            if args.budget:
                budget = aggregator.budget_analysis(args.budget)
                print(f"\n📊 Budget Analysis:")
                print(f"  Monthly budget: ${budget['budget']:.2f}")
                print(f"  Spent this month: ${budget['spent']:.2f}")
                print(f"  Remaining: ${budget['remaining']:.2f}")
                print(f"  Utilization: {budget['utilization_percent']:.1f}%")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
