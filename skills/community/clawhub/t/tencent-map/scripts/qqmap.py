#!/usr/bin/env python3
"""腾讯位置服务 WebService API 命令行工具（零依赖，仅标准库）。

环境变量:
    QQMAP_KEY   腾讯位置服务 Key（lbs.qq.com 免费申请，产品选 WebServiceAPI）

子命令:
    geocode <地址>                    地址 → 坐标
    regeo <lat,lng>                   坐标 → 地址（注意腾讯是 纬度,经度 顺序）
    search <关键词> <城市>            POI 搜索
    suggestion <关键词> <城市>        输入联想
    driving <起点lat,lng> <终点lat,lng>   驾车路线
    walking <起点lat,lng> <终点lat,lng>   步行路线
    ip [ip地址]                       IP 定位
    call <path> k=v [k=v...]          通用调用任意 /ws/ 接口

示例:
    export QQMAP_KEY=你的key
    python3 qqmap.py geocode "北京市海淀区中关村"
    python3 qqmap.py search 咖啡 北京
"""
import json
import os
import sys
import urllib.parse
import urllib.request

BASE = "https://apis.map.qq.com"


def die(msg: str) -> None:
    print(f"错误: {msg}", file=sys.stderr)
    sys.exit(1)


def api(path: str, **params) -> dict:
    key = os.environ.get("QQMAP_KEY") or die("未设置 QQMAP_KEY（lbs.qq.com 申请）")
    params["key"] = key
    url = f"{BASE}{path}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=20) as resp:
        r = json.loads(resp.read())
    if r.get("status") != 0:
        die(f"API 失败: status={r.get('status')} {r.get('message')} "
            "(301=参数缺失 311=key格式错误 306=配额/签名问题)")
    return r


def out(r: dict) -> None:
    print(json.dumps(r, ensure_ascii=False, indent=1))


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    cmd, rest = args[0], args[1:]

    if cmd == "geocode":
        rest or die("用法: geocode <地址>")
        out(api("/ws/geocoder/v1/", address=rest[0]))
    elif cmd == "regeo":
        rest or die("用法: regeo <lat,lng>")
        out(api("/ws/geocoder/v1/", location=rest[0]))
    elif cmd == "search":
        len(rest) >= 2 or die("用法: search <关键词> <城市>")
        out(api("/ws/place/v1/search", keyword=rest[0],
                boundary=f"region({rest[1]},0)", page_size=10))
    elif cmd == "suggestion":
        len(rest) >= 2 or die("用法: suggestion <关键词> <城市>")
        out(api("/ws/place/v1/suggestion", keyword=rest[0], region=rest[1]))
    elif cmd in ("driving", "walking"):
        len(rest) >= 2 or die(f"用法: {cmd} <起点lat,lng> <终点lat,lng>")
        out(api(f"/ws/direction/v1/{cmd}/", **{"from": rest[0], "to": rest[1]}))
    elif cmd == "ip":
        out(api("/ws/location/v1/ip", **({"ip": rest[0]} if rest else {})))
    elif cmd == "call":
        rest or die("用法: call <path> k=v [k=v...]")
        params = dict(kv.split("=", 1) for kv in rest[1:])
        out(api(rest[0], **params))
    else:
        die(f"未知子命令: {cmd}（运行不带参数查看帮助）")


if __name__ == "__main__":
    main()
