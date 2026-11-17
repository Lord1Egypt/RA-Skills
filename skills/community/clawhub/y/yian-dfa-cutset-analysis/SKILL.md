---
name: yian-dfa-cutset-analysis
description: DFA 割集分析更新 skill。当用户要求对 Excel 工作包中的割集进行 DFA（Dependent Failure Analysis）分析或更新时触发，例如"帮我进行割集 DFA 的分析/更新"。自动读取包含 "Cut-Set List" 关键字的源 sheet（若存在多个，优先选不含 old 的最新清单，如 _new），只处理 Order 为 2 或 3 的割集，按割集名合并同类项，将结果更新到包含 "DFA Analysis-CutSet" 关键字的目标 sheet：A/B/C/D/E 自动同步，新增 7 行块的 D 列标红色、废弃割集加删除线；新增块逐格复制已有正常块的边框/字体/对齐/填充/行高做到格式完全一致，并按组件自动填写 G..O 草稿（已有块的人工内容保持不动）。适用于 EPS 全冗余平台 FTA 割集变更后的 DFA 同步。
---

# 毅安 DFA 割集分析

## 概述

本 skill 用于把 FTA 导出的最小割集（Cut-Set）同步更新到 DFA Analysis-CutSet 工作表中。它按割集名称合并同类项，自动处理编号、顶级事件、ASIL、事件描述的拆分，并标记新增/废弃割集以便人工确认。

## 使用方式

1. 确认用户已给出 Excel 文件路径（或已上传/放置在工作空间）。
2. 调用脚本完成自动更新：
   ```bash
   C:\Users\86133\.workbuddy\skills\yian-dfa-cutset-analysis\.venv\Scripts\python.exe C:\Users\86133\.workbuddy\skills\yian-dfa-cutset-analysis\scripts\dfa_cutset_analysis.py <excel_path> [--backup]
   ```
   - `--backup`：在修改前创建 `.xlsx.bak` 备份。
   - 源 sheet 与目标 sheet 通过关键字自动识别（"Cut-Set List" 与 "DFA Analysis-CutSet"）。
   - **源 sheet 选择**：若存在多个含 "Cut-Set List" 的 sheet，优先选**不含 `old`** 的那一个（即最新的 `_new` 清单）；避免误用旧清单。
   - **只处理 Order 2/3**：源 sheet 的 E 列 `Order` 标识割集阶数，脚本默认只处理 Order ∈ {2, 3} 的割集；其余阶数的割集既不新增也不删除线，目标中已有的非 2/3 行保持原样不动。可用 `--order 2 3 4` 等参数覆盖。
3. 脚本运行后，**执行覆盖度校验**（必须，见下节），再人工复核新生成的红色 7 行块：格式已自动与已有块对齐，G/H 为固定定义文本，I 为按组件自动套用的草稿，J-O 为按耦合因子规则填充的草稿值。

## 覆盖度校验（每次交付前必做）

运行内置脚本，确认源 sheet 的编号在目标 sheet 中都能找到：

```bash
C:\Users\86133\.workbuddy\skills\yian-dfa-cutset-analysis\.venv\Scripts\python.exe C:\Users\86133\.workbuddy\skills\yian-dfa-cutset-analysis\scripts\check_no_coverage.py <excel_path>
```

- **校验内容**：源 sheet（`Cut-Set List`，优先不含 `old`）A 列的每个编号，是否都能在目标 sheet（`DFA Analysis-CutSet`）A 列中找到。
- **匹配方式必须是按token（数字）匹配，不能用字符串包含匹配**。目标 A 列每个块内含多个编号（同一割集的多行被合并后以空格分隔，如`"1001 2001 3001 4001 50"`），因此必须先按空白/逗号拆分再逐个比对。用`in` 做子串匹配会产生误判（例如 `"100"` 会匹配到 `"1001"` 内部）。
- **判定标准**：以 **Order 2/3 为准**。范围内缺失数必须为 **0**（退出码 0）。范围外阶数（1/4/6…）的缺失会单独列出，属预期行为，不代表错误。
- **同时输出两项辅助信息**：
  - *范围外缺失按 Order 分布*：用于确认缺失全部来自不处理的阶数。
  - *反向孤儿*（目标 A 列有、源 A 列已无的编号）：应全部归属于**已加删除线的废弃块**；若出现不属于删除线块的孤儿，说明有问题，需人工排查。
