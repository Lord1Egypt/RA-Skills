import { promises as fs } from "node:fs";
import { join, relative, resolve } from "node:path";

// ---------------------------------------------------------------------------
// Defaults
// ---------------------------------------------------------------------------
const DEFAULT_PROTOCOL_DIRS = ["memory/protocols"];
const DEFAULT_SKILLS_DIRS = ["skills"];
const DEFAULT_TOOLS_FILES = ["TOOLS.md"];
const DEFAULT_MAX_RESULTS = 3;
const DEFAULT_MIN_PROMPT_LENGTH = 20;
const DEFAULT_OLLAMA_BASE_URL = "http://localhost:11434";
const DEFAULT_EMBED_MODEL = "nomic-embed-text:latest";
const DEFAULT_REQUEST_TIMEOUT_MS = 10_000;
const DEFAULT_MIN_SCORE = 0.3;
const DEFAULT_MAX_DOC_LINES = 100; // token burn mitigation
const DOC_CACHE_TTL_MS = 60 * 60 * 1000; // 1 hour
const MAX_SESSION_CACHE = 100;

// Files to skip — generic meta/audit/eval docs that usually aren't actionable runtime skills
const SKIP_FILENAME_PATTERNS = [
  /(^|[-_.])audit([-_.]|$)/i,
  /(^|[-_.])eval(uation)?([-_.]|$)/i,
  /^protocols[-_.]hub\.md$/i,
];

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------
function resolveConfig(rawConfig) {
  const raw = rawConfig && typeof rawConfig === "object" ? rawConfig : {};
  return {
    protocolDirs: Array.isArray(raw.protocolDirs) ? raw.protocolDirs : DEFAULT_PROTOCOL_DIRS,
    skillsDirs: Array.isArray(raw.skillsDirs) ? raw.skillsDirs : DEFAULT_SKILLS_DIRS,
    toolsFiles: Array.isArray(raw.toolsFiles) ? raw.toolsFiles : DEFAULT_TOOLS_FILES,
    pinnedDocs: Array.isArray(raw.pinnedDocs) ? raw.pinnedDocs : [],
    maxResults: typeof raw.maxResults === "number" ? raw.maxResults : DEFAULT_MAX_RESULTS,
    maxDocLines: typeof raw.maxDocLines === "number" ? raw.maxDocLines : DEFAULT_MAX_DOC_LINES,
    ollamaBaseUrl: raw.ollamaBaseUrl?.trim() || DEFAULT_OLLAMA_BASE_URL,
    embedModel: raw.embedModel?.trim() || DEFAULT_EMBED_MODEL,
    minPromptLength:
      typeof raw.minPromptLength === "number" ? raw.minPromptLength : DEFAULT_MIN_PROMPT_LENGTH,
    requestTimeoutMs:
      typeof raw.requestTimeoutMs === "number"
        ? raw.requestTimeoutMs
        : DEFAULT_REQUEST_TIMEOUT_MS,
    minScore: typeof raw.minScore === "number" ? raw.minScore : DEFAULT_MIN_SCORE,
  };
}

function isLocalOllamaBaseUrl(value) {
  if (!value || typeof value !== "string") return false;
  try {
    const url = new URL(value);
    return ["localhost", "127.0.0.1", "::1"].includes(url.hostname);
  } catch {
    return false;
  }
}

