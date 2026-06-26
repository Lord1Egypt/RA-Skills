"""
self_checker.py
===============
对生成的图片进行逻辑一致性校验。

主要功能：
  check_figure_logical_consistency(fig_path, paper_text, figure_type)
    1. OCR 提取文字（优先级: rapidocr离线 > easyocr联网 > pytesseract）
    2. 检查占位符文字
    3. 检查关键词匹配（论文 vs 图片）
    4. 检查结构完整性（5种图类型）
    5. 检查分辨率/宽高比
    6. 返回 (passed, issues, ocr_text, warnings)
"""

import os, re

# ── OCR 引擎检测 ────────────────────────────────────────
HAS_PIL = False
HAS_TESSERACT = False
HAS_RAPIDOCR = False
HAS_EASYOCR = False

try:
    import PIL.Image
    HAS_PIL = True
except ImportError:
    pass

try:
    import pytesseract
    HAS_TESSERACT = True
except ImportError:
    pass

try:
    import rapidocr_onnxruntime
    HAS_RAPIDOCR = True
except ImportError:
    pass

try:
    import easyocr
    HAS_EASYOCR = True
except ImportError:
    pass

# lazy-load OCR readers（避免启动时就下载模型）
_rapid_reader = None
_easy_reader  = None

def _get_rapidocr():
    global _rapid_reader
    if _rapid_reader is None:
        from rapidocr_onnxruntime import RapidOCR
        _rapid_reader = RapidOCR()
    return _rapid_reader

def _get_easyocr():
    global _easy_reader
    if _easy_reader is None:
        import easyocr as _eo
        _easy_reader = _eo.Reader(["en", "zh_cn"], gpu=True, verbose=False)
    return _easy_reader


# ─────────────────────────────────────────────────────────
# 内部辅助函数
# ─────────────────────────────────────────────────────────
def _extract_keywords(text: str, top_n: int = 20) -> list[str]:
    stop_words = {
        "的", "是", "在", "和", "了", "我们", "方法", "本文", "该",
        "a", "an", "the", "is", "are", "and", "or", "of", "to", "in",
        "for", "with", "on", "that", "this", "as", "by", "from",
        "等人", "数据", "模型", "结果", "实验",
    }
    words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]{3,}', text)
    freq = {}
    for w in words:
        w = w.lower()
        if w not in stop_words and len(w) >= 2:
            freq[w] = freq.get(w, 0) + 1
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [w for w, _ in sorted_words[:top_n]]

def _check_architecture(fig_path: str, ocr_text: str) -> list[str]:
    issues = []
    expected = ["encoder", "image", "text", "loss", "encode", "学生", "冻结",
                "frozen", "student", "teacher", "distillation", "编码", "编码器"]
    found = sum(1 for m in expected if m.lower() in ocr_text.lower())
    if found < 3:
        issues.append("架构图中未发现足够的结构关键词（encoder/text/loss/teacher/student），结构可能不符合预期")
    return issues

def _check_line_chart(fig_path: str, ocr_text: str) -> list[str]:
    issues = []
    expected = ["%", "accuracy", "精度", "data", "数据", "clip", "declip", "12m", "88m",
                "imagenet", "top-1", "top1", "zero-shot"]
    found = sum(1 for m in expected if m.lower() in ocr_text.lower())
    if found < 2:
        issues.append("折线图中未发现坐标轴或数据标注，图表结构可能不完整")
    return issues

def _check_bar_chart(fig_path: str, ocr_text: str) -> list[str]:
    issues = []
    expected = ["%", "accuracy", "精度", "dataset", "clip", "declip", "transfer",
                "linear", "probe", "linear probe", "downstream"]
    found = sum(1 for m in expected if m.lower() in ocr_text.lower())
    if found < 2:
        issues.append("柱状图中未发现足够的数据集或指标标注，结构可能不完整")
    return issues

def _check_multipanel(fig_path: str, ocr_text: str) -> list[str]:
    issues = []
    expected = ["(a)", "(b)", "(c)", "a)", "b)", "c)", "fig", "fig.", "ss",
                "mvs", "nns", "self", "supervision", "multi", "nearest",
                "neighbor", "panel", "ablation"]
    found = sum(1 for m in expected if m.lower() in ocr_text.lower())
    if found < 2:
        issues.append("多面板图中未发现面板标记（如 (a)(b)(c)），结构可能不完整")
    return issues

def _check_table_chart(fig_path: str, ocr_text: str) -> list[str]:
    issues = []
    expected = ["ablation", "ss", "mvs", "nns", "loss", "losses",
                "消融", "监督", "supervision", "self-supervision"]
    found = sum(1 for m in expected if m.lower() in ocr_text.lower())
    if found < 1:
        issues.append("消融图中未发现监督信号相关关键词，结构可能偏离预期")
    return issues


