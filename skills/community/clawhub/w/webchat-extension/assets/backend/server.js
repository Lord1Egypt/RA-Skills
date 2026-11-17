import express from "express";
import cors from "cors";
import net from "net";
import os from "node:os";
import fs from "node:fs";
import path from "node:path";
import { spawnSync, execSync } from "node:child_process";
import dotenv from "dotenv";
import { query } from "@tencent-ai/agent-sdk";

dotenv.config();

// 定位官方 codebuddy CLI（@tencent-ai/codebuddy-code）。SDK 的 query() 通过 stdio 拉起它，
// 必须用官方 CLI（含 SDK 期望的 dist/codebuddy-headless.js），不能用 WorkBuddy 自带那份。
// ⚠️ 关键（Windows）：返回的路径必须是「绝对路径」且以 bin/codebuddy 结尾。
//   Node SDK 的 transport 会把 pathToCodebuddyCode 作为脚本参数交给 node 执行：
//     spawn('node', [pathToCodebuddyCode, ...args])
//   且只有当路径以 /bin/codebuddy 或 \bin\codebuddy 结尾时，才会自动改写成
//   dist/codebuddy-headless.js（SDK 期望的 headless 入口）。
//   若传裸 "codebuddy"（PATH 上的 sh 包装器），node 无法把它当脚本执行 → CLI 进程直接退出
//   → "CLI process stdout closed unexpectedly"。所以 Windows 上绝不能直接返回裸命令。
//   该 CLI 读取全局凭据（~/.codebuddy/local_storage），与你在终端/WorkBuddy 登录的是同一套，
//   因此「登录模式」直接复用，无需 Key。
// 解析优先级：① 显式 CODEBUDDY_CLI_PATH → ② Windows 受管 node 目录下的绝对路径 → ③ 非 Windows 用 PATH → ④ 兜底裸命令。
function resolveCli() {
  if (process.env.CODEBUDDY_CLI_PATH) return process.env.CODEBUDDY_CLI_PATH;

  if (process.platform === "win32") {
    // 在受管 node 各版本目录下查找 SDK 配套 CLI 的绝对路径（兼容版本号漂移）
    const base = path.join(os.homedir(), ".workbuddy", "binaries", "node", "versions");
    let candidates = [];
    try {
      const versions = fs.readdirSync(base);
      candidates = versions
        .map((v) =>
          path.join(base, v, "node_modules", "@tencent-ai", "codebuddy-code", "bin", "codebuddy")
        )
        .filter((p) => fs.existsSync(p));
    } catch (_) {}
    // 固定版本兜底
    candidates.push(
      path.join(
        os.homedir(),
        ".workbuddy/binaries/node/versions/22.22.2/node_modules/@tencent-ai/codebuddy-code/bin/codebuddy"
      )
    );
    for (const c of candidates) {
      if (fs.existsSync(c)) return c;
    }
    return "codebuddy"; // 最后兜底（通常仍会失败，但让 SDK 给出清晰报错）
  }

  // 非 Windows：裸 codebuddy 可正常工作（依赖 PATH）
  try {
    const r = spawnSync("codebuddy", ["--version"], { encoding: "utf8", windowsHide: true });
    if (r.status === 0 && (r.stdout || "").includes(".")) return "codebuddy";
  } catch (_) {}
  const fallback = path.join(
    os.homedir(),
    ".workbuddy/binaries/node/versions/22.22.2/node_modules/@tencent-ai/codebuddy-code/bin/codebuddy"
  );
  return fs.existsSync(fallback) ? fallback : "codebuddy";
}

