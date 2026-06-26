#!/usr/bin/env python3
"""
会议纪要 HTML → PDF 导出脚本
支持 Playwright (优先) 和 weasyprint 两种后端
用法: python export_pdf.py <input.html> <output.pdf>
"""
import sys
import os

def export_with_playwright(html_path: str, pdf_path: str) -> bool:
    """使用 Playwright Chromium 导出 PDF"""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f'file://{os.path.abspath(html_path)}')
            page.wait_for_load_state('networkidle')
            page.pdf(
                path=pdf_path,
                format='A4',
                print_background=True,
                margin={
                    'top': '20mm',
                    'right': '0mm',
                    'bottom': '20mm',
                    'left': '0mm'
                }
            )
            browser.close()
        return True
    except ImportError:
        return False
    except Exception as e:
        print(f"Playwright export failed: {e}", file=sys.stderr)
        return False

def export_with_weasyprint(html_path: str, pdf_path: str) -> bool:
    """使用 WeasyPrint 导出 PDF (备选方案)"""
    try:
        from weasyprint import HTML
        HTML(filename=html_path).write_pdf(pdf_path)
        return True
    except ImportError:
        return False
    except Exception as e:
        print(f"WeasyPrint export failed: {e}", file=sys.stderr)
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage: python export_pdf.py <input.html> <output.pdf>")
        sys.exit(1)

    html_path = sys.argv[1]
    pdf_path = sys.argv[2]

    if not os.path.exists(html_path):
        print(f"Error: {html_path} not found", file=sys.stderr)
        sys.exit(1)

    # 尝试 Playwright (优先，效果最好)
    if export_with_playwright(html_path, pdf_path):
        size = os.path.getsize(pdf_path)
        print(f"OK [playwright] {pdf_path} ({size:,} bytes)")
        return

    # 回退到 WeasyPrint
    if export_with_weasyprint(html_path, pdf_path):
        size = os.path.getsize(pdf_path)
        print(f"OK [weasyprint] {pdf_path} ({size:,} bytes)")
        return

    print("Error: No PDF backend available. Install one of:", file=sys.stderr)
    print("  pip install playwright && playwright install chromium", file=sys.stderr)
    print("  pip install weasyprint", file=sys.stderr)
    sys.exit(1)

if __name__ == '__main__':
    main()
