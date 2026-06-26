import { applyScriptFallback } from "./fallback";
import { loadJsonConfig } from "./configLoader";
import { normalizeMultilineString, normalizeStringArray } from "./outputParser";
import type { ScriptOutput } from "../schemas/output-schema";

export type ScriptOutputField =
  | "positioning"
  | "titles"
  | "hook"
  | "script"
  | "shotList"
  | "coverText"
  | "publishCaption"
  | "commentCTA";

export interface ResolveScriptOutputOptions {
  rootDir?: string;
  outputProfile?: string;
  includeShotList?: boolean;
  includePublishCaption?: boolean;
  includeCommentCTA?: boolean;
}

interface ScriptOutputProfileConfig {
  name: string;
  fields: ScriptOutputField[];
}

interface ScriptOutputProfilesConfig {
  [profileName: string]: ScriptOutputProfileConfig;
}

const DEFAULT_OUTPUT_PROFILE = "full_publish_pack";

export function resolveScriptOutputFields(options: ResolveScriptOutputOptions = {}): ScriptOutputField[] {
  const profiles = loadJsonConfig<ScriptOutputProfilesConfig>("script-output-profiles.json", options.rootDir);
  const profileName = options.outputProfile ?? DEFAULT_OUTPUT_PROFILE;
  const profile = profiles[profileName] ?? profiles[DEFAULT_OUTPUT_PROFILE];

  const fields = new Set<ScriptOutputField>(profile.fields);

  if (options.includeShotList === false) fields.delete("shotList");
  if (options.includePublishCaption === false) fields.delete("publishCaption");
  if (options.includeCommentCTA === false) fields.delete("commentCTA");

  return Array.from(fields);
}

export function buildScriptOutputRequirement(fields: ScriptOutputField[]): string {
  return `请只返回 JSON 对象，字段必须为 ${fields.join(",")}。`;
}

export function normalizeScriptOutput(raw: Record<string, unknown>, topic: string): ScriptOutput {
  return applyScriptFallback(
    {
      positioning: normalizeMultilineString(raw.positioning),
      titles: normalizeStringArray(raw.titles),
      hook: normalizeMultilineString(raw.hook),
      script: normalizeMultilineString(raw.script),
      shotList: normalizeStringArray(raw.shotList),
      coverText: normalizeMultilineString(raw.coverText),
      publishCaption: normalizeMultilineString(raw.publishCaption),
      commentCTA: normalizeMultilineString(raw.commentCTA),
    },
    topic,
  );
}

export function pruneScriptOutput(
  output: ScriptOutput,
  fields: ScriptOutputField[],
): Partial<ScriptOutput> {
  const fieldSet = new Set(fields);
  return {
    ...(fieldSet.has("positioning") ? { positioning: output.positioning } : {}),
    ...(fieldSet.has("titles") ? { titles: output.titles } : {}),
    ...(fieldSet.has("hook") ? { hook: output.hook } : {}),
    ...(fieldSet.has("script") ? { script: output.script } : {}),
    ...(fieldSet.has("shotList") ? { shotList: output.shotList } : {}),
    ...(fieldSet.has("coverText") ? { coverText: output.coverText } : {}),
    ...(fieldSet.has("publishCaption") ? { publishCaption: output.publishCaption } : {}),
    ...(fieldSet.has("commentCTA") ? { commentCTA: output.commentCTA } : {}),
  };
}
