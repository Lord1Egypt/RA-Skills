// content.js - Yahoo Finance 财报页面 content script
// 依赖: parser.js（manifest 中声明在 content.js 之前加载）
//
// 响应 background 发来的消息:
//   请求: { type: 'extract', date: 'YYYY-MM-DD' }
//   响应: { ok: true, data: [...] } | { ok: false, error: { code, message } }

const SELECTOR =
  '#main-content-wrapper > section > section:nth-child(4) > div.table-container > table > tbody > tr';
const WAIT_INTERVAL_MS = 300;
const WAIT_TIMEOUT_MS = 10000;

// 轮询等待财报表格出现（Yahoo Finance 异步加载数据）
function waitForTable() {
  return new Promise((resolve) => {
    let elapsed = 0;
    const timer = setInterval(() => {
      if (document.querySelectorAll(SELECTOR).length > 0) {
        clearInterval(timer);
        resolve(true);
        return;
      }
      elapsed += WAIT_INTERVAL_MS;
      if (elapsed >= WAIT_TIMEOUT_MS) {
        clearInterval(timer);
        resolve(false);
      }
    }, WAIT_INTERVAL_MS);
  });
}

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message.type !== 'extract') return false;

  waitForTable()
    .then((found) => {
      if (!found) {
        sendResponse({
          ok: false,
          error: { code: 'PAGE_TIMEOUT', message: '等待 Yahoo Finance 财报表格超时（10s）' },
        });
        return;
      }
      // parseEarnings 由 parser.js 提供
      const data = parseEarnings(message.date); // eslint-disable-line no-undef
      sendResponse({ ok: true, data });
    })
    .catch((err) => {
      sendResponse({ ok: false, error: { code: 'PARSE_ERROR', message: err.message } });
    });

  return true; // 声明异步 sendResponse
});
