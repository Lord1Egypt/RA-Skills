#!/usr/bin/env python3
"""
小红书登录保活脚本
Xiaohongshu Login Keeper - Maintain login session automatically
"""

import subprocess
import time
import json
import argparse
from datetime import datetime, timedelta


def run_browser_cmd(cmd):
    """执行浏览器命令"""
    try:
        # 替换 browser 为 openclaw browser
        if cmd.startswith("browser "):
            cmd = cmd.replace("browser ", "openclaw browser ", 1)
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip()
    except Exception as e:
        return False, str(e)


def check_browser_status():
    """检查浏览器运行状态"""
    success, output = run_browser_cmd("browser --browser-profile openclaw status")
    return success and "running" in output.lower()


def start_browser_if_needed():
    """如果浏览器未运行，启动它"""
    if not check_browser_status():
        print("🚀 启动托管浏览器...")
        success, _ = run_browser_cmd("browser --browser-profile openclaw start")
        if success:
            time.sleep(5)  # 等待启动完成
            return True
    return True


def check_login_status():
    """检查小红书登录状态"""
    print("🔍 检查登录状态...")
    
    # 导航到创作者页面
    cmd = "browser --browser-profile openclaw navigate https://creator.xiaohongshu.com"
    success, _ = run_browser_cmd(cmd)
    if not success:
        return False, "导航失败"
    
    time.sleep(3)
    
    # 检查页面内容，判断是否已登录
    cmd = '''browser --browser-profile openclaw evaluate --fn "() => {
        const url = window.location.href;
        const body = document.body.innerText;
        
        // 检查是否在登录页面
        if (url.includes('login') || body.includes('扫码登录') || body.includes('验证码登录')) {
            return 'need_login';
        }
        
        // 检查是否有用户信息
        if (body.includes('创作服务平台') || body.includes('笔记管理') || body.includes('数据看板')) {
            return 'logged_in';
        }
        
        // 检查是否有用户头像或昵称
        const avatars = document.querySelectorAll('img[alt*=\"头像\"], img[src*=\"avatar\"]');
        if (avatars.length > 0) {
            return 'logged_in';
        }
        
        return 'unknown';
    }"'''
    
    success, output = run_browser_cmd(cmd)
    if not success:
        return False, "状态检查失败"
    
    if 'logged_in' in output:
        return True, "已登录"
    elif 'need_login' in output:
        return False, "需要登录"
    else:
        return False, "状态未知"


def refresh_session():
    """刷新登录会话"""
    print("🔄 刷新登录会话...")
    
    # 访问几个关键页面来保持活跃
    pages = [
        "https://creator.xiaohongshu.com",
        "https://creator.xiaohongshu.com/publish/publish",
        "https://creator.xiaohongshu.com/creator"
    ]
    
    for page in pages:
        cmd = f"browser --browser-profile openclaw navigate {page}"
        run_browser_cmd(cmd)
        time.sleep(2)
    
    print("✅ 会话刷新完成")


def send_notification(message):
    """发送登录状态通知（可扩展到微信、邮件等）"""
    print(f"📱 通知: {message}")
    
    # 这里可以集成通知服务
    # 比如发送到 Telegram、微信、邮件等
    try:
        # 示例：写入日志文件
        with open("/tmp/xiaohongshu_login.log", "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {message}\n")
    except Exception as e:
        print(f"通知发送失败: {e}")


def backup_session():
    """备份浏览器会话数据"""
    print("💾 备份会话数据...")
    
    import shutil
    from pathlib import Path
    
    try:
        source = Path.home() / ".openclaw/browser/openclaw/user-data"
        backup = Path("/tmp/xiaohongshu_session_backup")
        
        if source.exists():
            if backup.exists():
                shutil.rmtree(backup)
            shutil.copytree(source, backup)
            print("✅ 会话数据备份完成")
        else:
            print("⚠️ 会话数据目录不存在")
    
    except Exception as e:
        print(f"❌ 备份失败: {e}")


def restore_session():
    """恢复浏览器会话数据"""
    print("🔄 恢复会话数据...")
    
    import shutil
    from pathlib import Path
    
    try:
        backup = Path("/tmp/xiaohongshu_session_backup")
        target = Path.home() / ".openclaw/browser/openclaw/user-data"
        
        if backup.exists():
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(backup, target)
            print("✅ 会话数据恢复完成")
        else:
            print("⚠️ 备份数据不存在")
    
    except Exception as e:
        print(f"❌ 恢复失败: {e}")


def keep_alive_once():
    """执行一次保活检查"""
    print(f"🕐 [{datetime.now().strftime('%H:%M:%S')}] 开始登录保活检查...")
    
    # 1. 确保浏览器运行
    if not start_browser_if_needed():
        send_notification("浏览器启动失败")
        return False
    
    # 2. 检查登录状态
    is_logged_in, status_msg = check_login_status()
    print(f"登录状态: {status_msg}")
    
    if is_logged_in:
        # 3. 已登录，刷新会话保持活跃
        refresh_session()
        
        # 4. 备份会话数据
        backup_session()
        
        send_notification(f"登录状态正常 - {status_msg}")
        return True
    
    else:
        # 5. 未登录，尝试恢复或发送告警
        send_notification(f"⚠️ 登录已过期 - {status_msg}")
        
        # 可以尝试恢复备份的会话
        print("🔄 尝试恢复备份会话...")
        restore_session()
        
        # 重启浏览器
        run_browser_cmd("browser --browser-profile openclaw stop")
        time.sleep(2)
        start_browser_if_needed()
        
        # 再次检查
        is_logged_in, status_msg = check_login_status()
        if is_logged_in:
            send_notification("✅ 会话恢复成功")
            return True
        else:
            send_notification("❌ 需要手动重新登录")
            return False


def keep_alive_daemon(interval_minutes=30):
    """守护进程模式，定期检查保活"""
    print(f"🔄 启动登录保活守护进程 (间隔: {interval_minutes}分钟)")
    
    while True:
        try:
            success = keep_alive_once()
            
            if success:
                print(f"✅ 保活成功，{interval_minutes}分钟后再次检查")
            else:
                print(f"❌ 保活失败，{interval_minutes}分钟后重试")
            
            # 等待下次检查
            time.sleep(interval_minutes * 60)
            
        except KeyboardInterrupt:
            print("\n👋 收到退出信号，停止保活守护进程")
            break
        except Exception as e:
            print(f"❌ 守护进程异常: {e}")
            send_notification(f"守护进程异常: {e}")
            time.sleep(60)  # 异常时等待1分钟再重试


def main():
    parser = argparse.ArgumentParser(description='小红书登录保活工具')
    parser.add_argument('--mode', choices=['check', 'daemon'], default='check', 
                       help='运行模式: check=单次检查, daemon=守护进程')
    parser.add_argument('--interval', type=int, default=30, 
                       help='守护进程检查间隔(分钟), 默认30分钟')
    
    args = parser.parse_args()
    
    if args.mode == 'check':
        # 单次检查模式
        success = keep_alive_once()
        exit(0 if success else 1)
    
    elif args.mode == 'daemon':
        # 守护进程模式
        keep_alive_daemon(args.interval)


if __name__ == '__main__':
    main()