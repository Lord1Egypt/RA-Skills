#!/usr/bin/env node

const search = require("../api/article");
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
    "--publishTime": {
      alias: "-t",
      key: "publishTime",
      type: "number",
      default: 0,
      transform: parseDecimalInteger,
      desc: "发布时间, 0:不限(默认), 1:最近1天, 2:最近7天, 3:最近半年",
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
    buildHelp(SCHEMA, "node scripts/wechat/article-cli.js <关键词> [选项]", [
      'node scripts/wechat/article-cli.js --keyword "AI"',
      'node scripts/wechat/article-cli.js --keyword "AI 模型"',
      "node scripts/wechat/article-cli.js --keyword AI --sort 2 --publishTime 1 --limit 10",
      'node scripts/wechat/article-cli.js -k "AI 模型" -s 1 -t 1 -l 20',
    ]) +
      "\n\n注意:\n" +
      "  - 关键词建议 2-50 个字符，不能是链接, 不含 < > \" ' &\n" +
      "  - 排序、发布时间、数量若不在允许范围内，命令会直接失败，不会改成默认值后继续搜索\n" +
      "  - 数量 1-10000；包月 Token 实际最多 20，超限返回 PLAN_LIMIT\n" +
      "  - 关键词以 - 开头时写成 --keyword=-AI，或在 -- 后面写位置参数",
  );
}

async function main() {
  const startTime = Date.now();
  const args = process.argv.slice(2);
  if (args.length === 0) {
    printHelp();
    emitError("article", "INVALID_ARGS", "缺少命令参数", 2, startTime);
    return;
  }

  let parsed;
  try {
    parsed = parseArgs(args, SCHEMA);
  } catch (error) {
    utils.printError(`参数解析错误: ${error.message}`);
    printHelp();
    emitError(
      "article",
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
  let { keyword, sort, publishTime, limit } = parsed;

  utils.printBanner();
  const keywordRaw = keyword;
  utils.printInfo(`原始关键词: ${keywordRaw}`);
  keyword = validator.normalizeKeyword(keyword);
  if (!validator.isKeywordValid(keyword)) {
    emitError(
      "article",
      "INVALID_KEYWORD",
      "关键词不合法: 需 2-50 个字符, 不能是链接, 不含 < > \" ' & 等特殊符号",
      1,
      startTime,
      {
        command: "article",
        keyword_raw: keywordRaw,
        keyword: keyword,
        sort: sort,
        publishTime: publishTime,
        limit: limit,
      },
    );
    return;
  }
  utils.printInfo(`清洗后关键词: ${keyword}`);
  try {
    [sort, publishTime, limit] = validator.assertArticleOptions(
      sort,
      publishTime,
      limit,
    );
  } catch (error) {
    utils.printError(error.message);
    emitError("article", "INVALID_ARGS", error.message, 2, startTime, {
      command: "article",
      keyword_raw: keywordRaw,
      keyword: keyword,
      sort: sort,
      publishTime: publishTime,
      limit: limit,
    });
    return;
  }
  utils.printInfo(
    `排序: ${sort}, 发布时间: ${publishTime}, 数量: ${limit}`,
  );

  const tokenValue = token.skillToken(process.env.GUAIKEI_API_TOKEN);
  if (tokenValue === "") {
    emitError(
      "article",
      "AUTH_REQUIRED",
      "GUAIKEI_API_TOKEN 未配置或格式无效。须为 16-256 位字母、数字、下划线或连字符",
      3,
      startTime,
      {
        command: "article",
        keyword_raw: keywordRaw,
        keyword: keyword,
        sort: sort,
        publishTime: publishTime,
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
      publishTime,
      limit,
    );
    utils.printSuccess(`文章搜索任务创建成功, 正在搜索中...`);

    searchTask = await search.getSearchTask(
      tokenValue,
      keyword,
      sort,
      publishTime,
      limit,
    );
  } catch (error) {
    utils.printError(`文章搜索失败: ${error.message}`);
    emitError(
      "article",
      error.code || "UNKNOWN",
      error.message,
      error.name === "AuthError" ? 3 : 1,
      startTime,
      {
        command: "article",
        keyword_raw: keywordRaw,
        keyword: keyword,
        sort: sort,
        publishTime: publishTime,
        limit: limit,
      },
    );
    return;
  }

  const searchRequest = {
    command: "article",
    keyword_raw: keywordRaw,
    keyword: keyword,
    sort: sort,
    publishTime: publishTime,
    limit: limit,
  };
  if (!searchTask || !Array.isArray(searchTask) || searchTask.length === 0) {
    utils.printInfo("没有找到匹配的文章");
    emitEmpty("没有找到匹配的文章", startTime, searchRequest);
    return;
  }

  const finalOutput = buildSuccessEnvelope(
    "文章搜索任务完成",
    startTime,
    searchRequest,
    searchTask,
    searchTask.length,
  );
  await finishSuccess(finalOutput, {
    logFilename: `${startTime}_${keyword}_${sort}_${publishTime}_article.json`,
    stderrMessage: `文章搜索任务完成, 共返回 ${finalOutput.results.length} 条结果`,
  });
}

main().catch((error) => {
  utils.printError(error.message || String(error));
  emitUncaught("article", error);
});
