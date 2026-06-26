import { loadJsonConfig } from "./configLoader";
import type { StyleRewriteItem } from "../services/rewriteStyle";

export type RewriteOutputField = "style" | "content";

interface RewriteProfileConfig {
  name: string;
  styles: string[];
  fields: RewriteOutputField[];
}

interface RewriteProfilesConfig {
  [profileName: string]: RewriteProfileConfig;
}

const DEFAULT_REWRITE_PROFILE = "default_rewrite";

export function resolveRewriteProfile(profileName = DEFAULT_REWRITE_PROFILE): RewriteProfileConfig {
  const profiles = loadJsonConfig<RewriteProfilesConfig>("rewrite-profiles.json");
  return profiles[profileName] ?? profiles[DEFAULT_REWRITE_PROFILE];
}

export function buildRewriteOutputRequirement(fields: RewriteOutputField[]): string {
  return `请只返回 JSON 数组，每个元素包含 ${fields.join(" 与 ")}。`;
}

export function normalizeRewriteOutput(
  parsed: StyleRewriteItem[] | null,
  styles: string[],
  originalScript: string,
): StyleRewriteItem[] {
  if (parsed && parsed.length > 0) return parsed;

  return styles.map((style) => ({
    style,
    content: originalScript,
  }));
}
