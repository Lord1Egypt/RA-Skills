#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { URL } = require('url');

const IMAGE_EXTS = new Set(['.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp']);

function readJsonIfExists(p) {
  try {
    if (!p || !fs.existsSync(p)) return null;
    return JSON.parse(fs.readFileSync(p, 'utf8'));
  } catch {
    return null;
  }
}

function findContextToken(accountsDir, recipient) {
  try {
    const files = fs.readdirSync(accountsDir).filter((f) => f.endsWith('.context-tokens.json'));
    for (const file of files) {
      const full = path.join(accountsDir, file);
      const data = readJsonIfExists(full);
      if (data && recipient && data[recipient]) {
        return { present: true, file: full };
      }
    }
    return { present: false, file: null };
  } catch {
    return { present: false, file: null };
  }
}

function guessMediaType(filePath) {
  const ext = path.extname(filePath || '').toLowerCase();
  return IMAGE_EXTS.has(ext) ? 'image' : (ext ? 'file' : 'unknown');
}

function main() {
  const filePath = process.argv[2] || '';
  const recipient = process.argv[3] || '当前会话';
  const debugPath = process.argv[4] || '';
  const accountsDir = path.join(process.env.HOME || '', '.openclaw/openclaw-weixin/accounts');
  const debug = readJsonIfExists(debugPath) || {};

  const uploadUrl = debug.upload_url || debug.uploadfullurl || 'n/a';
  let uploadUrlHost = 'n/a';
  try {
    if (uploadUrl !== 'n/a') uploadUrlHost = new URL(uploadUrl).host;
  } catch {}

  const encrypted = debug.encrypted_param || debug.downloadEncryptedQueryParam || '';
  const sendResp = debug.sendmessage_response || debug.sendmessage_raw || 'n/a';
  const sendStatus = debug.sendmessage_status || 'n/a';
  const context = findContextToken(accountsDir, recipient === '当前会话' ? '' : recipient);
  const exists = !!(filePath && fs.existsSync(filePath));
  const mediaType = guessMediaType(filePath);

  let probableCause = '需要检查宿主是否把结构化 media 回复映射到了 openclaw-weixin 的 sendMedia 路径';
  if (!exists) probableCause = '文件路径不存在或截图文件尚未生成';
  else if (!context.present && recipient !== '当前会话') probableCause = '未找到该接收人的 context token';
  else if (uploadUrl === 'n/a') probableCause = '未拿到 upload URL，可能是 token、会话态或请求字段不匹配';
  else if (encrypted && encrypted.length < 100) probableCause = 'encrypted param 过短，上传或返回头可能异常';
  else if (sendStatus !== 'n/a' && String(sendStatus) !== '200') probableCause = 'sendmessage 请求未成功';
  else if (String(sendResp).trim() === '{}' || String(sendResp).trim() === '') probableCause = 'sendmessage 返回空或空对象，常见于媒体对象无效或上下文不匹配';

  const out = {
    file_path: filePath || 'n/a',
    exists,
    recipient,
    upload_url: uploadUrl,
    upload_url_host: uploadUrlHost,
    encrypted_param_length: encrypted.length || 0,
    sendmessage_status: sendStatus,
    sendmessage_response: sendResp,
    context_token_present: context.present,
    context_token_file: context.file || 'n/a',
    media_type_guess: mediaType,
    probable_cause: probableCause,
  };

  console.log(JSON.stringify(out, null, 2));
}

main();
