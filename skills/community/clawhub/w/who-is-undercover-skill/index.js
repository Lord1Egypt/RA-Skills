/**
 * Who is Undercover - OpenClaw Skill Entry Point
 * Main skill implementation that integrates with OpenClaw framework
 */

const UndercoverGame = require('./game_logic');
const fs = require('fs');
const path = require('path');

// Global game instance storage (in real implementation, this would use proper session storage)
let currentGames = new Map();

/**
 * Skill metadata for OpenClaw
 */
const skillMetadata = {
  name: 'who-is-undercover',
  version: '1.0.0',
  description: '谁是卧底 - 经典派对游戏的AI版本',
  author: '龙5',
  category: 'games',
  keywords: ['桌游', 'party game', 'undercover', 'social deduction'],
  commands: {
    start: {
      description: '开始新游戏',
      usage: '/skill who-is-undercover start [玩家数量] [人类玩家数]',
      handler: handleStartGame
    },
    join: {
      description: '加入现有游戏',
      usage: '/skill who-is-undercover join',
      handler: handleJoinGame
    },
    describe: {
      description: '提交你的描述',
      usage: '/skill who-is-undercover describe "[描述内容]"',
      handler: handleDescribe
    },
    vote: {
      description: '投票给玩家',
      usage: '/skill who-is-undercover vote [玩家编号]',
      handler: handleVote
    },
    status: {
      description: '查看游戏状态',
      usage: '/skill who-is-undercover status',
      handler: handleStatus
    },
    end: {
      description: '结束当前游戏',
      usage: '/skill who-is-undercover end',
      handler: handleEndGame
    }
  }
};

/**
 * Handle skill command routing
 */
async function handleCommand(command, args, context) {
  const cmd = command.toLowerCase();
  
  if (cmd === 'start') {
    return await handleStartGame(args, context);
  } else if (cmd === 'join') {
    return await handleJoinGame(args, context);
  } else if (cmd === 'describe') {
    return await handleDescribe(args, context);
  } else if (cmd === 'vote') {
    return await handleVote(args, context);
  } else if (cmd === 'status') {
    return await handleStatus(args, context);
  } else if (cmd === 'end') {
    return await handleEndGame(args, context);
  } else {
    return {
      success: false,
      message: `未知命令: ${command}. 可用命令: start, join, describe, vote, status, end`
    };
  }
}

/**
 * Start a new game
 */
async function handleStartGame(args, context) {
  try {
    const playerCount = parseInt(args[0]) || 6;
    const humanPlayers = parseInt(args[1]) || 1;
    
    if (playerCount < 4 || playerCount > 10) {
      return {
        success: false,
        message: "玩家数量必须在4-10之间"
      };
    }
    
    if (humanPlayers < 1 || humanPlayers > playerCount) {
      return {
        success: false,
        message: "人类玩家数量必须在1-总玩家数之间"
      };
    }
    
    // Create new game instance
    const gameId = generateGameId();
    const game = new UndercoverGame(playerCount, humanPlayers);
    
    currentGames.set(gameId, game);
    
    // Store game ID in context for this session
    context.gameId = gameId;
    
    // Generate initial AI descriptions
    const aiPlayers = game.getActivePlayers().filter(p => !p.isHuman);
    for (const aiPlayer of aiPlayers) {
      game.generateAIDescription(aiPlayer.id);
    }
    
    const gameState = game.getGameState();
    const currentPlayerWords = game.getCurrentWordsForPlayer(1); // Human player 1
    
    return {
      success: true,
      message: `游戏已开始！共有${playerCount}名玩家（${humanPlayers}名人类，${playerCount - humanPlayers}名AI）。\n\n你的身份是：${currentPlayerWords.role === 'civilian' ? '平民' : '卧底'}\n你的词语是：${currentPlayerWords.word}\n\n第1轮描述阶段开始，请使用 /skill who-is-undercover describe "[你的描述]" 提交描述。`,
      gameId: gameId,
      gameState: gameState,
      yourWord: currentPlayerWords.word,
      yourRole: currentPlayerWords.role
    };
  } catch (error) {
    return {
      success: false,
      message: `启动游戏失败: ${error.message}`
    };
  }
}

