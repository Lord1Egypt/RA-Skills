"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.resolveTopicOutputFields = resolveTopicOutputFields;
exports.buildTopicOutputRequirement = buildTopicOutputRequirement;
exports.normalizeTopicOutput = normalizeTopicOutput;
const fallback_1 = require("./fallback");
const configLoader_1 = require("./configLoader");
const DEFAULT_TOPIC_OUTPUT_PROFILE = "default_topics";
function resolveTopicOutputFields(outputProfile = DEFAULT_TOPIC_OUTPUT_PROFILE) {
    const profiles = (0, configLoader_1.loadJsonConfig)("topic-output-profiles.json");
    const profile = profiles[outputProfile] ?? profiles[DEFAULT_TOPIC_OUTPUT_PROFILE];
    return profile.fields;
}
function buildTopicOutputRequirement(fields) {
    return `请只返回 JSON 数组，每个元素包含 ${fields.join(", ")}。`;
}
function normalizeTopicOutput(raw, targetAudience) {
    return (0, fallback_1.applyTopicFallback)(raw, targetAudience);
}
