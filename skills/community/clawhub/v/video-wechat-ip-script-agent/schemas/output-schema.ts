export interface TopicItem {
  title: string;
  category: "痛点" | "反差" | "观点" | "方法" | "案例";
  angle: string;
  targetAudience: string;
}

export interface ScriptOutput {
  positioning: string;
  titles: string[];
  hook: string;
  script: string;
  shotList: string[];
  coverText: string;
  publishCaption: string;
  commentCTA: string;
}

export interface ComplianceIssue {
  originalText: string;
  riskType: string;
  reason: string;
  suggestion: string;
}

export interface ComplianceOutput {
  issues: ComplianceIssue[];
  revisedVersion: string;
  safeTitles?: string[];
  safeCaption?: string;
}
