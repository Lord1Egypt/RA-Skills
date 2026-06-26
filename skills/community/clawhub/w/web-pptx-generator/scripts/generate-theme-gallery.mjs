#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { listThemes } from "./theme-bundles.mjs";

const scenes = {
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

const outDir = path.resolve(process.cwd(), "dist/gallery");
fs.mkdirSync(outDir, { recursive: true });

const commands = listThemes().map((theme) => {
  const title = theme.replaceAll("-", " ");
  const scene = scenes[theme] ?? "project-report";
  const out = path.join(outDir, `${theme}.html`);
  return { theme, scene, title, out };
});

for (const item of commands) {
  execFileSync(
    process.execPath,
    [
      path.resolve(process.cwd(), "scripts/generate-slide-html.mjs"),
      "--scene", item.scene,
      "--title", item.title,
      "--density", "medium",
      "--out", item.out,
    ],
    { stdio: "inherit" },
  );
}

const manifest = commands.map((item) => ({
  theme: item.theme,
  scene: item.scene,
  title: item.title,
  file: path.relative(process.cwd(), item.out),
}));

fs.writeFileSync(
  path.join(outDir, "manifest.json"),
  JSON.stringify(manifest, null, 2),
  "utf8",
);

const indexHtml = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Web Slides Theme Gallery</title>
  <style>
    * { box-sizing: border-box; }
    body { margin: 0; font-family: Inter, "PingFang SC", "Microsoft YaHei", sans-serif; background: linear-gradient(180deg, #0b1020, #111827); color: #f8fafc; }
    .wrap { max-width: 1240px; margin: 0 auto; padding: 48px 24px 80px; }
    h1 { margin: 0; font-size: clamp(2.4rem, 5vw, 4.8rem); }
    p { color: #94a3b8; line-height: 1.7; }
    .grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; margin-top: 28px; }
    .card { display: block; text-decoration: none; color: inherit; border-radius: 24px; padding: 22px; border: 1px solid rgba(255,255,255,0.08); background: rgba(255,255,255,0.04); box-shadow: 0 20px 60px rgba(0,0,0,0.20); }
    .theme { font-size: 1.2rem; font-weight: 700; margin-bottom: 10px; }
    .scene { color: #cbd5e1; font-size: 0.95rem; }
    .link { margin-top: 18px; color: #67e8f9; font-size: 0.9rem; letter-spacing: 0.08em; text-transform: uppercase; }
    @media (max-width: 960px) { .grid { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Web Slides Theme Gallery</h1>
    <p>12 套旗舰主题的 HTML 样张入口。每个页面都是单文件生成结果，可直接打开评估视觉质量与移动端表现。</p>
    <div class="grid">
      ${manifest.map((item) => `
        <a class="card" href="./${path.basename(item.file)}">
          <div class="theme">${item.theme}</div>
          <div class="scene">${item.scene}</div>
          <div class="link">Open Sample</div>
        </a>
      `).join("")}
    </div>
  </div>
</body>
</html>`;

fs.writeFileSync(path.join(outDir, "index.html"), indexHtml, "utf8");

console.log(JSON.stringify({
  outDir,
  themes: commands.length,
  manifest: path.join(outDir, "manifest.json"),
}, null, 2));
