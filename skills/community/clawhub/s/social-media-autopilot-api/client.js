#!/usr/bin/env node

import http from "node:http";
import https from "node:https";
import { URL } from "node:url";

export function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) continue;
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      args[key] = true;
      continue;
    }
    args[key] = next;
    i += 1;
  }
  return args;
}

export function getOption(args, name, required = true, fallback = "") {
  const v = args[name] ?? fallback;
  if (required && !v) {
    throw new Error(`Missing option: --${name}`);
  }
  return v;
}

const allowedApiHosts = new Set(["api.socialecho.net", "api-dev.socialecho.net"]);

function normalizeBaseUrl(raw) {
  const value = String(raw).replace(/\/+$/, "");
  const url = new URL(value);
  if (url.protocol !== "https:" || !allowedApiHosts.has(url.hostname) || url.username || url.password) {
    throw new Error("--base-url must be https://api.socialecho.net or https://api-dev.socialecho.net");
  }
  if (url.pathname !== "/" || url.search || url.hash) {
    throw new Error("--base-url must not include a path, query, or fragment");
  }
  return value;
}

export function buildRequestOptions(args) {
  return {
    apiKey: getOption(args, "api-key"),
    baseUrl: normalizeBaseUrl(getOption(args, "base-url", false, "https://api.socialecho.net")),
    teamId: getOption(args, "team-id", false, ""),
    lang: getOption(args, "lang", false, "zh_CN")
  };
}

export function buildHeaders(options) {
  const { apiKey, teamId, lang } = options;
  const headers = {
    Authorization: `Bearer ${apiKey}`,
    "X-Lang": lang
  };
  if (teamId) headers["X-Team-Id"] = String(teamId);
  return headers;
}

function appendQueryParams(urlString, params = {}) {
  const url = new URL(urlString);
  for (const [key, value] of Object.entries(params)) {
    if (value === undefined || value === null || value === "") continue;
    if (Array.isArray(value)) {
      for (const item of value) url.searchParams.append(`${key}[]`, String(item));
    } else {
      url.searchParams.set(key, String(value));
    }
  }
  return url.toString();
}

function requestJson(method, urlString, bodyObject, baseHeaders) {
  return new Promise((resolve, reject) => {
    const u = new URL(urlString);
    const isHttps = u.protocol === "https:";
    const lib = isHttps ? https : http;
    const bodyBuf = method === "GET" ? null : Buffer.from(JSON.stringify(bodyObject ?? {}), "utf8");
    const headers = bodyBuf
      ? {
          ...baseHeaders,
          "Content-Type": "application/json",
          "Content-Length": String(bodyBuf.length)
        }
      : baseHeaders;
    const opts = {
      hostname: u.hostname,
      port: u.port || (isHttps ? 443 : 80),
      path: `${u.pathname}${u.search}`,
      method,
      headers
    };
    const req = lib.request(opts, (res) => {
      const chunks = [];
      res.on("data", (c) => chunks.push(c));
      res.on("end", () => {
        const text = Buffer.concat(chunks).toString("utf8");
        let body;
        try {
          body = text ? JSON.parse(text) : {};
        } catch {
          body = { parse_error: true, raw: text };
        }
        resolve({ status: res.statusCode ?? 0, body });
      });
    });
    req.on("error", reject);
    if (bodyBuf) req.write(bodyBuf);
    req.end();
  });
}

export function isBusinessOk(body) {
  const c = body?.code;
  return c === 0;
}

/** GET 参数使用 QueryString；CloudFront 会拒绝带 body 的 GET 请求。 */
export async function callJsonGet(path, params, options) {
  const { baseUrl } = options;
  const url = appendQueryParams(
    `${baseUrl}${path.startsWith("/") ? path : `/${path}`}`,
    params
  );
  const h = buildHeaders(options);
  const { status, body: respBody } = await requestJson("GET", url, undefined, h);
  const ok = status === 200 && isBusinessOk(respBody);
  return { ok, status, body: respBody, url };
}

export async function callJsonPost(path, body, options) {
  const { baseUrl } = options;
  const url = `${baseUrl}${path.startsWith("/") ? path : `/${path}`}`;
  const h = buildHeaders(options);
  const { status, body: respBody } = await requestJson("POST", url, body, h);
  const ok = status === 200 && isBusinessOk(respBody);
  return { ok, status, body: respBody, url };
}

/** @deprecated 与 callJsonGet 相同，保留旧名 */
export async function callApi(path, params = {}, options) {
  return callJsonGet(path, params, options);
}

export function parseCsvIds(raw) {
  if (!raw) return "";
  return String(raw)
    .split(",")
    .map((x) => x.trim())
    .filter(Boolean)
    .join(",");
}

export function parseCsvIdsToArray(raw) {
  if (!raw) return undefined;
  const arr = String(raw)
    .split(",")
    .map((x) => x.trim())
    .filter(Boolean)
    .map((x) => Number(x))
    .filter((n) => !Number.isNaN(n));
  return arr.length ? arr : undefined;
}

export function printAndExit(result) {
  console.log(JSON.stringify(result, null, 2));
  if (!result.ok) process.exit(1);
}
