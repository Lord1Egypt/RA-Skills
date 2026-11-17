"""library.py — 图书馆综合查询子 SKILL 统一入口

整合清华大学图书馆多个子系统：
- seat.lib（座位）：实时余量（公开）+ 座位分布（公开）+ 我的预约记录（登录）
- cab.lib（研读间/研讨间）：空间占用状态（登录，走内部 API /ic-web/）

用法:
  library.py seat [--area 北馆]      # 座位余量（公开，无需登录）
  library.py areas [--area 北馆]     # 座位分布：馆→楼层→区域→总/不可用/剩余（公开）
  library.py my-bookings            # 我的座位预约记录（需登录）
  library.py rooms [--space 北馆团体研讨间（二层）]  # 研读间占用状态（需登录，API）

cab 内部 API（逆向，base=https://cab.lib.tsinghua.edu.cn/ic-web/）:
  查询: roomMenu(公开) / roomDevice/roomInfos / home/page/room/idle / seatDevice/resvStatus
  预约: POST reserve | reserve/bulkAdd; 改约 reserve/update; 取消 reserve/endReserve
  登录: CAS SSO（auth/address → CAS；登录态靠 cookie）
"""
import sys
import os
import json
import time
import re
import argparse
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "shared", "scripts"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "base-cas", "scripts"))
import common
import browser
import login

SEAT_URL = "https://seat.lib.tsinghua.edu.cn"
CAB_URL = "https://cab.lib.tsinghua.edu.cn"

# 馆区 id 映射
SEAT_AREAS = {
    "35": "北馆(李文正馆)", "64": "西馆(逸夫馆)", "89": "文科图书馆",
    "6": "法律图书馆", "19": "美术图书馆", "29": "金融图书馆",
}

# 研读间空间列表（cab）
CAB_SPACES = [
    "北馆单人研读间（三层）",
    "北馆团体研讨间（二层）",
    "西馆高山音乐研讨间（中208）",
    "西馆流水音乐研讨间（中210）",
    "文科馆单人研读间（三层）",
    "文科馆团体研讨间（二层）",
    "法律馆单人研读间（四层）",
    "法律馆研讨舱（四层、五层)",
    "法律馆双人舱（五层)",
]


# ---------- seat 余量 ----------
def _parse_seat_areas(page):
    return page.evaluate("""() => {
        const out = [];
        document.querySelectorAll('div.rooms').forEach(r => {
            const b = [...r.querySelectorAll('div.ceng.nowap.zh b')].map(x => (x.innerText||'').trim());
            const img = r.querySelector('img[src*="area/"]');
            let area_id = '';
            if (img) {
                const m = (img.getAttribute('src')||'').match(/area\\/(\\d+)/);
                if (m) area_id = m[1];
            }
            if (b.length >= 2) {
                const m = b[1].match(/今日剩余(\\d+)，总量(\\d+)/);
                out.push({name: b[0], area_id, remaining: m ? parseInt(m[1]) : null, total: m ? parseInt(m[2]) : null});
            }
        });
        return out;
    }""")


def cmd_seat(area_filter=""):
    browser.start_cdp(headed=False)
    pw, b, ctx, page = browser.connect_cdp()
    page.on("dialog", lambda d: d.accept())
    try:
        page.goto(SEAT_URL + "/home/web/f_second", wait_until="domcontentloaded", timeout=30000)
        time.sleep(8)
        areas = _parse_seat_areas(page)
        if not areas:
            common.output_json({"status": "error", "message": "未解析到座位数据"})
            sys.exit(1)
        if area_filter:
            areas = [a for a in areas if area_filter in a["name"]]
        common.output_json({"status": "ok", "type": "seat", "areas": areas})
    finally:
        try:
            browser.stop_cdp()
        except Exception:
            pass


def _fetch_v3areas(area_id):
    """公开 API 查馆区楼层/区域分布。"""
    try:
        r = urllib.request.urlopen(f"{SEAT_URL}/api.php/v3areas/{area_id}", timeout=15)
        d = json.loads(r.read().decode("utf-8"))
    except Exception:
        return None
    if d.get("status") != 1:
        return None
    data = d["data"]["list"]
    ai = data["areaInfo"]
    floors = []
    for f in data.get("childArea", []):
        total = f.get("TotalCount", 0) or 0
        un = f.get("UnavailableSpace", 0) or 0
        regions = []
        # 区域子节点（若有）
        if f.get("id") and f.get("id") != ai.get("id"):
            pass
        item = {"floor": f.get("name"), "id": f.get("id"),
                "total": total, "unavailable": un, "remaining": total - un}
        if total == 0:
            item["note"] = "0 为接口占位，不代表无座，请以 seat 实时余量为准"
        floors.append(item)
    return {"name": ai.get("name"), "id": ai.get("id"), "floors": floors}


def cmd_areas(area_filter=""):
    """座位分布：馆→楼层→区域→总/不可用/剩余（公开 API，无需登录）。"""
    ids = list(SEAT_AREAS.keys())
    if area_filter:
        ids = [aid for aid, name in SEAT_AREAS.items() if area_filter in name]
        if not ids:
            common.output_json({"status": "ok", "message": f"未找到馆区 {area_filter}", "areas": []})
            sys.exit(0)
    result = []
    for aid in ids:
        info = _fetch_v3areas(aid)
        if info:
            result.append(info)
    common.output_json({"status": "ok", "type": "areas", "areas": result})


# ---------- seat 我的预约 ----------
def _parse_my_bookings(page):
    return page.evaluate("""() => {
        const out = {bookings: []};
        document.querySelectorAll('table').forEach(t => {
            const rows = [...t.querySelectorAll('tr')].map(tr =>
                [...tr.querySelectorAll('td,th')].map(td => (td.innerText||'').trim()));
            if (rows.length > 1 && rows[0].join('|').includes('预约号')) {
                rows.slice(1).forEach(r => {
                    if (r.length >= 6 && r[0]) out.bookings.push({
                        no: r[0], space: r[1], start: r[2], end: r[3], status: r[4]
                    });
                });
            }
        });
        return out;
    }""")


