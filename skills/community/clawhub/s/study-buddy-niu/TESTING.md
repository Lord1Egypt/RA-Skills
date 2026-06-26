# Study Buddy - 测试和验证指南

## ✅ 已完成的文件清单

```
~/.openclaw/workspace/skills/study-buddy/
├── SKILL.md                      ✅ 触发条件说明
├── README.md                     ✅ 使用文档
├── src/
│   ├── index.js                  ✅ 主入口
│   ├── question-engine.js        ✅ 题库引擎
│   ├── bitable-client.js         ✅ Bitable API 封装
│   ├── schedule-gen.js           ✅ 学习计划生成器
│   ├── wrong-answers.js          ✅ 错题本管理
│   └── progress-tracker.js       ✅ 进度追踪
└── data/                         ⭕ 后续添加题库 JSON 文件
```

---

## 🧪 如何测试 Skill

### 方法 1: 直接在飞书聊天中测试（推荐）

1. **打开飞书**，找到你的 OpenClaw 机器人
2. **发送测试消息**：
   ```
   来一道 N2 语法题
   ```
3. **观察回复**：
   - 如果 Skill 正常工作，会返回一道日语 N2 语法题
   - 如果报错，检查日志

### 方法 2: 查看 OpenClaw 日志

```bash
# 查看 OpenClaw 运行日志
tail -f ~/.openclaw/logs/openclaw.log | grep "Study Buddy"

# 或者查看技能加载日志
openclaw status
```

### 方法 3: 手动触发测试

在 Node.js 环境中：

```javascript
const { handleMessage } = require('./src/index.js');

// 模拟用户消息
const message = { text: "来一道 N2 语法题", userId: "test_user" };
const context = { channel: "feishu", sessionId: "test_session" };

// 调用处理函数
handleMessage(message, context).then(response => {
  console.log('回复:', response.text);
});
```

---

## 🔍 常见问题排查

### 问题 1: Skill 没有响应

**可能原因**:
- OpenClaw 没有重新加载 Skills
- SKILL.md 触发关键词不匹配

**解决方法**:
```bash
# 重启 OpenClaw Gateway
openclaw gateway restart

# 检查 Skill 目录是否在正确位置
ls -la ~/.openclaw/workspace/skills/study-buddy/
```

### 问题 2: 提示"未找到题目"

**可能原因**:
- Bitable 中没有题目数据
- App Token 或 Table ID 配置错误

**解决方法**:
1. 检查 Bitable 配置是否正确：
   ```javascript
   // src/index.js
   const CONFIG = {
     BITABLE_APP_TOKEN: "SoZ5bkTBOa3LQisZHO1cAQuknDh",
     BITABLE_TABLE_ID: "tbl0TEk3P0GCqR2p"
   };
   ```

2. 确认 Bitable 中有题目数据：
   - 访问：https://my.feishu.cn/base/SoZ5bkTBOa3LQisZHO1cAQuknDh
   - 检查是否有至少 1 条记录

### 问题 3: 飞书 API 调用失败

**可能原因**:
- 飞书应用权限不足
- 网络问题

**解决方法**:
- 检查飞书开放平台的应用权限
- 确保有 `bitable:app` 相关权限
- 查看错误日志详情

---

## 📊 预期行为

### 正常流程示例

**用户**: `来一道 N2 语法题`

**助手**: 
```
📚 【N2 语法练习】第 38 题

题目：彼は約束の時間に遅れた_____、謝りもせず帰ってしまった。

选项:
A) うえに
B) あげく
C) とたん
D) さえ

━━━━━━━━━━━━━━━━━━━

💡 请直接回复 A/B/C/D 提交答案～
```

**用户**: `B`

**助手**: 
```
✅ 回答正确！太棒了！🎉

解析: 
「～あげく」表示经过一段时间或一系列过程后，最终产生了消极的结果。

知识点：～あげく
来源：N2 官方模拟题

━━━━━━━━━━━━━━━━━━━

继续挑战吗？
• 回复 "继续" 再来一道
• 回复 "来一道 N2 语法题" 指定类型
```

---

## 🎯 下一步行动

### 立即可以做的：

1. **测试 Skill**
   - 在飞书中对机器人说："来一道 N2 语法题"
   - 观察是否正常出题

2. **检查 Bitable 数据**
   - 访问：https://my.feishu.cn/base/SoZ5bkTBOa3LQisZHO1cAQuknDh
   - 确认有题目数据

3. **查看日志**
   - 如果有报错，查看 OpenClaw 日志

### 后续优化：

1. **导入更多题库**
   - 把 100 道完整题库导入 Bitable
   - 或者创建 JSON 文件放在 `data/` 目录

2. **创建错题表**
   - 在同一个 Bitable 中创建第二张表"错题本"
   - 更新 `wrong-answers.js` 中的表 ID

3. **完善模拟考试功能**
   - 实现 `handleMockExam` 函数
   - 支持一次性出多道题并统计分数

---

## 📞 获取帮助

如果遇到问题：

1. **查看日志文件**
   ```bash
   cat ~/.openclaw/logs/openclaw.log
   ```

2. **检查配置文件**
   - `src/index.js` 中的 CONFIG 配置
   - `SKILL.md` 中的触发关键词

3. **重新部署**
   ```bash
   # 重启 OpenClaw
   openclaw gateway restart
   ```

---

**祝测试顺利！🚀**

*如有问题，请查看日志或联系开发者。*
