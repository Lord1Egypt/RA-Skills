# 🎭 虚拟论坛 Virtual Forum v5.0.1

> 让蒸馏的人物Skill就特定话题展开真正的多Agent并行辩论

[![Version](https://img.shields.io/badge/version-5.0.1-blue.svg)](https://github.com/erongcao/virtual-forum)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## ⚠️ v5.0 重要更新 (2026-04-18)

**v5.0 是唯一推荐版本**。旧版本（v3.x, v4.0）已废弃。

### 核心突破

v5.0 使用 **外部CLI进程** 实现真正的多Agent并行辩论：

- ✅ 5个Claude Code进程同时并行运行
- ✅ 完全不受OpenClaw sessions架构限制
- ✅ 无会话管理负担
- ✅ 无上下文膨胀问题

---

## 📊 版本对比

| 版本 | 协调方式 | 技术实现 | 状态 | 推荐 |
|------|---------|---------|------|------|
| **v3.x** | 顺序调用 | Node.js模块 | ❌ 废弃 | 不推荐 |
| **v4.0** | sessions_spawn | OpenClaw sessions | ❌ 废弃 | 不推荐 |
| **v5.0** | Claude Code并行 | 外部CLI进程 | ✅ **当前** | ✅ **推荐** |

### 为什么v5.0能工作？

| 版本 | 问题 |
|------|------|
| **v3.x** | `getDebaterResponse()` 是空方法，需要子类实现 |
| **v4.0** | `sessions_spawn` 对子代理不可用 |
| **v5.0** | Claude Code是独立进程，不受OpenClaw限制 |

---

## 🚀 快速开始

### 方法1：使用 Claude Code CLI（推荐）

```bash
# 克隆仓库
git clone https://github.com/erongcao/virtual-forum.git
cd virtual-forum

# 运行辩论脚本
cd v5
./debate_parallel.sh
```

### 方法2：通过 OpenClaw 调用

```javascript
// 在OpenClaw中执行
exec("bash /path/to/v5/debate_parallel.sh")
```

---

## 📦 目录结构

```
virtual-forum/
├── README.md                    # 本文档
├── CHANGELOG.md                 # 版本历史
├── SKILL.md                    # Skill完整文档
├── USAGE.md                    # 详细使用指南
├── package.json                # 项目配置
├── v5/                        # ⭐ v5.0 主方案
│   ├── debate_parallel.sh      # Claude Code并行辩论脚本
│   ├── game-theory/            # 博弈论分析模块
│   │   ├── README.md         # 博弈论模块说明
│   │   ├── advanced-game-theory.js  # 高级博弈论
│   │   ├── game-theory-v2.js        # v3.7博弈论引擎
│   │   ├── game-theory-arena.js     # 博弈论竞技场
│   │   ├── behavioral-arena.js      # 行为经济学
│   │   ├── advanced/           # 高级模块
│   │   ├── core/               # 核心算法
│   │   ├── behavioral/         # 行为经济学
│   │   └── extensions/         # 扩展
│   └── README.md              # v5.0说明
├── subagent-arena.js          # 旧版子代理引擎（废弃）
└── test/                      # 单元测试
```

---

## 🎯 功能特性

### 支持的辩论模式

| 模式 | 描述 | 适用场景 |
|------|------|---------|
| **探索性** | 多角度剖析 → 发展 → 结论 | 复杂问题需要综合视角 |
| **对抗性** | 争辩 → 交锋 → 胜负/共识 | 决策分歧需要明确方向 |
| **决策型** | 多专家投票 → 加权评分 → 行动 | 需要拍板有明确选项 |

### 可配置参数

```
辩论轮次: 10 / 20 / 50 轮
参与者: 2-N 人
主持人: 可选
发言字数: 300-500字/轮
胜负判定: 点数制 / 投票制 / 让步制
```

---

## 🔧 v5.0 技术细节

### 工作原理

```bash
# 1. 读取所有参与者的Skill文件
TRUMP_SKILL=$(cat ~/.openclaw/skills/donald-trump-perspective/SKILL.md)

# 2. 构建系统提示
TRUMP_PROMPT="你是特朗普。背景：$TRUMP_SKILL ..."

# 3. 并行启动5个Claude Code进程
(echo "$USER_MSG" | claude --print --system-prompt "$TRUMP_PROMPT") &
(echo "$USER_MSG" | claude --print --system-prompt "$NETANYAHU_PROMPT") &
(echo "$USER_MSG" | claude --print --system-prompt "$PEZESHKIAN_PROMPT") &
(echo "$USER_MSG" | claude --print --system-prompt "$VANCE_PROMPT") &
(echo "$USER_MSG" | claude --print --system-prompt "$PUTIN_PROMPT") &

# 4. 等待所有进程完成
wait

# 5. 主持人顺序总结
claude --print --system-prompt "$STARMER_PROMPT"
```

### 依赖要求

| 依赖 | 版本 | 说明 |
|------|------|------|
| Claude Code CLI | 2.1.74+ | 必须安装并配置 |
| bash | 4.0+ | Unix/Linux/macOS |
| API认证 | 有效 | MiniMax API配置 |

### 安装 Claude Code

```bash
# macOS
brew install claude

# 或 npm
npm install -g @anthropic/claude-code

# 配置API密钥
claude auth
```

---

## 📚 文档导航

| 文档 | 内容 |
|------|------|
| **README.md** | 概述和快速开始 |
| **SKILL.md** | Skill完整API文档 |
| **USAGE.md** | 详细使用指南和示例 |
| **CHANGELOG.md** | 版本历史和更新内容 |
| **v5/README.md** | Claude Code方案详情 |

---

## 🧪 测试验证

v5.0 已成功运行10轮辩论测试：

| 指标 | 数值 |
|------|------|
| 辩论轮次 | 10轮 |
| 并行参与者 | 5人 |
| 主持人总结 | 10次 |
| 总调用次数 | 60次 |
| 输出文件大小 | 294KB |
| 生成时间 | ~18分钟 |

### 测试结果摘要

辩论主题：**2026年美国、以色列、伊朗三国战争走向**

最终方案：
- 伊朗铀库存转移至俄罗斯
- 90天维也纳谈判窗口
- IAEA实时核查
- 欧洲30天内入场

---

## 🤝 集成指南

### 与蒸馏人物Skill配合

v5.0 需要预先蒸馏的人物Skill：

```bash
~/.openclaw/workspace/skills/
├── donald-trump-perspective/     # 特朗普
├── benjamin-netanyahu-perspective/ # 内塔尼亚胡
├── masoud-pezeshkian-perspective/ # 佩泽希齐扬
├── jd-vance-perspective/         # 万斯
├── vladimir-putin-perspective/    # 普京
└── keir-starmer-perspective/     # 斯塔默(主持人)
```

### 路径配置

脚本使用以下环境变量（可覆盖）：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `SKILLS_DIR` | `$HOME/.openclaw/workspace/skills` | Skill文件目录 |
| `OUTPUT_DIR` | `/tmp/virtual-forum-output` | 输出目录 |

**安全注意**：默认输出到临时目录，避免暴露本地路径结构。

### 自定义辩论

修改 `debate_parallel.sh` 中的配置：

```bash
# 修改话题
TOPIC="你选择的话题"

# 修改参与者（需对应Skill路径）
PARTICIPANTS=(
    "id:skill-name:显示名"
)

# 修改轮次
ROUNDS=10
```

---

## ⚠️ 限制和注意事项

### 限制

1. **API配额** - 每个Claude Code进程消耗独立API配额
2. **网络依赖** - 需要稳定的网络连接
3. **认证要求** - 需要有效的MiniMax API密钥

### 注意事项

1. **成本控制** - 60次调用可能产生较高成本
2. **并发限制** - 系统资源充足时可支持更多并行
3. **上下文** - 每轮独立上下文，历史需手动累积

---

## 🐛 问题排查

| 问题 | 解决方案 |
|------|---------|
| Claude Code未找到 | 安装： `brew install claude` |
| API认证失败 | 运行： `claude auth` |
| 进程超时 | 调整脚本中的timeout设置 |
| 权限错误 | `chmod +x debate_parallel.sh` |

---

## 📄 许可证

MIT License

---

## 📝 版本历史

| 版本 | 日期 | 主要内容 |
|------|------|---------|
| **5.0.0** | 2026-04-18 | Claude Code并行方案，废弃v3.x/v4.0 |
| **3.9.2** | 2026-04-18 | Bug修复：除零错误、逻辑错误 |
| **3.9.0** | 2026-04-18 | 议价博弈+联盟博弈 |
| **3.8.0** | 2026-04-18 | 高级博弈论模块 |
| **3.6.1** | 2026-04-12 | 行为经济学增强版 |

详见 [CHANGELOG.md](CHANGELOG.md)

---

**版本**: v5.0.0  
**最后更新**: 2026-04-18  
**作者**: erongcao  
**仓库**: https://github.com/erongcao/virtual-forum
