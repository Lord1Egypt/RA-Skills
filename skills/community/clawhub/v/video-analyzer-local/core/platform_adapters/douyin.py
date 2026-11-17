"""抖音平台适配器"""

import json
import os
import re
import subprocess
import tempfile
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from .base import PlatformAdapter, PlatformMetadata, ShortVideoAnalysis
from ..logger import get_logger

logger = get_logger(__name__)


class DouyinAdapter(PlatformAdapter):
    """
    抖音平台适配器。
    
    功能：
    - 支持分享链接解析
    - 支持 yt-dlp 下载
    - 支持元数据提取
    - 支持黄金前3秒分析
    """
    
    # 抖音分享链接正则
    DOUYIN_PATTERNS = [
        r'v\.douyin\.com/([A-Za-z0-9]+)',
        r'douyin\.com/video/(\d+)',
        r'douyin\.com/user/.*',
        r'iesdouyin\.com/share/video/(\d+)',
    ]
    
    @property
    def platform_name(self) -> str:
        return "douyin"
    
    @property
    def domain_patterns(self) -> List[str]:
        return [
            "v.douyin.com",
            "www.douyin.com",
            "www.iesdouyin.com",
            "m.douyin.com",
        ]
    
    def parse_link(self, link: str) -> Optional[str]:
        """解析抖音链接"""
        link = link.strip()
        
        # 尝试匹配各种模式
        for pattern in self.DOUYIN_PATTERNS:
            match = re.search(pattern, link)
            if match:
                video_id = match.group(1)
                logger.info(f"解析抖音视频ID: {video_id}")
                return video_id
        
        # 尝试从短链接提取
        if "v.douyin.com" in link:
            return self._resolve_short_link(link)
        
        logger.warning(f"无法解析抖音链接: {link}")
        return None
    
    def _resolve_short_link(self, short_link: str) -> Optional[str]:
        """解析抖音短链接"""
        try:
            import urllib.request
            req = urllib.request.Request(
                short_link,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
            )
            # 获取重定向URL
            with urllib.request.urlopen(req, timeout=10) as resp:
                final_url = resp.geturl()
                # 从最终URL提取视频ID
                for pattern in self.DOUYIN_PATTERNS:
                    match = re.search(pattern, final_url)
                    if match:
                        return match.group(1)
        except Exception as e:
            logger.debug(f"短链接解析失败: {e}")
        return None
    
    def download_video(self, video_id: str, output_dir: str) -> Optional[str]:
        """使用 yt-dlp 下载抖音视频"""
        os.makedirs(output_dir, exist_ok=True)
        
        # 抖音视频链接
        video_url = f"https://www.douyin.com/video/{video_id}"
        output_path = os.path.join(output_dir, f"douyin_{video_id}.mp4")
        
        if os.path.exists(output_path):
            logger.info(f"视频已存在: {output_path}")
            return output_path
        
        # 使用 yt-dlp 下载
        cmd = [
            "yt-dlp",
            "-o", output_path,
            "--no-check-certificates",
            "--quiet",
            "--no-warnings",
            video_url,
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=300)
            if result.returncode == 0 and os.path.exists(output_path):
                logger.info(f"抖音视频下载成功: {output_path}")
                return output_path
            else:
                logger.error(f"抖音视频下载失败: {result.stderr.decode()}")
                return None
        except subprocess.TimeoutExpired:
            logger.error("下载超时")
            return None
        except FileNotFoundError:
            logger.error("yt-dlp 未安装，请执行: pip install yt-dlp")
            return None
        except Exception as e:
            logger.error(f"下载失败: {e}")
            return None
    
    def extract_metadata(self, video_id: str) -> PlatformMetadata:
        """提取抖音视频元数据"""
        metadata = PlatformMetadata(platform=self.platform_name, video_id=video_id)
        
        # 使用 yt-dlp 获取元数据
        video_url = f"https://www.douyin.com/video/{video_id}"
        
        cmd = [
            "yt-dlp",
            "--dump-json",
            "--no-download",
            "--no-check-certificates",
            "--quiet",
            video_url,
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0 and result.stdout:
                data = json.loads(result.stdout)
                
                metadata.title = data.get("title", "")
                metadata.description = data.get("description", "")
                metadata.tags = data.get("tags", [])
                metadata.duration = data.get("duration", 0)
                metadata.width = data.get("width", 0)
                metadata.height = data.get("height", 0)
                metadata.cover_url = data.get("thumbnail", "")
                metadata.author = data.get("uploader", "")
                metadata.author_id = data.get("uploader_id", "")
                metadata.publish_time = data.get("upload_date", "")
                metadata.like_count = data.get("like_count", 0)
                metadata.comment_count = data.get("comment_count", 0)
                metadata.share_count = data.get("repost_count", 0)
                metadata.view_count = data.get("view_count", 0)
                metadata.download_url = data.get("url", "")
                metadata.raw_metadata = data
                
        except Exception as e:
            logger.debug(f"元数据提取失败: {e}")
        
        return metadata
    
    def analyze_short_video(
        self,
        video_path: str,
        metadata: PlatformMetadata,
        transcript: Dict = None,
        scenes: Dict = None,
    ) -> ShortVideoAnalysis:
        """执行抖音短视频特有分析"""
        analysis = ShortVideoAnalysis()
        
        # 1. 黄金前3秒分析
        analysis.opening_3s = self._analyze_opening_3s(video_path, transcript)
        
        # 2. 完播率因素分析
        analysis.completion_factors = self._analyze_completion_factors(
            metadata, transcript, scenes
        )
        
        # 3. 带货分析
        analysis.ecommerce_analysis = self._analyze_ecommerce(transcript)
        
        # 4. 节奏分析
        analysis.rhythm_analysis = self._analyze_rhythm(scenes)
        
        return analysis
    
    def _analyze_opening_3s(
        self, video_path: str, transcript: Dict = None
    ) -> Dict:
        """分析黄金前3秒"""
        result = {
            "has_hook": False,
            "hook_type": "",
            "opening_text": "",
            "visual_changes": 0,
            "audio_energy": 0,
        }
        
        if not video_path or not os.path.exists(video_path):
            return result
        
        try:
            import cv2
            import numpy as np
            
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return result
            
            fps = cap.get(cv2.CAP_PROP_FPS) or 30
            frames_3s = int(fps * 3)
            
            prev_frame = None
            visual_changes = 0
            
            for i in range(min(frames_3s, 90)):  # 最多取90帧
                ret, frame = cap.read()
                if not ret:
                    break
                
                if prev_frame is not None:
                    # 计算帧间差异
                    diff = cv2.absdiff(prev_frame, frame)
                    mean_diff = np.mean(diff)
                    if mean_diff > 30:  # 阈值
                        visual_changes += 1
                
                prev_frame = frame
            
            cap.release()
            
            result["visual_changes"] = visual_changes
            result["has_hook"] = visual_changes > 5  # 前3秒画面变化大 = 有hook
            
            # 判断hook类型
            if visual_changes > 10:
                result["hook_type"] = "视觉冲击"
            elif visual_changes > 5:
                result["hook_type"] = "画面变化"
            else:
                result["hook_type"] = "平稳开场"
            
            # 提取前3秒文本
            if transcript:
                for seg in transcript.get("segments", []):
                    if seg.get("start", 0) <= 3.0:
                        result["opening_text"] += seg.get("text", "")
            
        except Exception as e:
            logger.debug(f"前3秒分析失败: {e}")
        
        return result
    
    def _analyze_completion_factors(
        self,
        metadata: PlatformMetadata,
        transcript: Dict = None,
        scenes: Dict = None,
    ) -> Dict:
        """分析完播率相关因素"""
        factors = {
            "video_length_score": 0,
            "content_density": 0,
            "has_call_to_action": False,
            "has_suspense": False,
            "rhythm_score": 0,
        }
        
        # 视频时长评分（抖音最佳时长15-60秒）
        duration = metadata.duration
        if 15 <= duration <= 60:
            factors["video_length_score"] = 100
        elif duration < 15:
            factors["video_length_score"] = 80
        elif duration <= 90:
            factors["video_length_score"] = 70
        else:
            factors["video_length_score"] = 50
        
        # 内容密度（对话覆盖率）
        if transcript:
            total_dialog = sum(
                seg.get("end", 0) - seg.get("start", 0)
                for seg in transcript.get("segments", [])
            )
            if duration > 0:
                factors["content_density"] = round(total_dialog / duration, 2)
        
        # 是否有行动号召
        if transcript:
            full_text = transcript.get("text", "")
            cta_keywords = ["关注", "点赞", "评论", "转发", "分享", "点击", "链接"]
            factors["has_call_to_action"] = any(kw in full_text for kw in cta_keywords)
        
        # 是否有悬念
        if transcript:
            full_text = transcript.get("text", "")
            suspense_keywords = ["但是", "然而", "竟然", "原来", "没想到", "秘密"]
            factors["has_suspense"] = any(kw in full_text for kw in suspense_keywords)
        
        # 节奏评分
        if scenes:
            scene_count = scenes.get("total_scenes", 0)
            if duration > 0:
                scene_rate = scene_count / duration
                # 抖音最佳节奏：每秒0.2-0.5个场景切换
                if 0.2 <= scene_rate <= 0.5:
                    factors["rhythm_score"] = 100
                elif scene_rate > 0.5:
                    factors["rhythm_score"] = 80
                else:
                    factors["rhythm_score"] = 60
        
        return factors
    
    def _analyze_ecommerce(self, transcript: Dict = None) -> Dict:
        """分析带货特征"""
        result = {
            "is_ecommerce": False,
            "products": [],
            "price_mentions": [],
            "promotion_keywords": [],
            "call_to_action": [],
        }
        
        if not transcript:
            return result
        
        full_text = transcript.get("text", "")
        
        # 带货关键词
        ecommerce_keywords = [
            "购买", "下单", "链接", "优惠", "折扣", "包邮", "限时",
            "秒杀", "特价", "原价", "现价", "到手", "福利", "抽奖",
            "免费", "赠送", "福利价", "专属价", "粉丝价",
        ]
        
        for kw in ecommerce_keywords:
            if kw in full_text:
                result["promotion_keywords"].append(kw)
        
        # 价格识别
        price_pattern = r'(\d+\.?\d*)\s*(元|块|RMB|￥|\$)'
        prices = re.findall(price_pattern, full_text)
        result["price_mentions"] = [f"{p[0]}{p[1]}" for p in prices]
        
        # 行动号召
        cta_patterns = ["点击链接", "评论区", "私信", "关注我", "下单"]
        for cta in cta_patterns:
            if cta in full_text:
                result["call_to_action"].append(cta)
        
        # 判断是否带货视频
        result["is_ecommerce"] = (
            len(result["promotion_keywords"]) >= 2 or
            len(result["price_mentions"]) > 0
        )
        
        return result
    
    def _analyze_rhythm(self, scenes: Dict = None) -> Dict:
        """分析视频节奏"""
        result = {
            "scene_count": 0,
            "avg_scene_duration": 0,
            "rhythm_type": "unknown",
        }
        
        if not scenes:
            return result
        
        scene_list = scenes.get("scenes", [])
        result["scene_count"] = len(scene_list)
        
        if scene_list:
            durations = [s.get("duration", 0) for s in scene_list]
            result["avg_scene_duration"] = round(sum(durations) / len(durations), 2)
            
            if result["avg_scene_duration"] < 3:
                result["rhythm_type"] = "快节奏"
            elif result["avg_scene_duration"] < 8:
                result["rhythm_type"] = "中等节奏"
            else:
                result["rhythm_type"] = "慢节奏"
        
        return result
