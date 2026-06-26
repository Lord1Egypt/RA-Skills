/**
 * Who is Undercover - OpenClaw Skill Entry Point (Multiplayer Enhanced)
 * Main skill implementation that integrates with OpenClaw framework with multiplayer support
 */

const UndercoverGame = require('./game_logic');
const fs = require('fs');
const path = require('path');

// Global game instance storage with proper session management
let currentGames = new Map();
let playerSessions = new Map(); // Maps sessionId to { gameId, playerId }

/**
 * Skill metadata for OpenClaw
 */
const skillMetadata = {
  name: 'who-is-undercover',
  version: '1.1.0',
  description: '谁是卧底 - 经典派对游戏的AI版本，支持多人游戏',
  author: '龙5',
  category: 'games',
  keywords: ['桌游', 'party game', 'undercover', 'social deduction', 'multiplayer'],
  commands: {
    start: {
      description: '开始新游戏',
      usage: '/skill who-is-undercover start [玩家数量] [人类玩家数]',
      handler: handleStartGame
    },
    join: {
      description: '加入现有游戏',
      usage: '/skill who-is-undercover join [game_id]',
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
    },
    list: {
      description: '列出可加入的游戏',
      usage: '/skill who-is-undercover list',
      handler: handleListGames
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
  } else if (cmd === 'list') {
    return await handleListGames(args, context);
  } else {
    return {
      success: false,
      message: `未知命令: ${command}. 可用命令: start, join, describe, vote, status, end, list`
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
    
    // Register the creator as the first human player
    const humanPlayerId = 1; // First human player
    registerPlayerSession(context.sessionId, gameId, humanPlayerId);
    
    // Generate initial AI descriptions for non-human players
    const aiPlayers = game.getActivePlayers().filter(p => !p.isHuman);
    for (const aiPlayer of aiPlayers) {
      game.generateAIDescription(aiPlayer.id);
    }
    
    const gameState = game.getGameState();
    const currentPlayerWords = game.getCurrentWordsForPlayer(humanPlayerId);
    
    return {
      success: true,
      message: `游戏已创建！游戏ID: ${gameId}\n共有${playerCount}名玩家（${humanPlayers}名人类，${playerCount - humanPlayers}名AI）。\n\n你的身份是：${currentPlayerWords.role === 'civilian' ? '平民' : '卧底'}\n你的词语是：${currentPlayerWords.word}\n\n第1轮描述阶段开始，请使用 /skill who-is-undercover describe "[你的描述]" 提交描述。\n\n其他玩家可以使用以下命令加入游戏:\n/skill who-is-undercover join ${gameId}`,
      gameId: gameId,
      gameState: gameState,
      yourWord: currentPlayerWords.word,
      yourRole: currentPlayerWords.role,
      playerId: humanPlayerId
    };
  } catch (error) {
    return {
      success: false,
      message: `启动游戏失败: ${error.message}`
    };
  }
}

/**
 * List available games to join
 */
async function handleListGames(args, context) {
  let availableGames = [];
  
  for (let [gameId, game] of currentGames) {
    const gameState = game.getGameState();
    if (gameState.gameActive && !gameState.gameOver) {
      const humanPlayers = game.players.filter(p => p.isHuman && !p.isEliminated);
      const totalHumanSlots = game.humanPlayerCount;
      const availableSlots = totalHumanSlots - humanPlayers.length;
      
      if (availableSlots > 0) {
        availableGames.push({
          gameId: gameId,
          playerCount: game.playerCount,
          humanPlayers: humanPlayers.length,
          availableSlots: availableSlots
        });
      }
    }
  }
  
  if (availableGames.length === 0) {
    return {
      success: true,
      message: "当前没有可加入的游戏。可以使用 /skill who-is-undercover start 创建新游戏。"
    };
  }
  
  let message = "可加入的游戏列表：\n";
  availableGames.forEach(gameInfo => {
    message += `游戏ID: ${gameInfo.gameId} | 总玩家: ${gameInfo.playerCount} | 已加入人类: ${gameInfo.humanPlayers}/${gameInfo.humanPlayers + gameInfo.availableSlots}\n`;
  });
  
  message += "\n使用 /skill who-is-undercover join [游戏ID] 加入游戏";
  
  return {
    success: true,
    message: message,
    games: availableGames
  };
}

/**
 * Join an existing game
 */
async function handleJoinGame(args, context) {
  const gameId = args[0];
  
  if (!gameId) {
    return {
      success: false,
      message: "请提供游戏ID。使用 /skill who-is-undercover list 查看可加入的游戏。"
    };
  }
  
  if (!currentGames.has(gameId)) {
    return {
      success: false,
      message: `游戏ID ${gameId} 不存在或已结束。`
    };
  }
  
  const game = currentGames.get(gameId);
  const gameState = game.getGameState();
  
  if (!gameState.gameActive || gameState.gameOver) {
    return {
      success: false,
      message: "该游戏已结束或尚未开始。"
    };
  }
  
  // Find available human player slot
  const humanPlayers = game.players.filter(p => p.isHuman && !p.isEliminated);
  if (humanPlayers.length >= game.humanPlayerCount) {
    return {
      success: false,
      message: "该游戏的人类玩家槽位已满。"
    };
  }
  
  // Assign the next available human player ID
  let assignedPlayerId = null;
  for (let i = 0; i < game.players.length; i++) {
    if (game.players[i].isHuman && !game.players[i].isEliminated) {
      // Check if this human player slot is already taken
      let isTaken = false;
      for (let [sessionId, playerInfo] of playerSessions) {
        if (playerInfo.gameId === gameId && playerInfo.playerId === game.players[i].id) {
          isTaken = true;
          break;
        }
      }
      if (!isTaken) {
        assignedPlayerId = game.players[i].id;
        break;
      }
    }
  }
  
  if (assignedPlayerId === null) {
    return {
      success: false,
      message: "没有可用的人类玩家槽位。"
    };
  }
  
  // Register the player session
  registerPlayerSession(context.sessionId, gameId, assignedPlayerId);
  
  const currentPlayerWords = game.getCurrentWordsForPlayer(assignedPlayerId);
  
  return {
    success: true,
    message: `成功加入游戏 ${gameId}！\n\n你的身份是：${currentPlayerWords.role === 'civilian' ? '平民' : '卧底'}\n你的词语是：${currentPlayerWords.word}\n\n当前轮次：第${gameState.currentRound}轮\n请提交你的描述。`,
    gameId: gameId,
    playerId: assignedPlayerId,
    yourWord: currentPlayerWords.word,
    yourRole: currentPlayerWords.role
  };
}

/**
 * Submit description
 */
async function handleDescribe(args, context) {
  const playerInfo = getPlayerSession(context.sessionId);
  if (!playerInfo) {
    return {
      success: false,
      message: "没有找到进行中的游戏。请先加入或创建游戏。"
    };
  }
  
  const { gameId, playerId } = playerInfo;
  const game = currentGames.get(gameId);
  
  if (!game) {
    cleanupPlayerSession(context.sessionId);
    return {
      success: false,
      message: "游戏已结束。"
    };
  }
  
  const gameState = game.getGameState();
  if (!gameState.gameActive || gameState.gameOver) {
    cleanupPlayerSession(context.sessionId);
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
  
  // Submit the player's description
  const result = game.submitDescription(playerId, description);
  
  if (!result.success) {
    return result;
  }
  
  // Check if all descriptions are submitted
  const activePlayers = game.getActivePlayers();
  const descriptionsSubmitted = Object.keys(game.descriptions).length;
  
  if (descriptionsSubmitted === activePlayers.length) {
    // All descriptions submitted, generate AI votes for AI players
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
  const playerInfo = getPlayerSession(context.sessionId);
  if (!playerInfo) {
    return {
      success: false,
      message: "没有找到进行中的游戏。请先加入或创建游戏。"
    };
  }
  
  const { gameId, playerId } = playerInfo;
  const game = currentGames.get(gameId);
  
  if (!game) {
    cleanupPlayerSession(context.sessionId);
    return {
      success: false,
      message: "游戏已结束。"
    };
  }
  
  const gameState = game.getGameState();
  if (!gameState.gameActive || gameState.gameOver) {
    cleanupPlayerSession(context.sessionId);
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
  
  // Submit the player's vote
  const result = game.submitVote(playerId, targetId);
  
  if (!result.success) {
    return result;
  }
  
  // Check if all votes are submitted
  const activePlayers = game.getActivePlayers();
  const votesSubmitted = Object.keys(game.votes).length;
  
  if (votesSubmitted === activePlayers.length) {
    // All votes submitted, process elimination
    const eliminationResult = game.processVotingRound();
    
    if (eliminationResult.gameOver) {
      const finalResults = getFinalGameResults(game, eliminationResult);
      cleanupGame(gameId);
      return {
        success: true,
        gameOver: true,
        message: eliminationResult.message + "\n\n" + finalResults,
        winner: eliminationResult.winner,
        gameState: game.getGameState()
      };
    }
    
    // Game continues, generate AI descriptions for next round
    const aiPlayers = game.getActivePlayers().filter(p => !p.isHuman);
    for (const aiPlayer of aiPlayers) {
      game.generateAIDescription(aiPlayer.id);
    }
    
    const currentPlayerWords = game.getCurrentWordsForPlayer(playerId);
    return {
      success: true,
      message: eliminationResult.message + "\n\n第" + game.currentRound + "轮开始！\n你的词语是：" + currentPlayerWords.word + "\n请提交新的描述。",
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
  const playerInfo = getPlayerSession(context.sessionId);
  if (!playerInfo) {
    return {
      success: false,
      message: "没有找到进行中的游戏。请先加入或创建游戏。"
    };
  }
  
  const { gameId, playerId } = playerInfo;
  const game = currentGames.get(gameId);
  
  if (!game) {
    cleanupPlayerSession(context.sessionId);
    return {
      success: false,
      message: "游戏已结束。"
    };
  }
  
  const gameState = game.getGameState();
  if (!gameState.gameActive && !gameState.gameOver) {
    return {
      success: false,
      message: "游戏尚未开始。"
    };
  }
  
  const currentPlayerWords = game.getCurrentWordsForPlayer(playerId);
  
  let statusMessage = `游戏状态：\n`;
  statusMessage += `游戏ID: ${gameId}\n`;
  statusMessage += `你的玩家ID: ${playerId}\n`;
  statusMessage += `你的身份: ${currentPlayerWords.role === 'civilian' ? '平民' : '卧底'}\n`;
  statusMessage += `你的词语: ${currentPlayerWords.word}\n`;
  statusMessage += `当前轮次：第${gameState.currentRound}轮\n`;
  statusMessage += `活跃玩家：${gameState.activePlayerCount}人\n`;
  statusMessage += `平民剩余：${gameState.civiliansRemaining}人\n`;
  statusMessage += `卧底剩余：${gameState.undercoversRemaining}人\n`;
  
  if (gameState.gameOver) {
    statusMessage += `\n游戏结束！获胜方：${gameState.winner === 'civilians' ? '平民' : '卧底'}\n`;
  } else {
    const descriptionsSubmitted = Object.keys(game.descriptions).length;
    const votesSubmitted = Object.keys(game.votes).length;
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
  const playerInfo = getPlayerSession(context.sessionId);
  if (!playerInfo) {
    return {
      success: false,
      message: "没有找到进行中的游戏。"
    };
  }
  
  const { gameId } = playerInfo;
  cleanupGame(gameId);
  
  return {
    success: true,
    message: "游戏已结束。"
  };
}

/**
 * Helper functions for session management
 */
function registerPlayerSession(sessionId, gameId, playerId) {
  playerSessions.set(sessionId, { gameId, playerId });
}

function getPlayerSession(sessionId) {
  return playerSessions.get(sessionId);
}

function cleanupPlayerSession(sessionId) {
  playerSessions.delete(sessionId);
}

function cleanupGame(gameId) {
  // Remove game from currentGames
  currentGames.delete(gameId);
  
  // Remove all player sessions for this game
  for (let [sessionId, playerInfo] of playerSessions) {
    if (playerInfo.gameId === gameId) {
      playerSessions.delete(sessionId);
    }
  }
}

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