#!/usr/bin/env python3
"""
T2-01 + T2-02：OCR 引擎封装模块 image_ocr.py
封装 Tesseract / PaddleOCR / EasyOCR 三级 OCR 引擎，
提供统一的 OCR 调用接口和近音字纠错后处理。

功能：
- Tesseract CLI subprocess 封装（首选）
- PaddleOCR CLI 备选
- EasyOCR 兜底（Python import，需 venv 路径）
- OCR 可用性检查
- 超时 30s + 重试 1 次 + 失败降级
- 串行执行，不并发
- EMF 图片先转 PNG 再 OCR（复用 image_extract.py 的 convert_emf_to_png）
- 近音字纠错后处理（T2-02）
- 输出：OCR 纯文本 + 引擎类型 + 耗时 + 状态

依赖：subprocess（系统级 OCR CLI）
"""

import json
import os
import re
import sys
import time
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass, asdict


# ============================================================
# 常量
# ============================================================

# OCR 超时（秒）
OCR_TIMEOUT = 30

# 最大重试次数
MAX_RETRY = 1

# 纠错置信度下调值
CORRECTION_CONFIDENCE_PENALTY = 0.1

# OCR 引擎优先级
ENGINE_PRIORITY = ["tesseract", "paddleocr", "easyocr"]


# ============================================================
# 数据结构
# ============================================================

@dataclass
class OCRResult:
    """单张图片 OCR 结果"""
    image_id: str = ""              # 图片 ID
    image_path: str = ""            # 图片路径
    ocr_text: str = ""              # OCR 识别文本
    corrected_text: str = ""        # 纠错后文本（T2-02）
    engine: str = ""                # 使用的 OCR 引擎
    elapsed_seconds: float = 0.0    # 耗时
    status: str = "pending"         # ok / empty / timeout / failed / engine_unavailable
    error_message: str = ""         # 错误信息
    retry_count: int = 0            # 重试次数
    correction_applied: bool = False  # 是否应用了纠错
    correction_details: List[str] = None  # 纠错详情

    def __post_init__(self):
        if self.correction_details is None:
            self.correction_details = []

    def to_dict(self) -> dict:
        return asdict(self)


# ============================================================
# OCR 可用性检查（复用 model_detect.py 的逻辑，独立实现避免循环依赖）
# ============================================================

