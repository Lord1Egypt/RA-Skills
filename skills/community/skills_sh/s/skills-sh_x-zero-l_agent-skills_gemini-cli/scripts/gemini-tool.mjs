#!/usr/bin/env node
import { spawn } from "node:child_process";
import { createHash } from "node:crypto";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";

const DEFAULT_MODEL = "gemini-3-pro-preview";
const FLASH_FALLBACK_MODEL = "gemini-3-flash-preview";
const CHANGE_MODE_MAX_CHARS_PER_CHUNK = 20_000;

const CACHE_DIR = path.join(os.tmpdir(), "gemini-cli-skill-chunks");
const CACHE_TTL_MS = 10 * 60 * 1000; // 10 minutes
const MAX_CACHE_FILES = 50;

function printUsage() {
  const cmd = "node scripts/gemini-tool.mjs";
  process.stdout.write(`
Gemini CLI helper (no MCP).

Usage:
  ${cmd} ask --prompt "<text|@file>" [--cwd <dir>] [--model <id>] [--sandbox] [--changeMode]
  ${cmd} brainstorm --prompt "<challenge>" [--model <id>] [--methodology <auto|divergent|convergent|scamper|design-thinking|lateral>] [--ideaCount 12] [--includeAnalysis true|false]
  ${cmd} fetch-chunk --cacheKey <key> --chunkIndex <n>
  ${cmd} help
  ${cmd} ping [--message "hi"]
  ${cmd} timeout-test --duration 30000
`);
}

function toCamelCaseFlag(flagName) {
  return flagName.replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());
}

function coerceValue(raw) {
  if (raw === undefined) return true;
  if (raw === "true") return true;
  if (raw === "false") return false;
  if (/^-?\d+(\.\d+)?$/.test(raw)) return Number(raw);
  return raw;
}

function parseArgs(argv) {
  const result = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const current = argv[i];
    if (!current.startsWith("--")) {
      result._.push(current);
      continue;
    }

    const eqIndex = current.indexOf("=");
    if (eqIndex !== -1) {
      const rawKey = current.slice(2, eqIndex);
      const key = toCamelCaseFlag(rawKey);
      const value = current.slice(eqIndex + 1);
      result[key] = coerceValue(value);
      continue;
    }

    const rawKey = current.slice(2);
    const key = toCamelCaseFlag(rawKey);
    const next = argv[i + 1];
    if (next === undefined || next.startsWith("--")) {
      result[key] = true;
      continue;
    }
    result[key] = coerceValue(next);
    i++;
  }
  return result;
}

async function runCommand(command, args, { env, cwd } = {}) {
  return await new Promise((resolve, reject) => {
    const child = spawn(command, args, {
      stdio: ["ignore", "pipe", "pipe"],
      cwd,
      env: {
        ...process.env,
        NODE_NO_WARNINGS: "1",
        ...env,
      },
    });

    let stdout = "";
    let stderr = "";

    child.stdout.on("data", (chunk) => {
      stdout += chunk.toString("utf8");
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString("utf8");
    });

    child.on("error", reject);
    child.on("close", (code) => {
      if (code === 0) return resolve({ stdout, stderr });
      const combined = `${stderr}${stderr && stdout ? "\n" : ""}${stdout}`.trim();
      reject(
        new Error(
          combined || `Command failed with exit code ${code}: ${command} ${args.join(" ")}`,
        ),
      );
    });
  });
}

async function runGemini(prompt, { model, sandbox, cwd } = {}) {
  const args = [];
  if (model) args.push("-m", model);
  if (sandbox) args.push("-s");
  args.push(prompt);

  try {
    const { stdout } = await runCommand("gemini", args, { cwd });
    return stdout.trimEnd();
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    const isQuota = message.includes("Quota exceeded for quota metric");
    if (isQuota && model && model !== FLASH_FALLBACK_MODEL) {
      const { stdout } = await runCommand("gemini", [
        "-m",
        FLASH_FALLBACK_MODEL,
        ...(sandbox ? ["-s"] : []),
        prompt,
      ], { cwd });
      return stdout.trimEnd();
    }
    throw error;
  }
}

