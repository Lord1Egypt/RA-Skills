// Worker thread for crawl.mjs: processes one page per message. Runs off the
// main thread so the crawler can terminate it when a page takes too long
// (a catastrophic regex, a pathological page) and still meet its deadline.

import { parentPort } from "node:worker_threads";
import { processPage } from "./page.mjs";

parentPort.on("message", (job) => {
  try {
    parentPort.postMessage({ ok: true, result: processPage(job) });
  } catch (e) {
    parentPort.postMessage({ ok: false, error: e?.message || String(e) });
  }
});
