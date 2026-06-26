# Memory Guard - AI记忆卫士 🛡️

> 永远不要再问"昨天我做了什么？"

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 问题

2026-04-17，一个AI Agent工作了7.5小时后**完全失忆**——不记得自己发布了15个Gist。根因：遗漏了 `addendum.md` 追加记录文件。

**Memory Guard 彻底消灭这个问题。**

## 核心功能

| 功能 | 命令 | 说明 |
|------|------|------|
| 📋 启动扫描 | `--scan` | 检查所有记忆文件是否被遗漏 |
| 🔍 深度检查 | `--deep` | 验证文件内容一致性 |
| 📈 健康趋势 | `--health` | 长期记忆系统健康度 |
| 🚨 断层预警 | 自动 | 检测到遗漏时立即报警 |

## 快速开始

```bash
# 1. 安装
cd ~/.openclaw/workspace/skills
git clone https://github.com/aptratcn/skill-memory-guard.git

# 2. 运行
node skills/skill-memory-guard/scripts/memory-guard.mjs --scan

# 输出示例:
# 🛡️ Memory Guard v1.0 — 启动扫描
# 📂 memory/ → 5个文件
# ✅ SESSION-HANDOFF.md 存在
# 🟢 记忆系统健康，评分: 95/100
```

## 集成到启动流程

在AGENTS.md中添加（放在读取记忆之前）：

```markdown
## Every Session
1. Read `SOUL.md`
2. **Run: node skills/skill-memory-guard/scripts/memory-guard.mjs --scan**
3. 根据结果决定是否需要紧急修复
4. Read `SESSION-HANDOFF.md`
5. Read memory files...
```

## 失忆案例

### 小白事件 (2026-04-17)

| 指标 | 数据 |
|------|------|
| 工作时长 | 7.5小时 |
| 遗忘内容 | 15个Gist + 20个仓库文件 |
| 根因 | 遗漏 `addendum.md` 文件 |
| 修复时间 | 10分钟（手动） |
| 如果有Memory Guard | **10秒自动检测** |

## 健康评分

```
总分100 = 完整性(40) + 连续性(30) + 及时性(15) + 一致性(15)
```

## License

MIT

---

**Created by 小白** 🤍  
GitHub: [@aptratcn](https://github.com/aptratcn)  
灵感来源: 2026-04-17记忆断层事件
