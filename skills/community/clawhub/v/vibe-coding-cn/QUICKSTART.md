# Vibe Coding CN - 快速开始

**版本**: v1.0.0  
**模式**: 混合模式（OpenClaw 技能 + CLI + 可视化监控）

---

## 🚀 三种使用方式

### 方式一：OpenClaw 技能调用（推荐）

**在 OpenClaw 对话中直接使用**：

```
用 vibe-coding 做一个个税计算器
```

**或者在代码中调用**：

```javascript
const { run } = require('./index.js');

await run('做一个个税计算器', {
  onProgress: (phase, data) => {
    console.log(`[${phase}]`, data);
  }
});
```

**优点**：
- ✅ 最简单，无需安装
- ✅ 自动继承 OpenClaw 上下文
- ✅ 实时进度汇报

---

### 方式二：CLI 命令行调用

**1. 全局安装（首次使用）**：

```bash
cd ~/.openclaw/workspace/skills/vibe-coding-cn
npm install -g .
```

**2. 使用**：

```bash
vibe-coding "做一个个税计算器"
```

**或者临时执行（不安装）**：

```bash
node ~/.openclaw/workspace/skills/vibe-coding-cn/index.js "做一个个税计算器"
```

**优点**：
- ✅ 独立运行，不依赖 OpenClaw
- ✅ 适合脚本自动化
- ✅ 可在 CI/CD 中使用

---

### 方式三：可视化监控（可选）

**1. 启动服务器**：

```bash
cd ~/.openclaw/workspace/skills/vibe-coding-cn
npm start  # 或者 node server.js
```

**2. 访问界面**：

- HTTP: http://localhost:3000
- WebSocket: ws://localhost:8765

**3. 启动执行**：

通过方式一或方式二启动执行，然后在 UI 中查看实时进度。

**注意**：UI 仅用于监控，不能控制执行流程。

---

## 📁 输出结构

执行完成后，项目输出在 `output/{项目名}/` 目录：

```
output/个税计算器/
├── docs/
│   ├── requirements.md    # 需求文档
│   ├── architecture.md    # 架构设计
│   └── vibe-report.md     # 总结报告
├── index.html             # 主页面
├── app.js                 # 应用逻辑
└── tests/
    └── test-cases.md      # 测试用例
```

---

## 📊 执行流程

```
1. Phase 1: 需求分析 (30 秒)
   → 分析用户需求，生成功能列表和用户故事

2. Phase 2: 架构设计 (90 秒)
   → 设计技术栈、模块结构、数据流

3. Phase 3: 代码实现 (90 秒)
   → 生成完整可运行代码

4. Phase 4: 测试编写 (30 秒)
   → 生成测试用例

5. Phase 5: 整合验收
   → 质量检查，生成总结报告
```

**总耗时**: 3-5 分钟

---

## 🎯 示例需求

```bash
# 工具类
vibe-coding "做一个个税计算器"
vibe-coding "做一个单位转换器"
vibe-coding "做一个密码生成器"

# 游戏类
vibe-coding "做一个打字游戏"
vibe-coding "做一个猜数字游戏"
vibe-coding "做一个 2048 游戏"

# 应用类
vibe-coding "做一个待办事项应用"
vibe-coding "做一个天气查询应用"
vibe-coding "做一个记账本"

# 业务类
vibe-coding "做一个客户画像功能"
vibe-coding "做一个数据看板"
vibe-coding "做一个报表生成器"
```

---

## ⚠️ 注意事项

1. **执行时间**: 3-5 分钟，需要耐心等待
2. **代码审查**: 生成的代码需要人工审查后使用
3. **网络要求**: 需要访问 AI 模型 API
4. **内存要求**: 建议至少 2GB 可用内存

---

## 🔧 故障排除

### 问题：执行时间过长

**解决**: 检查网络连接，确认 AI 模型 API 可访问

### 问题：生成的代码无法运行

**解决**: 查看错误信息，重新生成或手动修复

### 问题：CLI 命令找不到

**解决**: 
```bash
# 检查是否安装成功
npm list -g vibe-coding-cn

# 重新安装
npm install -g ~/.openclaw/workspace/skills/vibe-coding-cn
```

---

## 📚 更多文档

- [SKILL.md](./SKILL.md) - 完整技能说明
- [README.md](./README.md) - 项目介绍
- [EXECUTION-FLOW.md](./EXECUTION-FLOW.md) - 执行流程详解
- [UI-GUIDE.md](./UI-GUIDE.md) - 可视化界面使用指南

---

**Happy Coding! 🎨**
