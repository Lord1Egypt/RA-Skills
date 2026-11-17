#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一审批连接器（v4.4.0）

把钉钉 / 企业微信 / 飞书三套独立审批代码抽象为统一接口：

    class ApprovalConnector(ABC):
        send(expense_file, applicant_user_id, **kwargs) -> dict   # 发起审批
        query_status(approval_id) -> dict                          # 查询审批状态
        verify_callback(payload, **kwargs) -> bool                 # 回调验签

新增审批平台只需继承 ApprovalConnector 并实现三个方法，无需改动任何调用方。

安全约定：
- 密钥只从构造函数传入（上层由 secure_config 从环境变量读取），不落盘、不回显
- 所有 HTTP 调用使用 urllib，不启用 shell
"""

import hashlib
import hmac
import json
import time
import base64
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import urllib.request
    import urllib.parse
    import urllib.error
    HAS_URLLIB = True
except ImportError:
    HAS_URLLIB = False


class ApprovalError(Exception):
    """审批连接器异常"""


class ApprovalConnector(ABC):
    """审批平台统一接口"""

    platform: str = "base"
    display_name: str = "审批平台"

    def __init__(self, **credentials):
        self.credentials = credentials
        self.name = self.display_name
        self._token: Optional[str] = None
        self._token_expire: float = 0
        self.max_retries = 3
        self.retry_delay = 2

    # ---------- 必须实现的三个方法 ----------

    @abstractmethod
    def send(self, expense_file: str, applicant_user_id: Optional[str] = None,
             **kwargs) -> Dict[str, Any]:
        """发起审批"""

    @abstractmethod
    def query_status(self, approval_id: str) -> Dict[str, Any]:
        """查询审批状态"""

    @abstractmethod
    def verify_callback(self, payload: Dict[str, Any], **kwargs) -> bool:
        """回调验签"""

    # ---------- 兼容旧调用 ----------

    def submit_approval(self, expense_file: str, applicant_user_id: Optional[str] = None,
                        **kwargs) -> Dict[str, Any]:
        """兼容 v4.3.0 及更早的调用方式"""
        return self.send(expense_file, applicant_user_id=applicant_user_id, **kwargs)

    # ---------- 公共能力 ----------

    def _missing(self, *keys) -> list:
        return [k for k in keys if not self.credentials.get(k)]

    def _config_error(self, keys) -> Dict[str, Any]:
        return {
            "engine": self.name,
            "status": "config_incomplete",
            "message": f"缺少配置项：{', '.join(keys)}",
            "hint": "密钥请通过环境变量配置（INVOICE_ 前缀），不要写在 config.yaml 明文里",
        }

    def _http_json(self, url: str, data: Optional[bytes] = None,
                   headers: Optional[Dict[str, str]] = None,
                   method: Optional[str] = None,
                   timeout: int = 15) -> Optional[Dict[str, Any]]:
        """带重试的 JSON 请求，失败返回 None"""
        if not HAS_URLLIB:
            return None
        req = urllib.request.Request(url, data=data, headers=headers or {},
                                     method=method or ("POST" if data else "GET"))
        for attempt in range(self.max_retries):
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    return json.loads(resp.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                return {"_http_error": e.code,
                        "_body": e.read().decode("utf-8", errors="ignore")}
            except Exception:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                return None
        return None

    def _get_token(self) -> Optional[str]:
        """子类实现；基类默认无 token"""
        return None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} platform={self.platform}>"


# ==================== 钉钉 ====================

class DingTalkConnector(ApprovalConnector):
    """钉钉审批连接器"""

    platform = "dingtalk"
    display_name = "钉钉审批"

    def _get_token(self) -> Optional[str]:
        if self._token and time.time() < self._token_expire:
            return self._token
        miss = self._missing("app_key", "app_secret")
        if miss:
            return None
        url = "https://api.dingtalk.com/v1.0/oauth2/accessToken"
        body = json.dumps({
            "appKey": self.credentials["app_key"],
            "appSecret": self.credentials["app_secret"],
        }).encode("utf-8")
        data = self._http_json(url, data=body,
                               headers={"Content-Type": "application/json"})
        token = (data or {}).get("accessToken")
        if token:
            self._token = token
            self._token_expire = time.time() + int((data or {}).get("expireIn", 7200)) - 300
        return token

    def send(self, expense_file, applicant_user_id=None, **kwargs):
        miss = self._missing("app_key", "app_secret", "process_code")
        if miss:
            return self._config_error(miss)
        if not applicant_user_id:
            return {
                "engine": self.name,
                "status": "param_error",
                "message": "缺少申请人用户ID",
                "hint": "钉钉 → 我的 → 点击头像 → 查看个人信息中的工号",
            }

        token = self._get_token()
        if not token:
            return {
                "engine": self.name,
                "status": "token_failed",
                "message": "获取AccessToken失败",
                "hint": "请检查：1) app_key/app_secret 是否正确 2) 应用是否已审批 3) IP白名单是否已配置",
                "apply_url": "https://open-dev.dingtalk.com",
            }

        if expense_file and not Path(expense_file).exists():
            return {"engine": self.name, "status": "file_not_found",
                    "message": f"报销单文件不存在：{expense_file}"}

        amount = kwargs.get("amount", 0)
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            amount = 0.0
        expense_type = kwargs.get("expense_type", "日常报销")

        # 注意：钉钉审批 API 要求附件先上传获取 fileId，此处保留结构占位
        body = json.dumps({
            "process_code": self.credentials["process_code"],
            "originator_user_id": applicant_user_id,
            "form_component_values": [
                {"name": "费用类型", "value": expense_type},
                {"name": "报销金额", "value": f"{amount:.2f}"},
            ],
        }).encode("utf-8")

        data = self._http_json(
            "https://api.dingtalk.com/v1.0/process/instance",
            data=body,
            headers={"Content-Type": "application/json",
                     "x-acs-dingtalk-access-key": token},
        ) or {}

        if data.get("_http_error"):
            return {"engine": self.name, "status": "http_error",
                    "message": f"HTTP错误 {data['_http_error']}：{data.get('_body', '')}"}

        if data.get("requestId") or data.get("processInstanceId"):
            aid = data.get("processInstanceId") or data.get("requestId")
            return {
                "engine": self.name,
                "status": "success",
                "message": "审批提交成功",
                "approval_id": aid,
                "detail_url": f"https://aflow.dingtalk.com/dingtalk/mobile/h5approval/index.html?procInsId={aid}",
                "submit_time": datetime.now().isoformat(),
            }
        return {"engine": self.name, "status": "api_error",
                "message": f"钉钉API返回错误：{data.get('message', '未知错误')}",
                "raw_response": data}

    def query_status(self, approval_id: str):
        miss = self._missing("app_key", "app_secret")
        if miss:
            return self._config_error(miss)
        token = self._get_token()
        if not token:
            return {"engine": self.name, "status": "token_failed",
                    "message": "获取AccessToken失败"}
        url = f"https://api.dingtalk.com/v1.0/process/instances?processInstanceId={urllib.parse.quote(approval_id)}"
        data = self._http_json(url, headers={"x-acs-dingtalk-access-key": token})
        if not data or data.get("_http_error"):
            return {"engine": self.name, "status": "query_failed",
                    "message": f"查询失败：{data}"}
        return {
            "engine": self.name,
            "status": "success",
            "approval_id": approval_id,
            "result": data.get("result", {}).get("status", data.get("result", "UNKNOWN")),
            "raw_response": data,
        }

    def verify_callback(self, payload: Dict[str, Any], **kwargs) -> bool:
        """
        钉钉回调验签：把 timestamp + "\\n" + 签名密钥 做 HmacSHA256 再 base64，
        与回调中的 signature 比对
        """
        secret = self.credentials.get("callback_secret") or kwargs.get("secret")
        signature = payload.get("signature") or kwargs.get("signature")
        timestamp = payload.get("timestamp") or kwargs.get("timestamp")
        if not (secret and signature and timestamp):
            return False
        string_to_sign = f"{timestamp}\n{secret}"
        digest = hmac.new(secret.encode("utf-8"), string_to_sign.encode("utf-8"),
                          hashlib.sha256).digest()
        return hmac.compare_digest(base64.b64encode(digest).decode("utf-8"), str(signature))


# ==================== 企业微信 ====================

class WeComConnector(ApprovalConnector):
    """企业微信审批连接器"""

    platform = "wecom"
    display_name = "企业微信审批"

    def _get_token(self) -> Optional[str]:
        if self._token and time.time() < self._token_expire:
            return self._token
        miss = self._missing("corp_id", "secret")
        if miss:
            return None
        url = ("https://qyapi.weixin.qq.com/cgi-bin/gettoken"
               f"?corpid={urllib.parse.quote(str(self.credentials['corp_id']))}"
               f"&corpsecret={urllib.parse.quote(str(self.credentials['secret']))}")
        data = self._http_json(url)
        token = (data or {}).get("access_token")
        if token:
            self._token = token
            self._token_expire = time.time() + int((data or {}).get("expires_in", 7200)) - 300
        return token

    def send(self, expense_file, applicant_user_id=None, **kwargs):
        miss = self._missing("corp_id", "secret", "template_id")
        if miss:
            return self._config_error(miss)
        if not applicant_user_id:
            return {"engine": self.name, "status": "param_error",
                    "message": "缺少申请人用户ID"}
        if expense_file and not Path(expense_file).exists():
            return {"engine": self.name, "status": "file_not_found",
                    "message": f"报销单文件不存在：{expense_file}"}

        token = self._get_token()
        if not token:
            return {"engine": self.name, "status": "token_failed",
                    "message": "获取企业微信AccessToken失败",
                    "hint": "1. 确认corp_id和secret正确 2. 确认应用已开通审批权限 3. 确认IP白名单已配置",
                    "apply_url": "https://work.weixin.qq.com"}

        amount = kwargs.get("amount", 0)
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            amount = 0.0
        expense_type = kwargs.get("expense_type", "日常报销")

        body = json.dumps({
            "creator_userid": applicant_user_id,
            "template_id": self.credentials["template_id"],
            "use_template_approver": 0,
            "approver": [{"attr": 1, "userid": applicant_user_id}],
            "apply_data": {
                "contents": [
                    {"control": "Selector", "id": "fee_type",
                     "value": {"selector": {"type": "single",
                                            "options": [{"key": expense_type}]}}},
                    {"control": "Money", "id": "amount", "value": {"new_money": amount}},
                ]
            },
            "summary_list": [{"summary_info": [{"lang": "zh_CN",
                                                "text": f"报销申请：{amount}元"}]}],
        }).encode("utf-8")

        data = self._http_json(
            f"https://qyapi.weixin.qq.com/cgi-bin/oa/applyevent?access_token={token}",
            data=body, headers={"Content-Type": "application/json"}) or {}

        if data.get("_http_error"):
            return {"engine": self.name, "status": "http_error",
                    "message": f"HTTP错误 {data['_http_error']}：{data.get('_body', '')}"}

        if data.get("errcode") == 0:
            sp_no = data.get("sp_no", "")
            return {
                "engine": self.name,
                "status": "success",
                "message": "审批提交成功",
                "approval_id": sp_no,
                "detail_url": f"https://work.weixin.qq.com/wework_admin/approval/detail/{sp_no}",
                "submit_time": datetime.now().isoformat(),
            }
        return {"engine": self.name, "status": "api_error",
                "message": f"企微API返回错误：{data.get('errmsg', '未知错误')}",
                "raw_response": data}

    def query_status(self, approval_id: str):
        miss = self._missing("corp_id", "secret")
        if miss:
            return self._config_error(miss)
        token = self._get_token()
        if not token:
            return {"engine": self.name, "status": "token_failed",
                    "message": "获取AccessToken失败"}
        body = json.dumps({"sp_no": approval_id}).encode("utf-8")
        data = self._http_json(
            f"https://qyapi.weixin.qq.com/cgi-bin/oa/getapprovaldetail?access_token={token}",
            data=body, headers={"Content-Type": "application/json"}) or {}
        if not data or data.get("errcode") not in (0, None) or data.get("_http_error"):
            return {"engine": self.name, "status": "query_failed",
                    "message": data.get("errmsg") or str(data)}
        info = data.get("info", {})
        return {
            "engine": self.name,
            "status": "success",
            "approval_id": approval_id,
            "result": info.get("sp_status", "UNKNOWN"),
            "status_text": {1: "审批中", 2: "已通过", 3: "已驳回",
                            4: "已撤销"}.get(info.get("sp_status"), "未知"),
            "raw_response": data,
        }

    def verify_callback(self, payload: Dict[str, Any], **kwargs) -> bool:
        """
        企业微信回调验签：signature = SHA1(sort(token, timestamp, nonce))
        """
        token = self.credentials.get("callback_token") or kwargs.get("token")
        signature = payload.get("signature") or kwargs.get("signature")
        timestamp = str(payload.get("timestamp") or kwargs.get("timestamp") or "")
        nonce = str(payload.get("nonce") or kwargs.get("nonce") or "")
        if not (token and signature and timestamp and nonce):
            return False
        raw = "".join(sorted([token, timestamp, nonce]))
        return hmac.compare_digest(hashlib.sha1(raw.encode("utf-8")).hexdigest(),
                                   str(signature))


# ==================== 飞书 ====================

class FeishuConnector(ApprovalConnector):
    """飞书审批连接器"""

    platform = "feishu"
    display_name = "飞书审批"

    def _get_token(self) -> Optional[str]:
        if self._token and time.time() < self._token_expire:
            return self._token
        miss = self._missing("app_id", "app_secret")
        if miss:
            return None
        body = json.dumps({
            "app_id": self.credentials["app_id"],
            "app_secret": self.credentials["app_secret"],
        }).encode("utf-8")
        data = self._http_json(
            "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
            data=body, headers={"Content-Type": "application/json"})
        token = (data or {}).get("tenant_access_token")
        if token:
            self._token = token
            self._token_expire = time.time() + int((data or {}).get("expire", 7200)) - 300
        return token

    def send(self, expense_file, applicant_user_id=None, **kwargs):
        miss = self._missing("app_id", "app_secret", "approval_code")
        if miss:
            return self._config_error(miss)
        if not applicant_user_id:
            return {"engine": self.name, "status": "param_error",
                    "message": "缺少申请人用户ID"}
        if expense_file and not Path(expense_file).exists():
            return {"engine": self.name, "status": "file_not_found",
                    "message": f"报销单文件不存在：{expense_file}"}

        token = self._get_token()
        if not token:
            return {"engine": self.name, "status": "token_failed",
                    "message": "获取飞书TenantAccessToken失败",
                    "hint": "1. 确认app_id和app_secret正确 2. 确认应用已开通审批权限 3. 确认IP白名单已配置",
                    "apply_url": "https://open.feishu.cn"}

        amount = kwargs.get("amount", 0)
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            amount = 0.0
        expense_type = kwargs.get("expense_type", "日常报销")

        body = json.dumps({
            "approval_code": self.credentials["approval_code"],
            "user_id": applicant_user_id,
            "form": json.dumps([
                {"id": "expense_type", "type": "input", "value": expense_type},
                {"id": "amount", "type": "input", "value": f"{amount:.2f}"},
            ]),
        }).encode("utf-8")

        data = self._http_json(
            "https://open.feishu.cn/open-apis/approval/v4/instances",
            data=body,
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {token}"}) or {}

        if data.get("_http_error"):
            return {"engine": self.name, "status": "http_error",
                    "message": f"HTTP错误 {data['_http_error']}：{data.get('_body', '')}"}

        if data.get("code") == 0:
            code = data.get("data", {}).get("instance_code", "")
            return {
                "engine": self.name,
                "status": "success",
                "message": "审批提交成功",
                "approval_id": code,
                "detail_url": "https://applink.feishu.cn/client/mes/approval/detail",
                "submit_time": datetime.now().isoformat(),
            }
        return {"engine": self.name, "status": "api_error",
                "message": f"飞书API返回错误：{data.get('msg', '未知错误')}",
                "raw_response": data}

    def query_status(self, approval_id: str):
        miss = self._missing("app_id", "app_secret")
        if miss:
            return self._config_error(miss)
        token = self._get_token()
        if not token:
            return {"engine": self.name, "status": "token_failed",
                    "message": "获取AccessToken失败"}
        url = (f"https://open.feishu.cn/open-apis/approval/v4/instances/"
               f"{urllib.parse.quote(approval_id)}")
        data = self._http_json(url, headers={"Authorization": f"Bearer {token}"}) or {}
        if not data or data.get("code") not in (0, None) or data.get("_http_error"):
            return {"engine": self.name, "status": "query_failed",
                    "message": data.get("msg") or str(data)}
        return {
            "engine": self.name,
            "status": "success",
            "approval_id": approval_id,
            "result": data.get("data", {}).get("status", "UNKNOWN"),
            "status_text": {"PENDING": "审批中", "APPROVED": "已通过",
                            "REJECTED": "已驳回", "CANCELED": "已撤销",
                            "DELETED": "已删除"}.get(
                                data.get("data", {}).get("status"), "未知"),
            "raw_response": data,
        }

    def verify_callback(self, payload: Dict[str, Any], **kwargs) -> bool:
        """
        飞书回调验签：sha256(timestamp + nonce + app_secret + body) == signature
        """
        secret = self.credentials.get("app_secret")
        signature = payload.get("signature") or kwargs.get("signature")
        timestamp = str(payload.get("timestamp") or kwargs.get("timestamp") or "")
        nonce = str(payload.get("nonce") or kwargs.get("nonce") or "")
        body = str(payload.get("body") or kwargs.get("body") or "")
        if not (secret and signature and timestamp):
            return False
        raw = f"{timestamp}{nonce}{secret}{body}"
        return hmac.compare_digest(hashlib.sha256(raw.encode("utf-8")).hexdigest(),
                                   str(signature))


# ==================== 工厂 ====================

PLATFORM_CLASSES = {
    "dingtalk": DingTalkConnector,
    "wecom": WeComConnector,
    "feishu": FeishuConnector,
}


def get_connector(platform: str, credentials: Optional[Dict[str, Any]] = None
                  ) -> Optional[ApprovalConnector]:
    """按平台名创建连接器；未知平台返回 None"""
    cls = PLATFORM_CLASSES.get((platform or "").lower())
    if not cls:
        return None
    return cls(**(credentials or {}))


def supported_platforms() -> list:
    return sorted(PLATFORM_CLASSES.keys())
