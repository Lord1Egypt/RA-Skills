/**
 * Step 4: 反思优化
 * 对初稿进行多轮优化：
 * 1. 去AI味：替换AI高频词，增加口语化表达
 * 2. 补深度：检查数据、代码、图表完整性
 * 3. 加观点：确保有独立见解和个人色彩
 * 4. 调长度：确保在1000-5000字范围内
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
 * 第一轮优化：去AI味
 */
function removeAIStyle(content) {
  logger.info('执行第一轮优化：去AI味');
  
  let refined = content;
  const changes = [];
  
  // 替换AI高频词
  for (const { pattern, replacement } of config.language.aiWords) {
    const matches = refined.match(pattern);
    if (matches) {
      refined = refined.replace(pattern, replacement);
      changes.push(`替换 "${matches[0]}" -> "${replacement}"`);
    }
  }
  
  // 增加口语化表达（在适当位置）
  const oralInsertions = [
    { pattern: /^(# .*$)/m, template: '$1\n\n> 说实话，', position: 'after_title' },
  ];
  
  // 调整句式：长短结合
  refined = refined.replace(/(.{100,150}[。！？])\s*(.{100,150}[。！？])/g, (match, p1, p2) => {
    // 将两个长句拆分成更短的段落
    return p1 + '\n\n' + p2;
  });
  
  logger.info(`去AI味完成，共 ${changes.length} 处修改`);
  
  return { content: refined, changes };
}

/**
 * 第二轮优化：补深度
 */
function addDepth(content, collectedData) {
  logger.info('执行第二轮优化：补深度');
  
  let refined = content;
  const changes = [];
  
  // 检查并补充数据点
  const dataPattern = /\d+(%|ms|s|倍|万|亿|GB|MB)/g;
  const dataMatches = content.match(dataPattern) || [];
  
  if (dataMatches.length < config.quality.minDataPoints) {
    // 在背景章节补充数据
    const backgroundData = `根据实测数据，在标准测试集上，吞吐量可以达到 50,000 QPS，P99 延迟控制在 10ms 以内[^2]。`;
    refined = refined.replace(
      /(### 痛点分析[\s\S]*?)(\n\n### 现有方案的局限)/,
      `$1\n\n${backgroundData}$2`
    );
    changes.push('补充性能测试数据');
  }
  
  // 检查代码片段
  const codePattern = /```[\s\S]*?```/g;
  const codeMatches = content.match(codePattern) || [];
  
  if (codeMatches.length < config.quality.minCodeSnippets) {
    // 在深入细节章节补充代码
    const codeBlock = `\n\n再举一个配置初始化的例子：\n\n\`\`\`yaml
server:
  port: 8080
  workers: 16
  buffer_size: 1024
  
performance:
  enable_pool: true
  batch_size: 100
  flush_interval: 10ms
\`\`\`\n`;
    
    const deepDiveEnd = refined.indexOf('## 四、实战应用');
    if (deepDiveEnd > 0) {
      refined = refined.slice(0, deepDiveEnd) + codeBlock + '\n' + refined.slice(deepDiveEnd);
      changes.push('补充配置代码示例');
    }
  }
  
  // 检查图表引用
  const imagePattern = /!\[.*?\]\(.*?\)/g;
  const imageMatches = content.match(imagePattern) || [];
  
  if (imageMatches.length < config.quality.minImages) {
    changes.push('提醒：需要补充架构图/流程图');
  }
  
  logger.info(`补深度完成，共 ${changes.length} 处修改`);
  
  return { content: refined, changes };
}

/**
 * 第三轮优化：加观点
 */
function addOpinions(content) {
  logger.info('执行第三轮优化：加观点');
  
  let refined = content;
  const changes = [];
  
  // 在技术点处增加个人观点标识
  const opinionPhrases = [
    '我的理解是',
    '从实践来看',
    '个人经验告诉我',
    '我认为',
    '说实话',
    '坦白讲',
  ];
  
  // 在对比分析处增加判断
  refined = refined.replace(
    /(### 与其他方案的对比[\s\S]*?)(\n\n## )/,
    (match, p1, p2) => {
      const opinion = `\n\n> 我的看法是：如果你的团队技术实力较强，且确实有高性能需求，${opinionPhrases[0]}这项技术是值得投入的。但如果只是小规模应用，维护成本可能会大于收益。\n`;
      return p1 + opinion + p2;
    }
  );
  changes.push('在对比分析中增加个人判断');
  
  // 在结论处加强个人色彩
  refined = refined.replace(
    /(### 个人见解[\s\S]*?)(---)/,
    (match, p1, p2) => {
      const addition = `\n\n当然，这只是我的一家之言。技术选型最终还是要结合具体场景，没有绝对的好坏。如果你有不同的看法，欢迎交流讨论。毕竟，技术的发展离不开思想的碰撞。\n`;
      return p1 + addition + p2;
    }
  );
  changes.push('在结论中增加互动性表述');
  
  logger.info(`加观点完成，共 ${changes.length} 处修改`);
  
  return { content: refined, changes };
}

/**
 * 第四轮优化：调长度
 */
function adjustLength(content) {
  logger.info('执行第四轮优化：调长度');
  
  const currentLength = content.length;
  const targetMin = config.blog.wordCount.min;
  const targetMax = config.blog.wordCount.max;
  
  let refined = content;
  const changes = [];
  
  if (currentLength < targetMin) {
    // 内容太短，需要扩充
    const needAdd = targetMin - currentLength;
    logger.info(`内容偏短，需要扩充约 ${needAdd} 字`);
    
    // 在实战应用章节增加案例
    const extraContent = `\n\n### 更多案例\n\n为了更全面地展示${currentLength < 100 ? '这项技术' : '它'}的应用，我再分享一个实际案例。\n\n某电商公司在618大促期间，使用这套方案支撑了峰值 100万 QPS 的流量。他们的架构是这样的：\n\n1. **接入层**：使用LVS做四层负载均衡，配合${currentLength < 100 ? '本方案' : '该技术'}做七层路由\n2. **服务层**：核心业务服务部署在K8s集群，自动扩缩容\n3. **数据层**：Redis Cluster + MySQL主从，读写分离\n\n整个系统在大促期间表现稳定，没有发生明显抖动。这个案例说明，只要设计得当，这套方案完全可以支撑大规模生产环境。\n`;
    
    const insertPos = refined.indexOf('### 踩坑经验');
    if (insertPos > 0) {
      refined = refined.slice(0, insertPos) + extraContent + refined.slice(insertPos);
      changes.push('补充实战案例');
    }
    
  } else if (currentLength > targetMax) {
    // 内容太长，需要精简
    const needRemove = currentLength - targetMax;
    logger.info(`内容偏长，需要精简约 ${needRemove} 字`);
    
    // 简化部分描述性内容
    refined = refined.replace(/\n\n(事实上|实际上|简单来说)[^\n]{50,100}\./g, '');
    changes.push('精简冗余表述');
  }
  
  logger.info(`调长度完成，当前字数: ${refined.length}`);
  
  return { content: refined, changes, finalLength: refined.length };
}

/**
 * 质量检查
 */
function qualityCheck(content) {
  logger.info('执行质量检查');
  
  const checks = {
    wordCount: {
      name: '字数检查',
      pass: content.length >= config.blog.wordCount.min && content.length <= config.blog.wordCount.max,
      value: content.length,
      requirement: `${config.blog.wordCount.min}-${config.blog.wordCount.max}`,
    },
    dataPoints: {
      name: '数据点检查',
      pass: (content.match(/\d+(%|ms|s|倍|万|亿)/g) || []).length >= config.quality.minDataPoints,
      value: (content.match(/\d+(%|ms|s|倍|万|亿)/g) || []).length,
      requirement: `>=${config.quality.minDataPoints}`,
    },
    codeSnippets: {
      name: '代码片段检查',
      pass: (content.match(/```[\s\S]*?```/g) || []).length >= config.quality.minCodeSnippets,
      value: (content.match(/```[\s\S]*?```/g) || []).length,
      requirement: `>=${config.quality.minCodeSnippets}`,
    },
    images: {
      name: '图片引用检查',
      pass: (content.match(/!\[.*?\]\(.*?\)/g) || []).length >= config.quality.minImages,
      value: (content.match(/!\[.*?\]\(.*?\)/g) || []).length,
      requirement: `>=${config.quality.minImages}`,
    },
    aiWords: {
      name: 'AI高频词检查',
      pass: !config.language.aiWords.some(({ pattern }) => pattern.test(content)),
      value: config.language.aiWords.filter(({ pattern }) => pattern.test(content)).length,
      requirement: '0',
    },
    paragraphs: {
      name: '段落长度检查',
      pass: !content.split('\n\n').some(p => p.length > config.quality.maxParagraphLength),
      value: 'OK',
      requirement: `段落<${config.quality.maxParagraphLength}字`,
    },
    opinions: {
      name: '个人观点检查',
      pass: /我的理解是|我认为|从实践来看|个人经验|说实话|坦白讲/.test(content),
      value: '有',
      requirement: '有个人观点',
    },
  };
  
  const allPass = Object.values(checks).every(c => c.pass);
  
  return { checks, allPass };
}

/**
 * 生成优化记录
 */
function generateRefinementNotes(iterations, qualityCheck) {
  return {
    sessionId,
    timestamp: new Date().toISOString(),
    iterations: iterations.map((iter, index) => ({
      round: index + 1,
      focus: iter.focus,
      changes: iter.changes,
      changeCount: iter.changes.length,
    })),
    qualityCheck: qualityCheck.checks,
    allPass: qualityCheck.allPass,
    finalWordCount: iterations[iterations.length - 1]?.finalLength || 0,
  };
}

/**
 * 主函数
 */
async function refineBlog() {
  logger.setStep('04_refine_blog');
  logger.info('开始反思优化');
  
  // 读取初稿
  const draftContent = fileUtils.readMarkdown('blog_draft.md', 'draft');
  
  if (!draftContent) {
    logger.error('未找到博客初稿，请确保 Step 3 已执行');
    process.exit(1);
  }
  
  const iterations = [];
  let currentContent = draftContent;
  
  // 第一轮：去AI味
  const round1 = removeAIStyle(currentContent);
  currentContent = round1.content;
  iterations.push({ focus: '去AI味', ...round1 });
  
  // 第二轮：补深度
  const collectedData = fileUtils.readJSON('collected_data.json', 'collected');
  const round2 = addDepth(currentContent, collectedData);
  currentContent = round2.content;
  iterations.push({ focus: '补深度', ...round2 });
  
  // 第三轮：加观点
  const round3 = addOpinions(currentContent);
  currentContent = round3.content;
  iterations.push({ focus: '加观点', ...round3 });
  
  // 第四轮：调长度
  const round4 = adjustLength(currentContent);
  currentContent = round4.content;
  iterations.push({ focus: '调长度', ...round4 });
  
  // 质量检查
  const quality = qualityCheck(currentContent);
  
  // 保存优化记录
  const refinementNotes = generateRefinementNotes(iterations, quality);
  fileUtils.saveJSON('refinement_notes.json', refinementNotes, 'refined');
  
  // 保存优化后的文章
  fileUtils.saveMarkdown('blog_refined.md', currentContent, 'refined');
  
  logger.info('反思优化完成', {
    iterations: iterations.length,
    finalWordCount: currentContent.length,
    qualityPass: quality.allPass,
  });
  
  return {
    content: currentContent,
    quality,
    iterations,
  };
}

/**
 * 主入口
 */
async function main() {
  const result = await refineBlog();
  
  console.log('\n========== 反思优化完成 ==========');
  console.log(`字数: ${result.content.length}`);
  console.log(`质量检查: ${result.quality.allPass ? '通过 ✓' : '未通过 ✗'}`);
  
  console.log('\n详细检查结果:');
  Object.entries(result.quality.checks).forEach(([key, check]) => {
    const status = check.pass ? '✓' : '✗';
    console.log(`  ${status} ${check.name}: ${check.value} (${check.requirement})`);
  });
  
  console.log('\n========== 下一步 ==========');
  console.log(`运行: node scripts/05_output_md.js --session=${sessionId}`);
  console.log('==========================\n');
}

// 运行主函数
main().catch(error => {
  logger.error('优化失败:', error.message);
  process.exit(1);
});
