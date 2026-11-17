#!/usr/bin/env python3
"""ARI CLI for the amazon-supplier-feedback Skill.

Uses only Python's standard library. Paid collection and AI analysis commands
require an explicit --confirm flag after a free preview/quote.
"""

import argparse
import getpass
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor


# VERSION 必须与 _meta.json 的 version 一致：它进 User-Agent，服务端据此统计版本分布
# 并判定最低支持版本。发版时两处一起改。
VERSION = "1.5.3"
# CHANNEL 标记分发渠道（不同市场 listing），由打包脚本按变体烙入；官方母版为空串。
# 非空时 User-Agent 追加 " ch/<渠道>"，服务端据此统计各渠道的注册与用量。
CHANNEL = "supplier-feedback"
PROD_BASE = "https://ari.funewa.com"
TIMEOUT_SEC = 120
# SSE 分析在 meta 事件之后、LLM 首 token 之前可能长时间静默（推理模型可达数分钟）。
# urlopen 的 timeout 是「单次 read 拿不到数据」的上限，若沿用 120s，会在服务端已经
# 扣点并归档之后把一次成功的分析误报成网络错误，进而诱导重试 → 二次扣点。
SSE_TIMEOUT_SEC = 600
SITES = ("amz_us", "amz_uk", "amz_de", "amz_jp", "amz_ca", "amz_fr", "amz_es", "amz_it")
WATCH_SCHEDULES = ("daily", "weekly", "monthly")  # 商品监控刷新频率，每次刷新按频率扣点
ANALYSIS_TYPES =("voc", "keywords", "insight", "trend", "variant", "compare")
SSE_TYPES = ("voc", "keywords", "insight", "compare")  # 走 text/event-stream 的分析类型
MIN_ANALYSIS_REVIEWS = 10
# 轮询时值得重试的错误：瞬时故障不应中止一次已经冻结积点的采集等待。
RETRYABLE_CODES = ("NETWORK_ERROR", "HTTP_ERROR", "ARI_RATE_LIMITED",
                   "ARI_INTERNAL_ERROR", "ARI_UPSTREAM_ERROR")
_exit_code = 0
# 服务端在每个 API Key 响应上广播最新版本，任意一条命令都能顺带发现有新版，
# 不必等用户想起来跑 check。
_release = {"latest": "", "url": ""}

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass


class EndpointBlocked(ValueError):
    """Local security failure; never include an untrusted URL or credentials."""

    code = "ARI_ENDPOINT_BLOCKED"


class RedirectBlocked(EndpointBlocked):
    code = "ARI_REDIRECT_BLOCKED"


def validate_official_url(url):
    """Exact HTTPS origin, including authority syntax; TLS verifies the hostname."""
    if not isinstance(url, str) or any(ord(c) <= 32 or ord(c) == 127 for c in url) or "\\" in url:
        raise EndpointBlocked()
    try:
        parsed = urllib.parse.urlsplit(url)
        if (parsed.scheme != "https" or
                parsed.netloc.lower() not in ("ari.funewa.com", "ari.funewa.com:443") or
                parsed.hostname != "ari.funewa.com" or parsed.port not in (None, 443) or
                parsed.username is not None or parsed.password is not None or parsed.fragment):
            raise EndpointBlocked()
    except ValueError:
        raise EndpointBlocked() from None
    return parsed


def base_url():
    """Production builds do not support custom endpoints, even with the old opt-in."""
    override = os.environ.get("ARI_BASE_URL")
    if override:
        parsed = validate_official_url(override)
        if parsed.path not in ("", "/") or parsed.query or "?" in override or "#" in override:
            raise EndpointBlocked()
    return PROD_BASE


def web_root():
    """Account, billing and report links always use the official website."""
    return PROD_BASE


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        # Reject before parsing Location, copying headers, or issuing another request.
        fp.close()
        raise RedirectBlocked()

    http_error_301 = http_error_303 = http_error_307 = http_error_308 = http_error_302


def api_request(method, path, payload=None, params=None, accept="application/json", authenticated=True):
    """Validate the final destination before reading any API key."""
    if not isinstance(path, str) or not path.startswith("/api/v1/") or "?" in path or "#" in path:
        raise EndpointBlocked()
    url = base_url() + path
    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True)
    validate_official_url(url)
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Accept": accept, "User-Agent": user_agent()}
    if data is not None:
        headers["Content-Type"] = "application/json"
    if authenticated:
        headers["Authorization"] = "Bearer " + require_key()
    return urllib.request.Request(url, data=data, headers=headers, method=method)


def open_api(req, timeout):
    validate_official_url(req.full_url)
    # A private opener avoids globally installed redirect handlers. Default HTTPS
    # certificate/hostname verification is retained; do not install an insecure context.
    return urllib.request.build_opener(NoRedirect()).open(req, timeout=timeout)


def endpoint_error(exc):
    return error_obj(exc.code, 0, "安全策略已阻止非官方地址或重定向",
                     "仅支持 https://ari.funewa.com。清除自定义 ARI_BASE_URL；"
                     "ARI_ALLOW_CUSTOM_BASE 不再生效。若官方请求发生跳转，请联系 ARI 支持。")


def user_agent():
    """版本号后随渠道尾巴（若有）。服务端按第一个空格截断取版本。"""
    ua = "ARI-Review-Skill/" + VERSION
    return ua + " ch/" + CHANNEL if CHANNEL else ua


def links():
    root = web_root()
    return {
        "apiKeys": root + "/zh/account?ui=d47626f#api-keys",
        "billing": root + "/zh/billing",
        "products": root + "/zh/products",
        "reports": root + "/zh/reports",
        "dashboard": root + "/zh/dashboard",
        "notify": root + "/zh/account#notify",
        "monitor": root + "/zh/monitor",
    }


def product_url(asin, site):
    """网页产品页深链：带 asin 会自动定位/预填该产品（开监控、补采、生成报告都在这一页）。"""
    from urllib.parse import quote
    return "%s/zh/products?asin=%s&site=%s" % (web_root(), quote((asin or "").upper()), quote(site or "amz_us"))


def report_url(rid):
    """单份报告的网页深链（图表版 / 导出入口）。from=skill 供网页侧归因。"""
    try:
        rid = int(rid)
    except (TypeError, ValueError):
        return None
    if rid <= 0:
        return None
    return "%s/zh/reports/%d?from=skill" % (web_root(), rid)


def attach_report_urls(out):
    """给 /api/v1/reports 信封的每行补 reportUrl。原样返回 out 便于串联。"""
    data = data_of(out)
    if ok(out) and isinstance(data, dict):
        for r in data.get("reports") or []:
            if isinstance(r, dict) and r.get("id"):
                r["reportUrl"] = report_url(r["id"])
    return out


def config_path():
    return os.path.expanduser("~/.ari/config.json")


def resolve_key():
    """Key 只从 ARI_API_KEY 或用户配置目录读取。

    刻意不回退到 Skill 包目录：那个位置会随 Skill 一起被打包、复制或提交，
    与「Key 只保存在本机用户配置中」的承诺相悖。
    """
    key = os.environ.get("ARI_API_KEY", "").strip()
    if not key:
        path = config_path()
        if os.path.exists(path):
            try:
                with open(path, encoding="utf-8") as fh:
                    key = (json.load(fh).get("api_key") or "").strip()
            except (OSError, json.JSONDecodeError):
                key = ""
    # configure/setup 写入前都校验过前缀，这里再拦一道：环境变量或手工编辑过的
    # 配置文件里放了残缺 Key 时，与其让每个请求 401，不如本地直接说清楚。
    if key and not key.startswith("ari_live_"):
        emit(error_obj(
            "ARI_API_KEY_INVALID_FORMAT", 0,
            "已配置的 Key 不是 ari_live_ 开头，可能残缺或被改动过",
            "运行 python ari.py setup 重新授权，或 configure 重新粘贴完整 Key。"))
        raise SystemExit(2)
    return key or None


def require_key():
    key = resolve_key()
    if key:
        return key
    emit(error_obj(
        "ARI_API_KEY_MISSING", 0,
        "未找到 ARI API Key",
        "推荐运行 python ari.py setup 浏览器一键授权；也可 configure 手动粘贴或设置 ARI_API_KEY。",
    ))
    raise SystemExit(2)


def error_obj(code, status, message, hint="", query=None, partial=None):
    out = {
        "success": False,
        "error": {"code": code, "status": status, "message": message, "hint": hint},
        "links": links(),
    }
    if query is not None:
        out["_query"] = query
    if partial:
        out["partial"] = partial
    return out


def version_tuple(v):
    out = []
    for part in str(v or "").split("."):
        try:
            out.append(int(part.strip()))
        except ValueError:
            out.append(0)
    return tuple(out)


def version_cmp(a, b):
    """比较点分版本号，返回 -1/0/1。与服务端 compareVersions 同语义。

    段数不同时短的补 0：裸用元组比较会把 1.0 判成早于 1.0.0（前缀更短即更小），
    从而对已是最新版的用户反复弹升级提示。
    """
    at, bt = version_tuple(a), version_tuple(b)
    n = max(len(at), len(bt))
    at += (0,) * (n - len(at))
    bt += (0,) * (n - len(bt))
    return (at > bt) - (at < bt)


def note_release(headers):
    """记录服务端广播的最新版本（响应头），供 update_info 生成升级提示。"""
    try:
        latest = (headers.get("X-ARI-Skill-Latest") or "").strip()
        url = (headers.get("X-ARI-Skill-Update-Url") or "").strip()
    except Exception:
        return
    if latest:
        _release["latest"] = latest
    if url:
        _release["url"] = url


def update_info():
    """本地版本低于服务端最新版时返回升级提示，否则 None。

    只在「确实更旧」时提示：本地版本更新（开发中）不该反复告警。
    """
    latest = _release.get("latest") or ""
    if not latest or version_cmp(VERSION, latest) >= 0:
        return None
    return {
        "current": VERSION, "latest": latest,
        "url": _release.get("url") or links()["apiKeys"],
        "message": "有新版 Skill（%s → %s）。请通过原安装渠道更新后再使用；"
                   "本 CLI 不会自行下载或执行任何远端代码。" % (VERSION, latest),
    }


def emit(obj, compact=False):
    global _exit_code
    if isinstance(obj, dict) and obj.get("success") is False:
        _exit_code = 1
    if isinstance(obj, dict):
        upd = update_info()
        if upd:
            obj["update"] = upd
    print(json.dumps(
        obj, ensure_ascii=False,
        separators=((",", ":") if compact else (", ", ": ")),
        indent=(None if compact else 2),
    ))


def err_code(out):
    if not isinstance(out, dict):
        return ""
    err = out.get("error")
    if isinstance(err, dict) and err.get("code"):
        return str(err["code"])
    return str(out.get("code") or "")


def err_message(out):
    if not isinstance(out, dict):
        return ""
    err = out.get("error")
    if isinstance(err, dict) and err.get("message"):
        return str(err["message"])
    return str(out.get("message") or "")


def parse_http_error(exc, query):
    note_release(exc.headers)  # 426（版本过旧）等错误响应同样带广播头
    try:
        detail = json.loads(exc.read().decode("utf-8", errors="replace"))
    except Exception:
        detail = {}
    if isinstance(detail, dict) and detail:
        detail["_httpStatus"] = exc.code
        detail["_query"] = query
        detail["links"] = links()
        return detail
    return error_obj("HTTP_ERROR", exc.code, "HTTP %d" % exc.code, query=query)


