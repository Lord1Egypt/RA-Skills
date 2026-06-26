#!/usr/bin/env node
/**
 * Parse AI coding assistant session JSONL files into readable Markdown transcripts.
 *
 * Supports: Claude Code, Codex (OpenAI), OpenCode, and generic JSONL chat formats.
 *
 * Usage:
 *   # Parse all sessions for a project (auto-discovers JSONL files):
 *   node parse_session.js --project-dir /path/to/project
 *
 *   # Parse a single JSONL file:
 *   node parse_session.js /path/to/session.jsonl
 *
 * Outputs Markdown to stdout. Redirect to a file as needed.
 */

const fs = require("fs");
const path = require("path");
const os = require("os");

const FULL_DETAIL_SESSIONS = 5;
const MAX_SUMMARY_TURNS = 10;

function extractTextFromContent(content) {
  if (typeof content === "string") return content.trim();
  if (!Array.isArray(content)) return "";

  const parts = [];
  for (const block of content) {
    if (!block || typeof block !== "object") continue;
    const btype = block.type || "";

    if (btype === "text") {
      parts.push(block.text.trim());
    } else if (btype === "tool_use") {
      const name = block.name || "unknown";
      const inp = block.input || {};
      if (["Read", "Glob", "Grep", "read_file", "grep", "glob"].includes(name)) {
        const target = inp.file_path || inp.pattern || inp.path || "";
        parts.push(`[Tool: ${name}(${target})]`);
      } else if (["Bash", "shell", "run_command"].includes(name)) {
        let cmd = inp.command || "";
        if (cmd.length > 200) cmd = cmd.slice(0, 200) + "...";
        parts.push(`[Tool: ${name}] ${cmd}`);
      } else if (["Write", "Edit", "write_file", "edit_file"].includes(name)) {
        parts.push(`[Tool: ${name}(${inp.file_path || ""})]`);
      } else if (["Agent", "spawn_agent"].includes(name)) {
        const desc = (inp.description || inp.prompt || "").slice(0, 100);
        parts.push(`[Tool: Agent(${desc})]`);
      } else {
        parts.push(`[Tool: ${name}]`);
      }
    } else if (btype === "tool_result") {
      const rc = block.content || "";
      if (typeof rc === "string" && rc.trim()) {
        let text = rc.trim();
        if (text.length > 300) text = text.slice(0, 300) + "... [truncated]";
        parts.push(`[Tool Result] ${text}`);
      } else if (Array.isArray(rc)) {
        for (const sub of rc) {
          if (sub && sub.type === "text") {
            let text = sub.text.trim();
            if (text.length > 300) text = text.slice(0, 300) + "... [truncated]";
            parts.push(`[Tool Result] ${text}`);
          }
        }
      }
    } else if (btype === "function_call") {
      parts.push(`[Function: ${block.name || "unknown"}]`);
    }
    // Skip "thinking" blocks
  }
  return parts.join("\n");
}

function detectFormat(obj) {
  if (obj.type && ["user", "assistant", "system", "file-history-snapshot"].includes(obj.type)) {
    return "claude-code";
  }
  if (obj.role && obj.content !== undefined) return "openai";
  return "unknown";
}

function parseClaudeCode(lines) {
  const exchanges = [];
  for (const line of lines) {
    let obj;
    try { obj = JSON.parse(line); } catch { continue; }

    const msgType = obj.type || "";
    if (["file-history-snapshot", "attachment"].includes(msgType)) continue;
    if (obj.isMeta) continue;

    if (msgType === "user") {
      const content = (obj.message || {}).content || "";
      const text = extractTextFromContent(content);
      if (text && text.includes("<command-name>")) continue;
      if (text && !text.startsWith("[Tool Result]")) {
        exchanges.push(["user", text]);
      } else if (text) {
        exchanges.push(["tool_result", text]);
      }
    } else if (msgType === "assistant") {
      const content = (obj.message || {}).content || [];
      const text = extractTextFromContent(content);
      if (text) exchanges.push(["assistant", text]);
    } else if (msgType === "system") {
      const content = (obj.content || "").trim();
      if (content.length > 10) {
        const subtype = obj.subtype || "";
        if (subtype !== "local_command") {
          exchanges.push(["system", content.slice(0, 500)]);
        }
      }
    }
  }
  return exchanges;
}

