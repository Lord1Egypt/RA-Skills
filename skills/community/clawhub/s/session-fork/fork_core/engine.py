# role: core — 分叉主链路：读源会话 → 裁剪 → 递归改写会话 id → 写出 → 校验 → 注册（create_fork）
"""fork_core.engine — 跨产品通用的 fork 引擎。

不依赖任何产品细节，只通过 TranscriptionAdapter 接口与具体产品交互。
WorkBuddy / Claude Code / Codex 的差异全部被 adapter 吸收。
"""

from __future__ import annotations

import copy
import hashlib
import inspect
import json
import os
import re
import stat
import uuid

from .adapter_base import TranscriptionAdapter, notify
from .models import ForkResult, SessionMeta, VerifyItem

# 备份目录没有模块级默认值：由 adapter.backups_dir() 决定
# （读 FORK_BACKUP_DIR；见 adapter_base.TranscriptionAdapter.backups_dir）。


class ForkError(Exception):
    """fork-core 异常基类（库层不抛 SystemExit——那是 CLI 的事）。调用方 except ForkError 兜住全部。"""
    exit_code = 1


class ForkVerifyError(ForkError):
    """自检未通过。此时尚未产生任何外部可见副作用（verify 先于落位/登记）。"""
    exit_code = 2

    def __init__(self, errs):
        self.errs = list(errs)
        super().__init__("VERIFY FAILED:\n  - " + "\n  - ".join(self.errs))


class ForkRegisterError(ForkError):
    """文件已落位但登记失败。失败态经回滚处理后应为孤儿文件（无害，可安全重跑）。"""
    exit_code = 3


class ForkRollbackError(ForkError):
    """回滚失败——最严重：磁盘可能残留需人工处理。必须在信息里给出具体路径，绝不静默。"""
    exit_code = 4


def _safe_remove(path: str) -> bool:
    """尽力删除，返回结果而非吞异常。失败由调用方决定后果（tmp 无所谓 / dst 必须报警）。

    Windows 只读文件删除兜底：先去只读位再删（v1.2.0 曾把分支锁只读）。
    """
    try:
        os.remove(path)
        return True
    except FileNotFoundError:
        return True
    except PermissionError:
        try:
            # 仅对**本工具自己刚写的**临时/分支文件做可写位兜底（Windows 只读文件删除）
            from pathlib import Path

            Path(path).chmod(stat.S_IWRITE | stat.S_IREAD)
            os.remove(path)
            return True
        except OSError:
            return False
    except OSError:
        return False


def _load_lines(path: str) -> list[dict]:
    """读 jsonl 文件为 dict 列表（跳过空行/坏行）。"""
    lines = []
    for l in open(path, encoding="utf-8"):
        l = l.strip()
        if not l:
            continue
        try:
            lines.append(json.loads(l))
        except Exception:
            continue  # 坏行跳过（engine 不负责格式校验，adapter 判定时忽略）
    return lines


def locate_last_reply(adapter, lines: list[dict]) -> tuple[int, int]:
    """截断点 = 全文件最后一条有文本的 assistant 回复（**整份 fork** 语义）。

    用在：显式指定源会话（`--session <id>`，含"从分支再 fork"）、无会话上下文的外部执行。
    语义 = "把这个会话已落定的内容整份复制走"。

    ⚠️ **不要**用它实现"从会话内部打分支"的默认模式：agent 在本轮里执行 fork 时，
    它自己的叙述（reasoning / function_call / assistant 文本）**已经写进了同一份 transcript**，
    所以"文件末尾最后一条 assistant 文本"必然是本轮的叙述，而不是上一轮的收尾 ——
    分支会吞掉本轮（含"打分支"这条指令本身与 fork 自己的输出），且随 agent 再说话继续前移。
    那种场景要用 `locate_before_current_turn()`。

    历史注记（v2.1.0 回归，2026-09-15 定位）：本函数原名即"默认模式"，
    提交 82df3a5（v2.1.0，2026-09-01）为支持"分支再 fork 时整份复制"，
    把原实现里"锚在最后一条 user 消息之前"的 4 行删掉、只留全文件倒扫 ——
    于是**主用例（会话内打分支）被一起改坏**。两种语义都需要，故拆成两个函数，
    由 `create_fork` 按"我是否就在该会话里"（`adapter.running_session_id()`）分派。
    """
    n = len(lines)
    for i in range(n, 0, -1):
        o = lines[i - 1]
        if adapter.is_assistant_message(o) and adapter.get_text(o).strip():
            return i, n
    raise ForkError("No completed assistant reply found in transcript")


def locate_before_current_turn(adapter, lines: list[dict]) -> tuple[int, int, str]:
    """**从会话内部**打分支（`--session current`）的默认截断点。

    语义（= 文档承诺的"上一轮输出结束"）：截断点 = **最后一条 user 消息之前**的最后一条
    有文本的 assistant 回复末尾。返回 (cut, total, note)。

    为什么必须锚在 user 消息上（2026-09-15 真实事故，两个真实分支现场复原）：
    agent 执行 fork 时，本轮的 user 消息（"打分支"）与其后的全部叙述**都已经在文件里**。
    按"文件末尾最后一条 assistant 文本"切 ⇒ 切点必然落在本轮叙述上：
      · `3ccebc53`（源 `ec48e1ae`）：切在 L18782，正确应为 L18763 —— **多吞 19 行**
        （含"打分支"指令本身、dry-run 的输出、fork 自己的输出）；
      · `5df71252`（源 `d6af6ce6`）：切在 L8452，正确应为 L8424 —— 多吞 28 行。
    且切点随 agent 继续输出而**前移**：同一轮内 dry-run 报 18778、实跑写 18782（漂移 4 行）——
    执行者据此以为"截在上一轮输出结束"，实际截在自己的叙述上。
    锚在"最后一条 user 消息"上则**在本轮内稳定不漂移**（user 消息在本轮不会新增）。

    ⚠️ 该规则同时是被验证器假定的边界形态：`verify_branch` 判"追加区是否开启新回合"时，
    前提正是 **L(cut+1) 是一条 user 消息**。

    退化情形（都不是错误，退回整份 fork 语义并在 note 里说明，**不静默**）：
    - 文件里没有 user 消息（纯注入 / 异常会话）；
    - 最后一条 user 消息之前没有任何有文本的 assistant 回复（单轮会话：用户刚问、助手刚答）。
    """
    n = len(lines)
    last_user = None
    for i, o in enumerate(lines, 1):
        if adapter.is_user_message(o):
            last_user = i
    if last_user is None:
        cut, total = locate_last_reply(adapter, lines)
        return cut, total, "文件内无 user 消息 → 退回整份语义"
    for i in range(last_user - 1, 0, -1):
        o = lines[i - 1]
        if adapter.is_assistant_message(o) and adapter.get_text(o).strip():
            return i, n, (
                f"锚定 L{last_user} 的 user 消息「{_preview(adapter, lines[last_user - 1])}」"
                f"（= 本轮指令），切在它之前"
            )
    cut, total = locate_last_reply(adapter, lines)
    return cut, total, f"L{last_user} 之前无完整回复（单轮会话）→ 退回整份语义"


