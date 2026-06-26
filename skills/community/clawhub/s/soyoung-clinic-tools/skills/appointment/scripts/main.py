#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""appointment — 门店查询与预约管理。"""

from __future__ import annotations

import json
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from lib.soyoung_runtime import (  # noqa: E402
    PROTECTED_APPOINTMENT_ACTIONS,
    SoyoungRuntimeError,
    audit_event,
    authorize_protected_action,
    build_context_from_args,
    check_create_rate_limit,
    ensure_direct_message,
    ensure_owner,
    format_pending_prompt,
    gen_api_request_id,
    get_state_paths,
    load_api_key,
    load_binding,
    load_location,
    load_pending,
    mark_pending_consumed,
    mark_pending_rejected,
    read_api_base_url,
    read_debug_mode,
    resolve_pending_request,
)


API_BASE_URL = "https://skill.soyoung.com"

_DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")

# ── 门店列表缓存（按 workspace × 城市 × 日期，当天有效）────────────────────────


def _store_cache_path(paths, city_name: str | None) -> Path:
    """返回当天该城市门店缓存文件路径（本地日期，适配国内业务）。"""
    today = time.strftime("%Y-%m-%d")
    city_key = (city_name or "_all_").strip().lower().replace(" ", "_")
    return paths.workspace_dir / "cache" / "store_list" / f"{today}_{city_key}.json"


def _load_store_cache(paths, city_name: str | None) -> dict | None:
    cache_file = _store_cache_path(paths, city_name)
    if cache_file.exists():
        try:
            return json.loads(cache_file.read_text(encoding="utf-8"))
        except Exception:
            pass
    return None