function parseOpenAIFormat(lines) {
  const exchanges = [];
  for (const line of lines) {
    let obj;
    try { obj = JSON.parse(line); } catch { continue; }

    const role = obj.role || "";
    const text = extractTextFromContent(obj.content || "");
    if (!text) continue;

    if (["user", "human"].includes(role)) {
      exchanges.push(["user", text]);
    } else if (["assistant", "model"].includes(role)) {
      exchanges.push(["assistant", text]);
    } else if (role === "system" && text.length > 10) {
      exchanges.push(["system", text.slice(0, 500)]);
    } else if (role === "tool" && text.length > 10) {
      exchanges.push(["tool_result", text.slice(0, 300)]);
    }
  }
  return exchanges;
}

function parseSingleFile(filePath) {
  const lines = fs.readFileSync(filePath, "utf-8").trim().split("\n");

  let fmt = "unknown";
  for (const line of lines) {
    try {
      const obj = JSON.parse(line);
      fmt = detectFormat(obj);
      if (fmt !== "unknown") break;
    } catch { continue; }
  }

  if (fmt === "claude-code") return parseClaudeCode(lines);
  if (fmt === "openai") return parseOpenAIFormat(lines);

  const cc = parseClaudeCode(lines);
  const oai = parseOpenAIFormat(lines);
  return cc.length >= oai.length ? cc : oai;
}

function summarizeExchanges(exchanges) {
  const summary = [];
  let count = 0;
  for (const [role, text] of exchanges) {
    if (role === "user") {
      count++;
      if (count > MAX_SUMMARY_TURNS) {
        summary.push(["user", `... [${count}+ more user turns omitted] ...`]);
        break;
      }
      summary.push(["user", text.length > 300 ? text.slice(0, 300) + "... [truncated]" : text]);
    }
  }
  return summary;
}

function buildMarkdownMulti(sessionList) {
  const output = ["# Project Session Transcripts\n"];
  const total = sessionList.length;
  const fullStart = Math.max(0, total - FULL_DETAIL_SESSIONS);

  for (let i = 0; i < sessionList.length; i++) {
    const { file, mtime, exchanges } = sessionList[i];
    if (!exchanges.length) continue;

    const sessionNum = i + 1;
    const dateStr = new Date(mtime).toISOString().replace("T", " ").slice(0, 16);
    const sessionId = path.basename(file, ".jsonl").slice(0, 8);

    output.push("---\n");
    output.push(`## Session ${sessionNum} (${dateStr}, id: ${sessionId}...)\n`);

    if (i < fullStart) {
      const userCount = exchanges.filter(([r]) => r === "user").length;
      output.push(`*[Summary — ${userCount} user turns]*\n`);
      for (const [role, text] of summarizeExchanges(exchanges)) {
        if (role === "user") output.push(`- **User**: ${text.slice(0, 200)}`);
      }
      output.push("");
    } else {
      let turnNum = 0;
      for (const [role, text] of exchanges) {
        if (role === "user") {
          turnNum++;
          output.push(`### Turn ${turnNum} — User\n`);
          output.push(text, "");
        } else if (role === "assistant") {
          output.push("#### Assistant Response\n");
          output.push(text, "");
        } else if (role === "tool_result") {
          output.push(`> ${text.slice(0, 200)}`, "");
        } else if (role === "system") {
          output.push(`*[System: ${text.slice(0, 200)}]*`, "");
        }
      }
    }
  }
  return output.join("\n");
}

