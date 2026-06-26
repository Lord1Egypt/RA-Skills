# 系统架构

## 数据流总览

```
东方财富/巨潮资讯
      │
      ▼
eastmoney_api.py / cninfo_api.py  ─── 获取公告列表
      │
      ▼
stock_tracker.py ─── 主入口，协调各模块
      │
      ├─ Phase 1a: 正则跳过判断 (ann_detail.should_skip_content)
      │     │  13 条 SKIP_CONTENT_PATTERNS，极速过滤
      │     ▼
      ├─ Phase 1b: LLM 标题价值判断 (llm_judge.py)
      │     │  并发 20 workers，判断 valuable / non-valuable
      │     ▼
      ├─ Phase 2: 并发下载正文 (ann_detail.fetch_announcement_content)
      │     │  优先 API，回退 PDF 提取，max_workers=5
      │     ▼
      ├─ Phase 3: 顺序清洗 (text_cleaner.py) + 分批保存到 DB
      │     ▼
      ├─ daily_summary.py ─── 为有价值公告生成 LLM 摘要
      │     │  BATCH_SIZE=1, workers=20, 定期报告跳过 LLM
      │     ▼
      └─ dashboard.py ─── Flask Web 仪表盘，lazy loading
```

## 模块分解

### stock_tracker.py（主入口）

**CLI 参数：**

| 参数 | 用途 |
|------|------|
| `--force` | 强制重新抓取所有公告（覆盖已见检查） |
| `--days N` | 抓取最近 N 天公告 |
| `--dry-run` | 试运行，不更新数据库 |
| `--group` | 只追踪指定分组（模糊匹配） |
| `--list-groups` | 列出所有可用分组 |
| `--stats` | 查看数据库统计 |
| `--list` | 列出历史公告 |
| `--fetch-content` | 补抓缺少全文的公告正文 |
| `--clean` | 清洗已获取的公告正文 |
| `--prune` | 清理无正文的空记录 |
| `--source` | eastmoney（默认）或 cninfo |

**执行流程：**
1. 解析参数 → 执行子命令（stats/list/clean/prune/fetch-content）或完整运行
2. 完整运行：获取自选股列表 → 获取公告列表 → 过滤已见 → 获取全文 → 入库

### eastmoney_api.py（东方财富数据获取）

**自选股获取（3 级回退）：**
1. **myfavor API** `https://myfavor.eastmoney.com/v4/webouter` — 支持分组过滤
2. **Cookie 解析** — 从 `selfSelectStocks` 字段正则提取
3. **config.json** — 手动配置硬编码列表

**公告 API：**
- `https://np-anotice-stock.eastmoney.com/api/security/ann`
- `ann_type=A` 为 A 股，`ann_type=H` 为港股
- 参数：`stock_list={market},{code}`

**Market 字段值：**

| 值 | 市场 | 标签 |
|----|------|------|
| 0 | 深圳 | SZ |
| 1 | 上海 | SH |
| 100 | 美股 | US |
| 104 | 期货 | FUT |
| 116 | 港股 | HK |
| 119 | 外汇 | FX |
| 124 | 港股通 | HKI |
| 134 | 港股通(深) | HKF |
| 251 | 其他 | OTHER |

### cninfo_api.py（巨潮资讯网数据获取）

**API 端点：**
- 列表：`POST https://www.cninfo.com.cn/new/hisAnnouncement/query`
- PDF 基址：`https://static.cninfo.com.cn/{adjunctUrl}`

**请求参数：**
- `searchkey`: 股票代码
- `seDate`: 日期范围 `YYYY-MM-DD~YYYY-MM-DD`
- `pageNum` / `pageSize`: 分页
- `column`: szse

### ann_detail.py（公告正文获取）

**内容获取优先级：**
1. **内容 API** `https://np-cnotice-stock.eastmoney.com/api/content/ann`（需东方财富网络环境）
2. **PDF 下载 + 文本提取** `https://pdf.dfcfw.com/pdf/H2_{art_code}_1.pdf`
3. 外部传入 `pdf_url_override`（巨潮 PDF 链接）：直接下载 PDF

