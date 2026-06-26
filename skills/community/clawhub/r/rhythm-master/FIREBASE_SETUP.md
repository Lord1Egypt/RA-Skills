# 🔥 Firebase 联网排行榜配置教程

本教程将指导你如何配置 Firebase，让《节奏大师》拥有真正的全球排行榜功能。

---

## 📋 概述

**当前状态**：
- ✅ `rhythm-game.html` - 本地版（仅本地存储）
- ✅ `rhythm-game-online.html` - 联网版（需要 Firebase 配置）

**配置后效果**：
- 🌍 全球玩家分数实时同步
- 🏆 真正的全球排行榜
- 💾 数据永久保存，不会丢失
- ⚡ 实时更新，无需刷新页面

---

## 🚀 配置步骤（5分钟搞定）

### 步骤 1：创建 Firebase 项目

1. 访问 [Firebase 官网](https://firebase.google.com/)
2. 点击 **"Get Started"** 或 **"开始使用"**
3. 登录你的 Google 账号
4. 点击 **"创建项目"**
5. 输入项目名称（如：`rhythm-master-game`）
6. 勾选同意条款，点击 **"继续"**
7. 询问是否启用 Google Analytics → 选择 **"不启用"**（简化流程）
8. 点击 **"创建项目"**，等待创建完成

### 步骤 2：创建 Realtime Database

1. 项目创建完成后，点击 **"继续"**
2. 在左侧菜单找到 **"构建"** → **"Realtime Database"**
3. 点击 **"创建数据库"**
4. 选择数据库位置（建议选择 `asia-southeast1` 新加坡，离你最近）
5. 安全规则选择 **"以锁定模式开始"**（稍后会修改）
6. 点击 **"启用"**

### 步骤 3：修改安全规则

1. 数据库创建后，点击 **"规则"** 标签
2. 修改规则为以下内容（允许读写）：

```json
{
  "rules": {
    ".read": true,
    ".write": true,
    "leaderboard": {
      ".read": true,
      ".write": true
    }
  }
}
```

3. 点击 **"发布"**

⚠️ **注意**：这个规则允许任何人读写，仅用于演示。生产环境应该添加验证。

### 步骤 4：获取配置信息

1. 点击左侧 **"项目概览"** 旁边的 **"⚙️"**（齿轮图标）
2. 选择 **"项目设置"**
3. 在 **"常规"** 标签页，下拉到 **"你的应用"** 部分
4. 点击 **"</>"**（添加 Web 应用）
5. 输入应用昵称（如：`rhythm-web`）
6. 点击 **"注册应用"**
7. 你会看到一段配置代码，类似这样：

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyABC123DEF456GHI789",
  authDomain: "rhythm-master-game.firebaseapp.com",
  databaseURL: "https://rhythm-master-game-default-rtdb.firebaseio.com",
  projectId: "rhythm-master-game",
  storageBucket: "rhythm-master-game.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abc123def456"
};
```

### 步骤 5：配置游戏文件

1. 打开 `rhythm-game-online.html`
2. 找到第 92-100 行的 `firebaseConfig` 配置
3. 将你在步骤 4 获取的配置信息粘贴进去：

```javascript
// 原来的配置（需要替换）
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "your-project.firebaseapp.com",
    databaseURL: "https://your-project-default-rtdb.firebaseio.com",
    projectId: "your-project",
    storageBucket: "your-project.appspot.com",
    messagingSenderId: "YOUR_SENDER_ID",
    appId: "YOUR_APP_ID"
};

// 替换为你自己的配置，例如：
const firebaseConfig = {
    apiKey: "AIzaSyABC123DEF456GHI789",
    authDomain: "rhythm-master-game.firebaseapp.com",
    databaseURL: "https://rhythm-master-game-default-rtdb.firebaseio.com",
    projectId: "rhythm-master-game",
    storageBucket: "rhythm-master-game.appspot.com",
    messagingSenderId: "123456789012",
    appId: "1:123456789012:web:abc123def456"
};
```

4. 保存文件

### 步骤 6：测试

1. 在浏览器中打开配置好的 `rhythm-game-online.html`
2. 如果看到 **"🌐 已连接到全球服务器"**，说明配置成功！
3. 玩一局游戏，保存分数
4. 查看排行榜，应该能看到你的分数

---

## 🌐 部署到公网

配置好 Firebase 后，将游戏部署到公网，让所有人都能访问：

### 方案 1：GitHub Pages（免费，推荐）

1. 在 GitHub 创建新仓库（如 `rhythm-master`）
2. 上传 `rhythm-game-online.html` 并重命名为 `index.html`
3. 进入仓库 **Settings** → **Pages**
4. Source 选择 **Deploy from a branch**，Branch 选择 **main**
5. 等待几分钟后，访问 `https://你的用户名.github.io/rhythm-master/`

