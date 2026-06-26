import { buildPrompt } from "../lib/promptBuilder";
import { safeJsonParse } from "../lib/outputParser";
import {
  buildScriptOutputRequirement,
  normalizeScriptOutput,
  pruneScriptOutput,
  resolveScriptOutputFields,
} from "../lib/scriptOutput";
import type { ModelInvoker } from "../lib/modelInvoker";
import type { ScriptOutput } from "../schemas/output-schema";

export interface GenerateScriptInput {
  topic: string;
  industry?: string;
  targetAudience?: string;
  style?: string;
  scriptStructure?: string;
  outputProfile?: string;
  duration?: 30 | 60 | 90;
  platform?: string;
  includeShotList?: boolean;
  includePublishCaption?: boolean;
  includeCommentCTA?: boolean;
}

export async function generateScript(
  input: GenerateScriptInput,
  invokeModel: ModelInvoker,
): Promise<Partial<ScriptOutput>> {
  const outputFields = resolveScriptOutputFields({
    outputProfile: input.outputProfile,
    includeShotList: input.includeShotList,
    includePublishCaption: input.includePublishCaption,
    includeCommentCTA: input.includeCommentCTA,
  });

  const prompt = buildPrompt({
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
      outputRequirement: buildScriptOutputRequirement(outputFields),
    },
  });

  const raw = await invokeModel(prompt);
  const parsed = safeJsonParse<Record<string, unknown>>(raw) ?? {};
  const normalized = normalizeScriptOutput(parsed, input.topic);
  return pruneScriptOutput(normalized, outputFields);
}
