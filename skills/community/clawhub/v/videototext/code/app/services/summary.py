from __future__ import annotations

import logging
from typing import Any, Optional

import httpx

from app.core.settings import settings

logger = logging.getLogger(__name__)


def _message_content_to_text(message: dict[str, Any]) -> str:
    """OpenAI 兼容：content 为 str；部分网关为多段 list[{type,text}]。"""
    if not message:
        return ""
    raw = message.get("content")
    if isinstance(raw, str):
        return raw.strip()
    if isinstance(raw, list):
        chunks: list[str] = []
        for part in raw:
            if isinstance(part, dict):
                t = str(part.get("type") or "")
                if t == "text" and part.get("text"):
                    chunks.append(str(part["text"]))
                elif part.get("text"):
                    chunks.append(str(part["text"]))
            elif isinstance(part, str):
                chunks.append(part)
        return "\n".join(x.strip() for x in chunks if x and str(x).strip()).strip()
    return ""


class TextSummaryService:
    def summarize(self, text: str, title: str = "", max_chars: int = 100) -> str:
        src = (text or "").strip()
        if not src:
            return ""
        mc = max(50, min(8000, int(max_chars or 100)))
        llm = self._summarize_via_llm(src, title=title, max_chars=mc)
        if llm:
            return llm
        return self._summarize_fallback(src, title=title, max_chars=mc)

    def _chat_endpoint(self) -> Optional[str]:
        full = (settings.summary_llm_chat_completions_url or "").strip()
        if full:
            return full
        base = (settings.summary_llm_base_url or "").strip()
        if not base:
            return None
        b = base.rstrip("/")
        # 有人把完整 Chat Completions 地址误填在 BASE_URL 里，避免再拼一段 /chat/completions
        if b.endswith("/chat/completions"):
            return b
        return f"{b}/chat/completions"

    def _summarize_via_llm(
        self, text: str, title: str = "", max_chars: int = 200
    ) -> Optional[str]:
        if not bool(settings.summary_enabled):
            logger.info("总结稿跳过 LLM：SUMMARY_ENABLED=false")
            return None
        endpoint = self._chat_endpoint()
        api_key = (settings.summary_llm_api_key or "").strip()
        model = (settings.summary_llm_model or "").strip()
        if not endpoint:
            logger.info(
                "总结稿跳过 LLM：未配置 SUMMARY_LLM_BASE_URL / OPENAI_BASE_URL "
                "或 SUMMARY_LLM_CHAT_COMPLETIONS_URL / OPENAI_CHAT_COMPLETIONS_URL"
            )
            return None
        if not model:
            logger.info(
                "总结稿跳过 LLM：未配置 SUMMARY_LLM_MODEL 或 OPENAI_MODEL（仅有 baseUrl 与 apiKey 不会调用模型）"
            )
            return None
        # 短目标：极省字数的一段电报体；长目标：分主题 Markdown 块（与产品内「深度摘要」展示一致）。
        src_for_llm = text[:60000] if len(text) > 60000 else text
        if max_chars <= 200:
            prompt = (
                "你是一名中文内容编辑。请根据以下视频字幕写「总结稿」。\n"
                "输出要求：\n"
                f"1) 只输出一段连贯的简体中文，总字数尽量约 {max_chars} 字（可略浮动，勿明显超出）；\n"
                "2) 高密度「电报体」：用分号或逗号串联多个关键信息，优先保留人名、机构、数字、结论、对立观点；\n"
                "3) 不要条列、不要小标题、不要「要点/正文」两截；禁止同义重复。\n\n"
                f"视频标题：{title or '（无）'}\n\n"
                f"字幕正文：\n{src_for_llm}"
            )
            system_msg = (
                "你擅长从口语字幕中提炼极短、信息密度高、不重复的一段中文摘要。"
            )
        else:
            prompt = (
                "你是一名中文内容编辑。请根据以下视频字幕写「总结稿」，风格与深度读物摘要一致："
                "按内容自然分主题展开，信息密度高，避免正确的废话与同义复述。\n\n"
                "【版式要求 — 必须严格遵守】\n"
                "1) 第一行且仅一行：以 Markdown 二级标题开头，格式为 `## ` + 一句总标题。"
                " 可结合下方「视频标题」自拟，例如「xxx 内容摘要」「访谈要点梳理」等。\n"
                "2) 第二行起为正文：由若干「主题块」组成。每个主题块格式固定为："
                " 单独一行以 `**主题：**` 开头（主题 2～10 个字，根据字幕实际内容自拟，"
                " 访谈可写背景、人物经历、核心观点、方法论等；教程可写步骤、要点、注意事项；"
                " 新闻可写要素与后续影响；禁止滥用万能套话小标题）。\n"
                "3) 同一主题块内：`**主题：**` 之后紧接该主题下的叙述，可一句或多句；"
                " 块与块之间空一行（即连续两个换行）。\n"
                "4) 全文使用简体中文。不要输出 JSON、不要代码围栏、不要前置「以下是摘要」等套话。\n\n"
                f"【篇幅】全文总字数（含标点、含小标题中的字）尽量接近 {max_chars} 字，"
                "以该字数为硬上限，不要明显超出；若字幕极长，在字数内优先保留主线、转折、结论与关键事实。\n\n"
                f"视频标题：{title or '（无）'}\n\n"
                f"字幕正文：\n{src_for_llm}"
            )
            system_msg = (
                "你擅长将冗长口语字幕整理为分主题、可读性强的高密度中文摘要；"
                "严格使用「## 总标题」与「**主题：**段落」交替结构，主题名随内容变化，不模板化。"
            )
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        body = {
            "model": model,
            "temperature": float(settings.summary_llm_temperature),
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt},
            ],
        }
        timeout = max(5.0, float(settings.summary_llm_timeout_seconds))
        try:
            logger.info("总结稿请求 LLM：endpoint=%s model=%s", endpoint, model)
            with httpx.Client(timeout=timeout, headers=headers) as client:
                resp = client.post(endpoint, json=body)
                resp.raise_for_status()
                data = resp.json()
            choices = data.get("choices") or []
            if not choices:
                logger.warning(
                    "LLM summary 响应无 choices，回退本地摘要；keys=%s",
                    list(data.keys()) if isinstance(data, dict) else type(data),
                )
                return None
            msg = (choices[0] or {}).get("message") or {}
            out = _message_content_to_text(msg if isinstance(msg, dict) else {})
            if not out:
                # Kimi 等推理模型偶发仅 reasoning_content；无正文时不再静默回退，便于日志排查
                has_r = bool(
                    isinstance(msg, dict)
                    and isinstance(msg.get("reasoning_content"), str)
                    and (msg.get("reasoning_content") or "").strip()
                )
                logger.warning(
                    "LLM summary 的 message.content 为空，回退本地摘要；"
                    "message_keys=%s has_reasoning_content=%s",
                    list(msg.keys()) if isinstance(msg, dict) else type(msg),
                    has_r,
                )
                return None
            logger.info("总结稿已由 LLM 生成，长度=%s", len(out))
            return out
        except httpx.HTTPStatusError as exc:
            snippet = ""
            try:
                snippet = (exc.response.text or "")[:400]
            except Exception:
                pass
            logger.warning(
                "LLM summary HTTP %s，回退本地摘要: %s body=%r",
                exc.response.status_code,
                exc,
                snippet,
            )
            return None
        except Exception as exc:
            logger.warning("LLM summary failed, fallback to local summary: %s", exc)
            return None

    def _summarize_fallback(self, text: str, title: str = "", max_chars: int = 100) -> str:
        lines = [x.strip() for x in text.splitlines() if x.strip()]
        if not lines:
            return ""
        picks = []
        step = max(1, len(lines) // 6)
        idx = 0
        while idx < len(lines) and len(picks) < 6:
            picks.append(lines[idx])
            idx += step
        bullet = "\n".join([f"- {x}" for x in picks[:6]])
        summary = (
            f"本段围绕「{title or '该视频'}」展开，要点见上。"
            f"（本地回退摘要，目标约 {max_chars} 字；可在 .env 配置 SUMMARY_LLM_* 调用大模型。）"
        )
        return f"{bullet}\n\n{summary}"
