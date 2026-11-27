#!/usr/bin/env python3
"""YZL-AIoT 北向客户端（Python，标准库实现）。

一个接口一个方法，加载技能后可直接 import 使用：

    from north_client import NorthClient
    c = NorthClient.from_env()              # AIOT_TOKEN / AIOT_ACCOUNT+PASSWORD / AIOT_API_KEY
    c.list_devices(max_results=5)
    c.telemetry("DEV-1")
    c.send_command("DEV-1", "set", ["sw", "1"])

限频：北向 REST 用户配额 = 基础配额 + 设备数 × 每台追加（次/秒）；
写接口（POST/PUT/DELETE）按 3 倍配额计；超限返回 429。
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_BASE_URL = os.environ.get("AIOT_BASE_URL", "https://aiot.yzlkj.com")
USER_AGENT = "yzl-aiot-north/2.0"


class NorthError(Exception):
    """接口错误：code 为平台业务码，status 为 HTTP 状态。"""

    def __init__(self, message, code=None, status=None, body=None):
        super().__init__(message)
        self.code = code
        self.status = status
        self.body = body


def _quote(value):
    return urllib.parse.quote(str(value), safe="")


def _clean(params):
    return {k: v for k, v in params.items() if v is not None}


class NorthClient:
    def __init__(self, base_url=None, token=None, api_key=None, account=None,
                 password=None, timeout=15, user_agent=USER_AGENT):
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.token = token or None
        self.api_key = api_key or None
        self.account = account or None
        self.password = password or None
        self.timeout = timeout
        self.user_agent = user_agent

    # ------------------------------------------------------------ 构造 / 认证
    @classmethod
    def from_env(cls, **kwargs):
        return cls(
            base_url=kwargs.pop("base_url", os.environ.get("AIOT_BASE_URL")),
            token=kwargs.pop("token", os.environ.get("AIOT_TOKEN")),
            api_key=kwargs.pop("api_key", os.environ.get("AIOT_API_KEY")),
            account=kwargs.pop("account", os.environ.get("AIOT_ACCOUNT")),
            password=kwargs.pop("password", os.environ.get("AIOT_PASSWORD")),
            **kwargs,
        )

    def set_token(self, token):
        self.token = token or None

    def set_api_key(self, key):
        self.api_key = key or None

    def login(self, account=None, password=None):
        """POST /auth/login 换 JWT，返回 user 对象。"""
        account = account or self.account
        password = password or self.password
        if not account or not password:
            raise ValueError("account 和 password 必填")
        data = self.request("POST", "/auth/login",
                            body={"account": account, "password": password},
                            auth=False)
        token = (data or {}).get("token")
        if not token:
            raise NorthError("登录响应中没有 token", body=data)
        self.token, self.account, self.password = token, account, password
        return (data or {}).get("user") or {}

    # --------------------------------------------------------------- 底层请求
    def request(self, method, path, params=None, body=None, auth=True, _retry=True):
        if not path.startswith("/"):
            path = "/" + path
        query = urllib.parse.urlencode(_clean(params or {}))
        url = self.base_url + path + (("?" + query) if query else "")

        headers = {"Accept": "application/json", "User-Agent": self.user_agent}
        if body is not None:
            headers["Content-Type"] = "application/json"
        if auth and self.token:
            headers["Authorization"] = "Bearer " + self.token
        if auth and self.api_key:
            headers["X-API-Key"] = self.api_key
            headers["YZL-AIoT-KEY"] = self.api_key

        payload = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
        req = urllib.request.Request(url, data=payload, headers=headers, method=method.upper())
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                status, raw = resp.status, resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            status, raw = e.code, e.read().decode("utf-8", "replace")
        except urllib.error.URLError as e:
            raise NorthError("网络错误: %s" % e.reason)

        if status == 401 and _retry and self.account and self.password:
            self.login(self.account, self.password)
            return self.request(method, path, params, body, auth, _retry=False)

        try:
            envelope = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            raise NorthError("响应不是 JSON (HTTP %s): %s" % (status, raw[:200]), status=status)

        code = envelope.get("code")
        if code not in (0, None):
            hint = ""
            if code == 429:
                hint = "（限频：用户配额=基础+设备数×每台追加；写接口 3 倍）"
            elif code in (401, 403):
                hint = "（检查 AIOT_TOKEN / API Key 权限）"
            raise NorthError("%s%s" % (envelope.get("msg") or "接口错误", hint),
                             code=code, status=status, body=envelope)
        if status >= 400:
            raise NorthError("HTTP %s" % status, status=status, body=envelope)
        return envelope.get("data")

    # ---------------------------------------------------------------- 账号
    def profile(self):
        """GET /auth/profile（当前登录用户）。"""
        return self.request("GET", "/auth/profile")

    def account_summary(self):
        """GET /open/account（账号概览）。"""
        return self.request("GET", "/open/account")

    # ---------------------------------------------------------------- 设备
    def list_devices(self, filter=None, group_id=None, online=None,
                     max_results=50, offset=0, include_secrets=False):
        """GET /open/device/list。默认脱敏 password/bindCode。"""
        data = self.request("GET", "/open/device/list", {
            "Filter": filter, "GroupId": group_id, "Online": online,
            "MaxResultCount": max_results, "Offset": offset})
        if include_secrets or not isinstance(data, dict):
            return data
        for item in data.get("items") or []:
            for k in ("password", "bindCode"):
                if k in item:
                    item[k] = "***"
        return data

    def get_device(self, device_id, include_secrets=False):
        """GET /open/device/{id}。"""
        data = self.request("GET", "/open/device/%s" % _quote(device_id))
        if include_secrets or not isinstance(data, dict):
            return data
        for k in ("password", "bindCode"):
            if k in data:
                data[k] = "***"
        return data

    def device_stats(self, group_id=None):
        """GET /open/device/stats。"""
        return self.request("GET", "/open/device/stats", {"GroupId": group_id})

    def telemetry(self, device_id):
        """GET /open/device/{id}/telemetry（最新值）。"""
        return self.request("GET", "/open/device/%s/telemetry" % _quote(device_id))

    def history(self, device_id, keys=None, start=None, end=None, limit=None):
        """GET /open/device/{id}/history。keys 可为逗号字符串或列表。"""
        if isinstance(keys, (list, tuple)):
            keys = ",".join(str(k) for k in keys)
        return self.request("GET", "/open/device/%s/history" % _quote(device_id),
                            {"keys": keys, "start": start, "end": end, "limit": limit})

    def aggregate(self, device_id, keys, start, end, bucket="1h"):
        """GET /open/device/{id}/aggregate（按时间桶聚合）。"""
        if isinstance(keys, (list, tuple)):
            keys = ",".join(str(k) for k in keys)
        return self.request("GET", "/open/device/%s/aggregate" % _quote(device_id),
                            {"keys": keys, "start": start, "end": end, "bucket": bucket})

    def backfill_logs(self, device_id, limit=10):
        """GET /open/device/{id}/backfill-logs（补传记录）。"""
        return self.request("GET", "/open/device/%s/backfill-logs" % _quote(device_id),
                            {"limit": limit})

    def send_command(self, device_id, cmd, args=None, tra=None):
        """POST /open/device/{id}/command（set / get；写接口 3 倍配额）。"""
        if cmd not in ("set", "get"):
            raise ValueError("cmd 只能是 set 或 get")
        arg_list = list(args or [])
        if not arg_list or arg_list[0] != device_id:
            arg_list.insert(0, device_id)
        body = {"cmd": cmd, "args": arg_list}
        if tra:
            body["tra"] = tra
        return self.request("POST", "/open/device/%s/command" % _quote(device_id), body=body)

    # ---------------------------------------------------------------- 指令
    def list_commands(self, device_id=None, status=None, page=1, page_size=20):
        """GET /open/command/list。"""
        return self.request("GET", "/open/command/list", {
            "deviceId": device_id, "status": status, "page": page, "pageSize": page_size})

    def get_command(self, command_id):
        """GET /open/command/{id}。"""
        return self.request("GET", "/open/command/%s" % _quote(command_id))

    # ---------------------------------------------------------------- 告警
    def list_alarms(self, status=None, page=1, page_size=20):
        """GET /open/alarm/list（pageSize 可能被平台忽略）。"""
        return self.request("GET", "/open/alarm/list", {
            "status": status, "page": page, "pageSize": page_size})

    # ---------------------------------------------------------------- 型号/设施
    def list_products(self):
        """GET /open/product/list（含 metrics 定义）。"""
        return self.request("GET", "/open/product/list")

    def find_product(self, product_id):
        """按 id 在列表里找型号（平台单型号 GET 实测 404，故用列表过滤）。"""
        data = self.list_products()
        for item in (data or {}).get("items", []):
            if item.get("id") == product_id:
                return item
        return None

    def gateway_ports(self):
        """GET /open/gateway/ports。"""
        return self.request("GET", "/open/gateway/ports")

    def update_metric(self, product_id, key, data_type=None, access=None,
                      label=None, unit=None, visible=None):
        """PATCH /open/product/{id}/metric/{key}（单测点属性，写接口 3 倍配额）。"""
        body = {}
        if data_type is not None:
            body["dataType"] = data_type
        if access is not None:
            body["access"] = access
        if label is not None:
            body["label"] = label
        if unit is not None:
            body["unit"] = unit
        if visible is not None:
            body["visible"] = bool(visible)
        if not body:
            raise ValueError("至少指定一个要修改的字段")
        return self.request("PATCH", "/open/product/%s/metric/%s" % (_quote(product_id), _quote(key)),
                            body=body)

    def update_metrics_config(self, product_id, control=None, compare=None):
        """PUT /open/product/{id}/metrics-config（设施语义配置）。"""
        body = {}
        if control is not None:
            body["control"] = control
        if compare is not None:
            body["compare"] = compare
        return self.request("PUT", "/open/product/%s/metrics-config" % _quote(product_id), body=body)

    def clean_metrics(self, product_id, keys=None):
        """POST /open/product/{id}/clean-metrics（清理自动添加的设施）。"""
        body = {"keys": keys} if keys is not None else {}
        return self.request("POST", "/open/product/%s/clean-metrics" % _quote(product_id), body=body)

    # ---------------------------------------------------------------- 兼容别名
    devices = property(lambda self: _DevicesAPI(self))
    commands = property(lambda self: _CommandsAPI(self))
    alarms = property(lambda self: _AlarmsAPI(self))
    products = property(lambda self: _ProductsAPI(self))


class _DevicesAPI:
    def __init__(self, client):
        self.c = client

    def list(self, **kw):
        return self.c.list_devices(**kw)

    def get(self, device_id, **kw):
        return self.c.get_device(device_id, **kw)

    def telemetry(self, device_id):
        return self.c.telemetry(device_id)

    def history(self, device_id, **kw):
        return self.c.history(device_id, **kw)

    def aggregate(self, device_id, **kw):
        return self.c.aggregate(device_id, **kw)

    def command(self, device_id, cmd, args=None, **kw):
        return self.c.send_command(device_id, cmd, args, **kw)


class _CommandsAPI:
    def __init__(self, client):
        self.c = client

    def list(self, **kw):
        return self.c.list_commands(**kw)

    def get(self, command_id):
        return self.c.get_command(command_id)


class _AlarmsAPI:
    def __init__(self, client):
        self.c = client

    def list(self, **kw):
        return self.c.list_alarms(**kw)


class _ProductsAPI:
    def __init__(self, client):
        self.c = client

    def list(self):
        return self.c.list_products()

    def get(self, product_id):
        return self.c.find_product(product_id)

    def update_metric(self, product_id, key, **kw):
        return self.c.update_metric(product_id, key, **kw)
