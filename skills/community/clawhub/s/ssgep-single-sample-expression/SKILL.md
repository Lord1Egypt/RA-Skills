---
name: ssgep-single-sample-expression
description: 单样本无重复表达谱技能（SSGEP — Single Sample Gene Expression Profile）。植物/梨属等转录组表达谱分析全流程：原始数据获取→质控定量→差异与GO/KEGG富集→WGCNA共表达→SNP遗传分化→600DPI出图→论文三格式(HTML/DOCX/PPTX)+Shiny交互。**明确支持两种模式**：模式A 单样本无生物学重复（每个条件仅1样本，用固定离散度0.1+折叠变化法）；模式B 有生物学重复（标准DESeq2/edgeR离散度估计+设计公式）。当用户要做RNA-seq表达谱、差异基因(DEG)、WGCNA、功能基因挖掘，或要求"出论文三格式/做表达谱分析/打包项目案例"时调用。
agent_created: true
---

# 单样本无重复表达谱技能（SSGEP — Single Sample Gene Expression Profile）

> **来源 / Source**：本技能由 **山西大同大学 丁保朋（Ding Baopeng, Shanxi Datong University）** 整理并开源，基于梨属 5 品种 × 7 阶段转录组表达谱分析及褪黑素功能基因挖掘研究（Natural-language-driven AI agent for pear gene expression profiling and melatonin functional gene mining）。

> ## ⚠ 务必先确认：你的数据属于哪一种？
> - **单样本 / 无生物学重复（模式A，本技能核心场景）**：每个实验条件（如每个品种 × 每个发育阶段）**只有 1 个样本**，没有生物学重复。常规 DESeq2/edgeR **无法估计基因水平离散度（dispersion）**，差异分析必须用"固定离散度 + 折叠变化法"近似。本项目（梨属 5 品种 × 7 阶段 = 32 样本，每条件 1 样本）即属此类。
> - **有生物学重复（模式B）**：每个条件 ≥ 2 个（推荐 ≥ 3 个）生物学重复。可正常估计离散度，统计检验可靠。
>
> 两种模式下游（富集 / WGCNA / SNP / 出图 / 成稿）完全一致，差异只在"差异表达分析"这一步。下面分模式说明。

## 零、新购 Windows 电脑 0 基础起步（无任何生信环境）

即使你拿到一台**全新 Windows 电脑（或刚重装系统）、没装任何生信/编程软件**，也能跑通本项目。你不需要成为程序员——三条路任选：

### 路线 A（推荐新手）：WorkBuddy + ssgep 技能，让 AI 替你跑
1. 安装 WorkBuddy 桌面客户端。
2. 把本技能目录 `ssgep-single-sample-expression` 放进 `~/.workbuddy/skills/`（或发布/安装到技能市场）。
3. 在 WorkBuddy 里用中文说：“按 SSGEP 流程分析 data/raw 里的 fastq，出论文三格式”，AI 会自动检查环境、调用 R/Python、跑 01–10、并套用所有已知坑对策。
- 你只需提供原始 fastq 与参考转录本，其余交给 AI。

### 路线 B：本机装 R + Python 自己跑（数据完全本地）
1. **检查磁盘**：工作盘 ≥128 GB 空闲（推荐 256 GB SSD），参考盘 ≥1 GB。
2. **装 R**：https://cloud.r-project.org/bin/windows/base/ 下载 `R-4.x.x-win.exe`，下一步安装。
3. **装 RStudio**（图形界面，可选但推荐）：https://posit.co/download/rstudio-desktop/ 。
4. **（可选）装 Rtools**：https://cloud.r-project.org/bin/windows/Rtools/ —— 仅当你需要从源码编译包；本项目所有包都有 Windows 预编译二进制，通常**可跳过**。
5. **装 Python 3.12+**：https://www.python.org/downloads/windows/ ，安装时勾选 “Add python.exe to PATH”。
6. **一键装 R 包**（存为 `install_pkgs.R`，用 RStudio 打开运行，或右键“用 Rscript 运行”）：
```r
.libPaths(c('C:/Users/你的用户名/R/rlib', .libPaths()))   # 装到用户目录，避免权限问题
install.packages(c('plotly','shiny','bslib','DT','circlize','RColorBrewer','writexl'), type='binary')
if (!require('BiocManager', quietly=TRUE)) install.packages('BiocManager', type='binary')
BiocManager::install(c('DESeq2','edgeR','limma','WGCNA','Rsubread',
  'ComplexHeatmap','clusterProfiler','enrichplot','AnnotationDbi','org.Ppasinensa.eg.db'), ask=FALSE)
```
   Windows 会直接拉取**预编译二进制**，无需编译，几分钟完成。