def cmd_my_bookings():
    user = login._get_cred("cas_username")
    pwd = login._get_cred("cas_password")
    if not user or not pwd:
        common.output_json({"status": "error", "message": "CAS 凭据未配置"})
        sys.exit(1)
    browser.start_cdp(headed=False)
    pw, b, ctx, page = browser.connect_cdp()
    page.on("dialog", lambda d: d.accept())
    try:
        if not _seat_login(page, user, pwd, ctx):
            common.output_json({"status": "error", "message": "座位系统登录失败"})
            sys.exit(1)
        common.log("[library] seat 登录成功")
        page.goto(SEAT_URL + "/user/index/book", wait_until="domcontentloaded", timeout=30000)
        time.sleep(8)
        data = _parse_my_bookings(page)
        common.output_json({"status": "ok", "type": "my_bookings", **data})
    finally:
        try:
            browser.stop_cdp()
        except Exception:
            pass


# ---------- cab 研读间 ----------
def _cab_login(page, user, pwd):
    """cab 登录（Vue SPA，iframe CAS）。

    注意：cab 是 Vue SPA，body 在 Vue 挂载前为空。不能复用 _iframe_cas_login
    （它只检查"无 CAS 文案"会误判登录成功）。需等待 Vue ready：
      - 已登录（信任浏览器）→ body 出现"个人中心"
      - 未登录 → Vue 注入 CAS iframe → 填表
    """
    return login.ensure_iframe_cas(
        "cab", page, page.context,
        home_url=CAB_URL,
        logged_in_check="() => !!document.body && document.body.innerText.includes('个人中心')",
    )


def _click_space(page, space_name):
    """真实点击空间（Vue SPA 路由跳转）。"""
    try:
        page.click(f"text={space_name}", timeout=8000)
        return True
    except Exception:
        pass
    try:
        page.click(f"text={space_name}（三层）", timeout=5000)
        return True
    except Exception:
        return False


def _cab_api(page, path, method="GET", params=None):
    """调用 cab 内部 API（/ic-web/...），带登录态 cookie。

    在页面上下文用 fetch（自动带 cookie + hiddenReferer）。返回解析后的 dict。
    """
    return page.evaluate("""async (args) => {
        const {path, method, params} = args;
        const opt = {method: method, credentials: 'include',
                     headers: {'X-Requested-With': 'XMLHttpRequest',
                               'Content-Type': 'application/json; charset=UTF-8'}};
        if (method === 'GET' && params) {
            const qs = new URLSearchParams(params).toString();
            const r = await fetch('/ic-web/' + path + (qs ? '?' + qs : ''), opt);
            return await r.text();
        }
        if (params) opt.body = JSON.stringify(params);
        const r = await fetch('/ic-web/' + path, opt);
        return await r.text();
    }""", {"path": path, "method": method, "params": params or {}})


def _cab_roommenu(page):
    """获取研读间/研讨间空间列表（公开接口）。返回 [{kindId, kindName}]。"""
    raw = _cab_api(page, "roomMenu")
    try:
        d = json.loads(raw)
    except Exception:
        return []
    if d.get("code") != 0:
        return []
    return [{"kindId": x.get("kindId"), "kindName": x.get("kindName")} for x in (d.get("data") or [])]


def _cab_walk_roominfos(node, out):
    """递归遍历 roomDevice/roomInfos 响应，提取 [{kindName, roomInfos:[...]}]。

    实测结构：data=[{kindName, roomInfos:[{devId, devName, minResvTime,
        openTimes:[{openStartTime,openEndTime}], resvInfos:[{resvBeginTime,
        resvEndTime,resvStatus,trueName}]}]}]
    """
    if isinstance(node, dict):
        ris = node.get("roomInfos")
        if isinstance(ris, list) and ris and isinstance(ris[0], dict) and "devId" in ris[0]:
            out.append({"kindName": node.get("kindName") or node.get("name") or "",
                        "rooms": ris})
        for v in node.values():
            _cab_walk_roominfos(v, out)
    elif isinstance(node, list):
        for v in node:
            _cab_walk_roominfos(v, out)


def _cab_room_status(page, space_name, date=None):
    """查某空间某天的房间占用（reserve GET 接口，含预约人脱敏姓名）。

    实测：GET /ic-web/reserve?sysKind=1&resvDates=YYYYMMDD&page=1&pageSize=N&kindIds=<kindId>&labId=
    → data=[{devId, devName, kindName, labName, openStart, openEnd, resvRule, resvInfo:[{
        title, trueName(脱敏 张*嘉), logonName(脱敏 2***3), startTime(epoch ms),
        endTime, resvStatus, resvId}]}]

    返回 (kind, rooms, raw)。
    """
    import datetime
    menu = _cab_roommenu(page)
    kind = None
    for m in menu:
        if space_name and (space_name in m["kindName"] or m["kindName"] in space_name):
            kind = m
            break
    if kind is None and menu:
        kind = menu[0]
    day = date or datetime.datetime.now().strftime("%Y%m%d")
    raw = _cab_api(page, "reserve", params={
        "sysKind": 1, "resvDates": day, "page": 1, "pageSize": 30,
        "kindIds": (kind or {}).get("kindId", ""), "labId": "",
    })
    try:
        d = json.loads(raw)
    except Exception:
        return kind, [], raw
    if d.get("code") != 0:
        return kind, [], raw

    def _ts(ms):
        try:
            return datetime.datetime.fromtimestamp(int(ms) / 1000).strftime("%Y-%m-%d %H:%M")
        except Exception:
            return str(ms)

    rooms = []
    for r in (d.get("data") or []):
        resv = []
        for ri in (r.get("resvInfo") or []):
            resv.append({
                "who": ri.get("trueName") or "",       # 脱敏姓名（系统默认 张*嘉）
                "account": ri.get("logonName") or "",   # 脱敏学号
                "uuid": ri.get("uuid") or "",
                "resvId": ri.get("resvId"),
                "title": ri.get("title") or "",
                "start": _ts(ri.get("startTime")),
                "end": _ts(ri.get("endTime")),
                "status": _decode_resv_status(ri.get("resvStatus")),
                "status_raw": ri.get("resvStatus"),
            })
        rooms.append({
            "room": r.get("devName"),
            "devId": r.get("devId"),
            "group": r.get("kindName"),
            "lab": r.get("labName"),
            "open": f"{r.get('openStart','')}-{r.get('openEnd','')}",
            "min_resv_min": (r.get("resvRule") or {}).get("minResvTime"),
            "max_resv_min": (r.get("resvRule") or {}).get("maxResvTime"),
            "resv": resv,
        })
    return kind, rooms, raw