**跳过全文采集的标题模式（13 条）：**
1. 公司章程
2. 信用评级 / 跟踪评级
3. 募集说明书
4. 付息公告
5. 上市公告 / 摘牌
6. 发行结果公告 / 票面利率 / 簿记建档 / 更名公告 / 发行完毕
7. 董事会报告
8. 法律意见书
9. 股东会决议公告 / 股东会表决结果 / 投票表决结果
10. 薪酬
11. 周年会通告
12. 担保额度
13. 召开情况

**TOC 提取：**
超长文档（通函、海外市场公告、股东会会议资料、发行公告）只提取目录或开头 2000 字。

### llm_judge.py（LLM 标题价值判断）

**核心功能：**
- 判断公告标题是否有价值（valuable / non-valuable）
- 输出 category（大类）和 type（小类）
- 使用 JSON mode（`response_format: {"type": "json_object"}`）
- Fail-open：所有重试失败后默认视为有价值

**重试策略：** 最多 2 次重试，间隔递增

**System Prompt 结构：**
1. A 股 8 大类 + HK 7 大类分类体系
2. 高价值 type 列表
3. 低价值 type 列表
4. 需要结合标题判断的 type（董事会公告、借贷担保、利润分配）

### text_cleaner.py（公告正文清洗）

详见 `text-cleaning.md`。

### daily_summary.py（每日公告摘要）

**批处理参数：**
- `BATCH_SIZE=1`：每次 LLM 调用只处理一条公告（避免超长上下文）
- `max_workers=20`：并发线程数
- `SKIP_LLM_TYPES`：定期报告类型跳过 LLM，使用固定摘要 `【类型】标题`

**输出模式：**
- `--digest` 输出格式化摘要列表（STDOUT），供 agent 读取转发
- 格式：`DIGEST_TOTAL:N` → 编号列表

### db.py（SQLite 存储）

**核心特性：**
- WAL 模式：`PRAGMA journal_mode=WAL`
- UPSERT 含 null 保护：`ON CONFLICT(ann_id) DO UPDATE SET ... CASE WHEN excluded.x != '' THEN excluded.x ELSE announcements.x END`
- 自动迁移：`_migrate_schema()` 增量添加新字段（full_text, clean_text, attach_url, summary, status, ann_type_tag, ann_type_category, clean_text_length）

### dashboard.py（Flask Web 仪表盘）

**路由：**
| 端点 | 说明 |
|------|------|
| `GET /` | 首页（单页应用） |
| `GET /api/stocks` | 股票概览统计（7/15/30天/全部） |
| `GET /api/announcements/<code>` | 个股公告列表（lazy loading） |

**前端特性：**
- 股票表格行可展开
- 搜索框实时过滤
- 浮动个股栏（滚动时固定显示当前展开股票）
- 分类标签展示

## 过滤策略（3 层）

```
公告列表
   │
   ▼
Layer 1: 正则跳过 (should_skip_content)
   │  13 条 SKIP_CONTENT_PATTERNS
   │  公司章程、信用评级、募集说明书、付息公告、上市公告等
   │  跳过 → full_text=clean_text=""，status=filtered
   │
   ▼
Layer 2: LLM 标题判断 (llm_judge.judge)
   │  valuable → 继续下载全文
   │  non-valuable → full_text=clean_text=""，status=filtered
   │
   ▼
Layer 3: 下载失败
   │  API/PDF 均失败 → status=filtered
   │
   ▼
最终 DB 入库
   valuable 有价值 | filtered 已过滤
```

## LLM 有价值/无价值类型

**高价值 type（几乎总是下载）：**
- 财务报告类全部（业绩预告、业绩快报、季度/半年/年度报告）
- 交易提示类全部（停牌提示、交易异动、澄清公告、风险提示、特别处理、终止上市等）
- 重大事项类：资产重组、收购兼并、股权激励、关联交易、违纪违规
- 股权股本类：回购股权、权益变动
- 一般公告类：法律纠纷、产销经营快报、机构调研公告
- 港股：翌日报表、须公布的交易

**低价值 type（几乎总是跳过）：**
- 中介公告（法律意见书、保荐机构核查意见、律师核查意见）
- 股东大会通知
- 薪酬管理制度、董事会议事规则、公司章程修正案
- 债券付息公告、发行结果公告
