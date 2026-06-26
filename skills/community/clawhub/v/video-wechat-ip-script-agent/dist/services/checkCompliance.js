"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.checkCompliance = checkCompliance;
const promptBuilder_1 = require("../lib/promptBuilder");
const outputParser_1 = require("../lib/outputParser");
const complianceOutput_1 = require("../lib/complianceOutput");
async function checkCompliance(input, invokeModel) {
    const outputFields = (0, complianceOutput_1.resolveComplianceOutputFields)(input.outputProfile);
    const prompt = (0, promptBuilder_1.buildPrompt)({
        taskPromptFile: "compliance-checker.md",
        variables: {
            title: input.title ?? "",
            script: input.script ?? "",
            caption: input.caption ?? "",
            outputProfile: input.outputProfile ?? "full_compliance",
            outputFields,
            outputRequirement: (0, complianceOutput_1.buildComplianceOutputRequirement)(outputFields),
        },
    });
    const raw = await invokeModel(prompt);
    const parsed = (0, outputParser_1.safeJsonParse)(raw) ?? {};
    const normalized = (0, complianceOutput_1.normalizeComplianceOutput)(parsed);
    return (0, complianceOutput_1.pruneComplianceOutput)(normalized, outputFields);
}
