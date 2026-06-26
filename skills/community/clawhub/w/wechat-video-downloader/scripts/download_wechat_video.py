#!/usr/bin/env python3
"""
微信视频下载器 - 从微信公众号文章中提取并下载视频

使用方法:
    python download_wechat_video.py <文章 URL> [输出文件名]

示例:
    python download_wechat_video.py https://mp.weixin.qq.com/s/xxx
    python download_wechat_video.py https://mp.weixin.qq.com/s/xxx 我的视频.mp4
"""

import sys
import os
import subprocess
import json
import time
from pathlib import Path


def run_browser_command(action, params=None):
    """执行浏览器控制命令"""
    cmd = ["openclaw", "browser", action]
    if params:
        for key, value in params.items():
            if isinstance(value, bool):
                cmd.append(f"--{key}")
            else:
                cmd.append(f"--{key}={value}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"浏览器命令失败：{result.stderr}")
        return None
    
    try:
        return json.loads(result.stdout)
    except:
        return result.stdout


def extract_video_url(target_id):
    """从页面中提取视频 URL"""
    js_code = """() => {
        const video = document.querySelector('video');
        if(video) {
            return {
                src: video.src,
                currentSrc: video.currentSrc,
                tagName: video.tagName
            };
        }
        return null;
    }"""
    
    result = run_browser_command("act", {
        "targetId": target_id,
        "request": json.dumps({"kind": "evaluate", "fn": js_code})
    })
    
    if result and "result" in result:
        return result["result"]
    return None


def download_video(video_url, output_path, referer="https://mp.weixin.qq.com/"):
    """下载视频文件"""
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    
    cmd = [
        "curl", "-L",
        "-o", output_path,
        "-H", f"User-Agent: {user_agent}",
        "-H", f"Referer: {referer}",
        "-H", "Accept: video/webm,video/ogg,video/mp4,application/octet-stream",
        "--progress-bar",
        video_url
    ]
    
    print(f"开始下载视频到：{output_path}")
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        file_size = os.path.getsize(output_path)
        if file_size > 0:
            print(f"✅ 下载完成！文件大小：{file_size / 1024 / 1024:.1f}MB")
            return True
        else:
            print("❌ 下载的文件为空")
            if os.path.exists(output_path):
                os.remove(output_path)
            return False
    else:
        print(f"❌ 下载失败，退出码：{result.returncode}")
        return False


def download_wechat_video(article_url, output_filename=None):
    """主函数：下载微信公众号视频"""
    
    print(f"📱 打开微信公众号文章：{article_url}")
    
    # 1. 打开文章页面
    result = run_browser_command("open", {"targetUrl": article_url})
    if not result or "targetId" not in result:
        print("❌ 无法打开文章页面")
        return False
    
    target_id = result["targetId"]
    print(f"✓ 页面已打开 (targetId: {target_id})")
    
    # 等待页面加载
    time.sleep(2)
    
    # 2. 获取页面快照查找视频
    print("🔍 查找视频元素...")
    snapshot = run_browser_command("snapshot", {
        "targetId": target_id,
        "refs": "aria"
    })
    
    if not snapshot:
        print("❌ 无法获取页面快照")
        return False
    
    snapshot_str = str(snapshot)
    
    # 查找视频播放按钮
    video_refs = []
    for line in snapshot_str.split('\n'):
        if 'button' in line.lower() and ('播放' in line or 'video' in line.lower() or 'play' in line.lower()):
            if 'ref=' in line:
                ref = line.split('ref=')[1].split(']')[0]
                video_refs.append(ref)
    
    if not video_refs:
        print("❌ 未找到视频播放按钮")
        return False
    
    print(f"✓ 找到视频播放按钮 (refs: {video_refs})")
    
    # 3. 点击播放按钮触发视频加载
    video_ref = video_refs[0]
    print(f"▶️  点击播放按钮 (ref: {video_ref})")
    
    result = run_browser_command("act", {
        "targetId": target_id,
        "request": json.dumps({"kind": "click", "ref": video_ref})
    })
    
    if not result or not result.get("ok"):
        print("❌ 点击播放按钮失败")
        return False
    
    # 等待视频加载
    print("⏳ 等待视频加载...")
    time.sleep(3)
    
    # 4. 提取视频真实 URL
    print("🔗 提取视频 URL...")
    video_info = extract_video_url(target_id)
    
    if not video_info:
        print("❌ 无法提取视频 URL")
        return False
    
    video_url = video_info.get("src") or video_info.get("currentSrc")
    
    if not video_url:
        print("❌ 视频 URL 为空")
        return False
    
    print(f"✓ 获取到视频 URL")
    
    # 5. 确定输出文件名
    if not output_filename:
        vid = video_url.split("vid=")[-1].split("&")[0] if "vid=" in video_url else "wechat_video"
        output_filename = f"{vid}.mp4"
    
    output_path = Path(output_filename).resolve()
    
    # 6. 下载视频
    success = download_video(video_url, str(output_path))
    
    # 7. 关闭浏览器标签页
    run_browser_command("close", {"targetId": target_id})
    
    return success


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    article_url = sys.argv[1]
    output_filename = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = download_wechat_video(article_url, output_filename)
    
    if success:
        print("\n🎉 视频下载完成!")
        sys.exit(0)
    else:
        print("\n💥 视频下载失败!")
        sys.exit(1)


if __name__ == "__main__":
    main()
