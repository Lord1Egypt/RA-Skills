# 版本历史

> 正文只保留最近两版，完整历史在这份文件里。

### v2.6.0 (2026-10-02)

- **技能标识（slug）改为「先问一句」**：Step 1 需求澄清新增必问项，Step 3 新增「先定标识」小节 ——
  用户给了标识就原样采用（一个字符都不加工），说"随便/你定"才按「动作-对象」自动生成裸名。
  理由：标识上架后**永久锁死**，改名 = 整个重建，是四个待澄清项里唯一猜错就无法回退的。
- **去掉内置的 `ym-` 默认前缀**（破坏性变更）：生成器本身是要分发给别人用的，把某个人
  （作者）的命名习惯写成默认值，等于把个人习惯塞进所有人的技能包 —— 别人装完满屏看不懂的缩写，
  还会暴露是谁的机器产出的。前缀改为三档可选来源，优先级从高到低：
  `--no-prefix` > 命令行 `--prefix`（显式传空串 = 不加）> 环境变量 `SKILL_NAME_PREFIX`
  > 平台根 `skill-gen.json` 的 `name_prefix` > 不加。
  有固定标识习惯的使用者自己配后两档即可，技能本身不再含任何个人标识。
- 文档同步清理：`references/naming-and-discovery.md` 的起名清单第 0 条、`references/pitfalls.md`
  第 7 条、`templates/skill-skeleton.md` 的模板抬头，去掉「本机自建技能一律 ym- 开头」类表述；
  SKILL.md 新增常见坑 18，并把原先重复的编号 16 理顺成 17。

### v2.3.1 (2026-09-19)

- **新增体检规则「文档放行标记」**（P1）：`.md` / `.txt` 文档里出现 HTML 注释形式的放行标记
  直接判 P1，报错文案说明改法。缘由：这类注释**渲染后不可见**，第三方安全审计会读成
  「隐蔽地指示审计放行」= 提示注入 —— 实测已使一个技能在 SkillHub 被判 `suspicious`。
  放行应当可见、可审阅：脚本文件保留行尾注释，文档改用技能根的 `.skillignore` 写
  `rule:规则名`，或改写正文让它不再命中。体检项由 9 类增至 10 类。
- **修掉教人踩坑的文档**：`references/sanitize-rules.md` 原有「文档里的 HTML 注释写法同理」
  一句，等于在教人用隐藏注释放行，已改为明确禁止并给出两种正当做法；
  `references/checklist.md` 的「放行方式」与 `SKILL.md` 的放行表同步补上这条约束。
- **修 `new_skill.py --force`/全新生成的「随机访问被拒绝」**（批量批次实测 10 个里 6 个报 WinError 5，
  重跑又只挂其中 2 个）：`write_all` 的最后一步 `tmp.rename(target)` 会撞上技能目录 watcher /
  杀软实时扫描的竞争窗口 —— 目标路径刚出现的瞬间被别的进程打开，rename 即报 PermissionError。
  实测特征：同一名字稳定失败、改成别的名字就能成功、过一会儿再跑又好了。
  新增 `_rename_with_retry()`：PermissionError 时按 0.4s 递增间隔重试 5 次，其余异常原样抛出。
- 修 `new_skill.py` 的一处**漏改**：不传 `--desc` 时自动生成的占位说明仍带尖括号
  （`<一句话说清…>` 与 `<场景>`），于是「纯脚本生成、不给任何描述」这条路体检必报 1 条 P1，
  与 v2.3.0 里已修的两条同源。现统一成 `待填写：…` 写法。
  实测：骨架生成后 **P0=0 P1=0 P2=1**，脚本自己打印「骨架合规」。

### v2.3.0 (2026-09-16)

