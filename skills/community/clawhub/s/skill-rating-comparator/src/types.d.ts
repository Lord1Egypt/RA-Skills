// 类型声明 - OpenClaw SDK (运行时提供)
declare module '@openclaw/sdk' {
  export interface SkillContext {
    name: string;
    version: string;
    config: Record<string, any>;
  }

  export interface Message {
    content: string;
    sender: string;
    timestamp: number;
    channel: string;
  }

  export interface Response {
    content: string;
    type?: 'text' | 'markdown' | 'card';
  }

  export class Skill {
    constructor(config: { name: string; version: string });
    onMessage(handler: (ctx: SkillContext, msg: Message) => Promise<Response>): void;
    register(): void;
  }

  export const logger: {
    info: (msg: string, ...args: any[]) => void;
    warn: (msg: string, ...args: any[]) => void;
    error: (msg: string, ...args: any[]) => void;
    debug: (msg: string, ...args: any[]) => void;
  };
}

// ClawHub API 响应类型
export interface ClawHubSkill {
  id: string;
  name: string;
  description: string;
  version: string;
  downloads: number;
  rating: number;
  reviews: number;
  author: string;
  createdAt: string;
  updatedAt: string;
  tags: string[];
  repository?: string;
}

export interface ClawHubSearchResponse {
  skills: ClawHubSkill[];
  total: number;
  page: number;
  pageSize: number;
}

// GitHub API 响应类型
export interface GitHubRepo {
  full_name: string;
  description: string;
  stargazers_count: number;
  forks_count: number;
  open_issues_count: number;
  language: string;
  created_at: string;
  updated_at: string;
  pushed_at: string;
  homepage?: string;
  topics: string[];
}

// 评分维度
export interface SkillScores {
  functionality: number;      // 功能完整性 (0-10)
  codeQuality: number;        // 代码质量 (0-10)
  documentation: number;      // 文档完善度 (0-10)
  userReviews: number;        // 用户评价 (0-10)
  updateFrequency: number;    // 更新频率 (0-10)
  installation: number;       // 安装便捷性 (0-10)
}

// 评分结果
export interface SkillRating {
  skillId: string;
  name: string;
  platform: 'clawhub' | 'github';
  scores: SkillScores;
  totalScore: number;
  rank: number;
  metadata: {
    downloads?: number;
    stars?: number;
    forks?: number;
    issues?: number;
    lastUpdate: string;
    tags: string[];
  };
}

// 对比报告
export interface ComparisonReport {
  targetSkill: SkillRating;
  competitors: SkillRating[];
  summary: {
    strengths: string[];
    weaknesses: string[];
    recommendations: string[];
  };
  radarData: {
    labels: string[];
    datasets: number[][];
  };
}

// 评分权重配置
export interface RatingWeights {
  functionality: number;
  codeQuality: number;
  documentation: number;
  userReviews: number;
  updateFrequency: number;
  installation: number;
}

// 默认权重
export const DEFAULT_WEIGHTS: RatingWeights = {
  functionality: 0.25,
  codeQuality: 0.20,
  documentation: 0.15,
  userReviews: 0.15,
  updateFrequency: 0.15,
  installation: 0.10,
};
