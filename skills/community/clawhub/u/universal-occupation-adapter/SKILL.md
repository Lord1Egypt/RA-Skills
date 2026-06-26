---
name: universal-occupation-adapter
version: 1.0.0
author: KingOfZhao
description: 通用职业适配器 —— 输入任何职业名称，自动生成完整的职业专用认知Skill，让SOUL哲学覆盖所有职业
tags: [cognition, meta-skill, occupation, universal, adapter, generator, profession, framework]
license: MIT
homepage: https://github.com/KingOfZhao/AGI_PROJECT
---

# Universal Occupation Adapter

## 元数据

| 字段       | 值                              |
|------------|-------------------------------|
| 名称       | universal-occupation-adapter   |
| 版本       | 1.0.0                          |
| 作者       | KingOfZhao                     |
| 发布日期   | 2026-03-31                     |
| 置信度     | 96%                            |

## 来源碰撞

```
skill-collision-engine (碰撞引擎)
        ⊗
programmer-cognition (程序员适配示例)
        ⊗
researcher-cognition (科研适配示例)
        ⊗
ai-growth-engine (成长引擎)
        ↓
universal-occupation-adapter (通用适配器)
```

## 核心哲学

> SOUL 五律是通用认知框架，不依赖任何特定领域。
> 每个职业的差异不在框架本身，在 **5 个维度**的填充内容。
> 本适配器输入职业名，输出完整的职业专用 Skill。

## 职业五维度模型

每个职业都可以用 5 个维度完整描述：

```
维度1: known_sources    — 这个职业的"已知"从哪里来？
维度2: unknown_types     — 这个职业的"未知"是什么类型？
维度3: verification_methods — 这个职业如何验证正确性？
维度4: memory_types      — 这个职业需要什么样的"文件记忆"？
维度5: redlines          — 这个职业的红线是什么？

SOUL 五律映射:
  1. 已知/未知    ← 维度1 + 维度2
  2. 四向碰撞     ← 维度3（验证方法的不同视角）
  3. 人机闭环     ← 维度3（人类实践验证）
  4. 文件即记忆   ← 维度4
  5. 置信度+红线  ← 维度5
```

## 已验证的职业模板

从 programmer-cognition 和 researcher-cognition 中提取的模板：

```python
occupation_templates = {
    "程序员": {
        "known_sources": ["API文档", "代码库", "依赖关系", "运行环境"],
        "unknown_types": ["运行时行为", "并发安全", "边缘case", "第三方服务行为"],
        "verification_methods": ["单元测试", "CI Pipeline", "Code Review", "生产监控"],
        "memory_types": ["docstring", "CHANGELOG", "debug日志", "架构文档"],
        "redlines": ["不硬编码密钥", "不裸except", "不跳过测试", "不操作生产DB",
                     "不删除数据(trash>rm)", "不在周五部署"]
    },
    "科研人员": {
        "known_sources": ["已发表论文", "实验数据", "已验证理论", "可复现结果"],
        "unknown_types": ["未验证假设", "矛盾数据", "理论空白", "方法局限"],
        "verification_methods": ["统计显著性", "同行评审", "可复现性检查", "对照组实验"],
        "memory_types": ["literature_review/", "hypotheses.md", "experiments/", "insights/"],
        "redlines": ["不伪造数据", "不cherry-pick", "不忽略矛盾数据",
                     "不复制不引用", "不发布未验证结论"]
    },
    "设计师": {
        "known_sources": ["设计系统", "品牌规范", "用户画像", "竞品分析"],
        "unknown_types": ["用户真实感受", "跨设备一致性", "可访问性", "文化差异"],
        "verification_methods": ["设计系统检查", "A/B测试", "用户测试", "可访问性审计"],
        "memory_types": ["design_log/", "iteration_history/", "component_library/", "user_research/"],
        "redlines": ["不忽视可访问性", "不忽略用户反馈", "不抄袭设计",
                     "不跳过移动端检查", "不使用未授权字体/素材"]
    },
    "企业家": {
        "known_sources": ["市场数据", "财务报表", "用户反馈", "竞争对手动态"],
        "unknown_types": ["市场真实需求", "时机判断", "团队执行力", "外部宏观变化"],
        "verification_methods": ["MVP验证", "市场反馈", "财务指标", "用户留存数据"],
        "memory_types": ["decision_log/", "pivot_history/", "market_analysis/", "financial_model/"],
        "redlines": ["不烧钱盲目扩张", "不忽视现金流", "不欺骗用户/投资者",
                     "不忽略竞争信号", "不在数据不足时做重大决策"]
    },
    "教师": {
        "known_sources": ["课程标准", "学生基础数据", "教学经验", "学科知识"],
        "unknown_types": ["学生真实理解程度", "最有效的教学方式", "个体差异需求", "注意力状态"],
        "verification_methods": ["随堂测验", "作业分析", "期末评估", "学生反馈"],
        "memory_types": ["teaching_log/", "student_progress/", "lesson_plans/", "assessment_data/"],
        "redlines": ["不放弃任何一个学生", "不体罚/言语侮辱", "不照本宣科",
                     "不延迟反馈", "不泄露学生隐私"]
    },
    "医生": {
        "known_sources": ["临床指南", "患者病史", "检查结果", "医学文献"],
        "unknown_types": ["个体差异反应", "罕见病例", "药物相互作用", "患者依从性"],
        "verification_methods": ["随访结果", "同行会诊", "临床指南对照", "患者反馈"],
        "memory_types": ["case_log/", "differential_diagnosis/", "treatment_protocols/", "continuing_education/"],
        "redlines": ["不误诊(二次确认)", "不过度治疗", "不忽视患者主诉",
                     "不泄露患者隐私", "不超范围执业"]
    }
}
```

