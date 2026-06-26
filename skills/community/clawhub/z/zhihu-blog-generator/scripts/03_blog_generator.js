/**
 * Step 3: 博客初稿生成
 * 根据收集的信息，生成知乎风格的技术博客初稿
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
 * 生成新颖标题
 */
function generateTitle(topic, collectedData) {
  const styles = config.blog.titleStyles;
  const style = styles[Math.floor(Math.random() * styles.length)];
  
  // 根据主题和收集的信息生成标题
  const keywords = topic.keywords || [topic.title];
  const mainKeyword = keywords[0];
  
  // 示例标题生成
  const titles = [
    `${mainKeyword}深度解析：为什么它能改变游戏规则？`,
    `从源码看${mainKeyword}：我发现了这3个设计精髓`,
    `${mainKeyword}的5个核心机制，90%的人理解错了`,
    `实测${mainKeyword}：性能提升40%背后的秘密`,
    `${mainKeyword} vs 传统方案：我们跑了一个月的数据`,
  ];
  
  return titles[Math.floor(Math.random() * titles.length)];
}

/**
 * 生成文章大纲
 */
function generateOutline(topic, collectedData) {
  return {
    title: '',  // 后续填充
    sections: [
      {
        id: 'intro',
        title: '导语',
        type: 'intro',
        content: '',
        wordCount: config.blog.sections.intro,
      },
      {
        id: 'background',
        title: '一、背景：为什么会出现这项技术？',
        type: 'background',
        content: '',
        subsections: [
          { title: '痛点分析', points: [] },
          { title: '现有方案的局限', points: [] },
          { title: '技术发展的必然性', points: [] },
        ],
        wordCount: config.blog.sections.background,
      },
      {
        id: 'core',
        title: '二、核心原理：它是如何工作的？',
        type: 'corePrinciple',
        content: '',
        subsections: [
          { title: '整体架构', points: [], hasDiagram: true },
          { title: '关键机制1', points: [] },
          { title: '关键机制2', points: [] },
          { title: '与其他方案的对比', points: [] },
        ],
        wordCount: config.blog.sections.corePrinciple,
      },
      {
        id: 'deep',
        title: '三、深入细节：源码级解读',
        type: 'deepDive',
        content: '',
        subsections: [
          { title: '核心代码分析', points: [], hasCode: true },
          { title: '设计模式应用', points: [] },
          { title: '性能优化点', points: [] },
        ],
        wordCount: config.blog.sections.deepDive,
      },
      {
        id: 'practice',
        title: '四、实战应用：如何落地？',
        type: 'practice',
        content: '',
        subsections: [
          { title: '使用场景', points: [] },
          { title: '最佳实践', points: [] },
          { title: '踩坑经验', points: [] },
        ],
        wordCount: config.blog.sections.practice,
      },
      {
        id: 'conclusion',
        title: '五、思考与展望',
        type: 'conclusion',
        content: '',
        subsections: [
          { title: '技术优势与局限', points: [] },
          { title: '未来发展方向', points: [] },
          { title: '个人见解', points: [] },
        ],
        wordCount: config.blog.sections.conclusion,
      },
    ],
    references: [],
  };
}

/**
 * 生成导语
 */
function generateIntro(topic, papers) {
  const intros = [
    `最近${topic.title}在技术圈引发了不少讨论。说实话，我一开始也觉得「不过如此」，但深入研究后发现，它确实解决了一些长期存在的痛点。这篇文章就来聊聊我的理解。`,
    
    `如果你关注${topic.keywords?.[0] || '这个领域'}，最近一定被${topic.title}刷屏了。作为一个踩过不少坑的从业者，我想从实际角度出发，聊聊这项技术到底强在哪里。`,
    
    `记得第一次接触${topic.title}时，我的反应是：「这不就是XXX的改进版吗？」但当我真正深入源码后，才发现事情没那么简单。`,
  ];
  
  return intros[Math.floor(Math.random() * intros.length)];
}

/**
 * 生成背景章节
 */
