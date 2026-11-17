"""平台适配器抽象基类"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PlatformMetadata:
    """平台视频元数据"""
    platform: str = ""           # douyin/kuaishou/bilibili/wechat_video
    video_id: str = ""
    title: str = ""
    description: str = ""
    tags: List[str] = field(default_factory=list)
    duration: float = 0.0
    width: int = 0
    height: int = 0
    cover_url: str = ""
    author: str = ""
    author_id: str = ""
    publish_time: str = ""
    like_count: int = 0
    comment_count: int = 0
    share_count: int = 0
    view_count: int = 0
    collect_count: int = 0       # B站收藏/抖音收藏
    danmaku_count: int = 0       # B站弹幕
    music_title: str = ""         # 抖音/BGM
    music_author: str = ""
    video_url: str = ""
    download_url: str = ""
    is_downloadable: bool = True
    raw_metadata: Dict = field(default_factory=dict)


@dataclass
class ShortVideoAnalysis:
    """短视频特有分析结果"""
    # 黄金前3秒分析
    opening_3s: Dict = field(default_factory=dict)
    # 完播率相关因素
    completion_factors: Dict = field(default_factory=dict)
    # 评论区关键词
    comment_keywords: List[Dict] = field(default_factory=list)
    # 带货分析
    ecommerce_analysis: Dict = field(default_factory=dict)
    # 节奏分析
    rhythm_analysis: Dict = field(default_factory=dict)


class PlatformAdapter(ABC):
    """
    短视频平台适配器抽象基类。
    
    每个平台适配器负责：
    1. 解析视频链接/ID
    2. 下载视频（通过 yt-dlp 或专用API）
    3. 提取平台特有元数据
    4. 执行短视频特有分析
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.platform_config = config.get("platform_adapters", {})
        self._downloader = None
    
    @property
    @abstractmethod
    def platform_name(self) -> str:
        """平台名称"""
        pass
    
    @property
    @abstractmethod
    def domain_patterns(self) -> List[str]:
        """支持的域名模式（用于链接识别）"""
        pass
    
    @abstractmethod
    def parse_link(self, link: str) -> Optional[str]:
        """
        解析平台链接，返回视频ID。
        
        Args:
            link: 用户输入的链接（可能是短链、分享链接等）
            
        Returns:
            视频ID，解析失败返回 None
        """
        pass
    
    @abstractmethod
    def download_video(self, video_id: str, output_dir: str) -> Optional[str]:
        """
        下载视频到本地。
        
        Args:
            video_id: 视频ID
            output_dir: 输出目录
            
        Returns:
            下载后的本地文件路径
        """
        pass
    
    @abstractmethod
    def extract_metadata(self, video_id: str) -> PlatformMetadata:
        """
        提取平台特有元数据。
        
        Args:
            video_id: 视频ID
            
        Returns:
            PlatformMetadata
        """
        pass
    
    @abstractmethod
    def analyze_short_video(
        self,
        video_path: str,
        metadata: PlatformMetadata,
        transcript: Dict = None,
        scenes: Dict = None,
    ) -> ShortVideoAnalysis:
        """
        执行短视频特有分析。
        
        Args:
            video_path: 本地视频路径
            metadata: 平台元数据
            transcript: 语音识别结果
            scenes: 场景检测结果
            
        Returns:
            ShortVideoAnalysis
        """
        pass
    
    def get_platform_config(self, key: str, default=None):
        """获取平台特有配置"""
        return self.platform_config.get(self.platform_name, {}).get(key, default)
