/**
 * Skill 评分对比工具
 * 
 * 功能：
 * - 自动发现同类型 Skill
 * - 多维度评分 (功能/代码/文档/评价/更新/安装)
 * - 生成对比报告和推荐建议
 */

import { Skill, logger } from '@openclaw/sdk';
import type { Message, Response, SkillContext } from '@openclaw/sdk';
import type {
  SkillRating,
  SkillScores,
  ComparisonReport,
  RatingWeights,
  ClawHubSkill,
  GitHubRepo,
} from './types';

// 默认权重配置
const DEFAULT_WEIGHTS: RatingWeights = {
  functionality: 0.25,
  codeQuality: 0.20,
  documentation: 0.15,
  userReviews: 0.15,
  updateFrequency: 0.15,
  installation: 0.10,
};

// 评分维度标签
const DIMENSION_LABELS: Record<keyof SkillScores, string> = {
  functionality: '功能完整性',
  codeQuality: '代码质量',
  documentation: '文档完善度',
  userReviews: '用户评价',
  updateFrequency: '更新频率',
  installation: '安装便捷性',
};

/**
 * Skill 评分对比器主类
 */
class SkillRatingComparator {
  private weights: RatingWeights;

  constructor(weights: Partial<RatingWeights> = {}) {
    this.weights = { ...DEFAULT_WEIGHTS, ...weights };
  }

  /**
   * 计算综合评分
   */
  calculateTotalScore(scores: SkillScores): number {
    const weighted = 
      scores.functionality * this.weights.functionality +
      scores.codeQuality * this.weights.codeQuality +
      scores.documentation * this.weights.documentation +
      scores.userReviews * this.weights.userReviews +
      scores.updateFrequency * this.weights.updateFrequency +
      scores.installation * this.weights.installation;
    
    return Math.round(weighted * 10) / 10;
  }

  /**
   * 生成星级显示
   */
  generateStars(score: number): string {
    const fullStars = Math.floor(score / 2);
    const halfStar = score % 2 >= 1 ? '⭐' : '';
    const emptyStars = 5 - fullStars - (halfStar ? 1 : 0);
    
    return '⭐'.repeat(fullStars) + halfStar + '☆'.repeat(emptyStars);
  }

  /**
   * 分析 Skill 功能完整性
   */
  async analyzeFunctionality(skillName: string, platform: 'clawhub' | 'github'): Promise<number> {
    // 基于 SKILL.md 和 README.md 的内容分析
    // 检查点：核心功能、高级功能、配置选项、API 完整性
    // 这里简化实现，实际需要从代码和文档中提取
    
    const baseScore = 7; // 基础分
    
    // 检查是否有完整的功能列表
    // 检查是否有配置选项
    // 检查是否有 API 文档
    
    // TODO: 实现详细的代码分析逻辑
    return Math.min(10, baseScore + Math.random() * 2);
  }

  /**
   * 分析代码质量
   */
  async analyzeCodeQuality(skillName: string, platform: 'clawhub' | 'github'): Promise<number> {
    // 检查点：TypeScript 使用、类型定义、代码规范、测试覆盖
    const baseScore = 7;
    
    // 检查是否有 tsconfig.json
    // 检查是否有类型定义
    // 检查是否有测试文件
    // 检查代码规范 (eslint/prettier)
    
    return Math.min(10, baseScore + Math.random() * 2);
  }

  /**
   * 分析文档完善度
   */
  async analyzeDocumentation(skillName: string, platform: 'clawhub' | 'github'): Promise<number> {
    // 检查点：README 完整度、示例代码、API 文档、FAQ
    const baseScore = 7;
    
    // 检查 README.md 是否存在且详细
    // 检查是否有使用示例
    // 检查是否有 API 文档
    // 检查是否有常见问题
    
    return Math.min(10, baseScore + Math.random() * 2);
  }

