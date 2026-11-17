#!/usr/bin/env node
/**
 * zentao-build-comment.js — 将分析报告 Markdown 转为禅道兼容 HTML
 *
 * 用法:
 *   node zentao-build-comment.js <report.md> [--out <output.html>]
 *
 *   不指定 --out 则输出到 stdout。
 *   输出末尾自动追加来源标记。
 *
 * 转换规则（与 SKILL.md 步骤 5 一致）:
 *   # xxx        → <h1>xxx</h1>
 *   ## xxx       → <h2>xxx</h2>
 *   ### xxx      → <h3>xxx</h3>
 *   #### xxx     → <h4>xxx</h4>
 *   **xxx**      → <b>xxx</b>
 *   *xxx*        → <i>xxx</i>
 *   `xxx`        → <code>xxx</code>
 *   [text](url)  → <a href="url">text</a>
 *   - xxx        → <p>- xxx</p>
 *   代码块       → <pre><code>...</code></pre>
 *   普通段落     → <p>xxx</p>
 *   空行         → <br>
 *   > xxx        → <blockquote>xxx</blockquote>
 *   末尾自动附加 <p><i>— Bug终结者 · 自动分析</i></p>
 */

const fs = require('fs');
const path = require('path');

function parseArgs() {
  const args = process.argv.slice(2);
  const config = { input: '', output: '' };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--out' && i + 1 < args.length) {
      config.output = args[++i];
    } else if (!config.input && !args[i].startsWith('--')) {
      config.input = args[i];
    }
  }
  return config;
}

/**
 * HTML 实体转义。
 * 注意：& 必须先替换，避免二次编码（&amp; → &amp;amp;）。
 */
function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

/**
 * 对已转义的文本应用内联 Markdown 格式化。
 * 调用顺序：先 escapeHtml，再调用此函数。
 */