// 官方 codebuddy CLI 启动时会起一个 prewarm 本地 server，端口由 SERVER__PORT 控制。
// 本机 WorkBuddy 桌面应用自身也会起 serve/prewarm 实例（默认落在 ~63000-64000 区间，
// 例如 63516/63424）。若我们的 CLI 也抢到这个范围，会 EADDRINUSE 挂起，表现为
// SDK query() 永远 0 字节超时（"Request timeout: initialize"）。
// 因此不能在「OS 临时端口」里随机选——Windows 的临时端口分配与桌面 codebuddy 高度重叠。
// 这里改为在【桌面不使用的固定安全区间 45000-49999】内逐个 bind 校验，取第一个真正空闲的，
// 彻底避开桌面端口。也可在 .env 里手动指定 SERVER__PORT=<port> 覆盖。
const SAFE_PORT_RANGE = { min: 45000, max: 49999 };
async function getFreePort() {
  for (let port = SAFE_PORT_RANGE.min; port <= SAFE_PORT_RANGE.max; port++) {
    const free = await new Promise((resolve) => {
      const srv = net.createServer();
      srv.once("error", () => resolve(false));
      srv.listen(port, "127.0.0.1", () => srv.close(() => resolve(true)));
    });
    if (free) return port;
  }
  // 安全区间耗尽时的兜底：退回 OS 临时端口
  return new Promise((resolve, reject) => {
    const srv = net.createServer();
    srv.on("error", reject);
    srv.listen(0, () => {
      const { port } = srv.address();
      srv.close(() => resolve(port));
    });
  });
}

// 退出时清理：只杀「我们自己 spawn 出来的 codebuddy CLI 子进程」，绝不误伤外来进程。
// 设计原则（避免 误杀，参考 dingtalk-auto-reply 的看门狗机制）：
//   - 绝不按端口 netstat 扫描乱杀——端口子串匹配会把 45012 误中 450123，且易误杀
//     带有自己看门狗、会被自动重拉的进程（如 dingtalk 监控）。
//   - 改为：在「本进程(server.js)的进程树」里，找命令行包含我们解析到的 CLI 路径的后代进程，
//     只杀它们。dingtalk 监控 / WorkBuddy 桌面 / 其它 codebuddy 实例都不是我们的后代，绝不会被命中。
//   - 即便某进程有看门狗会自愈，我们也连误杀都不做——精确到「进程树 + CLI 路径」。
//   - Pass B 作为兜底：若 CLI 被 detach 不再是后代，再用 netstat 找监听在我们 SERVER__PORT 上的
//     进程，但**必须命令行含我们的 CLI 路径(marker)**才杀，相当于二次确认，杜绝误杀外来进程。
function killOwnCli() {
  const myPid = process.pid;
  const cliMarker = CODEBUDDY_CLI.replace(/\\/g, "/"); // 我们的 CLI 绝对路径（含 codebuddy-code/bin/codebuddy）
  const port = process.env.SERVER__PORT;
  try {
    if (process.platform === "win32") {
      const ps = `
$myPid = ${myPid}
$marker = "${cliMarker}"
$port = ${port}
$procs = Get-CimInstance Win32_Process -Property ProcessId,ParentProcessId,CommandLine
$child = @{}
foreach ($p in $procs) { if ($p.ParentProcessId) { if (-not $child.ContainsKey($p.ParentProcessId)) { $child[$p.ParentProcessId] = @() }; $child[$p.ParentProcessId] += $p.ProcessId } }
$desc = @{}
$queue = New-Object System.Collections.Queue
$queue.Enqueue($myPid)
while ($queue.Count -gt 0) { $cur = $queue.Dequeue(); foreach ($c in $child[$cur]) { if (-not $desc.ContainsKey($c)) { $desc[$c] = $true; $queue.Enqueue($c) } } }
$killed = @()
# Pass A：我们的后代里跑着我们 CLI 的进程
foreach ($p in $procs) { if ($desc[$p.ProcessId] -and $p.CommandLine -and $p.CommandLine.Replace('\','/').Contains($marker)) { Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue; $killed += $p.ProcessId } }
# Pass B（兜底）：监听在我们 SERVER__PORT 上、且命令行含我们 CLI 路径的进程（marker 门控，绝不误杀外来进程）
try {
  $net = netstat -ano | Select-String ":$port\\s" | Select-String "LISTENING"
  foreach ($line in $net) {
    $parts = ($line.Line -split '\\s+') | Where-Object { $_ -match '^\\d+$' }
    $pid = $parts | Select-Object -Last 1
    if ($pid -and ($procs | Where-Object { $_.ProcessId -eq $pid -and $_.CommandLine -and $_.CommandLine.Replace('\','/').Contains($marker) })) {
      Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue; $killed += $pid
    }
  }
} catch {}
Write-Host ("[cleanup] killed own codebuddy CLI pids: " + ($killed -join ','))
`;
      execSync("powershell -NoProfile -NonInteractive -Command -", {
        input: ps,
        windowsHide: true,
        encoding: "utf8",
      });
    } else {
      // 非 Windows：用 CLI 路径精确匹配（受管安装路径唯一，不会误中其它 codebuddy）
      const out = execSync(`pgrep -f ${JSON.stringify(cliMarker)}`, {
        encoding: "utf8",
        windowsHide: true,
      })
        .trim()
        .split(/\s+/)
        .filter(Boolean);
      for (const pid of out) execSync(`kill -9 ${pid}`, { windowsHide: true });
    }
  } catch (_) {
    /* 无后代 / 已退出，忽略 */
  }
}
// 校验某端口是否真的空闲（在 127.0.0.1 上真实 bind 一次）。
async function isPortFree(port) {
  return new Promise((resolve) => {
    const srv = net.createServer();
    srv.once("error", () => resolve(false));
    srv.listen(port, "127.0.0.1", () => srv.close(() => resolve(true)));
  });
}
// 端口分配策略（关键坑修复）：
//   - 未设置 SERVER__PORT → 分配空闲端口；
//   - 已设置但被占用（典型：直接 `node server.js` 时继承了 WorkBuddy 桌面的环境端口 63516）
//     → 也重新分配，避免 CLI prewarm 因 EADDRINUSE 挂死 / 0 字节超时。
//   - 已设置且空闲（如 launcher.mjs 从 .env 注入的明确端口）→ 尊重使用。
if (
  !process.env.SERVER__PORT ||
  !(await isPortFree(Number(process.env.SERVER__PORT)))
) {
  process.env.SERVER__PORT = String(await getFreePort());
}