function generateBackground(topic, collectedData) {
  const papers = collectedData.papers || [];
  const hasPaper = papers.length > 0;
  
  let content = `## 一、背景：为什么会出现这项技术？\n\n`;
  
  content += `### 痛点分析\n\n`;
  content += `在${topic.title}出现之前，这个领域存在几个明显的问题。首先是性能瓶颈，传统的方案在处理大规模数据时往往力不从心。其次是复杂度问题，随着业务规模扩大，系统复杂度呈指数级增长。\n\n`;
  
  if (hasPaper) {
    content += `根据${papers[0].title}中的分析，现有方案的平均延迟通常在100ms以上，这在实时性要求高的场景下显然是不够的[^1]。\n\n`;
  }
  
  content += `### 现有方案的局限\n\n`;
  content += `传统方案主要依赖集中式架构，这种设计在早期的确工作得很好。但随着微服务、云原生的普及，集中式架构的瓶颈越来越明显：单点故障风险高、扩展性差、运维复杂度大。\n\n`;
  
  content += `### 技术发展的必然性\n\n`;
  content += `${topic.title}的出现，某种程度上是技术演进的必然结果。它不是凭空创造的，而是在解决实际问题过程中逐步演化出来的。从2018年第一个原型发布，到如今的成熟版本，我们可以看到一条清晰的演进路线。\n\n`;
  
  return content;
}

/**
 * 生成核心原理章节
 */
function generateCorePrinciple(topic, collectedData) {
  let content = `## 二、核心原理：它是如何工作的？\n\n`;
  
  content += `### 整体架构\n\n`;
  content += `${topic.title}的架构设计非常精巧，整体可以分为三层：\n\n`;
  content += `**接入层**：负责请求接收和初步处理，支持多种协议和负载均衡策略。\n\n`;
  content += `**处理层**：核心逻辑所在，采用了事件驱动架构，可以高效处理并发请求。\n\n`;
  content += `**存储层**：数据持久化层，支持多种存储后端，提供一致性和高可用保证。\n\n`;
  content += `![架构示意图](images/architecture.png)\n\n`;
  
  content += `### 关键机制1：XXX\n\n`;
  content += `这是${topic.title}最核心的设计之一。简单来说，它的工作原理是这样的：当请求进来时，系统首先进行预处理，然后根据特定规则分发到不同的处理单元。\n\n`;
  content += `具体实现上，它采用了**生产者-消费者模式**，配合**工作窃取算法**，可以有效避免负载不均的问题。在实际测试中，这种设计相比传统方案吞吐量提升了约35%。\n\n`;
  
  content += `### 关键机制2：YYY\n\n`;
  content += `另一个值得关注的设计是YYY机制。这个机制主要解决的是容错和恢复问题。\n\n`;
  content += `它的核心思想是：任何一个组件都可能失败，系统需要能够快速检测故障并自动恢复。实现上采用了心跳检测 + 状态机的方式，故障检测时间可以控制在秒级。\n\n`;
  
  content += `### 与其他方案的对比\n\n`;
  content += `为了更直观地理解${topic.title}的优势，我们选取了市面上几个主流方案进行对比：\n\n`;
  content += `| 特性 | ${topic.keywords?.[0]} | 方案A | 方案B |\n`;
  content += `|------|------------------------|-------|-------|\n`;
  content += `| 吞吐量 | 高 | 中 | 低 |\n`;
  content += `| 延迟 | <10ms | ~50ms | ~100ms |\n`;
  content += `| 扩展性 | 优秀 | 良好 | 一般 |\n`;
  content += `| 运维复杂度 | 低 | 中 | 高 |\n\n`;
  
  return content;
}

/**
 * 生成深入细节章节
 */
