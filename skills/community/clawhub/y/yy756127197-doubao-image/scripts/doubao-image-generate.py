#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆包文生图 API 调用脚本 - Doubao SeeDream Image Generation
========================================================

通过火山引擎 ARK API 调用豆包 SeeDream 模型生成 AI 图片。

版本：2.0.0
作者：YangYang
许可：MIT License

用法:
    python doubao-image-generate.py --prompt "图片描述" [选项]

示例:
    python doubao-image-generate.py --prompt "一只在月光下的白色小猫"
    python doubao-image-generate.py --prompt "赛博朋克城市夜景" --size 1080P
    python doubao-image-generate.py --prompt "山水画" --no-watermark --output-dir ./artworks

环境变量:
    ARK_API_KEY           - 火山引擎 ARK API Key（必需）
    DOUBAO_API_TIMEOUT    - API 超时时间（秒，默认：60）
    DOUBAO_RETRY_COUNT    - 失败重试次数（默认：3）
    DOUBAO_OUTPUT_DIR     - 默认输出目录（默认：generated-images）
"""

import argparse
import hashlib
import json
import logging
import os
import platform
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from urllib.parse import urlparse

# 尝试导入 requests，如果不存在则使用 urllib
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    import urllib.request
    import urllib.error

# 版本信息
__version__ = "2.0.0"
__author__ = "YangYang"
__license__ = "MIT"

# 常量
API_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
MODEL = "doubao-seedream-5-0-260128"
VALID_SIZES = ["2K", "1080P", "720P"]
USER_AGENT = f"doubao-image-skill/{__version__}"

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class DoubaoImageGenerator:
    """豆包图片生成器类"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: int = 60,
        retry_count: int = 3,
        output_dir: str = "generated-images",
        verbose: bool = False
    ):
        """
        初始化生成器
        
        Args:
            api_key: ARK API Key，如果为 None 则从环境变量读取
            timeout: API 超时时间（秒）
            retry_count: 失败重试次数
            output_dir: 输出目录
            verbose: 是否启用详细日志
        """
        self.api_key = api_key or os.getenv("ARK_API_KEY")
        self.timeout = timeout or int(os.getenv("DOUBAO_API_TIMEOUT", "60"))
        self.retry_count = retry_count or int(os.getenv("DOUBAO_RETRY_COUNT", "3"))
        self.output_dir = Path(output_dir or os.getenv("DOUBAO_OUTPUT_DIR", "generated-images"))
        self.verbose = verbose or os.getenv("DOUBAO_VERBOSE", "false").lower() == "true"
        
        if verbose:
            logger.setLevel(logging.DEBUG)
        
        # 验证必需配置
        self._validate_config()
    
    def _validate_config(self) -> None:
        """验证配置"""
        if not self.api_key:
            raise EnvironmentError(
                "缺少 ARK_API_KEY 环境变量\n"
                "请设置：export ARK_API_KEY=your_api_key\n"
                "获取地址：https://console.volcengine.com/ark"
            )
        
        # 确保输出目录存在
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.debug(f"✓ 配置验证通过")
        logger.debug(f"  - API URL: {API_URL}")
        logger.debug(f"  - 模型：{MODEL}")
        logger.debug(f"  - 输出目录：{self.output_dir.absolute()}")
        logger.debug(f"  - 超时：{self.timeout}秒")
        logger.debug(f"  - 重试次数：{self.retry_count}")
    
    def _build_request_body(
        self,
        prompt: str,
        size: str = "2K",
        watermark: bool = True
    ) -> Dict[str, Any]:
        """
        构建 API 请求体
        
        Args:
            prompt: 图片描述
            size: 分辨率
            watermark: 是否添加水印
            
        Returns:
            请求体字典
        """
        return {
            "model": MODEL,
            "prompt": prompt,
            "sequential_image_generation": "disabled",
            "response_format": "url",
            "size": size,
            "stream": False,
            "watermark": watermark
        }
    
    def _call_api(
        self,
        body: Dict[str, Any],
        attempt: int = 1
    ) -> Dict[str, Any]:
        """
        调用 API
        
        Args:
            body: 请求体
            attempt: 当前尝试次数
            
        Returns:
            API 响应字典
            
        Raises:
            APIError: API 调用失败
        """
        logger.debug(f"API 调用尝试 {attempt}/{self.retry_count}")
        logger.debug(f"请求体：{json.dumps(body, ensure_ascii=False)}")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": USER_AGENT
        }
        
        try:
            if HAS_REQUESTS:
                response = requests.post(
                    API_URL,
                    headers=headers,
                    json=body,
                    timeout=self.timeout
                )
                response.raise_for_status()
                result = response.json()
            else:
                # 使用 urllib 作为 fallback
                req = urllib.request.Request(
                    API_URL,
                    data=json.dumps(body, ensure_ascii=False).encode('utf-8'),
                    headers=headers,
                    method='POST'
                )
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    result = json.loads(resp.read().decode('utf-8'))
            
            logger.debug(f"✓ API 调用成功")
            return result
            
        except Exception as e:
            error_msg = str(e)
            status_code = getattr(e, 'code', None) or getattr(e, 'status', None)
            
            logger.debug(f"API 调用失败：{error_msg}")
            
            # 处理不同错误
            if status_code == 401:
                raise APIError("认证失败：API Key 无效或已过期", status_code)
            elif status_code == 402:
                raise APIError("账户余额不足，请充值后重试", status_code)
            elif status_code == 400:
                raise APIError("请求被拒绝：可能包含敏感词汇", status_code)
            elif status_code == 429:
                # 频率限制，重试
                retry_after = 5
                logger.warning(f"请求频率超限，等待 {retry_after}秒后重试...")
                time.sleep(retry_after)
                return self._call_api(body, attempt + 1)
            elif status_code in [500, 503, 504]:
                # 服务器错误，指数退避
                if attempt < self.retry_count:
                    delay = 2 ** (attempt - 1)
                    logger.warning(f"服务器繁忙，等待 {delay}秒后重试...")
                    time.sleep(delay)
                    return self._call_api(body, attempt + 1)
                else:
                    raise APIError(f"服务器错误（HTTP {status_code}）：已达到最大重试次数", status_code)
            else:
                raise APIError(f"API 调用失败：{error_msg}", status_code)
    
    def _parse_response(self, response: Dict[str, Any]) -> str:
        """
        解析 API 响应
        
        Args:
            response: API 响应字典
            
        Returns:
            图片 URL
            
        Raises:
            APIError: 解析失败
        """
        try:
            data = response.get("data", [])
            if not data or len(data) == 0:
                raise APIError("API 返回数据为空")
            
            image_url = data[0].get("url", "")
            if not image_url:
                raise APIError("无法从响应中提取图片 URL")
            
            logger.debug(f"✓ 解析成功，图片 URL: {image_url}")
            return image_url
            
        except Exception as e:
            logger.error(f"响应解析失败：{e}")
            logger.error(f"原始响应：{json.dumps(response, ensure_ascii=False)}")
            raise APIError(f"响应解析失败：{e}")
    
    def _generate_filename(self, prompt: str) -> str:
        """
        生成唯一文件名
        
        Args:
            prompt: 图片描述
            
        Returns:
            文件名
        """
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        
        # 使用 prompt 的哈希值作为随机标识
        prompt_hash = hashlib.md5(prompt.encode('utf-8')).hexdigest()[:8]
        
        return f"doubao-{timestamp}-{prompt_hash}.png"
    
    def _download_image(self, image_url: str, output_path: Path) -> Path:
        """
        下载图片
        
        Args:
            image_url: 图片 URL
            output_path: 保存路径
            
        Returns:
            实际保存路径
            
        Raises:
            DownloadError: 下载失败
        """
        logger.info("正在下载图片...")
        logger.debug(f"URL: {image_url}")
        logger.debug(f"保存路径：{output_path}")
        
        try:
            if HAS_REQUESTS:
                response = requests.get(
                    image_url,
                    headers={"User-Agent": USER_AGENT},
                    timeout=120
                )
                response.raise_for_status()
                content = response.content
            else:
                req = urllib.request.Request(
                    image_url,
                    headers={"User-Agent": USER_AGENT}
                )
                with urllib.request.urlopen(req, timeout=120) as resp:
                    content = resp.read()
            
            # 写入文件
            with open(output_path, 'wb') as f:
                f.write(content)
            
            # 验证文件
            file_size = output_path.stat().st_size
            if file_size < 1024:
                output_path.unlink()
                raise DownloadError(f"下载的文件过小（{file_size} 字节），可能已损坏")
            
            logger.info(f"✓ 图片下载成功")
            logger.info(f"保存位置：{output_path.absolute()}")
            logger.info(f"文件大小：{file_size} 字节")
            
            return output_path
            
        except Exception as e:
            if output_path.exists():
                output_path.unlink()
            raise DownloadError(f"图片下载失败：{e}")
    
    def generate(
        self,
        prompt: str,
        size: str = "2K",
        watermark: bool = True
    ) -> Path:
        """
        生成图片
        
        Args:
            prompt: 图片描述
            size: 分辨率（2K/1080P/720P）
            watermark: 是否添加水印
            
        Returns:
            保存的图片路径
            
        Raises:
            ValidationError: 参数验证失败
            APIError: API 调用失败
            DownloadError: 下载失败
        """
        # 验证参数
        if not prompt or not prompt.strip():
            raise ValidationError("图片描述 prompt 不能为空")
        
        if size not in VALID_SIZES:
            raise ValidationError(f"无效的尺寸参数：{size}，有效值：{', '.join(VALID_SIZES)}")
        
        logger.info(f"开始生成图片...")
        logger.info(f"Prompt: {prompt}")
        logger.info(f"尺寸：{size}")
        logger.info(f"水印：{'是' if watermark else '否'}")
        
        # 构建请求体
        body = self._build_request_body(prompt, size, watermark)
        
        # 调用 API
        logger.info("正在调用 API...")
        response = self._call_api(body)
        
        # 解析响应
        image_url = self._parse_response(response)
        logger.info("✓ API 调用成功")
        
        # 下载图片
        filename = self._generate_filename(prompt)
        output_path = self.output_dir / filename
        
        downloaded_path = self._download_image(image_url, output_path)
        
        # 输出结果
        logger.info("=" * 50)
        logger.info("图片生成完成！")
        logger.info("=" * 50)
        logger.info(f"文件路径：{downloaded_path.absolute()}")
        logger.info(f"Prompt: {prompt}")
        logger.info(f"尺寸：{size}")
        logger.info(f"水印：{'是' if watermark else '否'}")
        logger.info("=" * 50)
        
        return downloaded_path


