#!/usr/bin/env node
/** 监听已开店铺 WebDriver 端口；端口退出则从 opened_malls 槽位队列删除。 */
import { writeFileSync, unlinkSync } from "node:fs";
import {
  PORT_WATCH_POLL_SEC,
  configureStdio,
  openedWatchPidPath,
  reapExitedOpenedMalls,
  sleep,
} from "./zhanfu_http.mjs";

configureStdio();
writeFileSync(openedWatchPidPath(), String(process.pid), "utf8");
let idle = 0;
while (true) {
  const remaining = reapExitedOpenedMalls();
  if (remaining <= 0) {
    idle += 1;
    if (idle >= 30) break;
  } else {
    idle = 0;
  }
  sleep(PORT_WATCH_POLL_SEC * 1000);
}
try {
  unlinkSync(openedWatchPidPath());
} catch {
  /* ignore */
}
process.exit(0);