# ─────────────────────────────────────────────────────────
# 核心校验函数
# ─────────────────────────────────────────────────────────
def check_figure_logical_consistency(
    figure_path: str,
    paper_text: str = "",
    figure_type: str = "",
) -> dict:
    issues  = []
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

    # ── 1. OCR 提取文字（三级降级链）────────────────
    # 优先级：rapidocr离线 > easyocr联网 > pytesseract
    ocr_success = False
    if HAS_PIL:
        # ── rapidocr（离线，自带 ONNX 模型）───────────
        if HAS_RAPIDOCR:
            try:
                reader = _get_rapidocr()
                # rapidocr 返回 (boxes_and_texts, metadata)，都是 list
                ocr_result, _ = reader(figure_path)
                if ocr_result:
                    ocr_text = " ".join(
                        item[1].strip() for item in ocr_result if item[1].strip()
                    ).strip()
                    ocr_success = True
            except Exception as e:
                warnings.append(f"rapidocr 失败：{e}，降级至备选引擎")
                ocr_text = ""

        # ── pytesseract（需要 Tesseract OCR 引擎）─────
        if not ocr_success and HAS_TESSERACT:
            try:
                import PIL.Image
                img = PIL.Image.open(figure_path)
                ocr_text = pytesseract.image_to_string(img, lang="eng+chi").strip()
                ocr_success = True
            except Exception:
                warnings.append("pytesseract 引擎不可用（请安装 Tesseract OCR）")
                ocr_text = ""

        # ── easyocr（联网下载模型）────────────────────
        if not ocr_success and HAS_EASYOCR:
            try:
                reader = _get_easyocr()
                result = reader.readtext(figure_path)
                ocr_text = " ".join(t.strip() for _, t, _ in result if t.strip()).strip()
                ocr_success = True
            except Exception as e:
                warnings.append(f"easyocr 也失败：{e}，跳过文字校验")

        if not ocr_success and not HAS_RAPIDOCR and not HAS_EASYOCR and not HAS_TESSERACT:
            warnings.append("未安装任何 OCR 引擎（rapidocr/pytesseract/easyocr），跳过文字校验")
    else:
        warnings.append("未安装 Pillow，跳过 OCR 校验")

    # ── 2. 占位符文字检查 ────────────────────────────
    for phrase in ["placeholder", "lorem ipsum", "todo", "tbd",
                   "undefined", "null", "xxx", "image placeholder"]:
        if phrase.lower() in ocr_text.lower():
            issues.append(f"检测到占位符文字（{phrase}），图片可能未正确生成完整内容")

    # ── 3. 关键词匹配 ─────────────────────────────────
    if paper_text and ocr_text:
        kws     = _extract_keywords(paper_text)
        missing = [kw for kw in kws if kw.lower() not in ocr_text.lower()]
        critical = [kw for kw in kws if len(kw) > 3]
        if missing and len(missing) > len(critical) * 0.7:
            warnings.append(
                f"图片中未发现论文关键概念词：{missing[:5]}，内容可能偏离主题"
            )

    # ── 4. 结构类型校验 ───────────────────────────────
    checkers = {
        "架构图":      _check_architecture,
        "对比折线图":  _check_line_chart,
        "折线图":      _check_line_chart,
        "对比柱状图":  _check_bar_chart,
        "多面板图":    _check_multipanel,
        "消融图/表格": _check_table_chart,
    }
    checker = checkers.get(figure_type)
    if checker and ocr_text:
        try:
            issues.extend(checker(figure_path, ocr_text))
        except Exception as e:
            warnings.append(f"结构校验出错：{e}")

    # ── 5. 分辨率/尺寸校验 ────────────────────────────
    if HAS_PIL:
        try:
            import PIL.Image
            img = PIL.Image.open(figure_path)
            w, h = img.size
            if w < 512 or h < 256:
                warnings.append(f"图片分辨率较低（{w}x{h}），建议重新生成更高分辨率")
            ratio = w / h if h > 0 else 1
            if ratio > 5:
                warnings.append(f"图片宽高比异常（{ratio:.1f}:1），结构可能被压缩变形")
        except Exception as e:
            warnings.append(f"尺寸校验失败：{e}")

    passed = len(issues) == 0
    return {
        "passed":   passed,
        "issues":   issues,
        "ocr_text": ocr_text,
        "warnings": warnings,
    }


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
    result   = check_figure_logical_consistency(fig_path, "", fig_type)
    print(f"passed : {result['passed']}")
    print(f"issues : {result['issues']}")
    print(f"warnings: {result['warnings']}")
    if result["ocr_text"]:
        print(f"\nOCR text (first 400 chars):\n{result['ocr_text'][:400]}")
