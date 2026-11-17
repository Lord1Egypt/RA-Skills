/**
 * 通用 HTTP 配置检查脚本（只读检测）
 * 用于检查目标服务的 HTTP 头部基础配置是否符合最佳实践
 *
 * 使用方式：
 *   node scripts/security-headers-check.js --url=http://localhost:3000
 *
 * 参数说明：
 *   --url      目标站点 URL（必填）
 *   --paths    额外检查的路径，逗号分隔（默认仅检查根路径）
 *   --timeout  单个请求超时 ms，默认 10000
 */

const http = require("http");
const https = require("https");
const { URL } = require("url");

const args = parseArgs(process.argv.slice(2));

const config = {
  targetUrl: args["--url"],
  paths: (args["--paths"] || "/").split(",").map((p) => p.trim()),
  timeout: parseInt(args["--timeout"] || "10000", 10),
};

if (!config.targetUrl) {
  console.error("错误：必须指定 --url 参数");
  process.exit(1);
}

const parsedUrl = new URL(config.targetUrl);
const client = parsedUrl.protocol === "https:" ? https : http;

function parseArgs(argv) {
  const result = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith("--")) {
      result[argv[i]] = argv[i + 1] || "";
      i++;
    }
  }
  return result;
}

function checkUrl(path) {
  return new Promise((resolve) => {
    const url = `${parsedUrl.origin}${path}`;
    const req = client.request(
      url,
      { method: "GET", timeout: config.timeout },
      (res) => {
        let data = "";
        res.on("data", (chunk) => (data += chunk));
        res.on("end", () => {
          resolve({
            path,
            url,
            status: res.statusCode,
            headers: res.headers,
            body: data.substring(0, 1000),
          });
        });
      }
    );

    req.on("timeout", () => {
      req.destroy();
      resolve({ path, url, status: 0, headers: {}, body: "", error: "请求超时" });
    });

    req.on("error", (err) => {
      resolve({ path, url, status: 0, headers: {}, body: "", error: err.message });
    });

    req.end();
  });
}

function checkSecurityHeaders(response) {
  const headers = response.headers;
  const issues = [];

  const rules = [
    {
      name: "Content-Security-Policy",
      header: "content-security-policy",
      check: (val) => val && val.length > 0,
      severity: "High",
      message: "CSP 未设置，存在内容注入风险",
      recommendation: "添加 Content-Security-Policy 头，限制脚本和样式来源",
    },
    {
      name: "Strict-Transport-Security",
      header: "strict-transport-security",
      check: (val) => val && val.includes("max-age"),
      severity: "High",
      message: "HSTS 未设置，存在传输层协议降级风险",
      recommendation: "添加 Strict-Transport-Security: max-age=31536000; includeSubDomains",
    },
    {
      name: "X-Content-Type-Options",
      header: "x-content-type-options",
      check: (val) => val && val.toLowerCase() === "nosniff",
      severity: "Medium",
      message: "X-Content-Type-Options 未设置或值不正确",
      recommendation: "添加 X-Content-Type-Options: nosniff",
    },
    {
      name: "X-Frame-Options",
      header: "x-frame-options",
      check: (val) => val && (val.toUpperCase() === "DENY" || val.toUpperCase() === "SAMEORIGIN"),
      severity: "Medium",
      message: "X-Frame-Options 未设置，存在页面嵌套风险",
      recommendation: "添加 X-Frame-Options: DENY 或 SAMEORIGIN",
    },
    {
      name: "Referrer-Policy",
      header: "referrer-policy",
      check: (val) => val && val.length > 0,
      severity: "Low",
      message: "Referrer-Policy 未设置，可能泄露来源 URL",
      recommendation: "添加 Referrer-Policy: strict-origin-when-cross-origin",
    },
    {
      name: "Permissions-Policy",
      header: "permissions-policy",
      check: (val) => val && val.length > 0,
      severity: "Low",
      message: "Permissions-Policy 未设置，浏览器功能权限未限制",
      recommendation: "添加 Permissions-Policy 头限制敏感 API 权限",
    },
  ];

  for (const rule of rules) {
    const value = headers[rule.header];
    if (!rule.check(value)) {
      issues.push({
        header: rule.name,
        currentValue: value || "(未设置)",
        severity: rule.severity,
        message: rule.message,
        recommendation: rule.recommendation,
      });
    }
  }

  return issues;
}

