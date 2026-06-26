/**
 * 测试 Agent - 模拟用户 Agent 端点，用于 E2E 测试
 *
 * 启动：node test-agent.js
 * 监听：http://localhost:3000/chat
 *
 * 收到企微消息后，原样回显（加上前缀）
 */

const http = require('http');

const PORT = process.env.TEST_AGENT_PORT || 3000;

const server = http.createServer(async (req, res) => {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  if (req.method !== 'POST' || req.url !== '/chat') {
    res.writeHead(404);
    res.end('Not Found');
    return;
  }

  // 读取请求体
  let body = '';
  req.on('data', chunk => body += chunk);

  req.on('end', () => {
    try {
      const msg = JSON.parse(body);

      const userId = msg.from && msg.from.user_id || '?';
      const content = msg.content || '';
      const msgId = msg.msg_id || '?';

      console.log(`\n📩 收到消息 | from=${userId} | "${content.slice(0, 50)}"`);

      // 回显消息（模拟 Agent 回复）
      const reply = {
        reply_to: msgId,
        content: `🤖 [测试Agent] 收到你的消息：「${content}」\n\n> 来自：${userId}\n> 时间：${new Date().toLocaleString('zh-CN')}`,
        msg_type: 'markdown',
      };

      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(reply));

      console.log(`📤 回复 | "${reply.content.slice(0, 100)}..."`);
    } catch (e) {
      console.error(`❌ JSON 解析失败: ${e.message}`);
      res.writeHead(400);
      res.end(JSON.stringify({ error: 'Invalid JSON' }));
    }
  });
});

server.listen(PORT, () => {
  console.log(`🧪 测试 Agent 已启动: http://localhost:${PORT}/chat`);
  console.log('   等待 Connector 转发企微消息...\n');
});