### 方案 2：Netlify（免费）

1. 访问 [Netlify](https://www.netlify.com/)
2. 注册账号（可用 GitHub 账号登录）
3. 点击 **"Add new site"** → **"Deploy manually"**
4. 将 `rhythm-game-online.html` 拖放到上传区域
5. 等待部署完成，获得免费域名

### 方案 3：Vercel（免费）

1. 访问 [Vercel](https://vercel.com/)
2. 注册账号（可用 GitHub 账号登录）
3. 点击 **"Add New..."** → **"Project"**
4. 导入 GitHub 仓库或上传文件
5. 自动部署，获得免费域名

---

## 📊 数据管理

### 查看数据库数据

1. 进入 Firebase 控制台
2. 点击 **"Realtime Database"**
3. 可以看到所有玩家提交的数据

### 数据结构

```json
{
  "leaderboard": {
    "-Nabc123": {
      "playerName": "玩家名",
      "score": 98500,
      "maxCombo": 156,
      "perfect": 120,
      "great": 35,
      "good": 5,
      "bad": 0,
      "miss": 0,
      "difficulty": "hard",
      "timestamp": 1678623456789,
      "date": "2026-03-12T10:30:00.000Z"
    },
    "-Ndef456": { ... }
  }
}
```

### 清理数据

如果想重置排行榜：
1. 进入 Realtime Database
2. 点击 `leaderboard` 节点
3. 点击右侧的 **"X"** 删除
4. 确认删除

---

## 🔒 安全建议

### 生产环境规则（进阶）

如果你要正式发布，建议使用更严格的规则：

```json
{
  "rules": {
    ".read": true,
    "leaderboard": {
      ".write": true,
      ".indexOn": ["score", "timestamp"],
      "$scoreId": {
        ".validate": "newData.hasChildren(['playerName', 'score', 'maxCombo', 'difficulty', 'timestamp'])"
      }
    }
  }
}
```

### 防作弊建议

1. **频率限制**：限制同一IP提交频率
2. **分数验证**：服务端验证分数合理性
3. **人机验证**：添加 reCAPTCHA

这些需要配合 Cloud Functions 实现，详见 [Firebase 文档](https://firebase.google.com/docs/functions)。

---

## ❓ 常见问题

### Q1: 连接失败，显示 "未连接到服务器"

**可能原因**：
- Firebase 配置信息错误
- 网络问题
- 安全规则未设置

**解决方案**：
1. 检查 `apiKey`、`databaseURL` 是否正确
2. 确保数据库规则已设置为允许读写
3. 打开浏览器开发者工具(F12)查看 Console 错误信息

### Q2: 可以提交分数，但排行榜不显示

**可能原因**：
- 数据格式错误
- 查询条件问题

**解决方案**：
1. 在 Firebase 控制台检查数据是否存在
2. 检查数据字段是否完整

### Q3: 排行榜加载很慢

**解决方案**：
1. 限制查询数量（已设置为50条）
2. 添加数据库索引（在安全规则中添加 `.indexOn`）
3. 使用分页加载

### Q4: 免费额度够吗？

Firebase 免费额度（Spark 计划）：
- 数据库：1GB 存储，10GB/月 下载
- 并发：100 个同时连接
- 足够支持数千名玩家

---

## 📱 测试清单

配置完成后，检查以下功能：

- [ ] 页面显示 "🌐 已连接到全球服务器"
- [ ] 可以正常游戏
- [ ] 游戏结束后可以保存分数
- [ ] 排行榜显示刚刚保存的分数
- [ ] 不同浏览器/设备可以看到相同的数据

---

## 🎉 完成！

配置完成后，你就拥有了一个真正联网的《节奏大师》游戏！

- 🌍 全球玩家可以一起竞技
- 🏆 实时更新的排行榜
- 💾 永久保存的游戏记录
- 📱 随时随地访问

快分享给朋友们一起玩吧！🎮

---

## 📞 需要帮助？

- Firebase 官方文档：https://firebase.google.com/docs
- Firebase 中文文档：https://firebase.google.cn/docs
- 社区支持：https://github.com/firebase/firebase-js-sdk/discussions
