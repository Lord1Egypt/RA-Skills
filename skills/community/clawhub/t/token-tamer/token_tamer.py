#!/usr/bin/env python3
"""
Token Tamer — AI API Cost Control
Monitor, budget, and optimize AI API spending across ANY provider.

Author: Shadow Rose
License: MIT
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

# Import config
try:
    import token_config as config
except ImportError:
    print("ERROR: token_config.py not found. Copy config_example.py to token_config.py and configure it.")
    sys.exit(1)


class UsageRecord:
    """Represents a single API usage event."""
    
    def __init__(self, provider: str, model: str, input_tokens: int, output_tokens: int,
                 cost: float, task: Optional[str] = None, session: Optional[str] = None,
                 metadata: Optional[Dict] = None):
        self.timestamp = datetime.now()
        self.provider = provider
        self.model = model
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.total_tokens = input_tokens + output_tokens
        self.cost = cost
        self.task = task or "unknown"
        self.session = session or "unknown"
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'timestamp': self.timestamp.isoformat(),
            'provider': self.provider,
            'model': self.model,
            'input_tokens': self.input_tokens,
            'output_tokens': self.output_tokens,
            'total_tokens': self.total_tokens,
            'cost': self.cost,
            'task': self.task,
            'session': self.session,
            'metadata': self.metadata
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'UsageRecord':
        """Create from dictionary."""
        record = UsageRecord(
            provider=data['provider'],
            model=data['model'],
            input_tokens=data['input_tokens'],
            output_tokens=data['output_tokens'],
            cost=data['cost'],
            task=data.get('task'),
            session=data.get('session'),
            metadata=data.get('metadata', {})
        )
        record.timestamp = datetime.fromisoformat(data['timestamp'])
        return record


class CostCalculator:
    """Calculate costs based on provider and model pricing."""
    
    def __init__(self, config_obj):
        self.config = config_obj
        self.pricing = getattr(config_obj, 'MODEL_PRICING', {})
    
    def calculate_cost(self, provider: str, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for a usage event."""
        # Look up pricing
        key = f"{provider}/{model}"
        if key not in self.pricing:
            # Try provider wildcard
            key = f"{provider}/*"
        
        if key not in self.pricing:
            # Unknown model, return 0 and warn
            print(f"Warning: No pricing data for {provider}/{model}", file=sys.stderr)
            return 0.0
        
        pricing = self.pricing[key]
        
        # Calculate cost (pricing is per million tokens)
        input_cost = (input_tokens / 1_000_000) * pricing['input']
        output_cost = (output_tokens / 1_000_000) * pricing['output']
        
        return input_cost + output_cost


class BudgetTracker:
    """Track spending against budgets."""
    
    def __init__(self, config_obj):
        self.config = config_obj
        self.budgets = getattr(config_obj, 'BUDGETS', {})
        self.alert_thresholds = getattr(config_obj, 'ALERT_THRESHOLDS', {})
    
    def check_budget(self, period: str, current_spend: float) -> Tuple[str, Optional[str]]:
        """Check if spending is within budget."""
        if period not in self.budgets:
            return 'OK', None
        
        budget = self.budgets[period]
        percent = (current_spend / budget) * 100 if budget > 0 else 0
        
        # Check thresholds
        if percent >= 100:
            return 'KILL', f"Budget exceeded: ${current_spend:.2f} / ${budget:.2f} ({percent:.1f}%)"
        elif percent >= self.alert_thresholds.get('critical', 95):
            return 'CRITICAL', f"Budget critical: ${current_spend:.2f} / ${budget:.2f} ({percent:.1f}%)"
        elif percent >= self.alert_thresholds.get('warning', 80):
            return 'WARNING', f"Budget warning: ${current_spend:.2f} / ${budget:.2f} ({percent:.1f}%)"
        else:
            return 'OK', None
    
    def should_throttle(self, period: str, current_spend: float) -> bool:
        """Determine if API calls should be throttled."""
        status, _ = self.check_budget(period, current_spend)
        return status in ['CRITICAL', 'KILL']
    
    def should_kill(self, period: str, current_spend: float) -> bool:
        """Determine if API calls should be completely blocked."""
        status, _ = self.check_budget(period, current_spend)
        return status == 'KILL'


