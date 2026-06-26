/**
 * weread-dl 章节解码器 — 本地解码微信读书加密章节数据
 * 
 * 算法（来自 weread-dl Chrome 扩展）：
 *   数据格式: 32位hex校验码 + 1位分隔符 + base64(UTF-8 HTML)
 *   e_0 = 完整 HTML 文档（含 body）
 *   e_1 = 续文片段
 *   e_3 = 续文片段
 *   e_2 = CSS 样式
 * 
 * 用法：
 *   node scripts/decode.js <books/<书名>/chapters>
 */

const fs = require('fs');
const path = require('path');

function stripB64(data) {
  if (!data || typeof data !== 'string') return '';
  // 跳过前 33 个字符（32 hex + 1 separator）
  let b64 = data.slice(33);
  // 补齐 base64
  while (b64.length % 4) b64 += '=';
  return b64;
}

function decodeBase64(b64) {
  const bin = Buffer.from(b64, 'base64');
  return bin.toString('utf-8');
}

/**
 * 解码单个加密文件
 */
function decodeEncFile(filepath) {
  const raw = fs.readFileSync(filepath, 'utf-8').trim();
  const b64 = stripB64(raw);
  if (!b64) return null;
  return decodeBase64(b64);
}

/**
 * 从 e_0 完整 HTML 中提取 body 内容
 */
function extractBody(html) {
  const m = html.match(/<body[^>]*>([\s\S]*)<\/body>/i);
  return m ? m[1] : html;
}

/**
 * 清理 HTML 标签，保留可读文本
 */
function stripHtml(html) {
  return html
    .replace(/<\?xml[^>]*\?>/g, '')
    .replace(/<!DOCTYPE[^>]*>/gi, '')
    .replace(/<\/?(?:html|head|body|title|link|meta|h1)[^>]*>/g, '')
    .replace(/<[^>]+>/g, '\n')
    .replace(/\uFFFD/g, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

/**
 * 解码完整章节（旧格式：扁平目录）
 * @param {string} chaptersDir - 章节文件夹（包含 chapter_e0.enc 等）
 * @returns {{ text: string, css: string, html: string, parts: object }}
 */
function decodeChapter(chaptersDir) {
  const parts = {};
  for (const suffix of ['e0', 'e1', 'e2', 'e3']) {
    const candidates = [
      path.join(chaptersDir, `${suffix}.enc`),
      path.join(chaptersDir, `chapter_${suffix}.enc`),
      path.join(chaptersDir, `chapter_e_${suffix.substring(1)}.enc`),
    ];
    for (const file of candidates) {
      if (fs.existsSync(file)) {
        parts[suffix] = decodeEncFile(file);
        break;
      }
    }
  }

  let bodyParts = [];
  if (parts['e0']) {
    bodyParts.push(extractBody(parts['e0']));
  }
  if (parts['e1']) {
    bodyParts.push(extractBody(parts['e1']));
  }
  if (parts['e3']) {
    bodyParts.push(extractBody(parts['e3']));
  }

  const html = bodyParts.join('\n');
  const text = stripHtml(html);
  const css = parts['e2'] || '';

  return { text, css, html, parts: Object.keys(parts) };
}

/**
 * 解码所有章节（新格式：每章一个子目录）
 * @param {string} chaptersDir - 包含 chapter_* 子目录的文件夹
 * @returns {string} 拼接后的文本
 */
function decodeAllChapters(chaptersDir) {
  const entries = fs.readdirSync(chaptersDir, { withFileTypes: true });
  const chapterDirs = entries
    .filter(e => e.isDirectory() && e.name.startsWith('chapter_'))
    .sort((a, b) => {
      const na = parseInt(a.name.replace('chapter_', ''), 10);
      const nb = parseInt(b.name.replace('chapter_', ''), 10);
      if (!isNaN(na) && !isNaN(nb)) return na - nb;
      return a.name.localeCompare(b.name);
    });

  const results = [];
  for (const dir of chapterDirs) {
    const dirPath = path.join(chaptersDir, dir.name);
    const parts = {};
    for (const suffix of ['e0', 'e1', 'e2', 'e3']) {
      const file = path.join(dirPath, `${suffix}.enc`);
      if (fs.existsSync(file)) {
        parts[suffix] = decodeEncFile(file);
      }
    }

    let bodyParts = [];
    if (parts['e0']) bodyParts.push(extractBody(parts['e0']));
    if (parts['e1']) bodyParts.push(extractBody(parts['e1']));
    if (parts['e3']) bodyParts.push(extractBody(parts['e3']));

    const html = bodyParts.join('\n');
    const text = stripHtml(html);
    const chapterLabel = dir.name.replace('chapter_', '');
    results.push(`=== Chapter ${chapterLabel} ===\n\n${text}\n======`);
  }

  return results.join('\n\n');
}

/**
 * 解码单个 enc 文件并输出文本
 */
if (require.main === module) {
  const target = process.argv[2];
  if (!target) {
    console.log('用法:');
    console.log('  node scripts/decode.js <chapters_dir>     解码完整章节');
    console.log('  node scripts/decode.js <chapter_e0.enc>   解码单个文件');
    process.exit(0);
  }

  const stat = fs.statSync(target);
  if (stat.isDirectory()) {
    const entries = fs.readdirSync(target, { withFileTypes: true });
    const hasChapterDirs = entries.some(e => e.isDirectory() && e.name.startsWith('chapter_'));
    if (hasChapterDirs) {
      const result = decodeAllChapters(target);
      console.log('='.repeat(60));
      console.log('解码完成');
      console.log('文本长度:', result.length);
      console.log('='.repeat(60));
      console.log(result);
    } else {
      const result = decodeChapter(target);
      console.log('='.repeat(60));
      console.log('解码完成');
      console.log('包含部分:', result.parts.join(', '));
      console.log('文本长度:', result.text.length);
      console.log('CSS长度:', result.css.length);
      console.log('='.repeat(60));
      console.log(result.text);
    }
  } else {
    const decoded = decodeEncFile(target);
    if (decoded) {
      console.log(decoded);
    } else {
      console.error('解码失败');
    }
  }
}

module.exports = { decodeEncFile, decodeChapter, decodeAllChapters, stripHtml, extractBody };
