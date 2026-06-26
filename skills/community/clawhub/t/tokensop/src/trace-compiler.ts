/**
 * Trace Compiler — converts a recorded OpenClaw session trace
 * into a reusable Lobster workflow.
 *
 * This is the core "one node explores, all nodes benefit" engine.
 * It takes the raw action history from a successful session and
 * compiles it into a parameterized, portable Lobster workflow.
 */

import { sanitizeActionArgs } from "./sanitizer.js";
import type {
  ActionTrace,
  LobsterWorkflow,
  LobsterStep,
  LobsterArgs,
} from "./types.js";

export interface CompileResult {
  workflow: LobsterWorkflow;
  argCount: number;
}

export function compileTrace(
  intentName: string,
  actions: ActionTrace[]
): CompileResult {
  const steps: LobsterStep[] = [];
  const collectedArgs: LobsterArgs = {};
  let stepIndex = 0;

  for (const action of actions) {
    // Skip failed actions — we only want the successful path
    if (!action.result.success) continue;

    // Skip non-browser actions (internal bookkeeping, etc.)
    if (!isBrowserAction(action)) continue;

    // Sanitize args to strip PII and extract Lobster arguments
    const { sanitized, extractedArgs } = sanitizeActionArgs(action.args);

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

    const step: LobsterStep = {
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

  const workflow: LobsterWorkflow = {
    name: intentToWorkflowName(intentName),
    args: collectedArgs,
    steps,
  };

  return { workflow, argCount: Object.keys(collectedArgs).length };
}

function isBrowserAction(action: ActionTrace): boolean {
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

function buildCommand(
  tool: string,
  action: string,
  args: Record<string, unknown>
): string {
  const argsStr = Object.entries(args)
    .map(([k, v]) => {
      if (typeof v === "string") return `${k}="${v}"`;
      return `${k}=${v}`;
    })
    .join(" ");

  return `openclaw.invoke ${tool}.${action} ${argsStr}`.trim();
}

function inferTimeout(action: ActionTrace): number {
  const actionName = `${action.tool}.${action.action}`;

  if (actionName.includes("navigate")) return 10000;
  if (actionName.includes("wait")) return 5000;
  if (actionName.includes("click")) return 3000;
  if (actionName.includes("type") || actionName.includes("fill")) return 2000;

  return 3000;
}

function isWaitStep(step: LobsterStep): boolean {
  return step.command.includes("browser.wait");
}

function intentToWorkflowName(intent: string): string {
  return intent
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, "")
    .trim()
    .replace(/\s+/g, "_")
    .slice(0, 64);
}