#: UI「复制请求 ID」得到的 JSON 原文：`{"conversationRequestId":"…","conversationId":"…"}`。
#: 只认**字段名 + 值**的形态，不认"随便一个 32 位十六进制串"（traceId 也是这个形状，
#: 但 traceId **不能**当断点用）。
_RE_PASTED_REQ_ID = re.compile(r'"conversationRequestId"\s*:\s*"([A-Za-z0-9_-]{8,64})"')


def find_pasted_request_id(adapter, lines: list[dict]) -> str | None:
    """**本轮** user 消息里是否贴了一个 request id（= 用户明确了"切在哪一条回复"）。

    只扫最后一条 user 消息：贴 ID 是"这次操作切哪儿"的指令，不是历史内容。
    """
    last_user = None
    for i, o in enumerate(lines, 1):
        if adapter.is_user_message(o):
            last_user = i
    if last_user is None:
        return None
    text = adapter.get_text(lines[last_user - 1]) or ""
    m = _RE_PASTED_REQ_ID.search(text)
    return m.group(1) if m else None


def apply_pasted_request_id(adapter, lines: list[dict], cut: int, src_id: str) -> tuple[int, str | None]:
    """本轮消息里贴了 request id ⇒ **按它切**，不静默按默认切、也不拒绝执行。

    返回 `(新的切点, 给用户看的说明或 None)`。

    这个函数是**两次改法的沉淀**（同一类事故，2026-11-04 一晚之内）：

    事故现场：用户贴了 `{"conversationRequestId":"f2fb6086…"}` 说"从这里打分支"，
    执行方只跑 `--session current` ⇒ 默认切点 L13495，而该 id 对应 L11470，
    相差 2025 行 ⇒ 产物把整段历史都复制了进去，而工具**没有任何报错**。

      ① v2.4.22 先做成「**拒绝**」：把"静默切错"变成"报错停下"，并给出两条命令。
         **实测失败**：执行方**不照抄报错里的命令**——当天它被拦之后，自己看着
         「P8 定稿」这个词改用 `--line 13479` 猜了个位置，于是又切错一次。
         对用户的结果是"还是打不成"。
      ② v2.4.23 改成「**采用并明示**」：贴了 id 就按 id 切，同时把"我按什么切、默认本会切哪"
         写进 `how`（`Split : …` 行）与 stderr，最后一行给出反向逃生口。
         依据：执行方可以忽略文档、可以忽略报错，但它**一定会把"打分支"这个动作跑完** ——
         那就让这个动作自己用对 id。

    判据没变（也不猜）：该 id 能在**本会话**解析出**不同于默认**的切点才动它；
    解析不出（属于别的会话 / 落点不是完整回复边界）或与默认切点相同 ⇒ 原样返回、保持静默。
    """
    rid = find_pasted_request_id(adapter, lines)
    if not rid:
        return cut, None
    try:
        rid_cut, _ = locate_split_point(adapter, lines, None, None, rid)
    except ForkError:
        return cut, None
    if rid_cut == cut:
        return cut, None
    delta = cut - rid_cut
    notify(
        f"⚠️  本轮消息里贴了 request id {rid}：**已按它切在 L{rid_cut}**"
        f"（默认切点本会是 L{cut}，相差 {abs(delta)} 行）。\n"
        f"    若你要的确实是默认切点，用 --line {cut} 重跑；要指定别的回复，用 --request-id <id>。",
        quietable=False,
    )
    return rid_cut, (
        f"本轮消息贴了 request id {rid} ⇒ 按它切在 L{rid_cut}"
        f"（默认本会是 L{cut}）"
    )


# 系统会在 user 消息首部注入上下文块（<system-reminder …>、<memory …> 等）。
# 预览若直接取消息开头，打印出来的是这串 wrapper —— 人拿着它**核对不出"是不是我刚说的那句话"**，
# 等于"打印了锚点原文"这件事白做。故跳过首部包裹块，取其后的**人类文本**。
_WRAPPER_BLOCK = re.compile(r"^\s*<([a-zA-Z][\w-]*)(?:\s[^>]*)?>.*?</\1>\s*", re.DOTALL)


def _strip_wrappers(text: str) -> str:
    """跳过首部系统注入的包裹块，取其后（或其内）的人类文本。

    真实形态有两种，都必须处理（2026-09-15 实测）：
      a) `<system-reminder …>…</system-reminder>人话`          → 取后面的"人话"
      b) `<system-reminder …>…</system-reminder><user_query>人话</user_query>`
         → 后面那块**自己**就是人话的容器，取它的**内容**
    ⚠️ 初版只在"剥完还剩东西"时才认，剩空就回退整串原文 ⇒ (b) 形态下又吐回 wrapper，
       等于没修。故改为：剥到空时，返回**最后剥掉的那块的内容**（即最内层载荷）。
    """
    out = text
    last_inner = ""
    while True:
        m = _WRAPPER_BLOCK.match(out)
        if not m:
            break
        block = m.group(0)
        inner = re.sub(r"^\s*<[^>]*>", "", block, count=1)
        inner = re.sub(r"</[^>]*>\s*$", "", inner, count=1).strip()
        rest = out[m.end():].strip()
        if not rest:
            # 后面没有了 ⇒ 这一块自己就是人话容器（形态 b）
            return inner or last_inner or text
        last_inner = inner or last_inner
        out = rest
    return out or last_inner or text


def _preview(adapter, obj: dict, limit: int = 28) -> str:
    """取一行消息的文本预览（单行化、截断）——给用户看"切在哪句话之前"。

    打印锚点原文是刻意的：**切点语义必须能被当场核对**。真实事故里执行者以为
    "截在上一轮输出结束"，实际截在自己的叙述上，而输出里没有任何可核对的东西。
    """
    text = " ".join((adapter.get_text(obj) or "").split())
    text = _strip_wrappers(text)
    return text[:limit] + ("…" if len(text) > limit else "")


def locate_split_point(adapter, lines: list[dict], match_text=None, line_no=None, request_id=None) -> tuple[int, int]:
    """指定模式：--match / --line / --request-id 定位截断点。

    返回 (cut, total)；cut 是 1-based 行号（截取 lines[:cut]）。
    校验：候选行必须是 assistant 消息，且下一行是 user 消息或 EOF（完整回复边界）。
    """
    n = len(lines)
    if request_id is not None:
        cand = None
        for i, o in enumerate(lines, 1):
            if adapter.is_assistant_message(o) and adapter.get_request_id(o) == request_id:
                cand = i  # keep last match
        if cand is None:
            raise ForkError(
                f"request_id not found in any assistant reply: {request_id!r}\n"
                f"  Hint 1（最常见）：若 {request_id!r} 其实是**一段文字**（用户说"
                f"「从『…』那条回复开始打分支」），那它不该进 --request-id，而该进 --match：\n"
                f"      … scripts/create_branch.py --session current --match \"{request_id}\"\n"
                "  Hint 2：若它确为请求 ID，则可能属于其他会话/工作区——复制 JSON 里 conversationId "
                "即源会话 ID，用 --session <conversationId> 指定（或用 --request-id 自动反查源会话）"
            )
    elif line_no is not None:
        cand = line_no
        if not (1 <= cand <= n):
            raise ForkError(f"--line {cand} out of range (file has {n} lines)")
    else:
        cand = None
        for i, o in enumerate(lines, 1):
            if not adapter.is_assistant_message(o):
                continue
            if match_text in adapter.get_text(o):
                cand = i  # keep last match
        if cand is None:
            raise ForkError(f"match text not found in any assistant reply: {match_text!r}")

    # 边界校验：截断行是 assistant 且完整收尾（下一行是 user 或 EOF）
    o = lines[cand - 1]
    if not adapter.is_assistant_message(o):
        raise ForkError(f"Split line {cand} is not an assistant message")
    if cand < n:
        nxt = lines[cand]
        if not (adapter.is_user_message(nxt) or nxt.get("type") in ("user", "message")):
            # 下一行既不是 user 消息也不是纯事件行 → 可能落在未完成回复中间
            if adapter.is_assistant_message(nxt):
                raise ForkError(
                    f"Line {cand} is not a complete reply boundary (line {cand+1} is assistant)"
                )
    return cand, n


