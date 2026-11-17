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
                reject(
                  new ApiError("API_ERROR", "接口响应缺少有效的 errcode", true),
                );
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
            const code =
              status >= 500 && status <= 599 ? "HTTP_5xx" : `HTTP_${status}`;
            reject(new ApiError(code, `请求失败, 状态码: ${status}`, true));
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

function commonHeaders(token, extra = {}) {
  return {
    "Accept-Encoding": "identity",
    TOKEN: token,
    "User-Agent": `${skillName()}/${constants.VERSION}`,
    ...extra,
  };
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
    headers: commonHeaders(token, {
      "Content-Type": "application/json",
      "Content-Length": Buffer.byteLength(jsonData),
    }),
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
    headers: commonHeaders(token),
  };

  return await request(options);
}

/**
 * 通用 API 请求方法（用于创建任务等）
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
 * @param {Error} error
 * @returns {"pending"|"fail"|"retry"}
 */
function classifyPollError(error) {
  if (error && String(error.code) === "1") {
    return "pending";
  }
  if (
    error &&
    (error.noRetry || error.name === "ApiError" || error.name === "AuthError")
  ) {
    return "fail";
  }
  return "retry";
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * 轮询任务结果。次数用尽仍是「处理中」时抛出 TIMEOUT。
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
    throw new SkillError(
      "TIMEOUT",
      "任务仍在处理中, 请使用完全相同的参数再次调用并等待",
      true,
    );
  }
  throw (
    lastError ||
    new SkillError(
      "TIMEOUT",
      "任务仍在处理中, 请使用完全相同的参数再次调用并等待",
      true,
    )
  );
}

module.exports = {
  getJson,
  postJson,
  requestApi,
  pollTaskResult,
  classifyPollError,
};
