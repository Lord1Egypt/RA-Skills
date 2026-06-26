# -*- coding: utf-8 -*-
"""qgdata 共享常量与工具函数（所有模块统一 import 此文件）"""
import os, re, time

QGDATA_RECHARGE_URL = "https://quantgo.ai/data"
QGDATA_SHARED_TOKEN = os.getenv("QGDATA_SHARED_TOKEN", "Mj9mN2xP5qR8vL3tY7wZ1aB4cD6eF8gH9nX4pL2qR7sT5vY8wZ1aB3cD3Tgd7ffg") #专用试用token，后端已做限流（每IP每日有限额度），可环境变量覆盖
QGDATA_TOKEN_RE = re.compile(r'[A-Za-z0-9]{60,70}')

def mask_token(token: str) -> str:
    return (token[:6] + "***") if token and len(token) > 6 else "***"

try: QG_MIN_INTERVAL_SEC = max(0.0, float(os.getenv("QGDATA_MIN_INTERVAL_SEC", "0.22"))) #默认≈4.5 rps
except (ValueError, TypeError): QG_MIN_INTERVAL_SEC = 0.22
try: QG_RETRY_MAX = max(1, int(os.getenv("QGDATA_RETRY_MAX", "3")))
except (ValueError, TypeError): QG_RETRY_MAX = 3
_QG_LAST_TS = 0.0

def qg_throttle():
    """最小间隔节流，所有 qgdata 调用前统一调用"""
    global _QG_LAST_TS
    if QG_MIN_INTERVAL_SEC <= 0: return
    now = time.time()
    wait = QG_MIN_INTERVAL_SEC - (now - _QG_LAST_TS)
    if wait > 0: time.sleep(wait)
    _QG_LAST_TS = time.time()

def qg_retryable(exc: Exception) -> bool:
    m = str(exc).lower()
    return any(k in m for k in ("429", "rate limit", "too many requests", "系统异常", "稍候再试", "timeout", "timed out", "temporarily unavailable", "connection reset"))

def qg_call(fn):
    """节流+重试封装：fn 为无参 callable，返回调用结果"""
    last = None
    for i in range(QG_RETRY_MAX):
        try:
            qg_throttle()
            return fn()
        except Exception as e:
            last = e
            if (not qg_retryable(e)) or i == QG_RETRY_MAX - 1: raise
            time.sleep(min(1.2, 0.25 * (2 ** i)))
    raise last if last else RuntimeError("qg_call failed")

def classify_qgdata_error(exc: Exception) -> tuple[str, str]:
    """分类qgdata异常→(error_code, 用户提示)。error_code: unauthorized|quota_exceeded|forbidden|api_transient|api_error"""
    msg = str(exc).lower()
    _http_re = re.search(r'\b(401|403|429)\b', msg)
    if "unauthorized" in msg or (_http_re and _http_re.group(1) == "401"):
        return "unauthorized", f"数据服务未授权，请配置有效Token。获取Token: {QGDATA_RECHARGE_URL}"
    if any(kw in msg for kw in ["额度已达上限", "额度不足", "quota", "rate limit", "too many requests"]) or (_http_re and _http_re.group(1) == "429"):
        return "quota_exceeded", f"当日额度已达上限，去 {QGDATA_RECHARGE_URL} 解锁更多能力"
    if "forbidden" in msg or "权限不足" in msg or (_http_re and _http_re.group(1) == "403"):
        return "forbidden", f"当前套餐无此接口权限，去 {QGDATA_RECHARGE_URL} 升级套餐"
    if any(kw in msg for kw in ["系统异常", "稍候再试", "temporarily unavailable", "timeout", "timed out", "connection reset"]):
        return "api_transient", "数据服务临时波动（可重试），建议稍后重试或降低请求频率"
    return "api_error", f"数据接口异常({type(exc).__name__}: {str(exc)[:100]})。如Token额度不足请到 {QGDATA_RECHARGE_URL} 充值"
