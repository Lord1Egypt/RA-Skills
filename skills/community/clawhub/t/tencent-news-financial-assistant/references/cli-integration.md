# tencent-news-cli 接入说明（股票行情）

目标技能：`tencent-news-financial-assistant`。最近核实：**2026-10-20**。核实方式：下载两个渠道的 `linux-amd64` 二进制到临时目录，与各自 `checksums.txt` 逐字比对后执行 `version` 与 `help`。本文只记录已核实内容，未执行的部分单独标注。

## 1. 工具与来源

| 项目 | 内容 |
| --- | --- |
| 可执行名称 | `tencent-news-cli`（Windows 为 `tencent-news-cli.exe`） |
| 本次依赖的能力 | `stock` 命令组，子命令 `quote` |
| 用途 | 股票行情查询，支持自然语言查询个股实时与历史行情 |
| 数据来源 | Neodata（命令自行查询数据源 `source_id`，调用方无需传入） |
| 适用系统 | macOS（Apple Silicon / Intel）、Linux（x64 / ARM64）、Windows x64 |

技能不直接调用二进制：除 `cli-state` 外，全部通过共享脚本 `scripts/run-cli.sh` / `scripts/run-cli.ps1` 执行，脚本按技能元数据注入 `--caller`，调用时不要重复传入该参数。

## 2. 新增能力（cli.mode: new）

- **变化范围**：`v1.0.17` 及更早版本没有任何金融类子命令（`help` 仅含 hot / search / morning / evening / weather / gaokao / sport / jiaozhen / knowledge 等）。`v1.0.18` 新增 `stock` 命令组，当前仅 `quote` 一个子命令。本技能依赖的就是这一新增能力。
- **实现来源**：test 渠道 `v1.0.18` 构建。首次核实（2026-10-20）为 `build_date` `2026-10-19T19:17:10`、`linux-amd64` SHA-256 `0cbd95c991c702c7e69a41f69d0553f2763d528e9ebf20601a08361444c94e1a`；2026-10-28 强制更新后构建已更换为 `build_date` `2026-10-28T11:33:51`、SHA-256 `cdedb08d1b48a7c66f02493629f514fc6ff7530883b6e4ae073e03635e0c80b1`（版本号仍为 `v1.0.18`，与 test `checksums.txt` 中 `linux-amd64/tencent-news-cli` 一行一致）。**版本号未变但构建已变，只能按哈希与 build_date 判断**。CLI 源码仓库的 MR / 提交位置尚未提供，待 CLI 维护人补充后回填 `skill.json` 的 `cli.changeRef`。
- **可用状态**：
  - **test**：已发布，最低支持版本 `v1.0.18`。
  - **formal**：**未发布**。2026-10-20 核实时 formal 渠道仍为 `v1.0.17`（`build_date` 为 `2026-10-12T16:22:38`，SHA-256 `3a6f4d9e137472342f0a5c56902c6022fe90718e5850e182fb1a54d3b1e2f2ff`），其 `help` 中**没有** `stock` 命令。面向正式环境前需重新核实该渠道是否已升级到含 `stock` 的构建。
- **返回类型由语义路由**：`stock quote` 是唯一入口，实测同一命令既能返回个股行情（A 股、港股），也能返回美股主要财务指标（2026-10-20 实测「苹果公司最新财报关键指标」返回 `2026-Q3` 主要财务指标表）。因此本技能不按"财务指标不支持"来拦截，而是如实按实际返回处理。
### 六类需求类别实测结果（2026-10-20，test `v1.0.18`）

需求表格里的类别在 `help` 中没有独立命令，全部走 `stock quote` 由语义路由返回。实测结论：