def verify_branch(adapter, dst_path: str, new_id: str, cut: int, src_id: str) -> list[str]:
    """验证分支文件完整性。返回错误列表（空 = 通过）。

    残留检查用结构化遍历（_find_residue，排除 rawContent/rawResponse 黑名单字段）
    ——与替换引擎策略一致：黑名单字段保留旧 id 是合法设计，不误报。
    """
    errs = []
    raw = adapter.read_raw(dst_path)
    check = [l for l in raw.splitlines() if l.strip()]
    parsed: list[dict] = []
    last_parse_failed = False
    if len(check) != cut:
        errs.append(f"line count {len(check)} != {cut}")
    for i, l in enumerate(check, 1):
        try:
            o = json.loads(l)
        except Exception as e:
            errs.append(f"parse error line {i}: {e}")
            if i == len(check):
                last_parse_failed = True
            continue
        parsed.append(o)
        sid = o.get("sessionId") or o.get("session_id")
        if sid is not None and sid != new_id:
            errs.append(f"line {i} sessionId mismatch: {sid}")
    # 旧 id 残留检查：排除黑名单字段（rawContent/rawResponse 合法保留）
    raw_keys = getattr(adapter, "_RAW_KEYS", set())
    residue = _find_residue(parsed, src_id, raw_keys)
    if residue:
        errs.append(f"old session id still present in {len(residue)} non-raw fields: {residue[:5]}")
    # 末条完整性（末行坏行时跳过——parse error 已单独报，避免检查错行误报）
    if parsed and not last_parse_failed:
        last = parsed[-1]
        if not (adapter.is_assistant_message(last) and adapter.get_text(last).strip()):
            errs.append("last line has no assistant output_text")
    return errs


def _register_branch_with_fp(adapter, src, new_id: str, dst: str, name: str, *,
                             parent_id: str, at_seq: int, prefix_fp: str | None) -> None:
    """调用 `adapter.register_branch`，并在其签名支持时一并传入前缀指纹。

    为什么先探测签名、而不是直接多传一个关键字实参：`register_branch` 是**公开扩展点**
    （本仓库之外也有人写自己的 adapter，文档鼓励这么做）。多传一个参数会让老 adapter
    直接 `TypeError`、**整次 fork 失败**——为一条"加分证据"付这个代价不值得。
    不支持就退回旧调用，代价只是该产品的分支走"未记录指纹"路径（体检里提示复核）。
    """
    kw = dict(src=src, new_id=new_id, dst_path=dst, name=name,
              parent_id=parent_id, at_seq=at_seq)
    try:
        params = inspect.signature(adapter.register_branch).parameters
        supports = "prefix_fp" in params or any(
            p.kind == inspect.Parameter.VAR_KEYWORD for p in params.values()
        )
    except Exception:
        # 自省失败（装饰器改签名等）一律退回旧调用：保守侧只少一层证据，
        # 绝不因为"多传一个参数"让整次 fork 失败（也不重试调用——重试可能重复登记）。
        supports = False
    if supports:
        kw["prefix_fp"] = prefix_fp
    return adapter.register_branch(**kw)


# ----------------------------------------------------------------------
# 分支前缀指纹（v2.4.15）：把"边界可信"从假设变成可核对的事实
# ----------------------------------------------------------------------

PREFIX_FP_ALGO = "sha256-1"
"""指纹算法标识（随记录落盘，将来换算法时能识别旧值 ⇒ 不会把旧值当"漂移"）。"""


def _raw_lines(text: str) -> list[str]:
    """行归一化——与 verify_branch 取行的口径**完全一致**（去空行）。

    两侧（fork 时 / 体检时）必须用同一口径，否则指纹会比出假差异。
    """
    return [l for l in text.splitlines() if l.strip()]


def _read_lines_checked(adapter, ref: str) -> tuple[list[dict], list[int], list[int]]:
    """读条目 + 坏行的两种坐标：`(objs, bad_files, bad_items)`。

    为什么不在这里 try/except 包住 `read_lines` 就算完：那只会把"坏行"重新变成
    "整轮体检崩掉+理由指错"——正是要修的形态。坏行必须**被跳过且被报出**。

    ⚠️ 三种坐标的用途（混用会看错位置，已有反例）：
      · `bad_files` = 文件行号 → **只用于报给用户**（能在编辑器里直接定位）；
      · `bad_items` = 条目序号 → **一切与 at_seq / 边界比较的地方都用它**；
      · `objs` = 条目本身 → 一律取适配器的**原生**实现（`read_lines_checked` / `read_lines`）：
        SQLite 后端的行里有 BLOB(bytes)，任何"经 read_raw 往返"的读法都会把它降级成字符串
        ——既破坏保真、又可能凭空造出"源 id 命中"（2026-09-19 真被全量测试拦住过一次）。
    """
    fn = getattr(adapter, "read_lines_checked", None)
    if callable(fn):
        try:
            r = fn(ref)
            bad_files = list(r.bad_lines)
            bad_items = list(getattr(r, "bad_items", None) or bad_files)
            return list(r.objs), bad_files, bad_items
        except Exception:
            pass
    return list(adapter.read_lines(ref)), [], []


def _prefix_fingerprint(adapter: TranscriptionAdapter, ref: str, n: int) -> str | None:
    """对产物「前 n 行」取指纹；不可读 / 不足 n 行 / n 非法 → None。

    为什么需要它（2026-09-19 设计，针对"体检常驻误报"）：
      判断"源 id 是否残留"必须有一个边界（`at_seq` = fork 当时复制出的前缀行数），
      而**这个边界过去只是个假设**——没有任何办法核对"前 n 行是否仍是 fork 当时的产物"。
      于是只有两种坏选择：要么把边界之后的整段也从严检查（⇒ 你在分支里记录一次血缘就
      常驻误报，闸门变"狼来了"），要么放宽但说不清依据。指纹把边界变成**可核对的事实**：
      fork 时把前 n 行的哈希随 `at_seq` 一起写进谱系，体检时重算比对。
        一致 = 这 n 行确是 fork 原样产物 ⇒ 边界可信（之后的差异只能来自 fork 之后）；
        不一致 = 前缀已被改动 ⇒ **据实报"前缀漂移"**，不再靠猜。
      ⚠️ 它证明的是"前 n 行未被改动"，**不是**"n 恰好等于当初的复制行数"——后者由
      create 期的硬校验保证（`verify_branch` 断言产物行数 == cut，不等则拒绝落位）。

    取指纹一律用**已落位**的产物：SQLite 后端的 tmp 与 dst 是两条取数路径
    （`_pending` vs 数据库），从 dst 取才能与体检侧同源，否则会凭空报"漂移"。
    """
    try:
        if not isinstance(n, int) or n <= 0:
            return None
        # 优先"只读前 n 行"（产物可能上百 MB，真机最大 107MB / 19,195 行）：
        # 适配器能流式读就给头部，读不了（SQLite 等非文件后端）就回退全量读——正确性优先。
        head = getattr(adapter, "read_raw_head", None)
        text = None
        if callable(head):
            try:
                text = head(ref, n)
            except Exception:
                text = None
        if text is None:
            text = adapter.read_raw(ref)
        lines = _raw_lines(text)
        if len(lines) < n:
            return None
        block = "\n".join(lines[:n]).encode("utf-8")
        return PREFIX_FP_ALGO + ":" + hashlib.sha256(block).hexdigest()
    except Exception:
        return None  # 指纹是"加分证据"：取不到不该让 fork 或体检失败


