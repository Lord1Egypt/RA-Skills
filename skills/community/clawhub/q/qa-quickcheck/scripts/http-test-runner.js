/**
 * 通用 HTTP 测试跑器 - 配置驱动的接口测试
 * 对应模块：02-动态功能测试
 *
 * 使用方式：
 *   node scripts/http-test-runner.js --config=test-cases.json
 *   node scripts/http-test-runner.js --config=test-cases.json --env=staging
 *   node scripts/http-test-runner.js --config=test-cases.json --parallel
 *
 * 配置文件格式（test-cases.json）：
 * {
 *   "baseUrl": "http://localhost:3000",
 *   "timeout": 10000,
 *   "env": {
 *     "staging": { "baseUrl": "https://staging.example.com" },
 *     "prod": { "baseUrl": "https://api.example.com" }
 *   },
 *   "setup": [
 *     { "name": "登录获取token", "method": "POST", "path": "/api/login", ... }
 *   ],
 *   "tests": [
 *     {
 *       "name": "获取用户列表",
 *       "method": "GET",
 *       "path": "/api/users",
 *       "expect": { "status": 200, "hasFields": ["id", "name"], "type": "array" },
 *       "priority": "P0"
 *     }
 *   ],
 *   "teardown": [
 *     { "name": "清理测试数据", "method": "DELETE", "path": "/api/test/cleanup" }
 *   ]
 * }
 */

const http = require("http");
const https = require("https");
const { URL } = require("url");
const fs = require("fs");
const path = require("path");

const args = parseArgs(process.argv.slice(2));

const configPath = args["--config"];
const envName = args["--env"];
const parallel = args["--parallel"] === "true" || args["--parallel"] === "";

if (!configPath) {
  console.error("错误：必须指定 --config 参数");
  console.error("用法：node scripts/http-test-runner.js --config=test-cases.json [--env=staging] [--parallel]");
  process.exit(1);
}

const configFile = path.resolve(configPath);
if (!fs.existsSync(configFile)) {
  console.error(`错误：配置文件不存在: ${configFile}`);
  process.exit(1);
}

const rawConfig = JSON.parse(fs.readFileSync(configFile, "utf-8"));
let config = { ...rawConfig };

if (envName && rawConfig.env && rawConfig.env[envName]) {
  config = { ...rawConfig, ...rawConfig.env[envName] };
  console.log(`使用环境配置: ${envName}`);
}

config.baseUrl = config.baseUrl || "http://localhost:3000";
config.timeout = config.timeout || 10000;
config.setup = config.setup || [];
config.tests = config.tests || [];
config.teardown = config.teardown || [];

const store = {};

let totalPassed = 0;
let totalFailed = 0;
let totalSkipped = 0;
const failedTests = [];

function parseArgs(argv) {
  const result = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith("--")) {
      const eqIdx = argv[i].indexOf("=");
      if (eqIdx > -1) {
        result[argv[i].substring(0, eqIdx)] = argv[i].substring(eqIdx + 1);
      } else {
        const next = argv[i + 1];
        if (next && !next.startsWith("--")) {
          result[argv[i]] = next;
          i++;
        } else {
          result[argv[i]] = "";
        }
      }
    }
  }
  return result;
}

function resolveValue(value) {
  if (typeof value === "string" && value.startsWith("$store.")) {
    const key = value.substring(7);
    const keys = key.split(".");
    let result = store;
    for (const k of keys) {
      result = result?.[k];
    }
    return result !== undefined ? result : value;
  }
  if (typeof value === "string" && value.startsWith("$env.")) {
    return process.env[value.substring(5)] || value;
  }
  if (typeof value === "string" && value.startsWith("$randomString:")) {
    const len = parseInt(value.substring(14), 10) || 8;
    return Math.random().toString(36).substring(2, 2 + len);
  }
  if (typeof value === "string" && value.startsWith("$timestamp")) {
    return Date.now().toString();
  }
  if (typeof value === "string" && value.startsWith("$uuid")) {
    return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
      const r = (Math.random() * 16) | 0;
      const v = c === "x" ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    });
  }
  return value;
}

function resolveObject(obj) {
  if (typeof obj === "string") return resolveValue(obj);
  if (Array.isArray(obj)) return obj.map(resolveObject);
  if (typeof obj === "object" && obj !== null) {
    const result = {};
    for (const [key, value] of Object.entries(obj)) {
      result[key] = resolveObject(value);
    }
    return result;
  }
  return obj;
}