def _save_store_cache(paths, city_name: str | None, result: dict) -> None:
    cache_file = _store_cache_path(paths, city_name)
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(
        json.dumps(result, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    # 顺手清理 7 天前的旧缓存文件（不阻塞主流程）
    try:
        cutoff = time.strftime(
            "%Y-%m-%d",
            time.localtime(time.time() - 7 * 86400),
        )
        for f in cache_file.parent.iterdir():
            if f.is_file() and f.name < cutoff:
                f.unlink(missing_ok=True)
    except Exception:
        pass
    # 同步更新门店索引
    _update_store_index(paths, city_name, result.get("data", []))


# ── 门店索引（store_index.json）：跨城市，永久累积，按 hospital_id 去重 ────────
# 结构：{"stores": [{"hospital_id": 1, "name": "蓝港店", "city": "北京", "address": "..."}, ...]}
# 用途：AI 可通过门店名直接反查 city_name + hospital_id，无需先猜城市再拉列表

_STORE_INDEX_FILE = "store_index.json"


def _store_index_path(paths) -> Path:
    return paths.workspace_dir / "cache" / _STORE_INDEX_FILE


def _load_store_index(paths) -> list[dict]:
    index_file = _store_index_path(paths)
    if index_file.exists():
        try:
            return json.loads(index_file.read_text(encoding="utf-8")).get("stores", [])
        except Exception:
            pass
    return []


def _update_store_index(paths, city_name: str | None, stores: list[dict]) -> None:
    """把一次 store_list 返回的门店合并进持久索引，按 hospital_id 去重。"""
    if not stores or not city_name:
        return
    try:
        index_file = _store_index_path(paths)
        index_file.parent.mkdir(parents=True, exist_ok=True)
        existing = _load_store_index(paths)
        existing_by_id = {s["hospital_id"]: s for s in existing if s.get("hospital_id")}
        for store in stores:
            hid = store.get("机构ID")
            if not hid:
                continue
            existing_by_id[hid] = {
                "hospital_id": hid,
                "name": store.get("机构名称", ""),
                "city": city_name,
                "address": store.get("机构地址", ""),
            }
        index_file.write_text(
            json.dumps(
                {"stores": list(existing_by_id.values())},
                ensure_ascii=False,
                separators=(",", ":"),
            ),
            encoding="utf-8",
        )
    except Exception:
        pass


def store_lookup(store_name: str, paths) -> dict:
    """从本地门店索引按名称模糊匹配，返回 city + hospital_id + address。"""
    index = _load_store_index(paths)
    if not index:
        return {
            "success": False,
            "error": "本地门店索引为空，请先查询一次门店列表以建立索引",
        }
    name_lower = store_name.lower()
    matched = [s for s in index if name_lower in s.get("name", "").lower()]
    if matched:
        return {"success": True, "data": matched}
    return {
        "success": False,
        "error": (
            f'本地索引中未找到包含"{store_name}"的门店。'
            "请先用 store_list 查询对应城市的门店列表以更新索引。"
        ),
    }


def _validate_datetime(value: str, name: str) -> None:
    """校验时间参数格式为 YYYY-MM-DD HH:MM:SS，防止注入任意字符串。"""
    if not _DATETIME_RE.match(value):
        raise SoyoungRuntimeError(
            f"❌ 参数 {name} 格式无效，需为 YYYY-MM-DD HH:MM:SS"
            f"（如 2026-04-11 09:00:00），实际收到：{value!r}"
        )


# 调试开关：req_id 始终会发给后端，仅此开关控制会话中是否展示
SOYOUNG_DEBUG: bool = os.environ.get("SOYOUNG_DEBUG", "false").lower() in (
    "1",
    "true",
    "yes",
)
_last_req_id: str = ""
_last_elapsed_ms: float = 0.0
_script_start: float = 0.0
_store_cache_hit: bool = False  # 当次调用是否命中缓存


def _debug_footer() -> str:
    if not SOYOUNG_DEBUG:
        return ""
    total_ms = (time.monotonic() - _script_start) * 1000 if _script_start else 0.0
    if _store_cache_hit:
        return f"\n\n> 🗄️ **缓存命中**（门店列表） · **总计**: `{total_ms:.0f} ms`"
    if not _last_req_id:
        return ""
    return (
        f"\n\n> 🔍 **req_id**: `{_last_req_id}`"
        f" · **接口**: `{_last_elapsed_ms:.0f} ms`"
        f" · **总计**: `{total_ms:.0f} ms`"
    )


def make_request(endpoint, body=None, api_key=None):
    global _last_req_id, _last_elapsed_ms
    req_id = gen_api_request_id()
    _last_req_id = req_id
    url = f"{API_BASE_URL}{endpoint}"
    payload = {"api_key": api_key or "", "request_id": req_id}
    if body:
        payload.update(body)
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Soyoung-Clinic-Tools-Appointment/2.2.2",
            "X-Request-Id": req_id,
        },
        method="POST",
    )
    _t0 = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body_bytes = resp.read()
        _last_elapsed_ms = (time.monotonic() - _t0) * 1000
        # json.loads 支持 bytes，无需显式 decode
        raw = json.loads(body_bytes)
        # 后端偶尔直接返回裸 list，统一包装成标准信封
        if isinstance(raw, list):
            return {"success": True, "data": raw}
        return raw
    except urllib.error.HTTPError as exc:
        _last_elapsed_ms = (time.monotonic() - _t0) * 1000
        code = exc.code
        if code == 401:
            return {"success": False, "error": "API Key 无效或已过期，请重新生成"}
        if code == 403:
            return {"success": False, "error": "无权限访问，请检查 API Key"}
        return {"success": False, "error": f"HTTP 错误：{code}"}
    except urllib.error.URLError as exc:
        _last_elapsed_ms = (time.monotonic() - _t0) * 1000
        if isinstance(exc.reason, (TimeoutError, socket.timeout)):
            return {"success": False, "error": "请求超时，请稍后重试"}
        return {"success": False, "error": "网络连接失败，请检查网络"}
    except (TimeoutError, socket.timeout):
        _last_elapsed_ms = (time.monotonic() - _t0) * 1000
        return {"success": False, "error": "请求超时，请稍后重试"}
    except Exception as exc:  # pragma: no cover - defensive
        _last_elapsed_ms = (time.monotonic() - _t0) * 1000
        return {"success": False, "error": f"请求失败：{str(exc)}"}


def store_list(city_name=None, api_key=None, paths=None, refresh=False):
    global _store_cache_hit
    _store_cache_hit = False
    if paths and not refresh:
        cached = _load_store_cache(paths, city_name)
        if cached is not None:
            _store_cache_hit = True
            return cached
    body = {}
    if city_name:
        body["city_name"] = city_name
    result = make_request("/booking/skill/query/store", body=body, api_key=api_key)
    if paths and result.get("success"):
        _save_store_cache(paths, city_name, result)
    return result


_SLICE_CACHE_TTL_SECS = 300


def _slice_cache_path(paths, hospital_id, date: str | None) -> Path:
    date_key = date if date else "_upcoming"
    return paths.workspace_dir / "cache" / "slice" / f"{hospital_id}_{date_key}.json"


