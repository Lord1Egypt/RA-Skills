#!/usr/bin/env node
/**
 * 批量解码二维码 - 本地解码 (Node.js 版)
 *
 * 用法:
 *   node scripts/batch_decode.js --input <文件> [--column <列>] [--output-txt <路径>]
 *
 * 输出 JSON 格式与 Python 版一致。
 */

const https = require("https");
const http = require("http");
const fs = require("fs");
const os = require("os");
const path = require("path");

const FAIL = "未解析到二维码";

// ── 参数解析 ──────────────────────────────────────────────

function parseArgs(argv) {
  const args = { input: null, column: null, outputTxt: null };
  for (let i = 2; i < argv.length; i++) {
    switch (argv[i]) {
      case "--input": args.input = argv[++i]; break;
      case "--column": args.column = argv[++i]; break;
      case "--output-txt": args.outputTxt = argv[++i]; break;
    }
  }
  return args;
}

// ── HTTP 工具 ──────────────────────────────────────────────

function isUrl(s) { return s.startsWith("http://") || s.startsWith("https://"); }

function downloadToTemp(url) {
  return new Promise((resolve, reject) => {
    const ext = path.extname(url.split("?")[0]) || ".png";
    const tmp = path.join(os.tmpdir(), `qr_${Date.now()}_${Math.random().toString(36).slice(2)}${ext}`);
    const mod = url.startsWith("https") ? https : http;
    const file = fs.createWriteStream(tmp);
    mod.get(url, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        file.close(); fs.unlinkSync(tmp);
        return downloadToTemp(res.headers.location).then(resolve, reject);
      }
      res.pipe(file);
      file.on("finish", () => { file.close(); resolve(tmp); });
    }).on("error", (e) => { file.close(); if (fs.existsSync(tmp)) fs.unlinkSync(tmp); reject(e); });
  });
}

// ── 解码函数 ──────────────────────────────────────────────

async function tryWechatQr(source) {
  try {
    const { scan } = await import("qr-scanner-wechat");
    const sharp = require("sharp");

    let imgPath = source;
    let tmpPath = null;
    if (isUrl(source)) {
      tmpPath = await downloadToTemp(source);
      imgPath = tmpPath;
    }
    try {
      const { data, info } = await sharp(imgPath)
        .ensureAlpha()
        .raw()
        .toBuffer({ resolveWithObject: true });
      const result = await scan({
        data: Uint8ClampedArray.from(data),
        width: info.width,
        height: info.height,
      });
      return result?.text || null;
    } finally {
      if (tmpPath && fs.existsSync(tmpPath)) fs.unlinkSync(tmpPath);
    }
  } catch {
    return null;
  }
}

async function decodeSingle(source) {
  const local = await tryWechatQr(source);
  return local || FAIL;
}

// ── 文件读写 ──────────────────────────────────────────────

const DECODE_KEYWORDS = ["url", "link", "image", "img", "图片", "链接", "网址", "二维码"];

function readTxt(fp) { return fs.readFileSync(fp, "utf-8").split("\n").map((l) => l.trim()).filter(Boolean); }

function parseCsvLine(line) {
  const result = []; let current = "", inQ = false;
  for (const ch of line) { if (ch === '"') inQ = !inQ; else if (ch === "," && !inQ) { result.push(current.trim()); current = ""; } else current += ch; }
  result.push(current.trim()); return result;
}

function readCsv(fp) { return fs.readFileSync(fp, "utf-8").replace(/^\uFEFF/, "").split("\n").filter(Boolean).map(parseCsvLine); }

function readExcel(fp) {
  const XLSX = require("xlsx");
  const wb = XLSX.readFile(fp);
  return XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]], { header: 1, defval: "" }).map((r) => r.map((c) => String(c ?? "")));
}

function resolveCol(headers, column) {
  if (column != null) {
    const num = parseInt(column);
    if (!isNaN(num) && num >= 0 && num < headers.length) return num;
    const low = String(column).toLowerCase().trim();
    for (let i = 0; i < headers.length; i++) { if (headers[i].trim().toLowerCase() === low) return i; }
    return null;
  }
  for (let i = 0; i < headers.length; i++) {
    const h = headers[i].trim().toLowerCase();
    for (const kw of DECODE_KEYWORDS) { if (h.includes(kw)) return i; }
  }
  return headers.length === 1 ? 0 : null;
}