function sendRequest(testCase) {
  return new Promise((resolve) => {
    const startTime = Date.now();
    const resolved = resolveObject(testCase);
    const url = new URL(resolved.path || "/", config.baseUrl);

    if (resolved.query) {
      Object.entries(resolved.query).forEach(([k, v]) => {
        url.searchParams.set(k, String(v));
      });
    }

    const resolvedHeaders = resolved.headers || {};
    if (!resolvedHeaders["Content-Type"] && resolved.body) {
      resolvedHeaders["Content-Type"] = "application/json";
    }

    const body = resolved.body
      ? typeof resolved.body === "string"
        ? resolved.body
        : JSON.stringify(resolved.body)
      : undefined;

    const client = url.protocol === "https:" ? https : http;

    const req = client.request(
      url.toString(),
      {
        method: resolved.method || "GET",
        headers: resolvedHeaders,
        timeout: config.timeout,
      },
      (res) => {
        let data = "";
        res.on("data", (chunk) => (data += chunk));
        res.on("end", () => {
          const duration = Date.now() - startTime;
          let parsed;
          try {
            parsed = JSON.parse(data);
          } catch {
            parsed = data;
          }

          if (resolved.storeAs) {
            store[resolved.storeAs] = parsed;
          }

          resolve({
            name: testCase.name || testCase.path,
            status: res.statusCode,
            body: typeof parsed === "string" ? parsed.substring(0, 500) : parsed,
            headers: res.headers,
            duration,
            success: res.statusCode >= 200 && res.statusCode < 300,
          });
        });
      }
    );

    req.on("timeout", () => {
      req.destroy();
      resolve({
        name: testCase.name || testCase.path,
        status: 0,
        body: "请求超时",
        duration: config.timeout,
        success: false,
      });
    });

    req.on("error", (err) => {
      resolve({
        name: testCase.name || testCase.path,
        status: 0,
        body: err.message,
        duration: Date.now() - startTime,
        success: false,
      });
    });

    if (body) req.write(body);
    req.end();
  });
}

function runAssertions(testCase, result) {
  const expect = testCase.expect;
  if (!expect) return [];

  const failures = [];

  if (expect.status !== undefined && result.status !== expect.status) {
    failures.push(`状态码期望 ${expect.status}，实际 ${result.status}`);
  }

  if (expect.statusIn && !expect.statusIn.includes(result.status)) {
    failures.push(`状态码期望在 [${expect.statusIn}] 内，实际 ${result.status}`);
  }

  if (expect.contains && typeof result.body === "string") {
    const contains = Array.isArray(expect.contains) ? expect.contains : [expect.contains];
    for (const c of contains) {
      if (!result.body.includes(c)) {
        failures.push(`响应体应包含 "${c}"`);
      }
    }
  }

  if (expect.notContains && typeof result.body === "string") {
    const notContains = Array.isArray(expect.notContains) ? expect.notContains : [expect.notContains];
    for (const c of notContains) {
      if (result.body.includes(c)) {
        failures.push(`响应体不应包含 "${c}"`);
      }
    }
  }

  if (expect.hasFields && typeof result.body === "object") {
    const body = result.body;
    const fields = Array.isArray(expect.hasFields) ? expect.hasFields : [expect.hasFields];
    for (const field of fields) {
      if (!(field in body)) {
        failures.push(`响应体缺少字段 "${field}"`);
      }
    }
  }

  if (expect.type === "array" && !Array.isArray(result.body)) {
    failures.push(`响应体期望为数组，实际为 ${typeof result.body}`);
  }

  if (expect.type === "object" && (typeof result.body !== "object" || Array.isArray(result.body))) {
    failures.push(`响应体期望为对象，实际为 ${typeof result.body}`);
  }

  if (expect.minLength !== undefined && Array.isArray(result.body)) {
    if (result.body.length < expect.minLength) {
      failures.push(`数组长度期望 >= ${expect.minLength}，实际 ${result.body.length}`);
    }
  }

  if (expect.maxDuration !== undefined && result.duration > expect.maxDuration) {
    failures.push(`响应时间期望 <= ${expect.maxDuration}ms，实际 ${result.duration}ms`);
  }

  if (expect.jsonPath) {
    for (const [jpath, expected] of Object.entries(expect.jsonPath)) {
      const actual = getJsonPath(result.body, jpath);
      if (String(actual) !== String(expected)) {
        failures.push(`jsonPath "${jpath}" 期望 "${expected}"，实际 "${actual}"`);
      }
    }
  }

  if (expect.headerContains) {
    for (const [hname, hvalue] of Object.entries(expect.headerContains)) {
      const actual = result.headers[hname.toLowerCase()];
      if (!actual || !actual.includes(hvalue)) {
        failures.push(`响应头 "${hname}" 应包含 "${hvalue}"，实际 "${actual || "(无)"}"`);
      }
    }
  }

  return failures;
}

function getJsonPath(obj, path) {
  const keys = path.split(".");
  let current = obj;
  for (const key of keys) {
    if (current === null || current === undefined) return undefined;
    if (Array.isArray(current) && /^\d+$/.test(key)) {
      current = current[parseInt(key, 10)];
    } else {
      current = current[key];
    }
  }
  return current;
}

