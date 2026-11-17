## 任务要求清单

每种任务类型的"零件清单"——必选/可选组件、组装顺序、领域约束。按清单逐项产出。字段级规范来源：WorkBuddy 开放平台官方文档（https://open.workbuddy.cn/docs，2026-09 版）；未覆盖处以官方文档为准。

---

### 多域总览

**跨域分类证明**：开放平台资产按"能力形态"分为六类，分类互斥且穷尽——①技能：教 AI 怎么做某类事的指令包；②连接器：把外部服务/CLI 接入 AI 的桥接包；③专家：单一领域角色的 Agent 包；④专家团：多角色协作的 Agent 包（含主理人编排）；⑤Buddy 应用：行业级 AI 工作台（平台网页配置，非资产包）；⑥外部应用接入：第三方系统经 OAuth 2.1 调用 Open API（服务端开发，非资产包）。任何"发布到开放平台"的需求必落入且仅落入一类。

**全类型通用红线**（所有域任务均须遵守）：
1. 任何文件不得硬编码真实 Token/密钥/内部地址；占位符统一 `${VAR_NAME}`
2. 标识符（source、name）用小写字母+连字符（kebab-case）且全局唯一
3. 面向用户的文案字段中英成对（{en, zh} 或独立 _zh/_en 字段）；LocalizedString 可写纯字符串或 {zh, en} 对象，缺语言回退 zh → en
4. version 用语义化版本，每次更新递增
5. 生成顺序恒为：先读 requirements 字段表 → 再从 templates/ 模板填充 → 生成后立即分步校准 → 交付前跑 D6-01
6. 打包均为 zip（Buddy 应用除外——其在开放平台网页端配置）

---

### D0 需求与路由域

#### 域级说明

D0 域承载所有生成请求的公共前置逻辑：需求信息是否齐全直接决定后续域能否一次成型。核心判定规则（D0-02 使用）：
- 教 AI"怎么做某类事"（纯指令/知识，无外部服务）→ **技能**
- 要把外部 API 服务或命令行工具接进 AI → **连接器**（有网络 API 选 MCP+Skill；已有稳定跨平台 CLI 选 CLI+Skill）
- 单个领域角色（一个人设+一份专业提示词）→ **专家**
- 多角色需按阶段协作（主理人调度成员）→ **专家团**
- 要一个面向最终用户的行业专属 AI 工作台 → **Buddy 应用**
- 第三方系统要以应用身份调用用户数据/驱动本地助理 → **外部应用接入**（要点：OAuth 2.1 授权码流程；access_token 有效期 24h，refresh_token 60d 且仅存服务端；Scope 最小权限——user.profile.readable / user.contact.readable / user.credit.exchange / user.task.invokable / user.task.readable / user.localassistant.invokable / user.localassistant.readable；平台网页注册应用获取 client_id/client_secret，后者仅展示一次。完整流程以官方 /docs/third-party-app 为准）

#### D0-01 需求信息收集
- **必选组件**: 资产名称与定位、核心能力清单、目标用户与使用场景、已有材料清单（API 文档/CLI 工具/知识文档/设计稿）、输出目录
- **可选组件**: 参考竞品、上架紧迫度、版本计划
- **组装顺序**: 逐项询问补全→材料收集→信息汇总表
- **约束**: 生成前必填项缺失必须向用户追问，不得假设；已有材料优先直接读取文件
- **格式**: 需求信息表（Markdown）

#### D0-02 资产类型判定
- **必选组件**: 类型判定结果、判定依据（对照域级说明判定规则）、类型特有补充信息清单
- **可选组件**: 多类型组合方案（如专家团内置技能）
- **组装顺序**: 能力形态分析→判定规则匹配→类型确认（向用户展示判定依据）→补充信息收集
- **约束**: 判定依据必须向用户展示；类型存疑时列出候选类型差异后请用户确认
- **格式**: 类型判定报告（Markdown）

#### D0-03 生成方案规划
- **必选组件**: 资产包目录与名称（kebab-case）、语言方案（中英字段清单）、产出文件清单（对照目标域 requirements 字段表）、依赖与凭证占位符清单
- **可选组件**: 里程碑拆分、风险项（如平台规范不确定点，标注"以官方文档为准"）
- **组装顺序**: 命名确定→文件清单生成→占位符规划→用户确认
- **约束**: 产出文件清单必须覆盖目标域全部必选文件；所有将引用凭证的位置预先规划 ${VAR} 占位符
- **格式**: 生成方案（Markdown）

---

### D1 技能生成域

#### 域级说明