class UsageStore:
    """Persistent storage for usage records."""
    
    def __init__(self, storage_file: Path):
        self.storage_file = storage_file
        self.records: List[UsageRecord] = []
        self.load()
    
    def load(self):
        """Load records from disk."""
        if self.storage_file.exists():
            try:
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                self.records = [UsageRecord.from_dict(r) for r in data.get('records', [])]
            except Exception as e:
                print(f"Error loading usage data: {e}", file=sys.stderr)
                self.records = []
    
    def save(self):
        """Save records to disk."""
        try:
            self.storage_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.storage_file, 'w') as f:
                data = {
                    'last_updated': datetime.now().isoformat(),
                    'records': [r.to_dict() for r in self.records]
                }
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving usage data: {e}", file=sys.stderr)
    
    def add_record(self, record: UsageRecord):
        """Add a usage record."""
        self.records.append(record)
        self.save()
    
    def get_records(self, start_date: Optional[datetime] = None, 
                   end_date: Optional[datetime] = None,
                   provider: Optional[str] = None,
                   task: Optional[str] = None) -> List[UsageRecord]:
        """Query records with filters."""
        filtered = self.records
        
        if start_date:
            filtered = [r for r in filtered if r.timestamp >= start_date]
        
        if end_date:
            filtered = [r for r in filtered if r.timestamp <= end_date]
        
        if provider:
            filtered = [r for r in filtered if r.provider == provider]
        
        if task:
            filtered = [r for r in filtered if r.task == task]
        
        return filtered
    
    def get_total_cost(self, start_date: Optional[datetime] = None,
                      end_date: Optional[datetime] = None,
                      provider: Optional[str] = None) -> float:
        """Get total cost for period."""
        records = self.get_records(start_date, end_date, provider)
        return sum(r.cost for r in records)


