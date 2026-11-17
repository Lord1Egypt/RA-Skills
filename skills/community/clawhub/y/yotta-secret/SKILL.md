---
name: yotta-secret
slug: yotta-secret
version: 0.2.4
displayName: 元钥·密钥泄露扫描
summary: 密钥泄露源头扫描：正则 + 熵 + 格式校验离线扫描源码、配置、git 历史，默认打码防二次泄露。
description: '元钥 —— 跨智能体的密钥 / 凭据泄露源头扫描技能：零依赖自研用「正则 + 熵 + 格式校验」离线扫描源码 / 配置 / .env / git 历史中的疑似密钥与凭据（云厂商 API Key、私钥、口令赋值、URL 内嵌凭据、高熵长 token），输出 text / JSON / CSV，默认打码防二次泄露。触发：用户要排查代码 / 配置 / 仓库里是否泄露了 API Key、密码、私钥、token，要在提交或发布前做密钥检查，或要校验某个字符串是否为已知格式的密钥时。边界：纯本地离线扫描，不联网验证密钥是否有效、不发送任何数据；结果只是「疑似密钥」，是否真实需人工核实；仅用于已获授权 / 自有资产 / 教学环境。'
tags: [密钥扫描, 凭据泄露, 源码检测, 安全扫描, secret, 泄露]
category: it-ops-security
license: MIT
homepage: https://github.com/YottaMeta/yotta-secret
---
# 元钥（yotta-secret）

跨智能体的密钥 / 凭据泄露源头扫描技能：零依赖自研用**「正则 + 熵 + 格式校验」**离线扫描
**源代码 / 配置文件 / .env / 日志 / git 历史**中的疑似密钥与凭据，覆盖
**云厂商 API Key、私钥、口令赋值、URL 内嵌凭据、高熵长 token** 五类，
输出 **text / JSON / CSV**，默认打码（--show-secret 才明文）。

纯 Python 3.8+ 标准库实现，零外部依赖；Windows + Linux + macOS 通用。
**纯本地离线**：不联网验证密钥是否有效、不发送任何数据。

## 何时使用

- 提交 / 发布前排查源码或配置里是否泄露了 API Key、密码、私钥、token；
- 扫描整个目录（递归）或 git 历史，找出硬编码凭据的源头；
- 校验某个字符串是不是已知格式的密钥（verify）；
- 在分享日志 / 工单 / 报告前把文本中的疑似密钥打码（mask，与元史脱敏同源）。

**Do NOT trigger**：
- 不联网验证密钥是否有效、不查询泄露库、不发送任何数据；
- 不主动扫描他人系统；只扫描**已存在**的本地文件与文本；
- 不自动轮换 / 吊销密钥——发现后由人工处理；
- 不在无授权情况下用于他人数据；仅用于已获授权 / 自有资产 / 教学环境。

## 快速使用

Windows 用 python，Linux/macOS 用 python3。

```bash
# 扫描目录（递归，自动跳过 .git / node_modules / 二进制）
python3 scripts/yotta_secret.py scan --path src/

# 从标准输入读取，输出 JSON
cat dump.txt | python3 scripts/yotta_secret.py scan --stdin --format json

# 只扫云厂商密钥与私钥两类
python3 scripts/yotta_secret.py scan --path . --types cloud,private_key

# 扫描 git 历史（新增行），输出 CSV
python3 scripts/yotta_secret.py scan --git --path repo/ --format csv --output report.csv

# 校验单个值是否为疑似密钥
python3 scripts/yotta_secret.py verify --value ghp_xxxxxxxxxxxxxxxx

# 把文本中的疑似密钥打码（防二次泄露）
python3 scripts/yotta_secret.py mask --path notes.txt --output safe.txt

# 计算信息熵（排查用）
python3 scripts/yotta_secret.py entropy --value abc123
```

退出码：**scan 0** = 未发现疑似密钥；**1** = 发现疑似密钥；**4** = 用法 / 读取 / git 不可用错误。
**verify 0** = 未命中规则；**1** = 命中规则；**4** = 用法错误。mask / entropy 成功均为 **0**。

## 工作流程（AI 智能体执行密钥排查时）

