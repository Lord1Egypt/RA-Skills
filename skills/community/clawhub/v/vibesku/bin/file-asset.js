"use strict";

const { readFile } = require("fs/promises");
const { basename, extname } = require("path");

const MIME_MAP = {
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp"
};

async function readUploadAsset(filePath) {
  const fileBuffer = await readFile(filePath);
  const fileName = basename(filePath);
  const ext = extname(filePath).toLowerCase();
  const contentType = MIME_MAP[ext] ?? "application/octet-stream";
  return { fileBuffer, fileName, contentType };
}

module.exports = {
  readUploadAsset
};
