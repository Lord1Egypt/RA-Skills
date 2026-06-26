#!/usr/bin/env node
/**
 * render-image.js — Render an HTML/CSS file to a PNG using headless Chrome.
 *
 * Usage:
 *   node render-image.js <input.html> <output.png> [--width=1080] [--height=1440] [--scale=2]
 *
 * Options:
 *   --width    Viewport width in CSS pixels (default 1080).
 *   --height   Viewport height in CSS pixels (default 1440, a 3:4 vertical card).
 *   --scale    deviceScaleFactor for crisp output (default 2 → 2160×2880 PNG).
 *   --full     Capture full scrollable page height instead of the fixed viewport.
 *
 * Runtime: Puppeteer (bundled Chromium) is preferred. If its browser is not
 * available, the script falls back to a system Chrome/Chromium. If no browser
 * can be launched, it prints manual-render instructions and exits non-zero
 * WITHOUT deleting the input HTML, so the user can render it by hand.
 *
 * No credentials, tokens, or network access are required.
 */

const fs = require("fs");
const path = require("path");

function parseArgs(argv) {
  const positional = [];
  const opts = { width: 1080, height: 1440, scale: 2, full: false };
  for (const arg of argv) {
    if (arg.startsWith("--")) {
      const [key, value] = arg.slice(2).split("=");
      if (key === "full") opts.full = true;
      else if (value !== undefined) opts[key] = Number(value) || value;
    } else {
      positional.push(arg);
    }
  }
  return { positional, opts };
}

// Common locations for a system Chrome/Chromium, checked when the bundled
// browser is missing. PUPPETEER_EXECUTABLE_PATH always wins if set.
function findSystemChrome() {
  if (process.env.PUPPETEER_EXECUTABLE_PATH) {
    return process.env.PUPPETEER_EXECUTABLE_PATH;
  }
  const candidates = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
  ];
  return candidates.find((p) => {
    try {
      return fs.existsSync(p);
    } catch {
      return false;
    }
  });
}

function manualFallback(inputPath, opts, reason) {
  const abs = path.resolve(inputPath);
  process.stderr.write(
    `\n[render-image] Could not launch a headless browser: ${reason}\n` +
      `[render-image] The HTML was NOT deleted. Render it manually:\n` +
      `  1) Open the file in Chrome and use "Capture node screenshot" in DevTools, or\n` +
      `  2) Run: chrome --headless --screenshot=out.png --window-size=${opts.width},${opts.height} "file://${abs}"\n` +
      `  3) Or set PUPPETEER_EXECUTABLE_PATH to a Chrome binary and re-run this script.\n\n`
  );
  // Plain-text fallback row on stdout so the path is easy to copy/paste.
  process.stdout.write(`HTML_READY\t${abs}\twidth=${opts.width}\theight=${opts.height}\n`);
}

async function main() {
  const { positional, opts } = parseArgs(process.argv.slice(2));
  const [inputPath, outputPath] = positional;

  if (!inputPath || !outputPath) {
    process.stderr.write(
      "Usage: node render-image.js <input.html> <output.png> " +
        "[--width=1080] [--height=1440] [--scale=2] [--full]\n"
    );
    process.exit(2);
  }
  if (!fs.existsSync(inputPath)) {
    process.stderr.write(`[render-image] Input HTML not found: ${inputPath}\n`);
    process.exit(2);
  }

  let puppeteer;
  try {
    puppeteer = require("puppeteer");
  } catch {
    manualFallback(inputPath, opts, "the 'puppeteer' package is not installed (run `npm install` in this scripts/ directory)");
    process.exit(1);
  }

  // Default args contain no sandbox-disabling flags. Linux/container users that
  // need them can pass them via RENDER_CHROME_ARGS (see render-image-setup.md).
  const extraArgs = (process.env.RENDER_CHROME_ARGS || "")
    .split(/\s+/)
    .filter(Boolean);
  const launchOptions = {
    headless: "new",
    args: ["--force-color-profile=srgb", ...extraArgs],
  };

  let browser;
  try {
    browser = await puppeteer.launch(launchOptions);
  } catch (bundledErr) {
    const systemChrome = findSystemChrome();
    if (!systemChrome) {
      manualFallback(
        inputPath,
        opts,
        `bundled Chromium failed (${bundledErr.message}) and no system Chrome was found`
      );
      process.exit(1);
    }
    try {
      browser = await puppeteer.launch({ ...launchOptions, executablePath: systemChrome });
      process.stderr.write(`[render-image] Using system Chrome at ${systemChrome}\n`);
    } catch (systemErr) {
      manualFallback(inputPath, opts, `no launchable browser (${systemErr.message})`);
      process.exit(1);
    }
  }

  try {
    const page = await browser.newPage();
    await page.setViewport({
      width: opts.width,
      height: opts.height,
      deviceScaleFactor: opts.scale,
    });
    await page.goto("file://" + path.resolve(inputPath), { waitUntil: "networkidle0" });
    await page.screenshot({ path: outputPath, fullPage: opts.full });
    process.stdout.write(`OK\t${path.resolve(outputPath)}\t${opts.width}x${opts.height}@${opts.scale}x\n`);
  } finally {
    await browser.close();
  }
}

main().catch((err) => {
  process.stderr.write(`[render-image] Unexpected error: ${err.stack || err}\n`);
  process.exit(1);
});
