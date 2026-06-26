import { buildPrompt } from "../lib/promptBuilder";
import { safeJsonParse } from "../lib/outputParser";
import {
  buildComplianceOutputRequirement,
  normalizeComplianceOutput,
  pruneComplianceOutput,
  resolveComplianceOutputFields,
} from "../lib/complianceOutput";
import type { ModelInvoker } from "../lib/modelInvoker";
import type { ComplianceOutput } from "../schemas/output-schema";

export interface CheckComplianceInput {
  title?: string;
  script?: string;
  caption?: string;
  outputProfile?: string;
}

export async function checkCompliance(
  input: CheckComplianceInput,
  invokeModel: ModelInvoker,
): Promise<Partial<ComplianceOutput>> {
  const outputFields = resolveComplianceOutputFields(input.outputProfile);

  const prompt = buildPrompt({
    taskPromptFile: "compliance-checker.md",
    variables: {
      title: input.title ?? "",
      script: input.script ?? "",
      caption: input.caption ?? "",
      outputProfile: input.outputProfile ?? "full_compliance",
      outputFields,
      outputRequirement: buildComplianceOutputRequirement(outputFields),
    },
  });

  const raw = await invokeModel(prompt);
  const parsed = safeJsonParse<Record<string, unknown>>(raw) ?? {};
  const normalized = normalizeComplianceOutput(parsed);
  return pruneComplianceOutput(normalized, outputFields);
}
