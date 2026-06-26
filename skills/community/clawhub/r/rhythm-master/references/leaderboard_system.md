# 排行榜系统说明

## 系统概述

《节奏大师》支持两种排行榜模式：
1. **本地排行榜** - 使用浏览器 LocalStorage 存储
2. **联网排行榜** - 使用后端服务器存储（需要额外配置）

---

## 本地排行榜

### 已实现功能

网页版游戏已内置本地排行榜功能：
- 自动保存前 100 名高分记录
- 数据存储在浏览器 LocalStorage
- 包含玩家名、分数、连击、难度、日期

### 数据结构
```javascript
{
  playerName: "玩家名",
  score: 98500,
  maxCombo: 156,
  perfect: 120,
  great: 35,
  good: 5,
  bad: 0,
  miss: 0,
  difficulty: "hard",
  date: "2026/3/12"
}
```

### 特点
- ✅ 无需服务器，开箱即用
- ✅ 数据私密，仅保存在本地
- ✅ 响应速度快
- ❌ 无法跨设备同步
- ❌ 浏览器清理数据会丢失

---

## 联网排行榜

### 方案一：使用免费云服务

#### 推荐平台
1. **Firebase** (Google)
   - 免费额度：100个并发连接，1GB存储
   - 实时数据库，支持实时排行榜
   
2. **Supabase**
   - 免费额度：500MB数据库
   - PostgreSQL数据库，易于使用

3. **JSONbin.io**
   - 免费额度：10,000条记录
   - 简单REST API

#### Firebase 实现示例

**1. 初始化 Firebase**
```javascript
// 在 HTML 中添加 Firebase SDK
<script src="https://www.gstatic.com/firebasejs/9.0.0/firebase-app.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.0.0/firebase-database.js"></script>

<script>
// Firebase 配置（需要替换为自己的配置）
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "your-project.firebaseapp.com",
  databaseURL: "https://your-project-default-rtdb.firebaseio.com",
  projectId: "your-project",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abcdef"
};

// 初始化
const app = firebase.initializeApp(firebaseConfig);
const database = firebase.database();
</script>
```

**2. 保存分数到云端**
```javascript
async function saveScoreOnline(scoreData) {
  try {
    const newScoreRef = database.ref('leaderboard').push();
    await newScoreRef.set({
      ...scoreData,
      timestamp: firebase.database.ServerValue.TIMESTAMP
    });
    console.log('分数已保存到云端');
  } catch (error) {
    console.error('保存失败:', error);
  }
}
```

**3. 获取排行榜**
```javascript
async function getOnlineLeaderboard(limit = 20) {
  try {
    const snapshot = await database.ref('leaderboard')
      .orderByChild('score')
      .limitToLast(limit)
      .once('value');
    
    const scores = [];
    snapshot.forEach(child => {
      scores.unshift(child.val()); // 降序排列
    });
    
    return scores;
  } catch (error) {
    console.error('获取排行榜失败:', error);
    return [];
  }
}
```

### 方案二：自建后端服务器

#### 技术栈推荐
- **Node.js + Express** - 轻量级后端
- **MongoDB** - 数据库存储
- **Redis** - 排行榜缓存

#### API 设计

**POST /api/scores - 提交分数**
```json
// Request
{
  "playerName": "Player123",
  "score": 98500,
  "maxCombo": 156,
  "difficulty": "hard",
  "stats": {
    "perfect": 120,
    "great": 35,
    "good": 5,
    "bad": 0,
    "miss": 0
  }
}

// Response
{
  "success": true,
  "rank": 15,
  "message": "分数已保存，排名第15位"
}
```

**GET /api/leaderboard - 获取排行榜**
```
GET /api/leaderboard?difficulty=hard&limit=20

// Response
{
  "success": true,
  "data": [
    {
      "rank": 1,
      "playerName": "RhythmKing",
      "score": 150000,
      "maxCombo": 300,
      "difficulty": "hard",
      "date": "2026-03-12"
    },
    // ...
  ]
}
```

**GET /api/rank/:playerId - 查询玩家排名**
```
GET /api/rank/Player123

// Response
{
  "success": true,
  "rank": 15,
  "total": 1250,
  "topPercent": 1.2
}
```

#### Node.js 后端示例