技能是教 AI 执行某类任务的指令包，上传 zip 后由平台解析。**解析失败排查顺序**：目录层级（仅支持两级，见下）→ 目录结构 → SKILL.md frontmatter 字段 → 编码（UTF-8）→ 文件引用路径。定位失败可邮件 openworkbuddy@tencent.com 或扫码进开发者社群。

**目录结构规范**：
```
skills/
└── {skill-name}/
    ├── SKILL.md              # ★ 必须存在的技能定义
    ├── references/           # 可选：SKILL.md 引用的补充知识（@references/xxx.md 引用）
    ├── scripts/              # 可选：可执行脚本（AI 经 Bash 调用，需声明命令与参数）
    └── templates/            # 可选：模板脚本/配置文件
```

**两级目录硬约束（平台实测，官方文档未载明）**：Skill 包仅支持两级目录结构（根目录/二级目录/文件），超限报错"目录层级超限 — Skill 包仅支持两级目录结构（根目录/二级目录/文件），请移除子目录嵌套"。因此 references/、scripts/、templates/ 内**不得再建任何子目录**，所有文件必须直接平铺在这三个二级目录内；SKILL.md 必须位于包根。

**SKILL.md 格式**：YAML frontmatter + Markdown 正文。正文为技能指令（何时触发、按什么步骤执行）。

**Frontmatter 字段表**（与官方文档技能页字段表 2026-09 版逐字段核对一致；display_name/display_name_en/category 见官方示例 frontmatter）：

| 字段 | 必填 | 说明 |
|------|------|------|
| name | 否 | 技能标识（kebab-case 惯例） |
| description | 是 | 写清用途和触发词 |
| description_zh | 是 | 简短中文介绍 |
| description_en | 是 | 简短英文介绍 |
| allowed-tools | 否 | 工具白名单（逗号分隔） |
| version | 是 | 版本号，语义化（x.y.z），每次更新递增 |
| disable-model-invocation | 否 | true 则 AI 不会自动触发，只能用户手动调用 |
| user-invocable | 否 | false 则隐藏菜单，仅供 AI 内部使用 |
| author | 是 | 合作方名称 |
| display_name / display_name_en | 否 | 市场展示名（官方示例含此字段） |
| category | 否 | 平台技能分类之一。2026-09 联网查证：技能市场官方预置分类为「生活服务 / 开发工具 / 投资理财 / 内容创作 / 数据分析 / 效率工具 / 办公协同 / 商业运营 / 知识与学习」；category 英文枚举官方未公开，官方示例值 writing 对应「内容创作」。生成时按技能定位选中文分类，英文值以开放平台"创建技能"流程的分类下拉为准（开发工具类推断值 development，需核对） |

可选字段使用规则：省略可选字段即取默认行为；disable-model-invocation / user-invocable 仅接受 true/false，仅在需要改变默认行为（禁止自动触发 / 隐藏菜单）时添加。

#### D1-01 技能目录结构生成
- **必选组件**: skills/{skill-name}/ 目录、SKILL.md 空文件占位、按需的 references/ scripts/ templates/ 目录
- **可选组件**: .gitignore、LICENSE
- **组装顺序**: 确定目录名（kebab-case）→创建骨架→空目录占位说明
- **约束**: 目录名与 name 一致；仅 SKILL.md 为必须文件，子目录按需创建不为凑数；**两级目录硬约束——references/、scripts/、templates/ 内禁止再建子目录，所有子资源文件直接平铺**
- **格式**: 目录树（文本）

#### D1-02 SKILL.md 生成
- **必选组件**: frontmatter（description、description_zh、description_en、version、author 必填 + 其余按需）、指令正文（触发条件 + 执行步骤 + 输出要求）
- **可选组件**: 子资源引用（@references/xxx.md）、脚本调用声明（命令 + 参数 + 依赖说明）、frontmatter 可选字段（display_name/display_name_en、category、allowed-tools、disable-model-invocation、user-invocable，按需添加，省略即默认行为）
- **组装顺序**: 从 templates/skill-SKILL-template.md 复制→逐字段填充→正文按清单法生成→对照字段表核对
- **约束**: 必填字段一个不缺（description、description_zh、description_en、version、author）；触发词写入 description；可选布尔字段只接受 true/false；正文步骤可直接执行无歧义；引用的子资源路径必须真实存在
- **格式**: SKILL.md 文件（UTF-8）

