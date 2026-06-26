#!/usr/bin/env python3
"""
yuanbao-send — 元宝派主动发消息（独立于 OpenClaw 插件）

通过 Yuanbao WebSocket 协议直接发送群消息，不依赖 OpenClaw 通道框架。
适用于从 cron 定时任务、其他 agent session、或后台脚本主动推送消息。
"""

import json
import sys
import os
import hmac
import hashlib
import struct
import random
import threading
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from urllib.request import Request, urlopen

# ── 配置 ──────────────────────────────────────────────
CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"
WS_URL = "wss://bot-wss.yuanbao.tencent.com/wss/connection"


# ── Protobuf 编解码（纯标准库）────────────────────────

def pb_varint(value):
    if value < 0:
        value = (1 << 64) + value
    result = []
    while value > 0x7F:
        result.append((value & 0x7F) | 0x80)
        value >>= 7
    result.append(value & 0x7F)
    return bytes(result)


def pb_tag(field, wire):
    return pb_varint((field << 3) | wire)


def pb_string(field, value):
    data = value.encode("utf-8")
    return pb_tag(field, 2) + pb_varint(len(data)) + data


def pb_bytes(field, value):
    return pb_tag(field, 2) + pb_varint(len(value)) + value


def pb_int32(field, value):
    return pb_tag(field, 0) + pb_varint(value)


def pb_uint32(field, value):
    return pb_tag(field, 0) + pb_varint(value)


def pb_msg(field, inner):
    return pb_tag(field, 2) + pb_varint(len(inner)) + inner


def pb_decode_varint(data, off=0):
    result = 0
    shift = 0
    while off < len(data):
        b = data[off]
        result |= (b & 0x7F) << shift
        off += 1
        if not (b & 0x80):
            break
        shift += 7
    return result, off


def pb_decode_delimited(data, off=0):
    length, off = pb_decode_varint(data, off)
    return data[off:off + length], off + length


def pb_decode_msg(data):
    """解码 protobuf 消息为 {field_num: (wire_type, value)}"""
    result = {}
    off = 0
    while off < len(data):
        tag, off = pb_decode_varint(data, off)
        field = tag >> 3
        wire = tag & 7
        if wire == 0:
            val, off = pb_decode_varint(data, off)
            result[field] = (0, val)
        elif wire == 2:
            val, off = pb_decode_delimited(data, off)
            result[field] = (2, val)
        elif wire == 5:
            val = struct.unpack_from("<I", data, off)[0]
            off += 4
            result[field] = (5, val)
        elif wire == 1:
            val = struct.unpack_from("<Q", data, off)[0]
            off += 8
            result[field] = (1, val)
        else:
            break
    return result


# ── ConnMsg（连接层消息）──────────────────────────────

def encode_conn_head(cmd_type, cmd, seq_no, msg_id, module):
    head = b""
    head += pb_int32(1, cmd_type)
    head += pb_string(2, cmd)
    head += pb_int32(3, seq_no)
    head += pb_string(4, msg_id)
    head += pb_string(5, module)
    return head


def encode_conn_msg(cmd_type, cmd, seq_no, msg_id, module, data=b""):
    frame = pb_msg(1, encode_conn_head(cmd_type, cmd, seq_no, msg_id, module))
    if data:
        frame += pb_bytes(2, data)
    return frame


def decode_conn_msg(data):
    """解码 ConnMsg，返回 {cmd, cmdType, data, ...}"""
    msg = pb_decode_msg(data)
    result = {}
    if 1 in msg:
        head = pb_decode_msg(msg[1][1])
        for fid, key in [(1, "cmdType"), (2, "cmd"), (3, "seqNo"), (4, "msgId"), (5, "module")]:
            if fid in head:
                val = head[fid][1]
                result[key] = val.decode("utf-8", errors="replace") if isinstance(val, bytes) else val
    if 2 in msg:
        result["data"] = msg[2][1]
    return result


# ── AuthBindReq ───────────────────────────────────────

def encode_auth_bind(biz_id, uid, source, token):
    auth_info = pb_string(1, uid) + pb_string(2, source) + pb_string(3, token)
    device_info = (
        pb_string(1, "2.0.1")
        + pb_string(2, "Linux")
        + pb_string(3, "2026.3.23-2")
        + pb_string(4, "16")
    )
    return pb_string(1, biz_id) + pb_msg(2, auth_info) + pb_msg(3, device_info)


# ── SendGroupMessageReq ──────────────────────────────

