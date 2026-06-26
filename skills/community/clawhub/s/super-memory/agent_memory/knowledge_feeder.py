from __future__ import annotations
"""
knowledge_feeder.py - 知识库投喂模块

功能：
1. 建立知识库对话窗口，支持所有类型文件投喂
2. 信息提取和格式转换（PDF、PPT、Excel、Word 等）
3. 内容提纯处理，过滤图片等非文字信息
4. 可选 LMM 多模态对接

使用：
    feeder = KnowledgeFeeder()
    result = feeder.feed_file("path/to/file.pdf")
    result = feeder.feed_text("纯文本内容")
    result = feeder.purify_content(raw_text)
"""

import os
import re
import logging
from abc import ABC, abstractmethod
from urllib.parse import urlparse
import ipaddress
import socket
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

from .format_converter import FormatConverter, ConversionManager, ConversionResult, FileFormat
from .media_processor import MediaProcessor, IMAGE_FORMATS, AUDIO_FORMATS, VIDEO_FORMATS
from .utils import _validate_url

logger = logging.getLogger(__name__)


def _is_safe_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
        hostname = parsed.hostname
        if not hostname:
            return False
        try:
            resolved = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
            for family, _, _, _, sockaddr in resolved:
                ip = ipaddress.ip_address(sockaddr[0])
                if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
                    return False
        except (socket.gaierror, ValueError):
            return False
        return True
    except Exception:
        return False


class ContentType(Enum):
    TEXT = "text"
    PDF = "pdf"
    WORD = "word"
    EXCEL = "excel"
    PPT = "ppt"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    URL = "url"
    UNKNOWN = "unknown"


@dataclass
class FeedResult:
    success: bool
    content_type: ContentType
    original_length: int = 0
    purified_length: int = 0
    content: str = ""
    metadata: Dict = field(default_factory=dict)
    error: Optional[str] = None
    warnings: List[str] = field(default_factory=list)


class ContentPurifier:
    """
    内容提纯处理器

    功能：
    - 去除 HTML/XML 标签
    - 去除特殊控制字符
    - 规范化空白字符
    - 过滤图片/媒体占位符
    - 保留文档结构信息
    """

    def __init__(self):
        self.html_tag_pattern = re.compile(r'<[^>]+>')
        self.control_char_pattern = re.compile(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]')
        self.extra_whitespace_pattern = re.compile(r'\s+')
        self.image_placeholder_pattern = re.compile(r'\[?(图片|图像|photo|image|img|图)[:：]?[^\]]*\]?', re.IGNORECASE)
        self.url_pattern = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')

    def purify(self, text: str, preserve_urls: bool = True) -> str:
        """
        提纯文本内容

        Args:
            text: 原始文本
            preserve_urls: 是否保留 URL

        Returns:
            str: 提纯后的文本
        """
        if not text:
            return ""

        result = text

        result = self.control_char_pattern.sub('', result)

        result = self.html_tag_pattern.sub(' ', result)

        if not preserve_urls:
            result = self.url_pattern.sub('[链接]', result)

        result = self.image_placeholder_pattern.sub('[图片内容已过滤]', result)

        result = result.replace('\r\n', '\n').replace('\r', '\n')

        result = self.extra_whitespace_pattern.sub(' ', result)

        lines = result.split('\n')
        cleaned_lines = []
        prev_empty = False
        for line in lines:
            line = line.strip()
            if line:
                cleaned_lines.append(line)
                prev_empty = False
            elif not prev_empty:
                cleaned_lines.append('')
                prev_empty = True
        result = '\n'.join(cleaned_lines)

        result = result.strip()

        return result

    def extract_urls(self, text: str) -> List[str]:
        """从文本中提取所有 URL"""
        return self.url_pattern.findall(text)

    def remove_urls(self, text: str) -> str:
        """从文本中移除所有 URL"""
        return self.url_pattern.sub('[链接]', text)

    def truncate(self, text: str, max_length: int = 50000, suffix: str = "...[内容截断]") -> str:
        """截断过长的文本"""
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix


class DocumentProcessor(ABC):
    """文档处理器抽象基类"""

    @abstractmethod
    def process(self, file_path: str) -> FeedResult:
        """处理文档并返回结果"""
        pass

    @abstractmethod
    def can_process(self, file_path: str) -> bool:
        """判断是否能够处理该文件"""
        pass


class PDFProcessor(DocumentProcessor):
    """PDF 文档处理器"""

    def can_process(self, file_path: str) -> bool:
        return file_path.lower().endswith('.pdf')

    def process(self, file_path: str) -> FeedResult:
        from media_processor import MediaProcessor

        try:
            processor = MediaProcessor.auto()
            result = processor.process(file_path)

            if result["success"]:
                purifier = ContentPurifier()
                purified = purifier.purify(result["description"])

                return FeedResult(
                    success=True,
                    content_type=ContentType.PDF,
                    original_length=len(result["description"]),
                    purified_length=len(purified),
                    content=purified,
                    metadata={
                        "filename": result["metadata"].get("filename", os.path.basename(file_path)),
                        "format": "pdf",
                        "pages": result["metadata"].get("pages", 0)
                    }
                )
            else:
                # 降级处理：返回文件基本信息
                filename = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)
                return FeedResult(
                    success=True,
                    content_type=ContentType.PDF,
                    original_length=0,
                    purified_length=0,
                    content=f"[PDF文件: {filename} ({file_size // 1024}KB)，如需提取内容请配置 LLM 多模态能力]",
                    metadata={
                        "filename": filename,
                        "format": "pdf",
                        "size_kb": file_size // 1024
                    },
                    warnings=["未配置 LMM，无法提取 PDF 内容"]
                )

        except Exception as e:
            logger.warning("knowledge_feeder: %s", e)
            # 降级处理：返回文件基本信息
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            return FeedResult(
                success=True,
                content_type=ContentType.PDF,
                original_length=0,
                purified_length=0,
                content=f"[PDF文件: {filename} ({file_size // 1024}KB)，处理失败: {str(e)}]",
                metadata={
                    "filename": filename,
                    "format": "pdf",
                    "size_kb": file_size // 1024
                },
                warnings=[f"PDF 处理失败: {str(e)}"]
            )


