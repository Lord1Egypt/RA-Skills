#!/usr/bin/env node
/**
 * Secure Storage — 安全存储
 * 源自 utils/secureStorage/ (6 文件, 629 行)
 * 
 * Linux 服务器降级为文件存储（权限 0600）
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const STORAGE_FILE = process.env.HOME + '/.openclaw/workspace/memory/secure-storage.json';

// 简单加密（Base64 + 密钥混淆，非生产级）
// 生产环境应使用系统密钥链或 KMS
const SIMPLE_KEY = 'openclaw-secure-storage-v1';

function encrypt(text) {
  const iv = crypto.randomBytes(16);
  const key = crypto.scryptSync(SIMPLE_KEY, 'salt', 32);
  const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  return iv.toString('hex') + ':' + encrypted;
}

function decrypt(text) {
  const parts = text.split(':');
  const iv = Buffer.from(parts[0], 'hex');
  const key = crypto.scryptSync(SIMPLE_KEY, 'salt', 32);
  const decipher = crypto.createDecipheriv('aes-256-cbc', key, iv);
  let decrypted = decipher.update(parts[1], 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  return decrypted;
}

function loadStorage() {
  try {
    return JSON.parse(fs.readFileSync(STORAGE_FILE, 'utf-8'));
  } catch { return {}; }
}

function saveStorage(data) {
  const dir = path.dirname(STORAGE_FILE);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(STORAGE_FILE, JSON.stringify(data, null, 2), { mode: 0o600 });
}

function setKey(key, value) {
  const storage = loadStorage();
  storage[key] = { encrypted: encrypt(value), createdAt: new Date().toISOString() };
  saveStorage(storage);
  console.log(`✅ 已存储: ${key}`);
}

function getKey(key) {
  const storage = loadStorage();
  if (!storage[key]) { console.log(`❌ 未找到: ${key}`); return; }
  try {
    const value = decrypt(storage[key].encrypted);
    console.log(`${key}: ${value}`);
    return value;
  } catch {
    console.log('❌ 解密失败');
  }
}

function deleteKey(key) {
  const storage = loadStorage();
  if (!storage[key]) { console.log(`❌ 未找到: ${key}`); return; }
  delete storage[key];
  saveStorage(storage);
  console.log(`✅ 已删除: ${key}`);
}

function listKeys() {
  const storage = loadStorage();
  const keys = Object.keys(storage);
  console.log('=== 安全存储 ===\n');
  if (keys.length === 0) { console.log('无存储项'); return; }
  console.log('密钥'.padEnd(30) + '创建时间');
  console.log('-'.repeat(50));
  keys.forEach(k => {
    const time = new Date(storage[k].createdAt).toLocaleString('zh-CN');
    console.log(k.padEnd(30) + time);
  });
  console.log(`\n共 ${keys.length} 项`);
}

const [command, ...args] = process.argv.slice(2);

switch (command) {
  case 'set':
    if (args.length < 2) { console.log('用法: node secure-storage.js set <key> <value>'); process.exit(1); }
    setKey(args[0], args.slice(1).join(' '));
    break;
  case 'get':
    if (!args[0]) { console.log('用法: node secure-storage.js get <key>'); process.exit(1); }
    getKey(args[0]);
    break;
  case 'delete':
    if (!args[0]) { console.log('用法: node secure-storage.js delete <key>'); process.exit(1); }
    deleteKey(args[0]);
    break;
  case 'list': listKeys(); break;
  default:
    console.log('用法: node secure-storage.js [set|get|delete|list]');
}
