#!/usr/bin/env node
/** 停止所有 open_mall.mjs 开店子进程；不停止端口监听。 */
import { ensureDeps } from "./ensure_deps.mjs";
ensureDeps();

import { configureStdio, emit, stopOpenMallRuns } from "./zhanfu_http.mjs";

configureStdio();
const n = stopOpenMallRuns();
process.exit(emit({ ok: true, status: "stopped", killed: n }, 0));
