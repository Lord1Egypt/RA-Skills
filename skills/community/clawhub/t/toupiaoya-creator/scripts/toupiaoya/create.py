from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from toupiaoya.constants import DEFAULT_BASE_URL
from toupiaoya.http import post_json


def parse_group_list(group_list_text: Optional[str]) -> Optional[List[Dict[str, Any]]]:
    if not group_list_text:
        return None
    parsed = json.loads(group_list_text)
    if not isinstance(parsed, list):
        raise ValueError("--groupList 必须是 JSON 数组")
    return parsed


class ToupiaoyaCreator:
    name: str = "toupiaoya_create"
    description: str = """通过投票鸭API接口创建投票作品"""

    def __init__(self, base_url: str = DEFAULT_BASE_URL) -> None:
        self.base_url = base_url.rstrip("/")

    def execute(
        self,
        brief_title: str,
        brief_desc: str,
        detail_title: Optional[str] = None,
        detail_desc: Optional[str] = None,
        vote_type: Optional[str] = None,
        time_start: Optional[str] = None,
        time_end: Optional[str] = None,
        group_list: Optional[List[Dict[str, Any]]] = None,
        template_id: Optional[int] = None,
        single_vote: Optional[bool] = True,
        sponsor: Optional[str] = None,
        access_token: Optional[str] = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "briefTitle": brief_title,
            "briefDesc": brief_desc,
            "singleVote": single_vote,
        }
        if detail_title:
            payload["detailTitle"] = detail_title
        if detail_desc:
            payload["detailDesc"] = detail_desc
        if vote_type:
            payload["voteType"] = vote_type
        if time_start:
            payload["timeStart"] = time_start
        if time_end:
            payload["timeEnd"] = time_end
        if group_list is not None:
            payload["groupList"] = group_list
        if template_id is not None:
            payload["templateId"] = template_id
        if sponsor:
            payload["sponsor"] = sponsor
        url = f"{self.base_url}/iaigc-toupiaoya/create"
        response = post_json(url, payload, access_token=access_token)
        response.raise_for_status()
        return response.json()