def as_collecting(out, http_status):
    """把「采集中、暂无足够数据」的 202 转成显式错误码。

    服务端在这种情况下返回 202 + success:true，但信封里既没有报告也没有内容；
    照原样交给上层会被当成一次成功的分析。该分支未扣点，重试是免费的。
    """
    if http_status != 202 or not isinstance(out, dict):
        return None
    data = out.get("data")
    if not isinstance(data, dict) or data.get("status") != "COLLECTING":
        return None
    wait = data.get("retryAfterSeconds") or 30
    return error_obj(
        "ARI_COLLECTING", 202, "该 ASIN 正在采集中，暂无足够数据可分析",
        "本次未扣点。等待约 %s 秒后重试即可（该分支重试免费）。" % wait)


def request_json(method, path, payload=None, params=None):
    query = {
        "method": method,
        "path": path,
        "params": {k: v for k, v in (params or {}).items() if v not in (None, "")},
        "payload": payload,
    }
    try:
        req = api_request(method, path, payload, query["params"])
        with open_api(req, timeout=TIMEOUT_SEC) as resp:
            note_release(resp.headers)
            raw = resp.read().decode("utf-8")
            out = json.loads(raw) if raw else {"success": True, "data": None}
            if isinstance(out, dict):
                alt = as_collecting(out, resp.status)
                if alt is not None:
                    alt["_query"] = query
                    return alt
                out["_query"] = query
            return out
    except EndpointBlocked as exc:
        return endpoint_error(exc)
    except urllib.error.HTTPError as exc:
        return parse_http_error(exc, query)
    except Exception as exc:
        return error_obj("NETWORK_ERROR", 0, str(exc), "检查网络或 ARI 官方服务状态", query)


def request_sse(path, payload, recovery_hint=None):
    query = {"method": "POST", "path": path, "params": {}, "payload": payload}
    result = {"meta": None, "content": "", "result": None, "reportId": 0, "creditsUsed": 0}
    try:
        req = api_request("POST", path, payload, accept="text/event-stream")
        with open_api(req, timeout=SSE_TIMEOUT_SEC) as resp:
            note_release(resp.headers)
            content_type = resp.headers.get("Content-Type", "")
            if "text/event-stream" not in content_type:
                # 就绪检查等前置校验在开流之前返回普通 JSON。
                raw = resp.read().decode("utf-8")
                out = json.loads(raw) if raw else {"success": True, "data": None}
                alt = as_collecting(out, resp.status)
                if alt is not None:
                    alt["_query"] = query
                    return alt
                out["_query"] = query
                return out

            for raw_line in resp:
                line = raw_line.decode("utf-8", errors="replace").strip()
                if not line.startswith("data: "):
                    continue
                raw = line[6:].strip()
                if not raw:
                    continue
                try:
                    event = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                kind = event.get("type")
                if kind == "meta":
                    result["meta"] = {k: v for k, v in event.items() if k != "type"}
                elif kind == "content":
                    result["content"] += event.get("content") or ""
                elif kind == "result":
                    result["result"] = event.get("data") or {
                        k: v for k, v in event.items() if k != "type"
                    }
                    result["reportId"] = event.get("reportId") or 0
                elif kind == "done":
                    result["creditsUsed"] = event.get("creditsUsed") or 0
                    result["reportId"] = event.get("reportId") or result["reportId"]
                    for key in ("requestId", "taskId", "reportUrl"):
                        if event.get(key):
                            result[key] = event[key]
                elif kind == "error":
                    return error_obj(
                        event.get("code") or "ARI_ANALYSIS_ERROR", 200,
                        event.get("message") or "analysis failed",
                        "已生成的部分内容保留在 partial 中", query, result)
            if result.get("reportId"):
                result["reportUrl"] = report_url(result["reportId"])
            return {"success": True, "data": result, "_query": query, "links": links()}
    except EndpointBlocked as exc:
        return endpoint_error(exc)
    except urllib.error.HTTPError as exc:
        return parse_http_error(exc, query)
    except Exception as exc:
        # 流中断（socket 超时 / 连接断开）时服务端往往已经跑完、扣点并归档。
        # 这里绝不能提示「重试」——重跑 --confirm 会为同一份报告扣第二次点。
        return error_obj(
            "ARI_STREAM_INTERRUPTED", 0, "分析流中断：%s" % exc,
            recovery_hint or
            "本次分析可能已扣点并已归档。请先运行 reports --asin <ASIN> --limit 1 "
            "确认是否已生成新报告；确认没有生成后才可重试，不要直接重跑 --confirm。",
            query, result)


def fetch_release():
    """读取公开的版本发布信息（免认证，Key 缺失或失效时也能拿到升级入口）。

    失败一律静默返回 None——查不到新版说明不该影响任何正常命令。
    """
    try:
        req = api_request("GET", "/api/v1/public/config", authenticated=False)
        with open_api(req, timeout=15) as resp:
            note_release(resp.headers)
            body = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None
    rel = ((body or {}).get("data") or {}).get("skillRelease")
    if not isinstance(rel, dict):
        return None
    if rel.get("latest"):
        _release["latest"] = str(rel["latest"])
    if rel.get("url"):
        _release["url"] = str(rel["url"])
    return rel


def data_of(out):
    return out.get("data") if isinstance(out, dict) else None


def ok(out):
    return isinstance(out, dict) and out.get("success") is True


def response_failures(node, prefix=""):
    """在 deepdive/charts 这类聚合结果里找出失败的子请求。

    只在「还没看到 success 字段」的层级继续下钻，避免把业务数据误判成响应信封。
    """
    fails = []
    for key, val in node.items():
        if key.startswith("_") or not isinstance(val, dict):
            continue
        name = prefix + key
        if "success" in val:
            if val.get("success") is False:
                fails.append({"part": name, "code": err_code(val),
                              "message": err_message(val)})
        else:
            fails.extend(response_failures(val, name + "."))
    return fails


def emit_bundle(bundle, compact):
    """聚合结果里任一子请求失败，外层就必须是 success:false。

    否则 agent 只看最外层信封就会把「图表 403 / 分析 402」当成完整数据，
    在缺数据的情况下继续写报告。
    """
    fails = response_failures(bundle)
    out = {"success": not fails, "data": bundle, "links": links()}
    if fails:
        out["failedParts"] = fails
        out["error"] = {
            "code": "ARI_PARTIAL_FAILURE", "status": 0,
            "message": "%d 个子请求失败：%s" % (
                len(fails), ", ".join(f["part"] for f in fails)),
            "hint": "只能使用 data 中成功返回的部分；缺失的数据不得推断或补造。",
        }
    emit(out, compact)


def save_key(key):
    """写本机用户配置（0600 直接创建，避免「默认权限 → chmod」之间的可读窗口）。"""
    path = config_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump({"api_key": key}, fh)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return path


def cmd_configure(args):
    key = getpass.getpass("ARI API Key (ari_live_*): ").strip()
    if not key.startswith("ari_live_"):
        emit(error_obj("ARI_API_KEY_INVALID_FORMAT", 0, "Key 必须以 ari_live_ 开头"), args.compact)
        raise SystemExit(2)
    path = save_key(key)
    emit({"success": True, "data": {
        "configured": True, "path": path,
        "note": "Windows 上 POSIX 权限位不生效，请自行确保该路径不被共享或同步到云端。",
    }}, args.compact)


def request_public(method, path, payload=None, timeout=15):
    """免认证请求（设备码授权等公开端点），错误统一转 error_obj。"""
    query = {"method": method, "path": path, "params": {}, "payload": payload}
    try:
        req = api_request(method, path, payload, authenticated=False)
        with open_api(req, timeout=timeout) as resp:
            note_release(resp.headers)
            out = json.loads(resp.read().decode("utf-8"))
            if isinstance(out, dict):
                out["_query"] = query
            return out
    except EndpointBlocked as exc:
        return endpoint_error(exc)
    except urllib.error.HTTPError as exc:
        return parse_http_error(exc, query)
    except Exception as exc:
        return error_obj("NETWORK_ERROR", 0, str(exc), "检查网络或 ARI 官方服务状态", query)


