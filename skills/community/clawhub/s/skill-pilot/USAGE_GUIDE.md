# SkillPilot 使用指南

**版本**: v0.3.1  
**定位**: 智能技能调度引擎 - 自动选择最优工具，持续学习优化

---

## 🚀 快速开始

### 安装后第一次使用

**无需任何配置**，直接使用即可！

```
伊朗最新战况
```

系统会自动：
1. ✅ 选择最优工具
2. ✅ 执行查询
3. ✅ 记录表现
4. ✅ 持续优化

---

## 📋 两种使用方式

### 方式 1: 默认模式（推荐日常使用）

**触发**: 输入内容**不包含**特殊关键词

**示例**:
```
伊朗最新战况
华为 Mate70 Pro 价格
今天天气如何
AI 技术发展趋势
```

**输出**: 简洁结果 + 来源

```
## 📊 伊朗最新战况

**冲突进入第 17-19 天**...（详细内容）

**来源**: tavily-search (响应时间：482ms)
```

**特点**:
- ⚡ 快速响应
- 📝 简洁输出
- 🎯 自动使用最优工具

---

### 方式 2: 全量模式（重要任务/对比优化）

**触发**: 输入内容**包含**以下关键词之一：
- `全量`
- `full`
- `对比`

**示例**:
```
全量模式 伊朗最新战况
mode=full 华为价格对比
对比各平台 iPhone 价格
```

**输出**: 详细对比报告

```
## 🎯 SkillPilot 全量模式执行报告

### 工具对比
| 工具 | 响应时间 | 质量分 |
|------|----------|--------|
| tavily-search | 482ms | 0.92 🏆 |
| multi-search-engine | 684ms | 0.85 |

### 🏆 最佳工具
tavily-search - 响应最快，内容最权威

### 📊 最新战况
...（详细内容）

### 自动优化
已更新默认工具：search → tavily-search
```

**特点**:
- 🔍 对比所有工具
- 🏆 自动选择最优
- 📈 持续优化默认设置

---

## 💡 使用场景

### 场景 1: 日常查询（默认模式）

```
用户：伊朗最新战况
SkillPilot: 直接使用最优工具，返回简洁结果
```

**适用**: 天气、新闻、价格、百科等日常查询

---

### 场景 2: 重要调研（全量模式）

```
用户：全量模式 对比各平台 iPhone 18 价格
SkillPilot: 对比所有工具，选择最优，自动更新默认设置
```

**适用**: 重要决策、多方对比、深度调研

---

### 场景 3: 持续优化

```
第 1 次：全量模式 中东局势分析
├─ 对比 3 个工具
├─ tavily-search 最优
└─ 自动更新默认工具

第 2 次：中东局势分析（默认模式）
└─ 直接使用 tavily-search（无需对比）

第 3 次：全量模式 中东局势分析
├─ 再次对比所有工具
├─ 如果有更优工具 → 自动更新
└─ 如果 tavily-search 仍最优 → 保持默认
```

**适用**: 长期使用，越用越聪明

---

## 🎯 常见问题

### Q1: 如何查看当前默认工具？

**方法 1**: 查看配置文件
```bash
cat ~/.openclaw/workspace/skills/skill-pilot/config/mode_config.json
```

**方法 2**: 使用默认模式查询，会显示使用的工具

---

### Q2: 如何重置默认工具？

```bash
# 编辑配置文件，修改默认工具
nano ~/.openclaw/workspace/skills/skill-pilot/config/mode_config.json

# 或者删除配置文件，恢复默认
rm ~/.openclaw/workspace/skills/skill-pilot/config/mode_config.json
```

---

### Q3: 全量模式会每次都更新默认工具吗？

**不会**。只有当发现更优工具时才会更新。

```
如果 tavily-search 仍然最优 → 保持默认
如果发现有更好的工具 → 自动更新
```

---

### Q4: 默认模式如何判断使用哪个工具？

**自动判断逻辑**:
1. 检查输入内容是否包含"全量/full/对比"
2. 无关键词 → 默认模式（使用默认工具）
3. 有关键词 → 全量模式（对比所有工具）

---

### Q5: 支持哪些任务类型？

| 任务类型 | 默认工具 | 工具池 |
|---------|---------|--------|
| **搜索** | tavily-search | multi-search-engine, exa-web-search-free, tavily-search |
| **抓取** | web_fetch | web_fetch, scrapling-fetch |
| **总结** | summarize | summarize |
| **分析** | tavily-search | tavily-search, exa-web-search-free |

---

## 📊 优化记录

### 查看优化历史

```bash
# 查看工具表现记录
cat ~/.openclaw/workspace/skills/skill-pilot/history/execution_log.jsonl
```

### 查看技能健康状态

```bash
cd ~/.openclaw/workspace/skills/skill-pilot
python scripts/observability.py health
```

---

## 🔧 高级用法

### 自定义默认工具

编辑 `config/mode_config.json`:
```json
{
  "default_tools": {
    "search": "multi-search-engine",
    "fetch": "scrapling-fetch",
    "summarize": "summarize"
  }
}
```

### 添加工具到工具池

编辑 `config/mode_config.json`:
```json
{
  "tool_pools": {
    "search": [
      "multi-search-engine",
      "exa-web-search-free",
      "tavily-search",
      "your-custom-tool"
    ]
  }
}
```

---

## 📈 性能对比

### 默认模式 vs 全量模式

| 维度 | 默认模式 | 全量模式 |
|------|---------|---------|
| 执行工具数 | 1 个 | 3 个 |
| 响应时间 | ~500ms | ~3000ms |
| 输出长度 | 简洁 | 详细 |
| 自动优化 | ❌ | ✅ |
| 适用场景 | 日常查询 | 重要任务 |

---

## 🎓 最佳实践

### ✅ 推荐做法

1. **日常查询用默认模式** - 快速高效
   ```
   伊朗最新战况
   ```

2. **重要任务用全量模式** - 确保最优
   ```
   全量模式 对比各平台价格
   ```

3. **定期全量模式** - 持续优化
   ```
   每周一次：全量模式 常规查询
   ```

4. **查看优化报告** - 了解工具表现
   ```
   python scripts/observability.py report
   ```

---

### ❌ 避免做法

1. **所有任务都用全量模式** - 资源浪费
2. **从不用全量模式** - 无法优化
3. **频繁修改默认工具** - 影响稳定性
4. **忽略优化报告** - 失去改进机会

---

## 📝 更新日志

### v0.3.1 (2026-03-18)
- ✅ 模式自动判断（根据关键词）
- ✅ 默认模式输出优化（简洁格式）
- ✅ 全量模式保持不变

### v0.3.0 (2026-03-17)
- ✅ 双模式支持
- ✅ 自动优化工具
- ✅ 环境感知
- ✅ 历史学习

---

## 🤝 反馈与支持

**问题反馈**: 在技能目录创建 issue  
**功能建议**: 编辑 `SKILL.md` 提交建议  
**优化报告**: 运行 `python scripts/observability.py report`

---

*最后更新：2026-03-18 03:10 UTC*  
*技能位置：~/.openclaw/workspace/skills/skill-pilot/*
