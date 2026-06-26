#!/usr/bin/env node
/**
 * 批量生成二维码 (Node.js 版)
 *
 * 用法:
 *   node scripts/batch_generate.js --input <文件> --mode url   [选项]
 *   node scripts/batch_generate.js --input <文件> --mode image --output-dir <目录> [选项]
 *
 * 输出 JSON 格式与 Python 版一致。
 */

const https = require("https");
const http = require("http");
const fs = require("fs");
const path = require("path");
const { URLSearchParams } = require("url");

const API_BASE = "https://api.2dcode.biz/v1/create-qr-code";

// ── 参数解析 ──────────────────────────────────────────────

function parseArgs(argv) {
  const args = {
    input: null, mode: null, column: null,
    outputTxt: null, outputDir: null,
    zip: false, useApi: false,
    size: "400", format: "png", ecc: "M", border: 2,
  };
  for (let i = 2; i < argv.length; i++) {
    switch (argv[i]) {
      case "--input": args.input = argv[++i]; break;
      case "--mode": args.mode = argv[++i]; break;
      case "--column": args.column = argv[++i]; break;
      case "--output-txt": args.outputTxt = argv[++i]; break;
      case "--output-dir": args.outputDir = argv[++i]; break;
      case "--zip": args.zip = true; break;
      case "--use-api": args.useApi = true; break;
      case "--size": args.size = argv[++i]; break;
      case "--format": args.format = argv[++i]; break;
      case "--error-correction": args.ecc = argv[++i]; break;
      case "--border": args.border = parseInt(argv[++i]); break;
    }
  }
  return args;
}

// ── 文件读取 ──────────────────────────────────────────────

const GEN_KEYWORDS = ["data", "text", "content", "url", "link", "内容", "文本", "数据", "链接", "网址"];

function readTxt(filepath) {
  return fs.readFileSync(filepath, "utf-8").split("\n").map((l) => l.trim()).filter(Boolean);
}

function readCsv(filepath) {
  const lines = fs.readFileSync(filepath, "utf-8").replace(/^\uFEFF/, "").split("\n").filter(Boolean);
  return lines.map((line) => parseCsvLine(line));
}

function parseCsvLine(line) {
  const result = [];
  let current = "", inQuotes = false;
  for (const ch of line) {
    if (ch === '"') { inQuotes = !inQuotes; }
    else if (ch === "," && !inQuotes) { result.push(current.trim()); current = ""; }
    else { current += ch; }
  }
  result.push(current.trim());
  return result;
}

function readExcel(filepath) {
  const XLSX = require("xlsx");
  const wb = XLSX.readFile(filepath);
  const ws = wb.Sheets[wb.SheetNames[0]];
  const rows = XLSX.utils.sheet_to_json(ws, { header: 1, defval: "" });
  return rows.map((r) => r.map((c) => String(c ?? "")));
}

function extractColumn(rows, column) {
  if (!rows.length) return { items: [], needCol: null };
  const headers = rows[0];
  const dataRows = rows.slice(1);

  if (column != null) {
    const idx = resolveColIdx(headers, column);
    if (idx == null) return { items: null, needCol: { need_column: true, columns: headers, preview: rows.slice(0, 6), message: `找不到列 '${column}'，请从以下列中选择` } };
    return { items: dataRows.map((r) => (r[idx] || "").trim()).filter(Boolean), needCol: null };
  }

  const idx = autoDetectCol(headers, GEN_KEYWORDS);
  if (idx == null) return { items: null, needCol: { need_column: true, columns: headers, preview: rows.slice(0, 6), message: "无法自动判断数据列，请指定 --column 参数" } };
  return { items: dataRows.map((r) => (r[idx] || "").trim()).filter(Boolean), needCol: null };
}

function resolveColIdx(headers, column) {
  const num = parseInt(column);
  if (!isNaN(num) && num >= 0 && num < headers.length) return num;
  const low = String(column).toLowerCase().trim();
  for (let i = 0; i < headers.length; i++) {
    if (headers[i].trim().toLowerCase() === low) return i;
  }
  return null;
}

function autoDetectCol(headers, keywords) {
  for (let i = 0; i < headers.length; i++) {
    const h = headers[i].trim().toLowerCase();
    for (const kw of keywords) { if (h.includes(kw)) return i; }
  }
  return headers.length === 1 ? 0 : null;
}

// ── URL 构建 ──────────────────────────────────────────────

function buildApiUrl(data, size, fmt, ecc, border) {
  const params = new URLSearchParams({ data, size });
  if (fmt !== "png") params.set("format", fmt);
  if (ecc !== "M") params.set("error_correction", ecc);
  if (border !== 2) params.set("border", String(border));
  return `${API_BASE}?${params.toString()}`;
}

// ── 下载 ──────────────────────────────────────────────

