#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import { loadLocalEnv } from "../../notion-pipeline/scripts/local_env.mjs";

const INFRA_REPORT_PATH = "/Users/dellymac/.openclaw/workspace/reports/infrastructure-ideas.json";

function getNotionToken() {
  return process.env.OPENCLAW_NOTION_TOKEN || process.env.NOTION_TOKEN;
}

function getNotionVersion() {
  return process.env.OPENCLAW_NOTION_VERSION || "2022-06-28";
}

function getTimezone() {
  return process.env.OPENCLAW_TIMEZONE || "Europe/Istanbul";
}

function getAliasMap() {
  return {
    ideas: process.env.OPENCLAW_NOTION_DB_PROJECT_IDEAS,
    runs: process.env.OPENCLAW_NOTION_DB_NIGHTLY_RUNS,
  };
}

function usage() {
  console.error("usage: build_report.mjs <output.json>");
}

function todayInTimezone(tz) {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: tz,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(new Date());
}

function normalizeName(name) {
  return String(name || "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "");
}

function pickProperty(properties, names) {
  const wanted = new Set(names.map(normalizeName));
  for (const [name, value] of Object.entries(properties || {})) {
    if (wanted.has(normalizeName(name))) {
      return value;
    }
  }
  return null;
}

function titleFromProperty(prop) {
  if (!prop || prop.type !== "title") {
    return "";
  }
  return prop.title.map((item) => item.plain_text || "").join("").trim();
}

function richTextFromProperty(prop) {
  if (!prop) {
    return "";
  }
  if (prop.type === "rich_text") {
    return prop.rich_text.map((item) => item.plain_text || "").join("").trim();
  }
  if (prop.type === "title") {
    return titleFromProperty(prop);
  }
  if (prop.type === "select") {
    return prop.select?.name || "";
  }
  if (prop.type === "status") {
    return prop.status?.name || "";
  }
  if (prop.type === "url") {
    return prop.url || "";
  }
  if (prop.type === "number") {
    return prop.number == null ? "" : String(prop.number);
  }
  if (prop.type === "date") {
    return prop.date?.start || "";
  }
  if (prop.type === "formula") {
    return formulaToString(prop.formula);
  }
  return "";
}

function formulaToString(formula) {
  if (!formula) {
    return "";
  }
  if (formula.type === "string") {
    return formula.string || "";
  }
  if (formula.type === "number") {
    return formula.number == null ? "" : String(formula.number);
  }
  if (formula.type === "boolean") {
    return formula.boolean ? "true" : "false";
  }
  if (formula.type === "date") {
    return formula.date?.start || "";
  }
  return "";
}

function numberFromProperty(prop) {
  if (!prop) {
    return null;
  }
  if (prop.type === "number") {
    return prop.number;
  }
  if (prop.type === "formula" && prop.formula?.type === "number") {
    return prop.formula.number;
  }
  const text = richTextFromProperty(prop);
  if (!text) {
    return null;
  }
  const numeric = Number(text);
  return Number.isFinite(numeric) ? numeric : null;
}

function urlFromProperty(prop) {
  if (!prop) {
    return "";
  }
  if (prop.type === "url") {
    return prop.url || "";
  }
  return richTextFromProperty(prop);
}

function dateFromProperty(prop) {
  if (!prop) {
    return "";
  }
  if (prop.type === "date") {
    return prop.date?.start || "";
  }
  return richTextFromProperty(prop);
}

function checkboxFromProperty(prop) {
  if (!prop) {
    return null;
  }
  if (prop.type === "checkbox") {
    return prop.checkbox;
  }
  const text = richTextFromProperty(prop).toLowerCase();
  if (!text) {
    return null;
  }
  if (["true", "yes", "y", "1", "shortlisted"].includes(text)) {
    return true;
  }
  if (["false", "no", "n", "0", "rejected"].includes(text)) {
    return false;
  }
  return null;
}

async function notionRequest(pathname, body) {
  const notionToken = getNotionToken();
  if (!notionToken) {
    throw new Error("OPENCLAW_NOTION_TOKEN is missing");
  }
  const response = await fetch(`https://api.notion.com/v1${pathname}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${notionToken}`,
      "Notion-Version": getNotionVersion(),
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  const text = await response.text();
  const json = text ? JSON.parse(text) : {};
  if (!response.ok) {
    const error = new Error(`Notion request failed: ${response.status}`);
    error.details = json;
    throw error;
  }
  return json;
}

async function queryDatabase(databaseId, body) {
  return notionRequest(`/databases/${databaseId}/query`, body);
}

function extractRunSummary(page) {
  const properties = page.properties || {};
  const summaryProp = pickProperty(properties, [
    "summary",
    "run summary",
    "nightly summary",
    "overview",
    "notes",
  ]);
  const summary = richTextFromProperty(summaryProp);
  if (summary) {
    return summary;
  }

  const counts = [
    ["signals", ["signals", "research signals"]],
    ["archived", ["archived", "archived cards"]],
    ["ideas", ["ideas", "generated ideas"]],
    ["shortlisted", ["shortlisted", "shortlist count"]],
  ]
    .map(([label, names]) => {
      const value = numberFromProperty(pickProperty(properties, names));
      return value == null ? null : `${value} ${label}`;
    })
    .filter(Boolean);

  return counts.length > 0 ? counts.join(", ") : "Nightly run summary is not available yet.";
}

function extractIdea(page) {
  const properties = page.properties || {};
  const title =
    titleFromProperty(
      pickProperty(properties, ["idea title", "title", "name", "project idea"])
    ) ||
    page.properties?.Name?.title?.map((item) => item.plain_text || "").join("").trim() ||
    "Untitled idea";

  const score =
    numberFromProperty(pickProperty(properties, ["score total", "total score", "score"])) ?? 0;
  const rank =
    numberFromProperty(pickProperty(properties, ["rank", "shortlist rank"])) ?? Number.MAX_SAFE_INTEGER;
  const approvalState = richTextFromProperty(
    pickProperty(properties, ["approval state", "status", "shortlist status"])
  ).toLowerCase();
  const shortlistedFlag = checkboxFromProperty(
    pickProperty(properties, ["shortlisted", "is shortlisted"])
  );
  const reason =
    richTextFromProperty(
      pickProperty(properties, ["reason", "why now", "one liner", "summary", "rationale"])
    ) || "Shortlisted by nightly evaluator.";
  const batchDate = dateFromProperty(pickProperty(properties, ["batch date", "date", "run date"]));
  const ideaId =
    richTextFromProperty(pickProperty(properties, ["idea id", "id"])) ||
    page.id.replace(/-/g, "");

  return {
    id: ideaId,
    title,
    score: Math.round(score),
    rank,
    reason,
    notionUrl: page.url || urlFromProperty(pickProperty(properties, ["url", "notion url"])),
    approvalState,
    shortlistedFlag,
    batchDate,
  };
}

function isShortlisted(idea) {
  if (idea.shortlistedFlag === true) {
    return true;
  }
  if (idea.approvalState === "shortlisted") {
    return true;
  }
  if (idea.approvalState.includes("shortlist")) {
    return true;
  }
  return idea.approvalState === "selected";
}

function buildBlockedPayload(date, blocker) {
  return {
    date,
    summary: blocker.message,
    reportUrl: null,
    ideas: [],
    blocker,
  };
}

async function readJsonIfExists(file) {
  try {
    const raw = await fs.readFile(file, "utf8");
    return JSON.parse(raw);
  } catch (error) {
    if (error.code === "ENOENT") {
      return null;
    }
    throw error;
  }
}

async function writeOutput(file, payload) {
  await fs.mkdir(path.dirname(file), { recursive: true });
  await fs.writeFile(file, JSON.stringify(payload, null, 2) + "\n", "utf8");
}

async function main() {
  await loadLocalEnv();
  const [outputPath] = process.argv.slice(2);
  if (!outputPath) {
    usage();
    process.exit(1);
  }

  const aliasMap = getAliasMap();
  const notionToken = getNotionToken();
  const date = todayInTimezone(getTimezone());
  const missing = [];
  if (!notionToken) {
    missing.push("OPENCLAW_NOTION_TOKEN");
  }
  for (const [alias, value] of Object.entries(aliasMap)) {
    if (!value) {
      missing.push(alias === "ideas" ? "OPENCLAW_NOTION_DB_PROJECT_IDEAS" : "OPENCLAW_NOTION_DB_NIGHTLY_RUNS");
    }
  }

  if (missing.length > 0) {
    const payload = buildBlockedPayload(date, {
      code: "missing_env",
      message: `Nightly report build blocked: missing ${missing.join(", ")}`,
      missing,
    });
    await writeOutput(outputPath, payload);
    console.log(JSON.stringify({ ok: true, mode: "blocked", outputPath, missing }, null, 2));
    return;
  }

  try {
    const runResult = await queryDatabase(aliasMap.runs, {
      page_size: 5,
      sorts: [{ timestamp: "last_edited_time", direction: "descending" }],
    });

    const runs = runResult.results || [];
    const latestRun =
      runs.find((page) => {
        const runDate = dateFromProperty(
          pickProperty(page.properties || {}, ["date", "run date", "batch date"])
        );
        return runDate && runDate.startsWith(date);
      }) ||
      runs[0] ||
      null;
    const runDate = latestRun
      ? dateFromProperty(pickProperty(latestRun.properties || {}, ["date", "run date", "batch date"]))
      : "";
    const effectiveDate = runDate || date;
    const ideasResult = await queryDatabase(aliasMap.ideas, {
      page_size: 20,
      filter: {
        property: "Batch Date",
        date: { equals: effectiveDate },
      },
      sorts: [{ timestamp: "last_edited_time", direction: "descending" }],
    });

    const shortlistedIdeas = (ideasResult.results || [])
      .map(extractIdea)
      .filter((idea) => idea.batchDate && idea.batchDate.startsWith(effectiveDate))
      .filter(isShortlisted)
      .sort((left, right) => {
        if (left.rank !== right.rank) {
          return left.rank - right.rank;
        }
        return right.score - left.score;
      })
      .slice(0, 3)
      .map(({ rank, approvalState, shortlistedFlag, batchDate, ...idea }) => idea);

    const infraPayload = await readJsonIfExists(INFRA_REPORT_PATH);
    const infrastructureIdeas = Array.isArray(infraPayload?.ideas)
      ? infraPayload.ideas.slice(0, 3).map((idea) => ({
          title: idea.title || "Untitled infrastructure idea",
          reason: idea.reason || idea.one_liner || "Infrastructure-focused suggestion.",
          notionUrl: idea.notionUrl || idea.url || null,
          score: idea.score ?? null,
        }))
      : [];

    const payload = {
      date: effectiveDate,
      summary: latestRun ? extractRunSummary(latestRun) : "No Nightly Runs entry was found.",
      reportUrl: latestRun?.url || null,
      ideas: shortlistedIdeas,
      infrastructureIdeas,
    };
    await writeOutput(outputPath, payload);
    console.log(
      JSON.stringify(
        {
          ok: true,
          mode: "report",
          outputPath,
          ideas: shortlistedIdeas.length,
          hasRun: Boolean(latestRun),
        },
        null,
        2
      )
    );
  } catch (error) {
    const payload = buildBlockedPayload(date, {
      code: "notion_query_failed",
      message: `Nightly report build blocked: ${error.message}`,
    });
    await writeOutput(outputPath, payload);
    console.log(JSON.stringify({ ok: true, mode: "blocked", outputPath, error: error.message }, null, 2));
  }
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
