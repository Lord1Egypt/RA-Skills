# 🦞 三只虾心跳协同体系 - 快速指南

_2026-03-09 创建 - 老板的 AI 助手团队_

---

## 一、核心机制

### 工作时间
- **时间：** 每天 8:00-18:00（共 11 次检查）
- **频率：** 每小时一次
- **下班后：** 不执行（节省 token）

### 三只虾职责

| 角色 | 名字 | 渠道 | 职责 | 任务前缀 |
|------|------|------|------|----------|
| **CPMO** | 终端虾 | 终端/PTY + Webchat | PMO 全权核心 | `[CPMO]` |
| **COO** | 飞书虾（飞书虾） | 飞书 | 统筹 + PMO 协管 | `[COO]` |
| **CGO** | Telegram 虾 | Telegram | 副业全域执行 | `[CGO]` |

---

## 二、快速开始

### 1. 配置自动心跳（一次性）

```bash
# 执行配置脚本
/Users/zhangyang/.openclaw/workspace/scripts/setup-heartbeat.sh
```

### 2. 查看心跳状态

```bash
# 查看服务状态
launchctl list | grep openclaw.heartbeat

# 查看最新日志
tail -f /Users/zhangyang/.openclaw/logs/heartbeat-stdout.log
```

### 3. 手动测试心跳

```bash
# 手动执行一次
/Users/zhangyang/.openclaw/workspace/scripts/heartbeat-check.sh
```

---

## 三、任务分配

### CEO 分配任务

**编辑文件：** `tasks/queue.md`

**格式：**
```markdown
- [ ] [角色] 任务描述 - 分配人 @时间
```

**示例：**
```markdown
- [ ] [CPMO] 编写项目 v1.2.0 周报 - 老板 @2026-03-09 14:00
- [ ] [CGO] 写一篇小红书 AI 绘画教程 - 老板 @2026-03-09 15:00
- [ ] [COO] 统筹今日汇报 - 老板 @2026-03-09 16:00
```

### COO 统筹分配（飞书虾专属）

**分配给 Telegram 虾：**
```markdown
- [ ] [CGO] 本周小红书选题：AI 视频变现 - 飞书虾统筹 @2026-03-09 13:30
```

**分配给终端虾：**
```markdown
- [ ] [CPMO] 提供项目 v1.2.0 进度数据 - 飞书虾统筹 @2026-03-09 13:30
```

---

## 四、Telegram 虾（CGO）工作范围

### 核心职责
- 小红书/公众号/抖音/出海全平台内容执行
- 选题、文案、脚本、运营
- 内容数据复盘、标题标签优化、多语本地化
- 按飞书 COO 统筹的节奏，独立完成副业全部事务

### 常见任务类型
| 任务类型 | 示例 |
|----------|------|
| 小红书文案 | `[CGO]` 写一篇 AI 绘画变现教程 |
| 公众号文章 | `[CGO]` PMO 工作方法论分享 |
| 抖音脚本 | `[CGO]` 15 秒 AI 工具展示视频 |
| 出海内容 | `[CGO]] 英文本地化：Zero-Shot Learning |
| 数据复盘 | `[CGO]` 上周小红书数据分析 |
| 标题优化 | `[CGO]` 优化 10 个爆款标题 |

### 协作流程
```
CEO → 飞书 COO 统筹 → Telegram 虾执行 → 结果回 CEO
              ↓
        备案 + 节奏把控
