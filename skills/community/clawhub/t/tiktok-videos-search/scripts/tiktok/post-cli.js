#!/usr/bin/env node

const log = require("../utils/log");
const post = require("../api/post");
const token = require("../utils/token");
const utils = require("../utils/utils");
const validator = require("../validate/url");
const { assertChoice, assertIntegerRange } = require("../validate/keyword");
const { parseArgs, buildHelp } = require("../utils/args");
const {
  emitError,
  emitEmpty,
  printSuccessEnvelope,
  emitUncaught,
} = require("../utils/output");

const SCHEMA = {
  flags: {
    "--url": {
      alias: "-u",
      key: "url",
      type: "string",
      required: true,
      desc: "TikTok 博主主页、@用户名或 sec_uid",
    },
    "--sort": {
      alias: "-s",
      key: "sort",
      type: "number",
      default: 0,
      transform: (v) => Number(v),
      desc: "排序, 0: 最新(默认), 1: 最热",
    },
    "--limit": {
      alias: "-l",
      key: "limit",
      type: "number",
      default: 10,
      transform: (v) => Number(v),
      desc: "作品数量, 1-10000",
    },
  },
  positionalKey: "url",
};

const AUTH_MESSAGE =
  "GUAIKEI_API_TOKEN 未配置或格式无效。须为 16-256 位字母、数字、下划线或连字符";

function printHelp() {
  process.stderr.write(
    buildHelp(SCHEMA, "node scripts/tiktok/post-cli.js <主页或sec_uid> [选项]", [
      'node scripts/tiktok/post-cli.js --url "https://www.tiktok.com/@username" --limit 20',
      "node scripts/tiktok/post-cli.js --url username --sort 1 --limit 20",
    ]) +
      "\n\n注意:\n" +
      "  - 这是博主主页、@用户名或 MS4w 开头的 sec_uid，不是视频链接，也不是纯数字 aweme_id\n" +
      "  - 不传 --sort 时是 0（最新）。要最热请显式传 --sort 1\n" +
      "  - 搜索的 --sort 1 是最多点赞，不能照搬到这里\n" +
      "  - 排序和数量若不在允许范围内，命令会直接失败，不会改成默认值后继续请求\n" +
      "  - 数量 1-10000；包月 Token 实际最多 30，超限返回 PLAN_LIMIT\n",
  );
}

async function main() {
  const startTime = Date.now();
  const args = process.argv.slice(2);
  if (args.length === 0) {
    printHelp();
    emitError("post", "INVALID_ARGS", "缺少命令参数", 2, startTime);
    return;
  }

  let parsed;
  try {
    parsed = parseArgs(args, SCHEMA);
  } catch (error) {
    utils.printError(`参数解析错误: ${error.message}`);
    printHelp();
    emitError(
      "post",
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
  const urlRaw = url;

  utils.printBanner();
  utils.printInfo(`原始链接: ${urlRaw}`);
  try {
    url = validator.resolveProfileUrl(url);
  } catch (error) {
    utils.printError(error.message);
    emitError("post", "INVALID_URL", error.message, 1, startTime, {
      command: "post",
      url_raw: urlRaw,
    });
    return;
  }
  utils.printInfo(`规范后的链接: ${url}`);
  try {
    sort = assertChoice(sort, [0, 1], "排序 sort");
    limit = assertIntegerRange(limit, 1, 10000, "作品数量 limit");
  } catch (error) {
    utils.printError(error.message);
    emitError("post", "INVALID_ARGS", error.message, 2, startTime, {
      command: "post",
      url_raw: urlRaw,
      url,
      sort,
      limit,
    });
    return;
  }
  utils.printInfo(`排序: ${sort}, 数量: ${limit}`);

  const tokenValue = token.skillToken(process.env.GUAIKEI_API_TOKEN);
  if (tokenValue === "") {
    emitError("post", "AUTH_REQUIRED", AUTH_MESSAGE, 3, startTime, {
      command: "post",
      url_raw: urlRaw,
      url,
      sort,
      limit,
    });
    return;
  }

  const postRequest = {
    command: "post",
    url_raw: urlRaw,
    url,
    sort,
    limit,
  };
  let postTask = null;
  try {
    await post.createPostTask(tokenValue, url, sort, limit);
    utils.printSuccess("获取作品任务创建成功, 正在查询中...");
    postTask = await post.getPostTask(tokenValue, url, sort, limit);
  } catch (error) {
    utils.printError(`获取作品失败: ${error.message}`);
    emitError(
      "post",
      error.code || "UNKNOWN",
      error.message,
      error.name === "AuthError" ? 3 : 1,
      startTime,
      postRequest,
    );
    return;
  }

  if (!Array.isArray(postTask) || postTask.length === 0) {
    utils.printInfo("没有找到作品");
    emitEmpty("没有找到作品", startTime, postRequest);
    return;
  }

  const { payload: finalOutput, text } = printSuccessEnvelope(
    "获取作品任务完成",
    startTime,
    postRequest,
    postTask,
  );
  utils.printSuccess(`获取作品任务完成, 共 ${finalOutput.results.length} 条结果`);

  await log.taskWrite(`${startTime}_${validator.url2Name(url)}_post.json`, text);
}

main().catch((error) => {
  utils.printError(error.message || String(error));
  emitUncaught("post", error);
});
