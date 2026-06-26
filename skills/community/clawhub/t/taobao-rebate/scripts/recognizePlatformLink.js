"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.extractLinks = extractLinks;
exports.normalizeHost = normalizeHost;
exports.detectPlatform = detectPlatform;
exports.detectCarrierType = detectCarrierType;
exports.recognizeRawMessage = recognizeRawMessage;
const URL_PATTERN = /https?:\/\/[^\s]+/gi;
const TRAILING_PUNCTUATION = /["'”’」】〉》),，。；;！？!?]+$/;
const TAOBAO_DOMAINS = new Set([
    "e.tb.cn",
    "taobao.com",
    "tmall.com",
    "traveldetail.fliggy.com",
    "detail.liangxinyao.com",
    "dataoke.com",
]);
const JD_DOMAINS = new Set([
    "3.cn",
    "u.jd.com",
    "item.jd.com",
    "jingfen.jd.com",
    "pro.m.jd.com",
    "jd.com",
    "jd.hk",
    "jingtuitui.com",
]);
const PDD_DOMAINS = new Set([
    "yangkeduo.com",
    "pinduoduo.com",
    "p.pinduoduo.com",
    "p.pindoduo.com",
]);
const PLATFORM_LABELS = {
    taobao: "淘宝",
    jd: "京东",
    pdd: "拼多多",
    unknown: "未知",
};
const SHORT_LINK_HOSTS = new Set(["e.tb.cn", "3.cn", "u.jd.com", "p.pinduoduo.com", "p.pindoduo.com"]);
function extractLinks(rawMessage) {
    const matches = String(rawMessage || "").match(URL_PATTERN) || [];
    return matches
        .map((match) => match.replace(TRAILING_PUNCTUATION, ""))
        .filter(Boolean);
}
function normalizeHost(hostname) {
    let host = String(hostname || "").trim().toLowerCase();
    if (host.startsWith("www.")) {
        host = host.slice(4);
    }
    return host;
}
function matchesDomain(host, domain) {
    return host === domain || host.endsWith(`.${domain}`);
}
function detectPlatformFromHost(host) {
    for (const domain of TAOBAO_DOMAINS) {
        if (matchesDomain(host, domain)) {
            return "taobao";
        }
    }
    for (const domain of JD_DOMAINS) {
        if (matchesDomain(host, domain)) {
            return "jd";
        }
    }
    for (const domain of PDD_DOMAINS) {
        if (matchesDomain(host, domain)) {
            return "pdd";
        }
    }
    return "unknown";
}
function detectPlatform(link) {
    try {
        const host = normalizeHost(new URL(link).hostname);
        const platform = detectPlatformFromHost(host);
        return { platform, isSupported: platform !== "unknown" };
    }
    catch {
        return { platform: "unknown", isSupported: false };
    }
}
function detectCarrierType(rawMessage, link) {
    const stripped = String(rawMessage || "").trim();
    if (stripped === link) {
        try {
            const host = normalizeHost(new URL(link).hostname);
            if (SHORT_LINK_HOSTS.has(host)) {
                return "short_link";
            }
        }
        catch {
            return "unknown";
        }
        return "direct_link";
    }
    return "mixed_text";
}
function buildSuccessResponse(rawMessage, link) {
    const { platform, isSupported } = detectPlatform(link);
    const carrierType = detectCarrierType(rawMessage, link);
    return {
        success: true,
        module: "platform-link-recognition",
        intent: "recognize_platform_link",
        next_action: "return_link_info",
        platform,
        original_link: link,
        carrier_type: carrierType,
        is_supported: isSupported,
        payload: {
            platform,
            link,
        },
        user_message: `链接识别结果\n\n平台：${PLATFORM_LABELS[platform] || "未知"}\n链接：${link}`,
    };
}
function buildMultipleSuccessResponse(rawMessage, links) {
    const results = [];
    const lines = ["链接识别结果"];
    links.forEach((link, index) => {
        const { platform, isSupported } = detectPlatform(link);
        const carrierType = detectCarrierType(rawMessage, link);
        results.push({
            platform,
            original_link: link,
            carrier_type: carrierType,
            is_supported: isSupported,
        });
        lines.push("", `${index + 1}. 平台：${PLATFORM_LABELS[platform] || "未知"}`, `链接：${link}`);
    });
    const allSupported = results.every((item) => item.is_supported);
    return {
        success: allSupported,
        module: "platform-link-recognition",
        intent: "recognize_platform_link",
        next_action: allSupported ? "return_link_info" : "ask_for_supported_link",
        platform: "multiple",
        original_link: null,
        carrier_type: "mixed_text",
        is_supported: allSupported,
        payload: { results },
        user_message: lines.join("\n"),
    };
}
function buildUnknownResponse(link, code = "UNSUPPORTED_LINK") {
    const lines = [
        "这个链接我暂时还不能处理。",
        "",
        "目前只支持淘宝、京东、拼多多的商品链接、短链或口令返利。",
        "",
        "你可以直接把这 3 个平台的商品详情页链接发给我，我来帮你转成返利链接。",
    ];
    if (link) {
        lines.push("", `你刚发的链接：${link}`);
    }
    return {
        success: false,
        module: "platform-link-recognition",
        intent: "recognize_platform_link",
        next_action: "ask_for_supported_link",
        platform: "unknown",
        original_link: link || null,
        carrier_type: "unknown",
        is_supported: false,
        code,
        payload: {
            platform: "unknown",
            link: link || null,
        },
        user_message: lines.join("\n"),
    };
}
function recognizeRawMessage(rawMessage) {
    const normalizedMessage = String(rawMessage || "").trim();
    const links = extractLinks(normalizedMessage);
    if (!links.length) {
        return buildUnknownResponse(undefined, "NO_LINK_FOUND");
    }
    if (links.length > 1) {
        return buildMultipleSuccessResponse(normalizedMessage, links);
    }
    const link = links[0];
    const { isSupported } = detectPlatform(link);
    if (!isSupported) {
        return buildUnknownResponse(link);
    }
    return buildSuccessResponse(normalizedMessage, link);
}
