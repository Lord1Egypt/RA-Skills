#!/usr/bin/env node
/**
 * RAG 3.0 CLI 工具
 * 命令行接口
 */

import { RAGRetrieverV3 } from './core/RAGRetrieverV3.js';
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';

const CONFIG_PATH = join(process.cwd(), '.rag3-config.json');

function loadConfig() {
  if (existsSync(CONFIG_PATH)) {
    try {
      return JSON.parse(readFileSync(CONFIG_PATH, 'utf-8'));
    } catch (error) {
      console.warn('配置文件加载失败:', error.message);
    }
  }
  return {};
}

async function cli() {
  const args = process.argv.slice(2);
  const config = loadConfig();
  
  const rag = new RAGRetrieverV3({
    dbPath: config.dbPath || './data/lancedb-v3',
    embeddingProvider: config.embeddingProvider || 'auto',
    ...config
  });

  try {
    const command = args[0];

    switch (command) {
      case 'init':
        console.log('📂 初始化 RAG 3.0 数据库...');
        await rag.initialize();
        console.log('✅ 初始化完成');
        console.log(`   数据库路径: ${rag.dbPath}`);
        console.log(`   嵌入模型: ${rag.embedding?.getInfo()?.modelName || 'auto'}`);
        break;

      case 'add':
        if (!args[1]) {
          console.error('用法: rag3 add <file-path> [metadata-json]');
          process.exit(1);
        }
        if (!existsSync(args[1])) {
          console.error(`❌ 文件不存在: ${args[1]}`);
          process.exit(1);
        }
        console.log(`📄 添加文档: ${args[1]}`);
        await rag.initialize();
        const content = readFileSync(args[1], 'utf-8');
        const metadata = args[2] ? JSON.parse(args[2]) : { source: args[1] };
        const result = await rag.addDocument(content, metadata);
        console.log(`✅ 添加成功: ${result.chunks} 块`);
        console.log(`   平均块大小: ${Math.round(result.stats.avgChunkSize)} 字符`);
        break;

      case 'search':
      case 'query':
        if (!args[1]) {
          console.error('用法: rag3 search <query> [limit]');
          process.exit(1);
        }
        console.log(`🔍 检索: "${args[1]}"`);
        await rag.initialize();
        const searchLimit = parseInt(args[2]) || 5;
        const searchResults = await rag.retrieve(args[1], { 
          limit: searchLimit,
          hybrid: true,
          rerank: true
        });
        console.log(`\n找到 ${searchResults.length} 条结果:\n`);
        searchResults.forEach((r, i) => {
          const citation = r.citation;
          console.log(`${citation.mark} 分数: ${(r.finalScore || r.rerankScore || r.rrfScore || r.score).toFixed(4)}`);
          console.log(`   来源: ${citation.source.title || '未知'}`);
          console.log(`   内容: ${r.content.substring(0, 150)}...\n`);
        });
        break;

      case 'vector-search':
        if (!args[1]) {
          console.error('用法: rag3 vector-search <query> [limit]');
          process.exit(1);
        }
        console.log(`🔍 向量检索: "${args[1]}"`);
        await rag.initialize();
        const vecLimit = parseInt(args[2]) || 5;
        const vecResults = await rag.vectorSearch(args[1], { limit: vecLimit });
        console.log(`\n找到 ${vecResults.length} 条结果:\n`);
        vecResults.forEach((r, i) => {
          console.log(`[${i + 1}] 分数: ${r.score.toFixed(4)}`);
          console.log(`   内容: ${r.content.substring(0, 150)}...\n`);
        });
        break;

      case 'keyword-search':
        if (!args[1]) {
          console.error('用法: rag3 keyword-search <query> [limit]');
          process.exit(1);
        }
        console.log(`🔍 关键词检索: "${args[1]}"`);
        await rag.initialize();
        const kwLimit = parseInt(args[2]) || 5;
        const kwResults = await rag.keywordSearch(args[1], { limit: kwLimit });
        console.log(`\n找到 ${kwResults.length} 条结果:\n`);
        kwResults.forEach((r, i) => {
          console.log(`[${i + 1}] BM25: ${r.score.toFixed(4)}`);
          console.log(`   内容: ${r.content.substring(0, 150)}...\n`);
        });
        break;

      case 'hybrid':
        if (!args[1]) {
          console.error('用法: rag3 hybrid <query> [limit]');
          process.exit(1);
        }
        console.log(`🔍 混合检索: "${args[1]}"`);
        await rag.initialize();
        const hybridLimit = parseInt(args[2]) || 5;
        const hybridResults = await rag.hybridSearch(args[1], { limit: hybridLimit });
        console.log(`\n找到 ${hybridResults.length} 条结果:\n`);
        hybridResults.forEach((r, i) => {
          console.log(`[${i + 1}] RRF: ${r.rrfScore.toFixed(4)} (来源: ${r.sourceCount} 个检索器)`);
          console.log(`   内容: ${r.content.substring(0, 150)}...\n`);
        });
        break;

      case 'rag':
        if (!args[1]) {
          console.error('用法: rag3 rag <query> [limit]');
          process.exit(1);
        }
        console.log(`🤖 RAG 查询: "${args[1]}"`);
        await rag.initialize();
        const ragLimit = parseInt(args[2]) || 5;
        const ragResult = await rag.retrieveForRAG(args[1], { limit: ragLimit });
        console.log(`\n查询: ${ragResult.query}`);
        console.log(`结果数: ${ragResult.resultCount}`);
        console.log(`\n上下文:\n${ragResult.context}`);
        console.log(`\n来源引用:\n${ragResult.citationList}`);
        break;

      case 'stats':
        console.log('📊 统计信息...');
        await rag.initialize();
        const stats = await rag.getStats();
        console.log(JSON.stringify(stats, null, 2));
        break;

      case 'list':
        console.log('📋 集合列表...');
        await rag.initialize();
        const collections = await rag.listCollections();
        console.log('集合:', collections);
        break;

      case 'models':
        console.log('🤖 可用模型列表...');
        const { getAvailableProviders } = await import('./embeddings/index.js');
        const { getAvailableRerankers } = await import('./rerank/index.js');
        
        console.log('\n嵌入模型:');
        const providers = getAvailableProviders();
        Object.entries(providers).forEach(([key, provider]) => {
          console.log(`\n  ${key}: ${provider.name}`);
          console.log(`    类型: ${provider.type}`);
          console.log(`    描述: ${provider.description}`);
          console.log('    可用模型:');
          provider.models.forEach(m => {
            console.log(`      - ${m.name} (${m.dimensions}维)`);
          });
        });
        
        console.log('\n重排序模型:');
        const rerankers = getAvailableRerankers();
        Object.entries(rerankers).forEach(([key, reranker]) => {
          console.log(`\n  ${key}: ${reranker.name}`);
          console.log(`    描述: ${reranker.description}`);
          console.log('    可用模型:');
          reranker.models.forEach(m => {
            console.log(`      - ${m.name}`);
          });
        });
        break;

      case 'help':
      default:
        console.log(`
🦞 RAG Retriever V3.0.0

用法:
  rag3 init                          # 初始化数据库
  rag3 add <file> [meta]             # 添加文档
  rag3 search <query> [n]            # 检索文档 (混合搜索+重排序)
  rag3 vector-search <query> [n]     # 仅向量搜索
  rag3 keyword-search <query> [n]    # 仅关键词搜索
  rag3 hybrid <query> [n]            # 混合搜索 (RRF融合)
  rag3 rag <query> [n]               # RAG 查询 (格式化上下文)
  rag3 stats                         # 统计信息
  rag3 list                          # 列出集合
  rag3 models                        # 显示可用模型
  rag3 help                          # 显示帮助

示例:
  rag3 init
  rag3 add ./readme.json '{"source":"github"}'
  rag3 search "什么是 RAG" 5
  rag3 hybrid "人工智能应用" 10
  rag3 rag "解释混合检索" 3
  rag3 stats

环境变量:
  OPENAI_API_KEY    # OpenAI API Key (可选，用于 OpenAI 嵌入)
`);
        break;
    }
  } catch (error) {
    console.error('❌ 错误:', error.message);
    if (process.env.DEBUG) {
      console.error(error.stack);
    }
    process.exit(1);
  } finally {
    await rag.close();
  }
}

// 如果直接运行，执行 CLI
if (process.argv[1]?.endsWith('cli.js') || process.argv[1]?.includes('rag3')) {
  cli();
}