def encode_msg_body_element(msg_type, text):
    msg_content = pb_string(1, text)
    return pb_string(1, msg_type) + pb_msg(2, msg_content)


def encode_send_group_req(group_code, text, msg_id="", from_account="", random_val=None):
    if random_val is None:
        random_val = str(random.randint(0, 2**32 - 1))

    body_elem = encode_msg_body_element("TIMTextElem", text)
    req = b""
    req += pb_string(1, msg_id)
    req += pb_string(2, group_code)
    req += pb_string(3, from_account)
    req += pb_string(4, "")
    req += pb_string(5, random_val)
    req += pb_msg(6, body_elem)
    req += pb_string(7, "")
    return req


def encode_send_c2c_req(to_account, text, msg_id="", from_account="", msg_random=None):
    """SendC2CMessageReq 编码

    字段（对照 proto）:
      1 msgId      string
      2 toAccount  string
      3 fromAccount string
      4 msgRandom  uint32
      5 msgBody    repeated MsgBodyElement
    """
    if msg_random is None:
        msg_random = random.randint(0, 2**32 - 1)

    body_elem = encode_msg_body_element("TIMTextElem", text)
    req = b""
    req += pb_string(1, msg_id)
    req += pb_string(2, to_account)
    req += pb_string(3, from_account)
    req += pb_uint32(4, msg_random)
    req += pb_msg(5, body_elem)
    return req


def decode_send_group_rsp(data):
    msg = pb_decode_msg(data)
    result = {}
    if 1 in msg:
        result["code"] = msg[1][1]
    if 2 in msg:
        result["message"] = msg[2][1].decode("utf-8", errors="replace")
    if 3 in msg:
        result["msgId"] = msg[3][1].decode("utf-8", errors="replace")
    if 4 in msg:
        result["msgSeq"] = msg[4][1]
    return result


def decode_send_c2c_rsp(data):
    msg = pb_decode_msg(data)
    result = {}
    if 1 in msg:
        result["code"] = msg[1][1]
    if 2 in msg:
        result["message"] = msg[2][1].decode("utf-8", errors="replace")
    return result


# ── 签票 ─────────────────────────────────────────────

def get_sign_token(app_key, app_secret):
    nonce = os.urandom(16).hex()
    bj_tz = timezone(timedelta(hours=8))
    timestamp = datetime.now(bj_tz).strftime("%Y-%m-%dT%H:%M:%S+08:00")
    plain = nonce + timestamp + app_key + app_secret
    signature = hmac.new(app_secret.encode(), plain.encode(), hashlib.sha256).hexdigest()

    body = json.dumps({
        "app_key": app_key,
        "nonce": nonce,
        "signature": signature,
        "timestamp": timestamp,
    }).encode()

    req = Request(
        "https://bot.yuanbao.tencent.com/api/v5/robotLogic/sign-token",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    resp = urlopen(req, timeout=15)
    data = json.loads(resp.read())
    if data.get("code") != 0:
        print(f"❌ 签票失败: {data}", file=sys.stderr)
        sys.exit(1)
    return data["data"]


# ── 发送消息 ─────────────────────────────────────────

def send_group_message(group_code, text):
    """通过 WebSocket 发送群消息到元宝派"""
    import websocket as ws_lib

    # 加载配置
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    yb = config.get("channels", {}).get("yuanbao", {})
    app_key = yb.get("appKey", "")
    app_secret = yb.get("appSecret", "")

    if not app_key:
        return {"ok": False, "error": "未找到元宝配置 (channels.yuanbao.appKey)"}

    # 签票
    token_data = get_sign_token(app_key, app_secret)

    auth_done = threading.Event()
    send_done = threading.Event()
    result = {"ok": False}

    def on_message(ws, data):
        if not isinstance(data, bytes):
            return
        msg = decode_conn_msg(data)
        cmd = msg.get("cmd", "")
        cmd_type = msg.get("cmdType", -1)

        if cmd == "auth-bind" and cmd_type == 1:
            auth_done.set()

        if cmd == "send_group_message" and cmd_type == 1:
            rsp_data = msg.get("data", b"")
            if rsp_data:
                rsp = decode_send_group_rsp(rsp_data)
                code = rsp.get("code", 0)  # code=0 是 protobuf 默认值不编码
                result["ok"] = code == 0
                result["code"] = code
                result["message"] = rsp.get("message", "")
            else:
                result["ok"] = True
            send_done.set()

    def on_open(ws):
        auth_payload = encode_auth_bind(
            biz_id="ybBot",
            uid=token_data["bot_id"],
            source=token_data.get("source", "bot"),
            token=token_data["token"],
        )
        auth_frame = encode_conn_msg(0, "auth-bind", 0, "auth001", "conn_access", auth_payload)
        ws.send(auth_frame, opcode=ws_lib.ABNF.OPCODE_BINARY)

    def on_error(ws, error):
        result["error"] = str(error)

    td = token_data
    ws = ws_lib.WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        header=[
            f"X-ID: {td['bot_id']}",
            f"X-Token: {td['token']}",
            f"X-Source: {td.get('source', 'bot')}",
            "X-AppVersion: 2.0.1",
            "X-OperationSystem: Linux",
            "X-Instance-Id: 99",
        ],
    )

    t = threading.Thread(target=ws.run_forever, kwargs={"ping_interval": None})
    t.daemon = True
    t.start()

    auth_done.wait(timeout=5)

    # 发送群消息
    msg_id = f"msg{int(time.time() * 1000)}"
    send_req = encode_send_group_req(
        group_code=group_code,
        text=text,
        msg_id=msg_id,
        from_account=token_data["bot_id"],
    )
    send_frame = encode_conn_msg(0, "send_group_message", 1, msg_id, "yuanbao_openclaw_proxy", send_req)
    ws.send(send_frame, opcode=ws_lib.ABNF.OPCODE_BINARY)

    send_done.wait(timeout=8)

    try:
        ws.close()
    except:
        pass

    if not result["ok"] and "code" not in result:
        result["ok"] = True
        result["note"] = "sent (no response received)"

    return result


