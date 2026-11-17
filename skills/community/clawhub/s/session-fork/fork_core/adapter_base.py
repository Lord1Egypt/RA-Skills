# role: core — 适配器接口契约（TranscriptionAdapter）+ 序列化安全阀 dumps_safe + 运行时提示 notify
"""fork_core.adapter_base — TranscriptionAdapter 接口定义。

通用引擎只依赖本接口；每个产品（WorkBuddy / Claude Code / Codex ...）
实现一个 adapter，把「产品特有存储格式」翻译成统一契约。

接口分四组：
  A. 定位     — find_transcript / resolve_session
  B. 消息判定 — is_user_message / is_assistant_message / get_text / get_request_id
  C. 读写     — read_lines / write_branch / rewrite_ids / extract_title_hint
  D. 注册     — load_session_meta / register_branch / list_branches / is_branch_name

所有方法都接收 engine 传入的上下文，不依赖全局状态。
"""

import json
import os
import shutil
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Optional

from .models import SessionMeta, VerifyItem


# ----------------------------------------------------------------------
# 序列化安全阀（2026-09-16 新增）：孤立代理致写出崩溃的**公共**修法
# ----------------------------------------------------------------------
@dataclass
class ParseResult:
    """逐行解析的结果：条目 + **坏行行号**（1-based，按文件行数计）。

    为什么要带着坏行号返回，而不是直接抛异常或静默跳过（2026-09-19）：
      · 抛异常：一个坏行就让**整轮体检崩掉**，其余检查全被跳过，而且报错理由指向
        "检查器"而不是"哪一行坏了"——排查成本高；
      · 静默跳过：体检会在"少看了一部分内容"的前提下报绿，等于把未知当已知。
    所以：**不抛、也不静默**——跳过它继续检查，但把坐标交出去，由调用方决定怎么说。

    ⚠️ 两种坐标**不可混用**（混用会看错位置，已有反例）：
      · `bad_lines` = **文件行号**（含空行的计数）——报给用户看，能直接在编辑器里定位；
      · `bad_items` = **条目序号**（跳过空行后的第几条）——与 `at_seq`/边界同一尺度，
        "它落在前缀内还是追加区"的比较**必须**用它，否则遇到空行就会看错位置。
    """

    objs: list[dict] = field(default_factory=list)
    bad_lines: list[int] = field(default_factory=list)
    bad_items: list[int] = field(default_factory=list)


def parse_jsonl(text: str) -> "ParseResult":
    """逐行解析 JSONL：坏行记坐标，不抛。**空行不算坏行**（换行/空行是合法排版）。

    "坏行"**可能**出现：产品在写入过程中被读取时，末尾会有半行（写到一半被截断）。
    ⚠️ 证据等级（2026-09-19 自检）：本机真库 165 个 transcript **实测 0 例坏行** ——
    所以这是**防御性**处理，不是"已观测到的高频故障"，别把它当成常见场景来宣称。
    做它的真实理由有两条，都不依赖"常见"：① 旧实现一遇坏行会让**整轮体检崩掉**、
    其余检查全被跳过且报错理由指错；② 静默跳过会让"少看了一部分内容"
    被当成全绿。所以这个函数是**读取路径的统一入口**：所有产品的 `read_lines` 都应经它。

    顶层不是对象的行（如一行是数组/字符串）也计入坏行：引擎各处都按 dict 处理，
    放行它只会在更远处崩；计入坏行 = **被跳过且被报出**，比静默丢失或远处崩更诚实。
    """
    objs: list[dict] = []
    bad_lines: list[int] = []
    bad_items: list[int] = []
    item_no = 0
    for i, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        item_no += 1
        try:
            o = json.loads(line)
        except Exception:
            bad_lines.append(i)
            bad_items.append(item_no)
            continue
        if isinstance(o, dict):
            objs.append(o)
        else:
            bad_lines.append(i)
            bad_items.append(item_no)
    return ParseResult(objs=objs, bad_lines=bad_lines, bad_items=bad_items)


