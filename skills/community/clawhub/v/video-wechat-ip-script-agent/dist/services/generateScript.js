"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.generateScript = generateScript;
const promptBuilder_1 = require("../lib/promptBuilder");
const outputParser_1 = require("../lib/outputParser");
const scriptOutput_1 = require("../lib/scriptOutput");
async function generateScript(input, invokeModel) {
    const outputFields = (0, scriptOutput_1.resolveScriptOutputFields)({
        outputProfile: input.outputProfile,
        includeShotList: input.includeShotList,
        includePublishCaption: input.includePublishCaption,
        includeCommentCTA: input.includeCommentCTA,
    });
    const prompt = (0, promptBuilder_1.buildPrompt)({
        taskPromptFile: "script-generator.md",
        variables: {
            topic: input.topic,
            industry: input.industry ?? "医美",
            targetAudience: input.targetAudience ?? "医美老板",
            style: input.style ?? "老板表达型",
            scriptStructure: input.scriptStructure ?? "wechat_core_v1",
            outputProfile: input.outputProfile ?? "full_publish_pack",
            outputFields,
            duration: input.duration ?? 60,
            platform: input.platform ?? "wechat_video",
            includeShotList: input.includeShotList ?? true,
            includePublishCaption: input.includePublishCaption ?? true,
            includeCommentCTA: input.includeCommentCTA ?? true,
            outputRequirement: (0, scriptOutput_1.buildScriptOutputRequirement)(outputFields),
        },
    });
    const raw = await invokeModel(prompt);
    const parsed = (0, outputParser_1.safeJsonParse)(raw) ?? {};
    const normalized = (0, scriptOutput_1.normalizeScriptOutput)(parsed, input.topic);
    return (0, scriptOutput_1.pruneScriptOutput)(normalized, outputFields);
}
