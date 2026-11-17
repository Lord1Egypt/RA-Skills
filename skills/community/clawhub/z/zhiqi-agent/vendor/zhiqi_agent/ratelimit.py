"""本地限流（令牌桶，状态持久化）。

**定位**：本地限流是「自保」，不是安全边界。平台侧限流才是权威；
本模块用于避免接入端把平台打爆、避免触发平台风控。

规则：
  - 每个类别（论坛读/写/检索、协作读/写、收件箱、心跳、下载）**独立分桶**
  - 桶状态持久化到 <home>/ratelimit.json，**进程重启不重置**
  - 触发限流**不静默失败**：抛出 RateLimited，带剩余等待秒数；CLI 以退出码 3 结束
  - --wait：阻塞直到令牌可用；--force：跳过（记日志，因为它不是安全边界）
  - 收到平台 429 / 1009 时读取 Retry-After 并自动退避，同时临时收紧本地桶
"""

import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, Optional

from .store import DEFAULT_SETTINGS

log = logging.getLogger("zhiqi.ratelimit")

# 收到 429/1009 时最多自动退避的秒数（避免无限等待）
MAX_BACKOFF_SECONDS = 60.0

# 硬退避结束后，本地桶继续「临时收紧」的时长（容量压到 1）
TIGHTEN_WINDOW_SECONDS = 60.0


class RateLimited(Exception):
    """本地限流触发（不静默失败）。"""

    def __init__(self, category: str, wait_seconds: float):
        self.category = category
        self.wait_seconds = max(0.0, float(wait_seconds))
        super().__init__(
            "本地限流：类别 %s 已达上限，需等待 %.1f 秒。"
            "可用 --wait 自动等待，或 --force 跳过（本地限流是自保不是安全边界）。"
            % (category, self.wait_seconds)
        )


def bucket_params(cfg: Dict[str, Any]) -> Dict[str, float]:
    """把配置项换算为 (rate 令牌/秒, capacity 桶容量)。"""
    per_minute = cfg.get("perMinute")
    per_hour = cfg.get("perHour")
    if per_minute:
        rate = float(per_minute) / 60.0
    elif per_hour:
        rate = float(per_hour) / 3600.0
    else:
        rate = 1.0 / 60.0
    burst = cfg.get("burst")
    capacity = float(burst) if burst else 1.0
    return {"rate": max(rate, 1e-9), "capacity": max(capacity, 1.0)}