#### D1-03 子资源生成
- **必选组件**: （按需）references/ 补充知识文档、scripts/ 可执行脚本、templates/ 模板文件
- **可选组件**: 脚本依赖声明、示例数据
- **组装顺序**: 判断是否需要子资源→逐个生成→在 SKILL.md 中登记引用
- **约束**: references/ 放知识文档；scripts/ 放可独立执行脚本且声明运行时；templates/ 放标准化模板；SKILL.md 未引用的文件不放入；**全部文件平铺在二级目录内（两级目录硬约束），示例数据类文档直接放 references/（如 references/examples.md），不建嵌套子目录**
- **格式**: 对应目录下文件

#### D1-04 技能打包
- **必选组件**: zip 包（目录名=技能名）、结构自检结果
- **可选组件**: CHANGELOG
- **组装顺序**: 结构自检（含两级目录深度检查）→压缩为 zip→记录包名与版本
- **约束**: zip 根层为 {skill-name}/ 目录；编码 UTF-8；包内不含真实凭证；**包内任意文件路径深度不得超过 根目录/二级目录/文件 两级，超限必被平台解析拒绝**
- **格式**: zip 文件 + 自检清单

---

### D2 连接器生成域

#### 域级说明

连接器把外部服务接入 AI。**接入方式判定规则**：有网络 API 服务或可开发 MCP Server → **MCP + Skill（推荐）**，远程服务用 HTTPS 的 SSE 或 streamableHttp；已有成熟跨平台命令行工具 → **CLI + Skill**。两种方式都含 connector-meta.json、icon 和可选的 skills/ 使用说明。

**MCP+Skill 目录结构**：
```
your-connector/
├── connector-meta.json     # ★ 元信息
├── mcp.json                # ★ MCP Server 连接配置
├── icon.svg                # ★ 市场图标（svg/png/jpg）
└── skills/{skill-name}/SKILL.md   # AI 使用说明（可选）
```

**MCP Server 要求**：遵循 MCP 稳定协议版本；远程用 HTTPS（SSE 或 streamableHttp），本地进程可用 stdio；工具名/描述/参数/返回值清晰稳定；返回可读错误并合理超时（单次建议 30 秒内）；涉及用户数据必须认证鉴权并最小权限；**一个连接器只配置一个 MCP Server**。

**mcp.json 字段表**：

| 字段 | 必填条件 | 说明 |
|------|---------|------|
| mcpServers | 必填 | 顶层配置；仅配置一个 Server |
| type | 远程服务必填 | sse、streamableHttp 或 stdio |
| url | SSE/streamableHttp 必填 | 生产环境必须 HTTPS |
| command | stdio 必填 | 启动命令，如 npx、uvx、node |
| args | 可选 | 启动参数数组 |
| headers / env | 可选 | 支持 ${VAR_NAME} 变量引用，不得写真实凭证 |
| timeout | 可选 | 连接超时，默认 30000 毫秒 |
| runtime | 可选 | stdio 所需运行时声明，目前支持 Node.js |
| disabledTools | 可选 | 不向 AI 暴露的工具列表 |

**CLI+Skill 目录结构**：connector-meta.json（type=cli）、cli.json、icon.svg、skills/（强烈推荐）。

**CLI 开发要求**：至少支持 macOS 和 Linux，建议支持 Windows；提供非交互式安装与明确的 auth/status/unAuth 命令；auth 成功后 CLI 自持久化登录态，status 只查状态无副作用，unAuth 撤销授权；明确退出码与可读错误，业务结果优先 JSON；不依赖用户机器预装运行时（在 cli.json 声明 runtime）；凭证与安装目录分离。

**cli.json 字段表**：

| 字段 | 必填 | 说明 |
|------|------|------|
| init.{platform} | 是 | 各平台安装命令，平台名 darwin、linux、win32 |
| auth | 按需 | 登录命令；支持单步或多步认证 |
| unAuth.{platform} | 有认证时必填 | 登出或清理授权命令 |
| status.{platform} | 有认证时必填 | 无副作用的认证状态检查命令 |
| statusMatch / statusMatchJson | 二选一 | 判断已登录的文本正则或 JSON 条件 |
| authUrlDomain | 建议 | 浏览器授权时限定可提取并打开的认证域名 |
| env | 可选 | 注入固定环境变量，可用 $HOME / ${HOME} |
| runtime | 依赖运行时时建议 | 声明 Node.js 或 Python 运行时及版本 |
| versionCheck | 可选 | 检查 CLI 最低版本，过低时重装 |

**connector-meta.json 字段表**：