| 需求类别 | 实测查询 | 实际返回 | 是否等于需求口径 |
| --- | --- | --- | --- |
| 公司公告 | 梳理拼多多最近发布的公告 | 「重大事件获取V2」表，字段为大事类型/分类（财务披露、分红送配、股权变动等）/事件日期/标题/描述/事件特有字段 JSON | **不等同**：是重大事件，不是公告原文 |
| 股本股东 | 京东的股本股东情况 | 摘要行写「京东(JD.US) 股东与机构持仓」，但未返回持仓明细表，直接接资讯段落 | **部分命中**：类别识别正确，本次无明细数据 |
| 指数行情 | minimax的指数行情 | MINIMAX-W(00100.HK) 个股行情明细（开盘/最高/最低/收盘/涨跌幅等） | **不等同**：查询词是股票名时被当作个股处理 |
| 大盘统计 | 蜜雪冰城的大盘统计 | 「蜜雪冰城概念(02GN2359.PT)」概念指数行情，市场标识为「指数」，含历史 K 线 | **不等同**：是概念指数行情，不是市场成交量额、涨跌分布、涨跌停统计、融资融券概况 |
| 公司基础信息 | 给我介绍下特斯拉这家公司的公司基础信息 | 「TSLA.US 特斯拉 公司信息」：基础信息（市场、英文名称）、上市与证券信息（上市日期 2010-06-29、状态）、业务信息（公司简介、主营业务） | **一致**：与需求「公司概况、上市信息、主营业务及所属行业」口径吻合 |
| 业绩发布会 | 腾讯Q3的业绩发布会何时开？ | 腾讯控股 00700.HK 历史 K 线表，多行「未开盘」空值，无任何发布会时间或内容 | **未命中**：退化为行情查询，需求口径（发布会完整内容与业绩解读）未覆盖；需求表格中该类也只列 A 股 2014 年至今 |

结论：六类中只有**公司基础信息**与所问口径一致；公告、指数行情、大盘统计返回的是近似数据，股本股东类别识别正确但无明细，业绩发布会未命中。返回值随语义路由变化，**除公司基础信息外没有稳定契约**。技能中的处理是照常调用、核对返回的表头与说明、如实说明实际返回内容，不用行情或财务数据冒充用户所问的类别。

## 3. 安装与版本

| 平台 | 安装命令 |
| --- | --- |
| macOS / Linux | `curl -fsSL https://mat1.gtimg.com/qqcdn/qqnews/cli/hub/tencent-news/setup.sh \| sh` |
| Windows PowerShell | `irm https://mat1.gtimg.com/qqcdn/qqnews/cli/hub/tencent-news/setup.ps1 \| iex` |

核实版本与能力：

```sh
sh scripts/run-cli.sh version          # 查看 current_version / build_date / 下载来源
sh scripts/run-cli.sh help             # 确认命令列表中是否包含 stock
sh scripts/run-cli.sh help stock       # 查看命令组用法
```

`help` 中没有 `stock` 即表示当前版本不支持行情查询，需要先更新到 `v1.0.18` 及以上。

**test 环境更新注意**：截至 2026-10-15 的仓库 Wiki 记录，test 安装脚本内部的默认下载地址与校验清单仍指向 `hub`（正式）渠道，因此不能只替换脚本 URL 就当作测试安装。测试环境请使用 test 渠道二进制并对照 test 的 `checksums.txt` 校验；`version` 返回的 `download_urls` 仍指向 `/hub/` 时，不要把它当作测试构建升级。

## 4. 下载渠道

| 项目 | formal（正式 / hub） | test（测试） |
| --- | --- | --- |
| CDN 根地址 | `https://mat1.gtimg.com/qqcdn/qqnews/cli/hub` | `https://mat1.gtimg.com/qqcdn/qqnews/cli/test` |
| SHA-256 清单 | `https://mat1.gtimg.com/qqcdn/qqnews/cli/hub/checksums.txt` | `https://mat1.gtimg.com/qqcdn/qqnews/cli/test/checksums.txt` |
| Linux x64 二进制 | `.../hub/linux-amd64/tencent-news-cli` | `.../test/linux-amd64/tencent-news-cli` |
| API Key 获取页 | `https://news.qq.com/exchange?scene=appkey` | `https://test.news.qq.com/exchange?scene=appkey&testApi=1` |
| API Key 消耗流水 | `https://news.qq.com/exchange?scene=points` | `https://test.news.qq.com/exchange?scene=points&testApi=1` |

测试链接必须保留 `testApi=1`；移除后使用的是正式环境 Key。校验时用清单中的完整相对文件名精确匹配（如 `linux-amd64/tencent-news-cli`），不要用 formal 的校验值验证 test 文件。

## 5. 身份与配置