function buildChangeModePrompt(userPrompt) {
  const processed = userPrompt.replace(/file:(\S+)/g, "@$1");
  return `
[CHANGEMODE INSTRUCTIONS]
You are generating code modifications that will be processed by an automated system. The output format is critical.

INSTRUCTIONS:
1. Analyze each provided file thoroughly
2. Identify locations requiring changes based on the user request
3. For each change, output in the exact format specified
4. The OLD section must be EXACTLY what appears in the file (copy-paste exact match)
5. Provide complete, directly replacing code blocks

CRITICAL REQUIREMENTS:
1. Output edits in the EXACT format specified below - no deviations
2. The OLD string MUST be findable with Ctrl+F - it must be a unique, exact match
3. Include enough surrounding lines to make the OLD string unique
4. Copy the OLD content EXACTLY as it appears - including all whitespace, indentation, line breaks

OUTPUT FORMAT (follow exactly):
**FILE: [filename]:[line_number]**
\`\`\`
OLD:
[exact code to be replaced - must match file content precisely]
NEW:
[new code to insert - complete and functional]
\`\`\`

USER REQUEST:
${processed}
`.trim();
}

function parseChangeModeOutput(geminiResponse) {
  const edits = [];
  const markdownPattern =
    /\*\*FILE:\s*(.+?):(\d+)\*\*\s*\n```\s*\nOLD:\s*\n([\s\S]*?)\nNEW:\s*\n([\s\S]*?)\n```/g;

  let match;
  while ((match = markdownPattern.exec(geminiResponse)) !== null) {
    const [, filename, startLineStr, oldCodeRaw, newCodeRaw] = match;

    const oldCode = oldCodeRaw.trimEnd();
    const newCode = newCodeRaw.trimEnd();
    const startLine = Number.parseInt(startLineStr, 10);

    const oldLineCount = oldCode === "" ? 0 : oldCode.split("\n").length;
    const newLineCount = newCode === "" ? 0 : newCode.split("\n").length;

    const oldEndLine = startLine + (oldLineCount > 0 ? oldLineCount - 1 : 0);
    const newStartLine = startLine;
    const newEndLine = newStartLine + (newLineCount > 0 ? newLineCount - 1 : 0);

    edits.push({
      filename: filename.trim(),
      oldStartLine: startLine,
      oldEndLine,
      oldCode,
      newStartLine,
      newEndLine,
      newCode,
    });
  }

  return edits;
}

function validateChangeModeEdits(edits) {
  const errors = [];
  for (const edit of edits) {
    if (!edit.filename) errors.push("Edit missing filename");
    if (edit.oldStartLine > edit.oldEndLine) {
      errors.push(
        `Invalid line range for ${edit.filename}: ${edit.oldStartLine} > ${edit.oldEndLine}`,
      );
    }
    if (edit.newStartLine > edit.newEndLine) {
      errors.push(
        `Invalid new line range for ${edit.filename}: ${edit.newStartLine} > ${edit.newEndLine}`,
      );
    }
    if (!edit.oldCode && !edit.newCode) errors.push(`Empty edit for ${edit.filename}`);
  }
  return { valid: errors.length === 0, errors };
}

function estimateEditSize(edit) {
  const jsonOverhead = 250;
  const contentSize = edit.filename.length * 2 + edit.oldCode.length + edit.newCode.length;
  return jsonOverhead + contentSize;
}

function groupEditsByFile(edits) {
  const groups = new Map();
  for (const edit of edits) {
    const fileEdits = groups.get(edit.filename) ?? [];
    fileEdits.push(edit);
    groups.set(edit.filename, fileEdits);
  }
  return groups;
}