def read_jsonl_file(path: str) -> "ParseResult":
    """读文件并解析（读取路径的统一实现，见 parse_jsonl 的说明）。"""
    with open(path, encoding="utf-8") as f:
        return parse_jsonl(f.read())


def read_jsonl_head(path: str, n: int) -> Optional[str]:
    """只读「前 n 个非空行」的原始文本；文件不存在 → None。

    性能用（2026-09-19）：前缀指纹只关心前 n 行，而整份产物可能上百 MB
    （真机最大 107MB / 19,195 行）。**必须与「全量读 + 取前 n 个非空行」逐字节等价**，
    否则指纹会算出假差异——故取行口径与 verify 完全一致（按非空行计数）。
    """
    if not os.path.isfile(path):
        return None
    out: list[str] = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            out.append(line)
            if len(out) >= n:
                break
    return "".join(out)


def dumps_safe(obj: Any, **kwargs: Any) -> str:
    """把对象序列化成「保证可 utf-8 写出」的 JSON 文本（行级与文件级通用）。

    背景（实测，非推断）
    -------------------
    `json.dumps(o, ensure_ascii=False)` 产出的文本若含**孤立代理**（lone surrogate，
    U+D800–U+DFFF；常见成因＝上游把 emoji 的代理对切开、留高丢低），则在写出时
    （`open(..., encoding="utf-8")` 的 write，或 sqlite3 绑定 str 参数）抛：
        UnicodeEncodeError: 'utf-8' codec can't encode character U+D83D ...
                            surrogates not allowed
    ⇒ **整份产物写出失败**。首次实测现场：WorkBuddy 会话
    `~/.workbuddy/projects/.../ec48e1ae-*.jsonl:18968`（全库 158 文件 / 238,636 行中唯一一处）。

    ⚠️ 实现注记（本条是自己踩出来的，2026-09-16）
    --------------------------------------------
    **本模块的 docstring 内不得书写单反斜杠的 u 转义**：Python 会把 docstring 里的
    该转义序列解析成**真正的孤立代理字符**，使本模块常量带上代理 ⇒ **整个包 import 即崩**
    （实测：加本函数时把 7 个适配器测试从全绿打成全红，由「编译 + 全量测试」当场拦住）。
    **要表达码点请写 `U+D83D` 这类形式**，不要写反斜杠转义。

    策略：保真优先 · 逐行 · 不净化
    ------------------------------
      · 默认 `ensure_ascii=False` —— 保持既有形态与人类可读（不改变绝大多数行的字节形态）；
      · **仅当该对象无法 utf-8 编码时**，降级 `ensure_ascii=True`
        —— 孤立代理在 JSON 层是**合法转义**（`\\ud83d`），`json.loads` 回读仍是同一代理
        ⇒ **语义逐字保真**：不替换、不丢弃、不改写内容。
      · 因此降级是**按对象局部**的：`write_branch` 逐行调用 ⇒ 只影响**含代理的那一行**
        （实测：107.7 MB / 19,195 行的最大会话中，仅 **1 行**被降级，其余 19,194 行**逐字符相同**）；
        而索引/谱系那类**整文件一次写出**的调用点 ⇒ 若该文件含代理，**整份文件**转义
        （仍可往返、不丢数据，只是可读性下降——仍优于"整份写不出来"）。

    有意**不用**的两条路（均实测过）
    -------------------------------
      · `encode('utf-8', 'surrogatepass')`：产物含 CESU-8 残片（`ed a0 bd`），
        是**非法 UTF-8**；宿主/Node 按严格 UTF-8 读会替换为 U+FFFD ⇒ **吞字**，不保真。
      · `encode('utf-8', 'backslashreplace')`：把代理写成**字面 6 字符**，单次写出虽可往返，
        但一旦该文本**再经一次序列化**即退化为普通文本（不保真）⇒ 语义脆，不采用。
    """
    kwargs.pop("ensure_ascii", None)  # 转义策略由本函数统一决定（见上），忽略调用方同名参数
    text = json.dumps(obj, ensure_ascii=False, **kwargs)
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        text = json.dumps(obj, ensure_ascii=True, **kwargs)
    return text