const app = express();
const PORT = process.env.PORT || 3000;
const API_KEY = (process.env.CODEBUDDY_API_KEY || "").trim();
const FORCE_DEMO = process.env.WEBCHAT_DEMO === "1";
// 认证模式（参考 dingtalk-auto-reply 的「Key / CLI 已登录」二选一范式，零配置优先）：
//  - key  ：配置了 CODEBUDDY_API_KEY → 用 Key 直连（推荐无人值守）
//  - login：未配 Key → 复用本机 codebuddy CLI 已登录凭据（零配置，与你在终端/WorkBuddy 登录的是同一套）
//  演示模式仅在显式 WEBCHAT_DEMO=1 时触发；否则只要能登录/有 Key 就走真实模型。
const AUTH_MODE = API_KEY ? "key" : "login";
const MODEL = process.env.CODEBUDDY_MODEL || "deepseek-v4-flash";
const ALLOWED_ORIGIN = process.env.ALLOWED_ORIGIN || "*";
// 托管模式：由扩展(webchat:// 协议)拉起时为 1。此时后端生命周期交给「扩展心跳」——
// 浏览器开着→扩展持续 ping 心跳→后端存活；浏览器关→扩展服务线程回收→心跳断→后端自退。
// 此模式下完全不需要知道浏览器进程名，任意 Chromium 内核通用。
const MANAGED = process.env.WEBCHAT_MANAGED === "1";
// @tencent-ai/agent-sdk 的 query() 需要本地有 codebuddy CLI 子进程（transport 通过 stdio 拉起它）。
// 必须用 SDK 配套的官方 CLI（@tencent-ai/codebuddy-code），它有 SDK 期望的 dist/codebuddy-headless.js 入口；
// 不能用 WorkBuddy 自带的那份 cli/dist/codebuddy.js（v2.106，与 SDK 协议不匹配，会 initialize 超时）。
const CODEBUDDY_CLI = resolveCli();

// 中国版必须设置该环境变量，否则默认走海外网关会拒绝国内 key（initialize 握手失败）。
if (!process.env.CODEBUDDY_INTERNET_ENVIRONMENT) {
  process.env.CODEBUDDY_INTERNET_ENVIRONMENT = "internal";
}

app.use(
  cors({
    origin: ALLOWED_ORIGIN,
    methods: ["GET", "POST", "OPTIONS"],
    credentials: false,
  })
);
app.use(express.json());

// 健康检查：顺便告诉前端当前是真实模式还是演示模式
app.get("/api/health", (req, res) => {
  res.json({
    status: "ok",
    mode: AUTH_MODE, // key | login
    demo: FORCE_DEMO,
    auth: AUTH_MODE,
    model: MODEL,
    serverPort: process.env.SERVER__PORT,
    managed: MANAGED,
    ts: new Date().toISOString(),
  });
});