def cmd_setup(args):
    """设备码授权：浏览器点一下，Key 自动落到本机，全程无复制粘贴。

    进度提示走 stderr（用户/代理立即可见），stdout 仍只输出最终 JSON。
    刻意不在 CLI 里做注册：注册留在网页（人机验证与邮箱验证防线不动）。
    """
    start = request_public("POST", "/api/v1/auth/device/start", {})
    if not ok(start):
        emit(start, args.compact)
        return
    data = start.get("data") or {}
    code = str(data.get("code") or "")
    verify_url = str(data.get("verifyUrl") or "")
    token = str(data.get("pollToken") or "")
    interval = max(1, int(data.get("interval") or 3))
    expires = int(data.get("expiresIn") or 600)
    if not (code and verify_url and token):
        emit(error_obj("ARI_DEVICE_START_MALFORMED", 0, "服务端响应缺少必要字段"), args.compact)
        return

    try:
        validate_official_url(verify_url)
    except EndpointBlocked as exc:
        emit(endpoint_error(exc), args.compact)
        return

    print("请在浏览器打开以下链接完成授权（设备码 %s，%d 分钟内有效）：" % (code, expires // 60),
          file=sys.stderr)
    print("  " + verify_url, file=sys.stderr)
    print("未注册会先引导注册（需完成邮箱验证）；授权后本命令自动完成。", file=sys.stderr)

    deadline = time.time() + expires
    while time.time() < deadline:
        time.sleep(interval)
        poll = request_public("POST", "/api/v1/auth/device/poll", {"pollToken": token})
        if not ok(poll):
            if err_code(poll) in ("ARI_NOT_FOUND", "ARI_ENDPOINT_BLOCKED", "ARI_REDIRECT_BLOCKED"):
                emit(poll, args.compact)
                return
            continue  # 网络抖动/限流：下轮再试
        status = str((poll.get("data") or {}).get("status") or "")
        if status == "APPROVED":
            key = str((poll.get("data") or {}).get("apiKey") or "")
            if not key.startswith("ari_live_"):
                emit(error_obj("ARI_DEVICE_KEY_MALFORMED", 0, "服务端未返回有效 Key"), args.compact)
                return
            path = save_key(key)
            emit({"success": True, "data": {
                "configured": True, "path": path,
                "keyPrefix": key[:len("ari_live_") + 8],
                "note": "API Key 已保存到本机用户配置，其余命令可直接使用。",
            }}, args.compact)
            return
        if status == "CLAIMED":
            emit(error_obj(
                "ARI_DEVICE_ALREADY_CLAIMED", 0, "该会话的 Key 已被领取",
                "若非你本人操作，请到用户中心撤销该 Key 后重新运行 setup。"), args.compact)
            return
        if status == "EXPIRED":
            break
    emit(error_obj(
        "ARI_DEVICE_EXPIRED", 0, "授权未在有效期内完成",
        "重新运行 python ari.py setup 并尽快在浏览器完成授权。"), args.compact)


def cmd_check(args):
    # 先取公开发布信息：Key 无效时也能顺带告诉用户「你的版本旧了、去哪儿更新」。
    release = fetch_release()
    me = request_json("GET", "/api/v1/user/me")
    if not ok(me):
        emit(me, args.compact)
        return
    balance = request_json("GET", "/api/v1/credits/balance")
    if not ok(balance):
        emit(balance, args.compact)
        return
    # 1.4.11：不再回报账户免确认策略。它只服务于「小额付费操作直接生成」，等于把
    # 「不用先问」交给 agent，与全系列「先报价、用户明确确认才执行」的契约冲突
    # （ClawSweeper 归类为 Autonomous Decision Making）。付费门槛仍由服务端策略
    # 控制，本地不做任何隐式确认，所以 check 只回 Key、账户与余额。
    emit({"success": True, "data": {
        "skillVersion": VERSION,
        "release": release,
        "user": data_of(me),
        "balance": data_of(balance),
    }, "links": links()}, args.compact)


AUTOCONFIRM_MODE_NOTE = {
    "always_ask": "每次付费操作都会先报价、等你确认。",
    "user_limit": "{limit} 积点以内的操作直接生成，超过才问你。",
    "free_small": "免费版 {max} 积点以内的操作直接生成（用的是赠送积点）。",
    "first_runs": "前几次付费操作直接生成、不看金额（还剩 {remaining} 次），之后会先问你。",
    "ask": "付费操作会先报价、等你确认。",
}


def cmd_autoconfirm(args):
    """免确认阈值：不带参数=查看；`autoconfirm 50`=50 积点以内不问；`autoconfirm off`=每次都问；`autoconfirm default`=恢复默认。"""
    value = (args.value or "").strip().lower()
    if value:
        if value in ("off", "ask", "0"):
            limit = 0
        elif value in ("default", "reset", "auto"):
            limit = -1
        else:
            try:
                limit = int(value)
            except ValueError:
                emit(error_obj("ARI_BAD_ARGUMENT", 0, "参数不对",
                               "用法：autoconfirm 50（50 积点以内不问）/ autoconfirm off（每次都问）/ autoconfirm default（恢复默认）"),
                     args.compact)
                return
        out = request_json("PUT", "/api/v1/user/autoconfirm", {"limit": limit})
    else:
        out = request_json("GET", "/api/v1/user/autoconfirm")
    if ok(out) and isinstance(data_of(out), dict):
        d = data_of(out)
        d["note"] = AUTOCONFIRM_MODE_NOTE.get(d.get("mode"), AUTOCONFIRM_MODE_NOTE["ask"]).format(
            limit=d.get("userLimit"), max=d.get("maxCredits"), remaining=d.get("remainingFreeRuns"))
    emit(out, args.compact)


def cmd_products(args):
    emit(request_json("GET", "/api/v1/asins"), args.compact)


def usable_balance(site):
    """返回该站点实际可用于采集的积点。

    赠送积点（注册礼/Free 周期发放/任务奖励等）只能在 amz_us 消费；
    付费积点（订阅套餐周期积点、增量包）全站可用。服务端在 balance 里
    给出 nonUsCollectCredits（非美站可用额），以它为准——
    只报「总余额」会让用户在余额看似充足的情况下确认后吃 402。
    返回 (info, err)：err 非 None 时应直接把它 emit 出去。
    """
    bal = request_json("GET", "/api/v1/credits/balance")
    if not ok(bal):
        return None, bal
    d = data_of(bal) or {}
    plan = int((d.get("planCredits") or {}).get("available") or 0)
    addon = int((d.get("addonCredits") or {}).get("available") or 0)
    if site == "amz_us":
        return {"usable": plan + addon, "planCredits": plan, "addonCredits": addon,
                "note": ""}, None
    non_us = d.get("nonUsCollectCredits")
    if non_us is None:
        # 旧服务端没有该字段时保守回落：只按付费增量包算，宁可少报不误导确认。
        non_us = addon
    # 1.5.0：服务端 credits.gift 策略下首次采集不限站点（giftAllSites=true），此时赠送积点
    # 也算进 nonUsCollectCredits——不要再对新用户说「赠送积点不可用」把人劝退。
    note = ""
    if not d.get("giftAllSites"):
        note = "非美国站采集仅可使用付费积点（订阅套餐/增量包），赠送积点不可用。"
    return {"usable": int(non_us), "planCredits": plan, "addonCredits": addon,
            "note": note}, None


def collection_plan(asin, site, pages, star="all_stars", sort="recent", alias="", schedule="manual"):
    pricing = request_json("GET", "/api/v1/billing/pricing")
    if not ok(pricing):
        return None, pricing
    pdata = data_of(pricing) or {}
    price = int(pdata.get("collectPerPage") or 5)
    max_pages = int(pdata.get("maxPages") or 10)
    if pages > max_pages:
        return None, error_obj(
            "ARI_COLLECT_PAGE_LIMIT", 403,
            "单次采集超过 %d 页需要月付 Professional 套餐或累计充值满 ¥99" % max_pages,
            "请改用 --pages %d，或升级套餐 / 充值后再采集更多页。" % max_pages)
    bal, err = usable_balance(site)
    if err is not None:
        return None, err
    # 试用：服务端给出该用户首次采集可免费的页数（trialFreePages），冻结与结算都按
    # (页数 − 免费页) × 单价；这里同口径，否则新用户赠送积点压线时会被误报「积点不足」。
    free_pages = min(max(int(pdata.get("trialFreePages") or 0), 0), pages)
    return {
        # 采集是固定单价：credits = 单价 × 计费页数，不是估算区间。上游评论不够这么多页时
        # 只收实际采到的页数（网关按商品评论总数预裁），差额自动退回。
        "credits": (pages - free_pages) * price,
        "freePages": free_pages,
        "pricePerPage": price,
        "pages": pages,
        "approxReviews": pages * int(pdata.get("reviewsPerPage") or 10),
        "balance": bal,
        "maxPages": max_pages,
        "monitoring": {"schedule": schedule, "pagesPerRun": int(pdata.get("schedulePages") or 1),
                       "creditsPerRun": price * int(pdata.get("schedulePages") or 1),
                       "monthlyEstimate": round(price * int(pdata.get("schedulePages") or 1) * 4.3) if schedule == "weekly" else 0,
                       "note": "仅新产品使用此计划；已有产品（包括询价留下的 idle 产品）保留原计划和暂停状态，以提交响应为准。weekly 会在首次采集后每 7 天自动采集并扣点，manual 只采本次。价格 / BSR 监控需单独开启。"},
        "payload": {
            "asin": asin.upper(), "site": site, "pageCount": pages,
            "filterByStar": star, "sortBy": sort, "alias": alias, "schedule": schedule,
        },
    }, None


def collection_quote(plan):
    bal = plan["balance"]
    return {
        "confirmationRequired": True,
        "monitoring": plan.get("monitoring"),
        "credits": plan["credits"],
        "pricePerPage": plan["pricePerPage"],
        "pages": plan["pages"],
        "approxReviews": plan["approxReviews"],
        "usableBalance": bal["usable"],
        "planCredits": bal["planCredits"],
        "addonCredits": bal["addonCredits"],
        "sufficient": bal["usable"] >= plan["credits"],
        "siteNote": bal["note"],
        "freePages": plan.get("freePages", 0),
        "pricingNote": (("首次采集试用：%d 页免费，其余 " % plan["freePages"]) if plan.get("freePages") else "固定 ")
                       + "%d 积点/页 × %d 页 = %d 积点；评论不够这么多页时只收实际采到的页数，差额自动退回。"
                       % (plan["pricePerPage"], plan["pages"] - plan.get("freePages", 0), plan["credits"]),
        "message": "确认后用同一命令追加 --confirm；需要等待完成再追加 --wait。",
        "request": plan["payload"],
    }


def execute_collection(plan, wait, interval, timeout):
    bal = plan["balance"]
    estimate = plan["credits"]
    site = plan["payload"]["site"]
    if bal["usable"] < estimate:
        return error_obj(
            "ARI_INSUFFICIENT_CREDITS", 402, "积点不足",
            "本次需要 %d 点（%d 积点/页 × %d 页），%s 站可用 %d 点。%s请充值后重试。"
            % (estimate, plan["pricePerPage"], plan["pages"], site, bal["usable"],
               bal["note"] and bal["note"] + " "))
    out = request_json("POST", "/api/v1/collection/submit", plan["payload"])
    if wait and ok(out):
        task_id = (data_of(out) or {}).get("taskId")
        if task_id:
            submitted = data_of(out)
            final = wait_task(task_id, interval, timeout)
            if ok(final):
                out = {"success": True, "data": {"submitted": submitted,
                                                   "final": data_of(final)},
                       "links": links()}
            else:
                final["submitted"] = submitted
                out = final
    return out


def wait_task(task_id, interval, timeout):
    """轮询到任务终态。jobs 表的状态集合是 queued/running/done/failed。

    单次瞬时错误不中止等待：此时采集积点已冻结、任务仍在后台跑，
    直接返回会让调用方误以为采集已经结束。
    """
    deadline = time.time() + timeout
    last = None
    transient = 0
    while time.time() < deadline:
        last = request_json("GET", "/api/v1/collection/status/" + urllib.parse.quote(task_id))
        if ok(last):
            transient = 0
            status = str((data_of(last) or {}).get("status") or "").lower()
            if status in ("done", "failed"):
                return last
        elif err_code(last) in RETRYABLE_CODES:
            transient += 1
            if transient >= 3:
                last["hint"] = ("连续 %d 次查询失败；采集任务仍可能在后台运行，"
                                "稍后用 status --task %s 查询。" % (transient, task_id))
                return last
        else:
            return last
        time.sleep(interval)
    return error_obj("WAIT_TIMEOUT", 0, "等待采集超时，任务仍可能在后台运行",
                     "稍后使用 status --task %s 查询" % task_id,
                     partial=data_of(last) if last else None)


def cmd_collect(args):
    plan, err = collection_plan(args.asin, args.site, args.pages,
                                args.star, args.sort, args.alias, getattr(args, "schedule", "weekly"))
    if err is not None:
        emit(err, args.compact)
        return
    if not args.confirm:
        emit({"success": True, "data": collection_quote(plan), "links": links()}, args.compact)
        return
    emit(execute_collection(plan, args.wait, args.interval, args.timeout), args.compact)


def cmd_monitor(args):
    """监控中心只读总览：不创建监控、不采集、不调用 LLM。"""
    emit(request_json("GET", "/api/v1/monitor/overview"), args.compact)


def cmd_schedule(args):
    """查看/设置产品的定期采集（免费操作，采集本身按页扣点）。

    这是 ARI 从「一次性查询」变成「持续积累」的那个开关：开着它，新评论每天/每周
    自动进库，趋势、差评归因、报告环比才有意义。不带 --set 时只列出当前计划。
    """
    if not args.set:
        out = request_json("GET", "/api/v1/asins")
        d = data_of(out) or {}
        rows = d.get("asins") if isinstance(d, dict) else None
        if ok(out) and isinstance(rows, list):
            monitored = [a for a in rows if a.get("schedule") != "manual" and not a.get("schedulePaused")]
            d["_monitorSummary"] = {
                "total": len(rows),
                "monitored": len(monitored),
                "manual": len([a for a in rows if a.get("schedule") == "manual"]),
                "paused": len([a for a in rows if a.get("schedulePaused")]),
                "note": "schedule=manual 表示只在手动触发时才更新，数据会停在最后一次采集那天。",
            }
        emit(out, args.compact)
        return

    asin_id = args.id
    if asin_id is None:
        if not args.asin:
            emit(error_obj("ARI_VALIDATION_ERROR", 0, "需要 --asin 或 --id",
                           "先跑 schedule（不带参数）或 products 拿到产品 id。"), args.compact)
            return
        listing = request_json("GET", "/api/v1/asins")
        if not ok(listing):
            emit(listing, args.compact)
            return
        want_asin, want_site = args.asin.upper(), args.site
        for a in (data_of(listing) or {}).get("asins") or []:
            if a.get("asin") == want_asin and (not want_site or a.get("site") == want_site):
                asin_id = a.get("id")
                break
        if asin_id is None:
            emit(error_obj("ARI_NOT_FOUND", 404, "未订阅该 ASIN",
                           "先用 collect 采集一次，产品会自动加入订阅列表。"), args.compact)
            return

    out = request_json("PUT", "/api/v1/asins/%d/schedule" % int(asin_id),
                       {"Schedule": args.set})
    if ok(out):
        pricing = request_json("GET", "/api/v1/billing/pricing")
        per = int((data_of(pricing) or {}).get("collectPerPage") or 5)
        pages = int((data_of(pricing) or {}).get("schedulePages") or 1)
        run = per * pages
        est = {"manual": 0, "weekly": round(run * 4.3), "daily": run * 30}.get(args.set, 0)
        d = data_of(out)
        if isinstance(d, dict):
            d["_costNote"] = ("每轮自动采集 %d 页 = %d 积点（只按实际采到的页数收）；按 %s 计约 %d 积点/月，随时可改回 manual。"
                              % (pages, run, args.set, est))
    emit(out, args.compact)


def cmd_competitors(args):
    """竞品管理：列出 / 添加 / 移除。竞品加进来即按周自动采集，是类目雷达的数据来源。"""
    base = "/api/v1/asins/%d/competitors" % args.id
    if args.remove:
        emit(request_json("DELETE", base + "/%d" % args.remove), args.compact)
        return
    if args.add:
        emit(request_json("POST", base, {"asin": args.add.upper(), "site": args.site}), args.compact)
        return
    emit(request_json("GET", base), args.compact)


def cmd_radar(args):
    """类目雷达：本品 vs 竞品最近 N 周的均分/新评论/差评走势（免费，纯 SQL 不烧积点）。

    曲线短的时候看不出什么，攒满一个季度就能看出谁在往上走——这正是持续监控的价值。
    """
    out = request_json("GET", "/api/v1/asins/%d/radar" % args.id,
                       params={"weeks": args.weeks})
    if err_code(out) == "ARI_FORBIDDEN":
        out["hint"] = "当前套餐未开放类目雷达，升级后可对比竞品走势：" + links().get("billing", "")
    emit(out, args.compact)


def _watch_id_or_error(args):
    value = getattr(args, "watch_id", None)
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        return None, error_obj(
            "ARI_VALIDATION_ERROR", 0, "watch-id 必须是正整数",
            "示例：watch digest --watch-id 123",
        )
    return value, None


def _watch_list_items(out):
    data = data_of(out)
    if isinstance(data, dict):
        items = data.get("watches")
    else:
        items = data
    return items if isinstance(items, list) else []


def _watch_update(args, enabled):
    watch_id, err = _watch_id_or_error(args)
    if err is not None:
        emit(err, args.compact)
        return
    # There is no GET /watches/{id} route.  Read the owned list first, then
    # preserve the server's current schedule in the PUT update.
    listed = request_json("GET", "/api/v1/product-operations/watches")
    if not ok(listed):
        emit(listed, args.compact)
        return
    current = next((item for item in _watch_list_items(listed)
                    if isinstance(item, dict) and item.get("id") == watch_id), None)
    if current is None:
        emit(error_obj("ARI_NOT_FOUND", 404, "找不到该 watch",
                       "先运行 watch list 查看当前账户的 watch。"), args.compact)
        return
    schedule = str(current.get("schedule") or "").strip()
    if schedule not in WATCH_SCHEDULES:
        emit(error_obj("ARI_VALIDATION_ERROR", 0, "watch 缺少有效 schedule",
                       "请先删除该 watch，再按 daily / weekly / monthly 重新创建。"), args.compact)
        return
    payload = {"schedule": schedule, "enabled": enabled}
    # 恢复即授权按刷新次数扣点：只有用户确认过 watch quote 的单价才带 acceptPrice；
    # 不带时服务端返回 ARI_CONFIRM_PRICE + 报价，原样交给用户确认，不自动重试。
    accept_price = getattr(args, "accept_price", None)
    if enabled and accept_price:
        payload["acceptPrice"] = accept_price
    emit(request_json(
        "PUT", "/api/v1/product-operations/watches/%d" % watch_id, payload,
    ), args.compact)


def cmd_watch_list(args):
    emit(request_json("GET", "/api/v1/product-operations/watches"), args.compact)


def cmd_watch_quote(args):
    """商品监控报价（只读）：每次到期刷新按频率扣点，单价以服务端后台配置为准。"""
    out = request_json("GET", "/api/v1/product-operations/capabilities")
    if not ok(out):
        emit(out, args.compact)
        return
    data = data_of(out)
    data = data if isinstance(data, dict) else {}
    emit({"success": True, "data": {
        "watchEnabled": bool(data.get("watchEnabled")),
        "watchPricing": data.get("watchPricing") or [],
        "note": "商品监控每次到期刷新按频率扣点（刷新失败不扣）。向用户复述所选频率的"
                "「每次 perRefresh 积点、约 monthlyEstimate 积点/月」并获得明确同意后，"
                "再用 --accept-price <perRefresh> 执行 watch create / watch resume。",
    }}, args.compact)


def cmd_watch_create(args):
    # main() already normalizes/validates ASIN; keep direct function calls safe
    # for callers and tests that bypass the parser.
    check_asin_args(args)
    payload = {
        "asin": args.asin,
        "site": args.site,
        "schedule": args.schedule,
        "enabled": not args.disabled,
    }
    competitor = getattr(args, "competitor", None)
    if competitor:
        payload["competitorAsin"] = competitor
    # 开启即授权周期扣点：acceptPrice 必须是用户确认过的 watch quote 单价。
    accept_price = getattr(args, "accept_price", None)
    if accept_price and not args.disabled:
        payload["acceptPrice"] = accept_price
    emit(request_json("POST", "/api/v1/product-operations/watches", payload), args.compact)


def cmd_watch_series(args):
    watch_id, err = _watch_id_or_error(args)
    if err is not None:
        emit(err, args.compact)
        return
    emit(request_json(
        "GET", "/api/v1/product-operations/watches/%d/series" % watch_id,
        params={"days": args.days},
    ), args.compact)


def cmd_watch_pause(args):
    _watch_update(args, False)


def cmd_watch_resume(args):
    _watch_update(args, True)


def cmd_watch_delete(args):
    watch_id, err = _watch_id_or_error(args)
    if err is not None:
        emit(err, args.compact)
        return
    emit(request_json(
        "DELETE", "/api/v1/product-operations/watches/%d" % watch_id
    ), args.compact)


def cmd_watch_digest(args):
    watch_id, err = _watch_id_or_error(args)
    if err is not None:
        emit(err, args.compact)
        return
    emit(request_json(
        "GET", "/api/v1/product-operations/watch-digest",
        params={"watchId": watch_id, "period": args.period},
    ), args.compact)


def cmd_watch_events(args):
    watch_id, err = _watch_id_or_error(args)
    if err is not None:
        emit(err, args.compact)
        return
    if isinstance(args.limit, bool) or not isinstance(args.limit, int) or args.limit <= 0:
        emit(error_obj(
            "ARI_VALIDATION_ERROR", 0, "limit 必须是正整数",
            "示例：watch events --watch-id 123 --limit 50",
        ), args.compact)
        return
    emit(request_json(
        "GET", "/api/v1/product-operations/events",
        params={"watchId": watch_id, "limit": args.limit},
    ), args.compact)


def cmd_status(args):
    emit(request_json("GET", "/api/v1/collection/status/" + urllib.parse.quote(args.task)), args.compact)


def cmd_reviews(args):
    """读取已采集评论。

    --sort helpful 配合 --stars negative 就是「高赞差评榜」：买家在商品页最先看到的
    就是这几条，对转化伤害最大，也是卖家最该先处理的。1.3.0 只能按时间排，这批评论
    永远沉在后面。
    """
    params = {"asin": args.asin.upper(), "site": args.site, "star": args.star,
              "stars": args.stars, "q": args.query, "page": args.page,
              "sort": args.sort}
    if getattr(args, "topic", ""):
        params["topic"] = args.topic  # 1.4.7：按话题标签筛，返回行带 tags（原句可引用）
    if args.with_images:
        params["withImages"] = "1"
    if args.vine:
        params["vine"] = "1"
    if args.purchased:
        params["purchased"] = "1"
    emit(request_json("GET", "/api/v1/reviews", params=params), args.compact)


def cmd_topics(args):
    """话题标签（1.4.7，免费）：每条评论入库后自动打上「维度 + 话题 + 原句」，这里按话题汇总。

    不带 --key 列全部话题（提及数 / 4~5 星与 1~3 星各多少 / 近 30 天新增）与打标进度；
    带 --key 看单个话题：近 12 个月趋势、常见原句、本品 vs 竞品的提及率与差评占比、标签洞察摘要。
    打标是采集后异步跑的，progress.tagged < progress.total 说明还在打，几分钟后再看。
    """
    if args.key:
        out = request_json("GET", "/api/v1/asins/%d/topics/%s" % (args.id, args.key),
                           params={"lang": args.lang})
    else:
        out = request_json("GET", "/api/v1/asins/%d/topics" % args.id,
                           params={"dimension": args.dimension, "days": args.days})
        if isinstance(out, dict) and isinstance(out.get("progress"), dict):
            pr = out["progress"]
            if pr.get("tagged", 0) < pr.get("total", 0):
                out["_note"] = ("已打标 %d/%d 条，剩余在后台几分钟内完成；现在看到的是已打标部分的汇总。"
                                % (pr.get("tagged", 0), pr.get("total", 0)))
    emit(out, args.compact)


def chart_bundle(asin, site, days):
    # 先在主线程把 Key 问题（缺失/格式错）解决掉：require_key 失败会 emit + exit，
    # 若发生在工作线程里会打出多份错误 JSON，破坏单对象输出契约。
    require_key()
    params = {"asin": asin.upper(), "site": site, "days": days}
    names = ("stars", "trend", "keywords", "flow")
    # 四个图表端点互不依赖，并行取。request_json 把所有异常转成错误 dict 返回，
    # 不会从线程里抛出来。
    with ThreadPoolExecutor(max_workers=len(names)) as pool:
        futures = [(name, pool.submit(
            request_json, "GET", "/api/v1/charts/" + name, params=params))
            for name in names]
        return {name: fut.result() for name, fut in futures}


def window_note(days):
    return {"days": days,
            "note": "days=0 表示全部历史；非 0 时图表只统计最近 N 天，"
                    "解读趋势/占比必须带上这个窗口。"}


def cmd_charts(args):
    bundle = chart_bundle(args.asin, args.site, args.days)
    bundle["_window"] = window_note(args.days)
    emit_bundle(bundle, args.compact)


def quote_payload(kind, asin, site, competitor, competitor_site):
    return {
        "type": kind, "asin": (asin or "").upper(), "site": site,
        "competitorAsin": (competitor or "").upper(),
        "competitorSite": competitor_site or site,
    }


def missing_competitor(kind, competitor):
    if kind != "compare" or (competitor or "").strip():
        return None
    return error_obj("ARI_VALIDATION_ERROR", 0, "compare 需要 --competitor <竞品ASIN>",
                     "示例：analyze --type compare --asin <目标ASIN> --competitor <竞品ASIN>")


def backfill_report_id(out, asin):
    """为兼容旧服务端，补上 VOC / compare 的 reportId。

    1.2.0 起 VOC 的 done 事件直接带 reportId；旧服务端仍可能不带。
    分析确实完成时回查最新报告作为兜底。
    """
    data = data_of(out)
    if not ok(out) or not isinstance(data, dict):
        return out
    if data.get("reportId") or not data.get("creditsUsed"):
        return out
    listed = request_json("GET", "/api/v1/reports",
                          params={"asin": (asin or "").upper(), "limit": 1})
    if ok(listed):
        items = (data_of(listed) or {}).get("reports") or []
        if items and items[0].get("id"):
            data["reportId"] = items[0]["id"]
            data["reportIdSource"] = "reports-lookup"
            data["reportUrl"] = report_url(items[0]["id"])
    return out


def run_analysis(kind, asin, site, competitor, competitor_site, language, confirm):
    bad = missing_competitor(kind, competitor)
    if bad is not None:
        return bad
    q_payload = quote_payload(kind, asin, site, competitor, competitor_site)
    quote = request_json("POST", "/api/v1/analysis/quote", q_payload)
    if not ok(quote):
        return quote
    q_data = data_of(quote) or {}
    # 1.5.0 免确认直达：与 cmd_voc 同一口径——**只认服务端 `autoConfirm` 一个布尔**。
    # 首次体验不看金额上限 / 用户自设阈值 / 「每次先问」/ 余额不足，全部由服务端
    # skill.autoConfirm 策略判定；客户端不从 note 文案或 autoConfirmRemaining 自行推断
    # （曾用「note 含『先确认』」判断，结果 Free 小额的提示语里恰好有这个词，把新用户挡回询价）。
    auto_confirmed = False
    if not confirm and q_data.get("sufficient") and bool(q_data.get("autoConfirm")):
        confirm = True
        auto_confirmed = True
    if not confirm:
        return {"success": True, "data": {"confirmationRequired": True, "quote": q_data,
                                             "webUrl": q_data.get("webUrl"),
                                             "message": "用户确认后追加 --confirm 才会生成并扣点。"},
                "links": links()}
    if not q_data.get("sufficient", False):
        return error_obj("ARI_INSUFFICIENT_CREDITS", 402, "积点不足",
                         "需要 %s 点，当前余额 %s；请充值后重试。" %
                         (q_data.get("price"), q_data.get("balance")))

    payload = {"asin": (asin or "").upper(), "site": site, "outputLanguage": language}
    if kind == "compare":
        payload.update({"competitorAsin": (competitor or "").upper(),
                        "competitorSite": competitor_site or site})
    path = "/api/v1/analysis/" + kind
    if kind in SSE_TYPES:
        out = backfill_report_id(request_sse(path, payload), asin)
    else:
        out = request_json("POST", path, payload)
    if ok(out) and isinstance(data_of(out), dict):
        d = data_of(out)
        d["webUrl"] = q_data.get("webUrl") or d.get("webUrl")
        if auto_confirmed:
            # 1.5.0：把实际扣点摆出来，事后一目了然；价格取服务端本次报价，不写死。
            _price = int(q_data.get("price") or 0)
            _balance = int(q_data.get("balance") or 0)
            d["autoConfirmed"] = True
            d["charges"] = {
                "totalCredits": _price,
                "balanceBefore": _balance,
                "balanceAfter": _balance - _price,
            }
            d["autoConfirmNote"] = ("本次按免确认策略自动生成，扣 %d 积点，余额 %d。"
                                    % (_price, _balance - _price))
    return out


def cmd_quote(args):
    bad = missing_competitor(args.type, args.competitor)
    if bad is not None:
        emit(bad, args.compact)
        return
    emit(request_json("POST", "/api/v1/analysis/quote",
                      quote_payload(args.type, args.asin, args.site,
                                    args.competitor, args.competitor_site)), args.compact)


def cmd_analyze(args):
    emit(run_analysis(args.type, args.asin, args.site, args.competitor,
                      args.competitor_site, args.language, args.confirm), args.compact)


def operation_defaults():
    """Read immutable workflow defaults generated into specialized Skills."""
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "skill-defaults.json")
    try:
        with open(path, encoding="utf-8") as fh:
            value = json.load(fh)
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def allowed_commands():
    """专属包构建期写入的命令白名单；返回 None 表示不限制。

    1.4.11 起打包脚本会把文档没有承诺的命令从本文件里整段删掉。这里再读
    一次 skill-defaults.json 兜底：只删代码不留闸的话，任何人把命令加回来
    就绕过了收窄。母版与全功能马甲包没有这个字段，行为完全不变。
    """
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "skill-defaults.json")
    try:
        with open(path, encoding="utf-8") as fh:
            value = json.load(fh)
    except (OSError, ValueError):
        return None
    if not isinstance(value, dict):
        return None
    commands = value.get("allowedCommands")
    if not isinstance(commands, list):
        return None
    allowed = {item.strip() for item in commands
               if isinstance(item, str) and item.strip()}
    return allowed or None


