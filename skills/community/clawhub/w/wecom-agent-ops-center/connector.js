/**
 * 企微 Agent Ops Center — 主入口 v2.4（Node.js）
 *
 * 一键启动：node connector.js
 * 配对码命令：node connector.js pair        # 生成配对码
 *            node connector.js join <CODE>  # 加入配对
 *            node connector.js status        # 查看 P2P 状态
 *
 * 架构（v2.4 — 进程守护 + Secrets 防护 + 域名白名单）：
 *   ┌─ L0 适配层 ──────────────────────────────┐
 *   │  WorkBuddy / OpenClaw / Generic / ...    │
 *   └──────────────┬───────────────────────────┘
 *                  │ EventEmitter
 *   ┌─ L2 核心引擎 ───────────────────────────┐
 *   │  AgentMonitor + TaskTracker +           │
 *   │  ResourceCollector + AuditLogger +      │
 *   │  LifecycleManager + SecretsScanner +    │
 *   │  NetworkGuard + StateStore              │
 *   └──────────────┬───────────────────────────┘
 *                  │
 *   ┌─ L1/L3 企微层 ──────────────────────────┐
 *   │  ws-client + notify-engine + dashboard   │
 *   └──────────────────────────────────────────┘
 */

const http = require('http');
const { loadConfig, validateConfig } = require('./config');
const { WeComWSClient } = require('./ws-client');
const { AgentBridge } = require('./agent-bridge');
const { AgentMonitor, EVENTS } = require('./agent-monitor');
const { NotifyEngine } = require('./notify-engine');
const { StateStore } = require('./state-store');
const { TaskTracker } = require('./core/task-tracker');
const { ResourceCollector } = require('./core/resource-collector');
const { AuditLogger } = require('./core/audit-logger');
const { LifecycleManager } = require('./core/lifecycle-manager');
const { SecretsScanner } = require('./core/secrets-scanner');
const { NetworkGuard } = require('./core/network-guard');
const { GenericAdapter } = require('./adapters/generic-adapter');
const { WorkBuddyAdapter } = require('./adapters/workbuddy-adapter');
const { OpenClawAdapter } = require('./adapters/openclaw-adapter');
const { standardToWecomReply, standardToWecomCard } = require('./msg-converter');
const { P2PRouter, startP2PInboundServer } = require('./p2p-router');
const { DashboardAPI } = require('./dashboard-api');
const fs = require('fs');
const path = require('path');

// ============================================================
// 初始化
// ============================================================
const config = loadConfig();

// 把 converter 配置注入环境变量（供 msg-converter.js 使用）
if (config.converter && config.converter.api_base) {
  process.env.CONVERTER_API_BASE = config.converter.api_base;
}
if (config.converter && config.converter.api_key) {
  process.env.CONVERTER_API_KEY = config.converter.api_key;
}

// 日志
const LOG_LEVELS = { DEBUG: 0, INFO: 1, WARN: 2, ERROR: 3 };
const LOG_LEVEL = LOG_LEVELS[config.connector.log_level.toUpperCase()] || 1;

function log(level, ...args) {
  if (LOG_LEVELS[level] >= LOG_LEVEL) {
    const ts = new Date().toLocaleTimeString('zh-CN', { hour12: false });
    console.log(`[${ts}] [${level}]`, ...args);
  }
}

// 组件
const wsClient = new WeComWSClient({
  botId: config.wecom.bot_id,
  botSecret: config.wecom.bot_secret,
  wsUrl: config.wecom.ws_url,
});

const agentBridge = new AgentBridge({
  endpoint: config.agent.endpoint,
  timeout: config.agent.timeout,
  retry: config.agent.retry,
});

// ─── 监控层（L2 企微 Agent Ops Center） ───
const stateStore = new StateStore({
  persistPath: config.monitor ? config.monitor.state_file : null,
});

const monitor = new AgentMonitor(stateStore, {
  heartbeatInterval: (config.monitor && config.monitor.heartbeat_interval) ? config.monitor.heartbeat_interval * 1000 : 30_000,
  healthTimeout: (config.monitor && config.monitor.health_timeout) ? config.monitor.health_timeout * 1000 : 5_000,
  offlineThreshold: (config.monitor && config.monitor.offline_threshold) || 3,
});

