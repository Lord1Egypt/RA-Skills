#!/usr/bin/env node
/**
 * upload-screenshot.mjs
 * 上传截图到云效工作项，并更新 description 展示图片
 *
 * 用法：
 *   node upload-screenshot.mjs <workitemId> <imagePath> [displayWidth]
 *
 * 示例：
 *   node upload-screenshot.mjs f5b5c9d7a2230660784d6d6e78 /tmp/bug.jpg 350
 *
 * 关键要求（踩坑记录 2026-03-18）：
 *   1. 图片必须上传到云效附件拿 hex fileId，OSS 外链不可用
 *   2. jsonMLValue 必须是完整树，不能传空 []（云效前端优先用 jsonML 渲染）
 *   3. img 节点属性 id/name/size/width/height/rotation/src 必须完整
 */

import fs from 'fs';
import path from 'path';
import { TOKEN, ORG_ID, requireConfig } from './config.mjs';

requireConfig();


const BASE = `https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/${ORG_ID}`;

async function apiGet(urlPath) {
  const resp = await fetch(`${BASE}${urlPath}`, {
    headers: { 'x-yunxiao-token': TOKEN },
  });
  if (!resp.ok) throw new Error(`GET ${urlPath} → ${resp.status}: ${await resp.text()}`);
  return resp.json();
}

async function apiPut(urlPath, body) {
  const resp = await fetch(`${BASE}${urlPath}`, {
    method: 'PUT',
    headers: { 'x-yunxiao-token': TOKEN, 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!resp.ok) throw new Error(`PUT ${urlPath} → ${resp.status}: ${await resp.text()}`);
  return resp.status;
}

/**
 * 上传图片，返回 hex fileId（需查附件列表，不能用上传返回的数字 identifier）
 */
async function uploadAttachment(workitemId, imagePath) {
  const imageData = fs.readFileSync(imagePath);
  const ext = path.extname(imagePath).slice(1).toLowerCase();
  const mimeType = {
    jpg: 'image/jpeg', jpeg: 'image/jpeg', png: 'image/png',
    gif: 'image/gif', webp: 'image/webp'
  }[ext] || 'application/octet-stream';

  const form = new FormData();
  form.append('file', new Blob([imageData], { type: mimeType }), path.basename(imagePath));

  const resp = await fetch(`${BASE}/workitems/${workitemId}/attachments`, {
    method: 'POST',
    headers: { 'x-yunxiao-token': TOKEN },
    body: form,
  });

  if (!resp.ok) throw new Error(`Upload failed ${resp.status}: ${await resp.text()}`);

  // 上传返回的是数字 identifier，必须查列表才能拿到 hex fileId
  const atts = await apiGet(`/workitems/${workitemId}/attachments`);
  const latest = atts[atts.length - 1];
  const fileId = latest?.fileId;
  if (!fileId) throw new Error(`No hex fileId in attachments: ${JSON.stringify(atts)}`);
  return { fileId, fileName: latest.fileName, fileSize: latest.size };
}

/**
 * 获取原有描述文字（strip HTML tags）
 */
async function getDescText(workitemId) {
  const item = await apiGet(`/workitems/${workitemId}`);
  const raw = item.description || '';
  if (!raw) return '';
  try {
    const parsed = JSON.parse(raw);
    return (parsed.htmlValue || '').replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').trim();
  } catch {
    return raw.replace(/<[^>]+>/g, '').trim();
  }
}

/**
 * 构造 jsonML leaf 节点
 */
function leaf(text) {
  return ['span', { 'data-type': 'text' }, ['span', { 'data-type': 'leaf' }, text]];
}

/**
 * 构造 jsonML p 节点
 */
function p(...children) {
  return ['p', {}, ...children];
}

/**
 * 构造 jsonML img 节点
 */
function imgNode(name, size, w, h, src) {
  return ['img', {
    id: 'scr' + Math.random().toString(36).slice(2, 8),
    name, size, width: w, height: h, rotation: 0, src
  }, leaf('')];
}

/**
 * 更新工作项 description（htmlValue + 完整 jsonMLValue）
 */
async function updateDescWithImage(workitemId, { fileId, fileName, fileSize }, displayW, existingText) {
  const imgSrc = `https://devops.aliyun.com/projex/api/workitem/file/url?fileIdentifier=${fileId}`;

  // 需要从附件列表里拿图片原始尺寸来计算比例
  // 暂时用 displayW x displayW（正方形），如果传了 height 则用传入值
  const displayH = displayW; // 调用方传入实际比例

  // htmlValue
  const textPart = existingText
    ? `<p style="text-align:left;text-indent:0;margin-left:0"><span>${existingText}</span></p>`
    : '';
  const html = [
    `<article class="4ever-article">`,
    textPart,
    `<p style="text-align:left;text-indent:0;margin-left:0">`,
    `<span></span>`,
    `<img src="${imgSrc}" style="width:${displayW}px;height:${displayH}px">`,
    `<span></span></p>`,
    `</article>`,
  ].join('');

  // jsonMLValue（完整树，不能是空 []）
  const jsonml = ['root', {}];
  if (existingText) jsonml.push(p(leaf(existingText)));
  jsonml.push(p(leaf(''), imgNode(fileName, fileSize, displayW, displayH, imgSrc), leaf('')));

  const inner = { htmlValue: html, jsonMLValue: jsonml };
  const description = JSON.stringify(inner);
  return apiPut(`/workitems/${workitemId}`, { description });
}

// ─── Main ─────────────────────────────────────────────────────────────────────
const [,, workitemId, imagePath, widthStr] = process.argv;

if (!workitemId || !imagePath) {
  console.error('Usage: node upload-screenshot.mjs <workitemId> <imagePath> [displayWidth=350]');
  process.exit(1);
}
if (!TOKEN) { console.error('❌ No YUNXIAO_ACCESS_TOKEN'); process.exit(1); }
if (!fs.existsSync(imagePath)) { console.error(`❌ File not found: ${imagePath}`); process.exit(1); }

const displayW = parseInt(widthStr || '350', 10);

console.log(`📸 上传截图: ${path.basename(imagePath)}`);
console.log(`📋 工作项: ${workitemId}`);

try {
  console.log('📖 读取原有描述...');
  const existingText = await getDescText(workitemId);
  if (existingText) console.log(`   原描述: ${existingText.slice(0, 80)}${existingText.length > 80 ? '...' : ''}`);

  console.log('⬆️  上传图片到云效...');
  const attachment = await uploadAttachment(workitemId, imagePath);
  console.log(`   ✅ fileId: ${attachment.fileId}`);
  console.log(`   🔗 ${`https://devops.aliyun.com/projex/api/workitem/file/url?fileIdentifier=${attachment.fileId}`}`);

  console.log('📝 更新工作项描述（htmlValue + jsonMLValue）...');
  const status = await updateDescWithImage(workitemId, attachment, displayW, existingText);
  console.log(`   ✅ 更新成功 (HTTP ${status})`);
  console.log(`\n🎉 完成！刷新云效页面即可看到图片`);
} catch (err) {
  console.error('❌ 失败:', err.message);
  process.exit(1);
}
