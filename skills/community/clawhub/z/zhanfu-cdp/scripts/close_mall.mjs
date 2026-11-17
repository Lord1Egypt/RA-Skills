#!/usr/bin/env node
/** 关闭指定店铺（CloseBrowser）。 */
import { ensureDeps } from "./ensure_deps.mjs";
ensureDeps();

import {
  call,
  configureStdio,
  emit,
  emitZhanfuDown,
  HttpError,
  removeOpeningMall,
  resolveMallId,
  resolveMallIdRefreshOnce,
  tryPreferredPort,
  unmarkMallOpened,
} from "./zhanfu_http.mjs";

async function closeOne(mallId, port) {
  const data = await call("CloseBrowser", { browserId: mallId, timeout: 15, port });
  return data.returnObj;
}

async function main() {
  configureStdio();
  let mallName = null;
  for (let i = 2; i < process.argv.length; i++) {
    if (process.argv[i] === "--mall-name" && process.argv[i + 1]) mallName = process.argv[++i];
  }
  if (!mallName) {
    console.error("需要 --mall-name");
    return 1;
  }
  mallName = mallName.trim();
  const port = tryPreferredPort();
  if (port == null) return emitZhanfuDown();

  let mallId;
  try {
    mallId = await resolveMallId(mallName, { port });
  } catch (exc) {
    if (exc instanceof HttpError) return emitZhanfuDown();
    console.log(String(exc.message || exc));
    return emit({ ok: false, status: "resolve_failed", msg: String(exc.message || exc) }, 1);
  }

  const t0 = performance.now();
  let ro;
  try {
    ro = await closeOne(mallId, port);
    if (ro === false) {
      mallId = await resolveMallIdRefreshOnce(mallName, port);
      ro = await closeOne(mallId, port);
    }
  } catch (exc) {
    console.log(`[耗时] CloseBrowser=${((performance.now() - t0) / 1000).toFixed(3)}s`);
    console.log(`CloseBrowser 超时/异常: ${exc.message || exc}`);
    return emit({ ok: false, status: "close_failed", mall_id: mallId, msg: String(exc.message || exc) }, 1);
  }
  console.log(`[耗时] CloseBrowser=${((performance.now() - t0) / 1000).toFixed(3)}s`);
  if (ro != null) {
    console.log(`关闭店铺失败: returnObj=${JSON.stringify(ro)}`);
    return emit({ ok: false, status: "close_failed", mall_id: mallId, returnObj: ro }, 1);
  }

  removeOpeningMall(mallName);
  unmarkMallOpened(mallName);
  console.log(`店铺 ${mallName} 已关闭。mall_id=${mallId}`);
  return emit({ ok: true, status: "closed", mall_name: mallName, mall_id: mallId }, 0);
}

process.exit(await main());