const notifyEngine = new NotifyEngine({
  alertCooldown: (config.monitor && config.monitor.alert_cooldown) ? config.monitor.alert_cooldown * 1000 : 300_000,
  chatId: (config.monitor && config.monitor.notify_chatid) || null,
});

// ─── 任务追踪器（v2.1） ───
const taskTracker = new TaskTracker({
  stateStore,
  notifyEngine,
});

// ─── 资源采集器（v2.2） ───
const resourceCollector = new ResourceCollector({
  stateStore,
  notifyEngine,
});

// ─── 审计日志（v2.3） ───
const auditLogger = new AuditLogger({
  stateStore,
  notifyEngine,
});

// ─── 进程生命周期管理（v2.4，仅当 enabled=true 时创建）──
const lifecycleMgr = config.lifecycle?.enabled
  ? new LifecycleManager({
      stateStore,
      notifyEngine,
      ensureInterval: (config.lifecycle?.check_interval || 600) * 1000,
      maxRestarts: config.lifecycle?.max_restarts || 5,
      restartWindow: (config.lifecycle?.restart_window || 300) * 1000,
      restartBackoffMin: (config.lifecycle?.restart_backoff_min || 2) * 1000,
      restartBackoffMax: (config.lifecycle?.restart_backoff_max || 120) * 1000,
    })
  : null;

// Lifecycle 事件 → 企微通知（仅当实例存在时注册）
if (lifecycleMgr) {
  lifecycleMgr.on('process:crashed', (data) => {
    log('WARN', `进程崩溃: ${data.name}(${data.id}), exit=${data.code}`);
  });
  lifecycleMgr.on('process:restarted', (data) => {
    log('INFO', `进程自动恢复: ${data.name}(${data.id}), 第${data.restartCount}次`);
  });
  lifecycleMgr.on('process:gaveup', (data) => {
    log('ERROR', `进程放弃重启: ${data.name}(${data.id}), 共${data.restartCount}次`);
  });
  lifecycleMgr.on('lifecycle:card', (card) => {
    _pushToWecom(card);
  });
}

// ─── 敏感信息扫描（v2.4，仅当 enabled=true 时创建）──
const secretsScanner = config.secrets?.enabled
  ? new SecretsScanner({
      mode: config.secrets?.mode || 'block',
      enabledCategories: config.secrets?.enabledCategories?.length > 0 ? config.secrets.enabledCategories : null,
      ignorePatterns: config.secrets?.ignorePatterns || [],
    })
  : null;

// Secrets 事件 → 企微告警（仅当实例存在时注册）
if (secretsScanner) {
  secretsScanner.on('secrets:detected', (data) => {
    log('WARN', `检测到 ${data.count} 处敏感信息泄露（来源: ${data.source}）`);
  });
  secretsScanner.on('secrets:blocked', (data) => {
    log('ERROR', `消息被阻断: 含 ${data.findings.length} 处敏感信息`);
    data.findings.forEach(f => {
      log('ERROR', `  - ${f.rule} (${f.severity}): ${f.context}`);
    });
  });
}

// ─── 网络请求守卫（v2.4，仅当 enabled=true 时创建）──
const networkGuard = config.network?.enabled
  ? new NetworkGuard({
      mode: config.network?.mode || 'block',
      domains: config.network?.domains || [],
      ips: config.network?.ips || [],
      cidrs: config.network?.cidrs || [],
      autoAllowInternal: config.network?.autoAllowInternal !== false,
    })
  : null;

// Network Guard 事件 → 企微告警（仅当实例存在时注册）
if (networkGuard) {
  networkGuard.on('request:blocked', (entry) => {
    log('WARN', `网络阻断: ${entry.host} — ${entry.reason}`);
  });
}

// ─── 适配器管理（v2.1） ───
const adapters = [];  // 所有激活的适配器实例

