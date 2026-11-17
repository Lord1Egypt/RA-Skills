// launcher.mjs —— 由 launcher.vbs（隐藏窗口）调用
// 职责：探测后端是否已在线；没在线就以「托管模式」(WEBCHAT_MANAGED=1) 静默拉起 server.js，
//   然后立即退出。后端生命周期不再由本进程看门狗管，而是交给「扩展心跳」：
//     浏览器开着 → 扩展的 background.js 周期性 ping /api/heartbeat → 后端存活；
//     浏览器关闭 → 扩展服务线程被回收、心跳断 → 后端在宽限期内自行优雅退出。
// 这样做彻底摆脱「写死浏览器进程名」的做法，千问/Edge/Chrome/夸克/任意 Chromium 内核通用。
// 放在 backend/ 目录下，自动以自身所在目录作为后端目录，便于整体拷贝/部署。
import { spawn } from "child_process";
import net from "net";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// 应用端口（用于探测后端是否已在线），默认 3000
let PORT = 3000;
// CLI prewarm 端口（由 SERVER__PORT 控制，避开 WorkBuddy 桌面占用的端口冲突）。
// null 表示「用户没在 .env 显式设置」→ 不注入，让 server.js 自己分配空闲端口；
// 非 null 表示用户显式设置了 → 显式注入，覆盖本机可能存在的系统级 SERVER__PORT，
// 否则 dotenv 不覆盖已存在环境变量，CLI prewarm 会撞上被占用的端口导致卡死。
let SERVER_PORT = null;
try {
  const txt = fs.readFileSync(path.join(__dirname, ".env"), "utf8");
  const mP = txt.match(/^\s*PORT\s*=\s*(\d+)/m);
  if (mP) PORT = parseInt(mP[1], 10);
  const mS = txt.match(/^\s*SERVER__PORT\s*=\s*(\d+)/m);
  if (mS) SERVER_PORT = parseInt(mS[1], 10);
} catch (_) {}

function probe() {
  return new Promise((resolve) => {
    const s = net.connect({ host: "127.0.0.1", port: PORT });
    let settled = false;
    const done = (v) => {
      if (settled) return;
      settled = true;
      try {
        s.destroy();
      } catch (_) {}
      resolve(v);
    };
    s.setTimeout(700);
    s.on("connect", () => done(true));
    s.on("error", () => done(false));
    s.on("timeout", () => done(false));
  });
}

const already = await probe();
if (already) {
  console.log("backend already running on port " + PORT);
  process.exit(0);
}

// 拉起 server.js：托管模式（靠扩展心跳续命），detached 脱离启动器独立运行
// 仅当用户在 .env 显式设了 SERVER__PORT 时才注入，用于覆盖系统级 SERVER__PORT，
// 避免 CLI prewarm 撞上 WorkBuddy 桌面已占用的端口而 EADDRINUSE 卡死。
const childEnv = { ...process.env, WEBCHAT_MANAGED: "1" };
if (SERVER_PORT !== null) childEnv.SERVER__PORT = String(SERVER_PORT);
const child = spawn(process.execPath, ["server.js"], {
  cwd: __dirname,
  detached: true,
  stdio: "ignore",
  windowsHide: true,
  env: childEnv,
});
child.unref(); // 不阻止本进程退出；后端作为独立进程继续运行

console.log("backend launched (managed mode), pid=" + child.pid);
process.exit(0);
