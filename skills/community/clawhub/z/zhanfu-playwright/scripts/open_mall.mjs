#!/usr/bin/env node
/** 打开店铺：按店名取 ID → OpenBrowser → 等 200ms → 取 WebDriverPort。 */
import { ensureDeps } from "./ensure_deps.mjs";
ensureDeps();

import {
  AFTER_OPEN_BROWSER_SEC,
  OPEN_MALL_FAIL_HINT,
  WD_FETCH_ATTEMPTS,
  WD_FETCH_HTTP_TIMEOUT,
  WD_FETCH_RETRY_SLEEP_SEC,
  addOpeningMall,
  call,
  configureStdio,
  emit,
  emitZhanfuDown,
  finishOpenMallRun,
  HttpError,
  keepSlotWithoutPort,
  loadOpenedState,
  markMallOpened,
  noteOpenBrowserDone,
  registerOpenMallPid,
  resolveMallId,
  resolveMallIdRefreshOnce,
  sleep,
  tryPreferredPort,
  unregisterOpenMallPid,
  waitAndClaimOpenSlot,
  webdriverPortAlive,
} from "./zhanfu_http.mjs";

const PROBE_TIMEOUT_SEC = 1.5;

function cost(label, started) {
  const sec = (performance.now() - started) / 1000;
  console.log(`[耗时] ${label}=${sec.toFixed(3)}s`);
  return sec;
}

function liveSlotWebdriver(mallName) {
  const info = (loadOpenedState().opened || {})[mallName];
  if (!info || typeof info !== "object") return null;
  const wd = Number(info.WebDriverPort || 0) || 0;
  if (wd && webdriverPortAlive(wd)) return [wd, info.KernalNumber];
  return null;
}

async function openShopById(mallId, port) {
  const args = JSON.stringify({
    isDownLoadConfirm: false,
    isOpenMallIndex: true,
    isSwitchDynamicNetwork: false,
  });
  const t0 = performance.now();
  let data;
  try {
    data = await call("OpenBrowser", { browserId: mallId, args, timeout: 30, port });
  } catch (exc) {
    throw new Error(`OpenBrowser 超时/异常: ${exc.message || exc}。${OPEN_MALL_FAIL_HINT}`);
  }
  if (data.ret !== 200 || data.returnObj !== true) {
    throw new Error(`OpenBrowser 失败: ${JSON.stringify(data.returnObj)}。${OPEN_MALL_FAIL_HINT}`);
  }
  cost("OpenBrowser", t0);
  const waitMs = Math.round(AFTER_OPEN_BROWSER_SEC * 1000);
  console.log(`[打开] OpenBrowser 成功，等待 ${waitMs}ms 后取端口`);
  sleep(AFTER_OPEN_BROWSER_SEC * 1000);
}

async function getWebdriverPort(mallId, port) {
  let lastDetail = "";
  const tAll = performance.now();
  for (let attempt = 1; attempt <= WD_FETCH_ATTEMPTS; attempt++) {
    const t0 = performance.now();
    console.log(
      `[端口] GetBrowserWebDriver 第${attempt}/${WD_FETCH_ATTEMPTS}次 ` +
        `timeout=${WD_FETCH_HTTP_TIMEOUT}s mall_id=${mallId}`
    );
    let data;
    try {
      data = await call("GetBrowserWebDriver", {
        browserId: mallId,
        timeout: WD_FETCH_HTTP_TIMEOUT,
        port,
      });
    } catch (exc) {
      lastDetail = `超时/异常: ${exc.message || exc}`;
      cost(`取端口第${attempt}次失败`, t0);
      console.log(`[端口] 第${attempt}次失败: ${lastDetail}`);
      if (attempt < WD_FETCH_ATTEMPTS) sleep(WD_FETCH_RETRY_SLEEP_SEC * 1000);
      continue;
    }
    const ro = data.returnObj || {};
    const wd = typeof ro === "object" ? ro.WebDriverPort : null;
    if (typeof ro === "object" && ro.success === true && wd) {
      cost(`取端口第${attempt}次成功`, t0);
      cost("取端口合计", tAll);
      return ro;
    }
    lastDetail = String(JSON.stringify(ro));
    cost(`取端口第${attempt}次无端口`, t0);
    console.log(`[端口] 第${attempt}次无 WebDriverPort: ${JSON.stringify(ro)}`);
    if (attempt < WD_FETCH_ATTEMPTS) sleep(WD_FETCH_RETRY_SLEEP_SEC * 1000);
  }
  cost("取端口合计失败", tAll);
  throw new Error(
    `未获取到 WebDriverPort（${WD_FETCH_ATTEMPTS}次）: ${lastDetail}。${OPEN_MALL_FAIL_HINT}`
  );
}