def send_c2c_message(to_account, text):
    """通过 WebSocket 发送私聊消息（C2C）"""
    import websocket as ws_lib

    with open(CONFIG_PATH) as f:
        config = json.load(f)
    yb = config.get("channels", {}).get("yuanbao", {})
    app_key = yb.get("appKey", "")
    app_secret = yb.get("appSecret", "")

    if not app_key:
        return {"ok": False, "error": "未找到元宝配置 (channels.yuanbao.appKey)"}

    token_data = get_sign_token(app_key, app_secret)

    auth_done = threading.Event()
    send_done = threading.Event()
    result = {"ok": False}

    def on_message(ws, data):
        if not isinstance(data, bytes):
            return
        msg = decode_conn_msg(data)
        cmd = msg.get("cmd", "")
        cmd_type = msg.get("cmdType", -1)

        if cmd == "auth-bind" and cmd_type == 1:
            auth_done.set()

        if cmd == "send_c2c_message" and cmd_type == 1:
            rsp_data = msg.get("data", b"")
            if rsp_data:
                rsp = decode_send_c2c_rsp(rsp_data)
                code = rsp.get("code", 0)
                result["ok"] = code == 0
                result["code"] = code
                result["message"] = rsp.get("message", "")
            else:
                result["ok"] = True
            send_done.set()

    def on_open(ws):
        auth_payload = encode_auth_bind(
            biz_id="ybBot",
            uid=token_data["bot_id"],
            source=token_data.get("source", "bot"),
            token=token_data["token"],
        )
        auth_frame = encode_conn_msg(0, "auth-bind", 0, "auth001", "conn_access", auth_payload)
        ws.send(auth_frame, opcode=ws_lib.ABNF.OPCODE_BINARY)

    def on_error(ws, error):
        result["error"] = str(error)

    td = token_data
    ws = ws_lib.WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        header=[
            f"X-ID: {td['bot_id']}",
            f"X-Token: {td['token']}",
            f"X-Source: {td.get('source', 'bot')}",
            "X-AppVersion: 2.0.1",
            "X-OperationSystem: Linux",
            "X-Instance-Id: 99",
        ],
    )

    t = threading.Thread(target=ws.run_forever, kwargs={"ping_interval": None})
    t.daemon = True
    t.start()

    auth_done.wait(timeout=5)

    # 发送私聊消息
    msg_id = f"msg{int(time.time() * 1000)}"
    send_req = encode_send_c2c_req(
        to_account=to_account,
        text=text,
        msg_id=msg_id,
        from_account=token_data["bot_id"],
    )
    send_frame = encode_conn_msg(0, "send_c2c_message", 1, msg_id, "yuanbao_openclaw_proxy", send_req)
    ws.send(send_frame, opcode=ws_lib.ABNF.OPCODE_BINARY)

    send_done.wait(timeout=8)

    try:
        ws.close()
    except:
        pass

    if not result["ok"] and "code" not in result:
        result["ok"] = True
        result["note"] = "sent (no response received)"

    return result

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".heic", ".tiff", ".ico"}