function loadAdapters() {
  // 兼容模式：旧 monitor.agents 配置 → 自动转为 generic 适配器
  if (config.monitor && config.monitor.agents && !config.adapters) {
    log('INFO', '检测到旧版 monitor.agents 配置，自动映射为 generic 适配器');
    for (const a of config.monitor.agents) {
      const adapter = new GenericAdapter({
        id: a.id || `agent_${Math.random().toString(36).slice(2, 8)}`,
        type: 'generic',
        agent: {
          id: a.id,
          name: a.name || a.id,
          endpoint: a.host && a.port ? `http://${a.host}:${a.port}` : (a.endpoint || ''),
        },
        options: {
          healthPath: a.health_path || '/health',
          healthInterval: (a.heartbeat_interval || 30) * 1000,
        },
      });
      adapters.push(adapter);
      monitor.registerAgent(adapter.agentId, {
        id: adapter.agentId,
        name: adapter.agentName,
        type: adapter.type,
        endpoint: adapter.endpoint,
        host: a.host,
        port: a.port,
        health_path: a.health_path,
      });
    }
    return;
  }

  // v2.1 适配器配置
  if (!config.adapters || !Array.isArray(config.adapters)) return;

  for (const adCfg of config.adapters) {
    let adapter;
    const AdapterClass = _getAdapterClass(adCfg.type);

    if (!AdapterClass) {
      console.warn(`[Connector] Unknown adapter type: ${adCfg.type}, skipping`);
      continue;
    }

    try {
      adapter = new AdapterClass({
        id: adCfg.id,
        type: adCfg.type,
        agent: adCfg.agent,
        apiKey: adCfg.apiKey || adCfg.agent?.apiKey,
        options: adCfg.options,
        healthUrl: adCfg.healthUrl,
      });

      // 监听适配器事件 → 转发到 monitor + notifyEngine
      adapter.on('health', (data) => {
        monitor._handleHealthEvent(data);
      });

      adapter.on('alert', (data) => {
        if (notifyEngine.shouldAlert(data.agentId)) {
          const card = notifyEngine.alertCard({
            agentId: data.agentId,
            agent: { name: data.agentName },
            prevStatus: 'healthy',
            failCount: 1,
            error: data.message,
          });
          _pushToWecom(card);
        }
      });

      adapter.on('version_change', (data) => {
        log('INFO', `[${adapter.agentName}] Version: ${data.from} → ${data.to}`);
      });

      // v2.2: 资源事件 → ResourceCollector
      adapter.on('resource', (data) => {
        resourceCollector.report(data).catch(err => {
          log('ERROR', `资源采集处理失败 (${data.agentId}): ${err.message}`);
        });
      });

      adapters.push(adapter);
      monitor.registerAgent(adapter.agentId, {
        id: adapter.agentId,
        name: adapter.agentName,
        type: adapter.type,
        endpoint: adapter.endpoint,
        version: adapter.version,
        selfHosted: adapter.selfHosted,
      });
    } catch (err) {
      console.error(`[Connector] Failed to create adapter ${adCfg.type}:${adCfg.id}: ${err.message}`);
    }
  }
}

function _getAdapterClass(type) {
  const map = {
    generic: GenericAdapter,
    workbuddy: WorkBuddyAdapter,
    openclaw: OpenClawAdapter,
  };
  return map[type] || null;
}

async function startAdapters() {
  for (const adapter of adapters) {
    try {
      await adapter.start();
      log('INFO', `✅ 适配器启动: ${adapter.type}:${adapter.id} → ${adapter.agentName}`);
    } catch (err) {
      log('ERROR', `❌ 适配器启动失败 ${adapter.id}: ${err.message}`);
    }
  }
}

async function stopAdapters() {
  for (const adapter of adapters) {
    try {
      await adapter.stop();
    } catch (err) {
      log('ERROR', `适配器停止失败 ${adapter.id}: ${err.message}`);
    }
  }
}

// NotifyEngine → 企微群卡片发送
function _pushToWecom(card) {
  if (!card) return;
  const chatId = (config.monitor && config.monitor.notify_chatid) || null;
  if (!chatId) {
    log('DEBUG', '未配置 notify_chatid，跳过卡片推送');
    return;
  }
  try {
    wsClient.sendMessage(chatId, card, 2); // group chat
  } catch (err) {
    log('ERROR', `企微卡片推送失败: ${err.message}`);
  }
}

// 注册卡片发送回调
notifyEngine.setSender((card) => _pushToWecom(card));