7. **装 Python 包**（命令提示符执行）：
```
pip install python-docx python-pptx matplotlib pandas openpyxl
```
8. **放入数据**：原始 fastq → `data/raw/`；参考转录本(tx2gene/salmon_index) → `data/ref/`。
9. **跑流程**：在 RStudio 或命令行依次 `Rscript scripts/01_*.R` … `10_*.R`（路径按项目改）。
10. **出图与成稿**：
```
python scripts/fig4_wgcna.py
python scripts/paper_full.py
python scripts/case_study_gen.py
```

### 路线 C：腾讯云 Ubuntu 上云（本机配置不足时）
- 开一台**标准型 S5（8 vCPU/32 GB）+ 200 GB SSD 数据盘**，Ubuntu 22.04，conda/bioconda 在云上顺畅（不受本机 safe-delete 限制），远程 SSH 跑 01–10。详见下方“资源需求”节的云方案。

### 新手最常见 3 个坑
- **包装到哪了**：上述脚本把包装进用户目录 `R/rlib`；每次运行分析脚本前，务必在脚本**首行**加 `.libPaths(c('.../rlib', .libPaths()))`，否则找不到包。
- **别用 conda（本实验机）**：本机 conda 被 safe-delete 死锁，已改用原生 R；普通新机器可用 conda，但**新手用原生 R 最省事**。
- **docx 被占用**：成稿脚本已做 `safe_save`，被 Word 占用会自动写 `paper_new.docx`，关掉占用重跑即可覆盖回 `paper.docx`。

> 小结：纯新手选 **路线 A**（装 WorkBuddy + 本技能，对话驱动）；想数据全本地选 **路线 B**（原生 R+Python）；本机带不动选 **路线 C**（腾讯云）。三条路最终都能产出 paper.html/docx/pptx + Shiny。

## 一、两种分析模式（差异表达这一步不同）

### 模式A：单样本无重复（single-sample, no replicate）
- **问题**：n=1/条件，无法从数据估计 dispersion。
- **做法**：
  1. `median-ratio` 法归一化（DESeq2 的 estimateSizeFactors 思路，或 edgeR 的 calcNormFactors）。
  2. **固定离散度 dispersion = 0.1**（经验值，替代基因水平估计）。
  3. 用 Wald 近似得到 p 值（仅供排序参考，**不可直接当显著性**）。
  4. **以折叠变化法作为主判定**：`|log2FC| ≥ 1` 且 `baseMean ≥ 10` 视为差异。
  5. 可加 `|log2FC| ≥ 2` 作"强差异"子集；用 Venn / 通路富集交叉验证。
- **注意**：无重复时 p 值不稳健，结论需在讨论中说明局限性，建议用 qRT-PCR 或独立数据集验证关键基因。

### 模式B：有生物学重复（with biological replicates）
- **做法**：
  1. `median-ratio` 归一化 + `estimateDisp`（edgeR）或 `estimateDispersions`（DESeq2）。
  2. 设定设计公式 `design = ~ condition`（多因子用 `~ batch + condition`）。
  3. 统计检验：DESeq2 `WaldTest`（两两）或 `LRT`（多水平）；edgeR `glmQLFTest` / `glmFit+glmLRT`。
  4. **以 `padj < 0.05` 且 `|log2FC| ≥ 1` 为 DEG 阈值**（不用原始 p，用 BH 校正后的 padj）。
  5. 质控：样本 PCA / 层次聚类 → 检查重复是否聚在一起、有无离群；剔除离群后再分析。
