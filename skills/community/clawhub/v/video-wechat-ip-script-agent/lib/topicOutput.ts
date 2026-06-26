import { applyTopicFallback } from "./fallback";
import { loadJsonConfig } from "./configLoader";
import type { TopicItem } from "../schemas/output-schema";

export type TopicOutputField = "title" | "category" | "angle" | "targetAudience";

interface TopicOutputProfileConfig {
  name: string;
  fields: TopicOutputField[];
}

interface TopicOutputProfilesConfig {
  [profileName: string]: TopicOutputProfileConfig;
}

const DEFAULT_TOPIC_OUTPUT_PROFILE = "default_topics";

export function resolveTopicOutputFields(outputProfile = DEFAULT_TOPIC_OUTPUT_PROFILE): TopicOutputField[] {
  const profiles = loadJsonConfig<TopicOutputProfilesConfig>("topic-output-profiles.json");
  const profile = profiles[outputProfile] ?? profiles[DEFAULT_TOPIC_OUTPUT_PROFILE];
  return profile.fields;
}

export function buildTopicOutputRequirement(fields: TopicOutputField[]): string {
  return `请只返回 JSON 数组，每个元素包含 ${fields.join(", ")}。`;
}

export function normalizeTopicOutput(raw: Partial<TopicItem>[], targetAudience: string): TopicItem[] {
  return applyTopicFallback(raw, targetAudience);
}
