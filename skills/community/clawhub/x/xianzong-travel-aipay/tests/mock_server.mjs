#!/usr/bin/env node
/**
 * 本地模拟资源服务（仅用于离线测试脚本，从不访问真实服务）。
 *
 * 行为与资源端点一致：
 *   POST /aipay/travel_consultant
 *     - 无 Payment-Proof            -> 402 + Payment-Needed（假账单）
 *     - Payment-Proof = invalid     -> 402（凭证无效，重新出账）
 *     - Payment-Proof = pending     -> 409 + Payment-Validation + Retry-After
 *     - Payment-Proof = error       -> 500
 *     - Payment-Proof = bizfail     -> 200 但业务层 resp_code=400
 *     - 其他值                      -> 200 + Payment-Validation + 资源
 *   GET /_state -> 记录到的请求（供测试断言「同订单复用」「不重复付款」）
 *
 * 启动：node tests/mock_server.mjs --port 8799
 */

import { createServer } from 'node:http';

const RESOURCE_ID = '/aipay/travel_consultant';
const state = { quoteCount: 0, deliverCount: 0, seenBodies: [], seenProofs: [] };

function b64url(payload) {
  return Buffer.from(JSON.stringify(payload), 'utf8').toString('base64url');
}

function okResult() {
  return {
    resp_code: 200,
    resp_message: 'SUCCESS',
    data: {
      content: '# 杭州三日亲子游\n\n第一天：西湖 → 灵隐\n第二天：宋城\n第三天：返程',
      ref_travel_infos: [{ title: '西湖', summary: '亲子友好', content: '...', guide: '...' }],
      model_name: 'deepseek',
      travel_query_info: { country_code: 'CN' },
      travel_destination: '杭州',
      pdf_oss_file_name: 'travel/demo.pdf',
      pdf_oss_file_url: 'https://example.invalid/demo.pdf?Expires=1&Signature=x',
    },
  };
}

function send(res, status, body, headers = {}) {
  const text = typeof body === 'string' ? body : JSON.stringify(body);
  res.writeHead(status, { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(text), ...headers });
  res.end(text);
}

const server = createServer((req, res) => {
  if (req.method === 'GET' && req.url === '/_state') {
    send(res, 200, state);
    return;
  }

  if (req.method !== 'POST' || req.url !== RESOURCE_ID) {
    send(res, 404, { code: 'NOT_FOUND' });
    return;
  }

  let raw = '';
  req.on('data', (chunk) => {
    raw += chunk.toString();
  });
  req.on('end', () => {
    let body;
    try {
      body = JSON.parse(raw || '{}');
    } catch {
      send(res, 400, { code: 'INVALID_JSON', message: 'body 不是 JSON' });
      return;
    }
    state.seenBodies.push(body);

    const proof = req.headers['payment-proof'];

    if (!proof) {
      state.quoteCount += 1;
      const outTradeNo = `AIPAY_MOCK_${String(state.quoteCount).padStart(3, '0')}`;
      const bill = { protocol: { out_trade_no: outTradeNo, amount: '0.99', currency: 'CNY' }, method: { goods_name: '仙踪问道_旅行咨询' } };
      send(
        res,
        402,
        {
          code: 'Payment-Needed',
          message: '需要支付',
          out_trade_no: outTradeNo,
          amount: '0.99',
          currency: 'CNY',
          goods_name: '仙踪问道_旅行咨询',
        },
        { 'Payment-Needed': b64url(bill) },
      );
      return;
    }

    state.deliverCount += 1;
    state.seenProofs.push(proof);

    switch (proof) {
      case 'invalid':
        send(res, 402, { code: 'Payment-Needed', message: '凭证无效，需重新支付' });
        return;
      case 'pending':
        send(
          res,
          409,
          { code: 'FULFILLMENT_IN_PROGRESS', message: '资源正在生成中，请勿重复支付', out_trade_no: 'AIPAY_MOCK_001', trade_no: 'TRADE_MOCK' },
          { 'Retry-After': '30', 'Payment-Validation': b64url({ validated: true }) },
        );
        return;
      case 'error':
        send(res, 500, { code: 'VERIFY_FAILED', message: '支付凭证验证失败' });
        return;
      case 'bizfail':
        send(
          res,
          200,
          {
            resource_id: RESOURCE_ID,
            content: JSON.stringify({ resp_code: 400, resp_message: '旅行咨询失败：召回结果为空' }),
            trade_no: 'TRADE_MOCK',
            out_trade_no: 'AIPAY_MOCK_001',
            already_fulfilled: false,
            fulfillment_confirmed: true,
          },
          { 'Payment-Validation': b64url({ validated: true }) },
        );
        return;
      default:
        send(
          res,
          200,
          {
            resource_id: RESOURCE_ID,
            content: JSON.stringify(okResult()),
            trade_no: 'TRADE_MOCK',
            out_trade_no: 'AIPAY_MOCK_001',
            already_fulfilled: state.deliverCount > 1,
            fulfillment_confirmed: true,
          },
          { 'Payment-Validation': b64url({ validated: true }) },
        );
    }
  });
});

const portArg = process.argv.indexOf('--port');
const port = portArg > -1 ? Number(process.argv[portArg + 1]) : 8799;

server.listen(port, '127.0.0.1', () => {
  process.stdout.write(`mock server listening on http://127.0.0.1:${port}${RESOURCE_ID}\n`);
});

for (const signal of ['SIGTERM', 'SIGINT']) {
  process.on(signal, () => server.close(() => process.exit(0)));
}
