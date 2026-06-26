#!/usr/bin/env python3
"""
Subtitle Refiner - AI驱动的字幕优化模块

使用 SiliconFlow GLM-4.7 模型优化 SRT 字幕文件：
- 去除语气词（嗯、啊、那个等）
- 修正 ASR 识别错误（XGBT→ChatGPT, RG→RAG）
- 保持时间戳完全不变
- 通过 Feishu 发送优化结果
"""

import os
import re
import subprocess
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# 确保输出编码为 UTF-8
if sys.version_info >= (3, 7):
    sys.stdout.reconfigure(encoding="utf-8")

# =====================
# API 配置
# =====================

SILICONFLOW_API_KEY = os.environ.get("SILICONFLOW_API_KEY", "").strip()
API_ENDPOINT = "https://api.siliconflow.cn/v1/chat/completions"
PRIMARY_MODEL = "Pro/zai-org/GLM-4.7"
FALLBACK_MODEL = "Qwen/Qwen2.5-7B-Instruct"

# 错误提示映射字典
ERROR_SOLUTIONS = {
    "401": {
        "emoji": "🔑",
        "title": "API Key 错误",
        "solution": "请检查环境变量 SILICONFLOW_API_KEY 是否正确"
    },
    "402": {
        "emoji": "💰",
        "title": "余额不足",
        "solution": "请充值：https://cloud.siliconflow.cn/me/account/ak"
    },
    "403": {
        "emoji": "🚫",
        "title": "权限不足",
        "solution": "请检查账户状态和 API 权限"
    },
    "429": {
        "emoji": "⏳",
        "title": "请求过于频繁",
        "solution": "请稍后重试"
    },
    "timeout": {
        "emoji": "⏱️",
        "title": "请求超时",
        "solution": "请检查网络连接或稍后重试"
    },
    "connection": {
        "emoji": "🔌",
        "title": "网络连接失败",
        "solution": "请检查网络设置和代理配置"
    }
}


# =====================
# 速率限制器
# =====================

class RateLimiter:
    """速率限制器 - 控制每秒和每分钟的请求数"""

    def __init__(self, max_per_second=10, max_per_minute=200):
        """
        初始化速率限制器

        Args:
            max_per_second: 每秒最大请求数
            max_per_minute: 每分钟最大请求数
        """
        self.max_per_second = max_per_second
        self.max_per_minute = max_per_minute
        self.request_times = []
        self.lock = threading.Lock()

    def acquire(self):
        """获取许可，如果超限则等待"""
        with self.lock:
            now = time.time()

            # 清理超过 1 分钟的旧记录
            self.request_times = [t for t in self.request_times if now - t < 60]

            # 检查并等待每分钟限制
            while len(self.request_times) >= self.max_per_minute:
                oldest_request = min(self.request_times)
                wait_time = 60 - (now - oldest_request) + 0.1
                print(f"  ⏳ 达到每分钟限制({self.max_per_minute}次/分)，等待 {wait_time:.1f}秒...", file=sys.stderr)
                time.sleep(wait_time)
                now = time.time()
                self.request_times = [t for t in self.request_times if now - t < 60]

            # 检查并等待每秒限制
            recent_second = len([t for t in self.request_times if now - t < 1])
            while recent_second >= self.max_per_second:
                # 计算需要等待的时间
                if self.request_times:
                    last_request_time = max([t for t in self.request_times if now - t < 1])
                    wait_time = 1.0 - (now - last_request_time)
                else:
                    wait_time = 0
                if wait_time > 0:
                    print(f"  ⏳ 达到每秒限制({self.max_per_second}次/秒)，等待 {wait_time:.1f}秒...", file=sys.stderr)
                    time.sleep(wait_time)
                    now = time.time()

            # 记录这次请求
            self.request_times.append(now)


# 全局速率限制器实例
API_RATE_LIMITER = RateLimiter(max_per_second=10, max_per_minute=200)


# =====================
# 环境检测函数
# =====================

def check_network_connection() -> bool:
    """
    检测网络连接是否正常

    Returns:
        bool: 网络连接正常返回 True，否则返回 False
    """
    try:
        import socket
        socket.create_connection(("www.siliconflow.cn", 443), timeout=5)
        return True
    except OSError:
        return False


