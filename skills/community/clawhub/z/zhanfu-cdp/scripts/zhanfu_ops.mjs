#!/usr/bin/env node
/** 创建店铺 / 改账号 / 下载目录 / 插件 / 清缓存。 */
import { ensureDeps } from "./ensure_deps.mjs";
ensureDeps();

import {
  call,
  clearOpenedMalls,
  clearOpeningMalls,
  configureStdio,
  emit,
  emitZhanfuDown,
  getMallByName,
  HttpError,
  isMac,
  removeOpeningMall,
  resolveMallId,
  resolveMallIdRefreshOnce,
  sleep,
  tryPreferredPort,
  unmarkMallOpened,
} from "./zhanfu_http.mjs";

function needWin(action) {
  if (isMac()) {
    console.log(`macOS 暂不支持 ${action}`);
    return emit({ ok: false, status: "macos_unsupported", action }, 1);
  }
  return null;
}

function argValue(argv, name) {
  const i = argv.indexOf(name);
  if (i >= 0 && argv[i + 1] != null) return argv[i + 1];
  return undefined;
}

function argAll(argv, name) {
  const out = [];
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === name && argv[i + 1] != null) out.push(argv[++i]);
  }
  return out;
}

function hasFlag(argv, name) {
  return argv.includes(name);
}

