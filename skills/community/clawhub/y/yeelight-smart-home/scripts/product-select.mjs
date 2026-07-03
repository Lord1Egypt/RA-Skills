#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const skillDir = path.resolve(__dirname, "..");
const catalogPath = path.join(skillDir, "assets", "catalog", "lighting-design-products.json");
const domainCatalogPath = path.join(skillDir, "assets", "catalog", "yeelight-domain.json");

function parseArgs(argv) {
  const result = { query: "", limit: 8, category: "", room: "", goal: "" };
  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === "--query" || value === "-q") {
      result.query = argv[index + 1] || "";
      index += 1;
    } else if (value === "--limit") {
      result.limit = Number.parseInt(argv[index + 1] || "8", 10);
      index += 1;
    } else if (value === "--category") {
      result.category = argv[index + 1] || "";
      index += 1;
    } else if (value === "--room") {
      result.room = argv[index + 1] || "";
      index += 1;
    } else if (value === "--goal") {
      result.goal = argv[index + 1] || "";
      index += 1;
    } else if (!value.startsWith("-")) {
      result.query = [result.query, value].filter(Boolean).join(" ");
    }
  }
  return result;
}

const DESIGN_TOKENS = {
  colors: ["黑色", "白色", "深空灰", "星空灰", "墨灰", "晶墨灰", "汉玉白", "丝墨青", "东方既白", "暖白", "陶瓷白"],
  installStyles: ["嵌入式", "明装", "吸顶", "磁吸", "轨道", "墙面", "壁装", "桌面", "吊装", "无边框", "窄边框"],
  beamAngles: ["8度", "8°", "15度", "15°", "24度", "24°", "32度", "32°", "36度", "36°", "60度", "60°"],
  openings: ["35开孔", "55开孔", "65开孔", "75开孔", "80开孔"],
  sizes: ["2.5寸", "3寸"],
  headCounts: ["3头", "5头", "6头", "10头", "12头"],
  wattages: ["8w", "12w", "15w", "36w"],
  shapes: ["方形", "圆形"],
  series: ["S系列", "爱思系列", "S21", "S20", "E+系列", "E20", "E系列", "M20", "D系列", "P20", "P21", "Nightingale"],
  keywords: ["夙夜", "Pro", "线下版", "标准版", "国内版", "电竞", "梦幻帘", "干接点"],
  categories: ["吸顶灯", "格栅灯", "筒射灯", "射灯", "筒灯", "青空灯", "灯带", "智能开关", "面板", "旋钮", "传感器", "人在传感器", "模块"]
};

const CATEGORY_COMPATIBILITY = {
  "射灯": ["射灯", "筒射灯"],
  "筒射灯": ["筒射灯", "射灯"],
  "筒灯": ["筒灯", "筒射灯"],
  "传感器": ["传感器", "人在传感器"]
};

function readLexicalAliases() {
  try {
    const catalog = JSON.parse(fs.readFileSync(domainCatalogPath, "utf8"));
    return (catalog.language?.lexicalAliases || [])
      .filter((item) => item?.from && item?.to)
      .sort((a, b) => String(b.from).length - String(a.from).length);
  } catch {
    return [];
  }
}

const LEXICAL_ALIASES = readLexicalAliases();

function normalizeBase(value) {
  return String(value || "")
    .trim()
    .toLowerCase()
    .replaceAll(" ", "")
    .replaceAll("\t", "")
    .replaceAll("-", "")
    .replaceAll("_", "")
    .replaceAll("（", "(")
    .replaceAll("）", ")")
    .replaceAll("°", "度");
}

function applyLexicalAliases(value) {
  let result = String(value || "");
  for (const alias of LEXICAL_ALIASES) {
    const from = String(alias.from || "");
    const to = String(alias.to || "");
    if (from && to) {
      result = result.split(from).join(to);
    }
  }
  return result;
}

