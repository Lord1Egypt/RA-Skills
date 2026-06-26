#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const FEISHU_BASE_URL = 'https://open.feishu.cn';
const CONFIG_PATH = '/home/SENSETIME/zhangjiazhao/.openclaw/workspace/skills/beijing-signed-price-tracker/projects.json';
const TARGET_JOB_ID = '407511f7-5f9f-4a1e-aee9-c2e0764fb5e4';
const TARGET_JOB_NAME = 'beijing-signed-price-tracker-hourly';
const RUNS_PATH = '/home/SENSETIME/zhangjiazhao/.openclaw/cron/runs/407511f7-5f9f-4a1e-aee9-c2e0764fb5e4.jsonl';
const TZ = 'Asia/Shanghai';

function formatShanghaiDateTime(ms) {
  if (!Number.isFinite(ms)) return '';
  const parts = new Intl.DateTimeFormat('en-CA', {
    timeZone: TZ,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  }).formatToParts(new Date(ms));
  const map = Object.fromEntries(parts.filter(part => part.type !== 'literal').map(part => [part.type, part.value]));
  return `${map.year}-${map.month}-${map.day} ${map.hour}:${map.minute}:${map.second}`;
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function readJsonLines(filePath) {
  if (!fs.existsSync(filePath)) return [];
  return fs.readFileSync(filePath, 'utf8')
    .split(/\r?\n/)
    .map(line => line.trim())
    .filter(Boolean)
    .map(line => JSON.parse(line));
}

function getLatestFinishedRun(entries) {
  return entries
    .filter(entry => entry?.action === 'finished')
    .sort((a, b) => Number(b?.runAtMs || b?.ts || 0) - Number(a?.runAtMs || a?.ts || 0))[0] || null;
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  const text = await response.text();
  let json;
  try {
    json = text ? JSON.parse(text) : {};
  } catch {
    json = { raw: text };
  }
  if (!response.ok || json?.code) {
    throw new Error(json?.msg || json?.message || `HTTP ${response.status}`);
  }
  return json;
}

async function getFeishuAccessToken(appId, appSecret) {
  const json = await fetchJson(`${FEISHU_BASE_URL}/open-apis/auth/v3/tenant_access_token/internal`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
    body: JSON.stringify({ app_id: appId, app_secret: appSecret })
  });
  return json.tenant_access_token;
}

async function sendFeishuTextMessage(accessToken, receiveId, text) {
  return fetchJson(`${FEISHU_BASE_URL}/open-apis/im/v1/messages?receive_id_type=open_id`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${accessToken}`,
      'Content-Type': 'application/json; charset=utf-8'
    },
    body: JSON.stringify({
      receive_id: receiveId,
      msg_type: 'text',
      content: JSON.stringify({ text })
    })
  });
}

function buildStatusText(latestRun) {
  const time = formatShanghaiDateTime(Number(latestRun?.runAtMs || latestRun?.ts || 0));
  const status = String(latestRun?.status || 'unknown');
  const detail = String(latestRun?.error || latestRun?.summary || '无详细信息');
  const title = status.toLowerCase() === 'ok'
    ? '北京签约跟踪最新状态'
    : '北京签约跟踪执行告警';
  return [
    title,
    `最近一次执行时间：${time}`,
    `状态：${status}`,
    `详情：${detail}`
  ].join('\n');
}

async function main() {
  const config = readJson(CONFIG_PATH);
  const feishu = config?.feishu || {};
  if (!feishu.appId || !feishu.appSecret || !feishu.notifyUserOpenId) {
    throw new Error('projects.json 缺少飞书通知所需配置（appId/appSecret/notifyUserOpenId）');
  }

  const entries = readJsonLines(RUNS_PATH);
  const latestRun = getLatestFinishedRun(entries);

  if (!latestRun) {
    console.log(JSON.stringify({ ok: true, notified: false, reason: 'no-finished-runs', targetJobId: TARGET_JOB_ID, targetJobName: TARGET_JOB_NAME }));
    return;
  }

  const accessToken = await getFeishuAccessToken(feishu.appId, feishu.appSecret);
  const text = buildStatusText(latestRun);
  await sendFeishuTextMessage(accessToken, feishu.notifyUserOpenId, text);
  console.log(JSON.stringify({ ok: true, notified: true, latestRunAt: latestRun.runAtMs || latestRun.ts || null, latestStatus: latestRun.status || 'unknown', targetJobId: TARGET_JOB_ID, targetJobName: TARGET_JOB_NAME }));
}

main().catch(error => {
  console.error(error?.stack || String(error));
  process.exitCode = 1;
});
