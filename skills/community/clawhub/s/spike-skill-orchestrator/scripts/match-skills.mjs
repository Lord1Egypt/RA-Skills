#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import process from "node:process";

const ROOT = "/Users/spikescp/.openclaw/workspace";
const REGISTRY_PATH = path.join(ROOT, "ops/skills/registry.json");
const ROUTER_PATH = path.join(ROOT, "ops/skills/trigger-router.json");
const STOP_TOKENS = new Set([
  "帮我",
  "一下",
  "这个",
  "那个",
  "什么",
  "怎么",
  "如何",
  "今天",
  "最近",
  "一下子",
  "有没有",
  "相关",
  "一下吧",
  "please",
  "with",
  "what",
  "how",
]);

const SKILL_ALIASES = {
  "frontend-design-3": ["落地页", "landing page", "页面", "首页", "官网", "web ui", "ui设计"],
  "impeccable-uxui": ["ui", "ux", "界面", "视觉", "排版", "设计"],
  "ui": ["界面", "页面", "ui", "组件"],
  "icons": ["图标", "icon"],
  "humanizer": ["小红书", "文案", "润色", "口语化", "去ai味"],
  "caveman-compress": ["压缩文案", "缩短", "精简"],
  "citation-fixer": ["引用", "来源", "citation"],
  "report-ui": ["看板", "dashboard", "报告页", "汇报页"],
  "smart-search": ["搜索", "调研", "查找", "research"],
  "local-deep-research": ["深度研究", "深挖", "research"],
  "aihot": ["ai资讯", "ai新闻", "ai日报", "今天 ai"],
  "github-trending": ["github", "开源", "trending", "开源榜", "热门仓库"],
  "trendradar": ["小红书", "爆款", "趋势", "trending", "热榜"],
};

const SCENARIO_ALIASES = {
  "UI/设计": ["落地页", "landing page", "页面", "首页", "ui", "设计", "官网"],
  "内容": ["小红书", "文案", "内容", "脚本", "改写", "润色", "发布"],
  "搜索/研究": ["搜索", "研究", "调研", "查找", "分析"],
  "深度研究": ["深度研究", "深入分析", "研究报告"],
  "写代码/修bug": ["修bug", "修复", "报错", "写代码", "编码", "开发"],
};

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf-8"));
}