function chunkChangeModeEdits(edits, maxCharsPerChunk = CHANGE_MODE_MAX_CHARS_PER_CHUNK) {
  if (edits.length === 0) {
    return [
      {
        edits: [],
        chunkIndex: 1,
        totalChunks: 1,
        hasMore: false,
        estimatedChars: 0,
      },
    ];
  }

  const chunks = [];
  const fileGroups = groupEditsByFile(edits);
  let currentChunk = [];
  let currentSize = 0;

  for (const [, fileEdits] of fileGroups) {
    const fileSize = fileEdits.reduce((sum, edit) => sum + estimateEditSize(edit), 0);

    if (fileSize > maxCharsPerChunk) {
      if (currentChunk.length > 0) {
        chunks.push({ edits: currentChunk, estimatedChars: currentSize });
        currentChunk = [];
        currentSize = 0;
      }

      for (const edit of fileEdits) {
        const editSize = estimateEditSize(edit);
        if (currentSize + editSize > maxCharsPerChunk && currentChunk.length > 0) {
          chunks.push({ edits: currentChunk, estimatedChars: currentSize });
          currentChunk = [];
          currentSize = 0;
        }
        currentChunk.push(edit);
        currentSize += editSize;
      }
      continue;
    }

    if (currentSize + fileSize > maxCharsPerChunk && currentChunk.length > 0) {
      chunks.push({ edits: currentChunk, estimatedChars: currentSize });
      currentChunk = [];
      currentSize = 0;
    }

    currentChunk.push(...fileEdits);
    currentSize += fileSize;
  }

  if (currentChunk.length > 0) {
    chunks.push({ edits: currentChunk, estimatedChars: currentSize });
  }

  const totalChunks = chunks.length;
  return chunks.map((chunk, index) => ({
    ...chunk,
    chunkIndex: index + 1,
    totalChunks,
    hasMore: index < totalChunks - 1,
  }));
}

function formatChangeModeResponse(edits, chunkInfo) {
  const header =
    chunkInfo && chunkInfo.total > 1
      ? `[CHANGEMODE OUTPUT - Chunk ${chunkInfo.current} of ${chunkInfo.total}]
This chunk contains ${edits.length} edit${edits.length === 1 ? "" : "s"}.
`
      : `[CHANGEMODE OUTPUT]
Edits: ${edits.length}
`;

  const body = edits
    .map(
      (edit, index) => `### Edit ${index + 1}: ${edit.filename}

OLD:
\`\`\`
${edit.oldCode}
\`\`\`

NEW:
\`\`\`
${edit.newCode}
\`\`\`
`,
    )
    .join("\n");

  let footer = `---
Apply edits in order. OLD must match file contents exactly.`;

  if (chunkInfo && chunkInfo.current < chunkInfo.total && chunkInfo.cacheKey) {
    footer += `

Next chunk:
  node scripts/gemini-tool.mjs fetch-chunk --cacheKey ${chunkInfo.cacheKey} --chunkIndex ${chunkInfo.current + 1}
`;
  }

  return `${header}\n${body}\n${footer}`.trimEnd();
}

function summarizeChangeModeEdits(edits, isPartialView) {
  const fileCounts = new Map();
  for (const edit of edits) {
    fileCounts.set(edit.filename, (fileCounts.get(edit.filename) ?? 0) + 1);
  }

  const lines = Array.from(fileCounts.entries())
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([file, count]) => `- ${file}: ${count} edit${count === 1 ? "" : "s"}`)
    .join("\n");

  return `${isPartialView ? "ChangeMode Summary (all chunks):" : "ChangeMode Summary:"}
Total edits: ${edits.length}${isPartialView ? " (across all chunks)" : ""}
Files affected: ${fileCounts.size}

${lines}`.trimEnd();
}

function ensureCacheDir() {
  if (!fs.existsSync(CACHE_DIR)) fs.mkdirSync(CACHE_DIR, { recursive: true });
}