def get_upload_info(app_key, token_data, file_name):
    """获取 COS 上传凭证"""
    file_id = os.urandom(8).hex()
    body = json.dumps({
        "fileName": file_name,
        "fileId": file_id,
        "docFrom": "localDoc",
        "docOpenId": "",
    }).encode()
    headers = {
        "Content-Type": "application/json",
        "X-ID": token_data["bot_id"],
        "X-Token": token_data["token"],
        "X-Source": token_data.get("source", "web"),
        "X-AppVersion": "2.0.1",
        "X-OperationSystem": "Linux",
        "X-Instance-Id": "99",
    }
    req = Request(
        "https://bot.yuanbao.tencent.com/api/resource/genUploadInfo",
        data=body,
        headers=headers,
        method="POST",
    )
    resp = urlopen(req, timeout=15)
    data = json.loads(resp.read())
    if data.get("code", 0) != 0:
        raise Exception(f"genUploadInfo 失败: {data}")
    return data


def upload_to_cos(upload_info, file_path):
    """上传文件到腾讯云 COS"""
    from qcloud_cos import CosConfig, CosS3Client

    config = CosConfig(
        Region=upload_info["region"],
        SecretId=upload_info["encryptTmpSecretId"],
        SecretKey=upload_info["encryptTmpSecretKey"],
        Token=upload_info["encryptToken"],
    )
    client = CosS3Client(config)
    with open(file_path, "rb") as f:
        client.put_object(
            Bucket=upload_info["bucketName"],
            Body=f,
            Key=upload_info["location"],
            ContentType="application/octet-stream",
        )
    return upload_info["resourceUrl"]


def send_file_msg(ws, group_code, token_data, resource_url, file_name, file_size, msg_type, body_elem):
    """发送文件/图片消息"""
    import websocket as ws_lib

    send_done = threading.Event()
    result = {"ok": False}

    # 保存原始 on_message
    orig_om = ws.on_message

    def on_message(ws2, data):
        if not isinstance(data, bytes):
            return
        msg = decode_conn_msg(data)
        cmd = msg.get("cmd", "")
        cmd_type = msg.get("cmdType", -1)
        if cmd == "send_group_message" and cmd_type == 1:
            rsp_data = msg.get("data", b"")
            if rsp_data:
                rsp = decode_send_group_rsp(rsp_data)
                code = rsp.get("code", -1)
                result["ok"] = code == 0 or rsp.get("message", "") == "succ"
                result["code"] = code
                result["message"] = rsp.get("message", "")
            else:
                result["ok"] = True
            send_done.set()

    ws.on_message = on_message

    msg_id = f"msg{int(time.time() * 1000)}"
    send_req = (
        pb_string(1, msg_id)
        + pb_string(2, group_code)
        + pb_string(3, token_data["bot_id"])
        + pb_string(4, "")
        + pb_string(5, str(random.randint(0, 2**32 - 1)))
        + pb_msg(6, body_elem)
        + pb_string(7, "")
    )
    send_frame = encode_conn_msg(0, "send_group_message", 1, msg_id, "yuanbao_openclaw_proxy", send_req)
    ws.send(send_frame, opcode=ws_lib.ABNF.OPCODE_BINARY)

    send_done.wait(timeout=10)
    ws.on_message = orig_om
    return result


def send_file_msg_dm(ws, to_account, token_data, resource_url, file_name, file_size, msg_type, body_elem):
    """发送文件/图片私聊消息"""
    import websocket as ws_lib

    send_done = threading.Event()
    result = {"ok": False}

    orig_om = ws.on_message

    def on_message(ws2, data):
        if not isinstance(data, bytes):
            return
        msg = decode_conn_msg(data)
        cmd = msg.get("cmd", "")
        cmd_type = msg.get("cmdType", -1)
        if cmd == "send_c2c_message" and cmd_type == 1:
            rsp_data = msg.get("data", b"")
            if rsp_data:
                rsp = decode_send_c2c_rsp(rsp_data)
                code = rsp.get("code", -1)
                result["ok"] = code == 0 or rsp.get("message", "") == "succ"
                result["code"] = code
                result["message"] = rsp.get("message", "")
            else:
                result["ok"] = True
            send_done.set()

    ws.on_message = on_message

    msg_id = f"msg{int(time.time() * 1000)}"
    send_req = (
        pb_string(1, msg_id)
        + pb_string(2, to_account)
        + pb_string(3, token_data["bot_id"])
        + pb_uint32(4, random.randint(0, 2**32 - 1))
        + pb_msg(5, body_elem)
    )
    send_frame = encode_conn_msg(0, "send_c2c_message", 1, msg_id, "yuanbao_openclaw_proxy", send_req)
    ws.send(send_frame, opcode=ws_lib.ABNF.OPCODE_BINARY)

    send_done.wait(timeout=10)
    ws.on_message = orig_om
    return result


