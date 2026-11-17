#!/usr/bin/env python3
"""skill-to-http params.json 自动生成器

读取 SKILL.md 内容，用 LLM 提取参数 schema，生成 params.json。
兜底策略：生成只有 message 字段的最小 schema。
"""

from __future__ import annotations

import json
import logging
import os
import urllib.request
from pathlib import Path
from typing import Any

logger = logging.getLogger("skill-to-http.params-gen")

# 最小兜底 schema
FALLBACK_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "message": {
            "type": "string",
            "description": "任务描述，告诉 Skill 需要完成什么工作",
        },
    },
    "required": ["message"],
    "additionalProperties": False,
}

# 用于提取 params 的 LLM 提示词
EXTRACTION_SYSTEM_PROMPT = """You are a JSON schema generator. Given a SKILL.md file content, extract all configurable parameters that the skill expects.

Output ONLY a valid JSON object (no markdown fences, no extra text) with this structure:

{
  "type": "object",
  "properties": {
    "message": {
      "type": "string",
      "description": "任务描述"
    },
    "param_name": {
      "type": "string|number|boolean|array|object",
      "description": "参数说明",
      "default": null,
      "enum": ["value1", "value2"]
    }
  },
  "required": ["message"],
  "additionalProperties": false
}

Rules:
- Always include "message" as a required string property
- Only include parameters that are explicitly mentioned as configurable in SKILL.md
- Use the skill's documented parameter names
- If no extra parameters are found, return the schema with only "message"
- Output pure JSON, no markdown backticks
"""


class ParamsGenerator:
    """自动生成 params.json。

    尝试用 LLM 读取 SKILL.md 并提取参数 schema，
    失败时使用只有 message 字段的最小兜底 schema。
    """

    def __init__(self, data_dir: str = "") -> None:
        self.data_dir: str = data_dir

    def generate(self, skill_name: str, skill_md: str) -> dict | None:
        """为指定 Skill 生成 params schema。"""
        # 尝试 LLM 提取
        schema = self._extract_with_llm(skill_name, skill_md)
        if schema:
            return schema

        # 兜底：返回深拷贝，防止调用方修改污染共享对象
        import copy
        logger.info(f"Using fallback schema for '{skill_name}'")
        return copy.deepcopy(FALLBACK_SCHEMA)

    def _extract_with_llm(self, skill_name: str, skill_md: str) -> dict | None:
        """尝试用 LLM 提取参数。"""
        cfg = self._load_config()
        llm_cfg = cfg.get("llm", {})

        base_url = self._resolve_env(llm_cfg.get("base_url", ""))
        api_key = self._resolve_env(llm_cfg.get("api_key", ""))
        model = llm_cfg.get("model", "gpt-4o")

        if not base_url or not api_key:
            logger.debug("LLM not configured, skipping params extraction")
            return None

        # 限制输入长度避免 token 浪费
        skill_md_truncated = skill_md[:6000]

        payload = json.dumps({
            "model": model,
            "messages": [
                {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
                {"role": "user", "content": f"SKILL.md for '{skill_name}':\n\n{skill_md_truncated}"},
            ],
            "temperature": 0.1,
            "max_tokens": 2000,
        }).encode("utf-8")

        chat_url = f"{base_url.rstrip('/')}/chat/completions"

        req = urllib.request.Request(
            chat_url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
            content = data["choices"][0]["message"]["content"]

            # 清理可能的 markdown 包裹
            content = content.strip()
            if content.startswith("```"):
                # 去掉首尾的 markdown fence
                lines = content.split("\n")
                content = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])

            schema = json.loads(content)
            if isinstance(schema, dict) and "type" in schema:
                logger.info(f"LLM extraction succeeded for '{skill_name}'")
                return schema
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse LLM response for '{skill_name}': {e}")
        except Exception as e:
            logger.warning(f"LLM extraction failed for '{skill_name}': {e}")

        return None

    def _load_config(self) -> dict:
        """加载配置文件。"""
        from _paths import CONFIG_PATH; cfg_path = CONFIG_PATH
        if cfg_path.exists():
            try:
                return json.loads(cfg_path.read_text())
            except Exception:
                pass
        return {}

    @staticmethod
    def _resolve_env(value: str) -> str:
        """解析 ${ENV_VAR} 引用。"""
        if value.startswith("${") and value.endswith("}"):
            return os.environ.get(value[2:-1], "")
        return value