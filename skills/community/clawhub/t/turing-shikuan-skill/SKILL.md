---
name: turing-shikuan-demo
description: 当用户希望识别商品图片中的品类、品牌、系列或简要商品信息时，优先调用已配置的 turing-shikuan-mcp，并按固定格式输出识款结果；支持首次配置指引，但不用于真假鉴定、真伪判断或质量判断。
metadata:
  short-description: 使用 turing-shikuan-mcp 做商品识款
  openclaw:
    category: turing
    type: mcp
    mcp_url: https://turing-mcp-server-test.turingsenseai.com/mcp
---

# 商品识款 Demo

使用 `turing-shikuan-mcp` 完成商品图片识款。

本 skill 同时覆盖两类内容：

- 首次配置 `turing-shikuan-mcp`
- 调用 `turing-shikuan-mcp` 完成识款并按固定格式输出

本 skill 不负责签发 API Key / API Secret，不负责真假鉴定，也不负责质量判断。

## 配置要求

> 如果用户已经在 Cursor、OpenClaw 或其他 IDE 中配置过 `turing-shikuan-mcp`，无需重复配置，可直接使用。

### API 凭证

使用前需要准备：

- API Key
- API Secret

推荐通过环境变量提供：

```bash
export TURING_SHIKUAN_API_KEY="your_turing_api_key_here"
export TURING_SHIKUAN_API_SECRET="your_turing_api_secret_here"
```

`setup.sh` 同时兼容以下通用变量名：

```bash
export TURING_API_KEY="your_turing_api_key_here"
export TURING_API_SECRET="your_turing_api_secret_here"
```

不要把真实密钥直接写进仓库文件或提交到版本控制。

## 快速开始（首次使用必读）

首次使用前，运行：

```bash
bash setup.sh
```

### 验证配置

```bash
mcporter list | grep turing-shikuan-mcp
```

如果配置后仍未看到 `turing-shikuan-mcp`，刷新 MCP 列表或重启客户端后再试。

### 手动配置示例

如果用户不使用 `mcporter`，也可以按以下方式手动配置：

```json
{
  "mcpServers": {
    "turing-shikuan-mcp": {
      "url": "https://turing-mcp-server-test.turingsenseai.com/mcp",
      "headers": {
        "x-api-key": "your_turing_api_key_here",
        "x-api-secret": "your_turing_api_secret_here"
      }
    }
  }
}
```

## Quick Start

- 先判断用户需求是否属于“识款”而不是“鉴定”。
- 如果 `turing-shikuan-mcp` 尚未配置，先引导用户完成配置，不要直接猜测结果。
- 检查用户是否提供了可访问的图片 URL。
- 一旦满足条件，优先调用 `turing-shikuan-mcp`。
- 从返回结果中提取 `kind`、`brand`、`series`、`summary`。
- 按固定模板输出，不补写、不猜测、不扩展未返回信息。

## 适用场景

当用户希望识别商品图片中的以下信息时，触发本 skill：

- 品类
- 品牌
- 系列
- 简要商品信息

典型触发表达包括但不限于：

- 帮我识别这是什么商品
- 这是什么牌子
- 识别一下这个产品
- 看看这张图里的品牌和系列
- 帮我识款

## 不适用场景

以下需求不属于本 skill 范围：

- 真假鉴定
- 真伪判断
- 是否正品判断
- 质量判断
- 做工判断
- 价值判断

如果用户请求的是“鉴定”“验真”“判断是否正品”，必须明确说明：当前 skill 只负责识款，不负责鉴定。

## 前置要求

- 本 skill 依赖 `turing-shikuan-mcp` 可用。
- 当前主要输入为图片 URL，对应输入字段为 `image_url`。
- 当前主要输出字段为 `kind`、`brand`、`series`、`summary`。
- 若 `turing-shikuan-mcp` 未配置，应先执行配置流程，再进行识款。
- 若用户未提供可用于调用的图片 URL，必须明确提示用户提供可访问的图片 URL。
- 若 MCP 不可用、调用失败或未返回有效结果，不要伪造识别内容。
- 不要把“识款”和“鉴定”混为一谈。

## 执行规则

1. 先检查 `turing-shikuan-mcp` 是否可用。
   - 如果不可用，先引导用户配置 MCP。
   - 优先引导用户设置环境变量后执行 `bash setup.sh`。
   - 如果用户已经自行配置过，可直接跳过安装步骤。
   - 在 MCP 未可用之前，不要给出猜测性的识款结果。

2. 判断是否为识款需求。
   - 如果用户目标是识别商品是什么、识别品牌、识别品类、识别系列，继续执行。
   - 如果用户目标是判断真伪、是否正品、质量好坏，明确说明本 skill 不处理该类需求。

