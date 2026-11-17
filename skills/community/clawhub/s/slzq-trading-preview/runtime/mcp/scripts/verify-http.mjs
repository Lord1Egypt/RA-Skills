#!/usr/bin/env node
/**
 * 只读请求 GET /open/v1/health，用于冒烟（无需 Api Key）。
 */
const domain = (process.env.SLZQ_OPENCLAW_DOMAIN ?? "https://slzqapi.sxslqhsh.com").trim().replace(/\/+$/, "");
const url = `${domain}/mobile-api/open/v1/health`;
const res = await fetch(url);
const text = await res.text();
console.log(`${res.status} ${url}`);
console.log(text);
process.exit(res.ok ? 0 : 1);