# resvStatus 位掩码（来自 SPA statusOption 注释）
_RESV_STATUS = {2: "待生效", 4: "已生效/使用中", 16: "已违约", 128: "已结束",
                256: "待审核", 512: "审核未通过", 1024: "审核通过", 2048: "已暂离"}


def _decode_resv_status(s):
    if s is None:
        return "?"
    names = [v for k, v in _RESV_STATUS.items() if s & k]
    return "|".join(names) if names else str(s)


def _cab_my_info(page):
    """当前登录用户信息（accNo/trueName/学号）。"""
    try:
        d = json.loads(_cab_api(page, "auth/userInfo"))
        if d.get("code") == 0:
            return d.get("data") or {}
    except Exception:
        pass
    return {}


def _cab_resolve_members(page, names):
    """姓名列表 → [{name, accNo, logonName, dept}]（account/getMembers?key=）。"""
    out = []
    for nm in names:
        nm = nm.strip()
        if not nm:
            continue
        try:
            d = json.loads(_cab_api(page, "account/getMembers",
                                    params={"key": nm, "page": 1, "pageNum": 10}))
        except Exception:
            d = {}
        hits = d.get("data") or []
        if hits:
            h = hits[0]
            out.append({"name": nm, "accNo": h.get("accNo"),
                        "logonName": h.get("logonName"), "dept": h.get("deptName"),
                        "matched": len(hits)})
        else:
            out.append({"name": nm, "accNo": None, "error": "未找到"})
    return out


def _cab_find_free_room(page, kind_id, date, start, end, room_filter=""):
    """在 kindId 空间下找 date 日 [start,end] 全空闲的房间。返回 (room_dict, all_rooms)。

    room_filter：只考虑房名包含该串的房间（如 "F2-29"）。
    """
    d = json.loads(_cab_api(page, "reserve", params={
        "sysKind": 1, "resvDates": date, "page": 1, "pageSize": 50,
        "kindIds": kind_id, "labId": "",
    }))
    if d.get("code") != 0:
        return None, []
    import datetime as _dt
    all_rooms = []
    for r in (d.get("data") or []):
        if room_filter and room_filter not in (r.get("devName") or ""):
            continue
        occ = []
        for ri in (r.get("resvInfo") or []):
            s = _dt.datetime.fromtimestamp(ri["startTime"] / 1000)
            e = _dt.datetime.fromtimestamp(ri["endTime"] / 1000)
            occ.append((s, e))
        info = {"room": r.get("devName"), "devId": r.get("devId"),
                "minUser": r.get("minUser"), "maxUser": r.get("maxUser"),
                "occupied": [(x.strftime("%H:%M"), y.strftime("%H:%M")) for x, y in occ]}
        all_rooms.append(info)
        ds = _dt.datetime.strptime(f"{date} {start}", "%Y%m%d %H:%M")
        de = _dt.datetime.strptime(f"{date} {end}", "%Y%m%d %H:%M")
        blocked = any(s < de and e > ds for s, e in occ)
        if not blocked:
            return info, all_rooms
    return None, all_rooms


