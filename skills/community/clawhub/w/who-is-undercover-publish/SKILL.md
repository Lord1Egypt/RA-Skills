---
name: who-is-undercover
description: 谁是卧底 - 经典社交推理游戏的AI版本，支持4-10人游戏，包含智能AI对手和完整游戏机制。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - node
    emoji: "🎭"
    homepage: https://github.com/long5/who-is-undercover
---

# Who is Undercover - OpenClaw Skill

## Description
A complete implementation of the popular party game "Who is Undercover" (谁是卧底) for OpenClaw. This skill allows users to play the game with AI agents simulating human players, featuring role assignment, speaking rounds, voting mechanics, and win condition detection.

## Game Rules
- Players are assigned secret roles: most are "civilians" with the same word, while 1-2 are "undercovers" with a different but related word
- Each round, players describe their word without revealing it directly
- After descriptions, players vote on who they think is the undercover
- The player with the most votes is eliminated
- Game continues until undercovers are eliminated (civilians win) or undercovers equal/exceed civilians (undercovers win)

## Features
- Configurable player count (4-10 players)
- AI agents simulate realistic human-like descriptions
- Smart voting logic based on speech analysis
- Interactive turn-based gameplay
- One-click installation via ClawHub
- Feishu integration for group play

## Usage
`/skill who-is-undercover start [player_count]` - Start a new game
`/skill who-is-undercover join` - Join an existing game
`/skill who-is-undercover describe "[description]"` - Submit your description
`/skill who-is-undercover vote [player_number]` - Vote for a player
`/skill who-is-undercover status` - Check current game status