function normalize(value) {
  return normalizeBase(applyLexicalAliases(value));
}

function contains(haystack, needle) {
  const text = normalize(needle);
  return text !== "" && normalize(haystack).includes(text);
}

function containsEither(left, right) {
  const normalizedLeft = normalize(left);
  const normalizedRight = normalize(right);
  return normalizedLeft !== "" && normalizedRight !== "" &&
    (normalizedLeft.includes(normalizedRight) || normalizedRight.includes(normalizedLeft));
}

function tokenMatches(normalizedText, tokens) {
  return tokens.filter((token) => contains(normalizedText, token));
}

function requestedSignals(input, categoryHint) {
  const normalizedInput = normalize(input);
  const signals = {
    colors: tokenMatches(normalizedInput, DESIGN_TOKENS.colors),
    installStyles: tokenMatches(normalizedInput, DESIGN_TOKENS.installStyles),
    beamAngles: tokenMatches(normalizedInput, DESIGN_TOKENS.beamAngles).map((item) => item.replace("度", "°")),
    openings: tokenMatches(normalizedInput, DESIGN_TOKENS.openings),
    sizes: tokenMatches(normalizedInput, DESIGN_TOKENS.sizes),
    headCounts: tokenMatches(normalizedInput, DESIGN_TOKENS.headCounts),
    wattages: tokenMatches(normalizedInput, DESIGN_TOKENS.wattages).map((item) => item.toUpperCase()),
    shapes: tokenMatches(normalizedInput, DESIGN_TOKENS.shapes),
    series: tokenMatches(normalizedInput, DESIGN_TOKENS.series).map((item) => item === "爱思系列" ? "S系列" : item),
    keywords: tokenMatches(normalizedInput, DESIGN_TOKENS.keywords),
    categories: tokenMatches(normalizedInput, DESIGN_TOKENS.categories)
  };
  if (categoryHint) signals.categories.push(categoryHint);
  return Object.fromEntries(Object.entries(signals).map(([key, values]) => [key, [...new Set(values)]]));
}

function evidencePush(evidence, text, points) {
  if (!text) return 0;
  evidence.push({ text, points });
  return points;
}

function scoreProduct(product, query, categoryHint, requested) {
  const normalizedQuery = normalize(query);
  const evidence = [];
  let score = 0;
  if (!normalizedQuery) return null;
  if (contains(normalizedQuery, product.skuCode)) {
    score += evidencePush(evidence, product.skuCode, 120);
  }
  for (const field of ["productName", "productSku", "productSpu"]) {
    if (containsEither(normalizedQuery, product[field])) {
      score += evidencePush(evidence, product[field], 45);
    }
  }
  if (categoryHint && normalize(product.category) === normalize(categoryHint)) {
    score += evidencePush(evidence, `category:${product.category}`, 30);
  } else if (contains(normalizedQuery, product.category)) {
    score += evidencePush(evidence, product.category, 28);
  }
  if (contains(normalizedQuery, product.series)) {
    score += evidencePush(evidence, product.series, 22);
  }
  for (const alias of product.aliases || []) {
    if (containsEither(normalizedQuery, alias)) {
      score += evidencePush(evidence, alias, 38);
    }
  }
  for (const token of ["黑色", "白色", "深空灰", "嵌入式", "明装", "方形", "圆形", "36度", "24度", "60度", "75开孔", "55开孔", "3寸", "5头", "6头", "10头", "12头", "8w", "12w", "15w", "36w", "夙夜", "Nightingale"]) {
    if (contains(normalizedQuery, token) && contains([product.productName, product.productSku, product.productSpu, ...(product.aliases || [])].join(" "), token)) {
      score += evidencePush(evidence, token, 10);
    }
  }
  if (contains(normalizedQuery, "s系列") && product.series === "S系列") {
    score += evidencePush(evidence, "S系列", 14);
  }
  if (contains(normalizedQuery, "s") && product.series === "S系列") {
    score += evidencePush(evidence, "爱思/S系列", 14);
  }
  if (evidence.length === 0 || score <= 0) return null;
  score += designFitScore(product, requested, evidence);
  score -= constraintPenalty(product, normalizedQuery);
  if (score <= 0) return null;
  score += Number(product.priority || 0) / 10;
  return {
    score: Math.round(score),
    evidence,
    product
  };
}

