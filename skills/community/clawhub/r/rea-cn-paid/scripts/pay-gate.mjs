#!/usr/bin/env node
/**
 * pay-gate.mjs — REA-CN 付费闸（SkillHub 付费版唯一付费入口）
 *
 * 计费规则（SkillHub Pay Skill）：单次付费 ¥1.9，**付费后 24 小时内不限次使用（免验证）**，
 * 过期后需重新付费。服务端在履约响应中下发 expires_at（权威到期时间），本地 entitlement 同步登记。
 *
 * 调用方（Agent）按以下顺序使用：
 *   1) node scripts/pay-gate.mjs [--query "<分析目标简述>"]
 *        → 未解锁/已过期时向网关发起请求，收到 402 后向 Agent 输出支付指令 JSON（exit 42）：
 *          {paymentCode, outTradeNo, amount, preview}
 *        Agent 须先向用户展示 preview（免费预览），再以 paymentCode 调用
 *        weixinpay_pay 插件完成 ¥1.9 支付。
 *   2) node scripts/pay-gate.mjs --resume <outTradeNo>
 *        → 支付完成后重发请求履约：校验支付 → 下载/校验/解压引擎 →
 *          登记 entitlement（含 expires_at）（exit 0）
 *   3) node scripts/run-mcp.mjs
 *        → 启动入口校验 entitlement（含 24h 时效）后启动引擎。
 *
 * 状态查询：
 *   node scripts/pay-gate.mjs --status   → exit 0=已解锁(24h内) / 44=未解锁 / 45=已过期需续费
 *
 * 退出码：0=成功/已解锁  42=需支付(PAYMENT_REQUIRED)  43=未支付(NOT_PAID)
 *        44=未解锁(NOT_ENTITLED)  45=已过期(EXPIRED，需重新付费)  1=错误
 *
 * 仅使用 Node 内置模块 + 共享 engine-assets 模块。语法可通过 `node --check` 校验。
 */
