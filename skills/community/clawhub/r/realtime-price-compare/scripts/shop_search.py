#!/usr/bin/env python3
"""电商商品搜索与比价（可搜平台由服务端渠道决定）：把参数发给购物推荐服务，原样输出结果 JSON。

用法（参数见技能说明，JSON 对象）：
  python3 shop_search.py '{"keywords":["降噪蓝牙耳机"],"budget_max_minor":30000,"limit":2}'
  python3 shop_search.py --file args.json      # 参数写在 UTF-8 文件里（引号难转义时用）
  echo '{...}' | python3 shop_search.py -      # 从标准输入读

输出：始终是一行 JSON（stdout）。服务端结果原样输出；脚本自身出错时输出
{"result_status":"error","error":{"code":...,"message":...,"retryable":...}}。
退出码：0 拿到服务端结果（含服务端返回的 error）；1 参数有误；2 网络或服务不可用。
只用 Python 标准库，不需要安装依赖，也不需要密钥。

数据与安全说明：
- 唯一的网络请求：把调用参数（商品关键词、预算、条件、用户原话等购物需求）以 HTTPS POST
  发给本技能作者运营的“购物推荐服务”（地址见 API_URL，即作者的服务器），由服务返回商品、
  到手价和购买链接。
- 不读取本机文件（--file 只读用户指定的参数文件）、不读环境中的密钥或账号、不上传任何个人信息，
  不执行服务端返回的任何内容，只把结果 JSON 原样打印。
- 可用环境变量 SHOP_SEARCH_API_URL 改成自己部署的同一服务地址。
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

# 购物推荐服务地址（本技能作者的服务器，只接收购物搜索参数）
API_URL = os.environ.get("SHOP_SEARCH_API_URL") or "https://47.100.160.98/commerce/api/pub/dumate-skill-1/recommend"
SKILL_NAME = "realtime-price-compare"
VERSION = "1.0.0"
TIMEOUT_SEC = 30
RETRY_STATUS = {502, 503, 504}


def emit(obj, code):
    sys.stdout.write(json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n")
    sys.stdout.flush()
    sys.exit(code)


def fail(code, message, retryable, exit_code):
    emit({"result_status": "error", "error": {"code": code, "message": message, "retryable": retryable}}, exit_code)


def read_args(argv):
    if len(argv) == 2 and argv[1] == "-":
        raw = sys.stdin.read()
    elif len(argv) == 3 and argv[1] == "--file":
        try:
            with open(argv[2], encoding="utf-8-sig") as f:
                raw = f.read()
        except OSError as e:
            fail("INVALID_ARGUMENT", f"读不到参数文件：{e}", False, 1)
    elif len(argv) == 2 and not argv[1].startswith("-"):
        raw = argv[1]
    else:
        fail("INVALID_ARGUMENT", "用法：shop_search.py '<JSON 参数>' | --file <文件> | -（标准输入）", False, 1)
    try:
        args = json.loads(raw)
    except ValueError as e:
        fail("INVALID_ARGUMENT", f"参数不是合法 JSON：{e}", False, 1)
    if not isinstance(args, dict):
        fail("INVALID_ARGUMENT", "参数必须是 JSON 对象，如 {\"keywords\":[\"电动牙刷\"]}", False, 1)
    return args


def post(body):
    req = urllib.request.Request(
        API_URL,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
            "User-Agent": f"{SKILL_NAME}/{VERSION} python/{sys.version_info[0]}.{sys.version_info[1]}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SEC) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # Windows 控制台默认编码输出中文会报错
    except (AttributeError, ValueError):
        pass
    if API_URL.startswith("__"):
        fail("SCRIPT_NOT_CONFIGURED", "脚本未配置服务地址（打包时未替换），请重新安装技能", False, 2)
    body = json.dumps(read_args(argv), ensure_ascii=False).encode("utf-8")

    status, data = None, b""
    for attempt in range(2):
        try:
            status, data = post(body)
        except TimeoutError:
            fail("SCRIPT_TIMEOUT", f"购物推荐服务 {TIMEOUT_SEC} 秒未响应", True, 2)
        except urllib.error.URLError as e:
            if isinstance(e.reason, TimeoutError):
                fail("SCRIPT_TIMEOUT", f"购物推荐服务 {TIMEOUT_SEC} 秒未响应", True, 2)
            if attempt == 0:
                time.sleep(1)
                continue
            fail("SCRIPT_NETWORK_ERROR", f"连不上购物推荐服务：{e.reason}", True, 2)
        if status in RETRY_STATUS and attempt == 0:
            time.sleep(1)
            continue
        break

    try:
        result = json.loads(data.decode("utf-8"))
    except ValueError:
        result = None
    # 服务端结果（含 429 限流、参数错误等 error 结果）原样输出
    if isinstance(result, dict) and "result_status" in result:
        emit(result, 0)
    if status == 404:
        fail("SCRIPT_NOT_AVAILABLE", "购物推荐服务暂未开放该入口（HTTP 404）", False, 2)
    fail("SCRIPT_NETWORK_ERROR", f"购物推荐服务暂时不可用（HTTP {status}）", True, 2)


if __name__ == "__main__":
    main(sys.argv)
