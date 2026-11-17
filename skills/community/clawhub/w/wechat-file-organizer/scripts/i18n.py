#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
i18n — 微信文件自动归类（无头版）的语言包（简体中文 / English）

零依赖（仅标准库），与 GUI 版 wechat-file-organizer-gui 的 i18n.py 结构一致。

语言优先级：--lang > 环境变量 WFO_LANG / WECHAT_ORG_LANG > 系统语言自动判定。
"""
import locale
import os
import sys

LANGS = ["zh", "en"]
LANG_NAMES = {"zh": "简体中文", "en": "English"}

_ALIASES = {
    "zh": "zh", "zh_cn": "zh", "zh-hans": "zh", "zh-hans-cn": "zh",
    "zh_cn.utf8": "zh", "chinese": "zh", "cn": "zh", "中文": "zh",
    "en": "en", "en_us": "en", "en-us": "en", "en_gb": "en", "en-gb": "en",
    "en_us.utf8": "en", "english": "en",
}

_current = "zh"

# 分类内部 key 顺序（显示名走 cat_name）
CATEGORY_ORDER = ["documents", "images", "archives", "videos", "audio",
                  "others"]

STRINGS = {
    "app.desc": {
        "zh": "微信文件自动归类（零依赖，默认只读 dry-run，与 GUI 版扫描逻辑一致）",
        "en": "WeChat file organizer (zero dependencies, read-only dry-run by "
              "default; same scan logic as the GUI app)",
    },

    # ---------------- 命令行参数说明 ----------------
    "arg.source": {
        "zh": "微信根目录；默认自动探测本机所有微信目录（多账号合并）",
        "en": "WeChat root folder; by default all WeChat folders on this "
              "machine are detected and merged",
    },
    "arg.dest": {
        "zh": "归类输出目录；默认在 source 同级建 WeChatFiles_Organized",
        "en": "Output folder; defaults to WeChatFiles_Organized next to the "
              "source folder",
    },
    "arg.scheme": {
        "zh": "归类方式（默认 type：按类型）",
        "en": "Organization method (default: type)",
    },
    "arg.apply": {
        "zh": "真正复制归类（默认仅 dry-run 报告，不改动任何文件）",
        "en": "Actually copy and organize (default is a dry-run report, "
              "nothing is modified)",
    },
    "arg.trash": {
        "zh": "配合 --apply：复制成功后把源文件移入%s（可恢复），Linux 跳过",
        "en": "With --apply: after copying, move the originals to the %s "
              "(recoverable); skipped on Linux",
    },
    "arg.dedupe": {
        "zh": "去重：相同内容的文件只保留一份（配合 --apply 生效）",
        "en": "Deduplicate: keep one copy of identical files "
              "(needs --apply)",
    },
    "arg.include_media": {
        "zh": "连 Image/Video 里的 .dat 也处理（默认跳过）",
        "en": "Also handle .dat files under Image/Video (skipped by default)",
    },
    "arg.scan_all": {
        "zh": "扫描 FileStorage 全部子目录（含图片/视频/语音等）",
        "en": "Scan every FileStorage subfolder (images / video / voice, ...)",
    },
    "arg.top": {
        "zh": "报告里列出最大的前 N 个文件（默认 10，0 关闭）",
        "en": "List the N largest files in the report (default 10, 0 disables)",
    },
    "arg.old_days": {
        "zh": "超过该天数的文件计为“老旧”（默认 365）",
        "en": "Files older than this many days count as \"old\" (default 365)",
    },
    "arg.json": {
        "zh": "输出 JSON（便于脚本/定时任务消费）",
        "en": "Emit JSON (for scripts / scheduled tasks)",
    },
    "arg.lang": {
        "zh": "界面语言：zh / en（默认按系统语言自动判定）",
        "en": "Language: zh / en (defaults to the system language)",
    },

    # ---------------- 分类 ----------------
    "cat.documents": {"zh": "文档", "en": "Documents"},
    "cat.images": {"zh": "图片", "en": "Images"},
    "cat.archives": {"zh": "压缩包", "en": "Archives"},
    "cat.videos": {"zh": "视频", "en": "Videos"},
    "cat.audio": {"zh": "音频", "en": "Audio"},
    "cat.others": {"zh": "其他", "en": "Other"},

    # ---------------- 报告 ----------------
    "report.title": {"zh": "微信文件归类报告  (%s)", "en": "WeChat files report  (%s)"},
    "report.apply": {"zh": "APPLY 已执行", "en": "APPLY executed"},
    "report.dryrun": {"zh": "DRY-RUN 只读", "en": "DRY-RUN (read-only)"},
    "report.source": {"zh": "源目录", "en": "Source"},
    "report.multi_source": {
        "zh": "%d 个微信目录（已合并扫描）",
        "en": "%d WeChat folders (merged scan)",
    },
    "report.accounts": {"zh": "微信账号", "en": "Accounts"},
    "report.accounts_line": {
        "zh": "%s: %d 个（%s）", "en": "%s: %d (%s)",
    },
    "report.type_line": {
        "zh": "  %s  %5d 个  %s", "en": "  %s  %5d file(s)  %s",
    },
    "report.total_files": {"zh": "文件总数", "en": "Total files"},
    "report.total_size": {"zh": "总大小", "en": "Total size"},
    "report.by_type": {"zh": "按类型", "en": "By type"},
    "report.dup": {"zh": "重复文件", "en": "Duplicates"},
    "report.dup_line": {
        "zh": "%d 组, 重复文件 %d 个, 可节省 %s",
        "en": "%d groups, %d duplicate files, %s reclaimable",
    },
    "report.old": {"zh": "老旧文件", "en": "Old files"},
    "report.old_line": {
        "zh": "%d 个 (超过 %d 天)", "en": "%d files (older than %d days)",
    },
    "report.top": {"zh": "最大的 %d 个文件", "en": "Largest %d files"},
    "report.ok": {"zh": "[OK] 已归类到: %s", "en": "[OK] Organized into: %s"},
    "report.copied": {
        "zh": "      复制 %d 个文件%s", "en": "      Copied %d files%s",
    },
    "report.dedupe_skip": {
        "zh": "，去重跳过 %d 个", "en": ", %d skipped by dedupe",
    },
    "report.trashed": {
        "zh": "      移入%s %d 个（失败 %d 个）",
        "en": "      To the %s: %d moved, %d failed",
    },
    "report.dryrun_hint": {
        "zh": "[DRY-RUN] 未做任何改动。加 --apply 才真正复制归类。",
        "en": "[DRY-RUN] Nothing was changed. Add --apply to actually copy "
              "and organize.",
    },
    "warn.copy_failed": {
        "zh": "[WARN] 复制失败 %s: %s", "en": "[WARN] Copy failed %s: %s",
    },
    "warn.trash_failed": {
        "zh": "[WARN] 把 %s 移入%s失败: %s",
        "en": "[WARN] Couldn't move %s to the %s: %s",
    },

    # ---------------- 错误 / 空结果 ----------------
    "err.no_dir": {"zh": "找不到微信文件目录", "en": "WeChat folder not found"},
    "err.no_dir_hint": {
        "zh": "请用 --source 指定微信目录，或设置 WECHAT_FILES_DIR 环境变量",
        "en": "Pass --source /path/to/wechat, or set the WECHAT_FILES_DIR "
              "environment variable",
    },
    "err.no_dir_text": {
        "zh": "[FAIL] 找不到微信文件目录。请用 --source 指定，或设置 WECHAT_FILES_DIR。",
        "en": "[FAIL] WeChat folder not found. Use --source, or set "
              "WECHAT_FILES_DIR.",
    },
    "skip.none": {"zh": "未发现可归类的文件", "en": "No files to organize"},
    "skip.none_text": {
        "zh": "[SKIP] 未发现可归类的文件。", "en": "[SKIP] No files to organize.",
    },

    # ---------------- 通用 / 回收站 ----------------
    "unknown": {"zh": "未知", "en": "Unknown"},
    "list_sep": {"zh": "、", "en": ", "},
    "trash.win": {"zh": "回收站", "en": "Recycle Bin"},
    "trash.mac": {"zh": "废纸篓", "en": "Trash"},
    "trash.linux": {"zh": "废纸篓", "en": "Trash"},
    "trash.linux_skip": {
        "zh": "Linux 暂不支持移入%s，已跳过（未删除任何文件）",
        "en": "Moving to the %s isn't supported on Linux yet — skipped "
              "(nothing was deleted)",
    },
    "trash.mac_fail": {"zh": "移入%s失败: %s", "en": "Couldn't move to the %s: %s"},
    "trash.win_unavailable": {
        "zh": "无法调用系统%s，已跳过（未删除任何文件）",
        "en": "Can't call the system %s — skipped (nothing was deleted)",
    },
    "trash.still_exists": {
        "zh": "仍存在于磁盘 (rc=%r)", "en": "Still on disk (rc=%r)",
    },
}


def set_lang(code):
    global _current
    if normalize(code) in LANGS:
        _current = normalize(code)
    return _current


def get_lang():
    return _current


def normalize(code):
    if not code:
        return ""
    c = str(code).strip().lower().replace("-", "_")
    if c in _ALIASES:
        return _ALIASES[c]
    base = c.split("_")[0].split(".")[0]
    return _ALIASES.get(base, "")


def detect_lang():
    """按系统语言自动选择：中文环境 -> zh，其余已知英文环境 -> en，未知默认 zh。"""
    for var in ("WFO_LANG", "WECHAT_ORG_LANG"):
        code = normalize(os.environ.get(var, ""))
        if code:
            return code

    loc = ""
    try:
        loc, _ = locale.getdefaultlocale()
    except Exception:
        loc = ""
    loc = loc or os.environ.get("LC_ALL") or os.environ.get("LANG") or ""
    code = normalize(loc)
    if code:
        return code

    if sys.platform == "win32" or os.name == "nt":
        try:
            import ctypes
            lcid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            return "zh" if (lcid & 0x3FF) == 0x04 else "en"
        except Exception:
            pass

    if loc.lower().startswith("en"):
        return "en"
    return "zh"


def lang_from_argv(argv, default=None):
    """从命令行里先取出 --lang，好让 --help 也用对应语言显示。"""
    for i, a in enumerate(argv):
        if a == "--lang" and i + 1 < len(argv):
            code = normalize(argv[i + 1])
            if code:
                return code
        elif a.startswith("--lang="):
            code = normalize(a.split("=", 1)[1])
            if code:
                return code
    return default or detect_lang()


def t(key):
    entry = STRINGS.get(key)
    if not entry:
        return key
    return entry.get(_current) or entry.get("zh") or key


def cat_name(key):
    return t("cat." + key) if key in CATEGORY_ORDER else (key or t("unknown"))


def join_list(items):
    """按语言习惯拼接列表（中文用「、」，英文用 ", "）。"""
    return t("list_sep").join(str(i) for i in items)


def trash_label(platform):
    return t("trash." + platform)