/**
 * Join an existing game
 */
async function handleJoinGame(args, context) {
  // In a real implementation, this would handle multiple human players
  // For now, we assume the game was started by this user
  const gameId = context.gameId;
  
  if (!gameId || !currentGames.has(gameId)) {
    return {
      success: false,
      message: "没有找到进行中的游戏。请先使用 /skill who-is-undercover start 开始游戏。"
    };
  }
  
  const game = currentGames.get(gameId);
  const gameState = game.getGameState();
  
  if (!gameState.gameActive) {
    return {
      success: false,
      message: "游戏已结束。"
    };
  }
  
  // Find the next available human player slot
  const humanPlayers = game.players.filter(p => p.isHuman && !p.isEliminated);
  if (humanPlayers.length === 0) {
    return {
      success: false,
      message: "没有可用的人类玩家槽位。"
    };
  }
  
  const currentPlayer = humanPlayers[0]; // Simplified - in real implementation, track which human is which
  const currentPlayerWords = game.getCurrentWordsForPlayer(currentPlayer.id);
  
  return {
    success: true,
    message: `已加入游戏！\n\n你的身份是：${currentPlayerWords.role === 'civilian' ? '平民' : '卧底'}\n你的词语是：${currentPlayerWords.word}\n\n当前轮次：第${gameState.currentRound}轮\n请提交你的描述。`,
    gameState: gameState,
    yourWord: currentPlayerWords.word,
    yourRole: currentPlayerWords.role
  };
}

/**
 * Submit description
 */
async function handleDescribe(args, context) {
  const gameId = context.gameId;
  if (!gameId || !currentGames.has(gameId)) {
    return {
      success: false,
      message: "没有找到进行中的游戏。"
    };
  }
  
  const game = currentGames.get(gameId);
  const gameState = game.getGameState();
  
  if (!gameState.gameActive) {
    return {
      success: false,
      message: "游戏已结束。"
    };
  }
  
  const description = args.join(' ').trim();
  if (!description) {
    return {
      success: false,
      message: "请输入有效的描述内容。"
    };
  }
  
  // Submit human player description (assume player 1 for simplicity)
  const result = game.submitDescription(1, description);
  
  if (!result.success) {
    return result;
  }
  
  // Check if all descriptions are in and generate AI votes if needed
  if (result.readyForVoting) {
    // Generate AI votes
    const activePlayers = game.getActivePlayers();
    const aiPlayers = activePlayers.filter(p => !p.isHuman);
    for (const aiPlayer of aiPlayers) {
      game.generateAIVote(aiPlayer.id);
    }
    
    return {
      success: true,
      message: "所有描述已提交！投票阶段开始。\n\n请使用 /skill who-is-undercover vote [玩家编号] 进行投票。\n\n各玩家描述：\n" + formatDescriptions(game),
      gameState: game.getGameState(),
      readyForVoting: true
    };
  }
  
  return {
    success: true,
    message: "描述已提交！等待其他玩家提交描述...",
    gameState: game.getGameState()
  };
}

/**
 * Submit vote
 */
async function handleVote(args, context) {
  const gameId = context.gameId;
  if (!gameId || !currentGames.has(gameId)) {
    return {
      success: false,
      message: "没有找到进行中的游戏。"
    };
  }
  
  const game = currentGames.get(gameId);
  const gameState = game.getGameState();
  
  if (!gameState.gameActive) {
    return {
      success: false,
      message: "游戏已结束。"
    };
  }
  
  const targetId = parseInt(args[0]);
  if (isNaN(targetId) || targetId < 1 || targetId > game.playerCount) {
    return {
      success: false,
      message: "请输入有效的玩家编号（1-" + game.playerCount + "）。"
    };
  }
  
  // Submit human player vote (assume player 1 for simplicity)
  const result = game.submitVote(1, targetId);
  
  if (!result.success) {
    return result;
  }
  
  // If game is over, show results
  if (result.gameOver) {
    const finalResults = getFinalGameResults(game, result);
    return {
      success: true,
      gameOver: true,
      message: result.message + "\n\n" + finalResults,
      winner: result.winner,
      gameState: game.getGameState()
    };
  }
  
  // If voting complete but game continues
  if (result.eliminated) {
    const currentPlayerWords = game.getCurrentWordsForPlayer(1);
    return {
      success: true,
      message: result.message + "\n\n第" + game.currentRound + "轮开始！\n你的词语是：" + currentPlayerWords.word + "\n请提交新的描述。",
      gameState: game.getGameState(),
      yourWord: currentPlayerWords.word
    };
  }
  
  return {
    success: true,
    message: "投票已提交！等待其他玩家投票...",
    gameState: game.getGameState()
  };
}