- **优势**：离散度真实估计，p 值可靠，可做精确 FDR 控制与功效分析。

> 自动判别：若每个条件样本数 = 1 → 模式A；若任一组 ≥ 2 → 模式B。在提示词/脚本里先统计 `table(sample$condition)` 再分支。

## 二、适用场景
- RNA-seq 表达谱分析（植物/梨/任意物种；本项目为梨属 5 品种 × 7 阶段 = 32 样本，单样本无重复）
- 差异基因(DEG)、GO/KEGG 富集、WGCNA 共表达网络
- SNP / 品种间遗传分化、功能基因（如褪黑素通路）挖掘
- 产出论文成稿：paper.html / paper.docx / paper.pptx + Shiny 交互应用

## 三、环境（本机已验证，避免重蹈 conda 坑）
- **R 系统版**：`C:\Program Files\R\R-4.2.1\bin\Rscript.exe`（4.2.1，按实际安装位置调整）
  - Bioconductor 包装到自定义库：`C:\Users\你的用户名\R\rlib`（脚本首行 `.libPaths(c(".../rlib",.libPaths()))`，路径按实际调整）
- **Python**：`python`（3.12+，确保已在 PATH；或用 WorkBuddy 托管 Python `...\.workbuddy\binaries\python\versions\<ver>\python.exe`）（docx/pptx/matplotlib/pandas 已装）
- **salmon**：经 WSL2 Ubuntu-22.04 跑 Linux 二进制(v1.10.0)；SRA Toolkit `fasterq-dump` 转 FASTQ
- **R 关键包**：WGCNA, edgeR, DESeq2, ggplot2, ComplexHeatmap, pheatmap, igraph, shiny, bslib, DT, DOSE, patchwork, ggVennDiagram
- ⚠ **禁止用 conda 新建/安装环境**（safe-delete 在收尾清理临时索引时触发批量删除确认并回滚，环境永远建不成）。一律用系统 R + 自定义 rlib。

## 四、流程（脚本位于 scripts/01_*.py … 10_*.py）
| 步骤 | 阶段 | 关键脚本 | 关键产出 |
|---|---|---|---|
| 01 | 原始数据获取与质控 | 01_fastq_qc_clean_reads.py / SRA Toolkit | clean reads 统计 + 样本-表型映射(Table1) |
| 02 | 注释与统计 | 02_annotation_and_tables.py | 注释统计(Table2) |
| 03 | 差异表达与褪黑素基因(R) | 03_de_and_melatonin.R | 模式A:185 DEG + 258 褪黑素通路基因 / 模式B:标准 DEG 列表 |
| 04 | GO/KEGG 富集 | 04_enrichment.py | 富集表+气泡图(可纯Python ORA) |
| 05 | SNP 与遗传分化 | 05_snp_melatonin.py | 每品种 269–606 SNP；pN/pS 0.533–0.788 |
| 06 | 表格汇总 | 06_tables.py / gen_tables.py | Table1–7(真实表格) |
| 07 | 主图(R) | 07_figures_main.R | Fig1–6 基础图 600 DPI |
| 08 | WGCNA 共表达 | 08_wgcna.R | 34 模块(yellow r=0.718, magenta r=-0.857) |
| 09 | 缩略图预览 | 09_make_previews.py | 低分辨率预览 |
| 10 | 论文成稿 | 10_build_paper.py / paper_full.py | paper.html/docx/pptx + Shiny |

