#!/usr/bin/env python3
"""News Delivery Script - Direct approach using OpenClaw message tool."""

import os, sys, subprocess, datetime, json, re

def extract_headlines(file_path):
    """Extract first tech and finance headlines from markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        tech_hl = "科技要闻汇总"
        finance_hl = "市场动态更新"
        
        in_tech_section = False
        in_finance_section = False
        
        for i, line in enumerate(lines):
            # Find Tech section (support both English and Chinese)
            if '## 🖥️' in line and ('Technology' in line or '科技' in line):
                in_tech_section = True
            
            # Find first headline after tech section
            if in_tech_section and re.search(r'^###\s*\d+\.\s*\*\*', line):
                tech_hl = re.sub(r'[###\*\s\d]+', '', line)[:50]
                break
            
            # Find Finance section (support both English and Chinese)
            if '## 📈' in line and ('Financial' in line or '财经' in line):
                in_tech_section = False
                in_finance_section = True
            
            # Find first headline after finance section
            if in_finance_section and re.search(r'^###\s*\d+\.\s*\*\*', line):
                finance_hl = re.sub(r'[###\*\s\d]+', '', line)[:50]
                break
        
        return tech_hl, finance_hl
        
    except Exception as e:
        print(f"Error extracting headlines: {e}")
        return "科技要闻汇总", "市场动态更新"

def create_delivery_message(news_file):
    """Create the delivery message with file attachment."""
    month_day = datetime.date.today().strftime('%m月%d日')
    tech_hl, finance_hl = extract_headlines(news_file)
    
    message = f"""📰 早安，Sir! 今日简报已送达 - {month_day}

🖥️ 科技要闻：{tech_hl}...
📈 财经动态：{finance_hl}...

完整报告：<qqfile>{news_file}</qqfile>

⏰ 明日同一时间自动推送 • Jarvis Daily Briefing"""
    
    return message

def send_via_openclaw_cli(message, target):
    """Send message using OpenClaw CLI."""
    try:
        cmd = [
            'openclaw', 'message', 'send',
            '--channel', 'qqbot',
            '-t', f'c2c:{target}',
            '-m', message
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            env={**os.environ}
        )
        
        if result.returncode == 0:
            print(f"✅ OpenClaw CLI succeeded")
            if result.stdout:
                print(f"   Response: {result.stdout[:200]}")
            return True
            
    except Exception as e:
        print(f"OpenClaw CLI error: {e}")
    
    return False

def send_via_cron_session(message, target):
    """Schedule delivery via openclaw cron session."""
    try:
        # Schedule for now + 30 seconds
        next_time = (datetime.datetime.now() + datetime.timedelta(seconds=30)).strftime('%Y-%m-%dT%H:%M:%S+08:00')
        
        cmd = [
            'openclaw', 'cron', 'add',
            '--name', f'daily-briefing-{datetime.date.today().isoformat()}',
            '--at', next_time,
            '--session', 'isolated',
            '--wake', 'now',
            '--announce',
            '--channel', 'qqbot',
            '--to', f'qqbot:c2c:{target}',
            '--message', message
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            env={**os.environ}
        )
        
        if result.returncode == 0:
            print(f"✅ Cron session scheduled successfully")
            print(f"   Trigger time: {next_time}")
            return True
            
    except Exception as e:
        print(f"Cron session error: {e}")
    
    return False

def main():
    """Main delivery function."""
    news_file = sys.argv[1] if len(sys.argv) > 1 else "/root/.openclaw/workspace/daily-news-" + datetime.date.today().strftime('%Y%m%d') + ".md"
    
    print(f"📨 Starting delivery for: {news_file}")
    
    # Verify file exists
    if not os.path.exists(news_file):
        print(f"❌ Error: News file not found: {news_file}")
        sys.exit(1)
    
    file_size = os.path.getsize(news_file)
    print(f"✅ File verified: {file_size} bytes")
    
    # Create message
    message = create_delivery_message(news_file)
    target_user = "9C12E02D9038B14FCEDCE1B69AAEAB3F"
    
    print(f"\n📝 Message preview ({len(message)} chars):")
    print(message[:300] + "...")
    print()
    
    # Try different delivery methods in order of preference
    success = False
    
    # Method 1: Try cron session (most reliable for proactive messages)
    print("🔄 Attempting Method 1: OpenClaw Cron Session...")
    if send_via_cron_session(message, target_user):
        success = True
        print(f"✅ Delivery scheduled successfully!")
        sys.exit(0)
    
    # Method 2: Try direct CLI message
    if not success:
        print("🔄 Attempting Method 2: Direct OpenClaw CLI...")
        if send_via_openclaw_cli(message, target_user):
            success = True
    
    # Report final status
    if success:
        print(f"\n✅ Delivery completed successfully!")
        sys.exit(0)
    else:
        print(f"\n❌ All delivery methods failed")
        print(f"💡 Manual delivery available: The news file is ready at {news_file}")
        sys.exit(1)

if __name__ == "__main__":
    main()
