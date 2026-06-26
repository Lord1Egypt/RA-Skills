"""
self_checker.py
===============
对生成的图片进行逻辑一致性校验。

主要功能：
  check_figure_logical_consistency(fig_path, paper_text, figure_type)
    1. 用 OCR 提取图片中的可见文字
    2. 检查文字内容是否与预期主题/关键词匹配
    3. 检查结构是否符合预期（通过分析图片特征）
    4. 返回 (passed: bool, issues: list[str])
"""

import os, io
from pathlib import Path

try:
    import pytesseract
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


def check_figure_logical_consistency(
    figure_path: str,
    paper_text: str = "",
    figure_type: str = "",
) -> dict:
    """
    校验图片逻辑一致性。

    参数：
      figure_path : str，生成的图片路径
      paper_text  : str，论文原文（用于关键词比对）
      figure_type : str，图类型（architecture/chart/multi-panel 等）

    返回：
      {
        "passed": bool,
        "issues": list[str],   # 如果 passed=False，列出具体问题
        "ocr_text": str,       # OCR 提取的文字（用于调试）
        "warnings": list[str], # 警告（不影响通过，但值得关注）
      }
    """
    issues = []
    warnings = []
    ocr_text = ""

    # ── 0. 文件存在性 ─────────────────────────────────
    if not os.path.exists(figure_path):
        issues.append(f"图片文件不存在：{figure_path}")
        return {"passed": False, "issues": issues, "ocr_text": "", "warnings": warnings}

    file_size = os.path.getsize(figure_path)
    if file_size < 5000:
        issues.append(f"图片文件过小（{file_size} bytes），可能是损坏或生成失败")
        return {"passed": False, "issues": issues, "ocr_text": "", "warnings": warnings}

    # ── 1. OCR 提取文字 ───────────────────────────────
    if HAS_PIL and HAS_TESSERACT:
        try:
            img = Image.open(figure_path)
            ocr_text = pytesseract.image_to_string(img, lang="eng+chi")
            ocr_text = ocr_text.strip()
        except Exception as e:
            warnings.append(f"OCR 提取失败：{e}，跳过文字校验")
    else:
        warnings.append("未安装 pytesseract 或 Pillow，跳过 OCR 校验")

    # ── 2. 检查占位符文字 ─────────────────────────────
    placeholder_phrases = [
        "placeholder", "lorem ipsum", "todo", "tbd",
        "undefined", "null", "none", "xxx", "...",
        "image placeholder", "text here",
    ]
    for phrase in placeholder_phrases:
        if phrase.lower() in ocr_text.lower():
            issues.append(
                f"检测到占位符文字「{phrase}」，图片可能未正确生成完整内容"
            )

    # ── 3. 关键词匹配校验 ─────────────────────────────
    if paper_text:
        # 从论文中提取关键概念词
        important_keywords = _extract_keywords(paper_text)
        ocr_lower = ocr_text.lower()

        missing_keywords = [
            kw for kw in important_keywords
            if kw.lower() not in ocr_lower
        ]
        # 容错：只对高频关键词做校验
        critical_kws = [kw for kw in important_keywords if len(kw) > 3]
        if missing_keywords and len(missing_keywords) > len(critical_kws) * 0.7:
            warnings.append(
                f"图片中未发现论文关键概念词：{missing_keywords[:5]}，"
                "内容可能偏离主题"
            )

    # ── 4. 结构类型校验 ───────────────────────────────
    type_checks = {
        "architecture":  _check_architecture,
        "对比折线图":     _check_line_chart,
        "对比柱状图":     _check_bar_chart,
        "多面板图":       _check_multipanel,
        "消融图/表格":    _check_table_chart,
    }

    checker = type_checks.get(figure_type)
    if checker and HAS_PIL and HAS_TESSERACT:
        try:
            type_issues = checker(figure_path, ocr_text)
            issues.extend(type_issues)
        except Exception as e:
            warnings.append(f"结构校验出错：{e}")

    # ── 5. 分辨率/尺寸校验 ─────────────────────────────
    if HAS_PIL:
        try:
            img = Image.open(figure_path)
            w, h = img.size
            if w < 512 or h < 256:
                warnings.append(
                    f"图片分辨率较低（{w}x{h}），建议重新生成更高分辨率版本"
                )
            aspect = w / h if h > 0 else 1
            if aspect > 5:
                warnings.append(
                    f"图片宽高比异常（{aspect:.1f}:1），结构可能被压缩变形"
                )
        except Exception as e:
            warnings.append(f"尺寸校验失败：{e}")

    passed = len(issues) == 0
    return {
        "passed": passed,
        "issues": issues,
        "ocr_text": ocr_text,
        "warnings": warnings,
    }