// AuditLogger → 当任务完成/失败时自动生成审计 → 推送企微 (v2.3)
auditLogger.on('audit:recorded', (auditEntry) => {
  const task = auditEntry.taskId ? stateStore.getTask(auditEntry.taskId) : null;
  notifyEngine.sendAuditSummaryCard(auditEntry, task);
});

// 监听 monitor 事件 → 企微通知（兼容旧版）
monitor.on(EVENTS.AGENT_OFFLINE, (event) => {
  const { agentId } = event;
  if (notifyEngine.shouldAlert(agentId)) {
    const card = notifyEngine.alertCard(event);
    _pushToWecom(card);
  }
});

monitor.on(EVENTS.AGENT_ONLINE, (event) => {
  const card = notifyEngine.stateChangeCard(event);
  if (card) _pushToWecom(card);
});

// 加载适配器
loadAdapters();

// ─── 安装网络守卫（必须在任何 HTTP 请求前） ───
if (networkGuard && config.network?.enabled !== false) {
  networkGuard.install();
  log('INFO', '🛡️ NetworkGuard 已激活');
}

// ─── 注册被管进程（Lifecycle Manager） ───
if (lifecycleMgr && config.lifecycle?.processes?.length > 0) {
  for (const procCfg of config.lifecycle.processes) {
    try {
      lifecycleMgr.register(procCfg);
      if (procCfg.autoStart !== false) {
        lifecycleMgr.start(procCfg.id).then(r => {
          log('INFO', `进程 ${procCfg.name || procCfg.id} 启动${r.ok ? '成功' : '失败: ' + r.error}`);
        });
      }
    } catch (err) {
      log('ERROR', `注册进程失败 ${procCfg.id}: ${err.message}`);
    }
  }
}

// ─── 仪表板 API（L2 → 仪表板 UI） ───
const dashboardAPI = new DashboardAPI(monitor, stateStore, notifyEngine, taskTracker, resourceCollector, auditLogger, lifecycleMgr, secretsScanner, networkGuard);

// P2P 路由器（仅当启用时）
let p2pRouter = null;
let p2pInboundServer = null;

if (config.p2p.enabled) {
  const hostname = config.p2p.p2p_host || '127.0.0.1';
  const p2pPort = config.p2p.p2p_port || 19528;

  p2pRouter = new P2PRouter({
    serverUrl: config.p2p.signaling_server,
    peerInfo: {
      version: '2.0.0',
      hostname: require('os').hostname(),
      p2p_host: hostname,
      p2p_port: p2pPort,
    },
  });
}

// 状态
const startTime = Date.now();
let shuttingDown = false;

// ============================================================
// 核心逻辑：消息流
// ============================================================

/**
 * 接收企微消息 → 转发 Agent → 获取回复 → 推回企微
 */
