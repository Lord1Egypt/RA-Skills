"""链接 → v1 拆解卡 查找 + freshness 判断 + 自动 fallback。

用户传 XHS 链接，v2 不让用户记拆解卡文件名。本模块负责：
1. 解析链接 → note_id（复用 v1 linkresolve）
2. 在 docs/deconstructions/ 查找包含此 note_id 的拆解卡
3. 判断 freshness（≤7 天直接复用；>7 天需用户决定）
4. 找不到 → 透明触发 v1 (extract_xhs.py) + 写 stub 拆解卡

兼容两种拆解卡结构：
- 旧（v1）：docs/deconstructions/AIC-xxx-slug.md
- 新（v2 后）：docs/deconstructions/AIC-xxx-slug/deconstruction.md

⚠️ Auto-fallback 限制（v0.2.1）：自动生成的 stub 卡只填**文本类字段**
（来自 note.json 的 desc / hashtags / 互动 + 来自 comments.json 的评论）。
**视觉拆解（参考内容拆解 / 风格 / 场景 / 情绪钩子）需 agent 后续读 frames/ 自己补**。
完整自动视觉拆解（vision LLM）规划在 v0.3.0+。
"""

from __future__ import annotations
import json
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path


# 默认拆解卡 freshness：7 天以内直接复用，超期需 prompt 用户
DEFAULT_FRESHNESS_DAYS = 7

# 拆解卡里嵌入 note_id 的形式（实测 v1 输出格式）
# - "> note_id: `xxx`"
# - "> 参考链接：https://www.xiaohongshu.com/explore/xxx"
_NOTE_ID_PATTERNS = [
    re.compile(r"`([a-f0-9]{24})`"),  # `note_id` style
    re.compile(r"explore/([a-f0-9]{24})"),  # explore URL
    re.compile(r"discovery/item/([a-f0-9]{24})"),  # discovery URL
]


@dataclass
class CardLookupResult:
    found: bool
    card_path: Path | None = None
    note_id: str | None = None
    age_days: int | None = None  # mtime 距今天数
    is_fresh: bool = False        # age_days <= freshness_days
    is_v2_structure: bool = False  # True = 目录/deconstruction.md, False = 单 .md


def _extract_note_ids_from_card(card_text: str) -> set[str]:
    """从拆解卡文本提取所有 24-hex note_id 候选。"""
    out = set()
    for pat in _NOTE_ID_PATTERNS:
        for m in pat.findall(card_text):
            out.add(m)
    return out


def _list_card_files(deconstructions_dir: Path) -> list[tuple[Path, bool]]:
    """列出所有拆解卡，返回 [(path, is_v2_structure)]。

    - v1 旧结构: docs/deconstructions/*.md (单文件)
    - v2 新结构: docs/deconstructions/*/deconstruction.md
    """
    out: list[tuple[Path, bool]] = []
    if not deconstructions_dir.exists():
        return out
    for p in deconstructions_dir.iterdir():
        if p.is_file() and p.suffix == ".md":
            # 跳过 .v1.md / .v2.md 备份
            if any(s in p.stem for s in (".v1", ".v2", ".v3")):
                continue
            out.append((p, False))
        elif p.is_dir():
            decon = p / "deconstruction.md"
            if decon.exists():
                out.append((decon, True))
    return out


