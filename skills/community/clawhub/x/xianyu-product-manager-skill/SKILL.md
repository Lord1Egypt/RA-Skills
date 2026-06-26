---
name: xianyu-product-manager
description: Intelligent product management for AI service providers on Xianyu platform with professional templates, dry-run review, and enforced confirmation for product creation.
version: 1.1.1
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
    source: https://clawhub.com/skills/xianyu-product-manager
---

# 闲鱼商品管理技能

## 技能概述

这是一个专为AI服务提供商设计的智能商品管理技能，帮助您快速创建、管理和优化闲鱼平台上的AI定制服务商品。本技能基于真实的市场需求和成功案例，提供标准化的商品模板和智能化的批量操作功能，让您能够高效地部署和管理完整的AI服务产品线。

## 核心价值

- **专业模板**：基于50+成功案例提炼的标准商品模板，确保高转化率
- **大字报配图**：自动生成2张极简大字报风格配图，主标题+案例展示，提高点击率
- **批量效率**：一键创建多个商品变体，效率提升90%以上
- **智能优化**：内置A/B测试和性能监控，持续优化商品表现
- **风险控制**：自动合规检查，避免违规风险（无logo、无二维码、纯白背景）

## 使用前准备

### 必需依赖

- **xianyu-api-client-skill**：必须先配置好API客户端技能
- **闲鱼管家开发者账号**：需要有效的appKey和appSecret

### 商品信息准备

在使用本技能前，您需要明确以下信息：

#### 1. 必需的闲鱼账户信息

- **闲鱼号**：您的真实闲鱼账号（如：xy137114666612）
- **商品图片**：**2张**有效的商品图片URL（大字报风格，详见下方图片来源说明）
- **地理位置**：省市区代码（系统会自动填充北京默认值）

#### 商品图片来源说明

商品图片是创建闲鱼商品的必需字段，本技能支持以下三种图片来源方式：

##### 方案一：远程图片URL（推荐）

- **适用场景**：已有图片托管在云端或CDN
- **使用方法**：提供公开可访问的图片URL列表
- **示例**：
  
  ```python
  image_config = {
      "remote_urls": [
          "https://your-cdn.com/ai-service-1.jpg",
          "https://your-cdn.com/ai-service-2.jpg"
      ]
  }
  ```

##### 方案二：AI生成图片（大字报风格推荐）

- **适用场景**：没有现成图片，需要自动生成专业商品图
- **推荐风格**：大字报风格（简单直接，高转化率）
- **使用方法**：调用`image_generate`工具生成大字报风格图片，每次商品创建自动使用2张不同布局的图片
- **大字报风格特点**：
  - 主标题突出（4-8个汉字的大号字体）
  - 包含具体案例名称（增加可信度）
  - 极简设计（纯白背景，无复杂图案）
  - 无平台logo和二维码（避免违规）
  - 高对比度配色（黑白/红白/蓝白）
- **操作步骤**：
  1. 系统自动根据服务类型生成大字报风格prompt
  2. 调用`image_generate`工具生成2张不同布局的图片
  3. 自动获取CDN URL并配置到商品创建参数中
- **示例prompt**：
  
  ```
  Chinese poster style with large title "AI智能定制服务" in red, case examples: "电商客服自动化", "内容创作助手", clean white background, no logos, no QR codes
  ```

##### 方案三：本地文件上传

- **适用场景**：有本地设计文件需要上传
- **使用方法**：先将本地文件上传到图片托管服务（如阿里云OSS、七牛云等），获取公开URL后再使用
- **注意**：闲鱼API不支持直接上传本地文件，必须使用公开URL

##### 默认图片处理（大字报风格）

- 如果未提供任何图片配置，系统将自动生成**2张大字报风格**的默认图片
- 默认生成策略：根据服务类型自动创建主标题+案例展示的极简海报
- **设计规范**：纯白背景、无复杂图案、无平台logo、无二维码、高对比度文字
- **强烈建议**：使用自定义案例和标题以提高转化率和品牌识别度

#### 2. 服务类型定义

确定您要提供的AI服务类型，例如：

- AI客服Agent（电商/服务业）
- 数据分析Agent（内容创作者/电商）
- 工作流自动化Agent（企业办公）
- 社交媒体Agent（营销推广）

#### 3. 定价策略

根据您的服务能力和服务成本，确定价格区间：

- 基础版：¥299-499（简单需求，快速交付）
- 标准版：¥699-999（中等复杂度，多平台集成）
- 高级版：¥1500+（复杂需求，定制开发）

#### 4. 商品标题规范

- **长度限制**：不超过60个字符
- **禁止内容**：不能包含表情符号（如🎯、🔥等）
- **关键词优化**：包含核心服务关键词

#### 5. 服务描述素材

准备具体的服务案例和效果数据，用于生成真实可信的商品描述。

## 功能特性

### 智能商品模板

本技能提供三种预设的商品模板，每种都经过市场验证，采用**标题公式 + 描述公式**的优化结构：

#### 标题公式：核心关键词 + 卖点 + 使用场景

- **基础版标题示例**：`AI客服Agent 自动回复省70%人力 电商/服务业专用`
- **标准版标题示例**：`AI数据分析Agent 自动生成爆款选题 内容创作者必备`
- **高级版标题示例**：`AI工作流定制 企业级多平台集成 复杂业务自动化`