## 五、提示词模板（直接发给 AI 智能体驱动流水线）
- **数据**：下载 NCBI SRA 中 X 品种×Y 阶段原始 fastq；fasterq-dump 转 FASTQ，校验文件>1GB 判成功；输出样本-表型映射表。先统计每组样本数判断单样本/有重复。
- **定量**：salmon(k=31) 在参考转录本上定量；aggregate.py 按 tx2gene 聚合成基因 count/TPM 矩阵。
- **差异（模式A 单样本无重复）**：median-ratio 归一 + 固定离散度 0.1 的 Wald 近似 p，以 |log2FC|≥1 且 baseMean≥10 为主判定；p 仅排序参考。
- **差异（模式B 有重复）**：estimateDisp → design=~condition → Wald/LRT；以 padj<0.05 且 |log2FC|≥1 为 DEG；先做 PCA/聚类质控。
- **网络**：WGCNA 得模块；Bonferroni 校正(P<0.05/检验数)筛显著模块；提取 hub gene 共表达网络。
- **成稿**：matplotlib/ggplot2 出 600 DPI 图；Table1–7 用真实表格（非图片）插入正文；生成 HTML/DOCX/PPTX 三格式 + 起 Shiny 应用。

## 六、已知坑与对策（务必先套用）
- **conda safe-delete 死锁** → 系统 R + 自定义 rlib，绝不 conda create/install。
- **docx 被 Word/预览占用→PermissionError** → safe_save：先写 paper.docx，捕获 PermissionError 回退 paper_new.docx；本机不能删文件，勿先删再写。
- **matplotlib ∝ 缺字(豆腐块)** → Times New Roman 缺 U+221D，用 mathtext `$\propto$`。
- **中文路径 R 乱码** → 矩阵/输出先拷到 ASCII 临时路径，结束再移回。
- **单样本无重复(模式A)** → 固定离散度 0.1 + 折叠变化法为主判定；结论需注明局限性并建议 qRT-PCR 验证。
- **有重复(模式B)离群** → 先做 PCA/聚类，剔除离群样本再估计离散度，否则 dispersion 被拉高、灵敏度下降。
- **salmon 无 Windows 版** → WSL 内 Linux 二进制，--http1.1 规避 HTTP/2 断流。
- **Shiny 公网难（CGNAT 无公网IPv4）** → 免费 shiny 按用户数受内存限制(Win 下每会话一个 R 进程)；公网分享用 shinyapps.io 或内网穿透，需账号 token。

## 七、资源需求
- **最低**：4 核/8 线程 · 16 GB RAM · 128 GB 工作盘
- **推荐**：8 核/16 线程 · 32–64 GB RAM · 256 GB SSD
- **峰值磁盘**≈101 GB（FASTQ 84 GB 定量后可删）；参考盘≈0.3 GB 一次性复用；最终结果仅 ~0.2–0.6 GB。
- **本地不足→上云**：腾讯云标准型 S5(8 vCPU/32 GB)+200 GB 增强型 SSD，Ubuntu 22.04 即可完整复现；无需 GPU，勿选 GPU 实例。

## 八、参考交付物（本工作区）
- `paper.html` / `paper.docx` / `paper.pptx` —— 论文三格式成稿
- `shiny_app/app.R` —— 交互式图表应用（本地 http://localhost:7788）
- `tables/Table1.csv … Table7.csv` —— 7 个真实数据表
- `figures/` —— Fig1–Fig6（600 DPI PNG+PDF）
- `paper_case.html / paper_case.docx / paper_case.pptx` —— 项目案例（含提示词/硬件/云方案/两种重复模式）
- 历史案例（示例）：`<项目根目录>\案例文件_梨属5品种7阶段转录组分析.{html,docx,pptx}`（即本技能产出的三格式案例，路径按实际项目调整）

---

## © 版权与署名
- **作者**：丁保朋（Ding Baopeng），山西大同大学（Shanxi Datong University）。
- 本技能基于梨属 5 品种 × 7 阶段转录组表达谱分析及褪黑素功能基因挖掘研究整理并开源，欢迎在注明出处的前提下使用与二次开发。