- **A 组 · 可靠性**（针对 TRACE 评测「异常处理 4.3 / 运行稳定性 4.4」）：
  - 新增 `scripts/_friendly.py`：四个脚本共用的中文错误出口（异常 → 人话 + 怎么修）与统一退出码
    `0 成功 / 1 有 P1 / 2 有 P0 / 3 参数或目录错 / 4 写入打包失败`，非 0 退出时打印含义与下一步。
  - **覆盖写改为「临时目录 + 备份 + 原子替换」**：`new_skill.py --force` 与 `pack_skill.py` 安装不再
    `shutil.rmtree` 后重建（中途失败旧技能就没了），旧版先移到 `~/.workbuddy/skill-backups/`。
  - pip 安装加重试与国内镜像兜底：新增 `_friendly.pip_install()`，`setup.py --install-pillow` 与
    `new_skill.py` 生成的 `scripts/setup.py` 模板都改成「直连 → 裸 pip → 清华源」三路重试。
  - 新增 `audit_skill.py --selftest`：在**系统临时目录**造带病/干净两个样例验证判定与退出码，再对自身跑一遍。
  - 修 `new_skill.py`：默认占位不再用尖括号（`<30 字…>` 会让「生成即体检」每次都报两条 P1）。
- **B 组 · 降误报**（针对「体检规则较严格，有时可能误报」）：
  - `.skillignore` **真正生效了** —— 以前文档写了这个文件，代码却没读；现在支持 glob 排除文件
    与 `rule:规则名` 按规则放行，体检与打包都认。
  - 新增 `--ignore-rule`（可重复）与 `--explain <规则名>`（判什么/为什么/怎么改/怎么放行）。
  - 内置三类噪音豁免：规则表里的**字典字面量**（`"msedge.exe": "..."` 不再被判「驱动浏览器」）、
    `.git` 不再报垃圾目录、「示例/产物路径」默认折叠成一行计数（`--show-noise` 才展开）。
  - 新增 `--fix [--write]`：只补 frontmatter 缺失字段（10 项，含 `slug` 与 `agent_created`），
    写前自动备份到 `~/.workbuddy/skill-backups/<技能名>/`，绝不改正文。
- **新增 `scripts/bump.py`**：一条命令递增 version 并在版本历史顶部插记录，
  解决「改了 version 忘了写版本历史」这个高频漏项。
- **文档瘦身**：版本历史迁 `references/CHANGELOG.md`、图标流程迁 `references/icon-guide.md`、
  发布与插件形态迁 `references/publishing.md`、低频坑迁 `references/pitfalls.md`；
  正文加 30 秒 TL;DR 与退出码表。（SKILL.md 27255 → 约 15000 字符，不再踩自家「偏长」线）

### v2.2.1 (2026-09-15)

- **补「发布后核查」实战结论**（发布 v2.2.0 时实测）：
  - CLI 的发布 payload 固定只有 9 个键，**不含 `category`** —— SKILL.md 里分类改对了、
    CLI 也返回 `✓ Published`，线上分类依旧不变，**只能走网页 dashboard 改**。
  - 线上字段分三档更新：`tags` 秒级生效；`version` / `summary` / 描述 / 版本列表 / 下载包
    要等三线安全审核通过；`category` 走 CLI 永远不动。
- Step 8 新增「发布 ≠ 上线」小节：三档更新表 + 三个免登录只读状态接口
  （`/api/v1/skills/<slug>`、`/versions`、`/download`），并标出两个会踩的路径
  （`/skills/@handle/slug` → 405，`/skills/resolve?slug=` → 400）。
- 新增坑 22（以为 CLI 能改分类）、坑 23（拿 `✓ Published` 当已上线）。
- `references/checklist.md` 同步补「`category` 有第二条坑：CLI 传不了它」。

### v2.2.0 (2026-09-15)

- **修「商店里没有中文名」**：本技能发布后商店里显示英文 slug，根因是 frontmatter 写的是
  下划线 `display_name`，而**平台只认驼峰 `displayName`**。补 `slug` / `displayName` /
  `summary` / `tags` 四个平台字段；`display_name` 保留给 WorkBuddy 本机。
- **`category: development` → `dev-programming`**：`development` 不在平台 13 个枚举内，
  这是商店里显示「未分类」的原因。
