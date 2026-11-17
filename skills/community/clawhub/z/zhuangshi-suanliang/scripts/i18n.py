#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""海外适配轻量层：CLI --lang en|zh 双语文本与 JSON 字段（纯标准库）。

设计目标（轻量层，不改业务算法）：
- 主 CLI 增加 ``--lang en|zh``（默认 zh，不破坏现有中文用户）。
- ``--lang en --help`` 输出英文 help；``--lang zh`` 输出保持原样。
- JSON 输出的 status/message/error 字段可按 lang 本地化（status 值固定 ok/error）。
- ascii/stdout 下 en 文本不出现中文。

用法：
    raw = sys.argv[1:]
    lang = i18n.argv_lang(raw)          # 预扫描，决定 parser 用哪套 help
    i18n.add_lang_arg(parser, default=lang)
    args = parser.parse_args(raw)
    g = i18n.I18N(args.lang)
    print(g.msg("ok"))                  # "完成"/"done"
    print(g.json(status="ok", message=g.msg("ok")))
"""

try:
    import os as _boot_os, sys as _boot_sys
    _boot_here = _boot_os.path.dirname(_boot_os.path.abspath(__file__))
    if _boot_here not in _boot_sys.path:
        _boot_sys.path.insert(0, _boot_here)
except Exception:
    pass


def argv_lang(argv):
    """从命令行预扫描 ``--lang en|zh``（帮助文本必须在解析前决定语言）。"""
    lang = "zh"
    try:
        for i, item in enumerate(argv):
            if item == "--lang":
                if i + 1 < len(argv) and argv[i + 1] in ("en", "zh"):
                    lang = argv[i + 1]
                break
            if item.startswith("--lang="):
                val = item.split("=", 1)[1]
                if val in ("en", "zh"):
                    lang = val
                break
    except Exception:
        pass
    return lang


def add_lang_arg(parser, default="zh"):
    lang = default if default in ("zh", "en") else "zh"
    help_ = (
        "Output language: en English, zh Chinese (pass --lang en before --help to see English help)"
        if lang == "en"
        else "输出语言：zh 中文（默认），en English"
    )
    parser.add_argument(
        "--lang",
        choices=("zh", "en"),
        default=default,
        help=help_,
    )


_TEXTS = {
    # key -> (zh, en)
    "ok": ("完成", "done"),
    "error": ("错误", "error"),
    "not_found": ("未找到", "not found"),
    "written": ("已写入", "written"),
    "skipped": ("已跳过", "skipped"),
    "warning": ("警告", "warning"),
    "version": ("版本", "version"),
    "skill_version": ("技能版本", "skill version"),
    "output_dir": ("输出目录", "output directory"),
    "input_file": ("输入文件", "input file"),
    "processing": ("处理中", "processing"),
    "scan_done": ("扫描完成", "scan completed"),
    "regenerated": ("已完成复算", "recomputed"),
    "audit_done": ("审计完成", "audit completed"),
    "self_test_ok": ("自测通过", "self-test passed"),
    "usage_hint": ("使用 --help 查看完整用法", "run with --help for full usage"),
    "privacy_note": ("本工具本机运行，不上传图纸/文档字节", "runs locally; drawing/document bytes never leave your machine"),
    "lang_title_en": ("English", "English"),
    "lang_title_zh": ("中文", "中文"),
}

_FIELDS = {
    "ok": "ok",
    "error": "error",
    "warning": "warning",
    "skipped": "skipped",
}

_EXTRA_SKILL = {
    "skill_name": ("技能", "skill"),
    "cli": ("命令行", "CLI"),
}


def T(lang, key, **kw):
    """取双语文本：key 不存在时回退英文 key 本身；kw 支持 {k} 占位。"""
    table = _TEXTS if key in _TEXTS else _EXTRA_SKILL
    pair = table.get(key, (key, key))
    text = pair[1] if lang == "en" else pair[0]
    if kw:
        try:
            return text.format(**kw)
        except Exception:
            return text
    return text


def field(lang, key):
    """JSON 字段值：status 等语义字段固定英文 ok/error/warning；message 类按语言。"""
    if key in _FIELDS:
        return _FIELDS[key]
    return T(lang, key)


def json_result(lang, status="ok", message=None, error=None, **extra):
    """构造本地化 JSON：status 固定英文；message/error 由调用方传入已本地化文本。"""
    data = {"status": field(lang, status or "ok")}
    if message is not None:
        data["message"] = message
    if error is not None:
        data["error"] = error
    data.update(extra)
    return data
