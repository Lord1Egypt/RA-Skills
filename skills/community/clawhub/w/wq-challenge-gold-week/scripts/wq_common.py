#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wq_common.py —— WorldQuant BRAIN API 共享工具模块

被 bootstrap.py / mine.py / submit_daily.py / check_score.py 四个脚本复用,职责:

- 凭证读取:只从环境变量读取(主用 BRAIN_EMAIL / BRAIN_PASSWORD,兼容 BRAIN_USER / BRAIN_PASS),
  绝不硬编码、绝不落盘明文。缺失时打印中文指引并退出。
- 会话管理:POST /authentication(HTTP Basic,期望 201);
  请求过程中遇 401 自动重认证一次;遇 429 按 Retry-After 头退避重试。
- 通用工具:分页拉取、alpha 指标读取、PnL 拉取并差分成日收益(带本地缓存)、
  Pearson 相关系数、universe 大小映射、jsonl 读写。

平台礼仪(硬约定,请勿修改数值去"绕过"限制):
- 并发回测上限 K = 2(低 tier 账号级硬限制)
- 轮询间隔 8 秒
- 429 限流按 Retry-After 等待,绝不硬刚

用法:本模块只被 import,不单独运行。
    from wq_common import BrainSession, WORKSPACE, paginate, ...

依赖:requests、numpy(其余均为标准库)。
"""

import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import requests

# ---------------------------------------------------------------------------
# 常量:API 与门槛(与 SKILL.md 完全对齐)
# ---------------------------------------------------------------------------

BASE = "https://api.worldquantbrain.com"   # API Base(见 SKILL.md §1.2)

POLL_INTERVAL = 8          # 轮询间隔(秒)—— 尊重平台,别打太快
MAX_CONCURRENCY = 2        # K=2 并发回测上限(账号级硬限制,绝不绕过)

SHARPE_MIN = 1.25          # 提交硬门槛 1:Sharpe ≥ 1.25
FITNESS_MIN = 1.0          # 提交硬门槛 2:Fitness ≥ 1.0
CORR_SUBMIT_MAX = 0.70     # 提交硬门槛 3:对已 ACTIVE 集合自相关 < 0.7(≥0.75 必被挡)
CORR_POOL_MAX = 0.90       # 入池(本地 keeper 库)去重阈值:池内多样性用,比提交线宽松

# 工作目录:所有运行时产物统一放这里(脚本自动创建,不污染仓库)
WORKSPACE = Path("wq_workspace")
PNL_CACHE_DIR = WORKSPACE / "pnl_cache"     # 各 alpha 的 PnL 缓存,避免重复拉
ARSENAL_PATH = WORKSPACE / "arsenal_usa.json"
POOL_PATH = WORKSPACE / "pool.jsonl"        # 过了三道门的 keeper 候选池
TRIED_PATH = WORKSPACE / "tried.txt"        # 已回测过的表达式(跨次运行去重)
SUBMIT_LOG_PATH = WORKSPACE / "submit_log.jsonl"

# universe 名称 → 股票数量(排序用:越小越优,见 SKILL.md §4.3)
UNIVERSE_SIZE = {
    "TOP200": 200, "TOP500": 500, "TOP1000": 1000, "TOP1200": 1200,
    "TOP2000": 2000, "TOP2500": 2500, "TOP3000": 3000, "TOPSP500": 500,
}


def universe_size(name):
    """universe 名称转规模;未知名称给一个大数,排序时垫底。"""
    return UNIVERSE_SIZE.get(str(name).upper(), 999999)


def ensure_workspace():
    """创建工作目录(幂等)。"""
    PNL_CACHE_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# 凭证与会话
# ---------------------------------------------------------------------------

_CRED_GUIDE = """
[缺少凭证] 未找到 BRAIN 账号环境变量。

请先在 shell 里导出你的 BRAIN 登录邮箱与密码(注册见 SKILL.md §1.2):

    export BRAIN_EMAIL="你的注册邮箱"
    export BRAIN_PASSWORD="你的登录密码"

(也兼容 BRAIN_USER / BRAIN_PASS 这对变量名,二选一即可。)

