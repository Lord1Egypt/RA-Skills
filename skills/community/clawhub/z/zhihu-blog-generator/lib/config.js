/**
 * 知乎技术博客生成器 - 配置文件
 */

const path = require('path');

const config = {
  // 输出路径
  output: {
    baseDir: 'D:\\techinsight\\reports',
    getSessionDir: (sessionId) => path.join(config.output.baseDir, `blog_${sessionId}`),
  },

  // 会话目录结构
  directories: {
    topic: '01_topic',
    collected: '02_collected',
    draft: '03_draft',
    refined: '04_refined',
    output: '05_output',
    images: '05_output/images',
  },

  // 搜索渠道配置
  search: {
    channels: [
      { name: 'arxiv', enabled: true, priority: 1, baseUrl: 'https://arxiv.org/search' },
      { name: 'github', enabled: true, priority: 2, baseUrl: 'https://github.com/search' },
      { name: 'hackernews', enabled: true, priority: 3, baseUrl: 'https://hn.algolia.com' },
      { name: 'zhihu', enabled: true, priority: 4, baseUrl: 'https://www.zhihu.com/search' },
      { name: 'stackoverflow', enabled: true, priority: 5, baseUrl: 'https://stackoverflow.com/search' },
    ],
    maxResultsPerChannel: 5,
    timeout: 30000,
  },

  // 热门话题源
  hotTopics: {
    sources: [
      { name: 'github_trending', url: 'https://github.com/trending', enabled: true },
      { name: 'hackernews', url: 'https://news.ycombinator.com', enabled: true },
      { name: 'arxiv_recent', url: 'https://arxiv.org/list/cs/recent', enabled: true },
    ],
    maxTopics: 8,
  },

  // 文章生成配置
  blog: {
    // 字数要求
    wordCount: {
      min: 1000,
      max: 5000,
      target: 3000,
    },
    
    // 章节配置
    sections: {
      intro: { minWords: 100, maxWords: 200, required: true },
      background: { minWords: 300, maxWords: 500, required: true },
      corePrinciple: { minWords: 800, maxWords: 1500, required: true },
      deepDive: { minWords: 600, maxWords: 1000, required: true },
      practice: { minWords: 400, maxWords: 800, required: true },
      conclusion: { minWords: 300, maxWords: 500, required: true },
    },

    // 标题风格
    titleStyles: [
      '{技术}深度解析：{观点}',
      '从源码看{技术}：{发现}',
      '{技术}的{N}个核心设计',
      '为什么{技术}能{效果}？',
      '{技术} vs {竞品}：深度对比',
      '实测{技术}：{结果}',
    ],
  },

  // 语言风格优化
  language: {
    // 需要去AI化的词汇
    aiWords: [
      { pattern: /值得注意的是/g, replacement: '有意思的是' },
      { pattern: /不可否认的是/g, replacement: '说实话' },
      { pattern: /总的来说/g, replacement: '总结一下' },
      { pattern: /众所周知/g, replacement: '熟悉这个领域的朋友都知道' },
      { pattern: /具有重要意义/g, replacement: '确实能解决实际问题' },
      { pattern: /极大地/g, replacement: '显著' },
      { pattern: /笔者认为/g, replacement: '我的看法是' },
      { pattern: /综上所述/g, replacement: '说了这么多' },
    ],
    
    // 增加口语化的词汇
    oralWords: ['咱们', '说实话', '坦白讲', '说白了', '你会发现', '仔细想想'],
    
    // 段落长度限制（字符数）
    paragraphMaxLength: 300,
  },

  // 质量检查规则
  quality: {
    minDataPoints: 2,        // 至少2个数据点
    minCodeSnippets: 1,      // 至少1个代码片段
    minImages: 1,            // 至少1张图
    minOpinions: 3,          // 至少3个个人观点
    maxParagraphLength: 300, // 段落最大长度
  },

  // 论文解析配置
  paper: {
    maxPapers: 3,
    extractFigures: true,
    extractTables: true,
    minRelevanceScore: 0.7,
  },

  // 日志配置
  log: {
    level: 'info', // debug, info, warn, error
    saveToFile: true,
    fileName: 'generator.log',
  },
};

module.exports = config;
