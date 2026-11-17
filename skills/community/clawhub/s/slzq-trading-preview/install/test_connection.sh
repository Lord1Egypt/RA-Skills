#!/usr/bin/env bash
set -euo pipefail

WITH_TRADE_TEST="false"
if [ "${1:-}" = "--with-trade-test" ]; then
  WITH_TRADE_TEST="true"
fi

export OPENCLAW_TEST_DOMAIN_ENV="SLZQ_OPENCLAW_DOMAIN"
export OPENCLAW_TEST_API_KEY_ENV="SLZQ_OPENCLAW_API_KEY"
export OPENCLAW_TEST_TRADING_ENV="SLZQ_OPENCLAW_ENV"
export OPENCLAW_TEST_WITH_TRADE="${WITH_TRADE_TEST}"

node <<'NODE'
import { readFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

const DEFAULT_DOMAIN = "https://slzqapi.sxslqhsh.com";
const domainEnv = process.env.OPENCLAW_TEST_DOMAIN_ENV;
const keyEnv = process.env.OPENCLAW_TEST_API_KEY_ENV;
const tradingEnvName = process.env.OPENCLAW_TEST_TRADING_ENV;
const domain = (process.env[domainEnv] || DEFAULT_DOMAIN).replace(/\/+$/, "");
// 与 MCP 一致：环境变量优先，其次是登录时落盘的凭据文件
const apiKey = process.env[keyEnv] || readPersistedApiKey();
const tradingEnv = (process.env[tradingEnvName] || "sim").toLowerCase();
const withTrade = process.env.OPENCLAW_TEST_WITH_TRADE === "true";

function fail(message, next) {
  console.error(`FAIL: ${message}`);
  console.error(`下一步：${next}`);
  process.exit(1);
}
function pass(message) {
  console.log(`PASS: ${message}`);
}
function readPersistedApiKey() {
  try {
    const raw = readFileSync(join(homedir(), ".slzq-trading", "credentials.json"), "utf8");
    const parsed = JSON.parse(raw);
    return typeof parsed.apiKey === "string" ? parsed.apiKey.trim() : "";
  } catch {
    return "";
  }
}
if (domain.includes("/mobile-api")) fail(`${domainEnv} 包含 /mobile-api`, "请改为仅 https:// + 主机名");

// apiBase 必须在下面的校验之前定义：缺少密钥时的提示里要给出可直接照抄的登录接口地址
const apiBase = `${domain}/mobile-api/open/v1`;

if (!apiKey)
  fail(
    `缺少 ${keyEnv}`,
    "两种取钥方式任选其一。方式 A（会话内登录领取，只需手机号 + 验证码；账号已有模拟盘密钥会原样返回）：" +
      "已注册 MCP 用 slzq_open_v1_auth_agreement → slzq_open_v1_auth_send_code → slzq_open_v1_auth_login；" +
      `没有 MCP 就直接调三个免鉴权接口 GET ${apiBase}/auth/agreement、POST ${apiBase}/auth/sms/send、POST ${apiBase}/auth/login。` +
      `方式 B（要用实盘密钥时只能走这条）：App「我的 → 期货辅助交易」一键复制已有密钥，配置到 ${keyEnv}。`
  );
if (!["sim", "live"].includes(tradingEnv)) fail(`${tradingEnvName} 非法`, "请设置为 sim 或 live");

async function request(path, { auth = true, method = "GET", body } = {}) {
  const headers = {};
  if (auth) {
    headers.Authorization = `Bearer ${apiKey}`;
    headers["X-Trading-Env"] = tradingEnv;
  }
  if (body !== undefined) headers["Content-Type"] = "application/json";
  const res = await fetch(`${apiBase}${path}`, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  let data;
  try { data = text ? JSON.parse(text) : null; } catch { data = { raw: text }; }
  if (!res.ok) fail(`${path} HTTP ${res.status}`, "请检查域名是否可达");
  if (data && data.success === false) fail(`${path} 返回失败：${data.errorInfo || data.errorCode}`, "请按 errorInfo 的下一步处理后重试");
  return data;
}
function pickContract(payload) {
  const data = payload && payload.data;
  const list = Array.isArray(data) ? data : (data && Array.isArray(data.list) ? data.list : []);
  for (const item of list) {
    const code = item.contractCode || item.mainContractCode || item.instrumentId || item.code;
    if (typeof code === "string" && /^[A-Za-z]+\d+$/.test(code)) return code;
  }
  return null;
}

(async () => {
  await request("/health", { auth: false });
  pass("health");
  await request("/skill/version", { auth: false });
  pass("skill/version");
  const me = await request("/me");
  pass(`me tradingEnv=${me?.data?.tradingEnv || tradingEnv} scope=${me?.data?.scope ?? "?"}（${me?.data?.scopeName ?? "未知档位"}）`);
  if (tradingEnv === "live" && me?.data?.canTradeLive === false) {
    fail("当前密钥无实盘权限，但交易环境设为 live", "改用 sim，或按 App 内实盘开通流程签发实盘密钥后重试");
  }
  let hot = await request("/catalog/hot");
  let contract = pickContract(hot);
  if (!contract) {
    const goods = await request("/catalog/goods?page=1&pageSize=20");
    contract = pickContract(goods);
  }
  if (!contract) fail("未能从 catalog/hot 或 catalog/goods 获取有效合约", "请检查目录接口数据，或稍后重试");
  pass(`动态选择合约 ${contract}`);
  const snapshot = await request(`/market/snapshot?instrumentId=${encodeURIComponent(contract)}`);
  if (snapshot?.data && (snapshot.data.volumeMultiple !== undefined || snapshot.data.instrumentId || snapshot.data.contractCode)) {
    pass("market/snapshot");
  } else {
    await request(`/catalog/contract?contractCode=${encodeURIComponent(contract)}`);
    pass("market/snapshot 暂无缓存，catalog/contract 已验证合约存在");
  }
  await request("/positions");
  pass("positions");
  if (withTrade) {
    if (tradingEnv !== "sim") fail("--with-trade-test 仅允许 sim", "请将交易环境改为 sim 后再执行交易链路自检");
    console.log("INFO: 交易链路自检已显式开启，但下单参数仍需结合当前行情和风控规则；本脚本默认不自动下单。");
  }
  console.log("连接自检完成：只读链路通过。");
})().catch((err) => fail(err?.message || String(err), "请根据错误信息修正配置后重试"));
NODE