def harden_output() -> None:
    """把 stdout 固定为 UTF-8 —— 仅当它当前的编码「容纳不了」中文与 emoji 时。

    为什么需要（2026-09-18，CI 三平台实测）：Windows 上 stdout 的编码分两种情况 ——
      · **真控制台**：CPython 走 WindowsConsoleIO，其 encoding 已是 `utf-8`（底层 UTF-16）
        ⇒ 本就能输出全部 Unicode；
      · **被重定向 / 管道 / MSYS pty**（AI 调用与 Git Bash 都属这类）：用 locale 编码
        （中文 Windows=cp936、英文 Windows=cp1252）且 errors 默认 **strict** ⇒ 输出含中文
        或 emoji 时 print 直接抛 UnicodeEncodeError，**命令被提示本身打断**：实测 `--verify`
        退出码 1，且报错行自身含 ❌ 从而二次崩（连错误信息都打不出来）。

    为什么按 **encoding** 判断而不是 `isatty()`：Windows 上 `isatty()` 为真**不等于**走的是
    ConsoleIO —— Git Bash 的 MSYS pty 就是 `isatty()=True` 但编码仍是 cp1252
    （实测：用 isatty 判断时该场景照样崩）。而"encoding 是否为 Unicode 系"直接对应
    「会不会编错」这个真问题。

    为什么选 UTF-8 而不是 `errors="replace"`：UTF-8 能容纳中文与 emoji，**信息零损失**；
    而 replace 在英文 Windows（cp1252）下会把**全部中文变成 "?"** —— 命令"成功"但 AI
    读到的是一片问号，比崩得更隐蔽。管道用 UTF-8 也是 AI/CLI 生态的通用约定。

    不动 stderr：其 errors 默认 backslashreplace，本就不会抛。
    """
    try:
        enc = (sys.stdout.encoding or "").lower().replace("-", "").replace("_", "")
        if enc.startswith("utf") or enc == "cp65001":
            return  # 已是 Unicode 编码（含 Windows 真控制台的 utf-8）：不会编错，不干预
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):
        pass  # 非 TextIOWrapper（如被替换为 BytesIO）或已关闭：无害跳过


def notify(msg: str, *, quietable: bool = True) -> None:
    """面向用户的运行时提示（写盘 / 删除 / 回滚等**有副作用**的动作前调用）。

    ⚠️ **副作用路径必须传 `quietable=False`**（2026-09-16 审查口径）：
    **"可以被关闭的提示"不构成 user-facing disclosure** —— 审查器对可静音提示仍判"无警告"。
    故 `FORK_QUIET=1` 只静音**非副作用**类提示（供库调用与测试）。

    提示串**中英并置**：安全相关提示不应只给一种语言（同一原因见语言政策项）。

    ⚠️ 此处**不需要**编码兜底：stderr 的 errors 默认是 `backslashreplace`，
    非 UTF-8 终端下不抛异常（只把不可编码字符写成 `\\uXXXX` 转义）；stdout 才需要，见 `harden_output`。
    """
    if not quietable or os.environ.get("FORK_QUIET") != "1":
        print("→ " + msg, file=sys.stderr)