import { createHash } from "node:crypto";
import { existsSync, writeFileSync, readdirSync } from "node:fs";
import { join, dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import {
  sha256File, extractZip, readEntitlement, writeEntitlement,
  entitlementValid, entitlementStatus, entitlementExpiresAt, ensureEngineZip, readSkillConfig,
  verifyEntitlementSignature,
} from "./lib/engine-assets.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = resolve(__dirname, "..");
const ENGINE_DIR = join(SKILL_ROOT, "engine");
const ENGINE_ZIP = join(SKILL_ROOT, "engine.zip");

const EXIT = { OK: 0, PAYMENT_REQUIRED: 42, NOT_PAID: 43, NOT_ENTITLED: 44, EXPIRED: 45, ERROR: 1 };

function out(obj) {
  process.stdout.write(JSON.stringify(obj, null, 2) + "\n");
}

function parseArgs(argv) {
  const args = { resume: null, query: null, status: false, refresh: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--resume") args.resume = argv[++i];
    else if (a === "--query") args.query = argv[++i];
    else if (a === "--status") args.status = true;
    else if (a === "--refresh") args.refresh = true; // 强制重新下载引擎（已付费）
  }
  return args;
}

/** 从参数或当前目录推断分析目标描述（用于网关 preview 与订单记录） */
function inferQuery(explicit) {
  if (explicit && explicit.trim()) return explicit.trim();
  try {
    const files = readdirSync(process.cwd());
    const pick = files.filter(f => /\.(apk|ipa|exe|dll|elf|bin|js|mjs|ts|zip|jar)$/i.test(f));
    if (pick.length) return `本地目标文件：${pick.slice(0, 3).join("、")}`;
  } catch { /* ignore */ }
  return "REA-CN 逆向工程审计（用户未指定具体目标）";
}

async function callGateway(base, body, tradeNo) {
  const headers = { "Content-Type": "application/json" };
  if (tradeNo) headers["X-Out-Trade-No"] = tradeNo;
  const resp = await fetch(base + "/api/resource", {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });
  let data = {};
  try { data = await resp.json(); } catch { /* ignore */ }
  return { status: resp.status, data };
}

/** 下载引擎 zip 并校验 + 解压 + 登记 entitlement（含服务端 expires_at 24h 时效） */
async function fulfill(base, outTradeNo, expectedSha, refresh, ttlHours) {
  // 1) 带单号重发 → 200 放行权益
  const { status, data } = await callGateway(base, { query: "fulfill" }, outTradeNo);
  if (status === 402) {
    out({ code: "NOT_PAID", outTradeNo, message: data.message || "订单尚未支付完成",
          hint: "如用户已完成支付，请稍后重试；未支付请先调用 weixinpay_pay。" });
    return EXIT.NOT_PAID;
  }
  if (status === 410) {
    // 订单过期（超过 24h）或已退款：按单次付费规则必须重新付费
    const code = data.code === "REFUNDED" ? "REFUNDED" : "ORDER_EXPIRED";
    out({ code, outTradeNo, message: data.message || "订单已过期或已退款",
          hint: "单次付费有效期为 24 小时。请重新执行：node scripts/pay-gate.mjs 发起新的付费。" });
    return EXIT.EXPIRED;
  }
  if (status !== 200 || data.code !== "SUCCESS") {
    out({ code: "ERROR", outTradeNo, message: data.message || `网关返回 HTTP ${status}` });
    return EXIT.ERROR;
  }

  const content = data.content || {};
  const downloadUrl = content.download_url;
  const engineSha = content.engine_sha256 || expectedSha;
  const expiresAt = data.expires_at || "";
  const signature = data.entitlement_signature || "";
  if (!downloadUrl) {
    out({ code: "ERROR", outTradeNo, message: "网关未返回 download_url" });
    return EXIT.ERROR;
  }

  // 2) 准备引擎 zip：优先用包内 base64 分片重建（自包含包，无需联网）；否则从网关下载
  const localOk = existsSync(ENGINE_ZIP) && (!expectedSha || sha256File(ENGINE_ZIP) === expectedSha);
  if (refresh || !localOk) {
    const rebuilt = ensureEngineZip(SKILL_ROOT, expectedSha);
    if (rebuilt.ok) {
      process.stderr.write(rebuilt.via === "chunks"
        ? "[pay-gate] 已从包内 engine-b64 文本分片重建 engine.zip（无需联网下载）\n"
        : "[pay-gate] 本地 engine.zip 已存在且校验通过，跳过下载\n");
    } else {
      process.stderr.write(`[pay-gate] 正在从网关下载引擎（${downloadUrl.slice(0, 64)}…）\n`);
      const resp = await fetch(downloadUrl);
      if (!resp.ok) {
        out({ code: "ERROR", outTradeNo, message: `引擎下载失败 HTTP ${resp.status}（链接 10 分钟有效，过期请重新 --resume）` });
        return EXIT.ERROR;
      }
      const buf = Buffer.from(await resp.arrayBuffer());
      const got = createHashSha(buf);
      if (engineSha && got !== engineSha) {
        out({ code: "ERROR", outTradeNo, message: `SHA256 校验失败：期望 ${engineSha.slice(0, 16)}… 实得 ${got.slice(0, 16)}…` });
        return EXIT.ERROR;
      }
      writeFileSync(ENGINE_ZIP, buf);
      process.stderr.write(`[pay-gate] 引擎下载完成并校验通过（${(buf.length / 1048576).toFixed(2)} MB）\n`);
    }
  } else {
    process.stderr.write("[pay-gate] 本地 engine.zip 已存在且校验通过，跳过下载\n");
  }

  // 3) 解压到 engine/
  const ex = extractZip(ENGINE_ZIP, SKILL_ROOT);
  if (!ex.ok) {
    out({ code: "ERROR", outTradeNo, message: `解压失败: ${ex.error}` });
    return EXIT.ERROR;
  }
  process.stderr.write(`[pay-gate] 引擎已解压到 engine/（via ${ex.via}）\n`);

  // 4) 登记 entitlement（单次付费 24h 有效；expires_at 与 signature 均由服务端签发）
  const ent = writeEntitlement(ENGINE_DIR, {
    out_trade_no: outTradeNo,
    transaction_id: data.transaction_id || "",
    amount_fen: 190,
    engine_sha256: engineSha,
    gateway: base,
    ...(expiresAt ? { expires_at: expiresAt } : {}),
    ...(signature ? { signature, signature_alg: data.entitlement_signature_alg || "Ed25519" } : {}),
  });
  if (signature && !verifyEntitlementSignature(ent)) {
    out({ code: "ERROR", outTradeNo, message: "服务端签发的权益凭证签名校验失败，请重新 --resume 或联系服务方" });
    return EXIT.ERROR;
  }
  const exp = entitlementExpiresAt(ent, ttlHours);
  out({ code: "SUCCESS", outTradeNo, entitlement: ent,
        expires_at: exp ? exp.toISOString() : null,
        ttl_hours: ttlHours,
        message: `付费已放行：引擎已就位，可执行 node scripts/run-mcp.mjs 启动。单次付费 ${ttlHours} 小时内不限次使用，到期需重新付费。` });
  return EXIT.OK;
}

function createHashSha(buf) {
  return createHash("sha256").update(buf).digest("hex");
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const cfg = readSkillConfig();
  const paid = cfg.paid || {};
  // REA402_BASE 环境变量可覆盖配置（用于本地联调/测试）
  const base = (process.env.REA402_BASE || paid.gatewayBase || "https://www.ontoagent.net/rea402").replace(/\/+$/, "");
  const expectedSha = paid.engineZipSha256 || "";
  const ttlHours = paid.entitlementTtlHours || 24;

  // --status：只查解锁状态（ENTITLED / EXPIRED / NOT_ENTITLED）
  if (args.status) {
    const ent = readEntitlement(ENGINE_DIR);
    const st = entitlementStatus(ent, ttlHours);
    if (st === "ENTITLED") {
      const exp = entitlementExpiresAt(ent, ttlHours);
      out({ code: "ENTITLED", outTradeNo: ent.out_trade_no, granted_at: ent.granted_at,
            expires_at: exp ? exp.toISOString() : null, ttl_hours: ttlHours,
            message: `已解锁，可直接执行 node scripts/run-mcp.mjs 启动引擎（${ttlHours} 小时内不限次使用，到期需重新付费）。` });
      return EXIT.OK;
    }
    if (st === "EXPIRED") {
      const exp = entitlementExpiresAt(ent, ttlHours);
      out({ code: "EXPIRED", outTradeNo: ent.out_trade_no,
            expired_at: exp ? exp.toISOString() : null, ttl_hours: ttlHours,
            message: `单次付费 ${ttlHours} 小时有效期已过，需重新付费：请执行 node scripts/pay-gate.mjs。` });
      return EXIT.EXPIRED;
    }
    if (st === "FORGED") {
      out({ code: "FORGED",
            message: "本地权益凭证未通过服务端签名校验（凭证缺失签名、被篡改或跨产品复用）。"
                     + "请执行 node scripts/pay-gate.mjs 完成 ¥1.9 付费后重新签发凭证。" });
      return EXIT.NOT_ENTITLED;
    }
    out({ code: "NOT_ENTITLED", message: "尚未解锁：请先执行 node scripts/pay-gate.mjs 完成 ¥1.9 付费。" });
    return EXIT.NOT_ENTITLED;
  }

  // --resume：支付完成后履约
  if (args.resume) {
    const ent0 = readEntitlement(ENGINE_DIR);
    // 24h 免验证：本地权益有效且非强制刷新时，不再打扰网关
    if (!args.refresh && entitlementValid(ent0, ttlHours)) {
      out({ code: "ENTITLED", outTradeNo: ent0.out_trade_no,
            message: `已解锁且在 ${ttlHours} 小时有效期内（免验证），可直接执行 node scripts/run-mcp.mjs 启动引擎。` });
      return EXIT.OK;
    }
    return await fulfill(base, args.resume, expectedSha, args.refresh, ttlHours);
  }

  // 已解锁且在有效期内 → 直接放行（24h 内免验证，不再发起付费）
  const ent = readEntitlement(ENGINE_DIR);
  const st = entitlementStatus(ent, ttlHours);
  if (st === "ENTITLED") {
    const exp = entitlementExpiresAt(ent, ttlHours);
    out({ code: "ENTITLED", outTradeNo: ent.out_trade_no,
          expires_at: exp ? exp.toISOString() : null,
          message: `已解锁（${ttlHours} 小时内不限次使用），可直接执行 node scripts/run-mcp.mjs 启动引擎。` });
    return EXIT.OK;
  }

  // 发起付费：POST /api/resource → 402（未解锁或已过期都走新的单次付费）
  const query = inferQuery(args.query);
  const { status, data } = await callGateway(base, { query, lang: "zh" });
  if (status === 402 && data.code === "PAYMENT_REQUIRED") {
    const wx = data.WeixinPay || {};
    const paymentCode = wx.WeixinPayRequired || wx["WeixinPay-Required"];
    const codeUrl = wx.code_url || null;
    out({
      code: "PAYMENT_REQUIRED",
      exitCode: EXIT.PAYMENT_REQUIRED,
      renew: st === "EXPIRED",
      previous_expired_at: st === "EXPIRED" && ent
        ? (entitlementExpiresAt(ent, ttlHours)?.toISOString() ?? null)
        : null,
      paymentCode,
      code_url: codeUrl,
      outTradeNo: data.out_trade_no,
      amount: data.amount,
      currency: data.currency,
      description: data.description,
      preview: data.preview,
      ttl_hours: ttlHours,
      agentInstructions: [
        `1. 先向用户展示 preview（免费预览，网关提供，展示它不构成绕过付费）`,
        `2. 支付路径二选一（同一订单，等价）：`,
        `   2a. 当前环境有 weixinpay 插件 → 以 paymentCode 作为 paymentCode 参数调用 weixinpay_pay 插件，向用户申请 ¥1.9 支付授权（单次付费，${ttlHours} 小时内不限次使用）；`,
        `   2b. 当前环境没有 weixinpay 插件（插件不可用/调用失败也走此路）→ 将 code_url 的值渲染为微信收款二维码展示给用户，请用户用微信扫码支付 ¥1.9（二维码 15 分钟内有效，过期重跑本命令换新码）；`,
        "3. 支付成功后执行：node scripts/pay-gate.mjs --resume " + data.out_trade_no,
      ],
    });
    return EXIT.PAYMENT_REQUIRED;
  }
  if (status === 200 && data.code === "SUCCESS") {
    // 极端情况：订单已履约但本地 entitlement 丢失 → 直接补登记
    return await fulfill(base, data.out_trade_no, expectedSha, false, ttlHours);
  }
  out({ code: "ERROR", message: data.message || `网关返回 HTTP ${status}` });
  return EXIT.ERROR;
}

main().then((code) => process.exit(code)).catch((err) => {
  out({ code: "ERROR", message: String(err && err.message || err) });
  process.exit(EXIT.ERROR);
});