// 登录态自检：供面板/手动确认 codebuddy CLI 是否已登录（登录模式用）。
// 用一次「极短 query」实测能否拉起 CLI 并出 token（15s 超时兜底，避免无头环境卡死）。
// 若实测通过 → loggedIn:true；若超时/失败 → 回退到「凭据文件存在性」判断，仍给明确结论。
app.get("/api/auth", async (req, res) => {
  // 有 Key 时直接视为已认证（key 模式）
  if (API_KEY) {
    return res.json({ loggedIn: true, mode: "key", via: "apikey" });
  }
  // 快速实测：跑一次 1-turn 极短 query，看 CLI 能否用登录凭据产出内容
  let probeOk = false;
  try {
    await Promise.race([
      (async () => {
        for await (const _m of query({
          prompt: "ping",
          options: {
            cwd: process.cwd(),
            model: MODEL,
            maxTurns: 1,
            systemPrompt: "你是自检探针，只回 ok",
            permissionMode: "default",
            canUseTool: async () => ({ behavior: "deny" }),
            pathToCodebuddyCode: CODEBUDDY_CLI,
            env: {
              CODEBUDDY_INTERNET_ENVIRONMENT:
                process.env.CODEBUDDY_INTERNET_ENVIRONMENT || "internal",
              SERVER__PORT: process.env.SERVER__PORT,
            },
          },
        })) {
          probeOk = true;
          break;
        }
      })(),
      new Promise((_, rej) => setTimeout(() => rej(new Error("timeout")), 15000)),
    ]);
  } catch {
    probeOk = false;
  }
  if (probeOk) {
    return res.json({ loggedIn: true, mode: "login", via: "probe" });
  }
  // 回退：检查 codebuddy 凭据目录是否存在（~/.codebuddy/local_storage 有内容即大概率已登录）
  const credDir = path.join(os.homedir(), ".codebuddy", "local_storage");
  const hasCred =
    fs.existsSync(credDir) && fs.readdirSync(credDir).length > 0;
  res.json({
    loggedIn: hasCred,
    mode: "login",
    via: "filesystem",
    hint: hasCred
      ? "凭据目录存在，但极短 query 实测未通过（CLI 可能首次冷启动较慢）。直接用面板提问即可；若持续失败，请确认 codebuddy 已登录：`codebuddy`。"
      : "未检测到 codebuddy 登录凭据。请先在终端运行 `codebuddy` 完成登录，或在 backend/.env 配置 CODEBUDDY_API_KEY。",
  });
});

// 心跳：仅托管模式(MANAGED=1)使用。扩展的 background.js 用 chrome.alarms 周期性调用本端点；
// 后端记录 lastHeartbeat，若超过 HEARTBEAT_TTL 没收到心跳(=浏览器已关)，自行优雅退出。
app.post("/api/heartbeat", (req, res) => {
  lastHeartbeat = Date.now();
  res.json({ status: "ok", managed: MANAGED, ttl: HEARTBEAT_TTL });
});

// 构造系统提示：把网页上下文塞进去，让 AI 知道用户在看什么
function buildSystemPrompt(context, pageTitle, pageUrl) {
  const ctxBlock =
    context && context.trim()
      ? `\n\n【用户当前正在浏览的网页上下文】\n网页标题：${
          pageTitle || "未知"
        }\n网页地址：${pageUrl || "未知"}\n用户选中的内容：\n"""\n${context.trim()}\n"""\n请基于以上网页内容回答用户问题；若问题与上下文无关，也可正常回答。`
      : "";
  return (
    '你是"小虾"，一个中文 AI 助手，风格简洁、直接、有帮助。回答用中文。' +
    ctxBlock
  );
}

// 把多轮历史 + 当前问题拼成单轮 prompt（无状态，最简单稳）
function buildUserPrompt(question, history) {
  let p = "";
  if (Array.isArray(history) && history.length) {
    p += "【对话历史】\n";
    for (const m of history) {
      p += (m.role === "assistant" ? "小虾" : "用户") + "：" + m.content + "\n";
    }
    p += "\n";
  }
  p += "【当前问题】\n" + (question || "");
  return p;
}