function cleanExpiredFiles() {
  try {
    ensureCacheDir();
    const now = Date.now();
    for (const name of fs.readdirSync(CACHE_DIR)) {
      if (!name.endsWith(".json")) continue;
      const filePath = path.join(CACHE_DIR, name);
      const stats = fs.statSync(filePath);
      if (now - stats.mtimeMs > CACHE_TTL_MS) fs.unlinkSync(filePath);
    }
  } catch {
    // non-critical
  }
}

function enforceFileLimits() {
  try {
    ensureCacheDir();
    const files = fs
      .readdirSync(CACHE_DIR)
      .filter((f) => f.endsWith(".json"))
      .map((name) => {
        const filePath = path.join(CACHE_DIR, name);
        return { name, filePath, mtimeMs: fs.statSync(filePath).mtimeMs };
      })
      .sort((a, b) => a.mtimeMs - b.mtimeMs);

    if (files.length <= MAX_CACHE_FILES) return;
    const toRemove = files.slice(0, files.length - MAX_CACHE_FILES);
    for (const file of toRemove) {
      try {
        fs.unlinkSync(file.filePath);
      } catch {
        // ignore
      }
    }
  } catch {
    // non-critical
  }
}

function cacheChunks(prompt, chunks) {
  ensureCacheDir();
  cleanExpiredFiles();

  const promptHash = createHash("sha256").update(prompt).digest("hex");
  const cacheKey = promptHash.slice(0, 8);
  const filePath = path.join(CACHE_DIR, `${cacheKey}.json`);

  const data = { chunks, timestamp: Date.now(), promptHash };
  fs.writeFileSync(filePath, JSON.stringify(data));
  enforceFileLimits();

  return cacheKey;
}

function getChunks(cacheKey) {
  const filePath = path.join(CACHE_DIR, `${cacheKey}.json`);
  try {
    if (!fs.existsSync(filePath)) return null;
    const data = JSON.parse(fs.readFileSync(filePath, "utf8"));
    if (Date.now() - data.timestamp > CACHE_TTL_MS) {
      fs.unlinkSync(filePath);
      return null;
    }
    return data.chunks;
  } catch {
    try {
      fs.unlinkSync(filePath);
    } catch {
      // ignore
    }
    return null;
  }
}

function processChangeModeOutput(rawResult, { chunkIndex, chunkCacheKey, prompt }) {
  if (chunkIndex && chunkCacheKey) {
    const cached = getChunks(String(chunkCacheKey));
    if (cached && chunkIndex >= 1 && chunkIndex <= cached.length) {
      const chunk = cached[chunkIndex - 1];
      const result = formatChangeModeResponse(chunk.edits, {
        current: chunkIndex,
        total: cached.length,
        cacheKey: chunkCacheKey,
      });
      const summary =
        chunkIndex === 1 && cached.length > 1
          ? summarizeChangeModeEdits(cached.flatMap((c) => c.edits), true) + "\n\n"
          : "";
      return `${summary}${result}`.trimEnd();
    }
  }

  const edits = parseChangeModeOutput(rawResult);
  if (edits.length === 0) {
    return `No edits found in Gemini output. Raw response:\n\n${rawResult}`.trimEnd();
  }

  const validation = validateChangeModeEdits(edits);
  if (!validation.valid) {
    return `Edit validation failed:\n${validation.errors.join("\n")}`.trimEnd();
  }

  const chunks = chunkChangeModeEdits(edits);
  const returnChunkIndex =
    chunkIndex && chunkIndex >= 1 && chunkIndex <= chunks.length ? chunkIndex : 1;
  const returnChunk = chunks[returnChunkIndex - 1];

  let cacheKey;
  if (chunks.length > 1 && prompt) cacheKey = cacheChunks(prompt, chunks);

  const summary =
    returnChunkIndex === 1 && edits.length > 5
      ? summarizeChangeModeEdits(edits, chunks.length > 1) + "\n\n"
      : "";

  const response = formatChangeModeResponse(
    returnChunk.edits,
    chunks.length > 1 ? { current: returnChunkIndex, total: chunks.length, cacheKey } : undefined,
  );

  return `${summary}${response}`.trimEnd();
}