**server.js**
```javascript
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// 连接 MongoDB
mongoose.connect('mongodb://localhost/rhythm_game');

// 分数模型
const ScoreSchema = new mongoose.Schema({
  playerName: String,
  score: Number,
  maxCombo: Number,
  difficulty: String,
  stats: Object,
  date: { type: Date, default: Date.now }
});

const Score = mongoose.model('Score', ScoreSchema);

// 提交分数
app.post('/api/scores', async (req, res) => {
  try {
    const score = new Score(req.body);
    await score.save();
    
    // 计算排名
    const rank = await Score.countDocuments({
      score: { $gt: req.body.score }
    }) + 1;
    
    res.json({ success: true, rank });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// 获取排行榜
app.get('/api/leaderboard', async (req, res) => {
  try {
    const { difficulty, limit = 20 } = req.query;
    const query = difficulty ? { difficulty } : {};
    
    const scores = await Score.find(query)
      .sort({ score: -1 })
      .limit(parseInt(limit));
    
    res.json({ success: true, data: scores });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

app.listen(3000, () => {
  console.log('服务器运行在 http://localhost:3000');
});
```

---

## 防作弊机制

### 客户端验证
1. **输入验证**
   - 检查按键频率是否合理（人类极限约 10次/秒）
   - 检查判定时间是否合理

2. **分数验证**
   ```javascript
   function validateScore(scoreData) {
     const { perfect, great, good, bad, miss, score, maxCombo } = scoreData;
     
     // 总音符数
     const totalNotes = perfect + great + good + bad + miss;
     
     // 计算理论最高分
     const maxPossibleScore = totalNotes * 100 * 2.5; // 假设全PERFECT+最高连击加成
     
     // 验证分数是否合理
     if (score > maxPossibleScore) return false;
     
     // 验证连击是否合理
     if (maxCombo > totalNotes) return false;
     
     return true;
   }
   ```

### 服务端验证
1. **请求频率限制** - 防止批量提交
2. **IP 限制** - 同一IP短时间内多次提交需验证
3. **分数合理性检查** - 服务端重新计算验证

---

## 排行榜功能增强

### 1. 分类排行榜
- 按难度分类（简单/普通/困难/专家排行榜）
- 按模式分类（经典/无尽/挑战模式排行榜）
- 按时间分类（今日/本周/本月/总榜）

### 2. 社交功能
- 好友排行榜
- 附近玩家排行榜
- 国家/地区排行榜

### 3. 成就系统
```javascript
const achievements = {
  firstPlay: { name: "初次体验", desc: "完成第一局游戏" },
  combo10: { name: "渐入佳境", desc: "达成10连击" },
  combo50: { name: "手速达人", desc: "达成50连击" },
  combo100: { name: "节奏大师", desc: "达成100连击" },
  combo200: { name: "神之手", desc: "达成200连击" },
  fullCombo: { name: "完美演出", desc: "无MISS完成游戏" },
  allPerfect: { name: "全P大神", desc: "全PERFECT完成游戏" },
  score100k: { name: "十万分俱乐部", desc: "单次得分超过10万" },
  score500k: { name: "五十万传奇", desc: "单次得分超过50万" }
};
```

---

## 部署建议

### 静态网页部署
将 `rhythm-game.html` 部署到以下免费平台：

1. **GitHub Pages**
   - 免费、稳定、自定义域名
   
2. **Netlify**
   - 免费额度充足
   - 支持自定义域名和 HTTPS

3. **Vercel**
   - 专为前端优化
   - 全球 CDN 加速

4. **Cloudflare Pages**
   - 无限带宽
   - 全球边缘网络

### 完整部署步骤

```bash
# 1. 创建项目目录
mkdir rhythm-master-game
cd rhythm-master-game

# 2. 复制游戏文件
cp assets/rhythm-game.html index.html

# 3. 初始化 Git
git init
git add .
git commit -m "Initial commit"

# 4. 创建 GitHub 仓库并推送
git remote add origin https://github.com/yourusername/rhythm-master.git
git push -u origin main

# 5. 启用 GitHub Pages
# 在仓库设置中启用 Pages，选择 main 分支

# 6. 访问 https://yourusername.github.io/rhythm-master
```

---

## 扩展功能建议

### 1. 添加音乐
使用 Web Audio API 播放背景音乐：
```javascript
const audioContext = new (window.AudioContext || window.webkitAudioContext)();
// 加载和播放音频文件
```

### 2. 自定义谱面
允许玩家创建和分享自定义音符序列：
```javascript
const customChart = {
  bpm: 120,
  notes: [
    { time: 0, lane: 'left' },
    { time: 0.5, lane: 'right' },
    // ...
  ]
};
```

### 3. 多人对战
使用 WebSocket 实现实时对战：
```javascript
const ws = new WebSocket('wss://your-server.com/game');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  // 更新对手分数
};
```

---

## 总结

当前实现已包含完整的本地排行榜功能。如需联网排行榜，建议：

1. **快速方案**：使用 Firebase，30分钟可完成集成
2. **完整方案**：自建 Node.js 后端，需要服务器资源
3. **折中方案**：使用 JSONbin.io 等简单云服务

根据实际需求选择合适的方案即可！
