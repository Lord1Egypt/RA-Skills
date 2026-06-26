#!/usr/bin/env python3
"""
Jira Work Log Tools
Simple Python scripts for managing Jira work logs
"""

#!/usr/bin/env python3
"""
Jira Work Log Tools
Simple Python scripts for managing Jira work logs
"""

import json
import os
import sys
from datetime import datetime, timedelta
import requests
from requests.auth import HTTPBasicAuth
import argparse
import readline  # For better input experience

class JiraClient:
    def __init__(self, config_file="jira_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        # Handle both password and api_token fields for compatibility
        password = self.config.get('password') or self.config.get('api_token')
        if not password:
            print("❌ Error: No 'password' or 'api_token' field found in config")
            sys.exit(1)
        self.auth = HTTPBasicAuth(self.config['username'], password)
        self.base_url = self.config['jira_url']
        self.api_version = '2'  # Default to v2
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def load_config(self):
        """Load configuration from JSON file"""
        if not os.path.exists(self.config_file):
            print(f"❌ Config file {self.config_file} not found!")
            print(f"   Please copy jira_config.example.json to {self.config_file} and add your credentials")
            sys.exit(1)
        
        with open(self.config_file, 'r') as f:
            return json.load(f)
    
    def test_connection(self):
        """Test connection to Jira"""
        # Try API v2 first (older Jira versions), then v3
        api_versions = ['2', '3']
        
        for api_version in api_versions:
            try:
                response = requests.get(
                    f"{self.base_url}/rest/api/{api_version}/myself",
                    auth=self.auth,
                    headers=self.headers
                )
                if response.status_code == 200:
                    user_data = response.json()
                    print(f"✅ Connected to Jira v{api_version} as: {user_data.get('displayName', 'Unknown')}")
                    print(f"   Email: {user_data.get('emailAddress', 'Unknown')}")
                    print(f"   Username: {user_data.get('name', 'Unknown')}")
                    self.api_version = api_version  # Store for other calls
                    return True
                elif response.status_code == 404:
                    print(f"   API v{api_version} not found, trying next...")
                    continue
                else:
                    print(f"❌ Connection failed: {response.status_code}")
                    print(f"   Response: {response.text[:200]}")
                    return False
            except Exception as e:
                print(f"❌ Connection error with v{api_version}: {e}")
                continue
        
        print("❌ Could not connect to any known Jira API version")
        return False
    
    def search_issues(self, jql="assignee = currentUser() AND status != Done ORDER BY updated DESC"):
        """Search for issues using JQL"""
        try:
            response = requests.post(
                f"{self.base_url}/rest/api/{self.api_version}/search",
                auth=self.auth,
                headers=self.headers,
                json={
                    'jql': jql,
                    'maxResults': 50,
                    'fields': ['key', 'summary', 'status', 'project']
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                issues = data.get('issues', [])
                print(f"\n📋 Found {len(issues)} issues:")
                for i, issue in enumerate(issues, 1):
                    key = issue['key']
                    summary = issue['fields']['summary'][:60]
                    status = issue['fields']['status']['name']
                    print(f"{i:2}. {key}: {summary}... [{status}]")
                return issues
            else:
                print(f"❌ Search failed: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return []
        except Exception as e:
            print(f"❌ Search error: {e}")
            return []
    
    def log_work(self, issue_key, time_spent, comment=None, started=None):
        """Log work to a Jira issue"""
        if started is None:
            started = datetime.now().isoformat()[:-13] + ".000+0000"
        
        # Different payload for API v2 vs v3
        if self.api_version == '3':
            payload = {
                "timeSpent": time_spent,
                "started": started,
                "comment": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": comment or "Work logged via Jira Tools"
                                }
                            ]
                        }
                    ]
                }
            }
        else:
            # API v2 uses simpler format
            payload = {
                "timeSpent": time_spent,
                "started": started,
                "comment": comment or "Work logged via Jira Tools"
            }
        
        try:
            response = requests.post(
                f"{self.base_url}/rest/api/{self.api_version}/issue/{issue_key}/worklog",
                auth=self.auth,
                headers=self.headers,
                json=payload
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ Work logged successfully to {issue_key}")
                print(f"   Time: {time_spent}")
                if comment:
                    print(f"   Comment: {comment}")
                return True
            else:
                print(f"❌ Failed to log work: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return False
        except Exception as e:
            print(f"❌ Error logging work: {e}")
            return False
    
    def get_issue_details(self, issue_key):
        """Get details for a specific issue"""
        try:
            response = requests.get(
                f"{self.base_url}/rest/api/{self.api_version}/issue/{issue_key}",
                auth=self.auth,
                headers=self.headers,
                params={'fields': 'summary,status,project'}
            )
            
            if response.status_code == 200:
                issue = response.json()
                summary = issue['fields']['summary']
                status = issue['fields']['status']['name']
                project = issue['fields']['project']['name']
                print(f"\n📄 Issue: {issue_key}")
                print(f"   Project: {project}")
                print(f"   Status: {status}")
                print(f"   Summary: {summary}")
                return issue
            else:
                print(f"❌ Failed to get issue: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return None
        except Exception as e:
            print(f"❌ Error getting issue: {e}")
            return None
    
    def quick_log(self):
        """Interactive quick log function"""
        print("\n🚀 Quick Work Log")
        print("=" * 40)
        
        # Show recent issues
        issues = self.search_issues("assignee = currentUser() AND updated >= -7d ORDER BY updated DESC")
        
        if not issues:
            print("No recent issues found. Please enter an issue key manually.")
            issue_key = input("Issue key (e.g., PROJ-123): ").strip()
        else:
            choice = input("\nSelect issue number or enter custom key: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(issues):
                issue_key = issues[int(choice) - 1]['key']
            else:
                issue_key = choice
        
        # Get issue details
        self.get_issue_details(issue_key)
        
        # Get time spent
        print("\n⏱️  Time Entry Examples:")
        print("   - 1h 30m")
        print("   - 45m")
        print("   - 2h")
        print("   - 30m")
        
        time_spent = input("\nTime spent (e.g., 1h 30m): ").strip()
        
        # Get comment
        comment = input("Comment (optional, press Enter to skip): ").strip()
        if not comment:
            comment = None
        
        # Confirm and log
        print(f"\n📝 Summary:")
        print(f"   Issue: {issue_key}")
        print(f"   Time: {time_spent}")
        if comment:
            print(f"   Comment: {comment}")
        
        confirm = input("\nLog this work? (y/N): ").strip().lower()
        if confirm == 'y':
            return self.log_work(issue_key, time_spent, comment)
        else:
            print("❌ Cancelled")
            return False

def main():
    parser = argparse.ArgumentParser(description="Jira Work Log Tools")
    parser.add_argument('command', nargs='?', default='quick', 
                       choices=['test', 'list', 'log', 'quick'],
                       help='Command to run')
    parser.add_argument('--issue', help='Issue key (for log command)')
    parser.add_argument('--time', help='Time spent (for log command)')
    parser.add_argument('--comment', help='Comment (for log command)')
    
    args = parser.parse_args()
    
    jira = JiraClient()
    
    if args.command == 'test':
        jira.test_connection()
    
    elif args.command == 'list':
        jql = input("Enter JQL query (press Enter for default): ").strip()
        if not jql:
            jql = "assignee = currentUser() AND status != Done ORDER BY updated DESC"
        jira.search_issues(jql)
    
    elif args.command == 'log':
        if not args.issue or not args.time:
            print("❌ Please provide --issue and --time arguments")
            print("   Example: python jira_tools.py log --issue PROJ-123 --time '1h 30m' --comment 'My work'")
            return
        
        jira.log_work(args.issue, args.time, args.comment)
    
    elif args.command == 'quick':
        jira.quick_log()

if __name__ == "__main__":
    main()