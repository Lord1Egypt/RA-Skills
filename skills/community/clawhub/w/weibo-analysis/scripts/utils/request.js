const https = require("https");
const querystring = require("querystring");
const constants = require("../config/constants");
const { withRetry } = require("../utils/retry");
const {
  SkillError,
  ApiError,
  NetworkError,
  TimeoutError,
  AuthError,
} = require("./errors");
const { mapBackendApiError } = require("./backendCodes");
const utils = require("../utils/utils");
const { skillName } = require("../utils/name");

async function request(options, data = null) {
  return new Promise((resolve, reject) => {
    let timedOut = false;

    const req = https.request(
      { ...options, timeout: constants.REQUEST_TIMEOUT },
      (res) => {
        res.setEncoding("utf-8");
        let body = "";
        res.on("data", (chunk) => (body += chunk));
        res.on("end", () => {
          if (timedOut) return;
          if (res.statusCode === 200) {
            try {
              const jsonBody = JSON.parse(body);
              if (typeof jsonBody.errcode !== "number") {
                const e = new ApiError(
                  "API_ERROR",
                  "接口响应缺少有效的 errcode",
                  true,
                );
                reject(e);
              } else if (jsonBody.errcode === 0) {
                resolve(jsonBody);
              } else if (
                jsonBody.errcode === 401 ||
                jsonBody.errcode === 403
              ) {
                const e = new AuthError(
                  "GUAIKEI_API_TOKEN 无效, 请检查环境变量 或 通过 www.guaikei.com 联系客服获取解决方案",
                );
                e.noRetry = true;
                reject(e);
              } else {
                reject(
                  mapBackendApiError(
                    jsonBody.errcode,
                    jsonBody.errmsg || "请求失败",
                  ),
                );
              }
            } catch (parseError) {
              reject(new NetworkError(`响应解析失败: ${parseError.message}`));
            }
          } else if (res.statusCode === 401 || res.statusCode === 403) {
            const e = new AuthError(
              "GUAIKEI_API_TOKEN 无效, 请检查环境变量 或 通过 www.guaikei.com 联系客服获取解决方案",
            );
            e.noRetry = true;
            reject(e);
          } else {
            const status = res.statusCode;
            if (status === 429) {
              // 传输层 429：可退避重试；与业务裸 errcode 2（noRetry）区分
              reject(
                new ApiError(
                  "RATE_LIMITED",
                  `请求过于频繁 (HTTP 429)，请稍后重试`,
                  false,
                ),
              );
            } else if (status >= 500 && status <= 599) {
              reject(
                new ApiError(
                  "HTTP_5xx",
                  `请求失败, 状态码: ${status}`,
                  false,
                ),
              );
            } else if (status === 404) {
              reject(
                new ApiError(
                  "HTTP_404",
                  "请求的接口路径不存在 (HTTP 404)，请升级技能或联系 www.guaikei.com 客服",
                  true,
                ),
              );
            } else if (status === 410) {
              // 传输层 HTTP 410；业务 JSON errcode 410（TOKEN 停用）不走这里
              reject(
                new ApiError(
                  "HTTP_410",
                  "上游返回 HTTP 410 Gone（传输层）。若信封曾是业务码 Gone，多为 TOKEN 停用而非接口下线；请核对 TOKEN 或联系客服",
                  true,
                ),
              );
            } else {
              reject(
                new ApiError(
                  `HTTP_${status}`,
                  `请求失败, 状态码: ${status}`,
                  true,
                ),
              );
            }
          }
        });
      },
    );

    req.on("error", (err) => {
      if (timedOut) {
        return;
      }
      if (err.code === "ETIMEDOUT" || err.code === "ECONNRESET") {
        reject(new TimeoutError("请求超时或连接被重置"));
      } else {
        reject(new NetworkError(`网络错误: ${err.message}`));
      }
    });

    req.on("timeout", () => {
      timedOut = true;
      req.destroy();
      reject(new TimeoutError(`请求超时 (${constants.REQUEST_TIMEOUT}ms)`));
    });

    if (data) {
      req.write(data);
    }
    req.end();
  });
}

async function postJson(path, params, data, token) {
  if (!path || typeof path !== "string") {
    throw new SkillError("PATH_INVALID", "path 必须是非空字符串");
  }
  if (!params || typeof params !== "object") {
    throw new SkillError("PARAM_INVALID", "params 必须是对象");
  }
  if (!data || typeof data !== "object") {
    throw new SkillError("DATA_INVALID", "data 必须是对象");
  }
  params.skill_name = skillName();

  const fullPath = `${path}?${querystring.stringify(params)}`;
  const jsonData = JSON.stringify(data);

  const options = {
    host: constants.BASE_URL,
    path: fullPath,
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept-Encoding": "identity",
      "Content-Length": Buffer.byteLength(jsonData),
      TOKEN: token,
    },
  };

  return await request(options, jsonData);
}