async function runPhase(phaseName, cases) {
  if (cases.length === 0) return;

  console.log(`\n${"=".repeat(60)}`);
  console.log(`[${phaseName}] ${cases.length} 个步骤`);
  console.log(`${"=".repeat(60)}`);

  if (parallel && phaseName === "测试用例") {
    const results = await Promise.all(cases.map((c) => sendRequest(c)));
    for (let i = 0; i < cases.length; i++) {
      const result = results[i];
      const testCase = cases[i];
      printResult(testCase, result, phaseName === "测试用例");
    }
  } else {
    for (const testCase of cases) {
      const result = await sendRequest(testCase);
      printResult(testCase, result, phaseName === "测试用例");
    }
  }
}

function printResult(testCase, result, countStats) {
  const priority = testCase.priority ? ` [${testCase.priority}]` : "";
  const name = testCase.name || testCase.path;

  if (result.status === 0) {
    console.log(`  ❌ ${name}${priority} — 连接失败: ${result.body}`);
    if (countStats) {
      totalFailed++;
      failedTests.push({ name, priority: testCase.priority, reason: result.body });
    }
    return;
  }

  const assertions = runAssertions(testCase, result);
  const allPassed = result.success && assertions.length === 0;

  const icon = allPassed ? "✅" : "❌";
  console.log(`  ${icon} ${name}${priority} — HTTP ${result.status} | ${result.duration}ms`);

  if (assertions.length > 0) {
    for (const failure of assertions) {
      console.log(`     ↳ ${failure}`);
    }
  }

  if (testCase.expect && testCase.expect.verbose && result.body) {
    console.log(`     ↳ 响应: ${typeof result.body === "string" ? result.body.substring(0, 200) : JSON.stringify(result.body).substring(0, 200)}`);
  }

  if (countStats) {
    if (allPassed) {
      totalPassed++;
    } else {
      totalFailed++;
      failedTests.push({ name, priority: testCase.priority, reason: assertions.join("; ") || `HTTP ${result.status}` });
    }
  }
}

async function main() {
  console.log("=".repeat(60));
  console.log("HTTP 测试跑器");
  console.log("=".repeat(60));
  console.log(`配置文件: ${configFile}`);
  console.log(`Base URL:  ${config.baseUrl}`);
  console.log(`超时:      ${config.timeout}ms`);
  console.log(`模式:      ${parallel ? "并行" : "串行"}`);

  // Setup 阶段
  if (config.setup.length > 0) {
    await runPhase("Setup", config.setup);
  }

  // 测试阶段
  if (config.tests.length === 0) {
    console.log("\n警告：配置文件中没有定义测试用例");
  } else {
    const priorityFilter = args["--priority"];
    let testsToRun = config.tests;

    if (priorityFilter) {
      testsToRun = config.tests.filter((t) => t.priority === priorityFilter);
      console.log(`优先级过滤: ${priorityFilter}（${testsToRun.length}/${config.tests.length} 个用例）`);
    }

    if (testsToRun.length === 0) {
      console.log("\n没有匹配的测试用例");
    } else {
      await runPhase("测试用例", testsToRun);
    }
  }

  // Teardown 阶段
  if (config.teardown.length > 0) {
    await runPhase("Teardown", config.teardown);
  }

  // 汇总
  const total = totalPassed + totalFailed + totalSkipped;
  console.log(`\n${"=".repeat(60)}`);
  console.log("测试结果汇总");
  console.log(`${"=".repeat(60)}`);
  console.log(`  总计:   ${total}`);
  console.log(`  通过:   ${totalPassed}`);
  console.log(`  失败:   ${totalFailed}`);
  console.log(`  跳过:   ${totalSkipped}`);

  if (failedTests.length > 0) {
    const byPriority = {};
    failedTests.forEach((t) => {
      const p = t.priority || "未标注";
      byPriority[p] = (byPriority[p] || 0) + 1;
    });

    console.log(`\n失败用例明细:`);
    failedTests.forEach((t) => {
      console.log(`  ❌ [${t.priority || "—"}] ${t.name}: ${t.reason}`);
    });

    console.log(`\n按优先级统计失败:`);
    for (const [p, count] of Object.entries(byPriority)) {
      console.log(`  ${p}: ${count} 个`);
    }

    const hasP0 = failedTests.some((t) => t.priority === "P0");
    console.log(`\n结论: ${hasP0 ? "阻塞 — 存在 P0 失败用例" : "有条件通过 — 存在非 P0 失败用例"}`);
    process.exit(hasP0 ? 1 : 0);
  } else {
    console.log("\n结论: 通过 — 所有测试用例通过");
    process.exit(0);
  }
}

main().catch((err) => {
  console.error("测试执行异常:", err.message);
  process.exit(1);
});