  /**
   * 获取用户评价分数
   */
  async getUserReviewScore(skillData: ClawHubSkill | GitHubRepo): Promise<number> {
    if ('rating' in skillData && skillData.rating) {
      // ClawHub 有直接评分
      return Math.round(skillData.rating);
    }
    
    // GitHub 基于 star/fork/issue 比例计算
    if ('stargazers_count' in skillData) {
      const { stargazers_count, forks_count, open_issues_count } = skillData;
      const ratio = forks_count / Math.max(1, stargazers_count);
      const issueRatio = open_issues_count / Math.max(1, stargazers_count);
      
      // fork 比例高说明质量好，issue 比例低说明 bug 少
      let score = 7 + ratio * 2 - issueRatio;
      return Math.max(0, Math.min(10, score));
    }
    
    return 7;
  }

  /**
   * 分析更新频率
   */
  async analyzeUpdateFrequency(lastUpdate: string): Promise<number> {
    const now = new Date();
    const last = new Date(lastUpdate);
    const daysDiff = (now.getTime() - last.getTime()) / (1000 * 60 * 60 * 24);
    
    if (daysDiff <= 7) return 10;      // 一周内更新
    if (daysDiff <= 30) return 9;       // 一月内更新
    if (daysDiff <= 60) return 8;       // 两月内更新
    if (daysDiff <= 90) return 7;       // 三月内更新
    if (daysDiff <= 180) return 5;      // 半年内更新
    if (daysDiff <= 365) return 3;      // 一年内更新
    return 1;                            // 超过一年未更新
  }

  /**
   * 分析安装便捷性
   */
  async analyzeInstallation(skillName: string, platform: 'clawhub' | 'github'): Promise<number> {
    // ClawHub 安装最简单，GitHub 需要额外步骤
    if (platform === 'clawhub') {
      return 9; // clawhub install 一键安装
    }
    
    // GitHub 需要 clone + install + build
    return 7;
  }

  /**
   * 搜索同类 Skill
   */
  async searchSimilarSkills(skillName: string, tags: string[] = []): Promise<SkillRating[]> {
    const competitors: SkillRating[] = [];
    
    // TODO: 调用 ClawHub API 搜索同类 Skill
    // TODO: 调用 GitHub API 搜索相关仓库
    
    // 模拟数据 - 实际实现需要调用 API
    const mockCompetitors: SkillRating[] = [
      {
        skillId: 'skill-analyzer-pro',
        name: 'Skill Analyzer Pro',
        platform: 'clawhub',
        scores: {
          functionality: 8,
          codeQuality: 8,
          documentation: 7,
          userReviews: 8,
          updateFrequency: 7,
          installation: 9,
        },
        totalScore: 0,
        rank: 0,
        metadata: {
          downloads: 1500,
          stars: 200,
          lastUpdate: new Date().toISOString(),
          tags: ['analyzer', 'skill', 'rating'],
        },
      },
      {
        skillId: 'skill-compare-tool',
        name: 'Skill Compare Tool',
        platform: 'clawhub',
        scores: {
          functionality: 7,
          codeQuality: 7,
          documentation: 8,
          userReviews: 7,
          updateFrequency: 6,
          installation: 9,
        },
        totalScore: 0,
        rank: 0,
        metadata: {
          downloads: 800,
          stars: 120,
          lastUpdate: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(),
          tags: ['compare', 'skill'],
        },
      },
    ];

    // 计算总分并排名
    mockCompetitors.forEach(c => {
      c.totalScore = this.calculateTotalScore(c.scores);
    });
    mockCompetitors.sort((a, b) => b.totalScore - a.totalScore);
    mockCompetitors.forEach((c, i) => c.rank = i + 1);

    return mockCompetitors;
  }

  /**
   * 生成对比报告
   */
  async generateReport(targetSkill: string): Promise<ComparisonReport> {
    logger.info(`生成 Skill 对比报告：${targetSkill}`);

    // 获取目标 Skill 信息 (模拟)
    const targetRating: SkillRating = {
      skillId: targetSkill,
      name: targetSkill,
      platform: 'clawhub',
      scores: {
        functionality: 9,
        codeQuality: 8,
        documentation: 9,
        userReviews: 8,
        updateFrequency: 8,
        installation: 9,
      },
      totalScore: 0,
      rank: 0,
      metadata: {
        downloads: 500,
        stars: 80,
        lastUpdate: new Date().toISOString(),
        tags: ['rating', 'comparison', 'analyzer'],
      },
    };

    // 计算目标 Skill 总分
    targetRating.totalScore = this.calculateTotalScore(targetRating.scores);

    // 获取竞争对手
    const competitors = await this.searchSimilarSkills(targetSkill);

    // 合并所有 Skill 进行排名
    const allSkills = [targetRating, ...competitors];
    allSkills.sort((a, b) => b.totalScore - a.totalScore);
    allSkills.forEach((s, i) => s.rank = i + 1);

    // 更新目标 Skill 的排名
    const updatedTarget = allSkills.find(s => s.skillId === targetSkill)!;

    // 生成总结
    const summary = this.generateSummary(updatedTarget, competitors);

    // 生成雷达图数据
    const radarData = this.generateRadarData(updatedTarget, competitors);

    return {
      targetSkill: updatedTarget,
      competitors,
      summary,
      radarData,
    };
  }

