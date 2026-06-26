"""
XHS Expert - 互动处理器
点赞、收藏、评论、关注、批量互动
"""

import asyncio
import json
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Dict, Any

from xhs_client import XHSClient


class ActionResult(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    NEED_LOGIN = "need_login"
    RATE_LIMITED = "rate_limited"


@dataclass
class InteractionResponse:
    """互动操作响应"""
    result: ActionResult
    message: str
    data: Optional[Dict] = None


class InteractionHandler:
    """
    互动处理器（API模式）

    通过小红书API直接执行互动操作。
    """

    def __init__(self, client: XHSClient):
        self.client = client

    async def like(
        self,
        note_id: str,
        action: str = "add"
    ) -> InteractionResponse:
        """
        点赞/取消点赞

        参数：
            note_id: 笔记ID
            action: "add" 点赞, "remove" 取消
        """
        try:
            result = await self.client.like_note(note_id, action)

            return InteractionResponse(
                result=ActionResult.SUCCESS,
                message=f"{'点赞' if action == 'add' else '取消点赞'}成功",
                data=result
            )
        except Exception as e:
            error_msg = str(e)

            if "登录" in error_msg:
                return InteractionResponse(
                    result=ActionResult.NEED_LOGIN,
                    message="请先登录"
                )
            elif "频繁" in error_msg or "限制" in error_msg:
                return InteractionResponse(
                    result=ActionResult.RATE_LIMITED,
                    message="操作太频繁，请稍后重试"
                )
            else:
                return InteractionResponse(
                    result=ActionResult.FAILED,
                    message=f"点赞失败: {error_msg}"
                )

    async def collect(
        self,
        note_id: str,
        collect_id: str = "",
        action: str = "add"
    ) -> InteractionResponse:
        """收藏/取消收藏"""
        try:
            result = await self.client.collect_note(note_id, collect_id, action)

            return InteractionResponse(
                result=ActionResult.SUCCESS,
                message=f"{'收藏' if action == 'add' else '取消收藏'}成功",
                data=result
            )
        except Exception as e:
            return InteractionResponse(
                result=ActionResult.FAILED,
                message=f"收藏失败: {str(e)}"
            )

    async def comment(
        self,
        note_id: str,
        content: str,
        xsec_token: str = ""
    ) -> InteractionResponse:
        """
        发表评论

        参数：
            note_id: 笔记ID
            content: 评论内容（支持emoji）
        """
        if not content or len(content.strip()) == 0:
            return InteractionResponse(
                result=ActionResult.FAILED,
                message="评论内容不能为空"
            )

        if len(content) > 500:
            return InteractionResponse(
                result=ActionResult.FAILED,
                message="评论内容不能超过500字"
            )

        try:
            result = await self.client.post_comment(note_id, content)

            return InteractionResponse(
                result=ActionResult.SUCCESS,
                message="评论成功",
                data=result
            )
        except Exception as e:
            error_msg = str(e)

            if "频繁" in error_msg or "限制" in error_msg:
                return InteractionResponse(
                    result=ActionResult.RATE_LIMITED,
                    message="评论太频繁，请稍后重试"
                )
            elif "敏感" in error_msg:
                return InteractionResponse(
                    result=ActionResult.FAILED,
                    message="评论包含敏感内容"
                )
            else:
                return InteractionResponse(
                    result=ActionResult.FAILED,
                    message=f"评论失败: {error_msg}"
                )

    async def reply_comment(
        self,
        note_id: str,
        comment_id: str,
        content: str
    ) -> InteractionResponse:
        """回复指定评论"""
        try:
            result = await self.client.post_comment(
                note_id, content, target_comment_id=comment_id
            )

            return InteractionResponse(
                result=ActionResult.SUCCESS,
                message="回复成功",
                data=result
            )
        except Exception as e:
            return InteractionResponse(
                result=ActionResult.FAILED,
                message=f"回复失败: {str(e)}"
            )

    async def follow(self, user_id: str) -> InteractionResponse:
        """关注用户"""
        try:
            result = await self.client.follow_user(user_id, "add")

            return InteractionResponse(
                result=ActionResult.SUCCESS,
                message="关注成功",
                data=result
            )
        except Exception as e:
            return InteractionResponse(
                result=ActionResult.FAILED,
                message=f"关注失败: {str(e)}"
            )

    async def unfollow(self, user_id: str) -> InteractionResponse:
        """取消关注"""
        try:
            result = await self.client.follow_user(user_id, "remove")

            return InteractionResponse(
                result=ActionResult.SUCCESS,
                message="取消关注成功",
                data=result
            )
        except Exception as e:
            return InteractionResponse(
                result=ActionResult.FAILED,
                message=f"取消关注失败: {str(e)}"
            )


class BatchInteractionHandler:
    """
    批量互动处理器

    支持批量点赞、评论、收藏，带频率控制。
    """

    def __init__(self, handler: InteractionHandler, delay: float = 2.0):
        self.handler = handler
        self.delay = delay

    async def batch_like(
        self,
        note_ids: List[str],
        delay: Optional[float] = None
    ) -> List[InteractionResponse]:
        """批量点赞"""
        delay = delay or self.delay
        results = []

        for note_id in note_ids:
            result = await self.handler.like(note_id)
            results.append(result)
            await asyncio.sleep(delay)

        return results

    async def batch_collect(
        self,
        note_ids: List[str],
        delay: Optional[float] = None
    ) -> List[InteractionResponse]:
        """批量收藏"""
        delay = delay or self.delay
        results = []

        for note_id in note_ids:
            result = await self.handler.collect(note_id)
            results.append(result)
            await asyncio.sleep(delay)

        return results

    async def batch_comment(
        self,
        note_contents: Dict[str, str],
        delay: Optional[float] = None
    ) -> List[InteractionResponse]:
        """
        批量评论

        参数：{note_id: comment_content}
        """
        delay = delay or self.delay
        results = []

        for note_id, content in note_contents.items():
            result = await self.handler.comment(note_id, content)
            results.append(result)
            await asyncio.sleep(delay)

        return results

    def summarize_results(self, results: List[InteractionResponse]) -> Dict[str, Any]:
        """汇总批量操作结果"""
        total = len(results)
        success = sum(
            1 for r in results if r.result == ActionResult.SUCCESS
        )
        failed = sum(
            1 for r in results if r.result == ActionResult.FAILED
        )
        rate_limited = sum(
            1 for r in results if r.result == ActionResult.RATE_LIMITED
        )
        need_login = sum(
            1 for r in results if r.result == ActionResult.NEED_LOGIN
        )

        return {
            "total": total,
            "success": success,
            "failed": failed,
            "rate_limited": rate_limited,
            "need_login": need_login,
            "success_rate": f"{success/total*100:.1f}%" if total else "0%"
        }
