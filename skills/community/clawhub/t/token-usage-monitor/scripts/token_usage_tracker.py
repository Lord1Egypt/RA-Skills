#!/usr/bin/env python3
"""
Token Usage Monitor - Track and analyze AI model token consumption
"""

import json
import time
import argparse
import datetime
from typing import Dict, List, Optional

class TokenUsageTracker:
    def __init__(self, data_file: str = "~/.openclaw/token_usage.json"):
        self.data_file = data_file
        self.usage_data = self._load_data()
        
    def _load_data(self) -> Dict:
        """Load token usage data from file"""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "sessions": {},
                "daily_totals": {},
                "thresholds": {},
                "model_pricing": {
                    "gpt-4": 0.03 / 1000,  # $0.03 per 1000 prompt tokens
                    "gpt-3.5-turbo": 0.0015 / 1000,  # $0.0015 per 1000 tokens
                    "claude-2": 0.0110 / 1000,  # $0.0110 per 1000 prompt tokens
                    "doubao-seed": 0.002 / 1000  # Example pricing for Doubao
                }
            }
    
    def _save_data(self):
        """Save token usage data to file"""
        import os
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.usage_data, f, indent=2)
    
    def track_usage(self, session_id: str, model: str, prompt_tokens: int, completion_tokens: int):
        """Track token usage for a session"""
        timestamp = datetime.datetime.now().isoformat()
        total_tokens = prompt_tokens + completion_tokens
        
        # Update session data
        if session_id not in self.usage_data["sessions"]:
            self.usage_data["sessions"][session_id] = []
        
        self.usage_data["sessions"][session_id].append({
            "timestamp": timestamp,
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens
        })
        
        # Update daily totals
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        if date_str not in self.usage_data["daily_totals"]:
            self.usage_data["daily_totals"][date_str] = {}
            
        if model not in self.usage_data["daily_totals"][date_str]:
            self.usage_data["daily_totals"][date_str][model] = {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }
            
        self.usage_data["daily_totals"][date_str][model]["prompt_tokens"] += prompt_tokens
        self.usage_data["daily_totals"][date_str][model]["completion_tokens"] += completion_tokens
        self.usage_data["daily_totals"][date_str][model]["total_tokens"] += total_tokens
        
        self._save_data()
        self._check_thresholds(model, total_tokens)
    
    def _check_thresholds(self, model: str, tokens_used: int):
        """Check if usage exceeds thresholds"""
        if model in self.usage_data["thresholds"]:
            threshold = self.usage_data["thresholds"][model]
            date_str = datetime.datetime.now().strftime("%Y-%m-%d")
            
            if date_str in self.usage_data["daily_totals"] and model in self.usage_data["daily_totals"][date_str]:
                daily_total = self.usage_data["daily_totals"][date_str][model]["total_tokens"]
                
                if daily_total >= threshold["limit"] and not threshold.get("alert_sent", False):
                    print(f"⚠️ ALERT: {model} usage ({daily_total} tokens) exceeds daily threshold of {threshold['limit']} tokens!")
                    threshold["alert_sent"] = True
                    self._save_data()
    
    def get_session_usage(self, session_id: Optional[str] = None) -> Dict:
        """Get token usage for a specific session or all sessions"""
        if session_id:
            return {session_id: self.usage_data["sessions"].get(session_id, [])}
        return self.usage_data["sessions"]
    
    def get_daily_report(self, date_str: Optional[str] = None) -> Dict:
        """Get daily usage report"""
        if not date_str:
            date_str = datetime.datetime.now().strftime("%Y-%m-%d")
            
        report = self.usage_data["daily_totals"].get(date_str, {})
        
        # Calculate costs
        for model, usage in report.items():
            pricing = self.usage_data["model_pricing"].get(model, 0.002 / 1000)
            cost = usage["total_tokens"] * pricing
            usage["estimated_cost"] = round(cost, 4)
            
        return {date_str: report}
    
    def set_threshold(self, model: str, limit: int, period: str = "day"):
        """Set usage threshold for a model"""
        self.usage_data["thresholds"][model] = {
            "limit": limit,
            "period": period,
            "alert_sent": False
        }
        self._save_data()
    
    def get_usage_summary(self) -> Dict:
        """Get overall usage summary"""
        total_tokens = 0
        total_cost = 0.0
        model_breakdown = {}
        
        # Calculate totals from daily data
        for date, models in self.usage_data["daily_totals"].items():
            for model, usage in models.items():
                if model not in model_breakdown:
                    model_breakdown[model] = {
                        "total_tokens": 0,
                        "estimated_cost": 0.0
                    }
                    
                model_breakdown[model]["total_tokens"] += usage["total_tokens"]
                pricing = self.usage_data["model_pricing"].get(model, 0.002 / 1000)
                cost = usage["total_tokens"] * pricing
                model_breakdown[model]["estimated_cost"] += cost
                
                total_tokens += usage["total_tokens"]
                total_cost += cost
        
        return {
            "total_tokens": total_tokens,
            "estimated_total_cost": round(total_cost, 4),
            "model_breakdown": model_breakdown,
            "days_tracked": len(self.usage_data["daily_totals"])
        }

