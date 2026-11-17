#!/usr/bin/env node
/*
 * 七国群雄传 · 联机对战 WebSocket 信令/中继服务器（零依赖）
 * - 按房间号中继两台客户端之间的消息（只转发给同房间其他 peer）
 * - 不解析游戏逻辑，只透传 JSON 文本帧
 * 启动：node net-server.js [port]   默认端口 8770
 */
const http = require('http');
const crypto = require('crypto');
const net = require('net');

const PORT = parseInt(process.argv[2] || process.env.PORT || '8770', 10);
const GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11';
const rooms = Object.create(null); // roomCode -> Set(peer)

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
  res.end('QIGUO NET RELAY OK\n');
});

server.on('upgrade', (req, socket) => {
  const key = req.headers['sec-websocket-key'];
  if (!key) { socket.destroy(); return; }
  const accept = crypto.createHash('sha1').update(key + GUID).digest('base64');
  socket.write(
    'HTTP/1.1 101 Switching Protocols\r\n' +
    'Upgrade: websocket\r\n' +
    'Connection: Upgrade\r\n' +
    'Sec-WebSocket-Accept: ' + accept + '\r\n\r\n'
  );
  socket.setNoDelay(true);

  const peer = { socket, room: null, alive: true };
  const buf = { chunks: [], len: 0 };

  socket.on('data', (data) => {
    buf.chunks.push(data);
    buf.len += data.length;
    let buffer = Buffer.concat(buf.chunks, buf.len);
    // 循环解析可能粘在一起的多个帧
    while (buffer.length >= 2) {
      const b0 = buffer[0], b1 = buffer[1];
      const opcode = b0 & 0x0f;
      const masked = (b1 & 0x80) === 0x80;
      let len = b1 & 0x7f;
      let offset = 2;
      if (len === 126) {
        if (buffer.length < offset + 2) break;
        len = buffer.readUInt16BE(offset); offset += 2;
      } else if (len === 127) {
        if (buffer.length < offset + 8) break;
        const hi = buffer.readUInt32BE(offset), lo = buffer.readUInt32BE(offset + 4);
        len = hi * 4294967296 + lo; offset += 8;
      }
      let maskKey = null;
      if (masked) {
        if (buffer.length < offset + 4) break;
        maskKey = buffer.slice(offset, offset + 4); offset += 4;
      }
      if (buffer.length < offset + len) break;
      let payload = buffer.slice(offset, offset + len);
      if (masked && maskKey) {
        const out = Buffer.allocUnsafe(len);
        for (let i = 0; i < len; i++) out[i] = payload[i] ^ maskKey[i & 3];
        payload = out;
      }
      buffer = buffer.slice(offset + len);
      buf.chunks = [buffer]; buf.len = buffer.length;
      handleFrame(peer, opcode, payload);
    }
  });

  socket.on('close', () => leaveRoom(peer));
  socket.on('error', () => leaveRoom(peer));
});

function handleFrame(peer, opcode, payload) {
  if (opcode === 0x8) { // close
    try { peer.socket.end(); } catch (e) {}
    leaveRoom(peer); return;
  }
  if (opcode === 0x9) { // ping -> pong
    try { peer.socket.write(encodeFrame(0xA, payload)); } catch (e) {}
    return;
  }
  if (opcode === 0xA) return; // pong
  if (opcode !== 0x1 && opcode !== 0x2) return; // 只处理文本/二进制
  let msg;
  try { msg = JSON.parse(payload.toString('utf8')); } catch (e) { return; }
  if (!msg || typeof msg.t !== 'string') return;

  if (msg.t === 'HELLO') {
    peer.room = String(msg.room || 'qiguo');
    if (!rooms[peer.room]) rooms[peer.room] = new Set();
    rooms[peer.room].add(peer);
    const n = rooms[peer.room].size;
    peer.socket.write(encodeFrame(0x1, Buffer.from(JSON.stringify({ t: 'ROOM', room: peer.room, size: n }))));
    if (n >= 2) { // 通知双方房间已就绪
      broadcast(peer.room, { t: 'READY' }, null);
    }
    return;
  }
  if (peer.room) broadcast(peer.room, msg, peer);
}

function broadcast(room, msg, except) {
  const set = rooms[room];
  if (!set) return;
  const data = encodeFrame(0x1, Buffer.from(JSON.stringify(msg)));
  for (const p of set) {
    if (p === except || !p.alive) continue;
    try { p.socket.write(data); } catch (e) { leaveRoom(p); }
  }
}

function leaveRoom(peer) {
  if (!peer.alive) return;
  peer.alive = false;
  if (peer.room && rooms[peer.room]) {
    rooms[peer.room].delete(peer);
    broadcast(peer.room, { t: 'PEER_LEFT' }, peer);
    if (rooms[peer.room].size === 0) delete rooms[peer.room];
  }
  try { peer.socket.destroy(); } catch (e) {}
}

function encodeFrame(opcode, payload) {
  const len = payload.length;
  let header;
  if (len < 126) {
    header = Buffer.from([0x80 | opcode, len]);
  } else if (len < 65536) {
    header = Buffer.allocUnsafe(4);
    header[0] = 0x80 | opcode; header[1] = 126;
    header.writeUInt16BE(len, 2);
  } else {
    header = Buffer.allocUnsafe(10);
    header[0] = 0x80 | opcode; header[1] = 127;
    header.writeUInt32BE(Math.floor(len / 4294967296), 2);
    header.writeUInt32BE(len >>> 0, 6);
  }
  return Buffer.concat([header, payload]);
}

server.listen(PORT, () => {
  console.log('[qiguo-net] WebSocket relay listening on ws://127.0.0.1:' + PORT);
});
