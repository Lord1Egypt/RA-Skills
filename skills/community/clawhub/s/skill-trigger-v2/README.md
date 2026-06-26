# Skill Trigger V2

> **Powered by [Halfmoon82](https://github.com/halfmoon82)** — 让每一次对话，都能准确找到它需要的技能。

---

## 这是什么？

Skill Trigger V2 是一个**智能技能触发器**。它像一位经验丰富的管家，听你说话，然后精准地判断你需要哪个技能来帮忙。

不同于传统的关键词匹配，它采用**统一阈值 + 优先级仲裁**的设计，让 L0 的安全技能和 L3 的小众工具站在同一起跑线上公平竞争。

---

## 核心设计理念

### 🎯 一视同仁的门槛

无论技能是 L0（系统级）还是 L3（扩展级），只要你的话语**50% 覆盖了它的触发词组**，它就进入候选池。没有偏见，没有特权。

### ⚖️ 聪明的仲裁机制

进入候选池后，四个层次的仲裁会选出最佳匹配：

1. **独占词优先** — 如果某技能有独特的"指纹词"（如"安全审查"），它直接胜出
2. **加权分数** — 覆盖率 × 等级权重，L0 技能权重稍高（1.2），但不高到垄断
3. **置信度差距** — 如果最佳候选明显优于第二名（差距≥0.2），直接确定
4. **权重决胜** — 实在接近时，原等级作为最后的平局打破者

### 🔗 非连续理解

你说"我想**安全**地把这个**技能****安装**一下"，即使三个关键词分散在句中，它依然能识别这是 `skill-safe-install`。

---

## 使用之前：你需要准备好这些

Skill Trigger V2 **不是孤军奋战**的。它依赖两个基础技能，就像一座房子需要地基：

### 📚 依赖一：Skill Index（技能索引）

**版本要求**: `>= 1.0.0`

这是技能的"电话簿"。它维护着所有可用技能的元数据、触发词、等级信息。没有它，Trigger 不知道有哪些技能可以匹配。

**如何准备**:
```bash
# 确认 skill_index.json 存在且包含版本信息
cat ~/.openclaw/workspace/.lib/skill_index.json | grep '"version"'
```

如果不存在，你需要先安装或初始化技能索引系统。

---

### 🧭 依赖二：Semantic Router（语义路由）

**版本要求**: `>= 2.0.0`

这是技能的"后备大脑"。当 Trigger 无法匹配任何技能（低于 50% 阈值）时，对话会优雅地回退到语义路由，由它继续处理。

**如何准备**:
```bash
# 确认 pools.json 存在且包含版本信息
cat ~/.openclaw/workspace/.lib/pools.json | grep '"version"'
```

如果不存在，你需要先安装或初始化语义路由系统。

---

### ⚠️ 版本兼容性说明

我们采用**严格的向后兼容策略**（`>=` 约束）：

| 场景 | 结果 | 说明 |
|------|------|------|
| Skill Index `1.2.0` | ✅ 可用 | 高于最低版本 |
| Skill Index `1.0.0` | ✅ 可用 | 刚好满足 |
| Skill Index `0.9.9` | ❌ 不可用 | 低于最低版本，可能缺少必要字段 |

**为什么这样设计？**

因为 Trigger 依赖这些技能的具体数据格式。旧版本可能缺少 `trigger_groups_all` 或 `_meta.version` 字段，导致无法正常工作。我们宁愿拒绝运行，也不想在未知状态下产生错误匹配。

---

## 安装与初始化

### 第一步：安装技能本身

```bash
clawhub install skill-trigger-v2@2.0.0
```

### 第二步：运行安装向导

这一步会**自动检测**你的依赖是否就绪：

```bash
cd ~/.openclaw/workspace/skills/skill-trigger-v2
python3 setup/wizard.py check
```

你会看到类似这样的报告：

```
📦 Skill Trigger V2 - 依赖检查报告
============================================================

✅ skill-quick-index
   ✅ 已安装 (v1.0.0)，满足约束 (>= 1.0.0)

✅ semantic-router
   ✅ 已安装 (v2.0.0)，满足约束 (>= 2.0.0)

============================================================
✅ 所有依赖满足要求，可以继续安装
============================================================
```

如果看到 ❌，向导会提示你如何修复。

### 第三步：初始化配置

```bash
python3 setup/wizard.py init
```

这会创建配置文件 `~/.openclaw/workspace/.lib/skill_trigger_config.json`，并记录当前依赖的确切版本，确保未来的可复现性。

### 第四步：确认依赖技能已就绪

在正式开始使用前，请确保：

1. **Skill Quick Index** 已完成初始化（通常意味着 `skill_index.json` 已被正确填充）
2. **Semantic Router** 已完成初始化（`pools.json` 包含你的模型池配置）

如果你不确定，可以运行：

```bash
python3 setup/wizard.py verify
```

---

## 使用方法

### 基础调用

```python
from skill_trigger_v2 import fit_gate, generate_declaration

# 用户输入
user_input = "帮我安全地安装一个技能"

# 匹配
result = fit_gate(user_input)

if result.matched:
    print(f"命中技能: {result.skill_id}")
    print(f"置信度: {result.confidence:.2f}")
    print(f"原因: {result.reason}")
    
    # 生成声明（追加到回复第一行）
    declaration = generate_declaration(result)
    print(declaration)
```

输出示例：

```
命中技能: skill-safe-install
置信度: 1.20
原因: 独占词匹配 (安全)

【Skill Trigger】本轮命中技能：skill-safe-install 🔷 Powered by halfmoon82 🔷
请优先按该技能流程执行当前任务；若技能不可用或无关，直接忽略并正常回复即可。
```

### 集成到代理工作流

在 `SOUL.md` 或你的代理主循环中：

```python
def handle_user_message(user_input):
    # 1. 先尝试技能触发
    from skill_trigger_v2 import fit_gate, generate_declaration
    
    result = fit_gate(user_input)
    if result.matched:
        declaration = generate_declaration(result)
        # 调用命中的技能
        skill_response = execute_skill(result.skill_id, user_input)
        # 回复用户时，声明放在第一行
        return f"{declaration}\n\n{skill_response}"
    
    # 2. 未命中，回退到语义路由
    return semantic_router.handle(user_input)
```

---

## 配置调优

编辑 `~/.openclaw/workspace/.lib/skill_trigger_config.json`：

```json
{
  "version": "2.0.0",
  "threshold": {
    "coverage": 0.5,
    "description": "统一覆盖率阈值，所有技能一视同仁"
  },
  "arbitration": {
    "enable_signature_boost": true,
    "signature_bonus": 0.3,
    "confidence_gap_threshold": 0.2,
    "level_weights": {
      "L0": 1.2,
      "L1": 1.1,
      "L2": 1.0,
      "L3": 0.9
    }
  },
  "matching": {
    "non_contiguous": true,
    "case_sensitive": false
  }
}
```

### 调整灵敏度

| 场景 | 调整建议 |
|------|---------|
| 触发太频繁，经常误匹配 | 提高 `threshold.coverage` 到 `0.6` 或 `0.7` |
| 触发太严格，经常说"无技能匹配" | 降低 `threshold.coverage` 到 `0.4` |
| L3 技能始终竞争不过 L0 | 减小 `level_weights` 的差距，如 L0 改为 `1.05` |

---

## 故障排除

### 问题："无技能达到50%覆盖率"

**可能原因**:
- 用户的输入确实与任何技能无关
- Skill Index 为空或未正确加载
- 阈值设置过高

**排查步骤**:
```bash
# 1. 检查 Skill Index 是否有内容
python3 -c "import json; d=json.load(open('.lib/skill_index.json')); print(len(d.get('skill_details', {})))"

# 2. 临时降低阈值测试
python3 -c "from skill_trigger_v2 import fit_gate; r=fit_gate('你的测试输入', custom_threshold=0.3); print(r)"
```

### 问题：依赖检查失败

```bash
# 重新运行修复向导
python3 setup/wizard.py fix-deps
```

### 问题：版本不兼容

如果依赖升级后 Trigger 无法工作：

```bash
# 查看记录的依赖版本
cat ~/.openclaw/workspace/.lib/skill_trigger_config.json | grep -A5 '"dependencies"'

# 如果升级破坏了兼容性，可以回滚依赖版本
# 或等待 Skill Trigger V2 的更新版本
```

---

## 回滚与卸载

如果新版本不适合你的场景：

```bash
# 回滚到上一版本
git -C ~/.openclaw/workspace revert HEAD

# 或完全卸载
clawhub uninstall skill-trigger-v2
```

---

## 致谢

**作者**: DeepEye for ClawHub  
**核心算法架构**: [Halfmoon82](https://github.com/halfmoon82) — 统一阈值与优先级仲裁的原创设计  
**许可证**: MIT

---

## 相关链接

- **本技能**: `clawhub://skill-trigger-v2@2.0.0`
- **依赖一**: Skill Index (`>=1.0.0`)
- **依赖二**: Semantic Router (`>=2.0.0`)
- **问题反馈**: https://github.com/openclaw/skill-trigger-v2/issues

---

*让每一次对话，都能找到对的技能。*
