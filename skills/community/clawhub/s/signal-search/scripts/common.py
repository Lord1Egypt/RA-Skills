"""scripts/common.py - 共享基础设施（配置加载 + 通用工具）。

统一约定：
- `load_config`：传入 cfg 则原样返回（支持调用方注入 / 测试 mock）；否则读取项目根
  config.json，缺失或损坏时返回 {}（不抛异常，顺带修 connector 缺键崩溃 F12）。
- `BoundedTTLMap`：长跑进程用的有界 TTL 缓存，杜绝全局态"只增不减"。
其它模块用 `from common import load_config as _load_cfg` 替换本地副本即可。
"""

import functools
import json
import os
import re
import threading
import time
from collections import OrderedDict
from typing import Any, Dict, Optional

CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json"
)

_DOMAIN_RE = re.compile(r"https?://([^/]+)")

# 进程级默认配置单例：load_config() 无参时返回同一对象（双检锁）。
# 作用：① 避免每次 retrieve()/score_source() 重读磁盘 config.json（性能）；
#      ② 使默认 cfg 的 id() 稳定，杜绝「每请求新 dict → 以 id(cfg) 为键的全局缓存只增不减」
#        的内存泄漏（见 clean_sources._ACTIVE_SRCS_CACHE）。
# 约定：返回的是进程内共享单例，调用方不应就地 mutate；需改配置请传入自己的 dict。
# 磁盘文件变更后需重启进程方才生效（符合服务启动期加载惯例）。
_DEFAULT_CFG: Optional[Dict[str, Any]] = None
_DEFAULT_CFG_LOCK = threading.Lock()


def load_config(cfg: Any = None, force_reload: bool = False) -> Dict[str, Any]:
    """返回配置。

    - 传入 cfg：原样返回（支持调用方注入 / 测试 mock）。
    - 无参：返回进程级单例（双检锁缓存，避免每请求重读磁盘 + 稳定 id(cfg)）。
    - force_reload=True：绕过缓存重新读取（只读、不污染单例），供测试模拟「配置文件变更/
      缺失」场景使用；生产环境磁盘变更需重启进程方才生效。
    """
    if cfg is not None:
        return cfg
    if force_reload:
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    global _DEFAULT_CFG
    if _DEFAULT_CFG is None:
        with _DEFAULT_CFG_LOCK:
            if _DEFAULT_CFG is None:
                try:
                    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                        _DEFAULT_CFG = json.load(f)
                except Exception:
                    _DEFAULT_CFG = {}
    return _DEFAULT_CFG


def domain_of(url: str) -> str:
    """从 URL 取小写域名（含端口）；取不到返回空串。"""
    m = _DOMAIN_RE.search(url or "")
    return m.group(1).lower() if m else ""


# CJK 统一表意 + 日文假名（平/片）：纳入 n-gram 处理；韩文/阿拉伯文等按 Unicode 词切分
_CJK_RE = re.compile(r"[一-鿿ぁ-んァ-ヶ]")
_WORD_RE = re.compile(r"[^\s\W_]+", re.UNICODE)

# 内置紧凑高频词典（CJK 最大正向匹配用，覆盖常见通用/技术词；未登录词回退 n-gram）。
# 仅作"更完整词边界"的增量信号，不替代 n-gram，故不影响以 tokenize 为输入的打分/去重语义。
_CJK_DICT = frozenset("""
人工智能 机器学习 深度学习 神经网络 自然语言 自然语言处理 大语言模型 大模型 语义 检索 向量
数据库 区块链 云计算 边缘计算 操作系统 编程语言 正则表达式 数据结构 算法 分布式 微服务 容器
缓存 内存 线程 进程 协议 网络 传输 路由 防火墙 加密 哈希 签名 证书 隐私 安全 漏洞 攻击 防御
权限 认证 授权 用户 界面 体验 设计 测试 部署 运维 监控 日志 指标 性能 延迟 吞吐 可用性 一致性
可靠性 可扩展性 开源 框架 模块 函数 变量 类型 对象 继承 多态 封装 抽象 接口 实现 模式 架构
组件 服务 网关 负载 均衡 限流 熔断 降级 容错 备份 恢复 灾难 灾难恢复 预训练 微调 推理 训练
数据集 标注 评测 基准 基准测试
""".split())

_MAX_WORD = 6  # 最大正向匹配的最大词长


