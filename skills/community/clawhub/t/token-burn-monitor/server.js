#!/usr/bin/env node
/**
 * Token Burn Monitor v5.3
 * Modular OpenClaw Skill — Core API + Swappable Themes
 * - Auto-discovers agents from AGENTS_DIR
 * - Reads cron schedule from filesystem (no shell execution)
 * - Theme system: themes/<name>/ served as static files with CSP
 * - API-first: all data via JSON endpoints, GET-only, localhost-bound
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

const SKILL_DIR = path.dirname(require.main.filename || __filename);
const AGENTS_DIR = process.env.OPENCLAW_AGENTS_DIR || '/home/node/.openclaw/agents';
const OPENCLAW_HOME = process.env.OPENCLAW_HOME || '/home/node/.openclaw';
const CRON_JOBS_FILE = path.join(OPENCLAW_HOME, 'cron', 'jobs.json');

// Load config
function loadConfig() {
  const defaults = { port: 3847, theme: 'default', showPrompts: false, agents: {}, modelPricing: {} };
  const configPath = path.join(SKILL_DIR, 'config.json');
  try {
    if (fs.existsSync(configPath)) {
      const userConfig = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      return {
        port: userConfig.port || defaults.port,
        theme: userConfig.theme || defaults.theme,
        showPrompts: userConfig.showPrompts !== undefined ? userConfig.showPrompts : defaults.showPrompts,
        agents: { ...defaults.agents, ...userConfig.agents },
        modelPricing: { ...defaults.modelPricing, ...userConfig.modelPricing }
      };
    }
  } catch (e) { console.warn('Warning: Failed to load config.json:', e.message); }
  return defaults;
}

const CONFIG = loadConfig();
const PORT = process.env.PORT || CONFIG.port;
const THEME_DIR = path.join(SKILL_DIR, 'themes', CONFIG.theme);

// Discover agents by scanning AGENTS_DIR
function discoverAgents() {
  const agents = [];
  try {
    if (fs.existsSync(AGENTS_DIR)) {
      const entries = fs.readdirSync(AGENTS_DIR);
      for (const entry of entries) {
        const fullPath = path.join(AGENTS_DIR, entry);
        try {
          const stat = fs.statSync(fullPath);
          if (stat.isDirectory() && entry !== 'default') {
            agents.push(entry);
          }
        } catch (e) { /* skip */ }
      }
    }
  } catch (e) { /* skip */ }
  return agents;
}

// Merge discovered agents with user config
function getAgentConfig() {
  const discovered = discoverAgents();
  const result = {};
  for (const id of discovered) {
    const userCfg = CONFIG.agents[id] || {};
    result[id] = {
      name: userCfg.name || id,
      icon: userCfg.icon || null
    };
  }
  // Also include any agents in config that weren't discovered (manual entries)
  for (const [id, cfg] of Object.entries(CONFIG.agents)) {
    if (!result[id]) {
      result[id] = { name: cfg.name || id, icon: cfg.icon || null };
    }
  }
  return result;
}

const DEFAULT_MODEL_PRICING = {
  'anthropic/claude-opus-4-5': { input: 15, output: 75, cacheRead: 1.5, cacheWrite: 18.75, provider: 'Anthropic' },
  'anthropic/claude-opus-4-6': { input: 15, output: 75, cacheRead: 1.5, cacheWrite: 18.75, provider: 'Anthropic' },
  'anthropic/claude-sonnet-4-5': { input: 3, output: 15, cacheRead: 0.3, cacheWrite: 3.75, provider: 'Anthropic' },
  'claude-opus-4-5': { input: 15, output: 75, cacheRead: 1.5, cacheWrite: 18.75, provider: 'Anthropic' },
  'claude-opus-4-6': { input: 15, output: 75, cacheRead: 1.5, cacheWrite: 18.75, provider: 'Anthropic' },
  'gpt-4o': { input: 2.5, output: 10, cacheRead: 1.25, cacheWrite: 2.5, provider: 'OpenAI' },
  'minimax-m2.5': { input: 0.5, output: 1.5, cacheRead: 0.25, cacheWrite: 0.5, provider: 'MiniMax' },
  'minimax/minimax-m2.5': { input: 0.5, output: 1.5, cacheRead: 0.25, cacheWrite: 0.5, provider: 'MiniMax' },
  'gemini-3.1-pro-preview': { input: 1.25, output: 5, cacheRead: 0.3, cacheWrite: 1.25, provider: 'Google' },
  'google/gemini-3.1-pro-preview': { input: 1.25, output: 5, cacheRead: 0.3, cacheWrite: 1.25, provider: 'Google' },
  'openrouter/google/gemini-3.1-pro-preview': { input: 1.25, output: 5, cacheRead: 0.3, cacheWrite: 1.25, provider: 'Google' },
  'default': { input: 5, output: 15, cacheRead: 0.5, cacheWrite: 5, provider: 'Unknown' }
};

