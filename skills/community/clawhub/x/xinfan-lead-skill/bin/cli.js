#!/usr/bin/env node
import { parseArgs } from "node:util";
import * as auth from "../lib/auth.js";
import { listCommands, getSchemaByCommand } from "../lib/schemas.js";
import {
  buildRequest,
  callApi,
  UsageError,
  AuthError,
  UpstreamError,
  NetworkError,
} from "../lib/apiClient.js";
import {
  buildParseArgsOptions,
  buildBodyFromFlags,
  validate,
  renderHelp,
} from "../lib/paramCodec.js";
import { computeQualityHighlight } from "../lib/qualityMetrics.js";

const CLI_NAME = "xinfan-lead-cli";

function fail(message, exitCode = 1) {
  process.stderr.write(`[${CLI_NAME}] ${message}\n`);
  process.exit(exitCode);
}

function printUsage() {
  const cmdNames = listCommands()
    .map((c) => `  ${CLI_NAME} ${c.command} [--schema | --help | <flags...>]`)
    .join("\n");
  process.stdout.write(`用法:
  ${CLI_NAME} auth set-token <token>
  ${CLI_NAME} auth status
  ${CLI_NAME} commands
${cmdNames}

每个接口子命令都支持：
  --schema    打印这个接口的 requestSchema/responseSchema（JSON Schema）
  --help      打印人类可读的字段说明、业务警示和示例命令
  --dry-run   只打印会发出的 method/url/body（token 脱敏），不真正发请求
  --confirm   写接口必须加这个才会真正执行

退出码:
  0 成功  1 用法错误  2 鉴权失效  3 上游业务错误  4 网络错误
`);
}

// 只有这三个返回 LeadDTO 的命令会追加 quality_highlight（非后端字段，本地基于 extra_metric
// 算出），其它命令的输出维持纯转发，不做任何加工。列表命令是 data.leads[]（数组），
// get_lead_detail 是 data.lead（单条），两种响应形状分开处理。
const QUALITY_HIGHLIGHT_LIST_COMMANDS = new Set(["list_private_leads", "list_public_leads"]);

function attachQualityHighlight(entry, result) {
  if (QUALITY_HIGHLIGHT_LIST_COMMANDS.has(entry.id)) {
    const leads = result?.data?.leads;
    if (Array.isArray(leads)) {
      for (const lead of leads) lead.quality_highlight = computeQualityHighlight(lead);
    }
    return result;
  }
  if (entry.id === "get_lead_detail" && result?.data?.lead) {
    result.data.lead.quality_highlight = computeQualityHighlight(result.data.lead);
  }
  return result;
}

// 通用 reserved flags：不属于任何接口的业务字段，所有子命令都支持。
const RESERVED_OPTIONS = {
  schema: { type: "boolean", default: false },
  help: { type: "boolean", default: false },
  confirm: { type: "boolean", default: false },
  "dry-run": { type: "boolean", default: false },
};

async function runCommand(entry, rest) {
  const options = { ...buildParseArgsOptions(entry.requestSchema), ...RESERVED_OPTIONS };
  let values;
  try {
    ({ values } = parseArgs({ args: rest, options }));
  } catch (err) {
    throw new UsageError(`参数解析失败：${err.message}`);
  }

  if (values.help) {
    process.stdout.write(renderHelp(entry, CLI_NAME));
    return;
  }

  if (values.schema) {
    process.stdout.write(
      JSON.stringify({ request: entry.requestSchema, response: entry.responseSchema }, null, 2) + "\n"
    );
    return;
  }

  const body = buildBodyFromFlags(entry.requestSchema, values);
  validate(entry.requestSchema, body);

  if (entry.mutating && !values.confirm) {
    throw new UsageError(
      `"${entry.command}"（${entry.summary}）会修改线索状态，需要显式加 --confirm（代表已获得运营人员确认）。将要发送的请求体：${JSON.stringify(body)}`
    );
  }

  if (values["dry-run"]) {
    // 会话通道模式：请求通过已登录浏览器页面发出，身份由页面天然携带，
    // 这里不再有可脱敏的 Cookie 头。dry-run 只展示将要发出的 method/url/channel/body。
    const req = buildRequest(entry, body);
    process.stdout.write(JSON.stringify({ ...req, bodyObj: body }, null, 2) + "\n");
    return;
  }

  const result = attachQualityHighlight(entry, await callApi(entry, body));
  process.stdout.write(JSON.stringify(result, null, 2) + "\n");
}

