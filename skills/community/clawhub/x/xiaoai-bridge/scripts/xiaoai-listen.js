#!/usr/bin/env node
/**
 * 小爱音箱消息监听 / TTS 播报桥接（CLI 入口）。
 *
 * 命令：
 *   node xiaoai-listen.js                监听并把语音指令以 JSON 行写到 stdout
 *   node xiaoai-listen.js speak "文本"   通过小爱音箱 TTS 播报
 *   node xiaoai-listen.js judge "文本"   用 Jev 判定模型对单条文本做转发决策
 *   node xiaoai-listen.js test           测试登录与设备连接（配置 Jev 时含连通性检查）
 *   node xiaoai-listen.js check          检查会话缓存目录/文件权限（不联网）
 *   node xiaoai-listen.js clean          清理本地会话缓存（含 passToken）
 */

import path from "node:path";
import { fileURLToPath } from "node:url";

import {
  ConfigError,
  MAX_TTS_TEXT_LENGTH,
  VERSION,
  pollOnce,
  pollTranscripts,
} from "./lib/core.js";
import { loadEnvironment } from "./lib/env.js";
import { createJevClient } from "./lib/jev-client.js";
import { connectMiNA } from "./lib/mi-client.js";
import { installRedactedConsole, redactSecrets } from "./lib/redact.js";
import {
  checkRuntimeSecurity,
  loadConfig,
  loadJevConfig,
  loadTriggerPrefix,
  resolveRuntimeStateDir,
} from "./lib/runtime.js";
import {
  CACHE_FILE_NAME,
  cleanStateDir,
  findLegacyCachePaths,
  prepareSessionState,
  verifyCacheFile,
} from "./lib/state.js";

// 上游库失败时会把带 Cookie 的 axios 错误对象打到 console；
// 在加载凭据之前先安装脱敏，避免 passToken/serviceToken 进入 stderr。
installRedactedConsole();

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = path.resolve(__dirname, "..");

const USAGE = `用法：
  node scripts/xiaoai-listen.js                 监听语音指令（stdout 仅输出 JSON 行）
  node scripts/xiaoai-listen.js speak "文本"    TTS 播报
  node scripts/xiaoai-listen.js judge "文本"    用 Jev 对单条文本做转发判定（需 JEV_API_KEY）
  node scripts/xiaoai-listen.js test            测试登录与设备（配置 Jev 时含连通性检查）
  node scripts/xiaoai-listen.js check           检查缓存目录/文件权限（不联网）
  node scripts/xiaoai-listen.js clean           清理本地会话缓存
  node scripts/xiaoai-listen.js --help          显示帮助
  node scripts/xiaoai-listen.js --version       显示版本

环境变量：
  MI_USER_ID              必填，纯数字小米 ID
  MI_DEVICE_ID            必填，设备名称 / miotDID / MAC
  MI_PASS_TOKEN           推荐，与 MI_PASSWORD 二选一
  MI_PASSWORD             备选，可能触发安全验证
  TRIGGER_PREFIX          触发词前缀，默认“请”（配置 Jev 后仅作为判定信号与降级后备）
  XIAOAI_ALLOW_UNFILTERED 设为 true 才允许空触发词（处理所有消息）
  POLL_INTERVAL           轮询间隔毫秒，默认 1000（范围 500-60000）
  JEV_API_KEY             可选，Jev 判定平台密钥（sk_ 开头）；配置后由 Jev 动态判定转发，
                          未配置或服务不可用时自动降级回热词触发
  JEV_LEVEL               判定挡位 loose / balanced / strict，默认 balanced
  JEV_DECISION_THRESHOLD  自定义转发概率阈值（0-1），覆盖挡位默认值
  JEV_TIMEOUT_MS          判定请求超时毫秒，默认 8000（范围 1000-30000）
  JEV_BASE_URL            Jev 服务地址，默认官方服务地址（仅支持 https）
  JEV_MODEL               判定模型，默认 NeoHorse-Jev-4B
  XIAOAI_STATE_DIR        会话缓存目录，默认当前用户的私有状态目录
  XIAOAI_ALLOW_INSECURE_STATE_DIR
                          仅在权限无法强制/ACL 无法验证时显式放行（有风险）
  XIAOAI_ENV_FILE         指定 .env 路径，默认 scripts/.env 或技能根目录 .env
  DEBUG                   设为 true 输出调试信息（stderr）`;

