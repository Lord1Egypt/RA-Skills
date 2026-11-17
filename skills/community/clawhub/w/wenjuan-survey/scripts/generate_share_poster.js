#!/usr/bin/env node
"use strict";

const fs = require("fs").promises;
const path = require("path");
const os = require("os");
const sharp = require("sharp");
const QRCode = require("qrcode");

const ASSETS_DIR = path.resolve(__dirname, "../assets");

/** 模板设计稿尺寸（四套模板均为 1080×1920） */
const TEMPLATE_WIDTH = 1080;
const TEMPLATE_HEIGHT = 1920;
/** 最终输出尺寸，与 Downloads/poster.png 一致（900×1350） */
const OUTPUT_WIDTH = 900;
const OUTPUT_HEIGHT = 1350;

/**
 * 分享海报模板：每次生成随机选用其一。
 * qr* 为二维码叠放位置（相对 1080×1920）；title* 为顶部标题样式。
 */
const POSTER_TEMPLATES = [
  {
    id: "template_1",
    file: "share_poster_template.png",
    titleFill: "#0f4db8",
    titleBaselineY: 250,
    qrLeft: 770,
    qrTop: 1631,
    qrSize: 168,
  },
  {
    id: "template_2",
    file: "share_poster_template_2.png",
    titleFill: "#0f4db8",
    titleBaselineY: 260,
    qrLeft: 767,
    qrTop: 1643,
    qrSize: 210,
  },
  {
    id: "template_3",
    file: "share_poster_template_3.png",
    titleFill: "#ffffff",
    titleBaselineY: 280,
    titleStroke: "rgba(8, 20, 120, 0.45)",
    qrLeft: 800,
    qrTop: 1685,
    qrSize: 220,
  },
  {
    id: "template_4",
    file: "share_poster_template_4.png",
    titleFill: "#0f4db8",
    titleBaselineY: 250,
    // 左下白色圆角占位区 133,1227,259×258
    qrLeft: 148,
    qrTop: 1241,
    qrSize: 230,
  },
].map((item) => ({
  ...item,
  path: path.join(ASSETS_DIR, item.file),
}));

const DEFAULT_TEMPLATE = POSTER_TEMPLATES[0].path;

function pickRandomTemplate() {
  return POSTER_TEMPLATES[Math.floor(Math.random() * POSTER_TEMPLATES.length)];
}

function resolveTemplate(templatePath) {
  if (!templatePath) return pickRandomTemplate();
  const resolved = path.resolve(templatePath);
  const matched = POSTER_TEMPLATES.find((item) => item.path === resolved);
  if (matched) return matched;
  // 自定义路径：沿用模板 1 的布局参数
  return { ...POSTER_TEMPLATES[0], id: "custom", path: resolved, file: path.basename(resolved) };
}

