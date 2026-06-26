/**
 * 配对流程 E2E 测试
 *
 * 模拟两个 Connector 完整配对流程：
 *   1. Connector A 生成配对码
 *   2. Connector B 用配对码加入
 *   3. 验证 WebSocket 通知双方
 *   4. 测试中继消息
 *   5. 测试断开
 */

const WebSocket = require('ws');

const SERVER_URL = 'http://localhost:19527';
const WS_URL = 'ws://localhost:19527/ws';

let passed = 0;
let failed = 0;

function check(name, condition, detail) {
  if (condition) {
    console.log(`  ✅ ${name}${detail ? ': ' + detail : ''}`);
    passed++;
  } else {
    console.log(`  ❌ ${name}${detail ? ': ' + detail : ''}`);
    failed++;
  }
}

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// ============================================================
// 测试 1: HTTP API — 生成配对码
// ============================================================
async function testGenerateCode() {
  console.log('\n📋 测试 1: 生成配对码');

  const resp = await fetch(`${SERVER_URL}/pair/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      connector_id: 'conn_A_test',
      peer_info: { hostname: 'pc-alice', p2p_port: 19528 },
    }),
  });

  const result = await resp.json();
  check('HTTP 201', resp.status === 201, `status=${resp.status}`);
  check('有配对码', !!result.code, result.code);
  check('connector_id 返回', result.connector_id === 'conn_A_test');
  check('有效期 300 秒', result.expires_in === 300);
  check('有 expires_at', !!result.expires_at);

  return result;
}

// ============================================================
// 测试 2: HTTP API — 查询配对状态
// ============================================================
async function testGetStatus(code) {
  console.log('\n📋 测试 2: 查询配对状态');

  const resp = await fetch(`${SERVER_URL}/pair/status/${code}`);
  const result = await resp.json();

  check('HTTP 200', resp.status === 200);
  check('status = waiting', result.status === 'waiting');
  check('has_joiner = false', result.has_joiner === false);

  return result;
}

// ============================================================
// 测试 3: HTTP API — 加入配对
// ============================================================
async function testJoinCode(code) {
  console.log('\n📋 测试 3: 加入配对');

  const resp = await fetch(`${SERVER_URL}/pair/join`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      code,
      connector_id: 'conn_B_test',
      peer_info: { hostname: 'pc-bob', p2p_port: 19528 },
    }),
  });

  const result = await resp.json();
  check('HTTP 200', resp.status === 200);
  check('status = joined', result.status === 'joined');
  check('返回 peer 信息', !!result.peer);
  check('peer.id = conn_A', result.peer.id === 'conn_A_test');

  return result;
}

// ============================================================
// 测试 4: 重复加入应拒绝
// ============================================================
async function testDuplicateJoin(code) {
  console.log('\n📋 测试 4: 重复加入应拒绝');

  const resp = await fetch(`${SERVER_URL}/pair/join`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code, connector_id: 'conn_C_test' }),
  });

  const result = await resp.json();
  check('HTTP 409', resp.status === 409);
  check('error = already_joined', result.error === 'already_joined');
}

// ============================================================
// 测试 5: WebSocket 信令通道 — 注册 + 通知
// ============================================================
async function testWebSocketSignaling() {
  console.log('\n📋 测试 5: WebSocket 信令通道');

  // Connector A 连接 WS
  const wsA = new WebSocket(WS_URL);
  let aRegistered = false;
  let aPeerJoined = false;

  await new Promise((resolve) => {
    wsA.on('open', () => {
      wsA.send(JSON.stringify({ type: 'register', connector_id: 'conn_A_ws' }));
    });
    wsA.on('message', (data) => {
      const msg = JSON.parse(data.toString());
      if (msg.type === 'registered') {
        aRegistered = true;
      }
      if (msg.type === 'peer_joined') {
        aPeerJoined = true;
      }
    });
    setTimeout(resolve, 500);
  });

  check('Connector A 注册成功', aRegistered);

  // 生成配对码（Connector A 发起）
  const resp = await fetch(`${SERVER_URL}/pair/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ connector_id: 'conn_A_ws' }),
  });
  const { code } = await resp.json();

  // Connector B 加入配对
  await fetch(`${SERVER_URL}/pair/join`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code, connector_id: 'conn_B_ws' }),
  });

  // 等待 WebSocket 通知到达
  await sleep(300);
  check('Connector A 收到 peer_joined', aPeerJoined);

  wsA.close();
}

