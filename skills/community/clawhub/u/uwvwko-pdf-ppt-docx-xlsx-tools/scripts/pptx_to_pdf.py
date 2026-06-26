"""PPTX → PDF (通过 LibreOffice)

用法:
    python pptx_to_pdf.py input.pptx [output_dir] [--soffice PATH]

参数:
    input.pptx  - PPTX 文件路径
    output_dir  - 输出目录 (默认: 与输入文件同目录)
    --soffice   - LibreOffice soffice 路径 (自动检测)
"""
import subprocess
import sys
import os


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
        print("用法: python pptx_to_pdf.py input.pptx [output_dir] [--soffice PATH]")
        sys.exit(1)

    pptx_path = os.path.abspath(sys.argv[1])
    out_dir = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None

    if not os.path.isfile(pptx_path):
        print(f"错误: 文件不存在 - {pptx_path}")
        sys.exit(1)

    soffice_path = None
    for i, arg in enumerate(sys.argv):
        if arg == "--soffice" and i + 1 < len(sys.argv):
            soffice_path = sys.argv[i + 1]
            break
    if not soffice_path:
        soffice_path = find_soffice()
    if not soffice_path:
        print("错误: 未找到 LibreOffice (soffice)，请安装或通过 --soffice 指定路径")
        sys.exit(1)

    if not out_dir:
        out_dir = os.path.dirname(pptx_path)
    os.makedirs(out_dir, exist_ok=True)

    cmd = [soffice_path, "--headless", "--convert-to", "pdf", "--outdir", out_dir, pptx_path]
    print(f"执行: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"错误: {result.stderr}")
        sys.exit(1)

    pdf_name = os.path.splitext(os.path.basename(pptx_path))[0] + ".pdf"
    pdf_path = os.path.join(out_dir, pdf_name)
    if os.path.isfile(pdf_path):
        print(f"完成: {pptx_path} -> {pdf_path}")
    else:
        print(f"警告: 命令执行成功但未找到输出文件 {pdf_path}")


if __name__ == "__main__":
    main()