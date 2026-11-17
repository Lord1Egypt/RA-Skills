# -*- coding: utf-8 -*-
"""跨模块复用的小工具（确认 token / 契约摘要）。

``make_token`` / ``contract_sha`` 原逐字散落于 ``modules/customize.py`` 与
``modules/import_asset.py``（确认/导入两步确认共用），抽到此处单一来源，
避免「改一处漏另一处」的漂移。
"""
from __future__ import annotations

import hashlib
import json
from typing import Any


def contract_sha(contract: dict[str, Any]) -> str:
    """契约摘要（SHA-256）：用于确认 token 防漂移 / 手滑。"""
    return hashlib.sha256(
        json.dumps(contract, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def make_token(payload: dict[str, Any], contract_sha: str) -> str:
    """确认 token：变更/暂存规范 + 当前契约摘要，防确认漂移 / 手滑。

    ``payload`` 为变更规范（customize）或导入候选暂存（import_asset）。
    """
    canon = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256((canon + "|" + contract_sha).encode("utf-8")).hexdigest()[:16]
