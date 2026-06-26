#!/usr/bin/env python3
"""
Token Optimizer — Waste detection and optimization suggestions
Part of Token Tamer — AI API Cost Control

Author: Shadow Rose
License: MIT
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict, Counter

# Import config
try:
    import token_config as config
except ImportError:
    print("ERROR: token_config.py not found. Copy config_example.py to token_config.py and configure it.")
    sys.exit(1)

# Import from main module
from token_tamer import UsageStore, UsageRecord


class WasteDetector:
    """Detect wasteful API usage patterns."""
    
    def __init__(self, config_obj):
        self.config = config_obj
        self.storage = UsageStore(Path(config_obj.USAGE_FILE))
        self.thresholds = getattr(config_obj, 'WASTE_THRESHOLDS', {
            'duplicate_window_minutes': 5,
            'excessive_retries_count': 3,
            'large_context_tokens': 50000,
            'low_output_ratio': 0.01  # Output/input < 1%
        })
    
    def detect_all(self, days: int = 7) -> Dict:
        """Run all waste detection algorithms."""
        start_date = datetime.now() - timedelta(days=days)
        records = self.storage.get_records(start_date=start_date)
        
        results = {
            'period': f"Last {days} days",
            'total_records': len(records),
            'waste_detected': [],
            'total_waste_cost': 0.0,
            'recommendations': []
        }
        
        # Detect duplicates
        duplicates = self.detect_duplicates(records)
        if duplicates:
            waste_cost = sum(sum(r.cost for r in group[1:]) for group in duplicates)
            results['waste_detected'].append({
                'type': 'duplicate_calls',
                'count': len(duplicates),
                'waste_cost': waste_cost,
                'description': f"{len(duplicates)} groups of duplicate API calls within {self.thresholds['duplicate_window_minutes']} minutes"
            })
            results['total_waste_cost'] += waste_cost
            results['recommendations'].append("Implement caching to avoid duplicate calls")
        
        # Detect excessive retries
        retries = self.detect_excessive_retries(records)
        if retries:
            waste_cost = sum(sum(r.cost for r in group[self.thresholds['excessive_retries_count']:]) for group in retries)
            results['waste_detected'].append({
                'type': 'excessive_retries',
                'count': len(retries),
                'waste_cost': waste_cost,
                'description': f"{len(retries)} tasks with >{self.thresholds['excessive_retries_count']} retry attempts"
            })
            results['total_waste_cost'] += waste_cost
            results['recommendations'].append("Add exponential backoff and better error handling")
        
        # Detect large contexts
        large_contexts = self.detect_large_contexts(records)
        if large_contexts:
            waste_cost = sum(r.cost * 0.5 for r in large_contexts)  # Assume 50% could be trimmed
            results['waste_detected'].append({
                'type': 'large_contexts',
                'count': len(large_contexts),
                'waste_cost': waste_cost,
                'description': f"{len(large_contexts)} calls with input >{self.thresholds['large_context_tokens']:,} tokens"
            })
            results['total_waste_cost'] += waste_cost
            results['recommendations'].append("Implement context pruning and summarization")
        
        # Detect low output ratio (mostly input, little output)
        low_output = self.detect_low_output_ratio(records)
        if low_output:
            waste_cost = sum(r.cost * 0.3 for r in low_output)  # Assume 30% could be saved
            results['waste_detected'].append({
                'type': 'low_output_ratio',
                'count': len(low_output),
                'waste_cost': waste_cost,
                'description': f"{len(low_output)} calls with output/input ratio <{self.thresholds['low_output_ratio']:.1%}"
            })
            results['total_waste_cost'] += waste_cost
            results['recommendations'].append("Review prompts — may be sending unnecessary context")
        
        # Detect expensive model usage for simple tasks
        expensive_simple = self.detect_expensive_models_simple_tasks(records)
        if expensive_simple:
            waste_cost = sum(r.cost * 0.7 for r in expensive_simple)  # Assume 70% could be saved with cheaper model
            results['waste_detected'].append({
                'type': 'overqualified_models',
                'count': len(expensive_simple),
                'waste_cost': waste_cost,
                'description': f"{len(expensive_simple)} calls using expensive models for likely simple tasks"
            })
            results['total_waste_cost'] += waste_cost
            results['recommendations'].append("Use cheaper models for simple/routine tasks")
        
        return results
    
    def detect_duplicates(self, records: List[UsageRecord]) -> List[List[UsageRecord]]:
        """Detect duplicate or near-duplicate API calls."""
        # Group by task and session
        by_key = defaultdict(list)
        for record in records:
            key = (record.task, record.session, record.model)
            by_key[key].append(record)
        
        duplicates = []
        window = timedelta(minutes=self.thresholds['duplicate_window_minutes'])
        
        for key, key_records in by_key.items():
            # Sort by timestamp
            sorted_records = sorted(key_records, key=lambda r: r.timestamp)
            
            # Find clusters within time window
            current_cluster = [sorted_records[0]]
            
            for record in sorted_records[1:]:
                if record.timestamp - current_cluster[-1].timestamp <= window:
                    # Similar token counts (within 10%)
                    if abs(record.total_tokens - current_cluster[0].total_tokens) / current_cluster[0].total_tokens < 0.1:
                        current_cluster.append(record)
                    else:
                        if len(current_cluster) > 1:
                            duplicates.append(current_cluster)
                        current_cluster = [record]
                else:
                    if len(current_cluster) > 1:
                        duplicates.append(current_cluster)
                    current_cluster = [record]
            
            if len(current_cluster) > 1:
                duplicates.append(current_cluster)
        
        return duplicates
    
    def detect_excessive_retries(self, records: List[UsageRecord]) -> List[List[UsageRecord]]:
        """Detect tasks with too many retry attempts."""
        by_task = defaultdict(list)
        for record in records:
            by_task[record.task].append(record)
        
        excessive = []
        threshold = self.thresholds['excessive_retries_count']
        
        for task, task_records in by_task.items():
            if len(task_records) > threshold:
                # Check if they're within a short time period (likely retries)
                sorted_records = sorted(task_records, key=lambda r: r.timestamp)
                time_span = (sorted_records[-1].timestamp - sorted_records[0].timestamp).total_seconds() / 3600
                
                if time_span < 1:  # All within 1 hour
                    excessive.append(task_records)
        
        return excessive
    
    def detect_large_contexts(self, records: List[UsageRecord]) -> List[UsageRecord]:
        """Detect calls with excessively large input contexts."""
        threshold = self.thresholds['large_context_tokens']
        return [r for r in records if r.input_tokens > threshold]
    
    def detect_low_output_ratio(self, records: List[UsageRecord]) -> List[UsageRecord]:
        """Detect calls with very low output relative to input (possible waste)."""
        threshold = self.thresholds['low_output_ratio']
        low_output = []
        
        for record in records:
            if record.input_tokens > 0:
                ratio = record.output_tokens / record.input_tokens
                if ratio < threshold:
                    low_output.append(record)
        
        return low_output
    
    def detect_expensive_models_simple_tasks(self, records: List[UsageRecord]) -> List[UsageRecord]:
        """Detect use of expensive models for likely simple tasks."""
        # Define expensive models (these are just examples, configure in real config)
        expensive_models = [
            'gpt-4', 'claude-opus', 'claude-3-opus', 'gpt-4-turbo'
        ]
        
        expensive = []
        
        for record in records:
            is_expensive = any(em in record.model.lower() for em in expensive_models)
            
            if is_expensive and record.total_tokens < 1000:
                # Expensive model used for small request (likely simple)
                expensive.append(record)
        
        return expensive


class Optimizer:
    """Generate optimization recommendations."""
    
    def __init__(self, config_obj):
        self.config = config_obj
        self.storage = UsageStore(Path(config_obj.USAGE_FILE))
        self.detector = WasteDetector(config_obj)
    
    def generate_recommendations(self, days: int = 7) -> Dict:
        """Generate comprehensive optimization recommendations."""
        waste = self.detector.detect_all(days)
        start_date = datetime.now() - timedelta(days=days)
        records = self.storage.get_records(start_date=start_date)
        
        recommendations = {
            'period': f"Last {days} days",
            'total_cost': sum(r.cost for r in records),
            'potential_savings': waste['total_waste_cost'],
            'savings_percent': (waste['total_waste_cost'] / sum(r.cost for r in records) * 100) if records else 0,
            'waste_summary': waste,
            'optimization_opportunities': []
        }
        
        # Model usage analysis
        model_usage = self._analyze_model_usage(records)
        if model_usage['recommendations']:
            recommendations['optimization_opportunities'].append({
                'category': 'Model Selection',
                'recommendations': model_usage['recommendations']
            })
        
        # Task analysis
        task_analysis = self._analyze_task_costs(records)
        if task_analysis['recommendations']:
            recommendations['optimization_opportunities'].append({
                'category': 'Task Optimization',
                'recommendations': task_analysis['recommendations']
            })
        
        return recommendations
    
    def _analyze_model_usage(self, records: List[UsageRecord]) -> Dict:
        """Analyze model usage patterns."""
        by_model = defaultdict(list)
        for record in records:
            key = f"{record.provider}/{record.model}"
            by_model[key].append(record)
        
        model_stats = {}
        for model, model_records in by_model.items():
            total_cost = sum(r.cost for r in model_records)
            avg_tokens = sum(r.total_tokens for r in model_records) / len(model_records)
            
            model_stats[model] = {
                'count': len(model_records),
                'total_cost': total_cost,
                'avg_tokens': avg_tokens
            }
        
        recommendations = []
        
        # Find most expensive model
        if model_stats:
            most_expensive = max(model_stats.items(), key=lambda x: x[1]['total_cost'])
            recommendations.append(
                f"Top spend: {most_expensive[0]} (${most_expensive[1]['total_cost']:.2f}, {most_expensive[1]['count']} calls)"
            )
            
            # Check if cheaper alternatives exist
            if 'gpt-4' in most_expensive[0].lower() or 'opus' in most_expensive[0].lower():
                recommendations.append(
                    f"Consider using cheaper model for routine tasks (potential 70% cost reduction)"
                )
        
        return {'model_stats': model_stats, 'recommendations': recommendations}
    
    def _analyze_task_costs(self, records: List[UsageRecord]) -> Dict:
        """Analyze task-level costs."""
        by_task = defaultdict(list)
        for record in records:
            by_task[record.task].append(record)
        
        task_stats = {}
        for task, task_records in by_task.items():
            total_cost = sum(r.cost for r in task_records)
            task_stats[task] = {
                'count': len(task_records),
                'total_cost': total_cost
            }
        
        recommendations = []
        
        # Find most expensive task
        if task_stats:
            most_expensive = max(task_stats.items(), key=lambda x: x[1]['total_cost'])
            recommendations.append(
                f"Most expensive task: '{most_expensive[0]}' (${most_expensive[1]['total_cost']:.2f}, {most_expensive[1]['count']} calls)"
            )
            
            if most_expensive[1]['count'] > 10:
                recommendations.append(
                    f"Task '{most_expensive[0]}' called {most_expensive[1]['count']} times — consider caching results"
                )
        
        return {'task_stats': task_stats, 'recommendations': recommendations}


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Token Optimizer — Waste detection and optimization")
    parser.add_argument('--detect-waste', action='store_true', help='Detect wasteful usage patterns')
    parser.add_argument('--recommendations', action='store_true', help='Generate optimization recommendations')
    parser.add_argument('--days', type=int, default=7, help='Number of days to analyze (default: 7)')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='Output format')
    
    args = parser.parse_args()
    
    if args.detect_waste:
        detector = WasteDetector(config)
        results = detector.detect_all(days=args.days)
        
        if args.format == 'json':
            print(json.dumps(results, indent=2))
        else:
            print("\n" + "=" * 60)
            print("WASTE DETECTION REPORT".center(60))
            print("=" * 60 + "\n")
            print(f"Period: {results['period']}")
            print(f"Total records analyzed: {results['total_records']:,}")
            print(f"Total waste detected: ${results['total_waste_cost']:.2f}\n")
            
            if results['waste_detected']:
                print("Waste Detected:\n")
                for waste in results['waste_detected']:
                    print(f"  • {waste['description']}")
                    print(f"    Estimated waste: ${waste['waste_cost']:.2f}\n")
            
            if results['recommendations']:
                print("Recommendations:\n")
                for rec in results['recommendations']:
                    print(f"  → {rec}")
                print()
    
    elif args.recommendations:
        optimizer = Optimizer(config)
        results = optimizer.generate_recommendations(days=args.days)
        
        if args.format == 'json':
            print(json.dumps(results, indent=2))
        else:
            print("\n" + "=" * 60)
            print("OPTIMIZATION RECOMMENDATIONS".center(60))
            print("=" * 60 + "\n")
            print(f"Period: {results['period']}")
            print(f"Total cost: ${results['total_cost']:.2f}")
            print(f"Potential savings: ${results['potential_savings']:.2f} ({results['savings_percent']:.1f}%)\n")
            
            for opp in results['optimization_opportunities']:
                print(f"{opp['category']}:")
                for rec in opp['recommendations']:
                    print(f"  → {rec}")
                print()
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
