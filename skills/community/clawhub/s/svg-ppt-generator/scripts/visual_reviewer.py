"""
PPT Visual Reviewer - Convert PPTX to images and review visually.

Uses LibreOffice for PPTX→PNG conversion, then provides images for LLM visual review.
Optionally uses Playwright to render slides in browser for higher-fidelity screenshots.
"""
import os
import subprocess
import tempfile
import shutil
import glob
import json
from pathlib import Path


def pptx_to_images(pptx_path: str, output_dir: str = None, dpi: int = 150) -> list[str]:
    """
    Convert PPTX to PNG images using LibreOffice.
    
    Args:
        pptx_path: Path to the PPTX file
        output_dir: Directory to save images (auto-created if None)
        dpi: Resolution for export (default 150, use 200+ for detailed review)
    
    Returns:
        List of image file paths, sorted by slide number
    """
    pptx_path = os.path.abspath(pptx_path)
    if not os.path.exists(pptx_path):
        raise FileNotFoundError(f"PPTX not found: {pptx_path}")

    if output_dir is None:
        base = os.path.splitext(os.path.basename(pptx_path))[0]
        output_dir = os.path.join(tempfile.gettempdir(), f"ppt_review_{base}")

    os.makedirs(output_dir, exist_ok=True)

    # Use a unique user profile to avoid LibreOffice lock conflicts
    profile_dir = tempfile.mkdtemp(prefix="lo_profile_")

    try:
        cmd = [
            "libreoffice",
            "--headless",
            "--norestore",
            f"-env:UserInstallation=file://{profile_dir}",
            "--convert-to", "png",
            "--outdir", output_dir,
            pptx_path,
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0:
            raise RuntimeError(f"LibreOffice conversion failed: {result.stderr}")
    finally:
        shutil.rmtree(profile_dir, ignore_errors=True)

    # LibreOffice outputs a single PNG for single-slide, or we need PDF route for multi-slide
    # For multi-slide, convert via PDF first then use pdftoppm
    png_files = sorted(glob.glob(os.path.join(output_dir, "*.png")))

    if len(png_files) <= 1:
        # LibreOffice --convert-to png only gives first slide
        # Use PDF intermediate for all slides
        return _pptx_via_pdf(pptx_path, output_dir, dpi)

    return png_files


def _pptx_via_pdf(pptx_path: str, output_dir: str, dpi: int = 150) -> list[str]:
    """Convert PPTX → PDF → PNG per page using pdftoppm or Playwright."""
    profile_dir = tempfile.mkdtemp(prefix="lo_profile_")

    try:
        # Step 1: PPTX → PDF
        cmd = [
            "libreoffice",
            "--headless",
            "--norestore",
            f"-env:UserInstallation=file://{profile_dir}",
            "--convert-to", "pdf",
            "--outdir", output_dir,
            pptx_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            raise RuntimeError(f"PDF conversion failed: {result.stderr}")
    finally:
        shutil.rmtree(profile_dir, ignore_errors=True)

    pdf_name = os.path.splitext(os.path.basename(pptx_path))[0] + ".pdf"
    pdf_path = os.path.join(output_dir, pdf_name)

    if not os.path.exists(pdf_path):
        raise RuntimeError(f"PDF not generated at {pdf_path}")

    # Step 2: PDF → PNG per page
    # Try pdftoppm first (poppler-utils), fall back to Playwright
    if shutil.which("pdftoppm"):
        return _pdf_to_png_pdftoppm(pdf_path, output_dir, dpi)
    else:
        return _pdf_to_png_playwright(pdf_path, output_dir)


def _pdf_to_png_pdftoppm(pdf_path: str, output_dir: str, dpi: int) -> list[str]:
    """Use pdftoppm (poppler) to split PDF into per-page PNGs."""
    prefix = os.path.join(output_dir, "slide")
    cmd = ["pdftoppm", "-png", "-r", str(dpi), pdf_path, prefix]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(f"pdftoppm failed: {result.stderr}")

    images = sorted(glob.glob(os.path.join(output_dir, "slide-*.png")))
    # Rename to slide_01.png, slide_02.png for clarity
    renamed = []
    for i, img in enumerate(images, 1):
        new_name = os.path.join(output_dir, f"slide_{i:02d}.png")
        if img != new_name:
            os.rename(img, new_name)
        renamed.append(new_name)
    return renamed


def _pdf_to_png_playwright(pdf_path: str, output_dir: str) -> list[str]:
    """Use Playwright to render PDF pages as screenshots (fallback)."""
    script = f"""
const {{ chromium }} = require('playwright');
(async () => {{
    const browser = await chromium.launch();
    const context = await browser.newContext();
    const page = await context.newPage();
    await page.setViewportSize({{ width: 1920, height: 1080 }});
    await page.goto('file://{pdf_path}');
    // PDF viewer in Chromium - wait for render
    await page.waitForTimeout(3000);
    await page.screenshot({{ path: '{output_dir}/slide_01.png', fullPage: true }});
    await browser.close();
}})();
"""
    # This is a simplified fallback - pdftoppm is strongly preferred
    script_path = os.path.join(output_dir, "_render.js")
    with open(script_path, "w") as f:
        f.write(script)
    subprocess.run(["node", script_path], capture_output=True, timeout=30)
    return sorted(glob.glob(os.path.join(output_dir, "slide_*.png")))


def generate_review_html(image_paths: list[str], output_path: str = None) -> str:
    """
    Generate an HTML page showing all slides side-by-side for Playwright screenshot.
    Useful for creating a single overview image of the entire deck.
    
    Args:
        image_paths: List of slide image paths
        output_path: Where to save the HTML (default: temp file)
    
    Returns:
        Path to the generated HTML file
    """
    if output_path is None:
        output_path = os.path.join(tempfile.gettempdir(), "ppt_review.html")

    slides_html = ""
    for i, img_path in enumerate(image_paths, 1):
        abs_path = os.path.abspath(img_path)
        slides_html += f"""
        <div class="slide-container">
            <div class="slide-number">Slide {i}</div>
            <img src="file://{abs_path}" class="slide-img" />
        </div>
        """

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body {{
        background: #1a1a1a;
        color: #fff;
        font-family: -apple-system, sans-serif;
        padding: 20px;
        margin: 0;
    }}
    h1 {{ text-align: center; color: #4DB6AC; margin-bottom: 30px; }}
    .grid {{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(480px, 1fr));
        gap: 20px;
        max-width: 1920px;
        margin: 0 auto;
    }}
    .slide-container {{
        background: #2a2a2a;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }}
    .slide-number {{
        padding: 8px 16px;
        font-size: 14px;
        color: #888;
        border-bottom: 1px solid #333;
    }}
    .slide-img {{
        width: 100%;
        display: block;
    }}
</style>
</head>
<body>
    <h1>PPT Visual Review</h1>
    <div class="grid">
        {slides_html}
    </div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path


def visual_review(pptx_path: str, dpi: int = 150) -> dict:
    """
    Full visual review pipeline:
    1. Convert PPTX to per-slide images
    2. Generate review HTML overview
    3. Return paths for LLM visual inspection
    
    Args:
        pptx_path: Path to the PPTX file
        dpi: Image resolution (150 for quick review, 200+ for detailed)
    
    Returns:
        dict with:
            - slide_images: list of per-slide PNG paths
            - review_html: path to overview HTML
            - output_dir: directory containing all outputs
    """
    base = os.path.splitext(os.path.basename(pptx_path))[0]
    output_dir = os.path.join(tempfile.gettempdir(), f"ppt_review_{base}")

    slide_images = pptx_to_images(pptx_path, output_dir, dpi)
    review_html = generate_review_html(
        slide_images,
        os.path.join(output_dir, "review.html"),
    )

    return {
        "slide_images": slide_images,
        "review_html": review_html,
        "output_dir": output_dir,
        "slide_count": len(slide_images),
    }


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/output.pptx"
    result = visual_review(path)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"\n✅ {result['slide_count']} slides exported to {result['output_dir']}")