function checkCORS(headers) {
  const issues = [];
  const allowOrigin = headers["access-control-allow-origin"];

  if (allowOrigin === "*") {
    issues.push({
      severity: "Medium",
      message: "CORS Access-Control-Allow-Origin 设置为 *，未限制来源域名",
      recommendation: "将 * 替换为具体的允许域名列表",
    });
  }

  return issues;
}

function checkCookieSecurity(headers) {
  const issues = [];
  const setCookie = headers["set-cookie"];

  if (!setCookie) return issues;

  const cookieStr = Array.isArray(setCookie) ? setCookie.join("; ") : setCookie;

  if (!cookieStr.toLowerCase().includes("httponly")) {
    issues.push({
      severity: "Medium",
      message: "Cookie 未设置 HttpOnly 属性，建议增强会话保护",
      recommendation: "为所有认证/会话 Cookie 添加 HttpOnly 属性",
    });
  }

  if (!cookieStr.toLowerCase().includes("secure")) {
    issues.push({
      severity: "Medium",
      message: "Cookie 未设置 Secure 属性，可能通过 HTTP 明文传输",
      recommendation: "为所有 Cookie 添加 Secure 属性（生产环境）",
    });
  }

  if (!cookieStr.toLowerCase().includes("samesite")) {
    issues.push({
      severity: "Low",
      message: "Cookie 未设置 SameSite 属性，存在跨站请求伪造风险",
      recommendation: "添加 SameSite=Lax 或 Strict",
    });
  }

  return issues;
}

