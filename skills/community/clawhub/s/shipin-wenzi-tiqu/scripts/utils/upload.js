const constants = require("../config/constants");
const helper = require("../utils/helper");
const utils = require("../utils/utils");
const { withRetry } = require("./retry");
const https = require("https");
const fs = require("fs");

function headerCI(headers, name) {
  if (!headers || typeof headers !== "object") return "";
  const want = String(name).toLowerCase();
  for (const [k, v] of Object.entries(headers)) {
    if (String(k).toLowerCase() === want && v) return String(v);
  }
  return "";
}

function markUploadRetry(error, statusCode) {
  if (
    statusCode >= 400 &&
    statusCode < 500 &&
    statusCode !== 408 &&
    statusCode !== 429
  ) {
    error.noRetry = true;
  }
  return error;
}

/**
 * 上传文件到本次预签名地址，仅用于视频转文案。处理完毕 24 小时后从服务器销毁，不存储、不对外泄露、不用于模型训练。
 * 网络错误、5xx、408、429 会重试；其它 4xx 立即失败。
 */
async function uploadOnce(filename, presignedUrl, headers) {
  const url = new URL(presignedUrl);
  if (url.protocol !== "https:") {
    throw new Error("上传URL必须是HTTPS协议");
  }
  return new Promise((resolve, reject) => {
    const fileStats = fs.statSync(filename);
    const totalSize = fileStats.size;
    let uploadedSize = 0;
    let settled = false;

    const fileStream = fs.createReadStream(filename);

    // 复制预签名 headers，并补充 OSS PUT 必需字段
    const uploadHeaders = Object.assign({}, headers);
    // 关键修复：明确 Content-Length，否则 Node 对流式 body 默认使用 chunked
    // Transfer-Encoding，阿里云 OSS 预签名 PUT 通常会拒绝而返回 400/403
    uploadHeaders["Content-Length"] = String(totalSize);
    if (!headerCI(uploadHeaders, "Content-Type")) {
      uploadHeaders["Content-Type"] = "video/mp4";
    }

    const options = {
      host: url.hostname,
      path: url.pathname + url.search,
      method: "PUT",
      headers: uploadHeaders,
    };
    const req = https.request(
      { ...options, timeout: constants.UPLOAD_TIMEOUT },
      (res) => {
        let body = "";
        res.on("data", (chunk) => {
          if (body.length < 2048) body += chunk;
        });
        res.on("end", () => {
          if (settled) return;
          settled = true;
          fileStream.destroy();
          if (res.statusCode >= 200 && res.statusCode < 300) {
            helper.inlineLog(`文件上传成功, ${helper.byteHumanize(totalSize)}`);
            resolve(body);
          } else {
            reject(
              markUploadRetry(
                new Error(
                  `文件上传失败, 状态码: ${res.statusCode}, 响应体: ${String(body).slice(0, 200)}`,
                ),
                res.statusCode,
              ),
            );
          }
        });
        res.on("error", (error) => {
          if (settled) return;
          settled = true;
          fileStream.destroy();
          req.destroy();
          utils.printError(`上传响应读取失败: ${error.message}`);
          reject(new Error(`上传响应读取失败: ${error.message}`));
        });
      },
    );
    fileStream.on("data", (chunk) => {
      uploadedSize += chunk.length;
      helper.inlineLog(
        `上传进度: ${helper.byteHumanize(uploadedSize)} / ${helper.byteHumanize(totalSize)}`,
      );
    });

    fileStream.on("error", (error) => {
      if (settled) return;
      settled = true;
      req.destroy();
      utils.printError(`上传读取文件失败: ${error.message}`);
      reject(error);
    });

    req.on("error", (error) => {
      if (settled) return;
      settled = true;
      fileStream.destroy();
      utils.printError(`上传请求失败: ${error.message}`);
      reject(error);
    });

    req.on("timeout", () => {
      if (settled) return;
      settled = true;
      fileStream.destroy();
      req.destroy();
      utils.printError(`上传请求超时: ${constants.UPLOAD_TIMEOUT}ms`);
      reject(new Error("上传请求超时"));
    });

    fileStream.pipe(req);
  });
}

async function uploadFileToOSS(filename, presignedUrl, headers) {
  const maxAttempts = constants.UPLOAD_MAX_ATTEMPTS;
  return await withRetry(
    async () => uploadOnce(filename, presignedUrl, headers),
    maxAttempts,
    (attempt, error) => {
      utils.printError(
        `【上传重试】${attempt + 1}/${maxAttempts} 次 - ${error.message}`,
      );
    },
  );
}

module.exports = { uploadFileToOSS };
