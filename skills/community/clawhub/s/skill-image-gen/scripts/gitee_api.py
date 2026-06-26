#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gitee AI API 封装模块
提供图片生成功能
"""

import base64
import os
from typing import Optional
import requests

from utils import base64_to_image, generate_timestamp_filename


class GiteeImageGenerator:
    """Gitee AI 图片生成器"""
    
    BASE_URL = "https://ai.gitee.com/v1"
    
    def __init__(
        self,
        api_key: str,
        model: str = "Kolors",
        cos_config: Optional[dict] = None
    ):
        """
        初始化生成器
        
        Args:
            api_key: Gitee AI API Key
            model: 使用的模型
            cos_config: 腾讯云 COS 配置 (可选)
        """
        self.api_key = api_key
        self.model = model
        self.cos_config = cos_config
        
        if not self.api_key:
            raise ValueError("API Key 不能为空")
    
    def generate(
        self,
        prompt: str,
        output_dir: str = "./output",
        upload_to_cos: bool = False,
        size: str = "1024x1024",
        n: int = 1
    ) -> dict:
        """
        生成图片
        
        Args:
            prompt: 图片描述提示词
            output_dir: 输出目录
            upload_to_cos: 是否上传到 COS
            size: 图片尺寸
            n: 生成数量
        
        Returns:
            包含图片信息的字典
        """
        # 调用 API 生成图片
        b64_image = self._call_api(prompt, size, n)
        
        # 保存到本地
        filename = generate_timestamp_filename()
        local_path = os.path.join(output_dir, filename)
        base64_to_image(b64_image, local_path)
        
        result = {
            "local_path": local_path,
            "filename": filename
        }
        
        # 上传到 COS
        if upload_to_cos and self.cos_config:
            cos_url = self._upload_to_cos(local_path, filename)
            result["cos_url"] = cos_url
            result["url"] = cos_url
        else:
            result["url"] = local_path
        
        return result
    
    def _call_api(self, prompt: str, size: str = "1024x1024", n: int = 1) -> str:
        """
        调用 Gitee AI API
        
        Args:
            prompt: 提示词
            size: 图片尺寸
            n: 生成数量
        
        Returns:
            Base64 编码的图片数据
        """
        url = f"{self.BASE_URL}/images/generations"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "n": n,
            "size": size,
            "response_format": "b64_json"
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        
        if response.status_code != 200:
            raise Exception(f"API 调用失败 ({response.status_code}): {response.text}")
        
        result = response.json()
        
        if "data" not in result or len(result["data"]) == 0:
            raise Exception("API 返回数据格式错误")
        
        return result["data"][0]["b64_json"]
    
    def _upload_to_cos(self, local_path: str, filename: str) -> str:
        """
        上传到腾讯云 COS
        
        Args:
            local_path: 本地文件路径
            filename: 文件名
        
        Returns:
            COS URL
        """
        from cos_uploader import CosUploader
        
        uploader = CosUploader(
            secret_id=self.cos_config['secret_id'],
            secret_key=self.cos_config['secret_key'],
            region=self.cos_config['region'],
            bucket=self.cos_config['bucket']
        )
        
        return uploader.upload(local_path, filename)
    
    @staticmethod
    def list_models() -> list:
        """获取支持的模型列表"""
        return [
            {"id": "Kolors", "name": "Kolors", "description": "快速文生图模型"},
            {"id": "flux-schnell", "name": "Flux Schnell", "description": "快速生成"},
            {"id": "stable-diffusion", "name": "Stable Diffusion", "description": "经典艺术风格"}
        ]
