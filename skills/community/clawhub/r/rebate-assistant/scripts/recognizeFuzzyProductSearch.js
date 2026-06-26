"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.recognizeRawMessage = recognizeRawMessage;
exports.main = main;
const common_1 = require("./common");
const productSearchProtocol_1 = require("./productSearchProtocol");
const recognizePreciseProductSearch_1 = require("./recognizePreciseProductSearch");
const FUZZY_INTENT_SYSTEM_PROMPT = `
你是一个电商模糊商品意图抽取器。

你只能输出一个 JSON 对象，不能输出 markdown，不能输出解释。

抽取目标：
- is_fuzzy_search
- confidence
- brand
- product_name
- category
- attributes
- specs
- crowd
- usage_scene
- gift_target
- sort_hint
- platform_hint
- price_min
- price_max
- price_target

输出要求：
1. 标量槽位输出 {"value": ..., "evidence": ...}
2. attributes 和 specs 输出数组，元素格式为 {"value": ..., "evidence": ...}
3. price_min / price_max / price_target 输出 number 或 null
4. evidence 必须是原文中的原样片段，不能改写
5. 不确定就返回 null 或 []
6. 不允许编造品牌、价格、平台、人群、送礼对象
7. 这是模糊购物需求理解，不是明确 SKU/型号 搜索
8. 重点识别用户真正想买的商品，以及预算、人群、场景、送礼对象
`.trim();
function isFuzzySearchCandidate(cleanedText, ruleSignals) {
    const priceConstraints = (0, recognizePreciseProductSearch_1.extractPriceConstraints)(cleanedText);
    if ((0, recognizePreciseProductSearch_1.containsFuzzyMarker)(cleanedText)) {
        return true;
    }
    if ([priceConstraints.price_min, priceConstraints.price_max, priceConstraints.price_target].some((value) => value !== null && value !== undefined)) {
        return true;
    }
    if ([(0, recognizePreciseProductSearch_1.extractCrowd)(cleanedText), (0, recognizePreciseProductSearch_1.extractUsageScene)(cleanedText), (0, recognizePreciseProductSearch_1.extractGiftTarget)(cleanedText), (0, recognizePreciseProductSearch_1.extractSortHint)(cleanedText), (0, recognizePreciseProductSearch_1.extractPlatformHint)(cleanedText)].some(Boolean)) {
        return true;
    }
    if (ruleSignals.category || ruleSignals.product_name) {
        return true;
    }
    if ((ruleSignals.attribute_aliases || []).length) {
        return true;
    }
    return false;
}
function buildFuzzyModelUserPrompt(rawMessage, cleanedText, ruleSignals) {
    const heuristicHint = {
        brand: ruleSignals.brand,
        product_name: ruleSignals.product_name,
        category: ruleSignals.category,
        attributes: ruleSignals.attribute_aliases,
        specs: ruleSignals.specs,
        budget: ruleSignals.budget,
        platform_hint: ruleSignals.platform_hint,
    };
    return [
        "请从下面的模糊购物需求中抽取商品意图。",
        "只返回 JSON 对象。",
        "尽量识别用户真正想买的商品，不要把动作词、语气词、量词当成商品本身。",
        `原始消息: ${rawMessage}`,
        `清洗后消息: ${cleanedText}`,
        `启发式参考(仅供参考，原文优先): ${JSON.stringify(heuristicHint, undefined, 0)}`,
    ].join("\n");
}
async function callModelFuzzyIntentExtractor(rawMessage, cleanedText, ruleSignals) {
    const response = await (0, common_1.requestModelJson)(FUZZY_INTENT_SYSTEM_PROMPT, buildFuzzyModelUserPrompt(rawMessage, cleanedText, ruleSignals), 0.1, 1200);
    const payload = response.json || {};
    return {
        slot_source: "model",
        model_provider: response.provider,
        model_name: response.model,
        is_fuzzy_search: (0, recognizePreciseProductSearch_1.parseBool)(payload.is_fuzzy_search, false),
        confidence: (0, recognizePreciseProductSearch_1.parseConfidence)(payload.confidence, 0),
        brand: (0, recognizePreciseProductSearch_1.normalizeScalarRawSlot)(payload.brand, cleanedText),
        product_name: (0, recognizePreciseProductSearch_1.normalizeScalarRawSlot)(payload.product_name, cleanedText),
        category: (0, recognizePreciseProductSearch_1.normalizeScalarRawSlot)(payload.category, cleanedText),
        attributes: (0, recognizePreciseProductSearch_1.normalizeListRawSlots)(payload.attributes, cleanedText),
        specs: (0, recognizePreciseProductSearch_1.normalizeListRawSlots)(payload.specs, cleanedText),
        crowd: (0, recognizePreciseProductSearch_1.normalizeScalarRawSlot)(payload.crowd, cleanedText),
        usage_scene: (0, recognizePreciseProductSearch_1.normalizeScalarRawSlot)(payload.usage_scene, cleanedText),
        gift_target: (0, recognizePreciseProductSearch_1.normalizeScalarRawSlot)(payload.gift_target, cleanedText),
        sort_hint: (0, recognizePreciseProductSearch_1.normalizeScalarRawSlot)(payload.sort_hint, cleanedText),
        platform_hint: (0, recognizePreciseProductSearch_1.normalizeScalarRawSlot)(payload.platform_hint, cleanedText),
        price_min: (0, recognizePreciseProductSearch_1.normalizePriceNumber)(payload.price_min),
        price_max: (0, recognizePreciseProductSearch_1.normalizePriceNumber)(payload.price_max),
        price_target: (0, recognizePreciseProductSearch_1.normalizePriceNumber)(payload.price_target),
    };
}
function mergeModelAndRuleFuzzyIntent(cleanedText, ruleSignals, modelSlots) {
    const ruleIntent = (0, recognizePreciseProductSearch_1.buildFuzzyIntentFromRuleSignals)(cleanedText, ruleSignals);
    if (!modelSlots) {
        return [ruleIntent, "rule_fallback", null, null];
    }
    const brandValue = (0, recognizePreciseProductSearch_1.choosePreferredText)((0, recognizePreciseProductSearch_1.normalizeBrandValue)((0, recognizePreciseProductSearch_1.getScalarSlotValue)(modelSlots.brand), modelSlots.brand?.evidence), ruleIntent.brand);
    const categoryValue = (0, recognizePreciseProductSearch_1.choosePreferredText)((0, recognizePreciseProductSearch_1.getScalarSlotValue)(modelSlots.category), ruleIntent.category, true);
    const productNameValue = (0, recognizePreciseProductSearch_1.normalizeFuzzyProductName)((0, recognizePreciseProductSearch_1.choosePreferredText)((0, recognizePreciseProductSearch_1.getScalarSlotValue)(modelSlots.product_name), ruleIntent.product_name, true), categoryValue, cleanedText);
    const attributes = (0, recognizePreciseProductSearch_1.sortValuesByPosition)(cleanedText, (0, recognizePreciseProductSearch_1.dropSubstringValues)([...(0, recognizePreciseProductSearch_1.getListSlotValues)(modelSlots.attributes), ...(ruleIntent.attributes || [])]));
    const specs = (0, recognizePreciseProductSearch_1.sortValuesByPosition)(cleanedText, [...(0, recognizePreciseProductSearch_1.getListSlotValues)(modelSlots.specs), ...(ruleIntent.specs || [])]);
    const crowdValue = (0, recognizePreciseProductSearch_1.getScalarSlotValue)(modelSlots.crowd) || ruleIntent.crowd;
    const usageSceneValue = (0, recognizePreciseProductSearch_1.getScalarSlotValue)(modelSlots.usage_scene) || ruleIntent.usage_scene;
    const giftTargetValue = (0, recognizePreciseProductSearch_1.getScalarSlotValue)(modelSlots.gift_target) || ruleIntent.gift_target;
    const sortHintValue = (0, recognizePreciseProductSearch_1.getScalarSlotValue)(modelSlots.sort_hint) || ruleIntent.sort_hint;
    const platformHintValue = (0, recognizePreciseProductSearch_1.normalizePlatformHintValue)((0, recognizePreciseProductSearch_1.getScalarSlotValue)(modelSlots.platform_hint), modelSlots.platform_hint?.evidence) ||
        ruleIntent.platform_hint;
    const queryTokens = (0, recognizePreciseProductSearch_1.dedupePreserveOrder)([productNameValue, brandValue, usageSceneValue, giftTargetValue, crowdValue].filter(Boolean)).concat((0, recognizePreciseProductSearch_1.selectQueryAttributes)(attributes));
    const normalizedQueryTokens = (0, recognizePreciseProductSearch_1.dedupePreserveOrder)(queryTokens);
    const queryText = normalizedQueryTokens.join(" ").trim();
    const intent = (0, recognizePreciseProductSearch_1.buildProductSearchIntent)({
        success: true,
        intent_mode: "fuzzy",
        query_text: queryText,
        query_tokens: normalizedQueryTokens,
        brand: brandValue,
        series: null,
        model: ruleIntent.model,
        sku: ruleIntent.sku,
        product_name: productNameValue,
        category: categoryValue,
        attributes,
        specs,
        price_min: modelSlots.price_min ?? ruleIntent.price_min,
        price_max: modelSlots.price_max ?? ruleIntent.price_max,
        price_target: modelSlots.price_target ?? ruleIntent.price_target,
        crowd: crowdValue,
        usage_scene: usageSceneValue,
        gift_target: giftTargetValue,
        sort_hint: sortHintValue,
        platform_hint: platformHintValue,
        confidence: Math.max(ruleIntent.confidence || 0, (0, recognizePreciseProductSearch_1.parseConfidence)(modelSlots.confidence, 0)),
        evidence: {
            brand: (0, recognizePreciseProductSearch_1.pickScalarEvidence)(cleanedText, brandValue, modelSlots.brand) || ruleIntent.evidence?.brand,
            series: null,
            model: ruleIntent.evidence?.model,
            sku: ruleIntent.evidence?.sku,
            product_name: (0, recognizePreciseProductSearch_1.pickScalarEvidence)(cleanedText, productNameValue, modelSlots.product_name) || ruleIntent.evidence?.product_name,
            category: (0, recognizePreciseProductSearch_1.pickScalarEvidence)(cleanedText, categoryValue, modelSlots.category) || ruleIntent.evidence?.category,
            attributes: (0, recognizePreciseProductSearch_1.pickListEvidence)(cleanedText, attributes),
            specs: (0, recognizePreciseProductSearch_1.pickListEvidence)(cleanedText, specs),
            crowd: (0, recognizePreciseProductSearch_1.pickScalarEvidence)(cleanedText, crowdValue, modelSlots.crowd) || (crowdValue && (0, recognizePreciseProductSearch_1.evidenceInText)(cleanedText, crowdValue) ? crowdValue : null),
            usage_scene: (0, recognizePreciseProductSearch_1.pickScalarEvidence)(cleanedText, usageSceneValue, modelSlots.usage_scene) || (usageSceneValue && (0, recognizePreciseProductSearch_1.evidenceInText)(cleanedText, usageSceneValue) ? usageSceneValue : null),
            gift_target: (0, recognizePreciseProductSearch_1.pickScalarEvidence)(cleanedText, giftTargetValue, modelSlots.gift_target) || (giftTargetValue && (0, recognizePreciseProductSearch_1.evidenceInText)(cleanedText, giftTargetValue) ? giftTargetValue : null),
        },
    });
    return [intent, modelSlots.slot_source || "model", modelSlots.model_provider || null, modelSlots.model_name || null];
}
async function buildSuccessResponse(rawMessage, cleanedText, ruleSignals) {
    let modelSlots = null;
    try {
        modelSlots = await callModelFuzzyIntentExtractor(rawMessage, cleanedText, ruleSignals);
    }
    catch {
        modelSlots = null;
    }
    const [intent, slotSource, modelProvider, modelName] = mergeModelAndRuleFuzzyIntent(cleanedText, ruleSignals, modelSlots);
    const searchRequest = (0, productSearchProtocol_1.buildSearchRequest)(intent);
    return {
        success: true,
        module: "fuzzy-product-search",
        intent: "recognize_fuzzy_product_search",
        next_action: "prepare_product_search",
        intent_mode: "fuzzy",
        is_fuzzy_search: true,
        slot_source: slotSource,
        model_provider: modelProvider,
        model_name: modelName,
        product_search_intent: intent,
        search_request: searchRequest,
        user_message: (0, productSearchProtocol_1.buildSearchReadyUserMessage)("商品搜索意图识别结果", "已识别到商品搜索需求，可进入搜索", intent),
    };
}
function buildImpreciseResponse() {
    const intent = (0, recognizePreciseProductSearch_1.buildEmptyProductSearchIntent)("fuzzy", 0.2);
    return {
        success: false,
        module: "fuzzy-product-search",
        intent: "recognize_fuzzy_product_search",
        next_action: "ask_for_fuzzy_query",
        intent_mode: "fuzzy",
        is_fuzzy_search: false,
        code: "INSUFFICIENT_FUZZY_SIGNAL",
        product_search_intent: intent,
        search_request: (0, productSearchProtocol_1.buildSearchRequest)(intent),
        user_message: [
            "商品搜索意图识别结果",
            "",
            "当前还没识别到明确的购物需求。",
            "请直接告诉我 想买什么 / 预算 / 用途 / 送给谁。",
            "例如：300 左右通勤耳机、适合送女朋友的礼物、100 以内儿童水杯",
        ].join("\n"),
    };
}
function buildPreciseLikeResponse() {
    const intent = (0, recognizePreciseProductSearch_1.buildEmptyProductSearchIntent)("precise", 0);
    return {
        success: false,
        module: "fuzzy-product-search",
        intent: "recognize_fuzzy_product_search",
        next_action: "route_to_m03",
        intent_mode: "precise",
        is_fuzzy_search: false,
        code: "PRECISE_SEARCH_LIKE",
        product_search_intent: intent,
        search_request: (0, productSearchProtocol_1.buildSearchRequest)(intent),
        user_message: "商品搜索意图识别结果\n\n当前消息更像明确商品搜索，请按商品搜索处理。",
    };
}
function buildLinkLikeResponse() {
    const intent = (0, recognizePreciseProductSearch_1.buildEmptyProductSearchIntent)("fuzzy", 0);
    return {
        success: false,
        module: "fuzzy-product-search",
        intent: "recognize_fuzzy_product_search",
        next_action: "route_to_m02",
        intent_mode: null,
        is_fuzzy_search: false,
        code: "LINK_LIKE_MESSAGE",
        product_search_intent: intent,
        search_request: (0, productSearchProtocol_1.buildSearchRequest)(intent),
        user_message: "商品搜索意图识别结果\n\n当前消息更像商品链接，请按链接返利处理。",
    };
}
async function recognizeRawMessage(rawMessage) {
    const normalizedMessage = String(rawMessage || "").trim();
    if (!normalizedMessage) {
        return buildImpreciseResponse();
    }
    if (recognizePreciseProductSearch_1.LINK_PATTERN.test(normalizedMessage)) {
        return buildLinkLikeResponse();
    }
    const cleanedText = (0, recognizePreciseProductSearch_1.normalizeText)(normalizedMessage);
    const ruleSignals = (0, recognizePreciseProductSearch_1.extractRuleSignals)(cleanedText);
    if ((0, recognizePreciseProductSearch_1.isPreciseSearch)(ruleSignals.brand, ruleSignals.sku, ruleSignals.model, ruleSignals.product_name, ruleSignals.category, ruleSignals.category_aliases || [], ruleSignals.attribute_aliases || [], cleanedText, ruleSignals.budget)) {
        return buildPreciseLikeResponse();
    }
    if (!isFuzzySearchCandidate(cleanedText, ruleSignals)) {
        return buildImpreciseResponse();
    }
    return await buildSuccessResponse(normalizedMessage, cleanedText, ruleSignals);
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