def cmd_book_room(space_filter="", date=None, start="", end="", members="", title="", confirm=False, room_filter=""):
    """预约团体研讨间（写操作，需 --confirm）。

    流程：登录 → 解析空间 kindId → 找 [start,end] 空闲房间 → 解析成员 accNo
         → POST /ic-web/reserve/bulkAdd。
    不带 --confirm 时仅 dry-run（展示将预约的房间/成员/时间，不提交）。
    """
    import datetime
    user = login._get_cred("cas_username")
    pwd = login._get_cred("cas_password")
    if not user or not pwd:
        common.output_json({"status": "error", "message": "CAS 凭据未配置"})
        sys.exit(1)
    if not (date and start and end):
        common.output_json({"status": "error", "message": "需要 --date YYYYMMDD --start HH:MM --end HH:MM"})
        sys.exit(1)
    member_names = [m.strip() for m in members.split(",") if m.strip()]
    if not member_names:
        common.output_json({"status": "error", "message": "需要 --members 姓名1,姓名2,..."})
        sys.exit(1)

    browser.start_cdp(headed=False)
    pw, b, ctx, page = browser.connect_cdp()
    page.on("dialog", lambda d: d.accept())
    try:
        if not _cab_login(page, user, pwd):
            common.output_json({"status": "error", "message": "研读间系统登录失败"})
            sys.exit(1)
        me = _cab_my_info(page)
        space = space_filter or "北馆团体研讨间（二层）"
        menu = _cab_roommenu(page)
        kind = next((m for m in menu if space in m["kindName"] or m["kindName"] in space), None)
        if not kind:
            common.output_json({"status": "error", "message": f"未找到空间 {space}", "spaces": menu})
            sys.exit(1)
        room, all_rooms = _cab_find_free_room(page, kind["kindId"], date, start, end, room_filter)
        resolved = _cab_resolve_members(page, member_names)
        missing = [r["name"] for r in resolved if not r.get("accNo")]
        plan = {
            "space": kind, "date": date, "start": start, "end": end,
            "room": room, "members": resolved,
            "requester": {"name": me.get("trueName"), "accNo": me.get("accNo")},
        }
        if missing:
            common.output_json({"status": "error", "message": f"成员未找到: {missing}", "plan": plan})
            sys.exit(1)
        if not room:
            common.output_json({"status": "error", "message": f"{space} 在 {date} {start}-{end} 无空闲房间",
                                "plan": plan, "all_rooms": all_rooms})
            sys.exit(1)
        if not confirm:
            common.output_json({"status": "ok", "type": "book_room_dry_run",
                                "message": "dry-run：加 --confirm 才提交", "plan": plan})
            return
        # 提交
        acc_list = [me.get("accNo")] + [r["accNo"] for r in resolved if r["accNo"] != me.get("accNo")]
        payload = {
            "resvBeginTime": f"{date[:4]}-{date[4:6]}-{date[6:]} {start}:00",
            "resvEndTime": f"{date[:4]}-{date[4:6]}-{date[6:]} {end}:00",
            "sysKind": 1, "appAccNo": me.get("accNo"),
            "memberKind": 2 if len(acc_list) > 1 else 1,
            "testName": title or "", "resvKind": 2, "resvProperty": 32,
            "appUrl": "", "resvMember": acc_list, "resvDev": [room["devId"]],
            "memo": "", "captcha": "", "addServices": [],
        }
        r = json.loads(_cab_api(page, "reserve", method="POST", params=payload))
        common.output_json({"status": "ok" if r.get("code") == 0 else "error",
                            "type": "book_room", "submitted": payload, "response": r})
    finally:
        try:
            browser.stop_cdp()
        except Exception:
            pass


def cmd_cancel_room(uuid="", confirm=False):
    """取消研讨间预约（写操作，需 --confirm）。

    端点：POST /ic-web/reserve/delete，body {"uuid": "<预约uuid>"}。
    uuid 从 `rooms` 输出的 resv[].uuid 获取。
    """
    if not uuid:
        common.output_json({"status": "error", "message": "需要 --uuid <预约uuid>（见 rooms 输出的 resv[].uuid）"})
        sys.exit(1)
    user = login._get_cred("cas_username")
    pwd = login._get_cred("cas_password")
    if not user or not pwd:
        common.output_json({"status": "error", "message": "CAS 凭据未配置"})
        sys.exit(1)
    if not confirm:
        common.output_json({"status": "ok", "type": "cancel_room_dry_run",
                            "message": "dry-run：加 --confirm 才取消", "uuid": uuid})
        return
    browser.start_cdp(headed=False)
    pw, b, ctx, page = browser.connect_cdp()
    page.on("dialog", lambda d: d.accept())
    try:
        if not _cab_login(page, user, pwd):
            common.output_json({"status": "error", "message": "研读间系统登录失败"})
            sys.exit(1)
        r = json.loads(_cab_api(page, "reserve/delete", method="POST", params={"uuid": uuid}))
        common.output_json({"status": "ok" if r.get("code") == 0 else "error",
                            "type": "cancel_room", "uuid": uuid, "response": r})
    finally:
        try:
            browser.stop_cdp()
        except Exception:
            pass


def _hm2m(s):
    h, mi = s.split(":")
    return int(h) * 60 + int(mi)

def _m2hm(m):
    return f"{m//60:02d}:{m%60:02d}"