function getMethodologyInstructions(methodology, domain) {
  const byMethod = {
    divergent: `**Divergent Thinking Approach:**
- Generate maximum quantity of ideas without self-censoring
- Build on wild ideas
- Combine unrelated concepts
- Postpone evaluation until the end`,
    convergent: `**Convergent Thinking Approach:**
- Refine and synthesize
- Apply critical evaluation
- Prioritize by feasibility and impact
- Outline implementation for top ideas`,
    scamper: `**SCAMPER Creative Triggers:**
- Substitute
- Combine
- Adapt
- Modify
- Put to other use
- Eliminate
- Reverse`,
    "design-thinking": `**Human-Centered Design Thinking:**
- Empathize
- Define
- Ideate
- Consider end-to-end journey
- Prototype mindset`,
    lateral: `**Lateral Thinking Approach:**
- Challenge assumptions
- Make unexpected connections
- Use metaphors and analogies`,
    auto: `**AI-Optimized Approach:**
${domain ? `Given the ${domain} domain,` : "I"} will combine divergent exploration, SCAMPER triggers, and human-centered evaluation.`,
  };
  return byMethod[methodology] ?? byMethod.auto;
}

function buildBrainstormPrompt({
  prompt,
  methodology,
  domain,
  constraints,
  existingContext,
  ideaCount,
  includeAnalysis,
}) {
  const framework = getMethodologyInstructions(methodology, domain);
  return `# BRAINSTORMING SESSION

## Core Challenge
${prompt}

## Methodology Framework
${framework}

## Context Engineering
${domain ? `**Domain Focus:** ${domain}` : ""}
${constraints ? `**Constraints & Boundaries:** ${constraints}` : ""}
${existingContext ? `**Background Context:** ${existingContext}` : ""}

## Output Requirements
- Generate ${ideaCount} distinct, creative ideas
- Each idea should be unique and non-obvious
- Focus on actionable, implementable concepts
- Use clear, descriptive naming
- Provide brief explanations for each idea

${includeAnalysis ? `## Analysis Framework
For each idea, provide:
- **Feasibility:** (1-5)
- **Impact:** (1-5)
- **Innovation:** (1-5)
- **Quick Assessment:** one sentence` : ""}

## Format
### Idea [N]: [Creative Name]
**Description:** [2-3 sentences]
${includeAnalysis ? "**Feasibility:** [1-5] | **Impact:** [1-5] | **Innovation:** [1-5]\n**Assessment:** [one sentence]" : ""}

Begin brainstorming session:`.trim();
}

async function cmdAsk(opts) {
  const prompt = String(opts.prompt ?? opts._?.join(" ") ?? "").trim();
  if (!prompt) throw new Error("Missing --prompt");

  const model = opts.model ? String(opts.model) : undefined;
  const sandbox = Boolean(opts.sandbox);
  const changeMode = Boolean(opts.changeMode);
  const cwd = opts.cwd ? String(opts.cwd) : undefined;

  const chunkIndex = opts.chunkIndex ? Number(opts.chunkIndex) : undefined;
  const chunkCacheKey = opts.chunkCacheKey ? String(opts.chunkCacheKey) : undefined;

  if (changeMode && chunkIndex && chunkCacheKey) {
    return processChangeModeOutput("", { chunkIndex, chunkCacheKey, prompt });
  }

  const finalPrompt = changeMode ? buildChangeModePrompt(prompt) : prompt;
  const output = await runGemini(finalPrompt, { model: model ?? DEFAULT_MODEL, sandbox, cwd });
  if (!changeMode) return output;

  return processChangeModeOutput(output, { chunkIndex, prompt });
}

