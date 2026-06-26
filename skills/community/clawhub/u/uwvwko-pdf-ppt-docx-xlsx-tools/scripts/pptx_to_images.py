"""PPTX → 图片 (PNG)

用法:
    python pptx_to_images.py input.pptx [output_dir] [dpi] [--soffice PATH]

参数:
    input.pptx  - PPTX 文件路径
    output_dir  - 输出目录 (默认: ./pptx_images_output)
    dpi         - 渲染分辨率 (默认: 200)
    --soffice   - LibreOffice 路径 (自动检测)

说明:
    先通过 LibreOffice 转为 PDF，再用 PyMuPDF 渲染为图片
"""
import fitz
import subprocess
import sys
import os
import tempfile


def find_soffice():
    candidates = [
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
        "/usr/bin/soffice",
        "/usr/bin/libreoffice",
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    for cmd in ["where soffice", "which soffice", "which libreoffice"]:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip().split("\n")[0]
        except Exception:
            continue
    return None


def main():
    if len(sys.argv) < 2:
        print("用法: python pptx_to_images.py input.pptx [output_dir] [dpi] [--soffice PATH]")
        sys.exit(1)

    pptx_path = os.path.abspath(sys.argv[1])
    out_dir = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else "./pptx_images_output"
    dpi = 200
    soffice_path = None

    for i, arg in enumerate(sys.argv):
        if arg == "--soffice" and i + 1 < len(sys.argv):
            soffice_path = sys.argv[i + 1]
        elif not arg.startswith("--") and i > 1:
            try:
                dpi = int(arg)
            except ValueError:
                pass

    if not os.path.isfile(pptx_path):
        print(f"错误: 文件不存在 - {pptx_path}")
        sys.exit(1)

    if not soffice_path:
        soffice_path = find_soffice()
    if not soffice_path:
        print("错误: 未找到 LibreOffice (soffice)，请安装或通过 --soffice 指定路径")
        sys.exit(1)

    os.makedirs(out_dir, exist_ok=True)

    # LibreOffice 转 PDF
    tmp_dir = tempfile.mkdtemp()
    subprocess.run(
        [soffice_path, "--headless", "--convert-to", "pdf", "--outdir", tmp_dir, pptx_path],
        check=True, capture_output=True,
    )
    pdf_name = os.path.splitext(os.path.basename(pptx_path))[0] + ".pdf"
    pdf_tmp = os.path.join(tmp_dir, pdf_name)

    # PyMuPDF 渲染
    doc = fitz.open(pdf_tmp)
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=dpi)
        out = os.path.join(out_dir, f"slide_{i + 1:04d}.png")
        pix.save(out)
        print(f"Saved: {out}")

    total = len(doc)
    doc.close()
    os.unlink(pdf_tmp)
    os.rmdir(tmp_dir)
    print(f"完成: {total} 张幻灯片 -> {out_dir}")


if __name__ == "__main__":
    main()