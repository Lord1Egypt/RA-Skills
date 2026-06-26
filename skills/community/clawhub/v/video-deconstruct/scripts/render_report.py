"""把模型 JSON 输出渲染成 markdown 报告。"""
from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape


def render(analysis: dict, video_name: str) -> str:
    template_dir = Path(__file__).resolve().parent.parent / "templates"
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(disabled_extensions=("j2",)),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    tmpl = env.get_template("report.md.j2")
    return tmpl.render(
        video_name=video_name,
        analysis=analysis,
    )
