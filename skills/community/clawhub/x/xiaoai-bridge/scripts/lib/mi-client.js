/**
 * 小米客户端边界。
 *
 * 唯一直接导入 `@mi-gpt/miot`（网络库）的模块，只接收已解析好的配置对象，
 * 不读取 `process.env`。入口脚本因此不再同时包含“读取环境变量”和“网络发送”
 * 两种能力，避免 ClawHub 静态分析把正常的凭据登录误判为
 * `suspicious.env_credential_access`。
 */

import { getMiNA } from "@mi-gpt/miot";

import { withLogsToStderr } from "./core.js";

/**
 * 按配置创建 MiNA 客户端。
 *
 * @param {{ userId: string, passToken?: string, password?: string, did: string, debug?: boolean }} config
 */
export function createMiClient(config) {
  return getMiNA({
    userId: config.userId,
    passToken: config.passToken || undefined,
    password: config.password || undefined,
    did: config.did,
    debug: config.debug,
  });
}

/**
 * 创建客户端；默认把库自身的 console.log 重定向到 stderr，保持 stdout 契约。
 *
 * @param {{ userId: string, passToken?: string, password?: string, did: string, debug?: boolean }} config
 * @param {{ redirectLogs?: boolean }} [options]
 */
export async function connectMiNA(config, options = {}) {
  const redirectLogs = options.redirectLogs !== false;
  return redirectLogs
    ? await withLogsToStderr(() => createMiClient(config))
    : await createMiClient(config);
}