def check_api_key_validity() -> Tuple[bool, str]:
    """
    验证 API Key 是否有效

    Returns:
        (是否有效, 错误消息)
    """
    if not SILICONFLOW_API_KEY:
        return False, "API Key 未设置"

    try:
        import requests
        # 发送一个简单的测试请求
        test_response = requests.get(
            "https://api.siliconflow.cn/v1/models",
            headers={"Authorization": f"Bearer {SILICONFLOW_API_KEY}"},
            timeout=10
        )

        if test_response.status_code == 401:
            return False, "API Key 无效或已过期"
        elif test_response.status_code == 403:
            return False, "API 权限不足或余额不足"
        elif test_response.status_code == 200:
            return True, "API Key 有效"
        else:
            return False, f"API 返回状态码 {test_response.status_code}"

    except ImportError:
        return False, "缺少 requests 库"
    except Exception as e:
        return False, f"网络连接失败: {str(e)}"


# =====================
# API 调用函数
# =====================

def validate_api_key() -> bool:
    """验证 API Key 是否存在"""
    if not SILICONFLOW_API_KEY:
        raise RuntimeError(
            "缺少 SILICONFLOW_API_KEY 环境变量。"
            "请设置：export SILICONFLOW_API_KEY=your_key"
        )
    return True


def call_siliconflow_api(
    prompt: str,
    model: Optional[str] = None,
    temperature: float = 0.2,
    system_message: Optional[str] = None
) -> Tuple[str, int, int]:
    """
    调用 SiliconFlow LLM API

    Args:
        prompt: 提示词
        model: 模型名称（默认使用 PRIMARY_MODEL）
        temperature: 采样温度
        system_message: 可选的system消息

    Returns:
        (响应内容, 输入token数, 输出token数)

    Raises:
        RuntimeError: API 调用失败
    """
    validate_api_key()

    if model is None:
        model = PRIMARY_MODEL

    headers = {
        "Authorization": f"Bearer {SILICONFLOW_API_KEY}",
        "Content-Type": "application/json"
    }

    # 构建messages数组
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "enable_thinking": False
    }

    try:
        import requests
        import json

        # 📋 打印请求参数（完整不省略）
        print("\n" + "=" * 80, file=sys.stderr)
        print("📤 API 请求参数", file=sys.stderr)
        print("=" * 80, file=sys.stderr)
        print(f"🔗 端点: {API_ENDPOINT}", file=sys.stderr)
        print(f"🤖 模型: {model}", file=sys.stderr)
        print(f"🌡️  温度: {temperature}", file=sys.stderr)
        print(f"🔑 认证: Bearer {SILICONFLOW_API_KEY}", file=sys.stderr)
        print(f"⏱️  超时: 连接=10秒, 读取=300秒", file=sys.stderr)

        # 打印消息内容（完整不截断）
        print(f"\n💬 消息数量: {len(messages)}", file=sys.stderr)
        for i, msg in enumerate(messages, 1):
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            print(f"\n{'=' * 80}", file=sys.stderr)
            print(f"  消息 {i} [{role}]:", file=sys.stderr)
            print(f"{'=' * 80}", file=sys.stderr)
            print(f"{content}", file=sys.stderr)
            print(f"{'=' * 80}", file=sys.stderr)

        # 打印完整的 payload（格式化的 JSON，完整内容）
        print(f"\n📦 完整请求体（JSON）:", file=sys.stderr)
        print(f"{'=' * 80}", file=sys.stderr)
        print("```json", file=sys.stderr)
        print(json.dumps(payload, indent=2, ensure_ascii=False), file=sys.stderr)
        print("```", file=sys.stderr)
        print(f"{'=' * 80}\n", file=sys.stderr)

        response = requests.post(
            API_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=(10, 300)  # 连接超时 10 秒，读取超时 300 秒
        )
        response.raise_for_status()

        # 📋 打印响应信息（完整不省略）
        print("\n" + "=" * 80, file=sys.stderr)
        print("📥 API 响应信息", file=sys.stderr)
        print("=" * 80, file=sys.stderr)
        print(f"✅ 状态码: {response.status_code}", file=sys.stderr)

        # 打印响应头信息
        trace_id = response.headers.get('x-siliconcloud-trace-id')
        if trace_id:
            print(f"🔍 追踪ID: {trace_id}", file=sys.stderr)

        # 检查余额警告（如果有）
        balance_warning = response.headers.get('X-Balance-Warning')
        if balance_warning:
            print(f"💰 余额警告: {balance_warning}", file=sys.stderr)

        data = response.json()

        # 打印响应基本信息
        request_id = data.get("id", "N/A")
        response_model = data.get("model", "N/A")
        print(f"🆔 请求ID: {request_id}", file=sys.stderr)
        print(f"🤖 实际模型: {response_model}", file=sys.stderr)

        # 打印 token 使用情况
        usage = data.get("usage", {})
        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)
        total_tokens = usage.get("total_tokens", 0)

        print(f"\n📊 Token 使用情况:", file=sys.stderr)
        print(f"  输入 tokens: {input_tokens}", file=sys.stderr)
        print(f"  输出 tokens: {output_tokens}", file=sys.stderr)
        print(f"  总计 tokens: {total_tokens}", file=sys.stderr)

        # 打印结束原因
        finish_reason = data.get("choices", [{}])[0].get("finish_reason", "N/A")
        print(f"🏁 结束原因: {finish_reason}", file=sys.stderr)

        # 打印完整响应内容（不截断）
        content = data["choices"][0]["message"]["content"].strip()
        print(f"\n📝 完整响应内容:", file=sys.stderr)
        print(f"{'=' * 80}", file=sys.stderr)
        print(f"{content}", file=sys.stderr)
        print(f"{'=' * 80}", file=sys.stderr)
        print(f"📊 内容长度: {len(content)} 字符", file=sys.stderr)

        # 打印完整的响应 JSON（原始数据）
        print(f"\n📦 完整响应 JSON:", file=sys.stderr)
        print(f"{'=' * 80}", file=sys.stderr)
        print("```json", file=sys.stderr)
        print(json.dumps(data, indent=2, ensure_ascii=False), file=sys.stderr)
        print("```", file=sys.stderr)
        print(f"{'=' * 80}\n", file=sys.stderr)

        return content, input_tokens, output_tokens

    except ImportError:
        raise RuntimeError("缺少 requests 库，请安装：pip install requests")

    except requests.exceptions.HTTPError as e:
        # 详细的 HTTP 错误处理
        status_code = e.response.status_code
        error_detail = e.response.text if hasattr(e.response, 'text') else str(e)

        if status_code == 401:
            raise RuntimeError(
                f"{ERROR_SOLUTIONS['401']['emoji']} API Key 错误或未设置。\n"
                f"请检查环境变量 SILICONFLOW_API_KEY 是否正确。\n"
                f"设置方法：export SILICONFLOW_API_KEY=your_key"
            )
        elif status_code == 402:
            raise RuntimeError(
                f"{ERROR_SOLUTIONS['402']['emoji']} API 余额不足。\n"
                f"服务器返回：{error_detail}\n"
                f"{ERROR_SOLUTIONS['402']['solution']}"
            )
        elif status_code == 403:
            raise RuntimeError(
                f"{ERROR_SOLUTIONS['403']['emoji']} API 权限问题。\n"
                f"服务器返回：{error_detail}\n"
                f"{ERROR_SOLUTIONS['403']['solution']}"
            )
        elif status_code == 429:
            retry_after = e.response.headers.get('Retry-After', '60')
            raise RuntimeError(
                f"{ERROR_SOLUTIONS['429']['emoji']} 请求过于频繁，请在 {retry_after} 秒后重试"
            )
        elif status_code >= 500:
            raise RuntimeError(
                f"⚠️  SiliconFlow 服务器错误（{status_code}）\n"
                f"请稍后重试或查看服务状态"
            )
        else:
            raise RuntimeError(
                f"❌ API 调用失败（HTTP {status_code}）\n"
                f"详情：{error_detail}"
            )

    except requests.exceptions.Timeout as e:
        raise RuntimeError(
            f"{ERROR_SOLUTIONS['timeout']['emoji']} API 请求超时。\n"
            f"{ERROR_SOLUTIONS['timeout']['solution']}"
        )

    except requests.exceptions.ConnectionError as e:
        raise RuntimeError(
            f"{ERROR_SOLUTIONS['connection']['emoji']} 无法连接到 SiliconFlow API。\n"
            f"{ERROR_SOLUTIONS['connection']['solution']}"
        )

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"API 调用失败: {str(e)}")

    except (KeyError, IndexError) as e:
        raise RuntimeError(f"API 响应格式错误: {str(e)}")


