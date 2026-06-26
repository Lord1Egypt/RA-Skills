# skill-setup-flow 快速参考

## 🎯 用途

为任何已安装的 OpenClaw 技能创建标准化的设置流程。

## 🚀 快速启动

```
为 {skill-name} 创建设置流程
初始化 {skill-name} 配置
设置 {skill-name} 技能
启用 {skill-name}
```

## 📋 支持的技能类型

### A. 配置型技能
需要 API 密钥或配置项
- 示例：weather, news-summary, tavily
- 创建：config.md, 配置模板

### B. 数据型技能
需要存储和管理数据
- 示例：self-improving, memory 相关
- 创建：数据目录，索引文件

### C. 行为型技能
改变 AI 的行为模式
- 示例：self-improving, proactive-agent
- 创建：memory.md, 行为规则

### D. 工具型技能
提供新的工具或命令
- 示例：mcporter, oracle
- 创建：工具配置，快速参考

## 📁 创建的文件

### 标准目录结构
```
~/skills/{skill-name}/
├── SKILL.md (已存在)
├── setup-log.md (设置日志)
├── config.md (配置选项，如需要)
├── state.md (运行状态，如需要)
├── memory.md (技能记忆，如需要)
├── examples/ (示例)
└── templates/ (模板)
```

### 工作区根目录（如需要）
```
~/
├── {skill-name}/ (技能数据目录)
│   ├── memory.md
│   ├── index.md
│   ├── state.md
│   ├── projects/
│   ├── domains/
│   └── archive/
```

## 🔧 标准流程

### 步骤 1: 分析技能
- 读取 SKILL.md
- 确定技能类型
- 识别配置需求

### 步骤 2: 创建结构
- 创建必要目录
- 创建配置文件
- 创建状态文件

### 步骤 3: 集成
- 更新 SOUL.md
- 更新 AGENTS.md
- 更新 MEMORY.md

### 步骤 4: 测试
- 基本功能测试
- 集成测试
- 记录结果

### 步骤 5: 文档
- 创建设置日志
- 创建快速参考
- 提供使用示例

## 📊 示例调用

```bash
# 为 self-improving 创建设置
为 self-improving 创建设置流程

# 为 weather 创建配置
为 weather 创建设置流程

# 为 proactive-agent 初始化
初始化 proactive-agent 配置

# 为 news-summary 设置
设置 news-summary 技能
```

## 🎯 输出内容

每次设置流程会创建：

1. **设置日志** (`setup-log.md`)
   - 设置日期
   - 创建的文件清单
   - 更新的核心文件
   - 测试结果

2. **配置文件** (如需要)
   - config.md
   - memory.md
   - state.md

3. **核心文件更新**
   - SOUL.md 添加行为指导
   - AGENTS.md 添加使用说明
   - MEMORY.md 记录事件

4. **快速参考**
   - 常用命令
   - 配置位置
   - 故障排除

## ✅ 检查清单

设置完成后确认：

- [ ] 技能文档已读取
- [ ] 目录结构已创建
- [ ] 配置文件已创建
- [ ] SOUL.md 已更新
- [ ] AGENTS.md 已更新
- [ ] MEMORY.md 已记录
- [ ] 基本功能测试通过
- [ ] 提供了快速参考
- [ ] 设置日志已记录

## 🎓 最佳实践

1. **最小化配置** - 只创建必要的文件
2. **提供默认值** - 所有配置都有合理默认值
3. **记录一切** - 详细记录设置过程
4. **可逆操作** - 提供重置/卸载方法
5. **测试导向** - 设置完成后立即测试

## 🔍 故障排除

**问题**: 技能未正确加载
**解决**: 检查 SKILL.md 格式和触发器

**问题**: 配置文件丢失
**解决**: 重新运行设置流程

**问题**: 技能行为异常
**解决**: 检查配置文件，重置为默认值

## 📚 相关技能

- `skill-creator` - 创建新技能
- `skill-vetter` - 审查技能安全性
- `find-skills` - 查找和安装技能

---

**版本**: 1.0.0
**作者**: 腾龙虾 🦞
**最后更新**: 2026-04-04
