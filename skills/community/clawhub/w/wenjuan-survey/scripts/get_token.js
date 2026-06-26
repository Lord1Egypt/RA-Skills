#!/usr/bin/env node
/**
 * 问卷网登录 Token 获取工具
 * 使用 device_code 轮询获取 OAuth 会话 JWT（与 token_store 约定的 JSON 字段一致）
 */

const fs = require('fs').promises;
const path = require('path');
const { getDefaultTokenDir, WJ_OAUTH_SESSION_JWT_KEY } = require("./token_store");
const { ensurePrivateDir, writeSecretFile } = require("./security_utils");
const { createSecureAxios } = require("./axios_secure");
const { wenjuanUrl } = require("./api_config");
const http = createSecureAxios();

// API 地址
const TOKEN_URL = wenjuanUrl("/login/token");

/**
 * 获取 token
 * @param {string} deviceCode - 设备码
 */
async function getToken(deviceCode) {
  try {
    const response = await http.post(
      TOKEN_URL,
      { device_code: deviceCode },
      { 
        timeout: 30000,
        headers: { 'Content-Type': 'application/json' }
      }
    );
    return response.data;
  } catch (error) {
    if (error.response) {
      return { error: `请求失败: ${error.response.status} ${error.response.statusText}` };
    }
    return { error: `请求失败: ${error.message}` };
  }
}

/**
 * 从文件读取 device_code
 * @param {string|null} [tokenDir] 默认 getDefaultTokenDir()
 */
async function getDeviceCodeFromFile(tokenDir = null) {
  const dir = tokenDir != null && String(tokenDir).trim() !== ""
    ? path.resolve(String(tokenDir).trim())
    : getDefaultTokenDir();
  const deviceCodeFile = path.join(dir, "device_code");
  try {
    const code = await fs.readFile(deviceCodeFile, 'utf-8');
    return code.trim();
  } catch (error) {
    return null;
  }
}

/**
 * 保存 token
 * @param {Object} tokenData
 * @param {string|null} [tokenDir] 默认 getDefaultTokenDir()
 */
