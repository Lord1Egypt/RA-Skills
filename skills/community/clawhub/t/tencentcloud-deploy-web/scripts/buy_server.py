#!/usr/bin/env python3
"""帮用户买轻量服务器（Lighthouse）：生成「已预选好」的购买链接，然后自动检测用户什么时候买好。
agent-ops 没有购买权限（这是有意的设计），付款必须由用户本人完成；这个脚本把用户要做的事压到最少。

用法：
    python buy_server.py plan [--size small|medium|large] [--region ap-hongkong]
        → 输出 JSON：推荐套餐、实时价格、预选好的购买链接，以及给用户看的卡片文字（card）
    python buy_server.py wait --bundle <plan 输出的 bundle_id> --since <plan 输出的 plan_at> [--timeout 1800]
        → 每 15 秒查一次，直到出现一台「套餐一致、在 plan 之后创建、状态 RUNNING」的实例；输出它的 ID、IP、到期时间
          （plan 输出里有现成的 wait_cmd，照抄即可；用户在 wait 启动前就买好了也不会漏）
    建议流程：先 plan，把 card 原样发给用户；同时在后台运行 wait。用户付完款，agent 自动接着往下做，
    不需要用户回复"好了"。

套餐选择（中国香港，2026-10-08 实测的价格档位，运行时以 API 实时数据为准）：
    small  ：锐驰型 2核2G 40G   → 静态站、博客、落地页
    medium ：锐驰型 2核4G 60G   → 带后端或数据库的网站（Node/Python + PostgreSQL 等）
    large  ：锐驰型 2核8G 80G   → 多个服务，或者比较吃内存的应用
    永远不推荐「中国香港入门型」：购买页上写明了它不保障大陆与香港之间的网络质量，而购买页默认选的偏偏就是它。
"""
import argparse
import json
from datetime import datetime, timezone
import sys
import time
from pathlib import Path
from urllib.parse import urlencode

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tcapi  # noqa: E402

# 购买页 regionId（2026-10-08 实测：5 = 中国香港，会自动选好可用区）
REGION_ID = {"ap-hongkong": 5}
SIZES = {"small": (2, 2), "medium": (2, 4), "large": (2, 8)}   # (CPU, 内存 GB)
OS_TITLE = "Ubuntu 24.04 LTS"


def pick_bundle(region, size):
    cpu, mem = SIZES[size]
    bs = tcapi.call("lighthouse", "DescribeBundles", {"Limit": 100}, region=region)["BundleSet"]
    ok = [b for b in bs if b.get("BundleSalesState") == "AVAILABLE" and b.get("SupportLinuxUnixPlatform")
          and b["CPU"] == cpu and b["Memory"] == mem and "入门" not in (b.get("BundleTypeDescription") or "")]
    # 优先锐驰型（高峰值带宽、不限流量），其次通用型
    ok.sort(key=lambda b: (0 if "锐驰" in (b.get("BundleTypeDescription") or "") else 1,
                           b["Price"]["InstancePrice"]["DiscountPrice"]))
    if not ok:
        raise SystemExit(json.dumps({"ok": False, "reason": f"{region} 暂时没有 {cpu}核{mem}G 的可售套餐，换个规格试试"},
                                    ensure_ascii=False))
    return ok[0]


def pick_blueprint(region):
    bp = tcapi.call("lighthouse", "DescribeBlueprints",
                    {"Limit": 100, "Filters": [{"Name": "blueprint-type", "Values": ["PURE_OS"]}]},
                    region=region)["BlueprintSet"]
    def title(b):
        return f'{b["DisplayTitle"]} {b.get("DisplayVersion", "")}'.strip()
    for b in bp:
        if title(b) == OS_TITLE:
            b["_title"] = title(b)
            return b
    b = next(b for b in bp if b["DisplayTitle"].startswith("Ubuntu"))
    b["_title"] = title(b)
    return b


