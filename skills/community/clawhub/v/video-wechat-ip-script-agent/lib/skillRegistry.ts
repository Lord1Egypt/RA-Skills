import type { CheckComplianceInput } from "../services/checkCompliance";
import { checkCompliance } from "../services/checkCompliance";
import type { GenerateScriptInput } from "../services/generateScript";
import { generateScript } from "../services/generateScript";
import type { GenerateTopicsInput } from "../services/generateTopics";
import { generateTopics } from "../services/generateTopics";
import type { RewriteStyleInput } from "../services/rewriteStyle";
import { rewriteStyle } from "../services/rewriteStyle";
import type { ModelInvoker } from "./modelInvoker";

export type SkillAction = "topics" | "script" | "rewrite" | "compliance";

export interface SkillPayloadMap {
  topics: GenerateTopicsInput;
  script: GenerateScriptInput;
  rewrite: RewriteStyleInput;
  compliance: CheckComplianceInput;
}

export interface OpenClawSkillRequest<TAction extends SkillAction = SkillAction> {
  action: TAction;
  payload: SkillPayloadMap[TAction];
}

type SkillValidator<TPayload> = (payload: Record<string, unknown>) => TPayload;
type SkillHandler<TPayload> = (payload: TPayload, invoker: ModelInvoker) => Promise<unknown>;

interface SkillDefinition<TAction extends SkillAction> {
  action: TAction;
  validate: SkillValidator<SkillPayloadMap[TAction]>;
  run: SkillHandler<SkillPayloadMap[TAction]>;
}

function assertNonEmptyString(value: unknown, fieldName: string): string {
  if (typeof value !== "string" || !value.trim()) {
    throw new Error(`Invalid payload: "${fieldName}" must be a non-empty string.`);
  }
  return value.trim();
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function validateTopicsPayload(payload: Record<string, unknown>): GenerateTopicsInput {
  return {
    direction: assertNonEmptyString(payload.direction, "direction"),
    targetAudience: assertNonEmptyString(payload.targetAudience, "targetAudience"),
    industry: typeof payload.industry === "string" ? payload.industry : undefined,
    count: typeof payload.count === "number" ? payload.count : undefined,
    style: typeof payload.style === "string" ? payload.style : undefined,
    outputProfile: typeof payload.outputProfile === "string" ? payload.outputProfile : undefined,
  };
}

function validateScriptPayload(payload: Record<string, unknown>): GenerateScriptInput {
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

function validateRewritePayload(payload: Record<string, unknown>): RewriteStyleInput {
  return {
    originalScript: assertNonEmptyString(payload.originalScript, "originalScript"),
    rewriteProfile: typeof payload.rewriteProfile === "string" ? payload.rewriteProfile : undefined,
    styles: Array.isArray(payload.styles)
      ? payload.styles.filter((item): item is string => typeof item === "string" && Boolean(item.trim()))
      : undefined,
  };
}

function validateCompliancePayload(payload: Record<string, unknown>): CheckComplianceInput {
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

const registry: { [K in SkillAction]: SkillDefinition<K> } = {
  topics: {
    action: "topics",
    validate: validateTopicsPayload,
    run: generateTopics,
  },
  script: {
    action: "script",
    validate: validateScriptPayload,
    run: generateScript,
  },
  rewrite: {
    action: "rewrite",
    validate: validateRewritePayload,
    run: rewriteStyle,
  },
  compliance: {
    action: "compliance",
    validate: validateCompliancePayload,
    run: checkCompliance,
  },
};

export function getSupportedActions(): SkillAction[] {
  return Object.keys(registry) as SkillAction[];
}

export function validateOpenClawSkillRequest(input: unknown): OpenClawSkillRequest {
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

  const definition = registry[action as SkillAction];
  return {
    action: definition.action,
    payload: definition.validate(payload) as SkillPayloadMap[SkillAction],
  };
}

export async function dispatchSkillRequest(
  request: OpenClawSkillRequest,
  invoker: ModelInvoker,
): Promise<unknown> {
  const definition = registry[request.action];
  return definition.run(request.payload as never, invoker);
}
