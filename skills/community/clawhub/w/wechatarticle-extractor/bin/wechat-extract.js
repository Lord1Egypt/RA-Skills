#!/usr/bin/env node

const { extract } = require('../scripts/extract');
const cheerio = require('cheerio');
const fs = require('fs');
const path = require('path');

// ANSI colors
const colors = {
  green: (text) => `\x1b[32m${text}\x1b[0m`,
  yellow: (text) => `\x1b[33m${text}\x1b[0m`,
  red: (text) => `\x1b[31m${text}\x1b[0m`,
  blue: (text) => `\x1b[34m${text}\x1b[0m`,
  gray: (text) => `\x1b[90m${text}\x1b[0m`
};

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    showHelp();
    return;
  }

  const url = args[0];
  const options = {
    output: args.includes('--output') ? args[args.indexOf('--output') + 1] : null,
    format: args.includes('--format') ? args[args.indexOf('--format') + 1] : 'markdown',
    json: args.includes('--json')
  };

  console.log(colors.blue('📱 正在提取微信公众号文章...'));

  try {
    const result = await extract(url);

    if (!result.done) {
      console.error(colors.red(`❌ 提取失败: ${result.msg} (错误码: ${result.code})`));
      process.exit(1);
    }

    const data = result.data;

    console.log(colors.green('✅ 提取成功!\n'));

    if (options.json) {
      console.log(JSON.stringify(data, null, 2));
      return;
    }

    // Display article info
    console.log(colors.gray('─'.repeat(50)));
    console.log(colors.yellow('标题:'), data.msg_title);
    console.log(colors.yellow('作者:'), data.msg_author || data.account_name);
    console.log(colors.yellow('公众号:'), data.account_name);
    console.log(colors.yellow('发布时间:'), data.msg_publish_time_str);
    console.log(colors.yellow('原文链接:'), data.msg_link);
    console.log(colors.gray('─'.repeat(50)));

    // Convert to markdown if requested
    if (options.format === 'markdown' || options.format === 'md') {
      const markdown = convertToMarkdown(data);
      const outputPath = options.output || path.join(process.cwd(), 'wechat-article.md');

      fs.writeFileSync(outputPath, markdown, 'utf8');
      console.log(colors.green(`\n📄 Markdown 已保存到: ${outputPath}`));
      console.log(colors.gray(`文件大小: ${(markdown.length / 1024).toFixed(2)} KB`));
    }

    // Show content preview
    if (data.msg_content) {
      const $ = cheerio.load(data.msg_content, { decodeEntities: false });
      const textPreview = $.text().trim().substring(0, 200);
      console.log(colors.gray('\n📖 内容预览:'));
      console.log(colors.gray(textPreview + '...'));
    }

  } catch (error) {
    console.error(colors.red(`❌ 发生错误: ${error.message}`));
    process.exit(1);
  }
}

function convertToMarkdown(data) {
  const $ = cheerio.load(data.msg_content, { decodeEntities: false });

  let markdown = `# ${data.msg_title}

**作者**: ${data.msg_author || data.account_name}
**发布时间**: ${data.msg_publish_time_str}
**公众号**: ${data.account_name}
**原文链接**: ${data.msg_link}

---

`;

  function processElement(elem) {
    const $elem = $(elem);
    const tagName = elem.tagName?.toLowerCase();

    if (!tagName) return;

    if (tagName === 'h2') {
      markdown += '\n## ' + $elem.text().trim() + '\n\n';
    } else if (tagName === 'h3') {
      markdown += '\n### ' + $elem.text().trim() + '\n\n';
    } else if (tagName === 'p') {
      let text = '';
      $elem.contents().each((i, child) => {
        if (child.type === 'text') {
          text += child.data;
        } else if (child.type === 'tag') {
          const $child = $(child);
          if (['strong', 'b', 'span'].includes(child.tagName)) {
            text += $child.text();
          } else if (child.tagName === 'br') {
            text += '\n';
          } else {
            text += $child.text();
          }
        }
      });
      text = text.trim();
      if (text) markdown += text + '\n\n';
    } else if (tagName === 'blockquote') {
      const text = $elem.text().trim();
      if (text) markdown += '> ' + text + '\n\n';
    } else if (tagName === 'ol') {
      $elem.children('li').each((i, li) => {
        const text = $(li).text().trim();
        if (text) markdown += `${i + 1}. ${text}\n`;
      });
      markdown += '\n';
    } else if (tagName === 'ul') {
      $elem.children('li').each((i, li) => {
        const text = $(li).text().trim();
        if (text) markdown += `- ${text}\n`;
      });
      markdown += '\n';
    } else if (tagName === 'img') {
      const src = $elem.attr('data-src') || $elem.attr('src');
      if (src) markdown += `\n![图片](${src})\n\n`;
    } else if (tagName === 'pre') {
      const codeText = $elem.find('code').text() || $elem.text();
      if (codeText.trim()) {
        markdown += '\n```\n' + codeText.trim() + '\n```\n\n';
      }
    } else if (['section', 'div', 'center'].includes(tagName)) {
      $elem.children().each((i, child) => {
        processElement(child);
      });
    }
  }

  const mainSection = $('section[data-plugin="note-to-mp"]');
  if (mainSection.length) {
    mainSection.children().each((i, child) => processElement(child));
  } else {
    $('body').children().each((i, child) => processElement(child));
  }

  return markdown.replace(/\n{3,}/g, '\n\n');
}

function showHelp() {
  console.log(`
${colors.green('微信公众号文章提取工具')}

${colors.yellow('用法:')}
  npx wechat-article-extractor <URL> [选项]

${colors.yellow('参数:')}
  <URL>                    微信公众号文章链接

${colors.yellow('选项:')}
  -h, --help               显示帮助信息
  --output <path>          输出文件路径 (默认: ./wechat-article.md)
  --format <format>        输出格式 (markdown|json|html) (默认: markdown)
  --json                   直接输出JSON格式

${colors.yellow('示例:')}
  # 提取文章并保存为markdown
  npx wechat-article-extractor https://mp.weixin.qq.com/s/xxx

  # 指定输出路径
  npx wechat-article-extractor https://mp.weixin.qq.com/s/xxx --output ./articles/post.md

  # 输出JSON格式
  npx wechat-article-extractor https://mp.weixin.qq.com/s/xxx --json

${colors.gray('注意:')}
  需要网络连接来获取文章内容
  如果遇到"访问过于频繁"错误，请稍后再试
`);
}

main();
