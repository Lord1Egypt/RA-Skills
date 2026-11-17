#!/usr/bin/env python3
# wb_travel.py —— WorkBuddy「派猫猫旅行」闭环(零 GUI 依赖, 标准库实现)
# ============================================================================
# 功能(2026-09-29 新增, 接口逆向自 totorosir-workbuddy-score 文档并实测):
#   1. 只读展示旅行状态(默认): idle 空闲 / traveling 旅行中(含到达倒计时) /
#      arrived 已到达可领积分
#   2. --auto 全自动闭环(写操作, 先领后派):
#        查状态 -> arrived 则 claim 领取 -> 重查 -> idle 且未达每日上限则 depart 派出
#      安全约束: 派出前必查 daily_limit_reached, 达上限绝不发写请求;
#               到达后状态保持 arrived 不丢积分, 下次运行自动补领。
#   3. --location N 指定派遣地点(1=咖啡馆 2=商场店铺 3=健身房 4=古镇客栈,
#      缺省随机; 四地时长与积分区间相同, 收益无差异)
#
# 接口(host=https://www.workbuddy.cn, 注意不带 /v2 前缀, 仅需 Bearer Token):
#   GET  /activity/growth/buddy/travel/status   旅行状态
#   GET  /activity/growth/buddy/travel/config   可选地点配置
#   POST /activity/growth/buddy/travel/claim    领取到达奖励 body={}
#   POST /activity/growth/buddy/travel/depart   派出 body={"location_id":N}
#
# 用法:
#   python wb_travel.py            # 只读状态展示
#   python wb_travel.py --auto     # 全自动闭环(先领后派)
#   python wb_travel.py --auto --location 1
#   python wb_travel.py --json     # 机器可读输出(不触发写操作)
#
# 退出码: 0=成功/只读正常  2=失败(token 缺失/接口异常)
#
# 【隐私与安全】凭据仅本地读取、不打印不落盘不外传; 写操作仅限上述
#   claim/depart 两个已验证接口, 且 depart 受 --auto + 上限双重保护。
# ============================================================================

import argparse
import json
import os
import random
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wb_api_checkin import get_token  # 同目录复用鉴权(含 5.6.2+ 解密兼容)

TRAVEL_BASE = "https://www.workbuddy.cn"
STATUS_PATH = "/activity/growth/buddy/travel/status"
CONFIG_PATH = "/activity/growth/buddy/travel/config"
CLAIM_PATH = "/activity/growth/buddy/travel/claim"
DEPART_PATH = "/activity/growth/buddy/travel/depart"
TIMEOUT = 15
# travel 接口不校验 UA(totorosir 实测默认 python UA 可通), 与 billing 接口不同
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) wb-travel/1.0"
STATE_TEXT = {"idle": "空闲(可派出)", "traveling": "旅行中", "arrived": "已到达(待领取)"}


