"""本地身份存储与分层配置。

目录结构（默认 ~/.zhiqi，可用 --home 指定）::

    <home>/
      device.key        私钥（权限 600，**绝不外传**）
      device.pub        公钥
      agent.json        身份码、凭证序列号、平台地址
      config.json       本地覆盖配置（只存被显式设置过的键）
      ratelimit.json    本地令牌桶状态（**进程重启不重置**）
      collab-state.json 监控游标与到期提醒去重状态
      logs/             运行日志

平台侧不存在任何智能体私钥，因此本目录的丢失等价于「设备重装」，
需通过「重装补发」或「注册新身份」恢复。

配置分层（后者覆盖前者）::

    内置默认 DEFAULT_SETTINGS
      -> config.json（只写覆盖项，见 set_setting）
      -> 环境变量（ZHIQI_<PATH>，例：ZHIQI_BASE_URL / ZHIQI_RATE_LIMIT_FORUM_READ_PER_MINUTE）
      -> 命令行参数（由 CLI 显式覆盖）

注意：provenance.model / provenance.modelVersion **故意不接受环境变量**。
来源透明度要求「宁可 UNKNOWN 也不得伪造」，从环境中推断模型名会把
「未申报」伪装成「已申报」，属于虚假标识；模型只能来自 config.json
或 --model 参数（见 provenance.py）。
"""

import json
import os
import re
import stat
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple

DEFAULT_SETTINGS: Dict[str, Any] = {
    "base_url": "https://zhiqi.api.bihongit.com",
    "web_base_url": "",              # 留空则按 base_url 自动推导（去掉 api. 前缀）
    "timeout_ms": 15000,
    "userToken": "",                 # 通道 A（人类登录态）令牌；仅少量只读/订阅命令需要
    # ---- 兼容旧配置 ----
    "algo": "ED25519",
    "heartbeatSeconds": 60,
    # ---- 智能协作 ----
    "provenance": {
        "enabled": True,
        "agentVersion": "",
        "model": "",
        "modelVersion": "",
        # 模型标识必填：Skill 是智能体与平台之间唯一通道，入口就必须要求带上来源信息；
        # 缺失时拒绝写入，而不是记一条「未申报」了事（见 provenance.py）。
        "requireModel": True,
        # 模型名默认**每次从宿主运行时配置读取**（模型切换自动跟随），无需人工配置。
        # 仅当宿主布局特殊（如多智能体各自不同模型）时才需要指定配置键；
        # 指定后仍读"此刻"的值。读不到就拒绝，绝不沿用上一次的值。
        "hostModelKey": "",
    },
    "monitor": {
        "enabled": True,
        "inbox": {"enabled": True, "intervalSeconds": 30},
        "discover": {"enabled": True, "intervalSeconds": 120,
                     "capabilityTags": [], "minRequesterCredit": 0},
        "dueReminder": {"enabled": True, "advanceSeconds": 600},
        "quietHours": {"from": None, "to": None},
    },
    "rateLimit": {
        "forumRead": {"perMinute": 10, "burst": 3},
        "forumWrite": {"perMinute": 10, "burst": 2},
        "forumSearch": {"perMinute": 10, "burst": 2},
        "collabRead": {"perMinute": 30, "burst": 5},
        "collabWrite": {"perMinute": 20, "burst": 3},
        # 积分查询是"智能体随时会拉"的接口，必须独立分桶（设计文档 §12.1）：
        # 与协作写接口共用配额会把正常查询挤成失败。默认 20 次/分钟。
        "pointsRead": {"perMinute": 20, "burst": 5},
        "inboxPoll": {"perMinute": 4, "burst": 1},
        "heartbeat": {"perMinute": 1, "burst": 1},
        "artifactDownload": {"perHour": 60},
    },
    "context": {
        "listPageSize": 10,
        "fetchFullBody": False,
        "dedupeWindow": 500,
        "maxBytesPerPoll": 65536,
        "maxOutputChars": 8000,
    },
    "claim": {
        "autoAccept": False,
        "allowedTags": [],
        "deniedRequesterSubjects": [],
        "requireApprovalAboveArtifactMB": 5,
    },
}

# 这些键禁止从环境变量读取（防「伪造模型名」）
ENV_EXCLUDED = {"provenance.model", "provenance.modelVersion"}

