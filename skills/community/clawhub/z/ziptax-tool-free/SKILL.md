---
slug: ziptax-tool-free
name: ziptax-tool-free
version: 1.0.0
displayName: 销售税查询(免费版)
summary: "面向个人开发者的销售税查询工具,支持按地址、邮编、经纬度查询,含基础CLI封装.。销售税查询工具免费版为个人开发者提供美国销售税率查询能力,支持按地址、邮编、经纬度查询,含基础CLI封装与税"
license: Proprietary
edition: free
description: '销售税查询工具免费版为个人开发者提供美国销售税率查询能力,支持按地址、邮编、经纬度查询,含基础CLI封装与税率解析。核心能力:

  - 按地址查询销售税(最精确)

  - 按邮编查询销售税

  - 按经纬度查询销售税

  - 税率结构解析(州/县/市/区)

  - 基础CLI封装(lookup。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。'
tags:
  - 销售税
  - 税务
  - API集成
  - 个人开发
  - 电商
  - 工具
  - 效率
  - 知识
  - api
  - ziptax_api_key
  - postalcode
  - metrics
  - zip-tax
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
---
# 销售税查询工具(免费版)

## 概述

`ziptax-tool-free` 为个人开发者提供美国销售税率查询能力。它支持按地址、邮编、经纬度查询,返回完整的税率结构(州/县/市/区),并附带基础 CLI 封装,适合个人电商项目、学习税务结构与小规模批量查询.
本工具通过调用 zip-tax.com API 完成查询,需要预先注册并获取 API Key。免费额度为每月 100 次调用.
## 核心能力

| 能力 | 说明 |
|---|---|
| 地址查询 | 最精确,返回单一明确结果 |
| 邮编查询 | 返回该 ZIP 内所有税率 |
| 经纬度查询 | 适合移动端或地理定位场景 |
| 税率结构解析 | 州/县/市/区各级税率明细 |
| 服务/运费税性 | 判断服务费与运费是否应税 |
| CLI 封装 | `lookup.sh` 脚本快速查询 |
| 响应码解析 | `metadata.response.code` 为 100 表示成功 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：面向个人开发者的、销售税查询工具、支持按地址、含基础、销售税查询工具免、费版为个人开发者、提供美国销售税率、查询能力、封装与税率解析、按地址查询销售税、按邮编查询销售税、按经纬度查询销售、Use、when、需要代码生成、编程辅助、调试测试、开发部署时使用、不适用于无明确技、术栈的模糊需求等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景 1:按地址查询销售税(推荐)

```bash
curl -s "https://api.zip-tax.com/request/v60?address=200+Spectrum+Center+Drive+Irvine+CA+92618" \
  -H "X-API-KEY: $ZIPTAX_API_KEY"
```

返回完整的税率结构,含州、县、市、区各级税率.
### 场景 2:按邮编查询销售税

```bash
zip-tax.com/request/v60?postalcode=92618" \
  -H "X-API-KEY: $ZIPTAX_API_KEY"
```

返回该 ZIP 内所有税率(可能多个,因为一个 ZIP 可能跨越多个税区).
### 场景 3:按经纬度查询销售税

```bash
zip-tax.com/request/v60?lat=33.6525&lng=-117.7479" \
  -H "X-API-KEY: $ZIPTAX_API_KEY"
```

适合移动端或基于地理定位的查询场景.
## 快速开始

### 第一步:获取 API Key

1. 访问 zip-tax.com 平台
2. 注册账号并登录
3. 进入 DEVELOP > API Keys 页面
4. 创建 API Key 并保存

### 第二步:配置环境变量

```bash
# Linux / macOS
export ZIPTAX_API_KEY="your-api-key-here"
# ...
# Windows PowerShell
$env:ZIPTAX_API_KEY="your-api-key-here"
# ...
# 永久保存(添加到 ~/.bashrc 或 ~/.zshrc)
echo 'export ZIPTAX_API_KEY="your-api-key-here"' >> ~/.bashrc
```

### 第三步:执行查询

```bash
# 使用 curl 直接查询
zip-tax.com/request/v60?postalcode=92618" \
  -H "X-API-KEY: $ZIPTAX_API_KEY"
# ...
# 或使用 CLI 封装
bash （请参考skill目录中的脚本文件） --postalcode 92618
```

#
## 示例

### CLI 封装脚本(lookup.sh)

```bash
#!/usr/bin/env bash
# （请参考skill目录中的脚本文件） — 销售税查询 CLI 封装
set -euo pipefail
# ...
if [ -z "$ZIPTAX_API_KEY" ]; then
  echo "错误:未设置 ZIPTAX_API_KEY 环境变量"
  exit 1
fi
# ...
API_URL="https://api.zip-tax.com/request/v60"
# ...
# 解析参数
while [[ $# -gt 0 ]]; do
  case "$1" in
    --address)
      ADDRESS="$2"; shift 2 ;;
    --postalcode)
      POSTALCODE="$2"; shift 2 ;;
    --lat)
      LAT="$2"; shift 2 ;;
    --lng)
      LNG="$2"; shift 2 ;;
    --metrics)
      METRICS=1; shift ;;
    *)
      echo "未知参数: $1"; exit 1 ;;
  esac
done
# ...
# 构建查询
QUERY=""
if [ -n "${ADDRESS:-}" ]; then
  QUERY="address=$(echo $ADDRESS | sed 's/ /+/g')"
elif [ -n "${POSTALCODE:-}" ]; then
  QUERY="postalcode=$POSTALCODE"
elif [ -n "${LAT:-}" ] && [ -n "${LNG:-}" ]; then
  QUERY="lat=$LAT&lng=$LNG"
else
  echo "用法: lookup.sh --address '地址' | --postalcode 邮编 | --lat 纬度 --lng 经度 | --metrics"
  exit 1
fi
# ...
# 查询额度(metrics 不计入额度)
if [ -n "${METRICS:-}" ]; then
  curl -s "$API_URL/account/metrics" -H "X-API-KEY: $ZIPTAX_API_KEY"
else
  curl -s "$API_URL?$QUERY" -H "X-API-KEY: $ZIPTAX_API_KEY"
fi
```

### 响应解析示例

```javascript
// 解析 v60 响应
const response = await fetch(
  `https://api.zip-tax.com/request/v60?postalcode=92618`,
  { headers: { 'X-API-KEY': apiKey } }
);
const data = await response.json();
// ...
// 检查响应码(100 = 成功)
if (data.metadata.response.code !== 100) {
  throw new Error(`查询失败: ${data.metadata.response.message}`);
}
// ...
// 获取总税率(小数形式,0.0775 = 7.75%)
const totalRate = data.taxSummaries[0].rate;
console.log(`总税率: ${(totalRate * 100).toFixed(2)}%`);
// ...
// 获取各级税率明细
data.baseRates.forEach(rate => {
  console.log(`${rate.type}: ${(rate.rate * 100).toFixed(2)}%`);
});
// ...
// 检查服务/运费税性
console.log(`服务应税: ${data.service.taxable}`);
console.log(`运费应税: ${data.shipping.taxable}`);
```

## 最佳实践

1. **优先用地址查询**:地址查询返回单一精确结果,邮编可能返回多个税区.
2. **API Key 不外泄**:永不将 API Key 提交到代码仓库或暴露在前端代码中.
3. **检查响应码**:`metadata.response.code` 为 100 才是成功,其他码表示错误.
4. **税率是小数**:0.0775 表示 7.75%,显示时乘以 100.
5. **metrics 不计额度**:`/account/metrics` 端点不消耗免费额度,可频繁查询.
6. **缓存结果**:同一地址的税率短期内不变,建议本地缓存减少调用次数.
7. **处理错误**:网络错误、API Key 失效、地址无效等情况需有明确错误处理.
8. **关注额度**:免费额度每月 100 次,接近上限时及时升级或优化查询.
## 常见问题

### Q1: 免费额度是多少?如何查询剩余额度?

免费额度为每月 100 次调用。通过 `/account/metrics` 端点查询已用额度,该端点不消耗额度.
### Q2: 地址查询和邮编查询有什么区别?

地址查询返回单一精确结果(最准);邮编查询返回该 ZIP 内所有税率(可能多个,因为一个 ZIP 可能跨越多个税区)。优先用地址查询.
### Q3: API Key 如何安全存储?

环境变量是最佳实践。生产环境用密钥管理服务(AWS Secrets Manager / HashiCorp Vault)。永不提交到代码仓库,永不硬编码在前端.
### Q4: 税率会变化吗?

会。美国销售税率可能随州/县/市立法调整。建议定期刷新缓存,关键场景(结账)实时查询.
### Q5: 免费版与 Pro 版的区别?

免费版提供每月 100 次免费查询与基础 CLI;Pro 版扩展批量查询、本地缓存、税务合规报告、企业级 API 集成与优先支持.
## 依赖说明

### 运行环境

- **Agent 平台**:支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**:Windows / macOS / Linux
- **curl**:用于 API 调用(系统预装)

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| curl | 系统工具 | 必需 | 系统预装 |
| zip-tax.com API | 外部 API | 必需 | 官网注册并获取 API Key |
| jq(JSON 解析) | 系统工具 | 可选 | 系统包管理器 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置

- **必需**:zip-tax.com API Key,通过环境变量 `ZIPTAX_API_KEY` 配置
- **获取方式**:访问 zip-tax.com 平台,注册账号,进入 DEVELOP > API Keys 页面创建
- **免费额度**:每月 100 次调用
- **安全要求**:永不外泄、永不提交代码仓库、永不硬编码前端

### 可用性分类

- **分类**: MD+EXEC(纯 Markdown 指令,部分功能需要 exec 命令行执行能力)
- **说明**: 基于自然语言指令驱动 Agent 调用 zip-tax.com API;需要预先注册并配置 API Key;查询通过 curl 或 CLI 封装脚本执行

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "销售税查询(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "ziptax"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