const ACTION_TEXT = {
  created: "新建",
  kept: "复用",
  replaced: "替换为安全文件",
  reset: "重置损坏内容",
  sanitized: "清理未知字段",
};

function log(line) {
  process.stderr.write(`${redactSecrets(line)}\n`);
}

/**
 * 提示旧版本可能遗留的凭据文件。只告警，不自动读取或删除。
 */
function warnLegacyCache(config) {
  const legacy = findLegacyCachePaths({
    scriptDir: __dirname,
    skillRoot: SKILL_ROOT,
    excludeDirs: config?.stateDir ? [config.stateDir] : [],
  });

  for (const file of legacy) {
    log(`⚠️  发现遗留会话文件：${file}`);
    log("    该文件可能包含小米账号凭据，请运行 clean 清理，并且不要提交到版本库。");
  }
}

/**
 * 校验私有状态目录，切换工作目录，并预创建 0600 的会话缓存。
 */
function prepareState(config) {
  warnLegacyCache(config);
  const session = prepareSessionState(config);

  for (const line of session.warnings) {
    log(line);
  }
  log(
    `📁 会话缓存目录：${session.dir}（来源：${
      config.stateDirSource === "env" ? "XIAOAI_STATE_DIR" : "默认"
    }）`,
  );
  if (process.platform === "win32") {
    log("🔒 目录校验通过：位于当前用户目录内，未跟随符号链接");
  } else {
    log(`🔒 目录校验通过：${session.dirMode}，属主为当前用户`);
  }
  log(
    `📝 会话缓存文件：${session.cacheFile}（${session.mode}，${
      ACTION_TEXT[session.action] ?? session.action
    }）`,
  );
  return session;
}

async function connect(config, { redirectLogs = true } = {}) {
  log("🔌 正在连接小爱音箱...");

  const client = await connectMiNA(config, { redirectLogs });

  if (!client) {
    throw new Error(
      "登录失败：请检查 MI_USER_ID、passToken/密码与 MI_DEVICE_ID（DEBUG=true 可打印设备列表）",
    );
  }

  log("✅ 连接成功");
  return client;
}

async function initSession(config, options = {}) {
  const session = prepareState(config);
  const client = await connect(config, options);

  const verified = verifyCacheFile(session.dir, {
    allowInsecure: config.allowInsecureStateDir,
    expected: session.identity ?? undefined,
  });
  for (const line of verified.warnings) {
    log(line);
  }
  log(`🔐 缓存文件校验通过：${verified.mode}`);
  return client;
}

/** Jev 连续失败次数达到该值后进入短冷却。 */
const JEV_FALLBACK_MAX_FAILURES = 3;
/** Jev 短冷却时长：冷却期内只用热词触发，期满自动重试 Jev。 */
const JEV_FALLBACK_COOLDOWN_MS = 60_000;
/** 认证类错误（401/403，属配置问题）的长冷却时长。 */
const JEV_AUTH_COOLDOWN_MS = 10 * 60_000;

function toBridgeMessage(transcript, via) {
  return {
    type: "message",
    text: transcript.text,
    originalText: transcript.originalText,
    timestamp: transcript.timestamp,
    via,
  };
}

/** stderr 判定日志只保留转写前 20 个字符，避免完整语音内容进入日志。 */
function summarizeForLog(text) {
  const clean = String(text ?? "").replace(/\s+/g, " ").trim();
  return clean.length > 20 ? `${clean.slice(0, 20)}…` : clean;
}

