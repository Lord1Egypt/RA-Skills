# 设计智能层 INDEX（reading-notes-master v2.4 前置能力）

> 本目录是 reading-notes-master **全量收录**的四个设计技能（2026-10-21 收录，共 92 文件 / 1.5MB），
> 使读书笔记生成器具备**证据驱动的设计决策能力**：定调不再只靠内置 20 组主题色映射，
> 而是先检索设计智能库，再落到页面。
> 收录时已剥离各技能的安装元数据（.clawhub / _meta.json / _skillhub_meta.json），
> 并修正 ui-ux-pro-max 的内部路径为 bundle 内相对路径；原 assets/data/ 为 data/ 的
> 字节级重复副本，已剔除（脚本只读 data/）。

## 四层能力架构

| 层 | 目录 | 能力 | 何时用 |
|---|---|---|---|
| **L3 引擎层** | `ui-ux-pro-max/` | BM25 检索引擎：67 种 UI 风格 / 161 套配色 / 57 组字体搭配 / 13 技术栈规范 / 99 条 UX 规范 / 图表选型 / 落地页模式 / 产品类型→风格推荐；含 design-system 生成器 | Step 0 必跑；Step 2 定调主依据 |
| **L2 中文本土化层** | `ui-ux-pro-max-cn/` | 中文产品设计规则：中文字体栈 / 中国色彩文化 / 微信小程序规范 / 国内技术栈（Element Plus·Ant Design·Vant·小程序原生）/ 五大中文行业规则 / 中文专属交付清单 | **内容或受众为中文时优先于 L3 英文语料** |
| **L1 品牌规范层** | `awesome-design-md/references/` | 54 个真实品牌的完整 DESIGN.md（Vercel/Stripe/Linear/Notion/Claude/Apple/BMW/SpaceX…），每份含色板/字体层级/组件/布局/阴影/Do's&Don'ts/响应式/提示词指南 9 节 | 用户指定品牌风格（"做得像 Vercel"）或需要高端品牌质感时 |
| **L0 选型导航层** | `awesome-design/SKILL.md` | 20+ 设计技能的目录与决策表（按任务/按框架） | 需求超出本 bundle 四层覆盖时，据此推荐外部技能 |

## Step 0 前置检索流程（v2.4 核心新增）

```
① 判语言/受众 → 中文内容/产品？──是──→ 先读 L2 中文规则（ui-ux-pro-max-cn/SKILL.md）
      │否/兼有
      ▼
② 跑 L3 引擎检索（英文关键词，中文需先译关键词）：
   python3 ui-ux-pro-max/scripts/search.py "<english query>" --domain <style|color|typography|landing|product|chart|ux>
   可选：--stack html-tailwind|nextjs|react|vue…（产出组件级规范）
   可选：--design-system -p "<项目名>"（一键聚合推荐完整设计系统；勿加 --persist）
      │
      ▼
③ 用户指定了品牌？──是──→ 读 L1 awesome-design-md/references/<brand>.md，令牌直接并入 :root
      │否 → 按 L1 的"项目类型→推荐品牌"表主动推荐 3–5 个（SaaS→Stripe/Vercel/Linear 等）
      ▼
④ 检索结果 → 汇成《设计决策单》（风格/主色/字体/器型偏好/禁项）→ 带入 Step 2 定调
      │
      ▼
⑤ 需求超出四层覆盖？→ 查 L0 awesome-design/SKILL.md 决策表，向用户推荐外部技能（不擅自安装）
```

## 与五步法的对接点

| 步骤 | 设计智能层接入方式 |
|---|---|
| **Step 0**（新增） | 上述前置检索，产出《设计决策单》 |
| Step 1 选型 | 叙事原型选定后，用 L3 `--domain product` 校验该类型书籍的推荐风格是否冲突 |
| Step 2 定调 | 《设计决策单》优先于内置映射表；两者冲突时以检索结果为准并在交付说明中注明 |
| Step 3 转译 | 器型选型可交叉验证 L3 `--domain chart`（图表类型推荐）与 L1 品牌器型偏好 |
| Step 4 排页 | 中文页面过 L2 交付清单（中文字体栈/行高≥1.6/中文 CTA/375–1440px）；品牌风格页面对齐 L1 Do's&Don'ts |
| Step 5 导出 | 无直接接入；导出前复核《设计决策单》禁项 |

## 命令速查

```bash
DI=references/design-intelligence          # 相对于 reading-notes-master 技能根

# L3 检索（10 个域）
python3 $DI/ui-ux-pro-max/scripts/search.py "saas dashboard data dense" --domain style
python3 $DI/ui-ux-pro-max/scripts/search.py "trust blue fintech" --domain color
python3 $DI/ui-ux-pro-max/scripts/search.py "editorial serif reading" --domain typography
python3 $DI/ui-ux-pro-max/scripts/search.py "conversion hero pricing" --domain landing
python3 $DI/ui-ux-pro-max/scripts/search.py "dashboard form table" --stack html-tailwind

# L3 设计系统一键生成（聚合产品+风格+配色+字体+落地页五域）
python3 $DI/ui-ux-pro-max/scripts/search.py "education platform" --design-system -p "项目名"

# L3 域自动识别（不传 --domain 时按关键词猜，猜错则显式指定）
python3 $DI/ui-ux-pro-max/scripts/search.py "line chart trend comparison"
```

**已知限制**：
1. L3 语料为英文，中文 query 直接检索会 0 结果——先把需求译成英文关键词再检索（如"教育平台首页"→ "education platform landing page"）。
2. `--design-system` 生成器只读不写（除非显式加 `--persist`，那会往 cwd 写 `design-system/`，用前确认工作区）。
3. L3 脚本仅依赖 Python 标准库，无需安装任何第三方包。

## 降级路径（引擎不可用时）

1. `python3` 缺失或脚本报错 → 直接读 L3 `ui-ux-pro-max/data/*.csv`（styles/colors/typography 三张表覆盖 80% 定调需求）。
2. 连 CSV 也不读 → 退回 SKILL.md 内置映射表（20 组主题色 + 四大家族兜底色），质量降级但不阻塞交付。
3. 中文场景 → 无条件可读 L2 `ui-ux-pro-max-cn/SKILL.md`（纯 Markdown，无执行依赖）。

## 来源与许可

| 目录 | 来源 | 版本 | 许可 |
|---|---|---|---|
| ui-ux-pro-max | ClawHub `xobi667/ui-ux-pro-max`（上游 github.com/nextlevelbuilder/ui-ux-pro-max-skill） | 0.1.0 | MIT-0 |
| ui-ux-pro-max-cn | ClawHub `guo123dong/ui-ux-pro-max-cn`（改造自上游，Apache-2.0 基础） | 1.0.0 | Apache-2.0 |
| awesome-design-md | github.com/VoltAgent/awesome-design-md（本地完整版；ClawHub `laojun509` 版为仅含外链的空壳，未采用） | 1.0.0 | MIT-0 |
| awesome-design | ClawHub `futurizerush/awesome-design` | 0.1.1 | MIT-0 |

> 四技能均经安全审查（全树扫描无网络调用/凭据采集/危险执行模式；L3 脚本为纯标准库本地 CSV 检索）。
> 安全审查方法沉淀：先入隔离区 → 全树扫描 → 读源码 → 实测功能 → 才入库。
