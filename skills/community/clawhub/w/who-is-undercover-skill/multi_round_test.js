// Multi-round Who is Undercover game simulation test
const fs = require('fs');
const path = require('path');

// Load the skill
const skill = require('./index.js');

class GameSimulator {
    constructor() {
        this.context = { gameId: null };
        this.testResults = [];
    }

    async runMultiRoundTest() {
        console.log("=== Multi-Round Who is Undercover Simulation Test ===\n");

        // Test different player configurations
        const testConfigs = [
            { players: 4, humans: 1, name: "Small Game (4 players)" },
            { players: 6, humans: 1, name: "Standard Game (6 players)" },
            { players: 8, humans: 2, name: "Large Game (8 players, 2 humans)" },
            { players: 10, humans: 1, name: "Max Game (10 players)" }
        ];

        for (const config of testConfigs) {
            console.log(`\n--- ${config.name} ---`);
            await this.testGameConfig(config);
        }

        this.generateReport();
    }

    async testGameConfig(config) {
        try {
            // Start game
            const startResult = await skill.handleCommand('start', [config.players.toString(), config.humans.toString()], this.context);
            
            if (!startResult.success) {
                console.log(`❌ Start failed: ${startResult.message}`);
                return;
            }

            console.log(`✅ Game started: ${config.players} players, ${config.humans} humans`);
            
            let round = 1;
            let gameOver = false;
            
            // Play multiple rounds or until game over
            while (round <= 3 && !gameOver) {
                console.log(`\nRound ${round}:`);
                
                // Get game state
                const statusResult = await skill.handleCommand('status', [], this.context);
                const gameState = statusResult.gameState;
                
                if (gameState.gameOver) {
                    console.log(`🎮 Game ended: ${statusResult.winner === 'civilians' ? 'Civilians win!' : 'Undercovers win!'}`);
                    gameOver = true;
                    break;
                }

                // Submit human description (player 1)
                const humanDesc = this.generateHumanDescription(gameState.currentRound);
                const descResult = await skill.handleCommand('describe', [humanDesc], this.context);
                console.log(`📝 Human description submitted`);

                // If ready for voting, submit human vote
                if (descResult.readyForVoting) {
                    // Get active players for voting
                    const activePlayers = gameState.activePlayerCount;
                    const targetPlayer = Math.floor(Math.random() * activePlayers) + 1;
                    const voteResult = await skill.handleCommand('vote', [targetPlayer.toString()], this.context);
                    
                    if (voteResult.gameOver) {
                        console.log(`🎯 Final vote cast. Game over!`);
                        gameOver = true;
                    } else {
                        console.log(`🗳️ Vote submitted for player ${targetPlayer}`);
                    }
                }

                round++;
            }

            this.testResults.push({
                config: config,
                success: true,
                roundsPlayed: round - 1,
                gameOver: gameOver
            });

        } catch (error) {
            console.log(`❌ Test failed: ${error.message}`);
            this.testResults.push({
                config: config,
                success: false,
                error: error.message
            });
        }
    }

    generateHumanDescription(round) {
        const descriptions = [
            "这是一个很常见的东西，大家都经常用到。",
            "我觉得这个很有意思，生活中离不开它。",
            "这是一个基础的日常用品，非常重要。",
            "很多人都喜欢这个，使用起来很方便。",
            "这是一个经典的东西，历史悠久。"
        ];
        return descriptions[Math.min(round - 1, descriptions.length - 1)];
    }

    generateReport() {
        const successCount = this.testResults.filter(r => r.success).length;
        const totalCount = this.testResults.length;
        const successRate = (successCount / totalCount * 100).toFixed(1);

        console.log("\n" + "=".repeat(60));
        console.log("FINAL TEST REPORT");
        console.log("=".repeat(60));
        console.log(`Total Configurations Tested: ${totalCount}`);
        console.log(`Successful Tests: ${successCount}`);
        console.log(`Success Rate: ${successRate}%`);
        console.log("");

        this.testResults.forEach((result, index) => {
            const config = result.config;
            if (result.success) {
                console.log(`✅ ${config.name}: ${result.roundsPlayed} rounds played${result.gameOver ? ', game ended' : ''}`);
            } else {
                console.log(`❌ ${config.name}: Failed - ${result.error}`);
            }
        });

        console.log("\n" + "=".repeat(60));
        console.log("TEST COMPLETE");
        console.log("=".repeat(60));
    }
}

// Run the simulation
async function main() {
    const simulator = new GameSimulator();
    await simulator.runMultiRoundTest();
}

if (require.main === module) {
    main().catch(console.error);
}

module.exports = GameSimulator;