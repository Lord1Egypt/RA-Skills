#!/usr/bin/env node
/**
 * 批量解码二维码 (Node.js 版)
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
const { URL } = require("url");

const API_ENDPOINT = "https://api.2dcode.biz/v1/read-qr-code";
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

function httpGet(url) {
  return new Promise((resolve, reject) => {
    const mod = url.startsWith("https") ? https : http;
    mod.get(url, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location)
        return httpGet(res.headers.location).then(resolve, reject);
      const chunks = [];
      res.on("data", (c) => chunks.push(c));
      res.on("end", () => resolve(Buffer.concat(chunks)));
    }).on("error", reject);
  });
}

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

function isUrl(s) { return s.startsWith("http://") || s.startsWith("https://"); }

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

async function decodeApiUrl(imageUrl) {
  try {
    const apiUrl = `${API_ENDPOINT}?file_url=${encodeURIComponent(imageUrl)}`;
    const buf = await httpGet(apiUrl);
    const data = JSON.parse(buf.toString());
    if (data.code === 0 && data.data?.contents?.length) return data.data.contents.join("; ");
    return null;
  } catch { return null; }
}

async function decodeApiFile(filePath) {
  return new Promise((resolve) => {
    try {
      const boundary = `----formdata${Date.now()}`;
      const filename = path.basename(filePath);
      const fileData = fs.readFileSync(filePath);
      const header = Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="file"; filename="${filename}"\r\nContent-Type: application/octet-stream\r\n\r\n`);
      const footer = Buffer.from(`\r\n--${boundary}--\r\n`);
      const body = Buffer.concat([header, fileData, footer]);
      const url = new URL(API_ENDPOINT);
      const options = { hostname: url.hostname, path: url.pathname, method: "POST", headers: { "Content-Type": `multipart/form-data; boundary=${boundary}`, "Content-Length": body.length } };
      const req = https.request(options, (res) => {
        const chunks = [];
        res.on("data", (c) => chunks.push(c));
        res.on("end", () => { try { const d = JSON.parse(Buffer.concat(chunks).toString()); resolve(d.code === 0 && d.data?.contents?.length ? d.data.contents.join("; ") : null); } catch { resolve(null); } });
      });
      req.on("error", () => resolve(null));
      req.write(body); req.end();
    } catch { resolve(null); }
  });
}

async function decodeSingle(source) {
  const local = await tryWechatQr(source);
  if (local) return local;

  if (isUrl(source)) {
    const r = await decodeApiUrl(source);
    return r || FAIL;
  } else if (fs.existsSync(source)) {
    const r = await decodeApiFile(source);
    return r || FAIL;
  } else {
    const r = await decodeApiUrl(source);
    return r || FAIL;
  }
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
