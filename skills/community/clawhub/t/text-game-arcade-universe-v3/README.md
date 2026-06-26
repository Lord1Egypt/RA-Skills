# Text Game Arcade Universe v3

这是一个面向 OpenClaw / ClawHub 的 **综合 ASCII 文字游戏大厅 Skill**。

这一版重点解决两个问题：

1. **棋盘太小、像草图** → 改成标准大棋盘与更像样的线框模板
2. **规则不够严谨** → 重新审核各游戏的合法性、开局、胜负与输入格式

## 本版亮点

- 五子棋默认恢复标准 **15x15**，不是缩水小盘
- 中国象棋按 **9x10 + 楚河汉界 + 九宫** 输出
- 国际象棋按 **8x8 标准布局** 输出
- 围棋、黑白棋、四子棋都补上更合理的棋盘模板
- 扫雷、数独、2048、推箱子、迷宫全部强化成更完整的题面格式
- 新增：**Lights Out / Nim / 汉诺塔 / 滑块拼图**
- 更强触发词与更稳的路由规则
- 更适合手机端，但不再牺牲“棋盘感”

## 支持游戏

### 棋类与对战
- 五子棋 Gomoku
- 围棋 Go
- 井字棋 Tic-Tac-Toe
- 黑白棋 Othello
- 四子棋 Connect Four
- 海战棋 Battleship
- 中国象棋 Xiangqi
- 国际象棋 Chess

### 益智闯关
- 扫雷 Minesweeper
- 数独 Sudoku
- 2048
- 推箱子 Sokoban
- 文字迷宫 Maze
- 熄灯 Lights Out
- 汉诺塔 Tower of Hanoi
- Nim
- 滑块拼图 Fifteen Puzzle

### 文字休闲
- 猜数字 Guess Number
- 猜单词 Hangman
- 猜密码 Mastermind
- 成语接龙 Idiom Chain
- 单词接龙 Word Relay

## 推荐测试句

- 来个小游戏
- 开一局五子棋，你先手
- 用 ASCII 画一个标准 15x15 五子棋盘
- 围棋 9x9，我执黑
- 中国象棋，按标准棋盘摆好
- 国际象棋，白方我先走
- 你当裁判，开一局黑白棋
- 开个扫雷，中等难度
- 给我一个推箱子第1关
- 来个 Lights Out
- 来局 Nim

## 安装后测试建议

1. 安装 skill 后，**请新开一个会话**。
2. 在聊天界面直接输入上面的测试句。
3. 若只想看规则，用：`rules` 或 “先讲规则”。
4. 若想让 AI 只当裁判，用：“你当裁判”。

## 文件结构

- `SKILL.md`：主技能说明、触发词、总工作流
- `references/rendering-and-state.md`：统一渲染模板和状态维护规则
- `references/*.md`：各游戏规则与输入方式
- `CHANGELOG.md`：版本更新记录
