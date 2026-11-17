#!/usr/bin/env python3
"""verify_part.py — Kiểm tra part đã dịch sau khi ghi out/.

Đếm số đoạn raw vs out (phải bằng nhau), phát hiện file out rỗng 0 byte,
còn sót ký tự \u3000 hoặc chữ Trung, và báo danh sách part bị thiếu.

Cách dùng:
    python scripts/verify_part.py <project_dir>
        # project_dir chứa raw/ và out/ (tự tìm thư mục chứa '111' nếu không truyền)
    python scripts/verify_part.py raw/part_027.md out/part_027.md
        # kiểm tra 1 cặp file

Quy ước:
    - raw có marker `第NN章` thì out phải có đúng 1 heading `# Chương NN:`.
    - Chênh lệch số đoạn <=1 coi là chấp nhận được (gộp/tách đoạn ngắn);
      lệch >1 hoặc file 0 byte là DẤU HIỆU CẮT CỤT / lỗi dịch — phải sửa trước khi merge.
"""
import sys
from pathlib import Path


def count_paras(text: str) -> int:
    return len([p for p in text.split("\n\n") if p.strip()])


def check_file(raw_path: Path, out_path: Path) -> tuple:
    """Trả về (ok: bool, msg: str) cho 1 cặp raw/out."""
    if not out_path.exists():
        return False, f"THIẾU file out: {out_path.name}"
    size = out_path.stat().st_size
    if size == 0:
        return False, f"FILE RỖNG 0 BYTE: {out_path.name} (xóa hoặc ghi lại)"
    raw = raw_path.read_text(encoding="utf-8")
    out = out_path.read_text(encoding="utf-8")
    n_raw = count_paras(raw)
    n_out = count_paras(out)
    msgs = []
    ok = True
    if abs(n_raw - n_out) > 1:
        ok = False
        msgs.append(f"SỐ ĐOẠN LỆCH: raw={n_raw} out={n_out} (lệch >1 → nghi cắt cụt/dịch vượt)")
    elif n_raw != n_out:
        msgs.append(f"chênh {n_raw} vs {n_out} (<=1, chấp nhận được)")
    if "\u3000" in out:
        ok = False
        msgs.append("CÒN \\u3000 (thụt đầu dòng to-width)")
    cjk = [c for c in out if "\u4e00" <= c <= "\u9fff"]
    if cjk:
        ok = False
        msgs.append(f"CÒN {len(cjk)} ký tự Trung (VD: {''.join(cjk[:10])})")
    # heading: nếu raw có marker chương, out phải có heading
    import re
    marks = re.findall(r"第[一二三四五六七八九十百]+章", raw)
    heads = [ln for ln in out.split("\n") if ln.startswith("# ")]
    if marks and not heads:
        ok = False
        msgs.append(f"raw có marker {marks} nhưng out thiếu heading # Chương")
    return ok, "; ".join(msgs) if msgs else "OK"


def main() -> int:
    args = sys.argv[1:]
    if len(args) == 2 and Path(args[0]).is_file() and Path(args[1]).is_file():
        ok, msg = check_file(Path(args[0]), Path(args[1]))
        print(f"{Path(args[1]).name}: {msg}")
        return 0 if ok else 1

    if len(args) >= 1:
        proj = Path(args[0])
    else:
        base = Path(r"C:\AI-WS\Translate")
        cands = [p for p in base.iterdir() if p.is_dir() and "111" in p.name]
        proj = cands[0] if cands else None
    if proj is None:
        print("Không tìm thấy project — truyền đường dẫn project làm đối số.")
        return 2

    raw_dir, out_dir = proj / "raw", proj / "out"
    raws = sorted(raw_dir.glob("part_*.md"))
    n_ok = n_bad = n_empty = 0
    for r in raws:
        out = out_dir / r.name
        ok, msg = check_file(r, out)
        if out.exists() and out.stat().st_size == 0:
            n_empty += 1
        if ok:
            n_ok += 1
        else:
            n_bad += 1
            print(f"  [{r.name}] {msg}")
    print(f"--- {proj.name}")
    print(f"raw: {len(raws)} part | out OK: {n_ok} | LỖI: {n_bad} | file rỗng: {n_empty}")
    if n_empty:
        print("DỌN: find out -name '*.md' -size 0 -delete")
    return 0 if n_bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
