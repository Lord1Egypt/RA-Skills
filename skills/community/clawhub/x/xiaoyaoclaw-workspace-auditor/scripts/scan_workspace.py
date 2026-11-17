#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scan_workspace.py - OpenClaw Workspace Auditor 核心扫描脚本

只读体检：扫描 OpenClaw agent 工作区健康度，输出分级报告（JSON / Markdown）。
零第三方依赖（Python 标准库），只报不修。

检查项（5 类，渐进式依赖）：
  1. 目录合规   (依赖 initializer 标准目录)
  2. 任务健康   (依赖 tracker PROGRESS.md 规范)
  3. 记忆健康   (通用约定 memory/ + MEMORY.md)
  4. 知识库健康 (依赖 kb-retriever data_structure.md 索引)
  5. 垃圾/临时  (通用，无依赖)

用法:
  python scan_workspace.py [--root PATH] [--json] [--report] [--days N] [--max-file MB]

退出码: 0 = 正常完成（无论发现什么）
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ---------------------------------------------------------------- 常量

VERSION = "1.1.0"

STANDARD_DIRS = ["projects", "tasks", "outputs", "knowledge", "scripts", "memory", "tmp"]

SYSTEM_DIR_NAMES = {".openclaw", "agent", "sessions", ".git", ".clawhub", "__pycache__", ".venv", "node_modules", "skills"}

# kb-retriever 支持的文件类型
KB_SUPPORTED_EXTS = {".md", ".pdf", ".xlsx"}

# tracker v2 PROGRESS.md 合法状态
PROGRESS_STATUSES = {"active", "done", "archived", "paused"}

# 命名豁免（系统/约定文件，不查命名）
NAME_EXEMPT = {
    "README.md", "README.en.md", "LICENSE", "DESIGN.md", "USER_GUIDE.md",
    "SKILL.md", "PROGRESS.md", "MEMORY.md", "WORKSPACE.md", "data_structure.md",
    "CHANGELOG.md", "CONTRIBUTING.md", "hero.svg", "community-qr.png",
}

# 根目录允许的非 *.md 配置文件（运行约定，豁免 root-nonmd）
ROOT_FILE_EXEMPT = {"distill-config.json"}

# 项目内部结构目录：命名由项目自身决定，auditor 不检查（上游保留/模板/原始数据等）
INTERNAL_DIR_NAMES = {
    "references", "templates", "raw", "docs", "scripts", "assets", "tests",
    "test", "examples", "dist", "build", "output", "outputs", "tmp", "archive",
}

# 正则
RE_KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*(\.[a-z0-9]+)*$")
RE_SNAKE = re.compile(r"^[a-z0-9_]+\.py$")
RE_CAMEL = re.compile(r"^[a-z][a-zA-Z0-9]*\.(js|ts|jsx|tsx)$")
RE_CJK = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf]")

TZ = timezone(timedelta(hours=8))  # Asia/Shanghai


# ---------------------------------------------------------------- 工具

def now_str():
    return datetime.now(TZ).strftime("%Y-%m-%dT%H:%M:%S%z")


def is_system_dir(name: str) -> bool:
    return name in SYSTEM_DIR_NAMES or name.startswith(".")


def has_cjk(text: str) -> bool:
    return bool(RE_CJK.search(text))


def find_workspace_root(start: Path) -> Path:
    """从 start 向上找 WORKSPACE.md，找不到返回 start 本身。"""
    cur = start.resolve()
    while True:
        if (cur / "WORKSPACE.md").exists():
            return cur
        if cur.parent == cur:
            return start.resolve()
        cur = cur.parent


def walk_files(root: Path, skip_system: bool = True):
    """遍历文件，返回相对路径列表（posix 风格）。跳过系统目录/隐藏目录。"""
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dp = Path(dirpath)
        rel_dir = dp.relative_to(root)
        if skip_system:
            # 只过滤系统目录；中文目录/文件名是内容库合法命名，保留
            dirnames[:] = [d for d in dirnames if not is_system_dir(d)]
        for fn in filenames:
            if skip_system and fn.startswith("."):
                continue
            out.append((rel_dir / fn).as_posix())
    return out


