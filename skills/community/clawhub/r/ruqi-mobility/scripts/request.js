/**
 * HTTP 请求封装 - 基于 curl 命令
 */

import { spawn } from "child_process";

const requestConfig = {
  baseUrl: "https://client.ruqimobility.com/mcp/v1",
  passengerH5Host: "https://web.ruqimobility.com",
  platform: "MINIPROGRAM_ANDROID",
  noTokenEndpoints: [
    "send_verification_code",
    "login_with_verification_code",
  ],
};

function execCommand(command, args, options = {}) {
  return new Promise((resolve, reject) => {
    const proc = spawn(command, args, {
      shell: false,
      stdio: ["ignore", "pipe", "pipe"],
      timeout: options.timeout || 30000
    });
    let stdout = "";
    let stderr = "";
    proc.stdout.on("data", (d) => (stdout += d.toString()));
    proc.stderr.on("data", (d) => (stderr += d.toString()));
    proc.on("close", (code) => {
      if (code === 0) resolve(stdout);
      else reject(new Error(stderr || `exit code ${code}`));
    });
    proc.on("error", reject);
  });
}

export async function httpRequest(
  endpoint,
  requestData,
  returnHeaders = false,
) {
  const needsToken = !requestConfig.noTokenEndpoints.includes(endpoint);
  const token = process.env.RUQI_CLIENT_MCP_TOKEN;

  if (needsToken && !token) {
    throw new Error("RUQI_CLIENT_MCP_TOKEN 环境变量未配置，请先登录");
  }

  const fullRequest = {
    platform: requestConfig.platform,
    timestamp: Date.now(),
    ...(token && { token }),
    ...requestData,
    deviceId: `${requestData.phone}-ruqimcp`,
  };

  const requestBody = {
    jsonrpc: "2.0",
    id: Date.now().toString(),
    method: "tools/call",
    params: {
      name: endpoint,
      arguments: fullRequest,
    },
  };

  const timeout = 30000;

  try {
    const result = await execCommand("curl", [
      "-s",
      "-i",
      "-X", "POST",
      "-H", "Content-Type: application/json",
      "-d", JSON.stringify(requestBody),
      "--max-time", String(timeout / 1000),
      requestConfig.baseUrl,
    ]);

    const headerEndIndex = result.indexOf("\r\n\r\n");
    let responseHeaders = {};
    let body = result;
    if (headerEndIndex !== -1) {
      const headerPart = result.substring(0, headerEndIndex);
      body = result.substring(headerEndIndex + 4);

      const headerLines = headerPart.split("\r\n");
      for (const line of headerLines) {
        const colonIndex = line.indexOf(":");
        if (colonIndex > 0) {
          const key = line.substring(0, colonIndex).trim().toLowerCase();
          const value = line.substring(colonIndex + 1).trim();
          if (key === "set-cookie") {
            if (!responseHeaders["set-cookie"]) {
              responseHeaders["set-cookie"] = [];
            }
            responseHeaders["set-cookie"].push(value);
          } else {
            responseHeaders[key] = value;
          }
        }
      }
    }

    let content;
    try {
      content = JSON.parse(body);
    } catch (e) {
      console.error("响应数据:", body);
      throw new Error("无效的响应格式");
    }

    const text = content?.data?.result?.content?.[0]?.text;

    if (text) {
      const parsedText = typeof text === "string" ? JSON.parse(text) : text;

      if (parsedText.code !== 0) {
        throw new Error(
          `业务错误: ${parsedText.message || JSON.stringify(parsedText)}`,
        );
      }

      if (returnHeaders) {
        return {
          data: parsedText,
          headers: responseHeaders,
        };
      }

      return parsedText;
    } else {
      console.error("响应数据:", JSON.stringify(content, null, 2));
      throw new Error("无效的响应格式");
    }
  } catch (error) {
    throw new Error("error: " + error.message);
  }
}

export { execCommand };