#!/usr/bin/env python3
"""
阴阳师原画壁纸下载脚本
- 自动抓取页面所有图片 URL
- 按分辨率筛选/下载
- 跳过已存在的文件
- 支持分批下载和进度显示
- 更好的错误处理和重试机制
"""

import os
import re
import sys
import random
import time
import urllib.request
import argparse

BASE_URL = "https://yys.163.com/media/picture.html"
DEFAULT_RESOLUTION = "1920x1080"
SAVE_DIR = os.path.expanduser("~/Pictures")
TIMEOUT = 30                    # 增加超时时间
# SKIP_EXISTING 常量已移除，使用命令行参数控制
MIN_DELAY = 0.3                 # 调整延迟范围
MAX_DELAY = 1.0
BATCH_SIZE = 50                 # 每批显示进度
MAX_RETRIES = 3                 # 最大重试次数


def fetch_page(url):
    """获取网页内容"""
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read().decode('utf-8', errors='ignore')


def extract_image_urls(html, resolution):
    """从页面 HTML 中提取所有图片 URL"""
    pattern = r'(https://yys\.res\.netease\.com/pc/zt/\d+/data/picture/\d+/\d+/' + re.escape(resolution) + r'\.(?:jpg|png))'
    urls = re.findall(pattern, html)
    return list(set(urls))


def url_to_filename(url, resolution):
    """将 URL 转换为文件名"""
    match = re.search(r'(picture/\d+/\d+/' + re.escape(resolution) + r'\.(?:jpg|png))', url)
    if match:
        path = match.group(1)
        return path.replace('picture/', '').replace('/', '_')
    return None


# get_save_path 函数已移除，直接在main函数中构建路径


def get_existing_files(resolution):
    """获取指定分辨率下已存在的文件列表"""
    target_dir = os.path.join(SAVE_DIR, resolution)
    if not os.path.exists(target_dir):
        return set()
    
    files = set()
    for f in os.listdir(target_dir):
        if f.endswith('.jpg') or f.endswith('.png'):
            files.add(f)
    return files


def download_file(url, save_path, retries=MAX_RETRIES):
    """下载单个文件，失败自动重试"""
    last_error = None
    
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            })
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                # 检查HTTP状态码
                if resp.status != 200:
                    raise ValueError(f"HTTP {resp.status}: {resp.reason}")
                
                data = resp.read()
                with open(save_path, 'wb') as f:
                    f.write(data)
            
            # 验证文件
            if os.path.getsize(save_path) == 0:
                os.remove(save_path)  # 删除空文件
                raise ValueError("文件大小为0")
            
            return True
            
        except urllib.error.HTTPError as e:
            last_error = f"HTTP错误 {e.code}: {e.reason}"
            if e.code == 404:
                # 404错误不需要重试
                raise ValueError(f"文件不存在 (404): {url}")
            
        except urllib.error.URLError as e:
            last_error = f"URL错误: {e.reason}"
            
        except Exception as e:
            last_error = str(e)
            
        # 如果不是最后一次重试，等待后继续
        if attempt < retries - 1:
            time.sleep(2 ** attempt)  # 指数退避：1, 2, 4秒
            continue
            
    # 所有重试都失败
    if last_error:
        raise ValueError(f"下载失败: {last_error}")
    else:
        raise ValueError("下载失败: 未知错误")


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='阴阳师原画壁纸下载工具')
    parser.add_argument('resolution', nargs='?', default=DEFAULT_RESOLUTION,
                       help=f'分辨率，默认: {DEFAULT_RESOLUTION}')
    parser.add_argument('--batch-size', type=int, default=BATCH_SIZE,
                       help=f'每批下载数量，默认: {BATCH_SIZE}')
    parser.add_argument('--no-skip', action='store_false', dest='skip_existing',
                       help='不跳过已存在的文件')
    parser.add_argument('--min-delay', type=float, default=MIN_DELAY,
                       help=f'最小延迟(秒)，默认: {MIN_DELAY}')
    parser.add_argument('--max-delay', type=float, default=MAX_DELAY,
                       help=f'最大延迟(秒)，默认: {MAX_DELAY}')
    
    return parser.parse_args()