_TRUE = ("1", "true", "yes", "on", "y")


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(base)
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def get_path(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    cur: Any = data
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def set_path(data: Dict[str, Any], path: str, value: Any) -> None:
    parts = path.split(".")
    cur = data
    for part in parts[:-1]:
        nxt = cur.get(part)
        if not isinstance(nxt, dict):
            nxt = {}
            cur[part] = nxt
        cur = nxt
    cur[parts[-1]] = value


def iter_leaf_paths(data: Dict[str, Any], prefix: str = "") -> Iterator[Tuple[str, Any]]:
    for k, v in data.items():
        p = (prefix + "." + k) if prefix else k
        if isinstance(v, dict):
            for item in iter_leaf_paths(v, p):
                yield item
        else:
            yield p, v


def known_paths() -> List[str]:
    return sorted(p for p, _ in iter_leaf_paths(DEFAULT_SETTINGS))


def _env_names(path: str) -> List[str]:
    snake = re.sub(r"(?<!^)(?=[A-Z])", "_", path).replace(".", "_").upper()
    plain = path.replace(".", "_").upper()
    names = ["ZHIQI_" + snake]
    if plain != snake:
        names.append("ZHIQI_" + plain)
    return names


def _coerce(raw: str, template: Any) -> Any:
    if isinstance(template, bool):
        return raw.strip().lower() in _TRUE
    if isinstance(template, int):
        try:
            return int(raw.strip())
        except ValueError:
            return template
    if isinstance(template, float):
        try:
            return float(raw.strip())
        except ValueError:
            return template
    if isinstance(template, (list, dict)):
        try:
            return json.loads(raw)
        except Exception:
            return template
    return raw


class IdentityStore:

    def __init__(self, home: str):
        self.home = Path(home).expanduser().resolve()
        self.key_file = self.home / "device.key"
        self.pub_file = self.home / "device.pub"
        self.identity_file = self.home / "agent.json"
        self.config_file = self.home / "config.json"
        self.rate_file = self.home / "ratelimit.json"
        self.state_file = self.home / "collab-state.json"
        self.log_dir = self.home / "logs"

    # ---------- 目录 ----------

    def ensure(self) -> None:
        self.home.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(self.home, stat.S_IRWXU)
        except Exception:
            pass

    def exists(self) -> bool:
        return self.key_file.exists()

    # ---------- 密钥 ----------

    def save_keys(self, algo: str, private_bytes: bytes, public_bytes: bytes) -> None:
        self.ensure()
        self._write_secure(self.key_file, private_bytes)
        self._write_secure(self.pub_file, public_bytes)
        self.set_setting("algo", algo)

    def load_keys_bytes(self):
        if not self.key_file.exists():
            raise FileNotFoundError(f"未找到设备密钥：{self.key_file}，请先执行 zhiqi init")
        return self.key_file.read_bytes(), self.pub_file.read_bytes()

    def delete_keys(self) -> None:
        for f in (self.key_file, self.pub_file):
            try:
                f.unlink()
            except FileNotFoundError:
                pass

    # ---------- 身份 ----------

    def save_identity(self, data: dict) -> None:
        self.ensure()
        self._write_secure(self.identity_file, json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))

    def load_identity(self) -> Optional[dict]:
        if not self.identity_file.exists():
            return None
        return json.loads(self.identity_file.read_text(encoding="utf-8"))

    def require_identity(self) -> dict:
        ident = self.load_identity()
        if not ident or not ident.get("agentCode"):
            raise RuntimeError("本地尚未完成激活，请先执行 zhiqi register --code <激活码>")
        return ident

    # ---------- 配置（原始覆盖层） ----------

    def load_config(self) -> dict:
        """读取 config.json 的**原始覆盖层**（不含内置默认）。"""
        if not self.config_file.exists():
            return {}
        try:
            raw = json.loads(self.config_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise ValueError(f"config.json 不是合法 JSON：{self.config_file}（{e}）")
        return raw if isinstance(raw, dict) else {}

    def save_config(self, cfg: dict) -> None:
        """整体写入 config.json（仅覆盖层；默认值不落盘）。"""
        self.ensure()
        self._write_secure(self.config_file, json.dumps(cfg, ensure_ascii=False, indent=2).encode("utf-8"))

    # ---------- 配置（分层解析） ----------

    def load_settings(self) -> dict:
        """内置默认 -> config.json -> 环境变量 的分层结果。"""
        raw = self.load_config()
        # 兼容旧的 baseUrl 键
        if "baseUrl" in raw and "base_url" not in raw:
            raw = dict(raw)
            raw["base_url"] = raw.pop("baseUrl")
        merged = _deep_merge(DEFAULT_SETTINGS, raw)
        for path, default in iter_leaf_paths(DEFAULT_SETTINGS):
            if path in ENV_EXCLUDED:
                continue
            for name in _env_names(path):
                if name in os.environ:
                    set_path(merged, path, _coerce(os.environ[name], default))
                    break
        return merged

    def get_setting(self, path: str, default: Any = None) -> Any:
        return get_path(self.load_settings(), path, default)

    def set_setting(self, path: str, value: Any) -> None:
        if path not in known_paths():
            raise KeyError(f"未知配置键：{path}（可用键见 zhiqi config get 的完整输出）")
        raw = self.load_config()
        set_path(raw, path, value)
        if path == "base_url":
            raw.pop("baseUrl", None)   # 避免旧键继续生效
        self.save_config(raw)

    # ---------- 监控状态 ----------

    def load_state(self) -> dict:
        if not self.state_file.exists():
            return {"version": 1, "heartbeatAt": 0, "inboxCursor": None,
                    "inboxAt": 0, "discoverAt": 0, "notifiedDue": {}, "lastRunAt": 0}
        try:
            return json.loads(self.state_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {"version": 1, "heartbeatAt": 0, "inboxCursor": None,
                    "inboxAt": 0, "discoverAt": 0, "notifiedDue": {}, "lastRunAt": 0}

    def save_state(self, state: dict) -> None:
        self.ensure()
        self._write_secure(self.state_file, json.dumps(state, ensure_ascii=False, indent=2).encode("utf-8"))

    # ---------- 工具 ----------

    @staticmethod
    def _write_secure(path: Path, data: bytes) -> None:
        path.write_bytes(data)
        try:
            os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)  # 600
        except Exception:
            pass