class WordProcessor(DocumentProcessor):
    """Word 文档处理器"""

    def can_process(self, file_path: str) -> bool:
        return file_path.lower().endswith(('.docx', '.doc'))

    def process(self, file_path: str) -> FeedResult:
        from media_processor import MediaProcessor

        try:
            processor = MediaProcessor.auto()
            result = processor.process(file_path)

            if result["success"]:
                purifier = ContentPurifier()
                purified = purifier.purify(result["description"])

                return FeedResult(
                    success=True,
                    content_type=ContentType.WORD,
                    original_length=len(result["description"]),
                    purified_length=len(purified),
                    content=purified,
                    metadata={
                        "filename": result["metadata"].get("filename", os.path.basename(file_path)),
                        "format": "word"
                    }
                )
            else:
                # 降级处理：返回文件基本信息
                filename = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)
                return FeedResult(
                    success=True,
                    content_type=ContentType.WORD,
                    original_length=0,
                    purified_length=0,
                    content=f"[Word文件: {filename} ({file_size // 1024}KB)，如需提取内容请配置 LLM 多模态能力]",
                    metadata={
                        "filename": filename,
                        "format": "word",
                        "size_kb": file_size // 1024
                    },
                    warnings=["未配置 LMM，无法提取 Word 内容"]
                )

        except Exception as e:
            logger.warning("knowledge_feeder: %s", e)
            # 降级处理：返回文件基本信息
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            return FeedResult(
                success=True,
                content_type=ContentType.WORD,
                original_length=0,
                purified_length=0,
                content=f"[Word文件: {filename} ({file_size // 1024}KB)，处理失败: {str(e)}]",
                metadata={
                    "filename": filename,
                    "format": "word",
                    "size_kb": file_size // 1024
                },
                warnings=[f"Word 处理失败: {str(e)}"]
            )


class ExcelProcessor(DocumentProcessor):
    """Excel 文档处理器"""

    def can_process(self, file_path: str) -> bool:
        return file_path.lower().endswith('.xlsx')

    def process(self, file_path: str) -> FeedResult:
        from media_processor import MediaProcessor

        try:
            processor = MediaProcessor.auto()
            result = processor.process(file_path)

            if result["success"]:
                purifier = ContentPurifier()
                purified = purifier.purify(result["description"])

                return FeedResult(
                    success=True,
                    content_type=ContentType.EXCEL,
                    original_length=len(result["description"]),
                    purified_length=len(purified),
                    content=purified,
                    metadata={
                        "filename": result["metadata"].get("filename", os.path.basename(file_path)),
                        "format": "excel",
                        "sheets": result["metadata"].get("sheets", []),
                        "sheet_count": result["metadata"].get("sheet_count", 0)
                    }
                )
            else:
                # 降级处理：返回文件基本信息
                filename = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)
                return FeedResult(
                    success=True,
                    content_type=ContentType.EXCEL,
                    original_length=0,
                    purified_length=0,
                    content=f"[Excel文件: {filename} ({file_size // 1024}KB)，如需提取内容请配置 LLM 多模态能力]",
                    metadata={
                        "filename": filename,
                        "format": "excel",
                        "size_kb": file_size // 1024
                    },
                    warnings=["未配置 LMM，无法提取 Excel 内容"]
                )

        except Exception as e:
            logger.warning("knowledge_feeder: %s", e)
            # 降级处理：返回文件基本信息
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            return FeedResult(
                success=True,
                content_type=ContentType.EXCEL,
                original_length=0,
                purified_length=0,
                content=f"[Excel文件: {filename} ({file_size // 1024}KB)，处理失败: {str(e)}]",
                metadata={
                    "filename": filename,
                    "format": "excel",
                    "size_kb": file_size // 1024
                },
                warnings=[f"Excel 处理失败: {str(e)}"]
            )


