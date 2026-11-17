// background.js —— MV3 service worker
// 职责：
//   1) 监听工具栏图标点击，向当前标签页的 content script 发消息打开/关闭浮层
//   2) 处理面板发来的 GET_SELECTION：用 chrome.scripting.executeScript(allFrames)
//      直插每一帧读取 window.getSelection()，合并返回（微信读书等 iframe 阅读器也能抓到选区）
//   3) 心跳看门狗：用 chrome.alarms 周期性 ping 本地后端 /api/heartbeat。
//      后端在「托管模式」(WEBCHAT_MANAGED=1) 下靠此心跳续命——浏览器开着→心跳不断→后端存活；
//      浏览器关闭→本服务工作线程被回收、alarms 停止触发→心跳断→后端自行优雅退出。
//      如此一来后端生命周期与浏览器解耦，且无需任何浏览器进程名硬编码，跨内核通用。
const HEARTBEAT_URL = "http://localhost:3000/api/heartbeat";
const HEARTBEAT_ALARM = "webchat-heartbeat";

chrome.action.onClicked.addListener((tab) => {
  if (!tab || !tab.id) return;
  chrome.tabs.sendMessage(tab.id, { type: "TOGGLE_PANEL" }).catch(() => {
    /* 内容脚本未注入（如 chrome:// 页面）时静默失败 */
  });
});

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (!msg) return;

  if (msg.type === "TOGGLE_PANEL") {
    // 仅作转发占位；实际由 content script 处理（见上行 onClicked）
    return;
  }

  if (msg.type === "GET_SELECTION") {
    const tabId = sender.tab && sender.tab.id;
    if (!tabId) {
      sendResponse({ text: "" });
      return;
    }
    // 直插所有帧读取选区，绕开 postMessage 中继的脆弱性
    chrome.scripting
      .executeScript({
        target: { tabId, allFrames: true },
        func: () => {
          try {
            return (window.getSelection() ? window.getSelection().toString() : "").trim();
          } catch (_) {
            return "";
          }
        },
      })
      .then((results) => {
        const text = (results || [])
          .map((r) => (r && r.result) || "")
          .filter(Boolean)
          .join("\n")
          .trim();
        sendResponse({ text });
      })
      .catch(() => sendResponse({ text: "" }));
    return true; // 异步响应
  }
});

// ---------- 心跳看门狗 ----------
async function pingBackend() {
  try {
    await fetch(HEARTBEAT_URL, { method: "POST", cache: "no-store" });
  } catch (_) {
    // 后端没跑/已退出都忽略；托管模式下后端会在宽限后自退，非托管模式不受影响
  }
}

// 确保心跳闹钟存在（幂等，每次 SW 唤醒都调用也无妨）
function ensureHeartbeatAlarm() {
  chrome.alarms.get(HEARTBEAT_ALARM, (existing) => {
    if (!existing) {
      // periodInMinutes 最小约 1 分钟；后端宽限 2.5 分钟，足够覆盖节流
      chrome.alarms.create(HEARTBEAT_ALARM, { periodInMinutes: 1 });
    }
  });
}

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === HEARTBEAT_ALARM) pingBackend();
});

chrome.runtime.onInstalled.addListener(ensureHeartbeatAlarm);
chrome.runtime.onStartup.addListener(ensureHeartbeatAlarm);
// SW 每次唤醒也兜底确保一次心跳并补齐闹钟
ensureHeartbeatAlarm();
pingBackend();