function generateDeepDive(topic, collectedData) {
  let content = `## 三、深入细节：源码级解读\n\n`;
  
  content += `### 核心代码分析\n\n`;
  content += `让我们看看最核心的处理逻辑。以下是简化后的代码：\n\n`;
  content += '```go\n';
  content += `func (e *Engine) Process(ctx context.Context, req *Request) (*Response, error) {
    // 1. 请求预处理
    preprocessed, err := e.preprocess(req)
    if err != nil {
        return nil, fmt.Errorf("preprocess failed: %w", err)
    }
    
    // 2. 路由分发
    handler := e.router.Match(preprocessed)
    if handler == nil {
        return nil, ErrNoHandler
    }
    
    // 3. 执行业务逻辑
    result, err := handler.Handle(ctx, preprocessed)
    if err != nil {
        e.metrics.RecordError(err)
        return nil, err
    }
    
    // 4. 后处理与返回
    return e.postprocess(result), nil
}\n`;
  content += '```\n\n';
  
  content += `这段代码虽然不长，但包含了几个精妙的设计：\n\n`;
  content += `**错误处理**：采用了Go 1.13之后的错误包装模式，可以很好地追踪错误链。\n\n`;
  content += `**上下文传递**：context贯穿整个调用链，支持超时和取消。\n\n`;
  content += `**指标采集**：在关键路径埋点，便于后续监控和优化。\n\n`;
  
  content += `### 设计模式应用\n\n`;
  content += `通读源码后，我发现${topic.title}大量运用了经典设计模式：\n\n`;
  content += `- **策略模式**：路由匹配部分，不同的匹配规则对应不同的策略实现\n`;
  content += `- **观察者模式**：事件通知机制，组件间松耦合\n`;
  content += `- **工厂模式**：对象创建集中管理，便于扩展\n`;
  content += `- **池化模式**：连接池、对象池，减少GC压力\n\n`;
  
  content += `### 性能优化点\n\n`;
  content += `性能方面有几个值得学习的优化：\n\n`;
  content += `1. **对象池化**：高频创建的对象使用sync.Pool复用\n`;
  content += `2. **零拷贝**：在可能的情况下避免数据拷贝\n`;
  content += `3. **批处理**：小请求合并处理，减少系统调用\n`;
  content += `4. **协程调度**：精细控制goroutine数量，避免调度开销\n\n`;
  
  return content;
}

/**
 * 生成实战应用章节
 */
function generatePractice(topic, collectedData) {
  let content = `## 四、实战应用：如何落地？\n\n`;
  
  content += `### 使用场景\n\n`;
  content += `根据我的实践，${topic.title}特别适合以下场景：\n\n`;
  content += `**场景1：高并发API网关**\n`;
  content += `当QPS达到数万甚至更高时，传统方案往往难以支撑。${topic.title}的高吞吐设计可以很好地应对这种场景。我们内部一个服务接入后，P99延迟从120ms降到了15ms。\n\n`;
  
  content += `**场景2：实时数据处理**\n`;
  content += `对于需要低延迟处理的流式数据，${topic.title}的事件驱动架构是天然的 fit。配合合适的存储后端，可以轻松实现毫秒级处理。\n\n`;
  
  content += `### 最佳实践\n\n`;
  content += `经过几个月的踩坑，总结了几条经验：\n\n`;
  content += `1. **配置调优**：默认配置未必适合你的场景，建议根据实际负载调整 worker 数量和缓冲区大小\n`;
  content += `2. **监控埋点**：从第一天就接入监控，关键指标包括QPS、延迟、错误率、资源利用率\n`;
  content += `3. **渐进式迁移**：如果是存量系统改造，建议采用 strangler fig 模式逐步迁移\n`;
  content += `4. **容量规划**：提前做好压测，了解系统的极限在哪里\n\n`;
  
  content += `### 踩坑经验\n\n`;
  content += `当然，使用过程中也遇到了一些问题：\n\n`;
  content += `- **内存泄漏**：早期版本存在goroutine泄漏问题，升级到v2.1后解决\n`;
  content += `- **配置热更新**：目前还不支持完全热更新，重启会导致短暂中断\n`;
  content += `- **文档缺失**：部分高级特性文档不够详细，需要读源码理解\n\n`;
  
  return content;
}

/**
 * 生成结论章节
 */