// ============================================================
// 测试 6: WebSocket 中继消息
// ============================================================
async function testRelayMessage() {
  console.log('\n📋 测试 6: WebSocket 中继消息');

  const wsA = new WebSocket(WS_URL);
  const wsB = new WebSocket(WS_URL);
  let bReceived = false;

  await new Promise((resolve, reject) => {
    let aReady = false;
    let bReady = false;

    wsA.on('open', () => wsA.send(JSON.stringify({ type: 'register', connector_id: 'relay_A' })));
    wsA.on('message', (data) => {
      const msg = JSON.parse(data.toString());
      if (msg.type === 'registered') aReady = true;
    });

    wsB.on('open', () => wsB.send(JSON.stringify({ type: 'register', connector_id: 'relay_B' })));
    wsB.on('message', (data) => {
      const msg = JSON.parse(data.toString());
      if (msg.type === 'registered') bReady = true;
      if (msg.type === 'relay' && msg.from_id === 'relay_A') {
        bReceived = true;
        check('中继消息 payload 正确', msg.payload.order === 'TEST_001');
        resolve(true);
      }
    });

    // 等待双方注册完成
    const checkReady = setInterval(() => {
      if (aReady && bReady) {
        clearInterval(checkReady);
        // 发送中继消息
        wsA.send(JSON.stringify({
          type: 'relay',
          target_id: 'relay_B',
          payload: { order: 'TEST_001', qty: 500 },
        }));
      }
    }, 100);

    setTimeout(() => reject(new Error('timeout')), 3000);
  });

  check('Connector B 收到中继消息', bReceived);

  wsA.close();
  wsB.close();
}

// ============================================================
// 测试 7: 错误处理
// ============================================================
async function testErrorHandling() {
  console.log('\n📋 测试 7: 错误处理');

  // 不存在的配对码
  const resp1 = await fetch(`${SERVER_URL}/pair/status/XXXX-YYYY`);
  check('不存在的码返回 404', resp1.status === 404);

  // 缺少配对码
  const resp2 = await fetch(`${SERVER_URL}/pair/join`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({}),
  });
  check('缺少 code 返回 400', resp2.status === 400);

  // 健康检查
  const resp3 = await fetch(`${SERVER_URL}/health`);
  const health = await resp3.json();
  check('健康检查 OK', health.status === 'ok');
}

// ============================================================
// 主测试
// ============================================================

async function main() {
  console.log('='.repeat(50));
  console.log('  配对服务器 E2E 测试');
  console.log('='.repeat(50));

  // 先检查服务器是否运行
  try {
    const resp = await fetch(`${SERVER_URL}/health`);
    if (resp.status !== 200) throw new Error('unhealthy');
  } catch (e) {
    console.error('❌ 配对服务器未运行，请先启动: node pairing-server.js');
    process.exit(1);
  }

  try {
    // 测试 1-4: HTTP API
    const genResult = await testGenerateCode();
    await testGetStatus(genResult.code);
    await testJoinCode(genResult.code);
    await testDuplicateJoin(genResult.code);

    // 测试 5-6: WebSocket
    await testWebSocketSignaling();
    await testRelayMessage();

    // 测试 7: 错误处理
    await testErrorHandling();

    // 结果
    console.log('\n' + '='.repeat(50));
    console.log(`  测试结果: ✅ ${passed} 通过  ❌ ${failed} 失败`);
    console.log('='.repeat(50));

    if (failed > 0) process.exit(1);
  } catch (e) {
    console.error('\n💥 测试异常:', e);
    process.exit(1);
  }
}

main();