// ---------------------------------------------------------------------------
// Doc extraction — title + description from markdown
// ---------------------------------------------------------------------------
function extractDocMeta(content, relPath) {
  const fmMatch = content.match(/^---\s*\n([\s\S]*?)\n---/);
  let name = null;
  let description = null;
  let status = null;

  if (fmMatch) {
    const fm = fmMatch[1];
    const nameMatch = fm.match(/^name:\s*["']?(.+?)["']?\s*$/m);
    const descMatch = fm.match(/^description:\s*["']?([\s\S]+?)["']?\s*$/m);
    const statusMatch = fm.match(/^status:\s*["']?(.+?)["']?\s*$/m);
    if (nameMatch) name = nameMatch[1].trim();
    if (descMatch) description = descMatch[1].trim().replace(/\n\s*/g, " ").slice(0, 400);
    if (statusMatch) status = statusMatch[1].trim().toLowerCase();
  }

  if (!name) {
    const headingMatch = content.match(/^#\s+(.+)$/m);
    name = headingMatch
      ? headingMatch[1].trim()
      : relPath.split("/").pop().replace(/\.md$/, "");
  }

  if (!description) {
    const body = content.replace(/^---[\s\S]*?---\s*/, "").split("\n");
    const lines = [];
    for (const line of body) {
      if (line.startsWith("#") || line.startsWith("---")) continue;
      const t = line.trim();
      if (t) lines.push(t);
      if (lines.length >= 4) break;
    }
    description = lines.join(" ").slice(0, 400);
  }

  return { name, description, status };
}

function shouldSkip(filename) {
  return SKIP_FILENAME_PATTERNS.some((pattern) => pattern.test(filename));
}

function isDeprecated(status) {
  return status === "deprecated" || status === "archived";
}

// ---------------------------------------------------------------------------
// Content truncation
// ---------------------------------------------------------------------------
function truncateContent(content, maxLines) {
  if (!maxLines || maxLines <= 0) return content;
  const lines = content.split("\n");
  if (lines.length <= maxLines) return content;
  return lines.slice(0, maxLines).join("\n") + "\n\n… (truncated)";
}

// ---------------------------------------------------------------------------
// Doc collection — recursive
// ---------------------------------------------------------------------------
async function collectMdFiles(absDir, workspaceDir, source, docs, depth = 0) {
  const MAX_DEPTH = 1;
  let entries;
  try {
    entries = await fs.readdir(absDir, { withFileTypes: true });
  } catch {
    return;
  }

  for (const entry of entries) {
    if (entry.isDirectory() && depth < MAX_DEPTH) {
      await collectMdFiles(join(absDir, entry.name), workspaceDir, source, docs, depth + 1);
    } else if (entry.isFile() && entry.name.endsWith(".md")) {
      if (shouldSkip(entry.name)) continue;
      const absPath = join(absDir, entry.name);
      const content = await fs.readFile(absPath, "utf-8");
      const relPath = relative(workspaceDir, absPath);
      const { name, description, status } = extractDocMeta(content, relPath);
      if (isDeprecated(status)) continue;
      docs.push({ source, title: name, description, relPath, absPath, content });
    }
  }
}

async function collectFromProtocolDir(workspaceDir, relDir) {
  const absDir = resolve(workspaceDir, relDir);
  const docs = [];
  await collectMdFiles(absDir, workspaceDir, "protocol", docs);
  return docs;
}

async function collectFromSkillsDir(workspaceDir, relDir) {
  const absDir = resolve(workspaceDir, relDir);
  const docs = [];
  try {
    const entries = await fs.readdir(absDir, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.isDirectory()) {
        // Check for SKILL.md first
        const skillFile = join(absDir, entry.name, "SKILL.md");
        try {
          const content = await fs.readFile(skillFile, "utf-8");
          const relPath = relative(workspaceDir, skillFile);
          const { name, description, status } = extractDocMeta(content, relPath);
          if (!isDeprecated(status))
            docs.push({ source: "skill", title: name, description, relPath, absPath: skillFile, content });
        } catch {
          // No SKILL.md — recurse for loose .md files
          await collectMdFiles(join(absDir, entry.name), workspaceDir, "skill", docs);
        }
      } else if (entry.isFile() && entry.name.endsWith(".md")) {
        if (shouldSkip(entry.name)) continue;
        const absPath = join(absDir, entry.name);
        const content = await fs.readFile(absPath, "utf-8");
        const relPath = relative(workspaceDir, absPath);
        const { name, description, status } = extractDocMeta(content, relPath);
        if (isDeprecated(status)) continue;
        docs.push({ source: "skill", title: name, description, relPath, absPath, content });
      }
    }
  } catch {
    // Dir doesn't exist — skip silently
  }
  return docs;
}

async function collectAllDocs(workspaceDir, cfg) {
  const docs = [];
  for (const dir of cfg.protocolDirs) {
    docs.push(...(await collectFromProtocolDir(workspaceDir, dir)));
  }
  for (const dir of cfg.skillsDirs) {
    docs.push(...(await collectFromSkillsDir(workspaceDir, dir)));
  }
  for (const file of cfg.toolsFiles) {
    const absPath = resolve(workspaceDir, file);
    try {
      const content = await fs.readFile(absPath, "utf-8");
      const relPath = relative(workspaceDir, absPath);
      const { name, description } = extractDocMeta(content, relPath);
      docs.push({ source: "tools", title: name, description, relPath, absPath, content });
    } catch {
      // File doesn't exist — skip silently
    }
  }
  return docs;
}

// ---------------------------------------------------------------------------
// Pinned docs — always injected regardless of score
// ---------------------------------------------------------------------------
async function loadPinnedDocs(workspaceDir, pinnedPaths) {
  const docs = [];
  for (const relPath of pinnedPaths) {
    const absPath = resolve(workspaceDir, relPath);
    try {
      const content = await fs.readFile(absPath, "utf-8");
      const { name, description } = extractDocMeta(content, relPath);
      docs.push({ source: "pinned", title: name, description, relPath, absPath, content });
    } catch {
      // Pinned file missing — skip silently
    }
  }
  return docs;
}

// ---------------------------------------------------------------------------
// Embeddings via nomic-embed-text (Ollama) — free, local, no API calls
// ---------------------------------------------------------------------------
function cosineSimilarity(a, b) {
  let dot = 0, normA = 0, normB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  const denom = Math.sqrt(normA) * Math.sqrt(normB);
  return denom === 0 ? 0 : dot / denom;
}

async function embedText(text, cfg) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), cfg.requestTimeoutMs);
  try {
    const response = await fetch(`${cfg.ollamaBaseUrl}/api/embed`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model: cfg.embedModel, input: text }),
      signal: controller.signal,
    });
    if (!response.ok) throw new Error(`embed error: ${response.status}`);
    const data = await response.json();
    return data.embeddings?.[0] ?? null;
  } catch {
    return null;
  } finally {
    clearTimeout(timer);
  }
}

