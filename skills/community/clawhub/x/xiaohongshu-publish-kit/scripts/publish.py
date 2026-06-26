#!/usr/bin/env python3
"""
小红书自动发布脚本
Xiaohongshu Auto Publisher Script
"""

import argparse
import sys
import subprocess
import time
from pathlib import Path


def run_browser_cmd(cmd):
    """执行浏览器命令并返回结果"""
    try:
        # 替换 browser 为 openclaw browser
        if cmd.startswith("browser "):
            cmd = cmd.replace("browser ", "openclaw browser ", 1)
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip()
    except Exception as e:
        print(f"命令执行失败: {e}")
        return False, str(e)


def check_browser_status():
    """检查浏览器状态"""
    success, output = run_browser_cmd("browser --browser-profile openclaw status")
    if not success:
        print("浏览器未启动，正在启动...")
        success, _ = run_browser_cmd("browser --browser-profile openclaw start")
        if not success:
            print("浏览器启动失败")
            return False
        time.sleep(3)
    return True


def check_login_status():
    """检查登录状态，如果未登录则自动尝试恢复"""
    print("🔍 检查小红书登录状态...")
    
    # 导航到创作者页面
    cmd = "browser --browser-profile openclaw navigate https://creator.xiaohongshu.com"
    success, _ = run_browser_cmd(cmd)
    if not success:
        print("❌ 无法访问小红书创作者页面")
        return False
    
    time.sleep(3)
    
    # 检查是否需要登录
    cmd = '''browser --browser-profile openclaw evaluate --fn "() => {
        const url = window.location.href;
        const body = document.body.innerText;
        
        if (url.includes('login') || body.includes('扫码登录') || body.includes('验证码登录')) {
            return 'need_login';
        }
        
        if (body.includes('创作服务平台') || body.includes('笔记管理') || body.includes('数据看板')) {
            return 'logged_in';
        }
        
        return 'unknown';
    }"'''
    
    success, output = run_browser_cmd(cmd)
    if success and 'logged_in' in output:
        print("✅ 登录状态正常")
        return True
    
    elif success and 'need_login' in output:
        print("⚠️ 需要登录，尝试恢复会话...")
        
        # 尝试恢复备份会话
        try:
            import shutil
            from pathlib import Path
            
            backup = Path("/tmp/xiaohongshu_session_backup")
            target = Path.home() / ".openclaw/browser/openclaw/user-data"
            
            if backup.exists():
                print("🔄 恢复备份会话...")
                run_browser_cmd("browser --browser-profile openclaw stop")
                time.sleep(2)
                
                if target.exists():
                    shutil.rmtree(target)
                shutil.copytree(backup, target)
                
                # 重启浏览器
                check_browser_status()
                time.sleep(5)
                
                # 再次检查登录状态
                return check_login_status_simple()
            
        except Exception as e:
            print(f"恢复会话失败: {e}")
        
        print("❌ 需要手动扫码登录")
        print("请在浏览器中完成登录后重试")
        return False
    
    else:
        print("❓ 登录状态未知，建议检查网络连接")
        return False


def check_login_status_simple():
    """简化的登录状态检查"""
    cmd = '''browser --browser-profile openclaw evaluate --fn "() => {
        const body = document.body.innerText;
        return body.includes('创作服务平台') || body.includes('笔记管理') ? 'ok' : 'fail';
    }"'''
    
    success, output = run_browser_cmd(cmd)
    return success and 'ok' in output


def navigate_to_publish_page():
    """导航到发布页面"""
    print("导航到小红书发布页面...")
    cmd = "browser --browser-profile openclaw navigate https://creator.xiaohongshu.com/publish/publish"
    success, _ = run_browser_cmd(cmd)
    if success:
        time.sleep(3)
    return success


def switch_to_image_mode():
    """切换到图文发布模式"""
    print("切换到图文发布模式...")
    cmd = '''browser --browser-profile openclaw evaluate --fn "() => {
        const tabs = document.querySelectorAll('.creator-tab, [class*=tab]');
        for (const t of tabs) {
            if (t.textContent.trim().includes('上传图文')) {
                t.click();
                return 'switched';
            }
        }
        return 'not found';
    }"'''
    success, output = run_browser_cmd(cmd)
    if success and 'switched' in output:
        time.sleep(2)
        return True
    return False