function flatProductDesignValues(product, key) {
  const attrs = product.designAttributes || {};
  const values = Array.isArray(attrs[key]) ? attrs[key] : [];
  if (key === "series") return [product.series].filter(Boolean);
  if (key === "categories") return [product.category].filter(Boolean);
  if (key === "keywords") return product.designKeywords || [];
  return values;
}

function hasDesignValue(product, key, value) {
  const productValues = flatProductDesignValues(product, key);
  if (key === "categories") {
    const compatible = CATEGORY_COMPATIBILITY[value] || [value];
    return productValues.some((candidate) => compatible.some((item) => normalize(candidate) === normalize(item)));
  }
  if (key === "keywords") {
    return productValues.some((candidate) => normalize(candidate) === normalize(value)) || contains(productText(product), value);
  }
  return productValues.some((candidate) => normalize(candidate) === normalize(value));
}

function designFitScore(product, requested, evidence) {
  let score = 0;
  for (const [key, values] of Object.entries(requested)) {
    for (const value of values) {
      if (hasDesignValue(product, key, value)) {
        score += evidencePush(evidence, `${key}:${value}`, key === "categories" ? 18 : 12);
      }
    }
  }
  if ((product.capabilityTags || []).includes("brightness")) {
    score += 2;
  }
  if ((product.capabilityTags || []).includes("colorTemperature")) {
    score += 2;
  }
  return score;
}

function productText(product) {
  return normalize([
    product.productName,
    product.productSku,
    product.productSpu,
    product.category,
    product.series,
    ...(product.designRoles || []),
    ...(product.designKeywords || []),
    ...(product.capabilityTags || []),
    ...Object.values(product.designAttributes || {}).flat(),
    ...(product.aliases || [])
  ].join(" "));
}

function constraintPenalty(product, normalizedQuery) {
  const text = productText(product);
  let penalty = 0;
  for (const token of ["黑色", "白色", "深空灰", "星空灰", "墨灰", "暖白", "陶瓷白", "晶墨灰", "云灰银"]) {
    if (contains(normalizedQuery, token) && !contains(text, token)) penalty += 35;
  }
  for (const token of ["嵌入式", "明装", "吸顶", "墙面", "磁吸", "无边框", "窄边框"]) {
    if (contains(normalizedQuery, token) && !contains(text, token)) penalty += 25;
  }
  for (const token of ["8度", "15度", "24度", "32度", "36度", "60度"]) {
    if (contains(normalizedQuery, token) && !contains(text, token)) penalty += 40;
  }
  for (const token of ["35开孔", "55开孔", "65开孔", "75开孔", "80开孔", "3寸", "5头", "6头", "10头", "12头", "8w", "12w", "15w", "36w"]) {
    if (contains(normalizedQuery, token) && !contains(text, token)) penalty += 25;
  }
  if ((contains(normalizedQuery, "爱思系列") || contains(normalizedQuery, "s系列")) && product.series !== "S系列") {
    penalty += 45;
  }
  return penalty;
}

function evaluateConstraints(product, requested) {
  const matched = [];
  const missing = [];
  for (const [key, values] of Object.entries(requested)) {
    for (const value of values) {
      const item = { type: key, value };
      if (hasDesignValue(product, key, value)) {
        matched.push(item);
      } else {
        missing.push(item);
      }
    }
  }
  return { matched, missing };
}

