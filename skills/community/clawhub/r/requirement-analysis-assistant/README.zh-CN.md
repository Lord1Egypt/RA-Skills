# 需求分析助手 Skill

[English README](README.md)

这是一个兼容 Codex 和 OpenClaw 的 Agent Skill，用于把业务方的一句话需求、模糊想法、截图、草图、竞品页面或已有 PRD，拆解成结构化的产品需求文档、原型结构、HTML Demo、视觉需求分析、功能规则、异常 case、优先级建议和验收标准。

它适合产品经理、发行团队、游戏运营、增长投放团队、设计、测试、业务方和项目协作团队使用。目标不是替代产品判断，而是把“从零写需求、搭框架、补规则、查漏补缺、快速做低保真 Demo”的重复工作交给 AI，让产品经理把时间放在业务取舍、方案判断和跨团队推动上。

## 能解决什么问题

- 业务方只会描述大概方向，产品还要重新梳理需求背景、用户场景和功能范围。
- PRD 结构不统一，不同产品写法差异大，研发和测试经常反复追问。
- 官网活动、储值中心、买量落地页、SDK、后台配置等发行场景有大量重复拆解工作。
- 异常 case、后台配置项、埋点需求、验收标准容易遗漏。
- 需求评审前缺少自动质检和补充建议。
- 业务方给一张截图、草图或竞品页面时，产品需要手动还原功能逻辑。
- 早期需求沟通缺少可视化 Demo，业务、产品、研发难以快速对齐。

## 核心能力

- 将简易需求方向生成标准 PRD 初稿。
- 根据缺失信息自动提出澄清问题。
- 输出用户场景、功能明细、交互规则和异常 case。
- 生成基础原型结构，包括页面清单、模块层级、跳转关系和后台字段。
- 根据一句话需求生成低保真 HTML 页面 Demo。
- 分析业务截图、草图、竞品页面或后台截图，输出可见事实、推断需求和待确认问题。
- 适配发行日常场景，包括官网活动、储值中心、买量投放、SDK、后台配置。
- 对已有需求文档进行质检，指出缺失规则、风险点和待确认问题。

## 适用场景

### 官网活动

例如预约活动、礼包领取、抽奖、分享拉新、活动页搭建、奖励配置和活动数据统计。

### 储值中心

例如充值档位、支付方式、首充奖励、累充返利、订单状态、支付回调、补单和对账。

### 买量投放

例如落地页、渠道参数、素材链接、转化追踪、归因回传、A/B 测试和数据看板。

### SDK

例如登录、支付、实名认证、用户协议、错误码、回调规则、版本兼容和接入文档。

### 后台配置

例如活动配置、奖励配置、权限控制、审核发布、操作日志、数据查询和回滚机制。

### 视觉需求分析

例如业务提供活动页截图、手绘草图、竞品页面、Figma 截图、后台配置截图，AI 分析页面模块、功能点、操作路径、后台配置、埋点和异常 case。

### HTML Demo

例如业务一句话描述“做一个官网预约活动页”，AI 可以生成低保真 HTML Demo，用于早期评审和对齐，不替代正式视觉设计。

## 仓库结构

```text
.
+-- SKILL.md
+-- README.md
+-- README.zh-CN.md
+-- LICENSE.txt
+-- agents/
|   +-- openai.yaml
+-- references/
    +-- prd-template.md
    +-- publishing-scenarios.md
    +-- quality-checklist.md
    +-- visual-prototype.md
```

## 安装到 Codex

使用 Skill Installer 安装：

```text
$skill-installer install https://github.com/<owner>/<repo>
```

也可以手动复制到：

```text
$CODEX_HOME/skills/requirement-analysis-assistant
```

安装后重启 Codex，让系统重新发现 Skill。

## 安装到 OpenClaw

如果你的 OpenClaw 版本支持 Git 安装，可以使用：

```bash
openclaw skills install git:<owner>/<repo>@main
```

也可以手动复制到 OpenClaw 的 skill 目录，例如：

```text
~/.openclaw/skills/requirement-analysis-assistant
<workspace>/skills/requirement-analysis-assistant
```

然后检查 Skill：

```bash
openclaw skills list
openclaw skills check
```

## 推荐安装工具

最低配置只需要 Codex 或 OpenClaw 能读取 `SKILL.md` 和 `references/`。如果要做完整数字员工，建议搭配：

- 文件读写工具：保存 PRD、HTML Demo 和分析报告。
- 浏览器或 Playwright：预览生成的 HTML Demo。
- Figma 或设计工具：把原型结构进一步转成设计稿。
- 图片理解能力：分析截图、草图和竞品页面。
- 知识库检索：接入组织认可的 PRD 模板、历史案例和业务术语。

## 使用示例

```text
使用 $requirement-analysis-assistant 帮我把这个想法拆成 PRD：
我们想做一个官网预约活动，用户预约后可以在上线后领取礼包，运营需要在后台配置活动时间和奖励。
```

```text
使用 $requirement-analysis-assistant 根据这个需求方向生成一个 HTML Demo：
做一个官网预约活动页，包含预约、礼包领取、活动状态和后台配置。
```

```text
使用 $requirement-analysis-assistant 分析这张截图，把页面可见内容、推断功能、后台配置、埋点和异常 case 拆出来。
```

```text
使用 $requirement-analysis-assistant 审查这份需求文档，帮我指出缺失的异常 case、后台规则、埋点和验收标准。
```

```text
使用 $requirement-analysis-assistant 给储值中心生成一个原型结构，包含充值档位、支付状态、订单记录和后台配置字段。
```

## 推荐输入信息

为了得到更稳定的输出，建议提供：

- 业务目标
- 目标用户
- 使用平台或入口
- 主要用户路径
- 已确认的业务规则
- 后台配置需求
- 埋点和数据指标
- 上线时间或资源限制
- 截图、草图或竞品参考图

如果信息不完整，Skill 会把内容拆成“已知信息”“图片可见事实”“推断假设”和“待确认问题”，避免把不确定内容写成确定结论。

## 输出内容

典型输出包括：

- 需求背景
- 用户场景
- 功能范围
- 功能明细
- 交互规则
- 后台配置
- 数据埋点
- 异常 case
- 优先级建议
- 验收标准
- 待确认问题
- 原型结构
- HTML Demo
- 图片需求分析
- 落地价值

## 组织私有定制建议

公开版本建议保留通用能力；组织私有版本可在本地或私有仓库里维护模板、案例和业务知识。

建议新增：

```text
references/
  company-prd-template.md
  company-writing-style.md
  company-scenarios.md
  company-quality-checklist.md
  cases/
    website-campaign-001.md
    recharge-center-001.md
    sdk-001.md
```

当这些文件存在于私有副本中时，可以要求 Skill 优先使用组织私有模板和场景知识。

## 设计原则

- 先生成可评审的需求初稿，再由产品经理确认和修订。
- 明确区分事实、图片可见内容、AI 推断和待确认内容。
- 不把支付、风控、隐私、合规、奖励、SDK 版本等不确定规则当成事实。
- HTML Demo 用于早期需求对齐，不默认当作最终视觉设计。
- 关注研发、测试、设计和运营都能使用的交付内容。
- 将稳定的模板和方法写进 `SKILL.md`，把详细场景知识放进 `references/`，方便后续维护。

## 开源协议

MIT-0。详见 `LICENSE.txt`。
