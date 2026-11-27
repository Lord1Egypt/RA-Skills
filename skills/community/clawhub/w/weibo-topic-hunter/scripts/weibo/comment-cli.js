#!/usr/bin/env node

const comment = require("../api/comment");
const token = require("../utils/token");
const utils = require("../utils/utils");
const { parseWeiboUrl, assertCommentOptions } = require("../validate/comment");
const { parseCliArgs, buildHelp, parseDecimalInteger } = require("../utils/args");
const {
  emitError,
  emitEmpty,
  buildSuccessEnvelope,
  finishSuccess,
  emitUncaught,
} = require("../utils/output");

const SCHEMA = {
  flags: {
    "--url": {
      alias: "-u",
      key: "url",
      type: "string",
      required: true,
      desc: "微博链接",
    },
    "--sort": {
      alias: "-s",
      key: "sort",
      type: "number",
      default: 0,
      transform: parseDecimalInteger,
      desc: "排序, 0: 按热度(默认), 1: 按时间",
    },
    "--limit": {
      alias: "-l",
      key: "limit",
      type: "number",
      default: 10,
      transform: parseDecimalInteger,
      desc: "评论数量, 1-10000",
    },
    "--save": {
      key: "save",
      type: "boolean",
      default: false,
      desc: "将完整结果写入本地日志（也可设 GUAIKEI_ENABLE_LOG=1）",
    },
  },
  positionalKey: "url",
};

function printHelp() {
  process.stderr.write(
    buildHelp(SCHEMA, "node scripts/weibo/comment-cli.js <微博链接> [选项]", [
      'node scripts/weibo/comment-cli.js --url "https://weibo.com/1234567890/AbCdEfGhI"',
      'node scripts/weibo/comment-cli.js --url "https://m.weibo.cn/detail/1234567890" --sort 1 --limit 20',
      'node scripts/weibo/comment-cli.js --json-args "{\\"url\\":\\"https://weibo.com/detail/1234567890\\",\\"sort\\":0,\\"limit\\":10}"',
    ]) +
      "\n\n注意:\n" +
      "  - 链接须含 weibo.com/ 或 weibo.cn/，长度 1-255。常见形态: weibo.com/uid/mid、weibo.com/detail/mid、weibo.com/status/mid、m.weibo.cn/detail/mid、m.weibo.cn/status/mid\n" +
      "  - 排序只允许 0 或 1。非法排序或数量直接失败，不会改成默认值后继续\n" +
      "  - 数量 1-10000；包月 Token 实际最多 50，超限返回 PLAN_LIMIT",
  );
}

async function main() {
  const startTime = Date.now();
  const args = process.argv.slice(2);
  if (args.length === 0) {
    printHelp();
    emitError("comment", "INVALID_ARGS", "缺少命令参数", 2, startTime);
    return;
  }

  let parsed;
  try {
    parsed = parseCliArgs(args, SCHEMA);
  } catch (error) {
    utils.printError(`参数解析错误: ${error.message}`);
    printHelp();
    emitError(
      "comment",
      "INVALID_ARGS",
      `参数解析错误: ${error.message}`,
      2,
      startTime,
    );
    return;
  }
  if (parsed._help) {
    printHelp();
    return;
  }

  let { url, sort, limit } = parsed;
  utils.printBanner();
  const urlRaw = url;
  url = parseWeiboUrl(url);
  if (!url) {
    emitError(
      "comment",
      "INVALID_URL",
      "无法识别微博链接。支持 weibo.com/uid/mid、weibo.com/detail/mid、weibo.com/status/mid、m.weibo.cn/detail/mid、m.weibo.cn/status/mid",
      1,
      startTime,
      { command: "comment", url: urlRaw, sort: sort, limit: limit },
    );
    return;
  }
  try {
    [sort, limit] = assertCommentOptions(sort, limit);
  } catch (error) {
    utils.printError(error.message);
    emitError("comment", "INVALID_ARGS", error.message, 2, startTime, {
      command: "comment",
      url: url,
      sort: sort,
      limit: limit,
    });
    return;
  }
  utils.printInfo(`排序: ${sort}, 数量: ${limit}`);

  const tokenValue = token.skillToken(process.env.GUAIKEI_API_TOKEN);
  if (tokenValue === "") {
    emitError(
      "comment",
      "AUTH_REQUIRED",
      "GUAIKEI_API_TOKEN 未配置或格式无效。须为 16-256 位字母、数字、下划线或连字符",
      3,
      startTime,
      { command: "comment", url: url, sort: sort, limit: limit },
    );
    return;
  }

  let rows = null;
  let taskCost;
  try {
    const taskId = await comment.createCommentTask(tokenValue, url, sort, limit);
    utils.printSuccess("评论任务创建成功, 正在获取中...");
    ({ results: rows, cost: taskCost } = await comment.getCommentTask(
      tokenValue,
      url,
      sort,
      limit,
      taskId,
    ));
  } catch (error) {
    utils.printError(`获取评论失败: ${error.message}`);
    emitError(
      "comment",
      error.code || "UNKNOWN",
      error.message,
      error.name === "AuthError" ? 3 : 1,
      startTime,
      { command: "comment", url: url, sort: sort, limit: limit },
    );
    return;
  }

  const request = { command: "comment", url: url, sort: sort, limit: limit };
  if (!rows || !Array.isArray(rows) || rows.length === 0) {
    utils.printInfo("没有找到匹配的评论");
    emitEmpty("没有找到匹配的评论", startTime, request, taskCost);
    return;
  }

  const finalOutput = buildSuccessEnvelope(
    "获取评论任务完成",
    startTime,
    request,
    rows,
    undefined,
    taskCost,
  );
  await finishSuccess(finalOutput, {
    logFilename: `${startTime}_${sort}_comment.json`,
    stderrMessage: `评论任务完成, 共返回 ${finalOutput.results.length} 条结果`,
    save: parsed.save === true,
  });
}

main().catch((error) => {
  utils.printError(error.message || String(error));
  emitUncaught("comment", error);
});
