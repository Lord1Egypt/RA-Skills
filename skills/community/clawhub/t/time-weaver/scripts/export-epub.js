#!/usr/bin/env node

/**
 * EPUB Exporter for Time Weaver
 * Usage: node export-epub.js [bookTitle] [author]
 */

const fs = require('fs');
const path = require('path');

const CHAPTERS_DIR = path.join(__dirname, '..', 'chapters');
const OUTPUT_DIR = path.join(__dirname, '..', 'output');

// 检查 epub-gen 是否安装
try {
  require.resolve('epub-gen');
} catch (e) {
  console.log('❌ 未安装 epub-gen，正在安装...');
  console.log('请运行: npm install epub-gen');
  process.exit(1);
}

const Epub = require('epub-gen');

// 获取命令行参数
const bookTitle = process.argv[2] || '烂尾之王';
const author = process.argv[3] || 'Time Weaver';

// 确保输出目录存在
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// Markdown 转 HTML
function markdownToHtml(markdown) {
  let html = markdown
    // 代码块
    .replace(/```[\s\S]*?```/g, match => {
      const code = match.replace(/```[\w]*\n?/, '').replace(/```$/, '');
      return `\u003cpre\u003e\u003ccode\u003e${code}\u003c/code\u003e\u003c/pre\u003e`;
    })
    // 标题
    .replace(/^####\s*(.+)$/gm, '\u003ch4\u003e$1\u003c/h4\u003e')
    .replace(/^###\s*(.+)$/gm, '\u003ch3\u003e$1\u003c/h3\u003e')
    .replace(/^##\s*(.+)$/gm, '\u003ch2\u003e$1\u003c/h2\u003e')
    .replace(/^#\s*(.+)$/gm, '\u003ch1\u003e$1\u003c/h1\u003e')
    // 粗体和斜体
    .replace(/\*\*\*(.+?)\*\*\*/g, '\u003cstrong\u003e\u003cem\u003e$1\u003c/em\u003e\u003c/strong\u003e')
    .replace(/\*\*(.+?)\*\*/g, '\u003cstrong\u003e$1\u003c/strong\u003e')
    .replace(/\*(.+?)\*/g, '\u003cem\u003e$1\u003c/em\u003e')
    // 行内代码
    .replace(/`(.+?)`/g, '\u003ccode\u003e$1\u003c/code\u003e')
    // 分隔线
    .replace(/^---+$/gm, '\u003chr\u003e')
    // 段落
    .split('\n\n')
    .map(para => {
      para = para.trim();
      if (!para) return '';
      if (para.startsWith('\u003ch') || para.startsWith('\u003cpre') || para.startsWith('\u003chr')) {
        return para;
      }
      // 处理换行
      return `\u003cp\u003e${para.replace(/\n/g, '\u003cbr\u003e')}\u003c/p\u003e`;
    })
    .join('\n');
  
  return html;
}

// 读取章节文件
function getChapters() {
  const files = fs.readdirSync(CHAPTERS_DIR);
  
  // 筛选 md 文件并按序号排序
  const chapterFiles = files
    .filter(f => f.endsWith('.md'))
    .sort((a, b) => {
      // 尝试提取数字进行排序
      const numA = parseInt(a.match(/\d+/)?.[0] || '0');
      const numB = parseInt(b.match(/\d+/)?.[0] || '0');
      return numA - numB;
    });
  
  return chapterFiles.map(file => {
    const filePath = path.join(CHAPTERS_DIR, file);
    const content = fs.readFileSync(filePath, 'utf8');
    
    // 提取章节标题（第一行 # 后面的内容）
    const titleMatch = content.match(/^#\s*(.+)$/m);
    const title = titleMatch ? titleMatch[1] : file.replace('.md', '');
    
    // 转换 Markdown 为 HTML
    const html = markdownToHtml(content);
    
    return {
      title: title,
      data: html
    };
  });
}

// 生成 EPUB
async function generateEpub() {
  console.log(`📚 开始导出《${bookTitle}》...`);
  
  // 检查章节目录
  if (!fs.existsSync(CHAPTERS_DIR)) {
    console.log('❌ 未找到 chapters 目录');
    process.exit(1);
  }
  
  const chapters = getChapters();
  console.log(`📖 读取到 ${chapters.length} 个章节`);
  
  if (chapters.length === 0) {
    console.log('❌ 没有找到章节文件');
    process.exit(1);
  }
  
  // 生成文件名
  const dateStr = new Date().toISOString().split('T')[0];
  const outputFile = path.join(OUTPUT_DIR, `${bookTitle}_${dateStr}.epub`);
  
  // EPUB 配置
  const options = {
    title: bookTitle,
    author: author,
    publisher: 'Time Weaver Studio',
    description: `《${bookTitle}》是一部穿越小说，由 Time Weaver 创作。`,
    tocTitle: '目录',
    lang: 'zh-CN',
    content: chapters
  };
  
  console.log('📝 正在生成 EPUB...');
  
  try {
    // epub-gen 使用回调方式
    new Epub(options, outputFile).promise
      .then(() => {
        console.log('✅ 导出成功！');
        console.log(`📂 文件路径: ${outputFile}`);
        const stats = fs.statSync(outputFile);
        console.log(`📊 文件大小: ${(stats.size / 1024).toFixed(2)} KB`);
      })
      .catch(err => {
        console.error('❌ 导出失败:', err.message);
        process.exit(1);
      });
      
  } catch (err) {
    console.error('❌ 导出失败:', err.message);
    process.exit(1);
  }
}

generateEpub();
