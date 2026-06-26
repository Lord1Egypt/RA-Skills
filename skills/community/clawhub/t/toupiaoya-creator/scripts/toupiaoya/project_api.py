from __future__ import annotations

import time
from typing import Any

from toupiaoya.constants import BROWSER_CHROME_UA, DEFAULT_BASE_URL, DEFAULT_TIMEOUT, LWORK_API_BASE
from toupiaoya.http import get, post_json
from typing import Any, Mapping, MutableMapping

_LWORK_LIST_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "user-agent": BROWSER_CHROME_UA,
}

def _rows_from_list2_body(body: Mapping[str, Any]) -> list[dict[str, Any]]:
    """list2 成功响应：列表在根级 list；兼容旧形态 obj 为数组或 obj.list。"""
    top = body.get("list")
    if isinstance(top, list) and all(isinstance(x, dict) for x in top):
        return list(top)
    obj = body.get("obj")
    if isinstance(obj, list):
        return [x for x in obj if isinstance(x, dict)]
    if isinstance(obj, dict):
        for key in ("list", "records", "rows"):
            v = obj.get(key)
            if isinstance(v, list) and all(isinstance(x, dict) for x in v):
                return list(v)
    return []


def _slim_upload_material_row(row: Mapping[str, Any]) -> dict[str, Any]:
    tag_ids = row.get("tagIds")
    if tag_ids is None:
        tid = row.get("tagId")
        if tid is None:
            tag_ids = []
        elif isinstance(tid, list):
            tag_ids = list(tid)
        else:
            tag_ids = [tid]
    return {
        "id": row.get("id"),
        "path": row.get("path"),
        "name": row.get("name"),
        "tagIds": tag_ids,
    }