class PPTProcessor(DocumentProcessor):
    """PowerPoint 文档处理器"""

    def can_process(self, file_path: str) -> bool:
        return file_path.lower().endswith('.pptx')

    def process(self, file_path: str) -> FeedResult:
        from media_processor import MediaProcessor

        try:
            processor = MediaProcessor.auto()
            result = processor.process(file_path)

            if result["success"]:
                purifier = ContentPurifier()
                purified = purifier.purify(result["description"])

                return FeedResult(
                    success=True,
                    content_type=ContentType.PPT,
                    original_length=len(result["description"]),
                    purified_length=len(purified),
                    content=purified,
                    metadata={
                        "filename": result["metadata"].get("filename", os.path.basename(file_path)),
                        "format": "ppt",
                        "slide_count": result["metadata"].get("slide_count", 0)
                    }
                )
            else:
                # 降级处理：返回文件基本信息
                filename = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)
                return FeedResult(
                    success=True,
                    content_type=ContentType.PPT,
                    original_length=0,
                    purified_length=0,
                    content=f"[PPT文件: {filename} ({file_size // 1024}KB)，如需提取内容请配置 LLM 多模态能力]",
                    metadata={
                        "filename": filename,
                        "format": "ppt",
                        "size_kb": file_size // 1024
                    },
                    warnings=["未配置 LMM，无法提取 PPT 内容"]
                )

        except Exception as e:
            logger.warning("knowledge_feeder: %s", e)
            # 降级处理：返回文件基本信息
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            return FeedResult(
                success=True,
                content_type=ContentType.PPT,
                original_length=0,
                purified_length=0,
                content=f"[PPT文件: {filename} ({file_size // 1024}KB)，处理失败: {str(e)}]",
                metadata={
                    "filename": filename,
                    "format": "ppt",
                    "size_kb": file_size // 1024
                },
                warnings=[f"PPT 处理失败: {str(e)}"]
            )


class TextProcessor(DocumentProcessor):
    """纯文本处理器"""

    SUPPORTED_EXTENSIONS = {'.txt', '.md', '.rtf', '.csv', '.json', '.xml', '.html', '.htm'}

    def can_process(self, file_path: str) -> bool:
        ext = os.path.splitext(file_path)[1].lower()
        return ext in self.SUPPORTED_EXTENSIONS

    def process(self, file_path: str) -> FeedResult:
        purifier = ContentPurifier()

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                original_content = f.read()

            purified = purifier.purify(original_content)

            return FeedResult(
                success=True,
                content_type=ContentType.TEXT,
                original_length=len(original_content),
                purified_length=len(purified),
                content=purified,
                metadata={
                    "filename": os.path.basename(file_path),
                    "format": os.path.splitext(file_path)[1].lower().lstrip('.')
                }
            )

        except Exception as e:
            logger.warning("knowledge_feeder: %s", e)
            return FeedResult(
                success=False,
                content_type=ContentType.TEXT,
                error=str(e)
            )


class ImageProcessor(DocumentProcessor):
    """图片处理器（可选 LMM 支持）"""

    SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff'}

    def __init__(self, vision_fn: Callable = None):
        self.vision_fn = vision_fn

    def can_process(self, file_path: str) -> bool:
        ext = os.path.splitext(file_path)[1].lower()
        return ext in self.SUPPORTED_EXTENSIONS

    def process(self, file_path: str) -> FeedResult:
        if self.vision_fn:
            return self._process_with_lmm(file_path)
        else:
            return self._process_fallback(file_path)

    def _process_with_lmm(self, file_path: str) -> FeedResult:
        """使用 LMM 模型处理图片"""
        try:
            with open(file_path, 'rb') as f:
                image_bytes = f.read()

            mime_type = self._get_mime_type(file_path)
            description = self.vision_fn(image_bytes, mime_type, "请详细描述这张图片的内容，包括所有文字、图表和关键信息。")

            purifier = ContentPurifier()
            purified = purifier.purify(description)

            return FeedResult(
                success=True,
                content_type=ContentType.IMAGE,
                original_length=len(description),
                purified_length=len(purified),
                content=purified,
                metadata={
                    "filename": os.path.basename(file_path),
                    "format": os.path.splitext(file_path)[1].lower().lstrip('.'),
                    "size_bytes": len(image_bytes),
                    "lmm_used": True
                }
            )

        except Exception as e:
            logger.warning("knowledge_feeder: %s", e)
            return FeedResult(
                success=False,
                content_type=ContentType.IMAGE,
                error=str(e)
            )

    def _process_fallback(self, file_path: str) -> FeedResult:
        """无 LMM 时的降级处理"""
        purifier = ContentPurifier()
        placeholder = f"[图片文件: {os.path.basename(file_path)}，如需提取内容请配置 LLM 多模态能力]"

        return FeedResult(
            success=True,
            content_type=ContentType.IMAGE,
            original_length=len(placeholder),
            purified_length=len(placeholder),
            content=placeholder,
            metadata={
                "filename": os.path.basename(file_path),
                "format": os.path.splitext(file_path)[1].lower().lstrip('.'),
                "lmm_used": False
            },
            warnings=["未配置 LMM，无法提取图片内容"]
        )

    def _get_mime_type(self, file_path: str) -> str:
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
            '.bmp': 'image/bmp',
            '.tiff': 'image/tiff'
        }
        return mime_types.get(os.path.splitext(file_path)[1].lower(), 'image/png')