def _tokenize_cjk(seg: str) -> set:
    """CJK/假名段的零依赖分词：1–3 gram 覆盖（兼容旧 bigram） + 词典最大正向匹配（增量词边界）。"""
    toks = set()
    n = len(seg)
    # 1–3 gram：兼容旧 bigram 行为，并提升短摘要的语义重叠分辨率
    for i in range(n):
        toks.add(seg[i])
        if i + 1 < n:
            toks.add(seg[i : i + 2])
        if i + 2 < n:
            toks.add(seg[i : i + 3])
    # 词典最大正向匹配：捕捉更完整词边界（如"人工智能"而非仅"人工/工智/智能"）
    i = 0
    while i < n:
        matched = None
        for L in range(min(_MAX_WORD, n - i), 0, -1):
            cand = seg[i : i + L]
            if cand in _CJK_DICT:
                matched = cand
                break
        if matched:
            toks.add(matched)
            i += len(matched)
        else:
            i += 1
    return toks


@functools.lru_cache(maxsize=4096)
def tokenize(text: str) -> set:
    """多语种分词（P2-11 增强）：CJK+假名段做 1–3 gram + 词典最大正向匹配；其余脚本按 \\w+ 取词。

    零依赖、纯正则/内置词典。统一替换各处的 [\\w\\u4e00-\\u9fa5]{2,} 内联写法，供打分/去重的词重叠计算。
    - CJK（汉字）与日文假名：无空格语言，做 n-gram（兼容旧 bigram）并以紧凑词典做最大正向匹配，
      提升词边界与跨语言重叠分辨率；
    - 韩文/阿拉伯文等非空格脚本：按 Unicode 词切分（谚文按音节、阿拉伯文按词），小写归一；
    - 拉丁/数字：按词切分并小写归一。
    """
    text = (text or "").lower()
    toks = set()
    cjk = "".join(_CJK_RE.findall(text))
    if cjk:
        toks |= _tokenize_cjk(cjk)
    for w in _WORD_RE.findall(text):
        if not _CJK_RE.search(w):  # 含 CJK/假名的整体词已交给 n-gram，避免重复
            toks.add(w)
    return toks


class BoundedTTLMap:
    """线程安全的有界 TTL 字典：条目到期自动失效，超上限按 FIFO 淘汰。

    用于长跑进程里的全局态（域名封禁表、robots 判定缓存、节流时间戳等）。
    普通 dict/set 在这些场景下只增不减，会造成两类问题：
    1) 内存慢泄漏——域名基数无上界；
    2) 语义错误——一次瞬时 429 会把域名永久拉黑。
    """

    __slots__ = ("_maxsize", "_ttl", "_data", "_lock")

    def __init__(self, maxsize: int = 512, ttl: float = 300.0):
        self._maxsize = max(int(maxsize), 1)
        self._ttl = float(ttl)
        self._data: "OrderedDict[Any, Any]" = OrderedDict()
        self._lock = threading.RLock()

    # -- 内部：调用方必须已持锁 --
    def _purge_expired(self, now: Optional[float] = None) -> None:
        now = time.time() if now is None else now
        for key in [k for k, (_, exp) in self._data.items() if exp <= now]:
            self._data.pop(key, None)

    def get(self, key: Any, default: Any = None) -> Any:
        with self._lock:
            item = self._data.get(key)
            if item is None:
                return default
            value, expire_at = item
            if expire_at <= time.time():
                self._data.pop(key, None)
                return default
            return value

    def set(self, key: Any, value: Any, ttl: Optional[float] = None) -> None:
        with self._lock:
            self._purge_expired()
            if key in self._data:
                self._data.pop(key, None)
            while len(self._data) >= self._maxsize:
                self._data.popitem(last=False)  # FIFO 淘汰最早条目
            self._data[key] = (value, time.time() + (self._ttl if ttl is None else float(ttl)))

    def pop(self, key: Any, default: Any = None) -> Any:
        with self._lock:
            item = self._data.pop(key, None)
            return default if item is None else item[0]

    def clear(self) -> None:
        with self._lock:
            self._data.clear()

    def __contains__(self, key: Any) -> bool:
        return self.get(key, _MISSING) is not _MISSING

    def __len__(self) -> int:
        with self._lock:
            self._purge_expired()
            return len(self._data)


_MISSING = object()
