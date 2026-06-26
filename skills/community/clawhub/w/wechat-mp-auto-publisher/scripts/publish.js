#!/usr/bin/env node

/**
 * 发布到微信公众号
 * 
 * 用法：node scripts/publish.js article.md
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const articleFile = process.argv[2];
if (!articleFile || !fs.existsSync(articleFile)) {
  console.log('❌ 用法：node publish.js article.md');
  process.exit(1);
}

console.log('📱 开始发布...');

// 检查 frontmatter
const article = fs.readFileSync(articleFile, 'utf8');
const hasTitle = /^---\n[\s\S]*?title:/m.test(article);
const hasCover = /^---\n[\s\S]*?cover:/m.test(article);

if (!hasTitle || !hasCover) {
  console.log('❌ 文章缺少 frontmatter（title 和 cover）');
  process.exit(1);
}

console.log('✅ frontmatter 检查通过');

// 调用 wechat-toolkit 发布
const publishScript = path.join(__dirname, '../../wechat-toolkit/scripts/publisher/publish.js');
if (fs.existsSync(publishScript)) {
  try {
    execSync(`node "${publishScript}" "${articleFile}"`, {
      encoding: 'utf8',
      env: { ...process.env },
      stdio: 'inherit',
    });
    console.log('\n✅ 发布完成！');
  } catch (error) {
    console.error('❌ 发布失败:', error.message);
    process.exit(1);
  }
} else {
  console.log('❌ 未找到 wechat-toolkit 发布脚本');
  console.log('请安装：clawhub install wechat-toolkit');
  process.exit(1);
}