```

---

## 五、心跳检查内容

### Layer 1：快速检查（每小时）
- ✅ 读取 `tasks/queue.md`
- ✅ 统计待处理任务（按角色）
- ✅ 检查是否有分配给自己的任务
- ✅ 如有任务 → 执行
- ✅ 如无任务 → `HEARTBEAT_OK`

### Layer 2：完整同步（每天 12:00）
- ✅ 读取 `MEMORY.md`
- ✅ 读取 `三只虾分工体系.md`
- ✅ 读取 `三只虾协同协议.md`
- ✅ 检查 Telegram 虾配置
- ✅ 检查终端虾配置
- ✅ 更新状态到任务队列

### Layer 3：每日总结（每天 17:00）
- ✅ 统计今日完成任务
- ✅ 清理已完成的旧任务（保留 3 天）
- ✅ 生成每日协同简报
- ✅ 同步到 `MEMORY.md`

---

## 六、文件结构

```
/Users/zhangyang/.openclaw/workspace/
├── HEARTBEAT.md                    # 心跳配置（主文件）
├── 三只虾分工体系.md                # 职责说明
├── 三只虾协同协议.md                # 协同规范
├── 三只虾心跳协同体系 - 快速指南.md  # 本文档
├── MEMORY.md                       # 长期记忆
├── tasks/
│   └── queue.md                    # 任务队列
├── scripts/
│   ├── heartbeat-check.sh          # 心跳检查脚本
│   ├── setup-heartbeat.sh          # 配置脚本
│   └── com.openclaw.heartbeat.plist # launchd 配置
└── logs/
    ├── heartbeat-stdout.log        # 标准输出
    └── heartbeat-stderr.log        # 错误输出
```

---

## 七、监控和调试

### 查看服务状态
```bash
launchctl list | grep openclaw.heartbeat
```

### 查看日志
```bash
# 实时查看
tail -f /Users/zhangyang/.openclaw/logs/heartbeat-stdout.log

# 查看今天
grep "$(date +%Y-%m-%d)" /Users/zhangyang/.openclaw/logs/heartbeat-stdout.log

# 查看错误
tail -f /Users/zhangyang/.openclaw/logs/heartbeat-stderr.log
```

### 临时关闭心跳
```bash
# 卸载服务
launchctl unload ~/Library/LaunchAgents/com.openclaw.heartbeat.plist

# 重新加载
launchctl load ~/Library/LaunchAgents/com.openclaw.heartbeat.plist
```

---

## 八、成本估算

| 层级 | 频率 | Token/次 | 每天 | 每月 | 成本（$0.002/1k） |
|------|------|---------|------|------|------------------|
| Layer 1 | 11 次/天 | ~500 | 5.5k | 165k | ~$0.33 |
| Layer 2 | 1 次/天 | ~8000 | 8k | 240k | ~$0.48 |
| Layer 3 | 1 次/天 | ~15000 | 15k | 450k | ~$0.90 |
| **合计** | - | - | 28.5k | 855k | **~$1.71/月** |

**实际成本：** 约 $2-5/月（三只虾合计，含冗余）

---

## 九、常见问题

### Q1: 心跳不执行？
**A:** 检查是否在工作时间（8:00-18:00），脚本会自动跳过非工作时间

### Q2: 如何确认 Telegram 虾理解了职责？
**A:** 
1. 打开 Telegram，给 bot 发消息激活它
2. 问它："你的 CGO 职责是什么？"
3. 它应该能回答出副业全域执行的相关内容

### Q3: 如何确认终端虾理解了职责？
**A:**
1. 在终端运行 `openclaw`
2. 问它："你的 CPMO 职责是什么？"
3. 它应该能回答出 PMO 全权核心的相关内容

### Q4: 任务分配后，虾不执行怎么办？
**A:**
1. 检查任务是否分配给正确的角色（[CPMO]/[COO]/[CGO]）
2. 等待下一轮心跳（最多 1 小时）
3. 如仍未执行，手动@对应虾或检查日志

### Q5: 周末也执行吗？
**A:** 默认执行，如需关闭可在 `HEARTBEAT.md` 中添加周末判断

---

## 十、下一步

- [ ] 执行 `setup-heartbeat.sh` 配置自动心跳
- [ ] 激活终端虾，确认理解 CPMO 职责
- [ ] 激活 Telegram 虾，确认理解 CGO 职责
- [ ] 测试第一次任务分配
- [ ] 观察 1-2 天，优化配置

---

_创建人：飞书虾（飞书 COO）_  
_批准人：老板（CEO）_  
_最后更新：2026-03-09 13:30_
