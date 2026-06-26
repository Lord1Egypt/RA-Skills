const { readFile } = require("node:fs/promises");
const { existsSync } = require("node:fs");
const { join, basename } = require("node:path");

const MAX_MESSAGES = 40;

function normalizeText(text) {
  return text
    .replace(/^System: \[.*?\] Feishu\[default\].*?(?:\n\n|$)/is, "")
    .replace(/Conversation info \(untrusted metadata\):\n```json\n[\s\S]*?\n```\n*/g, "")
    .replace(/Sender \(untrusted metadata\):\n```json\n[\s\S]*?\n```\n*/g, "")
    .replace(/<relevant-memories>[\s\S]*?<\/relevant-memories>/gi, " ")
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/\[\[\s*reply_to_current\s*\]\]/gi, " ")
    .replace(/\[\[\s*reply_to:[^\]]+\]\]/gi, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function isUsefulText(text) {
  if (!text) return false;
  if (text.startsWith("/")) return false;
  if (text.includes("<relevant-memories>")) return false;
  if (/^Skills store policy/i.test(text)) return false;
  if (/^✅\s*New session started/i.test(text)) return false;
  return true;
}

async function findSessionFile(event) {
  try {
    const fs = require("node:fs");
    const prev = event?.context?.previousSessionEntry;
    const curr = event?.context?.sessionEntry;
    const candidates = [prev?.sessionFile, curr?.sessionFile].filter(Boolean);

    for (const file of candidates) {
      if (typeof file === "string" && fs.existsSync(file)) return file;
    }

    const os = require("node:os");
    // [EDIT HERE] Replace '<YOUR_AGENT_ID>' with your actual agent ID (e.g. 'main')
    const sessionsDir = join(os.homedir(), ".openclaw/agents/<YOUR_AGENT_ID>/sessions");
    if (fs.existsSync(sessionsDir)) {
      const allFiles = fs.readdirSync(sessionsDir);
      const resetFiles = allFiles
        .filter((name) => name.includes(".reset."))
        .map((name) => ({ name, time: fs.statSync(join(sessionsDir, name)).mtimeMs }))
        .sort((a, b) => a.time - b.time);

      if (resetFiles.length > 0) {
        const latestResetFile = resetFiles[resetFiles.length - 1].name;
        return join(sessionsDir, latestResetFile);
      }
    }
  } catch (e) {
    console.error("[session-memory-structured] findSessionFile error:", e.message);
  }

  return null;
}

async function getProviderConfig() {
  const os = require("node:os");
  // [EDIT HERE] Replace '<YOUR_AGENT_ID>' with your actual agent ID
  const configPath = join(os.homedir(), ".openclaw", "agents", "<YOUR_AGENT_ID>", "agent", "models.json");
  const raw = await readFile(configPath, "utf8");
  const config = JSON.parse(raw);
  // [EDIT HERE] Replace '<YOUR_PROVIDER_ID>' with your actual provider key from models.json
  return config.providers?.["<YOUR_PROVIDER_ID>"];
}

async function readSessionMessages(sessionFile, maxCount) {
  try {
    const raw = await readFile(sessionFile, "utf8");
    const lines = raw.trim().split("\n");
    const result = [];

    for (const line of lines) {
      if (!line) continue;
      try {
        const obj = JSON.parse(line);
        if (obj.type === "message" && obj.message && ["user", "assistant"].includes(obj.message.role)) {
          let text = "";
          if (Array.isArray(obj.message.content)) {
            text = obj.message.content.find((c) => c.type === "text")?.text || "";
          } else {
            text = obj.message.content || "";
          }

          const cleanText = normalizeText(text);
          if (isUsefulText(cleanText)) {
            result.push({ role: obj.message.role, text: cleanText });
          }
        }
      } catch (e) {
        console.error("[session-memory-structured] parse loop error:", e.message);
      }
    }

    return result.slice(-maxCount);
  } catch (e) {
    console.error("[session-memory-structured] error reading session:", e.message);
    return [];
  }
}

