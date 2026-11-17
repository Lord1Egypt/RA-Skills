"""平台路由器 — 自动识别链接所属平台并分发"""

from typing import Any, Dict, List, Optional

from .base import PlatformAdapter, PlatformMetadata, ShortVideoAnalysis
from .douyin import DouyinAdapter
from .kuaishou import KuaishouAdapter
from .bilibili import BilibiliAdapter
from .wechat_video import WechatVideoAdapter
from ..logger import get_logger

logger = get_logger(__name__)


class PlatformRouter:
    """
    平台路由器。
    
    自动识别用户输入的链接属于哪个平台，
    并返回对应的适配器进行处理。
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._adapters: Dict[str, PlatformAdapter] = {}
        self._init_adapters()
    
    def _init_adapters(self):
        """初始化所有平台适配器"""
        adapter_classes = [
            DouyinAdapter,
            KuaishouAdapter,
            BilibiliAdapter,
            WechatVideoAdapter,
        ]
        
        for cls in adapter_classes:
            try:
                adapter = cls(self.config)
                self._adapters[adapter.platform_name] = adapter
                logger.debug(f"初始化平台适配器: {adapter.platform_name}")
            except Exception as e:
                logger.warning(f"初始化适配器 {cls.__name__} 失败: {e}")
    
    def detect_platform(self, link: str) -> Optional[str]:
        """
        自动检测链接所属平台。
        
        Args:
            link: 用户输入的链接
            
        Returns:
            平台名称，无法识别返回 None
        """
        link = link.strip().lower()
        
        for name, adapter in self._adapters.items():
            for pattern in adapter.domain_patterns:
                if pattern.lower() in link:
                    logger.info(f"检测到平台: {name} (链接: {link[:50]}...)")
                    return name
        
        logger.warning(f"无法识别平台: {link[:50]}...")
        return None
    
    def get_adapter(self, platform: str) -> Optional[PlatformAdapter]:
        """
        获取指定平台的适配器。
        
        Args:
            platform: 平台名称
            
        Returns:
            PlatformAdapter 实例
        """
        return self._adapters.get(platform)
    
    def parse_link(self, link: str) -> Optional[tuple]:
        """
        解析链接，返回 (platform, video_id)。
        
        Args:
            link: 用户输入的链接
            
        Returns:
            (平台名称, 视频ID) 元组，解析失败返回 None
        """
        platform = self.detect_platform(link)
        if not platform:
            return None
        
        adapter = self.get_adapter(platform)
        if not adapter:
            return None
        
        video_id = adapter.parse_link(link)
        if video_id:
            return (platform, video_id)
        
        return None
    
    def download_video(
        self, platform: str, video_id: str, output_dir: str
    ) -> Optional[str]:
        """
        下载视频。
        
        Args:
            platform: 平台名称
            video_id: 视频ID
            output_dir: 输出目录
            
        Returns:
            下载后的本地文件路径
        """
        adapter = self.get_adapter(platform)
        if not adapter:
            logger.error(f"未找到平台适配器: {platform}")
            return None
        
        return adapter.download_video(video_id, output_dir)
    
    def extract_metadata(self, platform: str, video_id: str) -> Optional[PlatformMetadata]:
        """
        提取平台元数据。
        
        Args:
            platform: 平台名称
            video_id: 视频ID
            
        Returns:
            PlatformMetadata
        """
        adapter = self.get_adapter(platform)
        if not adapter:
            logger.error(f"未找到平台适配器: {platform}")
            return None
        
        return adapter.extract_metadata(video_id)
    
    def analyze_short_video(
        self,
        platform: str,
        video_path: str,
        metadata: PlatformMetadata,
        transcript: Dict = None,
        scenes: Dict = None,
    ) -> Optional[ShortVideoAnalysis]:
        """
        执行短视频特有分析。
        
        Args:
            platform: 平台名称
            video_path: 本地视频路径
            metadata: 平台元数据
            transcript: 语音识别结果
            scenes: 场景检测结果
            
        Returns:
            ShortVideoAnalysis
        """
        adapter = self.get_adapter(platform)
        if not adapter:
            logger.error(f"未找到平台适配器: {platform}")
            return None
        
        return adapter.analyze_short_video(video_path, metadata, transcript, scenes)
    
    def list_supported_platforms(self) -> List[str]:
        """列出所有支持的平台"""
        return list(self._adapters.keys())
    
    def is_supported(self, link: str) -> bool:
        """检查链接是否受支持"""
        return self.detect_platform(link) is not None