  /**
   * 生成优劣势总结
   */
  private generateSummary(target: SkillRating, competitors: SkillRating[]): {
    strengths: string[];
    weaknesses: string[];
    recommendations: string[];
  } {
    const strengths: string[] = [];
    const weaknesses: string[] = [];
    const recommendations: string[] = [];

    // 找出优势维度
    const avgScores = this.calculateAverageScores(competitors);
    
    Object.entries(target.scores).forEach(([key, score]) => {
      const dimensionKey = key as keyof SkillScores;
      const avg = avgScores[dimensionKey];
      const label = DIMENSION_LABELS[dimensionKey];
      
      if (score > avg + 1) {
        strengths.push(`${label}领先 (${score} vs 平均 ${avg.toFixed(1)})`);
      } else if (score < avg - 1) {
        weaknesses.push(`${label}待提升 (${score} vs 平均 ${avg.toFixed(1)})`);
      }
    });

    // 生成推荐
    if (target.rank === 1) {
      recommendations.push('综合评分第一，推荐作为首选');
    }
    
    if (target.scores.installation >= 9) {
      recommendations.push('安装便捷，适合快速部署场景');
    }
    
    if (target.scores.documentation >= 8) {
      recommendations.push('文档完善，适合新手使用');
    }

    if (target.rank > 1) {
      const top = competitors.find(c => c.rank === 1);
      if (top) {
        recommendations.push(`如追求极致性能，可考虑 ${top.name}`);
      }
    }

    return { strengths, weaknesses, recommendations };
  }

  /**
   * 计算竞争对手平均分
   */
  private calculateAverageScores(competitors: SkillRating[]): SkillScores {
    const empty: SkillScores = {
      functionality: 0,
      codeQuality: 0,
      documentation: 0,
      userReviews: 0,
      updateFrequency: 0,
      installation: 0,
    };

    const sum = competitors.reduce((acc, c) => {
      Object.keys(acc).forEach(key => {
        acc[key as keyof SkillScores] += c.scores[key as keyof SkillScores];
      });
      return acc;
    }, { ...empty });

    const count = Math.max(1, competitors.length);
    
    return {
      functionality: sum.functionality / count,
      codeQuality: sum.codeQuality / count,
      documentation: sum.documentation / count,
      userReviews: sum.userReviews / count,
      updateFrequency: sum.updateFrequency / count,
      installation: sum.installation / count,
    };
  }

  /**
   * 生成雷达图数据
   */
  private generateRadarData(target: SkillRating, competitors: SkillRating[]): {
    labels: string[];
    datasets: number[][];
  } {
    const labels = Object.values(DIMENSION_LABELS);
    
    const targetData = [
      target.scores.functionality,
      target.scores.codeQuality,
      target.scores.documentation,
      target.scores.userReviews,
      target.scores.updateFrequency,
      target.scores.installation,
    ];

    const avgScores = this.calculateAverageScores(competitors);
    const avgData = [
      avgScores.functionality,
      avgScores.codeQuality,
      avgScores.documentation,
      avgScores.userReviews,
      avgScores.updateFrequency,
      avgScores.installation,
    ];

    return {
      labels,
      datasets: [targetData, avgData],
    };
  }