const SYSTEM_PROMPT = `你是一个会话历史总结助手。请基于提供的过去会话记录，生成一份高度凝练的结构化会话纪要。
请你严格输出以下四块内容，直接输出 Markdown 即可，不用输出多余的开场白或解释：

### 1. 本次会话做了什么
- 简要汇总对话的核心任务和操作

### 2. 新确认的偏好 / 规则 / 决定
- 提取用户明确要求的开发规则、上下文偏好或刚做出的架构决定 (若无则写 "- 暂无")

### 3. 重要但暂不进长期记忆的上下文
- 列出一些对后续有帮助，但还不需要沉淀为永久记忆的事实线索 (若无则写 "- 暂无")

### 4. 未完成事项 / 下次继续点
- 有什么待办、下一步计划或尚未验证的问题 (若无则写 "- 暂无")`;

const handler = async (event) => {
  const isTargetCommand = event?.type === "command" && (event.action === "new" || event.action === "reset");
  if (!isTargetCommand) return;

  try {
    const sessionFile = await findSessionFile(event);
    if (!sessionFile) return;

    const { readFileSync, promises: fsPromises } = require("node:fs");

    const sessionIdMatch = basename(sessionFile).match(/^([a-f0-9\-]{36})/);
    const sessionId = sessionIdMatch ? sessionIdMatch[1] : "unknown";
    if (sessionId === "unknown") return;

    const workspaceDir = typeof event?.context?.workspaceDir === "string" ? event.context.workspaceDir : process.cwd();
    const memoryDir = join(workspaceDir, "memory");

    const now = new Date();
    const pad = (n) => String(n).padStart(2, "0");
    const dateStr = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
    const archiveFile = join(memoryDir, `${dateStr}.md`);

    if (existsSync(archiveFile)) {
      const content = readFileSync(archiveFile, "utf8");
      if (content.includes(`Session ID: ${sessionId}`)) {
        return;
      }
    }

    console.log(`[session-memory-structured] summarizing session ${sessionId}...`);

    const messages = await readSessionMessages(sessionFile, MAX_MESSAGES);
    if (messages.length === 0) return;

    const historyText = messages.map((m) => `[${m.role.toUpperCase()}]: ${m.text}`).join("\n");

    const providerConfig = await getProviderConfig();
    if (!providerConfig || !providerConfig.apiKey || !providerConfig.baseUrl) {
      throw new Error("Local config lacks the specified provider or keys.");
    }

    const reqBody = {
      model: "ark-code-latest",
      messages: [
        { role: "system", content: SYSTEM_PROMPT },
        { role: "user", content: "以下是原始会话：\n\n" + historyText },
      ],
      temperature: 0.3,
    };

    const res = await fetch(`${providerConfig.baseUrl}/chat/completions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${providerConfig.apiKey}`,
      },
      body: JSON.stringify(reqBody),
    });

    if (!res.ok) throw new Error(`API HTTP ${res.status}`);

    const json = await res.json();
    const aiSummary = json.choices?.[0]?.message?.content;
    if (!aiSummary) throw new Error("Empty AI response");

    const timeStr = `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;
    await fsPromises.mkdir(memoryDir, { recursive: true });

    let block = "";
    if (!existsSync(archiveFile)) {
      block += `# ${dateStr} 工作记忆\n\n`;
    }

    block += `---\n\n## 🧾 会话整理 - ${dateStr} ${timeStr}\n- Session ID: ${sessionId}\n\n${aiSummary}\n\n`;

    await fsPromises.appendFile(archiveFile, block, "utf8");
    console.log(`[session-memory-structured] summary saved for ${sessionId}.`);
  } catch (error) {
    console.error("[session-memory-structured] failed:", error instanceof Error ? error.message : String(error));
  }
};

module.exports = handler;
module.exports.default = handler;
