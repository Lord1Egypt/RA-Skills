#!/usr/bin/env node
/**
 * Second Reality Video — 按量付费协议模拟器（mock service）
 *
 * 用途：在**没有**渲染引擎、**没有**支付宝账号的情况下，自测「402 Payment-Needed →
 * 付款凭证 → 重放同一请求 → 资源交付」的协议链路。
 *
 * 它**不是**渲染器：返回的 `world.mp4` 是占位字节，manifest 是模拟数据。
 * 真实影片只能由兼容的渲染服务端产出。
 *
 * 用法
 * ----
 *   node scripts/mock-service.mjs                # 监听 127.0.0.1:8788
 *   node scripts/mock-service.mjs --port 9000
 *
 * 配合开放客户端
 * ------------
 *   node scripts/second-reality-video-client.mjs probe \
 *     --api-base http://127.0.0.1:8788 --ticks 0-49 --state-dir .state --session-id demo
 *   node scripts/second-reality-video-client.mjs pay --state-dir .state --session-id demo
 *   node scripts/second-reality-video-client.mjs complete \
 *     --state-dir .state --session-id demo --payment-proof mock.<out_trade_no> --out-dir ./out
 */

import { createHash } from 'node:crypto';
import { createServer } from 'node:http';

const argv = process.argv.slice(2);
const portIndex = argv.indexOf('--port');
const PORT = portIndex >= 0 ? Number.parseInt(argv[portIndex + 1], 10) : 8788;
const HOST = '127.0.0.1';

const RESOURCE_ID = '/api/v1/render';
const SELLER_ID = 'mock-seller-2088';
const SELLER_APP_ID = 'mock-app-id';
const SERVICE_ID = 'api_mock_service_id';
const GOODS_NAME = '第二现实可复现视频渲染服务';
const AMOUNT = '0.01';

/** out_trade_no → 订单 */
const orders = new Map();

function base64url(value) {
  return Buffer.from(value, 'utf8').toString('base64url');
}

function buildBill(order) {
  // 沙箱联调不产生真实签名，字段结构与官方契约保持一致。
  const signSource = [
    `amount=${order.amount}`,
    `currency=${order.currency}`,
    `goods_name=${GOODS_NAME}`,
    `out_trade_no=${order.out_trade_no}`,
    `pay_before=${order.pay_before}`,
    `resource_id=${order.resource_id}`,
    `seller_id=${order.seller_id}`,
    `service_id=${order.service_id}`,
  ].join('&');
  return {
    protocol: {
      out_trade_no: order.out_trade_no,
      amount: order.amount,
      currency: order.currency,
      resource_id: order.resource_id,
      pay_before: order.pay_before,
      seller_signature: createHash('sha256').update(signSource).digest('base64'),
      seller_sign_type: 'RSA2',
      seller_unique_id: order.seller_id,
    },
    method: {
      seller_name: '测试商户',
      seller_id: order.seller_id,
      seller_app_id: SELLER_APP_ID,
      goods_name: GOODS_NAME,
      seller_unique_id_key: 'seller_id',
      service_id: order.service_id,
    },
  };
}

function fakeArtifacts(outTradeNo) {
  const mp4 = Buffer.from('MOCK-MP4-PLACEHOLDER: not a real film\n', 'utf8');
  const hashes = Buffer.from('# mock per-frame sha256 list (not real)\n', 'utf8');
  const manifest = Buffer.from(`${JSON.stringify({
    mock: true,
    note: 'simulated manifest - no rendering engine in this package',
    out_trade_no: outTradeNo,
    audit: { dimensions: 25, verdict: 'MOCK' },
  }, null, 2)}\n`, 'utf8');
  return [
    { name: 'world.mp4', content: mp4, url: `/api/v1/render/${outTradeNo}/artifacts/world.mp4` },
    { name: 'hashes.txt', content: hashes, url: `/api/v1/render/${outTradeNo}/artifacts/hashes.txt` },
    { name: 'manifest.json', content: manifest, url: `/api/v1/render/${outTradeNo}/artifacts/manifest.json` },
  ];
}

function send(res, status, payload, headers = {}) {
  const body = JSON.stringify(payload);
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(body),
    ...headers,
  });
  res.end(body);
}