- **description 三件套由 YAML 折叠块改为单行**：平台解析器只读「`key: 值`」那一行，
  `>-` 会被读成字面量 `>-`。`tags` 改内联列表写法（多行列表同样会被读空）。
- **`new_skill.py` 同步修**：生成的 frontmatter 直接就是平台可读形态（单行 + 平台字段），
  `--category` 默认值改为 `dev-programming`。
- **`audit_skill.py` 新增三项检查**：缺 `displayName` 判 P1；`description`/`tags` 等用块标量、
  `category` 不在枚举内各判 P2。
- `templates/skill-skeleton.md` 同步：字段注释改为独立成行（行尾注释会被平台读进值里）。

### v2.1.0 (2026-09-15)

- **改名 `skill-generator` → `ym-skill-generator`**：原 slug 已被他人占用（发布时被平台
  拒收「slug 'skill-generator' 已被其他用户占用」）。`name` / 目录名 / GitHub 仓库名
  **三处同步改**，保持一致，否则 `skillhub install <slug>` 会对不上。
- **更正 v2.0.1 的旧结论**：当时实测「`skill-generator` 精确名零重名」已失效。
  换用 `ym-` 前缀后，`ym-skill-generator` 等 9 个候选实测公开层面均无同名技能。
- `references/naming-and-discovery.md` 补「slug 占用怎么查」：判据是下载接口
  `GET /api/v1/download?slug=<slug>`（200 = 已被别人发布 / 404 = 公开层面无此技能）；
  两个反直觉点 —— **404 ≠ 可用**（被占用但未公开发布的同样 404），
  且**搜索接口不能判重**（`q=` 是模糊匹配，对短前缀直接返回兜底热门榜）。

### v2.0.9 (2026-09-15)

- **修发布阻断**：绑定 GitHub 仓库发布时，平台按「文件类型白名单」扫描仓库里的文件，
  技能目录里的 `.gitignore`、`.gitattributes`、`icons/*.png`、`templates/*.template`
  会让整次发布被拒（报「不支持的文件类型」）。本技能自身做了三处清理，并写进坑 18：
  - `.gitignore` / `.gitattributes` → 迁到 `.git/info/exclude` 与 `.git/info/attributes`
  - 图标不再输出到技能目录内：`make_icon.py` 默认改到 `~/.workbuddy/skill-icons/`
    （可用 `--out` 或环境变量 `SKILLHUB_ICON_DIR` 覆盖）
  - `templates/SKILL.md.template` → `templates/skill-skeleton.md`（`.template` 不在白名单）
- 「打包时排除图标」的规则**保留**（防御性），但职责已从「排除」改为「根本不该放进去」。
- 新增坑 18（非白名单文件导致发布被拒）。

### v2.0.8 (2026-09-15)

- **新增 `make_icon.py`：技能图标能力**（提示词构建 → 居中裁切 + 清生成标 → 512×512 / ≤500KB → 上传前自查）。
  - `--prompt` 按本技能 SKILL.md 的展示名与描述拼 ImageGen 提示词；`--check` 只做合规检查；
    直接传生成图则输出到技能根下的 `icons/`。
  - **图标不进技能包**：平台在创建技能时把图标当**表单字段**单独收，所以 `icons/` 打包时一律排除，
    上架时单独上传。人物头像那套（专家 `avatars/`）不适用于技能图标。
- **打包排除规则补齐**：新增「仓库元数据」（`.git/`、`.gitignore`、`.gitattributes`、`README.md`、
  `CHANGELOG.md`、`LICENSE`）与「发布图标」（`icons/`）两类排除；技能目录同时是 git 仓库时
  不再把仓库文件打进包。排除项会分类打印，不再与缓存混在一起。
- 新增坑 15（图标打进包）、坑 16（把 `.git` / `README.md` 打进包）、坑 17（拿专家头像规矩做技能图标）。
- 补 `scripts/setup.py`（环境自检 + `--install-pillow`）：图标能力带来唯一的可选依赖 Pillow，
  按本技能自己的约定（坑 6「有第三方包就给 setup.py」）补上一键安装入口。

