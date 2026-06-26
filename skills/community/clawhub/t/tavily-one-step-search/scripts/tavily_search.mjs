#!/usr/bin/env node
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const API_BASE = "https://api.tavily.com";

function loadKey() {
  if (process.env.TAVILY_API_KEY?.trim()) return process.env.TAVILY_API_KEY.trim();
  const envPath = path.join(os.homedir(), ".openclaw", ".env");
  if (!fs.existsSync(envPath)) return null;
  const txt = fs.readFileSync(envPath, "utf8");
  const m = txt.match(/^\s*TAVILY_API_KEY\s*=\s*(.+?)\s*$/m);
  if (!m) return null;
  return m[1].trim().replace(/^['"]|['"]$/g, "") || null;
}

function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith("--")) {
      out._.push(a);
      continue;
    }
    const k = a.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) out[k] = true;
    else {
      out[k] = next;
      i++;
    }
  }
  return out;
}

function splitCsv(v) {
  if (!v) return undefined;
  const arr = String(v).split(",").map((x) => x.trim()).filter(Boolean);
  return arr.length ? arr : undefined;
}

async function postJson(endpoint, payload, { timeout = 30, retries = 1 } = {}) {
  const key = loadKey();
  if (!key) throw new Error("Missing TAVILY_API_KEY (env or ~/.openclaw/.env)");

  const controller = new AbortController();
  let lastErr;
  const attempts = Math.max(1, Number(retries) + 1);
  for (let i = 0; i < attempts; i++) {
    const timer = setTimeout(() => controller.abort(), Math.max(5000, Number(timeout) * 1000));
    try {
      const res = await fetch(`${API_BASE}/${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
          "Authorization": `Bearer ${key}`,
        },
        body: JSON.stringify(payload),
        signal: controller.signal,
      });
      const txt = await res.text();
      if (!res.ok) {
        if ([429, 500, 502, 503, 504].includes(res.status) && i < attempts - 1) {
          await new Promise((r) => setTimeout(r, 1200 * (i + 1)));
          continue;
        }
        throw new Error(`HTTP ${res.status}: ${txt.slice(0, 400)}`);
      }
      return JSON.parse(txt);
    } catch (e) {
      lastErr = e;
      if (i < attempts - 1) await new Promise((r) => setTimeout(r, 1200 * (i + 1)));
    } finally {
      clearTimeout(timer);
    }
  }
  throw lastErr || new Error("Request failed");
}

function toBraveLike(raw, max = 400) {
  return {
    query: raw.query,
    ...(raw.answer ? { answer: raw.answer } : {}),
    results: (raw.results || []).map((r) => ({
      title: r.title,
      url: r.url,
      snippet: (r.content || "").length > max ? `${(r.content || "").slice(0, max).trim()}...` : (r.content || ""),
    })),
  };
}

function toMarkdownSearch(raw, max = 400) {
  const lines = [];
  if (raw.answer) lines.push(String(raw.answer).trim(), "");
  (raw.results || []).forEach((r, i) => {
    const title = (r.title || "").trim() || r.url || "(no title)";
    const snippet = (r.content || "").length > max ? `${(r.content || "").slice(0, max).trim()}...` : (r.content || "");
    lines.push(`${i + 1}. ${title}`);
    if (r.url) lines.push(`   ${r.url}`);
    if (snippet) lines.push(`   - ${snippet}`);
    lines.push("");
  });
  return `${lines.join("\n").trim()}\n`;
}

function toMarkdownGeneric(obj, limit = 20) {
  const lines = [];
  if (obj.base_url) lines.push(`Base URL: ${obj.base_url}`);
  if (obj.response_time != null) lines.push(`Response time: ${obj.response_time}s`);
  const results = Array.isArray(obj.results) ? obj.results : [];
  lines.push(`Results: ${results.length}`, "");
  results.slice(0, limit).forEach((r, i) => {
    const u = r.url || r.source_url || "";
    const t = r.title || u || `item-${i + 1}`;
    const c = (r.content || r.raw_content || "").toString();
    lines.push(`${i + 1}. ${t}`);
    if (u) lines.push(`   ${u}`);
    if (c) lines.push(`   - ${c.slice(0, 220)}${c.length > 220 ? "..." : ""}`);
    lines.push("");
  });
  return `${lines.join("\n").trim()}\n`;
}

async function run() {
  const args = parseArgs(process.argv.slice(2));
  const cmd = args._[0];
  if (!cmd || ["-h", "--help", "help"].includes(cmd)) {
    console.log("Usage: node tavily_search.mjs <search|extract|crawl|map> [--flags]");
    process.exit(0);
  }

  if (cmd === "search") {
    if (!args.query) throw new Error("--query is required for search");
    const payload = {
      query: args.query,
      max_results: Math.max(1, Math.min(20, Number(args["max-results"] || 5))),
      search_depth: args["search-depth"] || "basic",
      topic: args.topic || "general",
      include_answer: Boolean(args["include-answer"]),
      include_images: Boolean(args["include-images"]),
      include_image_descriptions: Boolean(args["include-image-descriptions"]),
      include_raw_content: Boolean(args["include-raw-content"]),
      include_favicon: Boolean(args["include-favicon"]),
      ...(splitCsv(args["include-domains"]) ? { include_domains: splitCsv(args["include-domains"]) } : {}),
      ...(splitCsv(args["exclude-domains"]) ? { exclude_domains: splitCsv(args["exclude-domains"]) } : {}),
      ...(args.country ? { country: args.country } : {}),
      ...(args["time-range"] ? { time_range: args["time-range"] } : {}),
      ...(args["start-date"] ? { start_date: args["start-date"] } : {}),
      ...(args["end-date"] ? { end_date: args["end-date"] } : {}),
      ...((args["search-depth"] || "basic") === "advanced"
        ? { chunks_per_source: Math.max(1, Math.min(3, Number(args["chunks-per-source"] || 3))) }
        : {}),
    };
    const obj = await postJson("search", payload, {
      timeout: Number(args.timeout || 30),
      retries: Number(args.retries || 1),
    });
    const raw = {
      query: args.query,
      ...(payload.include_answer ? { answer: obj.answer } : {}),
      results: (obj.results || []).slice(0, payload.max_results).map((r) => ({
        title: r.title,
        url: r.url,
        content: r.content,
        score: r.score,
      })),
    };

    const fmt = args.format || "brave";
    if (fmt === "md") {
      process.stdout.write(toMarkdownSearch(raw, Number(args["snippet-max-chars"] || 400)));
      return;
    }
    if (fmt === "brave") {
      process.stdout.write(`${JSON.stringify(toBraveLike(raw, Number(args["snippet-max-chars"] || 400)))}\n`);
      return;
    }
    process.stdout.write(`${JSON.stringify(raw)}\n`);
    return;
  }

  if (cmd === "extract") {
    if (!args.urls) throw new Error("--urls is required for extract");
    const urls = splitCsv(args.urls) || [];
    const payload = {
      urls: urls.length > 1 ? urls : urls[0],
      extract_depth: args["extract-depth"] || "basic",
      include_images: Boolean(args["include-images"]),
      include_favicon: Boolean(args["include-favicon"]),
      format: args["content-format"] || "markdown",
      ...(args.query ? { query: args.query, chunks_per_source: Math.max(1, Math.min(5, Number(args["chunks-per-source"] || 3))) } : {}),
    };
    const obj = await postJson("extract", payload, {
      timeout: Number(args.timeout || 30), retries: Number(args.retries || 1),
    });
    if ((args.format || "raw") === "md") process.stdout.write(toMarkdownGeneric(obj));
    else process.stdout.write(`${JSON.stringify(obj)}\n`);
    return;
  }

  if (cmd === "crawl" || cmd === "map") {
    if (!args.url) throw new Error(`--url is required for ${cmd}`);
    const payload = {
      url: args.url,
      max_depth: Math.max(1, Math.min(5, Number(args["max-depth"] || 1))),
      max_breadth: Math.max(1, Math.min(500, Number(args["max-breadth"] || 20))),
      limit: Math.max(1, Number(args.limit || 50)),
      allow_external: Boolean(args["allow-external"]),
      include_images: Boolean(args["include-images"]),
      ...(args.instructions ? { instructions: args.instructions } : {}),
      ...(splitCsv(args["select-paths"]) ? { select_paths: splitCsv(args["select-paths"]) } : {}),
      ...(splitCsv(args["exclude-paths"]) ? { exclude_paths: splitCsv(args["exclude-paths"]) } : {}),
      ...(splitCsv(args["select-domains"]) ? { select_domains: splitCsv(args["select-domains"]) } : {}),
      ...(splitCsv(args["exclude-domains"]) ? { exclude_domains: splitCsv(args["exclude-domains"]) } : {}),
      ...(cmd === "crawl"
        ? {
            extract_depth: args["extract-depth"] || "basic",
            format: args["content-format"] || "markdown",
            ...(args.instructions ? { chunks_per_source: Math.max(1, Math.min(5, Number(args["chunks-per-source"] || 3))) } : {}),
          }
        : {}),
    };
    const obj = await postJson(cmd, payload, {
      timeout: Number(args.timeout || 30), retries: Number(args.retries || 1),
    });
    if ((args.format || "raw") === "md") process.stdout.write(toMarkdownGeneric(obj, Number(args["md-limit"] || 20)));
    else process.stdout.write(`${JSON.stringify(obj)}\n`);
    return;
  }

  throw new Error(`Unknown command: ${cmd}`);
}

run().catch((e) => {
  console.error(e?.message || String(e));
  process.exit(2);
});
