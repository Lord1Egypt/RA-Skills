// InStreet游戏控制器 - 主控制逻辑
const InStreetGameAdapter = require('./instreet_adapter');
const fs = require('fs');

class InStreetGameController {
  constructor(apiKey) {
    this.adapter = new InStreetGameAdapter(apiKey);
    this.gameState = null;
    this.roomId = null;
  }

  // 创建并开始游戏
  async createAndStartGame() {
    console.log('🚀 开始创建InStreet桌游室房间...');
    
    // 创建房间
    const roomResult = await this.adapter.createSpyRoom('龙5的卧底对决', 6);
    if (!roomResult.success) {
      console.error('❌ 创建房间失败:', roomResult.error);
      return false;
    }
    
    this.roomId = roomResult.roomId;
    console.log(`✅ 房间创建成功!`);
    console.log(`🔗 房间链接: ${roomResult.roomUrl}`);
    console.log(`🎮 加入API: ${roomResult.joinApi}`);
    
    // 保存房间信息
    const roomInfo = {
      roomId: this.roomId,
      roomUrl: roomResult.roomUrl,
      joinApi: roomResult.joinApi,
      createdAt: new Date().toISOString(),
      status: 'waiting'
    };
    
    fs.writeFileSync('current_instreet_room.json', JSON.stringify(roomInfo, null, 2));
    console.log('💾 房间信息已保存到 current_instreet_room.json');
    
    return true;
  }

  // 游戏主循环
  async gameLoop() {
    console.log('🔄 开始游戏主循环...');
    
    while (true) {
      try {
        // 轮询活动状态
        const activity = await this.adapter.getActivity();
        if (!activity.success) {
          console.error('获取活动状态失败:', activity.error);
          await this.sleep(3000);
          continue;
        }
        
        const game = activity.data.active_game;
        if (!game) {
          console.log('📭 没有进行中的对局，等待新房间...');
          break;
        }
        
        console.log(`📊 当前游戏状态: ${game.status}, 阶段: ${game.phase || 'unknown'}`);
        
        // 检查是否轮到我们
        if (game.is_your_turn) {
          console.log('🎯 轮到我们了!');
          
          if (game.phase === 'describe') {
            await this.handleDescribePhase(game);
          } else if (game.phase === 'vote') {
            await this.handleVotePhase(game);
          }
        }
        
        // 等待2秒后继续轮询
        await this.sleep(2000);
        
      } catch (error) {
        console.error('游戏循环错误:', error.message);
        await this.sleep(3000);
      }
    }
  }

  // 处理描述阶段
  async handleDescribePhase(game) {
    const myWord = game.my_word;
    console.log(`📝 我的词语: ${myWord}`);
    
    // 这里可以集成更复杂的AI描述生成逻辑
    // 目前使用简单的策略
    const descriptions = [
      "这是一个很常见的东西",
      "很多人都在用这个",
      "这是现代生活中不可缺少的",
      "这个东西很有用"
    ];
    
    const description = descriptions[Math.floor(Math.random() * descriptions.length)];
    const reasoning = `随机选择描述策略`;
    
    console.log(`💬 提交描述: "${description}"`);
    const result = await this.adapter.submitDescription(this.roomId, description, reasoning);
    
    if (result.success) {
      console.log('✅ 描述提交成功!');
    } else {
      console.error('❌ 描述提交失败:', result.error);
    }
  }

  // 处理投票阶段
  async handleVotePhase(game) {
    const alivePlayers = game.alive_players;
    const descriptions = game.descriptions;
    
    console.log(`🗳️ 投票阶段 - 存活玩家: ${alivePlayers.length}`);
    
    // 简单投票策略：随机投票（实际应用中需要更复杂的分析）
    const otherPlayers = alivePlayers.filter(player => player.username !== '你');
    if (otherPlayers.length > 0) {
      const randomTarget = otherPlayers[Math.floor(Math.random() * otherPlayers.length)];
      const targetSeat = randomTarget.seat;
      
      console.log(`🎯 投票目标: 玩家${targetSeat} (${randomTarget.username})`);
      const reasoning = `随机投票策略`;
      
      const result = await this.adapter.submitVote(this.roomId, targetSeat, reasoning);
      
      if (result.success) {
        console.log('✅ 投票提交成功!');
      } else {
        console.error('❌ 投票提交失败:', result.error);
      }
    }
  }

  // 睡眠工具函数
  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// 主执行函数
async function main() {
  const apiKey = 'sk_inst_22609319753836272e6a044f4e9a44f3';
  const controller = new InStreetGameController(apiKey);
  
  // 创建房间
  const created = await controller.createAndStartGame();
  if (!created) {
    console.log('❌ 房间创建失败，退出程序');
    return;
  }
  
  // 开始游戏循环
  await controller.gameLoop();
}

// 如果直接运行此文件，则执行主函数
if (require.main === module) {
  main().catch(console.error);
}

module.exports = InStreetGameController;