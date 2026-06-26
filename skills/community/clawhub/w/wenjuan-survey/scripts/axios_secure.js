const axios = require("axios");
const https = require("https");
const tls = require("tls");
const crypto = require("crypto");
const { getTlsPinSha256, getMinRequestIntervalMs } = require("./wenjuan_env");

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function buildHttpsAgent() {
  const pin = getTlsPinSha256();
  return new https.Agent({
    keepAlive: true,
    rejectUnauthorized: true,
    minVersion: "TLSv1.2",
    checkServerIdentity: (host, cert) => {
      const err = tls.checkServerIdentity(host, cert);
      if (err) return err;
      if (!pin) return undefined;
      if (!cert || !cert.raw) return new Error("TLS 证书缺少 raw 字段，无法校验 pin");
      const actual = crypto.createHash("sha256").update(cert.raw).digest("hex");
      if (actual !== pin) {
        return new Error(`TLS 证书 pin 校验失败: ${host}`);
      }
      return undefined;
    },
  });
}

function createSecureAxios(baseConfig = {}) {
  const instance = axios.create({
    httpsAgent: buildHttpsAgent(),
    timeout: 30000,
    ...baseConfig,
  });

  // 简单客户端限流：同一进程最小间隔，避免高频误调用
  const minInterval = getMinRequestIntervalMs();
  let lastAt = 0;
  instance.interceptors.request.use(async (config) => {
    const now = Date.now();
    const waitMs = Math.max(0, minInterval - (now - lastAt));
    if (waitMs > 0) await sleep(waitMs);
    lastAt = Date.now();
    return config;
  });
  return instance;
}

module.exports = {
  createSecureAxios,
};