async function getJson(path, params, token) {
  if (!path || typeof path !== "string") {
    throw new SkillError("PATH_INVALID", "path 必须是非空字符串");
  }
  if (!params || typeof params !== "object") {
    throw new SkillError("PARAM_INVALID", "params 必须是对象");
  }
  params._ = Date.now();
  params.skill_name = skillName();

  const fullPath = `${path}?${querystring.stringify(params)}`;
  const options = {
    host: constants.BASE_URL,
    path: fullPath,
    method: "GET",
    headers: { "Accept-Encoding": "identity", TOKEN: token },
  };

  return await request(options);
}

/**
 * 创建等一次性请求（withRetry）。是否重试看错误的 noRetry，不是「errcode < 10 一律重试」。
 * 会重试：网络/超时/HTTP 429（映射 RATE_LIMITED 且 noRetry=false）·HTTP 5xx；未标 noRetry 的瞬时失败（如裸 1、裸 3）。
 * 不重试：业务 RATE_LIMITED（后端裸 2）、PLAN_LIMIT、INSUFFICIENT_BALANCE、DAILY_LIMIT、AUTH_* 等（见 backendCodes）。
 * @param {string} method - HTTP 方法 (GET/POST)
 * @param {string} path - 请求路径
 * @param {object} params - URL 参数
 * @param {object} [data] - 请求体数据 (仅 POST)
 * @param {string} token - 令牌
 * @param {number} maxAttempts - 最大重试次数
 * @param {string} actionName - 操作名称（用于日志）
 * @returns {Promise<object>} API 响应
 */
async function requestApi(
  method,
  path,
  params,
  data,
  token,
  maxAttempts,
  actionName,
) {
  return await withRetry(
    async () => {
      let response;
      if (method === "POST") {
        response = await postJson(path, params, data, token);
      } else {
        response = await getJson(path, params, token);
      }
      return response;
    },
    maxAttempts,
    (attempt, err) => {
      utils.printError(
        `【${actionName}重试】 ${attempt + 1}/${maxAttempts} 次 - ${err.message}`,
      );
    },
  );
}

/**
 * 查询接口的轮询分类。
 * 后端在任务未完成时返回 errcode 1（处理中, 请稍后）；errcode 0 才表示已完成。
 * 稳定业务错误（noRetry）立即失败。网络/超时/HTTP 429·5xx（noRetry=false）继续查。
 * @param {Error} error
 * @returns {"pending"|"fail"|"retry"}
 */
function classifyPollError(error) {
  if (!error) return "retry";
  if (String(error.code) === "1") {
    return "pending";
  }
  if (error.noRetry || error.name === "AuthError") {
    return "fail";
  }
  return "retry";
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * 轮询任务结果。仅用于搜索、作品、评论的查询接口。
 * 次数使用 QUERY_MAX_ATTEMPTS。两次查询之间的等待从 RETRY_INTERVAL 起按 2、4、8 秒翻倍，单次最长 60 秒。
 * 次数用尽仍是「处理中」时抛出 TIMEOUT，不把未完成当成空结果。
 * @param {string} path
 * @param {object} params 查询参数；有任务 id 时应为 `{ id }`（业务字段由调用方决定是否省略）
 * @param {string} token
 * @param {string} actionName
 * @returns {Promise<object>} errcode 为 0 的响应
 */
async function pollTaskResult(path, params, token, actionName) {
  const maxAttempts = constants.QUERY_MAX_ATTEMPTS;
  let lastError;
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    try {
      return await getJson(path, params, token);
    } catch (error) {
      lastError = error;
      const kind = classifyPollError(error);
      if (kind === "fail") {
        throw error;
      }
      if (kind === "pending") {
        utils.printInfo(
          `【${actionName}】处理中 ${attempt + 1}/${maxAttempts}`,
        );
      } else {
        utils.printError(
          `【${actionName}重试】 ${attempt + 1}/${maxAttempts} 次 - ${error.message}`,
        );
      }
      if (attempt < maxAttempts - 1) {
        const delay = Math.min(constants.RETRY_INTERVAL * 2 ** attempt, 60000);
        await sleep(delay);
      }
    }
  }
  if (classifyPollError(lastError) === "pending") {
    throw new SkillError("TIMEOUT", "任务仍在处理中, 请稍后重试", true);
  }
  throw lastError || new SkillError("TIMEOUT", "任务仍在处理中, 请稍后重试", true);
}

module.exports = {
  getJson,
  postJson,
  requestApi,
  pollTaskResult,
  classifyPollError,
};
