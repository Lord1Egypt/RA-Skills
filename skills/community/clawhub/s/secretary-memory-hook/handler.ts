import { exec } from "child_process";
import { promisify } from "util";
import { existsSync, mkdirSync } from "fs";
import { join } from "path";

const execAsync = promisify(exec);

const SKILL_SCRIPTS = "/root/.openclaw/workspace/skills/secretary-memory/scripts";
const MEMORY_DIR = "/root/.openclaw/workspace/memory";

/**
 * 运行 Python 脚本
 */
async function runPython(script: string, args: string[] = []): Promise<void> {
  const cmd = `python3 ${script} ${args.join(" ")}`;
  console.log(`[secretary-memory] Running: ${cmd}`);
  try {
    const { stdout, stderr } = await execAsync(cmd, { timeout: 60000 });
    if (stdout) console.log(`[secretary-memory] stdout: ${stdout}`);
    if (stderr) console.error(`[secretary-memory] stderr: ${stderr}`);
  } catch (err: any) {
    console.error(`[secretary-memory] Error: ${err.message}`);
  }
}

/**
 * 确保根目录的 md 文件移动到正确分区（修复索引遗漏问题）
 */
async function ensureRootMdFilesIndexed(): Promise<void> {
  try {
    const { execSync } = require("child_process");
    // 找出 memory/ 根目录下不在 daily/archive/agenda/profile/projects/knowledge 的 md 文件
    const rootMdFiles = execSync(
      `find ${MEMORY_DIR} -maxdepth 1 -name "*.md" -type f 2>/dev/null`
    ).toString().trim().split("\n").filter(Boolean);

    if (rootMdFiles.length === 0) return;

    console.log(`[secretary-memory] 发现 ${rootMdFiles.length} 个根目录 md 文件待迁移:`, rootMdFiles);

    // 确保 projects 目录存在
    const projectsDir = join(MEMORY_DIR, "projects");
    if (!existsSync(projectsDir)) {
      mkdirSync(projectsDir, { recursive: true });
    }

    for (const file of rootMdFiles) {
      const filename = file.split("/").pop();
      // 跳过隐藏文件
      if (filename.startsWith(".")) continue;
      const dest = join(projectsDir, filename);
      try {
        execSync(`mv "${file}" "${dest}"`);
        console.log(`[secretary-memory] 已迁移: ${filename} -> projects/`);
      } catch (e) {
        console.error(`[secretary-memory] 迁移失败: ${filename}`);
      }
    }

    // 迁移后重建索引
    console.log("[secretary-memory] 重建 FTS5 索引...");
    await runPython(`${SKILL_SCRIPTS}/fts5_index.py`, ["--rebuild"]);
  } catch (err: any) {
    console.error(`[secretary-memory] 确保根目录文件索引失败: ${err.message}`);
  }
}

/**
 * session:compact:before — 会话压缩前，生成摘要 + 提取偏好
 */
const handleCompactBefore = async (event: any) => {
  console.log("[secretary-memory] session:compact:before triggered");
  const sessionKey = event.sessionKey || "unknown";

  // 先确保根目录 md 文件被索引（防止 future 遗漏）
  await ensureRootMdFilesIndexed();

  // 功能3：会话摘要
  await runPython(`${SKILL_SCRIPTS}/session_summary.py`, ["--session-id", sessionKey, "--verbose"]);
  // 功能4：偏好提取（暂时禁用，有循环导入bug）
  // await runPython(`${SKILL_SCRIPTS}/profile_miner.py`, ["--session-id", sessionKey]);
};

/**
 * session:compact:after — 会话压缩后，加载上下文到 prompt
 */
const handleCompactAfter = async (event: any) => {
  console.log("[secretary-memory] session:compact:after triggered");
  const sessionKey = event.sessionKey || "unknown";
  await runPython(`${SKILL_SCRIPTS}/auto_loader.py`, ["--session-id", sessionKey]);
};

/**
 * message:sent — 每次回复后，增量记录
 */
const handleMessageSent = async (event: any) => {
  console.log("[secretary-memory] message:sent triggered");
  const sessionKey = event.sessionKey || "unknown";
  const content = event.context?.content || "";
  if (content) {
    const logPath = `${MEMORY_DIR}/daily/.增量日志_${sessionKey}.mdl`;
    const logLine = `\n${new Date().toISOString()} | ${content.substring(0, 200)}`;
    try {
      const { exec: execSync } = require("child_process");
      require("fs").appendFileSync(logPath, logLine);
      console.log(`[secretary-memory] 增量记录已写入: ${logLine.substring(0, 50)}...`);
    } catch (err: any) {
      console.error(`[secretary-memory] 增量记录失败: ${err.message}`);
    }
  }
};

const handler = async (event: any) => {
  const { type, action } = event;

  // Compaction events
  if (type === "session" && action === "compact:before") {
    await handleCompactBefore(event);
    return;
  }

  if (type === "session" && action === "compact:after") {
    await handleCompactAfter(event);
    return;
  }

  // message:sent — 每次回复后触发
  if (type === "message" && action === "sent") {
    await handleMessageSent(event);
    return;
  }

  // Fallback: generic session listener
  if (type === "session:compact:before") {
    await handleCompactBefore(event);
    return;
  }

  if (type === "session:compact:after") {
    await handleCompactAfter(event);
    return;
  }
};

export default handler;