# ─────────────────────────────────────────────────────────
# 内部辅助函数
# ─────────────────────────────────────────────────────────

def _extract_keywords(text: str, top_n: int = 20) -> list[str]:
    """从论文文本中提取高频实词关键词"""
    # 简单的停用词过滤
    stop_words = {
        "的", "是", "在", "和", "了", "我们", "方法", "本文", "该",
        "a", "an", "the", "is", "are", "and", "or", "of", "to", "in",
        "for", "with", "on", "that", "this", "as", "by", "from",
    }
    import re
    words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]{3,}', text)
    freq = {}
    for w in words:
        w = w.lower()
        if w not in stop_words and len(w) >= 2:
            freq[w] = freq.get(w, 0) + 1

    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [w for w, _ in sorted_words[:top_n]]


def _check_architecture(fig_path: str, ocr_text: str) -> list[str]:
    """校验架构图：检查是否包含编码器、损失函数等关键模块名"""
    issues = []
    expected_modules = ["encoder", "image", "text", "loss", "encode", "编码"]
    found = sum(1 for m in expected_modules if m.lower() in ocr_text.lower())
    if found < 2:
        issues.append(
            "架构图中未发现足够的结构关键词（如 encoder/text/loss），"
            "结构可能不符合预期"
        )
    return issues


def _check_line_chart(fig_path: str, ocr_text: str) -> list[str]:
    """校验折线图：检查是否有坐标轴标注、数据点"""
    issues = []
    expected = ["%", "accuracy", "精度", "data", "数据", "x", "y"]
    found = sum(1 for m in expected if m.lower() in ocr_text.lower())
    if found < 2:
        issues.append(
            "折线图中未发现坐标轴或数据标注，图表结构可能不完整"
        )
    return issues


def _check_bar_chart(fig_path: str, ocr_text: str) -> list[str]:
    """校验柱状图"""
    issues = []
    expected = ["%", "accuracy", "精度", "dataset", "数据集", "bar"]
    found = sum(1 for m in expected if m.lower() in ocr_text.lower())
    if found < 2:
        issues.append(
            "柱状图中未发现足够的数据集或指标标注，结构可能不完整"
        )
    return issues


def _check_multipanel(fig_path: str, ocr_text: str) -> list[str]:
    """校验多面板图：检查是否有面板标记"""
    issues = []
    expected = ["(a)", "(b)", "(c)", "a)", "b)", "c)", "panel", "图"]
    found = sum(1 for m in expected if m.lower() in ocr_text.lower())
    if found < 2:
        issues.append(
            "多面板图中未发现面板标记（如 (a)(b)(c)），结构可能不完整"
        )
    return issues


def _check_table_chart(fig_path: str, ocr_text: str) -> list[str]:
    """校验消融表格"""
    issues = []
    expected = ["ablation", "ss", "mvs", "nns", "loss", "losses", "消融"]
    found = sum(1 for m in expected if m.lower() in ocr_text.lower())
    if found < 1:
        issues.append(
            "消融图中未发现监督信号相关关键词，结构可能偏离预期"
        )
    return issues


# ─────────────────────────────────────────────────────────
# 快速测试
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python self_checker.py <图片路径> [图类型]")
        sys.exit(1)

    fig_path = sys.argv[1]
    fig_type = sys.argv[2] if len(sys.argv) > 2 else ""

    result = check_figure_logical_consistency(fig_path, "", fig_type)
    print(f"\npassed: {result['passed']}")
    print(f"issues: {result['issues']}")
    print(f"warnings: {result['warnings']}")
    if result["ocr_text"]:
        print(f"\nOCR text (first 300 chars):\n{result['ocr_text'][:300]}")