async function cmdCreate(ns) {
  if (!ns.mallName || !ns.platform) {
    console.log("创建店铺需要 --mall-name 与 --platform");
    return emit({ ok: false, status: "missing_args" }, 1);
  }
  if (ns.platform === "自定义平台" && !ns.platformUrl) {
    console.log("自定义平台必须提供 --platform-url");
    return emit({ ok: false, status: "missing_platform_url" }, 1);
  }
  const params = {
    mall_name: ns.mallName,
    mall_account: ns.mallAccount || "",
    mall_password: ns.mallPassword || "",
    platform: ns.platform,
    platform_url: ns.platformUrl || "",
    mall_address: ns.mallAddress || "",
    tags: ns.tags || "",
    authorizationMember: ns.authorizationMember || "",
    ip_content: ns.ipContent || "",
    browser_kernel_version: ns.browserKernelVersion,
    window_ua: "",
    mac_ua: "",
    android_ua: "",
    remark: ns.remark || "",
  };
  const port = tryPreferredPort();
  if (port == null) return emitZhanfuDown();
  let data;
  try {
    data = await call("CreateBrowser", {
      args: JSON.stringify(params),
      timeout: 30,
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
    return emit({ ok: false, status: "create_failed", msg: String(msg) }, 1);
  }
  console.log("创建成功，等待列表同步 8s");
  sleep(8000);
  const mallId = await getMallByName(ns.mallName, port);
  console.log(`店铺 ${ns.mallName} 已创建。mall_id=${mallId}`);
  return emit({ ok: true, status: "created", mall_name: ns.mallName, mall_id: mallId }, 0);
}

async function cmdUpdateAccount(ns) {
  if (ns.username === undefined && ns.password === undefined) {
    console.log("请提供 --username 和/或 --password（可显式传空字符串）");
    return emit({ ok: false, status: "missing_args" }, 1);
  }
  const port = tryPreferredPort();
  if (port == null) return emitZhanfuDown();
  let mallId = await resolveMallId(ns.mallName, { port });
  const body = {
    username: ns.username === undefined ? "" : ns.username,
    password: ns.password === undefined ? "" : ns.password,
  };
  let data = await call("UpdateAccount", {
    browserId: mallId,
    args: JSON.stringify(body),
    timeout: 15,
    port,
  });
  let ro = data.returnObj || {};
  if (typeof ro !== "object" || ro.success !== true) {
    mallId = await resolveMallIdRefreshOnce(ns.mallName, port);
    data = await call("UpdateAccount", {
      browserId: mallId,
      args: JSON.stringify(body),
      timeout: 15,
      port,
    });
    ro = data.returnObj || {};
  }
  if (typeof ro !== "object" || ro.success !== true) {
    const msg = typeof ro === "object" ? ro.msg : data;
    console.log(String(msg));
    return emit({ ok: false, status: "update_failed", msg: String(msg) }, 1);
  }
  console.log(`已修改店铺 ${ns.mallName} 账号密码。mall_id=${mallId}`);
  return emit({ ok: true, status: "updated", mall_id: mallId }, 0);
}

async function cmdDownload(ns) {
  const blocked = needWin("SetDownLoadPath");
  if (blocked != null) return blocked;
  if (!ns.filePath) {
    console.log("需要 --file-path");
    return emit({ ok: false, status: "missing_args" }, 1);
  }
  const port = tryPreferredPort();
  if (port == null) return emitZhanfuDown();
  const data = await call("SetDownLoadPath", {
    args: JSON.stringify({ FilePath: ns.filePath }),
    timeout: 15,
    port,
  });
  const ro = data.returnObj || {};
  if (typeof ro !== "object" || ro.success !== true) {
    const msg = typeof ro === "object" ? ro.msg : data;
    console.log(String(msg));
    return emit({ ok: false, status: "failed", msg: String(msg) }, 1);
  }
  console.log(`已设置下载目录: ${ns.filePath}`);
  return emit({ ok: true, status: "ok", FilePath: ns.filePath }, 0);
}

async function cmdPlugins(ns) {
  const blocked = needWin("SetInstallPlugins");
  if (blocked != null) return blocked;
  let plugins;
  if (ns.clear) {
    plugins = [];
  } else {
    const names = ns.pluginName || [];
    if (!names.length) {
      console.log("需要 --plugin-name，或使用 --clear 清空");
      return emit({ ok: false, status: "missing_args" }, 1);
    }
    const chromeIds = ns.chromeId || [];
    plugins = names.map((name, i) => {
      const item = { plugin_name: name };
      if (i < chromeIds.length) item.chrome_id = chromeIds[i];
      return item;
    });
  }
  const port = tryPreferredPort();
  if (port == null) return emitZhanfuDown();
  const data = await call("SetInstallPlugins", {
    args: JSON.stringify({ installPlugins: plugins }),
    timeout: 15,
    port,
  });
  const ro = data.returnObj || {};
  if (typeof ro !== "object" || ro.success !== true) {
    const msg = typeof ro === "object" ? ro.msg : data;
    console.log(String(msg));
    return emit({ ok: false, status: "failed", msg: String(msg) }, 1);
  }
  console.log("已设置店铺插件列表。");
  return emit({ ok: true, status: "ok", installPlugins: plugins }, 0);
}

async function cmdClearCache(ns) {
  if (ns.all) {
    const blocked = needWin("ClearCacheFolder");
    if (blocked != null) return blocked;
    const port = tryPreferredPort();
    if (port == null) return emitZhanfuDown();
    const data = await call("ClearCacheFolder", { args: "{}", timeout: 30, port });
    const ro = data.returnObj || {};
    if (typeof ro !== "object" || ro.success !== true) {
      const msg = typeof ro === "object" ? ro.msg : data;
      console.log(String(msg));
      return emit({ ok: false, status: "failed", msg: String(msg) }, 1);
    }
    clearOpeningMalls();
    clearOpenedMalls();
    console.log("已清除全部店铺缓存。");
    return emit({ ok: true, status: "cleared_all" }, 0);
  }

  const blocked = needWin("ClearCache");
  if (blocked != null) return blocked;
  if (!ns.mallName) {
    console.log("单店清缓存需要 --mall-name，或使用 --all");
    return emit({ ok: false, status: "missing_args" }, 1);
  }
  const port = tryPreferredPort();
  if (port == null) return emitZhanfuDown();
  let mallId = await resolveMallId(ns.mallName, { port });
  let data = await call("ClearCache", { browserId: mallId, args: "", timeout: 30, port });
  let ro = data.returnObj || {};
  if (typeof ro !== "object" || ro.success !== true) {
    mallId = await resolveMallIdRefreshOnce(ns.mallName, port);
    data = await call("ClearCache", { browserId: mallId, args: "", timeout: 30, port });
    ro = data.returnObj || {};
  }
  if (typeof ro !== "object" || ro.success !== true) {
    const msg = typeof ro === "object" ? ro.msg : data;
    console.log(String(msg));
    return emit({ ok: false, status: "failed", msg: String(msg) }, 1);
  }
  removeOpeningMall(ns.mallName);
  unmarkMallOpened(ns.mallName);
  console.log(`已清除店铺 ${ns.mallName} 缓存。mall_id=${mallId}`);
  return emit({ ok: true, status: "cleared", mall_id: mallId }, 0);
}

async function main() {
  configureStdio();
  const argv = process.argv.slice(2);
  const cmd = argv[0];
  const rest = argv.slice(1);

  if (cmd === "create-mall") {
    return cmdCreate({
      mallName: argValue(rest, "--mall-name"),
      platform: argValue(rest, "--platform"),
      platformUrl: argValue(rest, "--platform-url") || "",
      ipContent: argValue(rest, "--ip-content") || "",
      mallAccount: argValue(rest, "--mall-account") || "",
      mallPassword: argValue(rest, "--mall-password") || "",
      mallAddress: argValue(rest, "--mall-address") || "",
      tags: argValue(rest, "--tags") || "",
      authorizationMember: argValue(rest, "--authorization-member") || "",
      browserKernelVersion: Number(argValue(rest, "--browser-kernel-version") || 0),
      remark: argValue(rest, "--remark") || "",
    });
  }
  if (cmd === "update-account") {
    const hasUser = rest.includes("--username");
    const hasPass = rest.includes("--password");
    return cmdUpdateAccount({
      mallName: argValue(rest, "--mall-name"),
      username: hasUser ? (argValue(rest, "--username") ?? "") : undefined,
      password: hasPass ? (argValue(rest, "--password") ?? "") : undefined,
    });
  }
  if (cmd === "set-download") {
    return cmdDownload({ filePath: argValue(rest, "--file-path") });
  }
  if (cmd === "set-plugins") {
    return cmdPlugins({
      pluginName: argAll(rest, "--plugin-name"),
      chromeId: argAll(rest, "--chrome-id"),
      clear: hasFlag(rest, "--clear"),
    });
  }
  if (cmd === "clear-cache") {
    return cmdClearCache({
      mallName: argValue(rest, "--mall-name") || "",
      all: hasFlag(rest, "--all"),
    });
  }
  console.error(
    "用法: zhanfu_ops.mjs <create-mall|update-account|set-download|set-plugins|clear-cache> ..."
  );
  return 1;
}

process.exit(await main());