class ValidationError(Exception):
    """参数验证错误"""
    pass


class APIError(Exception):
    """API 调用错误"""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class DownloadError(Exception):
    """下载错误"""
    pass


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        prog="doubao-image-generate",
        description="豆包文生图 API 调用脚本 - 使用火山引擎 ARK API 生成 AI 图片",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --prompt "一只在月光下的白色小猫"
  %(prog)s --prompt "赛博朋克城市夜景" --size 1080P
  %(prog)s --prompt "山水画" --no-watermark --output-dir ./artworks
  %(prog)s -p "抽象艺术" -s 720P -v

环境变量:
  ARK_API_KEY           - 火山引擎 ARK API Key（必需）
  DOUBAO_API_TIMEOUT    - API 超时时间（秒，默认：60）
  DOUBAO_RETRY_COUNT    - 失败重试次数（默认：3）
  DOUBAO_OUTPUT_DIR     - 默认输出目录（默认：generated-images）
  DOUBAO_VERBOSE        - 启用详细日志（true/false）
        """
    )
    
    parser.add_argument(
        "-p", "--prompt",
        type=str,
        required=True,
        help="图片描述文本（必需）"
    )
    
    parser.add_argument(
        "-s", "--size",
        type=str,
        default="2K",
        choices=VALID_SIZES,
        help="分辨率：2K, 1080P, 720P（默认：2K）"
    )
    
    parser.add_argument(
        "--watermark",
        action="store_true",
        default=True,
        help="添加水印（默认）"
    )
    
    parser.add_argument(
        "--no-watermark",
        action="store_false",
        dest="watermark",
        help="不添加水印"
    )
    
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default=None,
        help="输出目录（默认：generated-images 或 DOUBAO_OUTPUT_DIR 环境变量）"
    )
    
    parser.add_argument(
        "--timeout",
        type=int,
        default=None,
        help="API 超时时间（秒，默认：60 或 DOUBAO_API_TIMEOUT 环境变量）"
    )
    
    parser.add_argument(
        "--retry",
        type=int,
        default=None,
        help="失败重试次数（默认：3 或 DOUBAO_RETRY_COUNT 环境变量）"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="启用详细日志输出"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    return parser


def main():
    """主函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        # 创建生成器
        generator = DoubaoImageGenerator(
            timeout=args.timeout,
            retry_count=args.retry,
            output_dir=args.output_dir,
            verbose=args.verbose
        )
        
        # 生成图片
        output_path = generator.generate(
            prompt=args.prompt,
            size=args.size,
            watermark=args.watermark
        )
        
        # 输出用于 WorkBuddy 的结果标记
        print(f"\nRESULT_FILE={output_path.absolute()}")
        
        sys.exit(0)
        
    except ValidationError as e:
        logger.error(f"参数验证失败：{e}")
        sys.exit(1)
    except APIError as e:
        logger.error(f"API 错误：{e}")
        if e.status_code:
            logger.error(f"HTTP 状态码：{e.status_code}")
        sys.exit(2)
    except DownloadError as e:
        logger.error(f"下载错误：{e}")
        sys.exit(3)
    except KeyboardInterrupt:
        logger.warning("\n操作已取消")
        sys.exit(130)
    except Exception as e:
        logger.exception(f"未知错误：{e}")
        sys.exit(99)


if __name__ == "__main__":
    main()
