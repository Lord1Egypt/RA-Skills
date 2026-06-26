#!/usr/bin/env node

/**
 * Vibe Coding 开发服务器
 * 
 * 提供：
 * 1. HTTP 服务器 - 托管可视化界面
 * 2. WebSocket 服务器 - 实时推送执行数据
 * 3. API 接口 - 启动执行任务
 */

const http = require('http');
const WebSocket = require('ws');
const fs = require('fs');
const path = require('path');
const { VibeExecutorIntegrated } = require('./executors/vibe-executor-integrated');

const PORT = process.env.PORT || 3000;
const WS_PORT = process.env.WS_PORT || 8765;

// 服务器根目录
const ROOT_DIR = __dirname;

/**
 * WebSocket 服务器 - 独立启动，作为消息中转站
 */
const wss = new WebSocket.Server({ port: WS_PORT });

console.log(`[WebSocket] 服务器启动在 ws://localhost:${WS_PORT}`);

wss.on('connection', (ws) => {
  console.log(`[WebSocket] 客户端已连接`);
  
  // 发送欢迎消息
  ws.send(JSON.stringify({
    type: 'connected',
    message: '已连接到 Vibe Coding 执行器',
    timestamp: new Date().toISOString()
  }));
  
  ws.on('close', () => {
    console.log(`[WebSocket] 客户端已断开`);
  });
  
  ws.on('error', (error) => {
    console.error(`[WebSocket] 错误:`, error);
  });
});

// 全局 WebSocket 广播函数
function broadcastToClients(data) {
  const message = JSON.stringify(data);
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(message);
    }
  });
}

/**
 * HTTP 服务器
 */
const server = http.createServer((req, res) => {
  // API 路由优先处理
  if (req.url === '/api/execute' && req.method === 'POST') {
    handleApiExecute(req, res);
    return;
  }
  
  // 静态文件服务
  console.log(`[HTTP] ${req.method} ${req.url}`);
  
  // 路由
  let filePath = path.join(ROOT_DIR, req.url);
  if (req.url === '/' || req.url === '/ui/vibe-dashboard.html') {
    filePath = path.join(ROOT_DIR, 'ui', 'vibe-dashboard.html');
  }
  
  const extname = path.extname(filePath);
  let contentType = 'text/html';
  
  const mimeTypes = {
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon'
  };
  
  contentType = mimeTypes[extname] || 'application/octet-stream';
  
  fs.readFile(filePath, (error, content) => {
    if (error) {
      if (error.code === 'ENOENT') {
        res.writeHead(404);
        res.end('404 Not Found');
      } else {
        res.writeHead(500);
        res.end(`500 Error: ${error.code}`);
      }
    } else {
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content);
    }
  });
});

/**
 * API 接口 - 启动执行
 */
async function handleApiExecute(req, res) {
  console.log(`[API] ${req.method} ${req.url}`);
  
  let body = '';
  
  req.on('data', chunk => {
    body += chunk.toString();
  });
  
  req.on('end', async () => {
    try {
      const { requirement } = JSON.parse(body);
      
      if (!requirement) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'requirement is required' }));
        return;
      }
      
      console.log(`[API] 启动执行：${requirement}`);
      
      // 发送开始消息
      broadcastToClients({
        type: 'execution_start',
        requirement,
        projectName: requirement.replace(/[^\w\u4e00-\u9fa5]/g, '').substring(0, 20),
        timestamp: new Date().toISOString()
      });
      
      // 启动执行器（使用全局 WebSocket 广播）
      const executor = new VibeExecutorIntegrated(requirement, {
        wsPort: WS_PORT,
        broadcastFn: broadcastToClients
      });
      
      // 异步执行，不等待完成
      executor.execute().then((result) => {
        broadcastToClients({
          type: 'execution_complete',
          stats: {
            duration: Math.round(result.duration / 1000),
            avgQualityScore: result.avgQualityScore,
            filesGenerated: result.files.length,
            phasesCompleted: 5
          },
          timestamp: new Date().toISOString()
        });
      }).catch((error) => {
        broadcastToClients({
          type: 'log',
          logType: 'error',
          message: `❌ 执行失败：${error.message}`,
          timestamp: new Date().toISOString()
        });
      });
      
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        status: 'started',
        requirement,
        wsUrl: `ws://localhost:${WS_PORT}`
      }));
    } catch (error) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: error.message }));
    }
  });
}

// 启动 HTTP 服务器
server.listen(PORT, () => {
  console.log(`
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🎨 Vibe Coding v3.0 开发服务器已启动                    ║
║                                                           ║
║   HTTP 服务器：http://localhost:${PORT}                     ║
║   WebSocket:    ws://localhost:${WS_PORT}                   ║
║                                                           ║
║   可视化界面：                                            ║
║   http://localhost:${PORT}/ui/vibe-dashboard.html           ║
║                                                           ║
║   API 接口：                                              ║
║   POST http://localhost:${PORT}/api/execute                 ║
║   Body: { "requirement": "做一个个税计算器" }          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
  `);
});

// 优雅退出
process.on('SIGINT', () => {
  console.log('\n[服务器] 正在关闭...');
  wss.close(() => {
    console.log('[WebSocket] 已关闭');
  });
  server.close(() => {
    console.log('[HTTP] 已关闭');
    process.exit(0);
  });
});

// 导出 WebSocket 广播函数
module.exports = { broadcastToClients, wss };
