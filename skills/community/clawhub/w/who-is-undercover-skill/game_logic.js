/**
 * Who is Undercover - Core Game Logic
 * Implements the complete game mechanics for the popular party game
 */

class UndercoverGame {
  constructor(playerCount = 6, humanPlayers = 1) {
    this.playerCount = Math.max(4, Math.min(10, playerCount));
    this.humanPlayers = Math.min(humanPlayers, this.playerCount);
    this.aiPlayers = this.playerCount - this.humanPlayers;
    
    // Game state
    this.currentRound = 1;
    this.gameActive = false;
    this.players = [];
    this.eliminatedPlayers = [];
    this.wordPairs = this.loadWordPairs();
    this.currentWords = null;
    this.descriptions = {};
    this.votes = {};
    this.gameWinner = null;
    
    this.initializePlayers();
  }
  
  loadWordPairs() {
    return [
      { civilian: "苹果", undercover: "香蕉" },
      { civilian: "咖啡", undercover: "茶" },
      { civilian: "飞机", undercover: "火车" },
      { civilian: "医生", undercover: "护士" },
      { civilian: "手机", undercover: "电脑" },
      { civilian: "足球", undercover: "篮球" },
      { civilian: "夏天", undercover: "冬天" },
      { civilian: "红色", undercover: "蓝色" },
      { civilian: "老师", undercover: "教授" },
      { civilian: "汽车", undercover: "摩托车" },
      { civilian: "电影", undercover: "电视剧" },
      { civilian: "米饭", undercover: "面条" },
      { civilian: "公园", undercover: "广场" },
      { civilian: "音乐", undercover: "舞蹈" },
      { civilian: "书", undercover: "杂志" }
    ];
  }
  
  initializePlayers() {
    // Select random word pair
    const randomPair = this.wordPairs[Math.floor(Math.random() * this.wordPairs.length)];
    this.currentWords = randomPair;
    
    // Determine number of undercovers (1-2 based on player count)
    const undercoverCount = this.playerCount <= 6 ? 1 : 2;
    
    // Create player array with roles
    const allPlayers = [];
    const undercoverIndices = this.getRandomIndices(this.playerCount, undercoverCount);
    
    for (let i = 0; i < this.playerCount; i++) {
      const isUndercover = undercoverIndices.includes(i);
      const role = isUndercover ? 'undercover' : 'civilian';
      const word = isUndercover ? randomPair.undercover : randomPair.civilian;
      
      allPlayers.push({
        id: i + 1,
        name: i < this.humanPlayers ? `玩家${i + 1}` : `AI${i + 1 - this.humanPlayers}`,
        role: role,
        word: word,
        isHuman: i < this.humanPlayers,
        isEliminated: false,
        description: '',
        voteTarget: null
      });
    }
    
    this.players = allPlayers;
    this.gameActive = true;
  }
  
  getRandomIndices(max, count) {
    const indices = [];
    while (indices.length < count) {
      const randomIndex = Math.floor(Math.random() * max);
      if (!indices.includes(randomIndex)) {
        indices.push(randomIndex);
      }
    }
    return indices;
  }
  
  submitDescription(playerId, description) {
    if (!this.gameActive || this.isPlayerEliminated(playerId)) {
      return { success: false, message: "Invalid action" };
    }
    
    const player = this.getPlayerById(playerId);
    if (!player) {
      return { success: false, message: "Player not found" };
    }
    
    player.description = description.trim();
    this.descriptions[playerId] = description.trim();
    
    // Check if all players have submitted descriptions
    if (Object.keys(this.descriptions).length === this.getActivePlayerCount()) {
      return { success: true, message: "All descriptions submitted. Ready for voting.", readyForVoting: true };
    }
    
    return { success: true, message: "Description submitted successfully." };
  }
  
