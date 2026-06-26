"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.LINK_PATTERN = void 0;
exports.normalizeText = normalizeText;
exports.dedupePreserveOrder = dedupePreserveOrder;
exports.findLiteralOccurrences = findLiteralOccurrences;
exports.selectNonOverlapping = selectNonOverlapping;
exports.extractBrand = extractBrand;
exports.extractLiteralTerms = extractLiteralTerms;
exports.extractCategories = extractCategories;
exports.extractAttributes = extractAttributes;
exports.pruneSubstringAliases = pruneSubstringAliases;
exports.guessBrandFromPrefix = guessBrandFromPrefix;
exports.isValidBrandCandidate = isValidBrandCandidate;
exports.extractSpecs = extractSpecs;
exports.extractModels = extractModels;
exports.normalizeModels = normalizeModels;
exports.extractExplicitSku = extractExplicitSku;
exports.extractBudget = extractBudget;
exports.extractPlatformHint = extractPlatformHint;
exports.containsFuzzyMarker = containsFuzzyMarker;
exports.cleanSlotText = cleanSlotText;
exports.evidenceInText = evidenceInText;
exports.makeScalarRawSlot = makeScalarRawSlot;
exports.makeListRawSlots = makeListRawSlots;
exports.normalizeScalarRawSlot = normalizeScalarRawSlot;
exports.normalizeListRawSlots = normalizeListRawSlots;
exports.parseBool = parseBool;
exports.parseConfidence = parseConfidence;
exports.normalizePriceNumber = normalizePriceNumber;
exports.extractPriceConstraints = extractPriceConstraints;
exports.normalizeBrandValue = normalizeBrandValue;
exports.normalizePlatformHintValue = normalizePlatformHintValue;
exports.extractCrowd = extractCrowd;
exports.extractUsageScene = extractUsageScene;
exports.extractGiftTarget = extractGiftTarget;
exports.extractSortHint = extractSortHint;
exports.sortValuesByPosition = sortValuesByPosition;
exports.dropSubstringValues = dropSubstringValues;
exports.choosePreferredText = choosePreferredText;
exports.selectQueryAttributes = selectQueryAttributes;
exports.pickScalarEvidence = pickScalarEvidence;
exports.pickListEvidence = pickListEvidence;
exports.buildProductSearchIntent = buildProductSearchIntent;
exports.extractRuleSignals = extractRuleSignals;
exports.getScalarSlotValue = getScalarSlotValue;
exports.getListSlotValues = getListSlotValues;
exports.isPreciseSearch = isPreciseSearch;
exports.normalizeFuzzyProductName = normalizeFuzzyProductName;
exports.buildFuzzyIntentFromRuleSignals = buildFuzzyIntentFromRuleSignals;
exports.buildEmptyProductSearchIntent = buildEmptyProductSearchIntent;
exports.recognizeRawMessage = recognizeRawMessage;
exports.main = main;
const common_1 = require("./common");
const productSearchProtocol_1 = require("./productSearchProtocol");
const ACTION_PREFIX_PATTERNS = [
    /^(?:帮我|麻烦|请|请帮我|我想|我要|想|想要|给我|替我|帮忙)?(?:搜一下|搜下|搜一搜|搜|查一下|查下|查一查|查|找一下|找下|找找|找|搜索一下|搜索|看一下|看下|看看|有没有|有无)\s*/i,
    /^(?:我想买|我要买|想买)\s*/i,
];
const BRAND_ALIASES = {
    "机械革命": "机械革命",
    "雅诗兰黛": "雅诗兰黛",
    "阿迪达斯": "阿迪达斯",
    "班尼路": "班尼路",
    traveldetail: "飞猪",
    iphone: "苹果",
    apple: "苹果",
    huawei: "华为",
    honor: "荣耀",
    redmi: "红米",
    lenovo: "联想",
    dell: "戴尔",
    asus: "华硕",
    sony: "索尼",
    oppo: "OPPO",
    vivo: "vivo",
    nike: "耐克",
    "李宁": "李宁",
    "安踏": "安踏",
    "361°": "361°",
    "361": "361°",
    "耐克": "耐克",
    "华为": "华为",
    "苹果": "苹果",
    "小米": "小米",
    "红米": "红米",
    "荣耀": "荣耀",
    "美的": "美的",
    "格力": "格力",
    "海尔": "海尔",
    "联想": "联想",
    "戴尔": "戴尔",
    "惠普": "惠普",
    "华硕": "华硕",
    "索尼": "索尼",
    OPPO: "OPPO",
};
const CATEGORY_TERMS = [
    "蓝牙耳机",
    "无线耳机",
    "机械键盘",
    "男裤",
    "女裤",
    "休闲长裤",
    "冰丝裤子",
    "冰丝裤",
    "速干裤",
    "束脚裤",
    "运动长裤",
    "休闲裤",
    "运动裤",
    "短裤",
    "徒步鞋",
    "运动鞋",
    "跑鞋",
    "长裤",
    "裤子",
    "手机",
    "耳机",
    "空调",
    "键盘",
    "鼠标",
    "显示器",
    "笔记本",
    "平板",
    "手表",
    "洗发水",
    "护肤品",
    "面膜",
    "电视",
    "冰箱",
    "洗衣机",
    "路由器",
    "袜子",
];
const ATTRIBUTE_TERMS = [
    "户外运动",
    "男士",
    "女士",
    "男款",
    "女款",
    "夏季",
    "冬季",
    "春秋",
    "户外",
    "运动",
    "速干",
    "冰丝",
    "超薄",
    "薄款",
    "束脚",
    "休闲",
];
const ATTRIBUTE_PATTERNS = [
    /(?:男|女)(?:士|款)?/g,
    /(?:速干|冰丝|纯棉|透气|保暖|轻薄|超薄|防水|防滑)/g,
    /(?:薄款|厚款|加绒|加厚|宽松|修身|直筒|束脚|阔腿|高腰|低帮|中帮|高帮)/g,
];
const GENERIC_ONLY_TERMS = new Set([...CATEGORY_TERMS, "鞋", "裤子", "长裤", "运动裤", "休闲裤", "袜子"]);
const PLATFORM_HINTS = {
    "淘宝": "taobao",
    "京东": "jd",
    "拼多多": "pdd",
};
const CROWD_HINTS = [
    ["男士", "男士"],
    ["男款", "男士"],
    ["男生", "男士"],
    ["女士", "女士"],
    ["女款", "女士"],
    ["女生", "女士"],
    ["儿童", "儿童"],
    ["小孩", "儿童"],
    ["宝宝", "宝宝"],
    ["婴儿", "婴儿"],
    ["孕妇", "孕妇"],
];
const USAGE_SCENE_HINTS = [
    ["通勤", "通勤"],
    ["户外", "户外"],
    ["运动", "运动"],
    ["跑步", "跑步"],
    ["徒步", "徒步"],
    ["健身", "健身"],
    ["办公", "办公"],
    ["家用", "家用"],
    ["宿舍", "宿舍"],
    ["旅行", "旅行"],
    ["露营", "露营"],
];
const GIFT_TARGET_HINTS = [
    ["送给女朋友", "女朋友"],
    ["送女朋友", "女朋友"],
    ["送给男朋友", "男朋友"],
    ["送男朋友", "男朋友"],
    ["送老婆", "老婆"],
    ["送老公", "老公"],
    ["送妈妈", "妈妈"],
    ["送爸爸", "爸爸"],
    ["送孩子", "孩子"],
];
const SORT_HINTS = [
    ["性价比", "性价比优先"],
    ["销量", "销量优先"],
    ["便宜", "低价优先"],
    ["最便宜", "低价优先"],
];
const FUZZY_MARKERS = ["推荐", "适合", "礼物", "左右", "以内", "以下", "预算", "性价比", "哪个好", "求推荐", "帮我选"];
const SPEC_PATTERNS = [
    /\d+\s*\+\s*\d+\s*(?:G|GB|TB)\b/gi,
    /\d+\s*(?:ml|ML|g|kg|KG|L|l|片|粒|只|瓶|袋|盒|支)\s*\*\s*\d+/g,
    /\d+\s*(?:G|GB|TB|kg|KG|g|ml|ML|L|l|寸|码|粒|片|只|瓶|袋|盒|支)\b/gi,
];
const MODEL_PATTERNS = [
    /\b(?:iPhone\s*\d+(?:\s*(?:Pro Max|Pro|Plus|mini))?)\b/gi,
    /\b(?:Mate\s*\d+(?:\s*(?:Pro\+?|RS|SE|X\d+))?)\b/gi,
    /\b(?:Pura\s*\d+(?:\s*(?:Ultra|Pro\+?|Pro))?)\b/gi,
    /[A-Za-z0-9]+(?:[&/+.-][A-Za-z0-9]+)+(?:系列)?/g,
    /\b[A-Za-z]{2,10}-\d[A-Za-z0-9\-_/+.]{1,}\b/g,
    /\b[A-Za-z]{1,6}\d[A-Za-z0-9\-_/+.]{1,}\b/g,
    /[\u4e00-\u9fff]{1,8}\d+[A-Za-z0-9\-+/]{0,6}/g,
    /\b[A-Z]{2,6}\b/g,
];
const EXPLICIT_SKU_PATTERN = /(?:sku|SKU|型号|货号|款号|编码)\s*[:：]?\s*([A-Za-z0-9][A-Za-z0-9\-_/+.]{2,})/;
const BUDGET_PATTERN = /(\d+(?:\.\d+)?)\s*(?:元)?(?:左右|以内|以下|上下)/;
const PRICE_RANGE_PATTERN = /(\d+(?:\.\d+)?)\s*(?:元)?\s*(?:到|至|-|~)\s*(\d+(?:\.\d+)?)\s*元?/;
const PRICE_MAX_PATTERN = /(\d+(?:\.\d+)?)\s*(?:元)?(?:以内|以下|不到)/;
const PRICE_MIN_PATTERN = /(\d+(?:\.\d+)?)\s*(?:元)?(?:以上|起|起步)/;
const PRICE_TARGET_PATTERN = /(\d+(?:\.\d+)?)\s*(?:元)?(?:左右|上下)/;
exports.LINK_PATTERN = /https?:\/\/[^\s]+/i;
const TOKEN_PATTERN = /[\u4e00-\u9fffA-Za-z0-9&+\-/.]+/g;
const LEADING_QUANTITY_PATTERN_TEXT = "(?:[一二两三四五六七八九十几\\d]+)?(?:双|条|件|个|款|只|包|盒|瓶|台|部|套|支|张|本|杯|顶|副)";
const LEADING_QUANTITY_PATTERN = new RegExp(`^${LEADING_QUANTITY_PATTERN_TEXT}$`);
const LEADING_QUANTITY_PREFIX_PATTERN = new RegExp(`^${LEADING_QUANTITY_PATTERN_TEXT}\\s*`);
const LOW_PRIORITY_QUERY_ATTRIBUTES = new Set(["男", "女", "男士", "女士", "男款", "女款", "夏季", "冬季", "春秋"]);
const NULL_LIKE_VALUES = new Set(["", "null", "none", "unknown", "n/a", "na", "无", "未知", "空"]);
const MODEL_SLOT_SYSTEM_PROMPT = `
你是一个电商商品标题槽位抽取器。

你只能输出一个 JSON 对象，不能输出 markdown，不能输出解释。

抽取目标：
- is_precise_search
- confidence
- brand
- model
- sku
- product_name
- category
- attributes
- specs
- platform_hint

输出要求：
1. 每个标量槽位输出 {"value": ..., "evidence": ...}
2. attributes 和 specs 输出数组，元素格式为 {"value": ..., "evidence": ...}
3. evidence 必须是原文中的原样片段，不能改写
4. 不确定就返回 null 或 []
5. 不允许编造品牌、型号、SKU、类目
6. 完整商品标题通常视为精准搜索
7. 品牌优先看标题前缀
8. 商品词/类目要尽量具体，不要只给过宽泛词
`.trim();
function escapeRegExp(value) {
    return String(value).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}
