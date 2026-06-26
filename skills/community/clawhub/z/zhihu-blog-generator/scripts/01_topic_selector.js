/**
 * Step 1: 话题选择
 * 支持两种模式：
 * 1. 指定主题：直接使用用户提供的主题
 * 2. 热门话题：获取热门技术话题，让用户选择
 */

const path = require('path');
const { v4: uuidv4 } = require('uuid');

// 加载 lib 模块
const config = require('../lib/config');
const Logger = require('../lib/logger');
const FileUtils = require('../lib/file_utils');

// 生成会话ID
const sessionId = uuidv4().slice(0, 8);
const logger = new Logger(sessionId);
const fileUtils = new FileUtils(sessionId);

/**
 * 显示热门话题列表
 */
function displayHotTopics(topics) {
  console.log('\n========== 热门技术话题 ==========\n');
  
  topics.forEach((topic, index) => {
    console.log(`[${index + 1}] ${topic.title}`);
    console.log(`    热度: ${'🔥'.repeat(Math.ceil(topic.hot_score / 20))} (${topic.hot_score})`);
    console.log(`    来源: ${topic.source}`);
    console.log(`    简介: ${topic.brief}`);
    console.log();
  });
  
  console.log('==================================\n');
}

/**
 * 模拟获取热门话题（实际使用时替换为真实数据获取）
 */
async function fetchHotTopics() {
  // 这里应该调用搜索工具获取真实热门话题
  // 示例数据：
  return [
    {
      id: 1,
      title: 'Claude 4 发布：自主编程能力突破',
      source: 'GitHub/HackerNews',
      hot_score: 95,
      keywords: ['Claude', 'AI编程', 'Agent'],
      brief: 'Anthropic 发布 Claude 4，支持 Agent 自主编程，可独立完成项目开发'
    },
    {
      id: 2,
      title: 'Kubernetes 1.31 新特性深度解读',
      source: 'GitHub/官方文档',
      hot_score: 82,
      keywords: ['Kubernetes', 'K8s', '容器编排'],
      brief: 'K8s 1.31 带来 Sidecar 容器 GA、InPlacePodVerticalScaling 等重要更新'
    },
    {
      id: 3,
      title: 'LLM 推理优化：从 vLLM 到 SGLang',
      source: 'ArXiv/GitHub',
      hot_score: 78,
      keywords: ['LLM', '推理优化', 'vLLM'],
      brief: '大模型推理框架演进，PagedAttention 与结构化生成技术解析'
    },
    {
      id: 4,
      title: 'MCP 协议：AI 应用的新标准',
      source: 'GitHub/知乎',
      hot_score: 75,
      keywords: ['MCP', 'AI协议', 'Anthropic'],
      brief: 'Model Context Protocol 成为 AI 应用与工具交互的标准协议'
    },
    {
      id: 5,
      title: 'Rust 异步运行时：Tokio 内幕',
      source: 'GitHub/技术博客',
      hot_score: 72,
      keywords: ['Rust', 'Tokio', '异步编程'],
      brief: '深度解析 Tokio 调度器设计、任务窃取与性能优化策略'
    },
    {
      id: 6,
      title: '向量数据库选型：Milvus vs Pinecone',
      source: '知乎/GitHub',
      hot_score: 68,
      keywords: ['向量数据库', 'Milvus', 'RAG'],
      brief: '主流向量数据库对比，性能、成本、生态全方位分析'
    },
  ];
}

/**
 * 主函数
 */
async function main() {
  logger.setStep('01_topic_selector');
  
  // 创建目录
  fileUtils.createSessionDirectories();
  logger.info('会话目录创建完成', { sessionId });
  
  // 解析命令行参数
  const args = process.argv.slice(2);
  const mode = args.find(a => a.startsWith('--mode='))?.split('=')[1] || 'specific';
  const topicArg = args.find(a => a.startsWith('--topic='))?.split('=')[1];
  
  let selectedTopic = null;
  
  if (mode === 'hot') {
    // 热门话题模式
    logger.info('模式：热门话题');
    
    const hotTopics = await fetchHotTopics();
    displayHotTopics(hotTopics);
    
    // 保存热门话题列表
    fileUtils.saveJSON('topic_info.json', {
      topics: hotTopics,
      timestamp: new Date().toISOString(),
      mode: 'hot'
    }, 'topic');
    
    // 注意：在实际环境中，这里需要等待用户输入
    // 由于 Node.js 脚本独立运行，这里输出提示信息
    console.log('\n请回复你想要选择的主题编号或输入自定义主题\n');
    console.log(`会话ID: ${sessionId}`);
    console.log('继续执行下一步：node scripts/02_info_collector.js');
    
    selectedTopic = { mode: 'hot', topics: hotTopics, pending: true };
    
  } else {
    // 指定主题模式
    const topic = topicArg || 'AI技术'; // 默认主题
    logger.info('模式：指定主题', { topic });
    
    selectedTopic = {
      id: 0,
      title: topic,
      source: 'user_input',
      hot_score: 100,
      keywords: topic.split(/\s+/),
      brief: `用户指定的主题: ${topic}`
    };
    
    console.log(`\n已选择主题: ${topic}\n`);
  }
  
  // 保存选择结果
  fileUtils.saveJSON('user_selection.json', {
    sessionId,
    selectedTopic,
    timestamp: new Date().toISOString(),
    mode
  }, 'topic');
  
  logger.info('话题选择完成', { mode, topic: selectedTopic.title || selectedTopic.mode });
  
  // 输出下一步提示
  console.log('\n========== 下一步 ==========');
  console.log(`运行: node scripts/02_info_collector.js --session=${sessionId}`);
  console.log('============================\n');
}

// 运行主函数
main().catch(error => {
  logger.error('话题选择失败:', error.message);
  process.exit(1);
});