| 字段 | 必填 | 说明 |
|------|------|------|
| name / name_en | 是 | 默认名与英文名；可补 name_zh |
| description / description_zh / description_en | 是 | 简明说明核心能力与适用场景 |
| source | 是 | 全局唯一标识，仅小写字母、数字、连字符 |
| type | 可选 | mcp（默认）、cli 或 skill-only；CLI 方案必须设为 cli |
| version | 建议 | 语义化版本，每次更新递增 |
| examples_zh / examples_en | 是 | 中英文使用示例，各 2~5 条 |
| minWorkbuddyVersion | 使用新字段时必填 | 要求的最低 WorkBuddy 版本 |
| auth_mode | MCP 按需 | 省略=Server 自带 OAuth/无认证；server-side 或 gateway=云端托管（接入前与 WorkBuddy 团队确认）；token=用户自填（需提供 token-schema.json 描述表单） |

**图标规范**：SVG（推荐）/PNG/JPG，文件名 icon.svg/icon.png/icon.jpg，PNG/JPG 建议 64×64px，背景透明，小尺寸可辨识。

**认证与凭证**：MCP 自带 OAuth 或无认证→auth_mode 省略；云端托管→server-side/gateway；用户自填→token + token-schema.json；CLI→cli.json 的 auth/status/unAuth。敏感凭证字段用密码类型；日志不输出完整凭证；授权失效返回可识别错误并引导重连。

#### D2-01 接入方式判定
- **必选组件**: 判定结果（mcp/cli）、判定依据、Server/CLI 能力清单（工具名或命令列表）
- **可选组件**: 认证方式初判
- **组装顺序**: 服务形态分析→判定规则匹配→向用户确认→能力清单汇总
- **约束**: 有网络 API 优先 MCP；仅已有稳定跨平台 CLI 才选 CLI；判定依据须展示给用户
- **格式**: 判定报告（Markdown）

#### D2-02 元信息与图标生成
- **必选组件**: connector-meta.json（全必填字段）、icon 文件（用户提供或生成 SVG）
- **可选组件**: name_zh、token-schema.json
- **组装顺序**: 从 templates/connector-meta.json-template.json 填充→source 唯一性确认→示例文案打磨→图标置入
- **约束**: source kebab-case 全局唯一；examples_zh/en 各 2~5 条且为用户真实口语；description 说明用户能完成什么
- **格式**: JSON + SVG/PNG

#### D2-03 连接配置生成
- **必选组件**: mcp.json（MCP 方案，单 Server）或 cli.json（CLI 方案，三平台命令）
- **可选组件**: headers/env 占位符、timeout、disabledTools、runtime、versionCheck
- **组装顺序**: 从 templates/mcp.json-template.json 或 cli.json-template.json 填充→凭证位置替换为 ${VAR}→协议字段核对
- **约束**: 远程 url 必须 HTTPS；mcpServers 下仅一个 Server；凭证零硬编码；CLI 方案 darwin/linux/win32 命令齐全且 status 无副作用
- **格式**: JSON 文件（UTF-8 无 BOM）

#### D2-04 配套 Skill 生成
- **必选组件**: skills/{skill-name}/SKILL.md，覆盖每个工具/命令的用途、参数表、调用示例、认证前置、错误恢复、高风险操作确认规则
- **可选组件**: 返回格式示例、典型场景编排示例
- **组装顺序**: 工具清单遍历→逐工具生成说明段→认证与异常章节→路径登记
- **约束**: MCP 有标准工具描述时可选，CLI 方案强烈推荐必须提供；参数名称/类型/必填/默认值与实际一致
- **格式**: SKILL.md 文件

---

### D3 专家生成域

#### 域级说明

专家是单一领域角色包，上传 zip 由平台解析（失败排查同 D1：结构→plugin.json 字段→编码；联系 openworkbuddy@tencent.com 或社群）。展示位置：客户端【专家·技能·连接器】→【专家】→ 专家市场。

**目录结构**：
```
my-expert/
├── .codebuddy-plugin/
│   └── plugin.json        # ★ 核心配置
├── avatars/
│   └── expert.png         # 头像
├── agents/
│   └── my-expert.md       # Agent 定义
└── README.md              # 推荐
```

**plugin.json 字段表——基础字段**：

| 字段 | 必填 | 说明 |
|------|------|------|
| name | ✅ | 唯一标识，小写字母+连字符（如 design-experts） |
| expertType | ✅ | 单专家填 "agent" |
| version | ✅ | 语义化版本 |
| description | ✅ | 英文简短描述 |
| author | ✅ | {name, email} |
| agents | ✅ | Agent 文件路径列表，如 ["./agents/my-expert.md"] |
| agentName | ✅ | 主 Agent 名称（agents/ 下 MD 文件名，不含 .md） |
| skills | 否 | 技能目录路径列表，如 ["./skills/my-skill"] |
| homepage / license / keywords | 否 | 主页/许可证/搜索标签 |
| dependencies | 否 | {mcpServers, connectors}，见 D3-04 |

