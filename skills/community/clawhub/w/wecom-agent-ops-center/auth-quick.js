/**
 * 快速订阅测试 - 使用正确的 aibot_subscribe 命令
 */
const WebSocket = require('ws');
const { loadConfig } = require('./config');

const config = loadConfig();
const ws = new WebSocket(config.wecom.ws_url);
let done = false;

ws.on('open', () => {
  const reqId = `req_${Date.now()}`;
  ws.send(JSON.stringify({
    cmd: 'aibot_subscribe',
    headers: { req_id: reqId },
    body: {
      bot_id: config.wecom.bot_id,
      secret: config.wecom.bot_secret,
    },
  }));
  console.log('sent aibot_subscribe');
});

ws.on('message', (data) => {
  const frame = JSON.parse(data.toString());
  console.log('received:', JSON.stringify(frame));

  if (frame.errcode !== undefined) {
    done = true;
    console.log(`RESULT: errcode=${frame.errcode} errmsg="${frame.errmsg}"`);
    console.log(frame.errcode === 0 ? 'AUTH_OK' : 'AUTH_FAIL');
    ws.close();
  }
});

ws.on('error', (err) => {
  if (!done) { done = true; console.log('ERROR:', err.message); }
});

setTimeout(() => {
  if (!done) { done = true; console.log('TIMEOUT'); ws.close(); }
}, 8000);