  generateAIDescription(playerId) {
    const player = this.getPlayerById(playerId);
    if (!player || player.isHuman) {
      return null;
    }
    
    // AI generates a description that hints at their word without being too obvious
    const word = player.word;
    const isUndercover = player.role === 'undercover';
    
    // Simple AI logic - in real implementation, this would use LLM
    const genericDescriptions = [
      "这是一个很常见的东西。",
      "大家都经常用到它。",
      "它在生活中很重要。",
      "我觉得这个很有趣。",
      "很多人都喜欢这个。",
      "这是一个基础的日常用品。"
    ];
    
    // More specific hints based on word type
    let specificHint = "";
    if (word.includes("医生") || word.includes("护士") || word.includes("老师") || word.includes("教授")) {
      specificHint = "这是一个职业。";
    } else if (word.includes("苹果") || word.includes("香蕉") || word.includes("米饭") || word.includes("面条")) {
      specificHint = "这是一种食物。";
    } else if (word.includes("手机") || word.includes("电脑") || word.includes("汽车") || word.includes("摩托车")) {
      specificHint = "这是一种工具或设备。";
    } else if (word.includes("夏天") || word.includes("冬天") || word.includes("红色") || word.includes("蓝色")) {
      specificHint = "这是一种自然现象或颜色。";
    } else if (word.includes("足球") || word.includes("篮球") || word.includes("音乐") || word.includes("舞蹈")) {
      specificHint = "这是一种娱乐或体育活动。";
    }
    
    const description = specificHint || genericDescriptions[Math.floor(Math.random() * genericDescriptions.length)];
    player.description = description;
    this.descriptions[playerId] = description;
    
    return description;
  }
  
  submitVote(playerId, targetId) {
    if (!this.gameActive || this.isPlayerEliminated(playerId)) {
      return { success: false, message: "Invalid action" };
    }
    
    const voter = this.getPlayerById(playerId);
    const target = this.getPlayerById(targetId);
    
    if (!voter || !target) {
      return { success: false, message: "Invalid player" };
    }
    
    if (this.isPlayerEliminated(targetId)) {
      return { success: false, message: "Cannot vote for eliminated player" };
    }
    
    voter.voteTarget = targetId;
    this.votes[playerId] = targetId;
    
    // Check if all votes are in
    if (Object.keys(this.votes).length === this.getActivePlayerCount()) {
      return this.processVotingResults();
    }
    
    return { success: true, message: "Vote submitted successfully." };
  }
  
  generateAIVote(playerId) {
    const player = this.getPlayerById(playerId);
    if (!player || player.isHuman) {
      return null;
    }
    
    // AI voting logic - analyze descriptions to find suspicious ones
    const activePlayers = this.getActivePlayers();
    const otherPlayers = activePlayers.filter(p => p.id !== playerId);
    
    if (otherPlayers.length === 0) {
      return null;
    }
    
    // Simple AI logic: vote for someone with very generic or very specific description
    let suspiciousPlayer = otherPlayers[0];
    let maxSuspicion = 0;
    
    for (const otherPlayer of otherPlayers) {
      const desc = otherPlayer.description || '';
      let suspicion = 0;
      
      // Too generic
      if (desc.length < 10) {
        suspicion += 0.3;
      }
      // Too specific (mentions exact word)
      if (desc.includes(otherPlayer.word)) {
        suspicion += 0.8;
      }
      // Very different from others (simplified logic)
      suspicion += Math.random() * 0.2;
      
      if (suspicion > maxSuspicion) {
        maxSuspicion = suspicion;
        suspiciousPlayer = otherPlayer;
      }
    }
    
    player.voteTarget = suspiciousPlayer.id;
    this.votes[playerId] = suspiciousPlayer.id;
    return suspiciousPlayer.id;
  }
  
