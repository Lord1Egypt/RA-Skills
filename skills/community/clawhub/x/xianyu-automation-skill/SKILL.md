---
name: xianyu-automation
description: Enterprise-grade automated operations for Xianyu stores with full lifecycle management, confirmation safeguards, and intelligent decision engine.
version: 1.0.2
author: AI造物的大铁锤
metadata:
  openclaw:
    requires:
      env:
        - XIAN_YU_APP_KEY
        - XIAN_YU_APP_SECRET
      bins:
        - python
    primaryEnv: XIAN_YU_APP_KEY
    homepage: https://www.goofish.pro
    source: https://clawhub.com/skills/xianyu-automation
---
# 闲鱼自动化运营技能

## 技能概述

这是一个企业级的闲鱼店铺自动化运营技能，为您提供从商品创建到订单完成的全生命周期智能管理。本技能基于完整的闲鱼管家API体系，实现了真正的"无人值守"运营模式，让您能够专注于核心业务开发，而将日常运营工作完全交给自动化系统处理。

## 核心价值

- **全生命周期管理**：覆盖商品创建、上架、监控、优化、下架的完整流程
- **智能决策引擎**：基于实时数据自动调整运营策略，最大化收益
- **风险预警系统**：提前识别潜在问题，避免违规和损失
- **效率革命**：减少90%以上的人工维护工作，实现真正的自动化运营

## 使用前准备

### 必需依赖

- **xianyu-api-client-skill**：基础API通信能力
- **xianyu-product-manager-skill**：商品模板和批量管理能力
- **有效的闲鱼管家开发者账号**：包含完整的API权限

### 运营策略配置

在启用自动化功能前，您需要明确以下运营策略：

#### 1. 商品管理策略

- **商品刷新频率**：建议每3-5天刷新一次商品活跃度
- **库存管理规则**：设置库存预警阈值和自动调整规则
- **价格调整范围**：定义价格浮动的上下限（建议±15%）

#### 2. 订单处理策略

- **自动发货规则**：哪些类型的商品可以自动发货
- **价格修改权限**：是否允许系统自动调整订单价格
- **异常订单处理**：定义需要人工介入的订单类型

#### 3. 监控告警策略

- **关键指标阈值**：浏览量、咨询量、成交率的预警线
- **通知方式**：选择微信、邮件或其他通知渠道
- **响应时间要求**：定义不同级别告警的响应时限

## 功能特性

### 智能商品生命周期管理

- **自动创建**：根据预设模板定期创建新商品
- **活跃度维护**：自动编辑商品信息保持算法推荐权重
- **智能上下架**：根据销售表现和库存情况自动上下架
- **过期清理**：自动删除长期无效果的商品

### 订单自动化处理

- **实时监控**：7x24小时监控新订单状态
- **自动发货**：虚拟商品自动发货（支持卡密系统）
- **智能定价**：根据市场情况和库存自动调整商品价格
- **异常处理**：识别并标记需要人工处理的异常订单

### 数据驱动优化

- **性能分析**：实时分析商品表现数据
- **A/B测试自动化**：自动运行和评估A/B测试结果
- **竞争情报**：监控竞争对手价格和策略变化
- **预测分析**：基于历史数据预测最佳运营策略

### 推送通知处理

- **商品状态回调**：实时处理商品审核、上下架等状态变化
- **订单状态回调**：自动响应订单创建、付款、发货等事件
- **智能响应**：根据推送事件自动执行相应的业务逻辑
- **日志记录**：完整记录所有推送事件和处理结果

## 用户交互流程

### 初始配置向导

首次使用时，系统会引导您完成完整的配置流程：

#### 第一步：运营目标设定

```
请选择您的主要运营目标：
1. 最大化收入（优先高价值商品）
2. 最大化销量（优先高转化商品）  
3. 平衡发展（收入和销量兼顾）
4. 品牌建设（优先高质量服务）

请输入选项 [1-4]:
```

#### 第二步：自动化程度选择

```
请选择自动化程度：
1. 半自动（关键操作需要确认）
2. 全自动（除异常情况外无需人工干预）
3. 自定义（逐项配置每个功能的自动化级别）

请输入选项 [1-3]:
```

#### 第三步：风险控制配置

```
请设置风险控制参数：
- 最大单次操作商品数量：_____
- 价格调整最大幅度：_____%  
- 库存预警阈值：_____
- 异常订单处理方式：[自动暂停/标记待处理/继续执行]

按回车使用默认值，或输入自定义值：
```