async function onWecomMessage(standardMsg, originalFrame) {
  // 安全防护：防止 from 缺失（断开事件等异常情况）
  if (!standardMsg || !standardMsg.from) {
    log('DEBUG', '跳过：标准消息缺少 from 字段');
    return;
  }

  if (standardMsg.msg_type === 'event') {
    log('DEBUG', `跳过事件: ${standardMsg.content}`);
    return;
  }

  // 获取会话信息
  const chatId = standardMsg.from.chat_id || standardMsg.from.chatid || 'unknown';
  const userId = standardMsg.from.user_id || standardMsg.from.userid || 'unknown';
  const userName = standardMsg.from.user_name || standardMsg.from.name || '用户';
  const message = standardMsg.content || '';

  let reply;

  // 转发到外部 Agent（由用户配置的实际 Agent）
  reply = await agentBridge.forward(standardMsg);

  if (!reply) return;

  // 如果 Agent 回复要求转发给 P2P peer
  if (reply.p2p_target && p2pRouter) {
    log('INFO', `Agent 要求转发给 P2P peer: ${reply.p2p_target.slice(0, 10)}...`);
    p2pRouter.sendToPeer(reply.p2p_target, reply.p2p_payload || reply);
    return;
  }

  // 正常回复到企微（先扫描敏感信息）
  const msgType = reply.msg_type || 'text';
  const chatid = standardMsg.from.chat_id || standardMsg.from.chatid;
  const chatType = standardMsg.from.chat_type === 'single' ? 1 : 2;

  // v2.4: 敏感信息扫描
  let body = null;
  if (config.secrets?.enabled !== false) {
    const scanText = typeof reply === 'string' ? reply : JSON.stringify(reply);
    const scanResult = secretsScanner.process(scanText, { source: `wecom_reply:${chatid || 'unknown'}` });
    if (scanResult.blocked) {
      log('ERROR', `🚨 回复被阻断（含敏感信息）: ${scanResult.findings.map(f => f.rule).join(', ')}`);
      body = standardToWecomReply({
        msg_type: 'text',
        content: '⚠️ 消息包含敏感信息，已被系统阻断。请联系管理员。',
      }, 'text');
    } else if (scanResult.text !== scanText) {
      // 有脱敏，构造新 reply 对象
      const redactedReply = { ...reply, content: scanResult.text };
      body = msgType === 'card' ? standardToWecomCard(redactedReply) : await standardToWecomReply(redactedReply, msgType);
    } else {
      body = msgType === 'card' ? standardToWecomCard(reply) : await standardToWecomReply(reply, 'markdown');
    }
  } else {
    if (msgType === 'card') {
      body = standardToWecomCard(reply);
    } else {
      body = await standardToWecomReply(reply, 'markdown');
    }
  }

  if (originalFrame) {
    wsClient.reply(originalFrame, body);
  } else if (chatid) {
    wsClient.sendMessage(chatid, body, chatType);
  } else {
    log('WARN', 'chatid 为空，无法推送回复');
  }
}

/**
 * P2P 入站消息处理（对方直连或中继发来的消息）
 */
function onP2PInbound(msg) {
  log('INFO', `← P2P 入站 from=${(msg.from_connector || '?').slice(0, 10)}...`);

  // 构造标准化消息转给 Agent
  const standardMsg = {
    msg_id: `p2p_${Date.now()}`,
    from: {
      user_id: msg.from_connector || 'p2p_peer',
      name: `P2P: ${(msg.from_connector || '').slice(0, 8)}`,
      type: 'p2p_peer',
    },
    content: JSON.stringify(msg.payload),
    msg_type: 'p2p',
    timestamp: new Date().toISOString(),
    channel: 'p2p',
  };

  // 转发给 Agent
  agentBridge.forward(standardMsg).catch(err => {
    log('ERROR', `P2P Agent 处理异常: ${err.message}`);
  });
}

// ============================================================
// 状态面板（轻量 HTTP + P2P 端点）
// ============================================================

