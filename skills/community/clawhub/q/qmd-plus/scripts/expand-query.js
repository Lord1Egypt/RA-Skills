#!/usr/bin/env node

/**
 * QMD LLM Query Expansion Script
 * 
 * Generates optimized lex/vec queries using LLM for better search results.
 * Call this script, then feed the LLM response to qmd query.
 * 
 * Usage:
 *   node expand-query.js "your query" [language]
 * 
 * Example:
 *   node expand-query.js "汽车测试流程" zh
 */

const query = process.argv[2];
const language = process.argv[3] || 'auto';

if (!query) {
  console.error('Usage: node expand-query.js "your query" [language]');
  console.error('Example: node expand-query.js "汽车测试流程" zh');
  process.exit(1);
}

const languagePrompt = language === 'auto' 
  ? '检测查询语言并用相同语言生成扩展'
  : language === 'zh' || language === 'zh-cn' || language === 'chinese'
    ? '用中文生成扩展查询'
    : language === 'en' || language === 'english'
      ? 'Generate expanded queries in English'
      : 'Detect query language and use the same language for expansion';

const prompt = `你是一个专业的知识库搜索查询优化器。你的任务是将用户查询扩展为多个优化的搜索变体，用于本地 Markdown 知识库搜索。

${languagePrompt}

## 输出格式

严格输出 JSON，不要有任何其他文字：

{
  "lex": ["关键词 1", "关键词 2", "关键词 3"],
  "vec": ["自然语言问题 1", "自然语言问题 2"]
}

## 要求

**lex (关键词搜索，BM25):**
- 2-5 个术语，无填充词
- 精确术语、同义词、相关概念
- 可以包含代码标识符
- 示例：["汽车测试", "整车试验", "VTS 验证"]

**vec (语义搜索，向量):**
- 完整的自然语言问题
- 具体、包含上下文
- 2-3 个变体
- 示例：["汽车测试流程是什么样的", "整车试验包括哪些步骤"]

## 用户查询

"${query}"

现在输出 JSON：`;

console.log(prompt);
