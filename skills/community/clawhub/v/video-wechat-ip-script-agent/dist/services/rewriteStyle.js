"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.rewriteStyle = rewriteStyle;
const promptBuilder_1 = require("../lib/promptBuilder");
const outputParser_1 = require("../lib/outputParser");
const rewriteOutput_1 = require("../lib/rewriteOutput");
async function rewriteStyle(input, invokeModel) {
    const profile = (0, rewriteOutput_1.resolveRewriteProfile)(input.rewriteProfile);
    const styles = input.styles ?? profile.styles;
    const prompt = (0, promptBuilder_1.buildPrompt)({
        taskPromptFile: "style-rewriter.md",
        variables: {
            originalScript: input.originalScript,
            rewriteProfile: input.rewriteProfile ?? "default_rewrite",
            targetStyles: styles,
            outputFields: profile.fields,
            outputRequirement: (0, rewriteOutput_1.buildRewriteOutputRequirement)(profile.fields),
        },
    });
    const raw = await invokeModel(prompt);
    const parsed = (0, outputParser_1.safeJsonParse)(raw);
    return (0, rewriteOutput_1.normalizeRewriteOutput)(parsed, styles, input.originalScript);
}
