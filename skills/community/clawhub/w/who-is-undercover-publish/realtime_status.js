// 实时游戏状态监控脚本
const fs = require('fs');
const path = require('path');

class GameStatusMonitor {
  constructor(gameId) {
    this.gameId = gameId;
    this.gameFile = path.join(__dirname, 'current_game.json');
    this.statusFile = path.join(__dirname, 'game_status.txt');
  }

  // 读取当前游戏状态
  readGameState() {
    try {
      const data = fs.readFileSync(this.gameFile, 'utf8');
      return JSON.parse(data);
    } catch (error) {
      console.error('读取游戏状态失败:', error);
      return null;
    }
  }

  // 生成实时状态报告
  generateStatusReport() {
    const gameState = this.readGameState();
    if (!gameState) return '游戏状态不可用';

    let report = `🎮 **谁是卧底 - 实时进度**\n\n`;
    report += `**游戏ID**: ${gameState.gameId}\n`;
    report += `**当前轮次**: 第${gameState.currentRound}轮\n`;
    report += `**当前阶段**: ${gameState.currentPhase === 'description' ? '描述阶段' : '投票阶段'}\n\n`;

    // 显示已提交的描述
    if (gameState.descriptions && gameState.descriptions.length > 0) {
      report += `**已提交描述**:\n`;
      gameState.descriptions.forEach(desc => {
        report += `- ${desc.playerName}: "${desc.description}"\n`;
      });
      report += `\n`;
    }

    // 显示投票情况
    if (gameState.votes && Object.keys(gameState.votes).length > 0) {
      report += `**投票情况**:\n`;
      Object.entries(gameState.votes).forEach(([voter, target]) => {
        report += `- ${voter} → 玩家${target}\n`;
      });
      report += `\n`;
    }

    // 显示存活玩家
    const alivePlayers = gameState.players.filter(p => p.alive);
    report += `**存活玩家** (${alivePlayers.length}/${gameState.players.length}):\n`;
    alivePlayers.forEach(player => {
      const roleEmoji = player.role === 'undercover' ? '🕵️' : '👤';
      report += `- 玩家${player.id} ${roleEmoji}\n`;
    });

    return report;
  }

  // 更新状态文件
  updateStatusFile() {
    const report = this.generateStatusReport();
    fs.writeFileSync(this.statusFile, report, 'utf8');
    console.log('状态文件已更新');
  }

  // 模拟AI代理行动
  simulateAIAction() {
    const gameState = this.readGameState();
    if (!gameState) return;

    // 如果是描述阶段，AI提交描述
    if (gameState.currentPhase === 'description') {
      const aiPlayer = gameState.players.find(p => p.name.includes('AI代理'));
      if (aiPlayer && !gameState.descriptions.some(d => d.playerId === aiPlayer.id)) {
        const descriptions = [
          "这是一种常见的交通工具",
          "它在现代生活中很重要", 
          "很多人都使用过这个",
          "这是现代科技的产物"
        ];
        const randomDesc = descriptions[Math.floor(Math.random() * descriptions.length)];
        
        gameState.descriptions.push({
          playerId: aiPlayer.id,
          playerName: aiPlayer.name,
          description: randomDesc
        });
        
        console.log(`AI代理提交描述: "${randomDesc}"`);
      }
    }

    // 如果所有玩家都提交了描述，进入投票阶段
    if (gameState.descriptions.length >= gameState.players.length) {
      gameState.currentPhase = 'voting';
      console.log('进入投票阶段');
    }

    fs.writeFileSync(this.gameFile, JSON.stringify(gameState, null, 2), 'utf8');
  }
}

// 主执行函数
const monitor = new GameStatusMonitor('wg-20260326-2324');
monitor.simulateAIAction();
monitor.updateStatusFile();

module.exports = GameStatusMonitor;