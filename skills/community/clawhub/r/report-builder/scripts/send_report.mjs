#!/usr/bin/env node

import fs from "node:fs/promises";
import { spawn } from "node:child_process";
import { loadLocalEnv } from "../../notion-pipeline/scripts/local_env.mjs";

async function readJson(file) {
  const raw = file === "-" ? await readStdin() : await fs.readFile(file, "utf8");
  return JSON.parse(raw);
}

async function readStdin() {
  let data = "";
  for await (const chunk of process.stdin) {
    data += chunk;
  }
  return data;
}

function buildMessage(report) {
  const lines = [];
  lines.push(`Gece Vardiyasi Raporu - ${report.date || "bugun"}`);
  if (report.summary) {
    lines.push("");
    lines.push(report.summary);
  }
  if (report.blocker?.message) {
    lines.push("");
    lines.push(report.blocker.message);
  }
  if (Array.isArray(report.ideas) && report.ideas.length > 0) {
    lines.push("");
    report.ideas.slice(0, 3).forEach((idea, index) => {
      lines.push(`${index + 1}. ${idea.title} - ${idea.score}/100`);
      if (idea.reason) {
        lines.push(`   ${idea.reason}`);
      }
      if (idea.notionUrl) {
        lines.push(`   ${idea.notionUrl}`);
      }
    });
  } else {
    lines.push("");
    lines.push(report.blocker?.message ? "Rapor blokeli, fikir listesi hazir degil." : "Bu sabah esigi gecen fikir yok.");
  }
  if (Array.isArray(report.infrastructureIdeas) && report.infrastructureIdeas.length > 0) {
    lines.push("");
    lines.push("Infra fikirleri:");
    report.infrastructureIdeas.slice(0, 3).forEach((idea, index) => {
      const scoreText = idea.score == null ? "" : ` - ${idea.score}/100`;
      lines.push(`I${index + 1}. ${idea.title}${scoreText}`);
      if (idea.reason) {
        lines.push(`   ${idea.reason}`);
      }
      if (idea.notionUrl) {
        lines.push(`   ${idea.notionUrl}`);
      }
    });
  }
  if (report.reportUrl) {
    lines.push("");
    lines.push(`Detay: ${report.reportUrl}`);
  }
  return lines.join("\n");
}

function buildButtons(report) {
  if (!Array.isArray(report.ideas) || report.ideas.length === 0) {
    return [];
  }
  return report.ideas.slice(0, 3).map((idea, index) => [
    { text: `Approve ${index + 1}`, callback_data: `approve:${idea.id}` },
    { text: `Reject ${index + 1}`, callback_data: `reject:${idea.id}` },
    { text: `Later ${index + 1}`, callback_data: `later:${idea.id}` },
  ]);
}

function parseJsonMaybe(value) {
  if (!value || !String(value).trim()) {
    return null;
  }
  try {
    return JSON.parse(value);
  } catch {
    return null;
  }
}

function extractMessageId(payload) {
  if (!payload || typeof payload !== "object") {
    return "";
  }
  const candidates = [
    payload.messageId,
    payload.message_id,
    payload.id,
    payload.result?.messageId,
    payload.result?.message_id,
    payload.result?.id,
    payload.message?.messageId,
    payload.message?.message_id,
    payload.message?.id,
    payload.delivery?.messageId,
    payload.delivery?.message_id,
    payload.delivery?.id,
    payload.payload?.messageId,
    payload.payload?.message_id,
    payload.payload?.id,
  ];
  return String(candidates.find((candidate) => candidate != null) || "").trim();
}

function runOpenClaw(args) {
  return new Promise((resolve, reject) => {
    const child = spawn("openclaw", args, {
      stdio: ["ignore", "pipe", "pipe"],
      env: process.env,
    });
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (chunk) => {
      stdout += chunk;
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk;
    });
    child.on("close", (code) => {
      if (code === 0) {
        resolve({ stdout, stderr });
        return;
      }
      reject(new Error(stderr.trim() || stdout.trim() || `openclaw failed (${code})`));
    });
  });
}

function runProcessWithInput(command, args, input) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, {
      stdio: ["pipe", "pipe", "pipe"],
      env: process.env,
    });
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (chunk) => {
      stdout += chunk;
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk;
    });
    child.on("close", (code) => {
      if (code === 0) {
        resolve({ stdout, stderr });
        return;
      }
      reject(new Error(stderr.trim() || stdout.trim() || `openclaw failed (${code})`));
    });
    child.stdin.end(input);
  });
}

async function main() {
  await loadLocalEnv();
  const args = process.argv.slice(2);
  const dryRun = args.includes("--dry-run");
  const filtered = args.filter((arg) => arg !== "--dry-run");
  const [file, targetArg] = filtered;
  if (!file) {
    throw new Error("usage: send_report.mjs <report.json|-> [telegramTarget] [--dry-run]");
  }
  const report = await readJson(file);
  const target = targetArg || process.env.OPENCLAW_TELEGRAM_TARGET;
  if (!target) {
    throw new Error("OPENCLAW_TELEGRAM_TARGET is missing");
  }
  const commandArgs = [
    "message",
    "send",
    "--channel",
    "telegram",
    "--target",
    String(target),
    "--message",
    buildMessage(report),
    "--json",
  ];
  if (dryRun) {
    commandArgs.push("--dry-run");
  }
  const buttons = buildButtons(report);
  if (buttons.length > 0) {
    commandArgs.push("--buttons", JSON.stringify(buttons));
  }
  const result = await runOpenClaw(commandArgs);
  const delivery = parseJsonMaybe(result.stdout);
  const messageId = dryRun ? "" : extractMessageId(delivery);
  if (messageId) {
    const auditPayload = {
      date: report.date,
      telegram_message_id: messageId,
      idea_ids: Array.isArray(report.ideas) ? report.ideas.map((idea) => idea.id).filter(Boolean) : [],
    };
    await runProcessWithInput(
      "node",
      [
        "/Users/dellymac/.openclaw/skills/notion-pipeline/scripts/factory_ops.mjs",
        "record-report-delivery",
        "-",
      ],
      JSON.stringify(auditPayload)
    );
  }
  process.stdout.write(result.stdout || "");
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