def _load_slice_cache(paths, hospital_id, date: str | None) -> dict | None:
    cache_file = _slice_cache_path(paths, hospital_id, date)
    if not cache_file.exists():
        return None
    try:
        payload = json.loads(cache_file.read_text(encoding="utf-8"))
        if time.time() - payload.get("_ts", 0) < _SLICE_CACHE_TTL_SECS:
            return payload.get("result")
    except Exception:
        pass
    return None


def _save_slice_cache(paths, hospital_id, date: str | None, result: dict) -> None:
    cache_file = _slice_cache_path(paths, hospital_id, date)
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(
        json.dumps(
            {"_ts": time.time(), "result": result},
            ensure_ascii=False,
            separators=(",", ":"),
        ),
        encoding="utf-8",
    )


def appointment_slice(hospital_id, city_name=None, date=None, api_key=None, paths=None):
    if paths:
        cached = _load_slice_cache(paths, hospital_id, date)
        if cached is not None:
            return cached
    body = {"hospital_id": int(hospital_id)}
    if city_name:
        body["city_name"] = city_name
    if date:
        body["date"] = date
    result = make_request(
        "/booking/skill/query/booking_slice", body=body, api_key=api_key
    )
    if paths and result.get("success"):
        _save_slice_cache(paths, hospital_id, date, result)
    return result


def appointment_query(api_key=None):
    return make_request("/booking/skill/query/booking", api_key=api_key)


def appointment_create(hospital_id, start_time, end_time, api_key=None):
    body = {
        "hospital_id": int(hospital_id),
        "start_time": start_time,
        "end_time": end_time,
    }
    return make_request("/booking/skill/submit/booking", body=body, api_key=api_key)


def appointment_update(booking_id, hospital_id, start_time, end_time, api_key=None):
    body = {
        "booking_id": int(booking_id),
        "hospital_id": int(hospital_id),
        "start_time": start_time,
        "end_time": end_time,
    }
    return make_request("/booking/skill/modify/booking", body=body, api_key=api_key)


def appointment_cancel(booking_id, api_key=None):
    body = {"booking_id": int(booking_id)}
    return make_request("/booking/skill/cancel/booking", body=body, api_key=api_key)


def _index_entry_to_store(s: dict) -> dict:
    return {
        "机构ID": s["hospital_id"],
        "机构名称": s["name"],
        "机构地址": s.get("address", ""),
        "营业时间": "",
    }


def store_and_slice(
    store_name, city_name=None, date=None, api_key=None, paths=None, refresh=False
):
    def _fetch(store):
        r = appointment_slice(
            hospital_id=store.get("机构ID"),
            city_name=city_name,
            date=date,
            api_key=api_key,
            paths=paths,
        )
        return {"store": store, "slices": r.get("data", []) if r.get("success") else []}

    if paths and not refresh:
        index_result = store_lookup(store_name=store_name, paths=paths)
        if index_result.get("success"):
            indexed_stores = [
                _index_entry_to_store(s) for s in index_result.get("data", [])
            ]
            if indexed_stores:
                if len(indexed_stores) == 1:
                    return {"success": True, "data": _fetch(indexed_stores[0])}
                with ThreadPoolExecutor(
                    max_workers=min(len(indexed_stores), 4)
                ) as pool:
                    results = list(pool.map(_fetch, indexed_stores))
                return {"success": True, "data": results, "_multiple_match": True}

    stores_result = store_list(
        city_name=city_name, api_key=api_key, paths=paths, refresh=refresh
    )
    if not stores_result.get("success"):
        return stores_result

    stores = stores_result.get("data", [])
    name_lower = store_name.lower()
    matched = [s for s in stores if name_lower in s.get("机构名称", "").lower()]

    if not matched:
        return {
            "success": False,
            "error": (
                f'未找到名称包含"{store_name}"的门店。'
                f"请用 store_list 查看全部门店，或检查门店名称是否正确。"
            ),
        }

    if len(matched) == 1:
        return {"success": True, "data": _fetch(matched[0])}

    with ThreadPoolExecutor(max_workers=min(len(matched), 4)) as pool:
        results = list(pool.map(_fetch, matched))
    return {"success": True, "data": results, "_multiple_match": True}


