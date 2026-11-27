#!/usr/bin/env node

const hot = require("../api/hot");
const token = require("../utils/token");
const utils = require("../utils/utils");
const { parseCliArgs, buildHelp } = require("../utils/args");
const { assertHotCategory, HOT_CATEGORIES } = require("../validate/hot");
const {
  emitError,
  emitEmpty,
  buildSuccessEnvelope,
  finishSuccess,
  emitUncaught,
} = require("../utils/output");

const SCHEMA = {
  flags: {
    "--category": {
      alias: "-c",
      key: "category",
      type: "string",
      default: "realtimehot",
      desc: "热搜榜: realtimehot 实时(默认), fun 文娱, social 社会, sportnav 体育, lifenav 生活, gamenav ACG, technologynav 科技",
    },
    "--save": {
      key: "save",
      type: "boolean",
      default: false,
      desc: "将完整结果写入本地日志（也可设 GUAIKEI_ENABLE_LOG=1）",
    },
  },
};

function printHelp() {
  process.stderr.write(
    buildHelp(SCHEMA, "node scripts/weibo/hot-cli.js [选项]", [
      "node scripts/weibo/hot-cli.js",
      "node scripts/weibo/hot-cli.js --category fun",
      'node scripts/weibo/hot-cli.js --json-args "{\\"category\\":\\"social\\"}"',
    ]) +
      "\n\n注意:\n" +
      `  - 类目只允许: ${HOT_CATEGORIES.join(", ")}\n` +
      "  - 省略 --category 使用 realtimehot；显式非法类目直接失败，不会改成默认榜\n" +
      "  - 热搜是异步任务，进程未退出前不要判定失败",
  );
}

async function main() {
  const startTime = Date.now();
  const args = process.argv.slice(2);

  let parsed;
  try {
    parsed = parseCliArgs(args, SCHEMA);
  } catch (error) {
    utils.printError(`参数解析错误: ${error.message}`);
    printHelp();
    emitError("hot", "INVALID_ARGS", `参数解析错误: ${error.message}`, 2, startTime);
    return;
  }
  if (parsed._help) {
    printHelp();
    return;
  }

  let category = parsed.category;
  utils.printBanner();
  try {
    category = assertHotCategory(category);
  } catch (error) {
    utils.printError(error.message);
    emitError("hot", "INVALID_ARGS", error.message, 2, startTime, {
      command: "hot",
      category: category,
    });
    return;
  }
  utils.printInfo(`热搜类目: ${category}`);

  const tokenValue = token.skillToken(process.env.GUAIKEI_API_TOKEN);
  if (tokenValue === "") {
    emitError(
      "hot",
      "AUTH_REQUIRED",
      "GUAIKEI_API_TOKEN 未配置或格式无效。须为 16-256 位字母、数字、下划线或连字符",
      3,
      startTime,
      { command: "hot", category: category },
    );
    return;
  }

  let rows = null;
  let taskCost;
  try {
    const taskId = await hot.createHotTask(tokenValue, category);
    utils.printSuccess("热搜任务创建成功, 正在获取中...");
    ({ results: rows, cost: taskCost } = await hot.getHotTask(
      tokenValue,
      category,
      taskId,
    ));
  } catch (error) {
    utils.printError(`获取微博热搜失败: ${error.message}`);
    emitError(
      "hot",
      error.code || "UNKNOWN",
      error.message,
      error.name === "AuthError" ? 3 : 1,
      startTime,
      { command: "hot", category: category },
    );
    return;
  }

  const request = { command: "hot", category: category };
  if (!rows || !Array.isArray(rows) || rows.length === 0) {
    utils.printInfo("没有找到热搜");
    emitEmpty("没有找到热搜", startTime, request, taskCost);
    return;
  }

  const finalOutput = buildSuccessEnvelope(
    "获取微博热搜任务完成",
    startTime,
    request,
    rows,
    rows.length,
    taskCost,
  );
  await finishSuccess(finalOutput, {
    logFilename: `${startTime}_${category}_hot.json`,
    stderrMessage: `热搜任务完成, 共返回 ${finalOutput.results.length} 条`,
    save: parsed.save === true,
  });
}

main().catch((error) => {
  utils.printError(error.message || String(error));
  emitUncaught("hot", error);
});
