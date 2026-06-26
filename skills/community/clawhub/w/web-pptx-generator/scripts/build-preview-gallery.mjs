#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { listThemes } from "./theme-bundles.mjs";

const repoRoot = process.cwd();
const outDir = path.resolve(repoRoot, "dist/previews");
fs.mkdirSync(outDir, { recursive: true });

const sceneByTheme = {
  "cyber-grid": "ai-product-launch",
  "executive-dark": "board-review",
  "executive-light": "consulting-proposal",
  "glass-future": "aigc-solution",
  "data-intelligence": "bi-report",
  "startup-pitch": "investor-pitch",
  "product-launch": "new-product-launch",
  "dev-summit": "tech-talk",
  "luxury-black-gold": "premium-brand-launch",
  "editorial-serif": "whitepaper",
  "neo-minimal": "design-proposal",
  "creative-motion": "campaign-proposal",
};

function runNode(script, args) {
  execFileSync(process.execPath, [path.join(repoRoot, script), ...args], {
    stdio: "inherit",
    cwd: repoRoot,
  });
}

const manifest = [];

for (const theme of listThemes()) {
  const html = path.join(outDir, `${theme}.html`);
  const png = path.join(outDir, `${theme}.png`);
  const mobilePng = path.join(outDir, `${theme}.mobile.png`);
  const scene = sceneByTheme[theme] ?? "project-report";

  runNode("scripts/generate-slide-html.mjs", [
    "--theme",
    theme,
    "--scene",
    scene,
    "--title",
    theme,
    "--out",
    html,
  ]);
  runNode("scripts/render-preview.mjs", ["--input", html, "--output", png]);
  runNode("scripts/render-preview.mjs", ["--input", html, "--output", mobilePng, "--mobile"]);

  manifest.push({
    theme,
    scene,
    html: path.relative(repoRoot, html),
    desktopPreview: path.relative(repoRoot, png),
    mobilePreview: path.relative(repoRoot, mobilePng),
  });
}

const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Web Slides Preview Gallery</title>
  <style>
    * { box-sizing: border-box; }
    body { margin: 0; background: #08111f; color: #f8fafc; font-family: Inter, "PingFang SC", sans-serif; }
    .wrap { max-width: 1480px; margin: 0 auto; padding: 40px 24px 80px; }
    h1 { margin: 0; font-size: clamp(2.4rem, 5vw, 4.8rem); }
    p { color: #94a3b8; line-height: 1.7; }
    .grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px; margin-top: 28px; }
    .card { border: 1px solid rgba(255,255,255,0.08); border-radius: 28px; background: rgba(255,255,255,0.03); padding: 20px; }
    .meta { display: flex; justify-content: space-between; gap: 20px; align-items: center; margin-bottom: 14px; }
    .theme { font-size: 1.1rem; font-weight: 700; }
    .scene { color: #67e8f9; font-size: 0.92rem; }
    .preview-grid { display: grid; grid-template-columns: 1.3fr 0.7fr; gap: 16px; align-items: start; }
    .preview-grid img { width: 100%; border-radius: 18px; display: block; border: 1px solid rgba(255,255,255,0.08); background: #020617; }
    .links { margin-top: 14px; display: flex; gap: 16px; }
    .links a { color: #7dd3fc; text-decoration: none; font-size: 0.92rem; }
    @media (max-width: 1080px) {
      .grid { grid-template-columns: 1fr; }
      .preview-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Web Slides Preview Gallery</h1>
    <p>桌面与移动端预览一并导出，方便在上架前集中检查 12 套主题的首屏效果与小屏表现。</p>
    <div class="grid">
      ${manifest.map((item) => `
        <div class="card">
          <div class="meta">
            <div class="theme">${item.theme}</div>
            <div class="scene">${item.scene}</div>
          </div>
          <div class="preview-grid">
            <img src="./${path.basename(item.desktopPreview)}" alt="${item.theme} desktop preview">
            <img src="./${path.basename(item.mobilePreview)}" alt="${item.theme} mobile preview">
          </div>
          <div class="links">
            <a href="./${path.basename(item.html)}">Open HTML</a>
            <a href="./${path.basename(item.desktopPreview)}">Desktop PNG</a>
            <a href="./${path.basename(item.mobilePreview)}">Mobile PNG</a>
          </div>
        </div>
      `).join("")}
    </div>
  </div>
</body>
</html>`;

fs.writeFileSync(path.join(outDir, "manifest.json"), JSON.stringify(manifest, null, 2), "utf8");
fs.writeFileSync(path.join(outDir, "index.html"), html, "utf8");

console.log(JSON.stringify({
  ok: true,
  outDir,
  themes: manifest.length,
}, null, 2));
