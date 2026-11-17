# 打包前检查清单

逐项判定标准、修复动作、放行条件。体检脚本会自动跑这些项，本文件是给人看的判定依据与话术。

分级定义：

| 级别 | 含义 | 是否能打包 |
|---|---|---|
| **P0** | 会造成泄漏或破坏，或技能根本装不上 | 绝对不能，`--allow-p1` 也拦不住 |
| **P1** | 换台机器/换个人很可能跑不起来，或存在风险能力 | 默认拦，确认安全后 `--allow-p1` 放行 |
| **P2** | 知情项与优化建议，不影响运行 | 可以打包，建议顺手改 |

---

## 1. 结构

| 检查 | P 级 | 判定 | 修复 |
|---|---|---|---|
| 存在 `SKILL.md` | P0 | 没有就不是技能目录 | 用 `scripts/new_skill.py` 生成骨架 |
| 有 YAML frontmatter | P0 | 首行必须是 `---`（顶部放 HTML 注释也会判 P0） | 补 frontmatter，注释移末尾 |
| `name` 字段存在 | P0 | — | 补 |
| `name` 为 kebab-case | P2（`--market` 下为 P1） | `^[a-z0-9][a-z0-9-]*$` | 本机自用不必改；要发布就改成小写连字符 |
| `name` 与目录名一致 | P2 | — | 安装/升级按目录名定位，建议对齐 |
| `description` 存在 | P0 | 支持单行标量，也支持 `>-` 折叠块（`fm_text()` 会把块拼起来判）；**但平台解析器认不出折叠块**，要发布就写单行 | 补 |
| `description` 无 `<` `>` | P1 | 打包校验会直接失败 | 换方括号或中文书名号 |
| `description` ≥ 30 字符 | P2 | 折叠块按拼接后的长度算 | 写清「做什么 / 何时用 / 触发词」 |
| 有 `agent_created: true` | P2 | — | 补上，否则后续无法用 skill_manage 修改 |
| SKILL.md ≤ 15000 字符 | P2/P1 | 超 30000 记 P1 | 细节迁到 `references/`，正文只留流程 |

## 2. 绝对路径

**为什么重要**：技能会被解压到别人的机器上。写死盘符、用户名、内网盘，换台机器直接崩。

| 形态 | 例子 | P 级（代码/文档） |
|---|---|---|
| Windows 盘符 | `C:` 开头的完整路径 | P1 / P2 |
| UNC 共享 | 双反斜杠开头的网络路径 | P1 / P2 |
| POSIX 家目录 | `/home/...`、`/Users/...`、`/root/...` | P1 / P2 |

修复原则：**代码用动态定位，文档用占位符**。映射表见 `sanitize-rules.md`。

**允许保留的例外**（属于合理默认值，不是硬编码）：

- 系统目录的兜底值，如取临时目录时回退到系统 Temp（记 P1 提示，人工确认）
- 探测浏览器/工具候选路径列表（本就该多候选遍历）

放行方式：脚本文件（`.py` / `.js` / `.sh`）行尾加放行标记并注明理由。
**`.md` 文档禁用注释形式** —— 渲染后不可见，第三方安全审计会判为提示注入；改用技能根的
`.skillignore` 写 `rule:规则名`，并在正文显式说明理由。

## 3. 凭据

**为什么重要**：一条 `password = "..."` 泄漏的可能不只是这个技能能用的账号。

| 判定 | P 级 |
|---|---|
| 高置信度密钥字面量：JWT、`sk-` 前缀、`AKIA` 前缀、`ghp_` 前缀、私钥块 | P0 |
| 敏感关键字（password/secret/token/密码/密钥…）后跟**写死的字面量** | P0（代码）/ P1（文档） |
| 敏感关键字后跟**变量、函数调用、环境变量** | 不报（这才是正确写法） |
| 配置模板里出现高置信度密钥 | P0 |
| 文档里的字段示例（如密码字段示例值） | P2 |

**不会误报的边界**：`hasPwd: !!document.querySelector(...)`、`password = args.password or ''`、`password = p1` 这类**不是写死字面量**的写法一律不报——只看字面量。

修复动作（三步，别只做第一步）：