def main():
    parser = argparse.ArgumentParser(description="Token Usage Monitor")
    parser.add_argument("--track", action="store_true", help="Track token usage")
    parser.add_argument("--session", action="store_true", help="Show current session usage")
    parser.add_argument("--report", action="store_true", help="Generate usage report")
    parser.add_argument("--period", choices=["day", "week", "month"], default="day", help="Report period")
    parser.add_argument("--set-threshold", action="store_true", help="Set usage threshold")
    parser.add_argument("--model", help="Model name (required for --track and --set-threshold)")
    parser.add_argument("--prompt-tokens", type=int, help="Prompt tokens used (required for --track)")
    parser.add_argument("--completion-tokens", type=int, help="Completion tokens used (required for --track)")
    parser.add_argument("--limit", type=int, help="Threshold limit (required for --set-threshold)")
    parser.add_argument("--summary", action="store_true", help="Show overall usage summary")
    
    args = parser.parse_args()
    
    tracker = TokenUsageTracker()
    
    if args.track:
        if not all([args.model, args.prompt_tokens, args.completion_tokens]):
            parser.error("--track requires --model, --prompt-tokens, and --completion-tokens")
        
        # Generate session ID (simplified for example)
        session_id = f"session_{int(time.time())}"
        tracker.track_usage(session_id, args.model, args.prompt_tokens, args.completion_tokens)
        print(f"✅ Tracked usage: {args.prompt_tokens} prompt tokens, {args.completion_tokens} completion tokens for {args.model}")
        
    elif args.session:
        usage = tracker.get_session_usage()
        print("\n📊 Session Usage:")
        for session_id, entries in usage.items():
            if entries:
                total = sum(entry["total_tokens"] for entry in entries)
                print(f"  {session_id}: {total} tokens total")
                for entry in entries[-3:]:  # Show last 3 entries
                    timestamp = datetime.datetime.fromisoformat(entry["timestamp"]).strftime("%H:%M:%S")
                    print(f"    {timestamp}: {entry['total_tokens']} tokens ({entry['model']})")
                    
    elif args.report:
        if args.period == "day":
            report = tracker.get_daily_report()
            date = list(report.keys())[0]
            print(f"\n📅 Daily Usage Report for {date}:")
            for model, usage in report[date].items():
                print(f"  {model}:")
                print(f"    Prompt tokens: {usage['prompt_tokens']}")
                print(f"    Completion tokens: {usage['completion_tokens']}")
                print(f"    Total tokens: {usage['total_tokens']}")
                if 'estimated_cost' in usage:
                    print(f"    Estimated cost: ${usage['estimated_cost']:.4f}")
                    
    elif args.set_threshold:
        if not all([args.model, args.limit]):
            parser.error("--set-threshold requires --model and --limit")
        
        tracker.set_threshold(args.model, args.limit)
        print(f"✅ Set threshold of {args.limit} tokens/day for {args.model}")
        
    elif args.summary:
        summary = tracker.get_usage_summary()
        print("\n📈 Overall Usage Summary:")
        print(f"  Total tokens used: {summary['total_tokens']}")
        print(f"  Estimated total cost: ${summary['estimated_total_cost']:.4f}")
        print(f"  Days tracked: {summary['days_tracked']}")
        print("\n  Model Breakdown:")
        for model, data in summary['model_breakdown'].items():
            print(f"    {model}: {data['total_tokens']} tokens (${data['estimated_cost']:.4f})")
            
    else:
        parser.print_help()

if __name__ == "__main__":
    main()