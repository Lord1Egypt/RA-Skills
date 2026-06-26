#!/usr/bin/env node
/**
 * QR Code Generator - 生成二维码并保存到本地 (Node.js 版)
 *
 * 用法:
 *   node scripts/generate.js --data <文本> --output <路径> [选项]
 *
 * 输出 JSON:
 *   {"url": "...", "file": "..."}
 *   {"error": "..."}
 */

const https = require("https");
const http = require("http");
const fs = require("fs");
const path = require("path");
const { URL, URLSearchParams } = require("url");

const API_BASE = "https://api.2dcode.biz/v1/create-qr-code";

function parseArgs(argv) {
  const args = { size: "400x400", format: "png", ecc: "M", border: 2 };
  for (let i = 2; i < argv.length; i++) {
    switch (argv[i]) {
      case "--data": args.data = argv[++i]; break;
      case "--output": args.output = argv[++i]; break;
      case "--size": args.size = argv[++i]; break;
      case "--format": args.format = argv[++i]; break;
      case "--error-correction": args.ecc = argv[++i]; break;
      case "--border": args.border = parseInt(argv[++i]); break;
    }
  }
  return args;
}

function buildUrl(data, size, fmt, ecc, border) {
  const params = new URLSearchParams({ data, size });
  if (fmt !== "png") params.set("format", fmt);
  if (ecc !== "M") params.set("error_correction", ecc);
  if (border !== 2) params.set("border", String(border));
  return `${API_BASE}?${params.toString()}`;
}

function download(url, dest) {
  return new Promise((resolve, reject) => {
    const mod = url.startsWith("https") ? https : http;
    const file = fs.createWriteStream(dest);
    mod.get(url, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        file.close();
        fs.unlinkSync(dest);
        return download(res.headers.location, dest).then(resolve, reject);
      }
      res.pipe(file);
      file.on("finish", () => { file.close(); resolve(); });
    }).on("error", (e) => { file.close(); fs.unlinkSync(dest); reject(e); });
  });
}

async function main() {
  const args = parseArgs(process.argv);
  if (!args.data || !args.output) {
    console.log(JSON.stringify({ error: "用法: node generate.js --data <文本> --output <路径>" }));
    process.exit(1);
  }

  const url = buildUrl(args.data, args.size, args.format, args.ecc, args.border);
  const outputPath = path.resolve(args.output);
  const dir = path.dirname(outputPath);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

  try {
    await download(url, outputPath);
    console.log(JSON.stringify({ url, file: outputPath }));
  } catch (e) {
    console.log(JSON.stringify({ error: `下载失败: ${e.message}` }));
    process.exit(1);
  }
}

main();