class TranscriptionAdapter:
    """接口基类。子类必须实现全部方法。"""

    # 产品名（如 "workbuddy" / "claude-code"）
    name: str = "base"

    # ------------------------------------------------------------------
    # A. 定位
    # ------------------------------------------------------------------
    def find_transcript(self, session_id: str) -> tuple[Optional[str], Optional[str]]:
        """定位会话 transcript 文件。返回 (path, workspace_slug)；找不到返回 (None, None)。"""
        raise NotImplementedError

    def resolve_session(self, session_ref: str) -> str:
        """把 'current' 解析为具体会话 id；否则原样返回。"""
        raise NotImplementedError

    def find_session_by_request_id(self, request_id: str) -> Optional[str]:
        """全盘反查含该 conversationRequestId 的会话（跨 workspace）。可选实现。

        用途：用户复制 UI 的"请求 ID"后打分支，但不知道源会话 id——
        引擎在 request-id 模式下优先调用本方法自动定位源会话。
        默认返回 None（不支持反查的产品，需用户显式 --session）。
        """
        return None

    def running_session_id(self) -> Optional[str]:
        """**执行本脚本的进程所处的会话 id** —— 即"我是不是就在某个会话里面"。

        为什么需要这个信号（v2.4.9 引入，2026-09-15）：
        默认截断点有两种语义，且**同一行命令、同一个 `--session current`** 下二者都会出现
        （agent 在自己的会话里打分支 vs 人从终端打分支），靠命令行字面量区分不了。
        唯一确定性的判据是"执行环境里有没有本次会话的标识"：
          - 返回具体 id ⇒ 本次调用发生在**某个会话内部** ⇒ 默认截断点取"上一轮输出结束"
            （切在最后一条 user 消息之前，不含本次"打分支"指令与本轮叙述）；
          - 返回 None   ⇒ 外部执行，没有"本轮"要排除 ⇒ 退回"整份复制"语义（旧行为）。

        默认实现读 Claude Code / WorkBuddy 系在执行环境里留下的会话标识
        （`CLAUDE_SESSION_ID`；`BAGGAGE` 里的 `codebuddy.session_id=<id>`）。
        其他产品若无此信号 → None（引擎退回整份语义，**行为不变**）；有等价信号的自行覆盖。
        """
        for key in ("CLAUDE_SESSION_ID", "CODEBUDDY_SESSION_ID"):
            v = os.environ.get(key)
            if v and v.strip():
                return v.strip()
        # BAGGAGE=codebuddy.session_id=<id>,codebuddy.conversation_request_id=<id>,…
        for part in (os.environ.get("BAGGAGE") or "").split(","):
            if part.startswith("codebuddy.session_id="):
                v = part.split("=", 1)[1].strip()
                if v:
                    return v
        return None

    # ------------------------------------------------------------------
    # B. 消息判定（供通用截断点定位逻辑使用）
    # ------------------------------------------------------------------
    def is_user_message(self, obj: dict) -> bool:
        """该行是否是 user 消息。"""
        raise NotImplementedError

    def is_assistant_message(self, obj: dict) -> bool:
        """该行是否是 assistant 消息。"""
        raise NotImplementedError

    def get_text(self, obj: dict) -> str:
        """提取该行的纯文本（用于 --match 匹配、output_text 完整性判断、标题摘要）。"""
        raise NotImplementedError

    def get_request_id(self, obj: dict) -> Optional[str]:
        """提取该行的 conversationRequestId（用于 --request-id 精确截断）；无则 None。"""
        return None

    # ------------------------------------------------------------------
    # C. 读写
    # ------------------------------------------------------------------
    # ⚠️ `read_lines` **只在本文件底部「H. 行存储抽象」定义一次**（默认实现 = 逐行 JSON 文件）。
    #    这里曾有一份 `raise NotImplementedError` 的接口桩，与下方同名同签名 ⇒ 被**静默覆盖**，
    #    读者会误以为"改了这个桩就能改行为"（实际不会）。已删除该桩（2026-09-15 复核）。
    #    `write_branch` / `rewrite_ids` 等仍按原样在本节声明。

    def write_branch(self, path: str, lines: list[dict]) -> None:
        """把分支行写入文件（引擎已处理好截断与 id 替换）。"""
        raise NotImplementedError

    def rewrite_ids(self, lines: list[dict], old_id: str, new_id: str) -> tuple[list[dict], int]:
        """结构化字段级 id 替换。返回 (新 lines, 替换次数)。"""
        raise NotImplementedError

    def extract_title_hint(self, lines: list[dict]) -> str:
        """从最后一条 user 消息提取分支名摘要；无则返回空串。"""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # D. 注册与查询
    # ------------------------------------------------------------------
    def load_session_meta(self, session_id: str) -> Optional[SessionMeta]:
        """读取会话元数据。"""
        raise NotImplementedError

    def register_branch(
        self,
        src: SessionMeta,
        new_id: str,
        dst_path: str,
        name: str,
        parent_id: Optional[str] = None,
        at_seq: Optional[int] = None,
        prefix_fp: Optional[str] = None,
    ) -> None:
        """在会话索引中注册新分支（各产品不同：数据库插入 / 索引文件 / 纯文件）。

        at_seq    = 截断点（会话级分支的"快照点"，谱系可回/可审计）。
        prefix_fp = 该前缀的指纹（引擎算好传入，v2.4.15）。

        **适配器契约（新增能力，务必遵守）**：实现本方法的产品应把 `prefix_fp` 原样存进
        自己的谱系记录（与 `at_seq` 同一条）。它让体检能核对"边界是否可信"：指纹一致
        ⇒ 前 `at_seq` 行确为 fork 原样产物，边界之后的引用只可能是 fork 之后写入的内容。
        **不存也不会坏**：引擎按"未记录指纹"处理，体检降级为提示复核（不判失败）；
        但那样该产品的用户就少了这层证据。引擎**先探测签名再传参**，故老实现不会因此报错。
        """
        raise NotImplementedError

    def unregister_branch(self, new_id: str) -> None:
        """撤销 register_branch 的副作用（db 行 + 谱系条目）。

        引擎层 register 失败时回滚用（2026-09-04 评审：回滚应撤销注册副作用，
        而不是删已验证的产物文件）。adapter 如无副作用/无法撤销则 no-op。
        """
        return None

    def list_branches(self, cwd: Optional[str] = None) -> list[SessionMeta]:
        """列出当前 workspace 的分支（含状态/时间）。"""
        raise NotImplementedError

    def is_branch_name(self, title: str) -> bool:
        """判断标题是否看起来像分支（用于 list 过滤）。"""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # E. 体检（fork --verify / --doctor 用，可选覆盖）
    # ------------------------------------------------------------------
    def verify_storage(self) -> list[VerifyItem]:
        """存储层体检（存在性/可写）。默认实现只查 PROJECTS_DIR 存在性。

        产品 adapter 应覆盖：数据库/schema 约束/真实会话数等（返回 VerifyItem 列表）。
        """
        items = []
        projects = getattr(self, "PROJECTS_DIR", None)
        ok = bool(projects) and os.path.isdir(projects) if projects else False
        items.append(VerifyItem(
            "transcript 目录", "L1", ok,
            str(projects) if ok else "缺失（无会话存储）",
        ))
        return items

    # ------------------------------------------------------------------
    # F. 会话枚举（可选覆盖；引擎真库体检 _collect_real_transcripts 用）
    # ------------------------------------------------------------------
    def storage_root(self) -> Optional[str]:
        """存储根目录（其下按 workspace 分子目录、子目录里放 *.jsonl）。

        默认取 PROJECTS_DIR（WorkBuddy / Claude Code 的形态）。
        存储布局不同的产品覆盖本方法，勿让引擎去猜属性名
        （2026-09-14 跨平台验证：引擎原先硬取 PROJECTS_DIR，pi 的 SESSIONS_DIR 取不到，
        导致真库体检恒报"无真实会话可用"）。
        """
        return getattr(self, "PROJECTS_DIR", None)

    def list_all_sessions(self) -> list[tuple[str, str]]:
        """枚举全部真实会话 → [(transcript_path, session_id)]。

        默认实现假定**文件名去掉 .jsonl 即会话 id**（WorkBuddy / Claude Code 成立）。

        ⚠️ 文件名与会话 id 解耦的产品必须覆盖本方法：pi 的文件名是
        `<ISO 时间戳>_<header.id>.jsonl`，会话 id 在**首行 header** 里。
        沿用默认实现会把时间戳前缀算进 id，使残留校验（拿错 id 去比对）
        与分支识别全部失真（2026-09-14 跨平台验证实测）。
        """
        out: list[tuple[str, str]] = []
        root = self.storage_root()
        if not root or not os.path.isdir(root):
            return out
        for slug in os.listdir(root):
            d = os.path.join(root, slug)
            if not os.path.isdir(d):
                continue
            for fn in os.listdir(d):
                if fn.endswith(".jsonl"):
                    out.append((os.path.join(d, fn), fn[:-6]))
        return out

    # ------------------------------------------------------------------
    # G. 面向用户的文案与路径（可选覆盖；默认 = WorkBuddy 口径，兼容旧行为）
    # ------------------------------------------------------------------
    def activation_hint(self) -> str:
        """分支落地后如何让产品"看见"它（各产品刷新机制不同）。

        默认返回 WorkBuddy 的运行期提示（重启客户端）。
        覆盖示例见 adapter_pi.activation_hint（pi 无需重启，/resume 即可见）。
        """
        return (
            "会话列表非实时刷新，需重启对应产品才能在左侧看到\n"
            "            macOS: ⌘Q 退出重开，或终端执行 open -a WorkBuddy\n"
            "            Windows: 托盘图标右键退出后重开"
        )

    def produce_hint(self) -> str:
        """体检发现"无真实会话"时，告诉用户怎么先产生一个会话。"""
        return "WorkBuddy 直接对话 / Claude Code 在终端跑 claude 命令"

    def _backups_root(self, default: str) -> str:
        """备份根目录的**统一取值规则**：环境变量 FORK_BACKUP_DIR 优先，否则用传入的产品目录。

        各 adapter 的 `backups_dir()` 都应经这里取值（否则用户设了环境变量却不生效）。
        非 WorkBuddy 用户不希望备份落在产品自己的目录里时，用它统一改到别处。
        """
        override = os.environ.get("FORK_BACKUP_DIR")
        return os.path.expanduser(override) if override else default

    def backups_dir(self) -> str:
        """源文件备份目录。默认 ~/.workbuddy/backups（历史默认值，勿改）。

        各产品通常覆盖为**自己产品目录下的 `fork-backups/`**（claude-code / codex /
        hermes / pi / openclaw 都如此）——备份跟着产品走，不污染别家目录。
        想要统一指定时用环境变量 **FORK_BACKUP_DIR**（对所有 adapter 生效）。
        """
        return self._backups_root(os.path.join(os.path.expanduser("~"), ".workbuddy", "backups"))

    # ------------------------------------------------------------------
    # H. 行存储抽象（v2.4.8 新增；默认实现 = 「一行一条 JSON 的文本文件」）
    #
    # 引擎原本直接对文件做 read / os.replace，隐含了"转录 = 文本文件"这个前提。
    # 而 OpenClaw ≥2026.9.x 把转录放进了 SQLite 的 transcript_events 表
    # （(session_id, seq) → event_json）——**语义与 JSONL 完全同构，只是介质不同**。
    # 下面几个方法把「介质」从引擎里抽出来：
    #   - 转录引用（ref）是不透明字符串：JSONL 后端 = 文件路径；
    #     SQLite 后端 = "<db 路径>#<session_id>" 形式的合成引用。
    #   - 默认实现严格保持既有 JSONL 行为，**旧适配器零改动**。
    # ------------------------------------------------------------------
    def read_lines(self, ref: str) -> list[dict]:
        """按 ref 读出有序条目序列。默认：逐行 JSON 文件（**坏行跳过，不抛**）。

        坏行不抛是有意的（理由见 parse_jsonl）：读取方不该因为一行坏掉就整轮崩掉。
        需要知道"跳过了哪些行"时用 `read_lines_checked`。
        """
        return self.read_lines_checked(ref).objs

    def read_lines_checked(self, ref: str) -> "ParseResult":
        """`read_lines` + **坏行行号**（体检等"要如实交代"的场景用）。**单次读取**，不重复解析。

        ⚠️ 实现要点（2026-09-19 踩过）：**不能**用 `parse_jsonl(self.read_raw(ref))` 做默认实现——
        SQLite 后端的行里有 BLOB(`bytes`)，经 `read_raw`（它有 `default=str`）往返会被**降级成字符串**：
        既破坏保真（写出的分支内容变形），又会凭空造出"源 id 命中"（二进制里恰好含那串字节）。
        所以：
          · 文件型引用 → 直接逐行解析（JSONL 里只有 `dict`，与旧行为一致）；
          · 非文件引用（SQLite 等）→ 走**该后端的原生 `read_lines`**，坏行信息由后端自行覆盖本方法提供。
        """
        if os.path.isfile(ref):
            return read_jsonl_file(ref)
        return ParseResult(objs=list(self.read_lines(ref)), bad_lines=[])

    def read_raw_head(self, ref: str, n: int) -> Optional[str]:
        """只读「前 n 个非空行」的原文（性能用）；**非文件引用 → None**，调用方回退全量读。

        用途：前缀指纹只需要前 n 行，而产物可能上百 MB（真机最大 107MB）。
        取行口径必须与 `read_raw` 侧的 `_raw_lines`（去空行）完全一致，否则会算出假差异。
        SQLite 等非文件后端沿用默认实现返回 None ⇒ 自动退回全量读（正确性优先）。
        """
        return read_jsonl_head(ref, n)

    def read_raw(self, ref: str) -> str:
        """读出可做行级校验的原始文本。默认：文件内容原样。

        SQLite 后端返回与 JSONL 等价的「每行一条 JSON」文本，
        使引擎现有的行数 / 解析 / 残留校验逻辑可原样复用。
        """
        with open(ref, encoding="utf-8") as f:
            return f.read()

    def branch_target(self, src_ref: str, new_id: str) -> str:
        """算产物引用。默认：与源同目录的 <new_id>.jsonl。"""
        return os.path.join(os.path.dirname(src_ref), new_id + ".jsonl")

    def finalize_branch(self, tmp_ref: str, dst_ref: str) -> None:
        """把「已校验但尚未对外可见」的产物落位（引擎的第一个发布动作）。

        默认：原子 rename（JSONL）。SQLite 后端：COMMIT 事务。
        """
        os.replace(tmp_ref, dst_ref)

    def backup_transcript(self, ref: str, backups_dir: str) -> str:
        """备份源。默认：复制单个文件。SQLite 后端应备份整个数据库文件。"""
        ts = time.strftime("%Y%m%d-%H%M%S")
        backup_dir = os.path.join(backups_dir, ts)
        os.makedirs(backup_dir, exist_ok=True)
        shutil.copy2(ref, os.path.join(backup_dir, os.path.basename(ref)))
        return backup_dir

    def is_historical_id_path(self, path: str) -> bool:
        """该路径下的 `sessionId`/`session_id` 是否属**历史记录**而非会话关联字段。

        默认 False（一律按关联字段查）。只有确实存在"产品会把源会话 id 写进
        历史记录"的情形才覆盖——覆盖面越小越好，这是纵深防御层的豁免口。
        """
        return False

    def sort_key(self, ref: str) -> float:
        """体检时的"最近使用"排序键。默认：文件 mtime。

        SQLite 后端的 ref 不是文件路径，必须覆盖（否则 getmtime 抛 FileNotFoundError）。
        """
        return os.path.getmtime(ref)

    def publish_hint(self) -> str:
        """产物落位后，是否还需要额外动作才能被产品看见（不需要 = 空串）。"""
        return ""

    def backup_note(self) -> str:
        """备份范围的一句话说明（给用户看，各介质不同）。"""
        return "source jsonl only, no database copy"

    def readonly_hint(self, dst_ref: str) -> str:
        """防止产品继续往分支追加消息的提示（无文件可锁的介质返回空串）。"""
        return (
            "分支文件未锁定只读（**本技能不会替你修改文件权限**）。如需防止主进程继续追加消息，"
            f"可由你自己把它设为只读——（用你系统的方式把该文件设为只读）{dst_ref}"
        )
