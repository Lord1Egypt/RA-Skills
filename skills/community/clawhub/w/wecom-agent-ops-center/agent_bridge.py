"""
Agent 桥接层 - 将标准化 JSON 转发到用户 Agent 的 HTTP 端点

职责：
1. POST 标准化 JSON → Agent HTTP 端点
2. 接收 Agent 的 JSON 响应
3. 调用 ws_client 回复/推送到企微
4. 重试 / 超时处理
"""

import asyncio
import json
import logging
import time
from typing import Optional

logger = logging.getLogger("wecom.connector")


class AgentBridge:
    """Agent 端点桥接器"""

    def __init__(self, endpoint: str, timeout: int = 30, retry: int = 3):
        self.endpoint = endpoint
        self.timeout = timeout
        self.retry = retry

        self._call_count: int = 0
        self._error_count: int = 0
        self._total_latency_ms: float = 0

    @property
    def stats(self) -> dict:
        avg_latency = 0
        if self._call_count > 0:
            avg_latency = round(self._total_latency_ms / self._call_count)
        return {
            "endpoint": self.endpoint,
            "calls": self._call_count,
            "errors": self._error_count,
            "avg_latency_ms": avg_latency,
        }

    async def forward(self, standard_msg: dict) -> Optional[dict]:
        """
        转发消息到 Agent 端点，返回 Agent 的回复。
        
        Args:
            standard_msg: 标准化 JSON（msg_converter.wecom_to_standard 输出）
        
        Returns:
            Agent 回复 dict，或 None（无回复 / 出错）
        """
        import aiohttp

        last_error = None
        for attempt in range(self.retry):
            try:
                timeout = aiohttp.ClientTimeout(total=self.timeout)
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    start = time.time()
                    async with session.post(
                        self.endpoint,
                        json=standard_msg,
                        headers={"Content-Type": "application/json"},
                    ) as resp:
                        latency = (time.time() - start) * 1000
                        self._call_count += 1
                        self._total_latency_ms += latency

                        if resp.status == 200:
                            reply = await resp.json()
                            logger.info(
                                f"Agent → 响应 | {resp.status} | "
                                f"{latency:.0f}ms | "
                                f"{str(reply)[:80]}"
                            )
                            return reply
                        elif resp.status == 204:
                            # Agent 不想回复（只看不说）
                            logger.info(f"Agent → 无回复 (204)")
                            return None
                        else:
                            last_error = f"HTTP {resp.status}"
                            logger.warning(f"Agent 错误: {resp.status} (attempt {attempt+1})")

            except aiohttp.ClientConnectorError:
                last_error = "连接被拒绝"
                logger.warning(f"Agent 不可达: {self.endpoint} (attempt {attempt+1})")
            except asyncio.TimeoutError:
                last_error = "超时"
                logger.warning(f"Agent 超时 ({self.timeout}s) (attempt {attempt+1})")
            except json.JSONDecodeError as e:
                last_error = f"JSON 解析失败"
                logger.error(f"Agent 返回非 JSON: {e}")
                break  # 非 JSON 不重试
            except Exception as e:
                last_error = str(e)[:80]
                logger.error(f"Agent 异常: {e} (attempt {attempt+1})")

            if attempt < self.retry - 1:
                await asyncio.sleep(1 * (attempt + 1))  # 退避: 1s, 2s, 3s...

        self._error_count += 1
        logger.error(f"Agent 转发失败 ({self.retry} 次重试后): {last_error}")
        return None
