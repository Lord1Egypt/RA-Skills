# 投流方案生成&全周期运营指导 Skill - 使用说明

## 📋 快速开始

### 1. 安装依赖

```bash
cd C:\Users\Administrator\.openclaw\workspace\skills\taobao-advisor
pip install -r requirements.txt
```

### 2. 配置环境变量（可选）

```bash
# 复制环境变量模板
copy .env.example .env

# 编辑 .env 文件（如使用淘宝 API）
notepad .env
```

### 3. 测试运行

```bash
# 新品测款方案
python scripts/advisor_main.py test-plan --款号 KZ20260326 --预算 5000 --周期 7

# 优化建议
python scripts/advisor_main.py optimize --计划 ID 12345 --时间范围 今日

# 复盘报告
python scripts/advisor_main.py review --周期 日 --日期 2026-03-26

# 全周期运营指导
python scripts/advisor_main.py lifecycle --款号 KZ20260326 --阶段 新品期
```

---

## 🎯 使用方式

### 方式 1：OpenClaw 对话调用

**在 OpenClaw 中发送：**
```
生成新品测款方案
款号：KZ20260326
预算：5000 元
周期：7 天
```

### 方式 2：终端直接调用

```bash
# 进入 Skill 目录
cd C:\Users\Administrator\.openclaw\workspace\skills\taobao-advisor

# 测款方案
python scripts/advisor_main.py test-plan --款号 KZ20260326 --预算 5000 --周期 7
```

---

## 📊 输出示例

### 1. 《新品测款投流方案》（Excel）

| 测款项目 | 方案内容 |
|----------|----------|
| 测款目标 | 测试 KZ20260326 市场反应 |
| 投放渠道 | 万相台无界 + 直通车 |
| 预算 | 5000 元 |
| 周期 | 7 天 |
| 达标阈值 - 点击率 | ≥3% |
| 达标阈值 - 收藏加购率 | ≥10% |
| 达标阈值 - ROI | ≥1.5 |

### 2. 《投流调整审核表》（Excel）

| 调整项 | 当前值 | 建议值 | 调整原因 | 预期效果 | 风险等级 | 人工确认 |
|--------|--------|--------|----------|----------|----------|----------|
| 关键词出价 | 1.5 元 | 1.8 元 | ROI 低于行业均值 | ROI 提升至 2.0 | 低 | |
| 人群溢价 | 10% | 15% | 收藏加购率高 | 转化率提升 20% | 中 | |

### 3. 投流日报/周报/月报

| 核心指标 | 数值 | 环比 |
|----------|------|------|
| 总曝光 | 100,000 | +10% |
| 总点击 | 3,000 | +15% |
| 总花费 | 4,500 元 | +5% |
| ROI | 2.5 | +12% |

---

## ⚠️ 安全限制

- 仅生成方案/建议/报告
- 不执行任何投流操作
- 所有操作必须人工审核
- 仅申请读权限 API

---

## 📁 文件结构

```
taobao-advisor/
├── SKILL.md
├── _meta.json
├── config.yaml
├── requirements.txt
├── .env.example
├── scripts/
│   └── advisor_main.py
├── templates/
└── reports/
```

---

## 📞 常见问题

### Q: 模块未找到？
```bash
pip install -r requirements.txt
```

### Q: 淘宝 API 调用失败？
检查 `.env` 文件中 API Key 配置是否正确

### Q: 报告生成失败？
检查输出目录是否有写权限

---

**最后更新：** 2026-03-26  
**版本：** 1.0.0
