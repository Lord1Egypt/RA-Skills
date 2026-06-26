#!/usr/bin/env node

/**
 * Web-to-PDF capture script
 *
 * Captures a web page (especially slide decks / single-page presentations)
 * as a multi-page PDF. Handles scroll-based, keyboard-navigated, and
 * statically-laid-out slide decks.
 *
 * Usage:
 *   node capture.mjs <url> <output.pdf> [--width 1920] [--height 1080] [--wait 1000] [--max-slides 50]
 *
 * Dependencies (auto-installed if missing):
 *   - playwright  (npm)
 *   - Pillow      (pip, for PNG→PDF assembly)
 */

import { chromium } from "playwright";
import { writeFileSync, unlinkSync, existsSync } from "fs";
import { execSync } from "child_process";
import { join, dirname } from "path";
import { tmpdir } from "os";

// ── CLI args ────────────────────────────────────────────────────────────
function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {
    url: null,
    output: null,
    width: 1920,
    height: 1080,
    wait: 1000, // ms to wait after navigating to each slide
    maxSlides: 50,
  };

  const positional = [];
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--width") opts.width = parseInt(args[++i], 10);
    else if (args[i] === "--height") opts.height = parseInt(args[++i], 10);
    else if (args[i] === "--wait") opts.wait = parseInt(args[++i], 10);
    else if (args[i] === "--max-slides")
      opts.maxSlides = parseInt(args[++i], 10);
    else positional.push(args[i]);
  }

  opts.url = positional[0];
  opts.output = positional[1];

  if (!opts.url || !opts.output) {
    console.error("Usage: node capture.mjs <url> <output.pdf> [options]");
    console.error("Options:");
    console.error("  --width  N      Viewport width  (default: 1920)");
    console.error("  --height N      Viewport height (default: 1080)");
    console.error("  --wait   N      Wait ms per slide (default: 1000)");
    console.error("  --max-slides N  Safety cap (default: 50)");
    process.exit(1);
  }

  return opts;
}

const opts = parseArgs();
const TMP_DIR = tmpdir();

// ── Slide detection ─────────────────────────────────────────────────────
async function detectSlides(page) {
  return page.evaluate(() => {
    // Common slide selectors used by presentation frameworks
    const selectors = [
      ".slide",
      "section.present",
      "section",
      ".step",
      ".swiper-slide",
      '[class*="slide"]',
      ".reveal .slides > section",
    ];

    for (const sel of selectors) {
      const els = document.querySelectorAll(sel);
      if (els.length >= 2) {
        return { selector: sel, count: els.length };
      }
    }

    return { selector: null, count: 1 };
  });
}

// ── Detect navigation model ────────────────────────────────────────────
async function detectNavModel(page, slideInfo) {
  return page.evaluate(
    ({ selector, count, viewportHeight }) => {
      const body = document.body;
      const bodyHeight = body.scrollHeight;
      const isScrollable = bodyHeight > viewportHeight * 1.5;

      // Check for known frameworks (verify both DOM and JS API)
      const hasReveal =
        !!document.querySelector(".reveal") &&
        typeof globalThis.Reveal !== "undefined" &&
        typeof globalThis.Reveal.slide === "function";
      const hasImpress = !!document.querySelector("#impress");
      const hasDeck = !!document.querySelector(".deck-container");

      if (hasReveal) return { type: "reveal" };
      if (hasImpress) return { type: "impress" };
      if (hasDeck) return { type: "deck" };

      // If page is tall enough for multiple slides, assume vertical scroll
      if (isScrollable && count > 1) return { type: "scroll", selector };

      // Fallback: try keyboard navigation
      return { type: "keyboard", selector };
    },
    {
      selector: slideInfo.selector,
      count: slideInfo.count,
      viewportHeight: opts.height,
    }
  );
}

// ── Make animated content visible ───────────────────────────────────────
async function revealAnimations(page) {
  await page.evaluate(() => {
    // Force all reveal/fade animations to their final state
    const animatedSelectors = [
      '[class*="reveal"]',
      '[class*="fade"]',
      '[class*="animate"]',
      ".fragment",
      '[style*="opacity: 0"]',
    ];

    for (const sel of animatedSelectors) {
      document.querySelectorAll(sel).forEach((el) => {
        el.style.opacity = "1";
        el.style.transform = "none";
        el.style.transition = "none";
        el.style.animation = "none";
        el.classList.add("visible", "current-fragment");
      });
    }
  });
}

// ── Capture strategies ──────────────────────────────────────────────────

async function captureByScroll(page, slideInfo) {
  const paths = [];
  for (let i = 0; i < Math.min(slideInfo.count, opts.maxSlides); i++) {
    await page.evaluate(
      ({ sel, idx }) => {
        const slides = document.querySelectorAll(sel);
        if (slides[idx]) {
          slides[idx].scrollIntoView({ behavior: "instant" });
          slides[idx].classList.add("visible", "active");
        }
      },
      { sel: slideInfo.selector, idx: i }
    );
    await page.waitForTimeout(opts.wait);
    await revealAnimations(page);
    await page.waitForTimeout(200);

    const p = join(TMP_DIR, `_wtpdf_slide_${String(i).padStart(3, "0")}.png`);
    await page.screenshot({ path: p, fullPage: false });
    paths.push(p);
    console.log(`  Captured slide ${i + 1}/${slideInfo.count}`);
  }
  return paths;
}

