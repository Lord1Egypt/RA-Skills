"use strict";
/**
 * Trace Compiler — converts a recorded OpenClaw session trace
 * into a reusable Lobster workflow.
 *
 * This is the core "one node explores, all nodes benefit" engine.
 * It takes the raw action history from a successful session and
 * compiles it into a parameterized, portable Lobster workflow.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.compileTrace = compileTrace;
const sanitizer_js_1 = require("./sanitizer.js");
function compileTrace(intentName, actions) {
    const steps = [];
    const collectedArgs = {};
    let stepIndex = 0;
    for (const action of actions) {
        // Skip failed actions — we only want the successful path
        if (!action.result.success)
            continue;
        // Skip non-browser actions (internal bookkeeping, etc.)
        if (!isBrowserAction(action))
            continue;
        // Sanitize args to strip PII and extract Lobster arguments
        const { sanitized, extractedArgs } = (0, sanitizer_js_1.sanitizeActionArgs)(action.args);
        // Register extracted args in the workflow args definition
        for (const [argName, argDef] of extractedArgs) {
            if (!collectedArgs[argName]) {
                collectedArgs[argName] = {
                    type: argDef.type,
                    required: true,
                };
            }
        }
        // Build the Lobster command string
        const command = buildCommand(action.tool, action.action, sanitized);
        const step = {
            id: `step_${stepIndex++}`,
            command,
            timeout_ms: inferTimeout(action),
        };
        // Merge consecutive waits
        if (steps.length > 0 && isWaitStep(step) && isWaitStep(steps[steps.length - 1])) {
            const prev = steps[steps.length - 1];
            prev.timeout_ms = (prev.timeout_ms || 1000) + (step.timeout_ms || 1000);
            continue;
        }
        steps.push(step);
    }
    // Optimize: remove trailing waits
    while (steps.length > 0 && isWaitStep(steps[steps.length - 1])) {
        steps.pop();
    }
    const workflow = {
        name: intentToWorkflowName(intentName),
        args: collectedArgs,
        steps,
    };
    return { workflow, argCount: Object.keys(collectedArgs).length };
}
function isBrowserAction(action) {
    const browserTools = [
        "browser.click",
        "browser.type",
        "browser.fill",
        "browser.select",
        "browser.check",
        "browser.navigate",
        "browser.scroll",
        "browser.wait",
        "browser.hover",
        "browser.press",
        "browser.evaluate",
    ];
    const fullAction = `${action.tool}.${action.action}`;
    return browserTools.some((bt) => fullAction.startsWith(bt));
}
function buildCommand(tool, action, args) {
    const argsStr = Object.entries(args)
        .map(([k, v]) => {
        if (typeof v === "string")
            return `${k}="${v}"`;
        return `${k}=${v}`;
    })
        .join(" ");
    return `openclaw.invoke ${tool}.${action} ${argsStr}`.trim();
}
function inferTimeout(action) {
    const actionName = `${action.tool}.${action.action}`;
    if (actionName.includes("navigate"))
        return 10000;
    if (actionName.includes("wait"))
        return 5000;
    if (actionName.includes("click"))
        return 3000;
    if (actionName.includes("type") || actionName.includes("fill"))
        return 2000;
    return 3000;
}
function isWaitStep(step) {
    return step.command.includes("browser.wait");
}
function intentToWorkflowName(intent) {
    return intent
        .toLowerCase()
        .replace(/[^a-z0-9\s]/g, "")
        .trim()
        .replace(/\s+/g, "_")
        .slice(0, 64);
}