const MODEL_PRICING = { ...DEFAULT_MODEL_PRICING, ...CONFIG.modelPricing };

// Convert cron expression to human-readable
function cronToHuman(expr) {
  if (!expr) return 'Unknown';
  const parts = expr.split(' ');
  if (parts.length !== 5) return expr;
  
  const [min, hour, dom, mon, dow] = parts;
  
  const dowMap = { '0': 'Sun', '1': 'Mon', '2': 'Tue', '3': 'Wed', '4': 'Thu', '5': 'Fri', '6': 'Sat', '7': 'Sun' };
  
  const hourDesc = (h) => {
    if (h === '*') return '';
    if (h.includes('-')) {
      const [start, end] = h.split('-').map(Number);
      const bjStart = (start + 8) % 24;
      const bjEnd = (end + 8) % 24;
      return `${bjStart}:00-${bjEnd}:00 Beijing`;
    }
    return '';
  };
  
  if (min === '*' && hour === '*') return 'Every minute';
  if (min === '0' && hour === '*') return 'Every hour';
  if (min === '30' && hour === '*') return 'Every hour at :30';
  if (min === '*/30' && hour === '*') return 'Every 30 min';
  if (min === '*/15' && hour === '*') return 'Every 15 min';
  
  if (hour.includes('-') && dow === '1-5') {
    const m = parseInt(min) || 0;
    const hRange = hourDesc(hour);
    return `Hourly${m > 0 ? ` at :${m.toString().padStart(2,'0')}` : ''}, ${hRange}, Weekdays`;
  }
  
  if (hour !== '*' && !hour.includes('-') && dom === '*' && mon === '*' && dow === '*') {
    const h = parseInt(hour);
    const m = parseInt(min) || 0;
    const time = `${h.toString().padStart(2,'0')}:${m.toString().padStart(2,'0')}`;
    return `Daily at ${time} UTC`;
  }
  
  if (hour !== '*' && !hour.includes('-') && dom === '*' && mon === '*' && dow === '1-5') {
    const h = parseInt(hour);
    const m = parseInt(min) || 0;
    const bjH = (h + 8) % 24;
    const time = `${bjH.toString().padStart(2,'0')}:${m.toString().padStart(2,'0')}`;
    return `Weekdays at ${time} Beijing`;
  }
  
  return expr;
}

function redactPrompt(text) {
  if (!text) return null;
  const showPrompts = process.env.SHOW_PROMPTS === '1' || CONFIG.showPrompts === true;
  if (!showPrompts) return '[redacted]';
  return text.slice(0, 300) + (text.length > 300 ? '...' : '');
}

function getProvider(model) {
  if (!model) return 'Unknown';
  if (model.includes('anthropic') || model.includes('claude')) return 'Anthropic';
  if (model.includes('openai') || model.includes('gpt') || model.includes('o1')) return 'OpenAI';
  if (model.includes('google') || model.includes('gemini')) return 'Google';
  if (model.includes('minimax')) return 'MiniMax';
  return 'Unknown';
}

function getTodayStr() {
  return new Date().toISOString().split('T')[0];
}

