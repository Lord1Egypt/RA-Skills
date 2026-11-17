/**
 * Topical platform webhooks → OpenClaw agent.
 * Handles topic_briefing (run bulletin) and topic_breaking_news (high-relevance alert).
 * Also accepts legacy types topic_digest and topic_event.
 *
 * Install: copy this file and topical.config.json into ~/.openclaw/hooks/transforms/
 * (see scripts/copy-transforms.sh in the topical-openclaw-setup skill).
 */

"use strict";

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const CONFIG_FILE = "topical.config.json";

const BRIEFING_TYPES = new Set(["topic_briefing", "topic_digest"]);
const ALERT_TYPES = new Set(["topic_breaking_news", "topic_event"]);
const EVENT_TYPES = new Set([...BRIEFING_TYPES, ...ALERT_TYPES]);
const MARKDOWN_LINK_RE = /\[([^\]]+)\]\(([^)]+)\)/g;

function mustObject(v, name) {
  if (!v || typeof v !== "object") throw new Error(`${name} must be an object`);
  return v;
}

function str(v, fallback = "") {
  if (v === undefined || v === null) return fallback;
  if (typeof v === "string") return v;
  return String(v);
}

function num(v, fallback = 0) {
  const n = Number(v);
  return Number.isFinite(n) ? n : fallback;
}

function arrayLength(v) {
  return Array.isArray(v) ? v.length : 0;
}

function loadTopicalConfig() {
  const configPath = path.join(__dirname, CONFIG_FILE);
  if (!fs.existsSync(configPath)) {
    throw new Error(
      `topical-inbound: missing ${CONFIG_FILE} in ${__dirname}. ` +
        "Copy topical.config.example.json from the Topical OpenClaw skill, rename it, and set agentId plus delivery channel.",
    );
  }

  const raw = JSON.parse(fs.readFileSync(configPath, "utf8"));
  mustObject(raw, CONFIG_FILE);

  const agentId = str(raw.agentId).trim();
  if (!agentId) {
    throw new Error(`topical-inbound: ${CONFIG_FILE} requires agentId`);
  }

  return {
    agentId,
    sessionKey: str(raw.sessionKey).trim() || `agent:${agentId}:main`,
    deliver: raw.deliver !== false,
    channel: str(raw.channel, "last").trim() || "last",
    to: str(raw.to).trim(),
    accountId: str(raw.accountId, "default").trim() || "default",
  };
}

/** @param {string} markdown */
function extractMarkdownLinks(markdown) {
  const links = [];
  const seen = new Set();
  let match;
  MARKDOWN_LINK_RE.lastIndex = 0;
  while ((match = MARKDOWN_LINK_RE.exec(markdown)) !== null) {
    const label = match[1].trim();
    const url = match[2].trim();
    if (!url || seen.has(url)) continue;
    seen.add(url);
    links.push({ label: label || url, url });
  }
  return links;
}

/** @param {{ label: string, url: string }[]} links */
function formatSourceLinks(links) {
  if (!links.length) return "";
  return [
    "",
    "Source links:",
    ...links.map((link, i) => `${i + 1}. ${link.label} — ${link.url}`),
  ].join("\n");
}

function parseSourceLinks(sources) {
  if (!Array.isArray(sources)) return [];
  const links = [];
  const seen = new Set();
  for (const source of sources) {
    if (!source || typeof source !== "object") continue;
    const url = str(source.url).trim();
    if (!url || seen.has(url)) continue;
    seen.add(url);
    links.push({
      label: str(source.title).trim() || url,
      url,
    });
  }
  return links;
}

function parseBriefingPayload(payload) {
  const markdown = str(payload.markdown);
  if (!markdown) {
    throw new Error("topical-inbound: topic_briefing requires markdown");
  }

  const breakingNewsCount =
    arrayLength(payload.breakingNews) ||
    arrayLength(payload.events) ||
    num(payload.eventCount);
  const signalCount = arrayLength(payload.signals) || num(payload.signalCount);
  const trendCount = arrayLength(payload.trends) || num(payload.trendCount);

  return {
    kind: "briefing",
    subscriptionId: str(payload.subscriptionId),
    topicId: str(payload.topicId),
    name: str(payload.name) || str(payload.topicId),
    deliveredAt: str(payload.deliveredAt),
    since: str(payload.since),
    markdown,
    breakingNewsCount,
    signalCount,
    trendCount,
    links: extractMarkdownLinks(markdown),
  };
}

function parseAlertPayload(payload) {
  const title = str(payload.title);
  const summary = str(payload.summary);
  if (!title && !summary) {
    throw new Error(
      "topical-inbound: topic_breaking_news requires at least title or summary",
    );
  }

  return {
    kind: "alert",
    subscriptionId: str(payload.subscriptionId),
    topicId: str(payload.topicId),
    alertId: str(payload.breakingNewsId) || str(payload.eventId),
    deliveredAt: str(payload.deliveredAt),
    title,
    summary,
    relevanceScore: num(payload.relevanceScore),
    relevanceReason: str(payload.relevanceReason),
    links: parseSourceLinks(payload.sources),
  };
}