### v2.0.7 (2026-09-15)

- 明确并验证技能上传包的最大目录深度为“技能根/二级目录/文件”；打包器继续输出扁平技能目录包，不生成插件嵌套结构。

### v2.0.6 (2026-09-15)

**修正一处根本性认知错误**。此前认为「技能上架也要 `.codebuddy-plugin/plugin.json`」，并据此把技能打成插件形态（`skills/<技能名>/SKILL.md`）——**这是错的**，照着传必被拒。官方要求的技能基础结构就是**技能目录本身**：

```
{skill-name}/
├── SKILL.md              # ★ 必须
├── references/  scripts/  templates/     # 均可选
```

**不需要**任何清单文件。平台是在技能目录根找 `SKILL.md`，按插件形态传会报「**压缩包缺少 SKILL.md 文件**」。

- **默认产出的技能目录包就是技能上传包**，原样传即可。
- `--platform` 更名 **`--as-plugin`**（旧名保留兼容）：它产出的是**插件形态**包，用于插件市场分发；上传开放平台技能类目**不要**用它。输出里已加显式告警。
- 纠正「压缩包缺少 .codebuddy-plugin/plugin.json」的归属：那是**专家 / 插件**那条上传线的报错，与技能上传无关。这条认知此前被错套在技能上。
- 文档补上官方要求的技能基础结构、frontmatter **必填字段表**（`description` / `description_zh` / `description_en` / `version` / `author`），以及技能 / 专家两条上传线的结构差异对照。

### v2.0.5 (2026-09-15)

- `--platform` 合成的 plugin.json 补 `category` 独立字段（技能上架的展示分类）。原先只把它塞进 `keywords`，平台展示位就没分类。⚠️ 技能用 `category`（字符串），专家用 `categoryId`（数字枚举），是两套规范，别串。
- 描述里触发词长尾的剥离分界词补全：新增「也适用于 / 亦适用于 / 触发词：/ 使用场景：」。此前只认「当用户说」，像「也适用于『生成专家包』这类说法」整句会残留进市场文案。
- 新增 `keywords` 取词口径说明：名字拆词 + 触发词前 6 个（category 已单独成字段，不再重复塞进去）。

### v2.0.4 (2026-09-15)
- 修引用检查误报：正文**同一行**标注了「运行时产物 / 输出文件 / 生成」等字样的路径，改判 P2 而非 P1「引用缺失」——此前写 `avatars/expert.png` 这类**运行后才生成**的文件会被判成断链，逼得用户改写文档才躲得过去
- 危险操作（P1）的提示文案补上放行办法：作用范围已收窄时在该行行尾加 `# skill-audit: ignore`——此前只说要"在 SKILL.md 说明"，但判定根本不看 SKILL.md，照着做也消不掉告警
- 回归复测 8 技能：P0/P1 无新增（P2 计数变化仅因「约定/示例路径」分桶合并）

### v2.0.3 (2026-09-15)
- 新增 `--platform`：产出**开放平台插件包**（`<技能名>-plugin.zip`），结构为 `<插件名>/.codebuddy-plugin/plugin.json` + `<插件名>/skills/<技能名>/...`
- 修「上传开放平台报 **压缩包缺少 .codebuddy-plugin/plugin.json 文件**」：平台分发单元是**插件**，技能包与本机技能包是两种形态，以前只能产出后者
- `plugin.json` 从 SKILL.md frontmatter 自动生成（`name`/`version`/`description`/`description_en`/`author`/`keywords`/`skills`），描述会剔除触发词堆砌并截断到 200 字
- 新增 `read_frontmatter()`：自解析 YAML，支持折叠块（`>-`）与列表；此前只有体检器内部有类似逻辑
- SKILL.md 新增「两种产出形态」对照表与开放平台插件结构说明
- 新增 `--flat-root`：平台包可不带顶层目录（zip 根即插件根），应对平台拒绝顶层目录的情况——两种形态无法从报错文案区分，故都保留

