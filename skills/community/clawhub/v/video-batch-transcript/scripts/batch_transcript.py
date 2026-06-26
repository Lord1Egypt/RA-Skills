#!/usr/bin/env python3
"""
Video Batch Transcript - 通用视频批量转录工具

支持 1000+ yt-dlp 兼容网站（B 站、YouTube、抖音、Twitch 等）
批量下载视频音频，GPU 加速转录，生成结构化学习笔记

用法:
    python batch_transcript.py --url "视频 URL" --output-dir "~/notes"
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple
import re

# 尝试导入依赖
try:
    import yt_dlp
    YTDLP_AVAILABLE = True
except ImportError:
    YTDLP_AVAILABLE = False
    print("错误：yt-dlp 未安装，请运行：pip install yt-dlp")
    sys.exit(1)

try:
    from faster_whisper import WhisperModel
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("错误：faster-whisper 未安装，请运行：pip install faster-whisper")
    sys.exit(1)

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


class VideoBatchTranscript:
    """通用视频批量转录处理器"""
    
    # 网站配置
    SITE_CONFIGS = {
        'youtube': {
            'name': 'YouTube',
            'patterns': ['youtube.com', 'youtu.be', 'youtube-nocookie.com'],
            'requires_cookies': False,  # 推荐但不强制
            'default_format': 'bestaudio',
            'notes': '建议使用 cookies 避免 403 错误'
        },
        'bilibili': {
            'name': '哔哩哔哩',
            'patterns': ['bilibili.com', 'b23.tv'],
            'requires_cookies': False,
            'default_format': 'bestaudio',
            'notes': '部分合集需要登录'
        },
        'douyin': {
            'name': '抖音',
            'patterns': ['douyin.com', 'iesdouyin.com'],
            'requires_cookies': True,
            'default_format': 'bestaudio',
            'notes': '通常需要 cookies'
        },
        'tiktok': {
            'name': 'TikTok',
            'patterns': ['tiktok.com'],
            'requires_cookies': False,
            'default_format': 'bestaudio',
            'notes': ''
        },
        'twitch': {
            'name': 'Twitch',
            'patterns': ['twitch.tv'],
            'requires_cookies': False,
            'default_format': 'bestaudio',
            'notes': '视频和直播回放'
        },
        'vimeo': {
            'name': 'Vimeo',
            'patterns': ['vimeo.com'],
            'requires_cookies': False,
            'default_format': 'bestaudio',
            'notes': ''
        },
        'instagram': {
            'name': 'Instagram',
            'patterns': ['instagram.com'],
            'requires_cookies': True,
            'default_format': 'bestaudio',
            'notes': '需要 cookies'
        },
        'twitter': {
            'name': 'Twitter/X',
            'patterns': ['twitter.com', 'x.com'],
            'requires_cookies': False,
            'default_format': 'bestaudio',
            'notes': ''
        },
        'netflix': {
            'name': 'Netflix',
            'patterns': ['netflix.com'],
            'requires_cookies': True,
            'default_format': 'bestaudio',
            'notes': '必须提供 cookies 文件'
        },
        'coursera': {
            'name': 'Coursera',
            'patterns': ['coursera.org'],
            'requires_cookies': True,
            'default_format': 'bestaudio',
            'notes': '需要登录'
        },
        'udemy': {
            'name': 'Udemy',
            'patterns': ['udemy.com'],
            'requires_cookies': True,
            'default_format': 'bestaudio',
            'notes': '需要登录'
        },
        'ted': {
            'name': 'TED',
            'patterns': ['ted.com'],
            'requires_cookies': False,
            'default_format': 'bestaudio',
            'notes': ''
        },
        'soundcloud': {
            'name': 'SoundCloud',
            'patterns': ['soundcloud.com'],
            'requires_cookies': False,
            'default_format': 'bestaudio',
            'notes': ''
        },
    }
    
    # 内置术语表
    DEFAULT_TERMINOLOGY = {
        "机器学习": ["机器学习", "ML", "Machine Learning"],
        "深度学习": ["深度学习", "DL", "Deep Learning"],
        "神经网络": ["神经网络", "NN", "Neural Network"],
        "Transformer": ["Transformer", "transformer"],
        "CUDA": ["CUDA", "cuda"],
        "GPU": ["GPU", "gpu", "显卡"],
        "CPU": ["CPU", "cpu", "处理器"],
        "API": ["API", "api", "Api"],
        "Python": ["Python", "python"],
        "GitHub": ["GitHub", "github"],
    }
    
    def __init__(
        self,
        output_dir: str = "~/video-notes",
        model_size: str = "small",
        device: str = "auto",
        language: str = "auto",
        compute_type: str = "float16",
        terminology_file: Optional[str] = None,
        workers: int = 1,
        cookies_from_browser: Optional[str] = None,
        cookies_file: Optional[str] = None,
        video_format: str = "bestaudio"
    ):
        """
        初始化处理器
        
        Args:
            output_dir: 输出目录
            model_size: Whisper 模型大小
            device: 设备 (cuda/cpu/auto)
            language: 语言代码 (auto 表示自动检测)
            compute_type: 计算类型
            terminology_file: 自定义术语表文件路径
            workers: 并行工作进程数
            cookies_from_browser: 从浏览器获取 cookies
            cookies_file: cookies 文件路径
            video_format: 视频/音频格式选择
        """
        self.output_dir = Path(output_dir).expanduser()
        self.model_size = model_size
        self.language = language if language != "auto" else None
        self.compute_type = compute_type
        self.workers = workers
        self.cookies_from_browser = cookies_from_browser
        self.cookies_file = cookies_file
        self.video_format = video_format
        
        # 确定设备
        if device == "auto":
            self.device = "cuda" if (TORCH_AVAILABLE and torch.cuda.is_available()) else "cpu"
        else:
            self.device = device
            
        print(f"使用设备：{self.device}")
        if self.device == "cuda":
            if TORCH_AVAILABLE and torch.cuda.is_available():
                print(f"GPU: {torch.cuda.get_device_name(0)}")
        
        # 加载术语表
        self.terminology = self.DEFAULT_TERMINOLOGY.copy()
        if terminology_file and Path(terminology_file).exists():
            with open(terminology_file, 'r', encoding='utf-8') as f:
                custom_terms = json.load(f)
                self.terminology.update(custom_terms)
            print(f"已加载自定义术语表：{terminology_file}")
        
        # 初始化 Whisper 模型
        self.model = None
        if WHISPER_AVAILABLE:
            print(f"正在加载 Whisper 模型：{model_size}...")
            self.model = WhisperModel(
                model_size,
                device=self.device,
                compute_type=self.compute_type
            )
            print("模型加载完成")
        
        # 创建输出目录
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"输出目录：{self.output_dir}")
    
    def detect_site(self, url: str) -> Optional[Dict[str, Any]]:
        """
        检测视频来源网站
        
        Args:
            url: 视频 URL
            
        Returns:
            网站配置信息，未知网站返回 None
        """
        for site_id, config in self.SITE_CONFIGS.items():
            for pattern in config['patterns']:
                if pattern in url:
                    return {
                        'id': site_id,
                        **config
                    }
        return None
    
    def get_ydl_opts(self, url: str, output_template: str) -> Dict[str, Any]:
        """
        获取 yt-dlp 配置选项
        
        Args:
            url: 视频 URL
            output_template: 输出文件模板
            
        Returns:
            yt-dlp 配置字典
        """
        site_info = self.detect_site(url)
        
        opts = {
            'format': self.video_format,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': output_template,
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        # Cookies 配置
        if self.cookies_from_browser:
            opts['cookiesfrombrowser'] = (self.cookies_from_browser,)
            print(f"使用浏览器 cookies: {self.cookies_from_browser}")
        elif self.cookies_file:
            if Path(self.cookies_file).exists():
                opts['cookiefile'] = self.cookies_file
                print(f"使用 cookies 文件：{self.cookies_file}")
            else:
                print(f"警告：cookies 文件不存在：{self.cookies_file}")
        
        # 网站特定优化
        if site_info:
            print(f"检测到网站：{site_info['name']}")
            if site_info['notes']:
                print(f"提示：{site_info['notes']}")
            
            # YouTube 特别处理
            if site_info['id'] == 'youtube':
                # 优先使用 cookies
                if not self.cookies_from_browser and not self.cookies_file:
                    print("提示：YouTube 建议使用 --cookies-from-browser chrome 避免 403 错误")
        
        return opts
    
    def get_collection_info(self, url: str) -> Dict[str, Any]:
        """
        获取合集/视频信息
        
        Args:
            url: 视频或合集 URL
            
        Returns:
            信息字典
        """
        print(f"正在获取信息：{url}")
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': 'in_playlist',  # 快速获取列表
        }
        
        # 添加 cookies 配置
        if self.cookies_from_browser:
            ydl_opts['cookiesfrombrowser'] = (self.cookies_from_browser,)
        elif self.cookies_file and Path(self.cookies_file).exists():
            ydl_opts['cookiefile'] = self.cookies_file
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # 检测是否为合集/播放列表
            is_playlist = info.get('_type') in ['playlist', 'tab'] or 'entries' in info
            
            collection_info = {
                'title': info.get('title', '未命名'),
                'uploader': info.get('uploader', info.get('channel', '未知')),
                'url': url,
                'site': self.detect_site(url),
                'is_playlist': is_playlist,
                'entries': []
            }
            
            # 处理视频列表
            entries = info.get('entries', [])
            if entries:
                for idx, entry in enumerate(entries, 1):
                    if entry:  # 跳过无效条目
                        collection_info['entries'].append({
                            'index': idx,
                            'id': entry.get('id', ''),
                            'title': entry.get('title', f'视频{idx}'),
                            'url': entry.get('url', entry.get('webpage_url', '')),
                            'duration': entry.get('duration', 0),
                            'uploader': entry.get('uploader', collection_info['uploader'])
                        })
            else:
                # 单个视频
                collection_info['entries'].append({
                    'index': 1,
                    'id': info.get('id', ''),
                    'title': info.get('title', '未命名'),
                    'url': url,
                    'duration': info.get('duration', 0),
                    'uploader': collection_info['uploader']
                })
            
            print(f"共 {len(collection_info['entries'])} 个视频")
            return collection_info
    
    def download_audio(self, video_url: str, output_path: Path) -> Optional[Path]:
        """
        下载视频音频
        
        Args:
            video_url: 视频 URL
            output_path: 输出路径
            
        Returns:
            音频文件路径，失败返回 None
        """
        # 检查是否已存在
        expected_path = output_path.with_suffix('.mp3')
        if expected_path.exists():
            print(f"音频已存在，跳过：{expected_path}")
            return expected_path
        
        print(f"正在下载音频：{video_url}")
        
        ydl_opts = self.get_ydl_opts(
            video_url,
            str(output_path.with_suffix(''))
        )
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            
            # 确认文件已创建
            if expected_path.exists():
                print(f"音频下载完成：{expected_path}")
                return expected_path
            else:
                # 尝试查找其他可能的位置
                for ext in ['.mp3', '.m4a', '.webm', '.opus']:
                    alt_path = output_path.with_suffix(ext)
                    if alt_path.exists():
                        print(f"音频下载完成：{alt_path}")
                        return alt_path
                
                print(f"警告：音频文件未找到")
                return None
        except Exception as e:
            print(f"下载失败：{e}")
            return None
    
    def transcribe_audio(self, audio_path: Path) -> Tuple[List[Dict[str, Any]], str]:
        """
        转录音频
        
        Args:
            audio_path: 音频文件路径
            
        Returns:
            (转录结果，检测到的语言)
        """
        if not self.model:
            raise RuntimeError("Whisper 模型未初始化")
        
        print(f"正在转录：{audio_path.name}")
        
        segments, info = self.model.transcribe(
            str(audio_path),
            language=self.language,
            vad_filter=True,
            vad_parameters=dict(
                min_silence_duration_ms=500,
                speech_pad_ms=200
            )
        )
        
        detected_language = info.language
        print(f"检测语言：{detected_language} (概率：{info.language_probability:.2f})")
        
        results = []
        for segment in segments:
            results.append({
                'start': segment.start,
                'end': segment.end,
                'text': segment.text.strip()
            })
        
        print(f"转录完成，共 {len(results)} 段")
        return results, detected_language
    
    def correct_terminology(self, text: str) -> str:
        """校正专业术语"""
        corrected = text
        for standard, variants in self.terminology.items():
            for variant in variants:
                if variant != standard and variant in corrected:
                    corrected = corrected.replace(variant, standard)
        return corrected
    
    def format_timestamp(self, seconds: float) -> str:
        """格式化时间戳为 MM:SS"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
    
    def generate_notes(
        self,
        video_info: Dict[str, Any],
        transcript: List[Dict[str, Any]],
        detected_language: str
    ) -> str:
        """生成结构化笔记"""
        title = video_info.get('title', '未命名')
        duration = video_info.get('duration', 0)
        uploader = video_info.get('uploader', '未知')
        url = video_info.get('url', '')
        site_info = video_info.get('site', {})
        site_name = site_info.get('name', '未知网站') if site_info else '未知网站'
        
        # 合并所有文本
        full_text = ' '.join([seg['text'] for seg in transcript])
        corrected_text = self.correct_terminology(full_text)
        
        # 生成时间轴摘要
        timeline = []
        for seg in transcript[:20]:
            timeline.append(f"- **{self.format_timestamp(seg['start'])}** - {seg['text'][:50]}...")
        
        notes = f"""# {title}

## 基本信息
- **来源**: {site_name}
- **UP 主/频道**: {uploader}
- **时长**: {self.format_timestamp(duration)}
- **语言**: {detected_language}
- **处理日期**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
- **视频链接**: {url}

## 完整转录

{corrected_text}

## 时间轴摘要

{chr(10).join(timeline)}

## 关键内容

> 待人工整理核心观点、知识点和行动项

---
*本笔记由 video-batch-transcript 自动生成*
"""
        return notes
    
    def save_metadata(
        self,
        video_info: Dict[str, Any],
        detected_language: str,
        output_path: Path
    ):
        """保存元数据"""
        site_info = video_info.get('site', {})
        
        metadata = {
            'title': video_info.get('title'),
            'uploader': video_info.get('uploader'),
            'url': video_info.get('url'),
            'site': site_info.get('name') if site_info else 'unknown',
            'site_id': site_info.get('id') if site_info else 'unknown',
            'duration': video_info.get('duration'),
            'language': detected_language,
            'processed_at': datetime.now().isoformat(),
            'model': self.model_size,
            'device': self.device,
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    def process_video(
        self,
        video_info: Dict[str, Any],
        episode_dir: Path,
        resume: bool = True
    ) -> bool:
        """处理单个视频"""
        title = video_info.get('title', '未命名')
        url = video_info.get('url', '')
        index = video_info.get('index', 0)
        
        # 创建视频目录
        episode_dir.mkdir(parents=True, exist_ok=True)
        
        # 检查是否已处理
        notes_file = episode_dir / f"{index:03d}_{title[:50]}.md"
        metadata_file = episode_dir / "metadata.json"
        
        if resume and notes_file.exists() and metadata_file.exists():
            print(f"视频已处理，跳过：{title}")
            return True
        
        # 下载音频
        audio_file = episode_dir / f"{index:03d}_audio"
        audio_path = self.download_audio(url, audio_file)
        
        if not audio_path:
            print(f"音频下载失败：{title}")
            return False
        
        # 转录
        try:
            transcript, detected_language = self.transcribe_audio(audio_path)
        except Exception as e:
            print(f"转录失败：{e}")
            return False
        
        # 生成笔记
        notes = self.generate_notes(video_info, transcript, detected_language)
        
        # 保存笔记
        with open(notes_file, 'w', encoding='utf-8') as f:
            f.write(notes)
        
        # 保存元数据
        self.save_metadata(video_info, detected_language, metadata_file)
        
        # 保存原始转录
        transcript_file = episode_dir / f"{index:03d}_transcript.txt"
        with open(transcript_file, 'w', encoding='utf-8') as f:
            for seg in transcript:
                f.write(f"[{self.format_timestamp(seg['start'])}] {seg['text']}\n")
        
        print(f"处理完成：{title}")
        return True
    
    def process_collection(
        self,
        url: str,
        episodes: Optional[str] = None,
        resume: bool = True
    ):
        """处理整个合集"""
        # 获取合集信息
        collection_info = self.get_collection_info(url)
        collection_title = collection_info['title']
        site_info = collection_info.get('site', {})
        
        # 创建合集目录
        site_name = site_info.get('id', 'unknown') if site_info else 'unknown'
        collection_dir = self.output_dir / f"{site_name}_{collection_title[:50]}"
        collection_dir.mkdir(parents=True, exist_ok=True)
        
        # 筛选集数
        entries = collection_info['entries']
        if episodes:
            selected_indices = self._parse_episode_range(episodes, len(entries))
            entries = [e for e in entries if e['index'] in selected_indices]
            print(f"已筛选：{len(entries)} 个视频")
        
        # 处理每个视频
        success_count = 0
        for entry in entries:
            episode_dir = collection_dir / f"{entry['index']:03d}_{entry['title'][:30]}"
            
            if self.process_video(entry, episode_dir, resume):
                success_count += 1
        
        # 生成合集汇总
        self._generate_collection_summary(collection_info, collection_dir)
        
        print(f"\n处理完成：{success_count}/{len(entries)} 个视频成功")
        print(f"输出目录：{collection_dir}")
    
    def _parse_episode_range(self, range_str: str, total: int) -> List[int]:
        """解析集数范围字符串"""
        indices = set()
        for part in range_str.split(','):
            part = part.strip()
            if '-' in part:
                start, end = map(int, part.split('-'))
                indices.update(range(start, min(end + 1, total + 1)))
            else:
                idx = int(part)
                if idx <= total:
                    indices.add(idx)
        return sorted(list(indices))
    
    def _generate_collection_summary(
        self,
        collection_info: Dict[str, Any],
        collection_dir: Path
    ):
        """生成合集汇总笔记"""
        summary_file = collection_dir / "合集汇总.md"
        
        site_info = collection_info.get('site', {})
        site_name = site_info.get('name', '未知网站') if site_info else '未知网站'
        
        entries = collection_info['entries']
        video_links = []
        for entry in entries:
            video_links.append(
                f"{entry['index']:03d}. [{entry['title']}]({entry['url']})"
            )
        
        summary = f"""# {collection_info['title']} - 合集汇总

## 基本信息
- **来源网站**: {site_name}
- **UP 主/频道**: {collection_info['uploader']}
- **视频数量**: {len(entries)}
- **处理日期**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
- **合集链接**: {collection_info['url']}

## 视频列表

{chr(10).join(video_links)}

## 使用说明

每个视频的笔记位于对应的子目录中，包含：
- `*.md` - 结构化笔记
- `*_transcript.txt` - 原始转录文本
- `metadata.json` - 元数据
- `*_audio.mp3` - 音频文件

---
*本汇总由 video-batch-transcript 自动生成*
"""
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)


