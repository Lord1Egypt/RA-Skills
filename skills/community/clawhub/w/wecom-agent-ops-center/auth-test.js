/**
 * 企微 WebSocket 完整测试 - 订阅 → 接收消息 → 自动回复
 *
 * 启动后请在企微里给机器人发消息！
 */

const WebSocket = require('ws');
const { loadConfig } = require('./config');

const config = loadConfig();

console.log('='.repeat(50));
console.log('  企微 WebSocket 连接测试');
console.log('='.repeat(50));
console.log(`  bot_id: ${config.wecom.bot_id}`);
console.log('');

const ws = new WebSocket(config.wecom.ws_url);
let subscribed = false;
let msgCount = 0;

ws.on('open', () => {
  console.log('[WS] TCP 已连接');
  const reqId = `req_${Date.now()}`;
  ws.send(JSON.stringify({
    cmd: 'aibot_subscribe',
    headers: { req_id: reqId },
    body: {
      bot_id: config.wecom.bot_id,
      secret: config.wecom.bot_secret,
    },
  }));
  console.log(`[WS] → 订阅请求 | req_id=${reqId}`);
});

ws.on('message', (data) => {
  try {
    const frame = JSON.parse(data.toString());

    // 订阅响应（无 cmd 字段，有 errcode）
    if (frame.errcode !== undefined) {
      subscribed = frame.errcode === 0;
      console.log(`\n${subscribed ? '✅' : '❌'} 订阅结果: errcode=${frame.errcode} errmsg="${frame.errmsg}"`);
      if (subscribed) {
        console.log('   企微长连接已建立！请在企微里给机器人发消息测试...');
        console.log('   (60 秒后自动断开，或按 Ctrl+C 退出)\n');
      }
      return;
    }

    // 消息回调
    const cmd = frame.cmd;
    if (cmd === 'aibot_msg_callback') {
      msgCount++;
      const body = frame.body || {};
      const userId = (body.from && body.from.userid) || '?';
      const content = (body.text && body.text.content) || '';
      const reqId = (frame.headers && frame.headers.req_id) || '';

      console.log(`📩 收到消息 #${msgCount} | from=${userId} | "${content}"`);

      // 自动回显
      const replyMsg = {
        cmd: 'aibot_msg_reply',
        headers: { req_id: reqId },
        body: {
          msgtype: 'markdown',
          markdown: {
            content: `## ✅ Connector 测试成功！\n\n收到消息：**${content}**\n\n> 发送者：${userId}\n> 时间：${new Date().toLocaleString('zh-CN')}\n> 消息序号：#${msgCount}`,
          },
        },
      };
      ws.send(JSON.stringify(replyMsg));
      console.log('📤 已自动回复\n');
      return;
    }

    console.log(`[WS] ← 其他帧 | ${JSON.stringify(frame).slice(0, 200)}`);
  } catch (e) {
    console.error(`[WS] 解析失败: ${e.message}`);
  }
});

ws.on('error', (err) => {
  console.error(`[WS] 错误: ${err.message}`);
});

ws.on('close', (code, reason) => {
  const reasonStr = reason ? reason.toString() : '';
  console.log(`\n[WS] 已断开 | code=${code}`);
  console.log(`   订阅: ${subscribed ? '✅' : '❌'}`);
  console.log(`   消息: ${msgCount} 条`);

  if (subscribed && msgCount > 0) {
    console.log('\n🎉 完整 E2E 测试通过！');
  } else if (subscribed) {
    console.log('\n⚠️  订阅成功但未收到消息');
  }
  process.exit(0);
});

// 超时退出
setTimeout(() => {
  if (!subscribed) {
    console.error('\n❌ 订阅超时');
    ws.close();
  }
}, 10000);

// 60 秒后自动断开
setTimeout(() => {
  if (subscribed) {
    console.log('\n⏰ 60 秒到，断开连接...');
    ws.close(1000, 'test complete');
  }
}, 60000);
