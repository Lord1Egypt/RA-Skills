#!/usr/bin/env node
/**
 * 问卷网微信自动登录脚本
 * - 自动获取二维码
 * - 始终尝试自动打开系统默认浏览器；失败时再提示手动复制链接（链接文件在获取二维码后即写入）
 * - 循环轮询获取 token
 * - 自动保存凭证
 *
 * 安全说明：本文件不包含任何硬编码的 API 密钥；OAuth 会话 JWT 仅来自用户扫码后
 * `/login/token` 接口返回，再写入用户指定目录（见 saveToken / token_store）。
 */

const fs = require('fs').promises;
const path = require('path');
const { openUrlBestEffort, writeUrlForManualOpen } = require("./open_url_cjs");
const readline = require('readline');
const {
  getDefaultTokenDir,
  resolveAccessToken,
  pathsForSkill,
  WJ_OAUTH_SESSION_JWT_KEY,
} = require("./token_store");
const { ensurePrivateDir, writeSecretFile } = require("./security_utils");
const { createSecureAxios } = require("./axios_secure");
const { wenjuanUrl } = require("./api_config");

// API 地址
// 生产环境域名
const QRCODE_URL = wenjuanUrl("/login/qrcode");
const TOKEN_URL = wenjuanUrl("/login/token");

// 默认配置（目录逻辑见 token_store.js / getDefaultTokenDir）
const POLL_INTERVAL = 3000; // 轮询间隔（毫秒）
/** 未传 --max-time 时，与 CLI 默认 300 秒一致（毫秒） */
const DEFAULT_MAX_POLL_MS = 300 * 1000;

/**
 * 问卷网登录管理器
 */
class WenjuanLogin {
  constructor(tokenDir = null, options = {}) {
    this.tokenDir =
      tokenDir != null && String(tokenDir).trim() !== ""
        ? path.resolve(String(tokenDir).trim())
        : getDefaultTokenDir();
    this.deviceCode = null;
    this.qrcodeUrl = null;
    this.session = createSecureAxios();
    this.maxPollTime =
      options.maxPollTime != null ? options.maxPollTime : DEFAULT_MAX_POLL_MS;
  }

  /**
   * 获取登录二维码
   */
  async getQrcode() {
    console.log("[1/4] 正在获取登录二维码...");

    try {
      const response = await this.session.post(QRCODE_URL, {}, { timeout: 30000 });
      const data = response.data;

      if (data.status_code !== 1 && data.code !== 0) {
        const errorMsg = data.message || data.error || '未知错误';
        console.error(`✗ 获取二维码失败: ${errorMsg}`);
        return false;
      }
      
      const result = data.data || {};
      this.deviceCode = result.device_code;
      this.qrcodeUrl = result.qrcode_url;
      
      if (!this.deviceCode || !this.qrcodeUrl) {
        console.error("✗ 响应中缺少必要字段");
        return false;
      }
      
      // 保存 device_code
      await ensurePrivateDir(this.tokenDir);
      const deviceCodeFile = path.join(this.tokenDir, "device_code");
      await writeSecretFile(deviceCodeFile, this.deviceCode);
      
      console.log(`✓ 设备码已保存: ${deviceCodeFile}`);
      console.log(`  device_code 长度: ${String(this.deviceCode).length}（完整值见上述文件，不在日志中打印）`);
      
      try {
        await writeUrlForManualOpen(
          this.qrcodeUrl,
          this.tokenDir,
          "last_wenjuan_login_url.txt"
        );
        const loginFile = path.join(this.tokenDir, "last_wenjuan_login_url.txt");
        console.log(
          `  [提示] 完整扫码链接已写入: ${loginFile}（Workerbuddy/OpenClaw/SSH 等若未弹出浏览器，请在本机打开该文件内整行链接）`
        );
      } catch (e) {
        console.log(`  [提示] 写入扫码链接文件失败: ${e.message}，将依赖下方打印或自动打开浏览器`);
      }

      console.log("  [提示] 下一步将尝试用系统默认浏览器打开扫码页（失败时会打印链接，亦可用上方文件）");
      return true;
      
    } catch (error) {
      console.error(`✗ 请求失败: ${error.message}`);
      return false;
    }
  }

