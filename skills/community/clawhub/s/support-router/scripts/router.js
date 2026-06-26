#!/usr/bin/env node
// support-router/scripts/router.js — 客服邮件智能分流脚本
//
// 轮询 support 邮箱，按关键词分类，自动回复或转发。
// 单次轮询模式，由 cron 每分钟调用。
//
// Usage: node router.js [--config router-config.json] [--dry-run] [--json]
//        node router.js --test-classify --subject "..." --body "..."
//
// Requires: mail-cli (npm install -g @clawemail/mail-cli)

const { execSync } = require("child_process");
const path = require("path");
const fs = require("fs");
const os = require("os");

// ========== 默认配置（可通过 --config 文件覆盖）==========
const DEFAULT_CONFIG = {
  supportProfile: "support",
  csbotProfile: "csbot",
  csbotEmail: "",                 // 留空则自动从 mail-cli config 读取
  mainEmail: "your-name@company.com",
  productName: "YourProduct",
  pricingUrl: "https://yourproduct.com/pricing",
  cancelUrl: "https://yourproduct.com/settings",
  fid: "1",                      // Claw 收件箱 folder ID
  maxRepliesPerAddr: 100,          // 每地址每天最多自动回复次数（宽松限制，兜底防循环）
  dataDir: "",                    // 留空则使用 ~/.local/share/support-router
  ignoreSenderDomains: ["claw.163.com"],  // 忽略这些域名的发件人（防止内部邮箱循环）
};

// ========== 分类规则（优先级从高到低）==========
const RULES = [
  {
    name: "pricing",
    pattern: /pricing|price|费用|多少钱|定价|how much|报价|plan.*cost|subscription fee/i,
    action: "auto_reply",
  },
  {
    name: "cancellation",
    pattern: /cancel|退订|取消|unsubscribe|退款|refund|close.*account|delete.*account/i,
    action: "auto_reply",
  },
  {
    name: "business",
    pattern: /合作|partnership|商务|business|invest|代理|reseller|enterprise.*inquiry/i,
    action: "forward_main",
  },
  {
    name: "bug",
    pattern: /bug|error|crash|报错|崩溃|打不开|无法|故障|not working|broken|failed|exception/i,
    action: "forward_csbot",
    tag: "[Bug反馈]",
  },
];

// ========== 自动回复邮件检测模式 ==========
const NOREPLY_PATTERN = /noreply|no-reply|mailer-daemon|postmaster/i;
const AUTO_REPLY_SUBJECT_PATTERN = /^(auto:|automatic reply|自动回复|out of office|ooo:|away:|回复：.*自动|退信通知|undeliverable|delivery (status |failure)|returned mail)/i;

// ========== 参数解析 ==========
const args = process.argv.slice(2);
let configFile = null;
let dryRun = false;
let outputJson = false;
let testClassify = false;
let testSubject = "";
let testBody = "";

for (let i = 0; i < args.length; i++) {
  switch (args[i]) {
    case "--config":
      configFile = args[++i];
      break;
    case "--dry-run":
      dryRun = true;
      break;
    case "--json":
      outputJson = true;
      break;
    case "--test-classify":
      testClassify = true;
      break;
    case "--subject":
      testSubject = args[++i] || "";
      break;
    case "--body":
      testBody = args[++i] || "";
      break;
    default:
      console.error(`Unknown option: ${args[i]}`);
      process.exit(1);
  }
}

// ========== 工具函数 ==========

function log(msg) {
  const ts = new Date().toISOString().replace("T", " ").slice(0, 19);
  if (!outputJson) console.log(`[support-router] [${ts}] ${msg}`);
}

function run(cmd, timeout = 30000) {
  try {
    return execSync(cmd, { encoding: "utf8", timeout, stdio: ["pipe", "pipe", "pipe"] });
  } catch (err) {
    const stderr = err.stderr ? err.stderr.toString().trim() : "";
    if (stderr && !outputJson) {
      const ts = new Date().toISOString().replace("T", " ").slice(0, 19);
      console.error(`[support-router] [${ts}] CMD FAILED: ${cmd.slice(0, 120)}...`);
      console.error(`[support-router] [${ts}] STDERR: ${stderr.slice(0, 500)}`);
    }
    return null;
  }
}

