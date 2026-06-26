#!/usr/bin/env node
// native-host/host.js
// Chrome Native Messaging Host
//
// 桥接角色:
//   CLI (Unix socket) <──> Chrome Extension (stdin/stdout Native Messaging 协议)
//
// 启动方式:
//   由 Chrome 在 Extension 调用 connectNative() 时自动启动
//   不应手动运行（stdin/stdout 由 Chrome 控制）
//
// Chrome Native Messaging 协议:
//   Host → Extension: 写入 stdout（4 字节 LE 长度 + UTF-8 JSON）
//   Extension → Host: 读取 stdin（同格式）

'use strict';

const net = require('net');
const fs = require('fs');

const SOCKET_PATH = '/tmp/today-earnings.sock';

// ─── Native Messaging 协议 ───────────────────────────────────────────────────

let readBuffer = Buffer.alloc(0);

process.stdin.on('data', (chunk) => {
  readBuffer = Buffer.concat([readBuffer, chunk]);
  // 逐条解析 length-prefixed 消息
  while (readBuffer.length >= 4) {
    const length = readBuffer.readUInt32LE(0);
    if (readBuffer.length < 4 + length) break;
    const payload = readBuffer.slice(4, 4 + length);
    readBuffer = readBuffer.slice(4 + length);
    try {
      const message = JSON.parse(payload.toString('utf8'));
      handleExtensionMessage(message);
    } catch (_) {
      // 忽略非 JSON 消息
    }
  }
});

// Chrome 关闭连接时退出
process.stdin.on('end', () => {
  cleanup();
  process.exit(0);
});

// Host → Extension: 写入 stdout
function sendToExtension(message) {
  const json = JSON.stringify(message);
  const payload = Buffer.from(json, 'utf8');
  const header = Buffer.alloc(4);
  header.writeUInt32LE(payload.length, 0);
  process.stdout.write(Buffer.concat([header, payload]));
}

// ─── 请求路由（Extension 响应 → CLI socket）─────────────────────────────────

// Map<_id, net.Socket>
const pendingRequests = new Map();
let requestIdCounter = 0;

// Extension 返回结果，路由给对应等待中的 CLI 连接
function handleExtensionMessage(message) {
  const { _id, ...response } = message;
  if (_id == null) return;
  const socket = pendingRequests.get(_id);
  if (!socket) return;
  pendingRequests.delete(_id);
  try {
    socket.write(JSON.stringify(response) + '\n');
    socket.end();
  } catch (_) {}
}

// ─── Unix Socket 服务（供 CLI 连接）─────────────────────────────────────────

let socketServer = null;

function startSocketServer() {
  // 清理可能残留的旧 socket 文件
  try {
    fs.unlinkSync(SOCKET_PATH);
  } catch (_) {}

  socketServer = net.createServer((socket) => {
    let buf = '';

    socket.on('data', (data) => {
      buf += data.toString('utf8');
      // 按换行分帧
      const nl = buf.indexOf('\n');
      if (nl === -1) return;

      const line = buf.slice(0, nl).trim();
      buf = buf.slice(nl + 1);

      let request;
      try {
        request = JSON.parse(line);
      } catch (_) {
        socket.write(
          JSON.stringify({ ok: false, error: { code: 'INVALID_REQUEST', message: 'Invalid JSON' } }) + '\n'
        );
        socket.end();
        return;
      }

      const id = ++requestIdCounter;
      pendingRequests.set(id, socket);

      // 转发给 Chrome Extension（写 stdout）
      sendToExtension({ ...request, _id: id });
    });

    // 60 秒无响应则断开
    socket.setTimeout(60000, () => socket.destroy());
    socket.on('error', () => {});
  });

  socketServer.listen(SOCKET_PATH, () => {
    // Unix socket 就绪，等待 CLI 连接
  });

  socketServer.on('error', (err) => {
    process.stderr.write(`Socket server error: ${err.message}\n`);
    process.exit(1);
  });
}

function cleanup() {
  try {
    fs.unlinkSync(SOCKET_PATH);
  } catch (_) {}
}

process.on('exit', cleanup);
process.on('SIGTERM', () => { cleanup(); process.exit(0); });
process.on('SIGINT', () => { cleanup(); process.exit(0); });

startSocketServer();
