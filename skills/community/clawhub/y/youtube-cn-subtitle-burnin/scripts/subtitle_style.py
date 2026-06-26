#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SubtitleStyle:
    name: str
    font: str
    zh_size: int
    en_size: int
    zh_margin_v: int
    en_margin_v: int
    outline: int
    shadow: int
    margin_l: int
    margin_r: int
    max_width: float
    font_scale: float
    bottom_margin: float
    stroke_width: int


STYLE_VERSION = "subtitle-style-v1"

STYLES: dict[str, SubtitleStyle] = {
    "zh-only-default": SubtitleStyle(
        name="zh-only-default",
        font="PingFang SC",
        zh_size=46,
        en_size=0,
        zh_margin_v=58,
        en_margin_v=0,
        outline=5,
        shadow=1,
        margin_l=64,
        margin_r=64,
        max_width=0.88,
        font_scale=0.061,
        bottom_margin=0.025,
        stroke_width=3,
    ),
    "zh-only-raised": SubtitleStyle(
        name="zh-only-raised",
        font="PingFang SC",
        zh_size=46,
        en_size=0,
        zh_margin_v=120,
        en_margin_v=0,
        outline=5,
        shadow=1,
        margin_l=64,
        margin_r=64,
        max_width=0.88,
        font_scale=0.061,
        bottom_margin=0.11,
        stroke_width=3,
    ),
    "bilingual-default": SubtitleStyle(
        name="bilingual-default",
        font="PingFang SC",
        zh_size=35,
        en_size=19,
        zh_margin_v=86,
        en_margin_v=46,
        outline=5,
        shadow=1,
        margin_l=64,
        margin_r=64,
        max_width=0.88,
        font_scale=0.061,
        bottom_margin=0.025,
        stroke_width=3,
    ),
    "bilingual-raised": SubtitleStyle(
        name="bilingual-raised",
        font="PingFang SC",
        zh_size=35,
        en_size=19,
        zh_margin_v=135,
        en_margin_v=95,
        outline=5,
        shadow=1,
        margin_l=64,
        margin_r=64,
        max_width=0.88,
        font_scale=0.061,
        bottom_margin=0.095,
        stroke_width=3,
    ),
}


def style_names() -> tuple[str, ...]:
    return tuple(STYLES)


def get_style(name: str) -> SubtitleStyle:
    try:
        return STYLES[name]
    except KeyError as exc:
        raise ValueError(f"unknown subtitle style profile: {name}") from exc


def ass_style_line(style_name: str, ass_name: str = "Default") -> str:
    style = get_style(style_name)
    size = style.zh_size if not ass_name.lower().startswith("english") else style.en_size
    margin_l = style.margin_l if not ass_name.lower().startswith("english") else 80
    margin_r = style.margin_r if not ass_name.lower().startswith("english") else 80
    margin_v = style.zh_margin_v if not ass_name.lower().startswith("english") else style.en_margin_v
    bold = "-1" if not ass_name.lower().startswith("english") else "0"
    outline = style.outline if not ass_name.lower().startswith("english") else max(3, style.outline - 1)
    return (
        f"Style: {ass_name},{style.font},{size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,"
        f"{bold},0,0,0,100,100,0,0,1,{outline},{style.shadow},2,{margin_l},{margin_r},{margin_v},1"
    )