function parseSessionFileSync(filePath, targetDate) {
  const stats = {
    totalTokens: 0, inputTokens: 0, outputTokens: 0,
    cacheReadTokens: 0, cacheWriteTokens: 0, reasoningTokens: 0,
    totalCost: 0, inputCost: 0, outputCost: 0, cacheReadCost: 0, cacheWriteCost: 0,
    messageCount: 0, queryCount: 0, models: {},
    messages: [],
    latestStatus: null
  };

  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n');
    
    let lastUserPrompt = null;
    
    for (const line of lines) {
      if (!line.trim()) continue;
      
      try {
        const entry = JSON.parse(line);
        const timestamp = entry.timestamp;
        
        if (entry.type === 'message' && entry.message?.role === 'user') {
          const msgContent = entry.message.content;
          let promptText = '';
          if (Array.isArray(msgContent)) {
            for (const c of msgContent) {
              if (c && c.type === 'text' && c.text) {
                promptText = c.text;
                break;
              }
            }
          } else if (typeof msgContent === 'string') {
            promptText = msgContent;
          }
          
          if (promptText) {
            const codeBlockEnd = promptText.lastIndexOf('```');
            if (codeBlockEnd !== -1) {
              const afterBlocks = promptText.slice(codeBlockEnd + 3).trim();
              if (afterBlocks) {
                promptText = afterBlocks;
              }
            } else if (promptText.startsWith('System:')) {
              const forwardMatch = promptText.match(/\[FORWARD_TO_(\w+)\]/);
              const taskMatch = promptText.match(/task:\s*(.+)/);
              if (forwardMatch) {
                const target = forwardMatch[1];
                const task = taskMatch ? taskMatch[1].trim() : '';
                promptText = `[Cron → ${target}]${task ? ' ' + task : ''}`;
              } else {
                const firstLine = promptText.match(/^System:\s*\[.*?\]\s*(.*)/);
                if (firstLine && firstLine[1]) {
                  promptText = firstLine[1].trim();
                }
              }
            }
            
            if (promptText.startsWith('Read HEARTBEAT.md')) {
              promptText = '[Heartbeat]';
            }
            
            if (promptText.length > 300) {
              promptText = promptText.slice(0, 300) + '…';
            }
            lastUserPrompt = { text: promptText, timestamp: entry.timestamp };
          }
        }
        
        if (!timestamp?.startsWith(targetDate)) continue;
        
        if (entry.type === 'message' && entry.message?.role === 'user') {
          stats.queryCount++;
        }
        
        if (entry.type === 'message' && entry.message?.role === 'assistant' && entry.message?.usage) {
          const usage = entry.message.usage;
          const model = entry.message.model || 'unknown';
          const content = entry.message.content || [];
          
          const toolCalls = content.filter(c => c.type === 'toolCall');
          const toolCallCount = toolCalls.length;
          const toolNames = toolCalls.map(tc => tc.name || 'unknown');
          
          const input = usage.input || 0;
          const output = usage.output || 0;
          const cacheRead = usage.cacheRead || 0;
          const cacheWrite = usage.cacheWrite || 0;
          const reasoning = usage.reasoning || 0;
          const total = usage.totalTokens || (input + output + cacheRead + cacheWrite + reasoning);
          
          const cost = usage.cost || {};
          const inputCost = cost.input || 0;
          const outputCost = cost.output || 0;
          const cacheReadCost = cost.cacheRead || 0;
          const cacheWriteCost = cost.cacheWrite || 0;
          const totalCost = cost.total || 0;
          
          stats.totalTokens += total;
          stats.inputTokens += input;
          stats.outputTokens += output;
          stats.cacheReadTokens += cacheRead;
          stats.cacheWriteTokens += cacheWrite;
          stats.reasoningTokens += reasoning;
          
          stats.totalCost += totalCost;
          stats.inputCost += inputCost;
          stats.outputCost += outputCost;
          stats.cacheReadCost += cacheReadCost;
          stats.cacheWriteCost += cacheWriteCost;
          
          stats.messageCount++;
          
          if (!stats.models[model]) {
            stats.models[model] = { tokens: 0, cost: 0, messages: 0, provider: getProvider(model) };
          }
          stats.models[model].tokens += total;
          stats.models[model].cost += totalCost;
          stats.models[model].messages++;
          
          stats.messages.push({
            timestamp,
            model,
            provider: getProvider(model),
            input, output, cacheRead, cacheWrite, reasoning,
            totalTokens: total,
            cost: totalCost,
            inputCost, outputCost, cacheReadCost, cacheWriteCost,
            toolCallCount,
            toolNames,
            userPrompt: lastUserPrompt ? redactPrompt(lastUserPrompt.text) : null
          });
          
          stats.latestStatus = {
            contextLength: input + cacheRead + cacheWrite,
            cacheHitRate: (input + cacheRead + cacheWrite) > 0 
              ? (cacheRead / (input + cacheRead + cacheWrite) * 100).toFixed(1) 
              : 0,
            lastModel: model,
            lastTimestamp: timestamp
          };
        }
      } catch (e) { /* skip */ }
    }
  } catch (e) { /* file error */ }
  
  stats.messages.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  return stats;
}

