import { buildPrompt } from "../lib/promptBuilder";
import { safeJsonParse } from "../lib/outputParser";
import type { ModelInvoker } from "../lib/modelInvoker";
import { buildTopicOutputRequirement, normalizeTopicOutput, resolveTopicOutputFields } from "../lib/topicOutput";
import type { TopicItem } from "../schemas/output-schema";

export interface GenerateTopicsInput {
  industry?: string;
  direction: string;
  targetAudience: string;
  count?: number;
  style?: string;
  outputProfile?: string;
}

export async function generateTopics(
  input: GenerateTopicsInput,
  invokeModel: ModelInvoker,
): Promise<TopicItem[]> {
  const outputFields = resolveTopicOutputFields(input.outputProfile);

  const prompt = buildPrompt({
    taskPromptFile: "topic-generator.md",
    variables: {
      industry: input.industry ?? "医美",
      direction: input.direction,
      targetAudience: input.targetAudience,
      count: input.count ?? 10,
      style: input.style ?? "观点型",
      outputProfile: input.outputProfile ?? "default_topics",
      outputFields,
      outputRequirement: buildTopicOutputRequirement(outputFields),
    },
  });

  const raw = await invokeModel(prompt);
  const parsed = safeJsonParse<Partial<TopicItem>[]>(raw) ?? [];
  return normalizeTopicOutput(parsed, input.targetAudience);
}
