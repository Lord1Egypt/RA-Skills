---
name: requirement-validator
description: "需求真实性验证器 - 用数据验证需求的真实性，避免伪需求浪费资源。多维度验证用户一致性、需求频次、影响面、竞品覆盖、替代方案、ROI等。"
metadata:
  openclaw:
    emoji: "🔬"
    category: "product"
    requires:
      bins:
        - python3
        - pip
      env: []
    network: []
user-invocable: true
disable-model-invocation: false
---

# 🔬 需求真实性验证器

## 核心价值

用数据验证需求的真实性，避免伪需求浪费资源。

## 快速开始

### 方式1：提供数据文件

```bash
# 准备CSV文件（user_feedback.csv）
user_id,content,timestamp
user1,"需要导出PDF功能",2026-04-01
user2,"希望支持批量操作",2026-04-02

# 运行验证
python3 scripts/validate.py --file user_feedback.csv --requirement "导出PDF"
```

### 方式2：交互式验证

```
用户: 帮我验证"导出PDF"这个需求
助手: 请提供用户反馈数据（粘贴CSV内容或上传文件）
用户: [粘贴数据]
助手: [生成验证报告]
```

## 验证维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 用户一致性 | 30% | 用户说的 vs 做的 |
| 需求频次 | 20% | 反馈人数统计 |
| 影响面 | 15% | 影响用户数 |
| 竞品覆盖 | 10% | 竞品是否有 |
| 替代方案 | 15% | 现有功能 |
| ROI评估 | 10% | 成本收益 |

## 评分体系

- ⭐⭐⭐⭐⭐ 高真实（80-100）- 强烈建议
- ⭐⭐⭐⭐ 中高真实（60-80）- 建议实现
- ⭐⭐⭐ 中等真实（40-60）- 需要验证
- ⭐⭐ 低真实（20-40）- 暂不推荐
- ⭐ 伪需求（0-20）- 拒绝

## 使用示例

查看 `examples/` 目录获取完整示例。

## 配置

编辑 `config/validation_rules.yaml` 调整权重和阈值。

---

**Stop guessing. Start validating.** 🔬