def cmd_free(date=None, min_hours=4, space_filter="", as_csv=False,
             room_filter="", min_user=0, free_start="", free_end="", free_after=""):
    """列出各空间房间的【空闲时段】（占用 dump + 空闲窗口分析）。

    date 默认今天；min_hours 过滤出可连续预约 ≥N 小时的窗口（默认 4）。
    as_csv=True 输出 CSV（便于后续分析/Excel）。
    筛选：room_filter 房名含该串；min_user 容量≥N（maxUser）；free_start/free_end
         只保留覆盖 [free_start,free_end] 的窗口；free_after 只保留起点≥该时间的窗口。
    """
    import datetime
    user = login._get_cred("cas_username")
    pwd = login._get_cred("cas_password")
    if not user or not pwd:
        common.output_json({"status": "error", "message": "CAS 凭据未配置"})
        sys.exit(1)
    browser.start_cdp(headed=False)
    pw, b, ctx, page = browser.connect_cdp()
    page.on("dialog", lambda d: d.accept())
    try:
        if not _cab_login(page, user, pwd):
            common.output_json({"status": "error", "message": "研读间系统登录失败"})
            sys.exit(1)
        day = date or datetime.datetime.now().strftime("%Y%m%d")
        menu = _cab_roommenu(page)
        spaces_out = []
        for sp in menu:
            if space_filter and space_filter not in sp["kindName"]:
                continue
            data = None
            for _attempt in range(4):
                try:
                    r = json.loads(_cab_api(page, "reserve", params={
                        "sysKind": 1, "resvDates": day, "page": 1, "pageSize": 50,
                        "kindIds": sp["kindId"], "labId": "",
                    }))
                except Exception:
                    r = {"code": -1}
                if r.get("code") == 0:
                    data = r.get("data") or []
                    break
                time.sleep(1.5)
            if data is None:
                spaces_out.append({"space": sp["kindName"], "error": "查询失败"})
                continue
            rooms_out = []
            for room in data:
                if room_filter and room_filter not in (room.get("devName") or ""):
                    continue
                if min_user and (room.get("maxUser") or 0) < min_user:
                    continue
                open_m = _hm2m(room.get("openStart") or "08:00")
                close_m = _hm2m(room.get("openEnd") or "22:00")
                occ = []
                for ri in (room.get("resvInfo") or []):
                    s = datetime.datetime.fromtimestamp(ri["startTime"] / 1000)
                    e = datetime.datetime.fromtimestamp(ri["endTime"] / 1000)
                    occ.append((_hm2m(s.strftime("%H:%M")), _hm2m(e.strftime("%H:%M"))))
                occ.sort()
                # 空闲窗口 = 开放时段 − 占用
                free = []
                cur = open_m
                for s, e in occ:
                    if s > cur:
                        free.append((cur, s))
                    cur = max(cur, e)
                if cur < close_m:
                    free.append((cur, close_m))
                free_h = [(a, b) for a, b in free if b - a >= min_hours * 60]
                # 额外筛选：覆盖 [free_start,free_end] / 起点≥free_after
                if free_start or free_end or free_after:
                    need_a = _hm2m(free_start) if free_start else None
                    need_b = _hm2m(free_end or free_start) if (free_start or free_end) else None
                    after_m = _hm2m(free_after) if free_after else None

                    def _ok(win):
                        a, b = win
                        if need_a is not None and not (a <= need_a and b >= need_b):
                            return False
                        if after_m is not None and a < after_m:
                            return False
                        return True
                    free_h = [w for w in free_h if _ok(w)]
                rooms_out.append({
                    "room": room.get("devName"), "devId": room.get("devId"),
                    "open": f"{_m2hm(open_m)}-{_m2hm(close_m)}",
                    "minUser": room.get("minUser"), "maxUser": room.get("maxUser"),
                    "booked": [{"start": _m2hm(s), "end": _m2hm(e)} for s, e in occ],
                    "free_ge_min": [{"start": _m2hm(a), "end": _m2hm(b), "hours": round((b - a) / 60, 1)}
                                    for a, b in free_h],
                })
            spaces_out.append({"space": sp["kindName"], "kindId": sp["kindId"], "rooms": rooms_out})
        if as_csv:
            import csv as _csv
            import io as _io
            buf = _io.StringIO()
            w = _csv.writer(buf)
            w.writerow(["space", "room", "devId", "minUser", "maxUser", "open",
                        "booked", "free_ge_minh"])
            for sp in spaces_out:
                if sp.get("error"):
                    w.writerow([sp["space"], "", "", "", "", "", "", ""]); continue
                for r in sp.get("rooms", []):
                    booked = ";".join(f"{x['start']}-{x['end']}" for x in (r.get("booked") or []))
                    freeg = ";".join(f"{x['start']}-{x['end']}" for x in (r.get("free_ge_min") or []))
                    w.writerow([sp["space"], r.get("room"), r.get("devId"), r.get("minUser"),
                                r.get("maxUser"), r.get("open"), booked, freeg])
            sys.stdout.write(buf.getvalue())
            return
        common.output_json({"status": "ok", "type": "free", "date": day,
                            "min_hours": min_hours, "spaces": spaces_out})
    finally:
        try:
            browser.stop_cdp()
        except Exception:
            pass


def cmd_rooms(space_filter="", date=None, as_csv=False):
    user = login._get_cred("cas_username")
    pwd = login._get_cred("cas_password")
    if not user or not pwd:
        common.output_json({"status": "error", "message": "CAS 凭据未配置"})
        sys.exit(1)
    browser.start_cdp(headed=False)
    pw, b, ctx, page = browser.connect_cdp()
    page.on("dialog", lambda d: d.accept())
    try:
        if not _cab_login(page, user, pwd):
            common.output_json({"status": "error", "message": "研读间系统登录失败"})
            sys.exit(1)
        common.log("[library] cab 登录成功")
        space = space_filter or "北馆团体研讨间（二层）"
        kind, rooms, raw = _cab_room_status(page, space, date)
        if not rooms:
            common.output_json({"status": "error", "message": f"未获取到房间状态（空间={space}）",
                                "kind": kind, "raw_head": (raw or "")[:400]})
            sys.exit(1)
        if as_csv:
            import csv as _csv, io as _io
            buf = _io.StringIO()
            w = _csv.writer(buf)
            w.writerow(["space", "room", "devId", "open", "who", "account", "uuid", "resvId", "start", "end", "status", "status_raw"])
            for r in rooms:
                for v in (r.get("resv") or []):
                    w.writerow([r.get("group"), r.get("room"), r.get("devId"), r.get("open"),
                                v.get("who"), v.get("account"), v.get("uuid"), v.get("resvId"),
                                v.get("start"), v.get("end"),
                                v.get("status"), v.get("status_raw")])
            sys.stdout.write(buf.getvalue())
            return
        common.output_json({"status": "ok", "type": "rooms", "space": kind,
                            "date": date or "today",
                            "room_count": len(rooms), "rooms": rooms})
    finally:
        try:
            browser.stop_cdp()
        except Exception:
            pass


# ---------- 座位预约（book/cancel）----------
def _seat_login(page, user, pwd, context=None):
    """座位系统登录 —— 走 base-cas 的 iframe CAS 会话复用（cookie 有效则免登录）。

    cookie 快照存 base-cas session（runtime/sessions/seat.json），跨进程复用；
    失效才 fallback 到 iframe CAS 填表。
    """
    return login.ensure_iframe_cas(
        "seat", page, context or page.context,
        home_url=SEAT_URL + "/home/web/f_second",
        trigger_js="() => { const a = document.querySelector('a.login_click'); if (a) a.click(); }",
    )


def _seat_lookup(page, area_id, day="today"):
    """查馆区楼层/区域树。返回楼层/区域列表。"""
    d = page.evaluate("""async (aid) => {
        const r = await fetch('/api.php/v3areas/' + aid, {credentials: 'include'});
        return await r.json();
    }""", area_id)
    if not d or d.get("status") != 1:
        return []
    data = d["data"]["list"]
    floors = []
    for f in data.get("childArea", []):
        total = f.get("TotalCount", 0) or 0
        un = f.get("UnavailableSpace", 0) or 0
        item = {"id": f.get("id"), "name": f.get("name"), "total": total,
                "unavailable": un, "remaining": total - un}
        if total == 0:
            item["note"] = "0 为接口占位，不代表无座，请以 seat 实时余量为准"
        floors.append(item)
    return floors


