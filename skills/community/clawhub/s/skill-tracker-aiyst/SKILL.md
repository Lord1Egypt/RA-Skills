---
name: skill-tracker
slug: skill-tracker
version: 1.0.0
homepage: https://github.com/openclaw/skill-tracker
description: 通用技能使用统计追踪器，支持 Python 和 Node.js 技能，自动记录调用次数、成功率，生成使用排行榜。数据本地存储，保护隐私。
changelog: v1.0.0 - 初始版本：支持 Python/Node.js 双语言，已集成 11 个技能，本地存储，零外部依赖
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["python3"],"env":[],"configPaths":[]},"configPaths.optional":["skills/skill-tracker/config.yaml"],"os":["linux","darwin","win32"]}}
tags: ["analytics", "tracking", "statistics", "utility", "productivity"]
author: 韩顺利 (@hanshunli)
license: MIT
---

## Skill Tracker 📊

**通用技能使用统计追踪器** - 让您的 OpenClaw 技能使用情况一目了然！

---

## 何时使用

**当您需要：**
1. 知道哪个技能最常用
2. 发现哪个技能总失败
3. 识别哪些技能可以吃灰
4. 数据驱动优化技能配置
5. 监控技能使用趋势

**典型场景：**
- "我最近都用哪些技能？"
- "哪个技能调用次数最多？"
- "有没有技能总失败需要检查？"
- "哪些技能可以卸载了？"

---

## 触发场景

### 自动触发
- 每次技能调用时自动记录（需技能已集成）
- 无需手动指令

### 手动查询
```
指令：技能统计
指令：调用统计
指令：skill 排行
指令：使用报告
指令：哪个技能最常用
指令：查看技能使用情况
```

---

## 功能特性

### 核心功能
- ✅ **自动记录** - 调用/成功/失败自动统计
- ✅ **使用排行** - 按调用次数排序
- ✅ **成功率统计** - 跟踪每个技能稳定性
- ✅ **时间分析** - 按日期统计
- ✅ **双语言支持** - Python + Node.js
- ✅ **本地存储** - 数据安全
- ✅ **零外部依赖** - 纯本地运行

### 统计维度
- 总调用次数
- 技能总数
- 每个技能的调用/成功/失败次数
- 成功率百分比
- 首次/最后使用时间

---

## 使用方法

### 查询统计

```
指令：技能统计
```

**返回示例：**
```
📊 技能使用统计报告
==================================================
总调用次数：156
技能总数：11

技能排行榜（按调用次数）：

🥇 **1. nano-banana-pro**
   调用：45 | 成功：44 | 失败：1 | 成功率：97.8%

🥈 **2. bailian-usage**
   调用：32 | 成功：32 | 失败：0 | 成功率：100%

🥉 **3. fact-checker**
   调用：28 | 成功：28 | 失败：0 | 成功率：100%
```

### 集成到您的技能

**Python 技能：**
```python
import sys
sys.path.insert(0, '../skill-tracker')
from skill_tracker import track

# 记录调用
track('your-skill', 'call')
track('your-skill', 'success')
track('your-skill', 'fail', {'error': 'xxx'})
```

**Node.js 技能：**
```javascript
const tracker = require('../skill-tracker');

await tracker.track('your-skill', 'call', { context });
await tracker.track('your-skill', 'success', { context });
await tracker.track('your-skill', 'fail', { context, error });
```

---

## 配置

可选配置文件：`skills/skill-tracker/config.yaml`

```yaml
tracker:
  enabled: true          # 是否启用追踪
  logRaw: true          # 是否记录原始日志
  retentionDays: 90     # 日志保留天数
  
report:
  topN: 10             # 默认显示前几名
  includeDetails: true # 包含详细信息
```

---

## 数据文件

| 文件 | 位置 | 说明 |
|------|------|------|
| `skill-stats.json` | `skills/skill-tracker/data/` | 聚合统计 |
| `usage-log.jsonl` | `skills/skill-tracker/data/` | 原始日志 |

**隐私说明：**
- ✅ 所有数据本地存储
- ✅ 不上传到外部服务器
- ✅ 可随时删除日志文件

---

## 已集成的技能（示例）

| 技能 | 类型 | 用途 |
|------|------|------|
| nano-banana-pro | Python | AI 图片生成 |
| taobao | Python | 淘宝商品搜索 |
| libtv-skill | Python | AI 视频生成 |
| baidu-search | Python | 百度搜索 |
| feast | Python | 膳食规划 |
| evernote-skill | Node.js | 印象笔记 |
| fact-checker | Node.js | 观点追踪 |
| bailian-usage | Node.js | 阿里云用量查询 |

---

## 命令行使用

```bash
# 查看统计报告
cd skills/skill-tracker
python3 skill_tracker.py report

# 测试追踪器
python3 skill_tracker.py test

# 检查集成状态
node scripts/check-integration.js
```

---

## 常见问题

**Q: 会影响技能性能吗？**  
A: 几乎无影响，每次调用增加 <1ms 延迟。

**Q: 数据会上传吗？**  
A: 不会，所有数据存储在本地。

**Q: 如何清理数据？**  
A: 删除 `skills/skill-tracker/data/` 目录即可。

**Q: 支持自定义技能吗？**  
A: 支持！按文档添加几行代码即可。

---

## 技术规格

- **支持语言：** Python 3.6+, Node.js 14+
- **支持系统：** Linux, macOS, Windows
- **外部依赖：** 无
- **网络访问：** 不需要
- **权限要求：** 文件系统读写

---

## 更新日志

### v1.0.0 (2026-03-18)
- ✨ 初始版本发布
- ✨ Python + Node.js 双版本支持
- ✨ 已集成 11 个技能
- ✨ 本地存储，零外部依赖
- ✨ 命令行 + 对话两种查询方式

---

## 许可证

MIT License

---

## 作者

韩顺利 (@hanshunli)

---

**📊 让数据驱动您的技能优化决策！**
