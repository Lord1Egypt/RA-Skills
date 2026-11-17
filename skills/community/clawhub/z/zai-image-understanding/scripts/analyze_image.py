#!/usr/bin/env python3
"""
Z.ai GLM-4.1V-thinking-flash 图片理解分析脚本

使用 Z.ai API 进行图片理解和视觉分析任务。
支持将图片 URL 和提示词发送给模型，返回结构化分析结果。

优化版本：
- 默认 max_tokens 设为 4096（可通过 --max-tokens 调整：4096/8192/16384）
- 使用 requests.Session 复用连接，减少 TLS 握手开销
- 增加进度指示器 (--verbose) 显示请求状态
- 详细的时间统计和日志输出
- 提取 reasoning_content (thinking 过程)
"""

import os
import sys
import json
import argparse
import time
import requests
from typing import Dict, Any, Optional
from pathlib import Path


# 默认配置
DEFAULT_API_BASE = "https://open.bigmodel.cn/api/paas/v4"
DEFAULT_MODEL = "glm-4.1v-thinking-flash"
DEFAULT_TIMEOUT = 120  # 默认超时 120 秒，适应 thinking 模式
MAX_RETRIES = 2
RETRY_BACKOFF_BASE = 2  # 指数退避基数

# Token 限制配置
# 默认 4096；如输出被截断，可通过 --max-tokens 调整至 8192 或 16384
DEFAULT_MAX_TOKENS = 4096
MAX_TOKENS_OPTIONS = [4096, 8192, 16384]  # 允许的调整值

# 支持的图片格式及对应 MIME 类型
SUPPORTED_IMAGE_FORMATS = {
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.webp': 'image/webp',
    '.bmp': 'image/bmp',
    '.gif': 'image/gif',
}


def encode_image_to_base64(image_path: str) -> str:
    """将本地图片编码为 Base64 Data URL"""
    import base64
    from pathlib import Path
    
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"图片文件不存在: {image_path}")
    
    suffix = path.suffix.lower()
    mime_type = SUPPORTED_IMAGE_FORMATS.get(suffix, 'image/jpeg')
    
    with open(path, 'rb') as f:
        image_data = f.read()
    
    # 检查文件大小 (5MB 限制)
    if len(image_data) > 5 * 1024 * 1024:
        raise ValueError(f"图片大小超过 5MB 限制: {len(image_data) / 1024 / 1024:.2f} MB")
    
    base64_str = base64.b64encode(image_data).decode('utf-8')
    return f"data:{mime_type};base64,{base64_str}"


