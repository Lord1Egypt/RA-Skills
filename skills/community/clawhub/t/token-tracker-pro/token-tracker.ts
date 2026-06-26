// Token Tracker 实现

import fs from 'fs';
import path from 'path';
import os from 'os';

interface TokenRecord {
  timestamp: number;
  date: string;
  week: string;
  model: string;
  tokens: number;
  sessionKey?: string;
}

interface TokenStats {
  total: number;
  count: number;
  average: number;
  max: number;
  min: number;
}

interface TokenTrackerData {
  tokens: TokenRecord[];
  total: number;
  daily: Record<string, number>;
  weekly: Record<string, number>;
}

class TokenTracker {
  private dataPath: string;
  private data: TokenTrackerData;

  constructor() {
    const homeDir = process.env.OPENCLAW_HOME || os.homedir();
    this.dataPath = path.join(homeDir, '.openclaw', 'skills/token-tracker/data/token-history.json');
    this.data = this.loadData();
  }

  // 加载数据
  private loadData(): TokenTrackerData {
    try {
      if (fs.existsSync(this.dataPath)) {
        const content = fs.readFileSync(this.dataPath, 'utf-8');
        return JSON.parse(content);
      }
    } catch (error) {
      console.error('Failed to load token data:', error);
    }

    return {
      tokens: [],
      total: 0,
      daily: {},
      weekly: {}
    };
  }

  // 保存数据
  private saveData(): void {
    try {
      const dir = path.dirname(this.dataPath);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      fs.writeFileSync(this.dataPath, JSON.stringify(this.data, null, 2), 'utf-8');
    } catch (error) {
      console.error('Failed to save token data:', error);
    }
  }

  // 记录 token 消耗
  record(data: {
    model?: string;
    tokens: number;
    sessionKey?: string;
  }): void {
    const now = Date.now();
    const date = new Date(now).toISOString().split('T')[0];
    const week = this.getWeekNumber(now);

    const record: TokenRecord = {
      timestamp: now,
      date,
      week,
      model: data.model || 'unknown',
      tokens: data.tokens,
      sessionKey: data.sessionKey
    };

    this.data.tokens.push(record);
    this.data.total += data.tokens;

    // 更新每日统计
    this.data.daily[date] = (this.data.daily[date] || 0) + data.tokens;

    // 更新每周统计
    this.data.weekly[week] = (this.data.weekly[week] || 0) + data.tokens;

    this.saveData();
  }

  // 获取周数
  private getWeekNumber(timestamp: number): string {
    const date = new Date(timestamp);
    const startOfYear = new Date(date.getFullYear(), 0, 1);
    const pastDays = Math.floor((date.getTime() - startOfYear.getTime()) / (1000 * 60 * 60 * 24));
    const weekNumber = Math.ceil((pastDays + startOfYear.getDay() + 1) / 7);
    return `${date.getFullYear()}-W${weekNumber}`;
  }

  // 获取今日统计
  getTodayStats(): TokenStats {
    const today = new Date().toISOString().split('T')[0];
    const todayTokens = this.data.daily[today] || 0;

    const todayRecords = this.data.tokens.filter(
      r => r.date === today
    );

    return {
      total: todayTokens,
      count: todayRecords.length,
      average: todayRecords.length > 0 ? todayTokens / todayRecords.length : 0,
      max: Math.max(0, ...todayRecords.map(r => r.tokens)),
      min: Math.max(0, ...todayRecords.map(r => r.tokens))
    };
  }

  // 获取本周统计
  getWeekStats(): TokenStats {
    const currentWeek = this.getWeekNumber(Date.now());
    const weekTokens = this.data.weekly[currentWeek] || 0;

    const weekRecords = this.data.tokens.filter(
      r => r.week === currentWeek
    );

    return {
      total: weekTokens,
      count: weekRecords.length,
      average: weekRecords.length > 0 ? weekTokens / weekRecords.length : 0,
      max: Math.max(0, ...weekRecords.map(r => r.tokens)),
      min: Math.max(0, ...weekRecords.map(r => r.tokens))
    };
  }

  // 获取累计统计
  getTotalStats(): TokenStats {
    return {
      total: this.data.total,
      count: this.data.tokens.length,
      average: this.data.tokens.length > 0 ? this.data.total / this.data.tokens.length : 0,
      max: Math.max(0, ...this.data.tokens.map(r => r.tokens)),
      min: Math.max(0, ...this.data.tokens.map(r => r.tokens))
    };
  }

