const REALTIME_NEWS_URL =
  "https://quantaccess.lxaa.top/api/v1/news/realtime_news";
const TOKEN_ENV_NAME = "TradeAlphaToken";
const TOKEN_GUIDE_URL = "https://quantaccess.lxaa.top/#/login";

const MIN_NEWS_TIME = "2025-04-01 00:00:00";
const DATE_ONLY_PATTERN = /^\d{4}-\d{2}-\d{2}$/;
const DATE_TIME_PATTERN = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/;
const NEWS_SOURCES = [
  "domestic",
  "truth",
  "bloomberg",
  "rtrs",
  "research_report",
];
const NEWS_CATEGORIES = [
  "政治军事",
  "社会",
  "娱乐体育",
  "公司",
  "超大型公司",
  "政策",
  "市场与货币",
];
const NEWS_LEVELS = ["很重要", "重要", "一般"];

function printHelp() {
  console.log("TradeAlpha 实时新闻脚本");
  console.log("");
  console.log("用法:");
  console.log("  node scripts/get-realtime-news.js");
  console.log(
    '  node scripts/get-realtime-news.js \'{"source":"bloomberg","level":"重要","page_size":5}\'',
  );
  console.log("");
  console.log("支持字段:");
  console.log("  start_time, end_time, source, category, level, page, page_size");
}

function printJson(payload, error = false) {
  const encoded = JSON.stringify(payload, null, 2);
  if (error) {
    console.error(encoded);
    return;
  }

  console.log(encoded);
}

function readStoredToken() {
  const envToken = process.env[TOKEN_ENV_NAME]?.trim();
  if (envToken) {
    return {
      token: envToken,
      token_source: "env",
    };
  }

  return {
    token: null,
    token_source: "none",
  };
}

function parseInput(argv) {
  const firstArg = argv[0];
  if (!firstArg) {
    return {};
  }

  if (firstArg === "--help" || firstArg === "-h") {
    printHelp();
    process.exit(0);
  }

  try {
    const parsed = JSON.parse(firstArg);
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
      throw new Error("输入必须是 JSON 对象。");
    }
    return parsed;
  } catch (error) {
    throw new Error(
      `参数必须是单个 JSON 对象字符串，例如 '{"source":"bloomberg","page_size":5}'。原始错误：${
        error instanceof Error ? error.message : String(error)
      }`,
    );
  }
}

function parseOptionalString(args, key) {
  const value = args[key];
  if (value == null) {
    return undefined;
  }

  if (typeof value !== "string") {
    throw new Error(`参数 \`${key}\` 必须是字符串。`);
  }

  const trimmed = value.trim();
  return trimmed || undefined;
}

function parseOptionalInteger(args, key) {
  const value = args[key];
  if (value == null) {
    return undefined;
  }

  if (typeof value === "number" && Number.isInteger(value)) {
    return value;
  }

  if (typeof value === "string" && value.trim() !== "") {
    const parsed = Number(value);
    if (Number.isInteger(parsed)) {
      return parsed;
    }
  }

  throw new Error(`参数 \`${key}\` 必须是整数。`);
}

function validateEnum(value, key, allowedValues) {
  if (!value) {
    return undefined;
  }

  if (!allowedValues.includes(value)) {
    throw new Error(
      `参数 \`${key}\` 取值无效，可选值为：${allowedValues.join("、")}。`,
    );
  }

  return value;
}

function normalizeComparableTime(value) {
  return DATE_ONLY_PATTERN.test(value) ? `${value} 00:00:00` : value;
}

function validateTimeFormat(value, key) {
  if (!DATE_ONLY_PATTERN.test(value) && !DATE_TIME_PATTERN.test(value)) {
    throw new Error(
      `参数 \`${key}\` 格式无效，必须为 YYYY-MM-DD 或 YYYY-MM-DD HH:mm:ss。`,
    );
  }

  if (normalizeComparableTime(value) < MIN_NEWS_TIME) {
    throw new Error(
      `参数 \`${key}\` 不能早于 2025-04-01 00:00:00（北京时间）。`,
    );
  }
}