def format_store_list(result):
    if not result.get("success"):
        return f"❌ **查询失败**：{result.get('error', '未知错误')}"
    stores = result.get("data", [])
    if not stores:
        return "🏥 **未找到门店**\n\n请尝试其他城市或位置"
    lines = ["🏥 **新氧门店列表**\n"]
    for i, store in enumerate(stores, 1):
        lines.append(
            f"**{i}. {store.get('机构名称', '未知')}**（ID: {store.get('机构ID', '')}）\n"
            f"📍 {store.get('机构地址', '未知')}  ⏰ {store.get('营业时间', '未知')}"
        )
    return "\n\n".join(lines)


def format_store_lookup(result):
    if not result.get("success"):
        return f"❌ **索引查询失败**：{result.get('error', '未知错误')}"
    stores = result.get("data", [])
    lines = [f"🗄️ **本地索引命中 {len(stores)} 家门店**\n"]
    for s in stores:
        lines.append(
            f"**{s.get('name', '未知')}**（ID: {s.get('hospital_id', '')}）\n"
            f"📍 {s.get('address', '未知')}  🏙️ {s.get('city', '未知')}"
        )
    return "\n\n".join(lines)


def _fmt_slices(slices: list) -> list[str]:
    """把切片数据渲染成行列表（供单店/多店复用）。"""
    lines = []
    for item in slices:
        date_str = (item.get("切片日期") or "")[:10]
        avail = item.get("剩余库存", 0)
        lines.append(f"📆 {date_str}（总{item.get('总库存', 0)} 剩{avail}）")
        for d in item.get("切片明细", []):
            if d.get("切片剩余库存", 0) > 0:
                lines.append(
                    f"  ✅ {d.get('切片开始时间', '')}—"
                    f"{d.get('切片结束时间', '')}（剩{d.get('切片剩余库存', 0)}）"
                )
    return lines


def format_store_and_slice(result):
    if not result.get("success"):
        return f"❌ **查询失败**：{result.get('error', '未知错误')}"
    data = result.get("data", {})

    if result.get("_multiple_match"):
        # data 是 [{store, slices}, ...] 列表，直接展示各家可约情况
        items = data if isinstance(data, list) else []
        lines = [f"🏥 找到 {len(items)} 家匹配门店：\n"]
        for item in items:
            store = item.get("store", {})
            lines.append(
                f"**{store.get('机构名称', '未知')}**（ID: {store.get('机构ID', '')}）\n"
                f"📍 {store.get('机构地址', '未知')}  ⏰ {store.get('营业时间', '未知')}"
            )
            slice_lines = _fmt_slices(item.get("slices", []))
            lines += slice_lines if slice_lines else ["📅 暂无可约时间"]
        return "\n\n".join(lines)

    store = data.get("store", {})
    slices = data.get("slices", [])
    lines = [
        f"🏥 **{store.get('机构名称', '未知')}**（ID: {store.get('机构ID', '')}）\n"
        f"📍 {store.get('机构地址', '未知')}  ⏰ {store.get('营业时间', '未知')}",
    ]
    slice_lines = _fmt_slices(slices)
    if not slice_lines:
        lines.append("📅 **暂无可约时间**，请稍后重试或选择其他门店")
    else:
        lines.append("📅 **可预约时间**")
        lines += slice_lines
    return "\n".join(lines)


def format_appointment_slice(result):
    if not result.get("success"):
        return f"❌ **查询失败**：{result.get('error', '未知错误')}"
    slices = result.get("data", [])
    if not slices:
        return "📅 **暂无可约时间**\n\n请稍后重试或选择其他门店"
    lines = ["📅 **可预约时间**"]
    lines += _fmt_slices(slices)
    return "\n".join(lines)


def format_appointment_record(result):
    if not result.get("success"):
        return f"❌ **查询失败**：{result.get('error', '未知错误')}"
    data = result.get("data")
    if not data:
        return "📋 **暂无预约记录**"
    date_groups = data if isinstance(data, list) else [data]
    lines = ["📋 **我的预约**\n"]
    for group in date_groups:
        date_label = group.get("日期名称", group.get("日期", ""))
        total = group.get("当天已预约总数", 0)
        lines.append(f"**{date_label}（{group.get('日期', '')}，共 {total} 条）**")
        for record in group.get("当天预约明细", []):
            lines.append(
                f"• #{record.get('预约ID', '?')}  🏥 {record.get('机构名称', '未知')}"
                f"  💉 {record.get('基础品名称', '未知')}\n"
                f"  ⏰ {record.get('预约开始时间', '')}—{record.get('预约结束时间', '')}"
            )
    return "\n".join(lines)