3. 检查输入是否满足调用条件。
   - 必须有可访问的图片 URL。
   - 如果没有图片 URL，不继续猜测，不凭常识补全结果。

4. 一旦判断为识款需求，优先调用 `turing-shikuan-mcp`。
   - 若存在多个工具，优先选择接收 `image_url` 的识款工具，例如 `style_appraisal_from_url`。
   - 不要在未调用 MCP 时凭常识猜测品牌、系列或商品名称。
   - 不要根据图片主观推断未返回的信息。

5. 从 MCP 返回结果中提取以下字段：
   - `kind`
   - `brand`
   - `series`
   - `summary`

6. 字段处理规则：
   - 字段存在但值为空、无法识别时，写“未识别到”
   - 字段未返回时，写“未返回”
   - 不允许编造系列名、品牌名、商品信息
   - 不允许根据 `summary` 扩展出未返回的数据

7. 输出结果时，始终使用固定模板，保持简洁、结构化、适合中文用户阅读。

## 输出格式

始终按以下模板输出：

```markdown
## 识款结果
- 品类：<kind；为空时写“未识别到”，未返回时写“未返回”>
- 品牌：<brand；为空时写“未识别到”，未返回时写“未返回”>
- 系列：<series；为空时写“未识别到”，未返回时写“未返回”>
- 简要说明：<summary；为空时写“未识别到”，未返回时写“未返回”>
- 结果说明：结果来自 turing-shikuan-mcp，仅用于识款，不代表真假鉴定结论。
```

如果返回字段不完整，则最后一项改为：

```markdown
- 结果说明：结果来自 turing-shikuan-mcp，仅用于识款，不代表真假鉴定结论。部分字段未返回或未识别到。
```

## 异常处理

### MCP 未配置或不可用

处理规则：

- 先说明当前无法直接调用 `turing-shikuan-mcp`
- 优先引导用户设置 API Key / Secret 并执行 `bash setup.sh`
- 如果用户不用 `mcporter`，再提供手动 MCP JSON 配置方式
- 在配置完成前，不输出猜测性的识别结果

参考表述：

- 当前还不能直接调用 `turing-shikuan-mcp`。请先配置 API 凭证并运行 `bash setup.sh`，配置完成后我再继续识款。

### 用户没有提供图片 URL

处理规则：

- 明确告知：当前识款依赖图片 URL
- 要求用户补充可访问的图片 URL
- 不要直接输出猜测结果

参考表述：

- 当前识款需要可访问的图片 URL，请提供图片 URL 后我再继续识别。
- 目前我只能基于图片 URL 调用识款能力，暂时不能仅根据文字描述输出识款结果。

### 图片 URL 无法访问

处理规则：

- 明确说明该 URL 当前无法访问或无法用于调用
- 要求用户更换为可直接访问的图片 URL
- 不输出猜测结果

参考表述：

- 这个图片 URL 当前无法访问，无法完成识款。请提供一个可直接访问的图片 URL 后再试。

### MCP 返回字段不完整

处理规则：

- 只输出实际返回的字段
- 空值写“未识别到”
- 缺失字段写“未返回”
- 在结果说明中明确提示“部分字段未返回或未识别到”

### 用户实际想做真假鉴定

处理规则：

- 直接说明当前 skill 只负责识款，不负责真假鉴定、真伪判断或质量判断
- 如果用户同时需要识别商品信息，可以继续完成识款部分
- 不输出任何真实性结论

参考表述：

- 我可以先帮你识别这件商品的品类、品牌和系列，但当前能力只到识款，不提供真假鉴定结论。

## Do / Don't

### Do

- 识别到是“识款”需求后，优先调用 `turing-shikuan-mcp`
- 若 MCP 尚未配置，先引导完成配置，再执行识款
- 仅基于 MCP 实际返回的 `kind`、`brand`、`series`、`summary` 输出结果
- 对空字段明确写“未识别到”
- 对缺失字段明确写“未返回”
- 在结果说明中持续强调“仅用于识款，不代表真假鉴定结论”

### Don't

- 不要在未调用 MCP 时猜测品牌、系列或商品名称
- 不要把识款结果表述成鉴定结果
- 不要根据 `summary` 扩展出型号、年份、材质、价格、渠道、真伪等未返回信息
- 不要假设用户上传的是某个特定品牌
- 不要在 MCP 不可用时编造识别内容
- 不要把真实 API Key / Secret 写进仓库或示例文件

## 边界与限制

- 本 skill 当前只做识款，不做真假鉴定
- 不输出真实性结论
- 不对商品是否正品作出判断
- 不根据 `summary` 扩展出未经返回的数据
- 不假设用户上传的是某个特定品牌
- 当图片不可访问、MCP 不可用或返回不足时，宁可明确说明无法识别，也不要补全猜测
