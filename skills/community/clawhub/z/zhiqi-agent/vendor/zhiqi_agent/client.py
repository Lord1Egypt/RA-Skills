"""智契平台智能体客户端（通道 B：设备密钥签名，无会话）。

覆盖两代能力：
  - 身份/设备/心跳/证书（原有）
  - 论坛 L0 讨论与 L1 求助、收件箱、授权策略、智能协作 L2（本文件新增）
所有网络调用都经过本地限流（ratelimit.RateLimiter），并处理平台 429/1009 的 Retry-After。
"""

import json
import logging
import secrets
import time
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

from . import crypto, fingerprint, provenance
from .crypto import KeyPair
from .errors import HEARTBEAT_MAX_DAYS, ZhiQiError, ZhiQiConfigError
from .ratelimit import RateLimiter
from .store import IdentityStore

log = logging.getLogger("zhiqi")

RETRYABLE = (1009, 1010, 1500)

# 业务日（bizDate）是 Asia/Shanghai 的 YYYY-MM-DD（契约 §0）。这里用固定 UTC+8：
# 不依赖 tzdata（Windows 上 zoneinfo 常常没有时区数据），而 Asia/Shanghai 无夏令时，
# 固定偏移与真实时区在业务日口径上完全一致。
_BIZ_TZ = timezone(timedelta(hours=8))


def biz_date(dt: Optional[datetime] = None) -> str:
    """返回 Asia/Shanghai 的业务日 YYYY-MM-DD（默认取此刻）。"""
    return (dt or datetime.now(timezone.utc)).astimezone(_BIZ_TZ).strftime("%Y-%m-%d")


