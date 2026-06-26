"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.generateTopics = generateTopics;
const promptBuilder_1 = require("../lib/promptBuilder");
const outputParser_1 = require("../lib/outputParser");
const topicOutput_1 = require("../lib/topicOutput");
async function generateTopics(input, invokeModel) {
    const outputFields = (0, topicOutput_1.resolveTopicOutputFields)(input.outputProfile);
    const prompt = (0, promptBuilder_1.buildPrompt)({
        taskPromptFile: "topic-generator.md",
        variables: {
            industry: input.industry ?? "医美",
            direction: input.direction,
            targetAudience: input.targetAudience,
            count: input.count ?? 10,
            style: input.style ?? "观点型",
            outputProfile: input.outputProfile ?? "default_topics",
            outputFields,
            outputRequirement: (0, topicOutput_1.buildTopicOutputRequirement)(outputFields),
        },
    });
    const raw = await invokeModel(prompt);
    const parsed = (0, outputParser_1.safeJsonParse)(raw) ?? [];
    return (0, topicOutput_1.normalizeTopicOutput)(parsed, input.targetAudience);
}
