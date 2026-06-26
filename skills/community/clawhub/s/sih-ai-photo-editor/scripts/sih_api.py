#!/usr/bin/env python3
"""
Sih.Ai API Client
封装豆包图片编辑API，支持换装、换背景、换脸、风格转换等功能
"""

import requests
import base64
import os
from pathlib import Path
from typing import Optional, Union, List, Dict
from urllib.parse import urlparse
from .config import SIH_API_KEY, SIH_API_BASE_URL, DEFAULT_MODEL, DEFAULT_SIZE, API_TIMEOUT


class SihClient:
    """Sih.Ai图片编辑客户端"""

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化客户端

        Args:
            api_key: Sih.Ai API Key，如果不提供则从config.py读取
        """
        self.api_key = api_key or SIH_API_KEY
        if not self.api_key:
            raise ValueError(
                "API Key is required. Either pass api_key parameter "
                "or set SIH_API_KEY in config.py"
            )

        self.base_url = f"{SIH_API_BASE_URL}/v1/images/generations/"
        self.default_model = DEFAULT_MODEL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def edit_image(
        self,
        image: Union[str, Path],
        prompt: str,
        model: Optional[str] = None,
        size: Optional[str] = None
    ) -> Dict:
        """
        编辑图片

        Args:
            image: 图片URL、Base64字符串或本地文件路径
            prompt: 编辑指令（如"把衣服换成bikini"）
            model: 模型名称，默认使用 sihai-image-27
            size: 输出尺寸（如"1024x1024"），可选

        Returns:
            API响应字典，包含生成的图片URL

        Raises:
            ValueError: 图片格式不支持或无法访问
            requests.RequestException: API请求失败
        """
        # 准备图片数据
        image_data = self._prepare_image(image)

        # 构建请求
        payload = {
            "image": [image_data],
            "prompt": prompt,
            "model": model or self.default_model
        }

        # 调用API
        response = requests.post(
            self.base_url,
            json=payload,
            headers=self.headers,
            timeout=60
        )

        # 检查响应
        response.raise_for_status()
        result = response.json()

        # 返回第一个结果
        if "data" in result and len(result["data"]) > 0:
            return {
                "url": result["data"][0]["url"],
                "size": result["data"][0].get("size", "unknown"),
                "model": result.get("model"),
                "usage": result.get("usage", {})
            }
        else:
            raise ValueError("API returned no results")

    def batch_edit(
        self,
        images: List[Union[str, Path]],
        prompt: str,
        model: Optional[str] = None
    ) -> List[Dict]:
        """
        批量编辑图片

        Args:
            images: 图片列表（URL/路径/Base64）
            prompt: 编辑指令
            model: 模型名称

        Returns:
            结果列表
        """
        image_data_list = [self._prepare_image(img) for img in images]

        payload = {
            "image": image_data_list,
            "prompt": prompt,
            "model": model or self.default_model
        }

        response = requests.post(
            self.base_url,
            json=payload,
            headers=self.headers,
            timeout=120
        )

        response.raise_for_status()
        result = response.json()

        return [
            {
                "url": item["url"],
                "size": item.get("size", "unknown")
            }
            for item in result.get("data", [])
        ]

    def _prepare_image(self, image: Union[str, Path]) -> str:
        """
        准备图片数据（URL或Base64）

        Args:
            image: 图片URL、Base64字符串或本地路径

        Returns:
            可用于API的图片字符串
        """
        # 如果是Path对象，转为字符串
        if isinstance(image, Path):
            image = str(image)

        # 已经是Base64格式
        if image.startswith("data:image/"):
            return image

        # 判断是URL还是本地文件
        if self._is_url(image):
            # 验证URL可访问性
            if not self._validate_url(image):
                raise ValueError(f"无法访问图片URL: {image}")
            return image

        # 本地文件路径
        if os.path.exists(image):
            return self._file_to_base64(image)

        raise ValueError(
            f"不支持的图片格式。请提供："
            f"(1) 可访问的URL "
            f"(2) Base64格式(data:image/...) "
            f"(3) 本地文件路径"
        )

    @staticmethod
    def _is_url(text: str) -> bool:
        """判断是否为URL"""
        try:
            result = urlparse(text)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    @staticmethod
    def _validate_url(url: str) -> bool:
        """验证URL是否可访问"""
        try:
            response = requests.head(url, timeout=10, allow_redirects=True)
            return response.status_code == 200
        except Exception:
            return False

    @staticmethod
    def _file_to_base64(file_path: str) -> str:
        """
        将本地文件转换为Base64格式

        Args:
            file_path: 文件路径

        Returns:
            data:image/...;base64,... 格式的字符串
        """
        # 读取文件
        with open(file_path, "rb") as f:
            image_data = f.read()

        # 编码为Base64
        base64_data = base64.b64encode(image_data).decode("utf-8")

        # 获取图片格式
        ext = Path(file_path).suffix.lower().lstrip(".")
        if ext not in ["jpg", "jpeg", "png", "webp", "gif"]:
            ext = "jpg"  # 默认

        return f"data:image/{ext};base64,{base64_data}"

    def get_credits_info(self) -> Dict:
        """
        获取API Key的额度信息（如果Sih.Ai提供此接口）

        Returns:
            额度信息字典
        """
        # 这个需要Sih.Ai提供具体的查询接口
        # 临时实现，根据实际API调整
        try:
            response = requests.get(
                "https://api.vwu.ai/v1/user/credits",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}


# 便捷函数
def quick_edit(
    image: Union[str, Path],
    prompt: str,
    api_key: Optional[str] = None
) -> str:
    """
    快速编辑图片（返回图片URL）

    Args:
        image: 图片（URL/路径/Base64）
        prompt: 编辑指令
        api_key: API Key（可选，从环境变量读取）

    Returns:
        生成的图片URL
    """
    client = SihClient(api_key=api_key)
    result = client.edit_image(image, prompt)
    return result["url"]


# 命令行使用
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("用法: python sih_api.py <图片路径/URL> <prompt> [api_key]")
        print("示例: python sih_api.py photo.jpg '把衣服换成bikini'")
        sys.exit(1)

    image_input = sys.argv[1]
    prompt_text = sys.argv[2]
    key = sys.argv[3] if len(sys.argv) > 3 else None

    try:
        client = SihClient(api_key=key)
        result = client.edit_image(image_input, prompt_text)
        print(f"✅ 处理成功！")
        print(f"图片URL: {result['url']}")
        print(f"尺寸: {result['size']}")
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)