async function processTxt(inputPath, outputTxt) {
  const lines = readTxt(inputPath);
  const results = [];
  let success = 0;
  for (const line of lines) {
    const d = await decodeSingle(line);
    results.push(d);
    if (d !== FAIL) success++;
  }
  const stem = path.basename(inputPath, path.extname(inputPath));
  const outPath = outputTxt || path.join(path.dirname(inputPath), `${stem}_decoded.txt`);
  fs.writeFileSync(outPath, results.join("\n"), "utf-8");
  return { total: lines.length, success, failed: lines.length - success, output_file: path.resolve(outPath), output_txt: path.resolve(outPath) };
}

async function processCsv(inputPath, column, outputTxt) {
  const rows = readCsv(inputPath);
  if (!rows.length) return { error: "CSV 文件为空" };
  const headers = rows[0];
  const dataRows = rows.slice(1);
  const colIdx = resolveCol(headers, column);
  if (colIdx == null) return { need_column: true, columns: headers, preview: rows.slice(0, 6), message: column == null ? "无法自动判断 URL 列，请指定 --column 参数" : `找不到列 '${column}'` };

  const decoded = [];
  let success = 0;
  for (const row of dataRows) {
    const url = (row[colIdx] || "").trim();
    const d = url ? await decodeSingle(url) : FAIL;
    decoded.push(d);
    if (d !== FAIL) success++;
  }

  if (outputTxt) {
    fs.writeFileSync(outputTxt, decoded.join("\n"), "utf-8");
    return { total: dataRows.length, success, failed: dataRows.length - success, output_file: path.resolve(inputPath), output_txt: path.resolve(outputTxt) };
  }

  headers.push("解码结果");
  dataRows.forEach((r, i) => r.push(decoded[i]));
  const csvContent = [headers, ...dataRows].map((r) => r.map((c) => `"${String(c).replace(/"/g, '""')}"`).join(",")).join("\n");
  fs.writeFileSync(inputPath, "\uFEFF" + csvContent, "utf-8");
  return { total: dataRows.length, success, failed: dataRows.length - success, output_file: path.resolve(inputPath), output_txt: null };
}

async function processExcel(inputPath, column, outputTxt) {
  const XLSX = require("xlsx");
  const rows = readExcel(inputPath);
  if (!rows.length) return { error: "Excel 文件为空" };
  const headers = rows[0];
  const dataRows = rows.slice(1);
  const colIdx = resolveCol(headers, column);
  if (colIdx == null) return { need_column: true, columns: headers, preview: rows.slice(0, 6), message: column == null ? "无法自动判断 URL 列，请指定 --column 参数" : `找不到列 '${column}'` };

  const decoded = [];
  let success = 0;
  for (const row of dataRows) {
    const url = (row[colIdx] || "").trim();
    const d = url ? await decodeSingle(url) : FAIL;
    decoded.push(d);
    if (d !== FAIL) success++;
  }

  if (outputTxt) {
    fs.writeFileSync(outputTxt, decoded.join("\n"), "utf-8");
    return { total: dataRows.length, success, failed: dataRows.length - success, output_file: path.resolve(inputPath), output_txt: path.resolve(outputTxt) };
  }

  headers.push("解码结果");
  dataRows.forEach((r, i) => r.push(decoded[i]));
  const allRows = [headers, ...dataRows];
  const wb = XLSX.utils.book_new();
  const ws = XLSX.utils.aoa_to_sheet(allRows);
  XLSX.utils.book_append_sheet(wb, ws);
  XLSX.writeFile(wb, inputPath);
  return { total: dataRows.length, success, failed: dataRows.length - success, output_file: path.resolve(inputPath), output_txt: null };
}

// ── 入口 ──────────────────────────────────────────────

async function main() {
  const args = parseArgs(process.argv);
  if (!args.input) { console.log(JSON.stringify({ error: "用法: node batch_decode.js --input <文件> [选项]" })); process.exit(1); }

  const ext = path.extname(args.input).toLowerCase();
  let result;
  if (ext === ".txt") result = await processTxt(args.input, args.outputTxt);
  else if (ext === ".csv") result = await processCsv(args.input, args.column, args.outputTxt);
  else if (ext === ".xlsx" || ext === ".xls") result = await processExcel(args.input, args.column, args.outputTxt);
  else result = { error: `不支持的文件格式: ${ext}，支持 txt/csv/xlsx` };

  console.log(JSON.stringify(result));
  if (result.error) process.exit(1);
}

main();