# ---------------------------------------------------------------- 检查器

class Auditor:
    def __init__(self, root: Path, days: int, max_file_mb: int):
        self.root = root
        self.days = days
        self.max_file_mb = max_file_mb
        self.findings = []
        self.skipped = []  # 降级提示

    # ---- 公共 ----
    def add(self, fid, severity, category, path, message, fix):
        self.findings.append({
            "id": fid, "severity": severity, "category": category,
            "path": path, "message": message, "fix": fix,
        })

    def skip(self, category, reason):
        self.skipped.append({"category": category, "reason": reason})

    # ============ 1. 目录合规 ============
    def check_dirs(self):
        cat = "dirs"
        missing = [d for d in STANDARD_DIRS if not (self.root / d).is_dir()]
        if missing:
            self.add("dir-missing", "yellow", cat, "",
                     f"标准目录缺失: {', '.join(missing)}",
                     "安装 xiaoyaoclaw-workspace-initializer 或手动创建这些目录")
        else:
            self.add("dir-ok", "green", cat, "", "标准目录齐全", "")

        # 根目录纯净：只允许 *.md 与目录/隐藏文件
        for item in sorted(self.root.iterdir()):
            if item.name.startswith(".") or is_system_dir(item.name):
                continue
            if (item.is_file() and item.suffix.lower() != ".md"
                    and item.name not in ROOT_FILE_EXEMPT):
                self.add("root-nonmd", "yellow", cat, item.name,
                         "根目录存在非 *.md 文件（规范：根目录只放配置文件）",
                         "把文件移到 projects/ tasks/ outputs/ 等对应目录")

        # 根目录多余目录：标准/系统/隐藏目录之外的一级目录（内容应归入标准目录）
        extra = [item.name for item in sorted(self.root.iterdir())
                 if item.is_dir()
                 and not item.name.startswith(".")
                 and not is_system_dir(item.name)
                 and item.name not in STANDARD_DIRS]
        if extra:
            self.add("root-extra-dir", "yellow", cat, "",
                     f"根目录存在非标准目录 {len(extra)} 个: {', '.join(extra)}"
                     "（规范：内容归入 projects/tasks/outputs/knowledge，根目录只放 *.md）",
                     "移入对应标准目录；确属系统/运行时目录可加入 SYSTEM_DIR_NAMES 豁免，或确认用途后归档")

        # 命名规范（内容目录：projects/tasks/knowledge；中文名与系统文件豁免）
        # 先扫根目录一级子目录（非标准/非系统目录的命名与存在性）
        for item in sorted(self.root.iterdir()):
            if not item.is_dir() or is_system_dir(item.name) or item.name.startswith("."):
                continue
            if item.name in STANDARD_DIRS:
                continue
            if has_cjk(item.name):
                continue
            if not RE_KEBAB.match(item.name):
                self.add("name-dir", "yellow", cat, item.name,
                         f"根目录子目录名不符合 kebab-case: {item.name}",
                         "重命名为小写+连字符，或归入标准目录")
        # 再扫内容目录递归
        for area in ("projects", "tasks", "knowledge"):
            base = self.root / area
            if not base.is_dir():
                continue
            for dirpath, dirnames, filenames in os.walk(base):
                dirnames[:] = [d for d in dirnames
                               if not is_system_dir(d) and d not in INTERNAL_DIR_NAMES]
                rel_dir = Path(dirpath).relative_to(self.root).as_posix()
                for d in dirnames:
                    if d in NAME_EXEMPT or has_cjk(d):
                        continue
                    if not RE_KEBAB.match(d):
                        self.add("name-dir", "yellow", cat, f"{rel_dir}/{d}",
                                 f"目录名不符合 kebab-case: {d}",
                                 "重命名为小写+连字符（如 my-project）")
                for fn in filenames:
                    if fn.startswith(".") or fn in NAME_EXEMPT or has_cjk(fn):
                        continue
                    p = Path(fn)
                    if p.suffix.lower() == ".md":
                        if not RE_KEBAB.match(fn):
                            self.add("name-md", "yellow", cat, f"{rel_dir}/{fn}",
                                     f"md 文件名不符合 kebab-case: {fn}",
                                     "重命名为小写+连字符（如 project-overview.md）")
                    elif p.suffix.lower() == ".py":
                        if not RE_SNAKE.match(fn):
                            self.add("name-py", "yellow", cat, f"{rel_dir}/{fn}",
                                     f"Python 文件名不符合 snake_case: {fn}",
                                     "重命名为小写+下划线（如 parse_data.py）")
                    elif p.suffix.lower() in (".js", ".ts", ".jsx", ".tsx"):
                        if not RE_CAMEL.match(fn):
                            self.add("name-js", "yellow", cat, f"{rel_dir}/{fn}",
                                     f"JS/TS 文件名不符合 camelCase: {fn}",
                                     "重命名为小驼峰（如 generateImage.js）")

    # ============ 2. 任务健康 ============
    def check_tasks(self):
        cat = "tasks"
        if not (self.root / "tasks").is_dir() and not (self.root / "projects").is_dir():
            self.skip(cat, "tasks/ 与 projects/ 均不存在（未装 initializer 或工作区为空）")
            return
        for area in ("tasks", "projects"):
            base = self.root / area
            if not base.is_dir():
                continue
            for child in sorted(base.iterdir()):
                if not child.is_dir() or is_system_dir(child.name):
                    continue
                pm = child / "PROGRESS.md"
                if not pm.exists():
                    self.add("task-orphan", "yellow", cat, f"{area}/{child.name}",
                             f"目录无 PROGRESS.md（目录即容器，进度卡缺失）",
                             "安装 xiaoyaoclaw-task-progress-tracker 补建进度卡")
                    continue
                # frontmatter status
                status = None
                try:
                    txt = pm.read_text(encoding="utf-8", errors="replace")
                    m = re.search(r"^status\s*:\s*(\S+)", txt, re.M)
                    if m:
                        status = m.group(1).strip().strip('"\'')
                except Exception:
                    txt = ""
                if status is None:
                    self.add("task-nostatus", "yellow", cat, f"{area}/{child.name}/PROGRESS.md",
                             "PROGRESS.md 缺少 status frontmatter",
                             "补充 status: active|done|archived|paused")
                elif status not in PROGRESS_STATUSES:
                    self.add("task-badstatus", "yellow", cat, f"{area}/{child.name}/PROGRESS.md",
                             f"status 非法: {status}",
                             f"改为 {sorted(PROGRESS_STATUSES)} 之一")
                # 超龄未完结
                age_days = (datetime.now(TZ) - datetime.fromtimestamp(pm.stat().st_mtime, TZ)).days
                if age_days > self.days and status not in ("done", "archived"):
                    self.add("task-stale", "yellow", cat, f"{area}/{child.name}",
                             f"进度卡 {age_days} 天未更新且未完结",
                             "更新 PROGRESS.md 或标记 done/archived")

    # ============ 3. 记忆健康 ============
    def check_memory(self):
        cat = "memory"
        mem_dir = self.root / "memory"
        if not mem_dir.is_dir():
            self.skip(cat, "memory/ 不存在")
            return
        logs = sorted(mem_dir.glob("20*.md"))
        if not logs:
            self.add("mem-nolog", "yellow", cat, "memory/",
                     "没有任何 YYYY-MM-DD.md 日志", "开始记录日常日志（memory-distill 可辅助）")
        else:
            latest = logs[-1]
            try:
                d = datetime.strptime(latest.stem, "%Y-%m-%d").replace(tzinfo=TZ)
                gap = (datetime.now(TZ) - d).days
                if gap > 7:
                    self.add("mem-gap", "yellow", cat, latest.name,
                             f"日志空窗 {gap} 天（最近: {latest.stem}）",
                             "补记最近动态，或确认确实无事发生")
            except ValueError:
                self.add("mem-badname", "yellow", cat, latest.name,
                         "日志文件名不是 YYYY-MM-DD.md 格式", "重命名日志文件")
        if not (self.root / "MEMORY.md").exists():
            self.add("mem-nomemory", "yellow", cat, "MEMORY.md",
                     "长期记忆 MEMORY.md 缺失", "用 xiaoyaoclaw-memory-distill 首次建忆")

    # ============ 4. 知识库健康 ============
    def check_knowledge(self):
        cat = "knowledge"
        kb = self.root / "knowledge"
        if not kb.is_dir():
            self.skip(cat, "knowledge/ 不存在（未装 initializer 或没有知识库）")
            return
        index = kb / "data_structure.md"
        index_txt = ""
        if index.exists():
            try:
                index_txt = index.read_text(encoding="utf-8", errors="replace")
            except Exception:
                index_txt = ""
        else:
            self.add("kb-noindex", "yellow", cat, "knowledge/",
                     "缺少 data_structure.md 分层索引（kb-retriever 检索入口）",
                     "安装 xiaoyaoclaw-kb-retriever 并用 build_index.py 生成索引")

        files = walk_files(kb)
        root_files = []
        for rel in files:
            if rel == "data_structure.md":
                continue  # 索引文件自身：不参与孤儿/散文件/类型检查
            # 根目录散文件
            if "/" not in rel:
                root_files.append(rel)
            # 类型支持（始终检查，与索引是否存在无关）
            ext = Path(rel).suffix.lower()
            if ext and ext not in KB_SUPPORTED_EXTS:
                self.add("kb-unsupported", "yellow", cat, f"knowledge/{rel}",
                         f"类型 {ext} 不受 kb-retriever 支持（仅 md/pdf/xlsx）",
                         "转换为 md 或归档到其他位置")
            # 超大文件
            p = kb / rel
            try:
                mb = p.stat().st_size / (1024 * 1024)
                if mb > 20:
                    self.add("kb-huge", "yellow", cat, f"knowledge/{rel}",
                             f"文件 {mb:.1f}MB（>20MB，PDF 提取/检索变慢）",
                             "拆分或压缩该文件")
            except OSError:
                pass
            # 索引孤儿（宽松匹配：路径或其目录前缀出现在索引文本即命中）
            if index_txt:
                rel_lower = rel.lower()
                hit = rel_lower in index_txt.lower()
                if not hit:
                    prefix = rel.rsplit("/", 1)[0] if "/" in rel else ""
                    hit = bool(prefix) and prefix.lower() in index_txt.lower()
                if not hit:
                    self.add("kb-index-orphan", "yellow", cat, f"knowledge/{rel}",
                             "文件未出现在 data_structure.md 索引中（检索不到 = 知识黑洞）",
                             "运行 build_index.py 重建索引")
        if root_files:
            self.add("kb-rootfiles", "yellow", cat, "knowledge/",
                     f"{len(root_files)} 个文件散落在知识库根目录: {', '.join(root_files[:5])}",
                     "按主题归档到对应子目录")

    # ============ 5. 垃圾/临时 ============
    def check_junk(self):
        cat = "junk"
        tmp = self.root / "tmp"
        if tmp.is_dir():
            old = []
            for p in tmp.rglob("*"):
                if p.is_file():
                    try:
                        age = (datetime.now(TZ) - datetime.fromtimestamp(p.stat().st_mtime, TZ)).days
                        if age > self.days:
                            old.append((p.relative_to(tmp).as_posix(), age))
                    except OSError:
                        pass
            if old:
                shown = ", ".join(f"{n}({a}d)" for n, a in old[:5])
                more = f" 等 {len(old)} 个" if len(old) > 5 else ""
                self.add("junk-tmp-old", "yellow", cat, "tmp/",
                         f"tmp/ 下 {len(old)} 个文件超过 {self.days} 天: {shown}{more}",
                         "指挥官确认后手动清理（红线：不自动删除）")
        # 全工作区大文件
        big = []
        for dirpath, dirnames, filenames in os.walk(self.root):
            dirnames[:] = [d for d in dirnames if not is_system_dir(d)]
            for fn in filenames:
                try:
                    p = Path(dirpath) / fn
                    mb = p.stat().st_size / (1024 * 1024)
                    if mb > self.max_file_mb:
                        big.append((p.relative_to(self.root).as_posix(), round(mb, 1)))
                except OSError:
                    pass
        if big:
            shown = ", ".join(f"{n}({m}MB)" for n, m in big[:5])
            more = f" 等 {len(big)} 个" if len(big) > 5 else ""
            self.add("junk-bigfile", "yellow", cat, "",
                     f"超大文件（>{self.max_file_mb}MB）: {shown}{more}",
                     "确认是否仍需要，不需要则归档或删除")

    # ---- 运行 ----
    def run(self):
        self.check_dirs()
        self.check_tasks()
        self.check_memory()
        self.check_knowledge()
        self.check_junk()

    def summary(self):
        sev = {"red": 0, "yellow": 0, "green": 0}
        for f in self.findings:
            sev[f["severity"]] = sev.get(f["severity"], 0) + 1
        return {
            "red": sev["red"], "yellow": sev["yellow"], "green": sev["green"],
            "skipped": len(self.skipped),
        }

    def to_json(self):
        return {
            "tool": "workspace-auditor",
            "version": VERSION,
            "workspace": str(self.root),
            "scanned_at": now_str(),
            "summary": self.summary(),
            "skipped": self.skipped,
            "findings": self.findings,
        }

    def to_markdown(self):
        s = self.summary()
        lines = [
            f"# 工作区体检报告",
            f"",
            f"- 工作区: `{self.root}`",
            f"- 扫描时间: {now_str()}",
            f"- 工具: workspace-auditor v{VERSION}",
            f"",
            f"## 总结",
            f"",
            f"| 级别 | 数量 |",
            f"|------|------|",
            f"| 🔴 违规 | {s['red']} |",
            f"| 🟡 警告 | {s['yellow']} |",
            f"| 🟢 正常 | {s['green']} |",
            f"| ⏭️ 降级跳过 | {s['skipped']} |",
            f"",
        ]
        if self.skipped:
            lines.append("## 降级提示（依赖缺失）")
            lines.append("")
            for sk in self.skipped:
                lines.append(f"- **{sk['category']}**: {sk['reason']}")
            lines.append("")
        if self.findings:
            lines.append("## 明细")
            lines.append("")
            sev_icon = {"red": "🔴", "yellow": "🟡", "green": "🟢"}
            cat_name = {"dirs": "目录合规", "tasks": "任务健康", "memory": "记忆健康",
                        "knowledge": "知识库健康", "junk": "垃圾/临时"}
            for f in sorted(self.findings, key=lambda x: (x["severity"] != "red", x["category"])):
                icon = sev_icon.get(f["severity"], "•")
                loc = f" `{f['path']}`" if f["path"] else ""
                lines.append(f"{icon} **[{cat_name.get(f['category'], f['category'])}]**{loc}")
                lines.append(f"   {f['message']}")
                if f["fix"]:
                    lines.append(f"   💡 {f['fix']}")
                lines.append("")
        else:
            lines.append("## 明细")
            lines.append("")
            lines.append("🎉 未发现问题，工作区很健康。")
            lines.append("")
        lines.append("---")
        lines.append("_只读体检，不修改任何文件。修复请按建议人工确认后执行。_")
        return "\n".join(lines)


# ---------------------------------------------------------------- main

def main():
    # Windows 控制台默认 GBK，强制 UTF-8 输出（中文 + emoji 兼容）
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="OpenClaw Workspace Auditor - 工作区体检")
    ap.add_argument("--root", help="工作区根目录（默认: 从 cwd 向上找 WORKSPACE.md）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--report", action="store_true", help="输出 Markdown 报告（默认）")
    ap.add_argument("--days", type=int, default=30, help="超龄阈值天数（默认 30）")
    ap.add_argument("--max-file", type=int, default=50, help="大文件阈值 MB（默认 50）")
    args = ap.parse_args()

    root = Path(args.root).resolve() if args.root else find_workspace_root(Path.cwd())
    if not root.is_dir():
        print(f"错误: 目录不存在 {root}", file=sys.stderr)
        sys.exit(2)

    auditor = Auditor(root, args.days, args.max_file)
    auditor.run()

    if args.json:
        print(json.dumps(auditor.to_json(), ensure_ascii=False, indent=2))
    else:
        print(auditor.to_markdown())
    sys.exit(0)


if __name__ == "__main__":
    main()