/**
 * 记录一次 Jev 判定失败，并在达到阈值/认证错误时进入冷却。
 *
 * @param {Error} error
 * @param {{ failures: number, cooldownUntil: number }} jevState
 * @returns {void}
 */
function noteJevFailure(error, jevState) {
  jevState.failures += 1;
  const category = error?.category ?? "network";
  const isAuth = category === "auth";

  if (isAuth || jevState.failures >= JEV_FALLBACK_MAX_FAILURES) {
    const cooldownMs = isAuth ? JEV_AUTH_COOLDOWN_MS : JEV_FALLBACK_COOLDOWN_MS;
    jevState.cooldownUntil = Date.now() + cooldownMs;
    log(`⚠️ Jev 判定失败（${category}）：${error.message}`);
    if (isAuth) {
      log(
        `⛔ 认证类错误（401/403），${Math.round(JEV_AUTH_COOLDOWN_MS / 60_000)} 分钟内回退热词触发；请检查 JEV_API_KEY 或账号权限`,
      );
    } else {
      log(
        `⛔ 连续失败 ${jevState.failures} 次，${Math.round(JEV_FALLBACK_COOLDOWN_MS / 1000)} 秒内回退热词触发，期满自动重试 Jev`,
      );
    }
  } else {
    log(
      `⚠️ Jev 判定失败（${category}）：${error.message}，本批剩余消息回退热词匹配（连续失败 ${jevState.failures}/${JEV_FALLBACK_MAX_FAILURES}）`,
    );
  }
}

async function runListen(client, config) {
  const state = {
    lastTimestamp: Date.now(),
    triggerPrefix: config.triggerPrefix,
    allowUnfiltered: config.allowUnfiltered,
  };

  const jev = config.jev ? createJevClient(config.jev) : null;
  if (jev) {
    const thresholdNote =
      config.jev.decisionThreshold !== undefined ? `，自定义阈值 ${config.jev.decisionThreshold}` : "";
    log(`🧠 Jev 智能判定已启用（挡位：${config.jev.level}${thresholdNote}），热词触发转为降级后备`);
    log("ℹ️  语音转写文本将发送至 Jev 判定服务用于转发决策（详见 SKILL.md 隐私说明）");
  }
  const jevState = { failures: 0, cooldownUntil: 0 };

  let running = true;
  let wakeFromSleep = null;
  const wait = (ms) =>
    new Promise((resolve) => {
      const timer = setTimeout(() => {
        wakeFromSleep = null;
        resolve();
      }, ms);
      wakeFromSleep = () => {
        clearTimeout(timer);
        wakeFromSleep = null;
        resolve();
      };
    });

  const stop = (signal) => {
    if (!running) {
      return;
    }
    running = false;
    log(`\n👋 收到 ${signal}，停止监听`);
    wakeFromSleep?.();
  };
  process.once("SIGINT", () => stop("SIGINT"));
  process.once("SIGTERM", () => stop("SIGTERM"));

  log("🎤 开始监听消息...");

  let failures = 0;
  let backoffMs = 1000;

  while (running) {
    try {
      const jevActive = Boolean(jev) && Date.now() >= jevState.cooldownUntil;
      let messages;

      if (jevActive) {
        const transcripts = await pollTranscripts(client, state);
        messages = [];
        let judgeFailure = null;
        let index = 0;

        for (; index < transcripts.length; index++) {
          const transcript = transcripts[index];
          try {
            const decision = await jev.decide(transcript.originalText, {
              prefix: config.triggerPrefix,
              prefixMatched: transcript.prefixMatched,
            });
            log(
              `🧠 [Jev] 「${summarizeForLog(transcript.originalText)}」→ ${
                decision.forward ? "转发" : "忽略"
              }（应转发 ${decision.shouldForward.toFixed(2)}，原生 ${decision.isNativeCapability.toFixed(2)}）${
                decision.traceId ? ` [trace:${decision.traceId}]` : ""
              }`,
            );
            if (decision.forward) {
              messages.push(toBridgeMessage(transcript, "jev"));
            }
          } catch (error) {
            judgeFailure = error;
            break;
          }
        }

        if (judgeFailure) {
          noteJevFailure(judgeFailure, jevState);
          // 当前这条及其后未判定的消息回退热词匹配（降级语义与旧版本一致）。
          for (; index < transcripts.length; index++) {
            const transcript = transcripts[index];
            if (transcript.prefixMatched) {
              messages.push(toBridgeMessage(transcript, "prefix"));
            }
          }
        } else if (jevState.failures > 0) {
          jevState.failures = 0;
          log("✅ Jev 判定已恢复");
        }
      } else {
        messages = (await pollOnce(client, state)).map((message) => ({ ...message, via: "prefix" }));
      }

      failures = 0;
      backoffMs = 1000;

      for (const message of messages) {
        process.stdout.write(`${JSON.stringify(message)}\n`);
      }
    } catch (error) {
      failures += 1;
      log(`❌ 获取消息失败（连续 ${failures} 次）：${error.message}`);
      await wait(backoffMs);
      backoffMs = Math.min(30000, backoffMs * 2);
      continue;
    }

    if (!running) {
      break;
    }
    await wait(config.pollIntervalMs);
  }
}