function designNotes(product, constraintReview) {
  const notes = [];
  if ((product.designRoles || []).includes("ambient")) notes.push("适合承担基础/环境照明");
  if ((product.designRoles || []).includes("accent")) notes.push("适合重点或洗墙/局部层次照明");
  if ((product.designRoles || []).includes("focused")) notes.push("窄光束候选，适合需要聚焦的主卧、陈列或重点照明");
  if ((product.designRoles || []).includes("comfort")) notes.push("偏舒适氛围候选，适合青空灯类空间体验");
  if ((product.capabilityTags || []).includes("brightness") && (product.capabilityTags || []).includes("colorTemperature")) {
    notes.push("支持亮度和色温，便于情景和自动化编排");
  }
  if (constraintReview.missing.length > 0) {
    notes.push("存在未完全命中的用户约束，最终选择前应说明假设或换更贴合候选");
  }
  return notes;
}

function selectionGuidance(matches) {
  if (matches.length === 0) {
    return "No candidate was found. Ask for a product family, series, install style, color, or SKU, or use product.pedia.search for official product facts.";
  }
  if (matches.length >= 2 && Math.abs(matches[0].score - matches[1].score) < 8) {
    return "Top candidates are close. AI should decide from room role, optical intent, installation constraints, color, series, wattage/opening, and whether the user needs a concrete design now.";
  }
  return "Use the top candidate only if its design notes and missing constraints fit the user request. Otherwise choose another candidate and pass explicit skuCode, capabilityPid, and productComponentId to Runtime.";
}

function confidence(score) {
  if (score >= 90) return "high";
  if (score >= 55) return "medium";
  return "low";
}

const args = parseArgs(process.argv.slice(2));
const input = [args.room, args.query, args.goal, args.category].filter(Boolean).join(" ");
const limit = Number.isFinite(args.limit) && args.limit > 0 ? Math.min(args.limit, 20) : 8;
const products = JSON.parse(fs.readFileSync(catalogPath, "utf8"));
const requested = requestedSignals(input, args.category);
const matches = products
  .map((product) => scoreProduct(product, input, args.category, requested))
  .filter(Boolean)
  .sort((a, b) => {
    if (b.score !== a.score) return b.score - a.score;
    if ((b.product.priority || 0) !== (a.product.priority || 0)) return (b.product.priority || 0) - (a.product.priority || 0);
    return String(a.product.skuCode).localeCompare(String(b.product.skuCode));
  })
  .slice(0, limit)
  .map((match) => {
    const constraintReview = evaluateConstraints(match.product, requested);
    return {
      skuCode: match.product.skuCode,
      capabilityPid: match.product.capabilityPid,
      productComponentId: match.product.productComponentId,
      productName: match.product.productName,
      productSku: match.product.productSku,
      productSpu: match.product.productSpu,
      category: match.product.category,
      series: match.product.series,
      designAttributes: match.product.designAttributes || {},
      designRoles: match.product.designRoles || [],
      designKeywords: match.product.designKeywords || [],
      capabilityTags: match.product.capabilityTags || [],
      adjustableProperties: match.product.adjustableProperties,
      propertyEvents: match.product.propertyEvents,
      sensorEvents: match.product.sensorEvents,
      score: match.score,
      confidence: confidence(match.score),
      evidence: match.evidence.slice(0, 10),
      constraintReview,
      designNotes: designNotes(match.product, constraintReview)
    };
  });

process.stdout.write(JSON.stringify({
  query: input,
  normalizedQuery: normalize(input),
  catalog: "skill_lighting_design_products",
  lexicalAliasCount: LEXICAL_ALIASES.length,
  requestedSignals: requested,
  returned: matches.length,
  candidates: matches,
  selectionGuidance: selectionGuidance(matches),
  runtimeRule: "After AI chooses a candidate, copy skuCode, capabilityPid, productComponentId, and readable productName/category/series/notes into lighting.design.import or device.slot.create. Do not rely on fuzzy Runtime auto-selection for final design choices."
}, null, 2));
process.stdout.write("\n");