  // 获取节省建议
  getSavingSuggestions(): string[] {
    const suggestions: string[] = [];

    const todayStats = this.getTodayStats();
    const weekStats = this.getWeekStats();
    const totalStats = this.getTotalStats();

    // 今日消耗分析
    if (todayStats.total > 10000) {
      suggestions.push('⚠️ 今日 token 消耗较高（' + todayStats.total + '），建议检查是否有不必要的操作');
    } else if (todayStats.total > 5000) {
      suggestions.push('💡 今日 token 消耗中等（' + todayStats.total + '），可考虑优化操作流程');
    }

    // 平均消耗分析
    if (totalStats.average > 5000) {
      suggestions.push('⚠️ 平均每次会话消耗 ' + Math.round(totalStats.average) + ' token，建议优化会话流程');
    } else if (totalStats.average > 2000) {
      suggestions.push('💡 平均每次会话消耗 ' + Math.round(totalStats.average) + ' token，可考虑进一步优化');
    }

    // 高峰时段分析
    const hourlyStats = this.getHourlyStats();
    const peakHour = Object.entries(hourlyStats).sort((a, b) => b[1] - a[1])[0];
    if (peakHour && peakHour[1] > totalStats.total * 0.1) {
      suggestions.push('💡 ' + this.formatHour(peakHour[0]) + ' 是消耗高峰时段（占' + Math.round(peakHour[1] / totalStats.total * 100) + '%），可考虑在该时段减少非必要操作');
    }

    // 记录次数分析
    if (todayStats.count > 10) {
      suggestions.push('💡 今日记录次数较多（' + todayStats.count + '次），建议合并重复操作');
    }

    // 模型使用分析
    const modelStats = this.getModelStats();
    if (Object.keys(modelStats).length > 1) {
      suggestions.push('💡 使用了 ' + Object.keys(modelStats).length + ' 种不同模型，可考虑统一使用高效模型');
    }

    // 建议列表
    suggestions.push('');
    suggestions.push('## 节省 Token 的建议：');
    suggestions.push('');
    suggestions.push('### 1. 使用 Memory 优化');
    suggestions.push('- 使用 `memory_search` 而不是重复搜索');
    suggestions.push('- 使用 `memory_get` 获取特定部分');
    suggestions.push('- 避免重复读取 MEMORY.md');
    suggestions.push('');
    suggestions.push('### 2. 减少不必要的工具调用');
    suggestions.push('- 合并多个工具调用');
    suggestions.push('- 减少日志输出');
    suggestions.push('- 避免不必要的检查');
    suggestions.push('');
    suggestions.push('### 3. 优化查询');
    suggestions.push('- 使用更精确的搜索词');
    suggestions.push('- 限制结果数量');
    suggestions.push('- 使用缓存');
    suggestions.push('');
    suggestions.push('### 4. 会话管理');
    suggestions.push('- 定期清理不必要的历史');
    suggestions.push('- 使用会话重置');
    suggestions.push('- 避免过度轮次');
    suggestions.push('');
    suggestions.push('### 5. 使用更高效的模型');
    suggestions.push('- 优先使用 `zai/glm-4.7-flash`');
    suggestions.push('- 避免使用高 token 消耗的模型');

    return suggestions;
  }

  // 获取模型使用统计
  private getModelStats(): Record<string, number> {
    const modelStats: Record<string, number> = {};

    this.data.tokens.forEach(record => {
      modelStats[record.model] = (modelStats[record.model] || 0) + record.tokens;
    });

    return modelStats;
  }

  // 获取每小时统计
  private getHourlyStats(): Record<string, number> {
    const hourly: Record<string, number> = {};
    const now = new Date();
    const currentHour = now.getHours();

    for (let i = 0; i < 24; i++) {
      const hour = i.toString().padStart(2, '0');
      hourly[hour] = 0;
    }

    this.data.tokens.forEach(record => {
      const recordHour = new Date(record.timestamp).getHours();
      hourly[recordHour.toString().padStart(2, '0')] += record.tokens;
    });

    return hourly;
  }

  // 格式化小时
  private formatHour(hour: string): string {
    const hourNum = parseInt(hour);
    const ampm = hourNum >= 12 ? 'PM' : 'AM';
    const hour12 = hourNum % 12 || 12;
    return `${hour12}:00 ${ampm}`;
  }

  // 获取历史记录
  getHistory(limit: number = 50): TokenRecord[] {
    return this.data.tokens
      .sort((a, b) => b.timestamp - a.timestamp)
      .slice(0, limit);
  }

  // 清理历史数据
  cleanup(days: number = 30): void {
    const cutoffTime = Date.now() - days * 24 * 60 * 60 * 1000;
    this.data.tokens = this.data.tokens.filter(
      r => r.timestamp > cutoffTime
    );

    // 重新计算统计
    this.data.total = this.data.tokens.reduce((sum, r) => sum + r.tokens, 0);
    this.data.daily = {};
    this.data.weekly = {};

    this.data.tokens.forEach(r => {
      this.data.daily[r.date] = (this.data.daily[r.date] || 0) + r.tokens;
      this.data.weekly[r.week] = (this.data.weekly[r.week] || 0) + r.tokens;
    });

    this.saveData();
  }
}

// 导出单例
export const tokenTracker = new TokenTracker();

export { TokenTracker };