function withGlobal(pattern) {
    const flags = pattern.flags.includes("g") ? pattern.flags : `${pattern.flags}g`;
    return new RegExp(pattern.source, flags);
}
function normalizeText(rawMessage) {
    const translation = new Map([
        ["，", " "],
        ["。", " "],
        ["！", " "],
        ["？", " "],
        ["：", ":"],
        ["（", "("],
        ["）", ")"],
        ["【", " "],
        ["】", " "],
        ["“", " "],
        ["”", " "],
        ["、", " "],
        ["\n", " "],
        ["\t", " "],
        ["\u3000", " "],
    ]);
    let normalized = String(rawMessage || "")
        .split("")
        .map((char) => translation.get(char) ?? char)
        .join("");
    normalized = normalized.replace(/\s+/g, " ").trim();
    let previous = "";
    while (previous !== normalized) {
        previous = normalized;
        for (const pattern of ACTION_PREFIX_PATTERNS) {
            normalized = normalized.replace(pattern, "").trim();
        }
    }
    return normalized;
}
function dedupePreserveOrder(values) {
    const seen = new Set();
    const result = [];
    for (const value of values || []) {
        const normalized = String(value || "").trim();
        if (!normalized) {
            continue;
        }
        const key = normalized.toLowerCase();
        if (seen.has(key)) {
            continue;
        }
        seen.add(key);
        result.push(normalized);
    }
    return result;
}
function findLiteralOccurrences(text, aliases) {
    const matches = [];
    const lowerText = text.toLowerCase();
    for (const [alias, canonical] of aliases) {
        let start = 0;
        const aliasLower = alias.toLowerCase();
        while (true) {
            const index = lowerText.indexOf(aliasLower, start);
            if (index === -1) {
                break;
            }
            matches.push({
                start: index,
                end: index + alias.length,
                text: text.slice(index, index + alias.length),
                value: canonical,
            });
            start = index + alias.length;
        }
    }
    return matches;
}
function selectNonOverlapping(matches) {
    const selected = [];
    const occupied = [];
    for (const match of [...matches].sort((a, b) => {
        const diff = a.start - b.start;
        if (diff !== 0) {
            return diff;
        }
        return (b.end - b.start) - (a.end - a.start);
    })) {
        const hasOverlap = occupied.some(([start, end]) => !(match.end <= start || match.start >= end));
        if (hasOverlap) {
            continue;
        }
        occupied.push([match.start, match.end]);
        selected.push(match);
    }
    return selected;
}
function extractBrand(text) {
    const aliasItems = Object.entries(BRAND_ALIASES).sort((a, b) => b[0].length - a[0].length);
    const matches = selectNonOverlapping(findLiteralOccurrences(text, aliasItems));
    const brands = dedupePreserveOrder(matches.map((match) => match.value));
    const aliases = dedupePreserveOrder(matches.map((match) => match.text));
    return [brands[0] || null, aliases];
}
function extractLiteralTerms(text, terms) {
    const aliasItems = [...terms].sort((a, b) => b.length - a.length).map((term) => [term, term]);
    const matches = selectNonOverlapping(findLiteralOccurrences(text, aliasItems));
    const values = dedupePreserveOrder(matches.map((match) => match.value));
    const aliases = dedupePreserveOrder(matches.map((match) => match.text));
    return [values, aliases];
}
function extractCategories(text) {
    const [categories, aliases] = extractLiteralTerms(text, CATEGORY_TERMS);
    return [categories[0] || null, aliases];
}
function extractAttributes(text) {
    const [literalAttributes, literalAliases] = extractLiteralTerms(text, ATTRIBUTE_TERMS);
    const patternAttributes = [];
    const patternAliases = [];
    for (const pattern of ATTRIBUTE_PATTERNS) {
        const regex = withGlobal(pattern);
        for (const match of text.matchAll(regex)) {
            const alias = String(match[0] || "").trim();
            if (alias) {
                patternAttributes.push(alias);
                patternAliases.push(alias);
            }
        }
    }
    const attributes = dedupePreserveOrder([...literalAttributes, ...patternAttributes]);
    const aliases = dedupePreserveOrder([...literalAliases, ...patternAliases]);
    return [attributes, aliases];
}
function pruneSubstringAliases(aliases, protectedAliases) {
    const filtered = [];
    for (const alias of aliases || []) {
        if (protectedAliases.some((protectedAlias) => alias !== protectedAlias && protectedAlias.includes(alias))) {
            continue;
        }
        filtered.push(alias);
    }
    return dedupePreserveOrder(filtered);
}
function guessBrandFromPrefix(text, models, categoryAliases, attributeAliases) {
    const candidatePositions = [];
    for (const value of dedupePreserveOrder([...models, ...categoryAliases, ...attributeAliases])) {
        const position = text.indexOf(value);
        if (position > 0) {
            candidatePositions.push(position);
        }
    }
    if (!candidatePositions.length) {
        return [null, []];
    }
    let prefix = text.slice(0, Math.min(...candidatePositions)).trim();
    prefix = prefix.replace(/[\s\-_/+.]+$/g, "");
    const compactPrefix = prefix.replace(/\s+/g, "");
    if (!isValidBrandCandidate(compactPrefix)) {
        return [null, []];
    }
    return [compactPrefix, [compactPrefix]];
}
function isValidBrandCandidate(candidate) {
    if (!candidate) {
        return false;
    }
    if (candidate.length < 2 || candidate.length > 12) {
        return false;
    }
    if (!/[\u4e00-\u9fffA-Za-z]/.test(candidate)) {
        return false;
    }
    if (/^[A-Za-z0-9]+$/.test(candidate) && candidate.length <= 2) {
        return false;
    }
    if (candidate.includes("的")) {
        return false;
    }
    if (containsFuzzyMarker(candidate)) {
        return false;
    }
    if (/\d+\s*(?:元)?(?:左右|以内|以下|上下)/.test(candidate)) {
        return false;
    }
    if (CATEGORY_TERMS.includes(candidate) || ATTRIBUTE_TERMS.includes(candidate)) {
        return false;
    }
    if (LEADING_QUANTITY_PATTERN.test(candidate)) {
        return false;
    }
    if (/^(?:男|女|男士|女士|男款|女款|夏季|冬季|春秋|速干|冰丝|运动|休闲|超薄|薄款|束脚)+$/.test(candidate)) {
        return false;
    }
    return true;
}
function extractSpecs(text) {
    const specs = [];
    for (const pattern of SPEC_PATTERNS) {
        const regex = withGlobal(pattern);
        for (const match of text.matchAll(regex)) {
            specs.push(String(match[0] || "").trim());
        }
    }
    return dedupePreserveOrder(specs);
}
function extractModels(text, specs) {
    const matches = [];
    for (const pattern of MODEL_PATTERNS) {
        const regex = withGlobal(pattern);
        for (const match of text.matchAll(regex)) {
            matches.push({
                start: match.index || 0,
                end: (match.index || 0) + String(match[0] || "").length,
                text: String(match[0] || "").trim(),
            });
        }
    }
    const selected = selectNonOverlapping(matches);
    const models = [];
    const specSet = new Set((specs || []).map((spec) => spec.toLowerCase()));
    const excluded = new Set(["pro", "max", "plus", "mini", "ultra", "gb", "tb", "ml", "kg"]);
    for (const match of selected) {
        const candidate = String(match.text || "").trim();
        const lowerCandidate = candidate.toLowerCase();
        if (specSet.has(lowerCandidate) || excluded.has(lowerCandidate) || /^\d+$/.test(candidate)) {
            continue;
        }
        models.push(candidate);
    }
    return dedupePreserveOrder(models);
}
function normalizeModels(models, brandAliases, brand) {
    const normalizedModels = [];
    const removablePrefixes = [];
    for (const alias of brandAliases || []) {
        if (!alias) {
            continue;
        }
        if (alias.toLowerCase() === String(brand || "").toLowerCase() || /[\u4e00-\u9fff]/.test(alias)) {
            removablePrefixes.push(alias);
        }
    }
    if (brand) {
        removablePrefixes.push(brand);
    }
    for (const model of models || []) {
        let normalized = model;
        for (const prefix of dedupePreserveOrder(removablePrefixes).sort((a, b) => b.length - a.length)) {
            if (prefix && normalized.toLowerCase().startsWith(prefix.toLowerCase())) {
                const trimmed = normalized.slice(prefix.length).trim();
                if (trimmed) {
                    normalized = trimmed;
                }
                break;
            }
        }
        normalizedModels.push(normalized);
    }
    return dedupePreserveOrder(normalizedModels);
}
function extractExplicitSku(text) {
    const match = text.match(EXPLICIT_SKU_PATTERN);
    return match ? String(match[1] || "").trim() || null : null;
}
function extractBudget(text) {
    const match = text.match(BUDGET_PATTERN);
    return match ? `${String(match[1] || "").trim()}元` : null;
}
function extractPlatformHint(text) {
    for (const [label, platform] of Object.entries(PLATFORM_HINTS)) {
        if (text.includes(label)) {
            return platform;
        }
    }
    return null;
}
function containsFuzzyMarker(text) {
    return FUZZY_MARKERS.some((marker) => text.includes(marker));
}
function cleanSlotText(value) {
    if (value === null || value === undefined || typeof value === "boolean") {
        return null;
    }
    const text = String(value).trim();
    if (!text) {
        return null;
    }
    const lower = text.toLowerCase();
    if (NULL_LIKE_VALUES.has(text) || NULL_LIKE_VALUES.has(lower)) {
        return null;
    }
    return text;
}
function compactText(text) {
    return String(text || "").replace(/[^0-9A-Za-z\u4e00-\u9fff&+\-/.]+/g, "").toLowerCase();
}
function evidenceInText(sourceText, evidence) {
    const normalizedSource = compactText(sourceText);
    const normalizedEvidence = compactText(evidence);
    return Boolean(normalizedSource && normalizedEvidence && normalizedSource.includes(normalizedEvidence));
}
function makeScalarRawSlot(value, evidence) {
    return {
        value: cleanSlotText(value),
        evidence: cleanSlotText(evidence),
    };
}
function makeListRawSlots(values) {
    return dedupePreserveOrder(values || []).map((value) => makeScalarRawSlot(value, value));
}
function normalizeScalarRawSlot(slot, sourceText) {
    if (Array.isArray(slot)) {
        slot = slot.length ? slot[0] : null;
    }
    let value;
    let evidence;
    if (slot && typeof slot === "object" && !Array.isArray(slot)) {
        value = cleanSlotText(slot.value);
        evidence = cleanSlotText(slot.evidence) || cleanSlotText(slot.quote);
    }
    else {
        value = cleanSlotText(slot);
        evidence = null;
    }
    if (!value && !evidence) {
        return makeScalarRawSlot();
    }
    if (!evidence) {
        evidence = value;
    }
    if (evidence && !evidenceInText(sourceText, evidence)) {
        const fallbackEvidence = value && evidenceInText(sourceText, value) ? value : null;
        if (!fallbackEvidence) {
            return makeScalarRawSlot();
        }
        evidence = fallbackEvidence;
    }
    if (!value) {
        value = evidence;
    }
    return makeScalarRawSlot(value, evidence);
}
function normalizeListRawSlots(items, sourceText) {
    if (items === null || items === undefined) {
        return [];
    }
    const list = Array.isArray(items) ? items : [items];
    const normalized = list
        .map((item) => normalizeScalarRawSlot(item, sourceText))
        .filter((slot) => Boolean(slot.value));
    const unique = [];
    const seen = new Set();
    for (const slot of normalized) {
        const key = `${String(slot.value || "").toLowerCase()}::${String(slot.evidence || "").toLowerCase()}`;
        if (seen.has(key)) {
            continue;
        }
        seen.add(key);
        unique.push(slot);
    }
    return unique;
}
function parseBool(value, defaultValue = false) {
    if (typeof value === "boolean") {
        return value;
    }
    const text = String(value || "").trim().toLowerCase();
    if (["true", "1", "yes"].includes(text)) {
        return true;
    }
    if (["false", "0", "no"].includes(text)) {
        return false;
    }
    return defaultValue;
}
function parseConfidence(value, defaultValue = 0) {
    const number = Number(value);
    if (!Number.isFinite(number)) {
        return defaultValue;
    }
    const normalized = number > 1 && number <= 100 ? number / 100 : number;
    return Math.round(Math.max(0, Math.min(normalized, 0.99)) * 100) / 100;
}
function normalizePriceNumber(value) {
    const number = Number(value);
    if (!Number.isFinite(number)) {
        return null;
    }
    if (Number.isInteger(number)) {
        return number;
    }
    return Math.round(number * 100) / 100;
}
function extractPriceConstraints(text) {
    let match = text.match(PRICE_RANGE_PATTERN);
    if (match) {
        return {
            price_min: normalizePriceNumber(match[1]),
            price_max: normalizePriceNumber(match[2]),
            price_target: null,
        };
    }
    match = text.match(PRICE_TARGET_PATTERN);
    if (match) {
        return {
            price_min: null,
            price_max: null,
            price_target: normalizePriceNumber(match[1]),
        };
    }
    match = text.match(PRICE_MAX_PATTERN);
    if (match) {
        return {
            price_min: null,
            price_max: normalizePriceNumber(match[1]),
            price_target: null,
        };
    }
    match = text.match(PRICE_MIN_PATTERN);
    if (match) {
        return {
            price_min: normalizePriceNumber(match[1]),
            price_max: null,
            price_target: null,
        };
    }
    match = text.match(BUDGET_PATTERN);
    if (match) {
        return {
            price_min: null,
            price_max: null,
            price_target: normalizePriceNumber(match[1]),
        };
    }
    return { price_min: null, price_max: null, price_target: null };
}
function normalizeBrandValue(value, evidence) {
    for (const candidate of [evidence, value]) {
        if (!candidate) {
            continue;
        }
        const candidateLower = candidate.toLowerCase();
        for (const [alias, canonical] of Object.entries(BRAND_ALIASES)) {
            if (alias.toLowerCase() === candidateLower) {
                return canonical;
            }
        }
    }
    return value || evidence || null;
}
function normalizePlatformHintValue(value, evidence) {
    for (const candidate of [value, evidence]) {
        const cleaned = cleanSlotText(candidate);
        if (!cleaned) {
            continue;
        }
        if (PLATFORM_HINTS[cleaned]) {
            return PLATFORM_HINTS[cleaned];
        }
        const lowered = cleaned.toLowerCase();
        if (["taobao", "jd", "pdd"].includes(lowered)) {
            return lowered;
        }
    }
    return null;
}
function extractMappedValue(text, hintPairs) {
    for (const [rawHint, normalized] of hintPairs) {
        if (text.includes(rawHint)) {
            return normalized;
        }
    }
    return null;
}
function extractCrowd(text) {
    return extractMappedValue(text, CROWD_HINTS);
}
function extractUsageScene(text) {
    return extractMappedValue(text, USAGE_SCENE_HINTS);
}
function extractGiftTarget(text) {
    return extractMappedValue(text, GIFT_TARGET_HINTS);
}
function extractSortHint(text) {
    return extractMappedValue(text, SORT_HINTS);
}
function sortValuesByPosition(sourceText, values) {
    const unique = dedupePreserveOrder(values || []);
    return unique
        .map((value) => ({
        index: sourceText.indexOf(value),
        weight: -value.length,
        value,
    }))
        .sort((a, b) => {
        const indexA = a.index >= 0 ? a.index : 10 ** 9;
        const indexB = b.index >= 0 ? b.index : 10 ** 9;
        if (indexA !== indexB) {
            return indexA - indexB;
        }
        return a.weight - b.weight;
    })
        .map((item) => item.value);
}
function dropSubstringValues(values) {
    const filtered = [];
    const unique = dedupePreserveOrder(values || []);
    for (const value of unique) {
        if (value.length === 1 && ["男", "女"].includes(value)) {
            continue;
        }
        if (unique.some((other) => value !== other && other.includes(value))) {
            continue;
        }
        filtered.push(value);
    }
    return filtered;
}
function choosePreferredText(modelValue, ruleValue, preferSpecific = false) {
    if (modelValue && ruleValue) {
        if (preferSpecific) {
            if (GENERIC_ONLY_TERMS.has(modelValue) && !GENERIC_ONLY_TERMS.has(ruleValue)) {
                return ruleValue;
            }
            if (ruleValue.length > modelValue.length && ruleValue.includes(modelValue)) {
                return ruleValue;
            }
        }
        return modelValue;
    }
    return modelValue || ruleValue || null;
}
function selectQueryAttributes(attributes) {
    const strong = (attributes || []).filter((value) => !LOW_PRIORITY_QUERY_ATTRIBUTES.has(value));
    return (strong.length ? strong : attributes || []).slice(0, 3);
}
function buildQueryCoreTokens(brand, sku, model, productName, category, attributes, specs) {
    const tokens = [];
    if (brand) {
        tokens.push(brand);
    }
    if (sku) {
        tokens.push(sku);
    }
    else if (model) {
        tokens.push(model);
    }
    if (productName) {
        tokens.push(productName);
    }
    else if (category) {
        tokens.push(category);
    }
    tokens.push(...selectQueryAttributes(attributes || []));
    if (specs?.length && !(sku || model)) {
        tokens.push(...specs.slice(0, 2));
    }
    else if (specs?.length) {
        tokens.push(...specs.slice(0, 1));
    }
    return dedupePreserveOrder(tokens);
}
function pickScalarEvidence(sourceText, selectedValue, ...slots) {
    if (!selectedValue) {
        return null;
    }
    const selectedKey = compactText(selectedValue);
    for (const slot of slots) {
        if (!slot || typeof slot !== "object") {
            continue;
        }
        const slotValue = cleanSlotText(slot.value);
        const slotEvidence = cleanSlotText(slot.evidence);
        if (slotValue && compactText(slotValue) === selectedKey) {
            return slotEvidence || slotValue;
        }
        if (slotEvidence && compactText(slotEvidence) === selectedKey) {
            return slotEvidence;
        }
    }
    return evidenceInText(sourceText, selectedValue) ? selectedValue : null;
}
function pickListEvidence(sourceText, values) {
    return dedupePreserveOrder((values || []).filter((value) => evidenceInText(sourceText, value)));
}
function buildProductSearchIntent(params) {
    const resolvedProductName = params.product_name || params.category;
    const resolvedQueryText = String(params.query_text || "").trim();
    const resolvedTokens = dedupePreserveOrder(params.query_tokens || []);
    return {
        success: Boolean(params.success && resolvedProductName && resolvedQueryText && resolvedTokens.length),
        intent_mode: params.intent_mode,
        query_text: resolvedQueryText,
        query_tokens: resolvedTokens,
        brand: params.brand ?? null,
        series: params.series ?? null,
        model: params.model ?? null,
        sku: params.sku ?? null,
        product_name: resolvedProductName,
        category: params.category ?? null,
        attributes: params.attributes || [],
        specs: params.specs || [],
        price_min: params.price_min ?? null,
        price_max: params.price_max ?? null,
        price_target: params.price_target ?? null,
        crowd: params.crowd ?? null,
        usage_scene: params.usage_scene ?? null,
        gift_target: params.gift_target ?? null,
        platform_hint: params.platform_hint ?? null,
        sort_hint: params.sort_hint ?? null,
        confidence: Math.round(Number(params.confidence || 0) * 100) / 100,
        evidence: params.evidence || {},
    };
}
function extractRuleSignals(cleanedText) {
    let [brand, brandAliases] = extractBrand(cleanedText);
    const [category, categoryAliases] = extractCategories(cleanedText);
    const [, attributeAliasesRaw] = extractAttributes(cleanedText);
    let attributeAliases = pruneSubstringAliases(attributeAliasesRaw, categoryAliases);
    attributeAliases = sortValuesByPosition(cleanedText, dropSubstringValues(attributeAliases));
    const specs = sortValuesByPosition(cleanedText, extractSpecs(cleanedText));
    const explicitSku = extractExplicitSku(cleanedText);
    let models = extractModels(cleanedText, specs);
    models = normalizeModels(models, brandAliases, brand);
    if (!brand) {
        const [guessedBrand, guessedAliases] = guessBrandFromPrefix(cleanedText, models, categoryAliases, attributeAliases);
        if (guessedBrand) {
            brand = guessedBrand;
            brandAliases = dedupePreserveOrder([...brandAliases, ...guessedAliases]);
        }
    }
    const model = models[0] || null;
    const budget = extractBudget(cleanedText);
    const platformHint = extractPlatformHint(cleanedText);
    const residualText = buildResidualText(cleanedText, brandAliases, categoryAliases, attributeAliases, models, specs, explicitSku, budget);
    const productName = deriveProductName(category, categoryAliases, residualText);
    return {
        brand,
        brand_aliases: brandAliases,
        category,
        category_aliases: categoryAliases,
        attribute_aliases: attributeAliases,
        specs,
        sku: explicitSku,
        models,
        model,
        budget,
        platform_hint: platformHint,
        product_name: productName,
    };
}
function buildRuleRawSlots(ruleSignals) {
    let productEvidence = ruleSignals.product_name;
    if ((ruleSignals.category_aliases || []).length) {
        productEvidence = ruleSignals.category_aliases[0];
    }
    return {
        brand: makeScalarRawSlot(ruleSignals.brand, ruleSignals.brand_aliases?.[0] || ruleSignals.brand),
        model: makeScalarRawSlot(ruleSignals.model, ruleSignals.model),
        sku: makeScalarRawSlot(ruleSignals.sku, ruleSignals.sku),
        product_name: makeScalarRawSlot(ruleSignals.product_name, productEvidence),
        category: makeScalarRawSlot(ruleSignals.category, ruleSignals.category_aliases?.[0] || ruleSignals.category),
        attributes: makeListRawSlots(ruleSignals.attribute_aliases || []),
        specs: makeListRawSlots(ruleSignals.specs || []),
        platform_hint: makeScalarRawSlot(ruleSignals.platform_hint, ruleSignals.platform_hint),
    };
}
function buildModelUserPrompt(rawMessage, cleanedText, ruleSignals) {
    const heuristicHint = {
        brand: ruleSignals.brand,
        model: ruleSignals.model,
        sku: ruleSignals.sku,
        product_name: ruleSignals.product_name,
        category: ruleSignals.category,
        attributes: ruleSignals.attribute_aliases,
        specs: ruleSignals.specs,
    };
    return [
        "请从下面的电商商品查询文本中抽取槽位。",
        "只返回 JSON 对象。",
        "如果是完整商品标题，也通常判定为精准搜索。",
        "品牌优先从标题前缀识别，例如“JR真维斯...”里的品牌是“JR真维斯”。",
        `原始消息: ${rawMessage}`,
        `清洗后消息: ${cleanedText}`,
        `启发式参考(仅供参考，原文优先): ${JSON.stringify(heuristicHint, undefined, 0)}`,
    ].join("\n");
}
async function callModelSlotExtractor(rawMessage, cleanedText, ruleSignals) {
    const response = await (0, common_1.requestModelJson)(MODEL_SLOT_SYSTEM_PROMPT, buildModelUserPrompt(rawMessage, cleanedText, ruleSignals), 0.1, 1200);
    const payload = response.json || {};
    return {
        slot_source: "model",
        model_provider: response.provider,
        model_name: response.model,
        is_precise_search: parseBool(payload.is_precise_search, false),
        confidence: parseConfidence(payload.confidence, 0),
        brand: normalizeScalarRawSlot(payload.brand, cleanedText),
        model: normalizeScalarRawSlot(payload.model, cleanedText),
        sku: normalizeScalarRawSlot(payload.sku, cleanedText),
        product_name: normalizeScalarRawSlot(payload.product_name, cleanedText),
        category: normalizeScalarRawSlot(payload.category, cleanedText),
        attributes: normalizeListRawSlots(payload.attributes, cleanedText),
        specs: normalizeListRawSlots(payload.specs, cleanedText),
        platform_hint: normalizeScalarRawSlot(payload.platform_hint, cleanedText),
    };
}
function getScalarSlotValue(slot) {
    if (!slot) {
        return null;
    }
    return cleanSlotText(slot.value);
}
function getListSlotValues(slots) {
    const values = [];
    for (const slot of slots || []) {
        const value = getScalarSlotValue(slot);
        if (value) {
            values.push(value);
        }
    }
    return dedupePreserveOrder(values);
}
function mergeModelAndRuleSlots(cleanedText, modelRawSlots, ruleSignals) {
    const ruleRawSlots = buildRuleRawSlots(ruleSignals);
    const activeRawSlots = modelRawSlots || {
        slot_source: "rule_fallback",
        model_provider: null,
        model_name: null,
        is_precise_search: false,
        confidence: 0,
        ...ruleRawSlots,
    };
    const brandValue = choosePreferredText(normalizeBrandValue(getScalarSlotValue(activeRawSlots.brand), activeRawSlots.brand?.evidence), normalizeBrandValue(getScalarSlotValue(ruleRawSlots.brand), ruleRawSlots.brand?.evidence));
    const modelValue = choosePreferredText(getScalarSlotValue(activeRawSlots.model), getScalarSlotValue(ruleRawSlots.model));
    const skuValue = choosePreferredText(getScalarSlotValue(activeRawSlots.sku), getScalarSlotValue(ruleRawSlots.sku));
    const productNameValue = choosePreferredText(getScalarSlotValue(activeRawSlots.product_name), getScalarSlotValue(ruleRawSlots.product_name), true);
    const categoryValue = choosePreferredText(getScalarSlotValue(activeRawSlots.category), getScalarSlotValue(ruleRawSlots.category), true);
    const platformHintValue = normalizePlatformHintValue(getScalarSlotValue(activeRawSlots.platform_hint), activeRawSlots.platform_hint?.evidence) ||
        ruleSignals.platform_hint;
    const attributes = sortValuesByPosition(cleanedText, dropSubstringValues([...getListSlotValues(activeRawSlots.attributes), ...(ruleSignals.attribute_aliases || [])]));
    const specs = sortValuesByPosition(cleanedText, [...getListSlotValues(activeRawSlots.specs), ...(ruleSignals.specs || [])]);
    const queryCoreTokens = buildQueryCoreTokens(brandValue, skuValue, modelValue, productNameValue, categoryValue, attributes, specs);
    const tokensAll = dedupePreserveOrder([brandValue, skuValue || modelValue, productNameValue, categoryValue !== productNameValue ? categoryValue : null]
        .filter(Boolean)).concat(attributes, specs);
    const tokens = dedupePreserveOrder(tokensAll);
    const queryCore = queryCoreTokens.join(" ").trim();
    const confidence = Math.max(parseConfidence(activeRawSlots.confidence, 0), calculateConfidence(brandValue, skuValue, modelValue, productNameValue, categoryValue, specs));
    const finalIsPreciseSearch = isPreciseSearch(brandValue, skuValue, modelValue, productNameValue, categoryValue, categoryValue ? [categoryValue] : [], attributes, cleanedText, ruleSignals.budget);
    const intentMode = finalIsPreciseSearch ? "precise" : "fuzzy";
    const crowdValue = extractCrowd(cleanedText);
    const usageSceneValue = extractUsageScene(cleanedText);
    const giftTargetValue = extractGiftTarget(cleanedText);
    const sortHintValue = extractSortHint(cleanedText);
    const priceConstraints = extractPriceConstraints(cleanedText);
    const productSearchIntent = buildProductSearchIntent({
        success: true,
        intent_mode: intentMode,
        query_text: queryCore,
        query_tokens: queryCoreTokens,
        brand: brandValue,
        series: null,
        model: modelValue,
        sku: skuValue,
        product_name: productNameValue,
        category: categoryValue,
        attributes,
        specs,
        price_min: priceConstraints.price_min,
        price_max: priceConstraints.price_max,
        price_target: priceConstraints.price_target,
        crowd: crowdValue,
        usage_scene: usageSceneValue,
        gift_target: giftTargetValue,
        sort_hint: sortHintValue,
        platform_hint: platformHintValue,
        confidence,
        evidence: {
            brand: pickScalarEvidence(cleanedText, brandValue, activeRawSlots.brand, ruleRawSlots.brand),
            series: null,
            model: pickScalarEvidence(cleanedText, modelValue, activeRawSlots.model, ruleRawSlots.model),
            sku: pickScalarEvidence(cleanedText, skuValue, activeRawSlots.sku, ruleRawSlots.sku),
            product_name: pickScalarEvidence(cleanedText, productNameValue, activeRawSlots.product_name, ruleRawSlots.product_name),
            category: pickScalarEvidence(cleanedText, categoryValue, activeRawSlots.category, ruleRawSlots.category),
            attributes: pickListEvidence(cleanedText, attributes),
            specs: pickListEvidence(cleanedText, specs),
            crowd: crowdValue && evidenceInText(cleanedText, crowdValue) ? crowdValue : null,
            usage_scene: usageSceneValue && evidenceInText(cleanedText, usageSceneValue) ? usageSceneValue : null,
            gift_target: giftTargetValue && evidenceInText(cleanedText, giftTargetValue) ? giftTargetValue : null,
        },
    });
    return {
        success: true,
        module: "precise-product-search",
        intent: "recognize_precise_product_search",
        next_action: "prepare_product_search",
        intent_mode: intentMode,
        slot_source: activeRawSlots.slot_source || "rule_fallback",
        model_provider: activeRawSlots.model_provider,
        model_name: activeRawSlots.model_name,
        is_precise_search: finalIsPreciseSearch,
        confidence: Math.round(confidence * 100) / 100,
        raw_slots: {
            brand: activeRawSlots.brand || makeScalarRawSlot(),
            product_name: activeRawSlots.product_name || makeScalarRawSlot(),
            model: activeRawSlots.model || makeScalarRawSlot(),
            sku: activeRawSlots.sku || makeScalarRawSlot(),
            category: activeRawSlots.category || makeScalarRawSlot(),
            attributes: activeRawSlots.attributes || [],
            specs: activeRawSlots.specs || [],
            platform_hint: activeRawSlots.platform_hint || makeScalarRawSlot(),
        },
        slots: {
            brand: brandValue,
            product_name: productNameValue,
            model: modelValue,
            sku: skuValue,
            specs,
            category: categoryValue,
            attributes,
            platform_hint: platformHintValue,
            budget: ruleSignals.budget,
            query_core: queryCore,
        },
        tokens_all: tokens,
        query_core_tokens: queryCoreTokens,
        tokens,
        product_search_intent: productSearchIntent,
        search_request: (0, productSearchProtocol_1.buildSearchRequest)(productSearchIntent),
        user_message: (0, productSearchProtocol_1.buildSearchReadyUserMessage)("商品搜索意图识别结果", "已识别到明确商品，可进入搜索", productSearchIntent),
    };
}
function shouldShortCircuitToFuzzy(cleanedText, ruleSignals) {
    if (ruleSignals.sku || ruleSignals.model) {
        return false;
    }
    if (ruleSignals.brand && (ruleSignals.product_name || ruleSignals.category)) {
        return false;
    }
    if (containsFuzzyMarker(cleanedText) && !(ruleSignals.brand || ruleSignals.sku || ruleSignals.model)) {
        return true;
    }
    return false;
}
function buildResidualText(text, brandAliases, categoryAliases, attributeAliases, models, specs, explicitSku, budget) {
    let residual = text;
    const removable = [...brandAliases, ...categoryAliases, ...attributeAliases, ...models, ...specs];
    if (explicitSku) {
        removable.push(explicitSku);
    }
    if (budget) {
        removable.push(budget);
    }
    for (const value of removable.sort((a, b) => b.length - a.length)) {
        if (!value) {
            continue;
        }
        residual = residual.replace(new RegExp(escapeRegExp(value), "gi"), " ");
    }
    for (const marker of Object.keys(PLATFORM_HINTS)) {
        residual = residual.replace(new RegExp(escapeRegExp(marker), "g"), " ");
    }
    residual = residual.replace(/(?:sku|SKU|型号|货号|款号|编码)\s*[:：]?/g, " ");
    return residual.replace(/\s+/g, " ").trim();
}
function deriveProductName(category, categoryAliases, residualText) {
    if (categoryAliases.length) {
        return categoryAliases[0];
    }
    const tokens = residualText.match(TOKEN_PATTERN) || [];
    const filtered = tokens.filter((token) => {
        const lowered = token.toLowerCase();
        if (Object.keys(PLATFORM_HINTS).map((value) => value.toLowerCase()).includes(lowered)) {
            return false;
        }
        if (token.length === 1 && /^[A-Za-z]$/.test(token)) {
            return false;
        }
        return true;
    });
    if (filtered.length) {
        return filtered.slice(0, 3).join(" ").trim();
    }
    return category;
}
function calculateConfidence(brand, sku, model, productName, category, specs) {
    let confidence = 0;
    if (sku) {
        confidence += 0.45;
    }
    if (model) {
        confidence += 0.4;
    }
    if (brand) {
        confidence += 0.25;
    }
    if (productName) {
        confidence += 0.2;
    }
    if (category) {
        confidence += 0.1;
    }
    if (specs?.length) {
        confidence += 0.05;
    }
    return Math.round(Math.min(confidence, 0.99) * 100) / 100;
}
function isPreciseSearch(brand, sku, model, productName, category, categoryAliases, attributeAliases, cleanedText, budget) {
    if (sku || model) {
        return true;
    }
    if (brand && (productName || category)) {
        return true;
    }
    if (productName &&
        category &&
        cleanedText.length >= 8 &&
        !containsFuzzyMarker(cleanedText) &&
        (categoryAliases.length >= 2 || attributeAliases.length >= 1)) {
        return true;
    }
    if (productName && !category && productName.length >= 6 && !containsFuzzyMarker(cleanedText)) {
        return true;
    }
    if (productName && GENERIC_ONLY_TERMS.has(productName)) {
        return false;
    }
    if (budget && !(brand || model || sku)) {
        return false;
    }
    if (containsFuzzyMarker(cleanedText) && !(brand || model || sku)) {
        return false;
    }
    return false;
}
function normalizeFuzzyProductName(productName, category, cleanedText) {
    if (category) {
        return category;
    }
    let normalized = cleanSlotText(productName) || "";
    if (cleanedText.includes("礼物")) {
        return "礼物";
    }
    normalized = normalized.replace(/^(?:适合|推荐个|推荐一款|推荐|帮我找|帮我选|找个|来个)\s*/, "");
    normalized = normalized.replace(/送给(?:女朋友|男朋友|老婆|老公|妈妈|爸爸|孩子|宝宝)(?:的)?/g, "");
    normalized = normalized.replace(LEADING_QUANTITY_PREFIX_PATTERN, "");
    normalized = normalized.trim();
    return normalized || productName || category;
}
function buildFuzzyIntentFromRuleSignals(cleanedText, ruleSignals, confidence = 0.45) {
    const attributes = ruleSignals.attribute_aliases || [];
    const specs = ruleSignals.specs || [];
    const category = ruleSignals.category;
    const crowdValue = extractCrowd(cleanedText);
    const usageSceneValue = extractUsageScene(cleanedText);
    const giftTargetValue = extractGiftTarget(cleanedText);
    const sortHintValue = extractSortHint(cleanedText);
    const productName = normalizeFuzzyProductName(ruleSignals.product_name, category, cleanedText);
    const priceConstraints = extractPriceConstraints(cleanedText);
    const queryTokens = dedupePreserveOrder([productName, ruleSignals.brand, usageSceneValue, giftTargetValue, crowdValue].filter(Boolean)).concat(selectQueryAttributes(attributes));
    const normalizedTokens = dedupePreserveOrder(queryTokens);
    return buildProductSearchIntent({
        success: true,
        intent_mode: "fuzzy",
        query_text: normalizedTokens.join(" ").trim(),
        query_tokens: normalizedTokens,
        brand: ruleSignals.brand,
        series: null,
        model: ruleSignals.model,
        sku: ruleSignals.sku,
        product_name: productName,
        category,
        attributes,
        specs,
        price_min: priceConstraints.price_min,
        price_max: priceConstraints.price_max,
        price_target: priceConstraints.price_target,
        crowd: crowdValue,
        usage_scene: usageSceneValue,
        gift_target: giftTargetValue,
        sort_hint: sortHintValue,
        platform_hint: ruleSignals.platform_hint,
        confidence,
        evidence: {
            brand: ruleSignals.brand ? ruleSignals.brand_aliases?.[0] || null : null,
            series: null,
            model: ruleSignals.model,
            sku: ruleSignals.sku,
            product_name: productName && evidenceInText(cleanedText, productName) ? productName : null,
            category: category && evidenceInText(cleanedText, category) ? category : null,
            attributes: pickListEvidence(cleanedText, attributes),
            specs: pickListEvidence(cleanedText, specs),
            crowd: crowdValue,
            usage_scene: usageSceneValue,
            gift_target: giftTargetValue,
        },
    });
}
function buildEmptyProductSearchIntent(intentMode = "fuzzy", confidence = 0) {
    return buildProductSearchIntent({
        success: false,
        intent_mode: intentMode,
        query_text: "",
        query_tokens: [],
        brand: null,
        series: null,
        model: null,
        sku: null,
        product_name: null,
        category: null,
        attributes: [],
        specs: [],
        price_min: null,
        price_max: null,
        price_target: null,
        crowd: null,
        usage_scene: null,
        gift_target: null,
        sort_hint: null,
        platform_hint: null,
        confidence,
        evidence: {},
    });
}
async function buildSuccessResponse(rawMessage) {
    const cleanedText = normalizeText(rawMessage);
    const ruleSignals = extractRuleSignals(cleanedText);
    let modelRawSlots = null;
    try {
        modelRawSlots = await callModelSlotExtractor(rawMessage, cleanedText, ruleSignals);
    }
    catch {
        modelRawSlots = null;
    }
    const merged = mergeModelAndRuleSlots(cleanedText, modelRawSlots, ruleSignals);
    if (!merged.is_precise_search) {
        return buildImpreciseResponse("FUZZY_SEARCH_LIKE", cleanedText, ruleSignals, merged);
    }
    return merged;
}
function buildImpreciseResponse(code = "FUZZY_SEARCH_LIKE", cleanedText, ruleSignals, merged) {
    let productSearchIntent = buildEmptyProductSearchIntent("fuzzy", 0.2);
    if (merged?.product_search_intent) {
        productSearchIntent = {
            ...merged.product_search_intent,
            intent_mode: "fuzzy",
            success: Boolean(merged.product_search_intent.product_name && merged.product_search_intent.query_text),
        };
    }
    else if (cleanedText !== undefined && ruleSignals) {
        productSearchIntent = buildFuzzyIntentFromRuleSignals(cleanedText, ruleSignals);
    }
    return {
        success: false,
        module: "precise-product-search",
        intent: "recognize_precise_product_search",
        next_action: "ask_for_precise_query",
        intent_mode: "fuzzy",
        is_precise_search: false,
        code,
        product_search_intent: productSearchIntent,
        search_request: (0, productSearchProtocol_1.buildSearchRequest)(productSearchIntent),
        user_message: [
            "商品搜索意图识别结果",
            "",
            "当前更像一般商品搜索需求，还缺少更明确的商品信息。",
            "请直接告诉我 品牌+型号 / 商品名 / SKU。",
            "例如：李宁 行川2SE、iPhone 15 Pro Max、A2698",
        ].join("\n"),
    };
}
function buildLinkLikeResponse() {
    const intent = buildEmptyProductSearchIntent("fuzzy", 0);
    return {
        success: false,
        module: "precise-product-search",
        intent: "recognize_precise_product_search",
        next_action: "route_to_m02",
        intent_mode: null,
        is_precise_search: false,
        code: "LINK_LIKE_MESSAGE",
        product_search_intent: intent,
        search_request: (0, productSearchProtocol_1.buildSearchRequest)(intent),
        user_message: "商品搜索意图识别结果\n\n当前消息更像商品链接，请按链接返利处理。",
    };
}
async function recognizeRawMessage(rawMessage) {
    const normalizedMessage = String(rawMessage || "").trim();
    if (!normalizedMessage) {
        return buildImpreciseResponse("EMPTY_QUERY");
    }
    if (exports.LINK_PATTERN.test(normalizedMessage)) {
        return buildLinkLikeResponse();
    }
    const cleanedText = normalizeText(normalizedMessage);
    const ruleSignals = extractRuleSignals(cleanedText);
    if (shouldShortCircuitToFuzzy(cleanedText, ruleSignals)) {
        return buildImpreciseResponse("FUZZY_SEARCH_LIKE", cleanedText, ruleSignals);
    }
    return await buildSuccessResponse(normalizedMessage);
}
async function main() {
    const rawMessage = process.argv[process.argv.indexOf("--raw-message") + 1];
    if (!rawMessage) {
        throw new Error("missing required option: --raw-message");
    }
    (0, common_1.printJson)(await recognizeRawMessage(rawMessage));
    return 0;
}
if (require.main === module) {
    main().then((code) => process.exit(code), (error) => {
        console.error(error instanceof Error ? error.message : String(error));
        process.exit(1);
    });
}
