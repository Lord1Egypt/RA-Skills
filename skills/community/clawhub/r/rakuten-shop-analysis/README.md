# Rakuten Shop Analysis Skill

这是一个给 OpenClaw 用的乐天店铺分析 skill。

它可以接收：

- 乐天店铺链接
- 乐天店铺 `shopCode`

然后输出一份结构化分析结果，适合做店铺分析、竞品研究、爆款样本查看和报告生成。

## 安装

OpenClaw 里直接安装这个 GitHub 仓库：

```text
https://github.com/abca12a/rakuten-shop-analysis-skill
```

安装后可直接匿名试用。
直接贴乐天店铺链接给 OpenClaw 就可以用。

## 网络与隐私说明

- 这个 skill 会把你输入的乐天店铺链接或 `shopCode` 发送到托管分析服务
- 当前托管后端域名：`https://rakuten.845817074.xyz`
- 当前版本不需要 token，直接匿名试用即可
- 如果你不接受把店铺标识发送到托管服务，请不要使用这个 skill

## 如何使用

安装完成后，直接对 OpenClaw 说这类话即可：

```text
分析这个乐天店铺：https://www.rakuten.co.jp/vacchetta-topkapi/
```

```text
帮我出一份这个乐天店铺的分析报告：https://www.rakuten.co.jp/vacchetta-topkapi/
```

也可以直接给 `shopCode`：

```text
分析这个乐天店铺：vacchetta-topkapi
```

## 匿名试用额度

当前匿名试用通道已开启。

- 当前限额：每个 IP 每 60 秒最多 30 次 API 请求
- 不需要先配置任何 token 就能直接试用
- 如果出现限流，等待约 1 分钟后再试即可
- 当前版本不开放 token 配置入口

## 说明

这个仓库只包含 skill 本体。分析能力由托管后端提供，skill 本身只负责把店铺输入发送到后端并返回结构化结果。

## 文件结构

```bash
SKILL.md
agents/openai.yaml
scripts/run.mjs
scripts/format-output.mjs
tests/run.test.mjs
```

## 本地验证

```bash
npm test
node scripts/run.mjs vacchetta-topkapi
```

## 分发建议

- 对外直接给这个 GitHub 地址即可
- `Display name` 建议用 `Rakuten Shop Analysis`