1. 把值从文件里删掉，改成从配置文件或环境变量读取
2. 补一份 `config/xxx.example.json`，字段留全、敏感值留空
3. 真值落到 `~/.workbuddy/<name>_config.json`，并确认该路径不会被一起打包

> 若值已经提交到过远程仓库或发给过别人，必须**轮换该凭据**，改代码不解决问题。

## 4. 危险操作

| 判定 | P 级 |
|---|---|
| 递归删除根目录/家目录、格式化盘符、批量强删 | P0 |
| 远程脚本直接灌进 shell | P0 |
| `eval`/`exec` 外部输入 | P0 |
| 写系统关键文件 | P0 |
| `shutil.rmtree` 等递归删目录 | P1 |
| 引用系统目录（清理临时文件等） | P1 |
| 终止进程 | P1 |

P1 类的处理不是删掉，而是**把范围讲清楚**：SKILL.md 里写明「只会清理什么、绝不碰什么」。例如只 kill 本进程自己拉起的子进程、拒绝杀已有会话。

## 5. 外部依赖

| 判定 | P 级 |
|---|---|
| 存在第三方 Python/Node 包 | P2（列出包名，提醒写安装命令） |
| 有第三方包但无 `scripts/setup.py` 也无 `package.json` | P1 |
| 依赖外部可执行文件（ffmpeg、edge-tts、浏览器、OCR…） | P1 |
| 使用中文字体渲染 | P1 |
| 大文件 > 5MB | P1 |

要求写进 SKILL.md 的「运行前提」三件事：**怎么装、怎么检测、缺了会怎样**。

## 6. 数据模板

| 判定 | P 级 |
|---|---|
| `config/` 有配置文件但没有 `.example` 模板 | P1 |
| 模板里出现真实凭据 | P0 |
| SKILL.md 未说明配置/数据的存放位置 | P2 |

模板的价值在于：别人 `cp` 一下就懂该填什么。字段名 + 注释留全，值一律留空。

## 7. 引用完整性

提取 SKILL.md 与 `references/*.md` 里的四类引用并校验存在性：

1. Markdown 链接 `[文字](路径)`
2. 反引号包裹的带扩展名路径
3. 命令里的脚本路径（`python scripts/xxx.py`）
4. 反引号包裹的目录型路径（`scripts/...`、`config/...`）

| 情况 | P 级 |
|---|---|
| 带目录分隔符且找不到 | P1（真·断链） |
| 同一行标注了「运行时产物 / 输出文件 / 生成」等字样 | P2（`OUTPUT_HINT_RE` 命中，视为产物） |
| 裸文件名且全技能递归找不到 | P2（大概率是运行时产物，标注一下即可） |
| 有 `scripts/`、`references/`、`assets/`、`templates/` 但正文没提 | P2 |

放行技巧：若是运行时产物，在**同一行**显式写成「输出文件 `xxx.json`」或「运行时产物」，判读时就不会被当成断链。
注意标注必须与路径**同行**——写在前一行不起作用。

## 8. 体积与垃圾

| 判定 | P 级 |
|---|---|
| `__pycache__`、`node_modules`、`.venv`、`dist`、`.git` 等目录 | P2（打包时自动排除） |
| `.pyc`、`.log`、`.tmp`、`.bak`、`.swp` | P2 |
| 疑似运行时数据目录（`profile`、`output`、`logs`、`cache`、`user_data`…） | P2 |
| 单文件 > 5MB | P1 |

前三类记 **P2 而非 P1**，原因是打包脚本本来就会自动排除它们；判 P1 只会让 `__pycache__` 把打包自己挡住（体检脚本一跑就会生成它）。

排除规则写在 `pack_skill.py` 的 `JUNK_DIRS` / `JUNK_SUFFIX` / `REPO_META_*` / `ICON_DIRS`，分三类：

| 类别 | 内容 | 为什么排除 |
|---|---|---|
| 构建缓存 | `__pycache__`、`node_modules`、`.venv`、`*.pyc`、`*.log` | 与运行无关，且体积白占 |
| **仓库元数据** | `.git/`、`.gitignore`、`.gitattributes`、`README.md`、`CHANGELOG.md`、`LICENSE` | 只对 git / 托管平台有意义，进包既没用又可能漏出仓库信息 |
| **发布图标** | `icons/` 下的图标 | 图标是平台创建技能时**单独收的字段**，不是 zip 里的文件 |

