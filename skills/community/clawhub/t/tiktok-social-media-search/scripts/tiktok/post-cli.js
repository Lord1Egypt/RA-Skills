#!/usr/bin/env node

const constants = require("../config/constants");
const log = require("../utils/log");
const post = require("../api/post");
const token = require("../utils/token");
const utils = require("../utils/utils");
const validator = require("../validate/post");
const { ApiError } = require("../utils/errors");
const { parseArgs, buildHelp } = require("../utils/args");

const SCHEMA = {
  flags: {
    "--url": {
      alias: "-u",
      key: "url",
      type: "string",
      required: true,
      desc: "TikTok博主主页URL或sec_uid",
    },
    "--sort": {
      alias: "-s",
      key: "sort",
      type: "number",
      default: 0,
      transform: (v) => Number(v),
      desc: "排序依据, 0: 最新(默认), 1: 最热",
    },
    "--limit": {
      alias: "-l",
      key: "limit",
      type: "number",
      default: 10,
      transform: (v) => Number(v),
      desc: "搜索数量, 1-10000",
    },
  },
  positionalKey: "url",
};

function printHelp() {
  console.log(
    buildHelp(SCHEMA, "node scripts/tiktok/post-cli.js <url> [选项]", [
      "node scripts/tiktok/post-cli.js https://www.tiktok.com/@xxx",
      'node scripts/tiktok/post-cli.js --url "https://www.tiktok.com/@xxx" --limit 20',
      'node scripts/tiktok/post-cli.js -u "xxx" -l 100',
    ]),
  );
}

/**
 * 主函数 - 获取TikTok博主作品列表
 */
async function main() {
  const startTime = Date.now();
  const args = process.argv.slice(2);
  if (args.length === 0) {
    printHelp();
    process.exit(0);
  }

  let parsed;
  try {
    parsed = parseArgs(args, SCHEMA);
  } catch (error) {
    utils.printError(`参数解析错误: ${error.message}`);
    printHelp();
    process.exit(1);
  }
  if (parsed._help) {
    printHelp();
    process.exit(0);
  }

  let { url, sort, limit } = parsed;

  utils.printBanner();
  utils.printInfo(`原始URL: ${url}`);
  url = validator.tiktokUserUrl(url);
  utils.printInfo(`规范后的URL: ${url}`);
  [sort, limit] = validator.optionFormat(sort, limit);

  const tokenValue = token.skillToken(process.env.GUAIKEI_API_TOKEN);
  if (tokenValue === "") process.exit(3);
  let postTask = null;
  try {
    await post.createPostTask(tokenValue, url, sort, limit);
    utils.printSuccess(`获取作品任务创建成功, 正在获取作品中...`);

    postTask = await post.getPostTask(tokenValue, url, sort, limit);
  } catch (error) {
    utils.printError(`获取作品失败: ${error.message}`);
    const errorOutput = {
      status: "error",
      error_code: error.code || "UNKNOWN",
      message: error.message,
      timestamp: new Date().toLocaleString(),
      request: {
        command: "post",
        url: url,
        sort: sort,
        limit: limit,
      },
      metadata: {
        skill_version: constants.VERSION,
        runtime_version: process.versions.node,
        execution_time: Date.now() - startTime,
      },
      results: null,
    };
    const exitCode = error.name === "AuthError" ? 3 : 1;
    process.stdout.write(JSON.stringify(errorOutput, null, 2) + "\n", () =>
      process.exit(exitCode),
    );
    return;
  }

  if (!postTask || !Array.isArray(postTask) || postTask.length === 0) {
    utils.printError(`获取作品任务没有返回结果, 请稍后重试或联系开发者`);
    const emptyOutput = {
      status: "empty",
      error_code: "NO_MATCH",
      message: "没有找到匹配的作品",
      timestamp: new Date().toLocaleString(),
      request: {
        command: "post",
        url: url,
        sort: sort,
        limit: limit,
      },
      metadata: {
        skill_version: constants.VERSION,
        runtime_version: process.versions.node,
        execution_time: Date.now() - startTime,
      },
      results: null,
    };
    process.stdout.write(JSON.stringify(emptyOutput, null, 2) + "\n", () =>
      process.exit(0),
    );
    return;
  }

  // 输出作品结果
  const finalOutput = {
    status: "success",
    error_code: "OK",
    message: "获取作品任务完成",
    timestamp: new Date().toLocaleString(),
    request: {
      command: "post",
      url: url,
      sort: sort,
      limit: limit,
    },
    metadata: {
      skill_version: constants.VERSION,
      runtime_version: process.versions.node,
      execution_time: Date.now() - startTime,
    },
    results: postTask,
  };
  console.log(JSON.stringify(finalOutput, null, 2));
  utils.printSuccess(
    `获取作品任务完成, 共 ${finalOutput.results.length} 条结果`,
  );

  url = url.replace(/[^a-zA-Z0-9_-]/g, "");
  url = url.replace("httpswwwtiktokcomvideo", "");
  await log.taskWrite(
    `${startTime}_${url}_post.json`,
    JSON.stringify(finalOutput, null, 2),
  );
}

main().catch((error) => {
  utils.printError(error.message);
  process.exit(1);
});
