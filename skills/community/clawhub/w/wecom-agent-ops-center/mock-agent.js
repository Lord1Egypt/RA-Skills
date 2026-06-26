/**
 * Mock Agent — 用于端到端测试
 * 启动：node mock-agent.js
 * 端口：3001
 */
const http = require('http');

const PORT = 3001;

const server = http.createServer((req, res) => {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  const urlPath = req.url.split('?')[0]; // 去掉 query string
  console.log(`[MockAgent] ${req.method} ${urlPath}`);

  if (req.method === 'POST' && urlPath === '/chat') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const data = JSON.parse(body || '{}');
        const userMsg = (data.content || '').slice(0, 100);
        console.log(`[MockAgent] 收到消息: ${userMsg}`);

        const reply = {
          content: `✅ Mock Agent 已收到你的消息！\n\n你发送的内容：${userMsg || '[空内容]'}\n\n当前时间：${new Date().toLocaleString('zh-CN')}\n\n（这是模拟回复，真实 Agent 会在这里返回 AI 生成的内容）`,
          msg_type: 'text',
        };

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(reply));
        console.log(`[MockAgent] 已回复`);
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: e.message }));
      }
    });
    return;
  }

  // 404
  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ error: 'Not found', url: req.url, path: urlPath }));
});

server.listen(PORT, '127.0.0.1', () => {
  console.log(`[MockAgent] 启动成功，监听 http://127.0.0.1:${PORT}/chat`);
  console.log(`[MockAgent] 等待 Connector 调用...`);
});
