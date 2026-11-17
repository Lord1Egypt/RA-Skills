import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { once } from "node:events";
import { copyFile, mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import http from "node:http";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";

// Exercise actual CLI + state transitions against an isolated local HTTP mock.
// No real Http.ini, shop state, client, or browser is used.
const scriptsDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const mallName = "recovery-test";
const mallId = "123456";
const missingPort = { success: true, KernalNumber: 137 };

async function fixture(t, handler) {
  const root = await mkdtemp(path.join(process.env.ZHANFU_TEST_TMPDIR || os.tmpdir(), "zhanfu-recovery-"));
  const scripts = path.join(root, "scripts");
  const appdata = path.join(root, "appdata");
  await mkdir(scripts);
  await mkdir(path.join(appdata, "ZhanFu"), { recursive: true });
  for (const name of ["open_mall.mjs", "zhanfu_http.mjs"]) {
    await copyFile(path.join(scriptsDir, name), path.join(scripts, name));
  }
  await writeFile(path.join(scripts, "ensure_deps.mjs"), "export function ensureDeps() {}\n");
  await writeFile(path.join(scripts, "watch_opened_ports.mjs"), "// No background watcher in test fixtures.\n");
  await writeFile(path.join(root, "mall_cache.json"), JSON.stringify({ mall_map: { [mallName]: mallId } }));
  const calls = [];
  const server = http.createServer(async (req, res) => {
    let body = "";
    for await (const chunk of req) body += chunk;
    const payload = JSON.parse(body);
    assert.equal(payload.browserId, mallId);
    calls.push(payload.action);
    const value = await handler(payload, calls);
    // Undefined deliberately simulates an unresponsive GetBrowserWebDriver.
    if (value === undefined) return;
    res.setHeader("content-type", "application/json");
    res.end(JSON.stringify({ ret: 200, returnObj: value }));
  });
  server.listen(0, "127.0.0.1");
  await once(server, "listening");
  const port = server.address().port;
  await writeFile(path.join(appdata, "ZhanFu", "Http.ini"), `[Common]\nhttpport=${port}\n`);
  const children = [];
  function run() {
    const child = spawn(process.execPath, [path.join(scripts, "open_mall.mjs"), "--mall-name", mallName], {
      cwd: root,
      env: { ...process.env, APPDATA: appdata },
      windowsHide: true,
      stdio: ["ignore", "pipe", "pipe"],
    });
    children.push(child);
    let output = "";
    child.stdout.on("data", (chunk) => { output += chunk; });
    child.stderr.on("data", (chunk) => { output += chunk; });
    return once(child, "close").then(([code]) => {
      const resultLine = output.split(/\r?\n/).findLast((line) => line.startsWith("RESULT_JSON="));
      assert.ok(resultLine, output);
      return { code, result: JSON.parse(resultLine.slice("RESULT_JSON=".length)), output };
    });
  }
  async function seed(info, flights = []) {
    await writeFile(path.join(root, "opened_malls.json"), JSON.stringify({
      opened: { [mallName]: { mall_id: mallId, WebDriverPort: 0, ...info } },
      queue: [], in_flight: flights,
    }));
  }
  async function state() {
    return JSON.parse(await readFile(path.join(root, "opened_malls.json"), "utf8"));
  }
  t.after(async () => {
    for (const child of children) {
      if (child.exitCode === null && child.signalCode === null) {
        child.kill();
        await once(child, "close");
      }
    }
    server.closeAllConnections();
    await new Promise((resolve) => server.close(resolve));
    await rm(root, { recursive: true, force: true, maxRetries: 5, retryDelay: 100 });
  });
  return { run, seed, state, calls, readyPort: () => ({ ...missingPort, WebDriverPort: port }) };
}

test("legacy failed zero-port hold can open again, and an open shop is reused", { timeout: 30000 }, async (t) => {
  let opened = false;
  const f = await fixture(t, async ({ action }) => {
    if (action === "OpenBrowser") { opened = true; return true; }
    return opened ? f.readyPort() : missingPort;
  });
  await f.seed({ pending: false, hold_without_port: true });
  const first = await f.run();
  assert.equal(first.code, 0, first.output);
  assert.equal(first.result.status, "opened");
  assert.deepEqual(f.calls, ["GetBrowserWebDriver", "OpenBrowser", "GetBrowserWebDriver"]);
  const second = await f.run();
  assert.equal(second.result.status, "already_open", second.output);
  assert.equal(f.calls.filter((a) => a === "OpenBrowser").length, 1);
});

test("20 failed fetches release occupancy; next request reuses a late browser without opening again", { timeout: 60000 }, async (t) => {
  let ready = false;
  const f = await fixture(t, async ({ action }) => action === "OpenBrowser" ? true : ready ? f.readyPort() : missingPort);
  const first = await f.run();
  assert.equal(first.code, 1, first.output);
  assert.equal(first.result.occupying, false);
  assert.equal(first.result.retryable, true);
  assert.equal(f.calls.filter((a) => a === "GetBrowserWebDriver").length, 21); // probe + 20 fetches
  assert.equal((await f.state()).opened[mallName], undefined);
  assert.deepEqual((await f.state()).in_flight, []);
  ready = true;
  const second = await f.run();
  assert.equal(second.result.status, "already_open", second.output);
  assert.equal(f.calls.filter((a) => a === "OpenBrowser").length, 1);
});

test("concurrent caller cannot repeat OpenBrowser while the owner waits for its response", { timeout: 30000 }, async (t) => {
  let enterOpen;
  const entered = new Promise((resolve) => { enterOpen = resolve; });
  let releaseOpen;
  const released = new Promise((resolve) => { releaseOpen = resolve; });
  let ready = false;
  const f = await fixture(t, async ({ action }) => {
    if (action === "OpenBrowser") { enterOpen(); await released; ready = true; return true; }
    return ready ? f.readyPort() : missingPort;
  });
  const first = f.run();
  await entered;
  const second = await f.run();
  assert.equal(second.result.occupying, true, second.output);
  assert.equal(f.calls.filter((a) => a === "OpenBrowser").length, 1);
  assert.equal((await f.state()).in_flight.length, 1);
  releaseOpen();
  assert.equal((await first).result.status, "opened");
});

test("concurrent caller preserves the owner after OpenBrowser succeeds but before a port appears", { timeout: 30000 }, async (t) => {
  let enteredFetch;
  const fetching = new Promise((resolve) => { enteredFetch = resolve; });
  let releaseFetch;
  const released = new Promise((resolve) => { releaseFetch = resolve; });
  let opens = 0;
  let fetches = 0;
  let ready = false;
  const f = await fixture(t, async ({ action }) => {
    if (action === "OpenBrowser") { opens++; return true; }
    if (opens && ++fetches === 1) { enteredFetch(); await released; }
    return ready ? f.readyPort() : missingPort;
  });
  const first = f.run();
  await fetching;
  assert.equal((await f.state()).in_flight.length, 1);
  const second = await f.run();
  assert.equal(second.result.occupying, true, second.output);
  assert.equal(opens, 1);
  assert.equal((await f.state()).in_flight.length, 1);
  ready = true;
  releaseFetch();
  assert.equal((await first).result.status, "opened");
});

test("interrupted, expired pending record does not block the next open", { timeout: 30000 }, async (t) => {
  let opened = false;
  const f = await fixture(t, async ({ action }) => {
    if (action === "OpenBrowser") { opened = true; return true; }
    return opened ? f.readyPort() : missingPort;
  });
  await f.seed({ pending: true, pending_until: 1 }, [{ mall_name: mallName, pid: 2147483647 }]);
  const run = await f.run();
  assert.equal(run.result.status, "opened", run.output);
  assert.equal(f.calls.filter((a) => a === "OpenBrowser").length, 1);
});

test("single probe timeout allows the requested open without requiring a close", { timeout: 30000 }, async (t) => {
  let opened = false;
  const f = await fixture(t, async ({ action }) => {
    if (action === "OpenBrowser") { opened = true; return true; }
    return opened ? f.readyPort() : undefined;
  });
  await f.seed({ pending: false, hold_without_port: true });
  const run = await f.run();
  assert.equal(run.result.status, "opened", run.output);
  assert.equal(f.calls.filter((a) => a === "OpenBrowser").length, 1);
});