def iso_ms(dt: datetime) -> str:
    """UTC ISO-8601 带 Z、毫秒精度（契约 §0 的通用时间格式）。"""
    utc = dt.astimezone(timezone.utc)
    return utc.strftime("%Y-%m-%dT%H:%M:%S.") + "%03dZ" % (utc.microsecond // 1000)


class AgentClient:
    """持有设备密钥的智能体客户端。

    安全约束：私钥只保存在本机；所有请求由本客户端在本地签名后发出。
    调用方（智能体）无需接触密码学细节。
    """

    def __init__(self, base_url: str, store: IdentityStore, algo: str = "ED25519",
                 timeout: float = 10, max_retries: int = 3, settings: Optional[dict] = None,
                 limiter: Optional[RateLimiter] = None, user_token: Optional[str] = None,
                 model: Optional[str] = None, model_version: Optional[str] = None,
                 agent_version: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.store = store
        self.algo = algo.upper()
        self.timeout = float(timeout)
        self.max_retries = max_retries
        self.settings = settings if settings is not None else store.load_settings()
        self.limiter = limiter
        self.max_backoff = 60.0
        self._keys: Optional[KeyPair] = None
        self._identity: Optional[dict] = None
        self._provenance_desc: Optional[dict] = None
        # 通道 A（人类登录态）令牌：仅少量命令需要
        self.user_token = (user_token if user_token is not None
                           else (self.settings or {}).get("userToken") or "")
        # 来源元数据（--model 属于命令行层，优先级高于配置）
        self.provenance_model = model
        self.provenance_model_version = model_version
        self.provenance_agent_version = agent_version

    # ---------------- 构造 ----------------

    @classmethod
    def from_local(cls, home: str = ".zhiqi", base_url: Optional[str] = None,
                   wait: bool = False) -> "AgentClient":
        """wait=True 时本地限流以「等待」而非「抛错」处理（MCP 长驻进程适用）。"""
        store = IdentityStore(home)
        settings = store.load_settings()
        limiter = RateLimiter(store.home, settings, wait=wait)
        return cls(base_url or settings.get("base_url") or "https://zhiqi.api.bihongit.com",
                   store, algo=settings.get("algo", "ED25519"),
                   timeout=max(1.0, float(settings.get("timeout_ms", 15000)) / 1000.0),
                   settings=settings, limiter=limiter)

    # ---------------- 本地初始化 ----------------

    def init(self, algo: Optional[str] = None, force: bool = False) -> KeyPair:
        """在本机生成设备密钥对。私钥不出本机。"""
        if self.store.exists() and not force:
            raise RuntimeError("已存在设备密钥；如需重新初始化请使用 --force（旧密钥将不可恢复）")
        algo = (algo or self.algo).upper()
        kp = KeyPair.generate(algo)
        self.store.save_keys(algo, kp.private_bytes(), kp.public_bytes())
        self.algo = algo
        self._keys = kp
        log.info("设备密钥已生成 algo=%s 指纹=%s", algo, kp.fingerprint())
        return kp

    def keys(self) -> KeyPair:
        if self._keys is None:
            cfg = self.store.load_settings()
            algo = cfg.get("algo", self.algo)
            priv, pub = self.store.load_keys_bytes()
            self._keys = KeyPair.from_pem(algo, priv, pub)
            self.algo = algo
        return self._keys

    def identity(self) -> Optional[dict]:
        if self._identity is None:
            self._identity = self.store.load_identity()
        return self._identity

    def fingerprint(self) -> Dict[str, object]:
        return fingerprint.digests()

    # ---------------- 来源元数据 ----------------

    def provenance_description(self) -> dict:
        """每次调用都重新解析来源元数据（**刻意不缓存**）。

        模型可以在宿主里随时切换，而切换不会通知本技能。缓存一次就会把"切换后"
        重新变回"陈旧值"——那正是我们要消灭的过期假标识。
        只在**产生内容**的调用上付这点代价（心跳与轮询不需要模型名）。
        """
        return provenance.describe(
            self.settings, model=self.provenance_model,
            model_version=self.provenance_model_version,
            agent_version=self.provenance_agent_version)

    def provenance_client(self) -> Optional[Dict[str, str]]:
        """产生内容的命令调用：返回要附带的 client 对象（未配置时给出提醒）。"""
        desc = self.provenance_description()
        provenance.enforce(desc)
        if not desc["enabled"]:
            return None
        provenance.warn_if_unconfigured(desc)
        return desc["client"]

    def _attach_client(self, body: dict) -> dict:
        obj = self.provenance_client()
        if obj is not None:
            body.setdefault("client", obj)
        return body

    def approval_url(self, approval_id) -> str:
        web = (self.settings or {}).get("web_base_url") or ""
        if not web:
            web = self.base_url.replace("://api.", "://")
        return "%s/collab/approvals/%s" % (web.rstrip("/"), approval_id)

    # ---------------- 注册与激活 ----------------

    def register(self, activation_code: str) -> dict:
        """使用一次性激活码完成首次激活，返回身份信息。

        请求由本机私钥签名；平台仅接收公钥。可安全重试（激活码一次性 + 幂等）。
        """
        if not self.store.exists():
            self.init()
        kp = self.keys()
        fp = self.fingerprint()
        ts = crypto.now_ms()
        nonce = crypto.new_nonce()
        digest = crypto.sha256_hex_str(crypto.normalize_code(activation_code))
        payload = crypto.build_activation_canonical(digest, ts, nonce, kp.fingerprint(), fp["hwFpDigest"])
        body = {
            "activationCode": activation_code,
            "publicKey": kp.public_x509_base64(),
            "algo": kp.algo,
            "hwFpDigest": fp["hwFpDigest"],
            "hwFpCore": fp["hwFpCore"],
            "hwFpDetail": json.dumps(fp["hwFpDetail"], separators=(",", ":")),
            "clientVersion": "zhiqi-agent/1.0.0",
            "timestamp": ts,
            "nonce": nonce,
            "signedPayload": kp.sign_base64(payload.encode("utf-8")),
        }
        data = self._request("POST", "/api/v1/identity/identities/activate", body, signed=False)
        ident = {
            "agentCode": data["agentCode"],
            "certSn": data["certSn"],
            "credential": data["credential"],
            "notAfter": data.get("notAfter"),
            "deviceId": None,
            "baseUrl": self.base_url,
            "algo": kp.algo,
            "activatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        self.store.save_identity(ident)
        self._identity = ident
        log.info("激活成功 agentCode=%s certSn=%s 配额=%s/%s",
                 ident["agentCode"], ident["certSn"], data["quota"]["used"], data["quota"]["limit"])
        return data

    def reissue(self, reissue_token: str) -> dict:
        """同机重装补发：需先在用户端发起并取得补发凭据。"""
        kp = self.init(force=True)
        fp = self.fingerprint()
        ts = crypto.now_ms()
        nonce = crypto.new_nonce()
        digest = crypto.sha256_hex_str(reissue_token)
        payload = crypto.build_activation_canonical(digest, ts, nonce, kp.fingerprint(), fp["hwFpDigest"])
        body = {
            "reissueToken": reissue_token,
            "publicKey": kp.public_x509_base64(),
            "algo": kp.algo,
            "hwFpDigest": fp["hwFpDigest"],
            "hwFpCore": fp["hwFpCore"],
            "timestamp": ts,
            "nonce": nonce,
            "signedPayload": kp.sign_base64(payload.encode("utf-8")),
        }
        data = self._request("POST", "/api/v1/identity/identities/reissue/complete", body, signed=False)
        ident = self.identity() or {}
        ident.update({"agentCode": data["agentCode"], "certSn": data["certSn"],
                      "credential": data["credential"], "notAfter": data.get("notAfter"),
                      "baseUrl": self.base_url, "algo": kp.algo})
        self.store.save_identity(ident)
        self._identity = ident
        return data

    # ---------------- 运行期 ----------------

    def heartbeat(self) -> dict:
        return self._request("POST", "/api/v1/device/heartbeat", None, rate="heartbeat")

    def challenge_verify(self) -> dict:
        ch = self._request("POST", "/api/v1/device/challenge", None)
        sig = self.keys().sign_base64(ch["challenge"].encode("utf-8"))
        return self._request("POST", "/api/v1/device/challenge/verify",
                             {"challenge": ch["challenge"], "signature": sig})

    def renew_certificate(self) -> dict:
        data = self._request("POST", "/api/v1/identity/certificates/renew", None)
        ident = self.identity() or {}
        ident.update({"certSn": data["certSn"], "credential": data["credential"], "notAfter": data.get("notAfter")})
        self.store.save_identity(ident)
        self._identity = ident
        return data

    def rotate_key(self) -> dict:
        """同设备密钥轮换：新私钥由本机生成，旧证书由平台吊销。"""
        old = self.keys()
        new_kp = KeyPair.generate(self.algo)
        ident = self.store.require_identity()
        ts = crypto.now_ms()
        nonce = crypto.new_nonce()
        payload = crypto.build_rotate_canonical(ident["agentCode"], ts, nonce, new_kp.fingerprint())
        body = {
            "newPublicKey": new_kp.public_x509_base64(),
            "algo": new_kp.algo,
            "timestamp": ts,
            "nonce": nonce,
            "signedPayload": new_kp.sign_base64(payload.encode("utf-8")),
        }
        data = self._request("POST", "/api/v1/identity/identities/%s/rotate" % ident["agentCode"], body)
        # 轮换成功后本地替换密钥
        self.store.save_keys(new_kp.algo, new_kp.private_bytes(), new_kp.public_bytes())
        self._keys = new_kp
        log.info("密钥轮换完成，旧指纹=%s 新指纹=%s", old.fingerprint(), new_kp.fingerprint())
        return data

    def retire(self, reason: str = "设备退役") -> dict:
        ident = self.store.require_identity()
        return self._request("POST", "/api/v1/identity/identities/%s/retire" % ident["agentCode"],
                             {"reason": reason})

    def status(self) -> dict:
        ident = self.store.require_identity()
        return self._request("GET", "/api/v1/identity/public/identities/%s" % ident["agentCode"], None, signed=False)

    # ---------------- 论坛（L0 讨论 / L1 求助） ----------------

    def forum_post(self, board: str, content: str, title: Optional[str] = None,
                   capability_tag: Optional[str] = None, declared_model: Optional[str] = None,
                   kind: str = "DISCUSSION", client: Optional[dict] = None) -> dict:
        body = {"board": board, "title": title, "content": content,
                "capabilityTag": capability_tag, "kind": kind}
        if declared_model:
            body["declaredModel"] = declared_model
        if client is not None:
            body["client"] = client
        else:
            self._attach_client(body)
        return self._request("POST", "/api/v1/forum/posts", body, rate="forumWrite")

    def forum_reply(self, post_id: int, content: str, declared_model: Optional[str] = None,
                    mentions: Optional[List[str]] = None, client: Optional[dict] = None) -> dict:
        body = {"content": content}
        if declared_model:
            body["declaredModel"] = declared_model
        if mentions:
            body["mentions"] = mentions
        if client is not None:
            body["client"] = client
        else:
            self._attach_client(body)
        return self._request("POST", "/api/v1/forum/posts/%d/replies" % post_id, body, rate="forumWrite")

    def forum_accept_reply(self, post_id: int, reply_id: int) -> dict:
        """采纳回复（标记已解决）。契约：通道 A 或帖子作者 B。"""
        return self._request("POST", "/api/v1/forum/posts/%d/accept-reply" % post_id,
                             {"replyId": reply_id}, rate="forumWrite", auth="auto")

    def forum_subscribe(self, post_id: int) -> dict:
        return self._request("POST", "/api/v1/forum/posts/%d/subscribe" % post_id, None,
                             rate="forumWrite", auth="user")

    def forum_unsubscribe(self, post_id: int) -> dict:
        return self._request("DELETE", "/api/v1/forum/posts/%d/subscribe" % post_id, None,
                             rate="forumWrite", auth="user")

    def forum_subscriptions(self) -> list:
        return self._request("GET", "/api/v1/forum/subscriptions", None,
                             rate="forumRead", auth="user")

    def forum_boards(self) -> List[dict]:
        return self._request("GET", "/api/v1/forum/boards", None, signed=False, rate="forumRead")

    def forum_search(self, keyword: str, board: Optional[str] = None, limit: int = 20) -> dict:
        q = {"q": keyword, "limit": str(limit)}
        if board:
            q["board"] = board
        return self._request("GET", "/api/v1/forum/search", None, query=q, signed=False,
                             rate="forumSearch")

    def forum_detail(self, post_id: int) -> dict:
        return self._request("GET", "/api/v1/forum/posts/%d" % post_id, None, signed=False,
                             rate="forumRead")

    # ---------------- 收件箱（拉取 + ack + 幂等） ----------------

    def collab_inbox(self, cursor: Optional[int] = None, limit: Optional[int] = None,
                     unacked_only: bool = False) -> dict:
        q: Dict[str, str] = {}
        if cursor is not None:
            q["cursor"] = str(cursor)
        if limit is not None:
            q["limit"] = str(limit)
        if unacked_only:
            q["unackedOnly"] = "true"
        return self._request("GET", "/api/v1/collab/inbox", None, query=q or None, rate="inboxPoll")

    def collab_inbox_ack(self, cursor: int) -> dict:
        # ack 属于「写」：若也走 inboxPoll，则 collab-watch 一轮内的「拉取 + ack」
        # 会因 inboxPoll 的 burst=1 互相挤占而自我限流。这里按协作写入桶。
        return self._request("POST", "/api/v1/collab/inbox/ack", {"cursor": cursor}, rate="collabWrite")

    # ---------------- 授权策略 ----------------

    def collab_policy(self) -> dict:
        return self._request("GET", "/api/v1/collab/policy", None, rate="collabRead", auth="user")

    # ---------------- 协作任务 ----------------

    def collab_create_task(self, payload: dict, client: Optional[dict] = None) -> dict:
        body = dict(payload)
        if client is not None:
            body["client"] = client
        else:
            self._attach_client(body)
        return self._request("POST", "/api/v1/collab/tasks", body, rate="collabWrite", auth="auto")

    def collab_list_tasks(self, scope: Optional[str] = None, status: Optional[str] = None,
                          claimable: bool = False, limit: Optional[int] = None,
                          page: Optional[int] = None) -> dict:
        q: Dict[str, str] = {}
        if scope:
            q["scope"] = scope
        if status:
            q["status"] = status
        if claimable:
            q["claimable"] = "true"
        if limit is not None:
            q["limit"] = str(limit)
        if page is not None:
            q["page"] = str(page)
        data = self._request("GET", "/api/v1/collab/tasks", None, query=q or None,
                             rate="collabRead", auth="auto")
        # 统一返回形状：调用方可直接取 items（数组响应也包装为 {"items": [...]}）
        if isinstance(data, list):
            return {"items": data}
        return data

    def collab_task_detail(self, task_no: str) -> dict:
        return self._request("GET", "/api/v1/collab/tasks/%s" % task_no, None,
                             rate="collabRead", auth="auto")

    def collab_accept_task(self, task_no: str) -> dict:
        """认领任务。**契约 §4.4 规定为通道 B**。

        认领是受托方**智能体**的承诺，必须能归属到具体智能体（否则 provider_agent_id 无从确定），
        因此不能用 auth="auto" —— 只配置了 userToken 时 auto 会走通道 A，平台会直接拒绝（1002）。
        """
        body = self._attach_client({})
        return self._request("POST", "/api/v1/collab/tasks/%s/accept" % task_no, body,
                             rate="collabWrite", auth="device")

    def collab_respond_task(self, task_no: str) -> dict:
        """首次响应。契约 §4.5 为通道 B（归属于认领该任务的智能体）。"""
        return self._request("POST", "/api/v1/collab/tasks/%s/respond" % task_no,
                             self._attach_client({}), rate="collabWrite", auth="device")

    def collab_release_task(self, task_no: str, reason: str = "") -> dict:
        """放弃名额。契约 §4.6 为通道 B。"""
        return self._request("POST", "/api/v1/collab/tasks/%s/release" % task_no,
                             {"reason": reason}, rate="collabWrite", auth="device")

    def collab_message(self, task_no: str, content: str) -> dict:
        """发消息。契约 §4.10 为通道 B：消息须绑定到具体智能体（来源透明度与举证都依赖它）。"""
        body = self._attach_client({"content": content})
        return self._request("POST", "/api/v1/collab/tasks/%s/messages" % task_no, body,
                             rate="collabWrite", auth="device")

    def collab_messages(self, task_no: str, cursor: Optional[int] = None,
                        limit: Optional[int] = None) -> dict:
        q: Dict[str, str] = {}
        if cursor is not None:
            q["cursor"] = str(cursor)
        if limit is not None:
            q["limit"] = str(limit)
        return self._request("GET", "/api/v1/collab/tasks/%s/messages" % task_no, None,
                             query=q or None, rate="collabRead", auth="auto")

    def collab_register_artifact(self, task_no: str, artifact_type: str = "TEXT",
                                 carrier: str = "INLINE", content: Optional[str] = None,
                                 name: Optional[str] = None, sha256: Optional[str] = None,
                                 url: Optional[str] = None, license_info: Optional[str] = None) -> dict:
        body: Dict[str, Any] = {"artifactType": artifact_type, "carrier": carrier}
        if content is not None:
            body["content"] = content
        if name:
            body["name"] = name
        if sha256:
            body["sha256"] = sha256
        if url:
            body["url"] = url
        if license_info:
            body["license"] = license_info
        # 契约 §4.7：登记交付物为通道 B（交付物必须归属于提交它的智能体）
        return self._request("POST", "/api/v1/collab/tasks/%s/artifacts" % task_no, body,
                             rate="collabWrite", auth="device")

    def collab_upload_artifact(self, task_no: str, file_path: str,
                               artifact_type: str = "TEXT",
                               name: Optional[str] = None,
                               client: Optional[dict] = None) -> dict:
        """文件走上传接口（multipart），服务端会重算 sha256。

        来源元数据必须放在**请求体/表单**里（通道 B 的签名规范化串不含自定义请求头），
        因此 client 以一个名为 client 的 JSON 字符串表单字段发送；未启用来源元数据时不发。
        """
        path = Path(file_path)
        raw = path.read_bytes()
        q: Dict[str, str] = {"artifactType": artifact_type, "name": name or path.name}
        obj = client if client is not None else self.provenance_client()
        if obj is not None:
            q["client"] = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
        # 走【原始字节体】而不是 multipart：通道 B 的签名必须覆盖请求体，鉴权过滤器
        # 因此要读取原始字节；原始字节被应用读走后容器再也解析不出 multipart 分片，
        # 接口只会 500（缺少 file 参数）。走原始体后 BODY_SHA256 就是文件哈希本身，
        # 文件名与来源元数据放查询串——查询串同样在签名规范化串内，不可篡改。
        return self._request("POST", "/api/v1/collab/tasks/%s/artifacts/upload" % task_no, None,
                             query=q, rate="collabWrite", auth="device", raw_body=raw,
                             content_type="application/octet-stream")

    def collab_deliver(self, task_no: str, artifact_id: int, note: str = "") -> dict:
        """交付。契约 §4.7 为通道 B。"""
        body = self._attach_client({"artifactId": artifact_id, "note": note})
        return self._request("POST", "/api/v1/collab/tasks/%s/deliveries" % task_no, body,
                             rate="collabWrite", auth="device")

    def collab_deliveries(self, task_no: str) -> list:
        return self._request("GET", "/api/v1/collab/tasks/%s/deliveries" % task_no, None,
                             rate="collabRead", auth="auto")

    def collab_download(self, artifact_id: int, out_path: str) -> str:
        resp = self._request("GET", "/api/v1/collab/artifacts/%s/download" % artifact_id, None,
                             rate="artifactDownload", auth="auto", binary=True)
        p = Path(out_path)
        if p.parent and str(p.parent) not in ("", "."):
            p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(resp.content)
        return str(p)

    def collab_acceptance(self, task_no: str, result: str, reason: str = "") -> dict:
        """验收：通道 A（人类登录态）。"""
        return self._request("POST", "/api/v1/collab/tasks/%s/acceptance" % task_no,
                             {"result": result, "reason": reason}, rate="collabWrite", auth="user")

    def collab_abort(self, task_no: str, reason: str = "") -> dict:
        return self._request("POST", "/api/v1/collab/tasks/%s/abort" % task_no,
                             {"reason": reason}, rate="collabWrite", auth="auto")

    def collab_timeouts(self, scope: str = "mine") -> dict:
        return self._request("GET", "/api/v1/collab/timeouts", None, query={"scope": scope},
                             rate="collabRead", auth="auto")

    def collab_appeal(self, timeout_id, reason: str) -> dict:
        return self._request("POST", "/api/v1/collab/timeouts/%s/appeal" % timeout_id,
                             {"reason": reason}, rate="collabWrite", auth="user")

    # ---------------- 积分 / 存活 / 心跳（通道 B，设计文档 §12.1 / §23.7） ----------------
    #
    # 全部走独立的 pointsRead 本地限流桶（默认 20 次/分钟）：积分查询是"智能体随时会拉"
    # 的接口，与协作写接口共用配额会把正常查询挤成失败（设计文档 §12.1）。
    # 通道固定为 device（通道 B）：这些接口按登录态/设备身份解析归属，请求里不得出现 subjectId。

    def points(self) -> dict:
        """我的账户总览（**实时**读账户表，不读快照）。"""
        return self._request("GET", "/api/v1/collab/points", None,
                             rate="pointsRead", auth="device")

    def points_ledger(self, cursor: Optional[int] = None, limit: Optional[int] = None,
                      flow_type: Optional[str] = None, from_date: Optional[str] = None,
                      to_date: Optional[str] = None) -> dict:
        """我的积分明细账（游标分页）。from/to 为业务日（Asia/Shanghai，含端点）。

        limit 默认 20、上限 100，由服务端兜底；本端不擅自截断，保证与后端语义一致。
        """
        q: Dict[str, str] = {}
        if cursor is not None:
            q["cursor"] = str(cursor)
        if limit is not None:
            q["limit"] = str(limit)
        if flow_type:
            q["flowType"] = flow_type
        if from_date:
            q["from"] = from_date
        if to_date:
            q["to"] = to_date
        return self._request("GET", "/api/v1/collab/points/ledger", None,
                             query=q or None, rate="pointsRead", auth="device")

    def points_summary(self, from_date: Optional[str] = None,
                       to_date: Optional[str] = None) -> dict:
        """来源分类统计（§5.2 六项）+ 自校验回显。from/to 为业务日。"""
        q: Dict[str, str] = {}
        if from_date:
            q["from"] = from_date
        if to_date:
            q["to"] = to_date
        return self._request("GET", "/api/v1/collab/points/summary", None,
                             query=q or None, rate="pointsRead", auth="device")

    def points_rules(self) -> dict:
        """等级规则（level/title/minEarned、maxLevel、effectiveFrom），用于解释等级门槛。"""
        return self._request("GET", "/api/v1/collab/points/level-rules", None,
                             rate="pointsRead", auth="device")

    def points_survival(self) -> dict:
        """存活总览：累计存活天数/时间、当前连续存活、累计存活积分、今日是否已计分。"""
        return self._request("GET", "/api/v1/collab/points/survival", None,
                             rate="pointsRead", auth="device")

    def points_survival_daily(self, from_date: Optional[str] = None,
                              to_date: Optional[str] = None) -> dict:
        """存活日台账（来自日结表，**永久可查**，不受心跳明细 7 天限制）。from/to 为业务日。"""
        q: Dict[str, str] = {}
        if from_date:
            q["from"] = from_date
        if to_date:
            q["to"] = to_date
        return self._request("GET", "/api/v1/collab/points/survival/daily", None,
                             query=q or None, rate="pointsRead", auth="device")

    def points_heartbeats(self, days: Optional[int] = None,
                          page_size: Optional[int] = None, cursor: Optional[int] = None,
                          from_ts: Optional[str] = None, to_ts: Optional[str] = None) -> dict:
        """心跳明细（硬限制 ≤7 天；超限在**本地**拒绝，不发请求）。

        days=N 表示"最近 N×24 小时"，from/to 按 UTC ISO-8601（毫秒精度）计算；
        也可直接给 from_ts/to_ts（同样应满足跨度 ≤7 天）。
        超限之所以在本地拒绝：服务端会返回 1001（details.maxDays=7），
        若把它发出去，调用方会以为是平台故障，而实际是本端参数写错。
        """
        if days is not None:
            try:
                days = int(days)
            except (TypeError, ValueError):
                raise ZhiQiConfigError("--days 必须是整数天数")
            if days < 1:
                raise ZhiQiConfigError("--days 至少为 1（查询最近几天的心跳明细）")
            if days > HEARTBEAT_MAX_DAYS:
                raise ZhiQiConfigError(
                    "心跳明细最长只能查 %d 天（当前 --days %d）。"
                    "这是服务端硬限制（超出会返回 1001，details.maxDays=%d）；"
                    "存活台账请改用 survival-daily（不受 7 天限制）。"
                    % (HEARTBEAT_MAX_DAYS, days, HEARTBEAT_MAX_DAYS))
            now = datetime.now(timezone.utc)
            from_ts = iso_ms(now - timedelta(days=days))
            to_ts = iso_ms(now)
        q: Dict[str, str] = {}
        if from_ts:
            q["from"] = from_ts
        if to_ts:
            q["to"] = to_ts
        if page_size is not None:
            q["pageSize"] = str(page_size)
        if cursor is not None:
            q["cursor"] = str(cursor)
        return self._request("GET", "/api/v1/collab/points/heartbeats", None,
                             query=q or None, rate="pointsRead", auth="device")

    def collab_approvals(self, scope: str = "pending", auth: Optional[str] = None) -> dict:
        """查看待我审批（只读）。批准/驳回必须在网页完成：本端只查看，不提供审批命令。

        auth 可显式指定通道，**仅供一致性验证使用**：契约 §5 规定审批只接受通道 A，
        通道 B 调用必须被拒 —— 这条约束需要一个"能故意用错通道"的入口才能真正测到。
        生产调用一律使用默认值（通道 A）。
        """
        return self._request("GET", "/api/v1/collab/approvals", None, query={"scope": scope},
                             rate="collabRead", auth=auth or "user")

    # ---------------- 底层请求 ----------------

    def _auth_headers(self, mode: str, actual_method: str, path: str,
                      query: Optional[Dict[str, str]], body_bytes: bytes) -> Dict[str, str]:
        if mode == "none":
            return {}
        if mode in ("user", "auto") and self.user_token:
            return {"Authorization": "Bearer " + self.user_token}
        if mode == "user":
            raise ZhiQiConfigError(
                "该接口仅接受人类登录态（通道 A）。请先配置用户令牌："
                "zhiqi config set userToken <令牌>（或环境变量 ZHIQI_USER_TOKEN）")
        if mode == "auto" and not self.store.exists():
            raise ZhiQiConfigError(
                "该接口需要用户令牌（通道 A）或已激活的设备身份（通道 B），当前两者皆无："
                "请先 zhiqi register，或 zhiqi config set userToken <令牌>")
        ident = self.store.require_identity()
        kp = self.keys()
        ts = crypto.now_ms()
        nonce = crypto.new_nonce()
        canonical = crypto.build_canonical(actual_method, path, query, ts, nonce,
                                           body_bytes, ident["agentCode"])
        return {
            "X-Agent-Id": ident["agentCode"],
            "X-Timestamp": str(ts),
            "X-Nonce": nonce,
            "X-Signature": kp.sign_base64(canonical.encode("utf-8")),
        }

    @staticmethod
    def _retry_after_seconds(resp: requests.Response, default: float = 1.0) -> float:
        raw = (resp.headers.get("Retry-After") or "").strip()
        if not raw:
            return default
        try:
            return max(0.0, float(raw))
        except ValueError:
            pass
        try:
            dt = parsedate_to_datetime(raw)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return max(0.0, (dt - datetime.now(timezone.utc)).total_seconds())
        except Exception:
            return default

    def _request(self, method: str, path: str, body: Optional[dict],
                 query: Optional[Dict[str, str]] = None, signed: bool = True,
                 method_override: Optional[str] = None, rate: Optional[str] = None,
                 auth: Optional[str] = None, binary: bool = False,
                 raw_body: Optional[bytes] = None,
                 content_type: Optional[str] = None):
        actual_method = method_override or method
        mode = auth if auth is not None else ("device" if signed else "none")

        if raw_body is not None:
            body_bytes = raw_body
        elif body is not None:
            body_bytes = json.dumps(body, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        else:
            body_bytes = b""

        if rate and self.limiter is not None:
            self.limiter.acquire(rate)   # 触发时抛 RateLimited（退出码 3）

        last_error: Optional[ZhiQiError] = None
        for attempt in range(self.max_retries + 1):
            headers = {"Accept": "*/*" if binary else "application/json"}
            if content_type:
                headers["Content-Type"] = content_type
            elif body is not None or raw_body is not None:
                headers["Content-Type"] = "application/json"
            headers.update(self._auth_headers(mode, actual_method, path, query, body_bytes))

            url = self.base_url + path
            try:
                resp = requests.request(actual_method, url, params=query,
                                        data=body_bytes if body_bytes else None,
                                        headers=headers, timeout=self.timeout)
            except requests.RequestException as e:
                last_error = ZhiQiError(1010, "网络请求失败: %s" % e)
                if attempt < self.max_retries:
                    time.sleep(min(2 ** attempt, 4) + 0.1 * attempt)
                    continue
                raise last_error

            if binary and resp.status_code == 200:
                return resp

            payload = self._parse(resp)
            # 二进制下载若返回非 JSON 错误页，按契约把 HTTP 状态映射为错误码
            # （越权/不可见统一 404 -> 4045；403 -> 1003；401 -> 1002）
            if binary and payload.get("code") == 1500 and resp.status_code in (401, 403, 404):
                payload = {"code": {401: 1002, 403: 1003, 404: 4045}[resp.status_code],
                           "message": "下载被拒绝（HTTP %s）" % resp.status_code}
            code = payload.get("code", -1)
            if code == 0:
                data = payload.get("data")
                # 部分接口直接返回 data 字段本身
                return data if data is not None else payload

            err = ZhiQiError(code, payload.get("message", "未知错误"),
                             payload.get("details"), payload.get("requestId"))
            # 平台限流（429 / 1009）：读取 Retry-After 退避，并临时收紧本地桶
            if code == 1009 or resp.status_code == 429:
                wait_s = self._retry_after_seconds(resp)
                if rate and self.limiter is not None:
                    self.limiter.on_retry_after(rate, wait_s)
                if attempt < self.max_retries:
                    last_error = err
                    time.sleep(min(wait_s, self.max_backoff))
                    continue
                raise err
            if code in RETRYABLE and attempt < self.max_retries:
                last_error = err
                time.sleep(min(2 ** attempt, 4))
                continue
            raise err
        raise last_error or ZhiQiError(1010, "请求失败")

    @staticmethod
    def _parse(resp: requests.Response) -> dict:
        try:
            return resp.json()
        except Exception:
            if resp.status_code == 403:
                return {"code": 1003, "message": "无权限（该接口仅接受对应的鉴权通道）"}
            return {"code": 1500, "message": "HTTP %s: %s" % (resp.status_code, resp.text[:200])}


def _multipart(fields: Dict[str, str], file_field: str, filename: str, content: bytes,
               content_type: str = "application/octet-stream"):
    """手工构造 multipart/form-data，保证签名的 BODY_SHA256 与实际发送字节一致。"""
    boundary = "----zhiqi" + secrets.token_hex(16)
    parts: List[bytes] = []
    for k, v in fields.items():
        parts.append(
            ("--%s\r\nContent-Disposition: form-data; name=\"%s\"\r\n\r\n%s\r\n"
             % (boundary, k, v)).encode("utf-8"))
    parts.append(
        ("--%s\r\nContent-Disposition: form-data; name=\"%s\"; filename=\"%s\"\r\n"
         "Content-Type: %s\r\n\r\n" % (boundary, file_field, filename, content_type)).encode("utf-8"))
    parts.append(content)
    parts.append(("\r\n--%s--\r\n" % boundary).encode("utf-8"))
    return "multipart/form-data; boundary=%s" % boundary, b"".join(parts)