class ZaiImageAnalyzer:
    """Z.ai 图片分析器"""
    
    def __init__(
        self,
        api_key: str,
        api_base: str = DEFAULT_API_BASE,
        timeout: int = DEFAULT_TIMEOUT,
        verbose: bool = False,
        max_tokens: int = DEFAULT_MAX_TOKENS
    ):
        self.api_key = api_key
        self.api_base = api_base.rstrip('/')
        self.timeout = timeout
        self.verbose = verbose
        self.max_tokens = max_tokens
        self.endpoint = f"{self.api_base}/chat/completions"
        
        # 使用 Session 复用连接，减少 TLS 握手开销
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
        
        # 记录时间统计
        self.timing = {}
    
    def _log(self, msg: str, level: str = "INFO"):
        """条件性日志输出"""
        if self.verbose:
            timestamp = time.strftime("%H:%M:%S")
            print(f"[{timestamp}] [{level}] {msg}", file=sys.stderr)
    
    def _build_payload(self, image_url: str, prompt: str) -> Dict[str, Any]:
        """构建请求载荷
        
        image_url 可以是:
        - 公网 HTTP/HTTPS URL
        - Base64 Data URL (data:image/...;base64,...)
        """
        return {
            "model": DEFAULT_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url}
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
            "stream": False,
            "do_sample": True,
            "temperature": 0.8,
            "top_p": 0.6,
            "max_tokens": self.max_tokens,
            "tool_choice": "auto"
        }
    
    def _make_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """发送请求，包含重试逻辑和时间统计"""
        last_error = None
        
        for attempt in range(MAX_RETRIES + 1):
            try:
                self._log(f"发送请求 (尝试 {attempt + 1}/{MAX_RETRIES + 1})...")
                self._log(f"  模型: {payload['model']}, max_tokens: {payload['max_tokens']}, temperature: {payload['temperature']}")
                
                # 记录请求开始时间
                request_start = time.perf_counter()
                
                response = self.session.post(
                    self.endpoint,
                    json=payload,
                    timeout=self.timeout
                )
                
                # 记录响应时间
                response_time = time.perf_counter() - request_start
                self._log(f"收到响应，耗时: {response_time:.2f}s, 状态码: {response.status_code}")
                
                # 处理 HTTP 错误状态码
                if response.status_code == 401:
                    return {"success": False, "error": "API 认证失败，请检查 ZAI_API_KEY 配置"}
                elif response.status_code == 400:
                    return {"success": False, "error": f"请求参数错误: {response.text}"}
                elif response.status_code == 429:
                    # 速率限制，尝试读取 Retry-After
                    retry_after = response.headers.get('Retry-After', '60')
                    try:
                        wait_time = int(retry_after)
                    except ValueError:
                        wait_time = 60
                    if attempt < MAX_RETRIES:
                        self._log(f"速率限制，等待 {wait_time}s 后重试...", "WARN")
                        time.sleep(wait_time)
                        continue
                    return {"success": False, "error": f"速率限制，等待 {wait_time} 秒后仍未恢复"}
                elif 500 <= response.status_code < 600:
                    if attempt < MAX_RETRIES:
                        wait_time = RETRY_BACKOFF_BASE ** attempt
                        self._log(f"服务器错误 ({response.status_code})，{wait_time}s 后重试...", "WARN")
                        time.sleep(wait_time)
                        continue
                    return {"success": False, "error": f"服务器错误 ({response.status_code}): {response.text}"}
                elif response.status_code != 200:
                    return {"success": False, "error": f"HTTP {response.status_code}: {response.text}"}
                
                # 解析响应
                parse_start = time.perf_counter()
                data = response.json()
                parse_time = time.perf_counter() - parse_start
                self._log(f"JSON 解析耗时: {parse_time:.3f}s")
                
                # 提取内容
                content = ""
                reasoning_content = ""
                if "choices" in data and len(data["choices"]) > 0:
                    choice = data["choices"][0]
                    if "message" in choice and "content" in choice["message"]:
                        content = choice["message"]["content"]
                    # 提取 reasoning_content (thinking 过程)
                    if "message" in choice and "reasoning_content" in choice["message"]:
                        reasoning_content = choice["message"]["reasoning_content"]
                
                if not content:
                    return {"success": False, "error": "模型返回空内容，请尝试调整提示词或重试"}
                
                # 记录使用统计
                usage = data.get("usage", {})
                if usage and self.verbose:
                    self._log(f"Token 使用: prompt={usage.get('prompt_tokens', 'N/A')}, "
                              f"completion={usage.get('completion_tokens', 'N/A')}, "
                              f"total={usage.get('total_tokens', 'N/A')}")
                    if reasoning_content:
                        self._log(f"Thinking 内容长度: {len(reasoning_content)} 字符")
                
                return {
                    "success": True,
                    "content": content,
                    "reasoning_content": reasoning_content,
                    "raw_response": data,
                    "usage": usage,
                    "timing": {
                        "request_time": response_time,
                        "parse_time": parse_time,
                        "total_time": response_time + parse_time
                    },
                    "error": None
                }
                
            except requests.exceptions.Timeout:
                last_error = "请求超时"
                self._log(f"请求超时 ({self.timeout}s)", "ERROR")
                if attempt < MAX_RETRIES:
                    wait_time = RETRY_BACKOFF_BASE ** attempt
                    self._log(f"{wait_time}s 后重试...", "WARN")
                    time.sleep(wait_time)
                    continue
            except requests.exceptions.ConnectionError:
                last_error = "网络连接失败"
                self._log("网络连接失败", "ERROR")
                if attempt < MAX_RETRIES:
                    wait_time = RETRY_BACKOFF_BASE ** attempt
                    self._log(f"{wait_time}s 后重试...", "WARN")
                    time.sleep(wait_time)
                    continue
            except requests.exceptions.RequestException as e:
                last_error = f"请求异常: {str(e)}"
                self._log(f"请求异常: {e}", "ERROR")
                if attempt < MAX_RETRIES:
                    wait_time = RETRY_BACKOFF_BASE ** attempt
                    self._log(f"{wait_time}s 后重试...", "WARN")
                    time.sleep(wait_time)
                    continue
            except json.JSONDecodeError:
                last_error = "响应解析失败"
                self._log("JSON 解析失败", "ERROR")
                if attempt < MAX_RETRIES:
                    wait_time = RETRY_BACKOFF_BASE ** attempt
                    self._log(f"{wait_time}s 后重试...", "WARN")
                    time.sleep(wait_time)
                    continue
            except Exception as e:
                last_error = f"未知错误: {str(e)}"
                self._log(f"未知错误: {e}", "ERROR")
                if attempt < MAX_RETRIES:
                    wait_time = RETRY_BACKOFF_BASE ** attempt
                    self._log(f"{wait_time}s 后重试...", "WARN")
                    time.sleep(wait_time)
                    continue
        
        return {"success": False, "error": f"{last_error}，重试 {MAX_RETRIES} 次后仍然失败"}
    
    def analyze(self, image_url: str, prompt: str) -> Dict[str, Any]:
        """
        分析图片
        
        Args:
            image_url: 图片的公网访问 URL 或 Base64 Data URL
            prompt: 分析提示词
            
        Returns:
            包含 success、content、reasoning_content、raw_response、usage、timing、error 字段的字典
        """
        # 基础验证
        if not image_url:
            return {"success": False, "error": "图片 URL 不能为空"}
        
        # 支持 HTTP/HTTPS URL 和 Data URL (Base64)
        is_http_url = image_url.startswith(('http://', 'https://'))
        is_data_url = image_url.startswith('data:image/')
        
        if not is_http_url and not is_data_url:
            return {"success": False, "error": "图片 URL 必须是 HTTP/HTTPS 链接或 Base64 Data URL (data:image/...)"}
        
        if not prompt or not prompt.strip():
            return {"success": False, "error": "提示词不能为空"}
        
        self._log(f"开始分析图片: {image_url[:80]}{'...' if len(image_url) > 80 else ''}")
        self._log(f"提示词: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
        
        start_time = time.perf_counter()
        payload = self._build_payload(image_url, prompt.strip())
        result = self._make_request(payload)
        total_time = time.perf_counter() - start_time
        
        # 添加总耗时信息
        if result.get("success") and "timing" in result:
            result["timing"]["total_elapsed"] = total_time
        
        if result.get("success"):
            self._log(f"分析完成，总耗时: {total_time:.2f}s")
        else:
            self._log(f"分析失败: {result.get('error')}", "ERROR")
        
        return result
    
    def analyze_local(self, image_path: str, prompt: str) -> Dict[str, Any]:
        """
        分析本地图片文件（自动转换为 Base64）
        
        Args:
            image_path: 本地图片文件路径
            prompt: 分析提示词
            
        Returns:
            包含 success、content、reasoning_content、raw_response、usage、timing、error 字段的字典
        """
        try:
            self._log(f"读取本地图片: {image_path}")
            data_url = encode_image_to_base64(image_path)
            self._log(f"Base64 编码完成，长度: {len(data_url)} 字符")
            return self.analyze(data_url, prompt)
        except Exception as e:
            return {"success": False, "error": f"本地图片处理失败: {str(e)}"}
    
    def close(self):
        """关闭 Session 连接"""
        self.session.close()


def main():
    parser = argparse.ArgumentParser(
        description="Z.ai GLM-4.1V-thinking-flash 图片理解分析工具 (优化版)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例:
  # 基础用法 (公网 URL)
  python analyze_image.py --image-url "https://example.com/image.jpg" --prompt "描述这张图片"
  
  # 本地文件上传
  python analyze_image.py --image-path "/path/to/image.jpg" --prompt "提取文字"
  
  # 详细模式 (显示进度和时间统计)
  python analyze_image.py --image-path "image.jpg" --prompt "分析图表" --verbose
  
  # 增加 max_tokens 解决输出截断 (默认 4096，可选 4096/8192/16384)
  python analyze_image.py --image-path "image.jpg" --prompt "详细分析" --max-tokens 8192
  
  # 自定义超时和输出
  python analyze_image.py --image-path "image.jpg" --prompt "详细分析" --timeout 180 --output result.json --pretty

环境变量:
  ZAI_API_KEY        - API Key (必需)
  ZAI_API_BASE       - API 基础地址 (默认: https://open.bigmodel.cn/api/paas/v4)
  ZAI_DEFAULT_TIMEOUT - 默认超时秒数 (默认: 120)
        """
    )
    
    parser.add_argument(
        "--image-url", "-u",
        help="图片的公网访问 URL (必须是 http/https)"
    )
    parser.add_argument(
        "--image-path", "-i",
        help="本地图片文件路径 (自动转为 Base64)"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="发送给模型的分析提示词"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="Z.ai API Key (默认读取环境变量 ZAI_API_KEY)"
    )
    parser.add_argument(
        "--api-base",
        default=os.environ.get("ZAI_API_BASE", DEFAULT_API_BASE),
        help=f"API 基础地址 (默认: {DEFAULT_API_BASE})"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=int(os.environ.get("ZAI_DEFAULT_TIMEOUT", DEFAULT_TIMEOUT)),
        help=f"请求超时秒数 (默认: {DEFAULT_TIMEOUT})"
    )
    parser.add_argument(
        "--output", "-o",
        help="输出文件路径 (默认输出到 stdout)"
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="美化 JSON 输出"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="显示详细进度和时间统计"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        choices=MAX_TOKENS_OPTIONS,
        default=DEFAULT_MAX_TOKENS,
        help=f"最大输出 tokens (默认: {DEFAULT_MAX_TOKENS}，可选: {', '.join(map(str, MAX_TOKENS_OPTIONS))})"
    )
    
    args = parser.parse_args()
    
    # 获取 API Key
    api_key = args.api_key or os.environ.get("ZAI_API_KEY")
    if not api_key:
        print(json.dumps({
            "success": False,
            "error": "未提供 API Key，请通过 --api-key 参数或设置 ZAI_API_KEY 环境变量"
        }, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    
    # 创建分析器并执行
    analyzer = ZaiImageAnalyzer(
        api_key=api_key,
        api_base=args.api_base,
        timeout=args.timeout,
        verbose=args.verbose,
        max_tokens=args.max_tokens
    )
    
    try:
        # 优先使用本地图片路径，否则使用 URL
        if args.image_path:
            result = analyzer.analyze_local(args.image_path, args.prompt)
        elif args.image_url:
            result = analyzer.analyze(args.image_url, args.prompt)
        else:
            print(json.dumps({
                "success": False,
                "error": "必须提供 --image-url 或 --image-path 参数之一"
            }, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)
    finally:
        analyzer.close()
    
    # 输出结果
    output_json = json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None)
    
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output_json)
            print(f"结果已保存到: {args.output}", file=sys.stderr)
        except Exception as e:
            print(f"写入文件失败: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output_json)
    
    # 非零退出码表示失败
    if not result.get("success", False):
        sys.exit(1)


if __name__ == "__main__":
    main()