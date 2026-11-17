# social-case-to-excel

将社媒记录整理成可回查的案例库、方法拆解和图文学习文档。

[中文](README.md) · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

## 这个 skill 用来做什么

我们用这个流程做过品牌出海历史追溯、社媒运营案例整理和评论需求分析。它不仅汇总“谁做了什么”，还会整理公开效果、拆解执行方法，并说明不同品牌和品类可以参考哪些动作。

设备品牌是其中一个研究样本，主题也可以是 AI 创意广告、产品冷启动、跨境电商或内容运营。研究对象与范围由使用者指定。

| 输出 | 内容 |
| --- | --- |
| Excel 案例库 | 案例主体、动作、公开效果、原帖链接、日期、证据限制与分类 |
| 方法拆解 | 逐条步骤、实施前提、不同品牌如何参考 |
| 配图与截图 | 对应原帖图片、视频封面或截图，嵌入表格并附来源说明 |
| 图文学习文档 | 把发现、案例和方法组织成可阅读的文档；需要时补 HTML |
| 原始候选池 | 保留检索范围与未入选记录，便于复核和增量研究 |

## 已有案例：回看中国品牌出海的第一年

一次历史追溯研究整理了六个品牌的44条事件，涵盖一加、安克、拓竹、Keychron、Snapmaker和EcoFlow。研究把预热、启动后首年与其他早期线索分开，也同时看官方、媒体、社区管理员和用户讨论。

例如，一加的记录能看到联系社区管理员、安排负责人问答的动作；Keychron的用户帖子显示了“先众筹购买、后在Reddit分享”的顺序；拓竹的讨论同时留下真实演示、耗材与交付方面的问题。我们把这些线索整理成方法参考，而没有把互动、众筹额和渠道销量混为一谈。

下面是该批次实际交付的局部截图，展示输出结构。截图内容为中文，其他语言版本沿用同一份示例。历史示例的覆盖不代表当前连接一定具备相同平台权限。

### 方法拆解

![逐条方法拆解示例](assets/readme/methods.png)

### 不同品牌如何参考

![不同品牌参考示例](assets/readme/brand-reference.png)

### 全参与者时间线与效果证据

![历史时间线示例](assets/readme/timeline.png)

Excel sample 文件统一放在 [`outputs/`](outputs/)；README 会按各份文件的真实主题介绍对应内容。

## 使用

将这个文件夹安装到你的 Agent 所支持的 skills 目录，在会话中调用 `$social-case-to-excel`，并提供研究主题、目标平台、时间范围和所需案例数量。例如：

> 回看几个中国品牌出海的早期历史。重点查 X 与 Reddit，区分官方、媒体和用户记录；整理方法、效果证据、不同品类如何参考，输出含配图的 Excel 和学习文档。

Python 表格构建需要 `openpyxl`、`Pillow`。脚本是研究与构建模板，需要按本轮主题适配；其他平台调用使用当前宿主连接暴露的 ClaudeBaby 工具。

## 数据连接

此版本统一使用 **ClaudeBaby** 数据服务。Reddit、X、YouTube、B站等是目标平台，实际可用范围取决于连接暴露的工具和权限。

首次使用先检查已有 ClaudeBaby MCP 连接，核对目标平台能力；未配置时再引导注册与配置。包内 HTTP 客户端可执行：

```bash
python3 scripts/claudebaby_preflight.py          # 本地配置检查，不联网
python3 scripts/claudebaby_preflight.py --probe  # MCP 握手与工具发现
```

客户端读取 `CLAUDEBABY_MCP_URL` 与 `CLAUDEBABY_MCP_TOKEN`，兼容旧的 `REDDIT_MCP_*` 变量。MCP 地址和认证按控制台提供的信息配置，不将 token 放进报告或仓库。

报告会保留原帖链接、时间和证据限制。自述结果与研究推导分开，截图与封面不会被当成完整视频审看。原帖媒体的权利归相应权利人，公开复用前需确认使用范围。

## ClaudeBaby 与项目

[ClaudeBaby 邀请注册](https://claudebaby.cn/console/register?ref=M8YYGRN4) · 邀请码：`M8YYGRN4`。通过该链接注册可领取邀请积分；已有账户可直接使用现有连接。

如果这个 skill 或示例对你的调研有帮助，欢迎给本仓库点一个 ⭐ Star。

```text
social-case-to-excel/
├── SKILL.md
├── README.md / README.en.md / README.ja.md / README.ko.md
├── assets/readme/
├── outputs/
├── references/
└── scripts/
```

## Installation / 安装 / インストール / 설치

```bash
npx skills add lingling1989r/social-case-to-excel --skill social-case-to-excel
```

[GitHub](https://github.com/lingling1989r/social-case-to-excel) · [ZIP](https://github.com/lingling1989r/social-case-to-excel/archive/refs/heads/main.zip)
