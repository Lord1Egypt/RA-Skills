#!/usr/bin/env node
/** 退出站斧客户端（ExitClient）。 */
import {
  call,
  clearOpenedMalls,
  clearOpeningMalls,
  configureStdio,
  emit,
  HttpError,
  preferredPort,
} from "./zhanfu_http.mjs";

async function main() {
  configureStdio();
  const port = preferredPort();
  let data;
  try {
    data = await call("ExitClient", { args: "", timeout: 8, port });
  } catch (exc) {
    if (exc instanceof HttpError) {
      console.log("站斧未打开或无法通讯。");
      return emit({ ok: false, status: "zhanfu_down" }, 1);
    }
    throw exc;
  }
  const ro = data.returnObj;
  clearOpeningMalls();
  clearOpenedMalls();
  console.log(`已退出站斧。returnObj=${JSON.stringify(ro)}`);
  return emit({ ok: true, status: "exited", returnObj: ro }, 0);
}

process.exit(await main());
