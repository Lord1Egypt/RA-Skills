# statdata-transfer / 统计数据格式转换器

[🇬🇧 English](./README.md)

<div align="center">
<img src="assets/icon.svg" width="240" height="240" />
</div>

---

> 读入 50+ 统计软件及临床试验数据格式，并**支持多数格式双向互转**，完整保留变量标签、值标签等元数据。无需安装任何统计软件——仅做数据格式转换。

## 如何在对话里使用

直接用自然语言跟智能体说即可。以下是真实示例（可直接复制）：

**① 最常用的——转换文件**
- **你这样说**：`把 C:/Users/Name/Desktop/data.sav 转成 .dta`
- **助手会这样回（示意）**：用 pyreadstat 读入 `data.sav`，保留全部变量标签，在同目录写出 `data.dta`。
- **如何触发真实转换**：默认只预览方案；说 `请直接写文件` / `直接转换` 才真正执行。

**② 看看里面有什么**
- **你这样说**：`读入 data.sav 并显示元数据`
- **助手会这样回**：打印 DataFrame 形状、变量标签、值标签，并列出哪些元数据会被保留。

**③ 转之前先确认会不会丢**
- **你这样说**：`.sav 转 .xlsx 会丢失元数据吗？`
- **助手会这样回**：提示 Excel 仅把标签放在额外工作表；建议用 Parquet/Stata 才能无损保留。

**④ 要可复现代码**
- **你这样说**：`给我把 .sav 转 .parquet 的 Python 代码`
- **助手会这样回**：打印 `read_stat_file` / `write_stat_file` 片段（代码始终是英文）。

**⑤ 切换语言**
- **你这样说**：`用中文回复` / `switch to English`——所有面向用户的提示会跟随你的系统语言或这句指令。

## 你能做些什么？（场景索引）

| 能力 | 典型用途 | 试试这样说 |
|:---|:---|:---|
| **读入 50+ 格式** | 把 SPSS/Stata/SAS/R/Excel/Parquet/HDF5/JSON… 读入 pandas | `读入 data.sav 并显示元数据` |
| **统计格式互转** | SPSS ↔ Stata ↔ R ↔ SAS XPT，保留全部标签 | `把 data.sav 转成 .dta 并保留变量标签` |
| **导出通用格式** | Parquet / Feather / HDF5 / JSON / CSV / Excel（标签内嵌） | `存成 parquet 但保留值标签` |
| **元数据安全往返** | 转换再转回，标签不丢 | `先转 parquet 再转回 sav，保留标签` |
| **元数据丢失警告** | 导出前先知道会丢什么 | `.sav 转 .xlsx 会丢元数据吗？` |
| **批量 / 文件夹** | 转换整个文件夹或 zip 包 | `把这个 zip 里的 .dta 全转成 .sav` |

完整格式清单与逐格式限制见下方**进阶参考**。

## 首次使用常见问题 FAQ

- **需要装 SPSS/Stata/R 吗？** 不需要。本技能是纯 Python；只有少数格式（Minitab/EpiData/R 写出）会**可选地**调用本地 R，且只有在你传入 `allow_r_exec=True` 时才运行。
- **怎么才能真写出文件、而不只是看代码？** 说 `请直接写文件` / `直接转换`。默认是预览，执行需你明确确认。
- **我的标签能保住吗？** 统计二进制格式（SPSS/Stata/SAS/R）——能，完整保留。文本/JSON——只保留可保留的子集。技能总会告诉你保留/丢失了什么。
- **能拿到可复现代码吗？** 能——说 `给我 Python 代码`，它会打印 `read_stat_file` / `write_stat_file` 调用。
- **中文系统下输出是中文吗？** 面向用户的提示在 `zh-*` 系统下自动切中文，或用 `用中文回复` 强制切换。代码始终是英文。
- **数据文件太大 / 无法直接上传？** 在提示词里用文件的绝对路径，或压缩成 `.zip` 再上传。

## 安全说明（用户语言）

本技能**完全本地运行**，遵循**安全预览**模型：它先展示将要读入/转换的方案，只有你明确要求时才写文件。所有会调用本地 R 解释器的路径都**默认关闭、需显式开启**——仅当你对可信文件传入 `allow_r_exec=True` 时才运行。除非你明确要求安装依赖包，否则你的数据绝不上网。输出仅供参看，在用于监管申报前请自行核验。

