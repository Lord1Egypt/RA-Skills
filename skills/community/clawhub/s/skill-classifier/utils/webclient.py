# -*- coding: utf-8 -*-
"""
极简 HTTP 客户端（纯标准库）
仅允许访问白名单内的 HTTPS 公网主机，拒绝明文协议与内网/环回/保留地址
"""
import ipaddress
import json
import socket
import urllib.error
import urllib.request
import uuid
from urllib.parse import urlparse

# 允许访问的远程服务主机
ALLOWED_HOSTS = {'open.feishu.cn', 'api.notion.com'}


def check_url(url: str) -> None:
    """校验 URL：仅 https、主机须在白名单且解析结果不含保留地址"""
    parsed = urlparse(url)
    if parsed.scheme != 'https':
        raise ValueError(f"仅允许 https 协议: {url}")
    host = parsed.hostname or ''
    if host not in ALLOWED_HOSTS:
        raise ValueError(f"主机不在白名单内: {host}")
    try:
        infos = socket.getaddrinfo(host, 443)
    except OSError as e:
        raise ValueError(f"域名解析失败: {host} ({e})")
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if (ip.is_private or ip.is_loopback or ip.is_reserved
                or ip.is_link_local or ip.is_multicast or ip.is_unspecified):
            raise ValueError(f"主机解析到保留地址: {host} -> {ip}")


def http_json(method: str, url: str, headers=None, body=None, timeout: int = 30):
    """请求 JSON 接口并返回解析后的响应；body 为 dict 时自动序列化"""
    check_url(url)
    data = None
    hdrs = dict(headers or {})
    if body is not None:
        data = json.dumps(body).encode('utf-8')
        hdrs.setdefault('Content-Type', 'application/json')
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        detail = e.read().decode('utf-8', errors='replace')[:500]
        raise RuntimeError(f"HTTP {e.code} {method} {url}: {detail}") from None


def http_multipart(url: str, headers, fields: dict, file_field: str,
                   file_name: str, file_bytes: bytes, timeout: int = 60):
    """multipart/form-data 上传（用于飞书文件上传），返回 JSON 响应"""
    check_url(url)
    boundary = '----ocsm' + uuid.uuid4().hex
    parts = []
    for k, v in fields.items():
        parts.append(
            (f'--{boundary}\r\nContent-Disposition: form-data; '
             f'name="{k}"\r\n\r\n{v}\r\n').encode('utf-8'))
    parts.append(
        (f'--{boundary}\r\nContent-Disposition: form-data; '
         f'name="{file_field}"; filename="{file_name}"\r\n'
         'Content-Type: application/octet-stream\r\n\r\n').encode('utf-8'))
    parts.append(file_bytes)
    parts.append(f'\r\n--{boundary}--\r\n'.encode('utf-8'))
    hdrs = dict(headers or {})
    hdrs['Content-Type'] = f'multipart/form-data; boundary={boundary}'
    req = urllib.request.Request(url, data=b''.join(parts), headers=hdrs, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        detail = e.read().decode('utf-8', errors='replace')[:500]
        raise RuntimeError(f"HTTP {e.code} 上传失败: {detail}") from None
