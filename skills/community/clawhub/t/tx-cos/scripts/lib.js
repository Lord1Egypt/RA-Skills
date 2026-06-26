#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function readJsonArg(index, name) {
  const raw = process.argv[index];
  if (!raw) {
    throw new Error(`Missing JSON argument: ${name}`);
  }
  try {
    return JSON.parse(raw);
  } catch (error) {
    throw new Error(`Invalid JSON for ${name}: ${error.message}`);
  }
}

function requireEnv(keys) {
  const missing = keys.filter((key) => !process.env[key]);
  if (missing.length) {
    const error = new Error(`Missing required config: ${missing.join(', ')}`);
    error.code = 'CONFIG_MISSING';
    throw error;
  }
}

function ensureFile(filePath) {
  const stat = fs.statSync(filePath);
  if (!stat.isFile()) {
    throw new Error(`Path is not a file: ${filePath}`);
  }
  return stat;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function walkFiles(dir) {
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      out.push(...walkFiles(full));
    } else if (entry.isFile()) {
      out.push(full);
    }
  }
  return out;
}

function createCos() {
  requireEnv(['COS_SECRET_ID', 'COS_SECRET_KEY', 'COS_REGION', 'COS_BUCKET']);
  const COS = require('cos-nodejs-sdk-v5');
  return new COS({
    SecretId: process.env.COS_SECRET_ID,
    SecretKey: process.env.COS_SECRET_KEY,
  });
}

function getBucketConfig() {
  return {
    bucket: process.env.COS_BUCKET,
    region: process.env.COS_REGION,
    domain: process.env.COS_DOMAIN || '',
  };
}

function buildUrl(key, customDomain) {
  const { bucket, region, domain } = getBucketConfig();
  const base = customDomain || domain || `https://${bucket}.cos.${region}.myqcloud.com`;
  return `${base.replace(/\/$/, '')}/${key}`;
}

function print(data) {
  console.log(JSON.stringify(data, null, 2));
}

function formatBytes(bytes) {
  if (!bytes) return '0 B';
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let value = bytes;
  let i = 0;
  while (value >= 1024 && i < units.length - 1) {
    value /= 1024;
    i += 1;
  }
  return `${Number(value.toFixed(2))} ${units[i]}`;
}

module.exports = {
  readJsonArg,
  requireEnv,
  ensureFile,
  sleep,
  walkFiles,
  createCos,
  getBucketConfig,
  buildUrl,
  print,
  formatBytes,
};