**plugin.json 字段表——展示字段**：

| 字段 | 必填 | 说明 |
|------|------|------|
| displayName | ✅ | {en, zh} 市场展示名 |
| profession | ✅ | {en, zh} 职业头衔 |
| displayDescription | ✅ | {en, zh} 展示描述，**中文 40~50 字**，突出核心能力 |
| avatar | ✅ | 头像相对路径（如 avatars/expert.png） |
| categoryId | ✅ | 行业分类 ID（15 选 1，见下表） |
| defaultInitPrompt | ✅ | 首次对话默认提示语，**必须与 quickPrompts 第一条一致** |
| plugin | ✅ | 关联 Plugin 名，**与 name 一致** |
| tags | ✅ | {en, zh}[] 擅长领域标签，**固定 3 个** |
| quickPrompts | ✅ | {en, zh}[] 推荐提示词，**固定 3 个** |

**categoryId 行业分类表**：01-ProductDesign 产品设计 / 02-Engineering 技术工程 / 03-GameSpatial 游戏空间 / 04-DataAI 数据智能 / 05-MarketingGrowth 营销增长 / 06-ContentCreative 内容创作 / 07-SalesCommerce 销售商务 / 08-FinanceInvestment 金融投资 / 09-OperationsHR 运营人力 / 10-ProjectQuality 项目质量 / 11-SecurityCompliance 法务安全 / 12-IndustryConsultant 行业顾问 / 13-TencentZone 腾讯专家 / 14-WorldWise 全球发展 / 15-Education 教育学习。