def plan(a):
    b, bp = pick_bundle(a.region, a.size), pick_blueprint(a.region)
    price = b["Price"]["InstancePrice"]["DiscountPrice"]
    url = "https://buy.cloud.tencent.com/lighthouse?" + urlencode({
        "blueprintType": "PURE_OS", "blueprintOfficialId": bp["BlueprintId"],
        "regionId": REGION_ID.get(a.region, 5), "bundleId": b["BundleId"]})
    spec = f'{b["CPU"]}核{b["Memory"]}G · {b["SystemDiskSize"]}GB 硬盘 · {b["InternetMaxBandwidthOut"]}Mbps'
    card = f"""🧑 需要你买一台服务器（约 3 分钟，需要付款）
我已经把配置都选好了，你只需要点链接、付钱：

👉 {url}

打开后请确认页面上是这样的（都已经帮你选好了，不需要改）：
  · 创建方式：基于操作系统镜像 → Ubuntu → {bp["_title"]}
  · 地域：中国香港（不需要备案）
  · 套餐：{b.get("BundleTypeDescription")} {spec}，约 ¥{price:g}/月
  · 登录方式：保持「自动生成密码」就行（我不需要这个密码，我有自己的管理通道）

你只需要做 4 件事：
  1. 页面最下方「时长」：先选 1 个月试用（满意的话以后可以改成包年，更便宜）
  2. 「自动续费」：建议勾上，以免到期后网站停掉。不勾也行，到期前我会提醒你
  3. 勾选「我已阅读并同意《腾讯云服务协议》…」
  4. 点右下角「立即购买」，然后按页面提示付款（微信支付等）

⚠️ 如果页面上选中的是「中国香港入门型」，请手动点回「{b.get("BundleTypeDescription")}」——入门型从大陆访问会很慢。
⚠️ 登录腾讯云时，用你的主账号（就是注册时那个微信/邮箱），不要用子账号。
⚠️ 页面上的价格如果和这里不一样（比如新用户优惠），以页面为准。

付完款不用回复我，我会自动发现新服务器，然后接着部署。"""
    plan_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out = {"ok": True, "plan_at": plan_at,
           "wait_cmd": f"python buy_server.py wait --bundle {b['BundleId']} --since {plan_at} --region {a.region}",
           "url": url, "bundle_id": b["BundleId"], "bundle": b.get("BundleTypeDescription"),
           "spec": spec, "price_month": price, "blueprint_id": bp["BlueprintId"], "os": bp["_title"],
           "card": card}
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


def list_ids(region):
    r = tcapi.call("lighthouse", "DescribeInstances", {"Limit": 100}, region=region)
    return {i["InstanceId"]: i for i in r.get("InstanceSet", [])}


def wait(a):
    since = datetime.strptime(a.since, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc) if a.since else None
    before = set() if since else set(list_ids(a.region))   # 没给 --since 时退回"新出现的实例"

    def created(i):
        try:
            return datetime.strptime(i.get("CreatedTime", ""), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        except ValueError:
            return None

    deadline = time.time() + a.timeout
    while time.time() < deadline:
        try:
            now = list_ids(a.region)
        except tcapi.TcError:
            now = {}
        cands = [i for k, i in now.items() if k not in before
                 and (not a.bundle or i.get("BundleId") == a.bundle)
                 and (not since or (created(i) and created(i) >= since))]
        running = sorted([i for i in cands if i.get("InstanceState") == "RUNNING"], key=lambda i: i.get("CreatedTime", ""))
        if running:
            i = running[-1]
            print(json.dumps({"ok": True, "instance_id": i["InstanceId"], "ip": (i.get("PublicAddresses") or [""])[0],
                              "bundle_id": i.get("BundleId"), "os": i.get("OsName"), "created": i.get("CreatedTime"),
                              "expired_time": i.get("ExpiredTime"), "renew_flag": i.get("RenewFlag"),
                              "also_matched": [x["InstanceId"] for x in running[:-1]]},
                             ensure_ascii=False, indent=1))
            return 0
        time.sleep(15)
    print(json.dumps({"ok": False, "reason": "timeout",
                      "say": "我还没看到新服务器。买好了吗？如果已经付款，可能要等一两分钟才能开好，我可以再等一会儿。"},
                     ensure_ascii=False))
    return 1


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["plan", "wait"])
    ap.add_argument("--size", choices=list(SIZES), default="small")
    ap.add_argument("--region", default="ap-hongkong")
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--bundle", help="wait：只认这个套餐（用 plan 输出的 bundle_id）")
    ap.add_argument("--since", help="wait：只认这个 UTC 时间之后创建的实例（用 plan 输出的 plan_at）")
    a = ap.parse_args()
    try:
        return plan(a) if a.cmd == "plan" else wait(a)
    except tcapi.TcError as e:
        print(json.dumps({"ok": False, **tcapi.error_report(e)}, ensure_ascii=False, indent=1))
        return 1


if __name__ == "__main__":
    sys.exit(main())