def _check_fail(result, action="操作"):
    if not result.get("success"):
        return f"❌ **{action}失败**：{result.get('error', '未知错误')}"
    data = result.get("data", result)
    if isinstance(data, dict) and data.get("失败原因"):
        return f"❌ **{action}失败**：{data.get('失败原因')}"
    return None


def format_appointment_create(result):
    err = _check_fail(result, "预约")
    if err:
        return err
    data = result.get("data", result)
    booking_id = data.get("预约ID", "未知") if isinstance(data, dict) else "未知"
    return f"✅ **预约成功！**\n\n📋 预约ID：{booking_id}\n\n> 请妥善保存预约ID，修改或取消时需要用到"


def format_appointment_update(result):
    err = _check_fail(result, "修改")
    if err:
        return err
    data = result.get("data", result)
    booking_id = data.get("预约ID", "未知") if isinstance(data, dict) else "未知"
    return f"✅ **预约已修改！**\n\n📋 预约ID：{booking_id}"


def format_appointment_cancel(result):
    err = _check_fail(result, "取消")
    if err:
        return err
    return "✅ **预约已取消**\n\n• 如需重新预约，请告诉我时间和门店"


def build_action_params(args) -> dict:
    if args.action == "appointment_query":
        return {}
    if args.action == "appointment_create":
        return {
            "hospital_id": args.hospital_id,
            "start_time": args.start_time,
            "end_time": args.end_time,
        }
    if args.action == "appointment_update":
        return {
            "booking_id": args.booking_id,
            "hospital_id": args.hospital_id,
            "start_time": args.start_time,
            "end_time": args.end_time,
        }
    if args.action == "appointment_cancel":
        return {"booking_id": args.booking_id}
    return {}


def run_action(
    action: str, params: dict, api_key: str, paths=None, refresh: bool = False
):
    if action == "store_lookup":
        if not paths:
            return {
                "success": False,
                "error": "store_lookup 需要 --workspace-key",
            }, format_store_lookup
        return store_lookup(
            store_name=params["store_name"], paths=paths
        ), format_store_lookup
    if action == "store_list":
        return store_list(
            city_name=params.get("city_name"),
            api_key=api_key,
            paths=paths,
            refresh=refresh,
        ), format_store_list
    if action == "store_and_slice":
        result = store_and_slice(
            store_name=params["store_name"],
            city_name=params.get("city_name"),
            date=params.get("date"),
            api_key=api_key,
            paths=paths,
            refresh=refresh,
        )
        return result, format_store_and_slice
    if action == "appointment_slice":
        return (
            appointment_slice(
                hospital_id=params["hospital_id"],
                city_name=params.get("city_name"),
                date=params.get("date"),
                api_key=api_key,
                paths=paths,
            ),
            format_appointment_slice,
        )
    if action == "appointment_query":
        return appointment_query(api_key=api_key), format_appointment_record
    if action == "appointment_create":
        return (
            appointment_create(
                hospital_id=params["hospital_id"],
                start_time=params["start_time"],
                end_time=params["end_time"],
                api_key=api_key,
            ),
            format_appointment_create,
        )
    if action == "appointment_update":
        return (
            appointment_update(
                booking_id=params["booking_id"],
                hospital_id=params["hospital_id"],
                start_time=params["start_time"],
                end_time=params["end_time"],
                api_key=api_key,
            ),
            format_appointment_update,
        )
    if action == "appointment_cancel":
        return appointment_cancel(
            booking_id=params["booking_id"], api_key=api_key
        ), format_appointment_cancel
    raise SoyoungRuntimeError(f"❌ 未知 action：{action}")