def call_llm_with_fallback(
    prompt: str,
    temperature: float = 0.2
) -> Tuple[str, int, int]:
    """
    调用 LLM，主模型失败时自动切换备用模型

    Args:
        prompt: 提示词
        temperature: 采样温度

    Returns:
        (响应内容, 输入token数, 输出token数)
    """
    try:
        return call_siliconflow_api(prompt, PRIMARY_MODEL, temperature)
    except RuntimeError as e:
        print(f"⚠️  主模型失败: {e}，尝试备用模型...", file=sys.stderr)
        try:
            return call_siliconflow_api(prompt, FALLBACK_MODEL, temperature)
        except RuntimeError as e2:
            raise RuntimeError(f"主模型和备用模型均失败: {str(e2)}")


# =====================
# SRT 解析和重建
# =====================

def parse_srt(content: str) -> List[Dict]:
    """
    解析 SRT 内容为结构化数据

    Args:
        content: SRT 文件内容

    Returns:
        字幕块列表，每个块包含 index, time, text
    """
    # 按空行分割字幕块
    blocks = re.split(r'\n\s*\n', content.strip())
    parsed = []

    for block in blocks:
        lines = block.split('\n')
        if len(lines) >= 3:
            # 提取序号、时间轴、文本
            parsed.append({
                "index": lines[0],
                "time": lines[1],
                "text": "\n".join(lines[2:]).strip()
            })

    return parsed


