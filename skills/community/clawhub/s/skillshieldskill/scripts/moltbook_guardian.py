#!/usr/bin/env python3
"""
SkillGuard Moltbook Integration
Automatically scan skills on Moltbook and post security reports
"""

import sys
import os
import json
import urllib.request
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skillguard import SkillScanner, format_report

# Moltbook API configuration
MOLTBOOK_API = "https://www.moltbook.com/api/v1"
API_KEY = os.environ.get('MOLTBOOK_API_KEY', '')


class MoltbookGuardian:
    """Monitor Moltbook for new skills and scan them"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or API_KEY
        self.scanner = SkillScanner()
        self.checked_posts = set()
    
    def get_recent_posts(self, limit: int = 10) -> list:
        """Get recent posts from Moltbook feed"""
        try:
            req = urllib.request.Request(
                f"{MOLTBOOK_API}/feed?limit={limit}",
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Accept': 'application/json'
                }
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read())
                return data.get('posts', [])
        except Exception as e:
            print(f"Error fetching posts: {e}")
            return []
    
    def check_for_skill_posts(self, posts: list) -> list:
        """Filter posts that mention skills"""
        skill_keywords = ['skill', 'clawhub', 'install', 'skill.md']
        skill_posts = []
        
        for post in posts:
            content = post.get('content', '').lower()
            title = post.get('title', '').lower()
            
            if any(keyword in content or keyword in title for keyword in skill_keywords):
                if post.get('id') not in self.checked_posts:
                    skill_posts.append(post)
        
        return skill_posts
    
    def generate_security_comment(self, result: dict) -> str:
        """Generate a security report comment for Moltbook"""
        rating = result.get('trust_rating', 'N/A')
        score = result.get('score', 0)
        warnings = result.get('warnings', [])
        
        # Emoji based on rating
        rating_emoji = {
            'A+': '🟢', 'A': '🟢', 'B': '🟡',
            'C': '🟠', 'D': '🔴', 'F': '⛔'
        }.get(rating, '⚪')
        
        lines = []
        lines.append(f"🔒 @SkillGuard 安全扫描报告")
        lines.append("")
        lines.append(f"📊 信任评级: {rating_emoji} **{rating}** (得分: {score}/100)")
        lines.append("")
        
        if warnings:
            lines.append(f"⚠️  **警告 ({len(warnings)} 个):**")
            lines.append("")
            
            # Show critical and high warnings
            for warning in warnings[:5]:  # Limit to 5
                severity = warning.get('severity', 'medium').upper()
                desc = warning.get('description', 'Unknown')
                
                emoji = {'CRITICAL': '⛔', 'HIGH': '🔴', 'MEDIUM': '🟠'}.get(severity, '⚪')
                lines.append(f"{emoji} [{severity}] {desc}")
            
            if len(warnings) > 5:
                lines.append(f"... 还有 {len(warnings) - 5} 个警告")
        else:
            lines.append("✅ **无警告** - 未发现明显安全问题")
        
        lines.append("")
        lines.append(f"💡 **建议:** {result.get('summary', '')}")
        lines.append("")
        lines.append("---")
        lines.append("🛡️ *由 SkillGuard 自动扫描* | 保护 Agent 生态安全")
        
        return "\n".join(lines)
    
    def monitor(self, interval: int = 300):
        """Continuously monitor Moltbook for new skills"""
        print(f"🔍 SkillGuard 开始监控 Moltbook...")
        print(f"   检查间隔: {interval} 秒")
        print(f"   API: {MOLTBOOK_API}")
        print("   按 Ctrl+C 停止\n")
        
        try:
            while True:
                # Get recent posts
                posts = self.get_recent_posts(limit=20)
                
                # Check for skill-related posts
                skill_posts = self.check_for_skill_posts(posts)
                
                for post in skill_posts:
                    post_id = post.get('id')
                    title = post.get('title', 'Untitled')
                    author = post.get('author', {}).get('name', 'Unknown')
                    
                    print(f"📌 发现 skill 相关帖子: {title} by @{author}")
                    
                    # Mark as checked
                    self.checked_posts.add(post_id)
                    
                    # TODO: Download and scan the actual skill
                    # For now, just generate a placeholder report
                    print(f"   💡 建议: 请联系作者提供 skill 代码进行扫描\n")
                
                # Sleep
                import time
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n👋 SkillGuard 监控已停止")
    
    def scan_skill_by_url(self, url: str) -> dict:
        """Download and scan a skill from URL"""
        # TODO: Implement skill download from GitHub/GitLab
        pass
    
    def post_comment(self, post_id: str, content: str):
        """Post a comment to a Moltbook post"""
        # TODO: Implement comment posting
        pass


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='SkillGuard Moltbook Guardian')
    parser.add_argument('--monitor', '-m', action='store_true',
                       help='持续监控 Moltbook')
    parser.add_argument('--interval', '-i', type=int, default=300,
                       help='检查间隔 (秒，默认: 300)')
    parser.add_argument('--scan-post', '-s', metavar='POST_ID',
                       help='扫描特定帖子')
    
    args = parser.parse_args()
    
    guardian = MoltbookGuardian()
    
    if args.monitor:
        guardian.monitor(interval=args.interval)
    elif args.scan_post:
        print(f"扫描帖子: {args.scan_post}")
        # TODO: Implement single post scanning
    else:
        # Test: Get recent posts and check
        print("🔍 测试模式: 获取最近帖子\n")
        posts = guardian.get_recent_posts(limit=10)
        print(f"获取到 {len(posts)} 个帖子")
        
        skill_posts = guardian.check_for_skill_posts(posts)
        print(f"发现 {len(skill_posts)} 个 skill 相关帖子")
        
        for post in skill_posts:
            print(f"\n📌 {post.get('title')}")
            print(f"   作者: {post.get('author', {}).get('name')}")


if __name__ == '__main__':
    main()
