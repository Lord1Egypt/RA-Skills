const mammoth = require('mammoth');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

/**
 * Parse document content from .docx, .md, or .pptx files
 */
async function parseDocument(filePath, ext) {
  switch (ext) {
    case '.docx':
      return parseDocx(filePath);
    case '.md':
      return parseMarkdown(filePath);
    case '.pptx':
      return parsePptx(filePath);
    default:
      throw new Error(`不支持的文件格式: ${ext}，仅支持 .docx .md .pptx`);
  }
}

async function parseDocx(filePath) {
  try {
    const result = await mammoth.extractRawText({ path: filePath });
    let text = result.value;
    // Clean up excessive whitespace
    text = text.replace(/\n{3,}/g, '\n\n').trim();
    return text;
  } catch (err) {
    throw new Error('Word文档解析失败: ' + err.message);
  }
}

function parseMarkdown(filePath) {
  const text = fs.readFileSync(filePath, 'utf-8');
  // Strip markdown syntax for cleaner text
  return text
    .replace(/^#{1,6}\s+/gm, '')          // Remove headings
    .replace(/\*\*(.+?)\*\*/g, '$1')       // Bold
    .replace(/\*(.+?)\*/g, '$1')            // Italic
    .replace(/`{1,3}[^`]*`{1,3}/g, '')     // Code blocks
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // Links
    .replace(/^\s*[-*+]\s+/gm, '')          // List items
    .replace(/^\s*\d+\.\s+/gm, '')          // Numbered lists
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

function parsePptx(filePath) {
  // PPTX is a ZIP file, extract text from slides
  const AdmZip = require('adm-zip');
  try {
    const zip = new AdmZip(filePath);
    const entries = zip.getEntries();
    let allText = [];

    for (const entry of entries) {
      if (entry.entryName.startsWith('ppt/slides/slide') && entry.entryName.endsWith('.xml')) {
        const content = entry.getData().toString('utf-8');
        // Extract text from XML
        const texts = content.match(/<a:t>([^<]+)<\/a:t>/g) || [];
        for (const t of texts) {
          const text = t.replace(/<\/?a:t>/g, '').trim();
          if (text) allText.push(text);
        }
      }
    }

    return allText.join('\n').replace(/\n{3,}/g, '\n\n').trim();
  } catch (err) {
    // Fallback: use strings command
    try {
      const output = execSync(`strings "${filePath}" | grep -E '[\\u4e00-\\u9fff]|[a-zA-Z]{3,}' | head -500`, { encoding: 'utf-8' });
      return output.replace(/^\s*\n+/, '').substring(0, 10000);
    } catch (e2) {
      throw new Error('PPTX解析失败: ' + err.message);
    }
  }
}

module.exports = { parseDocument };
