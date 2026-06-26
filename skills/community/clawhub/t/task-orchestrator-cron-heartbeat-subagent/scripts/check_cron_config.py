#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cron Task Configuration Check Tool

Checks if scheduled tasks have correctly configured agentId and accountId
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

def load_json_file(file_path: Path) -> Optional[Dict]:
    """Load JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to read file: {e}")
        return None

def get_agent_bindings(config: Dict) -> Dict[str, str]:
    """Get all agent channel bindings"""
    bindings = {}
    for binding in config.get('bindings', []):
        agent_id = binding.get('agentId')
        match = binding.get('match', {})
        account_id = match.get('accountId')
        if agent_id and account_id:
            bindings[agent_id] = account_id
    return bindings

def check_cron_jobs(cron_config: Dict, bindings: Dict[str, str]) -> List[Dict]:
    """Check scheduled task configuration"""
    issues = []
    
    for job in cron_config.get('jobs', []):
        job_id = job.get('id', 'unknown')
        job_name = job.get('name', 'unknown')
        agent_id = job.get('agentId')
        session_target = job.get('sessionTarget')
        delivery = job.get('delivery', {})
        account_id = delivery.get('accountId')
        channel = delivery.get('channel')
        
        job_issues = {
            'job_id': job_id,
            'job_name': job_name,
            'issues': []
        }
        
        # Check agentId
        if not agent_id:
            job_issues['issues'].append({
                'type': 'missing_agent_id',
                'severity': 'error',
                'message': 'No agentId configured (defaults to main execution)',
                'fix': f'Add --agentId "main" or specify other agent'
            })
        
        # Check sessionTarget
        if session_target == 'isolated':
            job_issues['issues'].append({
                'type': 'isolated_session',
                'severity': 'warning',
                'message': 'Using isolated session (doesn\'t inherit channel binding)',
                'fix': f'Consider using --session "{agent_id or "main"}"'
            })
        
        # Check accountId
        if not account_id:
            job_issues['issues'].append({
                'type': 'missing_account_id',
                'severity': 'error',
                'message': 'No accountId configured (defaults to default)',
                'fix': f'Add --accountId "default" or specify other account'
            })
        
        # Check agentId and accountId consistency
        if agent_id and agent_id in bindings:
            expected_account = bindings[agent_id]
            if account_id and account_id != expected_account:
                job_issues['issues'].append({
                    'type': 'account_mismatch',
                    'severity': 'warning',
                    'message': f'accountId doesn\'t match agent binding',
                    'details': {
                        'expected': expected_account,
                        'actual': account_id
                    },
                    'fix': f'Use --accountId "{expected_account}"'
                })
        
        if job_issues['issues']:
            issues.append(job_issues)
    
    return issues

def print_report(bindings: Dict[str, str], issues: List[Dict]):
    """Print check report"""
    print("=" * 70)
    print("📋 Cron Task Configuration Check Report")
    print("=" * 70)
    print()
    
    # Print agent bindings
    print("=== Agent Channel Bindings ===")
    if bindings:
        for agent_id, account_id in sorted(bindings.items()):
            print(f"  ✅ {agent_id}: {account_id}")
    else:
        print("  ⚠️ No agent bindings found")
    print()
    
    # Print issues
    print("=== Scheduled Task Configuration Check ===")
    if not issues:
        print("  ✅ All tasks configured correctly")
    else:
        for job in issues:
            print(f"\n  Task: {job['job_name']}")
            print(f"    ID: {job['job_id']}")
            
            for issue in job['issues']:
                severity = issue['severity']
                icon = "❌" if severity == 'error' else "⚠️"
                print(f"    {icon} [{severity.upper()}] {issue['message']}")
                if 'details' in issue:
                    for key, value in issue['details'].items():
                        print(f"       {key}: {value}")
                print(f"       Fix: {issue['fix']}")
    
    print()
    print("=" * 70)
    
    # Statistics
    error_count = sum(
        1 for job in issues 
        for issue in job['issues'] 
        if issue['severity'] == 'error'
    )
    warning_count = sum(
        1 for job in issues 
        for issue in job['issues'] 
        if issue['severity'] == 'warning'
    )
    
    print(f"Total: {error_count} errors, {warning_count} warnings")
    print("=" * 70)

def main():
    """Main function"""
    # Determine config paths
    home = Path.home()
    openclaw_dir = home / '.openclaw'
    
    config_file = openclaw_dir / 'openclaw.json'
    cron_file = openclaw_dir / 'cron' / 'jobs.json'
    
    # Check if files exist
    if not config_file.exists():
        print(f"❌ Config file not found: {config_file}")
        sys.exit(1)
    
    if not cron_file.exists():
        print(f"❌ Cron task file not found: {cron_file}")
        sys.exit(1)
    
    # Load config
    print("Loading configuration files...")
    config = load_json_file(config_file)
    cron_config = load_json_file(cron_file)
    
    if not config or not cron_config:
        sys.exit(1)
    
    # Get agent bindings
    bindings = get_agent_bindings(config)
    
    # Check scheduled tasks
    issues = check_cron_jobs(cron_config, bindings)
    
    # Print report
    print_report(bindings, issues)
    
    # Return exit code
    if any(
        issue['severity'] == 'error' 
        for job in issues 
        for issue in job['issues']
    ):
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()
