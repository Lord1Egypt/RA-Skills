#!/usr/bin/env python3
"""
GitHub工作内容获取脚本
获取指定仓库的commits、PRs、issues
"""

import argparse
import os
from datetime import datetime, timedelta
from github import Github


def get_github_data(token: str, repos: list, since_date: str, until_date: str):
    """获取GitHub数据"""
    g = Github(token)
    
    since = datetime.fromisoformat(since_date)
    until = datetime.fromisoformat(until_date)
    
    results = {
        "commits": [],
        "prs": [],
        "issues": []
    }
    
    for repo_name in repos:
        try:
            repo = g.get_repo(repo_name)
            
            # 获取commits
            commits = repo.get_commits(since=since, until=until)
            for commit in commits:
                results["commits"].append({
                    "repo": repo_name,
                    "sha": commit.sha[:7],
                    "message": commit.commit.message.split('\n')[0],
                    "author": commit.commit.author.name if commit.commit.author else "Unknown",
                    "date": commit.commit.author.date.isoformat() if commit.commit.author else None
                })
            
            # 获取PRs
            pulls = repo.get_pulls(state="closed", sort="updated", direction="desc")
            for pr in pulls:
                if pr.merged and pr.merged_at:
                    merged_date = pr.merged_at
                    if since <= merged_date <= until:
                        results["prs"].append({
                            "repo": repo_name,
                            "number": pr.number,
                            "title": pr.title,
                            "author": pr.user.login,
                            "merged_at": merged_date.isoformat()
                        })
            
            # 获取issues
            issues = repo.get_issues(state="closed", sort="updated", direction="desc")
            for issue in issues:
                if issue.closed_at and since <= issue.closed_at <= until:
                    if not issue.pull_request:  # 排除PR
                        results["issues"].append({
                            "repo": repo_name,
                            "number": issue.number,
                            "title": issue.title,
                            "author": issue.user.login,
                            "closed_at": issue.closed_at.isoformat()
                        })
                        
        except Exception as e:
            print(f"Error fetching {repo_name}: {e}")
    
    return results


def main():
    parser = argparse.ArgumentParser(description="获取GitHub工作数据")
    parser.add_argument("--token", required=True, help="GitHub Personal Access Token")
    parser.add_argument("--repos", nargs="+", required=True, help="仓库列表 (owner/repo)")
    parser.add_argument("--since", required=True, help="开始日期 (ISO格式)")
    parser.add_argument("--until", required=True, help="结束日期 (ISO格式)")
    
    args = parser.parse_args()
    
    results = get_github_data(args.token, args.repos, args.since, args.until)
    import json
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