function getAgentStats(agentId, targetDate) {
  const agentDir = path.join(AGENTS_DIR, agentId, 'sessions');
  
  const createEmpty = () => ({
    agentId,
    totalTokens: 0, inputTokens: 0, outputTokens: 0,
    cacheReadTokens: 0, cacheWriteTokens: 0, reasoningTokens: 0,
    totalCost: 0, inputCost: 0, outputCost: 0, cacheReadCost: 0, cacheWriteCost: 0,
    messageCount: 0, queryCount: 0, models: {},
    messages: [], latestStatus: null
  });
  
  if (!fs.existsSync(agentDir)) return createEmpty();

  const files = fs.readdirSync(agentDir).filter(f => f.endsWith('.jsonl'));
  const aggregated = createEmpty();

  for (const file of files) {
    const filePath = path.join(agentDir, file);
    const stats = parseSessionFileSync(filePath, targetDate);
    
    aggregated.totalTokens += stats.totalTokens;
    aggregated.inputTokens += stats.inputTokens;
    aggregated.outputTokens += stats.outputTokens;
    aggregated.cacheReadTokens += stats.cacheReadTokens;
    aggregated.cacheWriteTokens += stats.cacheWriteTokens;
    aggregated.reasoningTokens += stats.reasoningTokens;
    
    aggregated.totalCost += stats.totalCost;
    aggregated.inputCost += stats.inputCost;
    aggregated.outputCost += stats.outputCost;
    aggregated.cacheReadCost += stats.cacheReadCost;
    aggregated.cacheWriteCost += stats.cacheWriteCost;
    
    aggregated.messageCount += stats.messageCount;
    aggregated.queryCount += stats.queryCount;
    aggregated.messages.push(...stats.messages);
    
    if (stats.latestStatus) {
      if (!aggregated.latestStatus || 
          new Date(stats.latestStatus.lastTimestamp) > new Date(aggregated.latestStatus.lastTimestamp)) {
        aggregated.latestStatus = stats.latestStatus;
      }
    }
    
    for (const [model, data] of Object.entries(stats.models)) {
      if (!aggregated.models[model]) {
        aggregated.models[model] = { tokens: 0, cost: 0, messages: 0, provider: data.provider };
      }
      aggregated.models[model].tokens += data.tokens;
      aggregated.models[model].cost += data.cost;
      aggregated.models[model].messages += data.messages;
    }
  }
  
  aggregated.messages.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  return aggregated;
}

function getAllStats(targetDate) {
  const agentConfig = getAgentConfig();
  const allAgents = Object.keys(agentConfig);

  const results = {
    date: targetDate,
    timestamp: new Date().toISOString(),
    agents: {},
    totals: {
      totalTokens: 0, inputTokens: 0, outputTokens: 0,
      cacheReadTokens: 0, cacheWriteTokens: 0, reasoningTokens: 0,
      totalCost: 0, inputCost: 0, outputCost: 0, cacheReadCost: 0, cacheWriteCost: 0,
      messageCount: 0, queryCount: 0
    }
  };

  for (const agentId of allAgents) {
    const stats = getAgentStats(agentId, targetDate);
    const { messages, ...summary } = stats;
    results.agents[agentId] = summary;
    
    results.totals.totalTokens += stats.totalTokens;
    results.totals.inputTokens += stats.inputTokens;
    results.totals.outputTokens += stats.outputTokens;
    results.totals.cacheReadTokens += stats.cacheReadTokens;
    results.totals.cacheWriteTokens += stats.cacheWriteTokens;
    results.totals.reasoningTokens += stats.reasoningTokens;
    results.totals.totalCost += stats.totalCost;
    results.totals.inputCost += stats.inputCost;
    results.totals.outputCost += stats.outputCost;
    results.totals.cacheReadCost += stats.cacheReadCost;
    results.totals.cacheWriteCost += stats.cacheWriteCost;
    results.totals.messageCount += stats.messageCount;
    results.totals.queryCount += stats.queryCount;
  }

  return results;
}

