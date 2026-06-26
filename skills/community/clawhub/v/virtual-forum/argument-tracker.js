/**
 * 论点追踪器
 * Argument Tracker for Virtual Forum v3.5
 *
 * 修复：
 * - [P0] rebutral → rebuttal 拼写错误（导致反驳功能完全崩溃）
 * - 增加输入验证
 * - 增加统计摘要方法
 */

class ArgumentTracker {
  constructor() {
    this.arguments = [];
    this.scores = {};
    this.relationships = [];
  }

  /**
   * 添加论点
   */
  addArgument(participant, content, type, round) {
    // 输入验证
    if (!participant || typeof participant !== 'string') {
      throw new Error('participant 不能为空');
    }
    if (!content || typeof content !== 'string') {
      throw new Error('content 不能为空');
    }

    const argument = {
      id: this.arguments.length + 1,
      participant,
      content,
      type: type || 'statement', // 'statement' | 'challenge' | 'rebuttal' | 'question' | 'answer'
      round: round || 0,
      timestamp: Date.now(),
      rebuttals: [],
      isRebutted: false,
      points: 0
    };

    this.arguments.push(argument);

    // 初始化分数
    if (!this.scores[participant]) {
      this.scores[participant] = { total: 0, points: 0, rebuttals: 0, rebutted: 0 };
    }

    return argument;
  }

  /**
   * 添加反驳
   * [P0 FIX] 修复 rebutral → rebuttal 拼写错误
   */
  addRebuttal(rebutter, targetArgumentId, content) {
    // 输入验证
    if (!rebutter) throw new Error('rebutter 不能为空');
    if (!targetArgumentId) throw new Error('targetArgumentId 不能为空');
    if (!content) throw new Error('content 不能为空');

    const target = this.arguments.find(a => a.id === targetArgumentId);
    if (!target) {
      console.warn(`⚠️ 未找到目标论点 #${targetArgumentId}`);
      return null;
    }

    // [P0 FIX] 变量名修正：rebutral → rebuttal
    const rebuttal = {
      id: this.arguments.length + 1,
      participant: rebutter,
      content,
      type: 'rebuttal',
      round: target.round,
      timestamp: Date.now(),
      target: targetArgumentId,
      rebuttals: [],
      isRebutted: false,
      points: 0
    };

    // [P0 FIX] 使用正确的变量名
    this.arguments.push(rebuttal);
    target.rebuttals.push(rebuttal.id);
    target.isRebutted = true;

    // 计分
    this.awardPoints(rebutter, 'rebuttal_success', 3);
    this.awardPoints(target.participant, 'rebutted', -1);

    // 记录关系
    this.relationships.push({
      from: rebuttal.id,
      to: targetArgumentId,
      type: 'rebuts'
    });

    return rebuttal;
  }

  /**
   * 奖励分数
   */
  awardPoints(participant, action, points) {
    if (!this.scores[participant]) {
      this.scores[participant] = { total: 0, points: 0, rebuttals: 0, rebutted: 0 };
    }

    this.scores[participant].total += points;
    this.scores[participant].points += points;

    if (action === 'rebuttal_success') {
      this.scores[participant].rebuttals++;
    } else if (action === 'rebutted') {
      this.scores[participant].rebutted++;
    }
  }

  /**
   * 获取参与者的论点
   */
  getParticipantArguments(participant) {
    return this.arguments.filter(a => a.participant === participant);
  }

  /**
   * 获取论点关系图
   */
  getArgumentGraph() {
    return this.arguments.map(a => ({
      id: a.id,
      participant: a.participant,
      type: a.type,
      content: a.content.slice(0, 100),
      isRebutted: a.isRebutted,
      rebuttals: a.rebuttals.length
    }));
  }

  /**
   * 获取排行榜
   */
  getLeaderboard() {
    return Object.entries(this.scores)
      .map(([name, score]) => ({ name, ...score }))
      .sort((a, b) => b.total - a.total);
  }

  /**
   * 获取统计摘要
   */
  getSummary() {
    const totalArgs = this.arguments.length;
    const totalRebuttals = this.arguments.filter(a => a.type === 'rebuttal').length;
    const unrebutted = this.arguments.filter(a => a.type === 'statement' && !a.isRebutted).length;
    const leaderboard = this.getLeaderboard();

    return {
      totalArguments: totalArgs,
      totalRebuttals,
      unrebuttedStatements: unrebutted,
      leaderboard,
      winner: leaderboard.length > 0 ? leaderboard[0].name : null
    };
  }
}

module.exports = ArgumentTracker;