---

## 进阶参考

> 以下内容为开发者/参考资料，已从快速上手区下移。

### 支持格式与能力矩阵

*按字母排序。*

| 格式 | 扩展名 | 依赖 | 变量标签 | 值标签 | 特殊缺失 | 公式 | 元数据保留 |
|------|--------|------|---------|--------|---------|------|-----------|
| CDISC ODM | `.odm` | lxml | ✗ | ✗ | ✗ | ✗ | ⚠️ 仅临床数据 |
| dBASE / FoxPro | `.dbf` | dbfread / dbf | ✗ | ✗ | ✗ | ✗ | ⚠️ 读+写；大写字段名 |
| EpiData | `.rec` | R foreign | ✗ | ✗ | ✗ | ✗ | ⚠️ 通过 R 读入 |
| EpiInfo | `.prj` `.xml` | xml/etree | ✅ | ✅(codes) | ✗ | ✗ | ✅ XML 结构 |
| Excel | `.xlsx` `.xls` `.xlsm` | openpyxl / xlrd | ✗ | ✗ | ✗ | ⚠️ 仅结果 | ⚠️ 写出用额外工作表；合并单元格填充 |
| EViews | `.wf1` `.wf2` | 内置 | ✗ | ✗ | ✗ | ✗ | ⚠️ JSON 结构 |
| Feather | `.feather` `.arrow` | pyarrow | ✅(schema) | ✅(schema) | ✗ | ✗ | ⚠️ 版本差异 |
| FST | `.fst` | — | ✗ | ✗ | ✗ | ✗ | ✗ 探测降级（专有格式） |
| GraphPad Prism | `.pzfx` `.pz` | pzfx | ✗ | ✗ | ✗ | ✗ | ⚠️ 多表 |
| Gretl | `.gdt` `.gdtb` | 内置 | ✅ | ✅(tables) | ✗ | ✗ | ✅ string-tables |
| HDF5 | `.h5` `.hdf5` | h5py | ✗ | ✗ | ✗ | ✗ | ⚠️ 层级结构 + 属性标签 |
| HTML | `.html` | lxml | ✗ | ✗ | ✗ | ✗ | ⚠️ 仅表格 |
| jamovi | `.omv` | ZIP 内置 | ✅ | ✅ | ✗ | ✗ | ✅ JSON 分析 |
| JMP | `.jmp` | jmpio-python | ⚠️ | ⚠️ | ✗ | ✗ | ⚠️ 多表 |
| JSON | `.json` | 内置 | ✅ | ✅ | ✗ | ✗ | ✅ 写出嵌入 stat-full-meta |
| MATLAB | `.mat` | scipy | ✗ | ✗ | ✗ | ✗ | ⚠️ v7.3+ 走 h5py 回退 |
| Mathematica | `.wdx` | lxml | ✗ | ✗ | ✗ | ✗ | ⚠️ Best-effort XML |
| Minitab | `.mtw` `.mpj` | mtbpy / R | ✗ | ✗ | ✗ | ✗ | ⚠️ 通过 R 读入 |
| MS Access | `.mdb` `.accdb` | pyodbc + Access 驱动 | ✗ | ✗ | ✗ | ✗ | ⚠️ 多表；需系统驱动 |
| ODS | `.ods` | odfpy | ✗ | ✗ | ✗ | ✗ | ⚠️ 仅数据 |
| ORC | `.orc` | pyarrow | ✅(schema) | ✅(schema) | ✗ | ✗ | ⚠️ 版本差异 |
| Origin | `.opju` `.oggu` | zipfile + lxml | ✗ | ✗ | ✗ | ✗ | ⚠️ Best-effort |
| Parquet | `.parquet` | pyarrow | ✅(schema) | ✅(schema) | ✗ | ✗ | ⚠️ 嵌套类型；分区数据集 |
| R | `.rda` `.rds` `.rdata` | pyreadr + R | ✅ | ✅ | ✅ | ✗ | ✅ statdata_meta + R 桥接 |
| SAS | `.sas7bdat` `.xpt` `.sas7bcat` | pyreadstat | ✅ | ✅(需 catalog) | ⚠️ | ✗ | ✅ |
| SPSS | `.sav` `.zsav` `.por` | pyreadstat | ✅ | ✅ | ✅ | ✗ | ✅ |
| Stata | `.dta` | pyreadstat | ✅ | ✅ | ⚠️ | ✗ | ✅ |
| Weka ARFF | `.arff` | 内置 | ✅ | ✅(nominal) | ✗ | ✗ | ✅ 名义映射 |
| XML | `.xml` | lxml | ✗ | ✗ | ✗ | ✗ | ⚠️ 结构保留 |

