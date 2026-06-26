#!/usr/bin/env node
/**
 * WeryAI account CLI.
 *
 * Commands:
 *   balance
 *
 * Runtime secret:
 *   WERYAI_API_KEY
 */

const BASE_URL = (process.env.WERYAI_BASE_URL || "https://api.weryai.com").replace(/\/$/, "");
const PRICING_URL = "https://www.weryai.com/api/pricing";

const ERROR_MESSAGES = {
  401: "Authentication failed. Verify WERYAI_API_KEY.",
  403: "Invalid API key or IP access denied. Verify WERYAI_API_KEY.",
  500: "WeryAI server error. Please try again later.",
  1002: "Authentication failed. Verify WERYAI_API_KEY.",
};

function printHelp() {
  process.stdout.write(
    [
      "Usage:",
      "  node scripts/account.js balance",
      "",
      "Notes:",
      "  - Requires WERYAI_API_KEY.",
      "  - Queries the official WeryAI account credits endpoint.",
    ].join("\n") + "\n"
  );
}

function getApiKey() {
  const apiKey = (process.env.WERYAI_API_KEY || "").trim();
  return apiKey || null;
}

async function httpJson(method, url, apiKey) {
  const headers = {};
  if (apiKey) headers.Authorization = `Bearer ${apiKey}`;

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 30000);
  try {
    const res = await fetch(url, {
      method,
      headers,
      signal: controller.signal,
    });
    clearTimeout(timer);

    let data;
    try {
      data = await res.json();
    } catch {
      data = { status: res.status, message: `Non-JSON response (HTTP ${res.status})` };
    }
    return { httpStatus: res.status, ...data };
  } catch (error) {
    clearTimeout(timer);
    if (error?.name === "AbortError") throw new Error(`Request timeout: ${method} ${url}`);
    throw error;
  }
}

function isApiSuccess(res) {
  const httpOk = res.httpStatus >= 200 && res.httpStatus < 300;
  const bodyOk = res.status === 0 || res.status === 200;
  return httpOk && bodyOk;
}

function formatApiError(res) {
  const httpStatus = res.httpStatus || 0;
  const code = res.status;
  const msg = res.msg || res.message || "";

  if (httpStatus === 401 || httpStatus === 403) {
    const text = ERROR_MESSAGES[httpStatus] || ERROR_MESSAGES[1002];
    return {
      ok: false,
      phase: "failed",
      errorCode: String(httpStatus),
      errorMessage: `${text}${msg ? ` (${msg})` : ""}`,
    };
  }
  if (httpStatus >= 500) {
    return {
      ok: false,
      phase: "failed",
      errorCode: "500",
      errorMessage: `${ERROR_MESSAGES[500]}${msg ? ` (${msg})` : ""}`,
    };
  }
  const friendly = ERROR_MESSAGES[code] || "";
  return {
    ok: false,
    phase: "failed",
    errorCode: code != null ? String(code) : null,
    errorMessage: friendly && msg ? `${friendly} (${msg})` : friendly || msg || `API error (status ${code}, HTTP ${httpStatus})`,
  };
}

async function queryBalance(apiKey) {
  const res = await httpJson("GET", `${BASE_URL}/v1/generation/balance`, apiKey);
  if (!isApiSuccess(res)) return formatApiError(res);

  const balance = typeof res.data === "number" ? res.data : (res.data?.balance ?? res.data ?? null);
  return {
    ok: true,
    phase: "completed",
    balance,
    topUpRequired: balance === 0,
    rechargeUrl: balance === 0 ? PRICING_URL : null,
    guidance:
      balance === 0
        ? `Balance is 0. Recharge or buy credits at ${PRICING_URL} before running paid WeryAI jobs.`
        : null,
    errorCode: null,
    errorMessage: null,
  };
}

async function main() {
  const command = process.argv[2] || "help";
  if (command === "help" || command === "--help" || command === "-h") {
    printHelp();
    return;
  }
  if (command !== "balance") {
    throw new Error(`Unsupported command: ${command}`);
  }

  const apiKey = getApiKey();
  if (!apiKey) {
    process.stdout.write(
      JSON.stringify(
        {
          ok: false,
          phase: "failed",
          errorCode: "NO_API_KEY",
          errorMessage:
            "Missing WERYAI_API_KEY environment variable. Get one from https://www.weryai.com/api/keys and configure it only in the runtime environment before using this skill.",
        },
        null,
        2
      ) + "\n"
    );
    process.exitCode = 1;
    return;
  }

  const result = await queryBalance(apiKey);
  process.stdout.write(JSON.stringify(result, null, 2) + "\n");
  if (!result.ok) process.exitCode = 1;
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
  process.exit(1);
});