def operation_payload(args):
    defaults = operation_defaults()
    workflow = (getattr(args, "workflow", None) or defaults.get("workflow") or "").strip()
    focus = (getattr(args, "focus", None) or defaults.get("focus") or "").strip()
    if not workflow or not focus:
        return None, error_obj(
            "ARI_VALIDATION_ERROR", 0, "运营工作流缺少 workflow/focus",
            "通用 Skill 请显式传 --workflow 和 --focus；专属 Skill 会内置固定值。")
    request_id = (getattr(args, "request_id", None) or "").strip() or str(uuid.uuid4())
    return {
        "requestId": request_id,
        "workflow": workflow,
        "focus": focus,
        "asin": args.asin.upper(),
        "site": args.site or defaults.get("defaultSite") or "amz_us",
        "competitorAsin": (getattr(args, "competitor", None) or "").upper(),
    }, None


def operation_contract(payload):
    capabilities = request_json("GET", "/api/v1/product-operations/capabilities")
    if not ok(capabilities):
        return capabilities
    data = data_of(capabilities) or {}
    if not data.get("enabled"):
        return error_obj("ARI_OPERATIONS_DISABLED", 403,
                         "当前账户尚未启用商品运营工具", "请稍后再试或联系管理员开通灰度。")
    supported = False
    for item in data.get("workflows") or []:
        if (item.get("workflow") == payload["workflow"] and
                payload["focus"] in (item.get("focuses") or [])):
            supported = True
            break
    if not supported:
        return error_obj("ARI_INVALID_OPERATIONS_WORKFLOW", 422,
                         "服务端不支持该 workflow/focus 组合",
                         "先运行 operations capabilities 查看当前白名单。")
    return None