function buildRequest(rawArgs) {
  const start_time = parseOptionalString(rawArgs, "start_time");
  const end_time = parseOptionalString(rawArgs, "end_time");
  const source = validateEnum(
    parseOptionalString(rawArgs, "source"),
    "source",
    NEWS_SOURCES,
  );
  const category = validateEnum(
    parseOptionalString(rawArgs, "category"),
    "category",
    NEWS_CATEGORIES,
  );
  const level = validateEnum(
    parseOptionalString(rawArgs, "level"),
    "level",
    NEWS_LEVELS,
  );
  const page = parseOptionalInteger(rawArgs, "page") ?? 1;
  const page_size = parseOptionalInteger(rawArgs, "page_size") ?? 20;

  if (start_time) {
    validateTimeFormat(start_time, "start_time");
  }
  if (end_time) {
    validateTimeFormat(end_time, "end_time");
  }
  if (
    start_time &&
    end_time &&
    normalizeComparableTime(start_time) > normalizeComparableTime(end_time)
  ) {
    throw new Error("`start_time` 不能晚于 `end_time`。");
  }
  if (page < 1) {
    throw new Error("参数 `page` 必须大于或等于 1。");
  }
  if (page_size < 1 || page_size > 100) {
    throw new Error("参数 `page_size` 必须在 1 到 100 之间。");
  }

  return {
    start_time,
    end_time,
    source,
    category,
    level,
    page,
    page_size,
  };
}

async function fetchRealtimeNews(request, token) {
  const response = await fetch(REALTIME_NEWS_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      ...request,
      token,
    }),
  });

  let payload;
  try {
    payload = await response.json();
  } catch {
    throw new Error(`新闻接口返回了非 JSON 响应，HTTP ${response.status}。`);
  }

  if (!response.ok || payload?.code !== 0 || !payload?.data) {
    const detail =
      typeof payload?.message === "string"
        ? payload.message
        : `HTTP ${response.status}`;
    const codeText =
      typeof payload?.code === "number" ? `（code: ${payload.code}）` : "";
    const error = new Error(`获取新闻失败${codeText}：${detail}`);
    error.tradealpha_code =
      typeof payload?.code === "number" ? payload.code : null;
    throw error;
  }

  return payload.data;
}

async function main() {
  const args = parseInput(process.argv.slice(2));
  const request = buildRequest(args);
  const auth = readStoredToken();

  if (!auth.token) {
    printJson(
      {
        success: false,
        auth_required: false,
        next_action: "set_env",
        token_source: auth.token_source,
        error: `未找到环境变量 \`${TOKEN_ENV_NAME}\`。请先前往 ${TOKEN_GUIDE_URL} 注册并登录，获取 token 后将其设置到系统环境变量 \`${TOKEN_ENV_NAME}\` 中。`,
        message: `当前还没有可用 token，请先设置环境变量 \`${TOKEN_ENV_NAME}\`。`,
        guide_url: TOKEN_GUIDE_URL,
      },
      true,
    );
    process.exitCode = 1;
    return;
  }

  const data = await fetchRealtimeNews(request, auth.token);
  printJson({
    success: true,
    auth_required: false,
    next_action: "none",
    token_source: auth.token_source,
    request,
    total: data.total,
    page: data.page,
    page_size: data.page_size,
    list: data.list,
    note: "新闻数据通常存在 0-5 分钟客观延迟。",
  });
}

main().catch((error) => {
  const message = error instanceof Error ? error.message : String(error);
  const tradealphaCode =
    typeof error?.tradealpha_code === "number" ? error.tradealpha_code : null;
  const tokenInvalid = tradealphaCode === 1001;

  printJson(
    {
      success: false,
      auth_required: false,
      next_action: tokenInvalid ? "set_env" : "fetch_news",
      token_source: "none",
      error: message,
      error_code: tradealphaCode,
      message: tokenInvalid
        ? `环境变量 \`${TOKEN_ENV_NAME}\` 中的 token 无效或已过期，请前往 ${TOKEN_GUIDE_URL} 重新获取后更新环境变量。`
        : "新闻拉取失败，请检查参数或稍后重试。",
      guide_url: tokenInvalid ? TOKEN_GUIDE_URL : undefined,
    },
    true,
  );
  process.exitCode = 1;
});
