#!/usr/bin/env node
/** 打开站斧（WebDriver HTTP）。已打开则复用；未打开则冷启动并轮询就绪。 */
import { existsSync, readdirSync } from "node:fs";
import { spawn, spawnSync } from "node:child_process";
import os from "node:os";
import path from "node:path";
import {
  HTTP_PROBE_TIMEOUT,
  clearOpenedMalls,
  clearOpeningMalls,
  configureStdio,
  emit,
  getAvailablePort,
  isMac,
  isWin,
  loadApiPortState,
  preferredPort,
  saveApiPort,
  saveInstallDir,
  saveMallsToCache,
  sleep,
} from "./zhanfu_http.mjs";

const POLL_INTERVAL_MS = 500;
const WAIT_DEFAULT_SEC = 8;
const KILL_WAIT_MAX_MS = 1000;
const NOT_LOGGED_IN_MSG = "站斧未登录，请提供账号和密码";

const COMM_FAIL_TEMPLATE =
  "站斧启动后 {wait} 秒内未能建立 WebDriver 通讯，已按技能规则停止操作，未重复尝试。\n" +
  "安装位置已确认：{install_path}。请确认站斧版本要求（Windows ≥ 5.2.12，macOS > 5.2.10）无误；" +
  "若电脑因卡顿导致启动有延迟，可尝试再次打开站斧，请告诉我“打开站斧”。";

const NEED_PATH_WIN = "未找到站斧安装目录，请提供站斧安装路径（含 站斧.exe 的文件夹）";
const NEED_PATH_MAC = "未找到站斧.app，请提供路径（如 /Applications/站斧.app）";

