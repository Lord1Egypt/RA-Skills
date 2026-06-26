#!/usr/bin/env node
/**
 * zai-search — CLI for Z.AI Web Search API
 * 
 * Usage: zai-search "query" [options]
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// ---- Config ----
// 加载配置文件（合并 skill 目录和用户目录的配置）
function loadConfig() {
  const config = {};

  // 1. Skill directory config (same folder as this skill)
  const skillDir = path.dirname(__dirname); // scripts/.. = skill root
  const skillConfigPath = path.join(skillDir, 'config.json');
  try {
    const skillConfig = JSON.parse(fs.readFileSync(skillConfigPath, 'utf8'));
    Object.assign(config, skillConfig);
  } catch {}

  // 2. User config (~/.config/zai-web-search/config.json) - 覆盖 skill 配置
  const userConfigPath = path.join(process.env.HOME || '/root', '.config', 'zai-web-search', 'config.json');
  try {
    const userConfig = JSON.parse(fs.readFileSync(userConfigPath, 'utf8'));
    Object.assign(config, userConfig);
  } catch {}

  // 3. Environment variable (优先级最高)
  if (process.env.ZAI_API_KEY) {
    config.apiKey = process.env.ZAI_API_KEY;
  }

  return config;
}

function getApiKey() {
  const config = loadConfig();
  return config.apiKey || null;
}

// 获取默认配置参数（可被命令行参数覆盖）
function getDefaultParams() {
  const config = loadConfig();
  return {
    engine: config.engine || 'search_std',
    intent: config.intent || false,
    count: config.count || 10,
    recency: config.recency || 'noLimit',
    content: config.content || 'medium',
    domain: config.domain || '',
  };
}

// ---- Parse Args ----
function parseArgs(argv) {
  // 从配置文件加载默认参数
  const defaults = getDefaultParams();

  const args = {
    query: '',
    engine: defaults.engine,
    intent: defaults.intent,
    count: defaults.count,
    recency: defaults.recency,
    content: defaults.content,
    domain: defaults.domain,
    json: false,
    compact: false,
  };

  const positional = [];
  let i = 2; // skip node + script
  while (i < argv.length) {
    const a = argv[i];
    if (a === '--engine' || a === '-e') {
      args.engine = argv[++i];
    } else if (a === '--intent' || a === '-i') {
      args.intent = true;
    } else if (a === '--count' || a === '-c') {
      args.count = parseInt(argv[++i], 10);
    } else if (a === '--recency' || a === '-r') {
      args.recency = argv[++i];
    } else if (a === '--content' || a === '-s') {
      args.content = argv[++i];
    } else if (a === '--domain' || a === '-d') {
      args.domain = argv[++i];
    } else if (a === '--json' || a === '-j') {
      args.json = true;
    } else if (a === '--compact' || a === '-k') {
      args.compact = true;
    } else if (a === '--help' || a === '-h') {
      printHelp();
      process.exit(0);
    } else if (a.startsWith('--')) {
      console.error(`Unknown option: ${a}`);
      process.exit(1);
    } else {
      positional.push(a);
    }
    i++;
  }

  args.query = positional.join(' ');
  return args;
}

function printHelp() {
  console.log(`
zai-search — Z.AI Web Search API CLI

Usage:
  zai-search "query" [options]

Options:
  -e, --engine ENGINE     Search engine (search_std|search_pro|search_pro_sogou|search_pro_quark)
  -i, --intent            Enable search intent recognition
  -c, --count N           Number of results (1-50)
  -r, --recency FILTER    Time filter: oneDay|oneWeek|oneMonth|oneYear|noLimit
  -s, --content SIZE      Content size: medium|high
  -d, --domain DOMAIN     Limit to specific domain(s)
  -j, --json              Output raw JSON
  -k, --compact           Compact output (title + URL only)
  -h, --help              Show this help

Engines:
  search_std          智谱基础版
  search_pro          智谱高阶版 (best)
  search_pro_sogou    搜狗搜索
  search_pro_quark    夸克搜索

Examples:
  zai-search "哈尔滨冰雪大世界 2026"
  zai-search "北京天气预报" -e search_pro -c 5
  zai-search "latest AI news" --recency oneWeek --json
  zai-search "React 19" --domain react.dev --content high

Config:
  Create config.json in the skill folder or ~/.config/zai-web-search/config.json
  to set default values:

  {
    "apiKey": "your-api-key-here",
    "engine": "search_std",
    "intent": false,
    "count": 10,
    "recency": "noLimit",
    "content": "medium",
    "domain": ""
  }

  Command-line options override config defaults.
  See config.json.example for detailed parameter descriptions.
`);
}

// ---- API Call ----
function search(query, engine, intent, count, recency, contentSize, domain) {
  return new Promise((resolve, reject) => {
    const apiKey = getApiKey();
    if (!apiKey) {
      reject(new Error('No API key found. Set ZAI_API_KEY or create ~/.config/zai-web-search/config.json'));
      return;
    }

    const body = {
      search_query: query.slice(0, 70), // max 70 chars
      search_engine: engine,
      search_intent: intent,
      count: count,
    };

    // Optional fields (only include if non-default)
    if (recency && recency !== 'noLimit') {
      body.search_recency_filter = recency;
    }
    if (contentSize && contentSize !== 'medium') {
      body.content_size = contentSize;
    }
    if (domain) {
      body.search_domain_filter = domain;
    }

    const payload = JSON.stringify(body);

    const req = https.request({
      hostname: 'open.bigmodel.cn',
      port: 443,
      path: '/api/paas/v4/web_search',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload),
      },
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          if (parsed.error) {
            reject(new Error(`API Error ${parsed.error.code}: ${parsed.error.message}`));
          } else {
            resolve(parsed);
          }
        } catch {
          reject(new Error(`Failed to parse response: ${data.slice(0, 200)}`));
        }
      });
    });

    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

// ---- Output Formatting ----
function formatMarkdown(result) {
  const lines = [];

  // Intent info
  if (result.search_intent && result.search_intent.length > 0) {
    const si = result.search_intent[0];
    if (si.intent === 'SEARCH_NONE') {
      lines.push(`> ⚠️ 搜索意图识别: 无明确搜索意图 (SEARCH_NONE)`);
      lines.push(`> 原始查询: ${si.query}`);
      lines.push('');
    } else if (si.intent === 'SEARCH_ALL' && si.keywords && si.keywords !== si.query) {
      lines.push(`🔍 搜索: **${si.query}** → 关键词: *${si.keywords}*`);
      lines.push('');
    } else {
      lines.push(`🔍 搜索: **${si.query}**`);
      lines.push('');
    }
  }

  // Results
  if (!result.search_result || result.search_result.length === 0) {
    lines.push('_无搜索结果_');
    return lines.join('\n');
  }

  result.search_result.forEach((item, idx) => {
    lines.push(`### ${idx + 1}. ${item.title}`);
    lines.push(`> ${item.link}`);
    if (item.media) lines.push(`> 来源: ${item.media}${item.publish_date ? ' · ' + item.publish_date : ''}`);
    lines.push('');
    if (item.content) lines.push(item.content);
    lines.push('');
  });

  return lines.join('\n');
}

function formatCompact(result) {
  if (!result.search_result || result.search_result.length === 0) {
    return '_无搜索结果_';
  }
  return result.search_result.map((item, idx) => {
    return `${idx + 1}. ${item.title}\n   ${item.link}`;
  }).join('\n\n');
}

// ---- Main ----
async function main() {
  const args = parseArgs(process.argv);

  if (!args.query) {
    console.error('Usage: zai-search "your search query" [options]\n');
    console.error('Run zai-search --help for more info.');
    process.exit(1);
  }

  try {
    const result = await search(
      args.query,
      args.engine,
      args.intent,
      args.count,
      args.recency,
      args.content,
      args.domain
    );

    if (args.json) {
      console.log(JSON.stringify(result, null, 2));
    } else if (args.compact) {
      console.log(formatCompact(result));
    } else {
      console.log(formatMarkdown(result));
    }
  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  }
}

main();