async function main() {
  const [subcommand, ...rest] = process.argv.slice(2);

  if (!subcommand || subcommand === "-h" || subcommand === "--help") {
    printUsage();
    return;
  }

  if (subcommand === "auth") {
    const [action, ...authRest] = rest;
    if (action === "set-token") {
      const token = authRest[0];
      if (!token) throw new UsageError("用法：auth set-token <token>");
      auth.setToken(token);
      process.stdout.write(
        `token 已保存到 ${auth.CREDENTIALS_PATH}（${auth.maskToken(token)}）\n`
      );
      return;
    }
    if (action === "status") {
      const status = await auth.getStatus();
      const s = status.session || {};
      if (s.available) {
        process.stdout.write(
          `会话通道: 就绪 ✓\n` +
            `模式: 浏览器会话（用当前登录用户本人身份调用，不搬运 token）\n` +
            `域名: ${status.domain}\n` +
            `CDP: ${status.cdpUrl}\n` +
            `已登录页面: ${s.url}\n`
        );
        return;
      }
      const reasonMap = {
        no_page: "未找到已登录新帆的浏览器页面",
        no_ws: "找到页面但无可用调试通道",
        NO_CDP: "无法连接浏览器调试端点（浏览器可能未启动）",
        cdp_error: "探测浏览器时出错",
      };
      const reasonText = reasonMap[s.reason] || s.reason || "未知原因";
      process.stdout.write(
        `会话通道: 未就绪 ✗（${reasonText}）\n` +
          `域名: ${status.domain}\n` +
          `CDP: ${status.cdpUrl}\n\n` +
          `建立会话通道（见 SKILL.md「建立会话通道」）：\n` +
          `  1) 用浏览器打开 https://${status.domain}/seller/investClue\n` +
          `  2) 等待 3~5 秒完成公司 SSO(redpass) 登录（若跳登录页由用户本人登录一次）\n` +
          `  3) 确认页面显示为本人后，重新执行命令。\n`
      );
      return;
    }
    throw new UsageError(`未知的 auth 子命令 "${action}"，可选 set-token / status`);
  }

  if (subcommand === "commands") {
    const rows = listCommands().map((entry) => ({
      command: entry.command,
      path: entry.path,
      method: entry.method,
      mutating: entry.mutating,
      verified: entry.verified,
      summary: entry.summary,
    }));
    process.stdout.write(JSON.stringify(rows, null, 2) + "\n");
    return;
  }

  const entry = getSchemaByCommand(subcommand);
  if (!entry) {
    const valid = listCommands().map((c) => c.command).join(", ");
    throw new UsageError(`未知的子命令 "${subcommand}"，合法值：auth, commands, ${valid}`);
  }

  await runCommand(entry, rest);
}

main().catch((err) => {
  if (err instanceof UsageError) return fail(err.message, 1);
  if (err instanceof AuthError) return fail(err.message, 2);
  if (err instanceof UpstreamError) {
    process.stderr.write(`[${CLI_NAME}] ${err.message}\n`);
    if (err.body) {
      process.stderr.write(
        typeof err.body === "string" ? err.body : JSON.stringify(err.body, null, 2)
      );
      process.stderr.write("\n");
    }
    process.exit(3);
  }
  if (err instanceof NetworkError) return fail(err.message, 4);
  fail(`未预期的错误：${err.stack || err.message}`, 1);
});
