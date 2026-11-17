#!/usr/bin/env node
/** 站斧 WebDriver HTTP 公共库。browserId 一律转成字符串。 */
import { existsSync, lstatSync, readFileSync, readlinkSync, writeFileSync, openSync, closeSync, unlinkSync } from "node:fs";
import { spawn, spawnSync, execFileSync } from "node:child_process";
import { renameSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export const API_DEFAULT_PORT = 12678;
export const COMM_FAIL_MSG = "请打开最新的站斧";
export const HTTP_PROBE_TIMEOUT = 1.5;
export const OPEN_MALL_FAIL_HINT =
  "打开店铺失败，请确认该店铺是否已绑定 IP / 设备。" +
  "首次使用请先在站斧客户端手动打开该店铺以下载内核。";
export const MAC_UNSUPPORTED = new Set([
  "SetDownLoadPath",
  "ClearCacheFolder",
  "ClearCache",
  "SetInstallPlugins",
]);

export const OPEN_STAGGER_SEC = 0.3;
export const SLOT_POLL_SEC = 0.5;
export const PORT_WATCH_POLL_SEC = 1.0;
export const WD_FETCH_HTTP_TIMEOUT = 2;
export const WD_FETCH_ATTEMPTS = 20;
export const WD_FETCH_RETRY_SLEEP_SEC = 0.3;
export const AFTER_OPEN_BROWSER_SEC = 0.2;
export const PENDING_GRACE_SEC =
  AFTER_OPEN_BROWSER_SEC +
  WD_FETCH_ATTEMPTS * (WD_FETCH_HTTP_TIMEOUT + WD_FETCH_RETRY_SLEEP_SEC) +
  5;

let _killJobHandle = null;

export function sleep(ms) {
  const sab = new SharedArrayBuffer(4);
  Atomics.wait(new Int32Array(sab), 0, 0, Math.max(0, Math.ceil(ms)));
}

export function configureStdio() {
  try {
    if (process.stdout.setDefaultEncoding) process.stdout.setDefaultEncoding("utf8");
    if (process.stderr.setDefaultEncoding) process.stderr.setDefaultEncoding("utf8");
  } catch {
    /* ignore */
  }
}

export function isMac() {
  return process.platform === "darwin";
}

export function isWin() {
  return process.platform === "win32";
}

export function skillDir() {
  return path.dirname(__dirname);
}

export function nowIso() {
  const d = new Date();
  const offset = 8 * 60;
  const local = new Date(d.getTime() + (offset - d.getTimezoneOffset()) * 60000);
  return local.toISOString().replace("Z", "+08:00");
}

export function loadJson(filePath) {
  if (!existsSync(filePath)) return {};
  try {
    const raw = readFileSync(filePath, "utf8").replace(/^\uFEFF/, "");
    const data = JSON.parse(raw);
    return data && typeof data === "object" && !Array.isArray(data) ? data : {};
  } catch {
    return {};
  }
}

export function writeJson(filePath, data) {
  writeFileSync(filePath, JSON.stringify(data, null, 2) + "\n", "utf8");
}

export function httpIniPath() {
  if (isMac()) {
    return path.join(os.homedir(), "Library", "Application Support", "ZhanFu", "Http.ini");
  }
  const appdata = process.env.APPDATA || path.join(os.homedir(), "AppData", "Roaming");
  return path.join(appdata, "ZhanFu", "Http.ini");
}

function readUtf8File(filePath) {
  try {
    return readFileSync(filePath, "utf8").replace(/^\uFEFF/, "");
  } catch {
    return null;
  }
}

function parseHttpPort(text) {
  let inCommon = false;
  for (const line of String(text).split(/\r?\n/)) {
    const t = line.trim();
    if (!t || t.startsWith(";") || t.startsWith("#")) continue;
    const sec = t.match(/^\[(.+)\]$/);
    if (sec) {
      inCommon = sec[1].toLowerCase() === "common";
      continue;
    }
    if (!inCommon) continue;
    const m = t.match(/^([^=]+)=(.*)$/);
    if (!m) continue;
    if (m[1].trim().toLowerCase() !== "httpport") continue;
    const port = Number.parseInt(String(m[2]).trim(), 10);
    if (Number.isInteger(port) && port >= 1 && port <= 65535) return port;
    return null;
  }
  return null;
}

/** Node 读不到部分外联；readlink 可能带 \\?\ 、\??\ 或盘符加 \??\ 前缀。 */
function normalizeLinkTarget(linkPath, raw) {
  let target = String(raw ?? "").replace(/\0/g, "").trim();
  if (!target) return null;
  target = target.replace(/^[A-Za-z]:[\\/](?:\?\?|\?)[\\/]/, "");
  let rest = null;
  if (target.startsWith("\\\\?\\")) rest = target.slice(4);
  else if (target.startsWith("\\??\\")) rest = target.slice(4);
  if (rest != null) {
    target = rest.toLowerCase().startsWith("unc\\") ? `\\\\${rest.slice(4)}` : rest;
  }
  if (!path.isAbsolute(target)) target = path.resolve(path.dirname(linkPath), target);
  return target;
}

function reparseTarget(linkPath) {
  try {
    if (!lstatSync(linkPath).isSymbolicLink()) return null;
    return normalizeLinkTarget(linkPath, readlinkSync(linkPath));
  } catch {
    return null;
  }
}

function externalHttpIniPaths(filePath) {
  const name = path.basename(filePath);
  const out = [];
  const fileTarget = reparseTarget(filePath);
  if (fileTarget) {
    out.push(fileTarget);
    out.push(path.join(fileTarget, name));
  }
  const dirTarget = reparseTarget(path.dirname(filePath));
  if (dirTarget) out.push(path.join(dirTarget, name));
  return out;
}

export function readHttpIniPort() {
  const filePath = httpIniPath();
  const direct = readUtf8File(filePath);
  if (direct != null) return parseHttpPort(direct);

  const pathKey = (item) => {
    const resolved = path.resolve(item);
    return process.platform === "win32" ? resolved.toLowerCase() : resolved;
  };
  const seen = new Set([pathKey(filePath)]);
  for (const alt of externalHttpIniPaths(filePath)) {
    const key = pathKey(alt);
    if (seen.has(key)) continue;
    seen.add(key);
    const text = readUtf8File(alt);
    if (text != null) return parseHttpPort(text);
  }
  return null;
}

export function preferredPort() {
  const port = readHttpIniPort();
  if (port == null) {
    const err = new Error(COMM_FAIL_MSG);
    err.code = "ZHANFU_DOWN";
    throw err;
  }
  return port;
}

export function tryPreferredPort() {
  try {
    return preferredPort();
  } catch (e) {
    if (e && e.code === "ZHANFU_DOWN") return null;
    return null;
  }
}

export function mallCachePath() {
  return path.join(skillDir(), "mall_cache.json");
}

export function loadMallMap() {
  const data = loadJson(mallCachePath());
  const mallMap = data.mall_map;
  if (!mallMap || typeof mallMap !== "object" || Array.isArray(mallMap)) return {};
  const out = {};
  for (const [k, v] of Object.entries(mallMap)) out[String(k)] = String(v);
  return out;
}

export function saveMallMap(mallMap) {
  writeJson(mallCachePath(), { mall_map: mallMap, updated_at: nowIso() });
}

export function saveMallToCache(mallName, mallId) {
  const mallMap = loadMallMap();
  mallMap[mallName] = String(mallId);
  saveMallMap(mallMap);
  console.log(`[缓存] ${mallName} → ${mallId}`);
}

export function saveMallsToCache(malls) {
  const mallMap = loadMallMap();
  let changed = false;
  for (const mall of malls || []) {
    const name = mall?.mall_name;
    const mallId = mall?.mall_id;
    if (name == null || mallId == null) continue;
    const key = String(name);
    const value = String(mallId);
    if (mallMap[key] !== value) {
      mallMap[key] = value;
      changed = true;
    }
  }
  if (changed) {
    saveMallMap(mallMap);
    console.log(`[缓存] 已从列表更新 mall_cache.json（共 ${Object.keys(mallMap).length} 条）`);
  }
}

export function dropMallCache(mallName) {
  const mallMap = loadMallMap();
  if (mallName in mallMap) {
    delete mallMap[mallName];
    saveMallMap(mallMap);
    console.log(`[缓存] 已删除过期条目: ${mallName}`);
  }
}

export function openingMallsPath() {
  return path.join(skillDir(), "opening_malls.json");
}

export function loadOpeningMalls() {
  const malls = loadJson(openingMallsPath()).malls;
  if (!Array.isArray(malls)) return [];
  return malls.filter(Boolean).map(String);
}

export function writeOpeningMalls(malls) {
  writeJson(openingMallsPath(), {
    malls: [...new Set(malls)],
    updated_at: nowIso(),
  });
}

export function addOpeningMall(mallName) {
  const malls = loadOpeningMalls();
  if (malls.includes(mallName)) return;
  malls.push(mallName);
  writeOpeningMalls(malls);
  console.log(`[打开意图] 已写入: ${mallName}`);
}

export function removeOpeningMall(mallName) {
  writeOpeningMalls(loadOpeningMalls().filter((n) => n !== mallName));
}

export function clearOpeningMalls() {
  writeOpeningMalls([]);
  console.log("[打开意图] 已清空 opening_malls.json");
}

export function emit(result, code) {
  console.log("RESULT_JSON=" + JSON.stringify(result));
  return code;
}

export function emitZhanfuDown() {
  console.log(COMM_FAIL_MSG);
  return emit({ ok: false, status: "zhanfu_down", msg: COMM_FAIL_MSG }, 1);
}

export class HttpError extends Error {
  constructor(message) {
    super(message);
    this.name = "HttpError";
  }
}

export async function call(action, { browserId = "", args = "", timeout = 8, port = null } = {}) {
  if (isMac() && MAC_UNSUPPORTED.has(action)) {
    throw new Error(`macOS 暂不支持 ${action}`);
  }
  let apiPort = port;
  if (apiPort == null) {
    const resolved = tryPreferredPort();
    if (resolved == null) throw new HttpError(COMM_FAIL_MSG);
    apiPort = resolved;
  } else {
    apiPort = Number(apiPort);
  }
  const bid = browserId == null || browserId === "" ? "" : String(browserId);
  const payload = {
    module: "WebDriverModule",
    action,
    browserId: bid,
    args,
  };
  const ac = new AbortController();
  const timer = setTimeout(() => ac.abort(), Math.max(1, timeout * 1000));
  try {
    const resp = await fetch(`http://127.0.0.1:${apiPort}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: ac.signal,
    });
    const text = await resp.text();
    if (!text) throw new Error(`${action} 空响应 HTTP ${resp.status}`);
    return JSON.parse(text);
  } catch (e) {
    if (e?.name === "AbortError") throw new HttpError(`${action} 超时`);
    if (e instanceof HttpError) throw e;
    if (e instanceof SyntaxError) throw e;
    throw new HttpError(String(e?.message || e));
  } finally {
    clearTimeout(timer);
  }
}

export async function getMallByName(mallName, port = null) {
  const data = await call("GetMallByName", {
    args: JSON.stringify({ mallName }),
    port,
  });
  const ro = data.returnObj || {};
  if (typeof ro !== "object" || ro.success !== true) {
    const msg = typeof ro === "object" ? ro.msg : data;
    throw new Error(`GetMallByName 失败: ${msg}`);
  }
  const mallId = (ro.data || {}).mall_id;
  if (mallId == null) throw new Error("GetMallByName 未返回 mall_id");
  const mallIdStr = String(mallId);
  saveMallToCache(mallName, mallIdStr);
  return mallIdStr;
}

export async function resolveMallId(mallName, { useCache = true, port = null } = {}) {
  if (useCache) {
    const cached = loadMallMap()[mallName];
    if (cached) {
      console.log(`[店铺] 命中缓存 mall_id=${cached} (${mallName})`);
      return cached;
    }
  }
  const mallId = await getMallByName(mallName, port);
  console.log(`[店铺] mall_id=${mallId} (${mallName})`);
  return mallId;
}

export async function resolveMallIdRefreshOnce(mallName, port = null) {
  dropMallCache(mallName);
  return resolveMallId(mallName, { useCache: false, port });
}

export function openedMallsPath() {
  return path.join(skillDir(), "opened_malls.json");
}

export function openedMallsLockPath() {
  return path.join(skillDir(), "opened_malls.lock");
}

export function openedWatchPidPath() {
  return path.join(skillDir(), "opened_ports_watch.pid");
}

export function openMallPidsPath() {
  return path.join(skillDir(), "open_mall_pids.json");
}

function pidAlive(pid) {
  const n = Number(pid);
  if (!Number.isInteger(n) || n <= 0) return false;
  if (isWin()) {
    try {
      const out = execFileSync("tasklist", ["/FI", `PID eq ${n}`, "/NH"], {
        encoding: "utf8",
        windowsHide: true,
      });
      return out.includes(String(n));
    } catch {
      return false;
    }
  }
  try {
    process.kill(n, 0);
    return true;
  } catch (e) {
    return e?.code === "EPERM";
  }
}

export function registerOpenMallPid() {
  const pid = process.pid;
  const data = loadJson(openMallPidsPath());
  const pids = [];
  for (const raw of data.pids || []) {
    const old = Number(raw);
    if (Number.isInteger(old) && old && old !== pid && pidAlive(old)) pids.push(old);
  }
  pids.push(pid);
  writeJson(openMallPidsPath(), { pids, updated_at: nowIso() });
}

export function unregisterOpenMallPid() {
  const pid = process.pid;
  const data = loadJson(openMallPidsPath());
  const pids = [];
  for (const raw of data.pids || []) {
    const old = Number(raw);
    if (Number.isInteger(old) && old && old !== pid && pidAlive(old)) pids.push(old);
  }
  writeJson(openMallPidsPath(), { pids, updated_at: nowIso() });
}

function killPid(pid) {
  const n = Number(pid);
  if (!Number.isInteger(n) || n <= 0 || n === process.pid || !pidAlive(n)) return false;
  const watch = readWatchPid();
  if (watch && n === watch) return false;
  try {
    if (isWin()) {
      spawnSync("taskkill", ["/PID", String(n), "/F"], {
        windowsHide: true,
        stdio: "ignore",
      });
    } else {
      process.kill(n, "SIGTERM");
    }
    console.log(`[进程] 已结束 open_mall pid=${n}`);
    return true;
  } catch {
    return false;
  }
}

function pidsFromOpenMallCmdline() {
  const found = [];
  if (isWin()) {
    try {
      const raw = execFileSync(
        "wmic",
        ["process", "where", "name='node.exe'", "get", "ProcessId,CommandLine"],
        { encoding: "utf8", windowsHide: true, timeout: 8000 }
      );
      for (const line of raw.split(/\r?\n/)) {
        if (!line.includes("open_mall.mjs") || line.includes("watch_opened_ports")) continue;
        const parts = line.trim().split(/\s+/);
        const last = parts[parts.length - 1];
        if (/^\d+$/.test(last)) found.push(Number(last));
      }
    } catch {
      /* ignore */
    }
    return found;
  }
  try {
    const raw = execFileSync("ps", ["-ax", "-o", "pid=,command="], {
      encoding: "utf8",
      timeout: 8000,
    });
    for (const line of raw.split(/\n/)) {
      if (!line.includes("open_mall.mjs")) continue;
      const pid = Number(line.trim().split(/\s+/)[0]);
      if (Number.isInteger(pid)) found.push(pid);
    }
  } catch {
    /* ignore */
  }
  return found;
}

export function stopOpenMallRuns() {
  const pids = new Set();
  for (const raw of loadJson(openMallPidsPath()).pids || []) {
    const n = Number(raw);
    if (Number.isInteger(n)) pids.add(n);
  }
  for (const p of pidsFromOpenMallCmdline()) pids.add(p);
  let killed = 0;
  for (const pid of [...pids].sort((a, b) => a - b)) {
    if (killPid(pid)) killed += 1;
  }
  writeJson(openMallPidsPath(), { pids: [], updated_at: nowIso() });
  console.log(`[进程] 已停止 ${killed} 个 open_mall.mjs`);
  return killed;
}

export function attachCurrentProcessToKillJob() {
  if (!isWin()) return;
  // Node 无内置 Job Object；批量开店依赖父进程 wait + stop_open_malls。
  _killJobHandle = true;
  console.log("[进程] 批量开店：子进程随父进程等待结束；可用 stop_open_malls 强制停止");
}

function portAlive(port) {
  const p = Number(port);
  if (!Number.isInteger(p) || p <= 0) return false;
  const snippet = `
    const net=require('net');
    const s=net.connect({host:'127.0.0.1',port:${p}},()=>{s.destroy();process.exit(0)});
    s.on('error',()=>process.exit(1));
    setTimeout(()=>process.exit(1),400);
  `;
  try {
    const r = spawnSync(process.execPath, ["-e", snippet], {
      windowsHide: true,
      timeout: 1500,
    });
    return r.status === 0;
  } catch {
    return false;
  }
}

export function webdriverPortAlive(port) {
  return portAlive(port);
}

class OpenedLock {
  constructor() {
    this._heldPath = null;
  }
  enter() {
    const lockPath = openedMallsLockPath();
    const held = lockPath + ".held";
    while (true) {
      try {
        const fd = openSync(lockPath + ".taking", "wx");
        try {
          writeFileSync(fd, String(process.pid));
        } finally {
          closeSync(fd);
        }
        try {
          if (existsSync(held)) {
            let holder = 0;
            try {
              holder = Number(readFileSync(held, "utf8").trim());
            } catch {
              holder = 0;
            }
            if (holder && pidAlive(holder)) {
              try {
                unlinkSync(lockPath + ".taking");
              } catch {
                /* ignore */
              }
              sleep(SLOT_POLL_SEC * 1000);
              continue;
            }
            try {
              unlinkSync(held);
            } catch {
              /* ignore */
            }
          }
          renameSync(lockPath + ".taking", held);
          this._heldPath = held;
          return this;
        } catch {
          try {
            unlinkSync(lockPath + ".taking");
          } catch {
            /* ignore */
          }
          sleep(SLOT_POLL_SEC * 1000);
        }
      } catch {
        sleep(SLOT_POLL_SEC * 1000);
      }
    }
  }
  exit() {
    if (!this._heldPath) return;
    try {
      unlinkSync(this._heldPath);
    } catch {
      /* ignore */
    }
    this._heldPath = null;
  }
  with(fn) {
    this.enter();
    try {
      return fn();
    } finally {
      this.exit();
    }
  }
}

function emptyOpenedState() {
  return {
    opened: {},
    queue: [],
    in_flight: [],
    last_open_finished_at: 0.0,
    updated_at: nowIso(),
  };
}

export function loadOpenedState() {
  const data = loadJson(openedMallsPath());
  const state = emptyOpenedState();
  if (!data || !Object.keys(data).length) return state;
  state.opened = data.opened && typeof data.opened === "object" && !Array.isArray(data.opened) ? data.opened : {};
  state.queue = Array.isArray(data.queue) ? data.queue.map(String) : [];
  state.in_flight = asFlightList(data.in_flight);
  const last = Number(data.last_open_finished_at || 0);
  state.last_open_finished_at = Number.isFinite(last) ? last : 0;
  return state;
}

export function saveOpenedState(state) {
  const next = { ...state };
  delete next.max_open;
  next.in_flight = asFlightList(next.in_flight);
  next.updated_at = nowIso();
  writeJson(openedMallsPath(), next);
}

function asFlightList(flight) {
  if (flight && typeof flight === "object" && !Array.isArray(flight)) return [flight];
  if (Array.isArray(flight)) return flight.filter((x) => x && typeof x === "object");
  return [];
}

function normalizeInFlight(state) {
  state.in_flight = asFlightList(state.in_flight).filter((f) => pidAlive(Number(f.pid || 0)));
}

function dropInFlight(state, { mallName = "", pid = 0 } = {}) {
  state.in_flight = asFlightList(state.in_flight).filter((f) => {
    if (mallName && String(f.mall_name || "") === mallName) return false;
    if (pid && Number(f.pid || 0) === pid) return false;
    return true;
  });
}

function openSerialBusy(state) {
  const names = [];
  const seen = new Set();
  for (const flight of asFlightList(state.in_flight)) {
    const name = String(flight.mall_name || "");
    if (name && !seen.has(name)) {
      names.push(name);
      seen.add(name);
    }
  }
  const opened = state.opened || {};
  if (opened && typeof opened === "object") {
    for (const [name, info] of Object.entries(opened)) {
      if (info && typeof info === "object" && info.pending && !seen.has(name)) {
        names.push(String(name));
        seen.add(String(name));
      }
    }
  }
  return names;
}

function reapDeadOpened(state) {
  const opened = state.opened || (state.opened = {});
  const dead = [];
  const now = Date.now() / 1000;
  for (const [name, info] of Object.entries({ ...opened })) {
    let port = 0;
    let pending = false;
    let pendingUntil = 0;
    let openedAt = 0;
    if (info && typeof info === "object") {
      pending = Boolean(info.pending);
      port = Number(info.WebDriverPort || 0) || 0;
      pendingUntil = Number(info.pending_until || 0) || 0;
      openedAt = Number(info.opened_at || 0) || 0;
    }
    if (pending && now < pendingUntil) continue;
    if (openedAt && now - openedAt < 15) continue;
    if (port <= 0) {
      // 无端口的失败记录不能永久占位；仍在取端口的活跃任务保留保护。
      if (asFlightList(state.in_flight).some((f) => String(f.mall_name || "") === name)) continue;
    } else if (portAlive(port)) {
      continue;
    }
    delete opened[name];
    dead.push(name);
  }
  if (!dead.length) return dead;
  const deadSet = new Set(dead);
  state.queue = (state.queue || []).filter((n) => !deadSet.has(n));
  writeOpeningMalls(loadOpeningMalls().filter((n) => !deadSet.has(n)));
  return dead;
}

export function reapExitedOpenedMalls() {
  const lock = new OpenedLock();
  return lock.with(() => {
    const state = loadOpenedState();
    normalizeInFlight(state);
    const dead = reapDeadOpened(state);
    if (dead.length) saveOpenedState(state);
    return Object.keys(state.opened || {}).length;
  });
}

function readWatchPid() {
  const p = openedWatchPidPath();
  if (!existsSync(p)) return 0;
  try {
    return Number((readFileSync(p, "utf8") || "0").trim() || 0) || 0;
  } catch {
    return 0;
  }
}

export function stopOpenedPortWatcher() {
  const pid = readWatchPid();
  if (pid && pidAlive(pid) && pid !== process.pid) {
    try {
      if (isWin()) {
        spawnSync("taskkill", ["/PID", String(pid), "/F"], {
          windowsHide: true,
          stdio: "ignore",
        });
      } else {
        process.kill(pid, "SIGTERM");
      }
    } catch {
      /* ignore */
    }
  }
  try {
    unlinkSync(openedWatchPidPath());
  } catch {
    /* ignore */
  }
}

export function ensureOpenedPortWatcher() {
  const pid = readWatchPid();
  if (pid && pidAlive(pid)) return;
  const script = path.join(__dirname, "watch_opened_ports.mjs");
  const child = spawn(process.execPath, [script], {
    cwd: __dirname,
    detached: true,
    stdio: "ignore",
    windowsHide: true,
  });
  child.unref();
  writeFileSync(openedWatchPidPath(), String(child.pid), "utf8");
}

export function mallIsOpened(mallName) {
  return new OpenedLock().with(() => {
    const state = loadOpenedState();
    return mallName in (state.opened || {});
  });
}

export function markMallOpened(mallName, mallId, webdriverPort, kernalNumber = null) {
  new OpenedLock().with(() => {
    const state = loadOpenedState();
    const opened = state.opened || (state.opened = {});
    opened[mallName] = {
      mall_id: String(mallId),
      WebDriverPort: Number(webdriverPort),
      KernalNumber: kernalNumber,
      pending: false,
      opened_at: Date.now() / 1000,
    };
    state.queue = (state.queue || []).filter((n) => n !== mallName);
    dropInFlight(state, { mallName });
    state.last_open_finished_at = Date.now() / 1000;
    saveOpenedState(state);
  });
  ensureOpenedPortWatcher();
}

export function noteOpenBrowserDone(mallName, mallId) {
  new OpenedLock().with(() => {
    const state = loadOpenedState();
    const opened = state.opened || (state.opened = {});
    opened[mallName] = {
      mall_id: String(mallId),
      WebDriverPort: 0,
      KernalNumber: null,
      pending: true,
      pending_until: Date.now() / 1000 + PENDING_GRACE_SEC,
    };
    // 持有任务所有权直到取端口成功/失败，防止另一调用释放正在启动的店铺。
    saveOpenedState(state);
  });
}

export function unmarkMallOpened(mallName) {
  new OpenedLock().with(() => {
    const state = loadOpenedState();
    const opened = state.opened || (state.opened = {});
    delete opened[mallName];
    state.queue = (state.queue || []).filter((n) => n !== mallName);
    dropInFlight(state, { mallName });
    saveOpenedState(state);
  });
}

export function clearOpenedMalls() {
  new OpenedLock().with(() => {
    saveOpenedState(emptyOpenedState());
  });
  stopOpenedPortWatcher();
}

export function finishOpenMallRun() {
  new OpenedLock().with(() => {
    const state = loadOpenedState();
    dropInFlight(state, { pid: process.pid });
    saveOpenedState(state);
  });
}

export function waitAndClaimOpenSlot(mallName) {
  while (true) {
    let waitSec = 0;
    const turn = new OpenedLock().with(() => {
      const state = loadOpenedState();
      normalizeInFlight(state);
      reapDeadOpened(state);
      const opened = state.opened || (state.opened = {});
      const info = opened[mallName] && typeof opened[mallName] === "object" ? opened[mallName] : null;
      // OpenBrowser 尚未返回时还没有 opened 记录，也必须阻止并发重复打开。
      if (asFlightList(state.in_flight).some((f) => String(f.mall_name || "") === mallName)) {
        saveOpenedState(state);
        return "reused";
      }
      if (info) {
        let wd = Number(info.WebDriverPort || 0) || 0;
        if (wd && portAlive(wd)) {
          state.queue = (state.queue || []).filter((n) => n !== mallName);
          saveOpenedState(state);
          return "reused";
        }
        if (info.pending || info.hold_without_port || wd <= 0) {
          state.queue = (state.queue || []).filter((n) => n !== mallName);
          saveOpenedState(state);
          return "reused";
        }
      }

      const queue = state.queue || (state.queue = []);
      if (!queue.includes(mallName)) {
        queue.push(mallName);
        state.queue = queue;
        saveOpenedState(state);
      }

      const lastDone = Number(state.last_open_finished_at || 0);
      const gap = lastDone ? OPEN_STAGGER_SEC - (Date.now() / 1000 - lastDone) : 0;
      const busy = openSerialBusy(state);
      const canClaim = queue.length && queue[0] === mallName && gap <= 0 && !busy.length;
      if (canClaim) {
        state.queue = queue.filter((n) => n !== mallName);
        const flights = asFlightList(state.in_flight);
        flights.push({ mall_name: mallName, pid: process.pid });
        state.in_flight = flights;
        saveOpenedState(state);
        return "claimed";
      }
      if (busy.length) waitSec = SLOT_POLL_SEC;
      else if (gap > 0) waitSec = gap;
      saveOpenedState(state);
      return null;
    });
    if (turn) return turn;
    sleep((waitSec > 0 ? waitSec : SLOT_POLL_SEC) * 1000);
  }
}
