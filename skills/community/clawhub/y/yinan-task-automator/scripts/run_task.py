#!/usr/bin/env python3
"""
Task Runner - Execute automated tasks

Usage:
    python run_task.py --task file_organizer --config tasks/organize.json
"""

import argparse
import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

class TaskRunner:
    def __init__(self, task_name, config_path, dry_run=False, verbose=False):
        self.task_name = task_name
        self.config_path = config_path
        self.dry_run = dry_run
        self.verbose = verbose
        self.logs = []
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.logs.append(log_entry)
        if self.verbose or level in ["ERROR", "WARNING"]:
            print(log_entry)
    
    def load_config(self):
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def run(self):
        self.log(f"Starting task: {self.task_name}")
        
        if self.dry_run:
            self.log("DRY RUN MODE - No changes will be made", "WARNING")
        
        config = self.load_config()
        
        # Route to appropriate task handler
        if self.task_name == "file_organizer":
            return self.task_file_organizer(config)
        elif self.task_name == "data_converter":
            return self.task_data_converter(config)
        elif self.task_name == "api_sync":
            return self.task_api_sync(config)
        elif self.task_name == "web_monitor":
            return self.task_web_monitor(config)
        elif self.task_name == "order_processor":
            return self.task_order_processor(config)
        else:
            self.log(f"Unknown task: {self.task_name}", "ERROR")
            return {"status": "error", "message": f"Unknown task: {self.task_name}"}
    
    def task_file_organizer(self, config):
        """Organize files by rules."""
        source = Path(config.get('source', '~/Downloads')).expanduser()
        destination = Path(config.get('destination', '~/Organized')).expanduser()
        rules = config.get('rules', [])
        
        self.log(f"Source: {source}")
        self.log(f"Destination: {destination}")
        self.log(f"Rules: {len(rules)}")
        
        if not source.exists():
            self.log(f"Source directory does not exist: {source}", "ERROR")
            return {"status": "error", "message": "Source not found"}
        
        if not self.dry_run:
            destination.mkdir(parents=True, exist_ok=True)
        
        organized_count = 0
        
        for file in source.iterdir():
            if file.is_file():
                ext = file.suffix.lower()
                target_folder = None
                
                for rule in rules:
                    if rule.get('extension', '').lower() == ext:
                        target_folder = rule.get('folder', 'Other')
                        break
                
                if target_folder is None:
                    target_folder = 'Other'
                
                target_path = destination / target_folder
                
                if self.dry_run:
                    self.log(f"Would move: {file.name} -> {target_folder}/")
                else:
                    target_path.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(file), str(target_path / file.name))
                    self.log(f"Moved: {file.name} -> {target_folder}/")
                
                organized_count += 1
        
        self.log(f"Organized {organized_count} files")
        return {"status": "success", "organized": organized_count}
    
    def task_data_converter(self, config):
        """Convert data between formats."""
        import csv
        
        input_path = Path(config.get('input', '')).expanduser()
        output_path = Path(config.get('output', '')).expanduser()
        output_format = config.get('format', 'json')
        
        self.log(f"Input: {input_path}")
        self.log(f"Output: {output_path} ({output_format})")
        
        if not input_path.exists():
            self.log(f"Input file not found: {input_path}", "ERROR")
            return {"status": "error", "message": "Input not found"}
        
        # Read input
        data = []
        if input_path.suffix == '.csv':
            with open(input_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)
        elif input_path.suffix == '.json':
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            self.log(f"Unsupported input format: {input_path.suffix}", "ERROR")
            return {"status": "error", "message": "Unsupported format"}
        
        self.log(f"Read {len(data)} records")
        
        # Write output
        if self.dry_run:
            self.log(f"Would write {len(data)} records to {output_path}")
        else:
            if output_format == 'json':
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            elif output_format == 'csv':
                if data:
                    with open(output_path, 'w', encoding='utf-8', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=data[0].keys())
                        writer.writeheader()
                        writer.writerows(data)
            self.log(f"Wrote {len(data)} records to {output_path}")
        
        return {"status": "success", "records": len(data)}
    
    def task_api_sync(self, config):
        """Sync data between APIs."""
        self.log("API sync task - requires API configuration")
        # Placeholder - would need actual API implementations
        return {"status": "success", "message": "API sync placeholder"}
    
    def task_web_monitor(self, config):
        """Monitor websites for changes."""
        self.log("Web monitor task - requires browser automation")
        # Placeholder - would use agent-browser
        return {"status": "success", "message": "Web monitor placeholder"}
    
    def task_order_processor(self, config):
        """Process e-commerce orders."""
        stores = config.get('stores', [])
        actions = config.get('actions', [])
        
        self.log(f"Processing orders for stores: {stores}")
        self.log(f"Actions: {actions}")
        
        # Placeholder for e-commerce integration
        return {"status": "success", "message": "Order processor placeholder"}

def main():
    parser = argparse.ArgumentParser(description='Run automated tasks')
    parser.add_argument('--task', required=True, help='Task name to run')
    parser.add_argument('--config', required=True, help='Configuration file path')
    parser.add_argument('--dry-run', action='store_true', help='Simulate without executing')
    parser.add_argument('--verbose', action='store_true', help='Verbose logging')
    args = parser.parse_args()
    
    runner = TaskRunner(args.task, args.config, args.dry_run, args.verbose)
    result = runner.run()
    
    # Save logs
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"{args.task}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(runner.logs))
    
    print(f"\nLogs saved to: {log_file}")
    print(f"Result: {json.dumps(result, indent=2)}")
    
    return 0 if result.get('status') == 'success' else 1

if __name__ == '__main__':
    sys.exit(main())