def check_ocr_engine(engine: str) -> Dict:
    """
    检查指定 OCR 引擎是否可用。

    Args:
        engine: tesseract / paddleocr / easyocr

    Returns:
        {"available": bool, "version": str, "error": str}
    """
    if engine == "tesseract":
        try:
            result = subprocess.run(
                ['tesseract', '--version'],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                version = result.stdout.strip().split('\n')[0] if result.stdout else \
                          result.stderr.strip().split('\n')[0]
                return {"available": True, "version": version, "error": ""}
        except (FileNotFoundError, subprocess.TimeoutExpired) as e:
            return {"available": False, "version": "", "error": str(e)}

    elif engine == "paddleocr":
        try:
            result = subprocess.run(
                ['paddleocr', '--version'],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                version = result.stdout.strip().split('\n')[0]
                return {"available": True, "version": version, "error": ""}
        except (FileNotFoundError, subprocess.TimeoutExpired) as e:
            return {"available": False, "version": "", "error": str(e)}

    elif engine == "easyocr":
        try:
            result = subprocess.run(
                ['python3', '-c', 'import easyocr; print(easyocr.__version__)'],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                return {"available": True, "version": version, "error": ""}
        except (FileNotFoundError, subprocess.TimeoutExpired) as e:
            return {"available": False, "version": "", "error": str(e)}

    return {"available": False, "version": "", "error": f"未知引擎: {engine}"}


def detect_available_engine() -> Dict:
    """
    按优先级检测可用的 OCR 引擎。
    检查顺序：Tesseract CLI → PaddleOCR CLI → EasyOCR → 不可用。

    Returns:
        {
            "ocr_available": bool,
            "ocr_engine": str,  # tesseract / paddleocr / easyocr / none
            "version": str,
            "all_engines": {engine: {available, version, error}}
        }
    """
    all_engines = {}
    for engine in ENGINE_PRIORITY:
        all_engines[engine] = check_ocr_engine(engine)
        if all_engines[engine]["available"]:
            return {
                "ocr_available": True,
                "ocr_engine": engine,
                "version": all_engines[engine]["version"],
                "all_engines": all_engines,
            }

    return {
        "ocr_available": False,
        "ocr_engine": "none",
        "version": "",
        "all_engines": all_engines,
    }


# ============================================================
# EMF 转换（复用 image_extract.py 的逻辑）
# ============================================================

def _convert_emf_to_png(emf_path: str) -> Optional[str]:
    """
    将 EMF 格式图片转换为 PNG，返回 PNG 路径。
    转换失败返回 None。
    """
    png_path = emf_path.rsplit('.', 1)[0] + '.png'

    # 方式1：libreoffice 转换
    try:
        out_dir = os.path.dirname(emf_path) or '.'
        result = subprocess.run(
            ['libreoffice', '--headless', '--convert-to', 'png', emf_path, '--outdir', out_dir],
            capture_output=True, text=True, timeout=30
        )
        expected = os.path.join(out_dir, os.path.basename(emf_path).rsplit('.', 1)[0] + '.png')
        if os.path.exists(expected):
            if expected != png_path:
                os.rename(expected, png_path)
            return png_path
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # 方式2：Pillow 尝试
    try:
        from PIL import Image
        img = Image.open(emf_path)
        img.save(png_path, 'PNG')
        return png_path
    except Exception:
        pass

    return None


# ============================================================
# OCR 引擎调用
# ============================================================

def _ocr_tesseract(image_path: str, lang: str = "chi_sim") -> Tuple[str, str]:
    """
    Tesseract CLI 调用。

    Args:
        image_path: 图片路径
        lang: 语言包（默认中文简体）

    Returns:
        (ocr_text, error_message)
    """
    try:
        result = subprocess.run(
            ['tesseract', image_path, 'stdout', '-l', lang, '--psm', '6'],
            capture_output=True, text=True, timeout=OCR_TIMEOUT
        )
        if result.returncode == 0:
            text = result.stdout.strip()
            return (text, "")
        else:
            return ("", f"Tesseract 退出码 {result.returncode}: {result.stderr.strip()[:200]}")
    except subprocess.TimeoutExpired:
        return ("", "Tesseract 超时")
    except FileNotFoundError:
        return ("", "Tesseract 未安装")


def _ocr_paddleocr(image_path: str) -> Tuple[str, str]:
    """
    PaddleOCR CLI 调用。

    Returns:
        (ocr_text, error_message)
    """
    try:
        result = subprocess.run(
            ['paddleocr', 'ocr', '-i', image_path],
            capture_output=True, text=True, timeout=OCR_TIMEOUT
        )
        if result.returncode == 0:
            # PaddleOCR 输出格式解析：提取识别文本
            text = _parse_paddleocr_output(result.stdout)
            return (text, "")
        else:
            return ("", f"PaddleOCR 退出码 {result.returncode}: {result.stderr.strip()[:200]}")
    except subprocess.TimeoutExpired:
        return ("", "PaddleOCR 超时")
    except FileNotFoundError:
        return ("", "PaddleOCR 未安装")


def _parse_paddleocr_output(raw_output: str) -> str:
    """
    解析 PaddleOCR CLI 输出，提取纯文本。
    PaddleOCR 输出格式通常为每行一个识别结果。
    """
    lines = []
    for line in raw_output.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        # PaddleOCR 输出可能包含坐标信息，尝试提取文本部分
        # 格式示例：[[[x1,y1],[x2,y2],...], ('文本', 置信度)]
        match = re.search(r"'([^']+)'", line)
        if match:
            lines.append(match.group(1))
        elif not line.startswith('[') and not line.startswith('('):
            lines.append(line)
    return '\n'.join(lines)


def _ocr_easyocr(image_path: str) -> Tuple[str, str]:
    """
    EasyOCR 调用（通过 subprocess 执行 Python 脚本）。

    Returns:
        (ocr_text, error_message)
    """
    # AB-06修复：通过环境变量传递 image_path，避免命令注入
    script = (
        "import easyocr, os; "
        "reader = easyocr.Reader(['ch_sim', 'en'], gpu=False); "
        "results = reader.readtext(os.environ['IMG_PATH']); "
        "print('\\n'.join([r[1] for r in results]))"
    )
    env = {**os.environ, 'IMG_PATH': image_path}
    try:
        result = subprocess.run(
            ['python3', '-c', script],
            capture_output=True, text=True, timeout=OCR_TIMEOUT * 2,
            env=env  # AB-06修复：环境变量传递路径
        )
        if result.returncode == 0:
            text = result.stdout.strip()
            return (text, "")
        else:
            return ("", f"EasyOCR 错误: {result.stderr.strip()[:200]}")
    except subprocess.TimeoutExpired:
        return ("", "EasyOCR 超时")
    except FileNotFoundError:
        return ("", "Python3 未找到")


# ============================================================
# T2-02：近音字纠错后处理
# ============================================================

# 常见 Tesseract 中文近音/近形字误识映射
# 基于 Phase 0 实测数据 + 常见 OCR 误识模式
COMMON_OCR_CORRECTIONS = {
    "晾": "亮",
    "央化": "孵化",
    "升池": "升汇",
    "未填": "必填",
    "洗填": "选填",
    "起用": "启用",
    "仃用": "停用",
    "己录": "记录",
    "査询": "查询",
    "删徐": "删除",
    "提父": "提交",
    "审枇": "审批",
    "驳回": "驳回",  # 正确，保留
    "帐号": "账号",
    "登陆": "登录",
    "密玛": "密码",
    "验证玛": "验证码",
    "手机号玛": "手机号码",
    "身份证号玛": "身份证号码",
}


def postprocess_ocr_text(
    ocr_text: str,
    before_text: str = "",
    after_text: str = "",
    caption: str = "",
) -> Tuple[str, bool, List[str]]:
    """
    T2-02：OCR 近音字纠错后处理。
    上下文交叉校验 + 常见误识修正。

    策略：
    1. 常见 OCR 误识字典修正
    2. 上下文交叉校验：OCR 文本 vs before_text/after_text/caption 匹配
    3. 纠错失败时置信度下调 0.1

    Args:
        ocr_text: 原始 OCR 文本
        before_text: 图片前文本
        after_text: 图片后文本
        caption: 图注

    Returns:
        (corrected_text, correction_applied, correction_details)
    """
    if not ocr_text:
        return ("", False, [])

    corrected = ocr_text
    details = []
    context = f"{before_text} {after_text} {caption}".lower()
    context_words = set(re.findall(r'[\u4e00-\u9fff]+', context))

    # 策略1：常见 OCR 误识字典修正
    for wrong, right in COMMON_OCR_CORRECTIONS.items():
        if wrong in corrected:
            corrected = corrected.replace(wrong, right)
            details.append(f"字典修正: '{wrong}' → '{right}'")

    # 策略2：上下文交叉校验
    # 提取 OCR 文本中的中文词组
    ocr_words = re.findall(r'[\u4e00-\u9fff]{2,}', corrected)
    for ocr_word in ocr_words:
        # 检查 OCR 词是否在上下文中有近似匹配
        for ctx_word in context_words:
            if len(ctx_word) < 2:
                continue
            # 如果 OCR 词和上下文词长度相同且只差 1 个字，可能是误识
            if len(ocr_word) == len(ctx_word) and ocr_word != ctx_word:
                diff_count = sum(1 for a, b in zip(ocr_word, ctx_word) if a != b)
                if diff_count == 1:
                    # 上下文中的词更可信，替换
                    corrected = corrected.replace(ocr_word, ctx_word, 1)
                    details.append(f"上下文校验: '{ocr_word}' → '{ctx_word}'")
                    break

    applied = len(details) > 0
    return (corrected, applied, details)


# ============================================================
# 核心 OCR 处理函数
# ============================================================

def ocr_single_image(
    image_path: str,
    image_id: str = "",
    engine: str = "tesseract",
    before_text: str = "",
    after_text: str = "",
    caption: str = "",
    apply_correction: bool = True,
) -> OCRResult:
    """
    对单张图片执行 OCR 识别。
    支持超时 30s + 重试 1 次 + 失败降级。
    EMF 图片自动转 PNG。

    Args:
        image_path: 图片文件路径
        image_id: 图片 ID
        engine: OCR 引擎（tesseract / paddleocr / easyocr）
        before_text: 图片前文本（用于纠错）
        after_text: 图片后文本（用于纠错）
        caption: 图注（用于纠错）
        apply_correction: 是否应用近音字纠错

    Returns:
        OCRResult
    """
    result = OCRResult(image_id=image_id, image_path=image_path, engine=engine)
    start_time = time.time()

    # 检查文件存在
    if not os.path.exists(image_path):
        result.status = "failed"
        result.error_message = f"图片文件不存在: {image_path}"
        result.elapsed_seconds = time.time() - start_time
        return result

    # EMF 格式自动转 PNG
    actual_path = image_path
    if image_path.lower().endswith('.emf'):
        png_path = _convert_emf_to_png(image_path)
        if png_path and os.path.exists(png_path):
            actual_path = png_path
        else:
            result.status = "failed"
            result.error_message = "EMF 转 PNG 失败，无法执行 OCR"
            result.elapsed_seconds = time.time() - start_time
            return result

    # 选择 OCR 引擎并执行（含重试）
    ocr_text = ""
    error_msg = ""

    for attempt in range(MAX_RETRY + 1):
        if engine == "tesseract":
            ocr_text, error_msg = _ocr_tesseract(actual_path)
        elif engine == "paddleocr":
            ocr_text, error_msg = _ocr_paddleocr(actual_path)
        elif engine == "easyocr":
            ocr_text, error_msg = _ocr_easyocr(actual_path)
        else:
            error_msg = f"不支持的 OCR 引擎: {engine}"
            break

        if ocr_text:  # 成功
            break
        if not error_msg:  # 空输出
            error_msg = "OCR 输出为空"
        # I-FIX-09: 引擎未安装时重试无意义，直接跳出
        if "未安装" in error_msg or "未找到" in error_msg or "not found" in error_msg.lower():
            break
        result.retry_count = attempt

    result.elapsed_seconds = time.time() - start_time

    # 处理结果
    if ocr_text:
        result.ocr_text = ocr_text
        result.status = "ok"

        # T2-02：近音字纠错
        if apply_correction:
            corrected, applied, details = postprocess_ocr_text(
                ocr_text, before_text, after_text, caption
            )
            result.corrected_text = corrected
            result.correction_applied = applied
            result.correction_details = details
        else:
            result.corrected_text = ocr_text
    elif error_msg and "超时" in error_msg:
        result.status = "timeout"
        result.error_message = error_msg
    elif error_msg and "未安装" in error_msg:
        result.status = "engine_unavailable"
        result.error_message = error_msg
    else:
        result.status = "empty" if not error_msg else "failed"
        result.error_message = error_msg or "OCR 输出为空"

    return result


def ocr_batch_images(
    images: List[Dict],
    engine: str = "tesseract",
    apply_correction: bool = True,
) -> List[OCRResult]:
    """
    批量 OCR 处理（串行执行，不并发）。

    Args:
        images: 图片信息列表，每项需包含：
            - image_id: str
            - file_path: str
            - before_text: str (可选)
            - after_text: str (可选)
            - caption: str (可选)
        engine: OCR 引擎
        apply_correction: 是否应用纠错

    Returns:
        OCRResult 列表
    """
    results = []
    for img in images:
        result = ocr_single_image(
            image_path=img.get("file_path", ""),
            image_id=img.get("image_id", ""),
            engine=engine,
            before_text=img.get("before_text", ""),
            after_text=img.get("after_text", ""),
            caption=img.get("caption", ""),
            apply_correction=apply_correction,
        )
        results.append(result)
    return results


# ============================================================
# 公共接口
# ============================================================

def run_ocr(
    images: List[Dict],
    preferred_engine: str = None,
    apply_correction: bool = True,
) -> Dict:
    """
    OCR 处理的公共入口。
    自动检测可用引擎，串行处理所有图片。

    Args:
        images: 图片信息列表
        preferred_engine: 指定引擎（可选，默认自动检测）
        apply_correction: 是否应用近音字纠错

    Returns:
        {
            "engine_used": str,
            "engine_version": str,
            "total_images": int,
            "success_count": int,
            "failed_count": int,
            "empty_count": int,
            "total_elapsed": float,
            "results": [OCRResult.to_dict()]
        }
    """
    start_time = time.time()

    # 检测可用引擎
    if preferred_engine:
        engine_info = check_ocr_engine(preferred_engine)
        if engine_info["available"]:
            engine = preferred_engine
            version = engine_info["version"]
        else:
            # 指定引擎不可用，自动检测
            detected = detect_available_engine()
            engine = detected["ocr_engine"]
            version = detected["version"]
    else:
        detected = detect_available_engine()
        engine = detected["ocr_engine"]
        version = detected["version"]

    if engine == "none":
        return {
            "engine_used": "none",
            "engine_version": "",
            "total_images": len(images),
            "success_count": 0,
            "failed_count": len(images),
            "empty_count": 0,
            "total_elapsed": time.time() - start_time,
            "results": [
                OCRResult(
                    image_id=img.get("image_id", ""),
                    image_path=img.get("file_path", ""),
                    status="engine_unavailable",
                    error_message="无可用 OCR 引擎",
                ).to_dict()
                for img in images
            ],
        }

    # 串行执行 OCR
    results = ocr_batch_images(images, engine=engine, apply_correction=apply_correction)

    # 统计
    success_count = sum(1 for r in results if r.status == "ok")
    failed_count = sum(1 for r in results if r.status in ("failed", "timeout", "engine_unavailable"))
    empty_count = sum(1 for r in results if r.status == "empty")

    return {
        "engine_used": engine,
        "engine_version": version,
        "total_images": len(images),
        "success_count": success_count,
        "failed_count": failed_count,
        "empty_count": empty_count,
        "total_elapsed": time.time() - start_time,
        "results": [r.to_dict() for r in results],
    }


# ============================================================
# CLI 入口
# ============================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="OCR 引擎封装模块")
    parser.add_argument("images", nargs="*", help="图片文件路径列表")
    parser.add_argument("--engine", choices=["tesseract", "paddleocr", "easyocr"],
                        help="指定 OCR 引擎")
    parser.add_argument("--check", action="store_true", help="仅检查 OCR 可用性")
    parser.add_argument("--no-correction", action="store_true", help="禁用近音字纠错")
    parser.add_argument("--output", "-o", help="输出 JSON 路径")
    args = parser.parse_args()

    if args.check:
        # 仅检查可用性
        result = detect_available_engine()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    if not args.images:
        print("❌ 请提供图片文件路径")
        sys.exit(1)

    # 构建图片列表
    images = [
        {"image_id": f"IMG-{i+1:03d}", "file_path": p}
        for i, p in enumerate(args.images)
    ]

    result = run_ocr(
        images=images,
        preferred_engine=args.engine,
        apply_correction=not args.no_correction,
    )

    output_path = args.output or "ocr_result.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"🔍 OCR 处理完成:")
    print(f"  引擎: {result['engine_used']} ({result['engine_version']})")
    print(f"  总图片: {result['total_images']}")
    print(f"  成功: {result['success_count']}")
    print(f"  失败: {result['failed_count']}")
    print(f"  空输出: {result['empty_count']}")
    print(f"  耗时: {result['total_elapsed']:.2f}s")
    print(f"  结果: {output_path}")