  /**
   * 使用默认浏览器打开登录链接；失败则打印完整 URL（链接文件已在获取二维码后写入）
   */
  async openBrowser() {
    console.log("[2/4] 正在自动打开浏览器（若失败将改为下方手动链接方式，不影响后续扫码与轮询）...");
    
    let browserOpened = false;
    
    try {
      browserOpened = await openUrlBestEffort(this.qrcodeUrl);
      if (browserOpened) {
        console.log("✓ 已在浏览器中打开二维码页面");
      } else {
        console.log("✗ 自动打开失败（open 包与系统命令均不可用或失败）");
      }
    } catch (error) {
      console.log(`✗ 打开浏览器异常: ${error.message}`);
    }
    
    // 如果浏览器自动打开失败，提示用户手动操作
    if (!browserOpened) {
      console.log("\n" + "=".repeat(50));
      console.log("❌ 浏览器自动打开失败");
      console.log("=".repeat(50));
      console.log("\n请手动复制以下链接到浏览器地址栏打开（须完整一行，查询参数不可缺）：");
      console.log(`\n${this.qrcodeUrl}\n`);
      console.log("=".repeat(50));
      console.log(
        `（同一链接已保存在: ${path.join(this.tokenDir, "last_wenjuan_login_url.txt")}）`
      );
    } else {
      console.log("\n" + "=".repeat(50));
      console.log("📱 请使用微信扫描二维码");
      console.log("=".repeat(50));
    }
    
    return true; // 继续执行，不管浏览器是否成功打开
  }

  /**
   * 从 /login/token 响应中取出 OAuth 会话 JWT（兼容根级与 data 包裹）
   */
  _extractPollSessionJwt(data) {
    if (!data || typeof data !== "object") return null;
    const d = data.data;
    const k = WJ_OAUTH_SESSION_JWT_KEY;
    if (d && typeof d === "object" && d[k]) return d[k];
    if (data[k]) return data[k];
    return null;
  }

  /**
   * 是否应停止轮询（二维码过期、设备码作废等）；其余情况继续等到超时
   */
  _isFatalTokenPollError(data) {
    if (!data || typeof data !== "object") return false;
    const text = `${data.message || ""} ${data.err_msg || ""} ${data.msg || ""} ${data.error || ""}`.toLowerCase();
    const fatalHints = [
      "二维码已过期",
      "二维码过期",
      "qrcode expired",
      "设备码无效",
      "device_code",
      "device code invalid",
      "授权已拒绝",
      "access_denied",
    ];
    return fatalHints.some((h) => text.includes(h.toLowerCase()));
  }

  /**
   * 轮询获取 token（自动打开失败或手动复制链接后扫码，均依赖同一 device_code 轮询，逻辑相同）
   */
  async pollToken() {
    console.log("[3/4] 等待扫码登录...");
    console.log("=".repeat(50));
    console.log("请使用微信扫描二维码登录");
    console.log("=".repeat(50));
    console.log(
      "说明：若上一步是手动复制链接到浏览器，扫码成功后**无需再开终端**；请保持本窗口运行直至出现「登录成功」。"
    );

    const startTime = Date.now();

    while (true) {
      const elapsed = Date.now() - startTime;
      if (elapsed > this.maxPollTime) {
        console.log(`\n✗ 登录超时（超过${this.maxPollTime / 1000}秒），请重新运行脚本`);
        return null;
      }

      try {
        const sec = Math.floor(elapsed / 1000);
        const maxSec = Math.floor(this.maxPollTime / 1000);

        const response = await this.session.post(
          TOKEN_URL,
          { device_code: this.deviceCode },
          {
            timeout: 30000,
            headers: { "Content-Type": "application/json" },
          }
        );

        const data = response.data;

        const tokenFromPoll = this._extractPollSessionJwt(data);

        if (tokenFromPoll) {
          console.log(`\n✓ 登录成功！（耗时 ${Math.floor(elapsed / 1000)} 秒）`);
          const k = WJ_OAUTH_SESSION_JWT_KEY;
          return {
            [k]: tokenFromPoll,
            refresh_token: (data.data && data.data.refresh_token) || null,
            device_code: this.deviceCode,
            login_time: new Date().toISOString(),
          };
        }

        if (this._isFatalTokenPollError(data)) {
          const errorMsg =
            data.message || data.err_msg || data.error || "登录流程已无法继续";
          console.log(`\n✗ 获取 token 终止: ${errorMsg}`);
          return null;
        }

        // 未拿到 token 且非明确致命错误：继续轮询（兼容接口返回多种等待态 code，避免手动扫码后因未知 code 提前退出）
        console.log(
          `  等待扫码中… (${sec}s / ${maxSec}s) 请在浏览器打开的页面用微信扫码并确认登录`
        );
        await new Promise((resolve) => setTimeout(resolve, POLL_INTERVAL));
      } catch (error) {
        console.log(`\n! 请求出错: ${error.message}，3秒后重试...`);
        await new Promise((resolve) => setTimeout(resolve, 3000));
      }
    }
  }

