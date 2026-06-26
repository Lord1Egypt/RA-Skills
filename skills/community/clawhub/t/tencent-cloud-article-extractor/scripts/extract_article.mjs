#!/usr/bin/env node

/**
 * 腾讯云开发者社区文章提取器
 * 
 * 用法: node extract_article.mjs <文章URL> [输出文件路径]
 * 
 * 参数:
 *   文章URL      - 腾讯云文章链接 (如 https://cloud.tencent.com/developer/article/2636150)
 *   输出文件路径  - 可选，默认输出到 stdout
 * 
 * 示例:
 *   node extract_article.mjs https://cloud.tencent.com/developer/article/2636150
 *   node extract_article.mjs https://cloud.tencent.com/developer/article/2636150 article.md
 */

import { writeFileSync } from 'fs';
import { exit } from 'process';

const args = process.argv.slice(2);

if (args.length < 1) {
  console.error('用法: node extract_article.mjs <文章URL> [输出文件路径]');
  console.error('');
  console.error('示例:');
  console.error('  node extract_article.mjs https://cloud.tencent.com/developer/article/2636150');
  console.error('  node extract_article.mjs https://cloud.tencent.com/developer/article/2636150 article.md');
  exit(1);
}

const articleUrl = args[0];
const outputPath = args[1];

// 验证 URL 格式
const urlPattern = /^https?:\/\/cloud\.tencent\.com\/developer\/article\/(\d+)/;
const match = articleUrl.match(urlPattern);

if (!match) {
  console.error('错误: 无效的腾讯云文章 URL');
  console.error('URL 格式应为: https://cloud.tencent.com/developer/article/<文章ID>');
  exit(1);
}

const articleId = match[1];

console.error(`正在获取文章: ${articleUrl}`);

