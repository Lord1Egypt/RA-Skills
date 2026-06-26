#!/usr/bin/env python3
"""
Trich xuat thong tin tu anh CCCD/CMND Viet Nam bang EasyOCR.
Chay DOC LAP — khong can Claude, GPT hay bat ky AI model nao.

Cai dat:
    pip install easyocr opencv-python --break-system-packages

Cach dung:
    python cccd-ocr.py <anh_cccd.jpg>
    python cccd-ocr.py <anh_cccd.jpg> --json
    python cccd-ocr.py <anh_truoc.jpg> --back <anh_sau.jpg>
    python cccd-ocr.py <anh_cccd.jpg> --gpu
"""

import sys
import os
import re
import json
import argparse


def check_deps():
    missing = []
    try:
        import easyocr
    except ImportError:
        missing.append("easyocr")
    try:
        import cv2
    except ImportError:
        missing.append("opencv-python")
    if missing:
        print("Thieu thu vien. Chay lenh:")
        print(f"   pip install {' '.join(missing)} --break-system-packages")
        sys.exit(1)


def preprocess(image_path):
    import cv2
    import numpy as np
    img = cv2.imread(image_path)
    if img is None:
        print(f"Khong doc duoc anh: {image_path}")
        sys.exit(1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    denoised = cv2.fastNlMeansDenoising(enhanced, None, 10, 7, 21)
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(denoised, -1, kernel)
    return sharpened


def ocr_image(image_path, reader):
    processed = preprocess(image_path)
    return reader.readtext(processed, detail=1, paragraph=False)


def parse_front(results):
    info = {
        "so_cccd": None, "ho_ten": None, "ngay_sinh": None,
        "gioi_tinh": None, "quoc_tich": None, "que_quan": None,
        "noi_thuong_tru": None, "han_su_dung": None,
    }
    texts = [{"text": t.strip(), "conf": c, "y": b[0][1]} for b, t, c in results]
    texts.sort(key=lambda x: x["y"])

    for i, t in enumerate(texts):
        line = t["text"]
        lu = line.upper()

        # So CCCD (12 chu so)
        m = re.search(r'\b(\d{12})\b', line)
        if m and not info["so_cccd"]:
            info["so_cccd"] = m.group(1)

        # Ho ten
        if any(k in lu for k in ["HỌ VÀ TÊN", "HO VA TEN", "FULL NAME"]):
            name = re.sub(r'(?i)(họ và tên|ho va ten|full name)[:/\s]*', '', line).strip()
            if name and len(name) > 2:
                info["ho_ten"] = name.upper()
            elif i + 1 < len(texts):
                info["ho_ten"] = texts[i + 1]["text"].upper()

        # Ngay sinh + Gioi tinh
        if any(k in lu for k in ["NGÀY SINH", "NGAY SINH", "DATE OF BIRTH"]):
            dm = re.search(r'(\d{1,2}[/.\-]\d{1,2}[/.\-]\d{4})', line)
            if dm:
                info["ngay_sinh"] = dm.group(1).replace('.', '/').replace('-', '/')
            if "NAM" in lu and "NỮ" not in lu:
                info["gioi_tinh"] = "Nam"
            elif "NỮ" in lu or "NU" in lu:
                info["gioi_tinh"] = "Nữ"

        # Quoc tich
        if any(k in lu for k in ["QUỐC TỊCH", "QUOC TICH", "NATIONALITY"]):
            info["quoc_tich"] = "Việt Nam"

        # Que quan
        if any(k in lu for k in ["QUÊ QUÁN", "QUE QUAN", "PLACE OF ORIGIN"]):
            val = re.sub(r'(?i)(quê quán|que quan|place of origin)[:/\s]*', '', line).strip()
            if val and len(val) > 2:
                info["que_quan"] = val
            elif i + 1 < len(texts):
                info["que_quan"] = texts[i + 1]["text"]

        # Noi thuong tru (co the dai 2-3 dong)
        if any(k in lu for k in ["NƠI THƯỜNG TRÚ", "NOI THUONG TRU", "PLACE OF RESIDENCE"]):
            val = re.sub(r'(?i)(nơi thường trú|noi thuong tru|place of residence)[:/\s]*', '', line).strip()
            if val and len(val) > 2:
                info["noi_thuong_tru"] = val
            elif i + 1 < len(texts):
                parts = []
                for j in range(i + 1, min(i + 4, len(texts))):
                    nt = texts[j]["text"]
                    if any(k in nt.upper() for k in ["CÓ GIÁ TRỊ", "CO GIA TRI", "DATE OF EXPIRY"]):
                        break
                    parts.append(nt)
                info["noi_thuong_tru"] = ", ".join(parts)

        # Han su dung
        if any(k in lu for k in ["CÓ GIÁ TRỊ", "CO GIA TRI", "DATE OF EXPIRY"]):
            dm = re.search(r'(\d{1,2}[/.\-]\d{1,2}[/.\-]\d{4})', line)
            if dm:
                info["han_su_dung"] = dm.group(1).replace('.', '/').replace('-', '/')

    return info


def parse_back(results):
    info = {"ngay_cap": None, "noi_cap": None}
    texts = [{"text": t.strip(), "y": b[0][1]} for b, t, c in results]
    texts.sort(key=lambda x: x["y"])

    for t in texts:
        line = t["text"]
        # Ngay cap
        dm = re.search(r'[Nn]gày[:\s]*(\d{1,2}[/.\-]\d{1,2}[/.\-]\d{4})', line)
        if dm and not info["ngay_cap"]:
            info["ngay_cap"] = dm.group(1).replace('.', '/').replace('-', '/')
        vn = re.search(r'[Nn]gày\s*(\d{1,2})\s*tháng\s*(\d{1,2})\s*năm\s*(\d{4})', line)
        if vn and not info["ngay_cap"]:
            info["ngay_cap"] = f"{vn.group(1)}/{vn.group(2)}/{vn.group(3)}"
        # Noi cap
        if any(k in line.upper() for k in ["CỤC TRƯỞNG", "CUC TRUONG", "BỘ CÔNG AN", "BO CONG AN"]):
            info["noi_cap"] = "Cục trưởng Cục Cảnh sát quản lý hành chính về trật tự xã hội"

    if not info["noi_cap"]:
        info["noi_cap"] = "Cục trưởng Cục Cảnh sát quản lý hành chính về trật tự xã hội"
    return info


def main():
    ap = argparse.ArgumentParser(description="OCR quet CCCD Viet Nam (EasyOCR)")
    ap.add_argument("image", help="Anh CCCD mat truoc")
    ap.add_argument("--back", help="Anh CCCD mat sau (tuy chon)")
    ap.add_argument("--json", action="store_true", help="Xuat JSON")
    ap.add_argument("--gpu", action="store_true", help="Dung GPU")
    args = ap.parse_args()

    check_deps()
    import easyocr

    if not os.path.exists(args.image):
        print(f"Khong tim thay: {args.image}")
        sys.exit(1)

    print("Dang quet CCCD...")
    print("(Lan dau chay se tai model ~100MB, chi can 1 lan)")
    print("=" * 55)

    reader = easyocr.Reader(['vi', 'en'], gpu=args.gpu, verbose=False)

    print(f"Quet mat truoc: {args.image}")
    front_results = ocr_image(args.image, reader)
    info = parse_front(front_results)

    if args.back:
        if os.path.exists(args.back):
            print(f"Quet mat sau: {args.back}")
            back_results = ocr_image(args.back, reader)
            back_info = parse_back(back_results)
            info.update({k: v for k, v in back_info.items() if v})
        else:
            print(f"Khong tim thay mat sau: {args.back}")

    if args.json:
        print(json.dumps(info, ensure_ascii=False, indent=2))
    else:
        print("")
        print("KET QUA TRICH XUAT:")
        print("-" * 55)
        labels = [
            ("so_cccd", "So CCCD"), ("ho_ten", "Ho ten"),
            ("ngay_sinh", "Ngay sinh"), ("gioi_tinh", "Gioi tinh"),
            ("quoc_tich", "Quoc tich"), ("que_quan", "Que quan"),
            ("noi_thuong_tru", "Noi thuong tru"),
            ("ngay_cap", "Ngay cap"), ("noi_cap", "Noi cap"),
            ("han_su_dung", "Co gia tri den"),
        ]
        filled = 0
        for key, label in labels:
            val = info.get(key)
            if val:
                print(f"  {label}: {val}")
                filled += 1
            else:
                print(f"  {label}: [KHONG DOC DUOC]")

        total = len(labels)
        print("")
        print("=" * 55)
        print(f"Doc duoc: {filled}/{total} truong")

        if not args.back and not info.get("ngay_cap"):
            print("")
            print("Tip: Them --back <anh_mat_sau.jpg> de lay ngay cap, noi cap")

        print("")
        print("Thong tin can bo sung (CCCD khong co):")
        print("   - So dien thoai")
        print("   - Email")
        print("   - So tai khoan ngan hang + ten ngan hang")

    return info


if __name__ == "__main__":
    main()
