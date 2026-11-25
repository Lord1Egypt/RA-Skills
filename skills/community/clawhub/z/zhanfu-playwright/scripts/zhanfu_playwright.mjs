#!/usr/bin/env node
/**
 * 站斧 WebDriver + Playwright 参考 CLI（Node）。
 * 日常开店请用 open_mall.mjs；本文件供全流程调试参考。
 */
import { ensureDeps } from "./ensure_deps.mjs";
ensureDeps();

const { chromium } = await import("playwright");
const { ensureHeadedMode } = await import("./headed_mode.mjs");
const {
  COMM_FAIL_MSG,
  call,
  configureStdio,
  HttpError,
  resolveMallId,
  sleep,
  tryPreferredPort,
  addOpeningMall,
  removeOpeningMall,
} = await import("./zhanfu_http.mjs");

const HTTP_PROBE_TIMEOUT = 1.5;
const OPEN_MALL_FAIL_HINT = "打开店铺失败，请确认该店铺是否已绑定 IP / 设备";

function argValue(argv, name) {
  const i = argv.indexOf(name);
  if (i >= 0 && argv[i + 1] != null) return argv[i + 1];
  return undefined;
}

function hasFlag(argv, name) {
  return argv.includes(name);
}

async function classifyApiPort(port) {
  try {
    const data = await call("GetBrowserList", {
      args: JSON.stringify({ page: 1, limit: 20 }),
      timeout: HTTP_PROBE_TIMEOUT,
      port,
    });
    const ro = data.returnObj || {};
    if (typeof ro === "object" && ro.success === true) {
      const malls = (ro.data || {}).mall_list;
      if (malls != null) return "zhanfu_logged_in";
    }
    if (data.module === "WebDriverModule" || data.action) return "zhanfu_not_logged_in";
    return "foreign";
  } catch {
    return "down";
  }
}

async function probeZhanfuApi(overridePort) {
  const port = overridePort != null ? Number(overridePort) : tryPreferredPort();
  if (port == null) {
    console.log(COMM_FAIL_MSG);
    return null;
  }
  const status = await classifyApiPort(port);
  if (status === "zhanfu_logged_in") {
    console.log(`[探测] 站斧 API 已打开(能取到数据): ${port}`);
    return port;
  }
  if (status === "zhanfu_not_logged_in") {
    console.log(`[探测] 站斧 API HTTP可达(可能未登录): ${port}`);
    return port;
  }
  console.log(COMM_FAIL_MSG);
  return null;
}

async function main() {
  configureStdio();
  ensureHeadedMode();
  const argv = process.argv.slice(2);
  const action = argValue(argv, "--action") || "run";
  const apiPortArg = argValue(argv, "--api-port");
  const mallName = argValue(argv, "--mall-name");
  const mallIdArg = argValue(argv, "--mall-id");
  const connectCdp = hasFlag(argv, "--connect-cdp");
  const closeAfter = hasFlag(argv, "--close");
  const forceOpen = hasFlag(argv, "--force-open");
  const bootstrapOnly = hasFlag(argv, "--bootstrap-only");

  if (action === "close-browser") {
    const port = apiPortArg ? Number(apiPortArg) : tryPreferredPort();
    if (port == null) {
      console.log(COMM_FAIL_MSG);
      return 1;
    }
    if (!mallIdArg) {
      console.error("close-browser 需要 --mall-id");
      return 1;
    }
    await call("CloseBrowser", { browserId: mallIdArg, port });
    if (mallName) removeOpeningMall(mallName);
    console.log(JSON.stringify({ action, api_port: port, mall_id: mallIdArg }));
    return 0;
  }

  const apiPort = await probeZhanfuApi(apiPortArg);
  if (apiPort == null) return 1;
  console.log(`[复用] 使用 api_port=${apiPort}`);

  if (bootstrapOnly) {
    console.log(JSON.stringify({ api_port: apiPort }));
    return 0;
  }

  if (!mallName) {
    console.error("需要 --mall-name");
    return 1;
  }

  const mallId = await resolveMallId(mallName, { port: apiPort });
  addOpeningMall(mallName);

  let existingPort = null;
  try {
    const data = await call("GetBrowserWebDriver", {
      browserId: mallId,
      timeout: 5,
      port: apiPort,
    });
    const ro = data.returnObj || {};
    if (ro.success && ro.WebDriverPort) existingPort = Number(ro.WebDriverPort);
  } catch (exc) {
    console.log(`[探测] GetBrowserWebDriver 超时/异常，视为未开: ${exc.message || exc}`);
  }

  let wdPort;
  let kernel = 0;
  if (existingPort != null && !forceOpen) {
    console.log(`[打开] 店铺 ${mallName} 已打开 (WebDriverPort=${existingPort})，跳过 OpenBrowser`);
    wdPort = existingPort;
  } else {
    if (existingPort != null && forceOpen) {
      console.log(`[打开] 店铺已打开 (port=${existingPort})，--force-open 重新 OpenBrowser`);
    }
    const openArgs = JSON.stringify({
      isDownLoadConfirm: false,
      isOpenMallIndex: true,
      isSwitchDynamicNetwork: false,
    });
    const data = await call("OpenBrowser", {
      browserId: mallId,
      args: openArgs,
      timeout: 30,
      port: apiPort,
    });
    if (data.ret !== 200 || data.returnObj !== true) {
      throw new Error(`OpenBrowser 失败: ${JSON.stringify(data.returnObj)}。${OPEN_MALL_FAIL_HINT}`);
    }
    sleep(500);
    const wd = await call("GetBrowserWebDriver", {
      browserId: mallId,
      timeout: 10,
      port: apiPort,
    });
    const ro = wd.returnObj || {};
    wdPort = Number(ro.WebDriverPort);
    kernel = Number(ro.KernalNumber || 0);
    if (!wdPort) throw new Error(`无法获取 WebDriverPort。${OPEN_MALL_FAIL_HINT}`);
  }

  const result = {
    api_port: apiPort,
    mall_id: mallId,
    mall_name: mallName,
    webdriver_port: wdPort,
    kernel,
  };

  if (connectCdp) {
    const browser = await chromium.connectOverCDP(`http://127.0.0.1:${wdPort}`);
    const ctx = browser.contexts()[0];
    const page = ctx.pages()[0] || (await ctx.newPage());
    console.log(`[Playwright] 已连接 CDP 端口 ${wdPort}，当前页: ${page.url()}`);
    result.cdp_connected = true;
    result.current_url = page.url();
    if (closeAfter) await browser.close();
  }

  console.log(JSON.stringify(result));
  if (closeAfter) {
    await call("CloseBrowser", { browserId: mallId, port: apiPort });
    removeOpeningMall(mallName);
  }
  return 0;
}

try {
  process.exit(await main());
} catch (e) {
  if (e instanceof HttpError) {
    console.log(COMM_FAIL_MSG);
    process.exit(1);
  }
  console.error(String(e?.message || e));
  process.exit(1);
}
