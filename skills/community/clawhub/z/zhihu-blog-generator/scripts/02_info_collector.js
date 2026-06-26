/**
 * Step 2: 信息收集
 * 根据选定的话题，从多个渠道收集信息：
 * - ArXiv 论文
 * - GitHub 项目
 * - 技术博客
 * - 知乎/StackOverflow 讨论
 */

const path = require('path');
const config = require('../lib/config');
const Logger = require('../lib/logger');
const FileUtils = require('../lib/file_utils');
const SearchUtils = require('../lib/search_utils');
const PaperParser = require('../lib/paper_parser');

// 解析命令行参数
const args = process.argv.slice(2);
const sessionId = args.find(a => a.startsWith('--session='))?.split('=')[1];

if (!sessionId) {
  console.error('错误：请提供会话ID，例如: --session=abc123');
  process.exit(1);
}

const logger = new Logger(sessionId);
const fileUtils = new FileUtils(sessionId);
const searchUtils = new SearchUtils(logger);
const paperParser = new PaperParser(logger);

/**
 * 模拟网页内容提取
 */
async function extractWebContent(url, title, source) {
  logger.info(`提取内容: ${url}`);
  
  // 实际使用时，这里应该调用 browser_use 或其他工具获取网页内容
  // 示例返回：
  return {
    title: title || 'Unknown Title',
    url: url,
    content: `这是从 ${source} 提取的内容示例。\n\n实际使用时，这里应该是网页的正文内容。`,
    source: source,
    extractedAt: new Date().toISOString(),
  };
}

/**
 * 收集信息主函数
 */
async function collectInformation(topic) {
  logger.setStep('02_info_collector');
  logger.info('开始收集信息', { topic: topic.title, keywords: topic.keywords });
  
  const collectedData = {
    topic: topic,
    webPages: [],
    papers: [],
    codeSnippets: [],
    collectedAt: new Date().toISOString(),
  };
  
  const searchKeyword = topic.title;
  
  // 1. 搜索 ArXiv 论文
  logger.info('搜索 ArXiv 论文...');
  try {
    // 示例：模拟搜索论文
    const paperUrls = [
      { title: 'Attention Is All You Need', url: 'https://arxiv.org/abs/1706.03762' },
      { title: 'BERT: Pre-training of Deep Bidirectional Transformers', url: 'https://arxiv.org/abs/1810.04805' },
    ];
    
    for (let i = 0; i < Math.min(paperUrls.length, config.paper.maxPapers); i++) {
      const paper = paperUrls[i];
      logger.info(`发现论文: ${paper.title}`);
      
      // 模拟解析论文（实际使用时下载并解析PDF）
      const paperInfo = {
        title: paper.title,
        url: paper.url,
        authors: ['Author A', 'Author B'],
        abstract: 'This is a sample abstract of the paper...',
        keywords: topic.keywords,
        relevance: 0.85,
      };
      
      collectedData.papers.push(paperInfo);
      
      // 保存论文信息
      fileUtils.savePaper(
        paper.title,
        paperInfo,
        { index: i, source: 'arxiv' }
      );
    }
  } catch (error) {
    logger.warn('搜索论文失败:', error.message);
  }
  
  // 2. 搜索 GitHub 项目
  logger.info('搜索 GitHub 项目...');
  try {
    const githubUrls = [
      { title: 'awesome-project', url: 'https://github.com/example/awesome-project', stars: '12.5k' },
      { title: 'tech-framework', url: 'https://github.com/example/tech-framework', stars: '8.3k' },
    ];
    
    for (let i = 0; i < githubUrls.length; i++) {
      const project = githubUrls[i];
      const content = await extractWebContent(
        project.url,
        project.title,
        'github'
      );
      
      content.metadata = { stars: project.stars };
      
      const filePath = fileUtils.saveWebPage(
        i + 1,
        'github',
        project.title,
        JSON.stringify(content, null, 2)
      );
      
      collectedData.webPages.push({
        ...content,
        localPath: filePath,
      });
    }
  } catch (error) {
    logger.warn('搜索 GitHub 失败:', error.message);
  }
  
  // 3. 搜索技术博客/文章
  logger.info('搜索技术文章...');
  try {
    const blogUrls = [
      { title: '深入理解技术原理', url: 'https://example-blog.com/tech-deep-dive', source: 'blog' },
      { title: '实战经验分享', url: 'https://example-blog.com/practice', source: 'blog' },
    ];
    
    for (let i = 0; i < blogUrls.length; i++) {
      const article = blogUrls[i];
      const content = await extractWebContent(
        article.url,
        article.title,
        article.source
      );
      
      const filePath = fileUtils.saveWebPage(
        i + 10,
        article.source,
        article.title,
        JSON.stringify(content, null, 2)
      );
      
      collectedData.webPages.push({
        ...content,
        localPath: filePath,
      });
    }
  } catch (error) {
    logger.warn('搜索技术文章失败:', error.message);
  }
  
  // 4. 搜索知乎讨论
  logger.info('搜索知乎讨论...');
  try {
    const zhihuUrls = [
      { title: '如何评价这项技术？', url: 'https://zhuanlan.zhihu.com/p/example', source: 'zhihu' },
    ];
    
    for (let i = 0; i < zhihuUrls.length; i++) {
      const article = zhihuUrls[i];
      const content = await extractWebContent(
        article.url,
        article.title,
        'zhihu'
      );
      
      const filePath = fileUtils.saveWebPage(
        i + 20,
        'zhihu',
        article.title,
        JSON.stringify(content, null, 2)
      );
      
      collectedData.webPages.push({
        ...content,
        localPath: filePath,
      });
    }
  } catch (error) {
    logger.warn('搜索知乎失败:', error.message);
  }
  
  // 保存收集结果
  fileUtils.saveJSON('collected_data.json', collectedData, 'collected');
  
  logger.info('信息收集完成', {
    papersCount: collectedData.papers.length,
    webPagesCount: collectedData.webPages.length,
  });
  
  return collectedData;
}

/**
 * 主函数
 */
async function main() {
  // 读取话题选择结果
  const topicData = fileUtils.readJSON('user_selection.json', 'topic');
  
  if (!topicData) {
    logger.error('未找到话题选择结果，请先运行 01_topic_selector.js');
    process.exit(1);
  }
  
  const topic = topicData.selectedTopic;
  logger.info('读取话题', { title: topic.title });
  
  // 收集信息
  const collectedData = await collectInformation(topic);
  
  // 输出下一步提示
  console.log('\n========== 下一步 ==========');
  console.log(`运行: node scripts/03_blog_generator.js --session=${sessionId}`);
  console.log('============================\n');
}

// 运行主函数
main().catch(error => {
  logger.error('信息收集失败:', error.message);
  process.exit(1);
});
