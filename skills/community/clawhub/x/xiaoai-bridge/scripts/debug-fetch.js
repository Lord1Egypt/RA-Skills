#!/usr/bin/env node
/**
 * 调试工具：读取最近几条小爱音箱对话记录。
 *
 * 隐私默认值：不打印语音转写原文，只输出条数与时间。
 * 需要排查识别问题时，显式设置 PRINT_TRANSCRIPTS=true。
 */

import path from "node:path";
import { fileURLToPath } from "node:url";

import { ConfigError } from "./lib/core.js";
import { loadEnvironment } from "./lib/env.js";
import { connectMiNA } from "./lib/mi-client.js";
import { installRedactedConsole } from "./lib/redact.js";
import { loadConfig, transcriptsEnabled } from "./lib/runtime.js";
import { prepareSessionState, verifyCacheFile } from "./lib/state.js";

// 上游库失败时会把带 Cookie 的 axios 错误对象打到 console。
installRedactedConsole();

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = path.resolve(__dirname, "..");

async function main() {
  loadEnvironment({
    scriptDir: __dirname,
    skillRoot: SKILL_ROOT,
    warn: (line) => process.stderr.write(`${line}\n`),
  });
  const config = loadConfig();

  // 校验缓存目录 → chdir → 预创建 0600 缓存，避免凭据落进共享目录。
  const session = prepareSessionState(config);
  for (const line of session.warnings) {
    process.stderr.write(`${line}\n`);
  }

  const mina = await connectMiNA(config);

  if (!mina) {
    throw new Error("登录失败：请检查 MI_USER_ID、passToken/密码与 MI_DEVICE_ID");
  }

  const verified = verifyCacheFile(session.dir, {
    allowInsecure: config.allowInsecureStateDir,
    expected: session.identity ?? undefined,
  });
  for (const line of verified.warnings) {
    process.stderr.write(`${line}\n`);
  }

  const conversations = await mina.getConversations({ limit: 5 });
  const records = conversations?.records ?? [];

  console.log(`共 ${records.length} 条记录`);

  if (transcriptsEnabled()) {
    for (const record of records) {
      console.log(`时间: ${new Date(record.time).toLocaleString()}`);
      console.log(`内容: ${record.query}`);
      console.log("---");
    }
  } else {
    console.log("默认不打印语音转写内容；如需查看原文，请设置 PRINT_TRANSCRIPTS=true");
  }
}

try {
  await main();
} catch (error) {
  if (error instanceof ConfigError) {
    console.error(`❌ 配置错误：${error.message}`);
    process.exitCode = 2;
  } else {
    console.error(`❌ ${error.message}`);
    process.exitCode = 1;
  }
}
