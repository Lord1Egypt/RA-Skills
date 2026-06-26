#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wan2.6 图片生成工具
使用阿里云万相 2.6 模型生成微信公众号封面图和技术架构设计图
"""

import os
import sys
import time
import argparse
import json
from typing import Optional, List, Dict, Any

try:
    import dashscope
    from dashscope.aigc.image_generation import ImageGeneration
    from dashscope.api_entities.dashscope_response import Message
except ImportError:
    print("错误：请先安装 dashscope SDK")
    print("安装命令：pip install dashscope")
    sys.exit(1)

# 与 ~/.workbuddy/skills 下本技能文件夹名一致，作为 $HOME/WorkBuddy/<技能名> 的最后一级目录名
_SKILL_ROOT = os.path.dirname(os.path.abspath(__file__))
_SKILL_NAME = os.path.basename(_SKILL_ROOT)


class Wan26ImageGenerator:
    """wan2.6 图片生成器"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        region: str = "beijing",
        verbose: bool = True
    ):
        """
        初始化生成器
        
        Args:
            api_key: 阿里云 API Key，如不提供则从环境变量读取
            region: 地域，支持 beijing, singapore, virginia
        """
        self.verbose = verbose
        if not api_key:
            load_local_env()
        self.api_key = api_key or (
            os.getenv("DASHSCOPE_API_KEY")
            or os.getenv("QWEN_API_KEY")
            or os.getenv("ALIYUN_DASHSCOPE_API_KEY")
        )
        if not self.api_key:
            raise ValueError(
                "未提供 API Key，请通过 --api-key 或环境变量 "
                "DASHSCOPE_API_KEY / QWEN_API_KEY 设置"
            )
        
        # 设置地域对应的 API 地址
        region_urls = {
            "beijing": "https://dashscope.aliyuncs.com/api/v1",
            "singapore": "https://dashscope-intl.aliyuncs.com/api/v1",
            "virginia": "https://dashscope-us.aliyuncs.com/api/v1"
        }
        
        if region not in region_urls:
            raise ValueError(f"不支持的地域：{region}，支持：beijing, singapore, virginia")
        
        dashscope.base_http_api_url = region_urls[region]
        self._log(f"使用地域：{region}")
        self._log(f"API 地址：{dashscope.base_http_api_url}")

    def _log(self, message: str):
        if self.verbose:
            print(message, file=sys.stderr)
    
    def generate_wx_cover(self, title: str, content: Optional[str] = None, 
                          style: Optional[str] = None) -> Dict[str, Any]:
        """
        生成微信公众号封面图（16:9 比例）
        
        Args:
            title: 文章标题
            content: 文章内容摘要或关键词
            style: 风格描述
            
        Returns:
            包含图片 URL 和任务信息的字典
        """
        # 构建提示词
        prompt = self._build_cover_prompt(title, content, style)
        
        self._log(f"\n开始生成微信公众号封面图...")
        self._log(f"提示词：{prompt}")
        
        # 使用异步调用
        return self._generate_image_async(
            prompt=prompt,
            size="1280*720",  # 16:9 微信公众号封面比例
            n=1,
            enable_interleave=True  # 文生图模式：True
        )
    
    def generate_tech_diagram(self, description: str, components: Optional[str] = None,
                              style: Optional[str] = None) -> Dict[str, Any]:
        """
        生成技术架构设计图
        
        Args:
            description: 技术架构描述
            components: 主要组件列表，逗号分隔
            style: 图表风格
            
        Returns:
            包含图片 URL 和任务信息的字典
        """
        # 构建提示词
        prompt = self._build_tech_prompt(description, components, style)
        
        self._log(f"\n开始生成技术架构图...")
        self._log(f"提示词：{prompt}")
        
        # 使用异步调用
        return self._generate_image_async(
            prompt=prompt,
            size="1280*1280",  # 正方形适合架构图
            n=1,
            enable_interleave=True
        )
    
    def generate_article_images(self, content: str, count: int = 3,
                                size: str = "1280*720") -> Dict[str, Any]:
        """
        生成文章配图（支持多张）
        
        Args:
            content: 段落内容
            count: 生成图片数量，1-5
            size: 图片尺寸
            
        Returns:
            包含图片 URL 列表和任务信息的字典
        """
        if count < 1 or count > 5:
            raise ValueError("图片数量必须在 1-5 之间")
        
        prompt = f"根据以下内容生成{count}张配图，要求风格统一，清晰美观：\n\n{content}"
        
        self._log(f"\n开始生成{count}张文章配图...")
        self._log(f"提示词：{prompt[:200]}...")
        
        # 使用异步调用
        return self._generate_image_async(
            prompt=prompt,
            size=size,
            n=count,
            enable_interleave=True
        )
    
    def _build_cover_prompt(self, title: str, content: Optional[str], 
                           style: Optional[str]) -> str:
        """构建封面图提示词"""
        base_prompt = f"微信公众号文章封面图，标题：{title}"
        
        if content:
            base_prompt += f"\n内容关键词：{content}"
        
        if style:
            base_prompt += f"\n风格要求：{style}"
        
        # 添加通用要求
        base_prompt += "\n要求：高清，专业，吸引眼球，适合做封面，无文字或少文字"
        
        return base_prompt
    
    def _build_tech_prompt(self, description: str, components: Optional[str],
                          style: Optional[str]) -> str:
        """构建技术架构图提示词"""
        base_prompt = f"技术架构设计图：{description}"
        
        if components:
            base_prompt += f"\n主要组件：{components}"
        
        if style:
            base_prompt += f"\n风格：{style}"
        
        # 添加通用要求
        base_prompt += "\n要求：清晰的框图，专业的技术架构图，线条简洁，布局合理，适合技术文档"
        
        return base_prompt
    
    def _generate_image_async(self, prompt: str, size: str = "1K", n: int = 1,
                             enable_interleave: bool = False) -> Dict[str, Any]:
        """
        异步调用生成图片
        
        Args:
            prompt: 提示词
            size: 图片尺寸
            n: 图片数量
            enable_interleave: 是否启用图文混排
            
        Returns:
            包含结果的字典
        """
        try:
            # 创建消息
            message = Message(
                role="user",
                content=[{"text": prompt}]
            )
            
            # 创建异步任务
            self._log("创建异步任务...")
            
            # enable_interleave=True: 文生图模式（纯文本生成图片）
            # enable_interleave=False: 图生图模式（需要提供输入图片）
            # 根据参数决定，不强制覆盖
            use_interleave = enable_interleave
            
            response = ImageGeneration.async_call(
                model="wan2.6-image",
                api_key=self.api_key,
                messages=[message],
                negative_prompt="低分辨率，低画质，畸形，模糊，水印，文字错误",
                prompt_extend=True,  # 开启智能改写
                watermark=False,     # 不添加水印
                n=n,
                enable_interleave=use_interleave,
                size=size
            )
            
            if response.status_code != 200:
                raise Exception(f"创建任务失败：{response.code} - {response.message}")
            
            task_id = response.output.task_id
            self._log(f"任务创建成功，Task ID: {task_id}")
            
            # 轮询等待任务完成
            self._log("等待任务完成...")
            return self._wait_for_task(task_id)
            
        except Exception as e:
            self._log(f"生成失败：{str(e)}")
            return {"success": False, "error": str(e)}
    
    def _wait_for_task(self, task_id: str, poll_interval: int = 10, 
                      max_wait: int = 300) -> Dict[str, Any]:
        """
        轮询等待任务完成
        
        Args:
            task_id: 任务 ID
            poll_interval: 轮询间隔（秒）
            max_wait: 最大等待时间（秒）
            
        Returns:
            包含结果的字典
        """
        start_time = time.time()
        
        while True:
            elapsed = time.time() - start_time
            if elapsed > max_wait:
                return {
                    "success": False,
                    "error": f"等待超时（{max_wait}秒）",
                    "task_id": task_id
                }
            
            try:
                # 直接使用 HTTP API 查询任务状态
                import requests
                url = f"{dashscope.base_http_api_url}/tasks/{task_id}"
                headers = {
                    "Authorization": f"Bearer {self.api_key}"
                }
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    result_data = response.json()
                    # 手动构建状态对象
                    class TaskStatus:
                        def __init__(self, data):
                            self.output = type('obj', (object,), {
                                'task_id': data.get('output', {}).get('task_id'),
                                'task_status': data.get('output', {}).get('task_status'),
                                'choices': data.get('output', {}).get('choices', []),
                                'finished': data.get('output', {}).get('finished', False)
                            })()
                            self.usage = type('obj', (object,), {
                                'size': data.get('usage', {}).get('size', 'unknown'),
                                'image_count': data.get('usage', {}).get('image_count', 0)
                            })()
                    
                    status = TaskStatus(result_data)
                else:
                    self._log(f"查询任务失败：{response.status_code}")
                    time.sleep(poll_interval)
                    continue
                
                task_status = status.output.task_status
                self._log(f"当前状态：{task_status}（已等待{int(elapsed)}秒）")
                
                if task_status == "SUCCEEDED":
                    self._log("任务完成！")
                    return self._parse_success_result(status)
                elif task_status == "FAILED":
                    # 获取详细错误信息
                    error_msg = "任务执行失败"
                    if hasattr(status, 'output') and hasattr(status.output, 'choices'):
                        choices = status.output.choices
                        if choices and len(choices) > 0:
                            choice = choices[0]
                            if isinstance(choice, dict) and 'message' in choice:
                                error_msg = choice.get('message', error_msg)
                            elif hasattr(choice, 'get'):
                                error_msg = choice.get('message', error_msg)
                    self._log(f"失败详情：{error_msg}")
                    return {
                        "success": False,
                        "error": error_msg,
                        "task_id": task_id
                    }
                elif task_status == "CANCELED":
                    return {
                        "success": False,
                        "error": "任务已取消",
                        "task_id": task_id
                    }
                
                # 继续等待
                time.sleep(poll_interval)
                
            except Exception as e:
                self._log(f"查询任务状态失败：{str(e)}")
                time.sleep(poll_interval)
    
    def _parse_success_result(self, status) -> Dict[str, Any]:
        """解析成功结果"""
        result = {
            "success": True,
            "task_id": status.output.task_id,
            "images": [],
            "size": status.usage.size if hasattr(status.usage, 'size') else "unknown",
            "image_count": status.usage.image_count if hasattr(status.usage, 'image_count') else 0
        }
        
        if status.output.choices:
            for choice in status.output.choices:
                message = getattr(choice, "message", None)
                content = getattr(message, "content", None)
                if not content and isinstance(choice, dict):
                    message = choice.get("message", {})
                    content = message.get("content", [])
                if not content:
                    continue

                for item in content:
                    item_type = getattr(item, "type", None)
                    item_image = getattr(item, "image", None)
                    if isinstance(item, dict):
                        item_type = item.get("type", item_type)
                        item_image = item.get("image", item_image)

                    if item_type == "image" and item_image:
                        result["images"].append({
                            "url": item_image,
                            "type": "image"
                        })
        
        return result


