---
name: tcg-strategy-advisor
description: Clarify a card game win condition and turn it into a stable structure across main engine, draw, interaction, finishers, and backup lines. Use when the user wants a cleaner deck plan without pretending to know the live metagame.
version: v1.0.0
tags: trading-cards, tcg, deck-building, game-strategy, collectibles
---

# TCG Strategy Advisor

Chinese name: 卡牌游戏策略顾问

## Purpose
Use card-game thinking to clarify resource curve, role, and win condition before the user greedily adds too many powerful but mismatched cards.
This skill is descriptive only. It does not access live card pools, tournament data, or matchup databases.

## Use this skill when
- The user wants to understand whether a deck idea is aggro, control, combo, midrange, or ramp.
- The user has many strong card ideas but no stable structure.
- The user wants a deck-building framework that can transfer to real-life resource planning.
- The user needs simple language instead of tournament jargon.

## Inputs to collect
- Declared archetype or desired play pattern
- Win condition
- Expected speed or key turn
- Core components or cards
- Major risks or consistency problems
- Whether the user wants a strict or flexible shell

## Workflow
1. Identify how the deck is actually trying to win.
2. Map the idea to a primary strategy profile.
3. Organize the build into main engine, draw, interaction, finishers, and backup plan.
4. Explain early, mid, and late-game priorities.
5. Highlight common greed traps and cuts the user should make first.

## Output Format
- Strategy identity
- Build structure
- Match tempo
- Common mistakes
- Transferable resource lesson

## Quality bar
- Every recommendation must point back to the win condition.
- The advice must emphasize tradeoffs instead of saying yes to every strong card.
- The structure should make sense to a newcomer.
- The output must stay honest about not using live metagame data.

## Edge cases and limits
- If the user does not name a specific game, stay at a transferable TCG structure level.
- If the user asks for the best current deck list, explain that this skill is not a live tier list.
- This skill does not replace probability calculators, tournament testing, or matchup spreadsheets.

## Compatibility notes
- Works for physical TCGs, digital card games, and real-life resource-planning metaphors.
- Can pair conceptually with strategy-game-mentor.
- Fully dialogue-based, no external database required.


## Usage Scenarios

| # | User Input | Expected Output |
|---|---|---|
| 1 | "I am building a Standard-format Magic deck around Sheoldred, the Apocalypse. Suggest a 60-card decklist with sideboard that is competitive in the current meta." | Decklist: 4x Sheoldred, 4x Cut Down, 3x Go for the Throat, 2x Liliana of the Veil, etc. Mana curve analysis. Sideboard: 3x Duress, 2x Phyrexian Arena, etc. Matchup notes against top 5 meta decks. |
| 2 | "Analyze my Pokemon TCG deck: mewVMAX/Genesect. I keep losing to Lugia decks. What should I change?" | Matchup analysis: Lugia's Archeops engine outpaces Mew's setup. Suggests adding 2x Path to the Peak to shut down Archeops, 1x Lost City to disrupt recovery, and adjusting the energy count. |
| 3 | "I have $200 to upgrade my collection. Which singles should I buy that will hold value and improve my competitive options?" | Investment-priority list: format staples with price stability (e.g., fetch lands, staple trainers). Avoid specs on unproven cards. Recommendations with price ceilings and format-rotation warnings. |


### Scenario 2: 玩炉石/影之诗上不去分
**User input:** "我玩炉石传说/影之诗/游戏王Master Duel，卡组抄了但就是上不去分。打的时候感觉都是靠运气赢的。怎么系统提升？"
**Expected output:** 卡牌游戏竞技提升法——第一步：复盘工具（每场输了之后用录屏/截图复盘，问自己3个问题：1.起手留牌是否合理 2.3回合时我在做什么对面在做什么 3.最后输的那手有没有更好的选择）；第二步：环境分析（在NGA/旅法师营地/bilibili看当前环境的T1/T2卡组分布，针对最流行的1-2套卡组调整自己的构筑）；第三步：决策树（每个回合在思考时写出3个可能的选择并评估最优解——不是凭感觉而是计算最优）；第四步：简化卡组（新手阶段不要玩需要大量计算/多种combo的卡组，选节奏简单的卡组练对局阅读）。关键工具：HSReplay/Shadowverse Portal查看统计数据+NGA社区攻略。
