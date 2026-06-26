/**
 * Comprehensive test for Who is Undercover skill
 * Simulates a complete game flow with multiple rounds
 */

const { UndercoverGame } = require('./index');

console.log("=== Comprehensive Who is Undercover Test ===\n");

// Test full game flow
function testFullGame() {
  console.log("Starting 6-player game (1 human, 5 AI)...\n");
  
  const game = new UndercoverGame(6, 1);
  const gameState = game.getGameState();
  
  console.log(`Game started! Round ${gameState.currentRound}`);
  console.log(`Players: ${gameState.playerCount} (${gameState.civiliansRemaining} civilians, ${gameState.undercoversRemaining} undercovers)\n`);
  
  // Get human player info
  const humanPlayerWords = game.getCurrentWordsForPlayer(1);
  console.log(`Human player word: "${humanPlayerWords.word}" (${humanPlayerWords.role})\n`);
  
  // Round 1
  console.log("=== ROUND 1 ===");
  
  // Submit human description
  const humanDesc = "这是一个很常见的东西，大家都用过。";
  game.submitDescription(1, humanDesc);
  console.log(`Human submitted: "${humanDesc}"`);
  
  // Submit AI descriptions (already generated in constructor)
  const activePlayers = game.getActivePlayers();
  activePlayers.forEach(player => {
    if (!player.isHuman && game.descriptions[player.id]) {
      console.log(`AI ${player.name} submitted: "${game.descriptions[player.id]}"`);
    }
  });
  
  console.log("\nAll descriptions submitted. Moving to voting phase...\n");
  
  // Submit human vote
  const humanVoteTarget = activePlayers.find(p => !p.isHuman && p.id !== 1)?.id || activePlayers[1].id;
  game.submitVote(1, humanVoteTarget);
  console.log(`Human voted for player ${humanVoteTarget}`);
  
  // Submit AI votes (already generated)
  activePlayers.forEach(player => {
    if (!player.isHuman && game.votes[player.id]) {
      console.log(`AI ${player.name} voted for player ${game.votes[player.id]}`);
    }
  });
  
  // Process voting results
  const voteResult = game.processVotingResults();
  console.log(`\nVoting result: ${voteResult.message}`);
  
  if (voteResult.gameOver) {
    console.log(`Game over! Winner: ${voteResult.winner === 'civilians' ? 'Civilians' : 'Undercovers'}`);
    return;
  }
  
  // Round 2 (if game continues)
  if (game.gameActive) {
    console.log("\n=== ROUND 2 ===");
    const round2State = game.getGameState();
    console.log(`Round ${round2State.currentRound} started`);
    console.log(`Active players: ${round2State.activePlayerCount}`);
    
    // Submit new human description
    const humanDesc2 = "我觉得这个很有用。";
    game.submitDescription(1, humanDesc2);
    console.log(`Human submitted: "${humanDesc2}"`);
    
    // Submit votes again
    const remainingPlayers = game.getActivePlayers();
    const newVoteTarget = remainingPlayers.find(p => p.id !== 1)?.id || 1;
    game.submitVote(1, newVoteTarget);
    console.log(`Human voted for player ${newVoteTarget}`);
    
    // Process final results
    const finalResult = game.processVotingResults();
    console.log(`\nFinal result: ${finalResult.message}`);
    if (finalResult.gameOver) {
      console.log(`Game over! Winner: ${finalResult.winner === 'civilians' ? 'Civilians' : 'Undercovers'}`);
    }
  }
}

testFullGame();

console.log("\n=== Comprehensive test completed ===");