def find_card_by_note_id(
    note_id: str,
    deconstructions_dir: Path | None = None,
    freshness_days: int = DEFAULT_FRESHNESS_DAYS,
) -> CardLookupResult:
    """在 docs/deconstructions/ 找含此 note_id 的拆解卡。

    Args:
        note_id: 24-hex XHS note ID
        deconstructions_dir: 默认 cwd/docs/deconstructions/
        freshness_days: 复用阈值（>= 此天数会标 is_fresh=False）

    Returns:
        CardLookupResult — found/path/freshness 信息
    """
    if deconstructions_dir is None:
        deconstructions_dir = Path.cwd() / "docs" / "deconstructions"
    elif not isinstance(deconstructions_dir, Path):
        deconstructions_dir = Path(deconstructions_dir)

    for path, is_v2 in _list_card_files(deconstructions_dir):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if note_id in _extract_note_ids_from_card(text):
            mtime = path.stat().st_mtime
            age_seconds = time.time() - mtime
            age_days = int(age_seconds // 86400)
            return CardLookupResult(
                found=True,
                card_path=path,
                note_id=note_id,
                age_days=age_days,
                is_fresh=(age_days <= freshness_days),
                is_v2_structure=is_v2,
            )

    return CardLookupResult(found=False, note_id=note_id)


def make_v2_card_dir(
    deconstructions_dir: Path,
    task_id: str,
    title_slug: str,
) -> Path:
    """构造 v2 风格拆解卡目录 + deconstruction.md 路径。

    返回 deconstruction.md 的绝对路径（目录已 mkdir）。
    """
    safe_slug = re.sub(r"[^\w一-龥\-_·]+", "-", title_slug)[:30].strip("-") or "untitled"
    card_dir = deconstructions_dir / f"{task_id}-{safe_slug}"
    card_dir.mkdir(parents=True, exist_ok=True)
    return card_dir / "deconstruction.md"


def make_v2_generated_dir(card_dir: Path, gen_id: str, type_: str) -> Path:
    """在拆解卡目录下创建一次 generate 的产出子目录。

    形如 GEN-260427-001-{type}/
    """
    gen_dir = card_dir / "generated" / f"{gen_id}-{type_}"
    gen_dir.mkdir(parents=True, exist_ok=True)
    return gen_dir


# ─── auto-fallback：跑 extract_xhs.py + 写 stub 卡 ───

def _run_extract_xhs(link: str, out_dir: Path, log) -> Path:
    """subprocess 调用 extract_xhs.py，返回工作区路径。"""
    extract_script = Path(__file__).resolve().parent.parent / "extract_xhs.py"
    if not extract_script.exists():
        raise RuntimeError(f"extract_xhs.py not found at {extract_script}")

    log(f"    [auto-fallback] running extract_xhs.py to prepare workspace...")
    result = subprocess.run(
        [sys.executable, str(extract_script), link, "--out", str(out_dir)],
        capture_output=True,
        text=True,
        timeout=300,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"extract_xhs.py failed (exit {result.returncode}):\n"
            f"stderr: {result.stderr[-500:]}"
        )
    return out_dir


def _write_stub_card(
    note_data: dict,
    comments: list[dict],
    card_path: Path,
    task_id: str,
) -> None:
    """从 note.json + comments.json 数据合成一份 stub 拆解卡。

    填充：元数据 / 标题 / desc / 标签 / 评论
    留空：视觉拆解（参考内容拆解 / 风格 / 场景 / 情绪钩子 / 旁白逻辑）→ ⚠️ TODO 标记
    """
    nickname = note_data.get("author_nickname", "未知")
    note_id = note_data.get("note_id", "")
    title = note_data.get("title", "(无标题)")
    desc = note_data.get("desc", "")
    type_ = note_data.get("type", "")
    duration = note_data.get("video_duration", 0)
    likes = note_data.get("liked_count", 0)
    saves = note_data.get("collected_count", 0)
    cmt_count = note_data.get("comments_count", 0)
    shares = note_data.get("shared_count", 0)
    ip = note_data.get("ip_location", "")
    ts = note_data.get("time", 0)
    pub_date = time.strftime("%Y-%m-%d", time.localtime(ts / 1000)) if ts else ""
    hashtags = note_data.get("hashtags", [])
    ratio = (saves / likes) if likes else 0
    type_label = "视频" if type_ == "video" else "图片"

    # 真实评论（过滤 pinned）
    user_comments = [c for c in comments if not c.get("is_pinned")]
    cmt_list = "\n".join(f"  - {c.get('content', '')}" for c in user_comments[:10])
    if not cmt_list:
        cmt_list = "  - （无用户评论）"

    content = f"""# {task_id} | {title or '(无标题)'}

> 参考链接：https://www.xiaohongshu.com/explore/{note_id}
> 拆解时间：{time.strftime("%Y-%m-%d %H:%M")}
> 平台：小红书
> 内容类型：{type_label}{f"（{duration}s）" if duration else ""}
> **拆解状态：⚠️ AUTO-STUB**（v0.2.1 自动生成）—— 文本字段已填，视觉字段需 agent 后续完善

## 元数据
- **作者**：{nickname}
- **发布时间**：{pub_date}（IP {ip}）
- **互动**：👍 {likes} ｜ ⭐ {saves} ｜ 💬 {cmt_count} ｜ 📤 {shares}
- **note_id**：`{note_id}`
- **关键比例**：藏赞比 {ratio:.2f}

---

## 一、定位

### 1. 内容目标
未指定（agent 可推断）

### 2. 目标客群
⚠️ **AUTO-STUB**：agent 需结合 desc + 评论 + 视觉细节后填

### 3. 爆款主题
⚠️ **AUTO-STUB**：agent 需读 frames/ 后填

---

## 二、拆解

### 4. 参考内容拆解
⚠️ **AUTO-STUB**：v0.2.1 不做视觉拆解。
完整拆解请 agent 按 SKILL.md Step 4 流程：读 `frames/frame_*.png`（{type_label}帧）→ 按时间段聚合写入此处。
工作区路径：`{card_path.parent.parent.absolute() if card_path.parent.name != 'deconstructions' else card_path.parent.absolute()}/.workspace/`

### 5. 风格标签
⚠️ AUTO-STUB（agent 后填）

### 6. 场景标签
⚠️ AUTO-STUB（agent 后填）

### 7. 情绪钩子
⚠️ AUTO-STUB（agent 后填）

### 8. 评论关键词
**原始评论**（已过滤 pinned）：
{cmt_list}

> agent 后续按 Step 5c 分类成"问/求/夸/异议"四类。

---

## 三、文案

### 9. 参考视频旁白文案
{"⚠️ AUTO-STUB（agent 读 frames/ 字幕条 + desc 拼合）" if type_ == "video" else "无（图文内容）"}

### 10. 参考视频旁白文案逻辑分析
{"⚠️ AUTO-STUB（agent 后填，按分层结构）" if type_ == "video" else "不适用（图文）"}

### 11. 参考封面文案
⚠️ AUTO-STUB

### 12. 参考发布主题
{title or '(无标题)'}

### 13. 参考发布文案
```
{desc}
```

### 14. 参考热门标签
{' '.join('#' + t for t in hashtags) if hashtags else '⚠️ 无'}

---

## 四、可学习要点
⚠️ **AUTO-STUB**：v0.2.1 自动生成的 stub 卡留空。
agent 完成视觉拆解后，按客观/品牌视角模式补此章节。

---

## 图谱回写日志
本次为 AUTO-STUB，无图谱回写。
完整拆解后，agent 按 SKILL.md Step 6 决定是否回写。

---

> ℹ️ **此卡是 v2 generate auto-fallback 在 v0.2.1 自动生成的 stub**。
> v2 可基于此 stub 生成内容（质量受限于视觉信息缺失）。
> 推荐手动跑完整流程：
> 1. 读 `frames/` 下抽帧
> 2. 补全本卡的 ⚠️ 标记字段
> 3. 重新跑 v2 generate（用 `--fresh` 强制生效）
"""
    card_path.parent.mkdir(parents=True, exist_ok=True)
    card_path.write_text(content, encoding="utf-8")


def auto_create_card(
    link: str,
    note_id: str,
    deconstructions_dir: Path,
    log,
) -> Path:
    """没找到拆解卡时透明触发 v1 + 写 stub 卡。

    Returns:
        新创建的拆解卡路径
    """
    if not isinstance(deconstructions_dir, Path):
        deconstructions_dir = Path(deconstructions_dir)

    # 1. 跑 extract_xhs.py，工作区放在拆解卡目录的 .workspace 子目录
    task_id = f"AIC-{time.strftime('%y%m%d')}-AUTO-{int(time.time()) % 1000:03d}"
    card_dir = deconstructions_dir / f"{task_id}"
    workspace = card_dir / ".workspace"
    workspace.mkdir(parents=True, exist_ok=True)

    _run_extract_xhs(link, workspace, log)

    # 2. 读 note.json + comments.json
    note_json = workspace / "note.json"
    comments_json = workspace / "comments.json"

    if not note_json.exists():
        raise RuntimeError(f"extract_xhs.py 跑完后没找到 note.json @ {note_json}")

    note_data = json.loads(note_json.read_text(encoding="utf-8"))
    comments = []
    if comments_json.exists():
        try:
            data = json.loads(comments_json.read_text(encoding="utf-8"))
            if isinstance(data, list):
                comments = data
        except (json.JSONDecodeError, OSError):
            pass

    # 3. 写 stub 卡
    card_path = card_dir / "deconstruction.md"
    _write_stub_card(note_data, comments, card_path, task_id)
    log(f"    [auto-fallback] stub card created: {card_path.relative_to(deconstructions_dir.parent.parent) if card_path.is_relative_to(deconstructions_dir.parent.parent) else card_path}")
    log(f"    [auto-fallback] ⚠️ stub 仅含文本字段；视觉字段（拆解/风格/钩子）由 agent 后续完善")

    return card_path


def find_or_auto_create(
    link: str,
    note_id: str,
    deconstructions_dir: Path | None = None,
    freshness_days: int = DEFAULT_FRESHNESS_DAYS,
    log=print,
) -> CardLookupResult:
    """v2 generate 的 step 1 入口：先 find，没找到自动跑 v1 + 写 stub。

    Args:
        link: 用户原始 XHS 链接（auto-create 用）
        note_id: 已解析的 note_id
        deconstructions_dir: 默认 cwd/docs/deconstructions/
        freshness_days: 复用阈值
        log: 进度输出

    Returns:
        CardLookupResult — 永远 found=True（要么原本就有，要么刚创建）
    """
    if deconstructions_dir is None:
        deconstructions_dir = Path.cwd() / "docs" / "deconstructions"

    # 先找
    result = find_card_by_note_id(note_id, deconstructions_dir, freshness_days)
    if result.found:
        return result

    # 没找到 → auto-create
    log(f"    no existing card for {note_id} — triggering auto-fallback")
    card_path = auto_create_card(link, note_id, deconstructions_dir, log)

    # 重新 find（应该 found=True）
    return find_card_by_note_id(note_id, deconstructions_dir, freshness_days)