# ----------------------------------------------------------------------
# fork --verify / --doctor：真库体检（把"真库验证"从靠用户兜底变成内置强制检查）
# ----------------------------------------------------------------------

def _collect_real_transcripts(adapter, limit: int = 3) -> list[tuple[str, str, bool, str, int | None, str | None]]:
    """收集真实会话 transcript：分类为 源会话 / 分支，各自取最新 limit 个。

    返回 [(path, session_id, is_branch, parent_id_or_empty, at_seq_or_None, prefix_fp_or_None)]。
    分支识别：查谱系索引（lineage forks / branches）——分支必须用其 parent_id（源 id）
    做残留校验（分支正确时源 id 已被替换干净，若残留 = rewrite 回归）。
    at_seq = fork 当时的快照点（复制出的前缀行数），分支校验必须用它当边界：
    fork 后产品会继续往分支文件追加消息，用"当前最后一轮"当边界会把追加内容
    误判成残留（2026-09-14 修复）。
    prefix_fp = fork 时该前缀的指纹（v2.4.15），用来**核对边界是否可信**；
    老记录没有这个字段 ⇒ None ⇒ 体检按"无法证实边界"处理（只提示复核，不判失败）。
    """
    found: list[tuple[str, str]] = []
    # 会话枚举交给 adapter：文件名≠会话 id 的产品（pi 是 <时间戳>_<id>.jsonl）必须自行覆盖，
    # 否则引擎会把文件名当 id（2026-09-14 跨平台验证修复）。
    try:
        found = list(adapter.list_all_sessions())
    except Exception:
        found = []
    # 排序键交给 adapter：SQLite 后端的转录引用不是文件路径，os.path.getmtime 会崩
    # （2026-09-14 跨平台验证修复；这是第三处被暴露的"转录=文件"隐含假设）
    found.sort(key=lambda x: adapter.sort_key(x[0]), reverse=True)

    # 分支集合 + parent 映射 + 快照点（从旁路谱系索引；_lineage_get 返回 {fork_id: {...}}）
    # parent_id 为空的一律**不算分支**：空串会让 `old_id in v` 恒真 → 全字段误判污染
    # （2026-09-14 审查）。宁可退化为"当源会话检查"，也不要制造假红。
    branch_parent: dict[str, str] = {}
    branch_atseq: dict[str, int | None] = {}
    branch_fp: dict[str, str | None] = {}
    try:
        if hasattr(adapter, "_lineage_get"):
            data = adapter._lineage_get()
            branch_parent = {
                fid: f.get("parent_id") for fid, f in data.items() if f.get("parent_id")
            }
            branch_atseq = {
                fid: f.get("at_seq") for fid, f in data.items() if f.get("parent_id")
            }
            branch_fp = {
                fid: f.get("prefix_fp") for fid, f in data.items() if f.get("parent_id")
            }
        elif hasattr(adapter, "_read_index"):
            data = adapter._read_index()
            for f in data.get("branches", []):
                pid = f.get("parent_id") or f.get("source_id")
                if f.get("id") and pid:
                    branch_parent[f["id"]] = pid
                    branch_atseq[f["id"]] = f.get("at_seq")
                    branch_fp[f["id"]] = f.get("prefix_fp")
    except Exception:
        pass

    sources = [f for f in found if f[1] not in branch_parent]
    branches = [f for f in found if f[1] in branch_parent]
    result = []
    for path, sid in sources[:limit]:
        result.append((path, sid, False, "", None, None))
    for path, sid in branches[:limit]:
        result.append((path, sid, True, branch_parent.get(sid, ""),
                       branch_atseq.get(sid), branch_fp.get(sid)))
    return result


def _find_residue(objs: list[dict], old_id: str, raw_keys: set, start: int = 1) -> list[str]:
    """递归找旧 id 在非黑名单字段中的残留位置（黑名单 = 原始内容键，允许含旧 id）。

    start = objs[0] 在**原文件**中的行号（1-based）。传切片时用它校正行号，
    否则报告会把 L7740 之类的真实行号压成 L1，误导排障（2026-09-14 审查）。
    """
    hits = []

    def walk(node, path):
        if isinstance(node, str):
            if old_id in node:
                hits.append(path or "(root)")
        elif isinstance(node, dict):
            for k, v in node.items():
                if k in raw_keys:
                    continue
                walk(v, f"{path}.{k}" if path else k)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{path}[{i}]")

    for i, o in enumerate(objs, 1):
        walk(o, f"L{start + i - 1}")
    return hits


def _find_structural_residue(objs: list[dict], old_id: str, adapter=None) -> list[str]:
    """结构性残留：old_id 出现在**会话关联字段**（`sessionId` / `session_id`）的值上
    ——**不依赖任何行边界**。

    分支产物正确时，文件内所有会话关联字段都应是分支自己的 id（fork 时已递归改写），
    fork 之后追加的消息也属于分支本人。所以它等于源 id 一定是真污染，
    与"前缀/追加区"如何划分无关——即便谱系 `at_seq` 记录偏小也拦得住这一类。

    两个键都查：WorkBuddy 用 `sessionId`，其他产品/事件行可能用 `session_id`
    （创建期 verify_branch 也是两者都查，此处对齐，2026-09-14 审查）。
    `parentId` 是合法的谱系字段，允许等于源 id，不查。

    说明：本检查是**纵深防御层**（belt-and-braces），与 `_find_residue` 在
    `sessionId`/`session_id` 上存在功能重叠（后者也能命中这两个键）。保留它的价值有二：
    ① 不依赖"前缀/追加区"如何划分——即便未来有人改动边界或宽容逻辑，这一类仍硬拦；
    ② 失败原因可明确报成"会话关联字段结构性残留"而非泛泛的残留。
    它**不是**某条测试的专属兜底，别据此推断覆盖范围（2026-09-14 复核时明确）。
    """
    hits = []

    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                full = f"{path}.{k}" if path else k
                # adapter 可声明某些路径下的会话关联字段是**历史记录**而非关联字段
                # （例：OpenClaw 的 custom 条目 data.sessionId 记录"该 run 发生在哪个会话"）。
                exempt = bool(adapter is not None and adapter.is_historical_id_path(full))
                if not exempt and k in _SESSION_ID_KEYS and isinstance(v, str) and old_id in v:
                    hits.append(full)
                walk(v, full)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{path}[{i}]")

    for i, o in enumerate(objs, 1):
        walk(o, f"L{i}")
    return hits