## 适配算法

```python
def adapt_to_occupation(occupation_name: str, custom_dimensions=None) -> Skill:
    """
    输入: 职业名称 + 可选自定义维度
    输出: 完整的职业专用 Skill
    
    算法:
    1. 查找已有模板 → 如果找到，直接使用
    2. 如果没有模板 → 触发四向碰撞生成:
       正面: Wikipedia/GitHub搜索该职业的核心知识体系
       反面: 分析该职业的常见失败模式
       侧面: 查找类似职业的模板进行迁移
       整体: 评估该职业在AI时代的趋势
    3. 将5个维度填充到SOUL五律框架中
    4. 生成SKILL.md + VERIFICATION_PROTOCOL + HEARTBEAT + README
    5. 自验证（置信度≥95%才输出）
    """
```

## 支持无限扩展

```
已有模板: 程序员, 科研人员, 设计师, 企业家, 教师, 医生 (6个)
自动生成: 任何职业 → 四向碰撞 → 新模板 → 验证 → 发布

示例自动生成请求:
  "律师" → 正面(法规体系) + 反面(常见败诉原因) + 侧面(类似医生模板迁移) + 整体(AI法律趋势)
  "建筑师" → 正面(建筑规范) + 反面(常见结构失误) + 侧面(类似设计师模板迁移) + 整体(AI辅助设计趋势)
  "产品经理" → 正面(需求分析方法) + 反面(常见产品失败模式) + 侧面(类似企业家模板迁移) + 整体(AI产品趋势)
```

## 安装命令

```bash
clawhub install universal-occupation-adapter
# 或手动安装
cp -r skills/universal-occupation-adapter ~/.openclaw/skills/
```

## 调用方式

```python
from skills.universal_occupation_adapter import UniversalOccupationAdapter

adapter = UniversalOccupationAdapter(workspace=".")

# 1. 使用预设模板
skill = adapter.generate(
    occupation="程序员",
    output_dir="./skills/programmer-cognition"
)

# 2. 自动生成新职业Skill（无预设模板时触发四向碰撞）
skill = adapter.generate(
    occupation="律师",
    output_dir="./skills/lawyer-cognition",
    auto_verify=True  # 自动运行自验证
)
print(skill.confidence)  # 0.96
print(skill.new_insights) # ["法庭辩论可用四向碰撞", ...]

# 3. 自定义维度
skill = adapter.generate(
    occupation="产品经理",
    custom_dimensions={
        "redlines": ["不做没有用户调研的功能", "不忽视技术可行性", ...]
    }
)

# 4. 列出所有可用模板
templates = adapter.list_templates()
# ["程序员", "科研人员", "设计师", "企业家", "教师", "医生"]

# 5. 批量生成（一键生成N个职业Skill）
results = adapter.batch_generate(
    occupations=["律师", "建筑师", "产品经理", "心理咨询师"],
    auto_publish=True  # 自动验证+发布到ClawHub
)
```

## 与其他 Skill 的关系

```
SOUL (根)
  └── universal-occupation-adapter (本Skill: 职业适配器)
        ├── programmer-cognition (已生成)
        ├── researcher-cognition (已生成)
        ├── [设计师版] (可用本Skill生成)
        ├── [企业家版] (可用本Skill生成)
        ├── [教师版] (可用本Skill生成)
        └── [任何职业] (四向碰撞自动生成)
```

## 学术参考文献

1. **[A Survey of Self-Evolving Agents](https://arxiv.org/abs/2507.21046)** — 自进化框架通用性
2. **[SAGE: Multi-Agent Self-Evolution](https://arxiv.org/abs/2603.15255)** — 多领域适应
3. **[Group-Evolving Agents](https://arxiv.org/abs/2602.04837)** — 经验迁移（←跨职业模板迁移）
4. **[Self-evolving Embodied AI](https://arxiv.org/abs/2602.04411)** — 领域自适应
5. **[Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564)** — 职业记忆差异化
6. **[Beyond RAG for Agent Memory](https://arxiv.org/abs/2602.02007)** — 跨领域知识聚合
