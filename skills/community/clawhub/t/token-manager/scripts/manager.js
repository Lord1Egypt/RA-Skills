#!/usr/bin/env node
/**
 * Token Manager - 通用 LLM Token 管家
 * 支持多模型：Kimi/Moonshot, OpenAI, Anthropic, Google, 本地模型等
 * 
 * 🔒 安全说明 / Security Notice:
 * - API Key 优先从环境变量读取（MOONSHOT_API_KEY / DEEPSEEK_API_KEY / OPENAI_API_KEY / ANTHROPIC_API_KEY / GEMINI_API_KEY）
 * - CLI --api-key / 位置参数仅供临时调试，注意 shell 历史 与进程列表可见性
 * - 所有数据存储在本地 .data/ 目录，不上传到第三方
 * - 网络请求仅访问官方 LLM API，无其他外联
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

const DATA_DIR = process.env.TOKEN_MANAGER_DATA_DIR || path.join(__dirname, '..', '.data');
const CONFIG_FILE = path.join(DATA_DIR, 'config.json');
const LOG_FILE = path.join(DATA_DIR, 'token-usage.json');

// 默认配置
const DEFAULT_CONFIG = {
  providers: {
    moonshot: {
      name: 'Kimi/Moonshot',
      baseUrl: 'api.moonshot.cn',
      protocol: 'https',
      balanceEndpoint: '/v1/users/me/balance',
      tokenEstimateEndpoint: '/v1/tokenizers/estimate-token-count',
      modelsEndpoint: '/v1/models',
      supportsBalance: true,
      supportsTokenEstimate: true,
      contextWindow: 1048576,
      defaultModel: 'kimi-k3.1-pro',
      // 价格 as-of 2026-11-09，来源 https://platform.kimi.com/docs/pricing/chat（每百万 tokens，CNY）
      pricing: {
        'kimi-k3.1-pro': { input: 13, output: 26, unit: 'CNY', per: 1000000 },
        'kimi-k3.1-pro-highspeed': { input: 26, output: 52, unit: 'CNY', per: 1000000 },
        'kimi-k3': { input: 20, output: 40, unit: 'CNY', per: 1000000 },
        'kimi-k2.7-code': { input: 6.5, output: 27, unit: 'CNY', per: 1000000 },           // K2 系 2026-12 月底下线
        'kimi-k2.7-code-highspeed': { input: 13, output: 54, unit: 'CNY', per: 1000000 },  // 同上
        'kimi-k2.6': { input: 6.5, output: 27, unit: 'CNY', per: 1000000 }                 // 同上
      }
    },
    deepseek: {
      name: 'DeepSeek',
      baseUrl: 'api.deepseek.com',
      protocol: 'https',
      balanceEndpoint: '/user/balance',
      modelsEndpoint: '/models',
      supportsBalance: true,
      supportsTokenEstimate: false,
      contextWindow: 1048576,
      defaultModel: 'deepseek-flash',
      // 价格 as-of 2026-11-09，来源 https://api-docs.deepseek.com/zh-cn/quick_start/pricing（峰值时段价，空闲时段为半价）
      pricing: {
        'deepseek-flash': { input: 2, output: 8, unit: 'CNY', per: 1000000 },
        'deepseek-v4-pro': { input: 9, output: 27, unit: 'CNY', per: 1000000 }
      }
    },
    openai: {
      name: 'OpenAI',
      baseUrl: 'api.openai.com',
      protocol: 'https',
      usageEndpoint: '/v1/usage',
      modelsEndpoint: '/v1/models',
      supportsBalance: false, // 需要登录控制台查看
      supportsTokenEstimate: false, // 本地近似估算
      defaultModel: 'gpt-6.1-terra',
      // 价格 as-of 2026-11-09，来源 openrouter.ai/openai（第一方牌价）
      pricing: {
        'gpt-6.1-terra': { input: 1, output: 5, unit: 'USD', per: 1000000 },
        'gpt-6.1-sol': { input: 2, output: 10, unit: 'USD', per: 1000000 },
        'gpt-6-luna-pro': { input: 0.1, output: 0.5, unit: 'USD', per: 1000000 }
      }
    },
    anthropic: {
      name: 'Anthropic/Claude',
      baseUrl: 'api.anthropic.com',
      protocol: 'https',
      supportsBalance: false,
      supportsTokenEstimate: false,
      defaultModel: 'claude-sonnet-5.5',
      // 价格 as-of 2026-11-09，来源 openrouter.ai/anthropic
      pricing: {
        'claude-sonnet-5.5': { input: 2, output: 10, unit: 'USD', per: 1000000 },
        'claude-haiku-5.5': { input: 0.1, output: 0.5, unit: 'USD', per: 1000000 },
        'claude-opus-5.5': { input: 4, output: 20, unit: 'USD', per: 1000000 }
      }
    },
    gemini: {
      name: 'Google/Gemini',
      baseUrl: 'generativelanguage.googleapis.com',
      protocol: 'https',
      supportsBalance: false,
      supportsTokenEstimate: false,
      defaultModel: 'gemini-4-argon',
      // 价格 as-of 2026-11-09，来源 openrouter.ai/google
      pricing: {
        'gemini-4-argon': { input: 2, output: 10, unit: 'USD', per: 1000000 },
        'gemini-3.8-flash': { input: 0.75, output: 3.75, unit: 'USD', per: 1000000 }
      }
    },
    ollama: {
      name: 'Ollama/本地模型',
      baseUrl: 'localhost:11434',
      protocol: 'http',
      supportsBalance: false, // 本地免费
      supportsTokenEstimate: false,
      pricing: { input: 0, output: 0, unit: 'FREE', per: 1 }
    }
  },
  activeProvider: 'moonshot'
};

// 初始化数据目录
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

// 加载/创建配置
function loadConfig() {
  try {
    if (fs.existsSync(CONFIG_FILE)) {
      const saved = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
      return { ...DEFAULT_CONFIG, ...saved };
    }
  } catch (e) {}
  return DEFAULT_CONFIG;
}

function saveConfig(config) {
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));
}

// 加载历史
function loadHistory() {
  try {
    if (fs.existsSync(LOG_FILE)) {
      return JSON.parse(fs.readFileSync(LOG_FILE, 'utf8'));
    }
  } catch (e) {}
  return { sessions: [], daily: {}, alerts: [] };
}

function saveHistory(data) {
  fs.writeFileSync(LOG_FILE, JSON.stringify(data, null, 2));
}

// 通用 HTTP 请求
function makeRequest(config, path, method = 'GET', postData = null, headers = {}) {
  return new Promise((resolve) => {
    const lib = config.protocol === 'https' ? https : http;
    const options = {
      hostname: config.baseUrl,
      path: path,
      method: method,
      headers: {
        'Content-Type': 'application/json',
        ...headers
      },
      timeout: 10000
    };

    const req = lib.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          resolve({ success: true, data: parsed, status: res.statusCode });
        } catch (e) {
          resolve({ success: false, error: 'Parse error', raw: data });
        }
      });
    });

    req.on('error', (e) => resolve({ success: false, error: e.message }));
    req.on('timeout', () => {
      req.destroy();
      resolve({ success: false, error: 'Timeout' });
    });

    if (postData) {
      req.write(JSON.stringify(postData));
    }
    req.end();
  });
}

// 各提供商余额响应解析（结构来自官方文档：platform.kimi.com/docs/api/balance、api-docs.deepseek.com api/get-user-balance）
const BALANCE_PARSERS = {
  moonshot: (data) => data && data.data && {
    balance: data.data.available_balance || 0,
    cash: data.data.cash_balance || 0,
    voucher: data.data.voucher_balance || 0,
    currency: 'CNY'
  },
  deepseek: (data) => data && Array.isArray(data.balance_infos) && data.balance_infos[0] && {
    balance: parseFloat(data.balance_infos[0].total_balance) || 0,
    currency: data.balance_infos[0].currency || 'CNY',
    isAvailable: data.is_available !== false
  }
};

// 查询余额（支持多提供商）
async function queryBalance(providerName, apiKey) {
  const config = loadConfig().providers[providerName];
  if (!config) return { success: false, error: 'Unknown provider' };
  
  if (!config.supportsBalance) {
    return { 
      success: false, 
      error: 'Provider does not support balance query via API',
      hint: 'Please check balance in console',
      consoleUrl: getConsoleUrl(providerName)
    };
  }

  const parse = BALANCE_PARSERS[providerName];
  if (!parse) {
    return { success: false, error: `No balance parser for provider: ${providerName}` };
  }

  try {
    const result = await makeRequest(
      config,
      config.balanceEndpoint,
      'GET',
      null,
      { 'Authorization': `Bearer ${apiKey}` }
    );
    const parsed = result.success ? parse(result.data) : null;
    if (parsed) {
      return { success: true, provider: config.name, ...parsed };
    }
    return { success: false, error: 'Invalid response', status: result.status };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// 本地近似估算：中日韩文字 ≈ 0.6 token/字（官方口径 1 token ≈ 1.5-2 汉字），拉丁文 ≈ 1 token/4 字符
function approxTokens(text) {
  const s = typeof text === 'string' ? text : JSON.stringify(text);
  const cjk = (s.match(/[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]/g) || []).length;
  return Math.ceil(cjk * 0.6 + (s.length - cjk) / 4);
}

function fallbackEstimate(config, model, text, reason) {
  return {
    success: true,
    provider: config.name,
    total_tokens: approxTokens(text),
    model: model || 'unknown',
    note: `Approximate (${reason})`,
    method: 'approximation'
  };
}

// 估算 Token（支持多提供商）
async function estimateTokens(providerName, text, model, apiKey) {
  const config = loadConfig().providers[providerName];
  if (!config) return { success: false, error: 'Unknown provider' };
  
  // 无 key 时直接本地估算（有官方 API 也调不了）
  if (!apiKey && config.supportsTokenEstimate) {
    return fallbackEstimate(config, model, text, 'no API key provided');
  }

  // 如果没有 API 支持，使用本地近似估算
  if (!config.supportsTokenEstimate) {
    return fallbackEstimate(config, model, text, 'provider does not support token counting API');
  }

  try {
    switch (providerName) {
      case 'moonshot':
        const messages = Array.isArray(text) 
          ? text 
          : [{ role: 'user', content: text }];
        
        model = model || getDefaultModel(providerName);
        const result = await makeRequest(
          config,
          config.tokenEstimateEndpoint,
          'POST',
          { model, messages },
          { 'Authorization': `Bearer ${apiKey}` }
        );

        if (result.success && result.data.data) {
          return {
            success: true,
            provider: config.name,
            total_tokens: result.data.data.total_tokens || 0,
            model,
            method: 'api'
          };
        }
        // API 不可用（无 key / 网络不通）→ 本地近似兜底
        return fallbackEstimate(config, model, text, `API unavailable: ${result.error || 'invalid response'}`);
      
      default:
        return { success: false, error: 'Not implemented' };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// 获取控制台链接
function getConsoleUrl(provider) {
  const urls = {
    moonshot: 'https://platform.kimi.com/console/account',
    deepseek: 'https://platform.deepseek.com/',
    openai: 'https://platform.openai.com/usage',
    anthropic: 'https://console.anthropic.com/',
    gemini: 'https://ai.google.dev/'
  };
  return urls[provider] || 'N/A';
}

// 各 provider 对应的 API Key 环境变量
const ENV_KEYS = {
  moonshot: 'MOONSHOT_API_KEY',
  deepseek: 'DEEPSEEK_API_KEY',
  openai: 'OPENAI_API_KEY',
  anthropic: 'ANTHROPIC_API_KEY',
  gemini: 'GEMINI_API_KEY'
};

function getEnvKey(provider) {
  const k = ENV_KEYS[provider];
  if (!k) return undefined;
  return process.env[k] || (provider === 'gemini' ? process.env.GOOGLE_API_KEY : undefined);
}

function getDefaultModel(provider) {
  const p = loadConfig().providers[provider];
  return (p && p.defaultModel) || 'unknown';
}

function formatMoney(value, currency) {
  if (currency === 'FREE') return 'FREE';
  const symbol = currency === 'CNY' ? '¥' : currency === 'USD' ? '$' : `${currency} `;
  return `${symbol}${value.toFixed(4)}`;
}

function parseFlags(args) {
  const flags = {};
  for (let i = 0; i < args.length - 1; i++) {
    if (args[i] && args[i].startsWith('--')) flags[args[i].slice(2)] = args[i + 1];
  }
  return flags;
}

// 获取模型价格
function getPricing(provider, model) {
  const config = loadConfig().providers[provider];
  if (!config) return null;
  
  const pricing = config.pricing;
  if (!pricing) return null;
  
  // 如果是统一价格（包括 FREE）
  if (pricing.unit === 'FREE' || (typeof pricing.input === 'number' && typeof pricing.output === 'number')) {
    return { ...pricing, model: 'all' };
  }
  
  // 按模型定价：只接受精确匹配，未知模型返回 null（宁可报警不可猜价）
  if (model && pricing[model]) {
    return { ...pricing[model], model };
  }
  return null;
}

// 估算费用
function estimateCost(tokensIn, tokensOut, provider, model) {
  const pricing = getPricing(provider, model);
  if (!pricing) return null;
  if (pricing.unit === 'FREE') {
    return { input: 0, output: 0, total: 0, currency: 'FREE', model: pricing.model };
  }
  
  const costIn = (tokensIn / pricing.per) * pricing.input;
  const costOut = (tokensOut / pricing.per) * pricing.output;
  return {
    input: costIn,
    output: costOut,
    total: costIn + costOut,
    currency: pricing.unit,
    model: pricing.model
  };
}

// 智能分析建议
function analyzeUsage(sessionData, provider) {
  const suggestions = [];
  const warnings = [];
  const providerConfig = loadConfig().providers[provider];
  
  // 1. 上下文检查
  const contextRatio = sessionData.contextUsed / sessionData.contextMax;
  if (contextRatio > 0.8) {
    warnings.push({
      level: 'critical',
      message: '🚨 Context 80%+ full! Must compact immediately',
      messageCn: '🚨 上下文即将满载 (80%+)，必须压缩或清理',
      action: 'compact'
    });
  } else if (contextRatio > 0.5) {
    suggestions.push({
      priority: 'medium',
      message: `📚 Context ${(contextRatio * 100).toFixed(0)}% used, consider compacting`,
      messageCn: `📚 上下文使用 ${(contextRatio * 100).toFixed(0)}%，建议适时压缩`,
      action: 'compact'
    });
  }
  
  // 2. 会话大小检查
  const totalTokens = sessionData.tokensIn + sessionData.tokensOut;
  if (totalTokens > 50000) {
    warnings.push({
      level: 'high',
      message: '⚠️ Session 50k+ tokens! Split tasks now',
      messageCn: '⚠️ 当前会话已用 50k+ tokens，建议立即压缩或拆分任务',
      action: 'spawn'
    });
  } else if (totalTokens > 20000) {
    suggestions.push({
      priority: 'high',
      message: '📊 Large session (20k+), use sub-agents',
      messageCn: '📊 会话较大 (20k+ tokens)，建议拆分复杂任务到子代理',
      action: 'spawn'
    });
  }
  
  // 3. Reasoning 检查
  if (sessionData.thinking === 'on' || sessionData.reasoning === true) {
    if (sessionData.tokensIn < 5000) {
      suggestions.push({
        priority: 'low',
        message: '💡 Simple task? Disable reasoning to save 20-30%',
        messageCn: '💡 简单任务可关闭 reasoning 节省 20-30% token',
        action: 'thinking_off'
      });
    } else {
      suggestions.push({
        priority: 'info',
        message: '✅ Reasoning enabled, good for complex tasks',
        messageCn: '✅ Reasoning 开启中，适合复杂任务',
        action: 'keep'
      });
    }
  }
  
  // 4. 余额检查
  if (sessionData.balance !== undefined && sessionData.balance < 5) {
    warnings.push({
      level: 'critical',
      message: `🚨 Low balance ¥${sessionData.balance.toFixed(2)}! Enable save mode`,
      messageCn: `🚨 余额仅剩 ¥${sessionData.balance.toFixed(2)}，建议充值或开启省钱模式`,
      action: 'save_mode'
    });
  }
  
  // 5. 提供商特定建议
  if (providerConfig && providerConfig.name === 'Ollama/本地模型') {
    suggestions.push({
      priority: 'info',
      message: '🏠 Local model - no API costs!',
      messageCn: '🏠 本地模型运行，无 API 费用！',
      action: 'none'
    });
  }
  
  return { suggestions, warnings };
}

// 生成完整报告
async function generateReport(sessionData, provider = 'moonshot', apiKey) {
  const providerConfig = loadConfig().providers[provider];
  
  // 查询余额（如果支持）
  let balanceInfo = null;
  if (apiKey) {
    balanceInfo = await queryBalance(provider, apiKey);
  }
  
  // 计算费用
  const cost = estimateCost(
    sessionData.tokensIn, 
    sessionData.tokensOut, 
    provider, 
    sessionData.model
  );
  
  const report = {
    timestamp: new Date().toISOString(),
    provider: {
      id: provider,
      name: providerConfig?.name || provider
    },
    session: {
      ...sessionData,
      cost: cost ? {
        ...cost,
        inputFormatted: formatMoney(cost.input, cost.currency),
        outputFormatted: formatMoney(cost.output, cost.currency),
        totalFormatted: formatMoney(cost.total, cost.currency)
      } : null,
      costWarning: cost ? undefined :
        `Unknown pricing for ${provider}/${sessionData.model || '(no model)'}; known models: ${Object.keys((providerConfig || {}).pricing || {}).join(', ')}`
    },
    balance: balanceInfo?.success ? {
      available: balanceInfo.balance,
      currency: balanceInfo.currency,
      consoleUrl: getConsoleUrl(provider)
    } : { 
      note: balanceInfo?.error || 'API key not provided',
      consoleUrl: getConsoleUrl(provider)
    },
    analysis: analyzeUsage(sessionData, provider),
    quickActions: generateQuickActions(sessionData, provider)
  };
  
  // 历史记录由 session-tracker.js（record 命令）负责，report 保持只读、无副作用
  return report;
}

// 生成快捷操作
function generateQuickActions(sessionData, provider) {
  const actions = [];
  const contextRatio = sessionData.contextUsed / sessionData.contextMax;
  
  if (contextRatio > 0.5) {
    actions.push({
      name: 'Compact Context',
      nameCn: '压缩上下文',
      command: '/compact',
      description: 'Reduce context size'
    });
  }
  
  if ((sessionData.tokensIn + sessionData.tokensOut) > 15000) {
    actions.push({
      name: 'Spawn Sub-agent',
      nameCn: '拆分子代理',
      command: '/spawn <task>',
      description: 'Offload to new session'
    });
  }
  
  if (sessionData.thinking === 'on') {
    actions.push({
      name: 'Disable Reasoning',
      nameCn: '关闭推理',
      command: '/thinking off',
      description: 'Save 20-30% tokens'
    });
  }
  
  return actions;
}

// CLI 模式
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  const config = loadConfig();
  
  switch (command) {
    case 'report': {
      // 命名参数: --tokens-in --tokens-out --context-used --context-max --thinking --balance --provider --model --api-key
      const flags = parseFlags(args.slice(1));
      const provider = flags.provider || config.activeProvider || 'moonshot';
      const sessionData = {
        tokensIn: parseInt(flags['tokens-in']) || 0,
        tokensOut: parseInt(flags['tokens-out']) || 0,
        contextUsed: parseInt(flags['context-used']) || 0,
        contextMax: parseInt(flags['context-max']) || (config.providers[provider] || {}).contextWindow || 200000,
        thinking: flags.thinking || 'off',
        balance: flags.balance !== undefined ? parseFloat(flags.balance) || 0 : undefined,
        model: flags.model || getDefaultModel(provider)
      };
      const report = await generateReport(sessionData, provider, flags['api-key'] || getEnvKey(provider));
      console.log(JSON.stringify(report, null, 2));
      break;
    }
    
    case 'balance': {
      const p = args[1] || config.activeProvider;
      const key = args[2] || getEnvKey(p);
      const bal = await queryBalance(p, key);
      console.log(JSON.stringify(bal, null, 2));
      break;
    }
    
    case 'tokens': {
      // tokens <provider> <text|JSON messages数组> [--model m] [--api-key k]：官方 API 优先，失败回落本地近似
      const prov = args[1] || config.activeProvider || 'moonshot';
      const text = args[2] || '';
      const flags = parseFlags(args.slice(3));
      let parsed = text;
      if (text.trim().startsWith('[')) {
        try { parsed = JSON.parse(text); } catch (e) { /* 非法 JSON 按纯文本处理 */ }
      }
      const est = await estimateTokens(prov, parsed, flags.model, flags['api-key'] || getEnvKey(prov));
      console.log(JSON.stringify(est, null, 2));
      break;
    }
    
    case 'estimate':
      // estimate <provider> <tokensIn> <tokensOut> [model]
      const prov = args[1] || 'moonshot';
      const tIn = parseInt(args[2]) || 0;
      const tOut = parseInt(args[3]) || 0;
      const mdl = args[4];
      const est = estimateCost(tIn, tOut, prov, mdl);
      console.log(JSON.stringify(est ? {
        provider: prov,
        tokens: { in: tIn, out: tOut },
        cost: est
      } : {
        provider: prov,
        error: `Unknown pricing for ${prov}/${mdl || '(default)'}`,
        knownModels: Object.keys((config.providers[prov] || {}).pricing || {})
      }, null, 2));
      break;
    
    case 'providers':
      console.log(JSON.stringify({
        providers: Object.keys(config.providers).map(k => ({
          id: k,
          name: config.providers[k].name,
          supportsBalance: config.providers[k].supportsBalance,
          supportsTokenEstimate: config.providers[k].supportsTokenEstimate,
          consoleUrl: getConsoleUrl(k)
        }))
      }, null, 2));
      break;
    
    case 'set-provider':
      config.activeProvider = args[1];
      saveConfig(config);
      console.log(JSON.stringify({ success: true, activeProvider: args[1] }));
      break;
    
    case 'history':
      const hist = loadHistory();
      console.log(JSON.stringify(hist, null, 2));
      break;
    
    default:
      console.log(JSON.stringify({
        usage: 'node manager.js <command> [args]',
        commands: {
          report: '生成完整报告 --tokens-in N --tokens-out N --context-used N --context-max N --thinking on|off [--balance N] [--provider p] [--model m] [--api-key k]',
          tokens: '估算 token 数（官方 API 优先，失败回落本地近似）: tokens <provider> <text|JSON> [--model m]',
          balance: '查询余额 (provider apiKey)',
          estimate: '估算费用 (provider tokensIn tokensOut model)',
          providers: '列出支持的提供商',
          'set-provider': '设置默认提供商 (provider)',
          history: '显示使用历史'
        }
      }, null, 2));
  }
}

module.exports = {
  generateReport,
  queryBalance,
  estimateTokens,
  estimateCost,
  analyzeUsage,
  getPricing,
  loadConfig,
  saveConfig,
  approxTokens,
  getDefaultModel,
  getEnvKey,
  BALANCE_PARSERS
};

if (require.main === module) {
  main();
}
