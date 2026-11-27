#!/usr/bin/env node

const search = require("../api/search");
const token = require("../utils/token");
const utils = require("../utils/utils");
const validator = require("../validate/keyword");
const { assertSearchOptions } = require("../validate/search");
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
    "--keyword": {
      alias: "-k",
      key: "keyword",
      type: "string",
      required: true,
      desc: "搜索关键词",
    },
    "--search-type": {
      alias: "-s",
      key: "search_type",
      type: "number",
      default: 1,
      transform: parseDecimalInteger,
      desc: "搜索类型, 1: 综合(默认), 2: 实时, 3: 用户, 4: 视频, 5: 热门, 6: 话题, 7: 超话",
    },
    "--limit": {
      alias: "-l",
      key: "limit",
      type: "number",
      default: 10,
      transform: parseDecimalInteger,
      desc: "搜索数量, 1-10000",
    },
    "--save": {
      key: "save",
      type: "boolean",
      default: false,
      desc: "将完整结果写入本地日志（也可设 GUAIKEI_ENABLE_LOG=1）",
    },
  },
  positionalKey: "keyword",
};

function printHelp() {
  process.stderr.write(
    buildHelp(SCHEMA, "node scripts/weibo/search-cli.js <关键词> [选项]", [
      'node scripts/weibo/search-cli.js --keyword "AI"',
      "node scripts/weibo/search-cli.js --keyword AI --search-type 2 --limit 10",
      'node scripts/weibo/search-cli.js -k "AI 教程" -s 5 -l 20',
      'node scripts/weibo/search-cli.js --json-args "{\\"keyword\\":\\"AI 教程\\",\\"search_type\\":1,\\"limit\\":10}"',
    ]) +
      "\n\n注意:\n" +
      "  - 关键词 1-50 个字符，不能是链接, 不含 < > \" ' &\n" +
      "  - 类型只允许 1-7。非法类型或数量直接失败，不会改成默认值后继续搜索\n" +
      "  - 数量 1-10000；包月 Token 实际最多 30，超限返回 PLAN_LIMIT\n" +
      "  - 关键词以 - 开头时写成 --keyword=-AI，或在 -- 后面写位置参数",
  );
}

async function main() {
  const startTime = Date.now();
  const args = process.argv.slice(2);
  if (args.length === 0) {
    printHelp();
    emitError("search", "INVALID_ARGS", "缺少命令参数", 2, startTime);
    return;
  }

  let parsed;
  try {
    parsed = parseCliArgs(args, SCHEMA);
  } catch (error) {
    utils.printError(`参数解析错误: ${error.message}`);
    printHelp();
    emitError(
      "search",
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

  let { keyword, search_type: searchType, limit } = parsed;
  utils.printBanner();
  const keywordRaw = keyword;
  utils.printInfo(`原始关键词: ${keywordRaw}`);
  keyword = validator.normalizeKeyword(keyword);
  if (!validator.isKeywordValid(keyword)) {
    emitError(
      "search",
      "INVALID_KEYWORD",
      "关键词不合法: 需 1-50 个字符, 不能是链接, 不含 < > \" ' & 等特殊符号",
      1,
      startTime,
      {
        command: "search",
        keyword_raw: keywordRaw,
        keyword: keyword,
        search_type: searchType,
        limit: limit,
      },
    );
    return;
  }
  utils.printInfo(`清洗后关键词: ${keyword}`);
  try {
    [searchType, limit] = assertSearchOptions(searchType, limit);
  } catch (error) {
    utils.printError(error.message);
    emitError("search", "INVALID_ARGS", error.message, 2, startTime, {
      command: "search",
      keyword_raw: keywordRaw,
      keyword: keyword,
      search_type: searchType,
      limit: limit,
    });
    return;
  }
  utils.printInfo(`类型: ${searchType}, 数量: ${limit}`);

  const tokenValue = token.skillToken(process.env.GUAIKEI_API_TOKEN);
  if (tokenValue === "") {
    emitError(
      "search",
      "AUTH_REQUIRED",
      "GUAIKEI_API_TOKEN 未配置或格式无效。须为 16-256 位字母、数字、下划线或连字符",
      3,
      startTime,
      {
        command: "search",
        keyword_raw: keywordRaw,
        keyword: keyword,
        search_type: searchType,
        limit: limit,
      },
    );
    return;
  }

  let rows = null;
  let taskCost;
  try {
    const taskId = await search.createSearchTask(
      tokenValue,
      keyword,
      searchType,
      limit,
    );
    utils.printSuccess("搜索任务创建成功, 正在搜索中...");
    ({ results: rows, cost: taskCost } = await search.getSearchTask(
      tokenValue,
      keyword,
      searchType,
      limit,
      taskId,
    ));
  } catch (error) {
    utils.printError(`搜索失败: ${error.message}`);
    emitError(
      "search",
      error.code || "UNKNOWN",
      error.message,
      error.name === "AuthError" ? 3 : 1,
      startTime,
      {
        command: "search",
        keyword_raw: keywordRaw,
        keyword: keyword,
        search_type: searchType,
        limit: limit,
      },
    );
    return;
  }

  const request = {
    command: "search",
    keyword_raw: keywordRaw,
    keyword: keyword,
    search_type: searchType,
    limit: limit,
  };
  if (!rows || !Array.isArray(rows) || rows.length === 0) {
    utils.printInfo("没有找到匹配的微博");
    emitEmpty("没有找到匹配的微博", startTime, request, taskCost);
    return;
  }

  const finalOutput = buildSuccessEnvelope(
    "搜索任务完成",
    startTime,
    request,
    rows,
    undefined,
    taskCost,
  );
  await finishSuccess(finalOutput, {
    logFilename: `${startTime}_${keyword}_${searchType}_search.json`,
    stderrMessage: `搜索任务完成, 共返回 ${finalOutput.results.length} 条结果`,
    save: parsed.save === true,
  });
}

main().catch((error) => {
  utils.printError(error.message || String(error));
  emitUncaught("search", error);
});