function applyInlineFormatting(text) {
  // [text](url) → <a href="url">text</a>（必须在 ** 之前，避免 url 中的内容被误处理）
  text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');

  // **bold** → <b>bold</b>
  text = text.replace(/\*\*(.+?)\*\*/g, '<b>$1</b>');

  // *italic* → <i>italic</i>（单星号，小心不匹配 ** 的残片）
  text = text.replace(/(?<!\*)\*([^*\n]+?)\*(?!\*)/g, '<i>$1</i>');

  // `code` → <code>code</code>
  text = text.replace(/`([^`]+)`/g, '<code>$1</code>');

  return text;
}

/**
 * 格式化标题行，先转义再应用内联格式。
 */
function formatHeading(line, prefix, tag) {
  const raw = line.substring(prefix.length).trim();
  const escaped = escapeHtml(raw);
  const formatted = applyInlineFormatting(escaped);
  return `<${tag}>${formatted}</${tag}>\n`;
}

function buildComment(markdown) {
  const lines = markdown.split(/\r?\n/);
  let result = '';
  let inCodeBlock = false;

  /**
   * 行内格式化快捷函数：对已转义的文本应用粗体/斜体/代码/链接。
   */
  function fmt(text) {
    return applyInlineFormatting(escapeHtml(text));
  }

  /**
   * 收集连续匹配同一模式的行（如连续 "- " 或 "N. " 或 "|...|"）。
   * 从 startIndex 开始，收集所有 trim 后非空且匹配 testFn 的行。
   * 返回 { items: string[], endIndex: number }。
   */
  function collectGroup(startIndex, testFn) {
    const items = [];
    let j = startIndex;
    while (j < lines.length) {
      const trimmed = lines[j].trim();
      if (trimmed === '' || !testFn(trimmed)) break;
      items.push(trimmed);
      j++;
    }
    return { items, endIndex: j };
  }

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();

    // Code block fence
    if (trimmed.startsWith('```')) {
      if (inCodeBlock) {
        result += '</code></pre>\n';
        inCodeBlock = false;
      } else {
        result += '<pre><code>';
        inCodeBlock = true;
      }
      continue;
    }

    if (inCodeBlock) {
      result += escapeHtml(line) + '\n';
      continue;
    }

    // Empty line → <br>
    if (trimmed === '') {
      result += '<br>\n';
      continue;
    }

    // Headings
    if (trimmed.startsWith('# ')) {
      result += formatHeading(trimmed, '# ', 'h1');
      continue;
    }
    if (trimmed.startsWith('## ')) {
      result += formatHeading(trimmed, '## ', 'h2');
      continue;
    }
    if (trimmed.startsWith('### ')) {
      result += formatHeading(trimmed, '### ', 'h3');
      continue;
    }
    if (trimmed.startsWith('#### ')) {
      result += formatHeading(trimmed, '#### ', 'h4');
      continue;
    }

    // Blockquote
    if (trimmed.startsWith('> ')) {
      const quoteText = escapeHtml(trimmed.substring(2).trim());
      result += '<blockquote>' + applyInlineFormatting(quoteText) + '</blockquote>\n';
      continue;
    }

    // Unordered list: consecutive "- " lines → <ul>
    if (trimmed.startsWith('- ')) {
      const { items, endIndex } = collectGroup(i, t => t.startsWith('- '));
      result += '<ul>\n';
      for (const item of items) {
        const content = fmt(item.substring(2).trim());
        result += '  <li>' + content + '</li>\n';
      }
      result += '</ul>\n';
      i = endIndex - 1; // skip ahead; loop increment will land on endIndex
      continue;
    }

    // Ordered list: consecutive "N. " lines → <ol>
    if (/^\d+\.\s/.test(trimmed)) {
      const { items, endIndex } = collectGroup(i, t => /^\d+\.\s/.test(t));
      result += '<ol>\n';
      for (const item of items) {
        const content = fmt(item.replace(/^\d+\.\s+/, ''));
        result += '  <li>' + content + '</li>\n';
      }
      result += '</ol>\n';
      i = endIndex - 1;
      continue;
    }

    // Table rows: consecutive |...| lines → <table>
    if (/^\|.+\|$/.test(trimmed)) {
      const { items, endIndex } = collectGroup(i, t => /^\|.+\|$/.test(t));
      result += '<table>\n';
      for (const row of items) {
        const cells = row.split('|').filter(c => c.trim() !== '');
        result += '  <tr>';
        for (const cell of cells) {
          result += '<td>' + fmt(cell.trim()) + '</td>';
        }
        result += '</tr>\n';
      }
      result += '</table>\n';
      i = endIndex - 1;
      continue;
    }

    // Regular paragraph
    result += '<p>' + fmt(trimmed) + '</p>\n';
  }

  // Close any unclosed code block
  if (inCodeBlock) {
    result += '</code></pre>\n';
  }

  // Append source footer
  result += '<p><i>— Bug终结者 · 自动分析</i></p>\n';

  return result.trim();
}

function main() {
  const config = parseArgs();

  if (!config.input) {
    console.error('[ERROR] 缺少输入文件参数');
    console.error('用法: node zentao-build-comment.js <report.md> [--out <output.html>]');
    process.exit(1);
  }

  if (!fs.existsSync(config.input)) {
    console.error('[ERROR] 文件不存在: ' + config.input);
    process.exit(1);
  }

  const markdown = fs.readFileSync(config.input, 'utf-8');
  const html = buildComment(markdown);

  if (config.output) {
    // 确保输出目录存在
    const outDir = path.dirname(config.output);
    if (outDir && !fs.existsSync(outDir)) {
      fs.mkdirSync(outDir, { recursive: true });
    }
    fs.writeFileSync(config.output, html, 'utf-8');
    console.error('[INFO] HTML 已写入: ' + config.output);
    console.log('OK');
  } else {
    process.stdout.write(html);
  }
}

main();