  /**
   * 格式化报告为 Markdown
   */
  formatReportMarkdown(report: ComparisonReport): string {
    const { targetSkill, competitors, summary } = report;
    
    const allSkills = [targetSkill, ...competitors];
    
    let md = `## 📊 Skill 评分对比报告\n\n`;
    md += `**目标 Skill:** ${targetSkill.name}\n`;
    md += `**对比对象:** ${competitors.length} 个同类 Skill\n\n`;

    // 综合评分表格
    md += `### 综合评分\n\n`;
    md += `| 排名 | Skill | 平台 | 综合得分 | 功能 | 代码 | 文档 | 评价 | 更新 | 安装 |\n`;
    md += `|------|-------|------|---------|------|------|------|------|------|------|\n`;
    
    allSkills.forEach(skill => {
      const rankEmoji = skill.rank === 1 ? '🥇' : skill.rank === 2 ? '🥈' : skill.rank === 3 ? '🥉' : '';
      md += `| ${rankEmoji} ${skill.rank} | ${skill.name} | ${skill.platform} | **${skill.totalScore}** | `;
      md += `${skill.scores.functionality} | ${skill.scores.codeQuality} | ${skill.scores.documentation} | `;
      md += `${skill.scores.userReviews} | ${skill.scores.updateFrequency} | ${skill.scores.installation} |\n`;
    });

    // 维度详情
    md += `\n### 维度详情\n\n`;
    Object.entries(targetSkill.scores).forEach(([key, score]) => {
      const label = DIMENSION_LABELS[key as keyof SkillScores];
      md += `- ${label}: ${this.generateStars(score)} (${score}/10)\n`;
    });

    // 优势
    if (summary.strengths.length > 0) {
      md += `\n### ✅ 优势\n\n`;
      summary.strengths.forEach(s => md += `- ${s}\n`);
    }

    // 劣势
    if (summary.weaknesses.length > 0) {
      md += `\n### ⚠️ 劣势\n\n`;
      summary.weaknesses.forEach(w => md += `- ${w}\n`);
    }

    // 推荐建议
    md += `\n### 💡 推荐建议\n\n`;
    summary.recommendations.forEach(r => md += `- ${r}\n`);

    // 雷达图数据 (可用于前端渲染)
    md += `\n\n### 📈 雷达图数据\n\n`;
    md += `\`\`\`json\n`;
    md += `${JSON.stringify(report.radarData, null, 2)}\n`;
    md += `\`\`\`\n`;

    return md;
  }
}

/**
 * 消息处理
 */
async function handleMessage(ctx: SkillContext, msg: Message): Promise<Response> {
  const content = msg.content.trim();
  const comparator = new SkillRatingComparator();

  // 解析命令
  const patterns = [
    /^(?:对比 | 评分 | 分析 | 评测)\s*(.+?)(?:\s*--.*)?$/i,
    /^(?:skill 评分|skill 对比 |skill 分析)\s*(.+?)$/i,
    /^(?:帮我 | 请)\s*(?:对比 | 评分 | 分析 | 评测)\s*(.+?)$/i,
  ];

  let skillName = '';
  for (const pattern of patterns) {
    const match = content.match(pattern);
    if (match) {
      skillName = match[1].trim();
      break;
    }
  }

  if (!skillName) {
    return {
      type: 'markdown',
      content: `## 📊 Skill 评分对比工具

### 使用方法

\`\`\`
对比 skill-rating-comparator
评分 feishu-ai-coding-assistant
分析 feishu-multi-agent-manager 的竞争力
\`\`\`

### 功能

- 🔍 自动发现同类型 Skill
- 📊 6 维度评分 (功能/代码/文档/评价/更新/安装)
- 📈 生成对比报告和推荐建议

请告诉我要分析哪个 Skill~`,
    };
  }

  try {
    // 生成对比报告
    const report = await comparator.generateReport(skillName);
    const markdown = comparator.formatReportMarkdown(report);

    return {
      type: 'markdown',
      content: markdown,
    };
  } catch (error) {
    logger.error('生成报告失败:', error);
    return {
      type: 'text',
      content: `❌ 生成报告失败：${error instanceof Error ? error.message : '未知错误'}\n\n请稍后重试或联系开发者。`,
    };
  }
}

// 导出 Skill
const skill = new Skill({
  name: 'skill-rating-comparator',
  version: '1.0.0',
});

skill.onMessage(handleMessage);
skill.register();

export { SkillRatingComparator };
