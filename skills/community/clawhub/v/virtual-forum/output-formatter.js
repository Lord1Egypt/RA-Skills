/**
 * 输出格式化器
 * Output Formatter for Virtual Forum v3.5
 * 
 * 修复：
 * - [P2] 补全被截断的 formatReport 方法
 * - 增加 formatDecision 实现
 */

class OutputFormatter {
  constructor() {
    this.formats = {
      dialogue: 'dialogue',
      report: 'report',
      decision: 'decision',
      json: 'json'
    };
  }

  format(forum, formatType = 'dialogue') {
    switch (formatType) {
      case 'dialogue': return this.formatDialogue(forum);
      case 'report': return this.formatReport(forum);
      case 'decision': return this.formatDecision(forum);
      case 'json': return this.formatJSON(forum);
      default: return this.formatDialogue(forum);
    }
  }

  formatDialogue(forum) {
    let output = '';
    output += this.formatOpening(forum);
    for (const round of (forum.roundsData || [])) {
      output += this.formatRound(round, forum.participants.length);
    }
    output += this.formatResult(forum.result);
    return output;
  }

  formatOpening(forum) {
    let text = `\n${'═'.repeat(60)}\n`;
    text += `🎭 虚拟论坛: ${forum.topic}\n`;
    text += `${'═'.repeat(60)}\n\n`;
    text += `📋 模式: ${forum.mode} | 轮次: ${forum.rounds}\n`;
    text += `👥 参与者: ${forum.participants.map(p => p.name).join(' vs ')}\n`;
    text += `🎙️ 主持人: ${forum.moderator?.name || '默认'}\n\n`;
    text += `${'─'.repeat(60)}\n\n`;
    return text;
  }

  formatRound(round, participantCount) {
    let text = `\n📍 第 ${round.number} 轮\n\n`;
    for (const speech of (round.speeches || [])) {
      text += `【${speech.speaker}】\n${speech.content}\n\n`;
    }
    text += `${'─'.repeat(40)}\n`;
    return text;
  }

  formatResult(result) {
    if (!result) return '\n（讨论尚未产生结果）\n';
    let text = `\n${'═'.repeat(60)}\n`;
    text += `🏆 讨论结果\n`;
    text += `${'═'.repeat(60)}\n\n`;
    text += this.formatResultText(result);
    return text;
  }

  formatResultText(result) {
    if (!result) return '暂无结果\n';
    if (typeof result === 'string') return result + '\n';
    let text = '';
    if (result.winner) text += `🥇 胜出: ${result.winner}\n`;
    if (result.summary) text += `📝 总结: ${result.summary}\n`;
    if (result.scores) {
      text += `\n📊 得分:\n`;
      for (const [name, score] of Object.entries(result.scores)) {
        text += ` ${name}: ${score} 分\n`;
      }
    }
    return text;
  }

  /**
   * 报告格式（[P2 FIX] 补全被截断的代码）
   */
  formatReport(forum) {
    let report = '';
    report += `# 🎭 虚拟论坛讨论报告\n\n`;
    report += `---\n\n`;
    report += `## 📌 讨论话题\n${forum.topic}\n\n`;

    report += `## ⚙️ 讨论配置\n`;
    report += `- 模式: ${forum.mode}\n`;
    report += `- 轮次: ${forum.rounds}\n`;
    report += `- 主持人: ${forum.moderator?.name || '默认'}\n`;
    report += `- 判定方式: ${forum.verdictType || '点数制'}\n\n`;

    report += `## 👥 参与者\n`;
    for (const p of (forum.participants || [])) {
      report += `- **${p.name}**\n`;
    }
    report += `\n`;

    report += `## 💬 核心论点\n\n`;
    for (const [name, args] of Object.entries(forum.arguments || {})) {
      report += `### ${name}\n`;
      const topArgs = (args || [])
        .filter(a => a.type === 'statement' || a.type === '立论')
        .slice(0, 3);
      for (const arg of topArgs) {
        const text = arg.text || arg.content || '';
        report += `> ${text.slice(0, 200)}${text.length > 200 ? '...' : ''}\n\n`;
      }
    }

    report += `## 🏆 结果\n`;
    report += this.formatResultText(forum.result);
    report += `\n\n`;

    // [P2 FIX] 补全统计数据部分
    report += `## 📊 统计数据\n\n`;
    report += `| 参与者 | 得分 | 发言次数 |\n`;
    report += `|--------|------|----------|\n`;
    for (const p of (forum.participants || [])) {
      const score = forum.scores?.[p.name] || 0;
      const speeches = (forum.roundsData || [])
        .reduce((count, round) => {
          return count + (round.speeches || []).filter(s => s.speaker === p.name).length;
        }, 0);
      report += `| ${p.name} | ${score} | ${speeches} |\n`;
    }
    report += `\n`;

    report += `---\n`;
    report += `*报告生成时间: ${new Date().toLocaleString('zh-CN')}*\n`;

    return report;
  }

  /**
   * 决策格式
   */
  formatDecision(forum) {
    let decision = '';
    decision += `# 📋 决策报告: ${forum.topic}\n\n`;
    decision += `## 参与决策的专家\n`;
    for (const p of (forum.participants || [])) {
      decision += `- ${p.name}\n`;
    }
    decision += `\n## 各方观点摘要\n\n`;
    for (const [name, args] of Object.entries(forum.arguments || {})) {
      decision += `### ${name} 的核心主张\n`;
      const statements = (args || []).filter(a => a.type === 'statement').slice(0, 2);
      for (const s of statements) {
        decision += `- ${(s.text || s.content || '').slice(0, 150)}\n`;
      }
      decision += `\n`;
    }
    decision += `## 最终决策建议\n`;
    decision += this.formatResultText(forum.result);
    return decision;
  }

  formatJSON(forum) {
    return JSON.stringify({
      id: forum.id,
      topic: forum.topic,
      mode: forum.mode,
      rounds: forum.rounds,
      participants: (forum.participants || []).map(p => p.name),
      arguments: forum.arguments,
      scores: forum.scores,
      result: forum.result,
      generatedAt: new Date().toISOString()
    }, null, 2);
  }
}

module.exports = OutputFormatter;
