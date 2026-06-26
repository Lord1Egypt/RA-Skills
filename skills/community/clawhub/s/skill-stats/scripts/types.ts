export interface SkillCallRecord {
  skillName: string;
  timestamp: string;
  projectPath: string;
  sessionId: string;
  success: boolean;
}

export interface SkillStats {
  totalCalls: number;
  successCount: number;
  failureCount: number;
  lastUsed: string;
  projects: string[];
  avgExecutionTime: number;
  scope?: 'managed' | 'user' | 'project' | 'plugin' | 'builtin' | 'unknown'
        | 'openclaw-workspace' | 'openclaw-global';
  status?: 'active' | 'deleted' | 'never-used';
}

export interface GlobalStats {
  skills: Record<string, SkillStats>;
  lastUpdated: string;
  lastProcessedTimestamp: string;
}