async function cmdBrainstorm(opts) {
  const prompt = String(opts.prompt ?? opts._?.join(" ") ?? "").trim();
  if (!prompt) throw new Error("Missing --prompt");

  const model = opts.model ? String(opts.model) : DEFAULT_MODEL;
  const methodology = opts.methodology ? String(opts.methodology) : "auto";
  const domain = opts.domain ? String(opts.domain) : undefined;
  const constraints = opts.constraints ? String(opts.constraints) : undefined;
  const existingContext = opts.existingContext ? String(opts.existingContext) : undefined;
  const ideaCount = opts.ideaCount ? Number(opts.ideaCount) : 12;
  const includeAnalysis = opts.includeAnalysis === undefined ? true : Boolean(opts.includeAnalysis);
  const cwd = opts.cwd ? String(opts.cwd) : undefined;

  const brainstormPrompt = buildBrainstormPrompt({
    prompt,
    methodology,
    domain,
    constraints,
    existingContext,
    ideaCount,
    includeAnalysis,
  });

  return await runGemini(brainstormPrompt, { model, sandbox: false, cwd });
}

async function cmdFetchChunk(opts) {
  const cacheKey = opts.cacheKey ? String(opts.cacheKey) : undefined;
  const chunkIndex = opts.chunkIndex ? Number(opts.chunkIndex) : undefined;
  if (!cacheKey || !chunkIndex) throw new Error("Missing --cacheKey or --chunkIndex");

  const chunks = getChunks(cacheKey);
  if (!chunks) {
    return `Cache miss: "${cacheKey}" (expired after ${Math.round(CACHE_TTL_MS / 60000)} minutes). Re-run changeMode.`;
  }
  if (chunkIndex < 1 || chunkIndex > chunks.length) {
    return `Invalid chunkIndex ${chunkIndex}. Available: 1..${chunks.length}`;
  }

  const chunk = chunks[chunkIndex - 1];
  const summary =
    chunkIndex === 1 && chunks.length > 1
      ? summarizeChangeModeEdits(chunks.flatMap((c) => c.edits), true) + "\n\n"
      : "";

  return (
    summary +
    formatChangeModeResponse(chunk.edits, { current: chunkIndex, total: chunks.length, cacheKey })
  ).trimEnd();
}

async function cmdHelp() {
  const { stdout } = await runCommand("gemini", ["--help"]);
  return stdout.trimEnd();
}

async function cmdPing(opts) {
  const message = opts.message ? String(opts.message) : "Pong!";
  return message;
}

async function cmdTimeoutTest(opts) {
  const duration = opts.duration ? Number(opts.duration) : undefined;
  if (!duration || !Number.isFinite(duration) || duration < 10) {
    throw new Error("Invalid --duration (minimum 10ms)");
  }

  const steps = Math.max(1, Math.ceil(duration / 5000));
  const stepDuration = Math.ceil(duration / steps);
  const start = Date.now();

  const lines = [`Starting timeout test for ${duration}ms (${Math.round(duration / 1000)}s)`];
  for (let i = 1; i <= steps; i++) {
    await new Promise((resolve) => setTimeout(resolve, stepDuration));
    const elapsed = Date.now() - start;
    lines.push(`Step ${i}/${steps} - elapsed ${Math.round(elapsed / 1000)}s`);
  }
  lines.push("Timeout test completed.");
  return lines.join("\n");
}

async function main() {
  const argv = process.argv.slice(2);
  const command = argv[0];

  if (!command || command === "-h" || command === "--help") {
    printUsage();
    process.exit(0);
  }

  const opts = parseArgs(argv.slice(1));

  const handlers = {
    ask: cmdAsk,
    "ask-gemini": cmdAsk,
    brainstorm: cmdBrainstorm,
    "fetch-chunk": cmdFetchChunk,
    help: cmdHelp,
    ping: cmdPing,
    "timeout-test": cmdTimeoutTest,
  };

  const handler = handlers[command];
  if (!handler) {
    printUsage();
    throw new Error(`Unknown command: ${command}`);
  }

  const output = await handler(opts);
  process.stdout.write(`${output}\n`);
}

main().catch((error) => {
  const message = error instanceof Error ? error.message : String(error);
  process.stderr.write(`${message}\n`);
  process.exit(1);
});