> ✅=完整保留 · ⚠️=部分保留或条件性 · ✗=无法保留

### 探测降级格式

无现成解析库，识别扩展名并给出清晰导出指引（不解析数据）。

| 格式 | 扩展名 | 导出指引 |
|------|--------|---------|
| FST (R fst 包) | `.fst` | R: `fst::read_fst("in.fst", "out.csv")`，再读 CSV |
| LIMDEP / NLOGIT | `.lpw` | 从原软件导出 CSV |
| NCSS | `.ncss` | 导出 CSV |
| OxMetrics | `.in7` | 导出 CSV / `.dta` |
| Paradox | `.db` `.px` | 导出 `.dbf` / CSV |
| SAS CPORT | `.cpt` | SAS: `proc export` 为 XPORT(`.xpt`) / `.sas7bdat` |
| Statistica | `.sta` | 导出 `.sav` / `.csv` |
| SYSTAT | `.sys` `.syd` | 导出 CSV / `.sav` |

### 返回结构

```python
{
    "dataframe": pd.DataFrame,
    "metadata": {
        "file_format": "spss_sav",
        "row_count": 100, "column_count": 10,
        "variable_labels": {"q1": "问题1"},
        "value_labels": {"q1": {1: "是", 2: "否"}},
    },
    "warnings": [],
    "column_report": {"q1": {"source_type": "int", "pandas_dtype": "int64"}},
}
```

### 元数据保留层级

1. **统计二进制格式**（SPSS/Stata/SAS/R）：100% 元数据完整保留
2. **Arrow 生态**（Parquet/Feather/ORC）：仅还原 `write_stat_file` 写入的标签
3. **非统计格式**（CSV/Excel/XML/HTML/ODS）：仅保留数据值；可用 `apply_value_labels()` 手动附加
4. **R 格式**：通过 `statdata_meta` 属性嵌入全部元数据

### 推荐读入策略

| 需求 | 推荐 |
|------|------|
| 数据入库/ETL | SPSS `.sav` 或 Stata `.dta` → Parquet / HDF5 |
| 科学计算 | `.mat` 或 `.hdf5` → NumPy / pandas |
| 统计分析（Python） | `.sav` / `.dta` → pandas → scipy.stats |
| 报告输出 | pandas → JSON / HTML / Excel |
| 跨软件共享 | Stata ↔ SPSS ↔ R 直接互转 |

### 文件大小限制

| 格式 | 内存行为 |
|------|---------|
| pyreadstat (SPSS/Stata/SAS) | 全文件加载到 RAM |
| HDF5 | 支持分块读取；不受 RAM 限制 |
| Parquet | pyarrow 支持 mmap 映射；可处理 >内存的文件 |

### 编码注意事项

- **中文文件**：旧版 Stata/SAS 可能使用 GBK/gb2312。使用 `encoding='gbk'`。
- **欧洲文件**：部分 SAS 文件使用 Latin-1。UTF-8 失败时尝试 `encoding='latin1'`。
- **自动检测**：SPSS/Stata/SAS 默认启用 `_auto_detect_encoding`。

### 提供输入文件

AI 智能体只能直接上传有限类型的文件。当数据文件无法直接上传时：

1. **在提示词中使用文件绝对路径**（如 `把 C:/Users/Name/Desktop/data.sav 转成 .dta`）
2. **将文件压缩为 `.zip` 包**后上传

技能会自动解压并处理包含单个数据文件的 zip 归档。

### 命令行（进阶）

```bash
# 检查环境（仅显式要求时才安装）
python scripts/check_env.py --install
```

完整代码示例：[`references/usage_examples.py`](./references/usage_examples.py)

### 扩展

需要支持新格式？编辑 `scripts/reader_*.py` 添加读入函数，在 `scripts/reader_core.py` 的 `format_map` 中注册，并在 `scripts/reader_core.py` 中补充对应的 TypedDict 定义。

### 格式限制与解决方案

