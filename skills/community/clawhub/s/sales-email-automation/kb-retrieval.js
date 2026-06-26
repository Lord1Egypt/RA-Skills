#!/usr/bin/env node

/**
 * 知识库检索模块
 * 根据 intent 和关键实体检索相关知识库内容
 * 支持：LanceDB 向量搜索 + Obsidian 文档检索
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const CONFIG = {
  vectorStorePath: '/Users/wilson/.openclaw/workspace/vector_store',
  obsidianVault: '/Users/wilson/.openclaw/workspace/obsidian-vault/Farreach 知识库',
  venvPython: '/Users/wilson/.openclaw/workspace/vector_store/venv/bin/python3',
};

/**
 * 在 LanceDB 中搜索相关产品/知识
 */
async function searchVectorDB(query, limit = 3) {
  console.log(`🔍 向量数据库检索：${query}`);
  
  try {
    const searchScript = path.join(CONFIG.vectorStorePath, 'search-customers.py');
    
    // 尝试使用现有的向量搜索脚本
    const result = execSync(
      `${CONFIG.venvPython} "${searchScript}" "${query}" --limit ${limit}`,
      { encoding: 'utf8', timeout: 10000, stdio: ['pipe', 'pipe', 'ignore'] }
    );
    
    if (result && result.trim()) {
      console.log(`✅ 找到 ${limit} 条相关结果`);
      return {
        found: true,
        results: result.trim().split('\n').slice(0, limit),
        source: 'lancedb'
      };
    }
  } catch (err) {
    console.log(`⚠️  向量搜索不可用或无结果：${err.message}`);
  }
  
  return { found: false, results: [], source: 'none' };
}

/**
 * 在 Obsidian vault 中搜索相关文档
 */
function searchObsidian(keywords, limit = 3) {
  console.log(`📚 Obsidian 文档检索：${keywords.join(', ')}`);
  
  const results = [];
  
  try {
    // 递归搜索 markdown 文件
    const searchInDir = (dir, depth = 0) => {
      if (depth > 3 || results.length >= limit) return;
      
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      
      for (const entry of entries) {
        if (results.length >= limit) break;
        
        const fullPath = path.join(dir, entry.name);
        
        if (entry.isDirectory()) {
          if (!entry.name.startsWith('.')) {
            searchInDir(fullPath, depth + 1);
          }
        } else if (entry.name.endsWith('.md')) {
          try {
            const content = fs.readFileSync(fullPath, 'utf8').toLowerCase();
            
            // 检查是否包含关键词
            const matchScore = keywords.reduce((score, kw) => {
              const kwLower = kw.toLowerCase();
              if (content.includes(kwLower)) return score + 1;
              return score;
            }, 0);
            
            if (matchScore > 0) {
              // 提取相关片段
              const lines = content.split('\n');
              const relevantLines = [];
              
              for (let i = 0; i < lines.length; i++) {
                const line = lines[i].toLowerCase();
                if (keywords.some(kw => line.includes(kw.toLowerCase()))) {
                  relevantLines.push(lines[i]);
                  if (relevantLines.length >= 3) break;
                }
              }
              
              results.push({
                file: fullPath,
                score: matchScore,
                excerpt: relevantLines.join('\n').slice(0, 300)
              });
            }
          } catch (e) {
            // 忽略读取错误
          }
        }
      }
    };
    
    searchInDir(CONFIG.obsidianVault);
    
    // 按分数排序
    results.sort((a, b) => b.score - a.score);
    
    console.log(`✅ 找到 ${results.length} 篇相关文档`);
    return {
      found: results.length > 0,
      results: results.slice(0, limit),
      source: 'obsidian'
    };
  } catch (err) {
    console.log(`⚠️  Obsidian 检索失败：${err.message}`);
    return { found: false, results: [], source: 'none' };
  }
}

/**
 * 根据 intent 和实体检索知识库
 */
async function retrieveKnowledge(intent, keyEntities, language = 'en') {
  console.log(`\n📖 知识库检索启动`);
  console.log(`   Intent: ${intent}`);
  console.log(`   Entities: ${keyEntities.join(', ') || '无'}`);
  
  // 构建搜索查询
  const searchQueries = [];
  
  // 根据 intent 添加默认查询词
  const intentQueries = {
    'inquiry': ['product', 'specification', 'price', 'MOQ', 'catalog'],
    'delivery-chase': ['delivery', 'lead time', 'shipping', 'production'],
    'complaint': ['quality', 'warranty', 'return', 'replacement'],
    'technical': ['specification', 'compatibility', 'installation', 'parameter'],
    'partnership': ['distributor', 'agent', 'partnership', 'terms'],
    'spam': []
  };
  
  const baseQueries = intentQueries[intent] || [];
  searchQueries.push(...baseQueries);
  searchQueries.push(...keyEntities);
  
  // 去重
  const uniqueQueries = [...new Set(searchQueries)].slice(0, 5);
  
  if (uniqueQueries.length === 0) {
    console.log('⚠️  无搜索关键词，跳过检索');
    return { found: false, results: [] };
  }
  
  // 执行检索
  const vectorResults = await searchVectorDB(uniqueQueries.join(' '), 3);
  const obsidianResults = searchObsidian(uniqueQueries, 3);
  
  // 合并结果
  const allResults = [];
  
  if (vectorResults.found) {
    allResults.push({
      source: 'lancedb',
      content: vectorResults.results.join('\n')
    });
  }
  
  if (obsidianResults.found) {
    for (const r of obsidianResults.results) {
      allResults.push({
        source: 'obsidian',
        file: r.file,
        content: r.excerpt
      });
    }
  }
  
  console.log(`📦 检索完成，共 ${allResults.length} 条结果`);
  
  return {
    found: allResults.length > 0,
    results: allResults,
    queries: uniqueQueries
  };
}

module.exports = {
  retrieveKnowledge,
  searchVectorDB,
  searchObsidian
};