async function postBrowserList(port, timeoutSec = HTTP_PROBE_TIMEOUT) {
  const payload = {
    module: "WebDriverModule",
    action: "GetBrowserList",
    args: JSON.stringify({ page: 1, limit: 20 }),
  };
  const ac = new AbortController();
  const timer = setTimeout(() => ac.abort(), Math.max(1, timeoutSec * 1000));
  try {
    const resp = await fetch(`http://127.0.0.1:${port}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: ac.signal,
    });
    const text = (await resp.text()).trim();
    if (!text) return ["foreign", null];
    let data;
    try {
      data = JSON.parse(text);
    } catch {
      return ["foreign", null];
    }
    if (!data || typeof data !== "object" || Array.isArray(data)) return ["foreign", null];
    const isWd =
      data.module === "WebDriverModule" ||
      (data.action && ("returnObj" in data || "ret" in data));
    if (!isWd) return ["foreign", null];
    const ro = data.returnObj || {};
    if (typeof ro === "object" && ro.success === true) {
      const malls = (ro.data || {}).mall_list;
      if (malls != null) return ["logged_in", data];
    }
    return ["not_logged_in", data];
  } catch {
    return ["down", null];
  } finally {
    clearTimeout(timer);
  }
}

function windowsDesktopDirs() {
  const dirs = [];
  const home = os.homedir();
  for (const rel of ["Desktop", "桌面", path.join("OneDrive", "Desktop"), path.join("OneDrive", "桌面")]) {
    const p = path.join(home, rel);
    if (existsSync(p) && !dirs.includes(p)) dirs.push(p);
  }
  const pub = process.env.PUBLIC;
  if (pub) {
    for (const rel of ["Desktop", "桌面"]) {
      const p = path.join(pub, rel);
      if (existsSync(p) && !dirs.includes(p)) dirs.push(p);
    }
  }
  return dirs;
}

function resolveLnkTarget(lnkPath) {
  try {
    const esc = path.resolve(lnkPath).replace(/'/g, "''");
    const ps = `(New-Object -ComObject WScript.Shell).CreateShortcut('${esc}').TargetPath`;
    const r = spawnSync("powershell", ["-NoProfile", "-NoLogo", "-Command", ps], {
      encoding: "utf8",
      windowsHide: true,
      timeout: 15000,
    });
    if (r.status !== 0) return null;
    const t = String(r.stdout || "")
      .trim()
      .replace(/^"|"$/g, "");
    return t && existsSync(t) ? t : null;
  } catch {
    return null;
  }
}

function resolveFromDesktopShortcut() {
  const ordered = [];
  for (const desktop of windowsDesktopDirs()) {
    for (const exact of ["站斧.lnk", "站斧浏览器.lnk"]) {
      const c = path.join(desktop, exact);
      if (existsSync(c)) ordered.push(path.normalize(c));
    }
    try {
      for (const name of readdirSync(desktop)) {
        if (!name.includes("站斧") || !name.toLowerCase().endsWith(".lnk")) continue;
        const np = path.normalize(path.join(desktop, name));
        if (!ordered.includes(np)) ordered.push(np);
      }
    } catch {
      /* ignore */
    }
  }
  const seen = new Set();
  for (const lnk of ordered) {
    if (seen.has(lnk)) continue;
    seen.add(lnk);
    const tgt = resolveLnkTarget(lnk);
    if (!tgt) continue;
    const folder = path.dirname(path.normalize(tgt));
    if (path.basename(tgt).toLowerCase() === "站斧.exe") return [folder, tgt];
    const candidate = path.join(folder, "站斧.exe");
    if (existsSync(candidate)) return [folder, candidate];
  }
  return null;
}

function normalizeMacAppPath(folderPath) {
  const raw = path.normalize(folderPath.trim().replace(/^~(?=\/|\\|$)/, os.homedir()));
  if (raw.endsWith(".app") && existsSync(raw)) return raw;
  const candidate = path.join(raw, "站斧.app");
  if (existsSync(candidate)) return candidate;
  if (raw === "站斧" || raw === "站斧.app" || path.basename(raw) === "站斧" || path.basename(raw) === "站斧.app") {
    return "站斧";
  }
  return null;
}

function resolveZhanfu(folderPath = null) {
  if (folderPath) {
    if (isMac()) {
      const app = normalizeMacAppPath(folderPath);
      if (!app) throw new Error(NEED_PATH_MAC);
      saveInstallDir(app === "站斧" ? folderPath : app);
      return [app === "站斧" ? folderPath : app, app];
    }
    let folder = path.normalize(folderPath.replace(/^~(?=\/|\\|$)/, os.homedir()));
    const exe = folder.toLowerCase().endsWith("站斧.exe") ? folder : path.join(folder, "站斧.exe");
    if (!existsSync(exe)) throw new Error(NEED_PATH_WIN);
    saveInstallDir(path.dirname(exe));
    return [path.dirname(exe), exe];
  }

  const saved = loadApiPortState().install_dir;
  if (saved) {
    if (isMac()) {
      const app = normalizeMacAppPath(String(saved));
      if (app) {
        console.log(`[路径] 从 api_port.json 读取: ${saved}`);
        return [app === "站斧" ? String(saved) : String(saved), app];
      }
    } else {
      const folder = path.normalize(String(saved));
      const exe = path.join(folder, "站斧.exe");
      if (existsSync(exe)) {
        console.log(`[路径] 从 api_port.json 读取: ${folder}`);
        return [folder, exe];
      }
    }
  }

  if (isMac()) {
    for (const app of ["/Applications/站斧.app", path.join(os.homedir(), "Applications", "站斧.app")]) {
      if (existsSync(app)) {
        saveInstallDir(app);
        console.log(`[路径] 命中: ${app}`);
        return [app, app];
      }
    }
    throw new Error(NEED_PATH_MAC);
  }

  const shortcut = resolveFromDesktopShortcut();
  if (shortcut) {
    saveInstallDir(shortcut[0]);
    console.log(`[路径] 从桌面快捷方式解析: ${shortcut[0]}`);
    return shortcut;
  }

  const username = process.env.USERNAME || path.basename(os.homedir());
  for (const folder of [
    path.join("C:\\Users", username, "AppData\\Local\\Programs\\ZhanFu"),
    "C:\\Program Files\\ZhanFu",
  ]) {
    const exe = path.join(folder, "站斧.exe");
    if (existsSync(exe)) {
      saveInstallDir(folder);
      console.log(`[路径] 命中: ${folder}`);
      return [folder, exe];
    }
  }
  throw new Error(NEED_PATH_WIN);
}

function killZhanfu() {
  if (isWin()) {
    console.log("[杀进程] taskkill 站斧.exe");
    spawnSync("taskkill", ["/f", "/t", "/im", "站斧.exe"], { windowsHide: true, stdio: "ignore" });
    const deadline = Date.now() + KILL_WAIT_MAX_MS;
    while (Date.now() < deadline) {
      const r = spawnSync("tasklist", ["/FI", "IMAGENAME eq 站斧.exe"], {
        encoding: "utf8",
        windowsHide: true,
      });
      if (!String(r.stdout || "").includes("站斧.exe")) break;
      sleep(200);
    }
  } else if (isMac()) {
    console.log("[杀进程] killall 站斧");
    spawnSync("killall", ["站斧"], { stdio: "ignore" });
    sleep(Math.min(KILL_WAIT_MAX_MS, 1000));
  }
}

function startZhanfu(exePath, apiPort) {
  if (isMac()) {
    const cmd = [
      "open",
      "-a",
      exePath,
      "--args",
      "--multip",
      "--run_type=web_driver",
      "--ipc_type=http",
      `--httpport=${apiPort}`,
    ];
    spawn(cmd[0], cmd.slice(1), { detached: true, stdio: "ignore" }).unref();
    console.log(
      `[启动] open -a ${exePath} --multip --run_type=web_driver --ipc_type=http --httpport=${apiPort}`
    );
    return;
  }
  if (!existsSync(exePath)) throw new Error(`未找到站斧: ${exePath}`);
  // 禁止 windowsHide：否则站斧主窗口不会显示（Python 版 Popen 默认有界面）
  spawn(
    exePath,
    ["--multip", "--run_type=web_driver", "--ipc_type=http", `--httpport=${apiPort}`],
    { cwd: path.dirname(exePath) || undefined, detached: true, stdio: "ignore", windowsHide: false }
  ).unref();
  console.log(`[启动] 站斧.exe --multip --run_type=web_driver --ipc_type=http --httpport=${apiPort}`);
}

async function pollReady(port, waitSec) {
  const deadline = Date.now() + waitSec * 1000;
  let last = "down";
  let data = null;
  while (Date.now() < deadline) {
    [last, data] = await postBrowserList(port);
    if (last === "logged_in" || last === "not_logged_in") return [last, data];
    sleep(POLL_INTERVAL_MS);
  }
  return [last, data];
}

async function doLogin(port, username, password) {
  const payload = {
    module: "WebDriverModule",
    action: "Login",
    args: JSON.stringify({ username, password, isboss: true }),
  };
  try {
    const resp = await fetch(`http://127.0.0.1:${port}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(8000),
    });
    const data = await resp.json();
    const ro = data.returnObj || {};
    if (typeof ro === "object" && ro.success === true) return [true, ""];
    const msg = typeof ro === "object" ? String(ro.msg || "") : "";
    return [false, msg || JSON.stringify(data)];
  } catch (exc) {
    return [false, String(exc.message || exc)];
  }
}