async function saveToken(tokenData, tokenDir = null) {
  const dir = tokenDir != null && String(tokenDir).trim() !== ""
    ? path.resolve(String(tokenDir).trim())
    : getDefaultTokenDir();
  await ensurePrivateDir(dir);
  
  // 保存完整 token 信息
  const tokenFile = path.join(dir, "token.json");
  const data = {
    ...tokenData,
    login_time: new Date().toISOString()
  };
  await writeSecretFile(tokenFile, JSON.stringify(data, null, 2));

  const sessionJwt = tokenData[WJ_OAUTH_SESSION_JWT_KEY];
  if (sessionJwt) {
    const accessTokenFile = path.join(dir, WJ_OAUTH_SESSION_JWT_KEY);
    await writeSecretFile(accessTokenFile, sessionJwt);
  }
  
  // 单独保存 refresh_token
  if (tokenData.refresh_token) {
    const refreshTokenFile = path.join(dir, "refresh_token");
    await writeSecretFile(refreshTokenFile, tokenData.refresh_token);
  }
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);
  
  let deviceCode = null;
  let tokenDir = null;
  let poll = false;
  let maxAttempts = 10;
  let save = false;
  let outputJson = false;
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if ((arg === "-d" || arg === "--device-code") && i + 1 < args.length) {
      deviceCode = args[++i];
    } else if (arg === "--token-dir" && i + 1 < args.length) {
      tokenDir = args[++i];
    } else if (arg === "--poll") {
      poll = true;
    } else if ((arg === "-m" || arg === "--max-attempts") && i + 1 < args.length) {
      maxAttempts = parseInt(args[++i], 10);
    } else if (arg === "--save") {
      save = true;
    } else if (arg === "--json") {
      outputJson = true;
    } else if (arg === "-h" || arg === "--help") {
      showHelp();
      process.exit(0);
    }
  }
  
  // 如果没有提供 device_code，尝试从文件读取
  if (!deviceCode) {
    deviceCode = await getDeviceCodeFromFile(tokenDir);
    if (!deviceCode) {
      console.error("错误: 未提供 device_code，且无法从文件读取");
      console.error("请先运行 get_qrcode.js --save 获取二维码并保存 device_code");
      process.exit(1);
    }
  }
  
  if (poll) {
    // 轮询模式
    console.log("开始轮询获取 token...");
    console.log(`最大尝试次数: ${maxAttempts}`);
    console.log("请使用微信扫描二维码登录\n");
    
    for (let i = 0; i < maxAttempts; i++) {
      const result = await getToken(deviceCode);
      
      if (result.error) {
        console.error(`❌ ${result.error}`);
        process.exit(1);
      }
      
      const statusCode = result.status_code || result.code;
      const data = result.data || {};
      const sessionJwt = data[WJ_OAUTH_SESSION_JWT_KEY];

      if (sessionJwt) {
        console.log("\n✅ 登录成功！");

        if (save) {
          await saveToken(data, tokenDir);
          console.log(`✅ 凭证已保存到 ${tokenDir ? path.resolve(tokenDir) : getDefaultTokenDir()}`);
        }

        if (outputJson) {
          console.log(JSON.stringify(result, null, 2));
        } else if (!save) {
          console.log(
            "提示：未使用 --save，JWT 未落盘。需要完整机器可读响应请加 --json（勿将含密钥的日志提交到仓库）。"
          );
        }

        return;
      }
      
      if (statusCode === 1 || statusCode === 4001) {
        console.log(`[${i + 1}/${maxAttempts}] 等待扫码...`);
        await new Promise(resolve => setTimeout(resolve, 3000));
      } else {
        const errMsg = result.message || result.error || '未知错误';
        console.error(`❌ 获取失败: ${errMsg}`);
        process.exit(1);
      }
    }
    
    console.error("\n❌ 轮询超时，请重新获取二维码");
    process.exit(1);
  } else {
    // 单次获取模式
    const result = await getToken(deviceCode);
    
    if (result.error) {
      console.error(`❌ ${result.error}`);
      process.exit(1);
    }
    
    const data = result.data || {};
    const sessionJwt = data[WJ_OAUTH_SESSION_JWT_KEY];

    if (sessionJwt && save) {
      await saveToken(data, tokenDir);
      console.log(`✅ 凭证已保存到 ${tokenDir ? path.resolve(tokenDir) : getDefaultTokenDir()}`);
    }

    if (outputJson) {
      console.log(JSON.stringify(result, null, 2));
    } else {
      if (sessionJwt) {
        console.log(
          save
            ? "✅ 获取成功（凭证已保存）。"
            : "✅ 获取成功。未使用 --save：未写入文件。完整响应请加 --json（勿泄露日志）。"
        );
      } else {
        const statusCode = result.status_code || result.code;
        const errMsg = result.message || result.error || '等待扫码';
        console.log(`状态: ${errMsg} (code: ${statusCode})`);
      }
    }
  }
}

function showHelp() {
  console.log(`
问卷网登录 Token 获取工具

用法: node get_token.js [选项]

选项:
  -d, --device-code <code>  设备码（默认从 <凭证目录>/device_code 读取）
  --token-dir <dir>         凭证目录（默认 ~/.wenjuan 或环境变量 WENJUAN_TOKEN_DIR）
  --poll                    轮询模式，等待用户扫码
  -m, --max-attempts <num>  最大轮询次数，默认 10
  --save                    保存 token 到文件
  --json                    输出原始JSON响应
  -h, --help                显示帮助信息

示例:
  # 单次获取
  node get_token.js
  
  # 轮询等待扫码
  node get_token.js --poll --save
  
  # 指定 device_code
  node get_token.js -d "your_device_code" --poll --save
`);
}

// 导出模块
module.exports = {
  getToken,
  saveToken
};

// 如果是直接运行
if (require.main === module) {
  main();
}