def check_environment():
    """检查环境依赖"""
    print("=" * 50)
    print("Video Batch Transcript - 环境检查")
    print("=" * 50)
    print()
    
    # Python 版本
    print(f"Python: {sys.version.split()[0]}")
    
    # yt-dlp
    if YTDLP_AVAILABLE:
        print("✓ yt-dlp: 已安装")
    else:
        print("✗ yt-dlp: 未安装 (pip install yt-dlp)")
    
    # faster-whisper
    if WHISPER_AVAILABLE:
        print("✓ faster-whisper: 已安装")
        if TORCH_AVAILABLE and torch.cuda.is_available():
            print(f"✓ CUDA: 可用 ({torch.cuda.get_device_name(0)})")
        else:
            print("○ CUDA: 不可用 (将使用 CPU)")
    else:
        print("✗ faster-whisper: 未安装 (pip install faster-whisper)")
    
    # ffmpeg
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✓ ffmpeg: 已安装")
        else:
            print("✗ ffmpeg: 未安装")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("✗ ffmpeg: 未安装 (需要安装以处理音频)")
    
    print()
    print("支持网站：YouTube, B 站，抖音，Twitch, Vimeo, Instagram, Twitter/X, Netflix 等 1000+ 网站")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(
        description='通用视频批量转录工具 - 支持 1000+ 网站',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
支持的网站:
  - 国内：哔哩哔哩、抖音、快手、西瓜视频、腾讯视频等
  - 国际：YouTube, Vimeo, Dailymotion, Twitch, Twitter/X, Instagram, TikTok 等
  - 流媒体：Netflix, Hulu, HBO, Disney+ (需登录)
  - 音频：SoundCloud, Bandcamp, Spotify (需登录)
  - 教育：Coursera, edX, Udemy, Khan Academy, TED
  完整列表：https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

示例:
  # YouTube 视频
  python batch_transcript.py --url "https://youtube.com/watch?v=xxx"
  
  # B 站合集
  python batch_transcript.py --url "https://space.bilibili.com/xxx/collectiondetail?sid=xxx"
  
  # 使用 GPU 加速
  python batch_transcript.py --url "xxx" --device cuda
  
  # 使用浏览器 cookies (推荐用于 YouTube/抖音等)
  python batch_transcript.py --url "xxx" --cookies-from-browser chrome
  
  # 处理指定集数
  python batch_transcript.py --url "xxx" --episodes "1-5,8,10"
        """
    )
    
    parser.add_argument('--url', type=str, required=True, help='视频或合集 URL')
    parser.add_argument('--output-dir', type=str, default='~/video-notes', help='输出目录')
    parser.add_argument('--episodes', type=str, help='指定集数 (e.g., "1-5,8,10")')
    parser.add_argument('--model', type=str, default='small', 
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help='Whisper 模型大小')
    parser.add_argument('--device', type=str, default='auto',
                       choices=['auto', 'cuda', 'cpu'],
                       help='处理设备')
    parser.add_argument('--language', type=str, default='auto', 
                       help='语言代码 (auto=自动检测)')
    parser.add_argument('--format', type=str, default='bestaudio', help='视频/音频格式')
    parser.add_argument('--cookies-from-browser', type=str, 
                       choices=['chrome', 'firefox', 'safari', 'edge', 'brave', 'opera'],
                       help='从浏览器获取 cookies')
    parser.add_argument('--cookies', type=str, help='cookies 文件路径')
    parser.add_argument('--terminology', type=str, help='自定义术语表文件')
    parser.add_argument('--workers', type=int, default=1, help='并行工作进程数')
    parser.add_argument('--no-resume', action='store_true', help='禁用断点续传')
    parser.add_argument('--check-env', action='store_true', help='仅检查环境')
    
    args = parser.parse_args()
    
    # 环境检查
    if args.check_env:
        check_environment()
        return
    
    # 创建处理器并处理
    processor = VideoBatchTranscript(
        output_dir=args.output_dir,
        model_size=args.model,
        device=args.device,
        language=args.language,
        terminology_file=args.terminology,
        workers=args.workers,
        cookies_from_browser=args.cookies_from_browser,
        cookies_file=args.cookies,
        video_format=args.format
    )
    
    processor.process_collection(
        url=args.url,
        episodes=args.episodes,
        resume=not args.no_resume
    )


if __name__ == '__main__':
    main()
