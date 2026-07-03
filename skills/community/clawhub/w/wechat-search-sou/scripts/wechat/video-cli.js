#!/usr/bin/env node

const constants = require("../config/constants");
const token = require("../utils/token");
const log = require("../utils/log");
const search = require("../api/video");
const utils = require("../utils/utils");
const validator = require("../validate/keyword");

function parseArgs(args) {
  const result = {
    keyword: "",
    sort: 0,
    duration: 0,
    limit: 10,
    helpRequested: false,
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === "--keyword" || arg === "-K") {
      result.keyword = args[i + 1] || "";
      i++;
    } else if (arg === "--sort" || arg === "-S") {
      result.sort = Number(args[i + 1]) || 0;
      i++;
    } else if (arg === "--duration" || arg === "-D") {
      result.duration = Number(args[i + 1]) || 0;
      i++;
    } else if (arg === "--limit" || arg === "-L") {
      result.limit = Number(args[i + 1]) || 10;
      i++;
    } else if (arg === "--help" || arg === "-H") {
      printHelp();
      result.helpRequested = true;
    } else if (!arg.startsWith("--") && !result.keyword) {
      result.keyword = arg;
    }
  }

  return result;
}

function printHelp() {
  console.log(`
用法: node scripts/wechat/video-cli.js <关键词> [选项]

选项:
  --keyword -K \t<关键词> \t搜索关键词
  --sort -S \t<排序> \t排序, 0:综合, 1:最新, 2:最热
  --duration -D \t<时长> \t视频时长, 0:不限, 1:5分钟以下, 2:5-20分钟, 3:20分钟以上
  --limit -L \t<数量> \t搜索数量 (默认 10, 最大 10000)
  --help -H \t显示帮助信息

示例1: node scripts/wechat/video-cli.js --keyword AI
示例2: node scripts/wechat/video-cli.js --keyword "AI 模型"
示例3: node scripts/wechat/video-cli.js --keyword AI --sort 2 --duration 1 --limit 10
示例4: node scripts/wechat/video-cli.js -K "AI 模型" -S 1 -D 1 -L 20

注意: 
  - 关键词建议 2-50 个汉字，避免特殊符号
`);
}

/**
 * 主函数 - 视频搜索任务入口
 * @description 解析命令行参数，执行搜索任务，输出结果并保存日志
 */
async function main() {
  const startTime = Date.now();
  const args = process.argv.slice(2);
  if (args.length === 0) {
    printHelp();
    return;
  }

  const parsedArgs = parseArgs(args);
  let { keyword, sort, duration, limit, helpRequested } = parsedArgs;

  if (helpRequested) return;
  if (!keyword) {
    utils.printError(`未提供关键词`);
    printHelp();
    return;
  }

  utils.printBanner();
  utils.printInfo(`原始关键词: ${keyword}`);
  keyword = validator.cleanKeyword(keyword);
  const isRight = validator.isKeywordValid(keyword);
  if (!isRight) {
    return;
  }
  utils.printInfo(`清洗后关键词: ${keyword}`);
  [sort, duration, _, limit] = validator.optionFormat(sort, duration, 0, limit);
  utils.printInfo(`排序: ${sort}, 时长: ${duration}, 数量: ${limit}`);

  const tokenValue = token.skillToken(process.env.GUAIKEI_API_TOKEN);
  if (tokenValue === "") return;
  let searchTask = null;
  try {
    const status = await search.createSearchTask(
      tokenValue,
      keyword,
      sort,
      duration,
      limit,
    );
    if (!status || status.errcode !== 0) {
      throw new Error(
        `视频搜索任务创建失败时, 遇到未知错误, 请反馈给开发者 ${status} - ${Date.now()}`,
      );
    }
    utils.printSuccess(`视频搜索任务创建成功, 正在搜索中...`);

    searchTask = await search.getSearchTask(
      tokenValue,
      keyword,
      sort,
      duration,
      limit,
    );
  } catch (error) {
    utils.printError(`视频搜索任务失败: ${error.message}`);
    const errorOutput = {
      status: "error",
      keyword: keyword,
      message: error.message,
      error_code: error.code || "UNKNOWN",
      limit: limit,
      timestamp: new Date().toLocaleString(),
      results: [],
    };
    console.log(JSON.stringify(errorOutput, null, 2));
    return;
  }

  if (!searchTask || !Array.isArray(searchTask) || searchTask.length === 0) {
    utils.printError(`视频搜索任务没有返回结果, 请稍后重试或联系开发者`);
    const emptyOutput = {
      status: "empty",
      keyword: keyword,
      message: "没有找到匹配的视频内容",
      error_code: "NO_MATCH",
      limit: limit,
      timestamp: new Date().toLocaleString(),
      results: [],
    };
    console.log(JSON.stringify(emptyOutput, null, 2));
    return;
  }

  // 输出搜索结果
  const finalOutput = {
    status: "success",
    keyword: keyword,
    message: "视频搜索任务完成",
    limit: limit,
    total: searchTask.length,
    timestamp: new Date().toLocaleString(),
    metadata: {
      skill_version: constants.VERSION,
      runtime_version: process.versions.node,
      execution_time: Date.now() - startTime,
    },
    results: searchTask,
  };
  console.log(JSON.stringify(finalOutput, null, 2));
  utils.printSuccess(`视频搜索任务完成, 共返回 ${finalOutput.total} 条结果`);

  await log.taskWrite(
    `${startTime}_${keyword}_video.json`,
    JSON.stringify(finalOutput, null, 2),
  );
}

main().catch((error) => {
  utils.printError(error);
  process.exit(1);
});