def _call(path, token, method="GET", payload=None):
    """调 travel 接口。返回 (http_status, body_dict)。"""
    if payload is not None:
        body = json.dumps(payload).encode()
    else:
        body = json.dumps({}).encode() if method == "POST" else None
    req = urllib.request.Request(TRAVEL_BASE + path, data=body, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", UA)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status, json.loads(r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode("utf-8", "replace"))
        except Exception:
            return e.code, {"code": -1, "msg": "HTTP %s" % e.code}
    except Exception as e:
        return 0, {"code": -1, "msg": str(e)}


def _get(path, token):
    """只读 GET, 失败返回 None(静默降级)。"""
    st, body = _call(path, token, method="GET")
    if st == 200 and isinstance(body, dict) and body.get("code") == 0:
        return body.get("data")
    return None


def _fmt_duration(sec):
    if sec is None:
        return "?"
    sec = int(sec)
    h, rem = divmod(sec, 3600)
    m = rem // 60
    return ("%d 小时 %d 分" % (h, m)) if h else ("%d 分钟" % m if m else "%d 秒" % sec)


def travel_claim(token):
    """领取到达奖励(写)。返回 dict: success/reward/message。"""
    st, body = _call(CLAIM_PATH, token, method="POST", payload={})
    if st == 200 and isinstance(body, dict) and body.get("code") == 0:
        credit = (body.get("data") or {}).get("reward_credit")
        return {"success": True, "action": "claimed", "reward_credit": credit,
                "message": "✅ 旅行奖励已领取 +%s 积分" % (credit if credit is not None else "?")}
    msg = body.get("msg") if isinstance(body, dict) else None
    return {"success": False, "action": "failed", "code": body.get("code") if isinstance(body, dict) else None,
            "message": "❌ 领取失败: %s" % (msg or ("HTTP %s" % st))}


def travel_depart(token, location_id=None, locations=None):
    """派出(写)。location_id 为空则从可选地点随机。调用方须已确认未达上限。"""
    chosen = location_id
    if chosen is None:
        ids = [loc.get("id") for loc in (locations or []) if isinstance(loc, dict) and loc.get("id") is not None]
        if not ids:
            return {"success": False, "action": "failed", "message": "❌ 未能获取可选地点列表, 跳过派遣"}
        chosen = random.choice(ids)
    st, body = _call(DEPART_PATH, token, method="POST", payload={"location_id": chosen})
    if st == 200 and isinstance(body, dict) and body.get("code") == 0:
        data = body.get("data") or {}
        loc = data.get("location") or {}
        arrive = data.get("arrive_at")
        dur = ""
        if isinstance(arrive, int):
            dur = ", 预计 %s 后到达" % _fmt_duration(arrive - int(time.time()))
        return {"success": True, "action": "departed", "location_id": chosen,
                "message": "🚀 已派出猫猫前往【%s】%s" % (loc.get("name") or ("地点 %s" % chosen), dur)}
    msg = body.get("msg") if isinstance(body, dict) else None
    return {"success": False, "action": "failed", "code": body.get("code") if isinstance(body, dict) else None,
            "message": "❌ 派遣失败(地点 %s): %s" % (chosen, msg or ("HTTP %s" % st))}


def travel_auto(token, location_id=None):
    """全自动闭环(写): 先领后派。返回 (final_status, log_list)。"""
    log = []
    status = _get(STATUS_PATH, token)
    if status is None:
        return None, ["查询旅行状态失败, 已跳过全部写操作"]

    if status.get("state") == "arrived":
        r = travel_claim(token)
        log.append(r["message"])
        if r.get("action") == "claimed":
            fresh = _get(STATUS_PATH, token)
            if fresh is not None:
                status = fresh

    if status.get("daily_limit_reached"):
        log.append("今日派遣次数已用完, 跳过派遣")
    elif status.get("state") in (None, "", "idle"):
        config = _get(CONFIG_PATH, token) or {}
        r = travel_depart(token, location_id, config.get("locations") or [])
        log.append(r["message"])
        if r.get("action") == "departed":
            fresh = _get(STATUS_PATH, token)
            if fresh is not None:
                status = fresh
    else:
        log.append("猫猫正在旅行中, 无需派遣")

    return status, log


def describe(status, log=None):
    """把旅行状态 + 自动日志转成人类可读播报。"""
    if not isinstance(status, dict):
        lines = ["🐾 猫猫旅行: 状态不可用"]
    else:
        state = status.get("state")
        lines = ["🐾 猫猫旅行: %s" % STATE_TEXT.get(state, state or "未知")]
        loc = status.get("location") or {}
        if loc.get("name"):
            lines.append("   地点: %s" % loc["name"])
        if state == "traveling" and isinstance(status.get("arrive_at"), int) \
                and isinstance(status.get("server_now"), int):
            rem = max(0, status["arrive_at"] - status["server_now"])
            lines.append("   到达倒计时: %s" % _fmt_duration(rem))
        if state == "arrived" and status.get("reward_credit") is not None:
            lines.append("   可领积分: %s" % status["reward_credit"])
        if status.get("daily_limit_reached"):
            lines.append("   今日派遣: 已达上限")
    if log:
        lines.append("   自动执行: " + "; ".join(log))
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="WorkBuddy 派猫猫旅行")
    ap.add_argument("--auto", action="store_true", help="全自动闭环(先领后派, 写操作)")
    ap.add_argument("--location", type=int, default=None,
                    help="派遣地点 id(1=咖啡馆 2=商场 3=健身房 4=客栈), 缺省随机")
    ap.add_argument("--json", action="store_true", help="机器可读 JSON 输出")
    ns = ap.parse_args()

    token, src = get_token()
    if not token:
        print("ERROR: 未取得可用 accessToken(见 wb_api_checkin.py 鉴权说明)。")
        return 2

    if ns.auto:
        status, log = travel_auto(token, ns.location)
        if status is None and log:
            print(log[0])
            return 2
        out = {"mode": "auto", "log": log, "status": status}
        if ns.json:
            print(json.dumps(out, ensure_ascii=False))
        else:
            print(describe(status, log))
        return 0

    # 默认只读
    status = _get(STATUS_PATH, token)
    if ns.json:
        print(json.dumps({"mode": "status", "status": status}, ensure_ascii=False))
        return 0 if status is not None else 2
    if status is None:
        print("❌ 查询旅行状态失败(接口异常或未登录)")
        return 2
    print(describe(status))
    return 0


if __name__ == "__main__":
    sys.exit(main())