function getHistory(days = 30) {
  const history = [];
  const today = new Date();
  
  for (let i = 0; i < days; i++) {
    const date = new Date(today);
    date.setDate(date.getDate() - i);
    const dateStr = date.toISOString().split('T')[0];
    
    const stats = getAllStats(dateStr);
    history.push({
      date: dateStr,
      totalCost: stats.totals.totalCost,
      totalTokens: stats.totals.totalTokens,
      messageCount: stats.totals.messageCount,
      queryCount: stats.totals.queryCount,
      agents: Object.fromEntries(
        Object.entries(stats.agents).map(([id, a]) => [id, {
          totalCost: a.totalCost,
          totalTokens: a.totalTokens,
          messageCount: a.messageCount
        }])
      )
    });
  }
  
  return history.filter(d => d.totalCost > 0 || d.messageCount > 0);
}

function getCronJobs() {
  try {
    if (!fs.existsSync(CRON_JOBS_FILE)) return [];
    const data = JSON.parse(fs.readFileSync(CRON_JOBS_FILE, 'utf8'));
    return data.jobs || [];
  } catch (e) {
    return [];
  }
}

function getCronRuns(jobId) {
  if (!/^[\w\-]+$/.test(jobId)) {
    return { runs: [], error: 'Invalid job ID' };
  }
  try {
    const jobs = getCronJobs();
    const job = jobs.find(j => j.id === jobId);
    if (!job) return { runs: [], error: 'Job not found' };
    const state = job.state || {};
    const runs = [];
    if (state.lastRunAtMs) {
      runs.push({
        runAtMs: state.lastRunAtMs,
        status: state.lastRunStatus || 'unknown',
        durationMs: state.lastDurationMs || 0,
        nextRunAtMs: state.nextRunAtMs || null
      });
    }
    return { runs, total: runs.length };
  } catch (e) {
    return { runs: [], error: e.message };
  }
}

