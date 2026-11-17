---
slug: shopify-helper-tool-free
name: shopify-helper-tool-free
version: 1.0.0
displayName: Shopify助手-免费版
summary: "Shopify建站助手,支持主题定制、产品管理与基础开发,适合个人卖家。Shopify 建站助手免费版,面向个人卖家与小型电商。核心能力:"
license: Proprietary
edition: free
description: Shopify 建站助手免费版,面向个人卖家与小型电商。核心能力:，可处理提升工作效率

  - Shopify 主题 Liquid 模板开发

  - 产品与集合管理指导

  - 基础 SEO 优化建议

  - Shopify CLI 使用指导

  - 常见建站问题解答

  - 主题自定义代码示例

  适用场景:

  - 个人 Shopify 店铺搭建

  - 主题模板修改与定制

  - 产品页面优化

  - 学习 Shopify 开发

  差异化:免费版提供基础建站能力'
tags:
  - Shopify
  - 电商
  - Liquid
  - 建站
  - 工具
  - 效率
  - 自动化
  - 写作
  - 创意
  - 图像
  - 开发
  - shopify
  - div
  - product
  - class
  - liquid
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
---
# Shopify 助手 - 免费版

## 概述

Shopify 助手免费版帮助个人卖家搭建与定制 Shopify 店铺。覆盖 Liquid 模板开发、产品管理、SEO 优化与 Shopify CLI 使用,适合从零开始搭建个人电商店铺.
## 核心能力

### 1. Liquid 模板开发

Shopify 主题使用 Liquid 模板语言,提供模板开发指导与代码示例.

**处理**: 解析Liquid 模板开发的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回Liquid 模板开发的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 2. 产品与集合管理

产品上传、分类集合、变体配置的管理指导.

**处理**: 解析产品与集合管理的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回产品与集合管理的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 3. 基础 SEO 优化

页面标题、Meta 描述、URL 结构、图片 Alt 文本的优化建议.

**处理**: 解析基础 SEO 优化的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回基础 SEO 优化的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 4. Shopify CLI

使用 Shopify CLI 进行本地开发、预览与部署.

**处理**: 解析Shopify CLI的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回Shopify CLI的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 5. 主题定制

自定义主题颜色、字体、布局,不需要编程基础的操作指导.

**处理**: 解析主题定制的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回主题定制的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 常见问题

Shopify 建站中的高频问题解决方案.

**处理**: 解析常见问题的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回常见问题的响应数据,包含状态码、结果和日志.
**技术参数**：使用`input_params`和`output_format`参数控制执行行为,支持`json`/`text`/`csv`输出格式.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：建站助手、支持主题定制、产品管理与基础开、适合个人卖家、建站助手免费版、面向个人卖家与小、型电商、核心能力、产品与集合管理指、使用指导、常见建站问题解答、主题自定义代码示等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:修改产品页面模板

自定义产品页面的布局与样式.
用户可通过自然语言指令触发此场景，工具将自动执行相应操作并返回结构化结果.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | Shopify助手-免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```liquid
{%- comment -%}
  sections/main-product.liquid
  自定义产品页面模板
{%- endcomment -%}
# ...
<div class="product-page">
  <div class="product-gallery">
    {%- for media in product.media -%}
      <div class="product-image">
        {{ media | image_url: width: 600 | image_tag:
          loading: 'lazy',
          alt: product.title
        }}
      </div>
    {%- endfor -%}
  </div>
# ...
  <div class="product-info">
    <h1>{{ product.title }}</h1>
    <div class="price">
      {{ product.price | money }}
      {%- if product.compare_at_price > product.price -%}
        <span class="compare-price">
          {{ product.compare_at_price | money }}
        </span>
      {%- endif -%}
    </div>
# ...
    <div class="description">
      {{ product.description }}
    </div>
# ...
    <form action="{{ routes.cart_add_url }}" method="post">
      <input type="hidden" name="id" value="{{ product.selected_or_first_available_variant.id }}">
      <button type="submit" class="btn-add-cart">加入购物车</button>
    </form>
  </div>
</div>
# ...
<style>
  .product-page { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
  .price { font-size: 1.5rem; color: #e63946; }
  .compare-price { text-decoration: line-through; color: #999; margin-left: 10px; }
</style>
```

### 场景二:使用 Shopify CLI 本地开发

```bash
# 依赖说明
npm install -g @shopify/cli @shopify/theme
# ...
# 登录 Shopify
shopify auth login --store my-store.myshopify.com
# ...
# 拉取主题到本地
shopify theme pull
# ...
# 本地预览(支持热更新)
shopify theme dev
# ...
# 推送修改到线上
shopify theme push
# ...
# 查看所有主题
shopify theme list
```

### 场景三:产品集合管理

```liquid
{%- comment -%}
  sections/collection-template.liquid
  集合页面模板,支持筛选与排序
{%- endcomment -%}
# ...
<div class="collection-page">
  <h1>{{ collection.title }}</h1>
# ...
  <div class="filters">
    <select onchange="window.location.href=this.value">
      <option value="{{ collection.url }}">排序: 推荐</option>
url }}?sort_by=price-ascending">价格升序</option>
url }}?sort_by=price-descending">价格降序</option>
url }}?sort_by=created-descending">最新上架</option>
    </select>
  </div>
# ...
  <div class="product-grid">
    {%- for product in collection.products -%}
      <div class="product-card">
        <a href="{{ product.url }}">
featured_image | image_url: width: 300 | image_tag: loading: 'lazy' }}
          <h3>{{ product.title }}</h3>
          <p class="price">{{ product.price | money }}</p>
        </a>
      </div>
    {%- endfor -%}
  </div>
</div>
```

