#!/usr/bin/env node
/**
 * 将 plan-extract.json + ad geo resolve 落盘 JSON → campaign-create 配置。
 *
 * 用法：
 *   node assemble-campaign-from-plan.mjs \
 *     --plan ./plan-extract.json \
 *     --geo ./snap-geo/ad-geo-resolve-123.json \
 *     --template ./campaign-create-template.json \
 *     --out ./campaign.json
 *
 * 匹配类型与 geo id 只来自输入文件，不在此脚本内猜测。
 */
import { readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

function arg(name, fallback) {
  const i = process.argv.indexOf(name);
  if (i === -1) return fallback;
  return process.argv[i + 1];
}

function die(msg) {
  console.error(`❌ ${msg}`);
  process.exit(1);
}

function stripMeta(value) {
  if (Array.isArray(value)) return value.map(stripMeta);
  if (value && typeof value === "object") {
    const out = {};
    for (const [k, v] of Object.entries(value)) {
      if (k.startsWith("_")) continue;
      out[k] = stripMeta(v);
    }
    return out;
  }
  return value;
}

function normalizeMatchType(raw) {
  const u = String(raw ?? "BROAD")
    .trim()
    .toUpperCase();
  if (u === "EXACT" || u === "完全匹配" || u === "精确匹配") return "EXACT";
  if (u === "PHRASE" || u === "词组匹配" || u === "短语匹配") return "PHRASE";
  if (u === "BROAD" || u === "广泛匹配") return "BROAD";
  die(`未知 matchType: ${raw}`);
}

function formatKeyword(text, matchType) {
  const core = String(text ?? "")
    .trim()
    .replace(/^\[|\]$/g, "")
    .replace(/^"|"$/g, "");
  if (!core) die("关键词 text 为空");
  if (matchType === "EXACT") return `[${core}]`;
  if (matchType === "PHRASE") return `"${core}"`;
  return core;
}

function readJsonFile(path) {
  const raw = readFileSync(path, "utf8").replace(/^\uFEFF/, "");
  return JSON.parse(raw);
}

function loadGeoPayload(geoPath) {
  const geo = readJsonFile(geoPath);
  // 兼容 --json-out 包一层 / 直接 payload
  const payload = geo.targetedLocations ? geo : (geo.data ?? geo.payload ?? geo);
  if (!Array.isArray(payload.locations) || !Array.isArray(payload.targetedLocations)) {
    die(`geo 文件缺少 locations / targetedLocations：${geoPath}`);
  }
  if (payload.locations.length !== payload.targetedLocations.length) {
    die("geo 文件 locations 与 targetedLocations 数量不一致");
  }
  if (payload.failed > 0) {
    die(`geo resolve 仍有 ${payload.failed} 个失败项，请先修好再组装`);
  }
  return payload;
}

function buildKeywordBlocks(keywords, finalUrl) {
  const buckets = { EXACT: [], PHRASE: [], BROAD: [] };
  for (const kw of keywords ?? []) {
    const mt = normalizeMatchType(kw.matchType);
    buckets[mt].push(formatKeyword(kw.text, mt));
  }
  const order = ["EXACT", "PHRASE", "BROAD"];
  return order
    .filter((mt) => buckets[mt].length > 0)
    .map((mt) => ({
      KeywordText: buckets[mt],
      MatchTypeV2: mt,
      FinalURL: finalUrl,
    }));
}

function buildRsa(rsa, fallbackUrl) {
  const headlines = rsa?.headlines ?? [];
  const descriptions = rsa?.descriptions ?? [];
  if (headlines.length !== 15) {
    die(`RSA headlines 须为 15 条，当前 ${headlines.length}`);
  }
  if (descriptions.length !== 4) {
    die(`RSA descriptions 须为 4 条，当前 ${descriptions.length}`);
  }
  const url = rsa.finalUrl ?? fallbackUrl;
  return {
    TypeV2: "RESPONSIVE_SEARCH_AD",
    DestinationUrl: url,
    Finalurl: url,
    AdTitle: null,
    Path1: rsa.path1 ?? "",
    Path2: rsa.path2 ?? "",
    headlinePart1: headlines[0],
    headlinePart2: headlines[1],
    headlinePart3: headlines[2],
    AddtionalHeadlines: headlines.slice(3),
    adDescription: descriptions[0],
    adDescription2: descriptions[1],
    AddtionalAdDescriptions: descriptions.slice(2),
  };
}

function buildExtensions(ext, defaultUrl) {
  const out = [];
  for (const s of ext?.sitelinks ?? []) {
    out.push({
      level: "Campaign",
      typeV2: "SITELINK",
      AssetFieldType: "SITELINK",
      Properties: {
        Text: s.text,
        Line2: s.line2 ?? s.text,
        Line3: s.line3 ?? s.line2 ?? s.text,
        DestinationUrl: s.url ?? defaultUrl,
      },
    });
  }
  for (const c of ext?.callouts ?? []) {
    out.push({
      level: "Campaign",
      typeV2: "CALLOUT",
      AssetFieldType: "CALLOUT",
      Properties: { Text: c },
    });
  }
  const sn = ext?.structuredSnippet;
  if (sn?.header && Array.isArray(sn.values) && sn.values.length > 0) {
    out.push({
      level: "Campaign",
      typeV2: "STRUCTURED_SNIPPET",
      AssetFieldType: "STRUCTURED_SNIPPET",
      StructuredSnippetHeaderValue: { Key: sn.header, Value: sn.values },
    });
  }
  return out;
}

const planPath = arg("--plan");
const geoPath = arg("--geo");
const templatePath = arg("--template");
const outPath = arg("--out", "./campaign.json");

if (!planPath || !geoPath || !templatePath) {
  die(
    "用法: node assemble-campaign-from-plan.mjs --plan <plan-extract.json> --geo <geo-resolve.json> --template <campaign-create-template.json> [--out campaign.json]",
  );
}

const plan = stripMeta(readJsonFile(resolve(planPath)));
const geo = loadGeoPayload(resolve(geoPath));
const template = stripMeta(readJsonFile(resolve(templatePath)));

const url = plan.url ?? template.url ?? "";
const name = plan.name ?? template.name;
const defaultMaxCpc = Number(plan.maxCpcDefault ?? 5);

const negBlocks = (() => {
  const buckets = { EXACT: [], PHRASE: [], BROAD: [] };
  for (const kw of plan.negativeKeywords ?? []) {
    const mt = normalizeMatchType(kw.matchType ?? "BROAD");
    buckets[mt].push(formatKeyword(kw.text, mt));
  }
  return ["BROAD", "PHRASE", "EXACT"]
    .filter((mt) => buckets[mt].length > 0)
    .map((mt) => ({ KeywordText: buckets[mt], MatchTypeV2: mt, FinalURL: "" }));
})();

const adGroups = (plan.adGroups ?? []).map((g) => {
  const finalUrl = g.finalUrl ?? url;
  return {
    Name: g.name,
    StatusV2: "Enabled",
    TypeV2: "SEARCH_STANDARD",
    RotationModeV2: "Unspecified",
    MaxCPCAmount: Number(g.maxCpc ?? defaultMaxCpc),
    KeywordsForBatchJob: buildKeywordBlocks(g.keywords, finalUrl),
    AdsForBatchJob: [buildRsa(g.rsa ?? {}, finalUrl)],
  };
});

if (adGroups.length === 0) die("plan.adGroups 不能为空");

let exact = 0;
let phrase = 0;
let broad = 0;
for (const g of plan.adGroups ?? []) {
  for (const kw of g.keywords ?? []) {
    const mt = normalizeMatchType(kw.matchType);
    if (mt === "EXACT") exact++;
    else if (mt === "PHRASE") phrase++;
    else broad++;
  }
}

const campaign = {
  ...(template.campaign ?? {}),
  Name: name,
  StatusV2: "Enabled",
  ChannelTypeV2: "SEARCH",
  BiddingStrategyTypeV2: plan.biddingStrategyTypeV2 ?? "MANUAL_CPC",
  Budget: Number(plan.budget ?? template.campaign?.Budget ?? 0),
  BudgetShared: false,
  BudgetId: 0,
  BudgetBudgetDeliveryMethodV2: "STANDARD",
  TargetGoogleSearch: true,
  TargetSearchNetwork: false,
  TargetContentNetwork: false,
  TargetPartnerSearchNetwork: false,
  StartTime: plan.startTime ?? template.campaign?.StartTime,
  EndTime: plan.endTime ?? template.campaign?.EndTime,
  targetedLocations: geo.targetedLocations,
  excludedLocations: [],
  excludedIpAddresses: [],
  NegativeKeywordsForBatchJob: negBlocks,
  ExtensionsForBatchJob: buildExtensions(plan.extensions, url),
  AdGroupsForBatchJob: adGroups,
};

// MANUAL_CPC 不需要 TargetSpend 字段
if (campaign.BiddingStrategyTypeV2 === "MANUAL_CPC") {
  delete campaign.TargetSpend_BidCeilingAmount;
} else if (
  campaign.BiddingStrategyTypeV2 === "TARGET_SPEND" &&
  campaign.TargetSpend_BidCeilingAmount == null
) {
  campaign.TargetSpend_BidCeilingAmount = defaultMaxCpc;
}

const out = {
  account: String(plan.account ?? template.account),
  customerName: plan.customerName ?? template.customerName ?? "",
  name,
  url,
  locations: geo.locations,
  productWords: plan.productWords ?? [],
  googleDataRecordId: null,
  draft: false,
  campaign,
};

writeFileSync(resolve(outPath), JSON.stringify(out, null, 2) + "\n", "utf8");
console.log(
  JSON.stringify(
    {
      out: resolve(outPath),
      locations: geo.locations.length,
      adGroups: adGroups.length,
      keywords: { exact, phrase, broad, total: exact + phrase + broad },
      next: `siluzan-tso ad campaign-validate --config-file ${outPath}`,
    },
    null,
    2,
  ),
);
