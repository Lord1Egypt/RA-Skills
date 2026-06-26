/**
 * Observability Dashboard - 监控面板
 * 
 * 功能:
 * - 实时指标展示
 * - 日志查看
 * - 追踪详情
 * - 性能图表
 * - 告警状态
 * - LLM/MCP/A2A 监控
 * 
 * @version 0.2.0
 * @author 小蒲萄 (Clawd)
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

const { ObservabilitySystem } = require('./index');

// 创建可观测性系统
const obs = new ObservabilitySystem({
  logging: {
    level: 'info',
    console: true,
    file: true
  },
  metrics: {
    enabled: true,
    prefix: 'agent',
    autoReport: false
  },
  alerts: {
    enabled: true,
    createDefaultRules: true
  },
  llm: { enabled: true },
  mcp: { enabled: true },
  a2a: { enabled: true }
});

// HTML Dashboard
const dashboardHTML = `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🦞 OpenClaw Observability Dashboard</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      padding: 20px;
    }
    .container {
      max-width: 1600px;
      margin: 0 auto;
    }
    h1 {
      color: white;
      text-align: center;
      margin-bottom: 30px;
      font-size: 2.5em;
      text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
      gap: 20px;
      margin-bottom: 30px;
    }
    .card {
      background: white;
      border-radius: 15px;
      padding: 25px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.2);
      transition: transform 0.3s ease;
    }
    .card:hover {
      transform: translateY(-5px);
    }
    .card h2 {
      color: #667eea;
      margin-bottom: 15px;
      font-size: 1.3em;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .metric {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 0;
      border-bottom: 1px solid #eee;
    }
    .metric:last-child {
      border-bottom: none;
    }
    .metric-label {
      color: #666;
      font-size: 0.9em;
    }
    .metric-value {
      font-size: 1.5em;
      font-weight: bold;
      color: #333;
    }
    .metric-unit {
      font-size: 0.8em;
      color: #999;
      margin-left: 5px;
    }
    .status-good { color: #10b981; }
    .status-warn { color: #f59e0b; }
    .status-error { color: #ef4444; }
    .refresh-btn {
      background: #667eea;
      color: white;
      border: none;
      padding: 12px 30px;
      border-radius: 8px;
      font-size: 1em;
      cursor: pointer;
      transition: background 0.3s;
    }
    .refresh-btn:hover {
      background: #5568d3;
    }
    .actions {
      text-align: center;
      margin-bottom: 20px;
    }
    .log-viewer {
      background: #1e293b;
      color: #e2e8f0;
      padding: 20px;
      border-radius: 10px;
      font-family: 'Courier New', monospace;
      font-size: 0.85em;
      max-height: 400px;
      overflow-y: auto;
    }
    .log-entry {
      padding: 5px 0;
      border-bottom: 1px solid #334155;
    }
    .log-info { color: #60a5fa; }
    .log-warn { color: #fbbf24; }
    .log-error { color: #f87171; }
    .tabs {
      display: flex;
      gap: 10px;
      margin-bottom: 20px;
      justify-content: center;
    }
    .tab {
      background: rgba(255,255,255,0.2);
      color: white;
      border: none;
      padding: 10px 20px;
      border-radius: 8px;
      cursor: pointer;
      transition: background 0.3s;
    }
    .tab.active {
      background: white;
      color: #667eea;
    }
    .section {
      display: none;
    }
    .section.active {
      display: block;
    }
    .badge {
      display: inline-block;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 0.75em;
      font-weight: bold;
    }
    .badge-success { background: #d1fae5; color: #065f46; }
    .badge-warning { background: #fef3c7; color: #92400e; }
    .badge-error { background: #fee2e2; color: #991b1b; }
    .badge-info { background: #dbeafe; color: #1e40af; }
  </style>
</head>
<body>
  <div class="container">
    <h1>🦞 OpenClaw Observability Dashboard</h1>
    
    <div class="tabs">
      <button class="tab active" onclick="showSection('overview')">📊 概览</button>
      <button class="tab" onclick="showSection('llm')">🤖 LLM</button>
      <button class="tab" onclick="showSection('mcp')">🔧 MCP</button>
      <button class="tab" onclick="showSection('a2a')">📡 A2A</button>
      <button class="tab" onclick="showSection('alerts')">🚨 告警</button>
      <button class="tab" onclick="showSection('logs')">📝 日志</button>
    </div>

    <div class="actions">
      <button class="refresh-btn" onclick="refreshData()">🔄 刷新数据</button>
    </div>

    <!-- 概览 Section -->
    <div id="overview" class="section active">
      <div class="grid">
        <div class="card">
          <h2>📊 核心指标</h2>
          <div id="core-metrics">
            <div class="metric">
              <span class="metric-label">总调用次数</span>
              <span class="metric-value" id="total-calls">-</span>
            </div>
            <div class="metric">
              <span class="metric-label">平均延迟</span>
              <span class="metric-value" id="avg-latency">-</span>
              <span class="metric-unit">ms</span>
            </div>
            <div class="metric">
              <span class="metric-label">P99 延迟</span>
              <span class="metric-value" id="p99-latency">-</span>
              <span class="metric-unit">ms</span>
            </div>
            <div class="metric">
              <span class="metric-label">错误次数</span>
              <span class="metric-value status-error" id="total-errors">-</span>
            </div>
            <div class="metric">
              <span class="metric-label">活跃 Agent</span>
              <span class="metric-value" id="active-agents">-</span>
            </div>
          </div>
        </div>

        <div class="card">
          <h2>🔍 系统状态</h2>
          <div id="system-status">
            <div class="metric">
              <span class="metric-label">活跃追踪</span>
              <span class="metric-value" id="active-traces">-</span>
            </div>
            <div class="metric">
              <span class="metric-label">日志目录</span>
              <span class="metric-value" style="font-size: 0.9em;" id="log-dir">-</span>
            </div>
            <div class="metric">
              <span class="metric-label">系统状态</span>
              <span class="metric-value status-good" id="system-health">✅ 正常</span>
            </div>
          </div>
        </div>

        <div class="card">
          <h2>⏱️ 延迟分布</h2>
          <div id="latency-buckets">
            <div class="metric">
              <span class="metric-label">&lt; 50ms</span>
              <span class="metric-value status-good" id="latency-fast">-</span>
            </div>
            <div class="metric">
              <span class="metric-label">50-500ms</span>
              <span class="metric-value status-warn" id="latency-medium">-</span>
            </div>
            <div class="metric">
              <span class="metric-label">&gt; 500ms</span>
              <span class="metric-value status-error" id="latency-slow">-</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- LLM Section -->
    <div id="llm" class="section">
      <div class="grid">
        <div class="card">
          <h2>🤖 LLM 统计</h2>
          <div id="llm-stats">
            <div class="metric">
              <span class="metric-label">总调用次数</span>
              <span class="metric-value" id="llm-calls">-</span>
            </div>
            <div class="metric">
              <span class="metric-label">总 Token 数</span>
              <span class="metric-value" id="llm-tokens">-</span>
            </div>
            <div class="metric">
              <span class="metric-label">总成本</span>
              <span class="metric-value" id="llm-cost">-</span>
              <span class="metric-unit">USD</span>
            </div>
            <div class="metric">
              <span class="metric-label">错误次数</span>
              <span class="metric-value status-error" id="llm-errors">-</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- MCP Section -->
    <div id="mcp" class="section">
      <div class="grid">
        <div class="card">
          <h2>🔧 MCP 统计</h2>
          <div id="mcp-stats">
            <div class="metric">
              <span class="metric-label">总调用次数</span>
              <span class="metric-value" id="mcp-calls">-</span>
            </div>
            <div class="metric">
              <span class="metric-label">成功率</span>
              <span class="metric-value" id="mcp-success-rate">-</span>
              <span class="metric-unit">%</span>
            </div>
            <div class="metric">
              <span class="metric-label">平均执行时间</span>
              <span class="metric-value" id="mcp-avg-time">-</span>
              <span class="metric-unit">ms</span>
            </div>
            <div class="metric">
              <span class="metric-label">活跃工具数</span>
              <span class="metric-value" id="mcp-tools">-</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- A2A Section -->
    <div id="a2a" class="section">
      <div class="grid">
        <div class="card">
          <h2>📡 A2A 统计</h2>
          <div id="a2a-stats">
            <div class="metric">
              <span class="metric-label">总消息数</span>
              <span class="metric-value" id="a2a-messages">-</span>
            </div>
            <div class="metric">
              <span class="metric-label">成功率</span>
              <span class="metric-value" id="a2a-success-rate">-</span>
              <span class="metric-unit">%</span>
            </div>
            <div class="metric">
              <span class="metric-label">平均延迟</span>
              <span class="metric-value" id="a2a-avg-latency">-</span>
              <span class="metric-unit">ms</span>
            </div>
            <div class="metric">
              <span class="metric-label">活跃会话</span>
              <span class="metric-value" id="a2a-sessions">-</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Alerts Section -->
    <div id="alerts" class="section">
      <div class="grid">
        <div class="card">
          <h2>🚨 告警状态</h2>
          <div id="alert-stats">
            <div class="metric">
              <span class="metric-label">总规则数</span>
              <span class="metric-value" id="alert-rules">-</span>
            </div>
            <div class="metric">
              <span class="metric-label">触发中</span>
              <span class="metric-value status-error" id="alert-firing">-</span>
            </div>
            <div class="metric">
              <span class="metric-label">待处理</span>
              <span class="metric-value status-warn" id="alert-pending">-</span>
            </div>
            <div class="metric">
              <span class="metric-label">24h 告警数</span>
              <span class="metric-value" id="alert-24h">-</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Logs Section -->
    <div id="logs" class="section">
      <div class="card">
        <h2>📝 最近日志</h2>
        <div class="log-viewer" id="log-viewer">
          <div class="log-entry">等待日志数据...</div>
        </div>
      </div>
    </div>
  </div>

  <script>
    function showSection(sectionId) {
      // Hide all sections
      document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      
      // Show selected section
      document.getElementById(sectionId).classList.add('active');
      event.target.classList.add('active');
    }

    async function refreshData() {
      try {
        const response = await fetch('/api/status');
        const data = await response.json();

        // Update core metrics
        document.getElementById('total-calls').textContent = data.metrics?.totalCalls || 0;
        document.getElementById('avg-latency').textContent = (data.metrics?.avgLatency || 0).toFixed(1);
        document.getElementById('p99-latency').textContent = (data.metrics?.latencyP99 || 0).toFixed(0);
        document.getElementById('total-errors').textContent = data.metrics?.totalErrors || 0;
        document.getElementById('active-agents').textContent = data.metrics?.activeAgents || 0;

        // Update system status
        document.getElementById('active-traces').textContent = data.activeTraces || 0;
        document.getElementById('log-dir').textContent = data.logDir || '-';

        // Update LLM stats
        if (data.llm) {
          document.getElementById('llm-calls').textContent = data.llm.totalCalls || 0;
          document.getElementById('llm-tokens').textContent = data.llm.totalTokens || 0;
          document.getElementById('llm-cost').textContent = (data.llm.totalCost || 0).toFixed(4);
          document.getElementById('llm-errors').textContent = data.llm.totalErrors || 0;
        }

        // Update MCP stats
        if (data.mcp) {
          document.getElementById('mcp-calls').textContent = data.mcp.totalCalls || 0;
          document.getElementById('mcp-success-rate').textContent = (data.mcp.overallSuccessRate || 0).toFixed(1);
          document.getElementById('mcp-avg-time').textContent = (data.mcp.avgExecutionTime || 0).toFixed(1);
          document.getElementById('mcp-tools').textContent = (data.mcp.tools || []).length;
        }

        // Update A2A stats
        if (data.a2a) {
          document.getElementById('a2a-messages').textContent = data.a2a.totalMessages24h || 0;
          document.getElementById('a2a-success-rate').textContent = (data.a2a.successRate || 0).toFixed(1);
          document.getElementById('a2a-avg-latency').textContent = (data.a2a.avgLatency || 0).toFixed(1);
          document.getElementById('a2a-sessions').textContent = data.a2a.activeSessions || 0;
        }

        // Update alert stats
        if (data.alerts) {
          document.getElementById('alert-rules').textContent = data.alerts.totalRules || 0;
          document.getElementById('alert-firing').textContent = data.alerts.firingRules || 0;
          document.getElementById('alert-pending').textContent = data.alerts.pendingRules || 0;
          document.getElementById('alert-24h').textContent = data.alerts.totalAlerts24h || 0;
        }

        // Update logs
        const logsResponse = await fetch('/api/logs');
        const logs = await logsResponse.json();
        const logViewer = document.getElementById('log-viewer');
        logViewer.innerHTML = logs.slice(0, 50).map(log => {
          const levelClass = log.level === 'error' ? 'log-error' : 
                            log.level === 'warn' ? 'log-warn' : 
                            log.level === 'debug' ? 'log-debug' : 'log-info';
          return '<div class="log-entry"><span class="' + levelClass + '">[' + 
                 (log.timestamp || 'N/A') + '] ' + (log.level || 'info').toUpperCase() + 
                 '</span>: ' + (log.message || log.raw || 'N/A') + '</div>';
        }).join('');

      } catch (error) {
        console.error('Failed to refresh data:', error);
      }
    }

    // Initial load
    refreshData();
    
    // Auto refresh every 5 seconds
    setInterval(refreshData, 5000);
  </script>
</body>
</html>
`;

// Create HTTP server
const server = http.createServer((req, res) => {
  if (req.url === '/' || req.url === '/dashboard') {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(dashboardHTML);
  } else if (req.url === '/api/status') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(obs.getStatus(), null, 2));
  } else if (req.url === '/api/metrics') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(obs.exportMetrics(), null, 2));
  } else if (req.url === '/api/logs') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(obs.exportLogs({ limit: 100 })));
  } else if (req.url === '/api/prometheus') {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end(obs.exportMetrics('prometheus'));
  } else if (req.url === '/api/alerts') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(obs.getAlertHistory({ limit: 50 }), null, 2));
  } else {
    res.writeHead(404);
    res.end('Not Found');
  }
});

const PORT = process.env.OBSERVABILITY_PORT || 3001;

server.listen(PORT, () => {
  console.log('🦞 Observability Dashboard running at http://localhost:' + PORT);
  console.log('   API Endpoints:');
  console.log('   - GET /              - Dashboard UI');
  console.log('   - GET /api/status    - System status');
  console.log('   - GET /api/metrics   - Metrics (JSON)');
  console.log('   - GET /api/logs      - Recent logs');
  console.log('   - GET /api/prometheus - Prometheus format');
  console.log('   - GET /api/alerts    - Alert history');
});

// Simulate some metrics for demo
setTimeout(() => {
  const trace = obs.startTrace('agent.execute', { query: 'test' });
  setTimeout(() => {
    trace.end({ result: 'success' });
  }, 150);
}, 1000);

setTimeout(() => {
  const trace = obs.startTrace('agent.execute', { query: 'search' });
  setTimeout(() => {
    trace.end({ result: 'success' });
  }, 320);
}, 2000);

setTimeout(() => {
  const trace = obs.startTrace('agent.execute', { query: 'analyze' });
  setTimeout(() => {
    trace.end({ result: 'success' });
  }, 80);
}, 3000);