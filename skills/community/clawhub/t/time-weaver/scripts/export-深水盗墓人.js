#!/usr/bin/env node

/**
 * EPUB Exporter for 深水盗墓人
 */

const fs = require('fs');
const path = require('path');

const BOOK_NAME = '深水盗墓人';
const CHAPTERS_DIR = path.join(__dirname, '..', '.learnings', 'books', BOOK_NAME, 'chapters');
const OUTPUT_DIR = path.join(__dirname, '..', 'output');

const Epub = require('epub-gen');

// 确保输出目录存在
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// Markdown 转 HTML
function markdownToHtml(markdown) {
  let html = markdown
    .replace(/^####\s*(.+)$/gm, '<h4>$1</h4>')
    .replace(/^###\s*(.+)$/gm, '<h3>$1</h3>')
    .replace(/^##\s*(.+)$/gm, '<h2>$1</h2>')
    .replace(/^#\s*(.+)$/gm, '<h1>$1</h1>')
    .replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`(.+?)`/g, '<code>$1</code>')
    .replace(/^---+$/gm, '<hr>')
    .split('\n\n')
    .map(para => {
      para = para.trim();
      if (!para) return '';
      if (para.startsWith('<h') || para.startsWith('<hr')) return para;
      return `<p>${para.replace(/\n/g, '<br>')}</p>`;
    })
    .join('\n');
  
  return html;
}

// 读取章节
function getChapters() {
  const files = fs.readdirSync(CHAPTERS_DIR)
    .filter(f => f.endsWith('.md'))
    .sort((a, b) => {
      const numA = parseInt(a.match(/\d+/)?.[0] || '0');
      const numB = parseInt(b.match(/\d+/)?.[0] || '0');
      return numA - numB;
    });
  
  return files.map(file => {
    const content = fs.readFileSync(path.join(CHAPTERS_DIR, file), 'utf8');
    const titleMatch = content.match(/^#\s*(.+)$/m);
    const title = titleMatch ? titleMatch[1] : file.replace('.md', '');
    
    return {
      title: title,
      data: markdownToHtml(content)
    };
  });
}

async function generateEpub() {
  console.log(`📚 开始导出《${BOOK_NAME}》...`);
  
  const chapters = getChapters();
  console.log(`📖 读取到 ${chapters.length} 个章节`);
  
  if (chapters.length === 0) {
    console.log('❌ 没有找到章节文件');
    process.exit(1);
  }
  
  const dateStr = new Date().toISOString().split('T')[0];
  const outputFile = path.join(OUTPUT_DIR, `${BOOK_NAME}_${dateStr}.epub`);
  
  const options = {
    title: BOOK_NAME,
    author: 'Time Weaver',
    publisher: 'Time Weaver Studio',
    description: `《${BOOK_NAME}》是一部穿越小说，由 Time Weaver 创作。`,
    tocTitle: '目录',
    lang: 'zh-CN',
    content: chapters
  };
  
  console.log('📝 正在生成 EPUB...');
  
  try {
    await new Epub(options, outputFile).promise;
    console.log('✅ 导出成功！');
    console.log(`📂 文件路径: ${outputFile}`);
    const stats = fs.statSync(outputFile);
    console.log(`📊 文件大小: ${(stats.size / 1024).toFixed(2)} KB`);
  } catch (err) {
    console.error('❌ 导出失败:', err.message);
    process.exit(1);
  }
}

generateEpub();