async function runSpeak(config, text) {
  const content = String(text ?? "").trim();
  if (!content) {
    throw new ConfigError('用法：node scripts/xiaoai-listen.js speak "要说的话"');
  }
  if (content.length > MAX_TTS_TEXT_LENGTH) {
    throw new ConfigError(`TTS 文本超过 ${MAX_TTS_TEXT_LENGTH} 字符，请先拆分后再播报`);
  }

  const client = await initSession(config);
  const ok = await client.play({ text: content });
  if (!ok) {
    throw new Error("TTS 播报失败");
  }
  log("✅ 播报已发送");
}

async function runTest(config) {
  // 测试模式保留库自身的调试输出（DEBUG=true 时可查看设备列表）。
  await initSession(config, { redirectLogs: false });
  log("✅ 连接测试通过");

  if (config.jev) {
    log("🧠 正在检查 Jev 判定服务...");
    const jev = createJevClient(config.jev);
    const result = await jev.ping();
    log(
      `✅ Jev 连通正常（${result.latencyMs}ms${result.model ? `，模型 ${result.model}` : ""}，挡位 ${config.jev.level}）`,
    );
  }
}

/**
 * judge 子命令：对单条文本做一次 Jev 转发判定。
 *
 * 不需要小米账号配置，用于调试判定挡位与验证服务连通性。
 * stdout 输出一个 JSON 结果；未配置 JEV_API_KEY 时以配置错误退出（退出码 2）。
 */
async function runJudge(text) {
  const query = String(text ?? "").trim();
  if (!query) {
    throw new ConfigError('用法：node scripts/xiaoai-listen.js judge "语音文本"');
  }

  const jevConfig = loadJevConfig();
  if (!jevConfig) {
    throw new ConfigError("未配置 JEV_API_KEY，Jev 判定不可用（当前仅支持热词触发，参见 env.example）");
  }

  const prefix = loadTriggerPrefix();
  const prefixMatched = Boolean(prefix) && query.startsWith(prefix);
  const jev = createJevClient(jevConfig);
  const decision = await jev.decide(query, { prefix, prefixMatched });

  const result = {
    query,
    prefixMatched,
    level: decision.level,
    forward: decision.forward,
    shouldForward: decision.shouldForward,
    isNativeCapability: decision.isNativeCapability,
    threshold: decision.threshold,
    reason: decision.reason,
  };
  if (decision.traceId) {
    result.traceId = decision.traceId;
  }
  if (decision.model) {
    result.model = decision.model;
  }
  process.stdout.write(`${JSON.stringify(result)}\n`);
}

