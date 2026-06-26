#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片生成模块 - 优化版
调用 Nano Banana API (Grsai) 生成图片
支持 SSE 流式响应、队列控制、降级策略
"""

import os
import re
import json
import time
import threading
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed


@dataclass
class GenerationConfig:
    """生成配置"""
    model: str = "nano-banana-pro"
    width: int = 1024
    height: int = 1024
    num_images: int = 1
    style: str = "photorealistic"


class ImageGenerator:
    """
    图片生成器（Nano Banana API - Grsai 平台）
    
    优化点：
    - 队列控制：最多3张并行，超出排队
    - 超时：单张60秒，整体5分钟
    - 降级：重试1次失败则提示用户，不切即梦
    """
    
    # 类级别的并发控制
    _executor = ThreadPoolExecutor(max_workers=3)
    _lock = threading.Lock()
    _active_count = 0
    
    # 配置常量
    SINGLE_TIMEOUT = 60  # 单张图超时（秒）
    TOTAL_TIMEOUT = 300  # 整体任务超时（秒）
    MAX_RETRIES = 1  # 重试1次
    MAX_CONCURRENT = 3  # 最大并发数
    
    def __init__(self, api_key: str = None, use_overseas: bool = False):
        self.api_key = api_key or os.getenv('NANO_BANANA_API_KEY')
        
        # 海外节点和国内直连节点
        if use_overseas:
            base = "https://grsaiapi.com"
        else:
            base = "https://grsai.dakka.com.cn"
        
        self.endpoint = f"{base}/v1/draw/nano-banana"
        self.result_endpoint = f"{base}/v1/draw/result"
        self._start_time = None
    
    def generate_batch(
        self,
        prompts: List[Dict[str, Any]],
        callback: callable = None
    ) -> List[Dict[str, Any]]:
        """
        批量生成图片（带队列控制）
        
        Args:
            prompts: [{"name": "xxx", "prompt": "xxx", "config": config}]
            callback: 进度回调函数 (current, total, result)
        
        Returns:
            [{"name": "", "path": "", "success": bool, "error": ""}]
        """
        if not prompts:
            return []
        
        print(f"🎨 批量生成 {len(prompts)} 张图片（最多{self.MAX_CONCURRENT}张并行）...")
        
        results = []
        total = len(prompts)
        completed = 0
        
        # 分批执行，每批最多3个
        for i in range(0, total, self.MAX_CONCURRENT):
            batch = prompts[i:i + self.MAX_CONCURRENT]
            print(f"\n📦 批次 {i//self.MAX_CONCURRENT + 1}/{(total-1)//self.MAX_CONCURRENT + 1}（{len(batch)}张）")
            
            futures = {}
            for item in batch:
                future = self._executor.submit(
                    self._generate_single,
                    item.get("prompt", ""),
                    item.get("config", GenerationConfig()),
                    item.get("reference_images")
                )
                futures[future] = item
            
            # 等待批次完成
            for future in as_completed(futures, timeout=self.TOTAL_TIMEOUT):
                item = futures[future]
                try:
                    paths = future.result()
                    result = {
                        "name": item.get("name", ""),
                        "path": paths[0] if paths else None,
                        "success": len(paths) > 0,
                        "error": ""
                    }
                except Exception as e:
                    result = {
                        "name": item.get("name", ""),
                        "path": None,
                        "success": False,
                        "error": str(e)
                    }
                
                results.append(result)
                completed += 1
                
                if callback:
                    callback(completed, total, result)
                
                status = "✅" if result["success"] else "❌"
                print(f"   {status} {result['name']}")
        
        success_count = sum(1 for r in results if r["success"])
        print(f"\n📊 批量完成：{success_count}/{total} 张成功")
        
        return results
    
    def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        config: GenerationConfig = None,
        reference_images: List[str] = None,
        max_retries: int = None
    ) -> List[str]:
        """
        单张/多张图片生成（带降级策略）
        
        Args:
            max_retries: 最大重试次数（默认1次）
        
        Returns:
            图片路径列表，失败返回空列表
        """
        if max_retries is None:
            max_retries = self.MAX_RETRIES
        
        self._start_time = time.time()
        
        if not self.api_key:
            print("❌ 缺少 API Key")
            return []
        
        if config is None:
            config = GenerationConfig()
        
        print(f"🎨 Nano Banana API 生成中...")
        print(f"   尺寸：{config.width}x{config.height}")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        }
        
        payload = {
            "model": "nano-banana-pro",
            "prompt": prompt,
            "size": f"{config.width}x{config.height}",
            "n": config.num_images
        }
        
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt
        
        # 添加参考图片
        if reference_images:
            import base64
            payload["reference_images"] = []
            for img_path in reference_images:
                if os.path.exists(img_path):
                    with open(img_path, 'rb') as f:
                        img_base64 = base64.b64encode(f.read()).decode('utf-8')
                        payload["reference_images"].append(img_base64)
        
        # 重试机制（最多1次）
        for attempt in range(max_retries + 1):
            # 检查整体超时
            if time.time() - self._start_time > self.TOTAL_TIMEOUT:
                print(f"❌ 整体任务超时（>{self.TOTAL_TIMEOUT}秒）")
                return []
            
            if attempt > 0:
                print(f"   ⏳ 第{attempt}次重试...")
                time.sleep(3)
            
            try:
                paths = self._call_api(headers, payload, config)
                if paths:
                    return paths
            except Exception as e:
                print(f"   ❌ 调用失败：{e}")
                continue
        
        # 最终失败提示
        print(f"\n⚠️  Nano Banana 服务繁忙，生成失败")
        print(f"   建议：稍后重试，或检查网络连接")
        # 注意：即梦欠费，不自动切换
        return []
    
    def _call_api(
        self,
        headers: dict,
        payload: dict,
        config: GenerationConfig
    ) -> List[str]:
        """调用 API（内部方法）"""
        
        response = requests.post(
            self.endpoint,
            headers=headers,
            json=payload,
            stream=True,
            timeout=self.SINGLE_TIMEOUT
        )
        response.raise_for_status()
        
        # 解析 SSE 流
        final_result = self._parse_sse_stream(response)
        
        if not final_result:
            raise Exception("未获取到生成结果")
        
        status = final_result.get('status')
        if status != 'succeeded':
            error = final_result.get('failure_reason', '未知错误')
            raise Exception(f"生成失败：{error}")
        
        # 下载图片
        results = final_result.get('results', [])
        paths = []
        for idx, result in enumerate(results[:config.num_images], 1):
            url = result.get('url')
            if url:
                path = self._download_image(url, idx)
                if path:
                    paths.append(path)
        
        return paths
    
    def _generate_single(
        self,
        prompt: str,
        config: GenerationConfig,
        reference_images: List[str] = None
    ) -> List[str]:
        """线程安全的单张生成"""
        return self.generate(prompt, config=config, reference_images=reference_images)
    
    def _parse_sse_stream(self, response) -> Optional[Dict]:
        """解析 SSE 流式响应"""
        final_result = None
        
        for line in response.iter_lines():
            if not line:
                continue
            
            line_str = line.decode('utf-8')
            
            if line_str.startswith('data:'):
                data_str = line_str[5:].strip()
                
                try:
                    data = json.loads(data_str)
                    final_result = data
                    
                    progress = data.get('progress', 0)
                    status = data.get('status', 'pending')
                    
                    if status == 'running':
                        print(f"   生成中... {progress}%", end='\r')
                    elif status == 'succeeded':
                        print(f"   ✅ 生成完成！     ")
                    elif status == 'failed':
                        print(f"   ❌ 生成失败")
                        
                except json.JSONDecodeError:
                    continue
        
        return final_result
    
    def _download_image(self, url: str, index: int, save_dir: str = "/tmp") -> str:
        """下载图片"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"generated_{timestamp}_{index}.png"
            save_path = os.path.join(save_dir, filename)
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            size = len(response.content) / 1024
            return save_path
            
        except Exception as e:
            print(f"   ❌ 下载失败：{e}")
            return ""
    
    def build_prompt(
        self,
        product_features: Dict[str, Any],
        scheme: Any,
        shot: Any,
        language: str = "zh"
    ) -> str:
        """构建生成提示词"""
        base_prompt = f"{product_features.get('product_type', '产品')}，"
        base_prompt += f"{product_features.get('material', '')}，"
        base_prompt += f"{product_features.get('color', '')}"
        
        style_desc = f"{scheme.visual_language.lighting}，"
        style_desc += f"{scheme.visual_language.background_style}，"
        style_desc += f"{scheme.visual_language.composition}"
        
        shot_desc = f"{shot.description}，{shot.composition}"
        
        if language == "zh":
            prompt = f"{base_prompt}，{style_desc}，{shot_desc}，高清，专业摄影"
        else:
            prompt = f"{base_prompt}, {style_desc}, {shot_desc}, high quality, professional photography"
        
        return prompt
    
    def build_negative_prompt(self) -> str:
        """构建负面提示词"""
        return "模糊，低质量，变形，水印，文字，logo，低分辨率，噪点"


