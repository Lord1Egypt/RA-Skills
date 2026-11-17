#!/usr/bin/env node

const search = require("../api/video");
const token = require("../utils/token");
const utils = require("../utils/utils");
const validator = require("../validate/keyword");
const { parseArgs, buildHelp, parseDecimalInteger } = require("../utils/args");
const {
  emitError,
  emitEmpty,
  buildSuccessEnvelope,
  finishSuccess,
  emitUncaught,
} = require("../utils/output");

const SCHEMA = {
  flags: {
    "--keyword": {
      alias: "-k",
      key: "keyword",
      type: "string",
      required: true,
      desc: "搜索关键词",
    },
    "--sort": {
      alias: "-s",
      key: "sort",
      type: "number",
      default: 0,
      transform: parseDecimalInteger,
      desc: "排序, 0:综合(默认), 1:最新, 2:最热",
    },
    "--duration": {
      alias: "-d",
      key: "duration",
      type: "number",
      default: 0,
      transform: parseDecimalInteger,
      desc: "视频时长, 0:不限(默认), 1:5分钟以下, 2:5-20分钟, 3:20分钟以上",
    },
    "--limit": {
      alias: "-l",
      key: "limit",
      type: "number",
      default: 10,
      transform: parseDecimalInteger,
      desc: "搜索数量, 1-10000（包月 Token 实际最多 20）",
    },
  },
  positionalKey: "keyword",
};

function printHelp() {
  process.stderr.write(
    buildHelp(SCHEMA, "node scripts/wechat/video-cli.js <关键词> [选项]", [
      'node scripts/wechat/video-cli.js --keyword "AI"',
      'node scripts/wechat/video-cli.js --keyword "AI 模型"',
      "node scripts/wechat/video-cli.js --keyword AI --sort 1 --duration 2 --limit 10",
      'node scripts/wechat/video-cli.js -k "AI 模型" -s 2 -d 1 -l 20',
    ]) +
      "\n\n注意:\n" +
      "  - 关键词建议 2-50 个字符，不能是链接, 不含 < > \" ' &\n" +
      "  - 排序、时长、数量若不在允许范围内，命令会直接失败，不会改成默认值后继续搜索\n" +
      "  - 数量 1-10000；包月 Token 实际最多 20，超限返回 PLAN_LIMIT\n" +
      "  - 关键词以 - 开头时写成 --keyword=-AI，或在 -- 后面写位置参数",
  );
}

async function main() {
  const startTime = Date.now();
  const args = process.argv.slice(2);
  if (args.length === 0) {
    printHelp();
    emitError("video", "INVALID_ARGS", "缺少命令参数", 2, startTime);
    return;
  }

  let parsed;
  try {
    parsed = parseArgs(args, SCHEMA);
  } catch (error) {
    utils.printError(`参数解析错误: ${error.message}`);
    printHelp();
    emitError(
      "video",
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
  let { keyword, sort, duration, limit } = parsed;

  utils.printBanner();
  const keywordRaw = keyword;
  utils.printInfo(`原始关键词: ${keywordRaw}`);
  keyword = validator.normalizeKeyword(keyword);
  if (!validator.isKeywordValid(keyword)) {
    emitError(
      "video",
      "INVALID_KEYWORD",
      "关键词不合法: 需 2-50 个字符, 不能是链接, 不含 < > \" ' & 等特殊符号",
      1,
      startTime,
      {
        command: "video",
        keyword_raw: keywordRaw,
        keyword: keyword,
        sort: sort,
        duration: duration,
        limit: limit,
      },
    );
    return;
  }
  utils.printInfo(`清洗后关键词: ${keyword}`);
  try {
    [sort, duration, limit] = validator.assertVideoOptions(
      sort,
      duration,
      limit,
    );
  } catch (error) {
    utils.printError(error.message);
    emitError("video", "INVALID_ARGS", error.message, 2, startTime, {
      command: "video",
      keyword_raw: keywordRaw,
      keyword: keyword,
      sort: sort,
      duration: duration,
      limit: limit,
    });
    return;
  }
  utils.printInfo(`排序: ${sort}, 时长: ${duration}, 数量: ${limit}`);

  const tokenValue = token.skillToken(process.env.GUAIKEI_API_TOKEN);
  if (tokenValue === "") {
    emitError(
      "video",
      "AUTH_REQUIRED",
      "GUAIKEI_API_TOKEN 未配置或格式无效。须为 16-256 位字母、数字、下划线或连字符",
      3,
      startTime,
      {
        command: "video",
        keyword_raw: keywordRaw,
        keyword: keyword,
        sort: sort,
        duration: duration,
        limit: limit,
      },
    );
    return;
  }

  let searchTask = null;
  try {
    await search.createSearchTask(
      tokenValue,
      keyword,
      sort,
      duration,
      limit,
    );
    utils.printSuccess(`视频搜索任务创建成功, 正在搜索中...`);

    searchTask = await search.getSearchTask(
      tokenValue,
      keyword,
      sort,
      duration,
      limit,
    );
  } catch (error) {
    utils.printError(`视频搜索失败: ${error.message}`);
    emitError(
      "video",
      error.code || "UNKNOWN",
      error.message,
      error.name === "AuthError" ? 3 : 1,
      startTime,
      {
        command: "video",
        keyword_raw: keywordRaw,
        keyword: keyword,
        sort: sort,
        duration: duration,
        limit: limit,
      },
    );
    return;
  }

  const searchRequest = {
    command: "video",
    keyword_raw: keywordRaw,
    keyword: keyword,
    sort: sort,
    duration: duration,
    limit: limit,
  };
  if (!searchTask || !Array.isArray(searchTask) || searchTask.length === 0) {
    utils.printInfo("没有找到匹配的视频内容");
    emitEmpty("没有找到匹配的视频内容", startTime, searchRequest);
    return;
  }

  const finalOutput = buildSuccessEnvelope(
    "视频搜索任务完成",
    startTime,
    searchRequest,
    searchTask,
    searchTask.length,
  );
  await finishSuccess(finalOutput, {
    logFilename: `${startTime}_${keyword}_${sort}_${duration}_video.json`,
    stderrMessage: `视频搜索任务完成, 共返回 ${finalOutput.results.length} 条结果`,
  });
}

main().catch((error) => {
  utils.printError(error.message || String(error));
  emitUncaught("video", error);
});