function findProjectSessions(projectDir) {
  projectDir = fs.realpathSync(projectDir);
  const sessions = [];

  // Claude Code: ~/.claude/projects/<encoded-path>/*.jsonl
  const claudeHome = path.join(os.homedir(), ".claude", "projects");
  if (fs.existsSync(claudeHome)) {
    const encoded = "-" + projectDir.replace(/^\//,"").replace(/\//g, "-");
    const projectPath = path.join(claudeHome, encoded);
    if (fs.existsSync(projectPath)) {
      for (const f of fs.readdirSync(projectPath)) {
        if (!f.endsWith(".jsonl")) continue;
        const full = path.join(projectPath, f);
        // Skip subagent logs (only top-level files)
        if (fs.statSync(full).isFile()) {
          sessions.push({ file: full, mtime: fs.statSync(full).mtimeMs });
        }
      }
    }
  }

  // Codex: ~/.codex/sessions/*.jsonl
  const codexPath = path.join(os.homedir(), ".codex", "sessions");
  if (fs.existsSync(codexPath)) {
    for (const f of fs.readdirSync(codexPath)) {
      if (!f.endsWith(".jsonl")) continue;
      const full = path.join(codexPath, f);
      if (fs.statSync(full).isFile()) {
        sessions.push({ file: full, mtime: fs.statSync(full).mtimeMs });
      }
    }
  }

  // OpenCode: platform-dependent
  const ocPath = process.platform === "darwin"
    ? path.join(os.homedir(), "Library", "Application Support", "opencode", "sessions")
    : path.join(os.homedir(), ".local", "share", "opencode", "sessions");
  if (fs.existsSync(ocPath)) {
    for (const f of fs.readdirSync(ocPath)) {
      if (!f.endsWith(".jsonl")) continue;
      const full = path.join(ocPath, f);
      if (fs.statSync(full).isFile()) {
        sessions.push({ file: full, mtime: fs.statSync(full).mtimeMs });
      }
    }
  }

  sessions.sort((a, b) => a.mtime - b.mtime);
  return sessions;
}

function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.error("Usage:");
    console.error("  node parse_session.js --project-dir /path/to/project");
    console.error("  node parse_session.js /path/to/session.jsonl");
    process.exit(1);
  }

  if (args[0] === "--project-dir") {
    const projectDir = args[1];
    if (!projectDir || !fs.existsSync(projectDir) || !fs.statSync(projectDir).isDirectory()) {
      console.error(`Error: ${projectDir || "(missing)"} is not a directory`);
      process.exit(1);
    }

    const sessions = findProjectSessions(projectDir);
    if (!sessions.length) {
      console.error(`Error: No session files found for project ${projectDir}`);
      console.error("Searched in ~/.claude/projects/, ~/.codex/sessions/, and opencode sessions");
      process.exit(1);
    }

    console.error(`Found ${sessions.length} session(s)`);

    const sessionData = [];
    for (const { file, mtime } of sessions) {
      const exchanges = parseSingleFile(file);
      if (exchanges.length) sessionData.push({ file, mtime, exchanges });
    }

    if (!sessionData.length) {
      console.error("Error: All session files were empty or unparseable");
      process.exit(1);
    }

    console.error(`Parsed ${sessionData.length} non-empty session(s)`);
    console.log(buildMarkdownMulti(sessionData));

  } else {
    const filePath = args[0];
    if (!fs.existsSync(filePath)) {
      console.error(`Error: ${filePath} not found`);
      process.exit(1);
    }

    const exchanges = parseSingleFile(filePath);
    const output = ["# Session Transcript\n"];
    let turnNum = 0;
    for (const [role, text] of exchanges) {
      if (role === "user") {
        turnNum++;
        output.push(`## Turn ${turnNum} — User\n`, text, "");
      } else if (role === "assistant") {
        output.push("### Assistant Response\n", text, "");
      } else if (role === "tool_result") {
        output.push(`> ${text.slice(0, 200)}`, "");
      } else if (role === "system") {
        output.push(`*[System: ${text.slice(0, 200)}]*`, "");
      }
    }
    console.log(output.join("\n"));
  }
}

main();
