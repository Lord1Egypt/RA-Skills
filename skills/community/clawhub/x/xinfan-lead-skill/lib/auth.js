import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { DOMAIN } from "./config.js";
import { probeSession, CDP_URL } from "./browserSession.js";

// ─────────────────────────────────────────────────────────────────────────────
// 鉴权模型（v2：浏览器会话通道）
//
// 本 skill 不再搬运 token/cookie。新帆 merchant_lead 接口的身份，来自「当前登录
// 用户本人」在浏览器里完成公司 SSO(redpass) 登录后的会话——请求由 apiClient 通过
// CDP 投递到该已登录页面上下文执行，身份天然携带。每个 agent(DIBP) 实例背后是各自
// 的登录用户，因此用的永远是用户自己的身份和权限。
//
// 因此 `auth status` 的语义从「查看本地 token」变成「探测会话通道是否就绪」。
//
// set-token 仍然保留：作为极端兜底（例如未来某环境确实签发了可手动注入的 cookie，
// 或调试需要）。但它已不是主路径，默认流程不依赖它。
// ─────────────────────────────────────────────────────────────────────────────

const CRED_DIR = path.join(os.homedir(), ".xinfan-lead-cli");
const CRED_FILE = path.join(CRED_DIR, "credentials.json");

function readCredentials() {
  if (!fs.existsSync(CRED_FILE)) return null;
  try {
    return JSON.parse(fs.readFileSync(CRED_FILE, "utf8"));
  } catch {
    return null;
  }
}

function writeCredentials(data) {
  fs.mkdirSync(CRED_DIR, { recursive: true, mode: 0o700 });
  fs.writeFileSync(CRED_FILE, JSON.stringify(data, null, 2));
  fs.chmodSync(CRED_FILE, 0o600);
}

// 兜底用：手动保存一个 cookie 值（非主路径）。
export function setToken(token) {
  if (!token || !token.trim()) {
    throw new Error("token 不能为空");
  }
  writeCredentials({ token: token.trim(), capturedAt: new Date().toISOString() });
}

export function maskToken(token) {
  if (!token) return "(未设置)";
  return token.length <= 18 ? token : `${token.slice(0, 18)}…`;
}

// 探测会话通道是否可用，返回结构供 cli.js 的 auth status 直接渲染。
export async function getStatus() {
  const probe = await probeSession(DOMAIN);
  return {
    mode: "browser-session",
    cdpUrl: CDP_URL,
    domain: DOMAIN,
    session: probe, // { available, reason?, url?, targetId? }
  };
}

export const CREDENTIALS_PATH = CRED_FILE;
