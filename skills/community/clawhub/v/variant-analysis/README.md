# 亚马逊变体分析 · 颜色尺寸口碑对比

颜色尺寸规格口碑对比，揪出拖分变体

> **亚马逊变体分析 · 颜色尺寸口碑对比**
> 技术名 `amazon-variant-analysis`，ARI 官方出品的 Amazon 评论采集与消费者洞察 Skill，已适配 WorkBuddy。
> 安装后直接用中文描述需求即可，无需理解 API 或编写代码；所有付费操作都会先报价，
> 只有你明确确认后才会扣除积点。

## 能做什么

- 订阅 ASIN、采集评论，查看星级 / 关键词 / 趋势 / 流向等免费图表数据。
- 生成 **VOC**、**深度洞察**、**趋势**、**变体**、**竞品对比** 五类 AI 分析报告。
- 输出痛点、购买动因、用户画像、使用场景、改进机会与 Listing 建议。
- **差评预警**（差评突增自动提醒）与**差评工作台**（AI 生成回复/申诉建议）。
- **行业对标**（类目星级/差评率位置）与付费**类目排行**。
- 评论一键导出 **CSV**，报告导出 **Markdown / HTML**（付费套餐功能）。

安装后直接以自然语言提需求：

```text
使用 $amazon-variant-analysis 为 ASIN B0XXXXXXXX 生成 VOC 报告，站点 amz_us，我确认扣积分。
```

## 前置条件

- **Python 3**（只用标准库，无第三方依赖）。
- 一个 **ARI API Key**（`ari_live_` 开头）。首次使用运行
  `python scripts/ari.py setup`，在浏览器登录或注册后点一下「授权」，
  Key 会自动写入本机，无需手工复制粘贴。
  也可在 <https://ari.funewa.com/zh/account?ui=d47626f#api-keys> 手动创建。

## 安装到 WorkBuddy

保持文件夹名 `amazon-variant-analysis`，整个放进对应作用域即可：

| 作用域 | 路径 |
|---|---|
| 用户级（推荐） | `~/.workbuddy/skills/amazon-variant-analysis/` |
| 项目级 | `<项目目录>/.workbuddy/skills/amazon-variant-analysis/` |

装好后验证账户与积点余额：

```bash
python <SKILL_DIR>/scripts/ari.py check
```

> `<SKILL_DIR>` 是 WorkBuddy 加载 Skill 时自动替换的目录占位符；直接在终端跑时，
> 请先进入 Skill 目录，或把它换成实际路径。

Key 运行时从 `ARI_API_KEY` 或 `~/.ari/config.json` 读取——**切勿**提交进仓库，
也不要把 Key 贴进公开文档或发给他人。

## 命令一览

| Command | 作用 | 扣积点 |
|---|---|---|
| `setup` / `configure` | 部署 API Key | 否 |
| `check` | 账户与余额 | 否 |
| `products` | 已订阅 ASIN 列表 | 否 |
| `voc` | 自动采集 + VOC + 归档 + 报告链接 | **是，需 `--confirm`** |
| `collect` | 提交采集任务 | **是，需 `--confirm`** |
| `status` | 采集任务进度 | 否 |
| `reviews` | 读取已采集评论 | 否 |
| `charts` | 星级 / 趋势 / 关键词 / 流向 | 否 |
| `quote` | 分析报价 | 否 |
| `analyze` | voc / insight / trend / variant / compare | **是，需 `--confirm`** |
| `deepdive` | 产品 + 图表 + 评论 + 报告 + VOC 报价 | 默认否，`--confirm` 才分析 |
| `reports` / `report` | 历史报告列表 / 详情 | 否 |
| `alerts` | 差评/星级预警 | 否 |
| `benchmark` | 类目对标概览 | 否 |
| `leaderboard` | 类目排行 | **是，需 `--confirm`** |
| `workbench` | 差评列表 / 建议存档 / 状态流转 | 否 |
| `advise` | 单条差评 AI 回复建议 | **是，需 `--confirm`** |
| `export` | 评论 CSV / 报告 MD·HTML 导出 | 否（限付费套餐） |

`python scripts/ari.py <command> --help` 看完整参数。默认站点 `amz_us`，
另支持 `amz_uk / amz_de / amz_jp / amz_ca / amz_fr / amz_es / amz_it`。

## 扣费保护

采集与 AI 分析消耗积点。付费命令（`voc`、`collect`、`analyze`、付费 `deepdive`）**必须**
显式追加 `--confirm` 才真正执行，不带时只返回报价。

- **非美国站只能用付费积点。** 采集 `amz_uk` / `amz_de` 等站点时赠送积点不可用，
  以 `collect` 报价里的 `usableBalance` / `sufficient` 为准，别看账户总余额。
- **付费命令中断后不要直接重跑。** 出现 `ARI_STREAM_INTERRUPTED` / `NETWORK_ERROR` /
  `WAIT_TIMEOUT` 时服务端可能已扣点并归档，先用免费的
  `reports --asin <ASIN> --limit 1` 核对，确认没生成再重试。
- **聚合命令部分失败体现在最外层。** `charts` / `deepdive` 任一子请求失败时返回
  `success:false` 并附 `failedParts`，成功的部分仍在 `data` 里，只能用这部分。

## 目录结构

```
SKILL.md               # Skill 清单 + 操作指令（WorkBuddy 规范）
README.md              # 本文件
使用说明.md             # 中文终端用户指南
scripts/ari.py         # 仅依赖标准库的 CLI
references/reference.md# CLI 与 API 参考（命令 / 字段 / 错误码）
agents/openai.yaml     # 其他客户端的接口元数据（WorkBuddy 不使用，保留以兼容多端）
```

## 常用入口

- API Key：<https://ari.funewa.com/zh/account?ui=d47626f#api-keys>
- 充值套餐：<https://ari.funewa.com/zh/billing>
- 产品管理：<https://ari.funewa.com/zh/products>
- 报告中心：<https://ari.funewa.com/zh/reports>
- 新用户注册即赠积点，免费额度可通过任务中心持续解锁：
  <https://ari.funewa.com/zh/tasks>
