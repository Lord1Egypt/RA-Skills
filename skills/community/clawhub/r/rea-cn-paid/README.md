# REA 逆向工程审计包·国产适配（付费版）· `rea-cn-paid`

> 把 170 个 MCP 逆向分析工具适配到中文 LLM 环境。
> 用于原生 / 托管 / Electron·JS / 打包产物 / 固件 / 浏览器目标的研究学习、安全审计与版本比对。
> **按调用量计费 ¥1.9 / 次，单次付费 24 小时内不限次使用。**

权利人：天津市微数人工智能科技有限责任公司　·　版本：**1.2.3**

---

## 0. 先读这个

> **本技能仅用于研究学习与安全审计**（自有软件健壮性审计、遗留产物可维护性评估、版本差异比对等）。
> **不可用于破解、绕过技术保护措施、未经授权的逆向或任何违反法律法规的用途。**
> 完整声明见 [`DISCLAIMER.md`](./DISCLAIMER.md)。

**不适用于**：普通源码仓库的常规架构分析（这类需求直接用代码阅读工具即可）。

---

## 1. 它解决什么问题

上游引擎 `rea-agents@6.4.0` 暴露 170 个 MCP 工具（桥接 Ghidra / Hopper / IDA / JADX / JEB / adb / apktool / Binwalk / Unblob），
但**工具名与返回全是英文**，中文大模型驱动时会出现三类失败：工具名被翻译、报错看不懂、国产模型不兼容。

本包是**国产适配层**，不是引擎本身：

| 能力 | 说明 |
|---|---|
| 170 工具英汉对照 | `references/glossary-zh-en.md`，强制逐字英文调用（见工具调用契约） |
| 工具调用契约 | `references/tool-invocation-contract.md` —— 杜绝"工具名被翻成中文"这一 99% 的失败源 |
| 中文错误释义 | `references/error-reference.md` |
| 国内安装通道 | npmmirror / 国内镜像优先，含 `--engine` 兜底装引擎 |
| 国产大模型清单 | `references/domestic-models.md`（要求模型支持 function/tool calling） |
| 义务账本 | `references/obligation-ledger.md` —— 强制区分"已搞明白 / 仍未搞明白" |

---

## 2. 使用流程（三步）

```bash
# ① 发起付费：拿 402 + 免费 preview + paymentCode
node scripts/pay-gate.mjs

#   → 把响应里的 WeixinPay-Required 交给 weixinpay_pay 插件，向用户申请 ¥1.9 支付
#   → 向用户展示免费 preview（合规，不构成绕过付费）

# ② 支付成功后履约：下载引擎 → SHA256 校验 → 解压 → 登记权益凭证
node scripts/pay-gate.mjs --resume <outTradeNo>

# ③ 启动 MCP 引擎（工具名必须逐字英文）
node scripts/run-mcp.mjs
```

**24 小时内**再次使用免验证直接启动；**超过 24 小时** `run-mcp.mjs` 会 exit 65，需重新付费。

退出码：`0` 成功 · `42` 需支付 · `43` 未支付 · `44` 未解锁 · `45` 已过期需续费 · `65` 启动被拒（无有效凭证）

---

## 3. 付费与防绕过（v1.2.0）

付费闸**写在包里**，与下载渠道无关——从 SkillHub、GitHub、ClawHub 任一渠道拿到本包，使用流程完全一致，都会走到同一笔 ¥1.9 付费。

| 机制 | 说明 |
|---|---|
| 强制校验 | `run-mcp.mjs` 启动前校验 `engine/.entitlement.json`，无有效凭证 exit 65（写死、无开关） |
| **Ed25519 签名** | 凭证由服务端私钥对「产品ID + 订单号 + 到期时间」三要素签名；包内 `scripts/lib/entitlement-key.mjs` **只含公钥** → 本地凭证**可验不可伪造**。手写凭证 / 改到期时间 / 跨产品复用订单号，一律验签失败（`FORGED`） |
| 服务端 24h 时效 | 网关对超 24 小时订单返回 `410 ORDER_EXPIRED`，已退款订单 `410 REFUNDED`；旧订单号无法续期 |
| 网关地址 | `https://www.ontoagent.net/rea402`（X402 网关；与 ontoAI 质检官 Plus 同商户体系） |

**已知边界（诚实说明）**：明文 `.mjs` 脚本仍可被有技术能力者改掉校验逻辑；且上游引擎本就是 npm 公开的 MIT 包。
我们出售的是**国产适配层 + 文档 + 服务**，不是引擎字节。

---

## 4. 授权（重要：两部分不同授权）

| 组成部分 | 授权 |
|---|---|
| `engine/`（上游 `rea-agents@6.4.0`） | **MIT**，原作者 morluto，见 [`engine-LICENSE-MIT.md`](./engine-LICENSE-MIT.md) |
| 适配层（`SKILL.md` / `config/` / `scripts/` / `references/` / 文档） | **权利人自有商业授权**，见 [`LICENSE.md`](./LICENSE.md) —— 付费使用、禁止再分发、禁止绕过付费闸 |

---

## 5. 目录

```
SKILL.md / SKILL.en.md      技能主文档（frontmatter 含 slug / 版本 / 定价）
DISCLAIMER.md               免责声明
LICENSE.md                  自有授权（适配层）
engine-LICENSE-MIT.md           上游引擎 MIT 授权
CHANGELOG.md                变更记录
README.md                   本文件
config/cn-config.json       网关地址 / 价格 / 24h 时效 / 引擎 SHA256
scripts/pay-gate.mjs        付费闸（唯一入口）
scripts/run-mcp.mjs         MCP 启动入口（强制校验凭证）
scripts/cn-installer.mjs    依赖引导器（npmmirror）
scripts/lib/                共享模块（含 entitlement 验签公钥）
references/                 9 份中文适配文档
engine-b64/                 引擎 base64 文本分片（自包含版；付费后本地拼回）
tool-manifest.json          170 工具清单
```

---

## 6. 渠道

| 渠道 | Slug / 仓库 | 说明 |
|---|---|---|
| SkillHub | `rea-cn-paid` | 官方付费技能市场 |
| ClawHub | `@ontoai/rea-cn-paid` | 技能包市场 |
| GitHub | `ontoAI-weishu/rea-cn-paid` | 本仓库 |

三处包名、简介、定价一致；付费闸在包内，任何渠道下载的使用流程相同。
