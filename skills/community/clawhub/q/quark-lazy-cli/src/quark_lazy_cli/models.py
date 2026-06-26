"""
models - 数据结构定义

所有数据类定义在此，避免循环导入。
- DiskStatus, SearchGoal, SearchContext 由 app.py 创建，传给 advisor.py
- AdvisorDecision 由 advisor.py 返回给 app.py
"""

from dataclasses import dataclass, field


@dataclass
class DiskStatus:
    """网盘现状"""

    quark_userlocal_owned_eps_set: set[int]  # 已有的 EP 集合
    quark_userlocal_min_ep: int  # 最低 EP
    quark_userlocal_max_ep: int  # 用户夸克网盘最高 EP
    quark_userlocal_hole_eps_set: set[int]  # 缺失的 EP 集合
    last_updated: int | None = None  # 最新资源时间戳（毫秒）


@dataclass
class SearchGoal:
    """搜索目标"""

    mode: str  # "all" | "new"
    suggested_max_ep: int  # 最高剧集上限


@dataclass
class SearchContext:
    """搜索上下文"""

    taskname: str
    disk: DiskStatus
    goal: SearchGoal
    search_results: list[dict]
    ep_selection_policy: str = "prefer_size"
    dup_eps: list = field(default_factory=list)
    ep0_files: list = field(default_factory=list)
    unmatch_files: list = field(default_factory=list)
    add_prompt: str = ""  # 用户附加提示，仅 LLM 顾问使用
    fresh_invalid_count: int = 0  # 新鲜资源中过滤掉的失效链接数量
    invalid_search_items: list = field(default_factory=list)  # [{"item": ..., "reason": ...}, ...]


@dataclass
class AdvisorDecision:
    """顾问决策结果"""

    advisor_selected_urls_index: list[int] = field(default_factory=list)
    advisor_confirmed_max_ep: int = 0
    error: str = ""  # API错误信息
