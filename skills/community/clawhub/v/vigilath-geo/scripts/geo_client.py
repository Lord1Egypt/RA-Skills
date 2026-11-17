#!/usr/bin/env python3
"""Vigilath GEO agent 轻客户端 —— 让宿主 agent(小龙虾)链接 Vigilath GEO agent。

零三方依赖(纯标准库),drop-in 即用。鉴权走环境变量,token 绝不硬编码/打印。

用法:
  python geo_client.py check https://example.com               # 免登录!GEO+SEO 双体检
  python geo_client.py check https://example.com --no-seo      # 只要 GEO
  python geo_client.py check https://example.com --seo-only    # 只要 SEO
  python geo_client.py mention 你的品牌名 商用清洁机器人             # 免登录!拿品牌去问 AI,贴回原话
  python geo_client.py wallet                                  # 看余额(花钱前先看)
  python geo_client.py topup 100                               # 充值:拿付款要求
  python geo_client.py industry                                # 免登录!已建库的行业清单
  python geo_client.py industry 商用清洁机器人                  # 免登录!该行业 AI 里谁是 TOP1
  python geo_client.py chat "今天投放效果怎么样?"
  python geo_client.py data today          # today / coverage / report ...
  python geo_client.py capabilities        # 当前 token 能做什么
  python geo_client.py login               # 重新授权(设备码,token 过期/换账号时用)

凭证来源(优先级:环境变量 > ~/.vigilath/config):
  VIGILATH_AGENT_TOKEN   1 年期账号 token(Vigilath 领号发放),必填
  VIGILATH_BASE          选填,默认 https://vigilath.cn/api/agent/v1
一行安装(install.sh)会把 token 写进 ~/.vigilath/config,装完直接可用、无需设环境变量。
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


def _load_config() -> dict:
    """读 ~/.vigilath/config(KEY=VALUE 行),给免设环境变量的安装方式用。"""
    cfg: dict[str, str] = {}
    path = os.path.expanduser("~/.vigilath/config")
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    cfg[k.strip()] = v.strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return cfg


_CFG = _load_config()


def _conf(key: str, default: str = "") -> str:
    return (os.environ.get(key) or _CFG.get(key) or default).strip()


BASE = _conf("VIGILATH_BASE", "https://vigilath.cn/api/agent/v1").rstrip("/")
# 匿名检测端点在站点 API 根下(/api/check/anonymous),不在 /agent/v1 里,由 BASE 推出来
SITE_API = BASE[: -len("/agent/v1")] if BASE.endswith("/agent/v1") else BASE


def _die(msg: str, code: int = 1) -> "None":
    print(f"[vigilath-geo] 错误:{msg}", file=sys.stderr)
    sys.exit(code)


def _headers() -> dict:
    token = _conf("VIGILATH_AGENT_TOKEN")
    if not token:
        _die("缺少 token —— 跑一行安装,或设环境变量 VIGILATH_AGENT_TOKEN / 写进 ~/.vigilath/config。")
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def _explain_http(e: urllib.error.HTTPError) -> str:
    try:
        body = e.read().decode("utf-8", "ignore")
    except Exception:  # noqa: BLE001
        body = ""
    hint = {
        401: "token 无效 / 过期 / 已禁用 —— 联系 Vigilath 重发,别重试刷接口。",
        402: "余额不足 —— 这是付费能力。用 `wallet` 看余额、`topup <金额>` 充值;响应里通常带了还需要多少与充值方式,如实转达,别重试刷接口。",
        403: "无权限(能力未授权,或 Origin 不在白名单)。",
        429: "账号配额 / 限速,稍后退避重试。",
    }.get(e.code, "")
    return f"HTTP {e.code} {hint} {body}".strip()


def _request(req: urllib.request.Request, timeout: int):
    try:
        return urllib.request.urlopen(req, timeout=timeout)
    except urllib.error.HTTPError as e:
        _die(_explain_http(e))
    except urllib.error.URLError as e:
        _die(f"连不上 Vigilath({BASE}):{e.reason}")


def chat(message: str) -> dict:
    """对话:流式收 delta + cards,返回 {'text': ..., 'cards': [...]}。"""
    req = urllib.request.Request(
        f"{BASE}/chat",
        method="POST",
        data=json.dumps({"message": message}).encode("utf-8"),
        headers=_headers(),
    )
    text_parts: list[str] = []
    cards: list = []
    with _request(req, timeout=180) as resp:
        for raw in resp:                                  # SSE:逐行 data: {...}
            line = raw.decode("utf-8", "ignore").strip()
            if not line.startswith("data:"):
                continue
            try:
                evt = json.loads(line[5:].strip())
            except json.JSONDecodeError:
                continue
            if "delta" in evt:
                text_parts.append(evt["delta"])
            elif "cards" in evt:
                cards = evt["cards"]
            elif "error" in evt:
                _die(evt["error"])
    return {"text": "".join(text_parts), "cards": cards}


def get(path: str, timeout: int = 30) -> dict:
    """GET 一个只读端点(如 data/today、meta/capabilities)。"""
    req = urllib.request.Request(f"{BASE}/{path.lstrip('/')}", headers=_headers())
    with _request(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def check(url: str, include_seo: bool = True) -> dict:
    """免登录网站体检:GEO 25 类 + SEO 12 类全跑,免费档看 5+3 类明细。

    **不带 token** —— 这是整个 skill 里唯一不需要授权的命令,没装凭证也能跑,不限次数。
    代价:锁住的类目只给数量不给明细、没有修复建议、不写进账号历史。
    """
    body = json.dumps({"url": url, "include_seo": include_seo}).encode("utf-8")
    req = urllib.request.Request(
        f"{SITE_API}/check/anonymous",
        data=body,
        headers={"Content-Type": "application/json"},   # 刻意不带 Authorization
        method="POST",
    )
    # 25+12 类真跑,站点慢时要等;给足超时,别让 agent 误判成宕机
    with _request(req, timeout=180) as resp:
        d = json.loads(resp.read().decode("utf-8"))

    def _half(part: dict) -> dict:
        """把一半结果压成能念给用户的形状:按类目聚合,丢掉 i18n key 等噪音。"""
        cats: dict = {}
        for c in part.get("checks") or []:
            row = cats.setdefault(c["category"], {"pass": 0, "warn": 0, "fail": 0, "info": 0, "items": []})
            row[c["status"].lower()] = row.get(c["status"].lower(), 0) + 1
            row["items"].append({"status": c["status"], "message": c.get("message") or ""})
        return {
            "score": part.get("score"),
            "grade": part.get("grade"),
            "summary": part.get("summary"),
            "visible_categories": cats,
            "locked_count": len(part.get("locked_categories") or []),
            "locked_categories": part.get("locked_categories") or [],
        }

    out = {"url": d.get("url") or url, "tier": d.get("tier"), "geo": _half(d)}
    if d.get("seo"):
        out["seo"] = _half(d["seo"])
    out["note"] = (
        "免登录免费检测,不限次。锁住的类目只给了名字没给明细,也没有修复建议。"
        "要完整明细 + 修复建议:让用户在 Vigilath 注册后跑 `login` 授权。"
        "要知道 AI 引擎实际怎么说这个品牌(被引用率/竞品对比/舆情):那是「一键全面诊断」,"
        "走 `chat`,需要授权,整单 8-20 分钟。"
    )
    return out


def industry(key: str = "") -> dict:
    """免登录:看某个行业在 AI 搜索里谁是 TOP1、集中度多高、哪些问题还没有稳定推荐。

    数据来自平台的真实跑批(不是模型估算),但**只覆盖已建库的行业**,不传 key 时先列有哪些。
    与 check 一样不需要任何凭证。
    """
    if not key:
        req = urllib.request.Request(f"{SITE_API}/industry/list", headers={"Accept": "application/json"})
        with _request(req, timeout=30) as resp:
            d = json.loads(resp.read().decode("utf-8"))
        rows = d.get("industries") or []
        return {
            "industries": rows,
            "note": ("这是已建库的行业清单。挑一个跑 `industry <行业名>` 看详情。"
                     "用户的行业不在里面时,如实说「这个行业还没有建库」,"
                     "**不要拿别的行业的数字替代**;想测他自己的品牌要走需要授权的诊断。"),
        }
    req = urllib.request.Request(
        f"{SITE_API}/industry/{urllib.parse.quote(key)}/data",
        headers={"Accept": "application/json"},
    )
    with _request(req, timeout=60) as resp:
        d = json.loads(resp.read().decode("utf-8"))
    d["note"] = ("免登录、真实跑批数据。`coverage` 等百分比已是最终值,不要再乘 100;"
                 "`series` 是历史走势,`series_keys` 是对应日期。"
                 "这是**行业**层面的数据,不是用户自己品牌的表现 —— 别混说。")
    return d


def _device_id() -> str:
    """本机持久标识,免登录能力按它 + 出口 IP 限次。

    没有就现生成一个写进 ~/.vigilath/config。**即使没有 token 也要能写** ——
    免登录用户根本没有凭证文件,不能因为缺 token 就生成不出标识。
    用户清掉它就重置了设备额度,这是已知的:它只是自然分桶,硬约束在服务端的出口 IP。
    """
    did = _conf("VIGILATH_DEVICE_ID")
    if did:
        return did
    import uuid as _uuid

    did = "dev_" + _uuid.uuid4().hex[:20]
    path = os.path.expanduser("~/.vigilath/config")
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        cfg = dict(_CFG)
        cfg["VIGILATH_DEVICE_ID"] = did
        with open(path, "w", encoding="utf-8") as f:
            f.write("# Vigilath —— 机密,勿提交\n")
            for k, v in cfg.items():
                f.write(f"{k}={v}\n")
        os.chmod(path, 0o600)
    except OSError:
        pass          # 只读环境写不了就每次新生成,服务端还有 IP 这道闸
    _CFG["VIGILATH_DEVICE_ID"] = did
    return did


def mention(brand: str, industry_terms: list, wait: bool = True) -> dict:
    """免登录:拿品牌去问 AI,把**引擎原话**贴回来。3 条品类问题 × 3 个引擎。

    额度按设备 + 出口 IP 计(默认每设备 2 次 / 30 天)——这一条每次都真花引擎成本,
    和 check / industry 那种零成本能力不同。

    服务端是异步的,这里把轮询藏起来:一条命令等结果,体感同同步。
    """
    payload = json.dumps({
        "brand": brand,
        "industry_terms": industry_terms,
        "device_id": _device_id(),
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{SITE_API}/check/mention/anonymous",
        data=payload,
        headers={"Content-Type": "application/json"},   # 刻意不带 Authorization
        method="POST",
    )
    with _request(req, timeout=60) as resp:
        started = json.loads(resp.read().decode("utf-8"))
    if not wait:
        return started

    task_id = started["task_id"]
    print(f"[vigilath] 已发起(剩余额度见 quota),约 1-3 分钟,轮询中…", file=sys.stderr)
    import time as _time

    deadline = _time.time() + 600
    while _time.time() < deadline:
        _time.sleep(6)
        req2 = urllib.request.Request(f"{SITE_API}/check/mention/{task_id}")
        try:
            with _request(req2, timeout=30) as resp:
                d = json.loads(resp.read().decode("utf-8"))
        except Exception:  # noqa: BLE001
            continue        # 网络抖动不该中断轮询
        if d.get("status") == "done":
            out = d.get("result") or {}
            out["quota"] = started.get("quota")
            return out
        if d.get("status") == "failed":
            return {"status": "failed", "error": d.get("error") or "未知错误",
                    "note": "额度已计入(引擎调用一发出就产生成本),不要立刻重试。"}
    return {"status": "timeout", "task_id": task_id,
            "note": f"等超时了。稍后用 `mention-status {task_id}` 再查,任务还在跑。"}


def wallet() -> dict:
    """看余额。**花钱的动作之前先看一眼** —— 余额不够时早说,别让用户等到失败。"""
    return get("wallet")


def topup(amount_yuan: str, tx_hash: str = "") -> dict:
    """充值。两步:先拿付款要求(402),链上付完再带 tx_hash 回来核销。

    没有 tx_hash 时返回的是「怎么付」;**把里面的金额、收款地址、网络原样念给用户**,
    别自己编。用户也可以选择去网页充值,地址在返回的 web 字段里。
    """
    try:
        cents = int(round(float(amount_yuan) * 100))
    except ValueError:
        _die(f"充值金额要是数字(元),收到:{amount_yuan!r}")
    headers = {"Content-Type": "application/json"}
    if tx_hash:
        import base64 as _b64

        headers["X-PAYMENT"] = _b64.b64encode(
            json.dumps({"tx_hash": tx_hash}).encode("utf-8")
        ).decode("ascii")
    req = urllib.request.Request(
        f"{BASE}/wallet/topup",
        data=json.dumps({"amount_cents": cents}).encode("utf-8"),
        headers={**headers, "Authorization": _headers()["Authorization"]},
        method="POST",
    )
    try:
        with _request(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 402:
            # 402 是这条流程的**正常一步**,不是错误:它带着付款要求
            body = json.loads(e.read().decode("utf-8", "ignore") or "{}")
            body["_hint"] = ("这不是失败 —— 按 accepts 里的网络/资产/收款地址/金额付款,"
                             "拿到交易哈希后重跑:topup <金额> --tx <哈希>。"
                             "或者引导用户到 web 字段给的页面用微信充值。")
            return body
        raise


def login() -> "None":
    """设备码授权:终端出配对码,人在浏览器批准,拿到的 token 写回 ~/.vigilath/config。

    token 过期 / 换账号时用,不必重装 skill。与 install.sh 走的是同一套端点。
    """
    import socket
    import time

    def _post(path: str, payload: dict) -> dict:
        req = urllib.request.Request(
            f"{BASE}/{path}",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},   # 授权前无 token,不能带 Authorization
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))

    try:
        d = _post("device/code", {"client": socket.gethostname()})
    except Exception as e:  # noqa: BLE001
        _die(f"连不上 {BASE} —— 检查网络或 VIGILATH_BASE:{e}")
    if d.get("status") != "ok":
        _die(f"起授权流程失败:{d.get('message') or d.get('status')}")

    # 宿主 agent 跑本命令时 stdout 通常是管道 —— 默认全缓冲会把配对码扣在缓冲区里,
    # 用户干等到超时也看不到码。授权靠人肉眼看,所以这里必须行缓冲。
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:  # noqa: BLE001  (老 Python / 非常规 stdout)
        pass

    print("\n请在浏览器完成授权(10 分钟内有效):")
    print(f"    打开:{d.get('verify_url_complete') or d.get('verify_url')}")
    print(f"    配对码:{d['user_code']}\n")
    print("等待批准中…")

    interval = int(d.get("interval") or 5)
    deadline = time.time() + int(d.get("expires_in") or 600)
    token = ""
    while time.time() < deadline:
        time.sleep(interval)
        try:
            r = _post("device/token", {"device_code": d["device_code"]})
        except Exception:  # noqa: BLE001
            continue        # 网络抖动不该中断轮询
        st = r.get("status")
        if st == "approved":
            token = r["token"]
            break
        if st in ("denied", "expired"):
            _die(r.get("message") or f"授权失败:{st}")
    if not token:
        _die("等待授权超时(10 分钟),请重试 login")

    path = os.path.expanduser("~/.vigilath/config")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cfg = dict(_CFG)
    cfg["VIGILATH_AGENT_TOKEN"] = token
    cfg["VIGILATH_BASE"] = BASE
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Vigilath GEO —— 机密,勿提交\n")
        for k, v in cfg.items():
            f.write(f"{k}={v}\n")
    os.chmod(path, 0o600)
    print("✅ 授权成功,凭证已写入 ~/.vigilath/config(权限 600)")


def main(argv: list) -> "None":
    if len(argv) < 2:
        _die('用法:geo_client.py check <网址> | mention <品牌> <行业词> | industry [行业名] | '
             'chat "问题" | data <name> | wallet | topup <金额> | capabilities | login')
    cmd = argv[1]
    if cmd == "chat":
        if len(argv) < 3:
            _die('chat 需要一个问题参数,如:chat "今天投放效果?"')
        out = chat(argv[2])
        print(out["text"].strip())
        if out["cards"]:
            print("\n--- 结构化卡片(把数字念给用户)---")
            print(json.dumps(out["cards"], ensure_ascii=False, indent=2))
    elif cmd == "data":
        if len(argv) < 3:
            _die("data 需要名字:today / coverage / report ...")
        print(json.dumps(get(f"data/{argv[2]}"), ensure_ascii=False, indent=2))
    elif cmd == "check":
        if len(argv) < 3:
            _die("check 需要一个网址,如:check https://example.com")
        # --no-seo 只要 GEO(S1 网站体检);--seo-only 只要 SEO(S10 传统 SEO 体检)
        seo_only = "--seo-only" in argv
        out = check(argv[2], include_seo="--no-seo" not in argv or seo_only)
        if seo_only:
            out = {k: v for k, v in out.items() if k != "geo"}
            out["note"] = (
                "免登录免费 SEO 体检,不限次。12 类全跑,免费档给 3 类明细,其余只给类目名。"
                "SEO 分与 GEO 分是两套独立口径,**不要相加、不要合成综合分**。"
                "想知道 AI 爬虫读不读得懂这个站,那是另一件事,跑 `check <网址> --no-seo`。"
            )
        print(json.dumps(out, ensure_ascii=False, indent=2))
    elif cmd == "mention":
        if len(argv) < 4:
            _die('mention 需要品牌名和至少一个行业词,如:mention "你的品牌名" 商用清洁机器人')
        print(json.dumps(mention(argv[2], [a for a in argv[3:] if not a.startswith("--")]),
                         ensure_ascii=False, indent=2))
    elif cmd == "mention-status":
        if len(argv) < 3:
            _die("mention-status 需要 task_id")
        req = urllib.request.Request(f"{SITE_API}/check/mention/{argv[2]}")
        with _request(req, timeout=30) as resp:
            print(resp.read().decode("utf-8"))
    elif cmd == "wallet":
        print(json.dumps(wallet(), ensure_ascii=False, indent=2))
    elif cmd == "topup":
        if len(argv) < 3:
            _die("topup 需要金额(元),如:topup 100;付款后核销:topup 100 --tx 0x…")
        tx = ""
        if "--tx" in argv:
            i = argv.index("--tx")
            tx = argv[i + 1] if len(argv) > i + 1 else ""
        print(json.dumps(topup(argv[2], tx), ensure_ascii=False, indent=2))
    elif cmd == "industry":
        print(json.dumps(industry(argv[2] if len(argv) > 2 else ""), ensure_ascii=False, indent=2))
    elif cmd == "capabilities":
        print(json.dumps(get("meta/capabilities"), ensure_ascii=False, indent=2))
    elif cmd == "login":
        login()
    else:
        _die(f"未知命令:{cmd}(支持 check / mention / industry / chat / data / wallet / topup / capabilities / login)")


if __name__ == "__main__":
    main(sys.argv)
