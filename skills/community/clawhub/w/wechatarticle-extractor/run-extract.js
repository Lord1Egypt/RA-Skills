const { extract } = require('./scripts/extract');
const cheerio = require('cheerio');
const fs = require('fs');

const url = 'https://mp.weixin.qq.com/s/OmlRx3K8Ij-5nHxNB4YNfQ';

async function main() {
  console.log('正在提取文章...');
  const result = await extract(url);

  if (!result.done) {
    console.error('提取失败:', result.msg, result.code);
    process.exit(1);
  }

  const data = result.data;

  console.log('\n=== 文章信息 ===');
  console.log('标题:', data.msg_title);
  console.log('作者:', data.msg_author || data.account_name);
  console.log('公众号:', data.account_name);
  console.log('发布时间:', data.msg_publish_time_str);
  console.log('原文链接:', data.msg_link);

  // 转换为markdown格式
  const $ = cheerio.load(data.msg_content, { decodeEntities: false });

  let markdown = `\n# ${data.msg_title}

**作者**: ${data.msg_author || data.account_name}
**发布时间**: ${data.msg_publish_time_str}
**公众号**: ${data.account_name}
**原文链接**: ${data.msg_link}

---

`;

  function processElement(elem, isRoot = false) {
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
          if (child.tagName === 'strong' || child.tagName === 'b' || child.tagName === 'span') {
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
        if (text) markdown += (i + 1) + '. ' + text + '\n';
      });
      markdown += '\n';
    } else if (tagName === 'ul') {
      $elem.children('li').each((i, li) => {
        const text = $(li).text().trim();
        if (text) markdown += '- ' + text + '\n';
      });
      markdown += '\n';
    } else if (tagName === 'img') {
      const src = $elem.attr('data-src') || $elem.attr('src');
      if (src) markdown += '\n![图片](' + src + ')\n\n';
    } else if (tagName === 'code') {
      const text = $elem.text().trim();
      if (text) markdown += '`' + text + '`';
    } else if (tagName === 'pre' || (tagName === 'section' && $elem.hasClass('code-snippet__fix'))) {
      const codeText = $elem.find('code').text() || $elem.text();
      if (codeText.trim()) {
        markdown += '\n```\n' + codeText.trim() + '\n```\n\n';
      }
    } else if (tagName === 'section' || tagName === 'div' || tagName === 'center') {
      $elem.children().each((i, child) => {
        processElement(child);
      });
    }
  }

  const mainSection = $('section[data-plugin="note-to-mp"]');
  if (mainSection.length) {
    mainSection.children().each((i, child) => {
      processElement(child, true);
    });
  } else {
    $('body').children().each((i, child) => {
      processElement(child, true);
    });
  }

  markdown = markdown.replace(/\n{3,}/g, '\n\n');

  // 保存文件
  const outputPath = 'C:/Users/xsl/.openclaw/workspace/wechat-article.md';
  fs.writeFileSync(outputPath, markdown, 'utf8');

  console.log('\n文章已保存到:', outputPath);
  console.log('文件大小:', (markdown.length / 1024).toFixed(2), 'KB');

  // 输出markdown内容到控制台
  console.log('\n=== 文章内容 ===');
  console.log(markdown);
}

main().catch(console.error);