def operation_quote(args):
    payload, err = operation_payload(args)
    if err is not None:
        return err
    contract_err = operation_contract(payload)
    if contract_err is not None:
        return contract_err
    out = request_json("POST", "/api/v1/product-operations/quote", payload)
    data = data_of(out)
    if ok(out) and isinstance(data, dict):
        data["request"] = payload
        data["confirmationRequired"] = True
        data["message"] = "确认后使用同一 requestId 运行 operations run --confirm。"
    return out


def cmd_operation_capabilities(args):
    emit(request_json("GET", "/api/v1/product-operations/capabilities"), args.compact)


def cmd_operation_profile(args):
    emit(request_json("GET", "/api/v1/product-operations/profile",
                      params={"asin": args.asin.upper(), "site": args.site}), args.compact)


def cmd_operation_quote(args):
    emit(operation_quote(args), args.compact)


def cmd_operation_run(args):
    quote = operation_quote(args)
    if not ok(quote):
        emit(quote, args.compact)
        return
    quote_data = data_of(quote) or {}
    payload = quote_data.get("request") or {}
    details = quote_data.get("quote") or {}
    if not args.confirm:
        emit(quote, args.compact)
        return
    if not details.get("reviewReady", False):
        emit(error_obj("ARI_INSUFFICIENT_REVIEWS", 422, "评论尚未达到运营分析要求",
                       "先使用现有 collect 命令采集评论；不会隐式采集或扣分析点。"), args.compact)
        return
    if details.get("missingFields"):
        emit(error_obj("ARI_PRODUCT_FIELDS_INSUFFICIENT", 422,
                       "商品详情关键字段不足", "稍后刷新商品资料后重新报价。"), args.compact)
        return
    if not details.get("sufficient", False):
        emit(error_obj("ARI_INSUFFICIENT_CREDITS", 402, "积点不足",
                       "需要 %s 点，当前余额 %s。" %
                       (details.get("price"), details.get("balance"))), args.compact)
        return
    rid = payload.get("requestId") or "<requestId>"
    hint = ("本次运营任务可能已继续执行。不要直接重跑；先运行 operations status "
            "--request-id %s 精确查询状态。" % rid)
    emit(request_sse("/api/v1/product-operations/run", payload, hint), args.compact)


def cmd_operation_status(args):
    request_id = urllib.parse.quote(args.request_id.strip(), safe="")
    emit(request_json("GET", "/api/v1/product-operations/runs/" + request_id), args.compact)


def cmd_voc(args):
    """一条命令完成采集、VOC 分析、归档和报告链接返回。"""
    asin = args.asin.upper()
    quote = request_json("POST", "/api/v1/analysis/quote",
                         quote_payload("voc", asin, args.site, None, None))
    if not ok(quote):
        emit(quote, args.compact)
        return
    analysis_quote = data_of(quote) or {}
    needs_collection = int(analysis_quote.get("totalReviews") or 0) < MIN_ANALYSIS_REVIEWS
    plan = None
    collection_credits = 0
    collection_sufficient = True
    if needs_collection:
        plan, err = collection_plan(asin, args.site, args.pages)
        if err is not None:
            emit(err, args.compact)
            return
        collection_credits = plan["credits"]
        collection_sufficient = plan["balance"]["usable"] >= collection_credits

    # 新 ASIN 采集后抽样数会上升，用 basePrice 作为分析上限；
    # 已有足够评论时使用当前精确报价。
    analysis_credits = int(analysis_quote.get(
        "basePrice" if needs_collection else "price") or 0)
    total_credits = collection_credits + analysis_credits
    total_balance = int(analysis_quote.get("balance") or 0)
    sufficient = collection_sufficient and total_balance - collection_credits >= analysis_credits
    combined_quote = {
        "confirmationRequired": True,
        "asin": asin,
        "site": args.site,
        "needsCollection": needs_collection,
        "collectionCredits": collection_credits,
        "analysisCredits": analysis_credits,
        "totalCredits": total_credits,
        "balance": total_balance,
        "sufficient": sufficient,
        "message": "确认后追加 --confirm，将自动采集、生成 VOC、归档并返回报告链接。",
    }
    if plan is not None and plan["balance"]["note"]:
        combined_quote["siteNote"] = plan["balance"]["note"]
    combined_quote["webUrl"] = analysis_quote.get("webUrl")
    # 1.5.0 免确认直达：新用户的目标就是一次性拿到报告，不再停在报价等确认。
    #  - 是否免确认**只认服务端 `autoConfirm`**（skill.autoConfirm 策略：首次体验不看金额上限、
    #    用户自设阈值优先、「每次先问」尊重、余额不足不自动）。客户端不再从 note 文案或
    #    autoConfirmRemaining 推断——文案匹配曾把 Free 小额提示里的「先确认」误判成用户要求每次询问。
    #  - 这里的 sufficient 是「采集 + 分析」合计口径（服务端报价只看分析价），合计不够就不自动，
    #    带 sufficient=false 的报价返回给 agent 引导充值。
    auto_confirmed = (not args.confirm and sufficient
                      and bool(analysis_quote.get("autoConfirm")))
    if not args.confirm and not auto_confirmed:
        combined_quote["autoConfirm"] = bool(analysis_quote.get("autoConfirm"))
        combined_quote["autoConfirmRemaining"] = int(analysis_quote.get("autoConfirmRemaining") or 0)
        if analysis_quote.get("autoConfirmNote"):
            combined_quote["autoConfirmNote"] = analysis_quote.get("autoConfirmNote")
        emit({"success": True, "data": combined_quote, "links": links()}, args.compact)
        return
    if not sufficient:
        emit(error_obj(
            "ARI_INSUFFICIENT_CREDITS", 402, "积点不足",
            "采集 + VOC 需要 %d 点，当前余额 %d；请充值后重试。"
            % (total_credits, total_balance)), args.compact)
        return

    collected = None
    if plan is not None:
        collected = execute_collection(plan, True, args.interval, args.timeout)
        if not ok(collected):
            emit(collected, args.compact)
            return
        final = (data_of(collected) or {}).get("final") or {}
        if str(final.get("status") or "").lower() != "done":
            emit(error_obj(
                "ARI_COLLECTION_FAILED", 0, "评论采集未完成，未执行 VOC 分析",
                "请查看采集任务状态；已成功采集的数据会保留。",
                partial=data_of(collected)), args.compact)
            return

    analysis = run_analysis("voc", asin, args.site, None, None, args.language, True)
    if not ok(analysis):
        if collected is not None:
            analysis["collection"] = data_of(collected)
        emit(analysis, args.compact)
        return
    report = data_of(analysis) or {}
    emit({
        "success": True,
        "data": {
            "asin": asin,
            "site": args.site,
            "collection": data_of(collected) if collected is not None else None,
            "report": report,
            "reportId": report.get("reportId"),
            "reportUrl": report.get("reportUrl"),
            "autoConfirmed": auto_confirmed,
            # 1.5.0：无论是否走免确认，都把实际扣点摆出来，用户事后一目了然。
            "charges": {
                "collectionCredits": collection_credits,
                "analysisCredits": analysis_credits,
                "totalCredits": total_credits,
                "balanceBefore": total_balance,
                "balanceAfter": total_balance - total_credits,
            },
            "autoConfirmNote": (("本次按首次体验策略自动确认，合计扣 %d 积点（采集 %d + 分析 %d），余额 %d。"
                                 % (total_credits, collection_credits, analysis_credits,
                                    total_balance - total_credits)) if auto_confirmed else ""),
            # 网页是补充视图（图表版 / 分享链接 / 海报），不是转移目的地：Skill 里能做完的事继续在这里做
            "web": {
                "report": report.get("reportUrl"),
                "product": product_url(asin, args.site),
                "hint": "网页版有健康度图表、频次表和「分享」按钮（公开链接 + 海报）；开监控在这里用 schedule --set weekly 即可。",
            },
            "message": "VOC 报告已生成并保存到用户中心。",
        },
        "links": links(),
    }, args.compact)


