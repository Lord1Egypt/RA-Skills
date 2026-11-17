# role: models — 数据结构（SessionMeta / VerifyItem）
"""fork_core.models — 跨产品通用的数据结构定义。

这些 dataclass 与具体产品（WorkBuddy / Claude Code / Codex ...）无关，
是 fork 引擎的输入输出契约。
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SessionMeta:
    """一个会话的元数据（各产品 adapter 负责填充）。

    id       — 会话唯一标识（各产品一致：文件名/数据库 id）
    title    — 会话标题（可为空）
    status   — working / terminated 等（可为空）
    created_at — 创建时间（ms 时间戳或 ISO 字符串，可为空）
    cwd      — 工作目录（可为空）
    parent_id — 父会话 id（分支谱系用，可为空）
    extra    — 产品特有字段原样保留
    """
    id: str
    title: str = ""
    status: str = ""
    created_at: object = None
    cwd: str = ""
    parent_id: str = ""
    extra: dict = field(default_factory=dict)


@dataclass
class ForkResult:
    """create_fork 的返回结果（供 CLI 打印/汇报模板）。"""

    ok: bool
    src_id: str
    new_id: str
    name: str
    cut: int
    total: int
    how: str
    transcript_path: str
    dst_path: str
    backup_dir: Optional[str] = None
    error: Optional[str] = None
    replacements: int = 0
    dry_run: bool = False
    verified: bool = False
    # 降级路径标记（预留）：当前实现天然走"文件级兜底"（无官方 API 可调），恒 False；
    # 若将来出现产品官方的 fork API，一旦走降级路径即置 True，让"降级"对外可见。
    degraded: bool = False


@dataclass
class VerifyItem:
    """fork --verify 体检的单项结果。

    name   — 检查项名称（存储/schema/真实数据替换/谱系索引）
    level  — 该项达到的验证级别（L1 fixture / L2 真库 / L3 产品终验）
    ok     — 是否**判定失败**（False = 有需要修的问题，体检会以非 0 退出）
    detail — 结果描述（PASS 的证据 / FAIL 的原因）
    review — 未判失败、但**需人工复核**（v2.4.15 起）。

    为什么要区分 ok 与 review：有些检查项能给出"疑点"却无法断定是缺陷——
    典型是分支边界之外的源 id 引用（既可能是"你在分支里记录了血缘"这种正常内容，
    也可能是有问题）。把它们一律判失败，会让体检**常驻红**，久而久之没人看，
    真正的问题反而被淹没；一律放过又会丢掉信号。故单列一档：
    **review 项不影响汇总通过、不产生非 0 退出，但在输出里显式标注 ⚠️**。
    """

    name: str
    level: str
    ok: bool
    detail: str
    review: bool = False