技能目录常常同时是一个 git 仓库 —— 后两类是这种情况下最容易顺手打进去的东西。

## 9. 市场分发（`pack_skill.py` 默认检查；`audit_skill.py` 需加 `--market`）

**为什么单列一类**：第 1~8 项管的是「换台机器能不能跑」，这一项管的是「能不能上架」。字段不全在平台侧会被直接打回。

> **官方对「技能上传」的硬要求**（注意：这**不是**插件规范）
>
> - 包结构必须是 **`{skill-name}/SKILL.md`** + `references/` + `scripts/` + `templates/`，
>   **不需要** `.codebuddy-plugin/plugin.json`。打成 `skills/<技能名>/SKILL.md` 那种插件形态，
>   平台在技能目录根找不到 SKILL.md，会直接报「**压缩包缺少 SKILL.md 文件**」。
> - frontmatter **必填**：`description` / `description_zh` / `description_en` / `version` / `author`，
>   展示名还要给驼峰 **`displayName`**（下划线 `display_name` 平台不认，缺了商店里显示英文 slug）。
> - 「压缩包缺少 .codebuddy-plugin/plugin.json」是**专家 / 插件**那条上传线的报错，与技能无关。

| 字段 | 何时必填 | P 级 | 修复 |
|---|---|---|---|
| `description_zh` | 要分发 | P1 | 补一句话中文介绍，30 字以内 |
| `description_en` | 要分发 | P1 | 补一句话英文介绍 |
| `version` | 要分发 | P1 | 语义化版本号，如 `1.0.0` |
| `displayName` | 要分发 | P1 | 平台（SkillHub）的商店展示名，**驼峰**；缺了商店显示英文 slug |
| `display_name` / `display_name_en` | 建议 | P2 | **WorkBuddy 本机**的展示名（平台不读这两个） |
| `slug` | 建议 | P2 | 平台发布 CLI 必填（`SKILL.md 缺少 slug`），与 `name` 一致 |
| `summary` | 建议 | P2 | 商店列表摘要，一般复用 `description_zh` |
| `category` | 建议 | P2 | 分类之一，须落在平台 13 个枚举内（见 `SKILLHUB_CATEGORIES`） |
| `author` | 建议 | P2 | 署名；也可写在 `metadata:` 之下 |

**平台的解析规则比 YAML 更窄**（实测 SkillHub 自带 CLI）：

| 检查 | P 级 | 说明 |
|---|---|---|
| `description` / `summary` / `tags` 用 `>-` 块或 `- 项` 多行列表 | P2 | 平台只读「`key: 值`」那一行：`>-` 读成字面量 `>-`，多行列表读成空 |
| `category` 不在 13 个枚举内 | P2 | 不报错，但上架后显示「未分类」 |
| frontmatter 里有行尾 `#` 注释 | P2 | 平台不剥注释，会被拼进字段值；注释一律独立成行 |

所以：**长文本折成一行 + 列表用 `[a, b]`**。这对完整 YAML 解析器同样合法，两边都安全。

另外四项校验：

| 检查 | P 级 | 说明 |
|---|---|---|
| `name` 非 kebab-case | P1 | 市场要求小写字母+数字+连字符 |
| 展示类字段含 `<` `>` | P1 | 与 `description` 同源地导致校验失败 |
| 中英文介绍语言不匹配 | P2 | 中文介绍里没中文、英文介绍混进中文 |
| `author` 仍是机器默认值 | P2 | 如 `WorkBuddy AI Assistant`，应改真实署名 |

**定级依据是实测，不是规范文本**：本机 4 个真实市场技能里 `description_zh` / `description_en` 是 4/4 都有，`display_name` 3/4，`category` 2/4，`author` 只有 1/4（且写在 `metadata:` 之下）。所以只有前两个定 P1 阻断，其余一律 P2。照抄规范表格的"必填"会把大多数已上架技能判成不合格。