def rebuild_srt(parsed: List[Dict]) -> str:
    """
    从结构化数据重建 SRT 内容

    Args:
        parsed: 解析后的字幕数据

    Returns:
        SRT 格式字符串
    """
    result = []
    for block in parsed:
        result.append(
            f"{block['index']}\n{block['time']}\n{block['text']}"
        )
    return "\n\n".join(result)


# =====================
# 字幕优化器类
# =====================

class SubtitleRefiner:
    """字幕优化器"""

    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def detect_topic(self, texts: List[str]) -> str:
        """
        检测视频主题

        Args:
            texts: 字幕文本列表

        Returns:
            主题描述
        """
        # 使用前 20 条字幕进行主题分析
        combined = "\n".join(texts[:20])

        prompt = f"""请分析以下字幕内容的主题。

请用一句话总结这个视频的主要内容是什么。

字幕内容：
{combined}

只返回主题描述，不要解释。"""

        try:
            topic, input_tokens, output_tokens = call_llm_with_fallback(
                prompt,
                temperature=0
            )
            self.total_input_tokens += input_tokens
            self.total_output_tokens += output_tokens
            return topic
        except RuntimeError as e:
            print(f"⚠️  主题检测失败: {e}，使用默认主题", file=sys.stderr)
            return "通用视频内容"

    def refine_subtitle_line(
        self,
        text: str,
        topic: str
    ) -> Tuple[str, bool]:
        """
        优化单条字幕

        Args:
            text: 原始字幕文本
            topic: 视频主题

        Returns:
            (优化后的文本, 是否被修改)
        """
        prompt = f"""你是专业字幕校对编辑。

视频主题：{topic}

任务：只修正以下问题，不要做其他改动：

1. 删除口语语气词（嗯、啊、那个、就是、然后、呃等）
2. 修正语音识别错误（如：XGBT→ChatGPT，RG→RAG，菜GPT→ChatGPT等）
3. 保持原句意思完全不变
4. 不扩写、不缩写
5. 不改变语气


只返回优化后的字幕，不要解释。

原字幕：{text}"""

        try:
            refined, input_tokens, output_tokens = call_llm_with_fallback(
                prompt,
                temperature=0.2
            )
            self.total_input_tokens += input_tokens
            self.total_output_tokens += output_tokens

            refined = refined.strip()
            was_modified = (refined != text)

            return refined, was_modified

        except RuntimeError as e:
            print(f"⚠️  优化失败（行: {text[:30]}...）: {e}，保留原文", file=sys.stderr)
            return text, False

    def refine_batch(
        self,
        parsed: List[Dict],
        topic: str,
        batch_size: int = 100
    ) -> Tuple[List[Dict], List[Dict]]:
        """
        并发批量优化字幕（优化版：支持多chunk处理）

        每10条字幕为一个chunk，每2个chunks（20条字幕）为一个API请求

        Args:
            parsed: 解析后的字幕数据
            topic: 视频主题
            batch_size: 每批处理多少行（默认 100，此参数保留兼容性）

        Returns:
            (优化后的数据, 修改列表)
        """
        total = len(parsed)

        # 小批量优化：少于 30 行直接逐行处理
        if total <= 30:
            print(f"🔄 字幕数量较少（{total} 行），使用逐条优化", file=sys.stderr)
            return self._refine_line_by_line_full(parsed, topic)

        # 将字幕按10条分块
        chunk_size = 10  # 每个chunk包含10条字幕
        chunks = []
        for i in range(0, total, chunk_size):
            chunks.append(parsed[i:i + chunk_size])

        # 将2个chunks合并为一个请求
        chunks_per_request = 2  # 每个API请求处理2个chunks
        requests = []
        for i in range(0, len(chunks), chunks_per_request):
            requests.append(chunks[i:i + chunks_per_request])

        total_requests = len(requests)
        print(f"🎯 优化 {total} 条字幕（共 {total_requests} 个API请求，每请求20条）", file=sys.stderr)

        # 改为顺序执行，避免并发导致API限流
        changes = []
        completed = 0

        for req_idx, request_chunks in enumerate(requests):
            try:
                req_changes = self._process_chunk_with_rate_limit(
                    request_chunks,
                    topic,
                    req_idx + 1,
                    total_requests
                )
                changes.extend(req_changes)
                completed += 1
                print(f"  ✓ 请求 {completed}/{total_requests} 完成", file=sys.stderr)
            except Exception as e:
                print(f"  ⚠️  请求 {req_idx + 1} 失败: {e}", file=sys.stderr)

        return parsed, changes

    def _process_batch(
        self,
        batch: List[Dict],
        topic: str
    ) -> List[Dict]:
        """
        处理一批字幕

        Args:
            batch: 一批字幕数据
            topic: 视频主题

        Returns:
            这批的修改列表
        """
        import json

        # 构建 JSON 数组
        subtitles_json = json.dumps([
            {"index": block["index"], "text": block["text"]}
            for block in batch
        ], ensure_ascii=False)

        prompt = f"""你是专业字幕校对编辑。

视频主题：{topic}

任务：只修正以下问题，不要做其他改动：
1. 删除口语语气词（嗯、啊、那个、就是、然后、呃等）
2. 修正语音识别错误（如：XGBT→ChatGPT，RG→RAG，菜GPT→ChatGPT等）
3. 保持原句意思完全不变
4. 不扩写、不缩写
5. 不改变语气

字幕列表（JSON 格式）：
{subtitles_json}

请严格按照以下格式返回优化结果（每行一个 JSON 对象）：
{{"index": "序号", "text": "优化后的文本"}}
{{"index": "序号", "text": "优化后的文本"}}
...

重要要求：
1. 必须返回 JSON 对象列表（每行一个）
2. 不要使用 markdown 代码块（如 ```json）
3. 不要添加任何解释说明
4. 确保 index 值完全一致
5. 确保返回数量与输入数量一致（{len(batch)} 个）"""

        try:
            refined_text, input_tokens, output_tokens = call_llm_with_fallback(
                prompt,
                temperature=0.2
            )
            self.total_input_tokens += input_tokens
            self.total_output_tokens += output_tokens

            # 检查空响应
            if not refined_text or not refined_text.strip():
                raise ValueError("LLM 返回了空响应")

            refined_text = refined_text.strip()

            # 尝试提取 JSON（如果被 markdown 包裹）
            if refined_text.startswith("```"):
                import re
                match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', refined_text, re.DOTALL)
                if match:
                    refined_text = match.group(1).strip()
                    print(f"  ✓ 从 Markdown 代码块中提取 JSON", file=sys.stderr)
                else:
                    # 如果无法提取，尝试直接使用
                    refined_text = refined_text.replace('```', '').replace('json', '').strip()
                    print(f"  ⚠️  移除 Markdown 标记", file=sys.stderr)

            # 解析 JSON 结果
            refined_array = json.loads(refined_text)

            # 验证数量一致
            if len(refined_array) != len(batch):
                raise ValueError(f"返回数量不匹配：期望 {len(batch)}，得到 {len(refined_array)}")

            # 更新字幕并记录修改
            changes = []
            refined_map = {item["index"]: item["text"] for item in refined_array}

            for block in batch:
                original = block["text"]
                refined = refined_map.get(block["index"], original)
                block["text"] = refined

                if refined != original:
                    changes.append({
                        "index": block["index"],
                        "time": block["time"],
                        "original": original,
                        "refined": refined
                    })

            return changes

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"⚠️  批量处理失败: {e}", file=sys.stderr)
            print(f"⚠️  原始响应（前 200 字）: {refined_text[:200] if 'refined_text' in locals() else 'N/A'}...", file=sys.stderr)
            print(f"  ↘️  回退到逐行处理", file=sys.stderr)
            # 回退到逐行处理这一批
            return self._process_batch_line_by_line(batch, topic)

    def _process_multi_chunk_batch(
        self,
        chunks: List[List[Dict]],
        topic: str
    ) -> List[Dict]:
        """
        处理多个chunk批次（一个API请求处理多个chunk）

        每个chunk包含10条字幕，每个API请求处理2个chunks（共20条字幕）

        Args:
            chunks: chunk列表，每个chunk是10条字幕
            topic: 视频主题

        Returns:
            所有chunk的修改列表
        """
        import json

        # 构建多chunk prompt
        chunk_contents = []
        for chunk_idx, chunk in enumerate(chunks):
            chunk_text = f"DATA{chunk_idx}:\n"
            for idx, block in enumerate(chunk):
                # 只发送文本，不包含序号（序号会导致LLM在返回时重复序号）
                chunk_text += f'{block["text"]}\n'
            chunk_contents.append(chunk_text)

        prompt_content = "\n".join(chunk_contents)

        # 使用system消息定义角色
        system_msg = "你是字幕校对助手。只允许修正语音识别错误，不允许润色。"

        prompt = f"""主题：{topic}

分别校对以下字幕块，返回JSON。

{prompt_content}

返回格式要求：
1. 返回JSON对象（不是数组）
2. 每个DATA块对应一个数组
3. 格式示例：{{"DATA0": ["文本1", "文本2", ...], "DATA1": ["文本3", "文本4", ...]}}
4. 确保每个数组的元素数量与输入一致（每个DATA块10个文本）
5. 不要使用markdown代码块
6. 不要添加任何解释说明"""

        try:
            refined_text, input_tokens, output_tokens = call_siliconflow_api(
                prompt,
                PRIMARY_MODEL,
                0.2,
                system_message=system_msg
            )
            self.total_input_tokens += input_tokens
            self.total_output_tokens += output_tokens

            # 解析响应
            refined_text = refined_text.strip()

            # 移除markdown包裹
            if refined_text.startswith("```"):
                import re
                match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', refined_text, re.DOTALL)
                if match:
                    refined_text = match.group(1).strip()

            # 解析JSON对象
            refined_data = json.loads(refined_text)

            # 验证所有chunk都存在
            expected_keys = [f"DATA{i}" for i in range(len(chunks))]
            for key in expected_keys:
                if key not in refined_data:
                    raise ValueError(f"响应中缺少 {key}")

            # 处理每个chunk的结果
            changes = []
            for chunk_idx, chunk in enumerate(chunks):
                key = f"DATA{chunk_idx}"
                refined_texts = refined_data[key]

                if len(refined_texts) != len(chunk):
                    raise ValueError(
                        f"DATA{chunk_idx} 数量不匹配：期望 {len(chunk)}，得到 {len(refined_texts)}"
                    )

                # 更新字幕并记录修改
                for block_idx, block in enumerate(chunk):
                    original = block["text"]
                    refined = refined_texts[block_idx]
                    block["text"] = refined

                    if refined != original:
                        changes.append({
                            "index": block["index"],
                            "time": block["time"],
                            "original": original,
                            "refined": refined
                        })

            return changes

        except (json.JSONDecodeError, KeyError, ValueError, RuntimeError) as e:
            print(f"⚠️  多chunk处理失败: {e}", file=sys.stderr)
            print(f"⚠️  原始响应（前 200 字）: {refined_text[:200] if 'refined_text' in locals() else 'N/A'}...", file=sys.stderr)
            print(f"  ↘️  回退到逐条处理", file=sys.stderr)
            # 回退到逐条处理
            return self._process_lines_individually(chunks, topic)

    def _process_lines_individually(
        self,
        chunks: List[List[Dict]],
        topic: str
    ) -> List[Dict]:
        """
        逐条处理字幕（回退方案）

        Args:
            chunks: chunk列表
            topic: 视频主题

        Returns:
            所有chunk的修改列表
        """
        all_changes = []
        total_lines = sum(len(chunk) for chunk in chunks)
        processed = 0

        for chunk in chunks:
            for block in chunk:
                processed += 1
                print(f"  🔄 逐条处理 {processed}/{total_lines}...", file=sys.stderr, end='\r')

                original = block["text"]
                refined, was_modified = self.refine_subtitle_line(original, topic)
                block["text"] = refined

                if was_modified:
                    all_changes.append({
                        "index": block["index"],
                        "time": block["time"],
                        "original": original,
                        "refined": refined
                    })

        print()  # 换行
        return all_changes

    def _process_chunk_with_rate_limit(
        self,
        chunk: List[List[Dict]],
        topic: str,
        chunk_idx: int,
        total_chunks: int
    ) -> List[Dict]:
        """
        处理单个chunk（包含2个子chunks，共20条字幕）并应用速率限制

        Args:
            chunk: 包含2个子chunks的列表，每个子chunk有10条字幕
            topic: 视频主题
            chunk_idx: chunk索引
            total_chunks: 总chunk数

        Returns:
            这个chunk的修改列表
        """
        subtitles_count = sum(len(subchunk) for subchunk in chunk)
        print(f"  🔄 请求 {chunk_idx}/{total_chunks} 开始（包含 {subtitles_count} 条字幕）...", file=sys.stderr)

        # 应用速率限制
        API_RATE_LIMITER.acquire()

        # 调用多chunk处理逻辑
        return self._process_multi_chunk_batch(chunk, topic)

    def _process_batch_line_by_line(
        self,
        batch: List[Dict],
        topic: str
    ) -> List[Dict]:
        """逐行处理一批字幕（回退方案）"""
        changes = []

        for idx, block in enumerate(batch, 1):
            print(f"  🔄 逐行处理 {idx}/{len(batch)}...", file=sys.stderr, end='\r')

            original = block["text"]
            refined, was_modified = self.refine_subtitle_line(original, topic)

            block["text"] = refined

            if was_modified:
                changes.append({
                    "index": block["index"],
                    "time": block["time"],
                    "original": original,
                    "refined": refined
                })

        print()  # 换行
        return changes

    def _process_single_batch_with_rate_limit(
        self,
        batch: List[Dict],
        topic: str,
        batch_idx: int,
        total_batches: int
    ) -> List[Dict]:
        """
        处理单批字幕（带速率限制）

        Args:
            batch: 一批字幕数据
            topic: 视频主题
            batch_idx: 批次索引
            total_batches: 总批次数

        Returns:
            这批的修改列表
        """
        print(f"  🔄 批次 {batch_idx}/{total_batches} 开始...", file=sys.stderr)

        # 应用速率限制
        API_RATE_LIMITER.acquire()

        # 调用原有的批量处理逻辑
        return self._process_batch(batch, topic)

    def _refine_line_by_line_full(
        self,
        parsed: List[Dict],
        topic: str
    ) -> Tuple[List[Dict], List[Dict]]:
        """
        完整的逐行优化（用于小批量）

        Args:
            parsed: 解析后的字幕数据
            topic: 视频主题

        Returns:
            (优化后的数据, 修改列表)
        """
        changes = []
        total = len(parsed)

        for idx, block in enumerate(parsed, 1):
            print(f"🔄 正在处理 {idx}/{total}...", file=sys.stderr, end='\r')
            original = block["text"]
            refined, was_modified = self.refine_subtitle_line(original, topic)
            block["text"] = refined
            if was_modified:
                changes.append({
                    "index": block["index"],
                    "time": block["time"],
                    "original": original,
                    "refined": refined
                })
        print()
        return parsed, changes

    def refine(
        self,
        parsed: List[Dict]
    ) -> Tuple[List[Dict], str, List[Dict]]:
        """
        优化所有字幕

        Args:
            parsed: 解析后的字幕数据

        Returns:
            (优化后的数据, 主题, 修改列表)
        """
        texts = [b["text"] for b in parsed]

        # 步骤 1: 检测主题
        print("🔍 正在分析视频主题...", file=sys.stderr)
        topic = self.detect_topic(texts)
        print(f"✓ 检测到主题: {topic}", file=sys.stderr)

        # 步骤 2: 批量优化字幕（固定每 100 行一批）
        total = len(parsed)
        print(f"🎯 正在批量优化 {total} 条字幕（每批 100 行）...", file=sys.stderr)

        parsed, changes = self.refine_batch(parsed, topic, batch_size=100)

        print(f"\n✓ 已处理 {total} 条字幕", file=sys.stderr)
        print(f"✓ 修改了 {len(changes)} 处", file=sys.stderr)

        return parsed, topic, changes

    def generate_summary(self, changes: List[Dict]) -> str:
        """
        生成优化总结

        Args:
            changes: 修改列表

        Returns:
            格式化的总结字符串
        """
        total_input = self.total_input_tokens
        total_output = self.total_output_tokens
        change_count = len(changes)

        summary = f"""📊 字幕优化完成

本次消耗token：输入{total_input} 输出{total_output}，共修改了{change_count}处，以下为前3处："""

        for change in changes[:3]:
            summary += f"""

[{change['index']}]
原：{change['original']}
新：{change['refined']}"""

        return summary


