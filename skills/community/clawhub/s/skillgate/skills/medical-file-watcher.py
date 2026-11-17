#!/usr/bin/env python3
"""
medical-file-watcher — 医械文档变化监控。
监控医械文档的变化，用户改了文档，自动提醒要重新检查。
LGD: 有籍（监控有记录）、有证（变化有证据）、有门禁（提醒要检查）。
"""
import json
from pathlib import Path
from datetime import datetime


def _log_path(docs_dir: str) -> Path:
    """Watch log lives INSIDE the monitored folder (never outside it)."""
    return Path(docs_dir) / ".medical-file-watcher-log.json"


def get_doc_modification_times(docs_dir: str = ".") -> dict:
    """获取所有医械文档的修改时间。"""
    mod_times = {}
    docs_path = Path(docs_dir)

    # 监控常见的医械文档格式
    for ext in ["*.md", "*.docx", "*.pdf"]:
        for doc_file in docs_path.glob(ext):
            mod_times[str(doc_file)] = doc_file.stat().st_mtime

    return mod_times


def check_for_changes(docs_dir: str = ".") -> dict:
    """检查有没有医械文档变化。"""
    current_times = get_doc_modification_times(docs_dir)

    # 加载上次的记录（日志文件在被监控目录内）
    last_times = _load_last_times(docs_dir)

    if not last_times:
        # 第一次运行，保存当前状态
        _save_last_times(current_times, docs_dir)
        return {
            "changed": False,
            "message": "第一次运行，记录了当前状态——下次改文档会提醒你"
        }

    # 对比
    changed_docs = []
    for filename, mod_time in current_times.items():
        if filename not in last_times or mod_time > last_times[filename]:
            changed_docs.append(filename)

    if changed_docs:
        # 更新记录（写回被监控目录内）
        _save_last_times(current_times, docs_dir)
        return {
            "changed": True,
            "changed_docs": changed_docs,
            "message": f"⚠️ 检测到 {len(changed_docs)} 个医械文档改了——建议重新检查"
        }

    return {"changed": False, "message": "没有检测到文档变化"}


def _load_last_times(docs_dir: str) -> dict:
    """加载上次的记录。"""
    log = _log_path(docs_dir)
    if not log.exists():
        return {}

    try:
        return json.loads(log.read_text(encoding="utf-8"))
    except:
        return {}


def _save_last_times(times: dict, docs_dir: str):
    """保存当前状态（仅写被监控目录内；拒绝符号链接重定向）。"""
    log = _log_path(docs_dir)
    if log.is_symlink() or log.is_junction():
        print("错误: 日志路径不能是符号链接/junction", file=sys.stderr)
        sys.exit(2)
    log.write_text(
        json.dumps(times, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def main():
    import sys
    docs_dir = sys.argv[1] if len(sys.argv) > 1 else "."

    print("=" * 60)
    print("(")
    print("  👀 医械文档变化监控")
    print("=" * 60)
    print(f"\n  监控目录: {docs_dir}")

    result = check_for_changes(docs_dir)

    print(f"\n  结果: {result['message']}")

    if result["changed"]:
        print(f"\n  改了的文档：")
        for doc in result["changed_docs"]:
            print(f"    - {doc}")
        print(f"\n  💡 建议: 跑一下技能链重新检查")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
