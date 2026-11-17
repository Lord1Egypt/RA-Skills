#!/usr/bin/env node
/** 登录站斧。仅使用命令行当场提供的账号密码，isboss 固定 true。 */
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
  let username = null;
  let password = null;
  for (let i = 2; i < process.argv.length; i++) {
    if (process.argv[i] === "--username" && process.argv[i + 1]) username = process.argv[++i];
    if (process.argv[i] === "--password" && process.argv[i + 1]) password = process.argv[++i];
  }
  if (!username || !password) {
    console.log("缺少账号或密码");
    return emit({ ok: false, status: "missing_credentials" }, 1);
  }
  const port = tryPreferredPort();
  if (port == null) return emitZhanfuDown();

  let data;
  try {
    data = await call("Login", {
      args: JSON.stringify({ username, password, isboss: true }),
      timeout: 15,
      port,
    });
  } catch (exc) {
    if (exc instanceof HttpError) return emitZhanfuDown();
    throw exc;
  }

  const ro = data.returnObj || {};
  if (typeof ro !== "object" || ro.success !== true) {
    const msg = typeof ro === "object" ? ro.msg : data;
    console.log(String(msg));
    return emit({ ok: false, status: "login_failed", msg: String(msg) }, 1);
  }

  const listed = await call("GetBrowserList", {
    args: JSON.stringify({ page: 1, limit: 20 }),
    timeout: 8,
    port,
  });
  const info = ((listed.returnObj || {}).data || {});
  saveMallsToCache(info.mall_list || []);
  console.log("登录成功。");
  return emit({ ok: true, status: "logged_in", api_port: port }, 0);
}

process.exit(await main());
