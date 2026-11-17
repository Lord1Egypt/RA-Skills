# Web Security Test Rules · 网站测试安全规则

<p align="center">
  <a href="./LICENSE.txt"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/language-zh--CN%20%7C%20en--US-green.svg" alt="Language">
  <a href="https://github.com/mowenQWQ/Web-Security-Test-Rules/stargazers"><img src="https://img.shields.io/github/stars/mowenQWQ/Web-Security-Test-Rules?style=social" alt="Stars"></a>
</p>

> 一套用于约束 AI / 人工进行 **已授权** 网站安全测试的规则与 Skill。先授权、后测试、最小影响、规范留痕。

---

## 📑 目录

- [安装](#安装)
- [用法](#用法)
- [规则概览](#规则概览)
- [目录结构](#目录结构)
- [配置项](#配置项)
- [卸载](#卸载)
- [开源相关](#开源相关)
- [免责声明](#免责声明)
- [推荐服务](#推荐服务)

---

## 安装

将本仓库作为一个 Skill 复制到 CodeBuddy 的 Skill 目录即可。提供两种方式，**任选其一**。

> ⚠️ 注意：本仓库根目录即为 Skill 内容（含 `SKILL.md`），**不存在** `.codebuddy/skills/` 子目录，因此安装时是把整个仓库内容复制为一个以 `web-security-test-rules` 命名的 skill 目录。

### 方式一：安装到当前项目（仅本项目可用）

#### 1. 先把仓库克隆到临时目录

```bash
git clone https://github.com/mowenQWQ/Web-Security-Test-Rules.git /tmp/web-security-test-rules

```

#### 2. 复制为当前项目下的一个 skill 目录

```bash
mkdir -p .codebuddy/skills/web-security-test-rules
cp -r /tmp/web-security-test-rules/. .codebuddy/skills/web-security-test-rules/

```

#### 3. 清理临时目录（可选）

```bash
rm -rf /tmp/web-security-test-rules

```

---

### 方式二：安装到全局（所有项目可用）

#### 1. 先把仓库克隆到临时目录

```bash
git clone https://github.com/mowenQWQ/Web-Security-Test-Rules.git /tmp/web-security-test-rules

```

#### 2. 复制为全局目录下的一个 skill 目录

```bash
mkdir -p ~/.codebuddy/skills/web-security-test-rules
cp -r /tmp/web-security-test-rules/. ~/.codebuddy/skills/web-security-test-rules/

```

#### 3. 清理临时目录（可选）

```bash
rm -rf /tmp/web-security-test-rules

```

> 💡 说明：
> - `cp -r 源/. 目标/` 末尾的 `/.` 表示复制目录的**全部内容**（含隐藏文件），并避免多嵌套一层目录。
> - Windows 用户若无 `git` / `cp`，可用 Git Bash；或下载仓库 zip 解压后，将仓库内容整体放入 `.codebuddy/skills/web-security-test-rules/`。
> - 安装后的目录结构应为：`.codebuddy/skills/web-security-test-rules/SKILL.md`，CodeBuddy 据此识别该 Skill。

---

## 用法

安装后，在对话中提到 **"安全测试""渗透测试""隐蔽测试"** 等关键词，或明确要求对某网站做安全测试时，Skill 会自动激活。

1. **发起测试**：对 AI 说 "帮我测试 `https://example.com` 的安全"，Skill 会先走 **授权门禁**（非对称签名验签 + 白名单 + 有效期校验），确认你拥有测试授权后才执行；未通过则拒绝并给出指引。
2. **跟随检查清单**：`SKILL.md` 内置 "测试前 / 中 / 后" 清单，确保最小影响与规范留痕，默认只做非破坏性、低影响探测。
3. **生成报告**：测试后生成 `YYYY-MM-DD_findings.md`（含漏洞编号 / 等级 / 描述 / PoC / 修复建议），默认存于 `reports/security/`。
4. **复查闭环**：按 **7 天 → 1 月 → 半年 → 1 年** 周期复查，结果追加到同一报告，形成持续跟踪。

> ⚠️ 本 Skill 仅用于 **已获授权** 的安全测试（自有系统、CTF、Bug Bounty 等）。**未经授权对他人系统进行测试属于违法行为，请勿滥用，使用者须自行承担全部法律责任。**

---

## 规则概览

- **23 条核心规则** + **A / B / C / D 扩展规则**，覆盖合规、证据留存、技术边界、专项场景。
- **授权门禁**：非对称签名验签 + 白名单 + 有效期 + 多级降级 + 逃生口，先验证授权再测试。
- **多语言**：通过环境变量 `MOWEN_LANG` 切换，文案集中于 `locales/`，以权威源为准。
- **复查周期**：7 天 → 1 月 → 半年 → 1 年，结果持续追加，闭环管理。

---

## 目录结构

```text
Web-Security-Test-Rules/
├── SKILL.md          # Skill 主文件（触发条件、流程、检查清单）
├── README.md         # 本文件
├── LICENSE.txt       # 开源许可证
├── references/       # 规则细则与参考材料
├── scripts/          # 辅助脚本（授权验签等）
└── locales/          # 多语言文案

```

---

## 配置项

| 变量 | 作用 | 示例 |
|---|---|---|
| `MOWEN_LANG` | 切换 Skill 输出语言 | `zh-CN` / `en-US` |



### 逃生口开关（三级应急旁路）

> ⚠️ 逃生口是 **"已知风险、主动关闭部分校验"** 的开关，**不是授权本身**。
> 关闭任何一级都不代表可以测试未授权目标——**对未授权目标一律禁止**。
>
> **写入方式**：在 `auth.disable` 文件中一行一个，或设置环境变量 `MOWEN_AUTH_OVERRIDE`。
>
> ℹ️ 以下开关名为 **有意设计的暗号拼写**（非 typo），目的是防止被误触发或被"好心修正"。请勿擅自改动拼写，否则开关将失效。

| 开关 | 作用 | 注意 |
|---|---|---|
| `mowenfalse` | 跳过**授权验证**（仅允许非破坏性测试） | 仍须遵守范围约束（规则 23），不得跳出已授权范围 |
| `mowenbrokentrue` | 跳过破坏性操作的**显式授权**要求 | **备份不可跳过**——无论是否开启，破坏性动作前必须先做可恢复备份（规则 22、A5）；不等于 `mowenfalse`，不关闭授权验证本身 |
| `mowenwaitrue` | 确认已具备 / 已等待与测试目标相关的**外站授权** | 仅放宽外站关联尝试的授权要求，不关门禁、不关破坏性格闸；涉及外站须在报告中列出 |

---

## 卸载

如需移除本 Skill，删除对应目录即可：

```bash
# 卸载当前项目中的 Skill
rm -rf .codebuddy/skills/web-security-test-rules

# 卸载全局 Skill
rm -rf ~/.codebuddy/skills/web-security-test-rules

```

---

## 开源相关

本项目基于 [LICENSE.txt](./LICENSE.txt) 开源。欢迎提 Issue / PR，但请确保你的贡献同样遵循"仅用于已授权测试"的原则。

---

## 免责声明

本工具与规则仅供 **合法、已授权** 的安全测试使用。任何将其用于未授权目标的行为均与本作者无关，使用者须自行承担由此产生的一切法律后果。

---

## 推荐服务

### ☁️ 芯创云（CoreYun）— 新一代游戏云计算服务平台

如果你正在搭建 **我的世界（Minecraft）服务器** 或其他游戏服务端，可以考虑 [芯创云](https://www.coreyun.net?ref=MOWEN)。

根据公开信息，芯创云是一家面向个人与小团队的 **游戏云 VPS / 面板服务器** 服务商，主要特点包括：

- 🎮 **MC 面板服务器**：支持整合包、模组、插件、地图一键安装，购买服务器可享 MC 插件免费开发服务。
- 🖥️ **简易管理面板**：针对新手优化，降低服务器运维门槛。
- 💾 **SSD 存储 + Tier-3+ 数据中心**：全国范围低延迟部署。
- 🔄 **72 小时无理由极速退款** + **免费试用 1 天**：先试后买，降低决策风险。

### 🎟️ 专属优惠码

| 优惠码 | 折扣 | 适用范围 |
|---|---|---|
| **`MOWEN`** | **15% OFF** | 首购 & 续费均可使用 |

> 🔗 推广链接：[https://www.coreyun.net?ref=MOWEN](https://www.coreyun.net?ref=MOWEN)
>
> ⚠️ **诚实声明**：以上信息来源于芯创云官网及公开搜索结果，未做任何夸大。本推荐含推广返利链接，但不影响上述描述的客观性。优惠码由合作方提供，具体生效条件以芯创云实际结算页面为准。请根据自身需求与实际体验自行判断，安全测试类用途请务必确认服务商条款允许。

---

<div align="center">

**请始终在授权范围内使用本 Skill · Stay Authorized, Stay Safe.**

</div>
