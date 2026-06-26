#!/usr/bin/env python3
"""
Video Catcher Pro - 超强视频下载技能 v2.0
融合 Cat-Catch 核心功能 + yt-dlp 引擎
"""

import os
import sys
import re
import json
import subprocess
import argparse
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime
from urllib.parse import urlparse, parse_qs

try:
    import requests
except ImportError:
    print("需要安装 requests: pip install requests")
    sys.exit(1)


# ============================================================
# Cat-Catch 核心功能 (从JS移植)
# ============================================================

class M3U8Parser:
    """M3U8解析器 - 移植自Cat-Catch"""
    
    def __init__(self, m3u8_url: str, headers: Dict = None):
        self.m3u8_url = m3u8_url
        self.headers = headers or {}
        self.base_url = m3u8_url.rsplit('/', 1)[0] + '/'
        self.content = None
        self.segments = []
        self.duration = 0
        self.key_info = None
        self.is_encrypted = False
        
    def fetch(self) -> str:
        """获取M3U8内容"""
        try:
            resp = requests.get(self.m3u8_url, headers=self.headers, timeout=30)
            resp.raise_for_status()
            self.content = resp.text
            return self.content
        except Exception as e:
            raise Exception(f"获取M3U8失败: {e}")
    
    def parse(self) -> List[Dict]:
        """解析M3U8，提取所有切片"""
        if not self.content:
            self.fetch()
        
        lines = self.content.strip().split('\n')
        self.segments = []
        current_extinf = None
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            if line.startswith('#EXTINF:'):
                # 获取时长
                duration_match = re.search(r'#EXTINF:([\d.]+)', line)
                current_extinf = {
                    'duration': float(duration_match.group(1)) if duration_match else 0,
                    'title': ''
                }
                
            elif line.startswith('#EXT-X-KEY:'):
                # 处理加密信息
                self.is_encrypted = True
                key_match = re.search(r'KEY:method=([^,]+),uri="([^"]+)"', line)
                if key_match:
                    method, uri = key_match.groups()
                    self.key_info = {
                        'method': method,
                        'uri': uri if uri.startswith('http') else self.base_url + uri
                    }
                    
            elif line.startswith('#') or line == '':
                continue
                
            else:
                # 实际URL
                if current_extinf:
                    url = line.strip()
                    if url and not url.startswith('#'):
                        # 相对URL处理
                        if url.startswith('http'):
                            full_url = url
                        else:
                            full_url = self.base_url + url
                        
                        self.segments.append({
                            'url': full_url,
                            'duration': current_extinf['duration'],
                            'index': len(self.segments)
                        })
                    current_extinf = None
        
        self.duration = sum(s['duration'] for s in self.segments)
        return self.segments
    
    def get_info(self) -> Dict:
        """获取视频信息"""
        if not self.segments:
            self.parse()
        
        return {
            'url': self.m3u8_url,
            'segments_count': len(self.segments),
            'duration': self.duration,
            'duration_formatted': self._format_duration(self.duration),
            'is_encrypted': self.is_encrypted,
            'estimated_size_mb': len(self.segments) * 2 / 1024,
        }
    
    def _format_duration(self, seconds: float) -> str:
        """格式化时长"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        return f"{minutes}:{secs:02d}"


class TSDownloader:
    """TS切片下载器"""
    
    def __init__(self, output_dir: str = None, headers: Dict = None):
        self.output_dir = output_dir or r'C:\Users\26240\workspace\video-downloads'
        os.makedirs(self.output_dir, exist_ok=True)
        self.headers = headers or {}
        self.downloaded = []
        
    def download_segment(self, url: str, index: int, timeout: int = 30) -> Optional[str]:
        """下载单个TS切片"""
        try:
            resp = requests.get(url, headers=self.headers, timeout=timeout, stream=True)
            resp.raise_for_status()
            
            filename = f"segment_{index:05d}.ts"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            self.downloaded.append(filepath)
            return filepath
            
        except Exception as e:
            print(f"  下载失败 [{index}]: {e}")
            return None
    
    def download_all(self, segments: List[Dict], show_progress: bool = True) -> List[str]:
        """下载所有切片"""
        total = len(segments)
        print(f"\n开始下载 {total} 个切片...")
        
        for i, seg in enumerate(segments):
            if show_progress:
                print(f"\r  进度: {i+1}/{total} ({100*(i+1)//total}%)", end='', flush=True)
            
            self.download_segment(seg['url'], i)
        
        if show_progress:
            print()  # 换行
        
        return self.downloaded
    
    def merge_with_ffmpeg(self, output_name: str = "output.mp4") -> Optional[str]:
        """使用ffmpeg合并TS文件"""
        if not self.downloaded:
            print("没有下载的切片")
            return None
            
        output_path = os.path.join(self.output_dir, output_name)
        file_list = os.path.join(self.output_dir, "filelist.txt")
        
        # 创建文件列表
        with open(file_list, 'w', encoding='utf-8') as f:
            for filepath in sorted(self.downloaded):
                f.write(f"file '{filepath}'\n")
        
        # 使用ffmpeg合并
        try:
            cmd = [
                'ffmpeg', '-f', 'concat', '-safe', '0',
                '-i', file_list,
                '-c', 'copy',
                '-y', output_path
            ]
            
            print(f"\n合并中...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"合并完成: {output_path}")
                return output_path
            else:
                print(f"合并失败: {result.stderr}")
                return None
                
        except FileNotFoundError:
            print("ffmpeg未安装，将保留TS切片文件")
            return None
    
    def cleanup(self):
        """清理临时文件"""
        for f in self.downloaded:
            try:
                os.remove(f)
            except:
                pass
        
        filelist = os.path.join(self.output_dir, "filelist.txt")
        if os.path.exists(filelist):
            try:
                os.remove(filelist)
            except:
                pass


def download_m3u8(m3u8_url: str, output_dir: str = None, headers: Dict = None) -> Optional[str]:
    """下载M3U8视频（TS切片方式）"""
    output_dir = output_dir or rf'C:\Users\26240\workspace\video-downloads\{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    
    print(f"\n[Video Catcher Pro] M3U8下载")
    print(f"{'='*50}")
    print(f"URL: {m3u8_url}")
    
    parser = M3U8Parser(m3u8_url, headers)
    
    try:
        info = parser.get_info()
        print(f"\n解析成功!")
        print(f"  切片数量: {info['segments_count']}")
        print(f"  总时长: {info['duration_formatted']}")
        print(f"  加密: {'是' if info['is_encrypted'] else '否'}")
        
        # 下载切片
        downloader = TSDownloader(output_dir, headers)
        downloaded = downloader.download_all(parser.segments)
        
        print(f"\n下载完成: {len(downloaded)} 个切片")
        
        # 尝试合并
        merged = downloader.merge_with_ffmpeg("output.mp4")
        
        if merged:
            downloader.cleanup()
            return merged
        else:
            print(f"\nTS切片保存在: {output_dir}")
            return output_dir
            
    except Exception as e:
        print(f"错误: {e}")
        return None


# ============================================================
# yt-dlp 集成
# ============================================================

def check_ytdlp() -> bool:
    """检查yt-dlp是否安装"""
    try:
        subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
        return True
    except:
        return False


def download_with_ytdlp(url: str, output_dir: str = None, options: List[str] = None) -> Optional[str]:
    """使用yt-dlp下载视频"""
    output_dir = output_dir or r'C:\Users\26240\workspace\video-downloads'
    os.makedirs(output_dir, exist_ok=True)
    
    if not check_ytdlp():
        print("错误: yt-dlp未安装")
        print("安装: pip install yt-dlp")
        return None
    
    print(f"\n[Video Catcher Pro] yt-dlp下载")
    print(f"{'='*50}")
    print(f"URL: {url}")
    
    output_template = os.path.join(output_dir, '%(title)s.%(ext)s')
    cmd = ['yt-dlp', '-o', output_template, url]
    
    if options:
        cmd.extend(options)
    
    try:
        print(f"\n执行: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"\n✅ 下载完成!")
            # 显示最后几行输出
            output = result.stdout
            if len(output) > 500:
                output = output[-500:]
            print(output)
            return output_dir
        else:
            print(f"\n❌ 下载失败!")
            print(result.stderr[-1000:] if len(result.stderr) > 1000 else result.stderr)
            return None
            
    except Exception as e:
        print(f"错误: {e}")
        return None


def analyze_url(url: str) -> Dict:
    """分析视频URL"""
    result = {
        'url': url,
        'type': 'unknown',
        'platform': 'unknown',
        'downloadable': False,
        'recommend': 'unknown'
    }
    
    # 判断平台
    platform_map = {
        'youtube.com': 'YouTube',
        'youtu.be': 'YouTube',
        'bilibili.com': 'Bilibili',
        'b23.tv': 'Bilibili',
        'weibo.com': '微博',
        'video.sina.com.cn': '微博',
        'tiktok.com': 'TikTok',
        'douyin.com': '抖音',
        'twitter.com': 'Twitter',
        'x.com': 'Twitter',
        'instagram.com': 'Instagram',
        'facebook.com': 'Facebook',
        'v.qq.com': '腾讯视频',
        'vip.youku.com': '优酷',
        'iqiyi.com': '爱奇艺',
        'mgtv.com': '芒果TV',
        'xiaohongshu.com': '小红书',
    }
    
    for domain, name in platform_map.items():
        if domain in url.lower():
            result['platform'] = name
            result['downloadable'] = True
            result['recommend'] = 'yt-dlp'
            break
    
    # 判断URL类型
    if '.m3u8' in url.lower():
        result['type'] = 'M3U8 (HLS)'
        result['recommend'] = 'm3u8'
    elif '.mp4' in url.lower():
        result['type'] = 'MP4 (Direct)'
        result['recommend'] = 'ytdlp or direct'
    elif 'manifest' in url.lower():
        result['type'] = 'DASH'
        result['recommend'] = 'ytdlp'
    
    return result


def extract_from_webpage(url: str) -> List[Dict]:
    """从网页提取视频URL"""
    print(f"\n[Video Catcher Pro] 分析网页")
    print(f"{'='*50}")
    print(f"URL: {url}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        resp = requests.get(url, headers=headers, timeout=30)
        content = resp.text
        
        results = []
        
        # 提取M3U8链接
        m3u8_pattern = re.compile(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*')
        for match in m3u8_pattern.findall(content):
            if match not in [r['url'] for r in results]:
                results.append({'type': 'm3u8', 'url': match})
        
        # 提取MP4链接
        mp4_pattern = re.compile(r'https?://[^\s"\'<>]+\.mp4[^\s"\'<>]*')
        for match in mp4_pattern.findall(content):
            if match not in [r['url'] for r in results]:
                results.append({'type': 'mp4', 'url': match})
        
        # 提取M3U8在JS中的URL
        js_m3u8_pattern = re.compile(r'["\']([^"\']*\.m3u8[^"\']*)["\']')
        for match in js_m3u8_pattern.findall(content):
            if '.m3u8' in match and match not in [r['url'] for r in results]:
                results.append({'type': 'm3u8_js', 'url': match})
        
        print(f"\n发现 {len(results)} 个视频资源:")
        for i, r in enumerate(results[:10], 1):
            print(f"  {i}. [{r['type']}] {r['url'][:80]}...")
        
        if not results:
            print("\n未发现直接视频链接")
            print("提示: 使用yt-dlp可以下载大多数网站的视频")
        
        return results
    
    except Exception as e:
        print(f"错误: {e}")
        return []


def get_video_formats(url: str) -> str:
    """获取视频可用格式"""
    if not check_ytdlp():
        return "yt-dlp未安装"
    
    print(f"\n[Video Catcher Pro] 可用格式")
    print(f"{'='*50}")
    print(f"URL: {url}")
    
    try:
        cmd = ['yt-dlp', '--list-formats', url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return result.stdout
        else:
            return result.stderr
            
    except Exception as e:
        return str(e)


# ============================================================
# 主程序
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='Video Catcher Pro - 超强视频下载技能 v2.0')
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # M3U8下载
    m3u8_parser = subparsers.add_parser('m3u8', help='下载M3U8视频')
    m3u8_parser.add_argument('url', help='M3U8 URL')
    m3u8_parser.add_argument('-o', '--output', help='输出目录')
    m3u8_parser.add_argument('--referer', help='Referer头')
    
    # 分析URL
    analyze_parser = subparsers.add_parser('analyze', help='分析视频URL')
    analyze_parser.add_argument('url', help='视频URL')
    
    # 网页提取
    extract_parser = subparsers.add_parser('extract', help='从网页提取视频')
    extract_parser.add_argument('url', help='网页URL')
    
    # yt-dlp下载
    ytdlp_parser = subparsers.add_parser('ytdlp', help='使用yt-dlp下载')
    ytdlp_parser.add_argument('url', help='视频URL')
    ytdlp_parser.add_argument('-o', '--output', help='输出目录')
    
    # 格式列表
    formats_parser = subparsers.add_parser('formats', help='查看可用格式')
    formats_parser.add_argument('url', help='视频URL')
    
    args = parser.parse_args()
    
    if not args.command:
        ytdlp_status = '[OK]' if check_ytdlp() else '[MISSING]'
        print('Video Catcher Pro - 超强视频下载技能 v2.0')
        print('=' * 50)
        print('Usage:')
        print('  m3u8 <url>    - Download M3U8 video')
        print('  analyze <url>  - Analyze video URL')
        print('  extract <url>  - Extract video from webpage')
        print('  ytdlp <url>   - Download with yt-dlp')
        print('  formats <url> - List available formats')
        print()
        print('Tools:')
        print(f'  yt-dlp: {ytdlp_status}')
        return
    
    if args.command == 'm3u8':
        headers = {'Referer': args.referer} if args.referer else None
        download_m3u8(args.url, args.output, headers)
    
    elif args.command == 'analyze':
        info = analyze_url(args.url)
        print(f"\n分析结果:")
        print(f"  平台: {info['platform']}")
        print(f"  类型: {info['type']}")
        print(f"  可下载: {'是' if info['downloadable'] else '否'}")
        print(f"  推荐方式: {info['recommend']}")
    
    elif args.command == 'extract':
        extract_from_webpage(args.url)
    
    elif args.command == 'ytdlp':
        download_with_ytdlp(args.url, args.output)
    
    elif args.command == 'formats':
        print(get_video_formats(args.url))


if __name__ == '__main__':
    main()