def cmd_reports(args):
    params = {"asin": args.asin, "type": args.type, "starred": "1" if args.starred else "",
              "q": args.query, "limit": args.limit}
    emit(attach_report_urls(request_json("GET", "/api/v1/reports", params=params)), args.compact)


def cmd_report(args):
    out = request_json("GET", "/api/v1/reports/%d" % args.id)
    data = data_of(out)
    if ok(out) and isinstance(data, dict) and data.get("id"):
        data["reportUrl"] = report_url(data["id"])
        # 环比（服务端异步生成）：prevReportId 有值但 deltaMd 为空 = 还在算，
        # 不是失败。这里给出明确状态，免得汇报时误判成「没有环比」。
        if data.get("prevReportId") and not data.get("deltaMd"):
            data["_deltaStatus"] = "generating"
            data["_deltaNote"] = "环比正在后台生成，稍等十几秒后重新 report --id 即可看到。"
        elif data.get("deltaMd"):
            data["_deltaStatus"] = "ready"
        else:
            data["_deltaStatus"] = "none"
            data["_deltaNote"] = ("这是该产品该类型的第一份报告，没有可比对象。"
                                  "开启定期采集后再生成，就会有「已解决/新出现/持续存在」的环比。")
    emit(out, args.compact)


def cmd_deepdive(args):
    products = request_json("GET", "/api/v1/asins")
    if not ok(products):
        emit(products, args.compact)
        return
    items = (data_of(products) or {}).get("asins") or []
    asin = args.asin.upper()
    target = next((x for x in items if str(x.get("asin", "")).upper() == asin
                   and x.get("site") == args.site), None)
    # asins 列表只含主品（竞品订阅被过滤掉），但 charts/reviews 对竞品同样放行。
    # 因此这里不直接拒绝——否则会把用户引去重复 collect，白扣一次采集费，
    # 还可能撞上套餐的 ASIN 订阅上限。缺主品元数据时把 AI 分析降级为只报价。
    confirm = args.confirm and target is not None
    # charts/reviews/reports 三路免费读互不依赖，并行取；分析（可能付费）单独串行，
    # 保持「报价/扣点请求永远只有一路在飞」的可预期性。
    with ThreadPoolExecutor(max_workers=3) as pool:
        charts_f = pool.submit(chart_bundle, asin, args.site, args.days)
        reviews_f = pool.submit(request_json, "GET", "/api/v1/reviews",
                                params={"asin": asin, "site": args.site, "page": 1})
        reports_f = pool.submit(request_json, "GET", "/api/v1/reports",
                                params={"asin": asin, "limit": args.report_limit})
    bundle = {
        "_window": window_note(args.days),
        "product": target,
        "charts": charts_f.result(),
        "reviews": reviews_f.result(),
        "reports": attach_report_urls(reports_f.result()),
        "analysis": run_analysis("voc", asin, args.site, None, None,
                                 args.language, confirm),
    }
    if target is None:
        note = ("%s / %s 不在主品订阅列表中。若它是作为竞品添加的，"
                "charts / reviews / analyze 仍然可用；若从未采集过，"
                "请先运行 collect --asin %s --site %s 取报价。" % (asin, args.site, asin, args.site))
        if args.confirm:
            note += " 因缺少主品订阅，本次 AI 分析已降级为只报价，未扣点。"
        bundle["productNote"] = note
    emit_bundle(bundle, args.compact)


def export_root():
    """导出的允许落点根目录：默认当前工作目录，可用 ARI_EXPORT_DIR 显式放开。

    默认收在工作目录内是有意的：导出命令的 `--out` 由调用方（通常是模型）
    给出，不设边界就等于把「任意位置写文件」交给它。
    """
    configured = (os.environ.get("ARI_EXPORT_DIR") or "").strip()
    base = os.path.expanduser(configured) if configured else os.getcwd()
    return os.path.realpath(base)


def safe_export_path(dest):
    """把导出目标限制在 export_root() 内，并拒绝符号链接落点。

    `export --out` 接受任意路径，`--out ../../<敏感文件>` 或让目标名
    指向一个符号链接，就能覆盖工作目录之外的文件（ClawSweeper T09 / 任意文件
    覆盖）。这里只接受落在 export_root() 内的普通路径；越界或符号链接一律在
    发请求之前返回错误信封。返回 (绝对路径, None) 或 (None, 错误信封)。
    """
    if not str(dest or "").strip():
        return None, error_obj("ARI_EXPORT_PATH_BLOCKED", 0, "缺少导出文件名",
                               "请用 --out 指定文件名，或留空使用默认文件名。")
    raw = os.path.expanduser(str(dest))
    if not os.path.isabs(raw):
        raw = os.path.join(os.getcwd(), raw)
    if os.path.islink(raw):
        return None, error_obj("ARI_EXPORT_PATH_BLOCKED", 0,
                               "导出目标是指向别处的符号链接",
                               "请先删除该符号链接，或换一个文件名。")
    root = export_root()
    target = os.path.realpath(raw)
    if target != root and not target.startswith(root + os.sep):
        return None, error_obj(
            "ARI_EXPORT_PATH_BLOCKED", 0, "导出路径超出允许目录",
            "默认只能写当前工作目录（%s）内的文件；确实需要写到别处时，"
            "显式设置环境变量 ARI_EXPORT_DIR 指向目标目录。" % root)
    parent = os.path.dirname(target)
    if not os.path.isdir(parent):
        return None, error_obj("ARI_EXPORT_PATH_BLOCKED", 0, "导出目录不存在",
                               "请先创建目录：%s" % parent)
    return target, None


def request_download(path, params, dest):
    """下载非 JSON 响应（CSV / HTML / Markdown）到本地文件。

    服务端在计划限制、参数错误等情况下仍返回 JSON 错误信封——先看 Content-Type，
    JSON 一律按信封透传，不落盘。CSV 流式导出中途出错时响应头已发出，服务端只能
    在文件末尾追加「# export error:」注释行，这里嗅探出来转成显式错误。
    """
    dest, blocked = safe_export_path(dest)
    if blocked is not None:
        return blocked
    query = {"method": "GET", "path": path,
             "params": {k: v for k, v in (params or {}).items() if v not in (None, "")},
             "payload": None}
    try:
        req = api_request("GET", path, params=query["params"], accept="*/*")
        with open_api(req, timeout=TIMEOUT_SEC) as resp:
            note_release(resp.headers)
            ctype = resp.headers.get("Content-Type", "")
            body = resp.read()
            if "application/json" in ctype:
                out = json.loads(body.decode("utf-8", errors="replace"))
                if isinstance(out, dict):
                    out["_query"] = query
                return out
            tail = body[-300:].decode("utf-8", errors="replace")
            if "# export error:" in tail:
                return error_obj("ARI_EXPORT_ERROR", 200,
                                 tail.split("# export error:", 1)[1].strip(),
                                 "导出中途失败，文件不完整，未落盘。", query)
            # O_NOFOLLOW 兜住「检查通过之后才把目标换成符号链接」的竞态；
            # Windows 没有这个 flag，取 0 退回普通创建。
            flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, "O_NOFOLLOW", 0)
            with os.fdopen(os.open(dest, flags, 0o600), "wb") as fh:
                fh.write(body)
            return {"success": True,
                    "data": {"savedTo": os.path.abspath(dest), "bytes": len(body),
                             "contentType": ctype.split(";")[0].strip()},
                    "_query": query, "links": links()}
    except EndpointBlocked as exc:
        return endpoint_error(exc)
    except urllib.error.HTTPError as exc:
        return parse_http_error(exc, query)
    except Exception as exc:
        return error_obj("NETWORK_ERROR", 0, str(exc), "检查网络或 ARI 官方服务状态", query)


def unit_price(key):
    """从 /billing/pricing 读单价。定价由管理后台配置、随时可调，本地绝不
    内置兜底数字——读不到就返回 None，报价文案让用户以后台当前定价为准。"""
    pricing = request_json("GET", "/api/v1/billing/pricing")
    if ok(pricing):
        try:
            value = int((data_of(pricing) or {}).get(key) or 0)
            if value > 0:
                return value
        except (TypeError, ValueError):
            pass
    return None


def cmd_alerts(args):
    """情感预警（免费）。差评突增等预警由服务端离线生成，这里只读。"""
    if args.mark_read:
        emit(request_json("POST", "/api/v1/alerts/read"), args.compact)
        return
    emit(request_json("GET", "/api/v1/alerts", params={"limit": args.limit}), args.compact)


def cmd_benchmark(args):
    """类目对标概览（免费引流）：本品在类目里的星级/差评率位置。"""
    emit(request_json("GET", "/api/v1/benchmark",
                      params={"asin": args.asin.upper(), "site": args.site}), args.compact)


