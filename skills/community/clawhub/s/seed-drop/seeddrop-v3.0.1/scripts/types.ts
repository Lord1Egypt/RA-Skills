// SECURITY MANIFEST:
//   Environment variables accessed: none
//   External endpoints called: none
//   Local files read: none
//   Local files written: none

// ─── Credential ─────────────────────────────────────────────

export interface Credential {
  authType: 'api_token' | 'cookie' | 'oauth';
  value: string;
  profile?: string;
  source: 'socialvault' | 'local';
}

// ─── Post & Scoring ─────────────────────────────────────────

export interface Post {
  id: string;
  url: string;
  title: string;
  body: string;
  author: string;
  createdAt: string; // ISO 8601
  platform: string;
  community?: string; // 吧名、知乎话题、B站分区等
  metadata?: Record<string, unknown>;
}

export interface ScoreBreakdown {
  relevance: number;
  intent: number;
  freshness: number;
  risk: number;
}

export interface ScoredPost extends Post {
  scores: ScoreBreakdown;
  finalScore: number;
}

// ─── Reply ──────────────────────────────────────────────────

export interface ReplyResult {
  success: boolean;
  replyId?: string;
  error?: string;
  mode?: 'api' | 'browser';
}

export interface ReplyDraft {
  postId: string;
  postUrl: string;
  postTitle: string;
  platform: string;
  content: string;
  score: number;
}

// ─── Auth / Check ───────────────────────────────────────────

export interface CheckResult {
  valid: boolean;
  username?: string;
  error?: string;
}

export type AuthMode = 'socialvault' | 'none';

// ─── Rate Limiting ──────────────────────────────────────────

export interface RateLimitInfo {
  requestsPerMinute: number;
  repliesPerDay: number;
  minReplyIntervalSeconds: number;
  notes: string;
}

export interface DailyLimits {
  approve: number;
  auto: number;
}

export const PLATFORM_DAILY_LIMITS: Record<string, DailyLimits> = {
  'bilibili':           { approve: 30, auto: 15 },
  'tieba':              { approve: 20, auto: 10 },
  'zhihu':              { approve: 10, auto: 5  },
  'xiaohongshu':        { approve: 10, auto: 5  },
  '_default':           { approve: 10, auto: 5  },
};

// ─── Platform Adapter ───────────────────────────────────────

export interface PlatformAdapter {
  readonly platformId: string;
  readonly platformName: string;

  search(
    keyword: string,
    timeRange: string,
    credential: Credential,
    target?: string,
  ): Promise<Post[]>;

  reply(
    postId: string,
    content: string,
    credential: Credential,
  ): Promise<ReplyResult>;

  check(credential: Credential): Promise<CheckResult>;

  rateLimitInfo(): RateLimitInfo;
}

// ─── Interaction Log ────────────────────────────────────────

export interface InteractionLogEntry {
  timestamp: string; // ISO 8601
  platform: string;
  postId: string;
  postUrl: string;
  postTitle: string;
  author: string;
  replyContent: string;
  replyId?: string;
  score: number;
  mode: 'approve' | 'auto';
  success: boolean;
}

// ─── Brand Profile ──────────────────────────────────────────

export interface BrandProfile {
  businessName: string;
  description: string;
  keywords: string[];
  platforms: string[];
  mode: 'approve' | 'auto';
  threshold: number;
  language: string;
}

// ─── Scoring Config ─────────────────────────────────────────

export const SCORE_WEIGHTS = {
  relevance: 0.35,
  intent: 0.30,
  freshness: 0.20,
  risk: 0.15,
} as const;

export const DEFAULT_THRESHOLD = 0.6;
export const AUTO_MODE_MIN_THRESHOLD = 0.7;
export const AUTO_MODE_MIN_RISK = 0.5;

// ─── Browser Instruction (for adapter browser mode) ─────────

export const BROWSER_INSTRUCTION_ID = '__browser_instruction__';

export interface BrowserStep {
  action: 'navigate' | 'wait' | 'extract' | 'click' | 'type';
  url?: string;
  selector?: string;
  fields?: string[];
  text?: string;
}

export interface BrowserInstruction {
  mode: 'browser';
  action: 'search' | 'reply' | 'check';
  steps: BrowserStep[];
  cookies?: string;
}

// ─── Cookie Parsing ─────────────────────────────────────────

export function parseCookieValue(raw: string, name: string): string | undefined {
  const match = raw.match(new RegExp(`(?:^|;\\s*)${name}=([^;]*)`));
  return match?.[1];
}

// ─── Utility types ──────────────────────────────────────────

export type ReplyMode = 'approve' | 'auto';

export interface PerformanceStats {
  total_replies: number;
  by_platform: Record<string, number>;
  by_date: Record<string, number>;
}