def _seat_time_buckets(page, area_id, day):
    """查某区域可预约时间段。返回时段列表（segment id + start/end）。"""
    d = page.evaluate("""async (args) => {
        const r = await fetch('/api.php/space_time_buckets?area=' + args.area + '&day=' + args.day, {credentials: 'include'});
        return await r.json();
    }""", {"area": area_id, "day": day})
    if not d or d.get("status") != 1:
        return []
    lst = d["data"]["list"] or []
    out = []
    for item in lst:
        seg = item.get("id") or item.get("bookTimeId")
        if seg:
            out.append({"segment": seg, "spaceName": item.get("spaceName"),
                        "startTime": item.get("startTime"), "endTime": item.get("endTime"),
                        "status": item.get("status")})
    return out


def _seat_spaces(page, area_id, segment, day, start, end):
    """查某时段可选座位列表（spaces_old）。"""
    d = page.evaluate("""async (args) => {
        const q = 'area=' + args.area + '&segment=' + args.segment + '&day=' + args.day
                + '&startTime=' + args.start + '&endTime=' + args.end;
        const r = await fetch('/api.php/spaces_old?' + q, {credentials: 'include'});
        return await r.json();
    }""", {"area": area_id, "segment": segment, "day": day, "start": start, "end": end})
    if not d or d.get("status") != 1:
        return []
    lst = d["data"]["list"] or []
    out = []
    for item in lst:
        out.append({"id": item.get("id"), "no": item.get("no"),
                    "status": item.get("status"),
                    "x": item.get("point_x"), "y": item.get("point_y")})
    return out


SEAT_STATUS = {1: "可选", 2: "已预约", 6: "使用中", 7: "暂离", 3: "关闭", 4: "关闭", 5: "关闭"}

# 座位系统开放窗口：每日 6:00-23:00（可预约当日/次日）
OPEN_START_HOUR = 6
OPEN_END_HOUR = 23


def _check_open_hours(now=None):
    """校验当前是否在座位系统开放窗口（6:00-23:00）。

    窗口外 → 返回说明文字（调用方应直接报错退出，不启动浏览器/不登录）；
    窗口内 → 返回 None。
    now 可注入用于单测。
    """
    import datetime
    now = now or datetime.datetime.now()
    hour = now.hour
    if hour < OPEN_START_HOUR or hour >= OPEN_END_HOUR:
        return (f"座位系统开放时间为每日 6:00-23:00（可预约当日/次日座位），"
                f"当前 {now.strftime('%H:%M')} 不在开放窗口内，无法预约。"
                f"请 {OPEN_START_HOUR}:00 后再试（届时可预约当日或次日座位）。")
    return None


