"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.resolveRewriteProfile = resolveRewriteProfile;
exports.buildRewriteOutputRequirement = buildRewriteOutputRequirement;
exports.normalizeRewriteOutput = normalizeRewriteOutput;
const configLoader_1 = require("./configLoader");
const DEFAULT_REWRITE_PROFILE = "default_rewrite";
function resolveRewriteProfile(profileName = DEFAULT_REWRITE_PROFILE) {
    const profiles = (0, configLoader_1.loadJsonConfig)("rewrite-profiles.json");
    return profiles[profileName] ?? profiles[DEFAULT_REWRITE_PROFILE];
}
function buildRewriteOutputRequirement(fields) {
    return `请只返回 JSON 数组，每个元素包含 ${fields.join(" 与 ")}。`;
}
function normalizeRewriteOutput(parsed, styles, originalScript) {
    if (parsed && parsed.length > 0)
        return parsed;
    return styles.map((style) => ({
        style,
        content: originalScript,
    }));
}