// 演示模式：没有 API Key 时，模拟流式打字机回复，方便验收交互闭环
async function streamDemo(res, ctx, question) {
  const snippet = (ctx || "").trim().slice(0, 100);
  const reply =
    `（演示模式 · 未配置 CODEBUDDY_API_KEY）\n\n` +
    `我读到了你在网页上选中的内容：\n「${snippet}${
      ctx && ctx.length > 100 ? "…" : ""
    }」\n\n` +
    `你的问题是：「${question}」\n\n` +
    `这是一段模拟回复，用来验收「划线 → 唤起对话 → 流式显示」的闭环是否正常。\n` +
    `配置好 API Key 后，这里就会变成真实的 AI 回答 🦐`;
  const chunks = reply.match(/[\s\S]{1,12}/g) || [reply];
  for (const c of chunks) {
    res.write(`data: ${JSON.stringify({ type: "text", content: c })}\n\n`);
    await new Promise((r) => setTimeout(r, 22));
  }
  res.write(`data: ${JSON.stringify({ type: "done" })}\n\n`);
}

// 核心：网页划线对话接口（SSE 流式）
app.post("/api/chat", async (req, res) => {
  const {
    context = "",
    question = "",
    history = [],
    pageTitle = "",
    pageUrl = "",
  } = req.body || {};

  if (!question && !context) {
    return res.status(400).json({ error: "question 或 context 不能为空" });
  }

  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");

  // 演示模式（仅 WEBCHAT_DEMO=1 强制；否则无 Key 也走登录模式的真实模型，不再降级 demo）
  if (FORCE_DEMO) {
    res.write(`data: ${JSON.stringify({ type: "init", mode: "demo" })}\n\n`);
    await streamDemo(res, context, question);
    return res.end();
  }

  // 真实模式
  res.write(
    `data: ${JSON.stringify({ type: "init", mode: "real", model: MODEL })}\n\n`
  );
  const systemPrompt = buildSystemPrompt(context, pageTitle, pageUrl);
  const prompt = buildUserPrompt(question, history);
  const canUseTool = async () => ({
    behavior: "deny",
    message: "本插件仅做文本问答，不允许使用工具",
  });

  try {
    // 把认证相关环境变量显式传给 SDK（与 dingtalk-auto-reply 一致）：
    //  - CODEBUDDY_INTERNET_ENVIRONMENT 中国版 internal（已在上方兜底设置）
    //  - CODEBUDDY_API_KEY 仅在有 Key 时注入；无 Key 时让 SDK 复用 CLI 登录凭据（登录模式）
    //  - SERVER__PORT 复用本进程已分配的空闲端口，避免与 WorkBuddy 桌面冲突
    const sdkEnv = {
      CODEBUDDY_INTERNET_ENVIRONMENT:
        process.env.CODEBUDDY_INTERNET_ENVIRONMENT || "internal",
      SERVER__PORT: process.env.SERVER__PORT,
    };
    if (API_KEY) sdkEnv.CODEBUDDY_API_KEY = API_KEY;

    const stream = query({
      prompt,
      options: {
        cwd: process.cwd(),
        model: MODEL,
        maxTurns: 5,
        systemPrompt,
        permissionMode: "default",
        canUseTool,
        pathToCodebuddyCode: CODEBUDDY_CLI,
        env: sdkEnv,
        stderr: (t) => console.error("[clistderr]", t),
      },
    });

    for await (const msg of stream) {
      if (msg.type === "assistant") {
        const content = msg.message?.content;
        if (typeof content === "string") {
          res.write(
            `data: ${JSON.stringify({ type: "text", content })}\n\n`
          );
        } else if (Array.isArray(content)) {
          for (const block of content) {
            if (block?.type === "text" && block.text) {
              res.write(
                `data: ${JSON.stringify({ type: "text", content: block.text })}\n\n`
              );
            }
          }
        }
      } else if (msg.type === "result") {
        res.write(
          `data: ${JSON.stringify({
            type: "done",
            duration: msg.duration_ms || msg.duration,
          })}\n\n`
        );
      }
    }
    res.end();
  } catch (err) {
    const msg = err?.message || String(err);
    console.error("[chat] error:", msg);
    // 区分认证类错误（登录失效/未登录/Key 无效）与一般性错误，给清晰的修复指引
    const isAuth =
      /auth|login|token|unauthor|401|session|凭据|登录|initialize/i.test(msg);
    const hint = isAuth
      ? "认证失败：请先在终端运行 `codebuddy` 完成登录（与你在 WorkBuddy 用的是同一套凭据），或在 backend/.env 配置 CODEBUDDY_API_KEY 后重启后端。"
      : msg || "调用 AI 失败";
    res.write(
      `data: ${JSON.stringify({
        type: "error",
        message: hint,
        kind: isAuth ? "auth" : "generic",
      })}\n\n`
    );
    res.end();
  }
});