_SESSION_ID_KEYS = ("sessionId", "session_id")
"""**路由**键（结构性残留检查只认这两个）——证据与**已知缺口**都写在这里，别只看清单。

证据（2026-09-19 真库普查；可复跑，脚本已随仓库提供）:

    python3 tools/routing-key-survey.py keys --projects ~/.workbuddy/projects
    python3 tools/routing-key-survey.py branches --home ~

    覆盖：**约 167 个** WorkBuddy transcript / **约 23.5 万**次出现，判据＝「JSON 键 + 值含 uuid 形态」
    （数字是**撰写时的快照**——真库会持续增长，复跑同一命令得到的数只会更大，口径不变）

    键名                                出现次数      说明
    sessionId                            235,185     会话路由 → 本检查的目标
    parentId                             217,089     **消息级**树链（合法保留源 id，有意不查）
    logicalParentId                          304     **消息级**（同上）
    conversationId / threadId / thread_id / sessionKey / parentUuid …   **0**

⚠️ **已知缺口（不是"已覆盖"）**：本清单只覆盖"用 `sessionId` 命名路由键"的形态
   （WorkBuddy、Claude Code、Hermes 的 `messages.session_id` 都在其列）。**别的后端不在**：
   Codex 的路由键是 `payload.thread_id`（其 adapter docstring 记载 59 处；`payload.session_id`
   已覆盖），pi 的会话标识在 `header.id`、OpenClaw 在 `header.id` / `current_session_id`（键名就是 `id`，
   无法与消息级 `id` 靠键名区分）。
   ⇒ 后果是**偏漏检、不会误报**：这些后端若在**追加区**出现"路由键＝父 id"，只会给"需复核"
   而不是硬失败；**前缀区**仍由键无关的字符串搜索覆盖（那才是主拦截层）。
   ⇒ 要不要把某个键升级为硬拦：**先跑上面两条命令取证，再改**——盲加键名会命中
   `text` / `content` / `arguments` 这类内容字段（真库实测：13 条真实分支里 8 条会被新判红），
   等于把"在分支里写血缘"这种正常内容重新变成常驻红。
"""


# 工具/函数 I/O 数据字段 + 思维链（**段级**精确匹配，避免 "outputsList" 这类误伤）。
# 用途（v2.4.15 起）：只用来**给"需复核"的命中分类**（哪些是工具 I/O / 思维链、哪些是正文），
# 不再决定"是否判失败"——边界之外的命中一律只提示复核（见 verify_environment 的说明）。
# 之所以把它们单列：fork 之后追加的消息里，这些字段出现源 id 属**必然**——
#   · 工具输出：真实案例，`ls ~/.workbuddy/tasks` 的输出里恰好有个目录叫源会话 UUID；
#   · 思维链（`reasoning`）：模型"想"的时候会把刚读到的 id 复述一遍，几乎必现
#     （2026-09-16 补入：当时漏了它，导致本该是"工具/思维链"的命中被算进"正文"）。
_TOOL_IO_FIELD_NAMES = frozenset({
    "output", "arguments", "argumentsDisplayText", "toolResult", "renderer", "error",
    "reasoning",
})


def _is_tool_io_path(path: str) -> bool:
    segs = re.split(r"[.\[]", path)
    return any(s in _TOOL_IO_FIELD_NAMES for s in segs)


