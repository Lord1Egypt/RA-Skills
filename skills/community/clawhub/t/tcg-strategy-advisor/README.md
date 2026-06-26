# TCG Strategy Advisor / 卡牌游戏策略顾问

Use card-game thinking to clarify resource curve, role, and win condition before the user greedily adds too many powerful but mismatched cards. Works for physical TCGs, digital card games, and real-life resource-planning metaphors.

## Tags
trading-cards, tcg, deck-building, game-strategy, collectibles

## Usage Scenarios

### Scenario 1: 玩炉石/影之诗上不去分
**User Input:** "我玩炉石传说/影之诗/游戏王Master Duel，卡组抄了但就是上不去分。打的时候感觉都是靠运气赢的。怎么系统提升？"

**Expected Output:** 卡牌游戏竞技提升法——第一步：复盘工具（每场输了之后用录屏/截图复盘，问自己3个问题：1.起手留牌是否合理 2.3回合时我在做什么对面在做什么 3.最后输的那手有没有更好的选择）；第二步：环境分析（在NGA/旅法师营地/bilibili看当前环境的T1/T2卡组分布，针对最流行的1-2套卡组调整自己的构筑）；第三步：决策树（每个回合在思考时写出3个可能的选择并评估最优解——不是凭感觉而是计算最优）；第四步：简化卡组（新手阶段不要玩需要大量计算/多种combo的卡组，选节奏简单的卡组练对局阅读）。关键工具：HSReplay/Shadowverse Portal查看统计数据+NGA社区攻略。

### Scenario 2: Build a competitive Magic deck
**User Input:** "I am building a Standard-format Magic deck around Sheoldred, the Apocalypse. Suggest a 60-card decklist with sideboard that is competitive in the current meta."

**Expected Output:** Decklist: 4x Sheoldred, 4x Cut Down, 3x Go for the Throat, 2x Liliana of the Veil, etc. Mana curve analysis. Sideboard: 3x Duress, 2x Phyrexian Arena, etc. Matchup notes against top 5 meta decks.

### Scenario 3: Collection investment strategy
**User Input:** "I have $200 to upgrade my collection. Which singles should I buy that will hold value and improve my competitive options?"

**Expected Output:** Investment-priority list: format staples with price stability (e.g., fetch lands, staple trainers). Avoid specs on unproven cards. Recommendations with price ceilings and format-rotation warnings.