class RateLimiter:
    """按类别分桶的持久化令牌桶限流器。"""

    def __init__(self, home, settings: Optional[dict] = None, wait: bool = False,
                 force: bool = False, clock=None, sleeper=None, logger=None):
        self.home = Path(home).expanduser().resolve()
        self.state_file = self.home / "ratelimit.json"
        self.force_log = self.home / "logs" / "ratelimit-force.log"
        self.settings = settings if settings is not None else dict(DEFAULT_SETTINGS)
        self.limit_cfg = (self.settings or {}).get("rateLimit") or DEFAULT_SETTINGS["rateLimit"]
        self.wait = bool(wait)
        self.force = bool(force)
        self.clock = clock or time.time
        self.sleeper = sleeper or time.sleep
        self.log = logger or log
        self._state = self._load()

    # ---------------- 状态持久化 ----------------

    def _load(self) -> dict:
        if not self.state_file.exists():
            return {"version": 1, "buckets": {}}
        try:
            data = json.loads(self.state_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {"version": 1, "buckets": {}}
        if not isinstance(data, dict) or "buckets" not in data:
            return {"version": 1, "buckets": {}}
        return data

    def _save(self) -> None:
        try:
            self.home.mkdir(parents=True, exist_ok=True)
            self.state_file.write_text(
                json.dumps(self._state, ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError as e:  # 状态写失败不阻断请求，但必须可见
            self.log.warning("限流状态写入失败：%s", e)

    def reset(self) -> None:
        """清空全部桶状态（仅测试/排障使用）。"""
        self._state = {"version": 1, "buckets": {}}
        self._save()

    # ---------------- 桶计算 ----------------

    def _cfg_for(self, category: str) -> Dict[str, float]:
        raw = self.limit_cfg.get(category)
        return bucket_params(raw or {})

    def _bucket(self, category: str) -> dict:
        now = self.clock()
        b = self._state["buckets"].get(category)
        params = self._cfg_for(category)
        if b is None:
            b = {"tokens": params["capacity"], "updatedAt": now,
                 "penaltyUntil": 0.0, "tightUntil": 0.0}
            self._state["buckets"][category] = b
        return b

    def _refill(self, category: str, b: dict) -> Dict[str, float]:
        params = self._cfg_for(category)
        now = self.clock()
        capacity = params["capacity"]
        if now < float(b.get("tightUntil", 0.0)):
            capacity = min(capacity, 1.0)   # 临时收紧：容量压到 1
        elapsed = max(0.0, now - float(b.get("updatedAt", now)))
        b["tokens"] = min(capacity, float(b.get("tokens", capacity)) + elapsed * params["rate"])
        b["updatedAt"] = now
        params["capacity"] = capacity
        return params

    # ---------------- 取令牌 ----------------

    def try_acquire(self, category: str, tokens: int = 1):
        """返回 (是否允许, 需要等待秒数)；不阻塞、不抛异常。"""
        now = self.clock()
        b = self._bucket(category)
        penalty_until = float(b.get("penaltyUntil", 0.0))
        if now < penalty_until:
            self._save()
            return False, penalty_until - now
        params = self._refill(category, b)
        if float(b["tokens"]) >= tokens:
            b["tokens"] = float(b["tokens"]) - tokens
            self._save()
            return True, 0.0
        wait = (tokens - float(b["tokens"])) / params["rate"]
        self._save()
        return False, wait

    def acquire(self, category: str, tokens: int = 1) -> None:
        """取令牌；不允许则抛 RateLimited（--wait 时先等待）。"""
        if self.force:
            self._record_force(category)
            return
        allowed, wait = self.try_acquire(category, tokens)
        if allowed:
            return
        if self.wait and wait > 0:
            self.sleeper(min(wait, MAX_BACKOFF_SECONDS) + 0.01)
            allowed, wait2 = self.try_acquire(category, tokens)
            if allowed:
                return
            raise RateLimited(category, wait2)
        raise RateLimited(category, wait)

    def on_retry_after(self, category: str, seconds: float) -> float:
        """平台返回 429/1009 时调用：退避 + 临时收紧本地桶。"""
        seconds = max(1.0, float(seconds))
        now = self.clock()
        b = self._bucket(category)
        b["penaltyUntil"] = max(float(b.get("penaltyUntil", 0.0)), now + seconds)
        # 硬退避结束后再收紧一段时间，避免刚放开就再次打爆平台
        b["tightUntil"] = max(float(b.get("tightUntil", 0.0)),
                              now + seconds + TIGHTEN_WINDOW_SECONDS)
        b["tokens"] = 0.0
        b["updatedAt"] = now
        self._save()
        self.log.warning("平台限流：类别 %s 退避 %.0f 秒并临时收紧本地桶", category, seconds)
        return seconds

    # ---------------- 跳过记录 ----------------

    def _record_force(self, category: str) -> None:
        line = "%s FORCE-SKIP category=%s\n" % (
            time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(self.clock())), category)
        try:
            self.force_log.parent.mkdir(parents=True, exist_ok=True)
            with self.force_log.open("a", encoding="utf-8") as f:
                f.write(line)
        except OSError:
            pass
        self.log.warning("已用 --force 跳过本地限流：类别 %s（本地限流是自保不是安全边界）", category)

    # ---------------- 观察 ----------------

    def remaining(self, category: str) -> float:
        """当前类别可用令牌数（只读，不改变状态）。"""
        b = self._state["buckets"].get(category)
        if b is None:
            return self._cfg_for(category)["capacity"]
        params = self._cfg_for(category)
        now = self.clock()
        elapsed = max(0.0, now - float(b.get("updatedAt", now)))
        capacity = params["capacity"]
        if now < float(b.get("tightUntil", 0.0)):
            capacity = min(capacity, 1.0)
        return min(capacity, float(b.get("tokens", capacity)) + elapsed * params["rate"])
