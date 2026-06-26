from __future__ import annotations

import json
from typing import Any, Optional

import requests

from toupiaoya.constants import (
    BASE_IMAGE_URL,
    BASE_PREVIEW_URL,
    STORE_SEARCH_HEADERS,
    TOUPIAOYA_STORE_SEARCH_URL,
)


class ToupiaoyaStoreWebSearch:
    name: str = "toupiaoya_template_search"
    description: str = """进行投票鸭模板搜索，返回模板内容"""

    def execute(
        self,
        query: Optional[str] = None,
        page_no: int = 1,
        num_results: int = 10,
        sort_by: str = "common_total|desc",
        color: Optional[str] = None,
    ) -> dict[str, Any]:
        session = requests.Session()
        session.headers = dict(STORE_SEARCH_HEADERS)
        jsonquery: dict[str, Any] = {
            "sortBy": sort_by,
            "pageNo": page_no,
            "pageSize": num_results,
            "searchCode": "42312",
        }
        if query:
            jsonquery["keywords"] = query
        if color:
            jsonquery["color"] = color
        res = session.post(url=TOUPIAOYA_STORE_SEARCH_URL, json=jsonquery)
        res.encoding = "utf-8"
        result = json.loads(res.text)
        if result["obj"]["total"] == 0:
            return {}
        result_list = []
        for k in result["obj"]["dataList"]:
            result_list.append(
                {
                    "templateId": k["id"],
                    "title": k["title"],
                    "link": BASE_PREVIEW_URL + str(k["id"]),
                    "description": k["description"],
                    "pv": k["views"],
                    "cover": BASE_IMAGE_URL
                    + k.get("productTypeMap", {}).get("tmbPath")
                    + "?imageMogr2/thumbnail/320x320>",
                }
            )

        return {"total": result["obj"]["total"], "end": result["obj"]["end"], "results": result_list}
