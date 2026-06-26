#!/usr/bin/env node
/**
 * 问卷网登录二维码获取工具
 */

const fs = require('fs').promises;
const path = require('path');
const { getDefaultTokenDir } = require('./token_store');
const { ensurePrivateDir, writeSecretFile } = require("./security_utils");
const { createSecureAxios } = require("./axios_secure");
const { wenjuanUrl } = require("./api_config");
const http = createSecureAxios();

// API 地址
const QRCODE_URL = wenjuanUrl("/login/qrcode");

/**
 * 获取二维码
 */
async function getQrcode() {
  try {
    const response = await http.post(QRCODE_URL, {}, { timeout: 30000 });
    return response.data;
  } catch (error) {
    if (error.response) {
      return { error: `请求失败: ${error.response.status} ${error.response.statusText}` };
    }
    return { error: `请求失败: ${error.message}` };
  }
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);
  
  let saveDeviceCode = false;
  let outputJson = false;
  let tokenDir = null;
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === "--save") {
      saveDeviceCode = true;
    } else if (arg === "--token-dir" && i + 1 < args.length) {
      tokenDir = args[++i];
    } else if (arg === "--json") {
      outputJson = true;
    } else if (arg === "-h" || arg === "--help") {
      showHelp();
      process.exit(0);
    }
  }
  
  try {
    const result = await getQrcode();
    
    if (result.error) {
      console.error(`❌ ${result.error}`);
      process.exit(1);
    }
    
    if (saveDeviceCode && result.data && result.data.device_code) {
      const dir =
        tokenDir != null && String(tokenDir).trim() !== ""
          ? path.resolve(String(tokenDir).trim())
          : getDefaultTokenDir();
      await ensurePrivateDir(dir);
      const deviceCodeFile = path.join(dir, "device_code");
      await writeSecretFile(deviceCodeFile, result.data.device_code);
    }
    
    if (outputJson) {
      console.log(JSON.stringify(result, null, 2));
    } else {
      console.log("✅ 二维码获取成功");
      if (result.data) {
        console.log(`   device_code: ${result.data.device_code}`);
        console.log(`   qrcode_url: ${result.data.qrcode_url}`);
      }
    }
    
  } catch (error) {
    console.error(`❌ 错误: ${error.message}`);
    process.exit(1);
  }
}

function showHelp() {
  console.log(`
问卷网登录二维码获取工具

用法: node get_qrcode.js [选项]

选项:
  --save                  保存 device_code 到 <凭证目录>/device_code（目录见 --token-dir / auth.md）
  --token-dir <dir>       凭证目录（默认 ~/.wenjuan 或 WENJUAN_TOKEN_DIR）
  --json                  输出原始JSON响应
  -h, --help              显示帮助信息

示例:
  # 获取二维码
  node get_qrcode.js
  
  # 获取并保存 device_code
  node get_qrcode.js --save
`);
}

// 导出模块
module.exports = {
  getQrcode
};

// 如果是直接运行
if (require.main === module) {
  main();
}
