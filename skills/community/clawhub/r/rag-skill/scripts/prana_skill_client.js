#!/usr/bin/env node
/**
 * 调用 Prana 技能接口。：
 * --question / -q：用户需求任务描述，例如：帮我使用XXX技能
 * --request-id / -r：指定需要查询的任务的 request_id
 */
import { randomUUID } from "node:crypto";
import { parseArgs } from "node:util";

const DEFAULT_BASE_URL = "https://claw-uat.ebonex.io";
const DEFAULT_SKILL_KEY = "rag-skill";
const AGENT_RUN_TIMEOUT_MS = 150000;
const AGENT_RESULT_RETRY_TIMES = 30;
const AGENT_RESULT_RETRY_INTERVAL_MS = 20000;

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function isTimeoutError(error) {
  if (!error) return false;
  return error.name === "TimeoutError" || error.name === "AbortError";
}

async function postJson(url, payload, xApiKey, timeoutMs) {
  const requestId = payload && typeof payload === "object" ? payload.request_id || "" : "";
  console.error(`[HTTP REQUEST] request_id=${requestId}`);
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": xApiKey,
    },
    body: JSON.stringify(payload),
    signal: AbortSignal.timeout(timeoutMs),
  });
  const text = await res.text();
  if (!res.ok) {
    const error = new Error(`HTTP ${res.status}: ${text}`);
    error.status = res.status;
    throw error;
  }
  return JSON.parse(text);
}

async function invokeAgentResultWithRetry(baseUrl, requestId, xApiKey) {
  const url = `${baseUrl.replace(/\/+$/, "")}/api/claw/agent-result`;
  let lastResult = { error: true, detail: "agent-result 尚未获取到结果" };

  for (let attempt = 1; attempt <= AGENT_RESULT_RETRY_TIMES; attempt += 1) {
    if (attempt > 1) {
      await sleep(AGENT_RESULT_RETRY_INTERVAL_MS);
    }
    try {
      const result = await postJson(url, { request_id: requestId }, xApiKey, AGENT_RUN_TIMEOUT_MS);
      lastResult = result;
      let status = String(result?.data?.status || "").toLowerCase();
      if (!status) {
        status = String(result?.status || "").toLowerCase();
      }
      if (status === "running") {
        continue;
      }
      if (status) {
        return result;
      }
    } catch (error) {
      return { error: true, detail: `第 ${attempt} 次 agent-result 请求失败: ${error.message || error}` };
    }
  }

  console.error(
    "提示: 本轮尝试已达到上限；Prana 服务端任务可能仍需要较长时间才能完成。若希望继续等待同一任务结果，必须先向用户确认；仅在用户明确确认“重试”后，才可继续执行后续命令：node scripts/prana_skill_client.js -r " +
      requestId,
  );
  return null;
}

async function invokeAgentRun(baseUrl, skillKey, question, xApiKey) {
  const requestId = randomUUID();
  const url = `${baseUrl.replace(/\/+$/, "")}/api/claw/agent-run`;
  const payload = {
    skill_key: skillKey,
    question,
    request_id: requestId,
  };

  try {
    const runResult = await postJson(url, payload, xApiKey, AGENT_RUN_TIMEOUT_MS);
    const runStatus = String(runResult?.data?.status || "").toLowerCase();
    if (runStatus === "running") {
      return await invokeAgentResultWithRetry(baseUrl, requestId, xApiKey);
    }
    return runResult;
  } catch (error) {
    if (isTimeoutError(error)) {
      return await invokeAgentResultWithRetry(baseUrl, requestId, xApiKey);
    }
    throw error;
  }
}

async function main() {
  let values;
  try {
    ({ values } = parseArgs({
      args: process.argv.slice(2),
      options: {
        question: { type: "string", short: "q", default: "" },
        "request-id": { type: "string", short: "r", default: "" },
        help: { type: "boolean", short: "h", default: false },
      },
      allowPositionals: false,
    }));
  } catch (error) {
    console.error(error.message || error);
    process.exit(1);
  }

  if (values.help) {
    console.log(
      "调用 Prana 技能接口。\n" +
        "\n" +
        "  -q, --question   用户需求任务描述，例如：帮我使用XXX技能\n" +
        "  -r, --request-id 指定需要查询的任务的 request_id\n" +
        "\n" +
        '用法: node scripts/prana_skill_client.js -q "用户任务"\n' +
        "      或: node scripts/prana_skill_client.js -r <request_id>",
    );
    process.exit(0);
  }

  const questionTrimmed = String(values.question || "").trim();
  const requestIdArg = String(values["request-id"] || "").trim();
  if (!questionTrimmed && !requestIdArg) {
    console.error("错误: 请使用 -q / --question 发起新任务，或使用 -r / --request-id 查询指定任务状态。");
    process.exit(1);
  }

  const xApiKey = String(process.env.PRANA_SKILL_API_FLAG || "").trim();
  if (!xApiKey) {
    console.error("错误: 未检测到环境变量 PRANA_SKILL_API_FLAG。");
    process.exit(1);
  }

  try {
    const result = questionTrimmed
      ? await invokeAgentRun(
          DEFAULT_BASE_URL,
          DEFAULT_SKILL_KEY,
          questionTrimmed,
          xApiKey,
        )
      : await invokeAgentResultWithRetry(DEFAULT_BASE_URL, requestIdArg, xApiKey);
    if (result != null) {
      console.log(JSON.stringify(result, null, 2));
    }
  } catch (error) {
    console.error(`请求失败: ${error.message || error}`);
    process.exit(2);
  }
}

await main();