**Agent 定义文件**（agents/*.md）：YAML frontmatter + 系统提示词正文。frontmatter 字段：name✅（与文件名一致不含 .md）、description✅（英文，AI 判断何时激活）、displayName✅（{en, zh}）、profession✅（{en, zh}）、maxTurns（默认 50）、skills（预加载技能列表）。**开发者不可自行添加 tools**，工具由系统统一分配（Read/Write/Grep/Glob/Bash/WebSearch/WebFetch/AgentTool/SendMessage，后两者仅主理人可用）。

**头像规范**：PNG（推荐）/JPG，512×512px 正方形，单张 ≤500KB，统一漫画/插画风格，专业自然，符合角色定位，无违规内容；放 avatars/ 目录，plugin.json 相对路径引用。

**官方模板**：design-experts.zip（https://codebuddy-platform-1258344699.cos.ap-beijing.myqcloud.com/open/static/files/design-experts.zip）。

#### D3-01 专家包结构生成
- **必选组件**: .codebuddy-plugin/、agents/、avatars/ 目录、README.md
- **可选组件**: skills/（内置技能）、.mcp.json
- **组装顺序**: 目录名确定→骨架创建→占位
- **约束**: plugin.json 必须位于 .codebuddy-plugin/ 下；头像统一放 avatars/
- **格式**: 目录树（文本）

#### D3-02 plugin.json 生成
- **必选组件**: 基础字段全量 + 展示字段全量（对照上表）
- **可选组件**: skills、homepage、license、keywords、dependencies
- **组装顺序**: 从 templates/expert-plugin.json-template.json 填充→文案字段打磨（displayDescription 中文 40~50 字）→tags/quickPrompts 各 3 条→一致性核对（plugin=name、defaultInitPrompt=quickPrompts[0]、agentName 与 agents 文件对应）
- **约束**: categoryId 必须取 15 枚举之一；displayDescription 中文严格 40~50 字；三处一致性逐项核对
- **格式**: JSON 文件

#### D3-03 Agent 定义生成
- **必选组件**: agents/{name}.md：frontmatter（name/description/displayName/profession）+ 系统提示词（角色定位、核心能力、工作流程、输出规范）
- **可选组件**: maxTurns（默认 50）、skills 预加载
- **组装顺序**: 人设设计→frontmatter 填充→提示词正文（清单法：定位/能力/流程/输出规范）→与 plugin.json 一致性核对
- **约束**: name 与文件名一致；description 英文且说明激活时机；提示词不声明 tools（系统统一分配）；输出规范可直接执行
- **格式**: Markdown 文件

#### D3-04 依赖声明生成
- **必选组件**: （按需）dependencies 声明——仅当专家必须调用外部 MCP/企业连接器才能工作时声明；简单专家不声明
- **可选组件**: dependencies.mcpServers（相对路径字符串/路径数组/内联对象）、dependencies.connectors（平台已有连接器 ID 列表）、根目录 .mcp.json 兜底（含 x-workbuddy 元信息与 tokenSchema）
- **组装顺序**: 依赖必要性判定→声明方式选择（plugin.json 内声明推荐）→x-workbuddy 展示与鉴权信息填充
- **约束**: x-workbuddy 为平台私有字段（displayName/description/icon/auth.type: oauth|token|none/tokenSchema），连接后写入用户配置时会被剥离；token 类型时 headers 用 ${KEY} 占位且 tokenSchema.fields[].key 与之一致；包内严禁硬编码真实 Token
- **格式**: JSON 配置

---

### D4 专家团生成域

#### 域级说明

专家团是多角色协作包（expertType="team"），展示于专家市场【专家团】Tab。与单专家的关键差异：必含 teamInfo 与 members、必带 settings.json、主理人命名规则、团队级头像组。

**目录结构**：
```
my-team/
├── .codebuddy-plugin/plugin.json   # ★
├── avatars/                        # ★ team.png + 主理人 + 各成员头像
├── agents/                         # ★ {team}-team-lead.md + 成员 md
│                                   #    主理人名称须加专家团前缀，不可用通用 team-lead
├── skills/                         # 共享技能（可选，结构同 D1）
├── .mcp.json                       # 内置 MCP/连接器依赖（可选，同 D3-04）
├── bin/                            # 可执行文件（可选）
├── settings.json                   # ★ 设置主理人（必须存在；具体字段以官方模板为准）
└── README.md                       # 推荐
```

**plugin.json 相对单专家的差异字段**：expertType✅填 "team"；teamInfo✅={leadAgent, memberAgents[]}；members✅=[{id✅(对应 Agent md 文件名不含 .md), name✅{en,zh}, profession✅{en,zh}, avatar✅, role✅("lead"|"member")}]；profession 须与 displayName 保持一致；tags 官方示例为 3~4 个（示例 4 个），常规按 3 个。其余展示字段同 D3。

**主理人 Agent 提示词铁律**（官方 trading-team 示例范式，生成时按团队实际改写）：
1. 主理人不亲自做专业分析，只做编排：确认目标→按阶段调度→汇总传递→整合报告
2. 建团队（TeamCreate）必须且只能由主理人执行，严禁委派成员；严禁 spawn 主理人自己
3. 成员产出必须由成员输出，主理人严禁代写；所有跨成员信息流必须经主理人中转，成员不得互连
4. 严禁未完成前序阶段跳到后续阶段；每阶段结束向用户通报
5. 子任务命名：调度成员时在 Agent 工具 name 参数传入成员角色名（中文）
6. 输出语言与用户原始需求一致

**内置工具**：主理人可用 AgentTool/SendMessage 调度成员；成员工具同 D3 由系统分配。

**官方模板**：trading-team.zip（https://codebuddy-platform-1258344699.cos.ap-beijing.myqcloud.com/open/static/files/trading-team.zip）。settings.json 的字段规范官方文档未详列，生成时以该模板为准（待验证项）。

#### D4-01 团队角色设计
- **必选组件**: 团队定位、主理人职责（纯编排声明）、成员清单（角色名/职责/输出物）、SOP 阶段划分（3~5 阶段，含并行/串行标注）
- **可选组件**: 共享技能方案、依赖连接器方案
- **组装顺序**: 目标拆解→角色枚举→去重合并→SOP 阶段编排→与用户确认
- **约束**: 主理人必须纯编排不做专业产出；每个成员职责互斥可并行处明确标注；SOP 阶段有明确输入输出
- **格式**: 团队设计文档（Markdown）

#### D4-02 团队 plugin.json 生成
- **必选组件**: 基础字段 + 展示字段 + teamInfo + members 全量
- **可选组件**: skills、dependencies
- **组装顺序**: 从 templates/team-plugin.json-template.json 填充→members 与 agents 文件一一对应→一致性核对（plugin=name、defaultInitPrompt=quickPrompts[0]、profession=displayName）
- **约束**: teamInfo.leadAgent 与 members 中 role=lead 的 id 一致；memberAgents 与 members（member 角色）一致；主理人 agent 文件名含团队前缀且不叫 team-lead
- **格式**: JSON 文件

#### D4-03 主理人 Agent 生成
- **必选组件**: agents/{team}-team-lead.md：frontmatter（maxTurns 建议 ≥100）+ 提示词（编排定位、成员分工表、SOP 五段式、协作铁律、严禁行为清单）
- **可选组件**: 消息中转格式约定、进度通报模板
- **组装顺序**: 按 D4-01 设计稿→frontmatter→编排正文（对照铁律清单逐条写入）→与 plugin.json 成员表一致性核对
- **约束**: 铁律六条必须全部体现；严禁行为清单必须包含：禁跳过建团队、禁代写成员产出、禁跨阶段、禁成员直连、禁 spawn 自己
- **格式**: Markdown 文件

#### D4-04 成员 Agent 生成
- **必选组件**: 每个 agents/{member}.md：frontmatter + 专业提示词（分析维度/输出格式/maxTurns）
- **可选组件**: 与其他成员的协作接口说明
- **组装顺序**: 成员清单遍历（可并行生成）→逐成员生成→输出格式统一性核对
- **约束**: name 与文件名一致；description 英文说明职责；输出格式可被主理人直接汇编；不声明跨成员直连
- **格式**: Markdown 文件（每成员一个）

---

### D5 Buddy应用生成域

#### 域级说明

Buddy 应用是垂直行业 AI Harness：伙伴造配置不造产品，WorkBuddy 提供产品框架与 AI 底座（多 Agent 协同、上下文压缩、记忆工程、工具调用编排、安全权限管控开箱即用）。**与前三类不同：在开放平台网页端配置（左侧模块导航+右侧表单，5 个模块），不走 zip 上传**；模块可跳步骤、支持导出配置 JSON 本地预览。

**六大自定义维度**：①工作模式（System Prompt+预绑定 Skill，官方原文"内置 Skill"，模式级 Harness 全程生效）②场景胶囊（输入框上方快捷提示词模板，可绑定专家/Skill/连接器/案例，场景级 Harness）③模型配置（从平台模型池勾选、排序、指定默认）④垂直行业市场（Skill/专家/连接器/灵感案例）⑤内嵌已有功能（MCP Apps 等）。注：官方页面称"六个维度"但正文仅详述此 5 项，第 6 项见于官方架构总览图、未给文字说明，以官方文档为准。

**模块 1 创建应用**：应用 ID（系统生成不可改）、应用头像（建议 256×256）、应用名称、应用简介、授权列表、授权回调 URL、可信 Origin。创建后生成 Client ID 与 Client Secret（**仅展示一次，关闭后不可再看**）。授权回调 URL/可信 Origin 仅在应用涉及 OAuth 授权（如配置 OAuth 内置连接器）时需要伙伴真实域名；回调端点（接收授权码并换取令牌的 HTTPS 服务）由伙伴自行实现，不属于平台配置内容（参考实现见 templates/buddy_oauth_callback_local.py 与 buddy_oauth_callback_scf.py，配置 WB_* 环境变量即用，平台端点参数以官方文档为准）。

**模块 2 首页配置**：首页标题 Slogan、场景胶囊（快捷提示词模板）、工作模式（建议 2~4 个，各对应不同 System Prompt，可预绑定 Skill 覆盖模式下所有对话）、内置连接器（可选；**须为支持 OAuth 方式认证的 MCP**：用户首次进入应用完成应用授权后弹出"绑定应用"弹窗，点击"绑定"即跳转该 MCP 的 OAuth 认证）。

**模块 3 市场配置**：专家（可设分类标签；专家团可选开启）、技能、连接器、精选场景（可选开启，推荐位关联专家或专家团）。

**模块 4 其他配置**：跳过首次绑定应用授权（应用不使用绑定能力时可开启，如内置连接器走非 OAuth 方式授权）；绑定应用授权文案（绑定弹窗内"绑定后，即可获取「XX」专业能力"，不设置则默认展示应用名）；输入框占位符（中英文两种文案）；模型勾选/排序/默认模型。

**模块 5 预览调试**：提交审核前经预览链接下载对应版本 WorkBuddy 端验证配置。

**设计规范**：应用 icon 16px×16px、线宽 1.2px、有断口、圆角平滑 100%、风格与官方示例一致；专家页精选场景背景图 1000×910px、底图+3 层渐变蒙层、日夜间 2 套、极简插画风格（素材包 https://codebuddy-platform-1258344699.cos.ap-beijing.myqcloud.com/open/static/files/buddy-app.zip）。

**发布流程**：创建应用→填写基础信息→创建审核通过（进入草稿态）→分模块配置→预览调试→提交审核→发布上线；后续变更修改后重新提交审核。

**最佳实践**：先梳理目标用户至少 5 个高频场景再围绕场景组织配置（官方原文"至少5个高频场景"）；工作模式 2~4 个勿贪多；经 iframe/MCP Apps 集成已有系统；先发布最小可用版本再迭代；每次退出配置前导出配置文件。

#### D5-01 应用基础配置
- **必选组件**: 应用名称、应用简介、应用定位说明、授权要素清单（授权列表/回调 URL/可信 Origin 建议）
- **可选组件**: 头像设计要点（256×256）
- **组装顺序**: 定位梳理→字段逐项给出填写内容→凭证管理提醒（Client Secret 仅一次）
- **约束**: 本模块在平台网页操作，本任务输出"填写内容清单"供用户逐项粘贴；应用 ID 系统生成不可修改
- **格式**: 配置内容清单（Markdown）

#### D5-02 首页与市场配置
- **必选组件**: Slogan 文案（中英）、场景胶囊清单（2~5 条，可绑定资产）、工作模式定义（2~4 个，各含 System Prompt、预绑定 Skill 与适用场景）、市场资产清单（专家/技能/连接器，含引用 ID）
- **可选组件**: 内置连接器（须为支持 OAuth 认证的 MCP，附"绑定应用"弹窗流程说明）、精选场景方案（含背景图设计要求转述）
- **组装顺序**: 高频场景梳理→场景胶囊生成→工作模式 System Prompt 编写→市场资产对齐（引用 ID 与资产 source/name 一致）
- **约束**: 工作模式 2~4 个；场景胶囊用用户真实口语；引用的专家/技能/连接器必须已上架或同批生成
- **格式**: 配置内容清单（Markdown）

#### D5-03 其他配置与预览
- **必选组件**: 跳过首次绑定授权判定（开启/关闭及依据）、绑定应用授权文案（开启绑定时必填）、输入框占位符（中英）、模型配置建议（勾选清单/排序/默认模型）、icon 设计规格说明、预览调试步骤清单
- **可选组件**: 背景图设计需求说明、发布流程检查点
- **组装顺序**: 占位符文案→模型建议→设计规格转述→预览清单→发布流程提醒
- **约束**: icon/背景图规格按官方数值转述不得改动；提醒用户导出配置 JSON 再退出
- **格式**: 配置内容清单（Markdown）

---

### D6 校验与交付域

#### 域级说明

D6 是强制质量门禁：**校验未全 PASS 不得打包提交**。校验双轨：脚本校验（字段级，客观）+ 人工检查清单（文案质量、设计规范，主观）。入驻前置：企业认证（营业执照 OCR + 法人人脸核身/腾讯云授权/微信公众号小程序授权三选一；每账号最多认证 10 个企业主体，每企业最多被 50 账号认证）或个人认证（大陆二代身份证+实名手机号+邮箱+人脸；一个身份证全平台只能认证一个个人主体，每账号最多一个个人主体）。

**解析失败通用排查**：目录结构 → 配置文件字段 → UTF-8 编码 → 文件引用路径；仍失败邮件 openworkbuddy@tencent.com 或扫开放平台首页二维码进社群。

**审核要点**：名称简明可识别；描述直说用户能完成什么；示例用真实口语；无硬编码凭证；图标/头像符合规格；版本与最低兼容版本声明正确；覆盖超时/授权失效/参数错误等异常场景。

#### D6-01 规范校验
- **必选组件**: validate_asset.py 执行结果、人工检查清单结果、校验报告（每项 PASS/FAIL/WARN）
- **可选组件**: 修复建议清单
- **组装顺序**: 脚本校验（含技能包两级目录深度检查）→逐条解读→人工清单（文案/设计/安全）→FAIL 项回写对应生成任务→复检至全 PASS
- **约束**: 脚本 FAIL 必须修复；WARN 逐条向用户说明风险；安全类问题（硬编码凭证）零容忍；校验已有资产时本任务可作临时入口
- **格式**: 校验报告（Markdown）

#### D6-02 打包与提交指引
- **必选组件**: 打包产物（zip 或配置清单）、入驻前置核对结果、分类型提交步骤、失败排查预案
- **可选组件**: 版本记录、后续更新提醒
- **组装顺序**: 打包→入驻/资质核对→提交步骤给出→排查预案附上
- **约束**: 提交动作由用户在开放平台执行，本任务只产出指引；zip 结构符合各类型规范；提醒 Client Secret 仅展示一次、每次更新递增版本号
- **格式**: 提交指引文档（Markdown）
