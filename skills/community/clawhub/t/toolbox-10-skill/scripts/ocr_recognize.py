#!/usr/bin/env python3
"""
OCR 文字识别工具 — 基于 EasyOCR
支持中英文混合识别，输出文字内容和位置坐标。
"""

import argparse
import json
import sys
from pathlib import Path


def ocr_recognize(
    input_path: str,
    output_path: str = None,
    languages: list = None,
    detail: bool = True,
    min_confidence: float = 0.3,
) -> dict:
    """
    执行 OCR 识别。
    """
    try:
        import easyocr
    except ImportError:
        return {
            "success": False,
            "error": "需要安装 easyocr: pip install easyocr",
        }

    img_path = Path(input_path)
    if not img_path.exists():
        return {"success": False, "error": f"文件不存在: {input_path}"}

    if languages is None:
        languages = ["ch_sim", "en"]

    try:
        # 初始化 reader（首次会下载模型）
        reader = easyocr.Reader(languages, gpu=False)
        results = reader.readtext(str(img_path), detail=1)
    except Exception as e:
        return {"success": False, "error": f"OCR 识别失败: {str(e)}"}

    # 解析结果
    texts = []
    full_text_parts = []
    for bbox, text, confidence in results:
        if confidence < min_confidence:
            continue

        item = {
            "text": text,
            "confidence": round(float(confidence), 4),
            "bbox": [[int(p[0]), int(p[1])] for p in bbox],
        }
        texts.append(item)
        full_text_parts.append(text)

    full_text = "\n".join(full_text_parts)

    output = {
        "success": True,
        "input": str(img_path),
        "total_items": len(texts),
        "languages": languages,
        "texts": texts if detail else None,
        "full_text": full_text,
        "image_size": None,
    }

    # 获取图片尺寸
    try:
        from PIL import Image

        with Image.open(input_path) as img:
            output["image_size"] = {"width": img.width, "height": img.height}
    except Exception:
        pass

    # 保存到文件（如果指定）
    if output_path:
        out_path = Path(output_path)
        with open(out_path, "w", encoding="utf-8") as f:
            if out_path.suffix == ".json":
                json.dump(output, f, ensure_ascii=False, indent=2)
            else:
                f.write(full_text)
        output["output_file"] = str(out_path)

    return output


def main():
    parser = argparse.ArgumentParser(description="OCR 文字识别工具")
    parser.add_argument("input", help="输入图片路径")
    parser.add_argument("-o", "--output", help="输出文件路径 (.txt 或 .json)")
    parser.add_argument(
        "--lang",
        nargs="+",
        default=["ch_sim", "en"],
        help="识别语言 (默认: ch_sim en). 可选: ch_sim, en, ja, ko, fr, de, es 等",
    )
    parser.add_argument(
        "--no-detail", action="store_true", help="不输出详细坐标信息，只输出纯文本"
    )
    parser.add_argument(
        "--min-confidence",
        type=float,
        default=0.3,
        help="最小置信度阈值 (0-1, 默认0.3)",
    )
    parser.add_argument(
        "--json", action="store_true", help="以 JSON 格式输出完整结果到 stdout"
    )

    args = parser.parse_args()

    result = ocr_recognize(
        input_path=args.input,
        output_path=args.output,
        languages=args.lang,
        detail=not args.no_detail,
        min_confidence=args.min_confidence,
    )

    if args.json or "full_text" not in result:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 简洁模式
        if result.get("success"):
            print(f"=== 识别结果 ({result.get('total_items', 0)} 条) ===")
            print(result.get("full_text", ""))
            if result.get("output_file"):
                print(f"\n结果已保存到: {result['output_file']}")
        else:
            print(f"失败: {result.get('error', '未知错误')}")
            sys.exit(1)


if __name__ == "__main__":
    main()
