/**
 * Step 5: 输出最终MD文档
 * 生成符合知乎风格的技术博客最终文档
 */

const config = require('../lib/config');
const Logger = require('../lib/logger');
const FileUtils = require('../lib/file_utils');

// 解析命令行参数
const args = process.argv.slice(2);
const sessionId = args.find(a => a.startsWith('--session='))?.split('=')[1];

if (!sessionId) {
  console.error('错误：请提供会话ID，例如: --session=abc123');
  process.exit(1);
}

const logger = new Logger(sessionId);
const fileUtils = new FileUtils(sessionId);

/**
 * 生成文章元数据头部
 */
function generateFrontMatter(title, topic, wordCount, collectedData) {
  const date = new Date();
  const keywords = topic.keywords || [topic.title];
  
  const papers = collectedData?.papers || [];
  const webPages = collectedData?.webPages || [];
  
  const sources = [
    ...papers.map((p, i) => ({ type: 'paper', title: p.title, url: p.url })),
    ...webPages.map((w, i) => ({ type: w.source, title: w.title, url: w.url })),
  ];
  
  return `---
title: "${title}"
date: "${date.toISOString().split('T')[0]}"
topic: "${topic.title}"
word_count: ${wordCount}
keywords: [${keywords.map(k => `"${k}"`).join(', ')}]
sources:
${sources.map(s => `  - type: "${s.type}"\n    title: "${s.title}"\n    url: "${s.url}"`).join('\n')}
---

`;
}

/**
 * 生成作者信息
 */
function generateAuthorInfo() {
  return `> **作者**：技术极客
> **发布时间**：${new Date().toLocaleDateString('zh-CN')}
> **标签**：技术深度 | 源码解读 | 实战经验

---

`;
}

/**
 * 格式化最终文章内容
 */
function formatFinalContent(content, title) {
  // 确保标题格式正确
  let formatted = content;
  
  // 添加文章开头引导
  if (!formatted.includes('**作者**')) {
    const intro = generateAuthorInfo();
    const titleEnd = formatted.indexOf('\n\n');
    if (titleEnd > 0) {
      formatted = formatted.slice(0, titleEnd + 2) + intro + formatted.slice(titleEnd + 2);
    }
  }
  
  // 确保结尾有推荐和互动
  if (!formatted.includes('推荐阅读')) {
    const ending = `\n\n---\n\n**觉得有帮助？** 欢迎点赞、收藏、转发，你的支持是我持续创作的动力！\n\n**推荐阅读：**\n- [上一篇技术文章]\n- [相关主题深度解析]\n\n**关于我**：专注后端架构与性能优化，热爱开源技术。关注专栏，获取更多干货内容。\n`;
    formatted += ending;
  }
  
  return formatted;
}

/**
 * 复制图片到输出目录
 */
async function copyImagesToOutput() {
  const imagesDir = fileUtils.getDir('images');
  const outputImagesDir = fileUtils.getDir('output') + '/images';
  
  // 确保输出图片目录存在
  const fs = require('fs');
  if (!fs.existsSync(outputImagesDir)) {
    fs.mkdirSync(outputImagesDir, { recursive: true });
  }
  
  // 复制图片（如果有）
  const images = [];
  if (fs.existsSync(imagesDir)) {
    const files = fs.readdirSync(imagesDir);
    for (const file of files) {
      if (/\.(png|jpg|jpeg|gif|svg)$/i.test(file)) {
        const sourcePath = `${imagesDir}/${file}`;
        const destPath = `${outputImagesDir}/${file}`;
        fs.copyFileSync(sourcePath, destPath);
        images.push({
          filename: file,
          path: `images/${file}`,
        });
      }
    }
  }
  
  return images;
}

/**
 * 生成README说明文件
 */
