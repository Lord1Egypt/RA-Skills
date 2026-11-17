#!/usr/bin/env node
/** 检测站斧 check.html 插件页是否可进入业务自动化。 */
import { ensureDeps } from "./ensure_deps.mjs";
// connectOverCDP 只需 playwright 包，不必下载本地 Chromium
ensureDeps();

const { chromium } = await import("playwright");
const { ensureHeadedMode } = await import("./headed_mode.mjs");
const { sleep } = await import("./zhanfu_http.mjs");

const CUSTOMER_FAIL_MSG = "没检测成功无法进行自动化";
const DEFAULT_TIMEOUT_SEC = 15;
const POLL_INTERVAL_SEC = 1.0;
const KNOWN_CHECKS = ["设备安全检测", "环境安全检测", "线路优化检测"];

function findCheckPage(context) {
  for (const page of context.pages()) {
    if (page.url().includes("check.html")) return page;
  }
  const pages = context.pages();
  return pages.length ? pages[0] : null;
}

async function isOpenMallButtonEnabled(page) {
  try {
    // Node Playwright 必须传 Function；传字符串不会执行函数体（迁移回归）
    return await page.evaluate(() => {
      const btn =
        document.querySelector(".openMallOpenBtn") ||
        [...document.querySelectorAll("button")].find((b) =>
          (b.textContent || "").includes("打开店铺")
        );
      if (!btn) return null;
      const disabled =
        btn.disabled ||
        btn.getAttribute("aria-disabled") === "true" ||
        btn.classList.contains("is-disabled");
      return !disabled;
    });
  } catch {
    return null;
  }
}

async function evaluateDetectionPassed(context, page) {
  const tabCount = context.pages().length;
  const buttonEnabled = await isOpenMallButtonEnabled(page);
  const passed = tabCount >= 2 || buttonEnabled === true;
  let passReason = null;
  if (tabCount >= 2) passReason = "tabs>=2";
  else if (buttonEnabled === true) passReason = "open_mall_button_enabled";
  return {
    tab_count: tabCount,
    open_mall_button_enabled: buttonEnabled,
    device_security_success: passed,
    pass_reason: passReason,
    verdict: passed ? "success" : "in_progress",
  };
}

function parseSecurityStatus(text) {
  const lines = text
    .split(/\r?\n/)
    .map((ln) => ln.trim())
    .filter(Boolean);
  const checks = Object.fromEntries(KNOWN_CHECKS.map((n) => [n, null]));
  let current = null;
  for (const ln of lines) {
    if (KNOWN_CHECKS.includes(ln)) {
      current = ln;
      continue;
    }
    if ((ln === "成功" || ln === "失败") && current) {
      checks[current] = ln;
      current = null;
    }
  }
  return {
    device_security_check: checks["设备安全检测"],
    environment_check: checks["环境安全检测"],
    line_check: checks["线路优化检测"],
    safe_to_login: text.includes("当前环境检测安全"),
    all_checks: checks,
    related_lines: lines.filter((ln) =>
      ["设备安全", "环境安全", "线路优化", "检测安全", "检测失败"].some((k) => ln.includes(k))
    ),
    body_preview: text.slice(0, 500),
  };
}

async function readCheckStatus(context, page) {
  const info = await evaluateDetectionPassed(context, page);
  try {
    const text = await page.innerText("body", { timeout: 5000 });
    Object.assign(info, parseSecurityStatus(text));
  } catch (exc) {
    info.read_error = String(exc.message || exc);
  }
  return info;
}

async function waitDeviceSecuritySuccess(context, page, timeoutSec = DEFAULT_TIMEOUT_SEC) {
  const deadline = Date.now() + timeoutSec * 1000;
  let last = { verdict: "in_progress", device_security_success: false };
  let current = page;
  while (Date.now() < deadline) {
    try {
      current = findCheckPage(context) || current;
      last = await readCheckStatus(context, current);
      if (last.device_security_success) {
        last.verdict = "success";
        last.waited_sec = Math.round((timeoutSec * 1000 - (deadline - Date.now())) / 100) / 10;
        return last;
      }
    } catch (exc) {
      last.read_error = String(exc.message || exc);
    }
    sleep(POLL_INTERVAL_SEC * 1000);
  }
  current = findCheckPage(context) || current;
  last = await readCheckStatus(context, current);
  if (!last.device_security_success) {
    last.verdict = "timeout";
    last.device_security_success = false;
    last.customer_message = CUSTOMER_FAIL_MSG;
  }
  last.waited_sec = timeoutSec;
  return last;
}

async function inspect(webdriverPort, wait = false, timeoutSec = DEFAULT_TIMEOUT_SEC) {
  ensureHeadedMode();
  const browser = await chromium.connectOverCDP(`http://127.0.0.1:${webdriverPort}`);
  try {
    const context = browser.contexts()[0];
    const page = findCheckPage(context);
    if (!page) throw new Error("未找到任何标签页");
    const info = { url: page.url(), title: await page.title() };
    if (wait) Object.assign(info, await waitDeviceSecuritySuccess(context, page, timeoutSec));
    else Object.assign(info, await readCheckStatus(context, page));
    return info;
  } finally {
    await browser.close();
  }
}

async function main() {
  ensureHeadedMode();
  let port = null;
  let wait = false;
  let timeout = DEFAULT_TIMEOUT_SEC;
  for (let i = 2; i < process.argv.length; i++) {
    if (process.argv[i] === "--port" && process.argv[i + 1]) port = Number(process.argv[++i]);
    if (process.argv[i] === "--wait") wait = true;
    if (process.argv[i] === "--timeout" && process.argv[i + 1]) timeout = Number(process.argv[++i]);
  }
  if (!port) {
    console.error("需要 --port");
    return 1;
  }
  const result = await inspect(port, wait, timeout);
  console.log(JSON.stringify(result, null, 2));
  if (wait && !result.device_security_success) {
    console.error(CUSTOMER_FAIL_MSG);
    return 1;
  }
  return 0;
}

process.exit(await main());
