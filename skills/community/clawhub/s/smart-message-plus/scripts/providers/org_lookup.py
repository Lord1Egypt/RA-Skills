#!/usr/bin/env python3
"""smart-message-plus: org lookup dispatcher (builtin provider API vs custom URL)."""
from __future__ import annotations

import json
import os

from core.http import request


def resolve_department(provider_obj, dept_name: str, cfg: dict) -> dict:
    """Returns {"dept_id","dept_name","member_ids"[...]} using configured mode."""
    org = cfg.get("org_lookup", {})
    mode = org.get("mode", "builtin")
    if mode == "custom":
        url = org.get("custom_url", "").strip()
        if not url:
            raise ValueError(
                "org_lookup.mode=custom 但未配置 custom_url。"
                "请在 config.json 填写你的组织架构查询服务地址（契约见 references/org-lookup-contract.md）"
            )
        headers = {}
        env_name = org.get("custom_auth_header_env", "")
        if env_name and os.environ.get(env_name):
            headers["Authorization"] = os.environ[env_name]
        st, r = request(
            url,
            {"dept_name": dept_name, "provider": provider_obj.name},
            headers=headers,
            timeout=int(org.get("timeout", 10)),
        )
        if st != 200:
            raise RuntimeError(f"自定义组织架构接口 HTTP {st}: {json.dumps(r, ensure_ascii=False)[:200]}")
        if not r.get("member_ids"):
            raise ValueError(f"自定义接口未返回「{dept_name}」的成员（member_ids 为空）")
        return {
            "dept_id": str(r.get("dept_id", "")),
            "dept_name": r.get("dept_path") or r.get("dept_name") or dept_name,
            "member_ids": list(r["member_ids"]),
        }
    # builtin
    return provider_obj.org_resolve_department(dept_name)
