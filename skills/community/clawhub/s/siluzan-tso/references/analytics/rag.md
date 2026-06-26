# rag：知识库检索（TSO 广告投放辅助）

知识库管理页面在 https://www.siluzan.com/knowledge-base/

为 **广告投放、账户分析、拓词、诊断报告** 等 TSO 业务提供**企业已入库**的产品、行业、客户背景事实依据。

**何时用**：回答或生成内容依赖「客户产品参数、卖点、行业术语、公司背景」且不应凭模型记忆编造时，先 `rag list` 锁定客户库，再 `rag query` 取片段，再结合 `keyword` / `ad` / `google-analysis` 等命令执行。

**何时不用**：纯数据拉取（消耗、余额、系列状态）→ 走 `stats` / `google-analysis`；社媒口播/三库写稿 → 用 `siluzan-cso rag`（见 CSO skill）。

---

## 命令速览

```bash
# 1. 列出已建索引的知识库（按客户/品牌选 folder）
siluzan-tso rag list --rag-only --json-out ./snap

# 2. 检索产品/行业资料（建议锁定 --folder-id）
siluzan-tso rag query -q "产品核心卖点 应用场景 目标客群" --folder-id <id> --partition wiki --top-k 12
siluzan-tso rag query -q "行业术语 英文类目" --folder-id <id> --top-k 10
```

---

## 参数说明

| 选项          | 默认      | 说明                                                               |
| ------------- | --------- | ------------------------------------------------------------------ |
| `-q, --query` | 必填      | 检索词。含空白时按词分检、去重合并（`--json-out` 含 `subQueries`） |
| `--folder-id` | 全库      | 文件夹 ID，逗号分隔；**已识别客户/品牌时强烈建议锁定**             |
| `--tags`      | 不过滤    | 不传 = 全库无标签限制                                              |
| `--partition` | `default` | 仅 `wiki` 或 `default`；长正文优先 `wiki`，缺细节再补 `default`    |
| `--top-k`     | 7         | 每分检 3–30 条；多词合并上限 `min(30, topK×词数)`                  |
| `--json-out`  | false     | 机器可读输出（含 `score` 0–1，越大越相关）                         |

`belongToId` 默认从当前登录账号的 `companyId` 解析；`csoBaseUrl` 从 TSO API 自动推导，可用 `SILUZAN_CSO_BASE` 覆盖。

---

## TSO 业务场景路由

| 用户意图                       | 建议检索词（示例）                        | 后续 TSO 命令                                                                                                              |
| ------------------------------ | ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Google 搜索广告方案 / 批量草稿 | 产品卖点、应用行业、目标国家、竞品差异    | `google-ads/google-ads-campaign-plan.md` + `keyword` / `campaign-create`；草稿发布见 `google-ads/google-ads.md` § ad batch |
| 关键字拓词补语境               | 产品型号、英文类目、行业术语、应用场景    | `keyword suggest -k "..."`；编排见 `analytics/keyword-planner-workflows.md`                                                |
| 账户诊断 / 周期报告「背景」段  | 公司简介、主营产品、目标市场、认证资质    | `google-analysis` + `report-templates/` 对应模板                                                                           |
| 询盘分析报告                   | 产品线、出口市场、客户画像、大洲业务侧重  | `report-templates/google-inquiry-analysis.md`                                                                              |
| 开户行业/资质核对              | 营业执照经营范围、行业描述、品牌全称      | `accounts/open-account-by-media.md` 对应媒体开户流                                                                         |
| 优化建议解释                   | 产品毛利结构、旺季、转化路径（表单/电话） | `optimize` 记录 + 人工解读；数据仍来自 `google-analysis`                                                                   |

检索结果**只作事实参考**：广告标题/描述须符合 `google-ads/rules/google-ads-compliance.md`；数值指标仍以 CLI 拉数为准。

---

## AI 检索策略（TSO 版）

### 1. 先锁客户库

- 运行 `rag list --rag-only --json-out ./snap`，按知识库**名称**匹配用户说的公司/品牌。
- 多客户代运营：每个客户单独 `--folder-id`，**禁止**混库检索后张冠李戴。

### 2. 改写为「检索型」问句

去掉「帮我」「分析一下」等任务句，保留 **实体 + 属性**：

- 差：「这个客户 Google 广告怎么投」
- 好：`产品系列 出口 认证 CE FDA` 或 `注塑机 型号 吨位 应用`

### 3. 空格分检（多角度）

```bash
siluzan-tso rag query -q "产品 卖点 差异化" --folder-id <id> --partition wiki --top-k 12
siluzan-tso rag query -q "目标市场 国家 行业" --folder-id <id> --partition wiki --top-k 10
```

### 4. 与拉数命令配合

典型编排：

```
rag list --rag-only --json-out ./snap
  → rag query（产品/行业背景）
  → list-accounts -k <id>
  → keyword suggest / google-analysis / ad campaigns
  → 报告模板输出（背景段引用 RAG，数据段引用 JSON）
```

### 5. 结果使用纪律

- `score` 越大越相关；明显跑题片段丢弃。
- 不得把 RAG 片段里的过期价格/政策当作当前投放依据；金额与消耗以 `stats` / `google-analysis` 为准。
- 片段不足以支撑结论时如实说明缺口，**不要编造**。

---

## 与 CSO rag 的区别

| 维度      | siluzan-tso `rag`                         | siluzan-cso `rag`                                       |
| --------- | ----------------------------------------- | ------------------------------------------------------- |
| 主要用途  | 广告投放、分析、拓词、报告背景            | 社媒文案、三库素材、口播写稿                            |
| 默认 tags | 不过滤（按 folder 锁客户）                | 常配合三库 tags（见 CSO `references/analytics/rag.md`） |
| 后续命令  | `ad` / `keyword` / `google-analysis`      | `publish` / 写稿工作流                                  |
| API       | 相同 `cutapi/v1/material/queryknowledges` | 相同                                                    |
