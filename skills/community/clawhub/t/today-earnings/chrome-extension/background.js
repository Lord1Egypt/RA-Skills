// background.js - Chrome Extension 后台 Service Worker (Manifest V3)
//
// 职责:
//   1. 连接 Native Host（com.today.earnings.host）并保持连接
//   2. 接收来自 Native Host 的采集请求（源头是 CLI）
//   3. 打开 Yahoo Finance 财报页面，等待加载，触发 content script 提取数据
//   4. 将结果返回给 Native Host（进而返回给 CLI）
//
// 消息协议（与 native host 之间）:
//   请求: { type: 'fetchEarnings', date: 'YYYY-MM-DD', _id: N }
//   响应: { ok: true, data: [...], _id: N } | { ok: false, error: {...}, _id: N }

const HOST_NAME = 'com.today.earnings.host';
const COMM_INITIAL_WAIT_MS = 3000;   // 页面打开后先等待 3 秒
const COMM_RETRY_INTERVAL_MS = 1000; // 通讯失败时每隔 1 秒重试
const COMM_MAX_RETRIES = 10;         // 最大重试次数

let nativePort = null;

// ─── Native Host 连接管理 ────────────────────────────────────────────────────

function connectToHost() {
  if (nativePort) return;
  try {
    nativePort = chrome.runtime.connectNative(HOST_NAME);
    nativePort.onMessage.addListener(handleHostMessage);
    nativePort.onDisconnect.addListener(() => {
      nativePort = null;
      // 断开后 3 秒重连（避免 host 还未启动时高频重试）
      setTimeout(connectToHost, 3000);
    });
  } catch (_err) {
    nativePort = null;
    setTimeout(connectToHost, 3000);
  }
}

// ─── 请求处理 ────────────────────────────────────────────────────────────────

async function handleHostMessage(message) {
  if (message.type !== 'fetchEarnings') return;

  const { date, _id } = message;
  const url = `https://finance.yahoo.com/calendar/earnings?day=${date}&offset=0&size=100`;
  let tabId = null;

  try {
    const tab = await chrome.tabs.create({ url, active: false });
    tabId = tab.id;

    // 等待 content script 可通讯后发送提取请求
    const response = await waitAndExtract(tabId, { type: 'extract', date });
    nativePort.postMessage({ ...response, _id });
  } catch (err) {
    if (nativePort) {
      nativePort.postMessage({
        ok: false,
        error: { code: 'FETCH_ERROR', message: err.message },
        _id,
      });
    }
  } finally {
    if (tabId != null) {
      chrome.tabs.remove(tabId).catch(() => {});
    }
  }
}

// ─── 工具函数 ────────────────────────────────────────────────────────────────

/**
 * 等待 tab 的 content script 可通讯后发送消息并返回响应。
 * 策略：先等 3 秒，然后尝试通讯；失败则每隔 1 秒重试，最多 10 次。
 * 这样可以兼容那些长时间加载资源、tabs.status 迟迟不变为 complete 的页面。
 */
async function waitAndExtract(tabId, message) {
  await sleep(COMM_INITIAL_WAIT_MS);
  let lastErr;
  for (let i = 0; i <= COMM_MAX_RETRIES; i++) {
    try {
      return await chrome.tabs.sendMessage(tabId, message);
    } catch (err) {
      lastErr = err;
      if (i < COMM_MAX_RETRIES) await sleep(COMM_RETRY_INTERVAL_MS);
    }
  }
  throw lastErr;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// ─── Service Worker 生命周期 ─────────────────────────────────────────────────

chrome.runtime.onInstalled.addListener(() => {
  // 使用 alarms 周期性唤醒 service worker，防止 MV3 被提前终止
  chrome.alarms.create('keepAlive', { periodInMinutes: 0.4 });
  connectToHost();
});

chrome.runtime.onStartup.addListener(() => {
  connectToHost();
});

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'keepAlive' && !nativePort) {
    connectToHost();
  }
});