function parseTopicalPayload(ctx) {
  mustObject(ctx, "ctx");

  const payload =
    ctx.payload && typeof ctx.payload === "object" ? ctx.payload : ctx;

  const type = str(payload.type);
  if (!EVENT_TYPES.has(type)) {
    throw new Error(
      `topical-inbound: expected type "topic_briefing", "topic_breaking_news", "topic_digest", or "topic_event", got "${type || "(missing)"}"`,
    );
  }

  if (BRIEFING_TYPES.has(type)) {
    return parseBriefingPayload(payload);
  }

  return parseAlertPayload(payload);
}

function formatBriefingStats(event) {
  const parts = [];
  if (event.breakingNewsCount) {
    parts.push(
      `${event.breakingNewsCount} breaking news item${event.breakingNewsCount === 1 ? "" : "s"}`,
    );
  }
  if (event.signalCount) {
    parts.push(`${event.signalCount} signal${event.signalCount === 1 ? "" : "s"}`);
  }
  if (event.trendCount) {
    parts.push(`${event.trendCount} trend${event.trendCount === 1 ? "" : "s"}`);
  }
  return parts.length ? ` (${parts.join(", ")})` : "";
}

/** @param {ReturnType<typeof loadTopicalConfig>} config */
function deliveryFooter(config) {
  const lines = [
    "",
    "OpenClaw delivers your reply automatically when deliver=true — do not use the message tool unless the runtime requires it.",
  ];

  if (config.channel === "telegram" && config.to) {
    lines.push(
      `If the runtime forces the message tool: target "${config.to}", channel "telegram", accountId "${config.accountId}" (never target "${config.agentId}" — that is the bot account name, not a chat id).`,
    );
  }

  return lines.join("\n");
}

/** @param {ReturnType<typeof parseTopicalPayload>} event @param {ReturnType<typeof loadTopicalConfig>} config */
function buildAgentMessage(event, config) {
  const telegramFooter = deliveryFooter(config);

  if (event.kind === "briefing") {
    const stats = formatBriefingStats(event);

    const digestFooter = [
      "",
      "Delivery instructions:",
      "- Relay the Topical bulletin above to the user with minimal changes. It is already curated — preserve its wording, paragraph structure, and inline source links.",
      "- Do not rewrite, summarize, bulletize, or restructure it into new sections (no \"Key developments\", \"Thoughts\", etc.).",
      "- Do not add commentary, opinions, or analysis for its own sake.",
      "- Only add a brief note (1–2 sentences) when something in the bulletin is clearly relevant to your existing memory or knowledge about this user — otherwise skip commentary entirely.",
      "- Do not ask follow-up questions or offer tasks unless the user has asked for that pattern before.",
      telegramFooter,
    ].join("\n");

    return [
      "New Topical intelligence briefing.",
      "",
      `The user monitors "${event.name}" in Topical. Below is their latest briefing from a completed pipeline run${stats}.`,
      event.since ? `Covers activity since ${event.since}.` : "",
      "",
      "--- BEGIN TOPICAL BRIEFING ---",
      event.markdown,
      "--- END TOPICAL BRIEFING ---",
      digestFooter,
    ]
      .filter((line) => line !== "")
      .join("\n");
  }

  const eventFooter = [
    "",
    "Share this development with the user. Offer the source links so they can read more.",
    "Take any follow-up actions you think they might want based on this news.",
    telegramFooter,
  ].join("\n");

  const relevance =
    event.relevanceScore > 0
      ? `Relevance score: ${event.relevanceScore}${event.relevanceReason ? ` — ${event.relevanceReason}` : ""}.`
      : "";

  return [
    "New Topical breaking news alert.",
    "",
    `The user monitors topic "${event.topicId}" in Topical. A high-relevance development matched their topic.`,
    relevance,
    "",
    event.title,
    event.summary && event.summary !== event.title ? event.summary : "",
    formatSourceLinks(event.links),
    eventFooter,
  ]
    .filter(Boolean)
    .join("\n");
}

/**
 * @param {unknown} ctx
 * @returns {Promise<object>}
 */
export async function topicalInbound(ctx) {
  const config = loadTopicalConfig();
  const event = parseTopicalPayload(ctx);

  const action = {
    kind: "agent",
    agentId: config.agentId,
    sessionKey: config.sessionKey,
    message: buildAgentMessage(event, config),
    deliver: config.deliver,
    channel: config.channel,
    wakeMode: "now",
    allowUnsafeExternalContent: false,
  };

  if (config.to) {
    action.to = config.to;
  }
  if (config.accountId && config.channel === "telegram") {
    action.accountId = config.accountId;
  }

  return action;
}

export default topicalInbound;
