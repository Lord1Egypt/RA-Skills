# 日常运营 + 客服售后 + 合规风控三合一 Skill - 使用说明

## 📋 快速开始

### 1. 安装依赖

```bash
cd C:\Users\Administrator\.openclaw\workspace\skills\taobao-operations
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
# 每日运营日报
python scripts/operations_main.py daily-report --日期 2026-03-26

# 全店合规巡检
python scripts/operations_main.py compliance-check --全店

# 库存同步
python scripts/operations_main.py inventory-sync --款号 KZ20260326

# 每日操作清单
python scripts/operations_main.py task-list --日期 2026-03-26
```

---

## 🎯 使用方式

### 方式 1：OpenClaw 对话调用

**在 OpenClaw 中发送：**
```
生成每日运营日报
日期：2026-03-26
```

### 方式 2：终端直接调用

```bash
# 进入 Skill 目录
cd C:\Users\Administrator\.openclaw\workspace\skills\taobao-operations

# 每日运营日报
python scripts/operations_main.py daily-report --日期 2026-03-26
```

---

## 📊 输出示例

### 1. 《每日店铺运营日报》（Excel）

| 核心指标 | 今日数值 | 昨日数值 | 环比 | 异常标注 |
|----------|----------|----------|------|----------|
| 总销售额 | 15,000 元 | 12,000 元 | +25% | ✅ |
| 订单数 | 120 | 100 | +20% | ✅ |
| 客单价 | 125 元 | 120 元 | +4.2% | ✅ |
| 转化率 | 3.5% | 3.2% | +0.3% | ✅ |
| ROI | 2.5 | 2.3 | +8.7% | ✅ |

### 2. 《全店合规巡检报告》（Excel）

| 商品 ID | 商品名称 | 违禁词检测 | 属性完整性 | 风险等级 | 修改建议 |
|---------|----------|------------|------------|----------|----------|
| 1001 | 春秋夹克 | ✅ 通过 | ✅ 完整 | 低 | |
| 1002 | 休闲裤 | ✅ 通过 | ⚠️ 缺失面料 | 中 | 建议补充面料信息 |

### 3. 《每日运营关键操作清单》（Excel）

| 优先级 | 操作内容 | 操作步骤 | 完成时限 | 执行人 | 状态 |
|--------|----------|----------|----------|--------|------|
| P0-紧急 | 处理一级风险预警 | 查看预警详情→人工确认→执行处理 | 立即 | 人工 | 待处理 |
| P1-重要 | 优化低 ROI 计划 | 查看投流报告→调整出价→提交审核 | 今日 18:00 前 | 人工 | 待处理 |

---

## ⚠️ 安全限制

- 仅读 API 数据
- 不自动修改任何信息
- 客服合规回复
- 仅 3 类低风险售后自动处理
- 所有操作人工确认执行

---

## 📁 文件结构

```
taobao-operations/
├── SKILL.md
├── _meta.json
├── config.yaml
├── requirements.txt
├── .env.example
├── scripts/
│   └── operations_main.py
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
