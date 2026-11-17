# 教育版（--target edu）学生数据隐私扫描说明

教育版盘点「学生数据文件放在哪、存了哪几类个人信息、以什么形态存放、是否存在出本机风险」。
全程只读、零网络、不调用模型，报告一律脱敏且**不提供明文回显选项**。

## 使用方式

```bash
# 目录盘点（推荐先在小范围目录上试跑）
python3 scripts/yotta_audit.py --target edu --path ./班级资料

# 单文件 + JSON + Markdown 报告
python3 scripts/yotta_audit.py --target edu --path ./成绩表.xlsx --json --report ./edu-report.md

# 只报 high 及以上
python3 scripts/yotta_audit.py --target edu --path ./班级资料 --severity high

# 学校自备词表 / 规则包
python3 scripts/yotta_audit.py --target edu --path ./校车名单.csv --edu-rules ./school-rules.json
```

参数纪律：

- `--path` 必填，缺失或路径不存在返回退出码 4；教育版**不做自动发现**，不会扫描未指定的主目录或全盘；
- `--report` 输出路径不得位于被扫描目录内，也不得与输入文件相同（防止报告本身变成新的个人信息文件）；
- `--severity` 与技能模式一致：过滤更低级别，退出码只反映保留的条目。

## 文件形态

| 形态 | 处理方式 |
|---|---|
| `.csv` / `.tsv` | 按表头 + 数据行解析；分隔符自动判断，编码按 UTF-8（含 BOM）→ GBK → 替换兜底 |
| `.txt` / `.md` / `.json` / `.jsonl` / `.xml` / `.html` / `.yaml` / `.yml` | 按行扫描 |
| `.xlsx` | 标准库读取共享字符串与内联字符串（只读，不落盘、不解压到磁盘） |
| `.docx` | 标准库读取正文段落文本 |
| PDF / 图片 / 扫描件 / 旧版 Office / 压缩包 / 数据库 | 不解析（不做 OCR），计入报告「未解析 / 跳过」 |

单文件上限 4 MB、单次最多 2000 个文件、单表最多 5000 行，超出即跳过并计数，不静默丢弃。

## 规则清单（默认规则包）

规则包：`scripts/student_data_rules.json`（`schema_version` / `pack_version`）。

| 规则 | 面向 | 判定方式 | 默认级别 |
|---|---|---|---|
| EDU-ID-001 | 身份证号 | 18 位 + GB 11643 校验位（MOD 11-2）通过 | critical |
| EDU-ID-002 | 手机号 | `1[3-9]` 开头 11 位 | high |
| EDU-ID-003 | 邮箱 | 邮箱形态 | medium |
| EDU-ID-004 | 学籍号 / 考生号 | 表头命中 + 单元格为 8–25 位字母数字（不做形态断言） | medium |
| EDU-QI-001 | 姓名 + 成绩组合 | 同一表内同时存在姓名列与成绩 / 排名列 | high |
| EDU-QI-002 | 出生日期 | 表头命中且有数据 | high |
| EDU-QI-003 | 家庭住址 | 表头命中且有数据 | high |
| EDU-QI-004 | 家长联系方式 | 家长 / 监护人列且列内出现手机号 | high |
| EDU-SA-001 | 健康与身心状况 | 表头或内容命中（病史 / 残疾 / 过敏 / 心理 / 情绪等） | critical |
| EDU-SA-002 | 资助与家庭境况 | 表头或内容命中（低保 / 建档立卡 / 资助 / 孤儿 / 单亲 / 留守等） | critical |
| EDU-SA-003 | 生物识别信息 | 表头或内容命中（人脸 / 指纹 / 照片 / 人脸识别） | critical |
| EDU-SA-004 | 显式未成年人标记 | 文本显式出现（未成年 / 儿童 / 未满十四周岁） | critical |
| EDU-HR-001 | 出本机路径 | 路径命中云同步 / 网盘 / 即时通讯目录，且该文件已有内容命中 | high |
| EDU-HR-002 | 文件名疑似含姓名 | 文件名含成绩 / 评语 / 名单等词，且含常见姓氏+名或长数字编号 | high |
| EDU-HR-003 | AI 工具 / 临时目录 | 路径段命中 uploads / .tmp / tmp / temp，且该文件已有内容命中 | medium |

规则语义：

- **字段驱动优先**：中文表头是主要依据，内容正则为补充；同一列只报一条，按规则聚合计数；
- **要求有数据**：只有表头、没有数据的空模板不报，避免模板文件刷屏；
- **组合规则**：姓名 + 成绩这类组合风险单独成条，提示「可识别到具体学生」；
- **路径规则**：云同步 / 网盘 / 即时通讯目录默认要求同文件已有内容命中，避免把无关文件全部标红。

## 脱敏口径

报告只输出**类别、位置、计数与脱敏样例**：

| 类型 | 样例形态 |
|---|---|
| 身份证号 / 学籍号 / 手机号 | 保留末 4 位，其余等长 `*`（如 `**************1234`） |
| 姓名 | 保留姓（`张*`） |
| 地址 | 保留前 3 个字符（`辽宁省**` / `朝阳区**`） |
| 邮箱 | 保留首字符与域名（`z***@example.com`） |
| 健康 / 资助 / 生物识别等属性值 | 保留首字符（`过***`） |

约束：

- 不提供 `--show-raw` 之类的明文回显开关；
- Markdown 报告与 JSON 输出同等脱敏；
- 文件名命中姓名规则时，报告中的文件名同样部分脱敏；
- 不做跨文件个体关联（不生成可用于反查的稳定标识）；需要按学生聚合统计时使用元镜。

## 输出与退出码

- 文本报告：范围摘要 + 级别汇总 + 4 类风险视图 + 逐条发现 + 免责说明；
- `--json`：稳定契约（`tool` / `version` / `target` / `scope` / `summary` / `findings` / `edu`），
  `scope` 含 `path` / `files_scanned` / `files_skipped` / `skipped_ext` / `records_scanned` / `rules`；
- `--report`：Markdown 报告；
- 退出码沿用统一语义：`0` 干净或仅 low ｜ `1` medium ｜ `2` high ｜ `3` critical ｜ `4` 扫描器错误。

## 使用边界

- 只检测与报告：不移动、不删除、不加密、不上传任何文件；
- 不给出法律或合规结论；需要条款级判断时使用元规（yotta-compliance）；
- 不做学生年龄或身份推断，不做人脸 / 图片 / OCR 分析；
- 只扫描用户有权处理的目录；报告分享前请再次核对内容范围；
- 规则命中代表「出现可观察现象」，不代表违法或违规事实，处置前请人工复核。

## 自定义规则包

规则包是只读 JSON 数据，不执行任何表达式。顶层结构：

```json
{
  "schema_version": "1.0",
  "pack_version": "2026.09.1",
  "field_vocab": { "student_name": ["姓名", "学生姓名"] },
  "content_rules": [
    { "id": "EDU-CUSTOM-001", "title": "校车线路", "category": "handling_risk",
      "severity": "medium", "kind": "keyword_any", "keywords": ["校车线路"],
      "remediation": "限制流转范围" }
  ],
  "field_rules": [], "combo_rules": [], "path_rules": [], "filename_rules": []
}
```

校验规则：`schema_version` 必须为 `1.0`；`rule_id` 全局唯一；`category` 取
`direct_identifier` / `quasi_identifier` / `sensitive_attribute` / `handling_risk`；
`severity` 取 `low` / `medium` / `high` / `critical`；`field_rules` / `combo_rules`
只能引用 `field_vocab` 中已定义的词表。任一项不合规即整体失败（退出码 4）。