- 通过 `apikey-set` / `apikey-get` / `apikey-clear` 配置 API Key，`run-cli` 脚本会转发这些子命令。
- Key 写入用户本地 shell 配置：SHELL 为空读 `~/.profile`，bash 读 `~/.bash_profile`，zsh 读 `~/.zshrc`。
- 本文与技能包不保存任何实际 Key；技能不得索要、回显或记录 Key。
- 行情查询会消耗账户积分，测试环境积分不足时联系 `tatianasun` 并提供账号的 `news_suid`。

## 6. 调用契约

以下来自 2026-10-20 读取的 `help stock` 与 `help stock quote`（test 渠道 `v1.0.18`）：

```
tencent-news-cli stock quote [查询内容] [flags]
```

| 输入 | 类型 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| 位置参数 | string | 二选一 | 无 | 查询内容，例如 `腾讯控股今天行情` |
| `--query` | string | 二选一 | 空 | 查询内容，例如 `"今天腾讯股价多少"` |
| `--format` | string | 否 | `text` | `text`（默认，可直接阅读）或 `json` |
| `--app-id` | string | — | — | **已于 2026-10-28 构建中移除**：该构建 `help stock quote` 不再列出此参数（2026-10-19 构建曾提供，默认按编译环境取值 `app-a7e9c6c3`）。不要传已移除的参数 |
| `--score-threshold` | float | 否 | `0.2` | 最低相关度分数阈值 |
| `--top-k` | int | 否 | `10` | 最大召回条数 |
| `--caller` | string | 否 | 由 `run-cli` 注入 | 技能名称，用于上报，调用方不要手动传 |

- 命令会自动查询应用绑定的 Neodata 数据源 `source_id` 并携带该值发起查询，调用方**不要**自行构造或传入 `source_id`。
- 帮助中的典型用法：`tencent-news-cli stock quote --query "今天腾讯股价多少"`、`tencent-news-cli stock quote 腾讯控股今天行情`。

## 7. 输出契约与失败处理

- **成功输出（`--format text`）**：分段 markdown，退出码 0。实测结构为：
  1. `## 股票行情` 标题；
  2. 一行摘要，例如「腾讯控股(00700.HK) 2026-10-20 行情（实时+历史K线）：收盘价 411.400、涨跌幅 -1.53%、涨跌额 -6.400、成交额 5847103560.90元」；
  3. 标的明细表，行情类为「日期 / 开盘 / 最高 / 最低 / 收盘·最新 / 前收 / 涨跌额 / 涨跌幅 / 振幅 / 成交量 / 成交额 / 换手率 / 量比」，财务指标类为分组的「指标 / 数值」表（基本信息与口径、盈利与经营等）；
  4. 若干条附带「财经资讯」（发布时间、类型、链接、正文）。
  输出末尾附带 `请求 traceid: ...`，属内部信息，不展示给用户。
- **需要解析的字段**：标的名称、代码与市场、日期、用户所问核心指标（行情为收盘/最新价与涨跌幅，财务为对应报表指标），以及开盘、最高、最低、成交量、成交额等；缺失字段直接省略，不臆造。
- **其他表类型**：重大事件类返回「大事类型中文名称 / 大事分类 / 事件日期 / 大事标题 / 大事描述 / 事件特有字段（JSON 字符串，需二次解析）」表；指数与概念类返回市场标识为「指数」的行情表。摘要行会写明标的代码、名称与数据类型，是判断返回是否匹配问题的主要依据。
- **`--format json`（2026-10-20 实测）**：退出码 0，结构为 `code` / `msg` / `data.code` / `data.msg` / `data.suc` / `data.traceId` / `data.data.apiData.apiRecall[]`，其中 `apiRecall[]` 元素为 `content`（仍是 markdown 文本，与 text 格式内容一致）、`desc`、`tag`、`type`，另有 `data.data.entity[]` 给出标的代码等信息。即 **json 只是把同一段 markdown 包进结构化信封，不是逐字段的结构化行情数据**。
- **常见错误**：
  - `unknown command` / `help` 中无 `stock` → 版本过低，更新到 `v1.0.18` 及以上。
  - `invalid api key`、`unauthorized`、`401`、`403` → Key 无效或无权限，重新获取正确 Key，不要归因为无数据或网络问题。
  - `permission denied` → `chmod +x <cliPath>`。
  - 超时或安全软件拦截 → 按 SKILL.md「CLI 执行失败处理」引导用户处理。