  processVotingResults() {
    // Count votes
    const voteCounts = {};
    for (const vote of Object.values(this.votes)) {
      voteCounts[vote] = (voteCounts[vote] || 0) + 1;
    }
    
    // Find player with most votes
    let maxVotes = 0;
    let eliminatedPlayerId = null;
    
    for (const [playerId, votes] of Object.entries(voteCounts)) {
      if (votes > maxVotes) {
        maxVotes = votes;
        eliminatedPlayerId = parseInt(playerId);
      } else if (votes === maxVotes) {
        // Tie - randomly select between tied players
        if (Math.random() > 0.5) {
          eliminatedPlayerId = parseInt(playerId);
        }
      }
    }
    
    if (eliminatedPlayerId) {
      const eliminatedPlayer = this.getPlayerById(eliminatedPlayerId);
      eliminatedPlayer.isEliminated = true;
      this.eliminatedPlayers.push(eliminatedPlayer);
      
      // Check win conditions
      const result = this.checkWinCondition();
      if (result.gameOver) {
        this.gameActive = false;
        this.gameWinner = result.winner;
        return {
          success: true,
          gameOver: true,
          winner: result.winner,
          eliminated: eliminatedPlayerId,
          message: `玩家${eliminatedPlayerId}被投票出局！${result.message}`
        };
      }
      
      // Reset for next round
      this.resetRound();
      return {
        success: true,
        eliminated: eliminatedPlayerId,
        message: `玩家${eliminatedPlayerId}被投票出局！游戏继续第${this.currentRound}轮。`
      };
    }
    
    // No elimination (shouldn't happen in normal play)
    this.resetRound();
    return {
      success: true,
      message: "投票结果平局，无人被淘汰。游戏继续。"
    };
  }
  
  checkWinCondition() {
    const activePlayers = this.getActivePlayers();
    const civilianCount = activePlayers.filter(p => p.role === 'civilian').length;
    const undercoverCount = activePlayers.filter(p => p.role === 'undercover').length;
    
    if (undercoverCount === 0) {
      return {
        gameOver: true,
        winner: 'civilians',
        message: "卧底全部被淘汰！平民获胜！"
      };
    }
    
    if (undercoverCount >= civilianCount) {
      return {
        gameOver: true,
        winner: 'undercovers',
        message: "卧底人数大于等于平民！卧底获胜！"
      };
    }
    
    return { gameOver: false };
  }
  
  resetRound() {
    this.currentRound++;
    this.descriptions = {};
    this.votes = {};
    
    // Generate AI descriptions for new round
    for (const player of this.getActivePlayers()) {
      if (!player.isHuman) {
        this.generateAIDescription(player.id);
      }
    }
  }
  
  getPlayerById(playerId) {
    return this.players.find(p => p.id === playerId);
  }
  
  isPlayerEliminated(playerId) {
    return this.eliminatedPlayers.some(p => p.id === playerId);
  }
  
  getActivePlayers() {
    return this.players.filter(p => !p.isEliminated);
  }
  
  getActivePlayerCount() {
    return this.getActivePlayers().length;
  }
  
  getGameState() {
    return {
      gameActive: this.gameActive,
      currentRound: this.currentRound,
      playerCount: this.playerCount,
      activePlayerCount: this.getActivePlayerCount(),
      civiliansRemaining: this.getActivePlayers().filter(p => p.role === 'civilian').length,
      undercoversRemaining: this.getActivePlayers().filter(p => p.role === 'undercover').length,
      gameOver: !this.gameActive && this.gameWinner !== null,
      winner: this.gameWinner,
      descriptionsSubmitted: Object.keys(this.descriptions).length,
      votesSubmitted: Object.keys(this.votes).length,
      players: this.players.map(p => ({
        id: p.id,
        name: p.name,
        isHuman: p.isHuman,
        isEliminated: p.isEliminated,
        hasDescription: !!this.descriptions[p.id],
        hasVoted: !!this.votes[p.id]
      }))
    };
  }
  
  getCurrentWordsForPlayer(playerId) {
    const player = this.getPlayerById(playerId);
    if (!player) return null;
    return {
      word: player.word,
      role: player.role,
      isUndercover: player.role === 'undercover'
    };
  }
}

module.exports = UndercoverGame;