def _apply_env_file(path: str) -> None:
    """将 .env 中未出现在 os.environ 的键写入环境（与 OpenClaw / dotenv 行为一致，不覆盖已有变量）。"""
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            if line.startswith("export "):
                line = line[7:].strip()
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            if not key or " " in key:
                continue
            if key in os.environ:
                continue
            if (value.startswith('"') and value.endswith('"')) or (
                value.startswith("'") and value.endswith("'")
            ):
                value = value[1:-1]
            os.environ[key] = value


def load_local_env() -> None:
    """按 OpenClaw 习惯从多个路径加载 .env（仅补充缺失变量）。"""
    candidates = []
    custom = os.getenv("OPENCLAW_ENV_FILE")
    if custom:
        candidates.append(custom)
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    candidates.append(os.path.join(skill_dir, ".env"))
    home = os.path.expanduser("~")
    candidates.append(os.path.join(home, ".openclaw", ".env"))
    candidates.append(os.path.join(home, ".workbuddy", ".env"))
    seen = set()
    for env_path in candidates:
        if not env_path or env_path in seen:
            continue
        seen.add(env_path)
        _apply_env_file(env_path)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="wan2.6 图片生成工具")
    parser.add_argument("--api-key", type=str, help="阿里云 API Key（可选）")
    parser.add_argument("--region", type=str, default="beijing", 
                       choices=["beijing", "singapore", "virginia"],
                       help="API 地域")
    parser.add_argument("--json-only", action="store_true", help="仅输出 JSON 到 stdout")
    parser.add_argument(
        "--output-dir",
        type=str,
        help=f"图片保存目录（默认 ~/WorkBuddy/{_SKILL_NAME}，与技能根目录名一致）",
    )
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # 封面图命令
    cover_parser = subparsers.add_parser("cover", help="生成微信公众号封面图")
    cover_parser.add_argument("--title", type=str, required=True, help="文章标题")
    cover_parser.add_argument("--content", type=str, help="内容摘要")
    cover_parser.add_argument("--style", type=str, help="风格描述")
    
    # 技术架构图命令
    tech_parser = subparsers.add_parser("tech", help="生成技术架构图")
    tech_parser.add_argument("--description", type=str, required=True, help="架构描述")
    tech_parser.add_argument("--components", type=str, help="组件列表")
    tech_parser.add_argument("--style", type=str, help="风格")
    
    # 文章配图命令
    article_parser = subparsers.add_parser("article", help="生成文章配图")
    article_parser.add_argument("--content", type=str, required=True, help="段落内容")
    article_parser.add_argument("--count", type=int, default=3, help="图片数量")
    article_parser.add_argument("--size", type=str, default="1280*720", help="图片尺寸")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)

    default_output = os.path.join(os.path.expanduser("~"), "WorkBuddy", _SKILL_NAME)
    output_dir = getattr(args, "output_dir", None) or default_output

    try:
        load_local_env()
        generator = Wan26ImageGenerator(
            api_key=args.api_key,
            region=args.region,
            verbose=not args.json_only
        )
        
        if args.command == "cover":
            result = generator.generate_wx_cover(
                title=args.title,
                content=args.content,
                style=args.style
            )
        elif args.command == "tech":
            result = generator.generate_tech_diagram(
                description=args.description,
                components=args.components,
                style=args.style
            )
        elif args.command == "article":
            result = generator.generate_article_images(
                content=args.content,
                count=args.count,
                size=args.size
            )
        
        if result.get("success") and result.get("images"):
            os.makedirs(output_dir, exist_ok=True)
            import requests as _req
            saved = []
            for idx, img in enumerate(result["images"]):
                ext = "png"
                fname = f"image_{idx + 1}.{ext}" if len(result["images"]) > 1 else f"cover.{ext}"
                fpath = os.path.join(output_dir, fname)
                try:
                    resp = _req.get(img["url"], timeout=60)
                    resp.raise_for_status()
                    with open(fpath, "wb") as fp:
                        fp.write(resp.content)
                    img["local_path"] = fpath
                    saved.append(fpath)
                except Exception as dl_err:
                    if not args.json_only:
                        print(f"  ⚠️  下载失败: {dl_err}", file=sys.stderr)
            result["output_dir"] = output_dir
            result["saved_files"] = saved

        if args.json_only:
            print(json.dumps(result, ensure_ascii=False))
        else:
            print("\n" + "="*60)
            print("生成结果：")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
            if result.get("success") and result.get("images"):
                print(f"\n图片已保存到: {output_dir}")
                for img in result["images"]:
                    if img.get("local_path"):
                        print(f"  - {img['local_path']}")
                    else:
                        print(f"  - {img['url']}（仅 URL，下载失败）")
        
    except Exception as e:
        if args.json_only:
            print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False))
        else:
            print(f"\n❌ 错误：{str(e)}")
            print("\n任务中断，请检查：")
            print("  1. 环境变量 DASHSCOPE_API_KEY 是否已配置")
            print("  2. API Key 是否有效")
            print("  3. 网络连接是否正常")
        sys.exit(1)


if __name__ == "__main__":
    main()
