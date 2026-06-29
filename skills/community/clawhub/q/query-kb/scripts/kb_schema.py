from __future__ import annotations

COMMON_MODULE_VERSION = "paperkb-v3.0"

DOC_TYPES = {
    "paper": {"folder": "papers", "cn": "论文", "scored": True, "dated": False},
    "survey": {"folder": "surveys", "cn": "行业调研", "scored": True, "dated": False},
    "project": {"folder": "projects", "cn": "开源项目", "scored": True, "dated": False},
    "doc": {"folder": "docs_tech", "cn": "技术文档", "scored": True, "dated": False},
    "experiment": {"folder": "experiments", "cn": "实验记录", "scored": False, "dated": True},
    "meeting": {"folder": "meetings", "cn": "会议纪要", "scored": False, "dated": True},
    "codebase": {"folder": "codebases", "cn": "代码仓库总览", "scored": False, "dated": False},
    "note": {"folder": "notes", "cn": "个人笔记", "scored": False, "dated": True},
}

TEAM_EXTRA_DIRS = [
    "people",
    "projects/general",
    "imports",
    "onboarding",
    "reviews",
    "source_files/pdfs",
    "source_files/docs",
    "source_files/sheets",
    "source_files/text",
    "source_files/other",
]

PERSONAL_EXTRA_DIRS = [
    "imports",
    "notes",
    "reviews",
    "source_files/pdfs",
    "source_files/docs",
    "source_files/sheets",
    "source_files/text",
    "source_files/other",
]

PROJECT_FILES = {
    "index.md": "# General\n\n团队公共资料项目空间。\n",
    "timeline.md": "# Timeline\n\n",
    "decisions.md": "# Decisions\n\n",
    "open_questions.md": "# Open Questions\n\n",
    "people.md": "# People\n\n",
    "sources.md": "# Sources\n\n",
}


def summary_folders() -> list[str]:
    return [f"summaries/{meta['folder']}" for meta in DOC_TYPES.values()]


def resolve_type(value: str) -> str:
    if value in DOC_TYPES:
        return value
    for key, meta in DOC_TYPES.items():
        if value == meta["cn"]:
            return key
    return "doc"


def folder_of(type_key: str) -> str:
    return DOC_TYPES.get(resolve_type(type_key), DOC_TYPES["doc"])["folder"]
