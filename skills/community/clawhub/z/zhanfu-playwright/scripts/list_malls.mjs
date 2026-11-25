#!/usr/bin/env node
/** 获取店铺列表（GetBrowserList），并写入 mall_cache.json。 */
import { ensureDeps } from "./ensure_deps.mjs";
ensureDeps();

import {
  call,
  configureStdio,
  emit,
  emitZhanfuDown,
  HttpError,
  saveMallsToCache,
  tryPreferredPort,
} from "./zhanfu_http.mjs";

async function main() {
  configureStdio();
  let page = 1;
  let limit = 10;
  for (let i = 2; i < process.argv.length; i++) {
    if (process.argv[i] === "--page" && process.argv[i + 1]) page = Number(process.argv[++i]);
    if (process.argv[i] === "--limit" && process.argv[i + 1]) limit = Number(process.argv[++i]);
  }
  const port = tryPreferredPort();
  if (port == null) return emitZhanfuDown();

  let data;
  try {
    data = await call("GetBrowserList", {
      args: JSON.stringify({ page, limit }),
      timeout: 8,
      port,
    });
  } catch (exc) {
    if (exc instanceof HttpError) return emitZhanfuDown();
    throw exc;
  }

  const ro = data.returnObj || {};
  if (typeof ro !== "object" || ro.success !== true) {
    const msg = typeof ro === "object" ? ro.msg : data;
    console.log(`GetBrowserList 失败: ${msg}`);
    return emit({ ok: false, status: "list_failed", msg: String(msg) }, 1);
  }

  const info = ro.data || {};
  const malls = info.mall_list;
  if (malls == null) {
    console.log("站斧未登录，请提供账号和密码");
    return emit({ ok: false, status: "need_login", msg: "站斧未登录，请提供账号和密码" }, 2);
  }

  saveMallsToCache(Array.isArray(malls) ? malls : []);
  const total = info.total;
  console.log(`店铺列表 第${page}页 每页${limit} 共${total}个`);
  for (const mall of malls || []) {
    console.log(
      `- ${mall.mall_name}  id=${mall.mall_id}  平台=${mall.platform_name}  IP=${mall.ip_address}`
    );
  }
  return emit({ ok: true, status: "ok", page, limit, total, mall_list: malls }, 0);
}

process.exit(await main());