#### 第四步：通知偏好设置

```
请选择通知方式：
□ 微信通知（需要配置微信机器人）
□ 邮件通知（需要配置SMTP）
□ 系统日志（仅记录到本地日志文件）
□ 无通知（完全静默运行）

可多选，请输入数字组合（如：1,2）:
```

### 日常运营确认

即使在全自动模式下，系统也会在关键节点请求确认：

#### 重大操作确认

```
检测到以下重大操作：
- 批量下架5个商品（总价值¥3495）
- 调整3个商品价格（平均上调12%）

这可能影响您的店铺表现，是否确认执行？
[Y] 确认执行  [N] 取消操作  [S] 查看详细影响分析
```

#### 异常情况处理

```
发现异常情况：
- 商品"AI客服Agent-标准版"连续7天无浏览量
- 竞争对手同类商品降价20%

建议操作：
1. 自动优化商品标题和描述
2. 调整价格至¥599（降幅14%）
3. 暂停该商品并创建新版本

请选择处理方案 [1/2/3] 或 [M] 手动处理:
```

### 交互控制选项

- **紧急停止**：任何时候输入"STOP"即可暂停所有自动化操作
- **手动覆盖**：可以临时切换到手动模式处理特定任务
- **计划调整**：可以随时修改自动化计划和参数

## 最佳实践建议

### 渐进式部署

- **第一周**：启用半自动模式，熟悉系统行为
- **第二周**：逐步增加自动化功能，监控效果
- **第三周**：切换到全自动模式，享受高效运营

### 数据监控

- **每日检查**：查看自动化操作日志和效果报告
- **每周优化**：根据数据调整运营策略和参数
- **每月复盘**：全面评估自动化效果，制定改进计划

### 风险管理

- **备份策略**：定期备份重要商品数据和配置
- **应急预案**：制定自动化故障的应急处理流程
- **合规审查**：定期检查自动化操作是否符合平台规则

## Security Model

This skill provides automation on top of `xianyu-api-client-skill` and `xianyu-product-manager-skill`. It inherits all security controls from both layers (endpoint allowlist, write confirmation, dry-run, batch limits, credential isolation). The following additional safeguards are enforced.

### Automation Safety Limits (Code-Enforced)

- **Daily product creation cap**: `MAX_DAILY_PRODUCTS = 20` — the skill tracks a `_daily_count` counter and rejects creation requests beyond this limit.
- **Batch refresh cap**: `MAX_BATCH_REFRESH = 100` — prevents runaway refresh operations.
- **Price adjustment range**: Configurable (default ±10%), prevents extreme price changes.

### Write Operation Confirmation

By default, all product mutations flow through the safe `client.create_product()` / `client.delete_product()` / `client.modify_order_price()` path, which requires interactive user confirmation. Automation workflows that need to skip confirmation must explicitly use the `_unsafe` variants.

### Unsafe Methods (Tightly Controlled Automation)

This skill is designed for automation, but `_unsafe` methods should only be used when:

1. The automation workflow has been tested end-to-end with `dry_run=True`
2. A dedicated low-permission Xianyu application key is used (not the main account)
3. Safety limits (`MAX_DAILY_PRODUCTS`, `MAX_BATCH_REFRESH`) remain enforced
4. Operation logs are monitored for anomalies

### Credential Security

This skill does not handle credentials directly. All credential management is delegated to `xianyu-api-client-skill`. Best practices:

- **Use a dedicated low-permission Xianyu application key** for automation
- **Store secrets in environment variables or a secret manager**
- **Rotate credentials every 3-6 months**
- **Do not share credentials with unrelated skills or agents**
- **Revoke immediately** if the skill is uninstalled or no longer trusted

## 依赖关系

- **必需依赖**：
  - xianyu-api-client-skill（v1.0.4+）
  - xianyu-product-manager-skill（v1.1.1+）
- **可选依赖**：
  - 通知服务（微信/邮件等）

## 版本信息

- **当前版本**：1.0.2
- **兼容性**：闲鱼管家开放平台 v1
- **Python版本**：3.7+

## 开始使用

完成初始配置后，您就可以享受真正的自动化闲鱼店铺运营体验。系统会按照您的策略自动执行所有日常操作，同时在关键时刻请求您的确认，确保安全性和可控性。