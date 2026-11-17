#!/usr/bin/env node
/**
 * run-mcp.mjs — REA-CN 付费版 · MCP 服务器启动入口（WorkBuddy mcp.json 指向此文件）
 *
 * 与免费版的差异：启动前【强制付费闸】——
 *   1. 校验 engine/.entitlement.json（付费放行凭证，由 pay-gate.mjs 履约后登记）。
 *      缺失/无效/已过期（单次付费 24h 有效期）→ 拒绝启动并指引走付费/续费流程（exit 65）。
 *      —— 此即 SKILL.md「执行路径强制条款」的代码落实：引擎只能经付费关口放行后调用。
 *   2. entitlement 有效 → 若 engine/dist 缺失则从 engine.zip 解压（四路兜底）。
 *   3. 检查 engine/node_modules 依赖（哨兵齐全即就绪）；缺失 → 自动走 npmmirror 安装。
 *   4. 以 stdio 方式启动 rea-agents MCP 服务器并透传 stdio。
 *
 * 仅使用 Node 内置模块 + 同目录模块。语法可通过 `node --check` 校验。
 */
import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve, join } from "node:path";
import { depsReady, installDeps } from "./cn-installer.mjs";
import { readEntitlement, entitlementStatus, entitlementExpiresAt, extractZip, ensureEngineZip, readSkillConfig } from "./lib/engine-assets.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = resolve(__dirname, "..");
const ENGINE_DIR = join(SKILL_ROOT, "engine");
const ENGINE_ZIP = join(SKILL_ROOT, "engine.zip");

const EXIT_NOT_ENTITLED = 65;

function boot() {
  const child = spawn(
    process.execPath,
    [join(ENGINE_DIR, "scripts", "rea.mjs"), "mcp"],
    {
      cwd: ENGINE_DIR,
      env: { ...process.env, REA_PACKAGE_VERSION: "6.4.0" },
      stdio: ["inherit", "inherit", "inherit"],
    }
  );

  const forward = (sig) => {
    if (!child.killed) child.kill(sig);
  };
  process.on("SIGINT", () => forward("SIGINT"));
  process.on("SIGTERM", () => forward("SIGTER"));

  child.on("exit", (code, signal) => {
    process.exit(code ?? (signal ? 1 : 0));
  });
  child.on("error", (err) => {
    console.error(`[run-mcp] 启动引擎失败: ${err.message}`);
    process.exit(1);
  });
}

function main() {
  const cfg = readSkillConfig();
  const ttlHours = (cfg.paid || {}).entitlementTtlHours || 24;

  // ---- 付费闸：无 entitlement / 已过期一律拒绝启动（写死，无开关）----
  const ent = readEntitlement(ENGINE_DIR);
  const st = entitlementStatus(ent, ttlHours);
  if (st !== "ENTITLED") {
    if (st === "EXPIRED") {
      const exp = entitlementExpiresAt(ent, ttlHours);
      console.error([
        "[run-mcp] ⛔ 付费已过期（单次 ¥1.9 的有效期为 " + ttlHours + " 小时" +
          (exp ? "，本凭证到期于 " + exp.toISOString() : "") + "）。",
        "[run-mcp] 按 SkillHub 单次付费规则，24 小时后需重新付费。请执行：node scripts/pay-gate.mjs",
        "[run-mcp]   → 收到 402 后向用户展示免费 preview，再以 paymentCode 调用 weixinpay_pay 完成新的 ¥1.9 支付，",
        "[run-mcp]   → 支付成功后执行：node scripts/pay-gate.mjs --resume <新的 outTradeNo>",
      ].join("\n"));
    } else if (st === "FORGED") {
      console.error([
        "[run-mcp] ⛔ 本地权益凭证未通过服务端 Ed25519 签名校验（缺失签名 / 被篡改 / 跨产品复用）。",
        "[run-mcp] 凭证由服务端私钥签发，本地只有公钥（可验不可伪造），手写或修改到期时间均无效。",
        "[run-mcp] 请执行：node scripts/pay-gate.mjs 完成 ¥1.9 付费，拿到服务端签发的新凭证。",
      ].join("\n"));
    } else {
      console.error([
        "[run-mcp] ⛔ 未检测到付费放行凭证（engine/.entitlement.json）。",
        "[run-mcp] 按本技能「执行路径强制条款」，引擎只能经付费关口放行后调用。",
        "[run-mcp] 请先执行：node scripts/pay-gate.mjs",
        "[run-mcp]   → 收到 402 后向用户展示免费 preview，再以 paymentCode 调用 weixinpay_pay 完成 ¥1.9 支付，",
        "[run-mcp]   → 支付成功后执行：node scripts/pay-gate.mjs --resume <outTradeNo>",
      ].join("\n"));
    }
    process.exit(EXIT_NOT_ENTITLED);
  }
  const exp = entitlementExpiresAt(ent, ttlHours);
  console.error(`[run-mcp] 付费放行凭证有效（订单 ${ent.out_trade_no}，登记于 ${ent.granted_at}` +
    (exp ? `，${ttlHours}h 有效期至 ${exp.toISOString()}` : "") + "）");

  // ---- 引擎就位：entitlement 有效后才允许解压 ----
  const engineEntry = join(ENGINE_DIR, "scripts", "rea.mjs");
  if (!existsSync(engineEntry)) {
    if (!existsSync(ENGINE_ZIP)) {
      // 纯文本包无本地 zip：先试包内 base64 分片重建，再指引走网关/npm 兜底
      const rebuilt = ensureEngineZip(SKILL_ROOT, (cfg.paid || {}).engineZipSha256 || "");
      if (!rebuilt.ok) {
        console.error("[run-mcp] engine/ 缺失且本地无 engine.zip（纯文本包不含引擎二进制）。");
        console.error("[run-mcp] 请执行：node scripts/pay-gate.mjs --resume " + ent.out_trade_no + " --refresh 从官网网关下载并解压引擎；");
        console.error("[run-mcp] 或网关不可达时执行：node scripts/cn-installer.mjs --engine 从 npmmirror 安装引擎本体。");
        process.exit(1);
      }
      console.error(`[run-mcp] 已从包内 engine-b64 文本分片重建 engine.zip（${rebuilt.size} B）`);
    }
    console.error("[run-mcp] 检测到 engine/ 缺失，正在从 engine.zip 解压…");
    const ex = extractZip(ENGINE_ZIP, SKILL_ROOT);
    if (!ex.ok) {
      console.error(`[run-mcp] 解压失败: ${ex.error}`);
      process.exit(1);
    }
    console.error(`[run-mcp] 引擎已解压（via ${ex.via}）`);
  }

  // ---- 依赖查缺补漏 ----
  if (!depsReady(ENGINE_DIR)) {
    console.error("[run-mcp] 检测到 engine/node_modules 缺失，正在自动安装依赖（npmmirror）…");
    const code = installDeps();
    if (code !== 0) {
      console.error("[run-mcp] 依赖安装失败，无法启动。请检查网络或手动运行 `node scripts/cn-installer.mjs`。");
      process.exit(code || 1);
    }
  } else {
    console.error("[run-mcp] 依赖已就绪，启动 REA MCP 服务器。");
  }
  boot();
}

main();
