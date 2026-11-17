# Safe Terminal Executor / 安全终端执行器

## Core Rule: No Bare Commands — Everything Through Scripts / 核心规则：禁止裸命令——所有操作通过脚本执行

安全包装所有网络请求（curl/wget），强制带超时保护 + 进程退出保证 + 日志输出，防止命令卡死。

Safe wrapper for all network requests (curl/wget). Enforces timeout protection + guaranteed process exit + log output to prevent hung commands.

| Command Type | Handling |
|-------------|----------|
| HTTP API calls (curl/wget) | **Forbidden to execute directly** — generate `.cjs` script |
| File ops (mkdir/copy/rm) without network | Execute directly |
| Node.js scripts (`node xxx.cjs`) | Execute directly |
| npm/pip install | Execute directly, add `--no-progress` |
| Commands estimated >30s | **Forbidden** — split or generate script |
| `git add/commit/push` | Execute directly |

## 5-Step Workflow

### 1 — Classify Command Type
Check if it contains network requests. Yes → continue. No → judge per table above.

### 2 — Generate Test Script
Convert command to `.cjs` script, store in project `{{pipeline.paths.tests}}` directory:
- Naming: `{{pipeline.paths.tests}}test-{feature}-{date}.cjs`
- Must include: timeout guard, step logs, explicit `process.exit`

```javascript
const TIMEOUT = setTimeout(() => {
  console.error('FAIL: Request timed out');
  process.exit(1);
}, 10000);
console.log('[1/3] Sending request...');
```

### 3 — Display Script and Confirm
Show full script, brief explanation, wait for confirmation before execution.

### 4 — Execute + Report
Run `node {{pipeline.paths.tests}}test-xxx.cjs`, report results.

### 5 — Clean Up
Delete one-off scripts after execution. Keep reusable scripts.

## POST Request Template

```javascript
const http = require('http');
const TIMEOUT = setTimeout(() => { console.error('FAIL: Request timed out'); process.exit(1); }, 10000);

const body = JSON.stringify({ /* request params */ });
const options = {
  hostname: '{{pipeline.project.host}}',
  port: {{pipeline.project.port}},
  path: '/your-endpoint',
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) }
};

console.log(`[1/3] POST ${options.hostname}:${options.port}${options.path}`);
const req = http.request(options, res => {
  clearTimeout(TIMEOUT);
  let data = '';
  res.on('data', c => data += c);
  res.on('end', () => {
    console.log(`[3/3] HTTP ${res.statusCode}: ${data.substring(0, 300)}`);
    process.exit(res.statusCode >= 400 ? 1 : 0);
  });
});
req.on('error', e => { clearTimeout(TIMEOUT); console.error(`FAIL: ${e.message}`); process.exit(1); });
req.write(body);
req.end();
```

## GET Request Template

```javascript
const http = require('http');
const TIMEOUT = setTimeout(() => { console.error('FAIL: Request timed out'); process.exit(1); }, 10000);

const options = {
  hostname: '{{pipeline.project.host}}',
  port: {{pipeline.project.port}},
  path: '/your-endpoint',
  method: 'GET'
};

console.log(`[1/2] GET ${options.hostname}:${options.port}${options.path}`);
const req = http.request(options, res => {
  clearTimeout(TIMEOUT);
  let data = '';
  res.on('data', c => data += c);
  res.on('end', () => {
    console.log(`[2/2] HTTP ${res.statusCode}: ${data.substring(0, 300)}`);
    process.exit(res.statusCode >= 400 ? 1 : 0);
  });
});
req.on('error', e => { clearTimeout(TIMEOUT); console.error(`FAIL: ${e.message}`); process.exit(1); });
req.end();
```

## Division of Labor with web-testing

| | safe-terminal-executor | web-testing |
|---|---|---|
| Tests | Backend APIs, CLI commands | Web UI rendering, DOM, interaction |
| Tools | Node.js http module | Playwright + tesseract.js |
| Output | console.log + exit code | Screenshots + DOM assertions + OCR |

The two Skills are complementary, not overlapping.
