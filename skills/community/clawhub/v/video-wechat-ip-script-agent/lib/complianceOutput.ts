import { applyComplianceFallback } from "./fallback";
import { loadJsonConfig } from "./configLoader";
import { normalizeStringArray } from "./outputParser";
import type { ComplianceIssue, ComplianceOutput } from "../schemas/output-schema";

export type ComplianceOutputField = "issues" | "revisedVersion" | "safeTitles" | "safeCaption";

interface ComplianceOutputProfileConfig {
  name: string;
  fields: ComplianceOutputField[];
}

interface ComplianceOutputProfilesConfig {
  [profileName: string]: ComplianceOutputProfileConfig;
}

const DEFAULT_COMPLIANCE_PROFILE = "full_compliance";

export function resolveComplianceOutputFields(outputProfile = DEFAULT_COMPLIANCE_PROFILE): ComplianceOutputField[] {
  const profiles = loadJsonConfig<ComplianceOutputProfilesConfig>("compliance-output-profiles.json");
  const profile = profiles[outputProfile] ?? profiles[DEFAULT_COMPLIANCE_PROFILE];
  return profile.fields;
}

export function buildComplianceOutputRequirement(fields: ComplianceOutputField[]): string {
  return `请只返回 JSON 对象，字段必须为 ${fields.join(",")}。`;
}

export function normalizeComplianceOutput(raw: Record<string, unknown>): ComplianceOutput {
  const rawIssues = Array.isArray(raw.issues) ? raw.issues : [];
  const issues: ComplianceIssue[] = rawIssues.map((item) => {
    const record = (item ?? {}) as Record<string, unknown>;
    return {
      originalText: String(record.originalText ?? "").trim(),
      riskType: String(record.riskType ?? "").trim(),
      reason: String(record.reason ?? "").trim(),
      suggestion: String(record.suggestion ?? "").trim(),
    };
  }).filter((item) => item.originalText || item.riskType || item.reason || item.suggestion);

  return applyComplianceFallback({
    issues,
    revisedVersion: String(raw.revisedVersion ?? "").trim(),
    safeTitles: normalizeStringArray(raw.safeTitles),
    safeCaption: String(raw.safeCaption ?? "").trim(),
  });
}

export function pruneComplianceOutput(
  output: ComplianceOutput,
  fields: ComplianceOutputField[],
): Partial<ComplianceOutput> {
  const fieldSet = new Set(fields);
  return {
    ...(fieldSet.has("issues") ? { issues: output.issues } : {}),
    ...(fieldSet.has("revisedVersion") ? { revisedVersion: output.revisedVersion } : {}),
    ...(fieldSet.has("safeTitles") ? { safeTitles: output.safeTitles } : {}),
    ...(fieldSet.has("safeCaption") ? { safeCaption: output.safeCaption } : {}),
  };
}