function normalize(text) {
  return String(text || "")
    .toLowerCase()
    .replace(/[`"'“”‘’()[\]{}:,.!?/\\|<>+=_*#~-]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function tokenize(text) {
  const normalized = normalize(text);
  const english = normalized
    .split(" ")
    .map((token) => token.trim())
    .filter((token) => token.length >= 2);
  const chinese = (normalized.match(/[\u4e00-\u9fff]{2,}/g) || []).flatMap((chunk) => {
    const grams = [];
    for (let i = 0; i < chunk.length - 1; i += 1) {
      const gram = chunk.slice(i, i + 2);
      if (!STOP_TOKENS.has(gram)) grams.push(gram);
    }
    if (!STOP_TOKENS.has(chunk)) grams.push(chunk);
    return grams;
  });
  return unique([...english, ...chinese]).filter((token) => !STOP_TOKENS.has(token));
}

function scoreField(query, queryTokens, rawText, baseWeight, reasons, label) {
  if (!rawText) return 0;
  const text = normalize(rawText);
  if (!text) return 0;

  let score = 0;
  if (text.includes(query)) {
    score += baseWeight * 3;
    reasons.push(`${label}:全文命中`);
  }

  let matchedTokens = 0;
  for (const token of queryTokens) {
    if (token.length < 2) continue;
    if (text.includes(token)) matchedTokens += 1;
  }
  if (matchedTokens > 0) {
    score += matchedTokens * baseWeight;
    reasons.push(`${label}:词命中${matchedTokens}`);
  }

  return score;
}

function scoreAliases(query, queryTokens, aliases, baseWeight, reasons, label) {
  if (!Array.isArray(aliases) || aliases.length === 0) return 0;
  let score = 0;
  let hits = 0;
  for (const alias of aliases) {
    const normalized = normalize(alias);
    if (!normalized) continue;
    if (query.includes(normalized) || normalized.includes(query)) {
      score += baseWeight * 2;
      hits += 1;
      continue;
    }
    for (const token of queryTokens) {
      if (normalized.includes(token)) {
        score += baseWeight;
        hits += 1;
        break;
      }
    }
  }
  if (hits > 0) reasons.push(`${label}:别名命中${hits}`);
  return score;
}

function buildSkillCandidates(task, registry) {
  const query = normalize(task);
  const queryTokens = tokenize(task);

  return registry
    .map((skill) => {
      const reasons = [];
      let score = 0;

      score += scoreField(query, queryTokens, skill.name, 5, reasons, "name");
      score += scoreField(query, queryTokens, skill.trigger_hint, 3, reasons, "trigger");
      score += scoreField(query, queryTokens, skill.description, 2, reasons, "desc");
      score += scoreField(query, queryTokens, skill.group, 1, reasons, "group");
      score += scoreAliases(query, queryTokens, SKILL_ALIASES[skill.name], 3, reasons, "alias");

      if (skill.has_trigger) score += 0.25;

      return {
        name: skill.name,
        group: skill.group || "misc",
        score: Number(score.toFixed(2)),
        why: unique(reasons).slice(0, 4),
      };
    })
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score || a.name.localeCompare(b.name, "zh-CN"))
    .slice(0, 8);
}

function buildComboCandidates(task, combos, candidates) {
  const query = normalize(task);
  const queryTokens = tokenize(task);
  const candidateNames = new Set(candidates.filter((item) => item.score >= 3).map((item) => item.name));

  return Object.entries(combos)
    .map(([scenario, skills]) => {
      const reasons = [];
      let score = 0;
      const scenarioText = normalize(scenario);

      if (scenarioText.includes(query) || query.includes(scenarioText)) {
        score += 6;
        reasons.push("scenario:全文命中");
      }

      let scenarioTokenHits = 0;
      for (const token of queryTokens) {
        if (scenarioText.includes(token)) scenarioTokenHits += 1;
      }
      if (scenarioTokenHits > 0) {
        score += scenarioTokenHits * 2;
        reasons.push(`scenario:词命中${scenarioTokenHits}`);
      }

      score += scoreAliases(query, queryTokens, SCENARIO_ALIASES[scenario], 3, reasons, "scenario-alias");

      const overlap = skills.filter((name) => candidateNames.has(name));
      if (overlap.length > 0) {
        score += overlap.length * 4;
        reasons.push(`skills:候选重合${overlap.length}`);
      }

      return {
        scenario,
        skills,
        score: Number(score.toFixed(2)),
        why: unique(reasons),
      };
    })
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score || a.scenario.localeCompare(b.scenario, "zh-CN"))
    .slice(0, 5);
}

function main() {
  const args = process.argv.slice(2);
  const asJson = args.includes("--json");
  const task = args.filter((arg) => arg !== "--json").join(" ").trim();

  if (!task) {
    console.error("Usage: node match-skills.mjs <task text> [--json]");
    process.exit(1);
  }

  const registry = readJson(REGISTRY_PATH);
  const combos = readJson(ROUTER_PATH);

  const candidates = buildSkillCandidates(task, registry);
  const comboCandidates = buildComboCandidates(task, combos, candidates);

  const result = {
    task,
    candidates,
    combos: comboCandidates,
    meta: {
      candidateCount: candidates.length,
      comboCount: comboCandidates.length,
      registryPath: REGISTRY_PATH,
      routerPath: ROUTER_PATH,
    },
  };

  if (asJson) {
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  console.log(`# Skill matches: ${task}`);
  console.log("");
  console.log("## Candidates");
  if (candidates.length === 0) {
    console.log("- none");
  } else {
    for (const item of candidates) {
      console.log(`- ${item.name} [${item.group}] score=${item.score}`);
      if (item.why.length > 0) console.log(`  - ${item.why.join(" · ")}`);
    }
  }

  console.log("");
  console.log("## Combos");
  if (comboCandidates.length === 0) {
    console.log("- none");
  } else {
    for (const item of comboCandidates) {
      console.log(`- ${item.scenario} score=${item.score}`);
      console.log(`  - ${item.skills.join(", ")}`);
      if (item.why.length > 0) console.log(`  - ${item.why.join(" · ")}`);
    }
  }
}

main();
