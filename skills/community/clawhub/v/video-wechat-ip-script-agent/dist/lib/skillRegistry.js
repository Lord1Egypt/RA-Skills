"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getSupportedActions = getSupportedActions;
exports.validateOpenClawSkillRequest = validateOpenClawSkillRequest;
exports.dispatchSkillRequest = dispatchSkillRequest;
const checkCompliance_1 = require("../services/checkCompliance");
const generateScript_1 = require("../services/generateScript");
const generateTopics_1 = require("../services/generateTopics");
const rewriteStyle_1 = require("../services/rewriteStyle");
function assertNonEmptyString(value, fieldName) {
    if (typeof value !== "string" || !value.trim()) {
        throw new Error(`Invalid payload: "${fieldName}" must be a non-empty string.`);
    }
    return value.trim();
}
function isRecord(value) {
    return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}
function validateTopicsPayload(payload) {
    return {
        direction: assertNonEmptyString(payload.direction, "direction"),
        targetAudience: assertNonEmptyString(payload.targetAudience, "targetAudience"),
        industry: typeof payload.industry === "string" ? payload.industry : undefined,
        count: typeof payload.count === "number" ? payload.count : undefined,
        style: typeof payload.style === "string" ? payload.style : undefined,
        outputProfile: typeof payload.outputProfile === "string" ? payload.outputProfile : undefined,
    };
}
function validateScriptPayload(payload) {
    return {
        topic: assertNonEmptyString(payload.topic, "topic"),
        industry: typeof payload.industry === "string" ? payload.industry : undefined,
        targetAudience: typeof payload.targetAudience === "string" ? payload.targetAudience : undefined,
        style: typeof payload.style === "string" ? payload.style : undefined,
        scriptStructure: typeof payload.scriptStructure === "string" ? payload.scriptStructure : undefined,
        outputProfile: typeof payload.outputProfile === "string" ? payload.outputProfile : undefined,
        duration: payload.duration === 30 || payload.duration === 60 || payload.duration === 90 ? payload.duration : undefined,
        platform: typeof payload.platform === "string" ? payload.platform : undefined,
        includeShotList: typeof payload.includeShotList === "boolean" ? payload.includeShotList : undefined,
        includePublishCaption: typeof payload.includePublishCaption === "boolean" ? payload.includePublishCaption : undefined,
        includeCommentCTA: typeof payload.includeCommentCTA === "boolean" ? payload.includeCommentCTA : undefined,
    };
}
function validateRewritePayload(payload) {
    return {
        originalScript: assertNonEmptyString(payload.originalScript, "originalScript"),
        rewriteProfile: typeof payload.rewriteProfile === "string" ? payload.rewriteProfile : undefined,
        styles: Array.isArray(payload.styles)
            ? payload.styles.filter((item) => typeof item === "string" && Boolean(item.trim()))
            : undefined,
    };
}
function validateCompliancePayload(payload) {
    const title = typeof payload.title === "string" ? payload.title : undefined;
    const script = typeof payload.script === "string" ? payload.script : undefined;
    const caption = typeof payload.caption === "string" ? payload.caption : undefined;
    if (![title, script, caption].some((item) => item && item.trim())) {
        throw new Error('Invalid payload: compliance action requires at least one of "title", "script", or "caption".');
    }
    return {
        title,
        script,
        caption,
        outputProfile: typeof payload.outputProfile === "string" ? payload.outputProfile : undefined,
    };
}
const registry = {
    topics: {
        action: "topics",
        validate: validateTopicsPayload,
        run: generateTopics_1.generateTopics,
    },
    script: {
        action: "script",
        validate: validateScriptPayload,
        run: generateScript_1.generateScript,
    },
    rewrite: {
        action: "rewrite",
        validate: validateRewritePayload,
        run: rewriteStyle_1.rewriteStyle,
    },
    compliance: {
        action: "compliance",
        validate: validateCompliancePayload,
        run: checkCompliance_1.checkCompliance,
    },
};
function getSupportedActions() {
    return Object.keys(registry);
}
function validateOpenClawSkillRequest(input) {
    if (!isRecord(input)) {
        throw new Error("Invalid request: expected a JSON object.");
    }
    const action = input.action;
    if (typeof action !== "string" || !(action in registry)) {
        throw new Error(`Invalid action. Expected one of: ${getSupportedActions().join(", ")}.`);
    }
    const payload = input.payload;
    if (!isRecord(payload)) {
        throw new Error("Invalid request: \"payload\" must be a JSON object.");
    }
    const definition = registry[action];
    return {
        action: definition.action,
        payload: definition.validate(payload),
    };
}
async function dispatchSkillRequest(request, invoker) {
    const definition = registry[request.action];
    return definition.run(request.payload, invoker);
}