凭证安全铁律(SKILL.md 避坑⑥):
- 只放环境变量或被 .gitignore 的本地文件,绝不硬编码进代码
- 绝不提交进 Git、绝不粘进聊天记录 / issue
"""


def get_credentials():
    """从环境变量读取凭证;缺失则打印中文指引并退出。绝不硬编码。"""
    user = os.environ.get("BRAIN_EMAIL") or os.environ.get("BRAIN_USER")
    pwd = os.environ.get("BRAIN_PASSWORD") or os.environ.get("BRAIN_PASS")
    if not user or not pwd:
        print(_CRED_GUIDE)
        sys.exit(1)
    return user, pwd


class BrainSession:
    """带自动重认证与限流退避的 BRAIN API 会话。

    - 认证:HTTP Basic 打到 POST /authentication,期望 HTTP 201
    - 401:自动重认证一次后重试原请求(会话过期的常见情形)
    - 429:读 Retry-After 头退避重试(默认 15 秒),最多重试 10 次
    """

    def __init__(self):
        self._user, self._pwd = get_credentials()
        self.sess = requests.Session()
        self.login()

    def login(self):
        """POST /authentication 换取会话。成功返回 201,否则打印原因并退出。"""
        self.sess.auth = (self._user, self._pwd)
        try:
            r = self.sess.post(f"{BASE}/authentication", timeout=30)
        except requests.RequestException as e:
            print(f"[认证失败] 网络错误:{e}")
            sys.exit(1)
        if r.status_code != 201:
            print(f"[认证失败] POST /authentication 返回 HTTP {r.status_code}(期望 201)。")
            if r.status_code == 401:
                print("  → 邮箱或密码不对。请核对 BRAIN_EMAIL / BRAIN_PASSWORD 环境变量。")
            elif r.status_code == 429:
                print("  → 认证被限流,请稍等几分钟再试。")
            else:
                print(f"  → 响应片段:{r.text[:300]}")
            sys.exit(1)
        return r

    def request(self, method, url, **kw):
        """统一请求入口:429 退避 + 401 重认证一次。"""
        kw.setdefault("timeout", 60)
        reauth_left = 1          # 401 只自动重认证一次(SKILL.md 约定)
        retry_429_left = 10      # 429 有限次退避,避免死循环
        while True:
            r = self.sess.request(method, url, **kw)
            if r.status_code == 429 and retry_429_left > 0:
                wait = _retry_after_seconds(r, default=15.0)
                print(f"  [限流 429] 按 Retry-After 等待 {wait:.0f} 秒后重试 …")
                time.sleep(wait)
                retry_429_left -= 1
                continue
            if r.status_code == 401 and reauth_left > 0:
                print("  [会话过期 401] 自动重认证一次 …")
                self.login()
                reauth_left -= 1
                continue
            return r

    def get(self, url, **kw):
        return self.request("GET", url, **kw)

    def post(self, url, **kw):
        return self.request("POST", url, **kw)


def _retry_after_seconds(resp, default=15.0):
    """解析 Retry-After 头(秒)。解析失败用默认值。"""
    try:
        v = float(resp.headers.get("Retry-After", "") or default)
        return max(v, 1.0)
    except (TypeError, ValueError):
        return default


# ---------------------------------------------------------------------------
# 分页与 alpha 读取
# ---------------------------------------------------------------------------

def paginate(bs, url, params=None, limit=50):
    """通用分页:按 limit/offset 翻页,直到拉完 count 条(SKILL.md §2.2 的翻页方式)。"""
    results, offset = [], 0
    while True:
        p = dict(params or {})
        p.update({"limit": limit, "offset": offset})
        r = bs.get(url, params=p)
        r.raise_for_status()
        data = r.json()
        batch = data.get("results", [])
        results.extend(batch)
        offset += limit
        if not batch or offset >= data.get("count", 0):
            break
    return results


def get_alpha(bs, alpha_id):
    """GET /alphas/{id}:读取指标(is.sharpe / is.fitness / is.checks …)与状态。"""
    r = bs.get(f"{BASE}/alphas/{alpha_id}")
    r.raise_for_status()
    return r.json()


def alpha_failed_checks(alpha):
    """汇总 alpha 的 FAIL 检查项名字(is.checks 与顶层 checks 都看,以防结构差异)。"""
    checks = []
    checks += (alpha.get("is") or {}).get("checks") or []
    checks += alpha.get("checks") or []
    return sorted({c.get("name", "?") for c in checks if c.get("result") == "FAIL"})


# ---------------------------------------------------------------------------
# PnL → 日收益(带缓存)与相关系数
# ---------------------------------------------------------------------------

def get_daily_returns(bs, alpha_id, use_cache=True):
    """拉 GET /alphas/{id}/recordsets/pnl,把累计 PnL 差分成日收益序列。

    - 结果缓存到 wq_workspace/pnl_cache/{id}.json,避免重复拉(删缓存即强制刷新)
    - recordsets 生成中时平台会返回空体 + Retry-After 头,按头等待重试
    - 返回 list[float];拉不到返回 None
    """
    ensure_workspace()
    cache = PNL_CACHE_DIR / f"{alpha_id}.json"
    if use_cache and cache.exists():
        try:
            data = json.loads(cache.read_text())
        except (OSError, json.JSONDecodeError):
            data = None
        if data:
            return _pnl_to_returns(data)

    data = None
    for _ in range(20):  # recordsets 可能在后台生成,礼貌地按 Retry-After 等
        r = bs.get(f"{BASE}/alphas/{alpha_id}/recordsets/pnl")
        if r.status_code != 200:
            print(f"  [PnL] alpha {alpha_id} 拉取失败:HTTP {r.status_code}")
            return None
        if not r.text.strip():
            time.sleep(_retry_after_seconds(r, default=float(POLL_INTERVAL)))
            continue
        data = r.json()
        break
    if not data or not data.get("records"):
        print(f"  [PnL] alpha {alpha_id} 无 records,放弃")
        return None

    cache.write_text(json.dumps(data))
    return _pnl_to_returns(data)


def _pnl_to_returns(data):
    """把 recordsets/pnl 的 records(累计 PnL)差分成日收益。"""
    records = data.get("records") or []
    if len(records) < 2:
        return None
    # 从 schema 里找 pnl 列的下标;找不到就取最后一列
    idx = -1
    props = (data.get("schema") or {}).get("properties") or []
    for i, p in enumerate(props):
        if p.get("name") == "pnl":
            idx = i
            break
    series = []
    for row in records:
        try:
            v = row[idx]
        except (IndexError, TypeError):
            v = None
        series.append(float(v) if v is not None else None)
    # 缺失值用前值填充后再差分
    filled, last = [], 0.0
    for v in series:
        if v is not None:
            last = v
        filled.append(last)
    arr = np.asarray(filled, dtype=float)
    return np.diff(arr).tolist()


def pearson(a, b, min_overlap=20):
    """两条日收益序列的 Pearson 相关(按尾部对齐);重叠太短或方差为 0 时返回 0.0。"""
    n = min(len(a), len(b))
    if n < min_overlap:
        return 0.0
    x = np.asarray(a[-n:], dtype=float)
    y = np.asarray(b[-n:], dtype=float)
    if float(x.std()) == 0.0 or float(y.std()) == 0.0:
        return 0.0
    return float(np.corrcoef(x, y)[0, 1])


def max_abs_corr(cand_returns, basis_returns_list):
    """候选对一组基准序列的最大 |Pearson 相关|(SKILL.md §4.2 可过性预测器)。"""
    if not basis_returns_list:
        return 0.0
    return max(abs(pearson(cand_returns, b)) for b in basis_returns_list)


# ---------------------------------------------------------------------------
# jsonl / 文本小工具
# ---------------------------------------------------------------------------

def load_jsonl(path):
    """读 jsonl 为 list[dict];文件不存在返回空列表;坏行跳过。"""
    path = Path(path)
    if not path.exists():
        return []
    out = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def append_jsonl(path, obj):
    """追加一行 jsonl 并立即落盘(Ctrl-C 中断也不丢已写进度)。"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fp:
        fp.write(json.dumps(obj, ensure_ascii=False) + "\n")
        fp.flush()
        os.fsync(fp.fileno())


def load_tried():
    """读已试过的表达式集合(tried.txt,每行一条)。"""
    if not TRIED_PATH.exists():
        return set()
    return {ln.strip() for ln in TRIED_PATH.read_text().splitlines() if ln.strip()}


def mark_tried(expr):
    """把表达式追加进 tried.txt 并立即落盘。"""
    TRIED_PATH.parent.mkdir(parents=True, exist_ok=True)
    with TRIED_PATH.open("a", encoding="utf-8") as fp:
        fp.write(expr + "\n")
        fp.flush()
        os.fsync(fp.fileno())