function findMailCli() {
  const isWin = process.platform === "win32";
  const whichCmd = isWin ? "where mail-cli" : "which mail-cli";
  const result = run(whichCmd);
  if (result && result.trim()) return "mail-cli";
  return "npx mail-cli";
}

function loadMailCliConfig() {
  const configDir = process.env.XDG_CONFIG_HOME || path.join(os.homedir(), ".config");
  const configPath = path.join(configDir, "mail-cli", "config.json");
  if (fs.existsSync(configPath)) {
    return JSON.parse(fs.readFileSync(configPath, "utf8"));
  }
  const appData = process.env.APPDATA;
  if (appData) {
    const winPath = path.join(appData, "mail-cli", "config.json");
    if (fs.existsSync(winPath)) {
      return JSON.parse(fs.readFileSync(winPath, "utf8"));
    }
  }
  return null;
}

function loadRouterConfig() {
  let cfg = { ...DEFAULT_CONFIG };
  if (configFile) {
    const content = fs.readFileSync(configFile, "utf8");
    const userCfg = JSON.parse(content);
    cfg = { ...cfg, ...userCfg };
  }
  if (!cfg.dataDir) {
    cfg.dataDir = path.join(os.homedir(), ".local", "share", "support-router");
  }
  return cfg;
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

// ========== csbot 邮箱地址解析 ==========

function resolveCsbotEmail(cfg, cli) {
  // 1. 显式配置
  if (cfg.csbotEmail) return cfg.csbotEmail;
  // 2. 从 mail-cli config.json 读取
  const mailConfig = loadMailCliConfig();
  if (mailConfig?.profiles?.[cfg.csbotProfile]?.user) {
    return mailConfig.profiles[cfg.csbotProfile].user;
  }
  // 3. 回退：auth test
  const result = run(`${cli} --profile ${cfg.csbotProfile} auth test`);
  if (result) {
    const match = result.match(/[\w.-]+@claw\.163\.com/);
    if (match) return match[0];
  }
  return null;
}

// ========== 回复频率限制 ==========

function checkReplyLimit(cfg, addr) {
  const today = new Date().toISOString().slice(0, 10);
  const counterFile = path.join(cfg.dataDir, `.reply-count-${addr.replace(/[@.]/g, "_")}-${today}`);
  let count = 0;
  if (fs.existsSync(counterFile)) {
    count = parseInt(fs.readFileSync(counterFile, "utf8"), 10) || 0;
  }
  if (count >= cfg.maxRepliesPerAddr) return false;
  fs.writeFileSync(counterFile, String(count + 1));
  return true;
}

// ========== 自动回复检测 ==========

function isAutoReply(headers, subject) {
  // 1. Auto-Submitted 头（RFC 3834 标准）
  const autoSubmitted = headers["auto-submitted"] || headers["Auto-Submitted"] || "";
  if (autoSubmitted && autoSubmitted !== "no") return true;

  // 2. X-Auto-Response-Suppress 头（Microsoft 系）
  if (headers["x-auto-response-suppress"] || headers["X-Auto-Response-Suppress"]) return true;

  // 3. X-Autoreply / X-Autorespond 头
  if (headers["x-autoreply"] || headers["X-Autoreply"]) return true;
  if (headers["x-autorespond"] || headers["X-Autorespond"]) return true;

  // 4. Precedence: bulk / junk / auto_reply
  const precedence = (headers["precedence"] || headers["Precedence"] || "").toLowerCase();
  if (precedence === "bulk" || precedence === "junk" || precedence === "auto_reply") return true;

  // 5. Return-Path 为空（退信/bounce）— 仅当字段实际存在且值为 <> 时才判定
  const returnPath = headers["return-path"] || headers["Return-Path"];
  if (returnPath && returnPath.trim() === "<>") return true;

  // 6. noreply 发件人
  const from = headers.from || headers.From || "";
  if (NOREPLY_PATTERN.test(from)) return true;

  // 7. Subject 模式（自动回复、Out of Office、退信通知等）
  if (subject && AUTO_REPLY_SUBJECT_PATTERN.test(subject.trim())) return true;

  return false;
}

// ========== 内部发件人检测 ==========

function isInternalSender(fromAddr, cfg) {
  if (!fromAddr || fromAddr === "unknown") return false;
  const addr = fromAddr.toLowerCase();
  // 从发件人字段中提取纯邮箱地址（可能含 "Name <email>" 格式）
  const emailMatch = addr.match(/<([^>]+)>/) || [null, addr];
  const email = emailMatch[1].trim();
  const domains = cfg.ignoreSenderDomains || ["claw.163.com"];
  return domains.some(domain => email.endsWith(`@${domain.toLowerCase()}`));
}

// ========== 邮件分类 ==========

function classifyEmail(subject, body) {
  const combined = `${subject} ${body}`.toLowerCase();
  for (const rule of RULES) {
    if (rule.pattern.test(combined)) {
      return rule;
    }
  }
  return { name: "unknown", action: "forward_csbot", tag: "[待分类]" };
}

// ========== 回复模板（中英文双语）==========

function getPricingReply(cfg) {
  return [
    `您好！感谢关注 ${cfg.productName}。`,
    `定价详情请访问：${cfg.pricingUrl}`,
    `如有其他问题请随时回复此邮件。`,
    ``,
    `Hi! Thanks for your interest in ${cfg.productName}.`,
    `Pricing details: ${cfg.pricingUrl}`,
    `Feel free to reply if you have other questions.`,
  ].join("\n");
}

function getCancellationReply(cfg) {
  return [
    `您好！取消订阅步骤：`,
    `1. 登录 ${cfg.cancelUrl}`,
    `2. 点击「订阅管理」→「取消订阅」`,
    `取消后当前计费周期内仍可正常使用。如需帮助请回复此邮件。`,
    ``,
    `To cancel your subscription:`,
    `1. Visit ${cfg.cancelUrl}`,
    `2. Navigate to Subscription Management > Cancel`,
    `Your service remains active until the end of the billing cycle.`,
  ].join("\n");
}

// ========== 邮件操作 ==========

function sendReply(cli, cfg, toAddr, originalSubject, body) {
  const escapedBody = body.replace(/'/g, "'\\''");
  const escapedSubject = `Re: ${originalSubject}`.replace(/'/g, "'\\''");
  const cmd = `${cli} --profile ${cfg.supportProfile} compose send --to '${toAddr}' --subject '${escapedSubject}' --body '${escapedBody}'`;
  if (dryRun) {
    log(`  [DRY-RUN] 发送回复到 ${toAddr}`);
    return true;
  }
  return run(cmd) !== null;
}

function forwardEmail(cli, cfg, toAddr, fromAddr, originalSubject, body, tag) {
  const fwdBody = [
    `--- 转发自客服邮箱 ---`,
    `From: ${fromAddr}`,
    `Subject: ${originalSubject}`,
    ``,
    body,
    ``,
    `--- NOTE: 原邮件可能包含附件，请直接查看 support 收件箱 ---`,
  ].join("\n");
  const escapedBody = fwdBody.replace(/'/g, "'\\''");
  const subject = `${tag ? tag + " " : ""}Fwd: ${originalSubject}`.replace(/'/g, "'\\''");
  const cmd = `${cli} --profile ${cfg.supportProfile} compose send --to '${toAddr}' --subject '${subject}' --body '${escapedBody}'`;
  if (dryRun) {
    log(`  [DRY-RUN] 转发到 ${toAddr}`);
    return true;
  }
  return run(cmd) !== null;
}

function forwardToCsbotForAnalysis(cli, cfg, toAddr, fromAddr, originalSubject, body, tag) {
  const instructions = [
    `=== 客服分析请求 ===`,
    `此邮件由客服路由脚本自动转发，请分析并将分析报告发送给人工客服。`,
    ``,
    `请按以下步骤处理：`,
    `1. 仔细阅读下方原始客户邮件`,
    `2. 归类（技术问题 / 功能建议 / 账户问题 / 投诉 / 退款 / 其他，可多选）`,
    `3. 评估处理优先级（高 / 中 / 低）及简短理由`,
    `4. 给出 2-3 条具体处理建议`,
    `5. 使用 mail-cli 将分析报告发送到人工客服邮箱：${cfg.mainEmail}`,
    `   - 邮件主题：[客服分析] ${originalSubject}`,
    `   - 邮件正文格式：`,
    `       分类：<类别>`,
    `       优先级：<高/中/低>  原因：<简短说明>`,
    `       处理建议：`,
    `         1. <建议1>`,
    `         2. <建议2>`,
    `       原始邮件摘要：<50字以内>`,
    `       原始发件人：${fromAddr}`,
    ``,
    `⚠️ 重要：禁止直接回复原始客户邮件（${fromAddr}），只需将分析报告发给 ${cfg.mainEmail}。`,
    ``,
    `=== 原始客户邮件 ===`,
    `From: ${fromAddr}`,
    `Subject: ${originalSubject}`,
    ``,
    body,
    ``,
    `--- NOTE: 原邮件可能包含附件，请查看 support 收件箱 ---`,
  ].join("\n");
  const escapedBody = instructions.replace(/'/g, "'\\''");
  const subject = `${tag ? tag + " " : ""}[待分析] ${originalSubject}`.replace(/'/g, "'\\''");
  const cmd = `${cli} --profile ${cfg.supportProfile} compose send --to '${toAddr}' --subject '${subject}' --body '${escapedBody}'`;
  if (dryRun) {
    log(`  [DRY-RUN] 转发分析请求到 ${toAddr}`);
    return true;
  }
  return run(cmd) !== null;
}

function markAsRead(cli, cfg, msgId) {
  if (dryRun) {
    log(`  [DRY-RUN] 标记已读 ${msgId}`);
    return;
  }
  run(`${cli} --profile ${cfg.supportProfile} mail mark --ids '${msgId}' --fid ${cfg.fid} --read`);
}

// ========== 清理过期记录（7天）==========

function cleanupProcessed(dataDir) {
  const processedDir = path.join(dataDir, "processed");
  if (!fs.existsSync(processedDir)) return;
  const cutoff = Date.now() - 7 * 24 * 60 * 60 * 1000;
  for (const f of fs.readdirSync(processedDir)) {
    const fp = path.join(processedDir, f);
    try {
      const stat = fs.statSync(fp);
      if (stat.mtimeMs < cutoff) fs.unlinkSync(fp);
    } catch { /* ignore */ }
  }
  // 清理过期的频率计数文件
  for (const f of fs.readdirSync(dataDir)) {
    if (f.startsWith(".reply-count-")) {
      const fp = path.join(dataDir, f);
      try {
        const stat = fs.statSync(fp);
        if (stat.mtimeMs < cutoff) fs.unlinkSync(fp);
      } catch { /* ignore */ }
    }
  }
}

// ========== 主流程 ==========

function main() {
  const cfg = loadRouterConfig();
  const cli = findMailCli();
  const processedDir = path.join(cfg.dataDir, "processed");
  ensureDir(processedDir);

  // 互斥锁（跨平台简易版：lockfile）
  const lockFile = path.join(cfg.dataDir, "router.lock");
  try {
    // O_EXCL：如果文件已存在则报错，实现互斥
    const fd = fs.openSync(lockFile, "wx");
    fs.closeSync(fd);
  } catch {
    // 检查 lockfile 是否过期（超过 5 分钟视为残留）
    try {
      const stat = fs.statSync(lockFile);
      if (Date.now() - stat.mtimeMs > 5 * 60 * 1000) {
        fs.unlinkSync(lockFile);
        const fd = fs.openSync(lockFile, "wx");
        fs.closeSync(fd);
      } else {
        log("另一个 router 实例正在运行，跳过");
        process.exit(0);
      }
    } catch {
      log("无法获取锁，跳过");
      process.exit(0);
    }
  }

  // 确保退出时释放锁
  const releaseLock = () => { try { fs.unlinkSync(lockFile); } catch { /* ignore */ } };
  process.on("exit", releaseLock);
  process.on("SIGINT", () => { releaseLock(); process.exit(1); });
  process.on("SIGTERM", () => { releaseLock(); process.exit(1); });

  log("开始轮询...");
  cleanupProcessed(cfg.dataDir);

  // 校验 mainEmail 不应是 agent 邮箱
  if (/@claw\.163\.com\s*$/i.test(cfg.mainEmail)) {
    log("⚠ WARNING: mainEmail 配置为 @claw.163.com 地址（agent 邮箱）。");
    log("  mainEmail 应该是人类可直接查看的邮箱（如 admin@company.com），");
    log("  否则商务合作等需要人工处理的邮件将发到 agent 邮箱而非人类邮箱。");
    log("  请修改 router-config.json 中的 mainEmail 为人类邮箱地址。");
  }

  // 解析 csbot 邮箱地址
  const csbotEmail = resolveCsbotEmail(cfg, cli);
  if (!csbotEmail) {
    log("WARNING: 无法获取 csbot 邮箱地址，Bug/未分类邮件将转发到主邮箱");
  }

  // 搜索未读邮件
  const searchResult = run(`${cli} --profile ${cfg.supportProfile} mail search --fid ${cfg.fid} --unread --json`);
  if (!searchResult) {
    log("搜索未读邮件失败");
    process.exit(1);
  }

  let parsed;
  try {
    parsed = JSON.parse(searchResult);
  } catch {
    log("解析搜索结果失败");
    process.exit(1);
  }

  const messages = parsed.data || parsed;
  if (!Array.isArray(messages) || messages.length === 0) {
    log("无未读邮件");
    process.exit(0);
  }

  log(`发现 ${messages.length} 封未读邮件`);

  const results = []; // 用于 --json 输出

  for (const msg of messages) {
    const msgId = msg.id;
    if (!msgId) continue;

    // 跳过已处理
    const processedFile = path.join(processedDir, String(msgId));
    if (fs.existsSync(processedFile)) continue;

    log(`处理邮件 ID: ${msgId}`);

    // 读取 header
    const headerRaw = run(`${cli} --profile ${cfg.supportProfile} read header --id '${msgId}' --fid ${cfg.fid} --json`);
    const headerParsed = headerRaw ? (() => { try { return JSON.parse(headerRaw); } catch { return {}; } })() : {};
    const headers = headerParsed.data || headerParsed;

    // 读取 body
    const body = run(`${cli} --profile ${cfg.supportProfile} read body --id '${msgId}' --fid ${cfg.fid}`) || "";

    const fromAddr = Array.isArray(headers.from) ? headers.from[0] : (headers.from || headers.From || "unknown");
    const subject = headers.subject || headers.Subject || "(无主题)";

    log(`  From: ${fromAddr} | Subject: ${subject}`);

    // 跳过自动回复邮件
    if (isAutoReply(headers, subject)) {
      log("  跳过：检测到自动回复邮件");
      markAsRead(cli, cfg, msgId);
      fs.writeFileSync(processedFile, "auto-reply-skipped");
      results.push({ id: msgId, from: fromAddr, subject, category: "auto-reply", action: "skipped" });
      continue;
    }

    // 跳过内部发件人（如 csbot 回复、其他 agent 邮箱），--dry-run 模式不过滤以便测试
    if (!dryRun && isInternalSender(fromAddr, cfg)) {
      log("  跳过：内部发件人（agent 邮箱）");
      markAsRead(cli, cfg, msgId);
      fs.writeFileSync(processedFile, "internal-sender-skipped");
      results.push({ id: msgId, from: fromAddr, subject, category: "internal-sender", action: "skipped" });
      continue;
    }

    // 分类
    const rule = classifyEmail(subject, body);
    log(`  分类: ${rule.name}`);

    let action = "";

    switch (rule.action) {
      case "auto_reply": {
        if (checkReplyLimit(cfg, fromAddr)) {
          const replyBody = rule.name === "pricing" ? getPricingReply(cfg) : getCancellationReply(cfg);
          log(`  → 自动回复（${rule.name}）`);
          const sent = sendReply(cli, cfg, fromAddr, subject, replyBody);
          if (sent) {
            action = `auto_reply:${rule.name}`;
          } else {
            log(`  ⚠ 自动回复发送失败（${rule.name}），转发分析请求到 AI 邮箱`);
            if (csbotEmail) {
              forwardToCsbotForAnalysis(cli, cfg, csbotEmail, fromAddr, subject, body, `[${rule.name}-回复失败]`);
            } else {
              forwardEmail(cli, cfg, cfg.mainEmail, fromAddr, subject, body, `[${rule.name}-回复失败]`);
            }
            action = `auto_reply_failed:forward`;
          }
        } else {
          log(`  → 回复频率超限，转发分析请求到 AI 邮箱`);
          if (csbotEmail) {
            forwardToCsbotForAnalysis(cli, cfg, csbotEmail, fromAddr, subject, body, `[${rule.name}-超限]`);
          } else {
            forwardEmail(cli, cfg, cfg.mainEmail, fromAddr, subject, body, `[${rule.name}-超限]`);
          }
          action = `rate_limited:forward`;
        }
        break;
      }
      case "forward_main": {
        log(`  → 转发到主邮箱: ${cfg.mainEmail}`);
        forwardEmail(cli, cfg, cfg.mainEmail, fromAddr, subject, body, "[商务]");
        action = "forward_main";
        break;
      }
      case "forward_csbot": {
        const tag = rule.tag || "[待分类]";
        if (csbotEmail) {
          log(`  → 转发分析请求到 AI 邮箱 ${tag}`);
          forwardToCsbotForAnalysis(cli, cfg, csbotEmail, fromAddr, subject, body, tag);
          action = `forward_csbot:${tag}`;
        } else {
          log(`  → csbot 不可用，直接转发到主邮箱 ${tag}`);
          forwardEmail(cli, cfg, cfg.mainEmail, fromAddr, subject, body, tag);
          action = `forward_main:${tag}`;
        }
        break;
      }
    }

    // 标记已读
    markAsRead(cli, cfg, msgId);
    log("  已标记为已读");

    // 记录已处理
    fs.writeFileSync(processedFile, `${rule.name}:${action}`);
    results.push({ id: msgId, from: fromAddr, subject, category: rule.name, action });
  }

  log("轮询完成");

  if (outputJson) {
    console.log(JSON.stringify({ processed: results.length, results }, null, 2));
  }
}

// ========== --test-classify 模式：直接测试分类逻辑 ==========

if (testClassify) {
  if (!testSubject && !testBody) {
    console.error("Usage: node router.js --test-classify --subject \"...\" --body \"...\"");
    process.exit(1);
  }
  const rule = classifyEmail(testSubject, testBody);
  const result = {
    subject: testSubject,
    body: testBody.slice(0, 200) + (testBody.length > 200 ? "..." : ""),
    category: rule.name,
    action: rule.action,
    tag: rule.tag || null,
  };
  if (outputJson) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log(`分类: ${result.category}`);
    console.log(`动作: ${result.action}`);
    if (result.tag) console.log(`标签: ${result.tag}`);
  }
  process.exit(0);
}

main();
