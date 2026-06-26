import { buildPrompt } from "../lib/promptBuilder";
import { safeJsonParse } from "../lib/outputParser";
import type { ModelInvoker } from "../lib/modelInvoker";
import { buildRewriteOutputRequirement, normalizeRewriteOutput, resolveRewriteProfile } from "../lib/rewriteOutput";

export interface RewriteStyleInput {
  originalScript: string;
  styles?: string[];
  rewriteProfile?: string;
}

export interface StyleRewriteItem {
  style: string;
  content: string;
}

export async function rewriteStyle(
  input: RewriteStyleInput,
  invokeModel: ModelInvoker,
): Promise<StyleRewriteItem[]> {
  const profile = resolveRewriteProfile(input.rewriteProfile);
  const styles = input.styles ?? profile.styles;

  const prompt = buildPrompt({
    taskPromptFile: "style-rewriter.md",
    variables: {
      originalScript: input.originalScript,
      rewriteProfile: input.rewriteProfile ?? "default_rewrite",
      targetStyles: styles,
      outputFields: profile.fields,
      outputRequirement: buildRewriteOutputRequirement(profile.fields),
    },
  });

  const raw = await invokeModel(prompt);
  const parsed = safeJsonParse<StyleRewriteItem[]>(raw);
  return normalizeRewriteOutput(parsed, styles, input.originalScript);
}
