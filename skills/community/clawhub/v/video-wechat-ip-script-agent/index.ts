import { createModelInvoker, invokeModel, type ModelInvoker } from "./lib/modelInvoker";
import {
  dispatchSkillRequest,
  getSupportedActions,
  validateOpenClawSkillRequest,
  type OpenClawSkillRequest,
  type SkillAction,
} from "./lib/skillRegistry";
import { checkCompliance, type CheckComplianceInput } from "./services/checkCompliance";
import { generateScript, type GenerateScriptInput } from "./services/generateScript";
import { generateTopics, type GenerateTopicsInput } from "./services/generateTopics";
import { rewriteStyle, type RewriteStyleInput } from "./services/rewriteStyle";

export interface OpenClawSkillOptions {
  apiKey?: string;
  baseUrl?: string;
  model?: string;
  temperature?: number;
  maxTokens?: number;
  timeoutMs?: number;
  systemPrompt?: string;
  headers?: Record<string, string>;
  invoker?: ModelInvoker;
}

export async function runOpenClawSkill(
  request: OpenClawSkillRequest,
  options: OpenClawSkillOptions = {},
): Promise<unknown> {
  const validatedRequest = validateOpenClawSkillRequest(request);
  const modelInvoker = options.invoker ?? createModelInvoker(options);
  return dispatchSkillRequest(validatedRequest, modelInvoker);
}

export {
  dispatchSkillRequest,
  getSupportedActions,
  invokeModel,
  createModelInvoker,
  generateTopics,
  generateScript,
  rewriteStyle,
  checkCompliance,
  validateOpenClawSkillRequest,
};

export type { CheckComplianceInput, GenerateScriptInput, GenerateTopicsInput, RewriteStyleInput };
export type { OpenClawSkillRequest, SkillAction };
