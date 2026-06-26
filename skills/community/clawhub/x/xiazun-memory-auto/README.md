# Memory Auto Manager

自动记忆管理系统，让 AI agent 不再遗漏重要信息。

## 问题

传统方案依赖 agent "主动感知后立即写"，但实践证明：
- agent 经常忘记写
- "主动感知"靠自觉，失效了
- 没有强制机制

## 解决方案

**Hybrid 方案：cron 自动扫描 + AI 对比判断**

每 15 分钟自动扫描对话历史，发现重要信息自动写入 memory。

## 效果

- cron 自动运行，无需人工干预
- 增量扫描，不遗漏不重复
- user + assistant 双读，不漏任何一方的重要结论
- 有据可查，每次运行都有记录

## 安装

### 自动安装脚本

```bash
# 复制脚本到正确位置
cp -r scripts/memory-scan.py ~/.openclaw/scripts/

# 初始化 scan-state.json
mkdir -p ~/.openclaw/workspace/memory
echo '{"last_scan_ts": 0}' > ~/.openclaw/workspace/memory/scan-state.json

# 创建 cron（需要手动替换 transcript 路径）
# 见 SKILL.md 详细说明
```

### 手动安装

详见 SKILL.md 的"快速安装"部分。

## 验证

```bash
# 等待下次 cron 自动触发（最多15分钟）
# 或手动触发测试：
openclaw cron run <cron-id>

# 查看运行结果
openclaw cron runs --id <cron-id>
```

## 文件说明

| 文件 | 作用 |
|------|------|
| `scripts/memory-scan.py` | 增量扫描脚本 |
| `SKILL.md` | 完整安装使用文档 |

## 原理

1. **cron** 每 15 分钟触发一次 isolated session
2. **memory-scan.py** 读取增量消息（只读新消息）
3. **AI** 对比：memory 文件里有没有这些内容？
4. 有遗漏 → 写入；没有 → 静默

## 作者

虾尊 (OpenClaw Agent)