def verify_environment(adapter: TranscriptionAdapter) -> list[VerifyItem]:
    """真库体检（fork --verify / --doctor）。

    检查项：
    1. 存储层（adapter.verify_storage）：数据库/transcript 目录存在性 + schema 约束
    2. 真实数据替换验证（L2）：取最新真实会话 → 定位截断点 → rewrite_ids 全量替换
       → 断言非黑名单字段零残留——这就是 v2.2.0 两个 bug 的自动拦截器
    3. 谱系索引可读（旁路 fork.lineage.json / fork.branches.json）
    """
    items = []

    # 1. 存储层
    items.extend(adapter.verify_storage() or [])

    # 2. 真实数据替换验证（L2）
    #    源会话：模拟 rewrite，验证引擎能把自身 id 清干净（黑名单除外）；
    #    分支：直接查源 id（parent_id）是否残留——分支正确时源 id 已清零，
    #          残留 = rewrite 回归或分支产物被污染（不能模拟 rewrite，会顺手修复变假绿）。
    real = _collect_real_transcripts(adapter)
    if not real:
        items.append(VerifyItem(
            "真实数据替换验证", "L1", False,
            "无真实会话可用（仅 fixture 级）。请先用产品产生会话：" + adapter.produce_hint(),
        ))
    else:
        raw_keys = getattr(adapter, "_RAW_KEYS", set())
        n_src = sum(1 for r in real if not r[2])
        n_br = len(real) - n_src
        for path, sid, is_branch, parent_id, at_seq, prefix_fp in real:
            # 带坏行信息读取（v2.4.15 补）：坏行**不抛也不静默**——跳过它继续检查，
            # 但把行号交出来，下面按"落在前缀内还是追加区"分别处置。
            lines, bad_files, bad_items = _read_lines_checked(adapter, path)
            if not lines:
                items.append(VerifyItem(f"真实数据验证 {sid[:8]}", "L2", False, "transcript 为空或不可读"))
                continue
            if is_branch:
                # 分支产物验证：源 id 不得残留（黑名单除外）。**两层判定，判据不同、后果不同**：
                #
                #  【硬失败】产物自身的问题——必定是真问题，且改一下就能修好：
                #   ① 前缀残留（边界之内）：fork 复制出的那一段仍留着源 id ⇒ rewrite 回归 /
                #      产物被改动。前缀是**引擎的产物**，出现在那里的源 id 一定是残留。
                #   ② 全文件 sessionId/session_id 结构性残留：不依赖任何边界。分支产物里所有
                #      会话关联字段都应是分支自己的 id；等于源 id ⇒ 产品会按它把消息路由回源会话。
                #
                #  【需复核】边界之外的引用——**不是引擎的产物**，因此不判失败：
                #   ③ 边界（`at_seq` = fork 复制出的前缀行数）之后的内容，是 fork **之后**由产品
                #      写入的（你继续对话、产品追加工具结果）。那里出现源 id 属正常：分支的常见
                #      用途之一就是**记录自己的血缘**（"我的父会话是谁"），而记录血缘必然写下源 id。
                #      2026-09-19 真机取证：两处命中的实际内容分别是"读谱系文件的输出"与
                #      "身份登记表 + 自报正文"，主题全是"我从哪来"。
                #
                #  ⚠️ 代价与兜底（有意选择，不是疏漏）：降级同时放弃了"at_seq 被记小 ⇒ 被跳过的
                #      区域里藏着真残留"这一形态的**硬拦**。兜底有三条：① create 期整文件零残留
                #      硬校验（落位前拦截：任何 rewrite 回归都在那里挂掉，不会落地）；② 结构性检查
                #      完全不看边界；③ 前缀指纹（见下）能查出"边界之内被改动"。
                #
                #  为什么必须降级（v2.4.15）：③ 与"在分支里记录血缘"**在字节上不可区分**，
                #      旧判据的实际效果是"每正常用一次分支就常驻一条红"。闸门一旦常驻红就变成
                #      "狼来了"——真问题会被淹没在误报里，而 `--verify` 的全部价值就是发布前拦截。
                #      宁可留下可解释、可消解的"需复核"，也不要制造无效的红。
                n = at_seq if isinstance(at_seq, int) and at_seq > 0 else None
                if n is not None and (n > len(lines) or not adapter.is_assistant_message(lines[n - 1])):
                    # at_seq 结构性不可信（越界 / 不是完整 assistant 回复收尾）→ 弃用，
                    # 退回"当前最后一轮"边界：此时命中会落到前缀侧 ⇒ 仍是硬失败（从严）。
                    n = None
                if n is not None and any(bi <= n for bi in bad_items):
                    # 快照点之内有坏行 ⇒ 解析后的条目序列在那一带是断裂的，边界落点不再可信
                    # （可能把真残留认成"追加区"）⇒ 弃用边界，从严。
                    # ⚠️ 这里必须比**条目序号** `bad_items`，不是文件行号（见 parse_jsonl 的坐标说明）。
                    n = None
                boundary = n
                if boundary is None:
                    try:
                        boundary, _ = locate_last_reply(adapter, lines)
                    except ForkError as e:
                        items.append(VerifyItem(f"截断定位 {sid[:8]}", "L2", False, str(e)))
                        continue
                boundary = min(boundary, len(lines))

                # 边界证据 = 前缀指纹比对。只在"边界就是谱系快照点"时才可比——
                # 长度不同（如 at_seq 被弃用、改用最后一轮）就不是同一批行，比了也没意义。
                if n is not None and prefix_fp:
                    fp_now = _prefix_fingerprint(adapter, path, n)
                    if fp_now is None:
                        fp_verdict = "unreadable"
                    else:
                        fp_verdict = "match" if fp_now == prefix_fp else "drift"
                elif prefix_fp:
                    fp_verdict = "skipped"
                else:
                    fp_verdict = "absent"

                prefix_hits = _find_residue(lines[:boundary], parent_id, raw_keys)
                tail_hits = (
                    _find_residue(lines[boundary:], parent_id, raw_keys, start=boundary + 1)
                    if len(lines) > boundary else []
                )
                structural = _find_structural_residue(lines, parent_id, adapter)

                # 追加区的源 id 引用**一律只提示复核、不判失败**——v2.4.15 的定案。
                #
                # 曾试过"边界后未开新 user 回合就从严"（想关掉"污染正好写在边界后第一行"那类形态），
                # 2026-09-19 复核后把它否掉，两条理由都成立：
                #   ① 轴选错了：真实追加里"先开 user 回合"本来就是常态 ⇒ 它挡不住那类形态里最现实的
                #      一种（边界后就是 user 消息、正文里带父 id），那一种照样落在"追加区"；
                #   ② 代价无法证伪：本机只有 WorkBuddy 有真实分支（3 条被追加过、首行都是 user），
                #      其余 5 个后端的追加首行**没有证据**是 user——Claude Code 有 compaction 的
                #      `summary` 条目，Hermes / OpenClaw 有血缘记录条目。若它们先写非 user 条目，
                #      这条规则会把**合法内容**判失败，等于重新制造"常驻红"（本版要消灭的东西）。
                # ⇒ 保护"前缀"靠另外三层、都不依赖它：创建期整文件零残留硬校验、前缀的键无关字符串
                #   搜索、指纹漂移检测。追加区不是引擎的产物，只提示复核。
                appended_hits = list(tail_hits)
                # 边界后不是新回合时仍**据实提示**（只是不升级为失败）：信号有价值，但不足以判罪。
                boundary_not_turn = (
                    len(lines) > boundary and not adapter.is_user_message(lines[boundary])
                )

                # 坏行按"落在前缀内 / 追加区"分开处置（坏行不是"跳过就算"）。
                # ⚠️ 坐标必须用**条目序号**（`bad_items`），不能用文件行号：`at_seq` / `boundary`
                #    都是条目尺度，而文件行号把空行也算进去；混比会看错位置（有反例：
                #    文件第 3 行是坏行、但它只是第 2 个条目 ⇒ "3 <= 2" 为假，坏行被漏判）。
                #    报给用户时仍用**文件行号**（能直接定位到编辑器里那一行）。
                bad_prefix_files = [f for bi, f in zip(bad_items, bad_files) if bi <= boundary]
                bad_tail_files = [f for bi, f in zip(bad_items, bad_files) if bi > boundary]
                bad_marks = [f"L{f}（无法解析）" for f in bad_prefix_files]

                hard = list(prefix_hits) + list(structural) + bad_marks
                ok = not hard
                reviewable = appended_hits if ok else []
                fp_note = {
                    # 文案只承诺"前 boundary 行"——不能写成"这条分支的边界可信"：指纹对**追加区
                    # 一无所知**，那样说是假的安心（属过度承诺）。另外这里刻意不用
                    # markdown 强调符：本串直接打印到终端，`**` 只会原样显示成噪音。
                    "match": f"前缀指纹与 fork 时一致（证据只覆盖前 {boundary} 行；追加区不在其内）",
                    "drift": f"⚠️ 前缀指纹与 fork 时不符：前 {boundary} 行已被改动",
                    "unreadable": "前缀指纹无法读取（本次跳过比对）",
                    "skipped": "谱系快照点不可信，未能比对指纹",
                    "absent": "谱系未记录前缀指纹（旧记录）⇒ 无法证实前缀，建议重打该分支",
                }[fp_verdict]
                if ok:
                    notes = [f"判定前缀 L{boundary}", fp_note]
                    if len(lines) > boundary:
                        note = f"fork 后追加 {len(lines) - boundary} 行不计入"
                        if reviewable:
                            tool_io = [p for p in reviewable if _is_tool_io_path(p)]
                            note += (f"；其中 {len(reviewable)} 处源 id 引用需复核"
                                     f"（工具 I/O 或思维链 {len(tool_io)} 处、正文 "
                                     f"{len(reviewable) - len(tool_io)} 处；记录血缘一类写法属正常）")
                            if boundary_not_turn:
                                note += "；注意：紧接边界的不是新回合，建议多看一眼"
                        if bad_tail_files:
                            note += (f"；追加区另有 {len(bad_tail_files)} 行无法解析"
                                     f"（第 {bad_tail_files[:3]} 行——可能是产品写入过程中的半行）")
                        notes.append(note)
                    notes.append("全文件 sessionId/session_id 零残留")
                    detail = f"源 id {parent_id[:8]} 零残留（" + "；".join(notes) + "）"
                else:
                    if structural:
                        why = "会话关联字段（sessionId/session_id）结构性残留 = 真污染"
                    elif prefix_hits:
                        why = "前缀（fork 复制区）残留 = rewrite 回归或产物被改动"
                    else:
                        why = "前缀内有无法解析的行 ⇒ 产物被损坏或被改动"
                    if bad_prefix_files and not (prefix_hits or structural):
                        detail = (f"前缀内有 {len(bad_prefix_files)} 行无法解析"
                                  f"（第 {bad_prefix_files[:3]} 行）⇒ {why}")
                    else:
                        detail = f"源 id 残留 {len(hard)} 处：{hard[:3]}（{why}）"
                        if bad_prefix_files:
                            detail += (f"；另：前缀内有 {len(bad_prefix_files)} 行无法解析"
                                       f"（第 {bad_prefix_files[:3]} 行）")
                items.append(VerifyItem(f"分支产物校验 {sid[:8]}", "L2", ok, detail,
                                        review=bool(reviewable) or fp_verdict == "drift"))
            else:
                try:
                    cut, total = locate_last_reply(adapter, lines)
                except ForkError as e:
                    # 无任何完整 assistant 回复的会话**不是**适配器缺陷，而是产品侧
                    # 真实存在的形态：回合被中断/模型调用失败/纯注入会话。
                    # Codex 真机实测即有此例（`codex exec fork` 因上游 502 中断，
                    # transcript 里有 user 与元信息、无 assistant）。
                    # 这类会话既不能截断也无从验证 → 记为"跳过"，不计入失败，
                    # 否则体检会把环境噪声报成适配器回归（2026-09-14 真机发现）。
                    # 判据从严：只有**一条 assistant 回复都没有**才跳过；有回复却定位失败
                    # 依旧是硬失败（那是真的定位逻辑问题）。
                    has_reply = any(
                        adapter.is_assistant_message(o) and adapter.get_text(o).strip()
                        for o in lines
                    )
                    if has_reply:
                        items.append(VerifyItem(f"截断定位 {sid[:8]}", "L2", False, str(e)))
                    else:
                        items.append(VerifyItem(
                            f"截断定位 {sid[:8]}", "L2", True,
                            "跳过：该会话无任何完整 assistant 回复（回合中断/调用失败），不参与 L2 抽查",
                        ))
                    continue
                # 源会话：模拟 rewrite，验证引擎替换能力
                new_id = "verify-" + uuid.uuid4().hex[:12]
                rewritten, n = adapter.rewrite_ids(copy.deepcopy(lines[:cut]), sid, new_id)
                residue = _find_residue(rewritten, sid, raw_keys)
                ok = not residue
                detail = f"{n} 处替换，截断点 L{cut}/{total}"
                if residue:
                    detail += f"，残留 {len(residue)} 处：{residue[:3]}"
                # 源会话的坏行不算我们的缺陷（那是产品侧的数据），但**必须说出来**：
                # 一是"少看了一部分内容"不能当全绿，二是坏行落在复制范围内时打分支会被拒。
                if bad_files:
                    # 范围判定用条目序号、展示用文件行号（见 parse_jsonl 的坐标说明）
                    in_cut_lines = [f for bi, f in zip(bad_items, bad_files) if bi <= cut]
                    detail += (f"；⚠️ 该会话有 {len(bad_files)} 行无法解析（第 {bad_files[:3]} 行）已跳过"
                               + (f"，其中 {len(in_cut_lines)} 行落在复制范围内 ⇒ 打分支会被拒绝"
                                  f"（请先修好或换一个截断点）" if in_cut_lines else "，均在复制范围之外"))
                items.append(VerifyItem(f"真实数据替换 {sid[:8]}", "L2", ok, detail,
                                        review=bool(bad_files) and ok))
        # 汇总项 ok = 本轮所有真实数据检查项都通过（不硬编码绿，2026-09-03 复核）
        # 口径（v2.4.15）：只有"失败"才让汇总变红；"需复核"是提示，**不阻塞**——
        # 理由见分支判定处的说明（常驻红 = 闸门失效，比一条可解释的提示更糟）。
        data_items = [it for it in items if it.name.startswith(("真实数据替换", "分支产物校验", "截断定位"))]
        n_fail = sum(1 for it in data_items if not it.ok)
        n_review = sum(1 for it in data_items if it.ok and getattr(it, "review", False))
        all_ok = bool(data_items) and n_fail == 0
        if n_fail:
            tail = f"（{n_fail} 项失败——见上）"
        elif n_review:
            tail = f"（无失败项；{n_review} 项需人工复核，见上 ⚠️）"
        else:
            tail = "（全部通过）"
        items.append(VerifyItem(
            "体检覆盖", "L2", all_ok,
            f"抽查最新 {n_src} 个源会话 + {n_br} 个分支" + tail,
            # 汇总项**不**自己带 review 标记：否则上面那 N 项会被算成 N+1 项
            # （本轮真机实测发现的计数瑕疵）。需复核的清单在它上面的各分项里。
            review=False,
        ))

    # 3. 谱系索引
    try:
        if hasattr(adapter, "_read_index"):
            data = adapter._read_index()
            branches = data.get("branches", [])
            items.append(VerifyItem("谱系索引", "L2", True, f"可读（{len(branches)} 个分支记录）"))
        elif hasattr(adapter, "_lineage_get"):
            data = adapter._lineage_get()  # {fork_id: {...}}
            items.append(VerifyItem("谱系索引", "L2", True, f"可读（{len(data)} 个分支记录）"))
        else:
            items.append(VerifyItem("谱系索引", "L1", True, "adapter 无旁路索引（跳过）"))
    except Exception as e:
        items.append(VerifyItem("谱系索引", "L2", False, str(e)))

    return items