try {
  const response = await fetch(articleUrl, {
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
  });

  if (!response.ok) {
    console.error(`错误: HTTP ${response.status} - ${response.statusText}`);
    exit(1);
  }

  const html = await response.text();
  
  // 提取 __NEXT_DATA__ 中的 JSON
  const dataMatch = html.match(/<script id="__NEXT_DATA__" type="application\/json">([\s\S]*?)<\/script>/);
  
  if (!dataMatch) {
    console.error('错误: 未找到文章数据 (__NEXT_DATA__)');
    console.error('可能原因: 页面结构变化或需要登录');
    exit(1);
  }

  const data = JSON.parse(dataMatch[1]);
  
  // 获取文章内容和元数据
  const fallbackKey = `#url:"/api/article/detail",params:#articleId:${articleId},,`;
  const articleData = data.props?.pageProps?.fallback?.[fallbackKey];
  
  if (!articleData) {
    console.error('错误: 未找到文章内容');
    console.error('可用的 fallback keys:', Object.keys(data.props?.pageProps?.fallback || {}));
    exit(1);
  }

  const articleInfo = articleData.articleInfo || {};
  const articleStats = articleData.articleData || {};
  const content = articleInfo.content;

  if (!content) {
    console.error('错误: 文章内容为空');
    exit(1);
  }

  // 解析内容 JSON
  const doc = JSON.parse(content);

  // 转换为 Markdown
  function nodeToMarkdown(node, depth = 0) {
    if (!node) return '';
    
    if (node.type === 'text') {
      return node.text || '';
    }
    
    let result = '';
    
    if (node.type === 'doc' && node.content) {
      return node.content.map(n => nodeToMarkdown(n, depth)).join('\n\n');
    }
    
    if (node.type === 'heading') {
      const level = node.attrs?.level || 2;
      const prefix = '#'.repeat(level);
      const text = node.content?.map(n => nodeToMarkdown(n, depth)).join('') || '';
      result = `${prefix} ${text}`;
    }
    else if (node.type === 'paragraph') {
      const text = node.content?.map(n => nodeToMarkdown(n, depth)).join('') || '';
      result = text;
    }
    else if (node.type === 'codeBlock') {
      const code = node.content?.map(n => n.text || '').join('') || '';
      const lang = node.attrs?.language || '';
      result = `\`\`\`${lang}\n${code}\n\`\`\``;
    }
    else if (node.type === 'image') {
      const src = node.attrs?.src || '';
      const alt = node.attrs?.alt || '';
      result = `![${alt}](${src})`;
    }
    else if (node.type === 'blockquote') {
      const text = node.content?.map(n => nodeToMarkdown(n, depth)).join('') || '';
      const lines = text.split('\n');
      result = lines.map(line => `> ${line}`).join('\n');
    }
    else if (node.type === 'bulletList') {
      const items = node.content?.map(n => {
        const text = nodeToMarkdown(n, depth);
        return text.split('\n').map(line => `- ${line}`).join('\n');
      }) || [];
      result = items.join('\n');
    }
    else if (node.type === 'orderedList') {
      const items = node.content?.map((n, i) => {
        const text = nodeToMarkdown(n, depth);
        return text.split('\n').map(line => `${i + 1}. ${line}`).join('\n');
      }) || [];
      result = items.join('\n');
    }
    else if (node.type === 'listItem') {
      result = node.content?.map(n => nodeToMarkdown(n, depth)).join('') || '';
    }
    else if (node.type === 'hardBreak') {
      result = '\n';
    }
    else if (node.type === 'horizontalRule') {
      result = '---';
    }
    else if (node.content) {
      result = node.content.map(n => nodeToMarkdown(n, depth)).join('');
    }
    
    // 处理 marks (bold, italic, textStyle 等)
    if (node.marks) {
      for (const mark of node.marks) {
        if (mark.type === 'bold') {
          result = `**${result}**`;
        } else if (mark.type === 'italic') {
          result = `*${result}*`;
        } else if (mark.type === 'code') {
          result = `\`${result}\``;
        } else if (mark.type === 'link') {
          const href = mark.attrs?.href || '';
          result = `[${result}](${href})`;
        }
      }
    }
    
    return result;
  }

  // 构建完整的 Markdown 文档
  const title = articleInfo.title || '未命名文章';
  const author = articleInfo.authorInfo?.nickname || articleInfo.authorInfo?.name || '未知作者';
  
  // 格式化发布时间
  let publishTime = '';
  if (articleInfo.createTime) {
    // createTime 可能是时间戳（秒或毫秒）或已格式化的字符串
    const timestamp = parseInt(articleInfo.createTime);
    if (!isNaN(timestamp)) {
      // 判断是秒还是毫秒
      const date = new Date(timestamp > 10000000000 ? timestamp : timestamp * 1000);
      publishTime = date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        timeZone: 'Asia/Shanghai'
      }).replace(/\//g, '-');
    } else {
      publishTime = articleInfo.createTime;
    }
  }
  
  const wordsNum = articleStats.wordsNum || 0;
  const readingTime = articleStats.readingTime ? Math.round(articleStats.readingTime / 60) : 0;

  let markdown = `# ${title}\n\n`;
  markdown += `> 作者：${author}\n`;
  if (publishTime) {
    markdown += `> 发布时间：${publishTime}\n`;
  }
  markdown += `> 来源：腾讯云开发者社区\n`;
  markdown += `> 原文链接：${articleUrl}\n`;
  markdown += `\n---\n\n`;
  
  // 添加统计信息
  if (wordsNum > 0 || readingTime > 0) {
    markdown += `**文章统计**：`;
    if (wordsNum > 0) {
      markdown += `字数 ${wordsNum}`;
    }
    if (readingTime > 0) {
      markdown += ` | 预计阅读 ${readingTime} 分钟`;
    }
    markdown += `\n\n---\n\n`;
  }

  // 添加正文
  markdown += nodeToMarkdown(doc);

  // 输出结果
  if (outputPath) {
    writeFileSync(outputPath, markdown, 'utf-8');
    console.error(`文章已保存到: ${outputPath}`);
    console.error(`标题: ${title}`);
    console.error(`字数: ${wordsNum}`);
    console.error(`预计阅读时间: ${readingTime} 分钟`);
  } else {
    console.log(markdown);
  }

} catch (error) {
  console.error('错误:', error.message);
  exit(1);
}