function serveStatic(res, filePath, contentType) {
  const resolved = path.resolve(filePath);
  if (!resolved.startsWith(path.resolve(THEME_DIR))) {
    res.writeHead(403); res.end('Forbidden'); return;
  }
  fs.readFile(resolved, (err, data) => {
    if (err) { res.writeHead(404); res.end('Not found'); return; }
    const headers = { 'Content-Type': contentType };
    if (contentType === 'text/html') {
      headers['Content-Security-Policy'] = `default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; font-src 'self'`;
    }
    res.writeHead(200, headers);
    res.end(data);
  });
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  
  if (req.method !== 'GET') { res.writeHead(405); res.end('Method not allowed'); return; }

  if (url.pathname === '/api/config') {
    const agentConfig = getAgentConfig();
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ agents: agentConfig }, null, 2));
    return;
  }

  if (url.pathname === '/api/pricing') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(MODEL_PRICING, null, 2));
    return;
  }

  if (url.pathname === '/api/history') {
    const days = parseInt(url.searchParams.get('days')) || 30;
    try {
      const history = getHistory(days);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ history }, null, 2));
    } catch (e) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: e.message }));
    }
    return;
  }

  if (url.pathname === '/api/crons') {
    try {
      const jobs = getCronJobs();
      const agentConfig = getAgentConfig();
      const byAgent = {};
      
      for (const job of jobs) {
        let executingAgent = job.agentId || 'main';
        let brief = job.name || 'Unnamed';
        
        if (job.payload?.text) {
          const text = job.payload.text;
          const forwardMatch = text.match(/sessionKey:\s*agent:(\w+):main/i) || 
                              text.match(/FORWARD_TO_(\w+)/i) ||
                              text.match(/TRIGGER_(\w+)/i);
          if (forwardMatch) {
            executingAgent = forwardMatch[1].toLowerCase();
          }
          
          const taskLine = text.split('\n').find(l => l.includes('task:'));
          if (taskLine) {
            brief = taskLine.replace(/task:/i, '').trim();
          }
        }
        
        if (!byAgent[executingAgent]) byAgent[executingAgent] = [];
        
        let scheduleHuman = '';
        let scheduleRaw = '';
        if (job.schedule?.kind === 'cron') {
          scheduleRaw = job.schedule.expr;
          scheduleHuman = cronToHuman(job.schedule.expr);
        } else if (job.schedule?.kind === 'every') {
          const mins = Math.round(job.schedule.everyMs / 60000);
          scheduleHuman = `Every ${mins}m`;
          scheduleRaw = `every ${mins}m`;
        } else if (job.schedule?.kind === 'at') {
          scheduleHuman = `At ${job.schedule.at}`;
          scheduleRaw = job.schedule.at;
        }
        
        byAgent[executingAgent].push({
          id: job.id,
          name: job.name,
          brief,
          scheduleHuman,
          scheduleRaw,
          scheduleKind: job.schedule?.kind,
          triggerAgent: job.agentId,
          executingAgent,
          sessionTarget: job.sessionTarget,
          enabled: job.enabled,
          lastRunAt: job.state?.lastRunAtMs ? new Date(job.state.lastRunAtMs).toISOString() : null,
          lastStatus: job.state?.lastRunStatus,
          lastDurationMs: job.state?.lastDurationMs,
          nextRunAt: job.state?.nextRunAtMs ? new Date(job.state.nextRunAtMs).toISOString() : null,
          consecutiveErrors: job.state?.consecutiveErrors || 0
        });
      }
      
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ byAgent, total: jobs.length }, null, 2));
    } catch (e) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: e.message }));
    }
    return;
  }

  if (url.pathname.startsWith('/api/cron/') && url.pathname.includes('/runs')) {
    const parts = url.pathname.split('/');
    const jobId = parts[3];
    try {
      const result = getCronRuns(jobId);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(result, null, 2));
    } catch (e) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: e.message }));
    }
    return;
  }

  if (url.pathname === '/api/stats') {
    const date = url.searchParams.get('date') || getTodayStr();
    try {
      const stats = getAllStats(date);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(stats, null, 2));
    } catch (e) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: e.message }));
    }
    return;
  }

  if (url.pathname.startsWith('/api/agent/')) {
    const agentId = url.pathname.split('/')[3];
    const date = url.searchParams.get('date') || getTodayStr();
    try {
      const stats = getAgentStats(agentId, date);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(stats, null, 2));
    } catch (e) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: e.message }));
    }
    return;
  }

  if (url.pathname === '/' || url.pathname === '/index.html') {
    serveStatic(res, path.join(THEME_DIR, 'index.html'), 'text/html');
    return;
  }
  
  if (url.pathname.startsWith('/assets/')) {
    const filePath = path.join(THEME_DIR, url.pathname);
    const ext = path.extname(filePath);
    const contentTypes = {
      '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
      '.gif': 'image/gif', '.svg': 'image/svg+xml', '.webp': 'image/webp'
    };
    serveStatic(res, filePath, contentTypes[ext] || 'application/octet-stream');
    return;
  }

  res.writeHead(404);
  res.end('Not found');
});

const BIND_HOST = process.env.BIND_HOST || '127.0.0.1';
server.listen(PORT, BIND_HOST, () => {
  const agentCount = Object.keys(getAgentConfig()).length;
  console.log(`🔥 Token Burn Monitor v5.3 running at http://${BIND_HOST}:${PORT}`);
  console.log(`   Theme: ${CONFIG.theme} (${THEME_DIR})`);
  console.log(`   Discovered ${agentCount} agents from ${AGENTS_DIR}`);
});