# ========== 便捷函数 ==========

def generate_product_image(
    prompt: str,
    width: int = 1024,
    height: int = 1024,
    num_images: int = 1,
    api_key: str = None
) -> List[str]:
    """便捷函数：生成产品图（单张）"""
    config = GenerationConfig(
        width=width,
        height=height,
        num_images=num_images
    )
    
    generator = ImageGenerator(api_key=api_key)
    return generator.generate(prompt, config=config)


def generate_batch_images(
    prompts: List[str],
    width: int = 1024,
    height: int = 1024,
    api_key: str = None,
    callback: callable = None
) -> List[Dict[str, Any]]:
    """
    便捷函数：批量生成（自动队列控制）
    
    Args:
        prompts: 提示词列表
        callback: 进度回调 (current, total, result)
    
    Returns:
        [{"path": "", "success": bool, "error": ""}]
    """
    items = [
        {
            "name": f"image_{i+1}.png",
            "prompt": p,
            "config": GenerationConfig(width=width, height=height, num_images=1)
        }
        for i, p in enumerate(prompts)
    ]
    
    generator = ImageGenerator(api_key=api_key)
    return generator.generate_batch(items, callback)


if __name__ == '__main__':
    # 测试
    print("🎨 Nano Banana 图片生成器 - 优化版测试")
    print("=" * 50)
    
    api_key = "sk-6fe41fd597614d2686f6d0685b4bd232"
    
    # 单张测试
    print("\n1. 单张生成测试")
    prompt = "绿植盆栽，陶瓷花盆，自然光线，木质背景，高清摄影"
    generator = ImageGenerator(api_key=api_key)
    paths = generator.generate(prompt, config=GenerationConfig(width=1024, height=1024))
    print(f"结果：{paths}")
    
    # 批量测试（5张，会自动分批）
    print("\n2. 批量生成测试（5张）")
    prompts = [
        "红色玫瑰花，白色背景，产品摄影",
        "蓝色绣球花，白色背景，产品摄影",
        "黄色向日葵，白色背景，产品摄影",
        "粉色樱花，白色背景，产品摄影",
        "紫色薰衣草，白色背景，产品摄影"
    ]
    
    def on_progress(current, total, result):
        print(f"   进度：{current}/{total}")
    
    results = generate_batch_images(prompts, callback=on_progress)
    success = sum(1 for r in results if r["success"])
    print(f"\n批量结果：{success}/{len(results)} 张成功")