def main():
    args = parse_args()
    resolution = args.resolution
    batch_size = args.batch_size
    skip_existing = args.skip_existing
    min_delay = args.min_delay
    max_delay = args.max_delay

    print(f"📥 开始下载阴阳师壁纸 | 分辨率: {resolution}")
    print(f"📁 保存目录: {SAVE_DIR}/{resolution}/")
    print("-" * 50)

    # 创建保存目录
    target_dir = os.path.join(SAVE_DIR, resolution)
    os.makedirs(target_dir, exist_ok=True)

    # 获取已存在文件
    existing_files = get_existing_files(resolution)
    print(f"📊 已存在 {len(existing_files)} 个文件")

    # 获取页面
    print("🌐 获取页面...")
    try:
        html = fetch_page(BASE_URL)
    except Exception as e:
        print(f"❌ 获取页面失败: {e}")
        sys.exit(1)

    # 提取 URL
    urls = extract_image_urls(html, resolution)
    print(f"🔍 网站共有 {len(urls)} 张图片")

    if not urls:
        print("⚠️ 未找到图片，可能页面结构已变或该分辨率不存在")
        sys.exit(1)

    # 筛选需要下载的URL
    to_download = []
    for url in sorted(urls):
        filename = url_to_filename(url, resolution)
        if filename:
            if skip_existing and filename in existing_files:
                continue
            to_download.append((url, filename))
    
    total_needed = len(to_download)
    print(f"⬇️  需要下载 {total_needed} 张新图片")
    
    if total_needed == 0:
        print("✅ 所有图片已下载完成！")
        return

    # 分批下载
    downloaded = failed = 0
    skipped = len(urls) - total_needed  # 跳过的文件数
    
    for batch_start in range(0, total_needed, batch_size):
        batch_end = min(batch_start + batch_size, total_needed)
        batch = to_download[batch_start:batch_end]
        
        print(f"\n📦 批次 {batch_start//batch_size + 1}/{(total_needed + batch_size - 1)//batch_size}")
        print(f"   下载第 {batch_start+1}-{batch_end} 张")
        
        for i, (url, filename) in enumerate(batch, 1):
            save_path = os.path.join(target_dir, filename)
            global_index = batch_start + i
            
            # 随机延迟，避免请求过快
            time.sleep(random.uniform(min_delay, max_delay))
            
            print(f"   [{global_index}/{total_needed}] {filename}", end=" ... ", flush=True)
            
            try:
                download_file(url, save_path)
                size = os.path.getsize(save_path) / 1024
                print(f"✅ {size:.1f} KB")
                downloaded += 1
            except Exception as e:
                error_msg = str(e)
                if len(error_msg) > 50:
                    error_msg = error_msg[:47] + "..."
                print(f"❌ {error_msg}")
                failed += 1
        
        # 批次完成，显示进度
        progress = (batch_end / total_needed) * 100
        print(f"   📊 进度: {batch_end}/{total_needed} ({progress:.1f}%) | 成功: {downloaded} | 失败: {failed}")
    
    print("-" * 50)
    print(f"🎉 下载完成！")
    print(f"   网站图片总数: {len(urls)} 张")
    print(f"   跳过已存在: {skipped} 张")
    print(f"   需要下载: {total_needed} 张")
    print(f"   成功下载: {downloaded} 张")
    print(f"   下载失败: {failed} 张")
    
    # 最终统计
    final_count = len(get_existing_files(resolution))
    success_rate = (downloaded / total_needed * 100) if total_needed > 0 else 100
    print(f"   现有文件总数: {final_count} 个")
    print(f"   下载成功率: {success_rate:.1f}%")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n\n❌ 发生错误: {e}")
        sys.exit(1)