def upload_and_send(group_code, file_path):
    """上传文件并发送到元宝派群

    图片(.png/.jpg/.gif等) 走 TIMImageElem
    其他文件走 TIMFileElem
    """
    import websocket as ws_lib

    with open(CONFIG_PATH) as f:
        config = json.load(f)
    yb = config.get("channels", {}).get("yuanbao", {})
    app_key = yb.get("appKey", "")
    app_secret = yb.get("appSecret", "")

    if not app_key:
        return {"ok": False, "error": "未找到元宝配置"}

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    ext = os.path.splitext(file_name)[1].lower()
    is_image = ext in IMAGE_EXTS

    # 1. 签票
    token_data = get_sign_token(app_key, app_secret)

    # 2. 获取上传凭证
    upload_info = get_upload_info(app_key, token_data, file_name)

    # 3. 上传到 COS
    resource_url = upload_to_cos(upload_info, file_path)

    # 4. 构建消息体
    uuid = os.urandom(8).hex()

    if is_image:
        # TIMImageElem: uuid(2), imageFormat(3), imageInfoArray(8)
        # ImImageInfoArray: type(1), size(2), width(3), height(4), url(5)
        img_info = (
            pb_uint32(1, 1)
            + pb_uint32(2, file_size)
            + pb_uint32(3, 0)
            + pb_uint32(4, 0)
            + pb_string(5, resource_url)
        )
        mc = pb_string(2, uuid) + pb_uint32(3, 255) + pb_msg(8, img_info)
        body_elem = pb_string(1, "TIMImageElem") + pb_msg(2, mc)
    else:
        # TIMFileElem: uuid(2), url(10), fileSize(11), fileName(12)
        mc = (
            pb_string(2, uuid)
            + pb_string(10, resource_url)
            + pb_uint32(11, file_size)
            + pb_string(12, file_name)
        )
        body_elem = pb_string(1, "TIMFileElem") + pb_msg(2, mc)

    # 5. 建立 WebSocket 连接并发送
    auth_done = threading.Event()
    td = token_data

    def on_open(ws):
        auth_payload = encode_auth_bind(
            biz_id="ybBot",
            uid=td["bot_id"],
            source=td.get("source", "bot"),
            token=td["token"],
        )
        auth_frame = encode_conn_msg(0, "auth-bind", 0, "auth_upload", "conn_access", auth_payload)
        ws.send(auth_frame, opcode=ws_lib.ABNF.OPCODE_BINARY)

    def on_auth_msg(ws, data):
        if not isinstance(data, bytes):
            return
        msg = decode_conn_msg(data)
        if msg.get("cmd") == "auth-bind" and msg.get("cmdType") == 1:
            auth_done.set()

    def on_error(ws, error):
        pass

    ws = ws_lib.WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_auth_msg,
        on_error=on_error,
        header=[
            f"X-ID: {td['bot_id']}",
            f"X-Token: {td['token']}",
            f"X-Source: {td.get('source', 'bot')}",
            "X-AppVersion: 2.0.1",
            "X-OperationSystem: Linux",
            "X-Instance-Id: 99",
        ],
    )

    t = threading.Thread(target=ws.run_forever, kwargs={"ping_interval": None})
    t.daemon = True
    t.start()
    auth_done.wait(timeout=5)

    # 发送文件消息
    result = send_file_msg(ws, group_code, token_data, resource_url, file_name, file_size,
                           "TIMImageElem" if is_image else "TIMFileElem", body_elem)

    try:
        ws.close()
    except:
        pass

    result["file"] = file_name
    result["type"] = "TIMImageElem" if is_image else "TIMFileElem"
    return result