  /**
   * 保存 token 到本地
   * @param {Object} tokenData
   */
  async saveToken(tokenData) {
    console.log("[4/4] 正在保存登录凭证...");
    
    try {
      // 1. 保存到用户目录（默认位置）
      await ensurePrivateDir(this.tokenDir);
      
      const tokenFile = path.join(this.tokenDir, "token.json");
      await writeSecretFile(tokenFile, JSON.stringify(tokenData, null, 2));

      const k = WJ_OAUTH_SESSION_JWT_KEY;
      const sessionJwt = tokenData[k];
      const accessTokenFile = path.join(this.tokenDir, WJ_OAUTH_SESSION_JWT_KEY);
      await writeSecretFile(accessTokenFile, sessionJwt);
      
      if (tokenData.refresh_token) {
        const refreshTokenFile = path.join(this.tokenDir, "refresh_token");
        await writeSecretFile(refreshTokenFile, tokenData.refresh_token);
      }
      
      console.log(`✓ 凭证已保存到: ${this.tokenDir}`);
      
      // 2. 保存到项目目录（skill 使用）
      const scriptDir = __dirname;
      const projectTokenDir = path.join(scriptDir, '..', '.wenjuan');
      await ensurePrivateDir(projectTokenDir);
      
      const projectAuthFile = path.join(projectTokenDir, "auth.json");
      const authData = {
        [k]: sessionJwt,
        refresh_token: tokenData.refresh_token || null,
        device_code: this.deviceCode,
        login_time: new Date().toISOString()
      };
      await writeSecretFile(projectAuthFile, JSON.stringify(authData, null, 2));
      
      console.log(`✓ 凭证已保存到项目目录: ${projectAuthFile}`);
      console.log("  - 访问令牌（JWT）：已写入 token.json / 纯文本会话文件，终端不打印明文");
      console.log("  - refresh_token：若接口返回则一并落盘");
      
      return true;
      
    } catch (error) {
      console.error(`✗ 保存凭证失败: ${error.message}`);
      return false;
    }
  }

  /**
   * 执行完整登录流程：始终尝试自动打开浏览器；打开失败时凭已写入的链接与终端输出手动打开
   * @param {{ force?: boolean }} [opts] force=true 时忽略本地凭证，始终拉新二维码（如 API 返回 NEED_LOGIN 后重登）
   */
  async login(opts = {}) {
    const force = opts.force === true;

    if (await this._shouldSkipNewQrcode(force)) {
      console.log("=".repeat(50));
      console.log("✓ 已存在本地登录凭证（未过期），跳过扫码登录");
      console.log("  换账号或令牌失效时请执行: node scripts/login_auto.js --force-login");
      console.log("=".repeat(50));
      return true;
    }

    console.log("=".repeat(50));
    console.log("问卷网微信扫码登录");
    console.log("=".repeat(50));
    console.log();
    
    // 1. 获取二维码
    if (!(await this.getQrcode())) {
      return false;
    }
    
    console.log();
    
    // 2. 打开浏览器（始终尝试）
    await this.openBrowser();
    
    console.log();
    
    // 3. 轮询获取 token
    const tokenData = await this.pollToken();
    if (!tokenData) {
      return false;
    }
    
    console.log();
    
    // 4. 保存 token
    if (!(await this.saveToken(tokenData))) {
      return false;
    }
    
    console.log();
    console.log("=".repeat(50));
    console.log("✓ 登录流程完成！");
    console.log("=".repeat(50));
    console.log("\n访问令牌与刷新令牌已写入本地凭证文件（不在终端打印明文）。");
    
    return true;
  }

