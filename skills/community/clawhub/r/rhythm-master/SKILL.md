---
name: rhythm-master
description: This skill enables playing a rhythm game called "节奏大师" (Rhythm Master) similar to QQ Dance/DDR. Players press arrow keys and spacebar in time with falling notes to score points. The game features multiple difficulty levels, combo system, judgment ratings (PERFECT/GREAT/GOOD/BAD/MISS), local leaderboard, and can be extended with online leaderboards. Use this skill when the user wants to play a rhythm game, test their reflexes, or have fun with a keyboard-based music game.
---

# 节奏大师 - Rhythm Master

## 简介

《节奏大师》是一款键盘节奏游戏，玩家需要在正确的时机按下对应的按键（↑↓←→空格），跟随音乐节奏击打落下的音符。游戏拥有完善的判定系统、连击机制、多难度等级和排行榜功能。

## 何时使用此 Skill

- 用户说"我想玩节奏游戏"、"来玩音游"、"测试手速"
- 用户想要类似 QQ炫舞、osu!、太鼓达人 的游戏体验
- 用户想玩需要反应速度的键盘游戏
- 聚会时需要竞技性小游戏
- 用户明确表示想玩音乐节奏游戏

## 游戏特色

### 🎮 核心玩法
- **5键操作**：← ↓ SPACE ↑ →
- **实时判定**：PERFECT / GREAT / GOOD / BAD / MISS
- **连击系统**：连击越高，得分倍数越高
- **生命系统**：MISS会扣除生命，生命归零游戏结束

### 📊 难度等级
| 难度 | 速度 | 音符密度 | 适合人群 |
|------|------|----------|----------|
| 简单 (EASY) | 慢 | 稀疏 | 初学者 |
| 普通 (NORMAL) | 中等 | 中等 | 普通玩家 |
| 困难 (HARD) | 快 | 密集 | 熟练玩家 |
| 专家 (EXPERT) | 极快 | 极密 | 高手 |

### 🏆 排行榜系统
- **本地排行榜**：自动保存前100名，使用浏览器 LocalStorage
- **联网排行榜**：可扩展至 Firebase/自建服务器（需额外配置）
- **详细统计**：保存 PERFECT/GREAT/GOOD/BAD/MISS 数量和最大连击

## 游戏数据与资源

### 游戏机制文档
- `references/game_mechanics.md` - 完整游戏机制说明
  - 判定系统（50ms-200ms 时间窗口）
  - 得分计算公式
  - 连击加成表
  - 评级系统（SSS/A/B/C/D）
  - 游戏模式（经典/无尽/挑战/对战/练习）

### 排行榜系统文档
- `references/leaderboard_system.md` - 排行榜实现方案
  - 本地存储实现（已内置）
  - Firebase 联网方案
  - 自建后端方案（Node.js + MongoDB）
  - 防作弊机制
  - 部署指南

### 游戏实现
- `assets/rhythm-game.html` - 完整的网页版游戏
  - 单文件 HTML，开箱即用
  - 响应式设计，支持移动端
  - 完整的游戏逻辑和UI
  - 本地排行榜功能

## 如何使用

### 启动游戏

**方式一：直接打开 HTML 文件**
1. 打开 `assets/rhythm-game.html`
2. 使用浏览器打开（推荐 Chrome/Edge/Firefox）
3. 选择难度，点击"开始游戏"

**方式二：部署到网页服务器**
```bash
# 使用 Python 快速启动本地服务器
cd assets
python -m http.server 8080
# 访问 http://localhost:8080/rhythm-game.html
```

**方式三：部署到公网**
- GitHub Pages
- Netlify
- Vercel
- Cloudflare Pages

### 游戏操作

```
按键布局：

左手区          空格          右手区
┌───┬───┐                    ┌───┬───┐
│ ← │ ↓ │       [SPACE]      │ ↑ │ → │
└───┴───┘                    └───┴───┘
小指  无名指      双手拇指       食指  中指
```

**操作技巧：**
1. **保持节奏感**：跟着内心默数节拍
2. **预判音符**：眼睛看判定线，余光看音符
3. **手位固定**：保持手位不要移动
4. **宁可GOOD不断连**：保持连击比准确率更重要
5. **放松心态**：紧张会影响反应速度

### 游戏规则

1. **音符下落**：音符从上方落下，到达判定线时按键
2. **判定等级**：
   - 🌟 PERFECT (±50ms) - 100分
   - ✨ GREAT (±100ms) - 80分
   - 👍 GOOD (±150ms) - 50分
   - 😕 BAD (±200ms) - 20分，连击中断
   - ❌ MISS (>200ms) - 0分，扣1生命

3. **连击加成**：
   - 1-10连击：1.0x
   - 11-30连击：1.1x
   - 31-50连击：1.2x
   - 51-100连击：1.5x
   - 101-200连击：2.0x
   - 200+连击：2.5x

4. **评级系统**（根据准确率）：
   - SSS (100%) - 节奏之神
   - SS (95-99%) - 节奏大师
   - S (90-94%) - 节奏高手
   - A (80-89%) - 节奏达人
   - B (70-79%) - 节奏学徒
   - C (60-69%) - 节奏新手
   - D (<60%) - 节奏小白

## 游戏流程