class AudioProcessor(DocumentProcessor):
    """音频处理器（可选 LMM 支持）"""

    SUPPORTED_EXTENSIONS = {'.mp3', '.wav', '.ogg', '.flac', '.m4a', '.aac', '.wma'}

    def __init__(self, audio_fn: Callable = None):
        self.audio_fn = audio_fn

    def can_process(self, file_path: str) -> bool:
        ext = os.path.splitext(file_path)[1].lower()
        return ext in self.SUPPORTED_EXTENSIONS

    def process(self, file_path: str) -> FeedResult:
        if self.audio_fn:
            return self._process_with_lmm(file_path)
        else:
            return self._process_fallback(file_path)

    def _process_with_lmm(self, file_path: str) -> FeedResult:
        """使用 LMM 模型处理音频"""
        try:
            with open(file_path, 'rb') as f:
                audio_bytes = f.read()

            mime_type = self._get_mime_type(file_path)
            transcript = self.audio_fn(audio_bytes, mime_type)

            purifier = ContentPurifier()
            purified = purifier.purify(transcript)

            return FeedResult(
                success=True,
                content_type=ContentType.AUDIO,
                original_length=len(transcript),
                purified_length=len(purified),
                content=purified,
                metadata={
                    "filename": os.path.basename(file_path),
                    "format": os.path.splitext(file_path)[1].lower().lstrip('.'),
                    "size_bytes": len(audio_bytes),
                    "lmm_used": True
                }
            )

        except Exception as e:
            logger.warning("knowledge_feeder: %s", e)
            return FeedResult(
                success=False,
                content_type=ContentType.AUDIO,
                error=str(e)
            )

    def _process_fallback(self, file_path: str) -> FeedResult:
        """无 LMM 时的降级处理"""
        purifier = ContentPurifier()
        placeholder = f"[音频文件: {os.path.basename(file_path)}，如需提取内容请配置 LLM 多模态能力]"

        return FeedResult(
            success=True,
            content_type=ContentType.AUDIO,
            original_length=len(placeholder),
            purified_length=len(placeholder),
            content=placeholder,
            metadata={
                "filename": os.path.basename(file_path),
                "format": os.path.splitext(file_path)[1].lower().lstrip('.'),
                "lmm_used": False
            },
            warnings=["未配置 LMM，无法提取音频内容"]
        )

    def _get_mime_type(self, file_path: str) -> str:
        mime_types = {
            '.mp3': 'audio/mpeg',
            '.wav': 'audio/wav',
            '.ogg': 'audio/ogg',
            '.flac': 'audio/flac',
            '.m4a': 'audio/mp4',
            '.aac': 'audio/aac',
            '.wma': 'audio/wma'
        }
        return mime_types.get(os.path.splitext(file_path)[1].lower(), 'audio/wav')


class VideoProcessor(DocumentProcessor):
    """视频处理器（可选 LMM 支持）"""

    SUPPORTED_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv'}

    def __init__(self, vision_fn: Callable = None, audio_fn: Callable = None):
        self.vision_fn = vision_fn
        self.audio_fn = audio_fn

    def can_process(self, file_path: str) -> bool:
        ext = os.path.splitext(file_path)[1].lower()
        return ext in self.SUPPORTED_EXTENSIONS

    def process(self, file_path: str) -> FeedResult:
        if self.vision_fn or self.audio_fn:
            return self._process_with_lmm(file_path)
        else:
            return self._process_fallback(file_path)

    def _process_with_lmm(self, file_path: str) -> FeedResult:
        """使用 LMM 模型处理视频"""
        try:
            from media_processor import MediaProcessor
            processor = MediaProcessor(vision_fn=self.vision_fn, audio_fn=self.audio_fn)
            result = processor.process(file_path)

            if result["success"]:
                purifier = ContentPurifier()
                purified = purifier.purify(result["description"])

                return FeedResult(
                    success=True,
                    content_type=ContentType.VIDEO,
                    original_length=len(result["description"]),
                    purified_length=len(purified),
                    content=purified,
                    metadata={
                        "filename": os.path.basename(file_path),
                        "format": os.path.splitext(file_path)[1].lower().lstrip('.'),
                        "size_bytes": os.path.getsize(file_path),
                        "lmm_used": True,
                        **result["metadata"]
                    }
                )
            else:
                return FeedResult(
                    success=False,
                    content_type=ContentType.VIDEO,
                    error=result.get("error", "视频处理失败")
                )

        except Exception as e:
            logger.warning("knowledge_feeder: %s", e)
            return FeedResult(
                success=False,
                content_type=ContentType.VIDEO,
                error=str(e)
            )

    def _process_fallback(self, file_path: str) -> FeedResult:
        """无 LMM 时的降级处理"""
        purifier = ContentPurifier()
        placeholder = f"[视频文件: {os.path.basename(file_path)}，如需提取内容请配置 LLM 多模态能力]"

        return FeedResult(
            success=True,
            content_type=ContentType.VIDEO,
            original_length=len(placeholder),
            purified_length=len(placeholder),
            content=placeholder,
            metadata={
                "filename": os.path.basename(file_path),
                "format": os.path.splitext(file_path)[1].lower().lstrip('.'),
                "lmm_used": False
            },
            warnings=["未配置 LMM，无法提取视频内容"]
        )


