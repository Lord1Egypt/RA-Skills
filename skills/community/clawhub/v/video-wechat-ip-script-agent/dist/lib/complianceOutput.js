"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.resolveComplianceOutputFields = resolveComplianceOutputFields;
exports.buildComplianceOutputRequirement = buildComplianceOutputRequirement;
exports.normalizeComplianceOutput = normalizeComplianceOutput;
exports.pruneComplianceOutput = pruneComplianceOutput;
const fallback_1 = require("./fallback");
const configLoader_1 = require("./configLoader");
const outputParser_1 = require("./outputParser");
const DEFAULT_COMPLIANCE_PROFILE = "full_compliance";
function resolveComplianceOutputFields(outputProfile = DEFAULT_COMPLIANCE_PROFILE) {
    const profiles = (0, configLoader_1.loadJsonConfig)("compliance-output-profiles.json");
    const profile = profiles[outputProfile] ?? profiles[DEFAULT_COMPLIANCE_PROFILE];
    return profile.fields;
}
function buildComplianceOutputRequirement(fields) {
    return `请只返回 JSON 对象，字段必须为 ${fields.join(",")}。`;
}
function normalizeComplianceOutput(raw) {
    const rawIssues = Array.isArray(raw.issues) ? raw.issues : [];
    const issues = rawIssues.map((item) => {
        const record = (item ?? {});
        return {
            originalText: String(record.originalText ?? "").trim(),
            riskType: String(record.riskType ?? "").trim(),
            reason: String(record.reason ?? "").trim(),
            suggestion: String(record.suggestion ?? "").trim(),
        };
    }).filter((item) => item.originalText || item.riskType || item.reason || item.suggestion);
    return (0, fallback_1.applyComplianceFallback)({
        issues,
        revisedVersion: String(raw.revisedVersion ?? "").trim(),
        safeTitles: (0, outputParser_1.normalizeStringArray)(raw.safeTitles),
        safeCaption: String(raw.safeCaption ?? "").trim(),
    });
}
function pruneComplianceOutput(output, fields) {
    const fieldSet = new Set(fields);
    return {
        ...(fieldSet.has("issues") ? { issues: output.issues } : {}),
        ...(fieldSet.has("revisedVersion") ? { revisedVersion: output.revisedVersion } : {}),
        ...(fieldSet.has("safeTitles") ? { safeTitles: output.safeTitles } : {}),
        ...(fieldSet.has("safeCaption") ? { safeCaption: output.safeCaption } : {}),
    };
}