def fetch_scene_data_list(
    access_token: str,
    *,
    list_type: int = 3,
    sort: str = "update_time",
    order_type: str = "desc",
    page_num: int = 1,
    page_size: int = 27,
    biz_types: str = "",
    lwork_api_base: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """
    GET /m/scene/data/list
    工作台场景/作品分页列表（投票鸭 lwork-api）。
    """
    base = (lwork_api_base or LWORK_API_BASE).rstrip("/")
    url = f"{base}/m/scene/data/list"
    res = get(
        url,
        access_token=access_token,
        params={
            "type": list_type,
            "sort": sort,
            "orderType": order_type,
            "pageNum": page_num,
            "pageSize": page_size,
            "bizTypes": biz_types,
        },
        extra_headers=dict(_LWORK_LIST_HEADERS),
        timeout=timeout,
    )
    res.raise_for_status()
    body = res.json()
    if not isinstance(body, dict):
        raise RuntimeError("scene/data/list 返回非 JSON 对象")
    if not body.get("success") or body.get("code") != 200:
        raise RuntimeError(str(body.get("msg") or "作品列表 list 失败"))
    slim = [_slim_upload_material_row(r) for r in _rows_from_list2_body(body)]
    out: dict[str, Any] = {
        "success": bool(body.get("success")),
        "code": body.get("code"),
    }
    if "msg" in body:
        out["msg"] = body["msg"]
    if "obj" in body:
        out["obj"] = body["obj"]
    if "map" in body:
        out["map"] = body["map"]
    out["list"] = slim
    return out

def fetch_project_choices(
    access_token: str,
    *,
    project_id: int,
    base_url: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    base = (base_url or DEFAULT_BASE_URL).rstrip("/")
    url = f"{base}/iaigc-toupiaoya/get_choices"
    res = get(
        url,
        access_token=access_token,
        params={"id": project_id},
        timeout=timeout,
    )
    res.raise_for_status()
    body = res.json()
    if not isinstance(body, dict):
        raise RuntimeError("get_choices 返回非 JSON 对象")
    if not body.get("success") or body.get("code") != 200:
        raise RuntimeError(str(body.get("msg") or "获取选项失败"))
    return body


def update_project_choice(
    access_token: str,
    *,
    project_id: int,
    choice_id: int,
    choice_patch: dict[str, Any],
    base_url: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    base = (base_url or DEFAULT_BASE_URL).rstrip("/")
    url = f"{base}/iaigc-toupiaoya/update_choices"
    payload = {
        "id": project_id,
        "choiceId": choice_id,
        "choice": choice_patch,
    }
    res = post_json(url, payload, access_token=access_token, timeout=timeout)
    res.raise_for_status()
    body = res.json()
    if not isinstance(body, dict):
        raise RuntimeError("update_choices 返回非 JSON 对象")
    if not body.get("success") or body.get("code") != 200:
        raise RuntimeError(str(body.get("msg") or "更新选项失败"))
    return body


def add_project_choice(
    access_token: str,
    *,
    project_id: int,
    group_id: int,
    choice_payload: dict[str, Any],
    base_url: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    base = (base_url or DEFAULT_BASE_URL).rstrip("/")
    url = f"{base}/iaigc-toupiaoya/add_choices"
    payload = {
        "id": project_id,
        "groupId": group_id,
        "choice": choice_payload,
    }
    res = post_json(url, payload, access_token=access_token, timeout=timeout)
    res.raise_for_status()
    body = res.json()
    if not isinstance(body, dict):
        raise RuntimeError("add_choices 返回非 JSON 对象")
    if not body.get("success") or body.get("code") != 200:
        raise RuntimeError(str(body.get("msg") or "添加选项失败"))
    return body


def fetch_project_vote_data(
    access_token: str,
    *,
    project_id: int,
    page_no: int = 1,
    page_size: int = 10,
    start_time: str = "",
    end_time: str = "",
    show_trash: int = 1,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    url = "https://form-editor-api.toupiaoya.com/m/lp/data/list"
    payload = {
        "id": str(project_id),
        "startTime": start_time,
        "endTime": end_time,
        "pageNo": page_no,
        "pageSize": page_size,
        "time": int(time.time() * 1000),
        "showTrash": show_trash,
    }
    res = post_json(url, payload, access_token=access_token, timeout=timeout)
    res.raise_for_status()
    body = res.json()
    if not isinstance(body, dict):
        raise RuntimeError("vote-data 返回非 JSON 对象")
    if not body.get("success") or body.get("code") != 200:
        raise RuntimeError(str(body.get("msg") or "获取投票数据失败"))
    return body


def fetch_project_view_data(
    access_token: str,
    *,
    project_id: int,
    start_day: str,
    end_day: str,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    url = "https://lwork-api.toupiaoya.com/m/single/getWorkViewData"
    res = get(
        url,
        access_token=access_token,
        params={
            "sceneId": project_id,
            "product": "form",
            "startDay": start_day,
            "endDay": end_day,
        },
        timeout=timeout,
    )
    res.raise_for_status()
    body = res.json()
    if not isinstance(body, dict):
        raise RuntimeError("view-data 返回非 JSON 对象")
    if not body.get("success") or body.get("code") != 200:
        raise RuntimeError(str(body.get("msg") or "获取访问数据失败"))
    return body


def fetch_project_groups(
    access_token: str,
    *,
    project_id: int,
    base_url: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    base = (base_url or DEFAULT_BASE_URL).rstrip("/")
    url = f"{base}/iaigc-toupiaoya/get_groups"
    res = get(url, access_token=access_token, params={"id": project_id}, timeout=timeout)
    res.raise_for_status()
    body = res.json()
    if not isinstance(body, dict):
        raise RuntimeError("get_groups 返回非 JSON 对象")
    if not body.get("success") or body.get("code") != 200:
        raise RuntimeError(str(body.get("msg") or "获取分组失败"))
    return body


def add_project_group(
    access_token: str,
    *,
    project_id: int,
    group_name: str,
    base_url: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    base = (base_url or DEFAULT_BASE_URL).rstrip("/")
    url = f"{base}/iaigc-toupiaoya/add_group"
    payload = {"id": project_id, "group_name": group_name}
    res = post_json(url, payload, access_token=access_token, timeout=timeout)
    res.raise_for_status()
    body = res.json()
    if not isinstance(body, dict):
        raise RuntimeError("add_group 返回非 JSON 对象")
    if not body.get("success") or body.get("code") != 200:
        raise RuntimeError(str(body.get("msg") or "新增分组失败"))
    return body


def update_project_group(
    access_token: str,
    *,
    project_id: int,
    group_id: int,
    group_name: str,
    base_url: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    base = (base_url or DEFAULT_BASE_URL).rstrip("/")
    url = f"{base}/iaigc-toupiaoya/update_group"
    payload = {
        "id": project_id,
        "groupId": group_id,
        "group_name": group_name,
    }
    res = post_json(url, payload, access_token=access_token, timeout=timeout)
    res.raise_for_status()
    body = res.json()
    if not isinstance(body, dict):
        raise RuntimeError("update_group 返回非 JSON 对象")
    if not body.get("success") or body.get("code") != 200:
        raise RuntimeError(str(body.get("msg") or "更新分组失败"))
    return body