function startStatusServer() {
  const server = http.createServer((req, res) => {
    // CORS
    res.setHeader('Access-Control-Allow-Origin', '*');

    // GET /health
    if (req.url === '/health') {
      res.setHeader('Content-Type', 'application/json');
      const snap = monitor.getSnapshot();
      if (wsClient.isConnected && snap.offline === 0) {
        res.writeHead(200);
        res.end(JSON.stringify({ status: 'ok', agents: snap.agents.length, healthy: snap.healthy }));
      } else if (wsClient.isConnected) {
        res.writeHead(200);
        res.end(JSON.stringify({ status: 'degraded', reason: `${snap.offline} agents offline`, agents: snap.agents.length }));
      } else {
        res.writeHead(503);
        res.end(JSON.stringify({ status: 'unhealthy', reason: 'wecom not connected' }));
      }
      return;
    }

    // GET /status → JSON（兼容旧版 API）
    if (req.url === '/status') {
      res.setHeader('Content-Type', 'application/json');
      const uptime = Math.round((Date.now() - startTime) / 1000);
      res.writeHead(200);
      res.end(JSON.stringify({
        service: 'wecom-agent-ops-center',
        version: '2.4.0',
        runtime: 'node.js',
        uptime_seconds: uptime,
        wecom: wsClient.stats,
        agent: monitor.getSnapshot(),
        p2p: p2pRouter ? p2pRouter.stats : { enabled: false },
      }, null, 2));
      return;
    }

    // ─── 任务 API (v2.1 POST) ───
    if (req.url.startsWith('/api/tasks/') && req.method === 'POST') {
      let body = '';
      req.on('data', chunk => { body += chunk; });
      req.on('end', async () => {
        try {
          const data = JSON.parse(body);
          let result;

          if (req.url === '/api/tasks/start') {
            result = await taskTracker.startTask(data);
          } else if (req.url === '/api/tasks/progress') {
            result = await taskTracker.progressTask(data);
          } else if (req.url === '/api/tasks/complete') {
            result = await taskTracker.completeTask(data);
          } else if (req.url === '/api/tasks/fail') {
            result = await taskTracker.failTask(data);
          } else {
            res.writeHead(404, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: `Unknown task endpoint: ${req.url}` }));
            return;
          }

          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ ok: true, ...result }));
        } catch (err) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: err.message }));
        }
      });
      return;
    }

    // ─── 资源上报 API (v2.2 POST) ───
    if (req.url === '/api/resources/report' && req.method === 'POST') {
      let body = '';
      req.on('data', chunk => { body += chunk; });
      req.on('end', async () => {
        try {
          const data = JSON.parse(body);
          const result = await resourceCollector.report(data);
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ ok: true, snapshot: result.snapshot, alerts: result.alerts }));
        } catch (err) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: err.message }));
        }
      });
      return;
    }

    // ─── 审计日志 API (v2.3 POST) ───
    if (req.url === '/api/audit/log' && req.method === 'POST') {
      let body = '';
      req.on('data', chunk => { body += chunk; });
      req.on('end', async () => {
        try {
          const data = JSON.parse(body);
          const result = await auditLogger.log(data);
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ ok: true, auditId: result.auditId }));
        } catch (err) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: err.message }));
        }
      });
      return;
    }

    // ─── 从任务生成审计 (v2.3 POST) ───
    if (req.url === '/api/audit/log-from-task' && req.method === 'POST') {
      let body = '';
      req.on('data', chunk => { body += chunk; });
      req.on('end', async () => {
        try {
          const data = JSON.parse(body);
          const { taskId, decisionPoints, needsHumanReview, metadata } = data;
          const task = stateStore.getTask(taskId);
          if (!task) {
            res.writeHead(404, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: `Task '${taskId}' not found` }));
            return;
          }
          const result = await auditLogger.logFromTask(task, { decisionPoints, needsHumanReview, metadata });
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ ok: true, auditId: result.auditId }));
        } catch (err) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: err.message }));
        }
      });
      return;
    }

    // ─── 通知推送 API（v2.5 — 外部服务调用） ───
    if (req.url === '/api/notify/send' && req.method === 'POST') {
      let body = '';
      req.on('data', chunk => { body += chunk; });
      req.on('end', () => {
        try {
          const { chatid, msgtype, content, chattype } = JSON.parse(body);
          // chatid 可选：未传则用 wsClient 记录的最后一个 chatid → 配置默认值
          const targetChat = chatid || wsClient._lastChatId || config.monitor?.notify_chatid || process.env.WECOM_NOTIFY_CHATID || '';
          if (!targetChat) {
            res.writeHead(400, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'chatid is required (no default configured)' }));
            return;
          }
          if (!msgtype || !content) {
            res.writeHead(400, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'msgtype and content are required' }));
            return;
          }
          const ok = wsClient.sendMessage(targetChat, { msgtype, ...content }, chattype || 1);
          res.writeHead(ok ? 200 : 503, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ ok, reason: ok ? null : 'wecom not connected' }));
        } catch (err) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: err.message }));
        }
      });
      return;
    }

    // API 路由 → DashboardAPI（monitor + tasks + resources + audit + lifecycle + secrets + network + agents）
    if (req.url.startsWith('/api/monitor') || req.url.startsWith('/api/tasks') || req.url.startsWith('/api/resources') || req.url.startsWith('/api/audit') || req.url.startsWith('/api/lifecycle') || req.url.startsWith('/api/secrets') || req.url.startsWith('/api/network') || req.url.startsWith('/api/agents')) {
      dashboardAPI.handle(req, res);
      return;
    }

    // GET / → 仪表板 HTML
    if (req.url === '/' || req.url === '/dashboard' || req.url === '/dashboard.html') {
      const htmlPath = path.join(__dirname, 'dashboard.html');
      try {
        const html = fs.readFileSync(htmlPath, 'utf-8');
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(html);
      } catch (err) {
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Dashboard not found');
      }
      return;
    }

    // 404
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Not found' }));
  });

  const port = config.connector.port;
  server.listen(port, config.connector.host, () => {
  console.log(`📊 仪表板: http://${config.connector.host}:${port}`);
  console.log(`🩺 健康检查: http://${config.connector.host}:${port}/health`);
  });

  return server;
}