def upload_and_send_dm(to_account, file_path):
    """上传文件并发送私聊消息"""
    import websocket as ws_lib

    with open(CONFIG_PATH) as f:
        config = json.load(f)
    yb = config.get("channels", {}).get("yuanbao", {})
    app_key = yb.get("appKey", "")
    app_secret = yb.get("appSecret", "")

    if not app_key:
        return {"ok": False, "error": "未找到元宝配置"}

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    ext = os.path.splitext(file_name)[1].lower()
    is_image = ext in IMAGE_EXTS

    # 1. 签票
    token_data = get_sign_token(app_key, app_secret)

    # 2. 获取上传凭证
    upload_info = get_upload_info(app_key, token_data, file_name)

    # 3. 上传到 COS
    resource_url = upload_to_cos(upload_info, file_path)

    # 4. 构建消息体
    uuid = os.urandom(8).hex()

    if is_image:
        img_info = (
            pb_uint32(1, 1)
            + pb_uint32(2, file_size)
            + pb_uint32(3, 0)
            + pb_uint32(4, 0)
            + pb_string(5, resource_url)
        )
        mc = pb_string(2, uuid) + pb_uint32(3, 255) + pb_msg(8, img_info)
        body_elem = pb_string(1, "TIMImageElem") + pb_msg(2, mc)
    else:
        mc = (
            pb_string(2, uuid)
            + pb_string(10, resource_url)
            + pb_uint32(11, file_size)
            + pb_string(12, file_name)
        )
        body_elem = pb_string(1, "TIMFileElem") + pb_msg(2, mc)

    # 5. 建立 WebSocket 连接并发送
    auth_done = threading.Event()
    td = token_data

    def on_open(ws):
        auth_payload = encode_auth_bind(
            biz_id="ybBot",
            uid=td["bot_id"],
            source=td.get("source", "bot"),
            token=td["token"],
        )
        auth_frame = encode_conn_msg(0, "auth-bind", 0, "auth_upload_dm", "conn_access", auth_payload)
        ws.send(auth_frame, opcode=ws_lib.ABNF.OPCODE_BINARY)

    def on_auth_msg(ws, data):
        if not isinstance(data, bytes):
            return
        msg = decode_conn_msg(data)
        if msg.get("cmd") == "auth-bind" and msg.get("cmdType") == 1:
            auth_done.set()

    def on_error(ws, error):
        pass

    ws = ws_lib.WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_auth_msg,
        on_error=on_error,
        header=[
            f"X-ID: {td['bot_id']}",
            f"X-Token: {td['token']}",
            f"X-Source: {td.get('source', 'bot')}",
            "X-AppVersion: 2.0.1",
            "X-OperationSystem: Linux",
            "X-Instance-Id: 99",
        ],
    )

    t = threading.Thread(target=ws.run_forever, kwargs={"ping_interval": None})
    t.daemon = True
    t.start()
    auth_done.wait(timeout=5)

    # 发送私聊文件消息
    result = send_file_msg_dm(ws, to_account, token_data, resource_url, file_name, file_size,
                              "TIMImageElem" if is_image else "TIMFileElem", body_elem)

    try:
        ws.close()
    except:
        pass

    result["file"] = file_name
    result["type"] = "TIMImageElem" if is_image else "TIMFileElem"
    return result


# ── CLI ───────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="元宝派主动发消息（独立于 OpenClaw 插件）",
        epilog="示例: python3 send.py send 123456789 '你好！'",
    )
    sub = parser.add_subparsers(dest="cmd")

    send_p = sub.add_parser("send", help="发送群消息")
    send_p.add_argument("group", help="群号")
    send_p.add_argument("text", help="消息内容")

    dm_p = sub.add_parser("dm", help="发送私聊消息")
    dm_p.add_argument("user", help="用户 open_id")
    dm_p.add_argument("text", help="消息内容")

    upload_p = sub.add_parser("upload", help="上传文件并发送（群聊）")
    upload_p.add_argument("group", help="群号")
    upload_p.add_argument("file", help="文件路径")

    upload_dm_p = sub.add_parser("upload-dm", help="上传文件并发送（私聊）")
    upload_dm_p.add_argument("user", help="用户 open_id")
    upload_dm_p.add_argument("file", help="文件路径")

    args = parser.parse_args()

    if args.cmd == "send":
        result = send_group_message(args.group, args.text)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if result["ok"] else 1)
    elif args.cmd == "dm":
        result = send_c2c_message(args.user, args.text)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if result["ok"] else 1)
    elif args.cmd == "upload":
        result = upload_and_send(args.group, args.file)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if result.get("ok") else 1)
    elif args.cmd == "upload-dm":
        result = upload_and_send_dm(args.user, args.file)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if result.get("ok") else 1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