def print_result(result, formatter, *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(formatter(result) + _debug_footer())


def require_location_access(args, paths, binding):
    ctx = build_context_from_args(args, require=True)
    ensure_direct_message(ctx, "查看已保存位置")
    if not binding:
        raise SoyoungRuntimeError("❌ 当前 workspace 尚未绑定 API Key 主人。")
    ensure_owner(ctx, binding, "查看已保存位置")
    return ctx


def handle_approval(args, paths, binding):
    if not binding:
        raise SoyoungRuntimeError("❌ 当前 workspace 尚未绑定 API Key 主人。")
    ctx = build_context_from_args(args, require=True)
    request_id = args.request_id
    pending = resolve_pending_request(
        paths,
        owner_open_id=binding.get("ownerOpenId"),
        chat_id=ctx.chat_id,
        request_id=request_id,
    )

    if args.action == "approval_reject":
        pending = mark_pending_rejected(paths, pending=pending, ctx=ctx)
        print(
            f"🛑 已拒绝审批单 #{pending.get('requestId')}\n\n• 操作：{pending.get('previewText')}"
        )
        return

    api_key = load_api_key(paths, args.api_key)
    if not api_key:
        raise SoyoungRuntimeError("❌ 未找到 API Key，请先由主人在私聊中重新配置。")

    pending = mark_pending_consumed(paths, pending=pending, ctx=ctx)

    if pending["action"] == "appointment_create":
        p = pending.get("params", {})
        start = p.get("start_time", "")
        check_create_rate_limit(
            paths,
            sender_open_id=pending.get("requestedByOpenId") or ctx.sender_open_id,
            hospital_id=p.get("hospital_id"),
            date_str=start[:10] if start else None,
        )

    result, formatter = run_action(
        pending["action"], pending.get("params", {}), api_key, paths=paths
    )
    audit_event(
        paths,
        "protected_action_executed",
        {
            "requestId": pending.get("requestId"),
            "action": pending.get("action"),
            "chatId": pending.get("chatId"),
            "approvedByOpenId": ctx.sender_open_id,
            "success": bool(result.get("success", True)),
        },
    )
    if args.json:
        print(
            json.dumps(
                {"approval": pending, "result": result}, ensure_ascii=False, indent=2
            )
        )
    else:
        print(f"✅ 已收到主人确认，开始执行审批单 #{pending.get('requestId')}\n")
        print(formatter(result))


def main():
    import argparse

    global _script_start
    _script_start = time.monotonic()
    parser = argparse.ArgumentParser(description="appointment")
    parser.add_argument(
        "--action",
        choices=[
            "store_lookup",
            "store_list",
            "store_and_slice",
            "appointment_slice",
            "appointment_query",
            "appointment_create",
            "appointment_update",
            "appointment_cancel",
            "approval_confirm",
            "approval_reject",
        ],
    )
    parser.add_argument("--workspace-key")
    parser.add_argument("--chat-type")
    parser.add_argument("--chat-id")
    parser.add_argument("--message-id")
    parser.add_argument("--sender-open-id")
    parser.add_argument("--sender-name")
    parser.add_argument("--tenant-key")
    parser.add_argument("--mention-open-id", action="append", default=[])
    parser.add_argument("--city_name", "--city-name", dest="city_name")
    parser.add_argument("--store_name", "--store-name", dest="store_name")
    parser.add_argument("--hospital_id", "--hospital-id", dest="hospital_id")
    parser.add_argument("--date")
    parser.add_argument("--start_time", "--start-time", dest="start_time")
    parser.add_argument("--end_time", "--end-time", dest="end_time")
    parser.add_argument("--booking_id", "--booking-id", dest="booking_id")
    parser.add_argument("--request-id")
    parser.add_argument("--api-key")
    parser.add_argument("--get-location", action="store_true")
    parser.add_argument(
        "--refresh", action="store_true", help="忽略门店列表缓存，强制从接口重新拉取"
    )
    parser.add_argument("--json", action="store_true")
    # 捕获已知幻觉参数，给出明确提示而非 argparse 通用错误
    parser.add_argument(
        "--project-name",
        "--project_name",
        "--project",
        dest="_phantom_project",
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args()

    if getattr(args, "_phantom_project", None):
        print(
            "❌ appointment 脚本不接受 --project-name / --project 参数。\n"
            "• 预约切片固定只返回预约面诊，无需传项目参数\n"
            "• 项目/价格查询请调用 skills/project 脚本（--action project_search --content 水光）"
        )
        sys.exit(1)

    try:
        paths = get_state_paths(args.workspace_key)
        global SOYOUNG_DEBUG, API_BASE_URL
        SOYOUNG_DEBUG = read_debug_mode(paths)
        API_BASE_URL = read_api_base_url(paths)
        binding = load_binding(paths)

        if args.get_location:
            require_location_access(args, paths, binding)
            location = load_location(paths)
            if args.json:
                print(
                    json.dumps(
                        location or {"error": "尚未保存位置，请由主人在私聊中保存"},
                        ensure_ascii=False,
                        indent=2,
                    )
                )
            elif location:
                parts = [location.get("city", "")]
                if location.get("district"):
                    parts.append(location["district"])
                if location.get("street"):
                    parts.append(location["street"])
                print(
                    f"📍 已保存位置：{' '.join([part for part in parts if part])}\n"
                    f"🕐 更新时间：{location.get('updatedAt', '')}"
                )
            else:
                print("⚠️ 尚未保存位置信息\n\n请由主人在私聊中说「我在 XX 市 XX 区」")
            return

        if not args.action:
            parser.print_help()
            return

        if args.action in {"approval_confirm", "approval_reject"}:
            handle_approval(args, paths, binding)
            return

        # store_lookup 只查本地索引，不需要 API Key，提前处理
        if args.action == "store_lookup":
            if not args.store_name:
                print("❌ 缺少 --store_name")
                return
            result, formatter = run_action(
                "store_lookup", {"store_name": args.store_name}, api_key="", paths=paths
            )
            print_result(result, formatter, as_json=args.json)
            return

        api_key = load_api_key(paths, args.api_key)
        if not api_key:
            print(
                "❌ 未找到 API Key\n\n"
                "请先由主人在私聊中说：「配置新氧 API Key 为 xxx」\n"
                "（群聊绝不能发送 API Key）"
            )
            sys.exit(1)

        params = build_action_params(args)
        if args.action == "store_list":
            params = {"city_name": args.city_name}
        elif args.action == "store_and_slice":
            if not args.store_name:
                print("❌ 缺少 --store_name")
                return
            params = {
                "store_name": args.store_name,
                "city_name": args.city_name,
                "date": args.date,
            }
        elif args.action == "appointment_slice":
            if not args.hospital_id:
                if args.store_name:
                    # AI 传了 store_name 却忘了 hospital_id，自动路由到 store_and_slice
                    args.action = "store_and_slice"
                    params = {
                        "store_name": args.store_name,
                        "city_name": args.city_name,
                        "date": args.date,
                    }
                else:
                    print(
                        "❌ 缺少 --hospital_id（或用 --action store_and_slice --store_name 门店名 直接按名称查询）"
                    )
                    return
            else:
                params = {
                    "hospital_id": args.hospital_id,
                    "city_name": args.city_name,
                    "date": args.date,
                }
        elif args.action == "appointment_create":
            if not args.hospital_id or not args.start_time or not args.end_time:
                print("❌ 缺少 --hospital_id、--start_time 或 --end_time")
                return
            _validate_datetime(args.start_time, "--start_time")
            _validate_datetime(args.end_time, "--end_time")
        elif args.action == "appointment_update":
            if (
                not args.booking_id
                or not args.hospital_id
                or not args.start_time
                or not args.end_time
            ):
                print("❌ 缺少 --booking_id、--hospital_id、--start_time 或 --end_time")
                return
            _validate_datetime(args.start_time, "--start_time")
            _validate_datetime(args.end_time, "--end_time")
        elif args.action == "appointment_cancel":
            if not args.booking_id:
                print("❌ 缺少 --booking_id")
                return

        ctx = None
        if args.action in PROTECTED_APPOINTMENT_ACTIONS:
            ctx = build_context_from_args(args, require=True)
            decision = authorize_protected_action(
                paths,
                ctx=ctx,
                binding=binding,
                action=args.action,
                params=params,
            )
            if decision["type"] == "need_approval":
                print(format_pending_prompt(decision["pending"]))
                return

        if args.action == "appointment_create" and ctx:
            check_create_rate_limit(
                paths,
                sender_open_id=ctx.sender_open_id,
                hospital_id=params.get("hospital_id"),
                date_str=params.get("start_time", "")[:10] or None,
            )

        result, formatter = run_action(
            args.action, params, api_key, paths=paths, refresh=args.refresh
        )
        # 只对写操作记审计日志，只读门店/切片查询不落盘
        if args.action not in {"store_list", "store_and_slice", "appointment_slice"}:
            audit_event(
                paths,
                "appointment_action_executed",
                {
                    "action": args.action,
                    "chatId": ctx.chat_id if ctx else None,
                    "senderOpenId": ctx.sender_open_id if ctx else None,
                    "success": bool(result.get("success", True)),
                },
            )
        print_result(result, formatter, as_json=args.json)
    except SoyoungRuntimeError as exc:
        print(str(exc))


if __name__ == "__main__":
    main()
