---
name: rakuten-shop-analysis
description: 用于分析 Rakuten 乐天店铺。用户提供店铺链接或 shopCode 时使用，适合竞品研究、店铺结构分析和快速出报告。
metadata:
  openclaw:
    requires:
      bins: ["node"]
---

# Rakuten Shop Analysis

分析 Rakuten 乐天店铺，并返回结构化结果。

适合用于：

- 店铺分析
- 竞品研究
- 爆款样本查看
- 快速出分析报告

支持输入：

- 乐天店铺链接
- 乐天 `shopCode`

## 网络与隐私说明

- 这个 skill 会把你提供的店铺链接或 `shopCode` 发送到托管后端进行分析
- 当前托管后端域名：`https://rakuten.845817074.xyz`
- 当前版本不需要 token，走匿名试用模式
- 除了你输入的店铺标识和分析请求本身，不要求额外账号凭证

## 如何使用

安装后，直接对 OpenClaw 说：

```text
分析这个乐天店铺：https://www.rakuten.co.jp/vacchetta-topkapi/
```

或者：

```text
帮我出一份这个乐天店铺的分析报告：https://www.rakuten.co.jp/vacchetta-topkapi/
```

也可以直接输入 `shopCode`：

```text
分析这个乐天店铺：vacchetta-topkapi
```

## 当前说明

- 安装后可直接匿名试用
- 当前匿名限额：每个 IP 每 60 秒最多 30 次 API 请求
- 如果限流，等待约 1 分钟后再试即可
- 当前版本不需要配置 token，也不需要配置后端地址

## 结果返回规则

- 正常情况下，应等待 skill 执行完成后，再一次性返回最终分析结果
- 如果本次调用没有拿到最终结果，不要声称会在后台持续监控、稍后自动回复或继续异步跟进
- 遇到未完成、超时或宿主中断时，应明确告诉用户本次调用未完成，并请用户稍后重试

## 执行约束

- 必须使用 skill 自带执行入口，不要临时改用别的实现
- 不要向用户展示内部 API 地址、接口路径、查询参数或调试细节
- 不要向用户承诺“我会继续监控并稍后主动返回结果”这类后台跟进能力
- 不要 `write_file` 生成临时 JS/Python/Bash 抓取脚本
- 不要自行用 `axios`、`fetch`、`https.request`、`cheerio`、浏览器抓取等方式直接抓 Rakuten 页面
- 不要绕过 skill，自行拼接不存在的 API 主机、路径或参数
- 目标是调用托管分析服务并返回结果，而不是现场重写一个新的 Rakuten 抓取器
