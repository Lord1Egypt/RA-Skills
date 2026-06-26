#!/usr/bin/env node
/**
 * QR Code Decoder - 本地 wechat-qr 优先，失败时回退到草料 API (Node.js 版)
 *
 * 用法:
 *   node scripts/decode.js [--force-api] <图片路径或URL>
 *   node scripts/decode.js [--force-api] --file <本地路径>
 *   node scripts/decode.js [--force-api] --url <图片URL>
 *
 * 输出 JSON:
 *   {"source": "wechat-qr"|"api", "contents": ["..."]}
 *   {"error": "..."}
 */

const https = require("https");
const http = require("http");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { URL } = require("url");

const API_ENDPOINT = "https://api.2dcode.biz/v1/read-qr-code";

function output(source, contents) {
  console.log(JSON.stringify({ source, contents }));
  process.exit(0);
}

function error(msg) {
  console.log(JSON.stringify({ error: msg }));
  process.exit(1);
}

function isUrl(s) {
  return s.startsWith("http://") || s.startsWith("https://");
}

function httpGet(url) {
  return new Promise((resolve, reject) => {
    const mod = url.startsWith("https") ? https : http;
    mod.get(url, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return httpGet(res.headers.location).then(resolve, reject);
      }
      const chunks = [];
      res.on("data", (c) => chunks.push(c));
      res.on("end", () => resolve(Buffer.concat(chunks)));
    }).on("error", reject);
  });
}

function downloadToTemp(url) {
  return new Promise((resolve, reject) => {
    const ext = path.extname(url.split("?")[0]) || ".png";
    const tmp = path.join(os.tmpdir(), `qr_${Date.now()}${ext}`);
    const mod = url.startsWith("https") ? https : http;
    const file = fs.createWriteStream(tmp);
    mod.get(url, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        file.close();
        fs.unlinkSync(tmp);
        return downloadToTemp(res.headers.location).then(resolve, reject);
      }
      res.pipe(file);
      file.on("finish", () => { file.close(); resolve(tmp); });
    }).on("error", (e) => { file.close(); if (fs.existsSync(tmp)) fs.unlinkSync(tmp); reject(e); });
  });
}

async function decodeWithWechat(imagePath) {
  try {
    const { scan } = await import("qr-scanner-wechat");
    const sharp = require("sharp");
    const { data, info } = await sharp(imagePath)
      .ensureAlpha()
      .raw()
      .toBuffer({ resolveWithObject: true });
    const result = await scan({
      data: Uint8ClampedArray.from(data),
      width: info.width,
      height: info.height,
    });
    return result?.text ? [result.text] : null;
  } catch {
    return null;
  }
}

async function decodeWithApiUrl(imageUrl) {
  try {
    const apiUrl = `${API_ENDPOINT}?file_url=${encodeURIComponent(imageUrl)}`;
    const buf = await httpGet(apiUrl);
    const data = JSON.parse(buf.toString());
    if (data.code === 0 && data.data?.contents?.length) return data.data.contents;
    return null;
  } catch {
    return null;
  }
}

async function decodeWithApiFile(filePath) {
  return new Promise((resolve) => {
    try {
      const boundary = `----formdata${Date.now()}`;
      const filename = path.basename(filePath);
      const fileData = fs.readFileSync(filePath);
      const header = Buffer.from(
        `--${boundary}\r\nContent-Disposition: form-data; name="file"; filename="${filename}"\r\nContent-Type: application/octet-stream\r\n\r\n`
      );
      const footer = Buffer.from(`\r\n--${boundary}--\r\n`);
      const body = Buffer.concat([header, fileData, footer]);

      const url = new URL(API_ENDPOINT);
      const options = {
        hostname: url.hostname,
        path: url.pathname,
        method: "POST",
        headers: { "Content-Type": `multipart/form-data; boundary=${boundary}`, "Content-Length": body.length },
      };
      const req = https.request(options, (res) => {
        const chunks = [];
        res.on("data", (c) => chunks.push(c));
        res.on("end", () => {
          try {
            const data = JSON.parse(Buffer.concat(chunks).toString());
            if (data.code === 0 && data.data?.contents?.length) resolve(data.data.contents);
            else resolve(null);
          } catch { resolve(null); }
        });
      });
      req.on("error", () => resolve(null));
      req.write(body);
      req.end();
    } catch { resolve(null); }
  });
}

async function main() {
  const argv = process.argv.slice(2);
  const forceApi = argv.includes("--force-api");
  const filtered = argv.filter((a) => a !== "--force-api");

  if (!filtered.length) error("用法: node decode.js [--force-api] <图片路径或URL>");

  let mode, target;
  if ((filtered[0] === "--file" || filtered[0] === "--url") && filtered.length >= 2) {
    mode = filtered[0];
    target = filtered[1];
  } else {
    target = filtered[0];
    mode = isUrl(target) ? "--url" : "--file";
  }

  if (mode === "--file") {
    if (!fs.existsSync(target)) error(`文件不存在: ${target}`);

    if (!forceApi) {
      const results = await decodeWithWechat(target);
      if (results) output("wechat-qr", results);
    }

    const results = await decodeWithApiFile(target);
    if (results) output("api", results);

    error("无法解码: 本地 wechat-qr 和远程 API 均未识别到二维码");
  } else {
    if (!forceApi) {
      let tmpPath = null;
      try {
        tmpPath = await downloadToTemp(target);
        const results = await decodeWithWechat(tmpPath);
        if (results) output("wechat-qr", results);
      } catch { /* ignore */ } finally {
        if (tmpPath && fs.existsSync(tmpPath)) fs.unlinkSync(tmpPath);
      }
    }

    const results = await decodeWithApiUrl(target);
    if (results) output("api", results);

    error("无法解码: 远程 API 未识别到二维码");
  }
}

main();