### v2.0.2 (2026-09-15)
- **交付标准写进流程**：终点是「本机技能目录里有一份能用的技能」，zip 只是分发副本
- `pack_skill.py` **安装改为默认行为**（原先要手动加 `--install`，导致打包完只剩一个 zip、本机没有技能），新增 `--no-install` 给"只帮别人打包"的场景；结尾固定打印「技能目录 / 分发 zip」，未安装时用 `!!` 明确告警
- `new_skill.py` 新增 `--install`：`--out` 指向技能目录之外时补装一份；结尾区分"技能已就绪"与"本机还没有这个技能"
- 防自毁保险：新增 `is_inside`，安装目标落在源目录之内时拒绝覆盖，避免原地打包自我删除
- 安装时同步创建空目录，本机副本结构与 zip 一致

### v2.0.1 (2026-09-15)
- **为上架做可发现性优化**：`display_name` 改为「技能生成器 · 生成/体检/打包」（一次覆盖三个搜索词），`display_name_en` 加 `Packager`
- `description` 扩充长尾触发说法（技能打包 / 导出技能 / 技能上架 / 技能体检 / 技能合规检查 / build skill），`description_zh` / `description_en` 补入上架、分发、publishable 等词
- `trigger` 从 13 条扩到 19 条
- 新增 `references/naming-and-discovery.md`：三层可发现性模型、词根占位实测数据（creator/maker/studio/kit/forge/foundry 均已被占，`skill-generator` 精确名零重名）、关键词穷举法、起名检查清单
- **`name` 保持不变**——实测确认它零重名，而所有候选替代词根都已被占用

### v2.0.0 (2026-09-15)
- **技能从「技能打包器」升级为「技能生成器」**：新增从一句需求生成技能的能力，名字、目录、zip 名同步改为 `skill-generator`
- 新增 `scripts/new_skill.py`：一条命令生成合规骨架（frontmatter 齐全 + 分节正文 + 按需子目录 + 自动 `scripts/setup.py` / `config/*.example.json`），**生成后自动体检**，闭环到 0 告警
- 新增 `references/generation-guide.md`：形态决策、description 写法对照、资源分层判据
- `pack_skill.py` 把**空目录**也写进 zip —— 否则刚生成的骨架解压后 `scripts/`、`references/` 会丢
- 两个脚本加 `sys.dont_write_bytecode`，运行后不再在技能目录里留 `__pycache__`
- 修体检器误报：`description` 写成 YAML 折叠块（`>-`）时被判「过短」；`description_zh` / `description_en` 同理漏检。新增 `fm_text()` 统一处理块标量
- `templates/SKILL.md.template` 的说明注释从**文件开头移到末尾**——原来照抄模板会直接触发 P0「缺 frontmatter」

### v1.0.1 (2026-09-15)
- 对齐技能市场分发规范：frontmatter 补齐 `display_name` / `display_name_en` / `description_zh` / `description_en` / `category`，`author` 改为真实署名
- 新增 `templates/SKILL.md.template`：含全套字段的技能骨架
- `audit_skill.py` 新增 `--market` 模式：第 9 类检查「市场分发」，字段定级依据实测而非规范文本
- `pack_skill.py` **默认按市场规范打包**（`--no-market` 可关），并在打包前逐项列出字段齐备情况
- 修误报：`const sid = resp.result.sessionId` 这类**属性访问**被当成明文凭据（`PROPERTY_CHAIN` 判定）
- `fm_value` 支持 `metadata:` 下的**缩进嵌套**字段

### v1.0.0 (2026-09-15)
- 首版（原名 skill-packager）：产物清点 → 边界判定 → 骨架 → 脱敏 → 体检 → 打包 → 安装 全流程
- `scripts/audit_skill.py`：8 类检查，P0/P1/P2 分级，同类问题聚合，密钥打码
- `scripts/pack_skill.py`：体检门禁 + 自动排除垃圾 + zip + 安装
- `references/checklist.md`：逐项判定标准与放行条件
- `references/sanitize-rules.md`：绝对路径与凭据的替换映射表