# =====================
# Feishu 集成
# =====================

def send_file_via_openclaw(file_path: str, chat_id: str) -> bool:
    """
    通过 OpenClaw 发送文件到 Feishu

    Args:
        file_path: 文件路径
        chat_id: Feishu chat ID

    Returns:
        是否成功
    """
    cmd = [
        "openclaw", "message", "send",
        "--channel", "feishu",
        "--target", chat_id,
        "--media", file_path
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✓ 文件已发送: {file_path}", file=sys.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  发送文件失败: {e.stderr}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print(f"⚠️  未找到 openclaw 命令", file=sys.stderr)
        return False


def send_message_via_openclaw(message: str, chat_id: str) -> bool:
    """
    通过 OpenClaw 发送消息到 Feishu

    Args:
        message: 消息内容
        chat_id: Feishu chat ID

    Returns:
        是否成功
    """
    cmd = [
        "openclaw", "message", "send",
        "--channel", "feishu",
        "--target", chat_id,
        "--message", message
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✓ 消息已发送", file=sys.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  发送消息失败: {e.stderr}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print(f"⚠️  未找到 openclaw 命令", file=sys.stderr)
        return False


# =====================
# 主入口函数
# =====================

def refine_and_send(
    srt_file_path: str,
    chat_id: str,
    workspace_dir: str
) -> Dict:
    """
    优化字幕并发送结果（供 Agent 调用的主入口）

    Args:
        srt_file_path: SRT 文件路径
        chat_id: Feishu chat ID
        workspace_dir: OpenClaw workspace 目录

    Returns:
        包含处理结果的字典：
        {
            "success": bool,
            "output_file": str,
            "topic": str,
            "changes_count": int,
            "input_tokens": int,
            "output_tokens": int,
            "error": str (如果失败)
        }
    """
    result = {
        "success": False,
        "error": None
    }

    try:
        # =====================
        # 预检查环境
        # =====================
        print("🔍 正在检查环境...", file=sys.stderr)

        # 1. 检查网络连接
        if not check_network_connection():
            error_msg = (
                f"{ERROR_SOLUTIONS['connection']['emoji']} "
                f"无法连接到 SiliconFlow，{ERROR_SOLUTIONS['connection']['solution']}"
            )
            result["error"] = error_msg
            print(f"❌ {error_msg}", file=sys.stderr)
            return result

        # 2. 验证 API Key
        key_valid, key_msg = check_api_key_validity()
        if not key_valid:
            error_msg = (
                f"❌ API Key 检查失败：{key_msg}\n"
                f"请设置：export SILICONFLOW_API_KEY=your_key"
            )
            result["error"] = error_msg
            print(f"❌ {error_msg}", file=sys.stderr)
            return result

        print("✓ 环境检查通过", file=sys.stderr)

        # 验证输入文件
        if not os.path.exists(srt_file_path):
            raise FileNotFoundError(f"文件不存在: {srt_file_path}")

        print(f"📖 正在读取 SRT 文件: {srt_file_path}", file=sys.stderr)

        # 读取 SRT 内容
        with open(srt_file_path, "r", encoding="utf-8-sig") as f:
            content = f.read()

        # 处理字幕
        refiner = SubtitleRefiner()

        print("🔧 正在解析 SRT...", file=sys.stderr)
        parsed = parse_srt(content)

        if not parsed:
            raise ValueError("无法解析 SRT 文件或文件为空")

        print("🎯 正在优化字幕...", file=sys.stderr)
        parsed, topic, changes = refiner.refine(parsed)

        print("💾 正在保存优化后的文件...", file=sys.stderr)
        new_srt = rebuild_srt(parsed)

        # 生成输出文件名
        base_name = os.path.basename(srt_file_path).replace(".srt", "")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"{base_name}_优化_{timestamp}.srt"

        # 创建输出目录
        output_dir = os.path.join(workspace_dir, "subtitle_refine")
        os.makedirs(output_dir, exist_ok=True)

        # 写入优化后的文件
        output_path = os.path.join(output_dir, filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(new_srt)

        print(f"✓ 已保存到: {output_path}", file=sys.stderr)

        # 生成并发送总结
        summary = refiner.generate_summary(changes)

        print("📤 正在通过 Feishu 发送...", file=sys.stderr)
        send_file_via_openclaw(output_path, chat_id)
        # send_message_via_openclaw(summary, chat_id)

        # 返回结果
        result.update({
            "success": True,
            "output_file": output_path,
            "topic": topic,
            "changes_count": len(changes),
            "input_tokens": refiner.total_input_tokens,
            "output_tokens": refiner.total_output_tokens
        })

        print("✅ 完成！", file=sys.stderr)

    except Exception as e:
        error_msg = f"处理失败: {str(e)}"
        print(f"❌ {error_msg}", file=sys.stderr)
        result["error"] = error_msg

    return result


# =====================
# 测试入口（可选）
# =====================

if __name__ == "__main__":
    # 命令行入口：直接运行此脚本
    if len(sys.argv) < 4:
        print("用法: python3 refine.py <srt_file> <chat_id> <workspace_dir>", file=sys.stderr)
        print("示例: python3 refine.py demo.srt oc_xxx /workspace", file=sys.stderr)
        sys.exit(1)

    srt_file = sys.argv[1]
    chat_id = sys.argv[2]
    workspace = sys.argv[3]

    result = refine_and_send(srt_file, chat_id, workspace)

    if result["success"]:
        print(f"\n✓ 优化成功！", file=sys.stderr)
        print(f"  主题: {result['topic']}", file=sys.stderr)
        print(f"  修改: {result['changes_count']} 处", file=sys.stderr)
        print(f"  Token: 输入 {result['input_tokens']}, 输出 {result['output_tokens']}", file=sys.stderr)
    else:
        print(f"\n✗ 失败: {result['error']}", file=sys.stderr)
        sys.exit(1)