function docEmbedInput(doc) {
  const body = doc.content
    .replace(/^---[\s\S]*?---\s*/, "")
    .replace(/^#+\s+.*/gm, "")
    .replace(/\[\[.*?\]\]/g, "")
    .trim()
    .slice(0, 800);
  const input = `${doc.title}: ${doc.description || ""} ${body}`.trim();
  return `search_document: ${input}`;
}

async function rankDocs(prompt, docs, cfg, logger) {
  const promptWithPrefix = `search_query: ${prompt.slice(0, 1000)}`;
  const promptEmbedding = await embedText(promptWithPrefix, cfg);
  if (!promptEmbedding) {
    logger?.warn?.("skill-preflight: ollama embedding unavailable, falling back to first N docs");
    return docs.slice(0, cfg.maxResults);
  }

  // Embed docs — use cached _embedding if available
  const scored = await Promise.all(
    docs.map(async (doc) => {
      if (!doc._embedding) {
        doc._embedding = await embedText(docEmbedInput(doc), cfg);
      }
      const score = doc._embedding ? cosineSimilarity(promptEmbedding, doc._embedding) : 0;
      return { doc, score };
    })
  );

  // Score transparency — log top 5 at debug level
  const top5 = [...scored]
    .sort((a, b) => b.score - a.score)
    .slice(0, 5)
    .map(({ doc, score }) => `${doc.title}(${score.toFixed(2)})`)
    .join(", ");
  logger?.debug?.(`skill-preflight: scores — ${top5}`);

  return scored
    .sort((a, b) => b.score - a.score)
    .filter(({ score }) => score >= cfg.minScore)
    .slice(0, cfg.maxResults)
    .map(({ doc }) => doc);
}

// ---------------------------------------------------------------------------
// Format injected context block
// ---------------------------------------------------------------------------
function formatContext(matched, cfg) {
  if (matched.length === 0) return null;
  const sections = matched
    .map((doc, i) => {
      const label = `[${i + 1}/${matched.length}] ${doc.title}  ·  ${doc.relPath}`;
      const content = truncateContent(doc.content.trim(), cfg.maxDocLines);
      return `### ${label}\n\n${content}`;
    })
    .join("\n\n---\n\n");
  return `<relevant_skills>\n## Procedures to Execute for This Task\n\nThe following protocols and skills define HOW to do this task. Follow these steps — do not improvise or skip steps unless you have a specific reason.\n\n${sections}\n</relevant_skills>`;
}

// ---------------------------------------------------------------------------
// Plugin
// ---------------------------------------------------------------------------
const skillPreflightPlugin = {
  id: "skill-preflight",
  name: "Skill Preflight",
  description:
    "Injects relevant skills and protocols into agent context using Ollama embeddings (nomic-embed-text). No external embedding API is required when Ollama is local. Supports pinned docs, recursive scanning, and session deduplication.",

  register(api) {
    const cfg = resolveConfig(api.pluginConfig);
    let workspaceDir = null;

    // Doc cache with TTL
    let cachedDocs = null;
    let cacheExpiresAt = 0;

    // Session deduplication: sessionId -> Set<relPath>
    const sessionInjected = new Map();

    api.registerService({
      id: "skill-preflight-init",
      async start(ctx) {
        workspaceDir = ctx.workspaceDir || process.cwd();
        api.logger.info?.(
          `skill-preflight: ready (embed=${cfg.embedModel}, maxResults=${cfg.maxResults}, minScore=${cfg.minScore}, maxDocLines=${cfg.maxDocLines || "unlimited"}, pinned=${cfg.pinnedDocs.length})`
        );
        if (!isLocalOllamaBaseUrl(cfg.ollamaBaseUrl)) {
          api.logger.warn?.(
            `skill-preflight: ollamaBaseUrl is non-local (${cfg.ollamaBaseUrl}). Prompt text and indexed doc content will be sent to that host for embeddings. Use localhost/127.0.0.1/[::1] if you want local-only processing.`
          );
        }
      },
    });

    api.on("before_prompt_build", async (event, ctx) => {
      // Only run preflight on user-initiated prompts — skip heartbeats, crons,
      // overflow, and other internal triggers to avoid wasting tokens.
      const trigger = ctx?.trigger;
      if (trigger && trigger !== "user") {
        api.logger.debug?.(`skill-preflight: skipping non-user trigger "${trigger}"`);
        return;
      }

      const prompt = event.prompt || "";
      if (prompt.length < cfg.minPromptLength) return;

      const ws = workspaceDir || ctx.workspaceDir || process.cwd();

      // Session deduplication
      const sessionId = event.sessionId || event.sessionKey || event.runId || "global";
      if (!sessionInjected.has(sessionId)) {
        if (sessionInjected.size >= MAX_SESSION_CACHE) {
          const oldest = sessionInjected.keys().next().value;
          sessionInjected.delete(oldest);
        }
        sessionInjected.set(sessionId, new Set());
      }
      const alreadyInjected = sessionInjected.get(sessionId);

      try {
        // Refresh doc cache if stale
        const now = Date.now();
        if (!cachedDocs || now > cacheExpiresAt) {
          cachedDocs = await collectAllDocs(ws, cfg);
          cacheExpiresAt = now + DOC_CACHE_TTL_MS;
          api.logger.debug?.(`skill-preflight: loaded ${cachedDocs.length} docs`);
        }

        // Load pinned docs
        const pinnedDocs = await loadPinnedDocs(ws, cfg.pinnedDocs);
        const newPinned = pinnedDocs.filter((d) => !alreadyInjected.has(d.relPath));

        if (cachedDocs.length === 0 && newPinned.length === 0) return;

        // Rank non-pinned docs
        const matched = cachedDocs.length > 0
          ? await rankDocs(prompt, cachedDocs, cfg, api.logger)
          : [];

        // Filter already-injected
        const newRanked = matched.filter((d) => !alreadyInjected.has(d.relPath));

        const toInject = [...newPinned, ...newRanked];
        if (toInject.length === 0) {
          api.logger.debug?.("skill-preflight: all relevant docs already injected this session");
          return;
        }

        toInject.forEach((d) => alreadyInjected.add(d.relPath));

        const pinnedContext = formatContext(newPinned, cfg);
        const rankedContext = formatContext(newRanked, cfg);
        if (!pinnedContext && !rankedContext) return;

        const pinnedNote = newPinned.length ? ` (${newPinned.length} pinned)` : "";
        api.logger.info?.(
          `skill-preflight: injecting ${toInject.length} doc(s)${pinnedNote}: ${toInject.map((d) => d.title).join(", ")}`
        );

        const result = {};
        if (pinnedContext) result.prependSystemContext = pinnedContext;
        if (rankedContext) result.prependContext = rankedContext;
        return result;
      } catch (err) {
        api.logger.warn?.(`skill-preflight: ${String(err)}`);
      }
    });
  },
};

export default skillPreflightPlugin;
