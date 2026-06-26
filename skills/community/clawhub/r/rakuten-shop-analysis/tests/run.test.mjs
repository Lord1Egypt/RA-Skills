import test from 'node:test';
import assert from 'node:assert/strict';

import {
  runRakutenShopAnalysisSkillCli,
} from '../scripts/run.mjs';

function createStreamCollector() {
  const chunks = [];

  return {
    write(chunk) {
      chunks.push(String(chunk));
    },
    toString() {
      return chunks.join('');
    },
  };
}

test('runRakutenShopAnalysisSkillCli returns usage when shop input is missing', async () => {
  const stdout = createStreamCollector();
  const stderr = createStreamCollector();

  const result = await runRakutenShopAnalysisSkillCli({
    argv: [],
    stdout,
    stderr,
  });

  assert.equal(result.exitCode, 1);
  assert.match(stderr.toString(), /Usage: node .*run\.mjs <shopInput>/);
  assert.equal(stdout.toString(), '');
});

test('runRakutenShopAnalysisSkillCli starts job, polls, and prints compact payload', async () => {
  const stdout = createStreamCollector();
  const stderr = createStreamCollector();
  const requests = [];

  const responseQueue = [
    {
      status: 202,
      json: async () => ({
        jobId: 'job-1',
        status: 'running',
        shopCode: 'vacchetta-topkapi',
      }),
    },
    {
      status: 200,
      json: async () => ({
        jobId: 'job-1',
        status: 'completed',
        shopCode: 'vacchetta-topkapi',
      }),
    },
    {
      status: 200,
      json: async () => ({
        shop: {
          shopCode: 'vacchetta-topkapi',
          catalogSize: 253,
        },
        buckets: [
          {
            bucketId: 'top_reviewed',
            available: true,
            itemCount: 20,
          },
          {
            bucketId: 'ranking_hits',
            available: false,
            itemCount: 0,
          },
        ],
        capabilities: {
          degradedCapabilities: [
            {
              reasonCode: 'tag_request_limit',
            },
          ],
        },
      }),
    },
    {
      status: 200,
      json: async () => ({
        bucketId: 'top_reviewed',
        itemCount: 1,
        items: [
          {
            itemCode: 'vacchetta-topkapi:demo',
          },
        ],
      }),
    },
  ];

  const result = await runRakutenShopAnalysisSkillCli({
    argv: ['https://www.rakuten.co.jp/vacchetta-topkapi/'],
    env: {},
    stdout,
    stderr,
    fetchImpl: async (url, options = {}) => {
      requests.push({
        url,
        options,
      });
      const response = responseQueue.shift();
      if (!response) {
        throw new Error(`Unexpected request: ${url}`);
      }
      return response;
    },
    sleepImpl: async () => {},
  });

  assert.equal(result.exitCode, 0);
  assert.equal(requests.length, 4);
  assert.equal(requests[0].url, 'https://rakuten.845817074.xyz/skills/rakuten-shop-analysis/jobs');
  assert.equal(requests[3].url, 'https://rakuten.845817074.xyz/skills/rakuten-shop-analysis/shops/vacchetta-topkapi/buckets/top_reviewed');
  assert.match(stdout.toString(), /"shopCode": "vacchetta-topkapi"/);
  assert.match(stdout.toString(), /"top_reviewed"/);
  assert.match(stdout.toString(), /"tag_request_limit"/);
  assert.doesNotMatch(stdout.toString(), /apiBaseUrl/);
  assert.doesNotMatch(stdout.toString(), /rakuten\.845817074\.xyz/);
  assert.equal(stderr.toString(), '');
});

test('runRakutenShopAnalysisSkillCli retries on rate limit responses', async () => {
  const stdout = createStreamCollector();
  const stderr = createStreamCollector();
  const sleepCalls = [];
  const requests = [];

  const responseQueue = [
    {
      status: 202,
      headers: {
        get() {
          return null;
        },
      },
      json: async () => ({
        jobId: 'job-1',
        status: 'running',
        shopCode: 'retry-shop',
      }),
    },
    {
      status: 200,
      headers: {
        get() {
          return null;
        },
      },
      json: async () => ({
        jobId: 'job-1',
        status: 'completed',
        shopCode: 'retry-shop',
      }),
    },
    {
      status: 429,
      headers: {
        get(name) {
          return name === 'retry-after' ? '2' : null;
        },
      },
      json: async () => ({
        error: 'Rate limit exceeded',
      }),
    },
    {
      status: 200,
      headers: {
        get() {
          return null;
        },
      },
      json: async () => ({
        shop: {
          shopCode: 'retry-shop',
          catalogSize: 10,
        },
        buckets: [
          {
            bucketId: 'top_reviewed',
            available: true,
            itemCount: 1,
          },
        ],
        capabilities: {
          degradedCapabilities: [],
        },
      }),
    },
    {
      status: 200,
      headers: {
        get() {
          return null;
        },
      },
      json: async () => ({
        bucketId: 'top_reviewed',
        itemCount: 1,
        items: [
          {
            itemCode: 'retry-shop:demo',
          },
        ],
      }),
    },
  ];

  const result = await runRakutenShopAnalysisSkillCli({
    argv: ['retry-shop'],
    stdout,
    stderr,
    fetchImpl: async (url, options = {}) => {
      requests.push({
        url,
        options,
      });
      const response = responseQueue.shift();
      if (!response) {
        throw new Error(`Unexpected request: ${url}`);
      }
      return response;
    },
    sleepImpl: async ms => {
      sleepCalls.push(ms);
    },
  });

  assert.equal(result.exitCode, 0);
  assert.equal(sleepCalls[0], 2000);
  assert.equal(requests[2].url, 'https://rakuten.845817074.xyz/skills/rakuten-shop-analysis/shops/retry-shop/summary');
  assert.equal(requests[3].url, 'https://rakuten.845817074.xyz/skills/rakuten-shop-analysis/shops/retry-shop/summary');
  assert.match(stdout.toString(), /"retry-shop"/);
  assert.equal(stderr.toString(), '');
});
