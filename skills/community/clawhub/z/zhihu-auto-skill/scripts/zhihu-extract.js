#!/usr/bin/env node
/**
 * zhihu-extract.js — 知乎数据提取入口
 *
 * HTTP 通道优先，Plan B 自动降级到浏览器通道。
 * CLI 模式：
 *   node scripts/zhihu-extract.js --type hot-list [--limit 20]
 *   node scripts/zhihu-extract.js --type search --query "关键词"
 *   node scripts/zhihu-extract.js --type article --id 123
 *   node scripts/zhihu-extract.js --type user --id "url_token"
 *   node scripts/zhihu-extract.js --type question --id 123
 *   node scripts/zhihu-extract.js --type answers --id 123 [--limit 10]
 *
 * 可在其他模块中导入使用：
 *   import { extract } from './zhihu-extract.js';
 */

import { extract as httpExtract } from './zhihu-http.js';

// ──────────────────────────────────────────
// 类型映射
// ──────────────────────────────────────────

const TYPE_MAP = {
  'hot-list': 'hotList',
  'hot_list': 'hotList',
  'hotList': 'hotList',
  'search': 'search',
  'article': 'article',
  'user': 'user',
  'question': 'question',
  'answers': 'answers',
  'answer': 'answers',
};

// ──────────────────────────────────────────
// 提取入口
// ──────────────────────────────────────────

/**
 * 智能数据提取
 * HTTP 通道优先，HTTP 失败时标记为需要浏览器降级
 *
 * @param {string} type - 数据类型
 * @param {object} params - 参数
 * @param {boolean} [forceBrowser=false] - 强制浏览器通道
 * @returns {Promise<{ data: any, source: string }>}
 */
async function extract(type, params = {}, forceBrowser = false) {
  const mappedType = TYPE_MAP[type] || type;

  // 尝试 HTTP 通道
  if (!forceBrowser) {
    try {
      const result = await httpExtract(mappedType, params);
      if (result.data) {
        return { data: result.data, source: 'http' };
      }
      // degraded 标记 → 回退到浏览器
      console.log(`[zhihu-extract] HTTP 通道数据不可用，降级到浏览器`);
    } catch (err) {
      console.warn(`[zhihu-extract] HTTP 通道失败:`, err.message);
      console.log(`[zhihu-extract] 降级到浏览器通道（需要启动浏览器）`);
    }
  }

  // 浏览器降级（Phase 2 实现）
  // 当前返回标记信息，等待 Phase 2 接入实际浏览器提取
  if (mappedType === 'hotList') {
    // 浏览器热榜提取（待 Phase 2 实现完整逻辑）
    return {
      data: null,
      source: 'browser_pending',
      note: '浏览器通道数据提取需等待 Phase 2 开发完成',
    };
  }
  if (mappedType === 'search') {
    return {
      data: null,
      source: 'browser_pending',
      note: '浏览器通道搜索提取需等待 Phase 2 开发完成',
    };
  }
  if (mappedType === 'article') {
    return {
      data: null,
      source: 'browser_pending',
      note: '浏览器通道文章提取需等待 Phase 2 开发完成',
    };
  }

  throw new Error(`无法提取数据: 未知类型 ${type}`);
}

// ──────────────────────────────────────────
// CLI 入口
// ──────────────────────────────────────────

function main() {
  const args = process.argv.slice(2);
  const options = {};

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--type':
        options.type = args[++i];
        break;
      case '--query':
        options.query = args[++i];
        break;
      case '--id':
        options.id = args[++i];
        break;
      case '--limit':
        options.limit = parseInt(args[++i], 10) || 20;
        break;
      case '--browser':
        options.forceBrowser = true;
        break;
      default:
        // 支持简写: node script.js hot-list
        if (!options.type) options.type = args[i];
    }
  }

  if (!options.type) {
    console.error('用法: node scripts/zhihu-extract.js --type <type> [选项]');
    console.error('类型: hot-list | search | article | user | question | answers');
    process.exit(1);
  }

  extract(options.type, options, options.forceBrowser)
    .then(result => {
      if (result.data && result.source === 'http') {
        console.log(JSON.stringify(result.data, null, 2));
      } else if (result.source === 'browser_pending') {
        console.log(`[zhihu-extract] ${result.note}`);
      }
    })
    .catch(err => {
      console.error(`[zhihu-extract] 错误:`, err.message);
      process.exit(1);
    });
}

// 直接运行时执行 main
if (process.argv[1] === import.meta.filename || process.argv[1]?.endsWith('zhihu-extract.js')) {
  main();
}

export { extract, TYPE_MAP };
