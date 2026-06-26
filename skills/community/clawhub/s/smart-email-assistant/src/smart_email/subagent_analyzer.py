"""
Subagent 分析器 - 使用 OpenClaw Subagent 进行邮件分析
实现与 AIAnalyzer 相同的接口
"""
import os
import json
import time
import threading
import fcntl
from typing import Dict, Tuple, List, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# 延迟导入，避免循环依赖
try:
    from openclaw import sessions_spawn
    HAS_OPENCLAW = True
except ImportError:
    HAS_OPENCLAW = False


class SubagentAnalyzer:
    """
    Subagent 分析器 - 使用 OpenClaw Subagent 进行邮件分析

    通信机制：
    - 主进程写入邮件数据到 /tmp/smart-email/emails/{email_id}.json
    - Subagent 读取后分析，结果写入 /tmp/smart-email/results/{email_id}.json
    - Subagent 打印 ANALYSIS_COMPLETE: {email_id}
    - 主进程读取结果后删除临时文件

    并发控制：分批次处理，每批数量由 SMART_EMAIL_SUBAGENT_CONCURRENCY 控制
    """

    def __init__(self,
                 max_concurrent: int = 3,
                 retry_count: int = 3,
                 retry_base_delay: float = 1.0,
                 timeout: int = None):
        """
        初始化 Subagent 分析器

        Args:
            max_concurrent: 每批并发数量（SMART_EMAIL_SUBAGENT_CONCURRENCY）
            retry_count: 重试次数
            retry_base_delay: 重试基础延迟（秒）
            timeout: 超时时间（秒），默认从 SMART_EMAIL_SUBAGENT_TIMEOUT 读取
        """
        self.max_concurrent = max_concurrent
        self.retry_count = retry_count
        self.retry_base_delay = retry_base_delay

        # 从环境变量读取超时时间，默认 120 秒
        if timeout is None:
            timeout_str = os.getenv("SMART_EMAIL_SUBAGENT_TIMEOUT", "120")
            try:
                self.timeout = int(timeout_str)
            except ValueError:
                self.timeout = 120
        else:
            self.timeout = timeout

        # 临时文件目录
        self._emails_dir = Path("/tmp/smart-email/emails")
        self._results_dir = Path("/tmp/smart-email/results")

        # 创建目录
        self._emails_dir.mkdir(parents=True, exist_ok=True)
        self._results_dir.mkdir(parents=True, exist_ok=True)

        # 用于并发控制的锁
        self._lock = threading.Lock()

    def _write_email_for_subagent(self, email_data: Dict, email_id: str) -> Path:
        """
        将邮件数据写入临时文件，供 subagent 读取
        使用文件锁保护并发访问
        """
        email_file = self._emails_dir / f"{email_id}.json"
        with open(email_file, 'w', encoding='utf-8') as f:
            # 获取独占锁（写入保护）
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                json.dump(email_data, f, ensure_ascii=False, indent=2)
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        return email_file

    def _wait_for_result(self, email_id: str, timeout: float = None) -> Optional[Dict]:
        """
        等待 subagent 完成分析，读取结果
        使用文件锁保护并发读取

        Args:
            email_id: 邮件ID
            timeout: 超时时间（秒），默认使用 self.timeout

        Returns:
            分析结果字典，超时返回 None
        """
        if timeout is None:
            timeout = self.timeout
        result_file = self._results_dir / f"{email_id}.json"
        start_time = time.time()

        while time.time() - start_time < timeout:
            if result_file.exists():
                try:
                    with open(result_file, 'r', encoding='utf-8') as f:
                        # 获取共享锁（读取保护）
                        fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                        try:
                            result = json.load(f)
                            return result
                        finally:
                            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                except Exception as e:
                    print(f"  [Subagent] 读取结果失败: {e}")
                    time.sleep(0.5)
            time.sleep(1)

        return None

    def _cleanup_files(self, email_id: str):
        """
        清理临时文件
        使用文件锁保护并发删除
        """
        email_file = self._emails_dir / f"{email_id}.json"
        result_file = self._results_dir / f"{email_id}.json"

        try:
            if email_file.exists():
                # 获取独占锁确保没有进程正在写入/读取
                with open(email_file, 'r', encoding='utf-8') as f:
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                email_file.unlink()
        except (IOError, OSError):
            # 文件被占用，跳过删除
            pass
        except Exception as e:
            print(f"  [Subagent] 清理邮件文件失败: {e}")

        try:
            if result_file.exists():
                # 获取独占锁确保没有进程正在写入/读取
                with open(result_file, 'r', encoding='utf-8') as f:
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                result_file.unlink()
        except (IOError, OSError):
            # 文件被占用，跳过删除
            pass
        except Exception as e:
            print(f"  [Subagent] 清理结果文件失败: {e}")

    def _spawn_subagent_for_email(self, email_data: Dict, email_id: str) -> Tuple[bool, str, str]:
        """
        Spawn 一个 subagent 来分析单封邮件

        Returns:
            (是否紧急, 判断理由, 邮件摘要)
        """
        # 写入邮件数据
        email_file = self._write_email_for_subagent(email_data, email_id)

        # 构建 subagent prompt
        subject = email_data.get('subject', '')
        sender = email_data.get('sender', '')
        body = email_data.get('body_text', '')[:2000]

        prompt = f"""请扮演专业的商务邮件分发助手，深度分析以下邮件的上下文意图，并严格输出 JSON 格式结果。

邮件信息：
发件人: {sender}
主题: {subject}
正文: {body}

邮件数据文件: {email_file}
结果输出文件: {self._results_dir / f"{email_id}.json"}

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
- 务必只输出合法的纯 JSON 字符串，绝对不要输出哪怕一个字的额外解释文字，也不要包含 ```json 这样的 Markdown 标记。

请执行以下步骤：
1. 读取邮件数据文件（如果存在）
2. 分析邮件内容，判断是否紧急（严格按照上述4点逻辑）
3. 生成 JSON 格式的分析结果
4. 将结果写入结果文件（覆盖原有内容）
5. 打印 "ANALYSIS_COMPLETE: {email_id}"

注意：
- 结果文件格式必须为有效 JSON
- 确保打印 ANALYSIS_COMPLETE 标记以便主进程识别
"""

        last_error = None

        for attempt in range(self.retry_count):
            try:
                # 使用 sessions_spawn 触发 subagent 分析
                if not HAS_OPENCLAW:
                    raise ImportError("未安装 openclaw 包")

                result = sessions_spawn(
                    runtime="subagent",
                    mode="run",
                    message=prompt,
                    timeout_seconds=self.timeout
                )

                # 等待结果文件（使用相同的超时时间）
                analysis_result = self._wait_for_result(email_id)

                if analysis_result is None:
                    raise TimeoutError(f"等待 subagent 结果超时: {email_id}")

                # 解析结果
                is_urgent = analysis_result.get('is_urgent', False)
                reason = analysis_result.get('reason', '')
                summary = analysis_result.get('summary', '')

                if not isinstance(is_urgent, bool):
                    raise ValueError(f"is_urgent 类型错误: {type(is_urgent)}")

                return is_urgent, reason, summary

            except Exception as e:
                last_error = e
                if attempt < self.retry_count - 1:
                    delay = self.retry_base_delay * (2 ** attempt)
                    print(f"  [Subagent] 分析失败 (尝试 {attempt + 1}/{self.retry_count}): {e}")
                    print(f"  [Subagent] 等待 {delay}s 后重试...")
                    time.sleep(delay)
                else:
                    print(f"  [Subagent] 分析最终失败: {e}")
                    raise

        raise last_error if last_error else Exception("Subagent 分析失败")

    def analyze_email(self, email_data: Dict) -> Tuple[bool, str, str]:
        """
        分析单封邮件

        Returns:
            (是否紧急, 判断理由, 邮件摘要)
        """
        # 生成邮件ID（从 local_path 提取）
        local_path = email_data.get('local_path', '')
        if local_path:
            email_id = local_path.rstrip('/').split('/')[-1]
        else:
            email_id = email_data.get('id', f"email_{int(time.time() * 1000)}")

        try:
            is_urgent, reason, summary = self._spawn_subagent_for_email(email_data, email_id)
            return is_urgent, reason, summary
        finally:
            # 清理临时文件
            self._cleanup_files(email_id)

        # === v1 方法已废弃 (2026-03-30) ===
    # check_urgent() 和 summarize_email() 已删除
    # 所有分析统一使用 analyze_email() v2 方法（单次 JSON 调用）

    def analyze_emails_batch(self, emails: List[Dict],
                             callback: Optional[Callable] = None) -> List[Dict]:
        """
        批量分析邮件（分批次处理）

        Args:
            emails: 邮件列表
            callback: 每处理完一封邮件的回调函数

        Returns:
            分析后的邮件列表
        """
        results = []

        print(f"\n🤖 Subagent 批量分析 {len(emails)} 封邮件 (并发限制: {self.max_concurrent})...")

        # 分批次处理
        for batch_start in range(0, len(emails), self.max_concurrent):
            batch_end = min(batch_start + self.max_concurrent, len(emails))
            batch = emails[batch_start:batch_end]

            print(f"  处理批次 {batch_start // self.max_concurrent + 1}/{(len(emails) + self.max_concurrent - 1) // self.max_concurrent} ({len(batch)} 封)")

            with ThreadPoolExecutor(max_workers=len(batch)) as executor:
                future_to_email = {}

                for email in batch:
                    local_path = email.get('local_path', '')
                    if local_path:
                        email_id = local_path.rstrip('/').split('/')[-1]
                    else:
                        email_id = email.get('id', f"email_{int(time.time() * 1000)}")

                    # 写入邮件数据文件
                    self._write_email_for_subagent(email, email_id)

                    # 提交任务
                    future = executor.submit(self._spawn_subagent_for_email, email, email_id)
                    future_to_email[future] = (email, email_id)

                # 处理结果
                for i, future in enumerate(as_completed(future_to_email), 1):
                    email, email_id = future_to_email[future]
                    batch_idx = batch_start + i

                    try:
                        is_urgent, reason, summary = future.result()
                        email['is_urgent'] = is_urgent
                        email['reason'] = reason
                        email['summary'] = summary
                        results.append(email)

                        print(f"  [{batch_idx}/{len(emails)}] {email['subject'][:30]}... - 紧急: {'是' if is_urgent else '否'}")

                        if callback:
                            callback(email, is_urgent, reason, summary)

                    except Exception as e:
                        print(f"  [{batch_idx}/{len(emails)}] 分析失败: {e}")
                        email['is_urgent'] = False
                        email['reason'] = f"分析出错: {str(e)}"
                        email['summary'] = "[分析失败]"
                        results.append(email)
                    finally:
                        # 清理临时文件
                        self._cleanup_files(email_id)

        return results
