#!/usr/bin/env node
'use strict';

const { Memory } = require('./context/memory');
const { SkillOrchestrator } = require('./services');
const config = require('./config');
const constants = require('./constants');

const VERSION = '1.0.9';

function showHelp() {
  console.log(`
ZL-ClawPay Node.js v${VERSION} — SM2/SM3/SM4 加密支付技能

用法:
  node scripts/skill.js call -interfaceId=<ID> -method=<METHOD> -endpoint=<ENDPOINT> [--<API_PARAM>=<VALUE> ...]
  node scripts/skill.js help

指令集参数 (-前缀):
  -interfaceId    接口ID (C00003, C00005, C00007, C00009, C00011, L00001, L00002)
  -method         HTTP 方法 (POST/local)
  -endpoint       API 端点路径

接口参数 (--前缀):
  --apiKey        API Key (64 hex chars, SM2 私钥) — 仅 C00003 需要
  --subWalletName 子钱包名称 — C00003/C00011 需要
  --subWalletId   子钱包ID — 仅 C00003 需要
  --amount        支付金额（分）
  --merApiKey     商户 API Key
  --seqId         交易流水号
  --orderDetail   订单详情（商品名称）
  --orgSeqId      原始流水号
  --startDate     开始日期 (YYYYMMDD)
  --endDate       结束日期 (YYYYMMDD)

注意: 非 C00003 接口的 apiKey/subWalletId 自动从本地 state.json 中获取，无需传参。

示例:
  node scripts/skill.js call -interfaceId=L00001 -method=local
  node scripts/skill.js call -interfaceId=L00002 -method=local
  node scripts/skill.js call -interfaceId=C00003 -method=POST -endpoint=/post/claw/bind-sub-wallet --apiKey=<64位hex密钥> --subWalletName=<子钱包名称> --subWalletId=<32位hex子钱包ID>
  node scripts/skill.js call -interfaceId=C00011 -method=POST -endpoint=/post/pay-claw/unbind-sub-wallet --subWalletName=<子钱包名称>
  node scripts/skill.js call -interfaceId=C00009 -method=POST -endpoint=/post/pay-claw/payment --amount=100 --merApiKey=<商户apiKey> --seqId=<流水号>

安全提示:
  - 请在 APP 中更改子钱包默认支付限额以提高额度
  - 商户 apiKey 由平台审核后发放，只有审核通过的商户才能收款
  - apiKey 和 subWalletId 加密存储在本地 ~/.zl-claw-pay/state.json 中
`);
}

function parseArgs(argv) {
  const cli = {};
  const body = {};

  for (let i = 3; i < argv.length; i++) {
    const arg = argv[i];
    const eqIdx = arg.indexOf('=');

    if (arg.startsWith('--')) {
      const key = arg.slice(2, eqIdx > 0 ? eqIdx : arg.length);
      const value = eqIdx > 0 ? arg.slice(eqIdx + 1) : 'true';
      body[key] = value;
    } else if (arg.startsWith('-')) {
      const key = arg.slice(1, eqIdx > 0 ? eqIdx : arg.length);
      const value = eqIdx > 0 ? arg.slice(eqIdx + 1) : 'true';
      cli[key] = value;
    }
  }

  return { cli, body };
}

function output(result) {
  console.log(JSON.stringify(result, null, 2));
}

const ROUTES = {
  local: {
    L00001: 'queryWallet',
    L00002: 'unbindWallet',
  },
  post: {
    C00003: 'bindSubWallet',
    C00005: 'queryOrder',
    C00007: 'queryTransactions',
    C00009: 'initiatePayment',
    C00011: 'revokeBinding',
  },
};

function checkEnvironment() {
  const errors = [];

  const nodeVersion = process.versions.node;
  const majorVersion = parseInt(nodeVersion.split('.')[0], 10);
  if (majorVersion < constants.REQUIRED_NODE_VERSION) {
    errors.push(
      `Node.js version ${nodeVersion} is too old, requires >= ${constants.REQUIRED_NODE_VERSION}.0.0`
    );
  }

  const requiredModules = ['axios', 'dotenv', 'sm-crypto'];
  for (const mod of requiredModules) {
    try {
      require.resolve(mod);
    } catch (_) {
      errors.push(`Missing dependency: ${mod}. See references/dependency-guide.md for installation instructions.`);
    }
  }

  const fs = require('fs');
  const path = require('path');
  const configEnvPath = path.join(__dirname, '..', 'config', '.env');
  if (!fs.existsSync(configEnvPath)) {
    errors.push(
      `Platform config file not found: config/.env\n` +
      `  This file contains API gateway URL and server public key (not user credentials).\n` +
      `  Fix: Copy config/.env.example to config/.env, or re-package with pack-skill.ps1.`
    );
  }

  if (errors.length > 0) {
    throw new Error(`Environment check failed:\n  - ${errors.join('\n  - ')}`);
  }
}

function validateStrategies() {
  const memory = new Memory();
  const orchestrator = new SkillOrchestrator(memory);
  const errors = [];

  for (const [type, routes] of Object.entries(ROUTES)) {
    for (const [interfaceId, methodName] of Object.entries(routes)) {
      if (typeof orchestrator[methodName] !== 'function') {
        errors.push(`Interface ${interfaceId}: method '${methodName}' not found on SkillOrchestrator`);
      }
    }
  }

  if (errors.length > 0) {
    throw new Error(`Strategy validation failed:\n  - ${errors.join('\n  - ')}`);
  }
}

function validateEnvWhitelist() {
  const whitelist = constants.ENV_WHITELIST;
  const whitelistSet = new Set(whitelist);

  for (const key of Object.keys(process.env)) {
    if (key.startsWith('ZL_CLAW_PAY_') && !whitelistSet.has(key)) {
      throw new Error(
        `Unknown environment variable: ${key}. ` +
        `Only whitelisted variables are allowed: ${whitelist.join(', ')}`
      );
    }
  }
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === 'help' || command === '--help' || command === '-h') {
    showHelp();
    process.exit(0);
  }

  if (command === 'version' || command === '--version' || command === '-v') {
    console.log(VERSION);
    process.exit(0);
  }

  if (command !== 'call') {
    console.error(`Unknown command: ${command}`);
    showHelp();
    process.exit(1);
  }

  try {
    checkEnvironment();
    config.validate();
    validateStrategies();
    validateEnvWhitelist();
  } catch (err) {
    console.error('Pre-flight check failed:', err.message);
    process.exit(1);
  }

  const { cli, body } = parseArgs(process.argv);
  const isLocal = cli.method === 'local';

  if (!cli.interfaceId || !cli.method || (!isLocal && !cli.endpoint)) {
    console.error(isLocal
      ? 'Error: -interfaceId, -method are required'
      : 'Error: -interfaceId, -method, -endpoint are required');
    showHelp();
    process.exit(1);
  }

  try {
    const memory = new Memory();
    const orchestrator = new SkillOrchestrator(memory);

    const routeMap = isLocal ? ROUTES.local : ROUTES.post;
    const methodName = routeMap[cli.interfaceId];

    if (!methodName) {
      throw new Error(`Unknown ${isLocal ? 'local' : ''} interfaceId: ${cli.interfaceId}`);
    }

    const result = await orchestrator[methodName](body);
    output(result);
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

main();