async function probeWebdriver(mallId, port) {
  console.log(`[探测] GetBrowserWebDriver 单次 timeout=${PROBE_TIMEOUT_SEC}s mall_id=${mallId}`);
  const t0 = performance.now();
  try {
    const data = await call("GetBrowserWebDriver", {
      browserId: mallId,
      timeout: PROBE_TIMEOUT_SEC,
      port,
    });
    cost("探测", t0);
    const ro = data.returnObj || {};
    const wd = typeof ro === "object" ? ro.WebDriverPort : null;
    if (typeof ro === "object" && ro.success === true && wd) return [true, ro];
    return [false, typeof ro === "object" ? ro : {}];
  } catch (exc) {
    cost("探测(视为未开)", t0);
    console.log(`[探测] 超时/异常，视为未开: ${exc.message || exc}`);
    return [false, {}];
  }
}

function success(status, mallName, mallId, ro) {
  const wd = Number(ro.WebDriverPort);
  const kernel = ro.KernalNumber;
  markMallOpened(mallName, mallId, wd, kernel);
  if (status === "already_open") {
    console.log(`店铺 ${mallName} 已打开，未重复执行 OpenBrowser。`);
  } else {
    console.log(`店铺 ${mallName} 已打开。`);
  }
  console.log(`mall_id=${mallId}`);
  console.log(`WebDriverPort=${wd}`);
  return emit(
    {
      ok: true,
      status,
      mall_name: mallName,
      mall_id: mallId,
      WebDriverPort: wd,
      KernalNumber: kernel,
    },
    0
  );
}

async function run(mallName) {
  const tRun = performance.now();
  const port = tryPreferredPort();
  if (port == null) return emitZhanfuDown();
  let claimed = false;
  try {
    let mallId;
    const t0 = performance.now();
    try {
      mallId = await resolveMallId(mallName, { port });
    } catch (exc) {
      if (exc instanceof HttpError) return emitZhanfuDown();
      console.log(String(exc.message || exc));
      return emit({ ok: false, status: "resolve_failed", msg: String(exc.message || exc) }, 1);
    }
    cost("取mall_id", t0);

    const turn = waitAndClaimOpenSlot(mallName);
    claimed = true;
    if (turn === "reused") {
      const cached = liveSlotWebdriver(mallName);
      if (cached) {
        const [wd, kernel] = cached;
        cost("整次打开", tRun);
        return success("already_open", mallName, mallId, {
          WebDriverPort: wd,
          KernalNumber: kernel,
        });
      }
      const [opened, ro] = await probeWebdriver(mallId, port);
      if (opened) {
        cost("整次打开", tRun);
        return success("already_open", mallName, mallId, ro);
      }
      console.log(`店铺 ${mallName} 已在打开流程中但未拿到 WebDriverPort，不重复 OpenBrowser。`);
      cost("整次打开", tRun);
      return emit(
        {
          ok: false,
          status: "no_webdriver_port",
          mall_name: mallName,
          mall_id: mallId,
          occupying: true,
          msg: "已在打开流程中，20 次未拿到端口；仅 CloseBrowser 或端口退出才释放",
        },
        1
      );
    }

    addOpeningMall(mallName);
    const cached = liveSlotWebdriver(mallName);
    if (cached) {
      const [wd, kernel] = cached;
      cost("整次打开", tRun);
      return success("already_open", mallName, mallId, {
        WebDriverPort: wd,
        KernalNumber: kernel,
      });
    }

    try {
      await openShopById(mallId, port);
    } catch (exc) {
      console.log(String(exc.message || exc));
      try {
        mallId = await resolveMallIdRefreshOnce(mallName, port);
        await openShopById(mallId, port);
      } catch (exc2) {
        console.log(String(exc2.message || exc2));
        cost("整次打开", tRun);
        return emit({ ok: false, status: "open_failed", msg: String(exc2.message || exc2) }, 1);
      }
    }

    noteOpenBrowserDone(mallName, mallId);
    let ro;
    try {
      ro = await getWebdriverPort(mallId, port);
    } catch (exc) {
      console.log(String(exc.message || exc));
      keepSlotWithoutPort(mallName, mallId, { stillFetching: false });
      cost("整次打开", tRun);
      return emit(
        {
          ok: false,
          status: "no_webdriver_port",
          mall_name: mallName,
          mall_id: mallId,
          occupying: true,
          msg: String(exc.message || exc),
        },
        1
      );
    }

    cost("整次打开", tRun);
    return success("opened", mallName, mallId, ro);
  } finally {
    if (claimed) finishOpenMallRun();
  }
}

function parseArgs(argv) {
  let mallName = null;
  for (let i = 2; i < argv.length; i++) {
    if (argv[i] === "--mall-name" && argv[i + 1]) {
      mallName = argv[++i];
    }
  }
  if (!mallName) {
    console.error("需要 --mall-name");
    process.exit(1);
  }
  return mallName.trim();
}

configureStdio();
registerOpenMallPid();
try {
  const code = await run(parseArgs(process.argv));
  process.exit(code);
} finally {
  unregisterOpenMallPid();
}