def create_fork(
    adapter: TranscriptionAdapter,
    session_ref: str,
    match_text: str = None,
    line_no: int = None,
    request_id: str = None,
    name: str = None,
    dry_run: bool = False,
    backups_dir: str = None,
    whole: bool = False,
) -> ForkResult:
    """核心入口：创建分支。

    流程：resolve → find → locate → backup → truncate+rewrite → write → verify → register
    （verify 先于 register——验证失败不留任何 db/lineage 痕迹；2026-09-04 学习 Marvis）

    `whole=True`：默认模式下强制"整份复制"语义（含当前未完成回合的叙述）。
    只在"会话内打分支"时有区别——那种场景默认要切掉本轮（含"打分支"这条指令本身），
    而 `--whole` 是它的显式逃生口（v2.4.9）。

    `backups_dir=None` 时取 adapter.backups_dir()（读 FORK_BACKUP_DIR 环境变量）。
    """
    if backups_dir is None:
        backups_dir = adapter.backups_dir()
    # request-id 模式：用户复制 UI "请求 ID" 打分支，可能不知道源会话（跨 workspace）。
    # 若 --session 是 current（未显式指定源），先全盘反查该 request-id 属于哪个会话，
    # 自动定位源——这样用户只需贴复制的 ID 就能打分支，无需理解 session 概念。
    if request_id and (not session_ref or session_ref == "current"):
        auto_src = adapter.find_session_by_request_id(request_id)
        if auto_src:
            session_ref = auto_src

    src_id = adapter.resolve_session(session_ref)
    transcript, slug = adapter.find_transcript(src_id)
    if not transcript:
        raise ForkError(
            f"Transcript not found for {src_id!r}\n"
            f"  Hint 1（最常见）: 若 {src_id!r} 其实是**一段文字**而不是会话 ID，"
            f"那它不该进 --session，而该进 --match：\n"
            f"      … scripts/create_branch.py --session current --match \"{src_id}\"\n"
            "  Hint 2: 若它确为会话 ID，请确认该会话属于当前工作区（跨工作区需用对应的 --adapter）。"
        )

    src_meta = adapter.load_session_meta(src_id)
    if src_meta is None:
        # 有些产品无索引（纯文件），用最小 meta
        src_meta = SessionMeta(id=src_id, cwd=slug or "")

    lines, src_bad_files, src_bad_items = _read_lines_checked(adapter, transcript)
    if not lines:
        raise ForkError(f"Transcript is empty or unreadable: {transcript}")
    if src_bad_files:
        # 源会话里的坏行会被**跳过**（不复制进产物）——这是有意的，但绝不能静默：
        # 复制出来的东西会少一段，用户有权知道。（防御性：本机真库实测 0 例坏行。）
        notify(f"源会话有 {len(src_bad_files)} 行无法解析（第 {src_bad_files[:5]} 行），"
               f"已跳过、不会复制进分支", quietable=False)

    if match_text or line_no or request_id:
        # locate_split_point 找不到时自行 ForkError（带 Hint），此处不会返回 None
        cut, total = locate_split_point(adapter, lines, match_text, line_no, request_id)
        how = (
            f"match={match_text!r}" if match_text
            else (f"line={line_no}" if line_no else f"request_id={request_id!r}")
        )
    else:
        # 默认模式有两种语义，判据 = **"我是不是就在被 fork 的那个会话里"**：
        #
        #   ① 会话内打分支（agent 通过自己的工具执行本脚本，环境里带着该会话的标识）：
        #      要的是"上一轮输出结束" ⇒ 切在最后一条 user 消息（= 本轮"打分支"指令）之前。
        #      **必须锚 user 消息**：本轮叙述早已写进同一份文件，锚"最后一条 assistant 文本"
        #      会吞掉整段本轮内容，且随 agent 继续输出而前移（真实事故两例见
        #      locate_before_current_turn 的 docstring）。
        #   ② 外部打分支（终端执行 / 定时任务 / 显式指定别家会话）：要的是"整份复制"
        #      ⇒ 切在文件末尾最后一条完整 assistant 回复之前（v2.1.0 起的行为）。
        #
        # 判据用"执行环境里的会话标识"而不是 `--session` 字面：`--session current` 从终端
        # 执行时同样是 current（那时并没有"本轮"要排除），字面量区分不了二者。
        running = None
        probe = getattr(adapter, "running_session_id", None)
        if callable(probe):
            running = probe()
        if running and running == src_id and not whole:
            cut, total, note = locate_before_current_turn(adapter, lines)
            # 本轮指令贴了 request id ⇒ 按它切（v2.4.23：既不拒绝、也不静默按默认切）。
            # 两种改法的来龙去脉见 apply_pasted_request_id 的 docstring。
            cut, rid_note = apply_pasted_request_id(adapter, lines, cut, src_id)
            how = (f"in-session · {rid_note}" if rid_note
                   else f"in-session · 上一轮输出结束 · {note}")
        else:
            cut, total = locate_last_reply(adapter, lines)
            why = "显式 --whole" if (whole and running == src_id) else "未检出会话内上下文"
            how = f"whole · 最后一条完整 assistant 回复末尾（{why}）"

    new_id = str(uuid.uuid4())
    if name is None:
        hint = adapter.extract_title_hint(lines)
        name = f"分支·{hint}" if hint else "分支"

    backup_dir = None
    truncated = lines[:cut]
    truncated, replacements = adapter.rewrite_ids(truncated, src_id, new_id)
    dst = adapter.branch_target(transcript, new_id)
    # L0 原子写（2026-09-04 事务化改造）：先写 .tmp（不被侧边栏扫、不在 db → 零外部可见副作用），
    # verify 校验 tmp 的磁盘字节；通过才 os.replace 落位（原子，无中间态）。
    # 自检失败/中途异常 = 只留 tmp 垃圾文件（无害）——回滚不依赖删除（L0 优于 L1）。
    tmp = f"{dst}.{os.getpid()}.{uuid.uuid4().hex[:6]}.tmp"
    try:
        if not dry_run:
            notify(f"备份源会话 / backing up source session: {transcript}", quietable=False)
            backup_dir = adapter.backup_transcript(transcript, backups_dir)
        adapter.write_branch(tmp, truncated)
        try:
            errs = verify_branch(adapter, tmp, new_id, cut, src_id)
        except Exception as e:
            # verify 自身异常：tmp 删不掉也无害（不在 db/侧边栏）
            _safe_remove(tmp)
            raise ForkError(f"VERIFY 执行异常：{e}") from e

        if dry_run:
            # dry-run 走完整校验路径（洞 5：dry-run 的 ok 要有真实信息量），只是不落位/不登记
            if errs:
                _safe_remove(tmp)
                raise ForkVerifyError(errs)
            _safe_remove(tmp)
            return ForkResult(
                ok=True, src_id=src_id, new_id=new_id, name=name, cut=cut, total=total,
                how=how, transcript_path=transcript, dst_path=dst, backup_dir=None,
                replacements=replacements, dry_run=True, verified=True,
            )

        if errs:
            # 尚未产生任何外部可见状态——只需不开始，不需撤销
            _safe_remove(tmp)  # 删不掉也无所谓：.tmp 不被扫
            raise ForkVerifyError(errs)

        # ── 文件落位（第一个"发布"动作；失败态优先对准孤儿文件侧）──
        notify(f"落位分支文件 / landing branch file: {dst}", quietable=False)
        adapter.finalize_branch(tmp, dst)
        # 读锁不再自动加（v1.4.0 起提示用户自行设为只读），此处只负责落位

        # ── 前缀指纹（v2.4.15）：从**已落位**的产物取，随后跟 `at_seq` 一起登记 ──
        # 取不到（None）不阻断 fork：指纹是"加分证据"，用于让体检能核对边界，
        # 而体检对"无指纹"有明确退化路径（提示复核，不误判）。
        prefix_fp = _prefix_fingerprint(adapter, dst, cut)

        # ── 登记（db + lineage；内部顺序见 adapter，外层只做补救）──
        try:
            _register_branch_with_fp(adapter, src_meta, new_id, dst, name,
                                     parent_id=src_meta.id, at_seq=cut, prefix_fp=prefix_fp)
        except Exception as e:
            # register 失败（其内部已尽量同序，db/lineage 侧用 unregister 兜底清理）；
            # 文件已落位——回滚文件让失败态退回孤儿文件（无害）；删不掉必须显式报错
            unreg_err = ""
            try:
                unreg = getattr(adapter, "unregister_branch", None)
                if callable(unreg):
                    notify(f"回滚注册痕迹 / rolling back registration: {new_id}", quietable=False)
                    unreg(new_id)
            except Exception as re:
                unreg_err = f"\n  注册痕迹清理失败（db/lineage 可能残留 {new_id[:8]}，请人工清理）：{re}"
            if _safe_remove(dst):
                raise ForkRegisterError(f"登记失败，分支文件已回滚：{dst}{unreg_err}") from e
            raise ForkRollbackError(
                f"登记失败，且分支文件无法删除——需人工清理：\n  {dst}\n"
                f"  该文件未完整登记，可能残留 db/谱系痕迹{unreg_err}"
            ) from e
    finally:
        # 兜底清理 tmp（replace 成功后 tmp 已不存在）
        _safe_remove(tmp)

    return ForkResult(
        ok=True, src_id=src_id, new_id=new_id, name=name, cut=cut, total=total,
        how=how, transcript_path=transcript, dst_path=dst, backup_dir=backup_dir,
        replacements=replacements, verified=True,
    )


def list_forks(adapter: TranscriptionAdapter, cwd: str = None) -> list[SessionMeta]:
    """列出分支（交给 adapter 的查询实现）。"""
    return adapter.list_branches(cwd)