*已解决项标 ✅ / 新增能力标 🔄；未标项为固有格式限制（按字母排序，能力矩阵见上）。*

- **CDISC ODM (.odm)**：❌ XML 结构依赖，嵌套解析取决于 ODM 文件结构规范性；❌ ODM 规范本身不含统计元数据，仅保留临床数据结构
- **dBASE / FoxPro (.dbf)**：❌ 字段名强制大写（格式限制）；✅ 支持读+写
- **EpiData (.rec)**：❌ 读入需经 R + `foreign` 包桥接（需显式 `allow_r_exec=True` 开启，默认禁用）；❌ 统计元数据在 R→CSV 桥接中丢失
- **EpiInfo (.prj)**：❌ 项目文件不含数据，自动搜索同名 CSV；❌ Access 不支持，需先导出 CSV；✅ 变量标签和 codes 在 XML 结构中重建
- **Excel (.xlsx/.xls/.xlsm)**：✅ 合并单元格用锚点值填充（`fill_merged_cells=True`，默认）；❌ 公式丢失，仅保留计算结果；❌ 图表/形状不提取；写出时标签存于独立元数据工作表
- **HDF5 (.h5/.hdf5)**：✅ 多层级数据集 `pd.read_hdf` 失败时回退 h5py 合并全部顶层数值数据集；✅ 属性标签还原；❌ 层级结构仍展平为顶级变量
- **JMP (.jmp)**：❌ 依赖 jmpio-python，版本支持不一；❌ 多表仅返回第一个；写出仅支持单表
- **MATLAB (.mat)**：✅ v7.3+（HDF5）经 h5py；❌ 复杂结构（嵌套 cell、稀疏矩阵、函数句柄）单列扁平化；❌ Object 类和 datetime 丢失类型保真度
- **Parquet (.parquet)**：❌ 深层嵌套类型（>2 层）不透明；✅ 分区数据集经 `pyarrow.dataset` 合并读取
- **R (.rda/.rds/.rdata)**：✅ 旧版 ASCII XDR 自动回退到 R（需 `allow_r_exec=True`）；❌ factor 顺序可能未保留为 Categorical；写出经 `statdata_meta` 实现完整元数据往返
- **SAS (.sas7bdat/.xpt/.sas7bcat)**：✅ 值标签需 `.sas7bcat` 同目录自动加载；❌ Viya CAS `.sashdat` 不支持；日期基准 1960-01-01
- **SPSS (.sav/.zsav/.por)**：❌ MR Sets 读入为原始字典，语义需手动重建；❌ 公式丢失；⚠️ 特殊缺失值（`.A`–`.Z`）在 `special_missing` 中标记；`.zsav` 需 pyreadstat 1.2+，否则降级 `.sav`
- **Stata (.dta)**：⚠️ 特殊缺失（`.a`–`.z`）`user_missing=True`（默认）时保留为字符标签，`False` 时不可逆变 NaN；✅ 旧版 Latin-1 已自动检测；❌ Stata 117–119 不支持，写回自动降级 v15

### 安全 / Security

- **R 执行默认隔离且需显式开启**：读入 `.rda/.rds/.RData`、Minitab `.mtw/.mpj`、EpiData `.rec`、写出 R 格式均默认禁用，仅当对可信文件显式传入 `allow_r_exec=True` 时运行。纯 Python 解析器（pyreadr、mtbpy）优先。
- **无静默 R 回退**：纯 Python 解析失败且未设 `allow_r_exec` 时明确报错，而非静默启动 R，消除对不可信文件执行嵌入代码的风险。
- **R 脚本为静态模板**：启用 R 路径时，用户输入仅经命令行参数传入，绝不拼进可执行 R 代码。
- **临时 CSV 暴露（R 桥接）**：启用 R 时数据先物化为磁盘临时 CSV，用后即刻删除，但崩溃时可能短暂留存。处理高度敏感数据请避开 R 桥接格式。
- **无破坏性写入**：写入已存在的 `.hyper` 先轮转为 `.bak`，原文件失败保持不动。
- **依赖已固定版本**：核心依赖带上限约束，详见 `requirements.txt`。

## 联系作者

如有功能改进建议、Bug 报告或其他反馈，请直接联系作者：medstatstar@gmail.com（张文彤 / Wintone Zhang）。

## 许可证

MIT 许可证。详见 [LICENSE](LICENSE)。
