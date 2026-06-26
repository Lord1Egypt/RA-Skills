import json
import logging
import os
import sys
import warnings


def normalize_result(result, img_path):
    lines = []
    boxes = []
    scores = []

    if result is None:
        return {"text": "", "lines": [], "boxes": [], "scores": [], "source": img_path}

    if hasattr(result, "txts") and result.txts:
        lines = [str(x) for x in result.txts]

    if hasattr(result, "scores") and result.scores:
        try:
            scores = [float(x) for x in result.scores]
        except Exception:
            scores = [str(x) for x in result.scores]

    if hasattr(result, "boxes") and result.boxes is not None:
        try:
            boxes = result.boxes.tolist()
        except Exception:
            boxes = []

    if not lines and isinstance(result, (list, tuple)):
        for item in result:
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                continue
            if item and isinstance(item[0], (list, tuple)):
                boxes.append(item[0])
            lines.append(str(item[1]))
            if len(item) >= 3:
                try:
                    scores.append(float(item[2]))
                except Exception:
                    scores.append(str(item[2]))

    return {
        "text": "\n".join(lines),
        "lines": lines,
        "boxes": boxes,
        "scores": scores,
        "source": img_path,
    }


def main():
    if len(sys.argv) < 2:
        print("Missing image path.", file=sys.stderr)
        sys.exit(2)

    img_path = sys.argv[1]
    json_mode = "--json" in sys.argv[2:]

    warnings.filterwarnings("ignore")
    for name in ["RapidOCR", "rapidocr", "onnxruntime"]:
        logger = logging.getLogger(name)
        logger.handlers.clear()
        logger.propagate = False
        logger.setLevel(logging.CRITICAL)
    logging.disable(logging.CRITICAL)

    try:
        from rapidocr import RapidOCR
    except ImportError:
        python_cmd = os.environ.get("RAPIDOCR_PYTHON", "python")
        print(f"RapidOCR is not installed. Run: {python_cmd} -m pip install rapidocr onnxruntime", file=sys.stderr)
        sys.exit(1)

    engine = RapidOCR()
    result = normalize_result(engine(img_path), img_path)

    if json_mode:
        print(json.dumps(result, ensure_ascii=False))
        return

    print(result["text"])


if __name__ == "__main__":
    main()