// 优雅停止：面板点「停止后端」时调用，进程自行退出（无需关终端/任务管理器）
app.post("/api/stop", (req, res) => {
  res.json({ status: "stopping" });
  // 给响应一点时间 flush 后再退出
  setTimeout(() => {
    killOwnCli();
    process.exit(0);
  }, 300);
});

// 空闲自动退出：启动后若连续 IDLE_TIMEOUT_MIN 分钟无任何请求，自动退出。
// 目的：用户用完关闭浏览器后，常驻后端不会一直占资源（不常驻策略的兜底）。
const IDLE_TIMEOUT_MIN = Number(process.env.IDLE_TIMEOUT_MIN || 30);
let idleTimer = null;
function resetIdleTimer() {
  if (idleTimer) clearTimeout(idleTimer);
  idleTimer = setTimeout(() => {
    console.log(`\n[idle] ${IDLE_TIMEOUT_MIN} 分钟无请求，自动退出后端。`);
    killOwnCli();
    process.exit(0);
  }, IDLE_TIMEOUT_MIN * 60 * 1000);
}
resetIdleTimer();
// 所有请求都重置空闲计时（health / chat / stop）
app.use((req, res, next) => {
  if (req.path !== "/api/stop") resetIdleTimer();
  next();
});

// ---------- 托管模式心跳看门狗 ----------
// 心跳宽限：扩展闹钟约每 60s 一次，这里给 2.5 分钟宽限，避免 SW 节流误杀。
const HEARTBEAT_TTL = Number(process.env.HEARTBEAT_TTL || 150000);
let lastHeartbeat = Date.now(); // 托管模式下，以启动时刻为初始心跳
function startHeartbeatWatchdog() {
  setInterval(() => {
    if (Date.now() - lastHeartbeat > HEARTBEAT_TTL) {
      console.log(
        `\n[heartbeat] ${HEARTBEAT_TTL}ms 内未收到扩展心跳（浏览器已关闭？），自动退出后端。`
      );
      killOwnCli();
      process.exit(0);
    }
  }, 5000);
  console.log(`  托管模式：靠扩展心跳续命，心跳断 ${HEARTBEAT_TTL}ms 后自退（跨浏览器通用，无需进程名）`);
}

// 全局退出清理：无论何种方式退出，都只清理「我们自己 spawn 的 codebuddy CLI 子进程」
// （按进程树 + CLI 路径精确匹配），避免 prewarm 端口泄漏。绝不误杀外来进程（含带看门狗的）。
function cleanupCli() {
  killOwnCli();
}
process.on("exit", cleanupCli);
process.on("SIGINT", () => {
  cleanupCli();
  process.exit(0);
});
process.on("SIGTERM", () => {
  cleanupCli();
  process.exit(0);
});

app.listen(PORT, () => {
  console.log(`\n◉ 网页划线对话后端已启动: http://localhost:${PORT}`);
  console.log(
    `  认证模式: ${
      AUTH_MODE === "key"
        ? "真实 AI · API Key（CODEBUDDY_API_KEY 已配置）"
        : FORCE_DEMO
        ? "演示模式（WEBCHAT_DEMO=1 强制）"
        : "真实 AI · 登录模式（复用 codebuddy CLI 已登录凭据，零配置）"
    }`
  );
  console.log(`  CLI prewarm 端口 SERVER__PORT=${process.env.SERVER__PORT}（避开 WorkBuddy 端口冲突）`);
  console.log(`  空闲 ${IDLE_TIMEOUT_MIN} 分钟自动退出（可设 IDLE_TIMEOUT_MIN 调整）`);
  if (MANAGED) startHeartbeatWatchdog();
  console.log("");
});