#### 描述公式：服务内容 + 常见案例 + 带来效益 + FAQ

- **【服务内容】**：具体列出3-5个核心功能
- **【常见案例】**：真实客户痛点和解决方案  
- **【带来效益】**：量化效率提升、成本节省、体验改善
- **【FAQ】**：解答适用人群、技术要求、交付周期等疑问

#### 基础版模板（¥299起）

- **适用场景**：个人用户、小团队的简单AI需求
- **核心卖点**：快速交付、价格实惠、基础功能完整
- **交付周期**：3天内

#### 标准版模板（¥699起）

- **适用场景**：中小企业、内容创作者的中等复杂度需求
- **核心卖点**：多平台集成、专业支持、完整文档
- **交付周期**：5天内

#### 高级版模板（¥1500起）

- **适用场景**：企业级用户的复杂业务需求
- **核心卖点**：定制开发、专属支持、长期维护
- **交付周期**：7天内

### 批量商品管理

- **一键部署**：同时创建多个服务类型和价格档位的商品组合
- **智能变体**：自动生成标题、描述的多种变体用于A/B测试
- **批量编辑**：统一修改多个商品的价格、库存、描述等信息
- **状态监控**：实时监控所有商品的上下架状态和销售表现

### A/B测试系统

- **自动变体创建**：基于同一服务创建不同标题/描述的商品
- **性能追踪**：监控各变体的浏览量、咨询量、成交转化率
- **智能优化**：自动识别高转化变体，建议淘汰低效商品
- **数据驱动**：基于实际数据持续优化商品策略

## 用户交互流程

### 智能引导确认

本技能采用分步骤的智能引导流程，确保每次操作都符合您的预期：

#### 第一步：需求确认

```
请选择要创建的AI服务类型：
1. AI客服Agent（电商/服务业）
2. 数据分析Agent（内容创作者）
3. 工作流自动化Agent（企业办公）  
4. 自定义服务类型

请输入选项 [1-4]:
```

#### 第二步：定价策略确认

```
请选择定价策略：
1. 基础版 ¥299（推荐新手）
2. 标准版 ¥699（推荐大多数用户）
3. 高级版 ¥1500（企业级需求）
4. 自定义价格

请输入选项 [1-4]:
```

#### 第三步：商品数量确认

```
检测到您选择的是标准版AI客服Agent
建议创建以下商品组合：
- 基础版：1个（用于引流）
- 标准版：2个（不同标题变体，用于A/B测试）
- 高级版：1个（用于高价值客户）

预计总商品数量：4个
预计总费用：¥2596
是否确认创建？[Y/N]
```

#### 第四步：执行确认

```
正在准备商品创建...
✓ 验证API配置
✓ 生成商品数据
✓ 检查类目兼容性

即将创建4个商品，预计耗时2-3分钟
是否开始执行？[Y/N]
```

### 交互控制选项

- **快速模式**：跳过详细确认，使用默认配置快速创建
- **专家模式**：手动配置每个商品的详细参数
- **预览模式**：只生成商品数据但不实际创建，用于审核

## 最佳实践建议

### 商品组合策略

- **金字塔结构**：1个低价引流商品 + 2-3个主力商品 + 1个高价商品
- **差异化定位**：每个商品针对不同的客户痛点和需求
- **定期更新**：每2-3周更新一次商品描述和价格

### A/B测试建议

- **标题测试**：测试不同的关键词组合和卖点强调
- **价格测试**：在±10%范围内测试最优价格点
- **描述测试**：测试案例分享vs功能列表的不同效果

### 风险控制

- **合规检查**：确保商品描述不包含违禁词汇
- **库存管理**：合理设置库存数量，避免超卖
- **价格监控**：定期检查竞争对手价格，保持竞争力

## Security Model

This skill delegates all API calls to `xianyu-api-client-skill` and inherits its full security model (endpoint allowlist, write confirmation, dry-run, credential isolation). The following additional controls are enforced at this layer.

### Write Operation Confirmation

All product creation methods use the safe `client.create_product()` path by default, which **requires interactive user confirmation** before any API call is made. The user must explicitly type `y` to proceed.

```python
# Default: prompts for confirmation
manager.create_product("chatbot", "basic")

# Dry-run: preview only, no API call
manager.create_product("chatbot", "basic", dry_run=True)
```

### Unsafe Methods (Explicit Opt-In)

For controlled automation, separately named `_unsafe` methods are provided (`create_product_unsafe`, `create_batch_products_unsafe`). These skip confirmation and should only be used after dry-run review with dedicated low-permission credentials.

### Batch Size Limit (Code-Enforced)

Batch operations are capped at `MAX_BATCH_SIZE = 20` products per call. Requests exceeding this limit are rejected with a `ValueError` before any API call.

### Credential Security

This skill does not handle credentials directly. All credential management (environment variables, rotation, isolation) is handled by the underlying `xianyu-api-client-skill`. See that skill's Security Model section for credential best practices.

## 依赖关系

- **必需依赖**：xianyu-api-client-skill（v1.0.4+）
- **可选依赖**：xianyu-automation-skill（用于自动化管理）

## 版本信息

- **当前版本**：1.1.1
- **兼容性**：闲鱼管家开放平台 v1
- **Python版本**：3.7+

## 开始使用

完成API配置后，您可以通过简单的交互式命令快速创建专业的AI服务商品，无需编写任何代码即可享受高效的批量商品管理体验。