function runClean() {
  const resolved = resolveRuntimeStateDir();
  const primaryDir = resolved.dir;
  const legacyDirs = new Set();

  for (const file of findLegacyCachePaths({ scriptDir: __dirname, skillRoot: SKILL_ROOT })) {
    const dir = path.dirname(file);
    if (dir !== primaryDir) {
      legacyDirs.add(dir);
    }
  }

  let firstFailure = null;

  const reportResult = (dir, result, { isPrimary }) => {
    if (result.removedFile) {
      process.stdout.write(`✅ 已删除会话缓存：${path.join(dir, CACHE_FILE_NAME)}\n`);
    } else if (isPrimary) {
      process.stdout.write(`ℹ️  未找到会话缓存：${path.join(dir, CACHE_FILE_NAME)}\n`);
    }
    if (result.dirRemoved) {
      process.stdout.write(`✅ 已删除空缓存目录：${dir}\n`);
    }
    for (const note of result.notes) {
      process.stdout.write(`${note}\n`);
    }
  };

  try {
    const result = cleanStateDir(primaryDir, { removeEmptyDir: true });
    reportResult(primaryDir, result, { isPrimary: true });
  } catch (error) {
    firstFailure = error;
    log(`❌ 清理状态目录失败：${error.message}`);
  }

  for (const dir of legacyDirs) {
    try {
      // legacy 位置只删“像小米会话缓存”的文件，且绝不删除目录本身。
      const result = cleanStateDir(dir, { requireCacheSignature: true });
      reportResult(dir, result, { isPrimary: false });
    } catch (error) {
      firstFailure = firstFailure ?? error;
      log(`⚠️  跳过 ${dir}：${error.message}`);
    }
  }

  if (firstFailure) {
    throw firstFailure instanceof ConfigError
      ? firstFailure
      : new ConfigError(`清理未完成：${firstFailure.message}`);
  }
  process.stdout.write(
    "提示：删除本地缓存不等于撤销凭据；如 passToken 可能已泄露，请在小米账号中退出登录并更换 passToken。\n",
  );
}

function runCheck() {
  const report = checkRuntimeSecurity({
    scriptDir: __dirname,
    skillRoot: SKILL_ROOT,
    cwd: process.cwd(),
  });

  process.stdout.write("🔎 状态检查\n");
  for (const line of report.lines) {
    process.stdout.write(`   ${line}\n`);
  }
  process.stdout.write(`   结论：${report.ok ? "通过" : "失败"}\n`);
  process.exitCode = report.exitCode;
}

function printHelp() {
  process.stdout.write(`${USAGE}\n`);
}

async function main(argv) {
  const [command, ...rest] = argv;

  if (command === "--help" || command === "-h" || command === "help") {
    printHelp();
    return;
  }
  if (command === "--version" || command === "-V") {
    process.stdout.write(`${VERSION}\n`);
    return;
  }

  loadEnvironment({ scriptDir: __dirname, skillRoot: SKILL_ROOT, warn: log });

  if (command === "clean") {
    runClean();
    return;
  }
  if (command === "check" || command === "doctor") {
    runCheck();
    return;
  }

  // judge 不需要小米账号配置，放在 loadConfig 之前（loadEnvironment 已完成）。
  if (command === "judge") {
    await runJudge(rest.join(" "));
    return;
  }

  const config = loadConfig();

  if (command === "speak") {
    await runSpeak(config, rest.join(" "));
    return;
  }
  if (command === "test") {
    await runTest(config);
    return;
  }
  if (command === undefined) {
    const client = await initSession(config);
    await runListen(client, config);
    return;
  }

  throw new ConfigError(`未知命令：${command}\n\n${USAGE}`);
}

try {
  await main(process.argv.slice(2));
} catch (error) {
  if (error instanceof ConfigError) {
    log(`❌ 配置错误：${error.message}`);
    process.exitCode = 2;
  } else {
    log(`❌ ${error.message}`);
    process.exitCode = 1;
  }
}