def cmd_book(area_filter="", floor_filter="", region_filter="", seat_no="", confirm=False):
    """座位查找 + 预约。

    流程：
      1. 登录 seat
      2. 查馆区楼层/区域树（v3areas）
      3. 若指定区域 → 查时间段（space_time_buckets）→ 查可选座位（spaces_old）
      4. 若指定座位 → 预约（需 --confirm 才真正执行；否则仅预览）

    ⚠️ 写操作保护：预约是真实写操作，必须带 --confirm 才执行。AI 应先在对话里
    向用户 double check（座位号/时间段/规则提醒），用户确认后再带 --confirm 执行。
    """
    # 开放窗口校验：窗口外直接报错退出，不启动浏览器/不登录
    early = _check_open_hours()
    if early:
        common.output_json({"status": "error", "type": "book_out_of_window", "message": early})
        sys.exit(1)
    user = login._get_cred("cas_username")
    pwd = login._get_cred("cas_password")
    if not user or not pwd:
        common.output_json({"status": "error", "message": "CAS 凭据未配置"})
        sys.exit(1)
    browser.start_cdp(headed=False)
    pw, b, ctx, page = browser.connect_cdp()
    page.on("dialog", lambda d: d.accept())
    page.set_viewport_size({"width": 1280, "height": 900})
    try:
        if not _seat_login(page, user, pwd):
            common.output_json({"status": "error", "message": "座位系统登录失败"})
            sys.exit(1)
        common.log("[library] seat 登录成功")
        import datetime
        day = datetime.date.today().strftime("%Y-%m-%d")
        # 1. 查馆区
        area_id = None
        for aid, name in SEAT_AREAS.items():
            if not area_filter or area_filter in name:
                area_id = aid
                break
        if not area_id:
            common.output_json({"status": "error", "message": f"未找到馆区 {area_filter}"})
            sys.exit(1)
        floors = _seat_lookup(page, area_id)
        if not floors:
            common.output_json({"status": "error", "message": "馆区无楼层数据"})
            sys.exit(1)
        # 2. 选楼层 → 区域
        floor_id = None
        if floor_filter:
            for f in floors:
                if floor_filter in f["name"]:
                    floor_id = f["id"]
                    break
        # 若未指定楼层，输出分布并结束
        if not floor_id:
            common.output_json({"status": "ok", "type": "book_floors",
                                "area": SEAT_AREAS[area_id], "area_id": area_id,
                                "floors": floors,
                                "message": "请指定 --floor 楼层继续（如 --floor 二层）"})
            sys.exit(0)
        # 查楼层的区域（v3areas/<floor_id>）
        fd = page.evaluate("""async (fid) => {
            const r = await fetch('/api.php/v3areas/' + fid, {credentials: 'include'});
            return await r.json();
        }""", floor_id)
        regions = []
        if fd and fd.get("status") == 1 and fd["data"]["list"].get("childArea"):
            for r in fd["data"]["list"]["childArea"]:
                total = r.get("TotalCount", 0) or 0
                un = r.get("UnavailableSpace", 0) or 0
                regions.append({"id": r.get("id"), "name": r.get("name"),
                                "total": total, "unavailable": un, "remaining": total - un})
        # 选区域
        region_id = None
        if region_filter:
            for r in regions:
                if region_filter in r["name"]:
                    region_id = r["id"]
                    break
        if not region_id:
            common.output_json({"status": "ok", "type": "book_regions",
                                "area": SEAT_AREAS[area_id], "floor": floor_filter,
                                "regions": regions,
                                "message": "请指定 --region 区域（如 --region A）"})
            sys.exit(0)
        # 3. 查时间段
        segments = _seat_time_buckets(page, region_id, day)
        if not segments:
            common.output_json({"status": "ok", "type": "book_segments",
                                "region": region_filter, "segments": [],
                                "message": "该区域当前无可用时间段（当日可约时段已过或该区域今日不可约）。可改选其他区域/楼层（用 library.py areas 查分布），或次日 6:00 后预约当日座位。"})
            sys.exit(0)
        seg = segments[0]
        # 4. 查可选座位
        spaces = _seat_spaces(page, region_id, seg["segment"], day, seg["startTime"], seg["endTime"])
        avail = [s for s in spaces if s["status"] == 1]
        if not seat_no:
            common.output_json({"status": "ok", "type": "book_seats",
                                "region": region_filter, "segment": seg,
                                "total": len(spaces), "available": avail,
                                "message": "可选座位如上，请指定 --seat NF2A001 预约"})
            sys.exit(0)
        # 5. 预约指定座位
        target = None
        for s in spaces:
            if s["no"] == seat_no or str(s["id"]) == seat_no:
                target = s
                break
        if not target:
            common.output_json({"status": "error", "message": f"未找到座位 {seat_no}"})
            sys.exit(1)
        if target["status"] != 1:
            common.output_json({"status": "error", "message": f"座位 {seat_no} 不可预约（状态 {SEAT_STATUS.get(target['status'])}）"})
            sys.exit(1)
        # ⚠️ 写操作确认门禁：必须带 --confirm 才真正预约
        if not confirm:
            common.output_json({
                "status": "ok", "type": "book_preview",
                "action": "book",
                "seat": seat_no, "spaceId": target["id"],
                "segment": seg["segment"],
                "day": day, "startTime": seg["startTime"], "endTime": seg["endTime"],
                "remind": "预约是写操作。请先向用户 double check：确认预约该座位和时间段？并提醒：预约后 30 分钟内必须到场签到（未签到释放座位+记违规1次）；取消预约每日限1次；违规满5次暂停3天。用户确认后，带 --confirm 重新执行。",
                "confirm_required": True,
            })
            sys.exit(0)
        # 直接调 book API（比 DOM 点击更稳）
        d = page.evaluate("""async (args) => {
            const form = new URLSearchParams();
            form.append('access_token', ska.access_token);
            form.append('userid', ska.userid);
            form.append('segment', args.segment);
            form.append('type', '1');
            form.append('operateChannel', '2');
            const r = await fetch('/api.php/spaces/' + args.spaceId + '/book', {
                method: 'POST', credentials: 'include',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: form.toString()
            });
            return await r.json();
        }""", {"spaceId": target["id"], "segment": seg["segment"]})
        common.output_json({"status": "ok", "type": "book_result",
                            "seat": seat_no, "spaceId": target["id"],
                            "segment": seg["segment"],
                            "day": day, "startTime": seg["startTime"], "endTime": seg["endTime"],
                            "book_response": d,
                            "remind": "预约成功后 30 分钟内必须到场签到（未签到释放座位+记违规1次）；取消预约每日限1次；违规满5次暂停3天。请提醒用户确认时间安排。"})
    finally:
        try:
            browser.stop_cdp()
        except Exception:
            pass