/**
 * Show game status
 */
async function handleStatus(args, context) {
  const gameId = context.gameId;
  if (!gameId || !currentGames.has(gameId)) {
    return {
      success: false,
      message: "没有找到进行中的游戏。"
    };
  }
  
  const game = currentGames.get(gameId);
  const gameState = game.getGameState();
  
  if (!gameState.gameActive && !gameState.gameOver) {
    return {
      success: false,
      message: "游戏尚未开始。"
    };
  }
  
  let statusMessage = `游戏状态：\n`;
  statusMessage += `当前轮次：第${gameState.currentRound}轮\n`;
  statusMessage += `活跃玩家：${gameState.activePlayerCount}人\n`;
  statusMessage += `平民剩余：${gameState.civiliansRemaining}人\n`;
  statusMessage += `卧底剩余：${gameState.undercoversRemaining}人\n`;
  
  if (gameState.gameOver) {
    statusMessage += `\n游戏结束！获胜方：${gameState.winner === 'civilians' ? '平民' : '卧底'}\n`;
  } else {
    const descriptionsSubmitted = gameState.descriptionsSubmitted;
    const votesSubmitted = gameState.votesSubmitted;
    const totalActive = gameState.activePlayerCount;
    
    if (descriptionsSubmitted < totalActive) {
      statusMessage += `\n描述阶段：${descriptionsSubmitted}/${totalActive} 已提交\n`;
    } else if (votesSubmitted < totalActive) {
      statusMessage += `\n投票阶段：${votesSubmitted}/${totalActive} 已投票\n`;
      statusMessage += `\n各玩家描述：\n${formatDescriptions(game)}\n`;
    }
  }
  
  return {
    success: true,
    message: statusMessage,
    gameState: gameState
  };
}

/**
 * End current game
 */
async function handleEndGame(args, context) {
  const gameId = context.gameId;
  if (!gameId || !currentGames.has(gameId)) {
    return {
      success: false,
      message: "没有找到进行中的游戏。"
    };
  }
  
  currentGames.delete(gameId);
  delete context.gameId;
  
  return {
    success: true,
    message: "游戏已结束。"
  };
}

/**
 * Helper functions
 */
function generateGameId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2, 5);
}

function formatDescriptions(game) {
  const activePlayers = game.getActivePlayers();
  let descText = "";
  
  activePlayers.forEach(player => {
    const desc = game.descriptions[player.id] || "（未提交）";
    descText += `玩家${player.id} (${player.name}): ${desc}\n`;
  });
  
  return descText;
}

function getFinalGameResults(game, result) {
  let results = "=== 最终结果 ===\n";
  
  // Show all players and their roles
  game.players.forEach(player => {
    const status = player.isEliminated ? "（已淘汰）" : "（存活）";
    results += `玩家${player.id}: ${player.role === 'civilian' ? '平民' : '卧底'} - ${player.word} ${status}\n`;
  });
  
  results += `\n获胜方：${result.winner === 'civilians' ? '平民团队' : '卧底团队'}\n`;
  results += `\n感谢参与游戏！`;
  
  return results;
}

// Export skill interface
module.exports = {
  metadata: skillMetadata,
  handleCommand: handleCommand,
  // For testing purposes
  UndercoverGame: UndercoverGame
};