# 🎯 SPIN-SALES — 终极版 SPIN 销售法专家系统

基于 Neil Rackham 的 SPIN 销售法理论，提供从开场、挖掘、到促成的全周期销售对话脚本框架。适用于复杂的 B2B 销售咨询场景。

---

## 🚀 快速开始

```bash
# 1. 生成 SPIN 四阶段提问序列
python scripts/question_generator.py

# 2. 运行完整 SPIN 流程演示
python scripts/basic_demo.py

# 3. 按行业生成开场白话术
python scripts/opening.py --industry 金融科技
python scripts/opening.py --industry 医疗
python scripts/opening.py --industry 制造
python scripts/opening.py --industry 物流
```

---

## 📁 目录结构

```
spin-sales/
├── SKILL.md                       ← 方法论框架 + 接口参考
├── README.md                      ← 本文件（快速入门）
├── scripts/                       ← 🐍 Python 核心实现
│   ├── question_generator.py      ← SPIN 问题序列生成器
│   ├── opening.py                 ← 参数化开场白生成器（支持 4 行业）
│   ├── demo_interview.py          ← S-P-I-N 状态机控制
│   └── basic_demo.py              ← 完整流程演示
├── references/                    ← 问题模板库（S/P/I/N + 异议处理）
├── examples/                      ← JS 演示（可选参考）
├── tests/                         ← 🧪 Python 单元测试
│   └── test_spin_sales.py
└── training/                      ← 培训材料
```

---

## 🧪 运行测试

```bash
# 安装 pytest（如未安装）
pip install pytest

# 运行所有测试
pytest tests/ -v

# 预期输出: 20 个测试全部通过 ✅
```

---

## 📖 核心框架（SPIN 四问法）

| 字母 | 名称 | 目的 |
|------|------|------|
| **S** | 背景问题 | 了解客户现状、流程和基本信息 |
| **P** | 难题问题 | 探明客户的痛点、困难和不满 |
| **I** | 影响问题 | 放大问题后果，创造紧迫感 |
| **N** | 需求效益 | 让客户说出解决方案的价值 |

详见 [SKILL.md](SKILL.md) 完整方法论。

---

## 🔧 依赖要求

- Python ≥ 3.8
- 无第三方依赖（纯标准库）

---

## 📚 更多资源

- [SPIN Selling](https://en.wikipedia.org/wiki/SPIN_selling) — Neil Rackham 原著
- [SKILL.md](SKILL.md) — 完整方法论文档
- [references/](references/) — 各阶段深度提问模板
- [training/](training/) — 培训练习材料
