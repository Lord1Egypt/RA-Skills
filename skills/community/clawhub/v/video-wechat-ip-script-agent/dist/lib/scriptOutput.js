"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.resolveScriptOutputFields = resolveScriptOutputFields;
exports.buildScriptOutputRequirement = buildScriptOutputRequirement;
exports.normalizeScriptOutput = normalizeScriptOutput;
exports.pruneScriptOutput = pruneScriptOutput;
const fallback_1 = require("./fallback");
const configLoader_1 = require("./configLoader");
const outputParser_1 = require("./outputParser");
const DEFAULT_OUTPUT_PROFILE = "full_publish_pack";
function resolveScriptOutputFields(options = {}) {
    const profiles = (0, configLoader_1.loadJsonConfig)("script-output-profiles.json", options.rootDir);
    const profileName = options.outputProfile ?? DEFAULT_OUTPUT_PROFILE;
    const profile = profiles[profileName] ?? profiles[DEFAULT_OUTPUT_PROFILE];
    const fields = new Set(profile.fields);
    if (options.includeShotList === false)
        fields.delete("shotList");
    if (options.includePublishCaption === false)
        fields.delete("publishCaption");
    if (options.includeCommentCTA === false)
        fields.delete("commentCTA");
    return Array.from(fields);
}
function buildScriptOutputRequirement(fields) {
    return `请只返回 JSON 对象，字段必须为 ${fields.join(",")}。`;
}
function normalizeScriptOutput(raw, topic) {
    return (0, fallback_1.applyScriptFallback)({
        positioning: (0, outputParser_1.normalizeMultilineString)(raw.positioning),
        titles: (0, outputParser_1.normalizeStringArray)(raw.titles),
        hook: (0, outputParser_1.normalizeMultilineString)(raw.hook),
        script: (0, outputParser_1.normalizeMultilineString)(raw.script),
        shotList: (0, outputParser_1.normalizeStringArray)(raw.shotList),
        coverText: (0, outputParser_1.normalizeMultilineString)(raw.coverText),
        publishCaption: (0, outputParser_1.normalizeMultilineString)(raw.publishCaption),
        commentCTA: (0, outputParser_1.normalizeMultilineString)(raw.commentCTA),
    }, topic);
}
function pruneScriptOutput(output, fields) {
    const fieldSet = new Set(fields);
    return {
        ...(fieldSet.has("positioning") ? { positioning: output.positioning } : {}),
        ...(fieldSet.has("titles") ? { titles: output.titles } : {}),
        ...(fieldSet.has("hook") ? { hook: output.hook } : {}),
        ...(fieldSet.has("script") ? { script: output.script } : {}),
        ...(fieldSet.has("shotList") ? { shotList: output.shotList } : {}),
        ...(fieldSet.has("coverText") ? { coverText: output.coverText } : {}),
        ...(fieldSet.has("publishCaption") ? { publishCaption: output.publishCaption } : {}),
        ...(fieldSet.has("commentCTA") ? { commentCTA: output.commentCTA } : {}),
    };
}