function generateReadme(title, wordCount, qualityInfo) {
  return `# ${title}

## 文章信息

- **字数**: ${wordCount}
- **生成时间**: ${new Date().toLocaleString('zh-CN')}
- **质量评分**: 
${Object.entries(qualityInfo.checks).map(([key, check]) => `  - ${check.name}: ${check.pass ? '✓' : '✗'}`).join('\n')}

## 文件说明

- **最终文章**: ${fileUtils.generateFileName(title)}
- **初稿**: ../03_draft/blog_draft.md
- **优化稿**: ../04_refined/blog_refined.md
- **优化记录**: ../04_refined/refinement_notes.json

## 目录结构

\`\`\`
${sessionId}/
├── 01_topic/           # 话题选择
├── 02_collected/       # 收集的资料
│   ├── web_pages/      # 网页内容
│   └── papers/         # 论文解析
├── 03_draft/           # 初稿
├── 04_refined/         # 优化稿
└── 05_output/          # 最终输出
    ├── images/         # 图片资源
    └── *.md            # 最终文章
\`\`\`

## 发布建议

1. 检查所有链接是否可访问
2. 确认图片显示正常
3. 再次通读，修正明显的错别字
4. 调整标题吸引点击（但不要标题党）
5. 发布后关注评论反馈，及时回复
`;
}

/**
 * 主函数
 */
async function outputFinalDocument() {
  logger.setStep('05_output_md');
  logger.info('开始输出最终文档');
  
  // 读取必要的数据
  const refinedContent = fileUtils.readMarkdown('blog_refined.md', 'refined');
  const topicData = fileUtils.readJSON('user_selection.json', 'topic');
  const collectedData = fileUtils.readJSON('collected_data.json', 'collected');
  const refinementNotes = fileUtils.readJSON('refinement_notes.json', 'refined');
  const outline = fileUtils.readJSON('outline.json', 'draft');
  
  if (!refinedContent || !topicData) {
    logger.error('缺少必要的数据，请确保前面步骤已执行');
    process.exit(1);
  }
  
  const topic = topicData.selectedTopic;
  const title = outline?.title || topic.title;
  const wordCount = refinedContent.length;
  
  logger.info('生成最终文档', { title, wordCount });
  
  // 生成Front Matter
  const frontMatter = generateFrontMatter(title, topic, wordCount, collectedData);
  
  // 格式化内容
  const formattedContent = formatFinalContent(refinedContent, title);
  
  // 组合最终文章
  const finalContent = frontMatter + formattedContent;
  
  // 生成文件名
  const fileName = fileUtils.generateFileName(title);
  
  // 复制图片
  const images = await copyImagesToOutput();
  logger.info('图片复制完成', { count: images.length });
  
  // 保存最终文章
  const outputPath = fileUtils.saveMarkdown(fileName, finalContent, 'output');
  logger.info('最终文章已保存', { path: outputPath });
  
  // 生成README
  const readmeContent = generateReadme(title, wordCount, refinementNotes);
  fileUtils.saveMarkdown('README.md', readmeContent, 'output');
  
  // 保存日志
  logger.save(fileUtils.sessionDir);
  
  // 生成执行摘要
  const summary = logger.getSummary();
  fileUtils.saveJSON('summary.json', summary, 'output');
  
  logger.info('输出完成', {
    fileName,
    wordCount,
    imagesCount: images.length,
  });
  
  return {
    title,
    fileName,
    outputPath,
    wordCount,
    images,
    summary,
  };
}

/**
 * 主入口
 */
async function main() {
  const result = await outputFinalDocument();
  
  console.log('\n========================================');
  console.log('🎉 知乎技术博客生成完成！');
  console.log('========================================\n');
  
  console.log(`📄 文章标题: ${result.title}`);
  console.log(`📝 字数统计: ${result.wordCount} 字`);
  console.log(`📁 输出文件: ${result.outputPath}`);
  console.log(`🖼️  图片数量: ${result.images.length}`);
  console.log(`⏱️  总耗时: ${result.summary.duration}`);
  
  console.log('\n📋 文件结构:');
  console.log('   D:\\techinsight\\reports\\blog_' + sessionId + '\\');
  console.log('   ├── 01_topic/');
  console.log('   ├── 02_collected/');
  console.log('   ├── 03_draft/');
  console.log('   ├── 04_refined/');
  console.log('   └── 05_output/');
  console.log('       ├── ' + result.fileName);
  console.log('       └── images/');
  
  console.log('\n✅ 发布前检查清单:');
  console.log('   [ ] 通读全文，检查错别字');
  console.log('   [ ] 确认所有链接可访问');
  console.log('   [ ] 检查图片显示正常');
  console.log('   [ ] 标题吸引人但不过分标题党');
  console.log('   [ ] 导语能在3秒内抓住读者');
  
  console.log('\n🚀 可以直接复制文章内容到知乎发布！\n');
}

// 运行主函数
main().catch(error => {
  logger.error('输出失败:', error.message);
  process.exit(1);
});
