#!/usr/bin/env node
/**
 * QR Code Decoder - 本地 wechat-qr 解码 (Node.js 版)
 *
 * 用法:
 *   node scripts/decode.js <图片路径或URL>
 *   node scripts/decode.js --file <本地路径>
 *   node scripts/decode.js --url <图片URL>
 *
 * 输出 JSON:
 *   {"source": "wechat-qr", "contents": ["..."]}
 *   {"error": "..."}
 */

const https = require("https");
const http = require("http");
const fs = require("fs");
const os = require("os");
const path = require("path");

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

async function main() {
  const argv = process.argv.slice(2);

  if (!argv.length) error("用法: node decode.js <图片路径或URL>");

  let mode, target;
  if ((argv[0] === "--file" || argv[0] === "--url") && argv.length >= 2) {
    mode = argv[0];
    target = argv[1];
  } else {
    target = argv[0];
    mode = isUrl(target) ? "--url" : "--file";
  }

  if (mode === "--file") {
    if (!fs.existsSync(target)) error(`文件不存在: ${target}`);

    const results = await decodeWithWechat(target);
    if (results) output("wechat-qr", results);

    error("无法解码: 本地 wechat-qr 未识别到二维码");
  } else {
    let tmpPath = null;
    try {
      tmpPath = await downloadToTemp(target);
      const results = await decodeWithWechat(tmpPath);
      if (results) output("wechat-qr", results);
    } catch (e) {
      error(`下载图片失败: ${e.message}`);
    } finally {
      if (tmpPath && fs.existsSync(tmpPath)) fs.unlinkSync(tmpPath);
    }

    error("无法解码: 本地 wechat-qr 未识别到二维码");
  }
}

main();