function checkInfoLeak(body, status) {
  const issues = [];
  const leakPatterns = [
    { pattern: /(?:stack\s*trace|at\s+\S+\.\S+:\d+:\d+)/i, label: "堆栈跟踪信息" },
    { pattern: /(?:MySQL|PostgreSQL|MongoDB|Oracle|SQLite)\s*(?:Error|Exception)/i, label: "数据库错误信息" },
    { pattern: /(?:password|secret|token|api[_-]?key)\s*[=:]\s*['"]?\w+['"]?/i, label: "疑似凭据信息" },
    { pattern: /\/home\/\S+|C:\\\S+|\\Users\\\S+/i, label: "服务器内部路径" },
    { pattern: /(?:SELECT|INSERT|UPDATE|DELETE)\s+.*\s+(?:FROM|INTO|SET)/i, label: "SQL 查询语句" },
  ];

  for (const { pattern, label } of leakPatterns) {
    if (pattern.test(body)) {
      issues.push({
        severity: "High",
        message: `错误响应中泄露了${label}`,
        recommendation: "配置全局错误拦截器，生产环境统一返回通用错误信息",
      });
    }
  }

  return issues;
}

function checkDebugEndpoints(response) {
  const issues = [];
  const sensitivePaths = [
    "/admin",
    "/debug",
    "/swagger",
    "/swagger-ui",
    "/api-docs",
    "/actuator",
    "/graphql",
    "/.env",
    "/phpinfo",
    "/console",
    "/metrics",
    "/health",
  ];

  if (response.status >= 200 && response.status < 300) {
    const matchedPath = sensitivePaths.find((p) =>
      response.path.toLowerCase().includes(p)
    );
    if (matchedPath) {
      issues.push({
        severity: "High",
        message: `调试/管理端点 "${response.path}" 可公开访问（HTTP ${response.status}）`,
        recommendation: `为 "${matchedPath}" 添加认证或限制内网访问`,
      });
    }
  }

  return issues;
}

async function main() {
  console.log("=".repeat(60));
  console.log("HTTP 配置合规检查（只读检测）");
  console.log("=".repeat(60));
  console.log(`目标站点: ${parsedUrl.origin}`);
  console.log(`检查路径: ${config.paths.join(", ")}`);
  console.log("-".repeat(60));

  const allPaths = [
    ...config.paths,
    "/admin",
    "/debug",
    "/swagger",
    "/swagger-ui.html",
    "/api-docs",
    "/actuator",
    "/graphql",
    "/.env",
    "/phpinfo.php",
    "/console",
    "/metrics",
    "/health",
  ];

  const results = [];
  for (const path of allPaths) {
    const result = await checkUrl(path);
    console.log(`  ${result.status === 0 ? "❌" : result.status >= 200 && result.status < 300 ? "⚠️" : "✅"} ${path} → HTTP ${result.status}`);
    results.push(result);
  }

  const allIssues = [];

  for (const result of results) {
    if (result.status === 0) continue;

    const securityIssues = checkSecurityHeaders(result);
    securityIssues.forEach((issue) => {
      allIssues.push({ ...issue, path: result.path });
    });

    const corsIssues = checkCORS(result.headers);
    corsIssues.forEach((issue) => {
      allIssues.push({ ...issue, path: result.path, category: "CORS" });
    });

    const cookieIssues = checkCookieSecurity(result.headers);
    cookieIssues.forEach((issue) => {
      allIssues.push({ ...issue, path: result.path, category: "Cookie" });
    });

    const leakIssues = checkInfoLeak(result.body, result.status);
    leakIssues.forEach((issue) => {
      allIssues.push({ ...issue, path: result.path, category: "信息泄露" });
    });

    const debugIssues = checkDebugEndpoints(result);
    debugIssues.forEach((issue) => {
      allIssues.push({ ...issue, path: result.path, category: "调试端点" });
    });
  }

  const seenHeaders = new Set();
  const dedupedIssues = allIssues.filter((issue) => {
    if (issue.header) {
      if (seenHeaders.has(issue.header)) return false;
      seenHeaders.add(issue.header);
    }
    return true;
  });

  console.log("\n配置检查结果");
  console.log("-".repeat(60));

  if (dedupedIssues.length === 0) {
    console.log("未发现配置问题");
  } else {
    const bySeverity = { High: [], Medium: [], Low: [] };
    dedupedIssues.forEach((issue) => {
      bySeverity[issue.severity].push(issue);
    });

    console.log(`发现 ${dedupedIssues.length} 个配置项需要关注：`);
    console.log(`  High:   ${bySeverity.High.length} 个`);
    console.log(`  Medium: ${bySeverity.Medium.length} 个`);
    console.log(`  Low:    ${bySeverity.Low.length} 个`);

    for (const severity of ["High", "Medium", "Low"]) {
      const issues = bySeverity[severity];
      if (issues.length === 0) continue;
      console.log(`\n[${severity}] ${issues.length} 个问题`);
      issues.forEach((issue, i) => {
        console.log(`  ${i + 1}. [${issue.category || issue.header}] ${issue.message}`);
        console.log(`     路径: ${issue.path}`);
        console.log(`     建议: ${issue.recommendation}`);
        if (issue.currentValue) {
          console.log(`     当前值: ${issue.currentValue}`);
        }
      });
    }
  }

  console.log("\n测试结论");
  console.log("-".repeat(60));

  const highCount = dedupedIssues.filter((i) => i.severity === "High").length;
  const mediumCount = dedupedIssues.filter((i) => i.severity === "Medium").length;

  if (dedupedIssues.length === 0) {
    console.log("通过：所有配置符合最佳实践");
    process.exit(0);
  } else if (highCount > 0) {
    console.log(`不通过：存在 ${highCount} 个高危配置项，建议修复`);
    process.exit(1);
  } else if (mediumCount > 0) {
    console.log(`有条件通过：存在 ${mediumCount} 个中危配置项，建议修复`);
    process.exit(0);
  } else {
    console.log("通过：仅存在低危配置项，可后续优化");
    process.exit(0);
  }
}

main().catch((err) => {
  console.error("执行异常:", err.message);
  process.exit(1);
});