function parseArgs(argv) {
  let folderPath = "";
  let waitSeconds = WAIT_DEFAULT_SEC;
  let username = "";
  let password = "";
  for (let i = 2; i < argv.length; i++) {
    if (argv[i] === "--folder-path" && argv[i + 1]) folderPath = argv[++i];
    else if (argv[i] === "--wait-seconds" && argv[i + 1]) waitSeconds = Number(argv[++i]);
    else if (argv[i] === "--username" && argv[i + 1]) username = argv[++i];
    else if (argv[i] === "--password" && argv[i + 1]) password = argv[++i];
  }
  return { folderPath, waitSeconds, username, password };
}

async function main() {
  configureStdio();
  const ns = parseArgs(process.argv);

  if (!isWin() && !isMac()) {
    console.error("仅支持 Windows / macOS");
    return emit({ ok: false, status: "unsupported_os" }, 1);
  }

  let port = preferredPort();
  let [status, data] = await postBrowserList(port);
  console.log(`[探测] api_port=${port} status=${status}`);

  if (status === "logged_in") {
    saveApiPort(port);
    const malls = ((data || {}).returnObj || {}).data || {};
    saveMallsToCache(malls.mall_list || []);
    console.log("站斧已打开且已登录。");
    return emit({ ok: true, status: "already_open", api_port: port }, 0);
  }

  if (status === "not_logged_in") {
    saveApiPort(port);
    if (ns.username && ns.password) {
      const [ok, msg] = await doLogin(port, ns.username, ns.password);
      if (!ok) {
        console.log(msg || "Login 失败");
        return emit({ ok: false, status: "login_failed", api_port: port, msg }, 1);
      }
      const [st2, data2] = await postBrowserList(port);
      if (st2 === "logged_in") {
        const malls = ((data2 || {}).returnObj || {}).data || {};
        saveMallsToCache(malls.mall_list || []);
        console.log("站斧已登录。");
        return emit({ ok: true, status: "logged_in", api_port: port }, 0);
      }
    }
    console.log(NOT_LOGGED_IN_MSG);
    return emit({ ok: false, status: "need_login", api_port: port, msg: NOT_LOGGED_IN_MSG }, 2);
  }

  clearOpeningMalls();
  clearOpenedMalls();

  let folder;
  let exe;
  try {
    [folder, exe] = resolveZhanfu(ns.folderPath || null);
  } catch (exc) {
    console.log(String(exc.message || exc));
    return emit({ ok: false, status: "need_install_path", msg: String(exc.message || exc) }, 3);
  }

  killZhanfu();
  const apiPort = getAvailablePort(port);
  if (apiPort !== port) console.log(`[端口] ${port} 已被占用，改用空闲端口 ${apiPort}`);
  startZhanfu(exe, apiPort);

  const wait = Math.max(0.5, Number(ns.waitSeconds) || WAIT_DEFAULT_SEC);
  [status, data] = await pollReady(apiPort, wait);
  const installPath = exe;
  if (status !== "logged_in" && status !== "not_logged_in") {
    const waitLabel = wait === Math.floor(wait) ? String(Math.floor(wait)) : String(wait);
    const text = COMM_FAIL_TEMPLATE.replace("{wait}", waitLabel).replace("{install_path}", installPath);
    console.log(text);
    return emit(
      {
        ok: false,
        status: "comm_fail",
        api_port: apiPort,
        install_path: installPath,
        msg: text,
      },
      4
    );
  }

  saveApiPort(apiPort, isWin() ? folder : exe);
  if (status === "logged_in") {
    const malls = ((data || {}).returnObj || {}).data || {};
    saveMallsToCache(malls.mall_list || []);
    console.log("站斧已打开且已登录。");
    return emit({ ok: true, status: "started", api_port: apiPort, install_path: installPath }, 0);
  }

  if (ns.username && ns.password) {
    const [ok, msg] = await doLogin(apiPort, ns.username, ns.password);
    if (!ok) {
      console.log(msg || "Login 失败");
      return emit({ ok: false, status: "login_failed", api_port: apiPort, msg }, 1);
    }
    const [st2, data2] = await pollReady(apiPort, Math.min(8, wait));
    if (st2 === "logged_in") {
      const malls = ((data2 || {}).returnObj || {}).data || {};
      saveMallsToCache(malls.mall_list || []);
      console.log("站斧已打开且已登录。");
      return emit({ ok: true, status: "started", api_port: apiPort }, 0);
    }
  }

  console.log(NOT_LOGGED_IN_MSG);
  return emit({ ok: false, status: "need_login", api_port: apiPort, msg: NOT_LOGGED_IN_MSG }, 2);
}

process.exit(await main());