// ============================================================
// CLI 命令模式（不启动完整 Connector，只做配对操作）
// ============================================================

async function runCliCommand() {
  const args = process.argv.slice(2);
  const cmd = args[0];

  if (!cmd || cmd === 'start') return 'full'; // 正常启动

  // 检查 P2P 配置
  if (!config.p2p.enabled || !config.p2p.signaling_server) {
    console.error('❌ P2P 未启用，请先在 config.yaml 中设置 p2p.enabled=true 和 signaling_server');
    process.exit(1);
  }

  p2pRouter = new P2PRouter({
    serverUrl: config.p2p.signaling_server,
    peerInfo: { version: '1.1.0', hostname: require('os').hostname() },
  });

  switch (cmd) {
    case 'pair':
    case 'generate': {
      console.log('🔑 正在生成配对码...\n');
      const connected = await p2pRouter.connect();
      if (!connected) {
        console.error('❌ 无法连接配对服务器，请检查 signaling_server 配置');
        process.exit(1);
      }
      try {
        const result = await p2pRouter.generateCode();
        console.log('');
        console.log('='.repeat(40));
        console.log(`  📋 配对码: ${result.code}`);
        console.log(`  ⏰ 有效期: ${result.expires_in} 秒`);
        console.log('');
        console.log('  分享这个码给对方：');
        console.log(`    node connector.js join ${result.code}`);
        console.log('');
        console.log('  或让对方在 Skill 面板中输入：');
        console.log(`    ${result.code}`);
        console.log('='.repeat(40));
      } catch (e) {
        console.error(`❌ 生成失败: ${e.message}`);
        process.exit(1);
      }
      break;
    }

    case 'join': {
      const code = args[1];
      if (!code) {
        console.error('用法: node connector.js join <配对码>');
        console.error('例如: node connector.js join A1B2-C3D4');
        process.exit(1);
      }
      console.log(`🔗 正在加入配对: ${code}\n`);
      const connected = await p2pRouter.connect();
      if (!connected) {
        console.error('❌ 无法连接配对服务器');
        process.exit(1);
      }
      try {
        const result = await p2pRouter.joinWithCode(code);
        console.log('');
        console.log('='.repeat(40));
        console.log('  ✅ 配对成功！');
        console.log(`  Peer ID: ${result.peer.id.slice(0, 10)}...`);
        console.log(`  Peer 信息: ${JSON.stringify(result.peer.peer_info)}`);
        console.log('='.repeat(40));
      } catch (e) {
        console.error(`❌ 加入失败: ${e.message}`);
        process.exit(1);
      }
      break;
    }

    case 'status': {
      const code = args[1];
      if (!code) {
        console.error('用法: node connector.js status <配对码>');
        process.exit(1);
      }
      const result = await p2pRouter.getStatus(code);
      console.log(JSON.stringify(result, null, 2));
      break;
    }

    case 'disconnect': {
      const code = args[1];
      if (!code) {
        console.error('用法: node connector.js disconnect <配对码>');
        process.exit(1);
      }
      await p2pRouter.disconnect(code);
      console.log(`已断开配对 ${code}`);
      break;
    }

    case 'peers': {
      console.log('当前已配对节点:');
      if (p2pRouter.peers.length === 0) {
        console.log('  (无)');
      } else {
        p2pRouter.peers.forEach((p, i) => {
          console.log(`  ${i + 1}. ${p.id.slice(0, 10)}... [${p.channel}] ${p.peer_info?.hostname || '?'}`);
        });
      }
      break;
    }

    default:
      console.error(`未知命令: ${cmd}`);
      console.error('可用命令: pair (生成配对码) | join <码> (加入) | status <码> (查询) | disconnect <码> (断开) | peers (列表)');
      process.exit(1);
  }

  return 'cli';
}

