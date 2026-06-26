# token-optimizer

> 将会话输入 token 从 10万+ 压缩至 8,000 以内的完整解决方案。
> 三层索引 + 会话摘要压缩 + 任务隔离，开箱即用，自动使用 OpenClaw AI 配置。

---

## 核心原理

```
输入token来源分析：
  系统提示    ~2,000  （固定，不可压缩）
  会话历史   ~90,000  ← 主要元凶
  记忆文件    ~5,000  ← 可优化
  当前消息      ~500  （正常）

优化后：
  系统提示    ~2,000
  latest-summary  ~1,500  ← 替代完整历史
  任务记忆    ~1,000  ← 按需加载
  近5轮对话   ~3,000  ← 滑动窗口
  当前消息      ~500
  ─────────────────
  总计        ~8,000  ✅ 压缩92%
```

---

## 快速开始

### 1. 安装（从 ClawHub）
```bash
claw install token-optimizer
```

### 2. 无需配置！
自动使用 OpenClaw 的 AI 配置，开箱即用 🎉

### 3. 初始化记忆目录
```bash
cd ~/.openclaw/workspace/skills/token-optimizer
python3 scripts/new_session.py init
```

**重要：** 记忆文件存储在 `~/.openclaw/memory/`（OpenClaw全局记忆目录），不在技能目录内。

### 4. 每次新会话开始时
```
加载顺序（严格按此顺序，总计<8000 token）：
① INDEX.md          （本技能的索引，<1KB，必读）
② latest-summary.md （上次会话压缩摘要，<2KB）
③ 任务专属记忆       （按TaskID按需加载，<1KB）
④ 近5轮对话         （滑动窗口，不加载更早历史）
```

### 4. 会话结束时压缩
```bash
# 预览压缩效果（不保存）
python3 scripts/compress_session.py --dry-run

# 实际压缩并保存
python3 scripts/compress_session.py
```

---

## 三层索引体系

### 层1：任务层（TaskID）
```
格式：{类型}-{日期}-{序号}
示例：STOCK-20260227-001 / DEPLOY-20260227-002
```

| TaskID前缀 | 场景 | 加载记忆 |
|-----------|------|---------|
| STOCK-* | 股票/行情/交易 | stock.md |
| DEPLOY-* | 部署/安装/运维 | ops.md |
| CODE-* | 编写/修改代码 | 无 |
| QUERY-* | 一次性查询 | 无 |
| REMIND-* | 定时提醒 | 无 |

### 层2：记忆层（按需加载）
```
~/.openclaw/memory/          # OpenClaw 全局记忆目录
├── index/
│   ├── INDEX.md            # 必读，<1KB
│   └── RULES.md            # 规则详情
├── sessions/
│   ├── latest-summary.md   # 最新压缩摘要，替代完整历史
│   ├── SESSION-RULES.md    # 会话规范
│   └── {日期}-summary.md   # 历史归档
└── {domain}/               # 领域专属记忆（stock/ops等）
    └── {domain}.md
```

**注意：** 记忆文件存储在 `~/.openclaw/memory/`，不在技能目录内。详见 [MEMORY_STRUCTURE.md](MEMORY_STRUCTURE.md)

### 层3：内容层（关键词匹配）
匹配度 ≥ 0.8 才纳入上下文：
- 股票/行情/持仓/止损 → 加载 stock.md
- 部署/安装/报错/systemd → 加载 ops.md
- 天气/新闻/彩票 → 仅加载 INDEX.md

---

## 压缩规则

### 保留（必须）
- 关键配置参数（API地址、路径、密钥前缀）
- 已验证的解决方案
- 错误教训（避免重复踩坑）
- 服务状态和部署路径

### 删除（必须）
- 过程性对话和重复确认
- 调试输出和临时日志
- 格式说明和冗余解释
- 已完成的中间步骤

### 压缩目标
- 单次压缩率 ≥ 60%
- latest-summary.md ≤ 2KB（约1500 token）

---

## 自动触发机制

**session_guard.py** 会在每次对话时自动检查 token 使用情况：

| 条件 | 触发动作 |
|------|---------|
| 上下文 < 4万 token | 正常，无操作 |
| 上下文 4~7万 token | 自动压缩，静默执行 |
| 上下文 > 7万 token | 自动压缩 + 提示用户新开会话 |
| 会话轮数 > 25 轮 | 自动压缩 + 提示用户新开会话 |

**使用方式：**
```bash
# 每次对话前调用
python3 scripts/session_guard.py check \
  --message "用户消息" \
  --context-size 当前token数

# 新会话开始后重置状态
python3 scripts/session_guard.py reset
```

Agent 会自动执行压缩，无需用户手动干预 ✅

---

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `scripts/session_guard.py` | ⭐ 核心：自动判断是否需要压缩/新开会话 |
| `scripts/compress_session.py` | 压缩当前会话摘要，更新 latest-summary.md |
| `scripts/new_session.py` | 初始化新会话，输出本次应加载的记忆清单 |
| `scripts/status.py` | 显示当前token使用估算和记忆文件大小 |

---

## 集成到 OpenClaw Agent

在你的 Agent 中集成：

```python
import subprocess
import json

def check_session_health(user_message: str, context_size: int):
    """检查会话健康度"""
    result = subprocess.run(
        ['python3', 'scripts/session_guard.py', 'check',
         '--message', user_message,
         '--context-size', str(context_size)],
        capture_output=True,
        text=True,
        cwd='~/.openclaw/workspace/skills/token-optimizer'
    )
    
    # 解析输出
    if 'compress' in result.stdout.lower():
        # 执行压缩
        subprocess.run(
            ['python3', 'scripts/compress_session.py'],
            cwd='~/.openclaw/workspace/skills/token-optimizer'
        )
        return 'compressed'
    elif 'new_session' in result.stdout.lower():
        return 'new_session_needed'
    else:
        return 'continue'

# 在每次对话前调用
action = check_session_health(user_message, current_token_count)
if action == 'new_session_needed':
    print("💡 建议新开会话以获得最佳体验")
```

---

## 高级配置（可选）

虽然默认使用 OpenClaw 配置，但你也可以通过环境变量自定义：

```bash
# 自定义阈值
export TOKEN_OPTIMIZER_WARN_TOKENS="40000"
export TOKEN_OPTIMIZER_CRITICAL_TOKENS="70000"
export TOKEN_OPTIMIZER_MAX_ROUNDS="25"

# 自定义任务关键词
export TOKEN_OPTIMIZER_TASK_KEYWORDS='{"MYTASK": ["关键词1", "关键词2"]}'

# 覆盖 AI 配置（高级用户）
export TOKEN_OPTIMIZER_API_KEY="your-key"
export TOKEN_OPTIMIZER_MODEL="gpt-4"
```

---

## Token节省效果

| 场景 | 优化前 | 优化后 | 节省 |
|------|--------|--------|------|
| 长会话（50轮） | ~100,000 | ~8,000 | 92% |
| 中等会话（20轮） | ~40,000 | ~6,000 | 85% |
| 新会话 | ~5,000 | ~4,000 | 20% |

---

## 为什么选择 token-optimizer？

✅ **开箱即用** - 自动使用 OpenClaw AI 配置，无需额外配置  
✅ **智能判断** - 自动检测何时需要压缩或新开会话  
✅ **任务隔离** - 避免不同任务的上下文污染  
✅ **高效压缩** - 92% token 节省，显著降低成本  
✅ **易于集成** - 简单的 Python 脚本，易于集成到任何 Agent  

---

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 贡献

欢迎贡献！请访问 [GitHub](https://github.com/yourusername/token-optimizer)