function readBody(req) {
  return new Promise((resolvePromise) => {
    let data = '';
    req.on('data', (chunk) => {
      data += chunk;
      if (data.length > 1000000) req.destroy();
    });
    req.on('end', () => {
      try {
        resolvePromise(data ? JSON.parse(data) : {});
      } catch {
        resolvePromise({});
      }
    });
  });
}

const server = createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const path = url.pathname;

  if (req.method === 'GET' && path === '/health') {
    send(res, 200, { ok: true, service: 'second-reality-video-mock', billing_provider: 'mock' });
    return;
  }

  if (req.method === 'POST' && path === RESOURCE_ID) {
    const body = await readBody(req);
    const proof = String(req.headers['payment-proof'] || '').trim();

    if (!proof) {
      const outTradeNo = `ORDER_${Date.now()}_${Math.random().toString(16).slice(2, 14)}`;
      const order = {
        out_trade_no: outTradeNo,
        amount: AMOUNT,
        currency: 'CNY',
        resource_id: RESOURCE_ID,
        seller_id: SELLER_ID,
        service_id: SERVICE_ID,
        pay_before: new Date(Date.now() + 30 * 60 * 1000).toISOString(),
        status: 'PENDING_PAYMENT',
        fulfill_status: 'UNFULFILLED',
        artifacts: null,
      };
      orders.set(outTradeNo, order);
      const bill = buildBill(order);
      send(res, 402, {
        code: 'Payment-Needed',
        message: '需要支付',
        out_trade_no: outTradeNo,
        amount: order.amount,
        currency: order.currency,
        goods_name: GOODS_NAME,
        mock_proof_hint: `mock.${outTradeNo}`,
      }, { 'Payment-Needed': base64url(JSON.stringify(bill)) });
      return;
    }

    const outTradeNo = proof.startsWith('mock.') ? proof.slice(5) : '';
    const order = orders.get(outTradeNo);
    if (!order) {
      send(res, 402, { code: 'Payment-Needed', message: '需要支付', reason: 'order not found' });
      return;
    }

    if (!order.artifacts) {
      order.artifacts = fakeArtifacts(outTradeNo);
      order.fulfill_status = 'FULFILLED';
    }

    const content = {
      status: 'success',
      service_type: 'SECOND_REALITY_VIDEO_RENDER',
      resource_id: RESOURCE_ID,
      out_trade_no: outTradeNo,
      artifacts: order.artifacts.map((item) => ({
        name: item.name,
        size: item.content.length,
        sha256: createHash('sha256').update(item.content).digest('hex'),
        url: item.url,
      })),
      manifest: { mock: true },
    };
    const validation = base64url(JSON.stringify({
      trade_no: `MOCK_TRADE_${outTradeNo.slice(-12)}`,
      out_trade_no: outTradeNo,
      validated: true,
      resource_id: RESOURCE_ID,
    }));
    send(res, 200, {
      resource_id: RESOURCE_ID,
      content: JSON.stringify(content),
      trade_no: `MOCK_TRADE_${outTradeNo.slice(-12)}`,
      out_trade_no: outTradeNo,
      already_fulfilled: order.fulfill_status === 'FULFILLED' && order.artifacts.length > 0,
      fulfillment_confirmed: true,
    }, { 'Payment-Validation': validation });
    return;
  }

  const artifactMatch = path.match(/^\/api\/v1\/render\/([^/]+)\/artifacts\/(.+)$/);
  if (req.method === 'GET' && artifactMatch) {
    const order = orders.get(artifactMatch[1]);
    const item = order?.artifacts?.find((entry) => entry.name === artifactMatch[2]);
    if (!item) {
      send(res, 404, { error: 'artifact not found' });
      return;
    }
    res.writeHead(200, {
      'Content-Type': 'application/octet-stream',
      'Content-Length': item.content.length,
    });
    res.end(item.content);
    return;
  }

  send(res, 404, { error: 'not found', path });
});

server.listen(PORT, HOST, () => {
  console.log(`[mock-service] listening on http://${HOST}:${PORT}`);
  console.log('[mock-service] protocol simulator only - it does NOT render video and never charges money');
  console.log('[mock-service] Payment-Proof for any order: mock.<out_trade_no>');
});
