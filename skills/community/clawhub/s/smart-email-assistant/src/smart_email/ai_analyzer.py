"""
AI 模块 - 紧急邮件判断和内容总结
支持 OpenAI 兼容 API（支持任意模型提供商）
"""
import os
import re
import json
import base64
import time
import threading
from typing import Dict, Tuple, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI, APIError, APIConnectionError, RateLimitError


class AIAnalyzer:
    """AI 分析器 - 支持任意 OpenAI 兼容 API"""

    def __init__(self, api_key: str, base_url: str, model: str,
                 max_concurrent: int = 5,
                 multimodal_analysis: bool = False,
                 retry_count: int = 3, retry_base_delay: float = 1.0):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.max_concurrent = max_concurrent
        self.multimodal_analysis = multimodal_analysis
        self.retry_count = retry_count
        self.retry_base_delay = retry_base_delay

        # 验证配置
        if not api_key:
            raise ValueError(
                "❌ 未配置 API Key\n"
                "请在 ~/.openclaw/.env 中添加以下配置:\n"
                "  SMART_EMAIL_OPENAI_API_KEY=your_api_key"
            )

        if not base_url:
            raise ValueError(
                "❌ 未配置 API URL\n"
                "请在 ~/.openclaw/.env 中添加以下配置:\n"
                "  SMART_EMAIL_OPENAI_API_URL=https://api.example.com/v1"
            )

        if not model:
            raise ValueError(
                "❌ 未配置模型名称\n"
                "请在 ~/.openclaw/.env 中添加以下配置:\n"
                "  SMART_EMAIL_OPENAI_MODEL=your_model_name"
            )

        self.client = OpenAI(api_key=api_key, base_url=base_url)

        # 用于并发控制的信号量
        self._semaphore = threading.Semaphore(max_concurrent)
        self._lock = threading.Lock()
        self._active_requests = 0

    def _encode_image_to_base64(self, image_path: str) -> Optional[str]:
        """
        将图片文件编码为 base64

        Args:
            image_path: 图片文件路径

        Returns:
            base64 编码的字符串，失败返回 None
        """
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
                return base64.b64encode(image_data).decode('utf-8')
        except Exception as e:
            print(f"  [AI] 图片编码失败 {image_path}: {e}")
            return None

    def _build_multimodal_messages(self, prompt: str, image_paths: List[str]) -> List[Dict]:
        """
        构建多模态消息（文本 + 图片）

        Args:
            prompt: 文本提示
            image_paths: 图片路径列表

        Returns:
            OpenAI 格式的消息列表
        """
        content = [{"type": "text", "text": prompt}]

        for img_path in image_paths:
            base64_image = self._encode_image_to_base64(img_path)
            if base64_image:
                # 检测图片类型
                ext = os.path.splitext(img_path)[1].lower()
                mime_type = {
                    '.png': 'image/png',
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.gif': 'image/gif',
                    '.webp': 'image/webp'
                }.get(ext, 'image/jpeg')

                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{base64_image}"
                    }
                })

        return [
            {"role": "system", "content": "你是一个邮件助手，帮助分析邮件内容和图片。"},
            {"role": "user", "content": content}
        ]

    def _call_api_with_retry(self, messages: list, max_tokens: int = 1024) -> str:
        """
        带重试机制的 API 调用

        重试策略:
        - 重试次数: 默认 3 次
        - 重试间隔: 指数退避 (1s, 2s, 4s, ...)
        - 触发条件: 网络错误、超时、5xx 错误
        """
        last_error = None

        for attempt in range(self.retry_count):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=1,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content.strip()

            except (APIConnectionError, RateLimitError) as e:
                # 网络错误和限流错误需要重试
                last_error = e
                if attempt < self.retry_count - 1:
                    delay = self.retry_base_delay * (2 ** attempt)  # 指数退避
                    print(f"  [AI] API 调用失败 (尝试 {attempt + 1}/{self.retry_count}): {e}")
                    print(f"  [AI] 等待 {delay}s 后重试...")
                    time.sleep(delay)
                else:
                    print(f"  [AI] API 调用最终失败: {e}")
                    raise

            except APIError as e:
                # API 错误，检查状态码
                last_error = e
                status_code = getattr(e, 'status_code', None)

                # 5xx 错误需要重试
                if status_code and 500 <= status_code < 600:
                    if attempt < self.retry_count - 1:
                        delay = self.retry_base_delay * (2 ** attempt)
                        print(f"  [AI] API 服务器错误 {status_code} (尝试 {attempt + 1}/{self.retry_count})")
                        print(f"  [AI] 等待 {delay}s 后重试...")
                        time.sleep(delay)
                    else:
                        print(f"  [AI] API 服务器错误最终失败: {e}")
                        raise
                else:
                    # 4xx 错误不重试
                    print(f"  [AI] API 客户端错误: {e}")
                    raise

            except Exception as e:
                # 其他异常不重试
                print(f"  [AI] 未知错误: {e}")
                raise

        # 所有重试都失败了
        raise last_error if last_error else Exception("API 调用失败")

    def _call_api_with_limit(self, messages: list, max_tokens: int = 1024) -> str:
        """
        带并发限制和重试机制的 API 调用
        """
        with self._semaphore:
            with self._lock:
                self._active_requests += 1
                print(f"  [AI] 并发请求: {self._active_requests}/{self.max_concurrent}")

            try:
                return self._call_api_with_retry(messages, max_tokens)
            finally:
                with self._lock:
                    self._active_requests -= 1

    # === v1 方法已废弃 (2026-03-30) ===
    # check_urgent() 和 summarize_email() 已删除
    # 所有分析统一使用 analyze_email() v2 方法（单次 JSON 调用）
    # 如需紧急判断，请使用 analyze_email() 返回的 is_urgent 字段

    def analyze_emails_batch(self, emails: List[Dict],
                            callback=None) -> List[Dict]:
        """
        批量分析邮件（带并发控制）

        Args:
            emails: 邮件列表
            callback: 每处理完一封邮件的回调函数，参数为 (email_data, is_urgent, reason, summary)

        Returns:
            分析后的邮件列表（添加了 is_urgent, reason, summary 字段）
        """
        results = []

        print(f"\n🤖 批量分析 {len(emails)} 封邮件 (并发限制: {self.max_concurrent})...")

        with ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
            # 提交所有任务
            future_to_email = {}
            for email in emails:
                future = executor.submit(self._analyze_single_email, email)
                future_to_email[future] = email

            # 处理结果
            for i, future in enumerate(as_completed(future_to_email), 1):
                email = future_to_email[future]
                try:
                    is_urgent, reason, summary = future.result()
                    email['is_urgent'] = is_urgent
                    email['reason'] = reason
                    email['summary'] = summary
                    results.append(email)

                    print(f"  [{i}/{len(emails)}] {email['subject'][:30]}... - 紧急: {'是' if is_urgent else '否'}")

                    if callback:
                        callback(email, is_urgent, reason, summary)

                except Exception as e:
                    print(f"  [{i}/{len(emails)}] 分析失败: {e}")
                    email['is_urgent'] = False
                    email['reason'] = f"分析出错: {str(e)}"
                    email['summary'] = "[分析失败]"
                    results.append(email)

        return results

    def _analyze_single_email(self, email_data: Dict) -> Tuple[bool, str, str]:
        """
        分析单封邮件（内部方法，用于并发执行）
        使用 v2 analyze_email 一次调用返回所有字段

        Returns:
            (是否紧急, 判断理由, 邮件摘要)
        """
        return self.analyze_email(email_data)

    def analyze_email(self, email_data: Dict) -> Tuple[bool, str, str]:
        """
        分析单封邮件，一次调用返回所有字段（v2 新方法）

        Returns:
            (是否紧急, 判断理由, 邮件摘要)
        """
        subject = email_data.get('subject', '')
        sender = email_data.get('sender', '')
        body = email_data.get('body_text', '')[:2000]  # 限制长度用于判断

        prompt = f"""请扮演专业的商务邮件分发助手，深度分析以下邮件的上下文意图，并严格输出 JSON 格式结果。

邮件信息：
发件人: {sender}
主题: {subject}
正文: {body}

评估紧急性（is_urgent）的核心判定逻辑（请防范营销"虚假紧急"及委婉语气的"隐性紧急"）：
1. 明确的时间边界（Temporal Anchors）：正文中是否包含即将到期的严格时间节点（如"今天下班前(EOD)"、"ASAP"、"会议前"、"24小时内"）。如果没有时间限制，仅有"请查看"、"请提交"等动作，不算紧急。
2. 业务阻碍与负面后果（Consequences）：如果不立即响应，是否会导致明确的负面业务后果（如项目停滞、客户投诉、系统故障、合规违约）。
3. 真实的人际请求（Intent Analysis）：必须排除营销推广（如"限时折扣"、"系统自动群发"）、Newsletter 订阅通讯和仅供参考（FYI）的常规汇报。真正的紧急邮件通常有清晰的针对性特定要求。
4. 委婉但紧急（Politeness Masking）：注意识别语气礼貌但带有明确死线或严重后果的邮件（如"如果方便的话，客户希望能在下午3点前得到答复"），这属于紧急。

输出格式：
{{
  "is_urgent": true/false,
  "reason": "一句话说明紧急原因或非紧急理由（不少于5个字）",
  "summary": "50字以内的邮件核心内容摘要"
}}

要求：
- is_urgent: 严格按照上述4点逻辑综合判定，二值输出 true 或 false。
- reason: 必须是一句话，不能为空，不能少于5个字。若为 true，需点明【具体DDL】或【业务阻碍】；若为 false，需点明其属于【常规汇报】、【营销邮件】或【无具体限期的普通动作】。
- summary: 严格控制在50字以内，提炼出动作核心（谁需要什么/通报了什么）。
- 务必只输出合法的纯 JSON 字符串，绝对不要输出哪怕一个字的额外解释文字，也不要包含 ```json 这样的 Markdown 标记。"""

        try:
            # 检查是否开启多模态分析，且邮件包含正文图片
            image_paths = []
            if self.multimodal_analysis:
                saved_attachments = email_data.get('saved_attachments', [])
                for att in saved_attachments:
                    if att.get('is_inline') and att.get('content_type', '').startswith('image/'):
                        image_paths.append(att['local_path'])

                if image_paths:
                    print(f"  [AI] 多模态分析: 包含 {len(image_paths)} 张正文图片")
                    messages = self._build_multimodal_messages(prompt, image_paths)
                else:
                    messages = [
                        {"role": "system", "content": "你是一个邮件助手，负责判断邮件紧急程度并生成摘要。"},
                        {"role": "user", "content": prompt}
                    ]
            else:
                messages = [
                    {"role": "system", "content": "你是一个邮件助手，负责判断邮件紧急程度并生成摘要。"},
                    {"role": "user", "content": prompt}
                ]

            result = self._call_api_with_limit(messages, max_tokens=1024)

            # 解析 JSON 结果（使用改进的嵌套 JSON 提取逻辑）
            parsed = self._extract_json_from_result(result)

            # 验证结果
            is_urgent = parsed.get('is_urgent', False)
            reason = parsed.get('reason', '')
            summary = parsed.get('summary', '')

            if not isinstance(is_urgent, bool):
                raise ValueError(f"is_urgent 类型错误: {type(is_urgent)}")
            if not reason or len(reason) < 5:
                raise ValueError(f"reason 为空或太短: {reason}")
            if not summary:
                raise ValueError(f"summary 为空")

            return is_urgent, reason, summary

        except Exception as e:
            print(f"  [AI] 分析失败: {e}")
            raise

    def _extract_json_from_result(self, result: str) -> dict:
        """
        从 LLM 返回结果中提取 JSON 对象（支持嵌套）

        Args:
            result: LLM 返回的原始字符串

        Returns:
            解析后的 JSON 字典

        Raises:
            ValueError: 无法解析 JSON 时抛出
        """
        # 移除可能的 markdown 代码块
        json_str = result.strip()
        if json_str.startswith('```'):
            json_str = re.sub(r'^```json?', '', json_str)
            json_str = re.sub(r'```$', '', json_str)
        json_str = json_str.strip()

        # 尝试直接解析
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass

        # 尝试提取 JSON 对象（支持嵌套）
        # 使用计数器来匹配嵌套的大括号
        json_match = None
        for i, char in enumerate(json_str):
            if char == '{':
                brace_count = 0
                for j in range(i, len(json_str)):
                    if json_str[j] == '{':
                        brace_count += 1
                    elif json_str[j] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            # 找到一个完整的 JSON 对象
                            try:
                                candidate = json_str[i:j+1]
                                parsed = json.loads(candidate)
                                # 检查是否包含必需的字段
                                if 'is_urgent' in parsed:
                                    return parsed
                                # 保存第一个有效的 JSON
                                if json_match is None:
                                    json_match = parsed
                            except json.JSONDecodeError:
                                pass
                            break

        if json_match is not None:
            return json_match

        # 最后的尝试：查找任何 JSON 对象模式
        json_pattern = re.search(r'\{.*\}', json_str, re.DOTALL)
        if json_pattern:
            try:
                return json.loads(json_pattern.group())
            except json.JSONDecodeError:
                pass

        raise ValueError(f"无法解析 LLM 返回: {result[:200]}")

    def classify_importance(self, emails: list) -> Tuple[list, list]:
        """
        批量分类邮件重要性

        Returns:
            (重要邮件列表, 一般邮件列表)
        """
        important = []
        normal = []

        for email in emails:
            # 使用 v2 analyze_email 一次性获取所有字段
            is_urgent, reason, summary = self.analyze_email(email)
            email['is_urgent'] = is_urgent
            email['reason'] = reason
            email['summary'] = summary

            if is_urgent:
                important.append(email)
            else:
                # 进一步判断是否为重要但非紧急
                subject = email.get('subject', '').lower()
                sender = email.get('sender', '').lower()

                # 简单启发式规则
                important_keywords = ['面试', 'offer', '合同', '发票', '付款', '会议', 'deadline', '截止']
                if any(kw in subject for kw in important_keywords):
                    important.append(email)
                else:
                    normal.append(email)

        return important, normal