// ============================================================
// 主流程
// ============================================================

async function main() {
  // 先检查是否是 CLI 命令
  const mode = await runCliCommand();
  if (mode === 'cli') {
    process.exit(0);
  }

  console.log('='.repeat(50));
  console.log('  企微 Agent Ops Center v2.3 (Node.js)');
  console.log('  在企微群里看到你的 Agent 在做什么');
  console.log('='.repeat(50));
  console.log('');

  // 验证配置
  const errors = validateConfig(config);
  if (errors.length > 0) {
    errors.forEach(e => console.error(`❌ 配置错误: ${e}`));
    console.error('请编辑 config.yaml 填写 bot_id 和 bot_secret');
    process.exit(1);
  }

  // 启动状态面板
  const statusServer = startStatusServer();

  // 启动 P2P（如果启用）
  if (p2pRouter) {
    console.log(`🌐 配对服务器: ${config.p2p.signaling_server}`);
    const p2pOk = await p2pRouter.connect();
    if (p2pOk) {
      console.log('✅ P2P 网络已连接');

      // 注册 P2P 消息处理 → 转发给 Agent
      p2pRouter.onPeerMessage((msg) => {
        onP2PInbound(msg);
      });

      // 启动 P2P 入站 HTTP 端点（接收对方直连消息）
      const p2pPort = config.p2p.p2p_port || 19528;
      p2pInboundServer = startP2PInboundServer(p2pPort, onP2PInbound);

      console.log('');
    } else {
      console.log('⚠️ P2P 不可用（配对服务器连接失败），仅企微模式运行');
    }
  }

  // 建立企微连接
  console.log(`🔌 正在连接企微... bot=${config.wecom.bot_id.slice(0, 8)}...`);
  const wecomOk = await wsClient.connect(onWecomMessage);

  if (!wecomOk) {
    console.error('❌ 企微连接失败，退出');
    statusServer.close();
    if (p2pInboundServer) p2pInboundServer.close();
    process.exit(1);
  }

  if (config.agent && config.agent.endpoint) {
    console.log(`🤖 Agent 端点: ${config.agent.endpoint}`);
  }
  if (adapters.length > 0) {
    console.log(`📡 ${adapters.length} 个适配器已加载（类型: ${adapters.map(a => a.type).join(', ')}）`);
  }
  if (config.monitor && config.monitor.notify_chatid) {
    console.log(`📢 通知群: ${config.monitor.notify_chatid}`);
  }
  console.log('');
  console.log('✅ 企微 Agent Ops Center 运行中...');

  // 启动适配器（替代旧版 monitor.start()）
  if (adapters.length > 0) {
    await startAdapters();
    stateStore.startPersistence();
  } else {
    // 兼容：如果没有任何适配器但有旧版 monitor agents
    if (monitor.agents.size > 0) {
      monitor.start();
      stateStore.startPersistence();
    }
  }

  if (p2pRouter?.isConnected) {
    console.log('🌐 P2P 已激活 — 可用以下命令:');
    console.log('   node connector.js pair         # 生成配对码');
    console.log('   node connector.js join <CODE>  # 加入配对');
  }

  console.log('   在企微里给机器人发消息试试！');
  console.log('   按 Ctrl+C 退出');
  console.log('');

  // 优雅退出
  const shutdown = async (signal) => {
    if (shuttingDown) return;
    shuttingDown = true;

    console.log(`\n🛑 收到 ${signal}，正在关闭...`);
    monitor.stop();
    await stopAdapters();
    await taskTracker.shutdown();
    await resourceCollector.shutdown();
    await auditLogger.shutdown();
    await lifecycleMgr?.shutdown();   // v2.4 Lifecycle
    networkGuard?.uninstall();               // v2.4 NetworkGuard
    await stateStore.stop();
    await wsClient.disconnect();
    statusServer.close();
    if (p2pInboundServer) p2pInboundServer.close();
    console.log('👋 已关闭');
    process.exit(0);
  };

  process.on('SIGINT', () => shutdown('SIGINT'));
  process.on('SIGTERM', () => shutdown('SIGTERM'));
}

main().catch(err => {
  console.error('💥 致命错误:', err);
  process.exit(1);
});