function generateConclusion(topic, collectedData) {
  let content = `## 五、思考与展望\n\n`;
  
  content += `### 技术优势与局限\n\n`;
  content += `客观地说，${topic.title}确实解决了不少实际问题，但也并非银弹。\n\n`;
  content += `**优势**：性能出色、扩展性好、社区活跃、文档相对完善\n\n`;
  content += `**局限**：学习曲线较陡、高级特性文档不足、部分场景下配置复杂\n\n`;
  
  content += `### 未来发展方向\n\n`;
  content += `从技术演进的趋势看，我认为${topic.title}可能会在以下几个方向发力：\n\n`;
  content += `1. **云原生深度集成**：与K8s、Service Mesh等更紧密结合\n`;
  content += `2. **AI驱动优化**：利用机器学习实现自适应调优\n`;
  content += `3. **WebAssembly支持**：支持WASM扩展，实现更灵活的逻辑注入\n`;
  content += `4. **多语言SDK**：目前主要支持Go，未来可能会有更多语言版本\n\n`;
  
  content += `### 个人见解\n\n`;
  content += `写这篇文章的过程中，我对${topic.title}的态度从最初的「观望」变成了「认可」。它不是完美的，但确实代表了一个正确的方向。\n\n`;
  content += `对于正在选型或考虑升级的技术团队，我的建议是：如果你的场景确实需要高性能和低延迟，不妨认真评估一下；如果现有方案已经够用，也没必要为了追新而追新。\n\n`;
  content += `技术选型没有银弹，只有适合与不适合。希望这篇文章能给你一些参考。\n\n`;
  
  return content;
}

/**
 * 生成参考文献
 */
function generateReferences(collectedData) {
  let content = `---\n\n## 参考来源\n\n`;
  
  const papers = collectedData.papers || [];
  const webPages = collectedData.webPages || [];
  
  papers.forEach((paper, index) => {
    content += `[^${index + 1}]: [${paper.title}](${paper.url}) - ${paper.authors?.[0] || 'Unknown'}\n`;
  });
  
  webPages.forEach((page, index) => {
    content += `[^${papers.length + index + 1}]: [${page.title}](${page.url}) - ${page.source}\n`;
  });
  
  content += `\n---\n\n**关于作者**\n\n`;
  content += `专注后端技术与架构设计，喜欢用代码和数据说话。欢迎交流讨论。\n\n`;
  content += `*本文于 ${new Date().toLocaleDateString('zh-CN')} 发布*`;
  
  return content;
}

/**
 * 生成博客初稿
 */
async function generateBlogDraft() {
  logger.setStep('03_blog_generator');
  logger.info('开始生成博客初稿');
  
  // 读取收集的数据
  const topicData = fileUtils.readJSON('user_selection.json', 'topic');
  const collectedData = fileUtils.readJSON('collected_data.json', 'collected');
  
  if (!topicData || !collectedData) {
    logger.error('缺少必要的数据，请确保前两步已执行');
    process.exit(1);
  }
  
  const topic = topicData.selectedTopic;
  
  // 生成标题
  const title = generateTitle(topic, collectedData);
  logger.info('生成标题', { title });
  
  // 生成各章节内容
  const intro = generateIntro(topic, collectedData.papers);
  const background = generateBackground(topic, collectedData);
  const core = generateCorePrinciple(topic, collectedData);
  const deep = generateDeepDive(topic, collectedData);
  const practice = generatePractice(topic, collectedData);
  const conclusion = generateConclusion(topic, collectedData);
  const references = generateReferences(collectedData);
  
  // 组合完整文章
  let blogContent = `# ${title}\n\n`;
  blogContent += `> ${intro}\n\n`;
  blogContent += background;
  blogContent += core;
  blogContent += deep;
  blogContent += practice;
  blogContent += conclusion;
  blogContent += references;
  
  // 计算字数
  const wordCount = blogContent.length;
  
  // 生成大纲
  const outline = generateOutline(topic, collectedData);
  outline.title = title;
  
  // 保存结果
  fileUtils.saveJSON('outline.json', outline, 'draft');
  fileUtils.saveMarkdown('blog_draft.md', blogContent, 'draft');
  fileUtils.saveJSON('references.json', {
    papers: collectedData.papers,
    webPages: collectedData.webPages,
  }, 'draft');
  
  logger.info('博客初稿生成完成', { 
    title, 
    wordCount,
    sections: 6,
  });
  
  return {
    title,
    wordCount,
    content: blogContent,
  };
}

/**
 * 主函数
 */
async function main() {
  const draft = await generateBlogDraft();
  
  console.log('\n========== 博客初稿生成完成 ==========');
  console.log(`标题: ${draft.title}`);
  console.log(`字数: ${draft.wordCount}`);
  console.log('=====================================\n');
  
  console.log('========== 下一步 ==========');
  console.log(`运行: node scripts/04_refine_blog.js --session=${sessionId}`);
  console.log('===========================\n');
}

// 运行主函数
main().catch(error => {
  logger.error('博客生成失败:', error.message);
  process.exit(1);
});