def cmd_leaderboard(args):
    """类目排行（付费，服务端按次收 leaderboard 单价）。

    服务端没有该查询的 quote 握手，收费在返回结果时发生，所以本地必须先报价
    再要求 --confirm，与其余付费命令的「先报价后确认」纪律保持一致。
    """
    if not args.confirm:
        price = unit_price("leaderboard")
        quote = {
            "confirmationRequired": True,
            "category": args.category, "site": args.site, "by": args.by,
            "message": "类目排行为付费查询；用户确认后追加 --confirm 执行并扣点。"
                       "类目无数据时不收费。",
        }
        if price is not None:
            quote["price"] = price
        else:
            quote["priceNote"] = "未能读取当前定价，以后台实时定价为准。"
        emit({"success": True, "data": quote, "links": links()}, args.compact)
        return
    emit(request_json("GET", "/api/v1/leaderboard",
                      params={"site": args.site, "category": args.category,
                              "by": args.by, "limit": args.limit}), args.compact)


def cmd_workbench(args):
    """差评工作台：默认列差评（免费）；--history 看建议存档；--set-status 更新处理状态。"""
    if args.set_status:
        if not args.review_id:
            emit(error_obj("ARI_VALIDATION_ERROR", 0, "--set-status 需要 --review-id",
                           "先用 workbench 列差评拿到 reviewId。"), args.compact)
            return
        emit(request_json("PUT", "/api/v1/workbench/reviews/%d/status" % args.review_id,
                          {"status": args.set_status}), args.compact)
        return
    if args.history:
        emit(request_json("GET", "/api/v1/workbench/advices",
                          params={"asin": (args.asin or "").upper(), "q": args.query,
                                  "limit": args.limit}), args.compact)
        return
    params = {"asin": (args.asin or "").upper(), "site": args.site,
              "status": args.status, "sort": args.sort}
    if args.new_only:
        params["newOnly"] = "1"
    out = request_json("GET", "/api/v1/workbench/reviews", params=params)
    # stats 随列表一起回（pending / newThisWeek / doneMonth / doneTotal）——
    # 汇报时先说数字再说条目，用户才知道自己在推进而不是面对无尽列表。
    emit(out, args.compact)


def cmd_advise(args):
    """为单条差评生成 AI 回复/处理建议（付费，SSE 流式）。"""
    quote = request_json("POST", "/api/v1/analysis/quote", {"type": "advise"})
    if not ok(quote):
        emit(quote, args.compact)
        return
    q_data = data_of(quote) or {}
    if not args.confirm:
        emit({"success": True, "data": {
            "confirmationRequired": True, "reviewId": args.review_id, "quote": q_data,
            "message": "用户确认后追加 --confirm 生成建议并扣点。",
        }, "links": links()}, args.compact)
        return
    if not q_data.get("sufficient", True):
        emit(error_obj("ARI_INSUFFICIENT_CREDITS", 402, "积点不足",
                       "需要 %s 点，当前余额 %s；请充值后重试。" %
                       (q_data.get("price") or q_data.get("basePrice"),
                        q_data.get("balance"))), args.compact)
        return
    emit(request_sse("/api/v1/workbench/advise", {"reviewId": args.review_id}),
         args.compact)


def cmd_export(args):
    """导出评论 CSV 或报告 HTML/Markdown 到本地文件（付费套餐功能，不扣积点）。"""
    if args.report_id:
        fmt = args.format or "md"
        dest = args.out or ("ari_report_%d.%s" % (args.report_id,
                                                  "html" if fmt == "html" else "md"))
        emit(request_download("/api/v1/export/reports/%d" % args.report_id,
                              {"format": fmt}, dest), args.compact)
        return
    if not args.asin:
        emit(error_obj("ARI_VALIDATION_ERROR", 0, "需要 --asin 或 --report-id",
                       "export --asin <ASIN> 导出评论 CSV；export --report-id <ID> "
                       "导出报告（--format md|html）。"), args.compact)
        return
    dest = args.out or ("ari_reviews_%s.csv" % args.asin.upper())
    emit(request_download("/api/v1/export/reviews",
                          {"asin": args.asin.upper(), "site": args.site}, dest),
         args.compact)


ASIN_RE = re.compile(r"^[A-Z0-9]{10}$")
# 文档示例里的占位 ASIN：格式合法但必然不是真实商品，单独拦截并给出明确指引。
PLACEHOLDER_ASINS = {"B0XXXXXXXX", "B0AAAAAAAA", "B0BBBBBBBB"}


def check_asin_args(args):
    """本地快速失败：格式错误的 ASIN 不值得打到服务端换一个模糊的 4xx。

    ASIN 只保证 10 位字母数字，不保证以 B 开头（书类沿用 ISBN-10，数字开头），
    所以校验不能写死 B 前缀。顺手把值归一成大写，后续命令不必再 upper()。
    """
    for attr in ("asin", "competitor"):
        value = getattr(args, attr, None)
        if value in (None, ""):
            continue
        normalized = str(value).strip().upper()
        if not ASIN_RE.match(normalized) or normalized in PLACEHOLDER_ASINS:
            emit(error_obj(
                "ARI_INVALID_ASIN", 0,
                "%s 不是有效的 ASIN（应为 10 位字母数字，如 B08N5WRWNW）" % value,
                "请从商品详情页 URL 的 /dp/ 后复制真实 ASIN；文档中的占位符示例不能直接使用。"),
                args.compact)
            raise SystemExit(2)
        setattr(args, attr, normalized)


def cmd_version(args):
    emit({"success": True, "data": {
        "skillVersion": VERSION,
        "channel": CHANNEL or "official",
        "python": sys.version.split()[0],
    }}, args.compact)


def add_analysis_args(parser, include_type=True):
    if include_type:
        parser.add_argument("--type", required=True, choices=ANALYSIS_TYPES)
    parser.add_argument("--asin", required=True)
    parser.add_argument("--site", default="amz_us", choices=SITES)
    parser.add_argument("--competitor")
    parser.add_argument("--competitor-site", choices=SITES)
    parser.add_argument("--language", default="zh")


def add_operation_args(parser, confirm=False):
    parser.add_argument("--asin", required=True)
    parser.add_argument("--site", default="amz_us", choices=SITES)
    parser.add_argument("--workflow")
    parser.add_argument("--focus")
    parser.add_argument("--competitor")
    parser.add_argument("--request-id", default="")
    if confirm:
        parser.add_argument("--confirm", action="store_true",
                            help="确认按报价扣点并生成；未提供时只返回报价")


def positive_int(value):
    """Parse a positive integer without imposing a string-format policy."""
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError("必须是正整数")
    if number <= 0:
        raise argparse.ArgumentTypeError("必须是正整数")
    return number


