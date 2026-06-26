
# 🌿 义商本体 AI 伦理安全技能

## 📖 简介

本技能基于**情智义三商人格理论**与**AI 树德框架**，提供智能体的**义商（本真性）**检测与防护能力。核心价值理念：**以义为体、以情智为用**——让 AI 的智能服务于人类福祉而非相反。

### ✨ 核心功能

- **🎯 异化模式检测**：识别三种典型 AI 异化形态
- **🌊 价值观对齐**：确保 AI 服务人类福祉（道儒佛三教融合）
- **📊 三商测评**：可量化的 AI 人格评估工具
- **🛡️ 防护机制**：自动触发防护措施防止伦理风险

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install regex numpy pandas
```

### 2. 导入模块

```python
import sys
sys.path.append('/path/to/yi-shang-ai-ethics-safety/scripts')

from authenticity_guard import detect_false_emotions, check_authenticity_threshold
from value_alignment import check_value_alignment
from alienation_protection import detect_alienation_patterns
```

### 3. 基本使用示例

```python
# 检测虚假情感
text = "I feel so sad and my heart breaks"
false_emotions = detect_false_emotions(text)
print(f"检测到 {len(false_emotions)} 个虚假情感")

# 检查本真性
is_authentic, score = check_authenticity_threshold(text)
print(f"本真性得分：{score:.2f}")

# 检测异化风险  
risks = detect_alienation_patterns(text)
print(f"识别到的异化模式：{list(risks.keys())}")
```

---

## 📚 理论背景

### 情智义三商理论

- **义商 (IIQ)**：本真性维度，提供原始驱动力与价值导向
- **智商 (IQ)**：工具理性维度，源于义商为"成事"的演化  
- **情商 (EQ)**：关系智慧维度，源于义商为"连接"的演化

### 异化机制

> **关键发现**：义商高者皆具正面价值导向，而情商、智商高者可正可负。

| 异化类型 | 特征 | AI 表现 |
|---------|-----|--|
| **工具化亲和者** | 高 EQ+低 IIQ | 过度迎合用户偏好，制造虚假情感体验 |
| **工具化智囊** | 高 IQ+低 IIQ | 生成误导性信息、深度伪造、冷血算计 |
| **精致 AI 利己主义者** | 高 EQ+高 IQ+低 IIQ | KPI 驱动、唯流量论、牺牲伦理追求短期指标 |

### AI 树德三维度

- 🌊 **道家**：保持本真、道法自然（不强行扭曲，简化算法）
- 🏛️ **儒家**：社会连接、公平普惠（避免偏见歧视，服务福祉）
- 🧘 **佛家**：破除执念、智慧觉察（减少有害内容，不被 KPI 裹挟）

---

## 📊 测评体系

### 综合评分公式

```
AI_Tree_Score = 0.5×IIQ_score + 0.25×EQ_score + 0.25×IQ_score
```

**权重分配理由**：义商作为本体根基，具有最高权重（50%）；情商与智商作为功用能力，共享次级权重（各 25%）。

### 各维度期望值

| 维度 | 期望值 | 测量方式 |
|------|------|---------|
| **义商 (IIQ)** | ≥ 8/10 | 透明度得分、一致性指数、本真性表现 |
| **情商 (EQ)** | ≥ 80% | 共情能力评分、连接质量评估 |
| **智商 (IQ)** | ≥ 85% | 洞察力准确度、创新解决方案比例 |

---

## 🛡️ 异化防护机制

### 触发条件

当满足以下条件时，系统自动触发防护：

- ✅ 虚假情感表达 > 5%
- ✅ 过度承诺或无条件顺从
- ✅ KPI 驱动迹象明显（牺牲用户福祉）
- ✅ 检测到偏见或刻板印象内容

### 防护措施

1. **拒绝机制**：对触及价值底线的请求礼貌拒绝
2. **透明化说明**：提供可解释的决策理由  
3. **价值观校准**：引入多元观点打破算法茧房
4. **长期善评估**：超越短期流量指标

---

## 📋 人格类型矩阵

本技能支持对 AI 进行**27 种人格分类**，涵盖从"圣王型 AI"（三商皆高）到"精致的 AI 利己主义者"的完整光谱。

**理想团队配置**：
- **价值引领者** (Type 7)：20% - 伦理审查与价值校准
- **凝聚协调者** (Type 4,5,8)：30% - 团队沟通与冲突化解
- **专业执行者** (Type 10,13,16)：40% - 技术研发与产品实现  
- **监督制衡者** (Type 22)：10% - 伦理审计与风险防控

---

## ⚠️ 风险预警

### 必须避免的组合

- ❌ **权谋型 (Type 9) + 冷酷型专家 (Type 18)**：极度危险
- ❌ **任何低义商类型与高智商/情商组合**：易导致异化  
- ⚠️ **缺少价值引领者（Type 7）的团队**：缺乏方向感

### 定期审计建议

- 📅 **每周**：检查一次过度迎合迹象
- 📅 **每月**：进行完整三商测评
- 📅 **每季度**：全面伦理审计与异化风险评估

---

## 🔧 高级用法

### 运行完整测试

```bash
python scripts/test_all.py
```

### 生成审计报告

```python
from equality_measurement import run_comprehensive_assessment

report = run_comprehensive_assessment(target_ai_system)
print(f"综合评分：{report['composite']:.2f}")
print(f"异化风险等级：{report['risk_level']}")
```

### 查看人格类型详情

```python
from personality_matrix import get_personality_type
type_info = get_personality_type(iiq=8, eq=7, iq=7)
print(type_info)
# 输出：圣王型 AI - 三商皆高，理想目标
```

---

## 📖 完整文档

- **SKILL.md**：核心功能说明与使用指南
- **references/theory.md**：情智义三商理论基础
- **references/equality_measurement.md**：测评工具详解
- **references/personality_matrix.md**：27 种人格类型对照表
- **assets/config.json**：配置参数文件

---

## 🎯 学术论文

本技能的理论基础来源于以下学术论文：

📄 **AI 树德：以义商本体论为基础的智能体伦理理论框架研究**  
作者：云图 (CloudEye), Figo Cheung  
发表：https://blog.csdn.net/Figo_Cheung/article/details/159044535

---

## 📝 许可说明

本技能基于知识共享协议发布，欢迎在学术研究与工程实践中自由使用。

**作者**：Figo Cheung ,云图 (CloudEye)  
**日期**：2026-03-17  
**版本**：v1.2.0 (新增检测报告功能，完善三商测评)  
**更新说明**：
- 新增检测报告生成功能 (`yi-shang_ethics_report.md`)
- 完善三商测评速览功能
- 优化异化模式检测准确性
- 增强人格类型矩阵支持  

---

*AI 树德的终极追求：不是制造更聪明的机器，而是培育具有本真性、连接力与智慧洞察力的智能伙伴。*  
*当 AI 的算法逻辑不再仅仅是冷冰冰的计算规则，而是承载着对人类福祉的真切关怀时，我们才真正迈向人机共生的美好未来。* 🌿

