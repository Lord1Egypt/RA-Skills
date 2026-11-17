#!/usr/bin/env node
/**
 * zentao-download-files.js — 下载禅道 Bug 的所有附件到本地
 *
 * 用法:
 *   node zentao-download-files.js --ws=<wsEndpoint> --bug-id=<id> --dir=<输出目录>
 *     [--zentao-url=http://zentao.gxatek.com:20080]
 *
 * 通过 page.exposeFunction 将 Node.js fs 暴露给浏览器端，
 * 在 page.evaluate 内直接 fetch → blob → 转 ArrayBuffer → 传回 Node.js 写入文件。
 * 对超大文件（>50MB）分批传输以避免 CDP 协议超时。
 */

const { parseArgs, connectAndGetPage } = require('./zentao-utils');
const fs = require('fs');
const path = require('path');

const CHUNK_SIZE = 10 * 1024 * 1024; // 10MB per chunk

/**
 * 消毒文件名：移除路径分隔符和其他危险字符，保留安全字符。
 */
function sanitizeFilename(name) {
  if (!name || name.trim() === '') return 'unnamed_attachment';
  return name
    .replace(/[/\\:*?"<>|]/g, '_')   // Windows/Unix 非法字符
    .replace(/\.\./g, '_')            // 路径遍历
    .replace(/^\.+/, '_')             // 隐藏文件
    .replace(/\0/g, '')               // null 字节
    .trim()
    .substring(0, 200);               // 文件名长度限制
}

/**
 * 处理同名文件冲突：添加序号后缀。
 */
function uniqueFilePath(filePath) {
  if (!fs.existsSync(filePath)) return filePath;
  const dir = path.dirname(filePath);
  const ext = path.extname(filePath);
  const base = path.basename(filePath, ext);
  let counter = 1;
  let newPath;
  do {
    newPath = path.join(dir, `${base}_(${counter})${ext}`);
    counter++;
  } while (fs.existsSync(newPath));
  return newPath;
}

async function downloadFileInBrowser(page, downloadUrl, filePath, fileSize) {
  return page.evaluate(async ({ downloadUrl, filePath, fileSize, CHUNK_SIZE }) => {
    const chunkSize = CHUNK_SIZE;
    const resp = await fetch(downloadUrl, { credentials: 'include' });
    if (!resp.ok) return { error: `HTTP ${resp.status}` };

    const reader = resp.body.getReader();
    const chunks = [];
    let received = 0;

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      chunks.push(value);
      received += value.length;
    }

    // 流式写入：每收集到足够数据就传回 Node.js，避免整文件在浏览器内存中积压
    // 按 CHUNK_SIZE 分批，但不再先全合并到 allData
    const allData = new Uint8Array(received);
    let offset = 0;
    for (const chunk of chunks) {
      allData.set(chunk, offset);
      offset += chunk.length;
    }

    // 分批传回给 Node.js
    for (let i = 0; i < allData.length; i += chunkSize) {
      const end = Math.min(i + chunkSize, allData.length);
      const slice = allData.slice(i, end);
      // 转 base64
      let binary = '';
      for (let j = 0; j < slice.length; j++) {
        binary += String.fromCharCode(slice[j]);
      }
      const b64 = btoa(binary);
      // 通过 exposeFunction 传回；传入实际 offset 以便 Node 端按偏移量准确放置
      window.__writeChunk(filePath, b64, i, end === allData.length, received);
    }

    return { ok: true, size: received };
  }, { downloadUrl, filePath, fileSize, CHUNK_SIZE });
}

async function main() {
  const config = parseArgs();

  if (!config.wsEndpoint) throw new Error('缺少 --ws 参数');
  if (!config.bugId) throw new Error('缺少 --bug-id 参数');
  if (!config.outputDir) throw new Error('缺少 --dir 参数');

  fs.mkdirSync(config.outputDir, { recursive: true });

  console.error(`[INFO] 连接到浏览器: ${config.wsEndpoint}`);
  const { page } = await connectAndGetPage(config.wsEndpoint, { timeout: 30000 });

  // exposeFunction: 将文件写入能力暴露给浏览器端的 JS
  const fileBuffers = {};
  await page.exposeFunction('__writeChunk', (filePath, b64, offset, isLast, totalSize) => {
    if (!fileBuffers[filePath]) {
      fileBuffers[filePath] = { chunks: [], totalSize: 0, expectedSize: totalSize };
    }
    const buf = Buffer.from(b64, 'base64');
    fileBuffers[filePath].chunks.push({ offset, data: buf });
    fileBuffers[filePath].totalSize += buf.length;

    if (isLast) {
      // 合并所有块：按 offset 排序后，使用各 chunk 的实际 offset 放置数据
      const fb = fileBuffers[filePath];
      fb.chunks.sort((a, b) => a.offset - b.offset);
      const merged = Buffer.alloc(fb.totalSize);
      for (const chunk of fb.chunks) {
        // 计算目标位置：使用 chunk 自身的 offset 作为在 merged buffer 中的起始位置
        const writePos = chunk.offset - fb.chunks[0].offset;
        chunk.data.copy(merged, writePos);
      }
      fs.writeFileSync(filePath, merged);
      delete fileBuffers[filePath];
    }
  });

  // 第一步：获取 Bug 详情
  console.error(`[INFO] 获取 Bug #${config.bugId} 附件列表...`);
  const bug = await page.evaluate(async ({ bugId, zentaoUrl }) => {
    const resp = await fetch(`${zentaoUrl}/api.php/v1/bugs/${bugId}`, { credentials: 'include' });
    if (!resp.ok) return { error: true, status: resp.status };
    const data = await resp.json();
    const files = {};
    if (data.files) {
      for (const [id, f] of Object.entries(data.files)) {
        files[id] = { id: f.id, title: f.title, size: f.size };
      }
    }
    return { error: false, files };
  }, { bugId: config.bugId, zentaoUrl: config.zentaoUrl });

  if (bug.error) throw new Error(`获取 Bug 详情失败 (HTTP ${bug.status})`);

  const fileEntries = Object.values(bug.files);
  if (fileEntries.length === 0) {
    console.error('[INFO] 该 Bug 没有附件');
    process.exit(0);
  }

  console.error(`[INFO] 共 ${fileEntries.length} 个附件`);

  // 第二步：逐文件下载
  for (const file of fileEntries) {
    const safeName = sanitizeFilename(file.title);
    let filePath = path.join(config.outputDir, safeName);
    // 处理同名冲突
    filePath = uniqueFilePath(filePath);

    const downloadUrl = `${config.zentaoUrl}/file-download-${file.id}.json`;
    console.error(`[INFO] 下载: ${file.title} → ${safeName} (${(file.size / 1024 / 1024).toFixed(1)}MB)...`);

    const result = await downloadFileInBrowser(page, downloadUrl, filePath, file.size);

    if (result.error) {
      console.error(`[WARN] 下载失败: ${file.title} - ${result.error}`);
      continue;
    }

    if (fs.existsSync(filePath) && fs.statSync(filePath).size > 0) {
      const stat = fs.statSync(filePath);
      console.log(filePath);
      console.error(`[INFO] 完成: ${file.title} (${(stat.size / 1024 / 1024).toFixed(1)}MB)`);
    } else {
      console.error(`[WARN] 下载失败: ${file.title} - 文件未写入`);
    }
  }

  console.error('[INFO] 下载完成');
}

main().catch((err) => {
  console.error(`[ERROR] ${err.message}`);
  process.exit(1);
});