function download(url, dest) {
  return new Promise((resolve, reject) => {
    const mod = url.startsWith("https") ? https : http;
    const file = fs.createWriteStream(dest);
    mod.get(url, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        file.close(); fs.unlinkSync(dest);
        return download(res.headers.location, dest).then(resolve, reject);
      }
      res.pipe(file);
      file.on("finish", () => { file.close(); resolve(); });
    }).on("error", (e) => { file.close(); if (fs.existsSync(dest)) fs.unlinkSync(dest); reject(e); });
  });
}

// ── 本地生成 ──────────────────────────────────────────────

async function generateLocal(data, filepath, fmt, ecc, border) {
  const QRCode = require("qrcode");
  const eccMap = { L: "low", M: "medium", Q: "quartile", H: "high" };
  const opts = { errorCorrectionLevel: eccMap[ecc] || "medium", margin: border };

  if (fmt === "svg") {
    const svg = await QRCode.toString(data, { ...opts, type: "svg" });
    fs.writeFileSync(filepath, svg);
  } else {
    await QRCode.toFile(filepath, data, opts);
  }
}

function checkLocalAvailable() {
  try { require("qrcode"); return true; } catch { return false; }
}

// ── 模式执行 ──────────────────────────────────────────────

function runUrlMode(items, args) {
  const sizeStr = `${args.size}x${args.size}`;
  const urls = items.map((d) => buildApiUrl(d, sizeStr, args.format, args.ecc, args.border));

  let outputTxt = null;
  if (args.outputTxt) {
    outputTxt = path.resolve(args.outputTxt);
    const dir = path.dirname(outputTxt);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(outputTxt, urls.join("\n"), "utf-8");
  }

  console.log(JSON.stringify({ mode: "url", total: urls.length, urls, output_txt: outputTxt }));
}

async function runImageMode(items, args) {
  if (!args.outputDir) {
    console.log(JSON.stringify({ error: "image 模式必须指定 --output-dir" }));
    process.exit(1);
  }

  const outputDir = path.resolve(args.outputDir);
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

  const sizeInt = parseInt(args.size.split("x")[0]);
  const sizeStr = `${sizeInt}x${sizeInt}`;
  const useLocal = !args.useApi && checkLocalAvailable();

  if (!args.useApi && !useLocal) {
    console.log(JSON.stringify({ error: "本地 qrcode 库未安装，请先执行 npm install，或使用 --use-api 参数走远程 API" }));
    process.exit(1);
  }

  let success = 0, failed = 0, apiFallback = 0;
  const errors = [];

  for (let i = 0; i < items.length; i++) {
    const data = items[i];
    const filename = `${i + 1}.${args.format}`;
    const filepath = path.join(outputDir, filename);
    try {
      if (useLocal) {
        try {
          await generateLocal(data, filepath, args.format, args.ecc, args.border);
        } catch {
          await download(buildApiUrl(data, sizeStr, args.format, args.ecc, args.border), filepath);
          apiFallback++;
        }
      } else {
        await download(buildApiUrl(data, sizeStr, args.format, args.ecc, args.border), filepath);
      }
      success++;
    } catch (e) {
      failed++;
      errors.push({ index: i + 1, data, error: e.message });
    }
  }

  const result = {
    mode: "image", source: useLocal ? "local" : "api",
    total: items.length, success, failed, api_fallback: apiFallback,
    output_dir: outputDir, zip_file: null, errors,
  };

  if (args.zip && success > 0) {
    const archiver = require("archiver");
    const zipPath = outputDir + ".zip";
    await new Promise((resolve, reject) => {
      const out = fs.createWriteStream(zipPath);
      const archive = archiver("zip");
      out.on("close", resolve);
      archive.on("error", reject);
      archive.pipe(out);
      archive.directory(outputDir, false);
      archive.finalize();
    });
    result.zip_file = zipPath;
  }

  console.log(JSON.stringify(result));
}

// ── 入口 ──────────────────────────────────────────────

async function main() {
  const args = parseArgs(process.argv);
  if (!args.input || !args.mode) {
    console.log(JSON.stringify({ error: "用法: node batch_generate.js --input <文件> --mode url|image [选项]" }));
    process.exit(1);
  }

  const ext = path.extname(args.input).toLowerCase();
  let rows, items, needCol;

  if (ext === ".txt") {
    items = readTxt(args.input);
    needCol = null;
  } else if (ext === ".csv") {
    rows = readCsv(args.input);
    ({ items, needCol } = extractColumn(rows, args.column));
  } else if (ext === ".xlsx" || ext === ".xls") {
    rows = readExcel(args.input);
    ({ items, needCol } = extractColumn(rows, args.column));
  } else {
    console.log(JSON.stringify({ error: `不支持的文件格式: ${ext}，支持 txt/csv/xlsx` }));
    process.exit(1);
  }

  if (needCol) { console.log(JSON.stringify(needCol)); process.exit(0); }
  if (!items || !items.length) { console.log(JSON.stringify({ error: "文件中未读取到有效数据" })); process.exit(1); }

  if (args.mode === "url") {
    runUrlMode(items, args);
  } else {
    await runImageMode(items, args);
  }
}

main();