- 源 sheet A 列中形如 `EP2x_SG01 FTA Cut Set:` 的行是**顶级事件标题行**，不是编号，脚本会单独识别并排除，不计入缺失。

## 自动处理规则

- 读取源 sheet 的 A/B/C/D/E/F 列，按 D 列割集名称合并（仅 Order 2/3）。
- 目标 sheet 结构：**每个割集占 7 行**。A/B/C/D 跨 7 行合并；E 按 (1-2, 3-4, 5-6) 三对合并，第 7 行单列；F 列每行 1 个标准耦合因子标签，G/H/I... 按行填写。
  - 注意：表头行（第 1、2 行）**不是**割集块；真正的割集块以 D 列纵向合并单元格为标志。脚本据此跳过表头，避免把表头误当成割集。
- A 列编号、B 列顶级事件 ID：相同割集的多行值按出现顺序合并，以空格分隔。
- C 列 ASIL：相同则只写一个；不同则把所有不同值列出。
- E 列：块内第 1-2 行写入 `DFA Coupling Factor\nSource of Common Causes and Coupling Factors\n<失效描述>`；块内第 3-4 行写入 `<安全机制描述>`；其余 E 单元格留空（与已有块一致）。
- F 列：7 个标准耦合因子标签，固定为
  1. 共享资源/ Shared resourse
  2. 共享信息输入/ Shared Information Inputs
  3. 环境抗干扰能力不足/ Insufficient Environmental Immunity
  4. 系统耦合 / Systematic Coupling
  5. 同类型组件/  Component of Identical Type
  6. 通讯/ Communication
  7. 非预期接口/ Unintended Interface
- **格式完全对齐**：新增块的每一行都从目标 sheet 中**第一个正常的已有块**（D 列未加删除线、字体非红色、且 D 纵向合并）逐格复制边框、字体（name/size/bold）、对齐方式、填充色、行高，因此新增块与已有块外观一致。唯D 列在此基础上改为红色，且保留原字体名与字号。
- **已有块保持不动**：已有块的人工填写的 G..O 内容不覆盖、不清空。
- **新增块自动填写 G..O（草稿，需人工复核）**：
  - G 列（共因和级联失效的来源）与 H 列（参考示例）：按耦合因子填入固定定义文本（已确认在全表所有块中完全一致）。
  - I 列（可能的根本原因）：按割集所属**组件**套用已有块中的真实措辞。识别顺序为 TMR sensor → TAS sensor → current sensor → Vcore → ECU power supply → EPS ECU（兜底，覆盖电机/转矩/角度/输出/温度等 ECU 内部功能割集）。割集描述与割集名称都会参与关键词匹配；CH2 割集会把草稿中的 CH1 自动替换为 CH2。
  - J..O 列：按耦合因子规则填入草稿——环境抗干扰与非预期接口行填 `CCF` + 对应测试/热仿真措施 + `NO`；共享资源行除电流传感器（无共享资源→全部 `N.A.`）外填 `CCF`/`NO`；其余行填 `N.A.`。
- 新增割集：目标 sheet 中没有的割集，在末尾**新增一个 7 行块**，A/B/C/D 合并、D 列字体设为红色。
- 废弃割集：源 sheet 中没有但目标 sheet 中已有的割集，对 7 行块中 A/B/C/D 合并区域加删除线，保留整块供人工确认。

## 异常处理

- 若脚本因环境、权限或 Excel 格式问题无法运行，改为参考 `references/procedure.md` 中的详细步骤，使用 `workbuddy-sheetagent` 或 `workbuddy-local-office-edit` 手动完成。
- 若 sheet 命名特殊（不含默认关键字），使用 `--source-sheet` 和 `--target-sheet` 显式指定。
- 若覆盖度校验未通过（退出码非 0），先看缺失项的 Order：范围外的缺失属预期；**范围内（Order 2/3）出现缺失**则说明目标表漏了割集，需排查源 sheet 选择是否正确（是否误用了 `_old`）或合并逻辑是否漏组。

## 依赖

- 脚本依赖 Python 3 与 openpyxl。
- 运行环境已预置在 `C:\Users\86133\.workbuddy\skills\yian-dfa-cutset-analysis\.venv` 中；如缺失，使用 venv 中的 pip 重新安装 `openpyxl`。

## 参考文档

- 详细步骤与截图对应规则见 [references/procedure.md](references/procedure.md)。