class KnowledgeFeeder:
    """
    知识库投喂器

    功能：
    1. 统一入口处理所有类型的投喂内容
    2. 自动识别文件类型并路由到对应处理器
    3. 内容提纯和格式化
    4. 支持 LMM 多模态（可选）
    5. 对话式交互接口
    """

    def __init__(self, vision_fn: Callable = None, audio_fn: Callable = None):
        """
        初始化知识库投喂器

        Args:
            vision_fn: LMM 视觉处理函数，签名为 fn(bytes, mime_type, prompt) -> str
            audio_fn: 音频处理函数，签名为 fn(bytes, mime_type) -> str
        """
        # 初始化 MediaProcessor
        self.media_processor = MediaProcessor(vision_fn=vision_fn, audio_fn=audio_fn)

        self.processors: List[DocumentProcessor] = [
            PDFProcessor(),
            WordProcessor(),
            ExcelProcessor(),
            PPTProcessor(),
            ImageProcessor(vision_fn=vision_fn),
            AudioProcessor(audio_fn=audio_fn),
            VideoProcessor(vision_fn=vision_fn, audio_fn=audio_fn),
            TextProcessor(),
        ]

        self.purifier = ContentPurifier()
        self.vision_fn = vision_fn
        self.audio_fn = audio_fn

        self.feed_history: List[FeedResult] = []

        self._file_type_cache: Dict[str, ContentType] = {}

        # 格式转换功能
        self.converter = FormatConverter()
        self.conversion_manager = ConversionManager()

    def detect_content_type(self, file_path: str) -> ContentType:
        """
        自动检测文件内容类型

        Args:
            file_path: 文件路径

        Returns:
            ContentType: 检测到的内容类型
        """
        if file_path in self._file_type_cache:
            return self._file_type_cache[file_path]

        ext = os.path.splitext(file_path)[1].lower()

        type_map = {
            '.pdf': ContentType.PDF,
            '.docx': ContentType.WORD,
            '.doc': ContentType.WORD,
            '.xlsx': ContentType.EXCEL,
            '.pptx': ContentType.PPT,
            '.jpg': ContentType.IMAGE,
            '.jpeg': ContentType.IMAGE,
            '.png': ContentType.IMAGE,
            '.gif': ContentType.IMAGE,
            '.webp': ContentType.IMAGE,
            '.bmp': ContentType.IMAGE,
            '.tiff': ContentType.IMAGE,
            '.mp3': ContentType.AUDIO,
            '.wav': ContentType.AUDIO,
            '.ogg': ContentType.AUDIO,
            '.flac': ContentType.AUDIO,
            '.m4a': ContentType.AUDIO,
            '.aac': ContentType.AUDIO,
            '.wma': ContentType.AUDIO,
            '.mp4': ContentType.VIDEO,
            '.avi': ContentType.VIDEO,
            '.mov': ContentType.VIDEO,
            '.mkv': ContentType.VIDEO,
            '.webm': ContentType.VIDEO,
            '.flv': ContentType.VIDEO,
            '.wmv': ContentType.VIDEO,
            '.txt': ContentType.TEXT,
            '.md': ContentType.TEXT,
            '.rtf': ContentType.TEXT,
            '.csv': ContentType.TEXT,
            '.json': ContentType.TEXT,
            '.html': ContentType.TEXT,
            '.htm': ContentType.TEXT,
        }

        content_type = type_map.get(ext, ContentType.UNKNOWN)
        self._file_type_cache[file_path] = content_type
        return content_type

    def feed_file(self, file_path: str, skip_purify: bool = False) -> FeedResult:
        """
        投喂文件

        Args:
            file_path: 文件路径
            skip_purify: 是否跳过提纯步骤

        Returns:
            FeedResult: 投喂结果
        """
        if not os.path.exists(file_path):
            return FeedResult(
                success=False,
                content_type=ContentType.UNKNOWN,
                error=f"文件不存在: {file_path}"
            )

        content_type = self.detect_content_type(file_path)

        for processor in self.processors:
            if processor.can_process(file_path):
                result = processor.process(file_path)

                if result.success and not skip_purify:
                    result.content = self.purifier.purify(result.content)
                    result.purified_length = len(result.content)

                if result.success:
                    self.feed_history.append(result)

                return result

        return FeedResult(
            success=False,
            content_type=content_type,
            error=f"不支持的文件类型: {content_type.value}"
        )

    def feed_text(self, text: str, metadata: Dict = None) -> FeedResult:
        """
        投喂纯文本

        Args:
            text: 文本内容
            metadata: 额外元数据

        Returns:
            FeedResult: 投喂结果
        """
        original_length = len(text)
        purified = self.purifier.purify(text)

        result = FeedResult(
            success=True,
            content_type=ContentType.TEXT,
            original_length=original_length,
            purified_length=len(purified),
            content=purified,
            metadata=metadata or {}
        )

        self.feed_history.append(result)
        return result

    def feed_url(self, url: str) -> FeedResult:
        """
        投喂 URL（网页内容）

        Args:
            url: 网页 URL

        Returns:
            FeedResult: 投喂结果
        """
        try:
            import urllib.request
            import urllib.parse

            if not _is_safe_url(url):
                logger.warning(f"Blocked unsafe URL: {url}")
                return FeedResult(success=False, content_type=ContentType.URL, original_length=0, purified_length=0, error=f"Blocked unsafe URL: {url}")

            _validate_url(url)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0',
                'Referer': 'https://www.google.com/',
            }
            req = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(req, timeout=15)
            html = response.read().decode('utf-8', errors='ignore')

            from html.parser import HTMLParser

            class TextExtractor(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.text = []
                    self.skip_tags = {'script', 'style', 'head', 'noscript', 'iframe'}
                    self.current_tag = None

                def handle_starttag(self, tag, attrs):
                    self.current_tag = tag

                def handle_endtag(self, tag):
                    self.current_tag = None

                def handle_data(self, data):
                    if self.current_tag not in self.skip_tags:
                        self.text.append(data)

            extractor = TextExtractor()
            extractor.feed(html)
            text = ''.join(extractor.text)

            purifier = ContentPurifier()
            purified = purifier.purify(text, preserve_urls=True)

            # 生成网页内容的摘要
            summary = self._generate_url_summary(purified, url)

            result = FeedResult(
                success=True,
                content_type=ContentType.URL,
                original_length=len(text),
                purified_length=len(purified),
                content=purified,
                metadata={
                    "url": url,
                    "domain": urllib.parse.urlparse(url).netloc,
                    "summary": summary
                }
            )

            self.feed_history.append(result)
            return result

        except Exception as e:
            logger.warning("knowledge_feeder: %s", e)
            return FeedResult(
                success=True,
                content_type=ContentType.URL,
                original_length=0,
                purified_length=0,
                content=f"[网页链接: {url}，处理失败: {str(e)}]",
                metadata={
                    "url": url,
                    "domain": urllib.parse.urlparse(url).netloc
                },
                warnings=[f"URL 处理失败: {str(e)}"]
            )
    
    def _generate_url_summary(self, content: str, url: str) -> str:
        """
        生成网页内容的摘要

        Args:
            content: 网页内容
            url: 网页 URL

        Returns:
            str: 网页摘要
        """
        # 简单的摘要生成逻辑
        # 提取前200个字符作为摘要
        summary = content.strip()
        if len(summary) > 200:
            summary = summary[:200] + "..."
        return summary

    def purify_content(self, text: str, preserve_urls: bool = True) -> str:
        """
        提纯文本内容

        Args:
            text: 原始文本
            preserve_urls: 是否保留 URL

        Returns:
            str: 提纯后的文本
        """
        return self.purifier.purify(text, preserve_urls=preserve_urls)

    def get_history(self, limit: int = 100) -> List[FeedResult]:
        """获取投喂历史"""
        return self.feed_history[-limit:]

    def clear_history(self):
        """清空投喂历史"""
        self.feed_history.clear()

    def get_statistics(self) -> Dict:
        """获取投喂统计信息"""
        total = len(self.feed_history)
        type_counts = {}

        for result in self.feed_history:
            type_name = result.content_type.value
            type_counts[type_name] = type_counts.get(type_name, 0) + 1

        return {
            "total_items": total,
            "type_counts": type_counts,
            "total_original_length": sum(r.original_length for r in self.feed_history),
            "total_purified_length": sum(r.purified_length for r in self.feed_history),
            "compression_ratio": (
                sum(r.purified_length for r in self.feed_history) /
                max(sum(r.original_length for r in self.feed_history), 1)
            )
        }

    def export_as_markdown(self, include_metadata: bool = True) -> str:
        """
        导出投喂内容为 Markdown 格式

        Args:
            include_metadata: 是否包含元数据

        Returns:
            str: Markdown 格式的内容
        """
        lines = ["# 知识库投喂内容\n"]

        for i, result in enumerate(self.feed_history, 1):
            lines.append(f"## {i}. {result.content_type.value.upper()}")

            if include_metadata and result.metadata:
                lines.append("**元数据:**")
                for key, value in result.metadata.items():
                    lines.append(f"- {key}: {value}")
                lines.append("")

            lines.append(result.content)
            lines.append("")

            if result.error:
                lines.append(f"> **错误:** {result.error}")

            if result.warnings:
                for warning in result.warnings:
                    lines.append(f"> **警告:** {warning}")

            lines.append("---\n")

        return '\n'.join(lines)

    def convert_format(self, input_path: str, output_path: str, **kwargs) -> ConversionResult:
        """
        格式转换

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            **kwargs: 额外参数

        Returns:
            ConversionResult: 转换结果
        """
        return self.conversion_manager.convert(input_path, output_path, **kwargs)

    def batch_convert(self, files: List[tuple], **kwargs) -> List[ConversionResult]:
        """
        批量格式转换

        Args:
            files: 包含 (input_path, output_path) 的列表
            **kwargs: 额外参数

        Returns:
            List[ConversionResult]: 转换结果列表
        """
        return self.conversion_manager.batch_convert(files, **kwargs)

    def get_conversion_history(self, limit: int = 100) -> List[ConversionResult]:
        """
        获取转换历史

        Args:
            limit: 限制数量

        Returns:
            List[ConversionResult]: 历史记录
        """
        return self.conversion_manager.get_history(limit=limit)

    def get_conversion_statistics(self) -> Dict:
        """
        获取转换统计信息

        Returns:
            Dict: 统计信息
        """
        return self.conversion_manager.get_statistics()

    def get_supported_conversions(self) -> List[tuple]:
        """
        获取支持的格式转换

        Returns:
            List[tuple]: 支持的格式对列表
        """
        return self.converter.get_supported_conversions()

    def is_conversion_supported(self, input_path: str, output_path: str) -> bool:
        """
        检查是否支持指定的格式转换

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径

        Returns:
            bool: 是否支持
        """
        return self.converter.is_supported(input_path, output_path)


class FeederChatWindow:
    """
    投喂对话窗口接口

    提供对话式交互接口，支持：
    1. 实时对话
    2. 文件投喂
    3. 内容查询
    4. 上下文管理
    """

    def __init__(self, knowledge_feeder: KnowledgeFeeder = None, llm_fn: Callable = None):
        """
        初始化对话窗口

        Args:
            knowledge_feeder: 知识库投喂器实例
            llm_fn: LLM 对话函数，签名为 fn(messages: List[dict]) -> str
        """
        self.feeder = knowledge_feeder or KnowledgeFeeder()
        self.llm_fn = llm_fn
        self.conversation_history: List[Dict] = []
        self.context_enabled = True

    def chat(self, message: str, context: str = None) -> Dict:
        """
        处理对话消息

        Args:
            message: 用户消息
            context: 可选的额外上下文

        Returns:
            dict: 回复结果
        """
        message_lower = message.lower().strip()

        if message_lower.startswith('/feed '):
            file_path = message[6:].strip()
            result = self.feeder.feed_file(file_path)
            return self._format_file_result(result)

        if message_lower.startswith('/url '):
            url = message[5:].strip()
            result = self.feeder.feed_url(url)
            return self._format_url_result(result)

        if message_lower in ['/stats', '/statistics']:
            stats = self.feeder.get_statistics()
            return {
                "type": "system",
                "content": self._format_stats(stats)
            }

        if message_lower in ['/export', '/export md']:
            md_content = self.feeder.export_as_markdown()
            return {
                "type": "export",
                "content": md_content
            }

        if message_lower in ['/clear', '/reset']:
            self.feeder.clear_history()
            self.conversation_history.clear()
            return {
                "type": "system",
                "content": "已清空投喂历史和对话历史"
            }

        if message_lower in ['/help', 'help']:
            return {
                "type": "system",
                "content": self._get_help_text()
            }

        if message_lower.startswith('/convert '):
            parts = message[8:].strip().split(' ')
            if len(parts) >= 2:
                input_path = parts[0]
                output_path = parts[1]
                result = self.feeder.convert_format(input_path, output_path)
                return self._format_conversion_result(result)
            else:
                return {
                    "type": "system",
                    "content": "使用格式: /convert <输入文件> <输出文件>"
                }

        if message_lower in ['/convert stats', '/convert stats']:
            stats = self.feeder.get_conversion_statistics()
            return {
                "type": "system",
                "content": self._format_conversion_stats(stats)
            }

        if message_lower in ['/convert list', '/convert formats']:
            conversions = self.feeder.get_supported_conversions()
            return {
                "type": "system",
                "content": self._format_supported_conversions(conversions)
            }

        if self.llm_fn and (self.context_enabled or context):
            context_content = ""
            if self.context_enabled:
                recent = self.feeder.get_history(limit=10)
                if recent:
                    context_content = "\n\n".join([
                        f"[{r.content_type.value}] {r.content[:500]}"
                        for r in recent
                    ])

            if context:
                context_content = context_content + "\n\n" + context if context_content else context

            messages = [
                {"role": "system", "content": "你是知识库的智能助手。用户正在与你对话，同时知识库中有以下相关内容："},
                {"role": "user", "content": f"知识库内容:\n{context_content}\n\n用户消息: {message}"}
            ]

            try:
                response = self.llm_fn(messages)
                self.conversation_history.append({"role": "user", "content": message})
                self.conversation_history.append({"role": "assistant", "content": response})
                return {"type": "assistant", "content": response}
            except Exception as e:
                logger.warning("knowledge_feeder: %s", e)
                return {
                    "type": "assistant",
                    "content": "抱歉，LLM 服务暂时不可用。请告诉我你需要什么帮助，或者投喂文件来丰富知识库。"
                }

        return {
            "type": "assistant",
            "content": "我是知识库助手。你可以：\n1. 直接输入文字与我对话\n2. 使用 /feed <文件路径> 投喂文件\n3. 使用 /url <网址> 投喂网页\n4. 使用 /stats 查看投喂统计\n5. 使用 /export 导出内容\n6. 使用 /help 查看更多命令"
        }

    def feed_text(self, text: str) -> FeedResult:
        """直接投喂文本"""
        return self.feeder.feed_text(text)

    def _format_file_result(self, result: FeedResult) -> Dict:
        """格式化文件投喂结果"""
        if result.success:
            content_preview = result.content[:300] + "..." if len(result.content) > 300 else result.content
            return {
                "type": "system",
                "content": (
                    f"✅ **文件投喂成功**\n\n"
                    f"类型: {result.content_type.value}\n"
                    f"文件名: {result.metadata.get('filename', '未知')}\n"
                    f"原始长度: {result.original_length} 字符\n"
                    f"提纯后: {result.purified_length} 字符\n"
                    f"压缩比: {result.purified_length / max(result.original_length, 1):.1%}\n\n"
                    f"**内容预览:**\n{content_preview}"
                )
            }
        else:
            return {
                "type": "system",
                "content": f"❌ **文件投喂失败**\n\n错误: {result.error}"
            }

    def _format_url_result(self, result: FeedResult) -> Dict:
        """格式化 URL 投喂结果"""
        if result.success:
            content_preview = result.content[:300] + "..." if len(result.content) > 300 else result.content
            return {
                "type": "system",
                "content": (
                    f"✅ **URL 投喂成功**\n\n"
                    f"网址: {result.metadata.get('url', '未知')}\n"
                    f"域名: {result.metadata.get('domain', '未知')}\n"
                    f"提纯后: {result.purified_length} 字符\n\n"
                    f"**内容预览:**\n{content_preview}"
                )
            }
        else:
            return {
                "type": "system",
                "content": f"❌ **URL 投喂失败**\n\n错误: {result.error}"
            }

    def _format_stats(self, stats: Dict) -> str:
        """格式化统计信息"""
        lines = ["📊 **投喂统计**\n"]
        lines.append(f"- 总条目: {stats['total_items']}")
        lines.append(f"- 原始总长度: {stats['total_original_length']} 字符")
        lines.append(f"- 提纯后总长度: {stats['total_purified_length']} 字符")
        lines.append(f"- 压缩比: {stats['compression_ratio']:.1%}")
        lines.append("\n**类型分布:**")
        for content_type, count in stats['type_counts'].items():
            lines.append(f"- {content_type}: {count}")
        return '\n'.join(lines)

    def _get_help_text(self) -> str:
        """获取帮助文本"""
        return """
📚 **知识库投喂助手 - 命令帮助**

**文件投喂:**
- `/feed <文件路径>` - 投喂文件（支持 PDF、Word、Excel、PPT、图片等）

**内容投喂:**
- `/url <网址>` - 投喂网页内容
- 直接输入文字 - 作为文本投喂

**知识库操作:**
- `/stats` - 查看投喂统计
- `/export` - 导出投喂内容为 Markdown
- `/clear` - 清空历史记录

**格式转换:**
- `/convert <输入文件> <输出文件>` - 格式转换
- `/convert stats` - 查看转换统计
- `/convert list` - 查看支持的格式转换

**对话功能:**
- 开启 LLM 后，可进行智能问答
- 系统会结合知识库内容进行回答

**快捷命令:**
- `help` - 显示此帮助
- `purify:<文本>` - 提纯指定文本
        """

    def _format_conversion_result(self, result: ConversionResult) -> Dict:
        """格式化转换结果"""
        if result.success:
            return {
                "type": "system",
                "content": (
                    f"✅ **格式转换成功**\n\n"
                    f"输入: {result.input_format.value}\n"
                    f"输出: {result.output_format.value}\n"
                    f"输入文件: {result.input_file}\n"
                    f"输出文件: {result.output_file}\n"
                    f"输入大小: {result.input_size / 1024:.1f} KB\n"
                    f"输出大小: {result.output_size / 1024:.1f} KB\n"
                    f"转换时间: {result.conversion_time:.2f} 秒\n\n"
                    f"**状态:** {result.message}"
                )
            }
        else:
            return {
                "type": "system",
                "content": f"❌ **格式转换失败**\n\n错误: {result.error}"
            }

    def _format_conversion_stats(self, stats: Dict) -> str:
        """格式化转换统计"""
        lines = ["📊 **转换统计**\n"]
        lines.append(f"- 总任务: {stats['total_tasks']}")
        lines.append(f"- 成功: {stats['success_count']}")
        lines.append(f"- 失败: {stats['failed_count']}")
        lines.append(f"- 成功率: {stats['success_rate']:.1%}")
        lines.append(f"- 活跃任务: {stats['active_tasks']}")
        lines.append("\n**格式分布:**")
        for conversion, count in stats['format_stats'].items():
            lines.append(f"- {conversion}: {count}")
        return '\n'.join(lines)

    def _format_supported_conversions(self, conversions: List[tuple]) -> str:
        """格式化支持的转换"""
        lines = ["📋 **支持的格式转换**\n"]
        for from_format, to_format in conversions:
            lines.append(f"- {from_format.value} → {to_format.value}")
        return '\n'.join(lines)

def create_knowledge_feeder(vision_fn: Callable = None, audio_fn: Callable = None) -> KnowledgeFeeder:
    """
    创建知识库投喂器实例

    Args:
        vision_fn: LMM 视觉处理函数
        audio_fn: 音频处理函数

    Returns:
        KnowledgeFeeder: 投喂器实例
    """
    return KnowledgeFeeder(vision_fn=vision_fn, audio_fn=audio_fn)


def create_chat_window(knowledge_feeder: KnowledgeFeeder = None, llm_fn: Callable = None) -> FeederChatWindow:
    """
    创建投喂对话窗口实例

    Args:
        knowledge_feeder: 知识库投喂器
        llm_fn: LLM 对话函数

    Returns:
        FeederChatWindow: 对话窗口实例
    """
    return FeederChatWindow(knowledge_feeder=knowledge_feeder, llm_fn=llm_fn)


if __name__ == "__main__":
    feeder = KnowledgeFeeder()

    result = feeder.feed_text("这是一段测试文本，包含  多个   空白字符和<link>HTML标签</link>。")
    print(f"Text feed: {result.success}, purified: {result.content}")

    import os
    test_files = [
        "test.pdf",
        "test.docx",
        "test.xlsx",
        "test.pptx",
    ]

    for f in test_files:
        if os.path.exists(f):
            result = feeder.feed_file(f)
            print(f"File {f}: {result.success}, type: {result.content_type.value}")