### 1. 主菜单
```
🎵 节奏大师

[选择难度：简单/普通/困难/专家]

[▶ 开始游戏]
[🏆 排行榜]
[❓ 游戏说明]
```

### 2. 游戏界面
```
得分: 12,500  |  连击: 45  |  生命: ♥♥♥♥♥  |  时间: 45s

        [COMBO 显示区域]

    ←       ↓      SPACE      ↑       →
    ○       ○        ○        ○       ○

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
              [判定线]

    【音符从这里落下】
```

### 3. 游戏结束
```
🎉 游戏结束

最终得分: 98,500
评级: S

统计：
PERFECT: 120  |  GREAT: 35  |  GOOD: 5
BAD: 0        |  MISS: 0    |  最大连击: 156

[输入名字保存分数]
[💾 保存分数] [🏆 查看排行榜] [🔙 返回主菜单]
```

## 扩展联网排行榜

### 快速方案：Firebase（推荐）

**步骤：**
1. 访问 https://firebase.google.com 创建项目
2. 获取配置信息
3. 在 `rhythm-game.html` 中添加 Firebase SDK
4. 修改保存分数和获取排行榜的函数

**代码示例：**
```javascript
// 保存到云端
async function saveScoreOnline(scoreData) {
  const db = firebase.database();
  await db.ref('leaderboard').push(scoreData);
}

// 获取排行榜
async function getOnlineLeaderboard() {
  const snapshot = await db.ref('leaderboard')
    .orderByChild('score')
    .limitToLast(20)
    .once('value');
  return snapshot.val();
}
```

详细配置请参考 `references/leaderboard_system.md`

## 游戏特色功能

### 视觉效果
- 🌈 霓虹科技风格 UI
- ✨ 判定结果动态特效
- 🔥 连击数越高背景越华丽
- 💥 MISS时屏幕震动反馈
- 🎨 不同按键不同颜色区分

### 音效反馈
- 每个按键有不同的音高
- 判定结果有不同音效
- 连击 milestone 有特殊音效

### 响应式设计
- 支持桌面端和移动端
- 自适应不同屏幕尺寸
- 触摸操作支持（移动端）

## 技术规格

### 性能要求
- 目标帧率：60fps
- 输入延迟：<16ms
- 支持浏览器：Chrome 80+, Firefox 75+, Edge 80+, Safari 13+

### 代码结构
```
rhythm-game.html
├── HTML 结构
│   ├── 菜单界面
│   ├── 游戏界面
│   ├── 结算界面
│   └── 排行榜界面
├── CSS 样式
│   ├── 霓虹灯主题
│   ├── 动画效果
│   └── 响应式布局
└── JavaScript 逻辑
    ├── 游戏状态管理
    ├── 音符生成系统
    ├── 判定系统
    ├── 得分计算
    └── 排行榜存储
```

## 注意事项

### 键盘兼容性
- 确保键盘支持多键同时按下（防鬼键）
- 部分笔记本键盘可能有限制
- 推荐使用外接机械键盘获得最佳体验

### 浏览器设置
- 确保浏览器允许自动播放（如需添加背景音乐）
- 建议全屏模式游玩（按 F11）
- 关闭省电模式以保持 60fps

### 游戏体验优化
1. **首次游玩**：建议从"简单"难度开始
2. **提高准确率**：专注听节奏而非看音符
3. **保持连击**：宁可准确率稍低也不要断连
4. **休息间隔**：每玩3-5局休息眼睛和手指

## 示例对话

### 启动游戏
```
用户：我想玩节奏游戏

AI：好的！为你启动《节奏大师》🎵

这是一款键盘节奏游戏，使用 ← ↓ SPACE ↑ → 五个按键。
音符会从上方落下，到达判定线时按下对应按键！

游戏已准备好，选择难度开始吧：
- 🟢 简单 - 适合初学者
- 🔵 普通 - 标准难度
- 🟡 困难 - 需要较好反应
- 🔴 专家 - 极限挑战

你想选择哪个难度？
```

### 游戏进行中提示
```
AI：游戏开始！跟着节奏点击按键...

💡 小技巧：
1. 眼睛看判定线，余光看音符
2. 保持放松，紧张会影响反应
3. 宁可GOOD不断连，连击加成很重要！

当前状态：
❤️ 生命：5/5  |  ⭐ 连击：0  |  🎯 得分：0

准备好了吗？3... 2... 1... GO! 🎮
```

### 游戏结束后
```
AI：🎉 游戏结束！

📊 你的成绩：
━━━━━━━━━━━━━━━━━━━━━━
得分：98,500
评级：S (节奏高手)
最大连击：156

详细统计：
🌟 PERFECT：120
✨ GREAT：35
👍 GOOD：5
😕 BAD：0
❌ MISS：0
━━━━━━━━━━━━━━━━━━━━━━

太棒了！几乎没有失误！想再挑战一次更高难度吗？
```

## 文件清单

```
rhythm-master/
├── SKILL.md                          # 本文件 - 核心文档
├── references/
│   ├── game_mechanics.md            # 游戏机制详细说明
│   └── leaderboard_system.md        # 排行榜系统方案
└── assets/
    └── rhythm-game.html             # 完整游戏文件
```

## 许可

本 Skill 为开源项目，可自由使用、修改和分发。

---

🎵 **准备好挑战你的反应极限了吗？打开 rhythm-game.html 开始游戏吧！**