- **失败后不要重试换方式**，也不要改用 WebSearch 等外部数据源补做查询。

## 8. 操作影响

- 只读取数据，不写入业务数据、不发消息、不发布内容。
- 每次调用消耗账户 API 积分；避免对同一标的同一问题重复调用。
- 不提供投资建议，不产生交易行为。

## 9. 最小调用

变量 `<QUERY>` 为用户的自然语言问题，例如 `今天腾讯股价多少`：

```sh
# macOS / Linux
sh scripts/run-cli.sh stock quote --query "<QUERY>"

# Windows
powershell scripts/run-cli.ps1 stock quote --query "<QUERY>"
```

预期：`--format text` 下返回该标的的行情文本（含最新价、涨跌幅等）；若帮助中参数有变化，以当次 `help stock quote` 为准。

## 10. 验证证据

| 项目 | 结果 |
| --- | --- |
| 核实时间 | 2026-10-20 |
| test 构建（2026-10-28 强制更新后） | `v1.0.18`，`build_date` `2026-10-28T11:33:51`，`linux-amd64` SHA-256 `cdedb08d…80b1`，与 test `checksums.txt` 一致；`stock` / `stock quote` 仍在，`--app-id` 已移除 |
| test 构建（最初核实） | `v1.0.18`，`build_date` `2026-10-19T19:17:10`，`linux-amd64` SHA-256 `0cbd95c9…4e1a` |
| formal 构建 | `v1.0.17`，`build_date` `2026-10-12T16:22:38`，`linux-amd64` SHA-256 `3a6f4d9e…f2ff`，与 hub `checksums.txt` 一致；`help` 无 `stock` |
| 已执行 · 业务调用 | 3 条展示 examples（2026-10-20，test `v1.0.18` + 测试 Key，均退出码 0）：腾讯控股 → 港股 00700.HK 行情表；贵州茅台 → 沪市 600519.SH 行情表；苹果 → AAPL.US 2026-Q3 主要财务指标表 |
| 已执行 · 类别实测 | 6 类需求场景两轮真实调用，均退出码 0：2026-10-20 在 `build 2026-10-19` 构建上首次实测；2026-10-28 在 `build 2026-10-28`（sha256 `cdedb08d…`）构建上重跑，**六类结论与首轮完全一致**（拼多多公告 → 重大事件表；京东股本股东 → 股东与机构持仓标题但无明细；minimax 指数行情 → MINIMAX-W 个股行情；蜜雪冰城大盘统计 → 蜜雪冰城概念指数行情；特斯拉公司基础信息 → 公司概况/上市信息/业务简介，口径一致；腾讯 Q3 业绩发布会 → 退化为历史 K 线，无发布会数据）。结论见上文表格 |
| 已执行 · 输出格式 | `--format json` 实测退出码 0，返回 `data.data.apiData.apiRecall[].content` 内的 markdown |
| 已执行 · 渠道与平台 | 两个渠道 `checksums.txt` 与二进制哈希比对；`version`、`help`、`help stock`、`help stock quote`；test 渠道 5 个平台二进制下载后逐字校验全部 MATCH；darwin / windows 二进制静态检查均含 `stock` 命令字符串 |
| 未执行 | darwin / windows / linux-arm64 二进制**无法在本机（Linux amd64）运行验证**：执行返回 `cannot execute binary file: Exec format error`，退出码 126；这些平台只完成下载校验与静态检查。formal 渠道 2026-10-20 复核仍为 `v1.0.17`（`linux-amd64` SHA-256 `3a6f4d9e…f2ff`，与首次读取一致），无 `stock`，未做业务调用（正式 Key 亦未配置）。公司基础信息、业绩发布会两类未实测 |

## 11. 维护联络

| 事项 | 联系人 |
| --- | --- |
| CLI 使用或实现问题（含 `stock` 命令与源码变更位置） | `quonliu` |
| Skill 搭建问题、本仓库 MR 的 review 与合入 | `corinli` |
| 测试环境 API Key 增加积分 | `tatianasun`（提供账号 `news_suid`） |

技能负责人见 `skill.json` 的 `owners`；维护联络不等于授权自动发送消息。