function escapeXml(value) {
  return String(value || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

function charWidth(char) {
  return /[\u0000-\u00ff]/.test(char) ? 0.55 : 1;
}

function wrapTitle(title, maxUnits, maxLines = 2) {
  const chars = Array.from(String(title || "").replace(/\s+/g, " ").trim());
  const lines = [];
  let line = "";
  let units = 0;

  for (let i = 0; i < chars.length; i++) {
    const char = chars[i];
    const width = charWidth(char);
    if (line && units + width > maxUnits) {
      lines.push(line.trim());
      line = "";
      units = 0;
      if (lines.length === maxLines) {
        const last = lines[maxLines - 1];
        lines[maxLines - 1] = `${last.slice(0, Math.max(1, last.length - 1))}…`;
        return lines;
      }
    }
    line += char;
    units += width;
  }

  if (line.trim() && lines.length < maxLines) lines.push(line.trim());
  return lines.length ? lines : ["问卷调查"];
}

function titleSvg(title, width, height, template) {
  const normalized = String(title || "").trim();
  const fontSize =
    normalized.length <= 14 ? 64 : normalized.length <= 28 ? 54 : 46;
  const lines = wrapTitle(normalized, (width - 120) / fontSize, 2);
  const lineHeight = Math.round(fontSize * 1.28);
  const baselineY = template.titleBaselineY || 250;
  const startY = baselineY - ((lines.length - 1) * lineHeight) / 2;
  const tspans = lines
    .map(
      (line, index) =>
        `<tspan x="${Math.round(width / 2)}" y="${Math.round(
          startY + index * lineHeight
        )}">${escapeXml(line)}</tspan>`
    )
    .join("");
  const stroke = template.titleStroke
    ? `paint-order: stroke;
          stroke: ${template.titleStroke};
          stroke-width: 6px;
          stroke-linejoin: round;`
    : "";

  return Buffer.from(`
    <svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
      <style>
        .title {
          fill: ${template.titleFill || "#0f4db8"};
          font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
          font-size: ${fontSize}px;
          font-weight: 700;
          text-anchor: middle;
          ${stroke}
        }
      </style>
      <text class="title">${tspans}</text>
    </svg>
  `);
}

function safeFilename(value) {
  const safe = String(value || "survey")
    .replace(/[<>:"/\\|?*\u0000-\u001f]/g, "_")
    .replace(/\s+/g, "_")
    .slice(0, 60);
  return safe || "survey";
}

async function generateSharePoster({
  title,
  surveyLink,
  projectId = "",
  outputPath = "",
  templatePath,
}) {
  if (!surveyLink || !/^https?:\/\//i.test(String(surveyLink))) {
    throw new Error("生成分享海报需要有效的 http(s) 答题链接");
  }

  const template = resolveTemplate(templatePath);
  const metadata = await sharp(template.path).metadata();
  if (!metadata.width || !metadata.height) {
    throw new Error("无法读取分享海报模板尺寸");
  }

  const scaleX = metadata.width / TEMPLATE_WIDTH;
  const scaleY = metadata.height / TEMPLATE_HEIGHT;
  const qrSize = Math.max(64, Math.round(template.qrSize * Math.min(scaleX, scaleY)));
  const qrLeft = Math.round(template.qrLeft * scaleX);
  const qrTop = Math.round(template.qrTop * scaleY);

  const qr = await QRCode.toBuffer(String(surveyLink), {
    type: "png",
    errorCorrectionLevel: "M",
    width: qrSize,
    margin: 1,
    color: { dark: "#000000", light: "#ffffff" },
  });

  const resolvedOutput = outputPath
    ? path.resolve(outputPath)
    : path.join(
        os.homedir(),
        ".wenjuan",
        "posters",
        `${safeFilename(title)}${projectId ? `-${projectId}` : ""}.png`
      );
  await fs.mkdir(path.dirname(resolvedOutput), { recursive: true, mode: 0o700 });

  const composed = await sharp(template.path)
    .composite([
      {
        input: titleSvg(title, metadata.width, metadata.height, template),
        left: 0,
        top: 0,
      },
      { input: qr, left: qrLeft, top: qrTop },
    ])
    .png()
    .toBuffer();

  await sharp(composed)
    .resize(OUTPUT_WIDTH, OUTPUT_HEIGHT, { fit: "fill" })
    .png()
    .toFile(resolvedOutput);

  return resolvedOutput;
}

function parseArgs(argv) {
  const result = {};
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === "--title" && argv[i + 1]) result.title = argv[++i];
    else if (arg === "--url" && argv[i + 1]) result.surveyLink = argv[++i];
    else if (arg === "--project-id" && argv[i + 1]) result.projectId = argv[++i];
    else if ((arg === "--output" || arg === "-o") && argv[i + 1]) {
      result.outputPath = argv[++i];
    } else if (arg === "--template" && argv[i + 1]) {
      result.templatePath = argv[++i];
    }
  }
  return result;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.title || !args.surveyLink) {
    console.error(
      '用法: node generate_share_poster.js --title "项目标题" --url "https://www.wenjuan.com/s/xxx" [-o poster.png] [--template path]'
    );
    process.exit(1);
  }
  const output = await generateSharePoster(args);
  console.log(output);
}

module.exports = {
  DEFAULT_TEMPLATE,
  POSTER_TEMPLATES,
  OUTPUT_WIDTH,
  OUTPUT_HEIGHT,
  pickRandomTemplate,
  generateSharePoster,
  wrapTitle,
};

if (require.main === module) {
  main().catch((error) => {
    console.error(`生成分享海报失败: ${error.message}`);
    process.exit(1);
  });
}