async function captureByKeyboard(page, slideInfo) {
  const paths = [];
  const total = Math.min(slideInfo.count, opts.maxSlides);

  for (let i = 0; i < total; i++) {
    await revealAnimations(page);
    await page.waitForTimeout(300);

    const p = join(TMP_DIR, `_wtpdf_slide_${String(i).padStart(3, "0")}.png`);
    await page.screenshot({ path: p, fullPage: false });
    paths.push(p);
    console.log(`  Captured slide ${i + 1}/${total}`);

    if (i < total - 1) {
      // Try common "next slide" keys
      await page.keyboard.press("ArrowRight");
      await page.waitForTimeout(opts.wait);

      // Check if the page changed; if not, try ArrowDown or Space
      const changed = await page.evaluate(
        ({ sel, expected }) => {
          if (!sel) return true; // can't check, assume it changed
          const active = document.querySelector(
            `${sel}.active, ${sel}.present, ${sel}.current`
          );
          if (!active) return true;
          const all = Array.from(document.querySelectorAll(sel));
          return all.indexOf(active) !== expected;
        },
        { sel: slideInfo.selector, expected: i }
      );

      if (!changed) {
        await page.keyboard.press("ArrowDown");
        await page.waitForTimeout(opts.wait);
      }
    }
  }
  return paths;
}

async function captureReveal(page) {
  const paths = [];
  const total = await page.evaluate(
    () => Reveal?.getTotalSlides?.() ?? document.querySelectorAll("section").length
  );

  for (let i = 0; i < Math.min(total, opts.maxSlides); i++) {
    await page.evaluate((idx) => Reveal?.slide?.(idx), i);
    await page.waitForTimeout(opts.wait);
    await revealAnimations(page);
    await page.waitForTimeout(200);

    const p = join(TMP_DIR, `_wtpdf_slide_${String(i).padStart(3, "0")}.png`);
    await page.screenshot({ path: p, fullPage: false });
    paths.push(p);
    console.log(`  Captured slide ${i + 1}/${total}`);
  }
  return paths;
}

async function captureSinglePage(page) {
  // Fallback: capture the full page as a single tall screenshot, then split
  const p = join(TMP_DIR, `_wtpdf_slide_000.png`);
  await revealAnimations(page);
  await page.waitForTimeout(500);
  await page.screenshot({ path: p, fullPage: true });
  console.log("  Captured full page");
  return [p];
}

// ── PNG → PDF assembly ──────────────────────────────────────────────────
function assemblePDF(pngPaths, outputPath) {
  const pyScript = `
import sys, json
from PIL import Image

paths = json.loads(sys.argv[1])
output = sys.argv[2]
vw = int(sys.argv[3])
vh = int(sys.argv[4])

images = []
for p in paths:
    img = Image.open(p).convert('RGB')
    # If the image is a tall full-page screenshot, split into viewport-sized pages
    if img.height > vh * 1.5 and len(paths) == 1:
        num_pages = round(img.height / vh)
        page_h = img.height // num_pages
        for j in range(num_pages):
            top = j * page_h
            bottom = min(top + page_h, img.height)
            page_img = img.crop((0, top, img.width, bottom))
            images.append(page_img)
    else:
        images.append(img)

if not images:
    print("No images to assemble", file=sys.stderr)
    sys.exit(1)

images[0].save(
    output,
    save_all=True,
    append_images=images[1:],
    resolution=150.0
)
print(f"PDF created: {len(images)} pages -> {output}")
`;

  const scriptPath = join(TMP_DIR, "_wtpdf_assemble.py");
  writeFileSync(scriptPath, pyScript);

  try {
    const result = execSync(
      `python3 "${scriptPath}" '${JSON.stringify(pngPaths)}' "${outputPath}" ${opts.width} ${opts.height}`,
      { encoding: "utf-8" }
    );
    console.log(result.trim());
  } finally {
    // Cleanup temp files
    try { unlinkSync(scriptPath); } catch {}
    for (const p of pngPaths) {
      try { unlinkSync(p); } catch {}
    }
  }
}

// ── Main ────────────────────────────────────────────────────────────────
async function main() {
  console.log(`Capturing: ${opts.url}`);
  console.log(`Output:    ${opts.output}`);
  console.log(`Viewport:  ${opts.width}x${opts.height}`);

  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: opts.width, height: opts.height });

  console.log("Loading page...");
  await page.goto(opts.url, { waitUntil: "networkidle", timeout: 60000 });
  await page.waitForTimeout(2000);

  // Detect slides and navigation model
  const slideInfo = await detectSlides(page);
  console.log(
    `Detected ${slideInfo.count} slides (selector: ${slideInfo.selector || "none"})`
  );

  const navModel = await detectNavModel(page, slideInfo);
  console.log(`Navigation model: ${navModel.type}`);

  let pngPaths;

  switch (navModel.type) {
    case "reveal":
      pngPaths = await captureReveal(page);
      break;
    case "scroll":
      pngPaths = await captureByScroll(page, slideInfo);
      break;
    case "keyboard":
      if (slideInfo.count > 1) {
        pngPaths = await captureByKeyboard(page, slideInfo);
      } else {
        pngPaths = await captureSinglePage(page);
      }
      break;
    default:
      pngPaths = await captureSinglePage(page);
  }

  await browser.close();

  // Assemble into PDF
  console.log("Assembling PDF...");
  assemblePDF(pngPaths, opts.output);
}

main().catch((err) => {
  console.error("Error:", err.message);
  process.exit(1);
});