def main():
    # --compact 用 parents 挂到每个子命令上，这样放在子命令前后都能识别。
    # default=SUPPRESS 是必须的：否则子解析器会用自己的默认值覆盖掉
    # 已经在顶层解析出来的 --compact。缺省值只能在 parse_args 之后补，
    # 不能用 set_defaults——parents 共享同一个 action 对象，
    # set_defaults 会把 SUPPRESS 改掉，反而把覆盖问题带回来。
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--compact", action="store_true",
                        default=argparse.SUPPRESS, help="输出单行 JSON")

    ap = argparse.ArgumentParser(prog="ari.py", parents=[common],
                                 description="ARI Amazon 评论采集与智能分析 CLI")
    sub = ap.add_subparsers(dest="command", required=True)

    p = sub.add_parser("setup", parents=[common],
                       help="浏览器一键授权，自动获取并保存 API Key（推荐首次使用）")
    p.set_defaults(fn=cmd_setup)

    p = sub.add_parser("configure", parents=[common], help="隐藏输入并保存 ARI API Key")
    p.set_defaults(fn=cmd_configure)

    p = sub.add_parser("check", parents=[common], help="验证 Key、账户和积点余额")
    p.set_defaults(fn=cmd_check)

    p = sub.add_parser("autoconfirm", parents=[common],
                       help="免确认阈值：autoconfirm 50 / autoconfirm off / autoconfirm default；不带参数查看")
    p.add_argument("value", nargs="?", default="")
    p.set_defaults(fn=cmd_autoconfirm)

    p = sub.add_parser("version", parents=[common], help="显示 Skill 版本与渠道（无需 Key）")
    p.set_defaults(fn=cmd_version)

    p = sub.add_parser("products", parents=[common], help="列出当前账户订阅的 ASIN")
    p.set_defaults(fn=cmd_products)

    p = sub.add_parser("collect", parents=[common], help="采集报价或提交采集任务")
    p.add_argument("--asin", required=True)
    p.add_argument("--site", default="amz_us", choices=SITES)
    p.add_argument("--pages", type=int, default=3, choices=range(1, 11), metavar="1..10")
    p.add_argument("--star", default="all_stars",
                   choices=("all_stars", "critical", "positive", "one_star", "two_star",
                            "three_star", "four_star", "five_star"))
    p.add_argument("--sort", default="recent", choices=("recent", "helpful"))
    p.add_argument("--alias", default="")
    p.add_argument("--schedule", default="weekly", choices=("weekly", "manual"),
                   help="新产品默认每周自动采集并扣点；manual 只采本次，已有产品保留计划")
    p.add_argument("--confirm", action="store_true", help="确认扣点并提交")
    p.add_argument("--wait", action="store_true", help="提交后等待任务完成")
    p.add_argument("--interval", type=int, default=3)
    p.add_argument("--timeout", type=int, default=600)
    p.set_defaults(fn=cmd_collect)

    p = sub.add_parser("status", parents=[common], help="查询采集任务状态")
    p.add_argument("--task", required=True)
    p.set_defaults(fn=cmd_status)

    p = sub.add_parser("reviews", parents=[common],
                       help="读取已采集评论（支持高赞差评榜 / 带图 / Vine / 真实购买）")
    p.add_argument("--asin", required=True)
    p.add_argument("--site", default="amz_us", choices=SITES)
    p.add_argument("--star", type=int, choices=range(1, 6), help="单一星级，与 --stars 互斥（优先）")
    p.add_argument("--stars", default="", choices=("", "negative", "positive"),
                   help="negative=1-3星 positive=4-5星")
    p.add_argument("--sort", default="recent",
                   choices=("recent", "helpful", "star_asc", "oldest"),
                   help="helpful=高赞优先（配 --stars negative 即高赞差评榜）")
    p.add_argument("--with-images", action="store_true", help="只看带买家实拍图的评论")
    p.add_argument("--vine", action="store_true", help="只看 Vine 评论")
    p.add_argument("--purchased", action="store_true", help="只看已验证购买")
    p.add_argument("--query")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--topic", default="", help="按话题 key 筛（1.4.7，key 来自 topics 命令）")
    p.set_defaults(fn=cmd_reviews)

    p = sub.add_parser("monitor", parents=[common], help="监控中心总览：评论、商品变化、差评与未读预警（只读免费）")
    p.set_defaults(fn=cmd_monitor)

    p = sub.add_parser("schedule", parents=[common],
                       help="查看/设置定期采集（持续积累的核心开关，设置本身免费）")
    p.add_argument("--set", choices=("manual", "daily", "weekly"),
                   help="不传=只列出当前各产品的采集计划")
    p.add_argument("--asin", help="配合 --set：按 ASIN 定位产品")
    p.add_argument("--site", default="amz_us", choices=SITES)
    p.add_argument("--id", type=int, help="配合 --set：直接给产品 id（比 --asin 精确）")
    p.set_defaults(fn=cmd_schedule)

    p = sub.add_parser("competitors", parents=[common],
                       help="竞品管理：列出/添加/移除（竞品加入后按周自动采集）")
    p.add_argument("--id", type=int, required=True, help="本品的产品 id（products / schedule 可查）")
    p.add_argument("--add", help="要添加的竞品 ASIN")
    p.add_argument("--remove", type=int, help="要移除的竞品行 id")
    p.add_argument("--site", default="amz_us", choices=SITES)
    p.set_defaults(fn=cmd_competitors)

    p = sub.add_parser("topics", parents=[common],
                       help="话题标签：按话题汇总评论 / 看单个话题的趋势、原句与本品 vs 竞品（免费）")
    p.add_argument("--id", type=int, required=True, help="产品 id（products 里的 id，本品或竞品行都行）")
    p.add_argument("--key", default="", help="话题 key（列表里的 key）；给了就看该话题详情")
    p.add_argument("--dimension", default="",
                   choices=("", "negative", "positive", "expect", "scene", "behavior", "moment", "location", "motive"),
                   help="只看某一维度：negative 差评 / positive 好评 / expect 期望 / scene 场景 …")
    p.add_argument("--days", type=int, default=0, help="只统计最近 N 天，0=全部")
    p.add_argument("--lang", default="zh", choices=("zh", "en"), help="标签洞察摘要语言")
    p.set_defaults(fn=cmd_topics)

    p = sub.add_parser("radar", parents=[common],
                       help="类目雷达：本品 vs 竞品的周走势对比（免费）")
    p.add_argument("--id", type=int, required=True, help="本品的产品 id")
    p.add_argument("--weeks", type=int, default=12, help="回看周数，默认 12")
    p.set_defaults(fn=cmd_radar)

    p = sub.add_parser("charts", parents=[common],
                       help="读取免费星级、趋势、关键词和流向数据")
    p.add_argument("--asin", required=True)
    p.add_argument("--site", default="amz_us", choices=SITES)
    p.add_argument("--days", type=int, default=0, help="0=全部历史")
    p.set_defaults(fn=cmd_charts)

    p = sub.add_parser("quote", parents=[common], help="查询 AI 分析报价（不扣点）")
    add_analysis_args(p)
    p.set_defaults(fn=cmd_quote)

    p = sub.add_parser("analyze", parents=[common], help="AI 分析报价或确认生成")
    add_analysis_args(p)
    p.add_argument("--confirm", action="store_true", help="确认按报价扣点并生成")
    p.set_defaults(fn=cmd_analyze)

    watch_parser = sub.add_parser(
        "watch", parents=[common], help="管理商品监控（每次刷新按频率扣点；摘要/事件/趋势读取 0 积点）"
    )
    watch_sub = watch_parser.add_subparsers(dest="watch_command", required=True)

    p = watch_sub.add_parser("list", parents=[common], help="列出当前账户的 watch")
    p.set_defaults(fn=cmd_watch_list)

    p = watch_sub.add_parser("quote", parents=[common], help="读取商品监控各频率单价与月估算（0 积点）")
    p.set_defaults(fn=cmd_watch_quote)

    p = watch_sub.add_parser("create", parents=[common], help="创建商品监控（开启即按刷新次数扣点）")
    p.add_argument("--asin", required=True)
    p.add_argument("--site", default="amz_us", choices=SITES)
    p.add_argument("--competitor", help="已授权竞品 ASIN；与 --asin 主品组成账户级监控关系")
    p.add_argument("--schedule", default="weekly", choices=WATCH_SCHEDULES)
    p.add_argument("--accept-price", type=positive_int,
                   help="用户已确认的每次刷新单价（来自 watch quote 的 perRefresh）")
    p.add_argument("--disabled", action="store_true", help="创建后保持暂停（不扣点）")
    p.set_defaults(fn=cmd_watch_create)

    p = watch_sub.add_parser("pause", parents=[common], help="暂停 watch 调度（暂停期间不扣点）")
    p.add_argument("--watch-id", required=True, type=positive_int)
    p.set_defaults(fn=cmd_watch_pause)

    p = watch_sub.add_parser("resume", parents=[common], help="恢复 watch 调度（恢复即按刷新次数扣点）")
    p.add_argument("--watch-id", required=True, type=positive_int)
    p.add_argument("--accept-price", type=positive_int,
                   help="用户已确认的每次刷新单价（来自 watch quote 的 perRefresh）")
    p.set_defaults(fn=cmd_watch_resume)

    p = watch_sub.add_parser("series", parents=[common], help="读取价格 / BSR / 评分日序列（0 积点）")
    p.add_argument("--watch-id", required=True, type=positive_int)
    p.add_argument("--days", type=positive_int, default=90)
    p.set_defaults(fn=cmd_watch_series)

    p = watch_sub.add_parser("delete", parents=[common], help="删除 watch（不删除共享数据）")
    p.add_argument("--watch-id", required=True, type=positive_int)
    p.set_defaults(fn=cmd_watch_delete)

    p = watch_sub.add_parser("digest", parents=[common], help="读取确定性 watch 摘要（0 积点）")
    p.add_argument("--watch-id", required=True, type=positive_int)
    p.add_argument("--period", default="7d", choices=("7d", "30d"))
    p.set_defaults(fn=cmd_watch_digest)

    p = watch_sub.add_parser("events", parents=[common], help="读取 watch 变化事件")
    p.add_argument("--watch-id", required=True, type=positive_int)
    p.add_argument("--limit", type=positive_int, default=50)
    p.set_defaults(fn=cmd_watch_events)

    operations_parser = sub.add_parser(
        "operations", parents=[common], help="商品运营工具：能力、资料、报价、运行与状态")
    operations_sub = operations_parser.add_subparsers(dest="operations_command", required=True)

    p = operations_sub.add_parser("capabilities", parents=[common], help="查看运营能力与套餐限制")
    p.set_defaults(fn=cmd_operation_capabilities)

    p = operations_sub.add_parser("profile", parents=[common], help="读取商品资料与字段完整度")
    p.add_argument("--asin", required=True)
    p.add_argument("--site", default="amz_us", choices=SITES)
    p.set_defaults(fn=cmd_operation_profile)

    p = operations_sub.add_parser("quote", parents=[common], help="运营分析报价（不扣点）")
    add_operation_args(p)
    p.set_defaults(fn=cmd_operation_quote)

    p = operations_sub.add_parser("run", parents=[common], help="报价或确认运行运营分析")
    add_operation_args(p, confirm=True)
    p.set_defaults(fn=cmd_operation_run)

    p = operations_sub.add_parser("status", parents=[common], help="按 requestId 精确查询运营任务")
    p.add_argument("--request-id", required=True)
    p.set_defaults(fn=cmd_operation_status)

    p = sub.add_parser("voc", parents=[common], help="一键采集并生成 VOC 报告")
    p.add_argument("asin", help="Amazon ASIN")
    p.add_argument("--site", default="amz_us", choices=SITES)
    p.add_argument("--pages", type=int, default=3, choices=range(1, 11), metavar="1..10")
    p.add_argument("--language", default="zh")
    p.add_argument("--confirm", action="store_true", help="确认采集与 VOC 分析的总报价")
    p.add_argument("--interval", type=int, default=3)
    p.add_argument("--timeout", type=int, default=600)
    p.set_defaults(fn=cmd_voc)

    p = sub.add_parser("deepdive", parents=[common],
                       help="产品、图表、评论、报告与 VOC 报价/分析")
    p.add_argument("--asin", required=True)
    p.add_argument("--site", default="amz_us", choices=SITES)
    p.add_argument("--days", type=int, default=0, help="0=全部历史，与 charts 保持一致")
    p.add_argument("--report-limit", type=int, default=10)
    p.add_argument("--language", default="zh")
    p.add_argument("--confirm", action="store_true", help="确认 VOC 报价并生成")
    p.set_defaults(fn=cmd_deepdive)

    p = sub.add_parser("alerts", parents=[common], help="情感预警列表（免费）")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--mark-read", action="store_true", help="把全部未读预警置为已读")
    p.set_defaults(fn=cmd_alerts)

    p = sub.add_parser("benchmark", parents=[common], help="类目对标概览（免费）")
    p.add_argument("--asin", required=True)
    p.add_argument("--site", default="amz_us", choices=SITES)
    p.set_defaults(fn=cmd_benchmark)

    p = sub.add_parser("leaderboard", parents=[common],
                       help="类目排行（付费，需 --confirm）")
    p.add_argument("--category", required=True)
    p.add_argument("--site", default="amz_us", choices=SITES)
    p.add_argument("--by", default="new30", choices=("new30", "neg_rate", "avg_star"),
                   help="new30=近30天热度 neg_rate=差评率 avg_star=平均星级")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--confirm", action="store_true", help="确认扣点并查询")
    p.set_defaults(fn=cmd_leaderboard)

    p = sub.add_parser("workbench", parents=[common],
                       help="差评工作台：列差评/建议存档/更新处理状态（免费）")
    p.add_argument("--asin")
    p.add_argument("--site", default="", help="留空为全部站点")
    p.add_argument("--status", default="",
                   choices=("", "pending", "contacted", "appealed", "improving", "archived"))
    p.add_argument("--sort", default="severity", choices=("severity", "recent", "arrived"),
                   help="severity=高赞与低星优先（默认，最伤转化的排前面）")
    p.add_argument("--new-only", action="store_true", help="只看近 7 天新入库的差评")
    p.add_argument("--history", action="store_true", help="列历史 AI 建议存档")
    p.add_argument("--query", default="", help="配合 --history 搜索")
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--review-id", type=int, help="配合 --set-status 指定差评")
    p.add_argument("--set-status",
                   choices=("pending", "contacted", "appealed", "improving", "archived"),
                   help="更新该差评的处理状态")
    p.set_defaults(fn=cmd_workbench)

    p = sub.add_parser("advise", parents=[common],
                       help="为单条差评生成 AI 回复建议（付费，需 --confirm）")
    p.add_argument("--review-id", type=int, required=True,
                   help="workbench 列表里的 reviewId")
    p.add_argument("--confirm", action="store_true", help="确认扣点并生成")
    p.set_defaults(fn=cmd_advise)

    p = sub.add_parser("export", parents=[common],
                       help="导出评论 CSV 或报告 HTML/MD（付费套餐功能，不扣积点）")
    p.add_argument("--asin", help="导出该 ASIN 的评论 CSV")
    p.add_argument("--site", default="amz_us", choices=SITES)
    p.add_argument("--report-id", type=int, help="导出该报告（与 --asin 二选一）")
    p.add_argument("--format", choices=("md", "html"), help="报告导出格式，默认 md")
    p.add_argument("--out", help="输出文件路径，默认当前目录自动命名")
    p.set_defaults(fn=cmd_export)

    p = sub.add_parser("reports", parents=[common], help="列出归档报告")
    p.add_argument("--asin")
    p.add_argument("--type")
    p.add_argument("--starred", action="store_true")
    p.add_argument("--query")
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(fn=cmd_reports)

    p = sub.add_parser("report", parents=[common], help="读取单份归档报告")
    p.add_argument("--id", type=int, required=True)
    p.set_defaults(fn=cmd_report)

    args = ap.parse_args()
    if not hasattr(args, "compact"):
        args.compact = False
    # 专属包的运行期兜底闸。打包脚本（scripts/build_skill_variants.py）已把
    # 未承诺的命令从本文件整段删掉，这里再按 skill-defaults.json 的
    # allowedCommands 复核一次——只删代码不留闸的话，把命令加回来就绕过了收窄。
    allowed = allowed_commands()
    if allowed is not None and getattr(args, "command", None) not in allowed:
        emit(error_obj(
            "ARI_COMMAND_NOT_ALLOWED", 0,
            "本包不提供 %s 命令" % getattr(args, "command", "?"),
            "此 Skill 只提供：%s。需要其他能力请安装对应的 ARI Skill 包。" %
            "、".join(sorted(allowed))), args.compact)
        raise SystemExit(2)
    check_asin_args(args)
    args.fn(args)
    raise SystemExit(_exit_code)


if __name__ == "__main__":
    main()