  /**
   * 检查当前登录状态（读取 token.json；与 resolveAccessToken 路径可能不一致，见 _shouldSkipNewQrcode）
   */
  async checkLoginStatus() {
    const tokenFile = path.join(this.tokenDir, "token.json");
    
    try {
      const content = await fs.readFile(tokenFile, 'utf-8');
      const tokenData = JSON.parse(content);
      
      // 检查 token 是否过期（简化检查，实际应该调用 API 验证）
      const loginTime = tokenData.login_time;
      if (loginTime) {
        const loginDt = new Date(loginTime);
        const elapsed = (Date.now() - loginDt.getTime()) / 1000;
        // 假设 token 有效期为 7 天
        if (elapsed > 7 * 24 * 3600) {
          return { valid: false, reason: "token 可能已过期", data: tokenData };
        }
      }
      
      return { valid: true, data: tokenData };
      
    } catch (error) {
      return null;
    }
  }

  /**
   * 若本地已有可读凭证且未声明过期，则不再拉新二维码（减少 Workerbuddy/多步骤任务里重复扫码）
   * @param {boolean} force 为 true 时永远不跳过（例如服务端已返回 NEED_LOGIN）
   */
  async _shouldSkipNewQrcode(force) {
    if (force) return false;
    const t = await resolveAccessToken();
    if (!t || String(t).trim().length <= 10) return false;

    const paths = pathsForSkill(undefined, this.tokenDir);
    const maxAgeSec = 7 * 24 * 3600;

    for (const fp of [paths.projectAuthPath, paths.tokenJsonPath]) {
      try {
        const raw = await fs.readFile(fp, "utf-8");
        const tokenData = JSON.parse(raw);
        const loginTime = tokenData.login_time;
        if (loginTime) {
          const elapsed = (Date.now() - new Date(loginTime).getTime()) / 1000;
          if (elapsed > maxAgeSec) return false;
        }
        return true;
      } catch (_) {
        /* try next */
      }
    }

    try {
      const raw = (await fs.readFile(paths.accessTokenPath, "utf-8")).trim();
      if (raw.length > 20) return true;
    } catch (_) {}

    return false;
  }
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);
  
  let tokenDir = null;
  let checkOnly = false;
  let maxTime = 300;
  let forceLogin = false;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if ((arg === "--token-dir" || arg === "-t") && i + 1 < args.length) {
      tokenDir = args[++i];
    } else if (arg === "--check" || arg === "-c") {
      checkOnly = true;
    } else if (arg === "--force-login" || arg === "--force") {
      forceLogin = true;
    } else if ((arg === "--max-time" || arg === "-m") && i + 1 < args.length) {
      maxTime = parseInt(args[++i], 10);
    } else if (arg === "-h" || arg === "--help") {
      showHelp();
      process.exit(0);
    }
  }

  const loginManager = new WenjuanLogin(tokenDir, {
    maxPollTime: maxTime * 1000,
  });
  
  if (checkOnly) {
    // 检查登录状态
    const status = await loginManager.checkLoginStatus();
    if (status) {
      if (status.valid) {
        console.log("✓ 已登录");
        console.log("  会话 JWT: <已登录，明文见 token.json，此处不打印>");
        console.log(`  登录时间: ${status.data.login_time || '未知'}`);
      } else {
        console.log(`! ${status.reason}`);
        console.log("  请重新运行脚本登录");
      }
    } else {
      console.log("✗ 未登录");
    }
    return;
  }
  
  // 执行登录
  await loginManager.login({ force: forceLogin });
}

function showHelp() {
  console.log(`
问卷网微信自动登录

用法: node login_auto.js [选项]

选项:
  -t, --token-dir <dir>  凭证存储目录
  -c, --check            检查登录状态
  --force-login          忽略本地已有凭证，强制重新拉二维码（换账号或调试时用）
  -m, --max-time <sec>   最大等待时间（秒）
  -h, --help             显示帮助信息

说明:
  若本地已有未过期凭证（见 token_store 约定路径），默认不再重复扫码，直接成功退出。
  会始终尝试自动打开系统默认浏览器；若 open/系统命令失败，会自动打印链接并写入
  <token-dir>/last_wenjuan_login_url.txt，扫码与轮询不受影响。
  链接较长，半选复制易丢参数，请用该文件或整行复制。
`);
}

// 导出模块
module.exports = {
  WenjuanLogin,
  QRCODE_URL,
  TOKEN_URL
};

// 如果是直接运行
if (require.main === module) {
  main();
}
