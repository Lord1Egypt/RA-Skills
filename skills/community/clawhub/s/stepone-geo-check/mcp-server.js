#!/usr/bin/env node
'use strict';

/**
 * Zero-Dependency Stdio MCP Server for StepOneAI GEO Check
 * Exposes tool: `check_website_geo` for Cursor, Claude Desktop, OpenClaw & Tencent WorkBuddy
 */

const readline = require('readline');
const { runGeoCheck, ENGINE_VERSION } = require('./lib/engine');

const SERVER_INFO = {
  name: 'stepone-geo-check',
  version: ENGINE_VERSION
};

const TOOLS = [
  {
    name: 'check_website_geo',
    description: '对任意公开企业官网执行免费、纯代码的 6 维度 28 项 GEO 与 AI 搜索可读性真实检测（覆盖豆包 Bytespider、百度、夸克千问、DeepSeek、ChatGPT、Claude、Perplexity、Bing、Google 爬虫放行，以及 /llms.txt、SSR 无 JS 可读性、Schema JSON-LD 与原生 HTML 对比表），返回评分、实测证据与定制修复代码。',
    inputSchema: {
      type: 'object',
      properties: {
        url: {
          type: 'string',
          description: '要体检的公开企业官网网址，例如 https://www.steponeai.com'
        },
        include_snippets: {
          type: 'boolean',
          description: '是否附带定制生成的 llms.txt / robots.txt / JSON-LD 修复代码，默认 true'
        }
      },
      required: ['url']
    }
  }
];

function send(msg) {
  process.stdout.write(JSON.stringify(msg) + '\n');
}

async function handleMessage(req) {
  const { id, method, params } = req || {};
  if (method === 'initialize') {
    return send({
      jsonrpc: '2.0',
      id,
      result: {
        protocolVersion: '2024-11-05',
        capabilities: { tools: {} },
        serverInfo: SERVER_INFO
      }
    });
  }
  if (method === 'notifications/initialized') return;

  if (method === 'tools/list') {
    return send({ jsonrpc: '2.0', id, result: { tools: TOOLS } });
  }

  if (method === 'tools/call') {
    const name = params && params.name;
    const args = (params && params.arguments) || {};
    if (name !== 'check_website_geo') {
      return send({ jsonrpc: '2.0', id, error: { code: -32601, message: `Unknown tool: ${name}` } });
    }
    try {
      const report = await runGeoCheck(args.url);
      if (args.include_snippets === false) delete report.snippets;
      return send({
        jsonrpc: '2.0',
        id,
        result: {
          content: [{ type: 'text', text: JSON.stringify(report, null, 2) }]
        }
      });
    } catch (err) {
      return send({
        jsonrpc: '2.0',
        id,
        result: {
          isError: true,
          content: [{ type: 'text', text: `GEO Check Error: ${err.message}` }]
        }
      });
    }
  }

  if (id !== undefined) {
    send({ jsonrpc: '2.0', id, error: { code: -32601, message: `Method not found: ${method}` } });
  }
}

const rl = readline.createInterface({ input: process.stdin, terminal: false });
rl.on('line', (line) => {
  const trimmed = line.trim();
  if (!trimmed) return;
  try {
    handleMessage(JSON.parse(trimmed));
  } catch (_) {}
});