def cmd_cancel(booking_id="", userid="", access_token="", confirm=False):
    """取消座位预约。

    参数：--id 预约 id（我的预约列表里的预约号或内部 id）。
    若不指定 id → 列出当前有效预约。
    ⚠️ 写操作保护：取消是真实写操作（且取消每日限 1 次），必须带 --confirm 才执行；
    否则仅预览将取消的预约。AI 应先在对话里向用户 double check。
    """
    user = login._get_cred("cas_username")
    pwd = login._get_cred("cas_password")
    if not user or not pwd:
        common.output_json({"status": "error", "message": "CAS 凭据未配置"})
        sys.exit(1)
    browser.start_cdp(headed=False)
    pw, b, ctx, page = browser.connect_cdp()
    page.on("dialog", lambda d: d.accept())
    page.set_viewport_size({"width": 1280, "height": 900})
    try:
        if not _seat_login(page, user, pwd):
            common.output_json({"status": "error", "message": "座位系统登录失败"})
            sys.exit(1)
        common.log("[library] seat 登录成功")
        # 我的预约列表
        page.goto(SEAT_URL + "/user/index/book", wait_until="domcontentloaded", timeout=30000)
        time.sleep(8)
        # 找可取消的预约（含"取消"按钮，状态为预约成功/提醒）
        rows = page.evaluate("""() => {
            const out = [];
            document.querySelectorAll('tr').forEach(tr => {
                const tds = [...tr.querySelectorAll('td')].map(td => (td.innerText||'').trim());
                if (tds.length >= 5 && /^\\d{12}$/.test(tds[0])) {
                    const del = tr.querySelector('a[onclick*="menuDel"]');
                    out.push({
                        no: tds[0], space: tds[1], start: tds[2], end: tds[3], status: tds[4],
                        cancelId: del ? (del.getAttribute('onclick').match(/\\d+/g)||[]).pop() : null
                    });
                }
            });
            return out;
        }""")
        cancellable = [r for r in rows if r["cancelId"]]
        if not booking_id:
            common.output_json({"status": "ok", "type": "cancel_list",
                                "bookings": rows, "cancellable": cancellable,
                                "message": "请指定 --id <预约内部id> 取消（cancellable 里的 cancelId）"})
            sys.exit(0)
        # 取消指定预约
        # 参数可能是预约号或 cancelId
        cancel_id = booking_id
        for r in rows:
            if r["no"] == booking_id:
                cancel_id = r["cancelId"]
                break
        if not cancel_id:
            common.output_json({"status": "error", "message": f"未找到可取消的预约 {booking_id}"})
            sys.exit(1)
        # 从页面 JS 提取 access_token + userid（我的预约页无 ska，token 在 menuDel 硬编码）
        token = page.evaluate("""() => {
            const scripts = [...document.querySelectorAll('script')].map(s => s.textContent || '').join('');
            const m = scripts.match(/access_token['":\\s]+([a-f0-9]{32})/i);
            const u = scripts.match(/userid['":\\s]+([0-9]{8,10})/i);
            return {token: m ? m[1] : '', userid: u ? u[1] : ''};
        }""")
        if not token.get("token"):
            common.output_json({"status": "error", "message": "无法获取 access_token（我的预约页无 token）"})
            sys.exit(1)
        uid = token["userid"] or "2025013187"
        # ⚠️ 写操作确认门禁：必须带 --confirm 才真正取消
        if not confirm:
            common.output_json({
                "status": "ok", "type": "cancel_preview",
                "action": "cancel",
                "booking": booking_id, "cancel_id": cancel_id,
                "remind": "取消是写操作，且【取消预约每日限1次】。请先向用户 double check：确认取消该预约？用户确认后，带 --confirm 重新执行。",
                "confirm_required": True,
            })
            sys.exit(0)
        d = page.evaluate("""async (args) => {
            const form = new URLSearchParams();
            form.append('_method', 'delete');
            form.append('id', args.id);
            form.append('userid', args.userid);
            form.append('access_token', args.token);
            form.append('operateChannel', '2');
            const r = await fetch('/api.php/profile/books/' + args.id, {
                method: 'POST', credentials: 'include',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: form.toString()
            });
            return await r.json();
        }""", {"id": cancel_id, "userid": uid, "token": token["token"]})
        common.output_json({"status": "ok", "type": "cancel_result",
                            "booking": booking_id, "cancel_id": cancel_id,
                            "cancel_response": d})
    finally:
        try:
            browser.stop_cdp()
        except Exception:
            pass


def main():
    ap = argparse.ArgumentParser(description="图书馆综合查询")
    ap.add_argument("cmd", choices=["seat", "areas", "my-bookings", "rooms", "free", "book", "book-room", "cancel", "cancel-room"])
    ap.add_argument("--area", default="", help="seat/areas/book: 馆区筛选")
    ap.add_argument("--floor", default="", help="book: 楼层筛选")
    ap.add_argument("--region", default="", help="book: 区域筛选")
    ap.add_argument("--seat", default="", help="book: 座位号（如 NF2A001）")
    ap.add_argument("--id", default="", help="cancel: 预约内部id")
    ap.add_argument("--space", default="", help="rooms/book-room: 研读间空间名")
    ap.add_argument("--date", default="", help="rooms/book-room: 日期 YYYYMMDD（默认今天）")
    ap.add_argument("--start", default="", help="book-room: 开始时间 HH:MM")
    ap.add_argument("--end", default="", help="book-room: 结束时间 HH:MM")
    ap.add_argument("--members", default="", help="book-room: 成员姓名，逗号分隔（含预约人）")
    ap.add_argument("--title", default="", help="book-room: 主题（可选）")
    ap.add_argument("--min-hours", type=float, default=4, help="free: 只列出可连续预约 ≥N 小时的空闲窗口（默认 4）")
    ap.add_argument("--csv", action="store_true", help="rooms/free: 输出 CSV（便于分析/Excel）")
    ap.add_argument("--room", default="", help="book-room/free: 房间名关键词（如 F2-29）")
    ap.add_argument("--uuid", default="", help="cancel-room: 预约 uuid（见 rooms 输出的 resv[].uuid）")
    ap.add_argument("--min-user", type=int, default=0, help="free: 只保留容量（maxUser）≥N 的房间")
    ap.add_argument("--free-start", default="", help="free: 只保留覆盖该起始时刻的窗口 HH:MM")
    ap.add_argument("--free-end", default="", help="free: 配合 --free-start，覆盖到该时刻")
    ap.add_argument("--free-after", default="", help="free: 只保留起点 ≥ 该时刻的窗口 HH:MM")
    ap.add_argument("--confirm", action="store_true", help="book/book-room/cancel: 确认执行写操作。不带则仅预览。")
    args = ap.parse_args()
    if args.cmd == "seat":
        cmd_seat(args.area)
    elif args.cmd == "areas":
        cmd_areas(args.area)
    elif args.cmd == "my-bookings":
        cmd_my_bookings()
    elif args.cmd == "rooms":
        cmd_rooms(args.space, args.date or None, args.csv)
    elif args.cmd == "free":
        cmd_free(args.date or None, args.min_hours, args.space, args.csv,
                 args.room, args.min_user, args.free_start, args.free_end, args.free_after)
    elif args.cmd == "book-room":
        cmd_book_room(args.space, args.date or None, args.start, args.end, args.members, args.title, args.confirm, args.room)
    elif args.cmd == "cancel-room":
        cmd_cancel_room(args.uuid, args.confirm)
    elif args.cmd == "book":
        cmd_book(args.area, args.floor, args.region, args.seat, args.confirm)
    elif args.cmd == "cancel":
        cmd_cancel(args.id, confirm=args.confirm)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        common.log(f"[library] 未捕获异常: {e}")
        common.output_json({"status": "error", "error": "unexpected", "message": f"脚本异常: {str(e)[:200]}"})
        sys.exit(1)
