// RAG CLI 工具
// 命令行接口

import { RAGRetriever } from './retriever.js';
import { readFileSync } from 'fs';

async function cli() {
  const args = process.argv.slice(2);
  const rag = new RAGRetriever({
    dbPath: './data/lancedb',
    dimensions: 384
  });

  try {
    const command = args[0];

    switch (command) {
      case 'init':
        console.log('📂 初始化 RAG 数据库...');
        await rag.initialize(args[1] || 'documents');
        console.log('✅ 初始化完成');
        break;

      case 'add':
        if (!args[1]) {
          console.error('用法：rag add <file-path> [metadata-json]');
          process.exit(1);
        }
        console.log(`📄 添加文档：${args[1]}`);
        await rag.initialize();
        const content = readFileSync(args[1], 'utf-8');
        const metadata = args[2] ? JSON.parse(args[2]) : { source: args[1] };
        const result = await rag.addDocument(content, metadata);
        console.log(`✅ 添加成功：${result.chunks} 块`);
        break;

      case 'search':
      case 'query':
        if (!args[1]) {
          console.error('用法：rag search <query> [limit]');
          process.exit(1);
        }
        console.log(`🔍 检索：${args[1]}`);
        await rag.initialize('documents');
        const limit = parseInt(args[2]) || 5;
        const results = await rag.retrieve(args[1], { limit });
        console.log(`\n找到 ${results.length} 条结果:\n`);
        results.forEach((r, i) => {
          console.log(`[${i + 1}] 分数：${r.score.toFixed(4)}`);
          console.log(`    内容：${r.content.substring(0, 150)}...`);
          console.log(`    元数据：${JSON.stringify(r.metadata)}\n`);
        });
        break;

      case 'rag':
        if (!args[1]) {
          console.error('用法：rag rag <query> [limit]');
          process.exit(1);
        }
        console.log(`🤖 RAG 查询：${args[1]}`);
        await rag.initialize();
        const ragLimit = parseInt(args[2]) || 5;
        const ragResult = await rag.retrieveForRAG(args[1], { limit: ragLimit });
        console.log(`\n查询：${ragResult.query}`);
        console.log(`结果数：${ragResult.resultCount}`);
        console.log(`\n上下文:\n${ragResult.context}`);
        break;

      case 'stats':
        console.log('📊 统计信息...');
        await rag.initialize();
        const stats = await rag.getStats();
        console.log('统计:', JSON.stringify(stats, null, 2));
        break;

      case 'list':
        console.log('📋 集合列表...');
        await rag.initialize();
        const collections = await rag.listCollections();
        console.log('集合:', collections);
        break;

      case 'help':
      default:
        console.log(`
🦞 RAG Retriever v0.1.0

用法：
  rag init [collection]     # 初始化数据库
  rag add <file> [meta]     # 添加文档
  rag search <query> [n]    # 检索文档
  rag rag <query> [n]       # RAG 查询 (格式化上下文)
  rag stats                 # 统计信息
  rag list                  # 列出集合
  rag help                  # 显示帮助

示例：
  rag init my_docs
  rag add ./readme.json '{"source":"github"}'
  rag search "MCP protocol" 5
  rag rag "什么是 RAG" 3
  rag stats
        `);
        break;
    }
  } catch (error) {
    console.error('❌ 错误:', error.message);
    if (error.stack) {
      console.error(error.stack);
    }
    process.exit(1);
  } finally {
    await rag.close();
  }
}

// 如果直接运行，执行 CLI
if (process.argv[1]?.endsWith('rag-skill.js')) {
  cli();
}
