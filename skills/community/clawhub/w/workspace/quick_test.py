#!/usr/bin/env python3
from jira_tools import JiraClient

jira = JiraClient()
print("Testing Jira connection and listing issues...")

# Test connection
if jira.test_connection():
    print("\n✅ Connection successful!")
    
    # List recent issues
    print("\n📋 Listing your recent issues...")
    issues = jira.search_issues("assignee = currentUser() AND updated >= -7d ORDER BY updated DESC")
    
    if issues:
        print(f"\nFound {len(issues)} recent issues")
        print("\nYou can now use:")
        print("  ./jira_log.sh log       - To log work")
        print("  ./jira_log.sh list      - To list issues")
        print("  ./jira_log.sh today     - To create daily log")
    else:
        print("\n⚠️  No recent issues found. Try a different JQL query.")
else:
    print("\n❌ Connection failed. Please check your credentials in jira_config.json")