def upload_image(image_path):
    """上传图片"""
    if not Path(image_path).exists():
        print(f"图片文件不存在: {image_path}")
        return False
    
    print(f"上传图片: {image_path}")
    
    # 创建上传目录并复制图片
    upload_dir = Path("/tmp/openclaw/uploads")
    upload_dir.mkdir(exist_ok=True)
    
    import shutil
    dest_path = upload_dir / Path(image_path).name
    shutil.copy2(image_path, dest_path)
    
    # arm 上传
    cmd = f"browser --browser-profile openclaw upload {dest_path}"
    success, _ = run_browser_cmd(cmd)
    if not success:
        return False
    
    # 获取页面快照找上传按钮
    cmd = "browser --browser-profile openclaw snapshot"
    success, output = run_browser_cmd(cmd)
    if not success:
        return False
    
    # 查找上传按钮ref（简化版，实际应解析snapshot）
    # 这里使用通用的点击方式
    cmd = '''browser --browser-profile openclaw evaluate --fn "() => {
        const btns = document.querySelectorAll('button');
        for (const b of btns) {
            if (b.textContent.includes('上传图片')) {
                b.click();
                return 'clicked';
            }
        }
        return 'not found';
    }"'''
    success, output = run_browser_cmd(cmd)
    
    if success:
        time.sleep(5)  # 等待上传完成
        return True
    return False


def set_title(title):
    """设置标题"""
    if len(title) > 20:
        print(f"警告: 标题长度 {len(title)} 超过20字限制，将被截断")
        title = title[:20]
    
    print(f"设置标题: {title}")
    
    # 转义单引号
    title_escaped = title.replace("'", "\\'")
    
    cmd = f'''browser --browser-profile openclaw evaluate --fn "() => {{
        const el = document.querySelector('input[placeholder*=\"标题\"]');
        if (!el) return 'title input not found';
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        setter.call(el, '{title_escaped}');
        el.dispatchEvent(new Event('input', {{bubbles:true}}));
        el.dispatchEvent(new Event('change', {{bubbles:true}}));
        return 'title set, length=' + el.value.length;
    }}"'''
    
    success, output = run_browser_cmd(cmd)
    return success and 'title set' in output


def set_content(content):
    """设置正文内容"""
    if len(content) > 1000:
        print(f"警告: 正文长度 {len(content)} 超过1000字限制，将被截断")
        content = content[:1000]
    
    print(f"设置正文内容 ({len(content)}字)")
    
    # 将内容转换为HTML段落格式
    paragraphs = content.split('\n')
    html_content = ''
    for p in paragraphs:
        if p.strip():
            # 转义单引号和双引号
            p_escaped = p.replace("'", "\\'").replace('"', '\\"')
            html_content += f'<p>{p_escaped}</p>'
        else:
            html_content += '<p><br></p>'
    
    cmd = f'''browser --browser-profile openclaw evaluate --fn "() => {{
        const el = document.querySelector('.ql-editor, [contenteditable=true], .ProseMirror');
        if (!el) return 'editor not found';
        el.focus();
        el.innerHTML = '{html_content}';
        el.dispatchEvent(new Event('input', {{bubbles:true}}));
        return 'content set, length=' + el.textContent.length;
    }}"'''
    
    success, output = run_browser_cmd(cmd)
    return success and 'content set' in output


def publish():
    """发布笔记"""
    print("发布笔记...")
    
    cmd = '''browser --browser-profile openclaw evaluate --fn "() => {
        const btns = document.querySelectorAll('button');
        for (const b of btns) {
            if (b.textContent.trim() === '发布') {
                b.click();
                return 'publish clicked';
            }
        }
        return 'publish button not found';
    }"'''
    
    success, output = run_browser_cmd(cmd)
    if not success or 'clicked' not in output:
        return False
    
    time.sleep(5)  # 等待发布完成
    
    # 检查发布状态
    cmd = "browser --browser-profile openclaw tabs"
    success, output = run_browser_cmd(cmd)
    
    if success and 'published=true' in output:
        print("✅ 发布成功!")
        return True
    else:
        print("❌ 发布可能失败，请检查页面状态")
        return False


def main():
    parser = argparse.ArgumentParser(description='小红书自动发布工具')
    parser.add_argument('--title', required=True, help='笔记标题 (最多20字)')
    parser.add_argument('--content', required=True, help='笔记内容 (最多1000字)')
    parser.add_argument('--image', required=True, help='封面图片路径')
    
    args = parser.parse_args()
    
    print("🚀 开始自动发布到小红书...")
    
    # 检查浏览器状态
    if not check_browser_status():
        print("❌ 浏览器启动失败")
        sys.exit(1)
    
    # 检查登录状态
    if not check_login_status():
        print("❌ 登录状态异常，无法继续发布")
        sys.exit(1)
    
    # 导航到发布页面
    if not navigate_to_publish_page():
        print("❌ 导航到发布页面失败")
        sys.exit(1)
    
    # 切换到图文模式
    if not switch_to_image_mode():
        print("❌ 切换到图文模式失败")
        sys.exit(1)
    
    # 上传图片
    if not upload_image(args.image):
        print("❌ 图片上传失败")
        sys.exit(1)
    
    # 设置标题
    if not set_title(args.title):
        print("❌ 标题设置失败")
        sys.exit(1)
    
    # 设置内容
    if not set_content(args.content):
        print("❌ 内容设置失败")
        sys.exit(1)
    
    # 发布
    if not publish():
        print("❌ 发布失败")
        sys.exit(1)
    
    print("🎉 小红书发布完成!")


if __name__ == '__main__':
    main()