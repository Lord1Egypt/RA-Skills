#!/usr/bin/env python3
"""企业微信群机器人命令行工具（零依赖，仅标准库）。

环境变量:
    WECOM_WEBHOOK_KEY   群机器人 Webhook 的 key（添加机器人后 URL 里的 key= 部分）

子命令:
    text <内容> [@userid,userid|@all]   发文本（@all 提醒所有人）
    markdown <md文件或内容>             发 markdown 消息
    image <图片文件>                    发图片（自动算 base64+md5，≤2MB）
    file <文件路径>                     发文件（先上传临时素材再发送，≤20MB）

示例:
    export WECOM_WEBHOOK_KEY=693a91f6-7xxx-4bc4-97a0-0ec2sifa5aaa
    python3 wecombot.py text "部署完成 ✅" @all
    python3 wecombot.py markdown report.md
    python3 wecombot.py image chart.png
"""
import base64
import hashlib
import json
import mimetypes
import os
import sys
import time
import urllib.request

BASE = "https://qyapi.weixin.qq.com/cgi-bin/webhook"


def die(msg: str) -> None:
    print(f"错误: {msg}", file=sys.stderr)
    sys.exit(1)


def key() -> str:
    return os.environ.get("WECOM_WEBHOOK_KEY") or die("未设置 WECOM_WEBHOOK_KEY")


def post(url: str, data: bytes, ctype: str) -> dict:
    req = urllib.request.Request(url, data, {"Content-Type": ctype})
    with urllib.request.urlopen(req, timeout=30) as resp:
        r = json.loads(resp.read())
    if r.get("errcode") != 0:
        # 93000=webhook key无效 45009=接口超限(每机器人20条/分钟)
        die(f"API 失败: {r}")
    return r


def send(body: dict) -> None:
    post(f"{BASE}/send?key={key()}",
         json.dumps(body, ensure_ascii=False).encode("utf-8"),
         "application/json")
    print(json.dumps({"errcode": 0, "errmsg": "ok"}, ensure_ascii=False))


def read_arg_or_file(v: str) -> str:
    return open(v, encoding="utf-8").read() if os.path.isfile(v) else v


def upload_file(filepath: str) -> str:
    os.path.isfile(filepath) or die(f"文件不存在: {filepath}")
    boundary = "----wecombotboundary%d" % int(time.time())
    fname = os.path.basename(filepath)
    ctype = mimetypes.guess_type(fname)[0] or "application/octet-stream"
    raw = open(filepath, "rb").read()
    parts = (
        f"--{boundary}\r\nContent-Disposition: form-data; "
        f'name="media"; filename="{fname}"\r\n'
        f"Content-Type: {ctype}\r\n\r\n"
    ).encode() + raw + f"\r\n--{boundary}--\r\n".encode()
    r = post(f"{BASE}/upload_media?key={key()}&type=file", parts,
             f"multipart/form-data; boundary={boundary}")
    return r["media_id"]


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    cmd, rest = args[0], args[1:]

    if cmd == "text":
        rest or die("用法: text <内容> [@userid,userid|@all]")
        text = {"content": rest[0]}
        if len(rest) > 1:
            at = rest[1]
            text["mentioned_list"] = (["@all"] if at == "@all"
                                      else at.lstrip("@").split(","))
        send({"msgtype": "text", "text": text})
    elif cmd == "markdown":
        rest or die("用法: markdown <md文件或内容>")
        send({"msgtype": "markdown",
              "markdown": {"content": read_arg_or_file(rest[0])}})
    elif cmd == "image":
        rest or die("用法: image <图片文件>")
        raw = open(rest[0], "rb").read()
        len(raw) <= 2 * 1024 * 1024 or die("图片超过 2MB 限制")
        send({"msgtype": "image",
              "image": {"base64": base64.b64encode(raw).decode(),
                        "md5": hashlib.md5(raw).hexdigest()}})
    elif cmd == "file":
        rest or die("用法: file <文件路径>")
        send({"msgtype": "file", "file": {"media_id": upload_file(rest[0])}})
    else:
        die(f"未知子命令: {cmd}（运行不带参数查看帮助）")


if __name__ == "__main__":
    main()