1. **确认范围**：明确要扫描的路径 / 文本 / git 历史，与需要关注的类别；纯本地，不做任何外部动作。
2. **扫描**：`scan --path` 指向目录 / 文件，或 `--stdin` 从管道读取；`--git` 扫历史。
3. **判定**：正则命中 → 值级校验（熵 / 格式 / 占位符过滤）→ 按严重度分级（critical / high / medium）。
4. **输出**：text / JSON / CSV 三种格式；默认打码，确需明文用 `--show-secret`。
5. **决策纪律**：结果只是「疑似密钥」，是否真实、是否泄露需人工核实；向用户如实报告并给出处理建议（轮换 / 移入密钥管理 / 清理历史）。

## 功能

- **五类检测**：cloud（AWS / Google / OpenAI / GitHub / Slack / Stripe / JWT 等云厂商与 SaaS 密钥）、
  private_key（PEM / PGP / OpenSSH / PuTTY 私钥）、credential（password / secret / token 等赋值，
  含 `MYAPP_SECRET=` 后缀式 key）、url_userinfo（URL 内嵌账号密码）、generic（高熵长 token）；
- **三重判定**：正则格式 → Shannon 熵阈值 → 值级校验（纯哈希 / UUID / 占位符 / 示例值过滤）；
- **git 历史扫描**：`--git` 走 `git log -p` 只扫新增行，逐条带 commit 与路径，找出泄露源头；
- **默认打码**：输出只保留密钥头尾（如 `ghp_****abcd`），`--show-secret` 才明文；
- **误报控制**：占位符 / 示例值 / 环境变量引用过滤、中等置信 key 需更长或更高熵、同值跨规则去重；
- **与元史联动**：mask 输出与元史 yotta-logs redact 脱敏同源（本引擎规则为超集），源头扫描 + 输出脱敏闭环；
- **与元盾联动**：scan 退出码可作为提交 / 写入前的拦截依据，JSON 结果可直接喂给元盾审计或 CI 门禁。

详细的规则目录、熵与格式校验、联动说明见 references/。

## 检测类型一览

| 类别 | 中文 | 示例 | 说明 |
|---|---|---|---|
| cloud | 云厂商 / SaaS 密钥 | `AKIA…` `ghp_…` `sk-…` `eyJ…` | AWS / Google / OpenAI / GitHub / Slack / Stripe / JWT 等 |
| private_key | 私钥 | `-----BEGIN RSA PRIVATE KEY-----` | PEM / PGP / OpenSSH / PuTTY 私钥块 |
| credential | 凭据赋值 | `DB_PASSWORD=…` `api_key=…` | 高置信 key 名 + 非占位值 |
| url_userinfo | URL 内嵌凭据 | `https://admin:hunter2@…` | URL userinfo 携带账号密码 |
| generic | 高熵长 Token | 40+ 位高熵字符串 | 无前缀但熵达标的兜底检测（medium，人工复核） |

## 输出格式

- **text**：按类别分组的可读报告（含严重度 / 文件行号 / 密钥打码 / 熵 / 上下文）；
- **json**：`{tool, version, generated, source, summary, findings[], rules[]}`，findings 每条含
  `rule_id / rule_name / category / severity / file / line / secret / entropy / length / snippet / commit`；
- **csv**：`rule_id,rule_name,category,severity,file,line,secret,entropy,length,snippet,commit,path_in_commit`。

## 边界（安全红线）

- **纯本地离线**：不联网验证密钥是否有效、不查询泄露库、不发送任何数据；
- **不给定性**：所有结果只是「疑似密钥」，是否真实需人工核实；处理建议（轮换等）由用户决定；
- **授权**：仅用于已获明确授权 / 自有资产 / 教学环境；未经授权扫描他人数据违反法律，使用者自行承担责任。

## 参考文档

- references/rules.md — 规则目录与匹配说明（五类规则 / 判定流程 / 已知取舍）
- references/entropy-and-verification.md — 熵与格式校验规范（阈值 / 占位符过滤 / 校验函数）
- references/integration.md — 与元史脱敏词库共享、与元盾联动、CI / 提交门禁使用姿势

## 常见问题（速查）

扫不到、误报、git 历史、打码与明文、退出码问题先看 references/faq.md（含速查索引与安装排障）。

## 法律声明

本技能仅用于**已获明确授权**的安全排查（自有资产、授权测试、CTF 靶场、教学环境）。
未经授权扫描他人数据违反中国《网络安全法》与《刑法》相关条款，使用者自行承担法律责任。
