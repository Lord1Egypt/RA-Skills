#!/usr/bin/env python3
"""Stable user-facing error codes for yotta-resume."""

ERROR_CATALOG = {
    "YRS-INPUT-001": {
        "title": "输入文件不存在",
        "impact": "无法读取简历或 JD，分析、导出或面试未开始。",
        "next_action": "检查文件路径后重试；无法找到原文件时可用 --resume-text - 粘贴正文。",
    },
    "YRS-INPUT-002": {
        "title": "输入内容无法解析",
        "impact": "当前文件不能形成可靠的文本输入，本次命令未生成结果。",
        "next_action": "改用 UTF-8 Markdown、DOCX 或文字层 PDF；特殊来源可复制正文并用 --resume-text -。",
    },
    "YRS-INPUT-003": {
        "title": "旧版文件格式不受支持",
        "impact": "无法直接读取旧版 .doc 或类似二进制文档，本次分析未开始。",
        "next_action": "另存为 .docx / PDF / Markdown，或复制正文并用 --resume-text - 从 stdin 读取。",
    },
    "YRS-PDF-001": {
        "title": "未找到可用 PDF 浏览器",
        "impact": "DOCX / HTML 不受影响；当前环境不能导出 PDF。",
        "next_action": "安装 Chromium、Chrome 或 Edge 后重试，或继续使用 DOCX / HTML。",
    },
    "YRS-PDF-002": {
        "title": "PDF 渲染失败",
        "impact": "本次 PDF 未生成；事务化导出不会留下半成品。",
        "next_action": "关闭占用浏览器进程后重试；仍失败时改用 DOCX / HTML 并保留完整错误信息。",
    },
    "YRS-EXPORT-001": {
        "title": "导出参数无效",
        "impact": "尚未写入任何成品文件。",
        "next_action": "至少指定一种输出格式，并确保不同格式使用不同文件路径。",
    },
    "YRS-EXPORT-002": {
        "title": "导出写入失败",
        "impact": "本次事务未完成，已有同名文件会被保留。",
        "next_action": "检查目标目录权限、磁盘空间和文件占用情况后重试。",
    },
    "YRS-EXPORT-003": {
        "title": "行动包目录不可覆盖",
        "impact": "目标目录已有内容，本次行动包未写入，原有文件保持不变。",
        "next_action": "改用新的 --out-dir；确认旧内容不再需要时再手动清理空目录。",
    },
    "YRS-EXPORT-004": {
        "title": "输出路径与输入冲突",
        "impact": "为避免覆盖原始简历或 JD，本次结果未写入，输入文件保持不变。",
        "next_action": "另选一个与输入文件不同的新 --out 路径后重试。",
    },
    "YRS-DATA-001": {
        "title": "随包数据契约校验失败",
        "impact": "题库、岗位映射或数据契约不可信，当前安装副本不应继续用于正式分析。",
        "next_action": "重新安装正式包；若问题持续，保留错误输出并提交缺陷。",
    },
    "YRS-DATA-002": {
        "title": "随包数据不可用",
        "impact": "行业识别或分析依赖的数据文件无法读取，本次命令未完成。",
        "next_action": "检查安装是否完整，重新安装正式包后重试。",
    },
    "YRS-INTERVIEW-001": {
        "title": "模拟面试输入或状态无效",
        "impact": "会话未继续推进，已有会话文件不会被静默覆盖。",
        "next_action": "按提示修正岗位族、职级、回答或会话文件后重试。",
    },
    "YRS-INTERVIEW-002": {
        "title": "模拟面试会话已存在",
        "impact": "为避免覆盖上次进度，本次 start 未写入会话。",
        "next_action": "使用新的 --session 路径；确认不再需要旧进度时才追加 --force。",
    },
    "YRS-ENV-001": {
        "title": "本地临时目录不可用",
        "impact": "分析或事务化导出无法安全暂存文件。",
        "next_action": "检查临时目录权限和磁盘空间，设置可写的 TEMP / TMP 后重试。",
    },
    "YRS-SELFTEST-001": {
        "title": "随包自检未通过",
        "impact": "至少一个核心检查失败，当前安装副本需要修复后再使用。",
        "next_action": "查看失败检查的影响与下一步，重新安装正式包后再次运行 selftest。",
    },
}


def error_details(code):
    """Return immutable metadata for one stable error code."""
    try:
        return dict(ERROR_CATALOG[code])
    except KeyError as error:
        raise ValueError("unknown error code: {}".format(code)) from error


def format_controlled_error(code, detail=None):
    """Render a stable, copyable error with impact and next action."""
    metadata = error_details(code)
    message = detail or metadata["title"]
    return (
        "[{code}] {message}\n"
        "影响：{impact}\n"
        "下一步：{next_action}"
    ).format(
        code=code,
        message=message,
        impact=metadata["impact"],
        next_action=metadata["next_action"],
    )