**例外是 `displayName`（定 P1）**：判据不是"规范说必填"，而是**它的缺失是静默的** —— 发布成功、不报任何错，只是商店列表里显示英文 slug。`description_zh` 那类缺了顶多少句介绍，`displayName` 缺了是"我的技能没有中文名"，必须拦。同理，块标量被平台读成 `>-`、`category` 落到「未分类」也都是静默失败，所以各加一条 P2 提示。

> ⚠️ **`category` 有第二条坑：CLI 发布根本传不了它。**
> SkillHub CLI 的发布 payload 固定只有 `slug` / `version` / `displayName` / `summary` /
> `description` / `tags` / `license` / `homepage` / `changelog` —— **没有 `category`**。
> 所以「SKILL.md 里分类填对了」只保证**体检能过**，**不保证线上分类会对**，改分类只能走网页 dashboard。
> 发布后复核：`GET /api/v1/skills/<slug>` 看 `skill.category`。
>
> 同理，**`✓ Published` ≠ 已上线**：`tags` 秒级生效，`version` / `summary` / 描述 / 版本列表 /
> 下载包要等三线安全审核通过才写进 `latestVersion`。发完立刻看商店「没变化」属正常，
> 先查 `GET /api/v1/skills/<slug>/versions` 确认新版本号在不在列表里。

> ⚠️ 但官方文档把 `version` / `author` 也列为**必填**。实测有已上架技能缺 `author`，
> 说明解析阶段未必强卡；**一旦上传被字段校验拦下，先把这 5 个必填补齐再传**。
> `version` 已按 P1 处理，`author` 暂居 P2。

**默认开关为什么两套**：`pack_skill.py` 打包时默认跑（打包往往是分发的第一步），要跳过就 `--no-market`；`audit_skill.py` 默认不跑，上架前才 `--market`。若两边都默认开启，体检任何老技能都会满屏告警，工具就没人用了。

**包结构对了，还差一张图**：平台创建技能时另要一张**图标**（512×512、PNG/JPG、≤500KB）。
它是表单字段，**不在 zip 里**，用 `make_icon.py` 单独生成、上架时单独上传：

```bash
python scripts/make_icon.py --prompt        # 拿提示词 → 交给 ImageGen（1024×1024）
python scripts/make_icon.py <生成图>        # 居中裁切 + 清生成标 + 512×512 + ≤500KB
python scripts/make_icon.py --check icons/*.png   # 上传前自查
```

图标不进包（`icons/` 已被打包器排除），也不做体检 —— 规格对不对由 `--check` 判。

---

## 10. 生成期检查（生成模式专属，人工过）

体检只覆盖「合规」，下面这些决定「好不好用」，脚本管不了：

| 检查 | 判据 |
|---|---|
| 形态选对 | 需要精确复现的写了脚本；一句祈使句能说清的不写脚本。判据见 `generation-guide.md` §1 |
| `description` 三件事齐备 | 做什么 / 边界（不做什么）/ 触发词 |
| 触发词是用户原话 | 用户会说「查待办」，不会说「获取待办事项列表」 |
| 中英文介绍另行撰写 | `description_zh` 不是 `description` 的复制粘贴 |
| 占位全部替换 | 正文里 `<...>` 一个不剩 |
| `scripts/setup.py` | 有第三方依赖就必须有（`new_skill.py --deps` 自动生成） |
| `config/*.example.json` | 有配置就必须有，字段留全、值留空 |
| 「常见坑」非空 | 至少 1 条真实踩过的坑：现象 + 原因 + 规避 |

设计取舍细节见 `references/generation-guide.md`。

---

## 打包门禁

```
P0 存在        → 中止，逐条修
P0 无、P1 存在  → 中止，修完重跑；确认安全可 --allow-p1
P0/P1 均无      → 通过，可打包（P2 建议顺手处理）
```

> `pack_skill.py` **默认按 `--market` 运行**，所以上表 P1 里也包含「市场分发字段缺失」。
> 只想本机自用、不在乎上架时加 `--no-market`，第 9 项完全不参与判定。

## 安全项放行

```bash
# 单行放行（要写理由）
PROBE_PATHS = ["C:\\Program Files\\Edge\\msedge.exe"]  # skill-audit: ignore 浏览器探测候选

# 整文件放行：技能根目录建 .skillignore，每行一个 glob
references/internal-endpoints.md
assets/generated/*
```