class TokenTamer:
    """Main cost tracking and budget engine."""
    
    def __init__(self, config_obj):
        self.config = config_obj
        self.storage = UsageStore(Path(config_obj.USAGE_FILE))
        self.calculator = CostCalculator(config_obj)
        self.budget_tracker = BudgetTracker(config_obj)
        self.kill_switch_active = False
    
    def log_usage(self, provider: str, model: str, input_tokens: int, output_tokens: int,
                  task: Optional[str] = None, session: Optional[str] = None,
                  metadata: Optional[Dict] = None) -> Tuple[float, str]:
        """Log API usage and return cost + status."""
        
        # Calculate cost
        cost = self.calculator.calculate_cost(provider, model, input_tokens, output_tokens)
        
        # Create record
        record = UsageRecord(provider, model, input_tokens, output_tokens, cost, task, session, metadata)
        
        # Check budget before logging
        daily_cost = self.get_daily_cost()
        status, message = self.budget_tracker.check_budget('daily', daily_cost + cost)
        
        # Check kill switch
        if self.budget_tracker.should_kill('daily', daily_cost + cost):
            self.kill_switch_active = True
            print(f"🚨 KILL SWITCH ACTIVATED: {message}", file=sys.stderr)
            return cost, 'KILL'
        
        # Log the record
        self.storage.add_record(record)
        
        # Check throttle
        if self.budget_tracker.should_throttle('daily', daily_cost + cost):
            print(f"⚠️  THROTTLE WARNING: {message}", file=sys.stderr)
            return cost, 'THROTTLE'
        
        if message:
            print(f"💰 Budget status: {message}", file=sys.stderr)
        
        return cost, status
    
    def get_daily_cost(self) -> float:
        """Get today's total cost."""
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return self.storage.get_total_cost(start_date=today_start)
    
    def get_weekly_cost(self) -> float:
        """Get this week's total cost."""
        now = datetime.now()
        week_start = now - timedelta(days=now.weekday())
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        return self.storage.get_total_cost(start_date=week_start)
    
    def get_monthly_cost(self) -> float:
        """Get this month's total cost."""
        now = datetime.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return self.storage.get_total_cost(start_date=month_start)
    
    def get_status(self) -> Dict:
        """Get current cost status."""
        daily = self.get_daily_cost()
        weekly = self.get_weekly_cost()
        monthly = self.get_monthly_cost()
        
        daily_status, daily_msg = self.budget_tracker.check_budget('daily', daily)
        weekly_status, weekly_msg = self.budget_tracker.check_budget('weekly', weekly)
        monthly_status, monthly_msg = self.budget_tracker.check_budget('monthly', monthly)
        
        return {
            'daily': {
                'cost': daily,
                'budget': self.budget_tracker.budgets.get('daily', 0),
                'status': daily_status,
                'message': daily_msg
            },
            'weekly': {
                'cost': weekly,
                'budget': self.budget_tracker.budgets.get('weekly', 0),
                'status': weekly_status,
                'message': weekly_msg
            },
            'monthly': {
                'cost': monthly,
                'budget': self.budget_tracker.budgets.get('monthly', 0),
                'status': monthly_status,
                'message': monthly_msg
            },
            'kill_switch': self.kill_switch_active
        }
    
    def check_before_call(self, estimated_cost: float = 0.10) -> bool:
        """Check if API call should proceed (return True = OK, False = blocked)."""
        if self.kill_switch_active:
            print("🚨 KILL SWITCH ACTIVE: API calls blocked", file=sys.stderr)
            return False
        
        daily = self.get_daily_cost()
        
        if self.budget_tracker.should_kill('daily', daily + estimated_cost):
            self.kill_switch_active = True
            print("🚨 KILL SWITCH ACTIVATED: Budget exceeded", file=sys.stderr)
            return False
        
        return True


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Token Tamer — AI API Cost Control")
    parser.add_argument('--log', action='store_true', help='Log a usage event')
    parser.add_argument('--provider', type=str, help='Provider name (e.g., openai, anthropic)')
    parser.add_argument('--model', type=str, help='Model name')
    parser.add_argument('--input-tokens', type=int, help='Input tokens')
    parser.add_argument('--output-tokens', type=int, help='Output tokens')
    parser.add_argument('--task', type=str, help='Task name')
    parser.add_argument('--session', type=str, help='Session ID')
    parser.add_argument('--status', action='store_true', help='Show current cost status')
    parser.add_argument('--check', action='store_true', help='Check if API call should proceed')
    
    args = parser.parse_args()
    
    tamer = TokenTamer(config)
    
    if args.status:
        status = tamer.get_status()
        print("\n=== Token Tamer Status ===\n")
        print(f"Daily:   ${status['daily']['cost']:8.2f} / ${status['daily']['budget']:8.2f}  [{status['daily']['status']}]")
        if status['daily']['message']:
            print(f"         {status['daily']['message']}")
        print(f"Weekly:  ${status['weekly']['cost']:8.2f} / ${status['weekly']['budget']:8.2f}  [{status['weekly']['status']}]")
        if status['weekly']['message']:
            print(f"         {status['weekly']['message']}")
        print(f"Monthly: ${status['monthly']['cost']:8.2f} / ${status['monthly']['budget']:8.2f}  [{status['monthly']['status']}]")
        if status['monthly']['message']:
            print(f"         {status['monthly']['message']}")
        print(f"\nKill switch: {'🚨 ACTIVE' if status['kill_switch'] else '✓ OK'}")
    
    elif args.check:
        can_proceed = tamer.check_before_call()
        if can_proceed:
            print("✓ OK: API call can proceed")
            sys.exit(0)
        else:
            print("✗ BLOCKED: Kill switch active or budget exceeded")
            sys.exit(1)
    
    elif args.log:
        if not all([args.provider, args.model, args.input_tokens is not None, args.output_tokens is not None]):
            print("ERROR: --log requires --provider, --model, --input-tokens, --output-tokens")
            sys.exit(1)
        
        cost, status = tamer.log_usage(
            provider=args.provider,
            model=args.model,
            input_tokens=args.input_tokens,
            output_tokens=args.output_tokens,
            task=args.task,
            session=args.session
        )
        
        print(f"✓ Logged: ${cost:.4f} [{status}]")
        
        if status == 'KILL':
            sys.exit(1)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