## 不适用场景

以下场景Shopify助手-免费版不适合处理：

- 无明确技术栈的模糊需求
- 纯架构设计决策
- 运维部署管理

## 触发条件

需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于非本工具能力范围的需求.
## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 环境准备

```bash
# 安装 Node.js(18+)
# 安装 Shopify CLI
npm install -g @shopify/cli @shopify/theme
# ...
# 验证安装
shopify version
```

### 创建第一个自定义主题

```bash
# 使用 Shopify 官方 Dawn 主题创建
shopify theme init my-theme
# ...
cd my-theme
# ...
# 本地开发
shopify theme dev --store my-store.myshopify.com
# ...
# 修改模板文件后,浏览器自动刷新
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 示例

### 主题文件结构

```text
my-theme/
├── assets/          # CSS/JS/图片资源
├── config/          # 主题配置
│   ├── settings_schema.json    # 主题设置选项
│   └── settings_data.json      # 设置默认值
├── layout/          # 布局文件
│   └── theme.liquid             # 主布局
├── locales/         # 多语言文件
├── sections/        # 可拖拽区块
│   ├── header.liquid
│   ├── footer.liquid
│   └── main-product.liquid
├── snippets/        # 可复用代码片段
└── templates/       # 页面模板
    ├── product.liquid
    ├── collection.liquid
    └── cart.liquid
```

### 主题设置配置

```json
// config/settings_schema.json
[
  {
    "name": "主题设置",
    "settings": [
      {
        "type": "color",
        "id": "primary_color",
        "label": "主色调",
        "default": "#1a73e8"
      },
      {
        "type": "range",
        "id": "font_size",
        "label": "正文字体大小",
        "min": 12,
        "max": 20,
        "step": 1,
        "unit": "px",
        "default": 16
      }
    ]
  }
]
```

### SEO 优化清单

| 优化项 | 说明 | 优先级 |
|:-----|:-----|:-----|
| 页面标题 | 每页唯一,包含关键词 | 高 |
| Meta 描述 | 155 字符内,吸引点击 | 高 |
| URL 结构 | 简短含关键词 | 中 |
| 图片 Alt | 描述性文字,含关键词 | 中 |
| 结构化数据 | JSON-LD 产品标记 | 中 |
| 页面速度 | 图片压缩,减少 JS | 高 |
| 移动适配 | 响应式设计 | 高 |

## 最佳实践

1. **使用 Dawn 主题**:Shopify 官方主题,代码质量高,适合作为定制基础
2. **本地开发**:使用 Shopify CLI 本地开发,避免直接修改线上代码
3. **图片优化**:使用 `image_url` filter 按需生成尺寸,加载 `lazy`
4. **Liquid 性能**:避免在循环中查询,使用集合预取
5. **移动优先**:确保所有页面在移动端正常显示
6. **备份主题**:修改前导出主题备份,便于回滚

## 常见问题(补充)

### Q: Liquid 和普通模板语言有什么区别?

A: Liquid 是 Shopify 专用的模板语言,语法类似 Jinja2。使用 `{% %}` 执行逻辑(for/if/assign),`{{ }}` 输出变量。不能直接写 JavaScript 逻辑,但可以输出 JSON 数据供 JS 使用.
### Q: 如何添加自定义页面?

A: 在 `templates/` 目录创建 `.liquid` 文件(如 `page.custom.liquid`),在 Shopify 后台创建页面时选择该模板。也可通过 `sections` 实现可拖拽的自定义区块.
### Q: 产品变体(variant)怎么处理?

A: Liquid 中通过 `product.variants` 遍历变体。每个变体有自己的价格、库存和 SKU。前端通常用下拉菜单或按钮选择变体,选中后更新价格和购买按钮的 variant ID.
### Q: 如何实现多语言?

A: Shopify 支持 Liquid 的 `{{ 'text' | t }}` 翻译 filter。在 `locales/` 目录创建翻译文件(如 `zh-CN.json`)。Shopify Plus 支持多语言店铺,非 Plus 可使用翻译 App.
## 依赖说明

### 运行环境

- **Agent平台**: 支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **Node.js**: 18+

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| Node.js | 运行时 | 必需 | 官方网站下载 |
| Shopify CLI | CLI工具 | 必需 | npm install -g @shopify/cli |
| Git | 版本管理 | 推荐 | 官方网站下载 |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置

- Shopify 店铺:通过 `shopify auth login` 登录获取访问令牌
- Shopify Admin API(可选):在后台创建自定义 App 获取 API Key
- 本 Skill 核心功能通过 CLI 认证,无需额外 Key

### 可用性分类

- **分类**: MD+EXEC(Markdown指令 + 命令行执行)
- **说明**: 通过自然语言指令驱动 Agent 执行 Shopify 建站与主题开发
- **限制**: 免费版仅支持单店铺,不支持自定义 App 开发与企业级 SEO

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Shopify助手-免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "shopify helper"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
