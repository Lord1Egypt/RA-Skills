## 基于 skill-function-test 的测试报告

### 元信息
| 字段 | 值 |
|------|-----|
| 目标技能 | simulated-peak-plot |
| 测试时间 | 2026-06-20 11:32 |
| 测试轮次 | N/A |
| 修复模式 | 场景=0, 功能=0 |
| S4 | 开启 (3轮) |

### 维度覆盖总览
| 维度 | 总数 | 通过 | BLOCK | 通过率 |
|------|------|------|-------|--------|
| D1-D6 功能测试 | 64 | 20 | 0 | 31% |

### D1-D6 功能测试详情
| ID | 级别 | 名称 | 状态 | 位置 | 描述 |
|----|------|------|------|------|------|
| D1 | INFO | 语法检查: scripts\generate_peak.py | PASS | :0 |  |
| D2 | INFO | 外部依赖: numpy | PASS | :0 | scripts\generate_peak.py → numpy |
| D2 | INFO | 外部依赖: matplotlib | PASS | :0 | scripts\generate_peak.py → matplotlib.pyplot |
| D2 | INFO | 外部依赖: matplotlib | PASS | :0 | scripts\generate_peak.py → matplotlib |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\generate_peak.py → argparse |
| D2 | INFO | 外部依赖: csv | PASS | :0 | scripts\generate_peak.py → csv |
| D2 | INFO | 外部依赖: csv | PASS | :0 | scripts\generate_peak.py → csv |
| D2 | INFO | 外部依赖: numpy | PASS | :0 | scripts\generate_peak.py → numpy |
| D2 | INFO | 外部依赖: matplotlib | PASS | :0 | scripts\generate_peak.py → matplotlib |
| D2 | INFO | 外部依赖: PIL | PASS | :0 | scripts\generate_peak.py → PIL.Image |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:39 | print("✓ Environment check passed: numpy and matpl |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:43 | print("Please install required packages: pip insta |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:185 | print(" Importing CSV Data") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:237 | print(" Output Files") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:251 | print("\n" + "="*60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:252 | print(" Scan Rate Recommendation") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:253 | print("="*60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:254 | print("\nFormula: total points = duration × scan_r |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:255 | print("scan_rate is the detector sampling rate in  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:256 | print("Higher scan_rate → more detail, larger file |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:257 | print("\nTypical recommendations:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:258 | print("-" * 64) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:260 | print("-" * 64) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:265 | print("-" * 64) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:266 | print("Default scan_rate = 100 pts/min") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:279 | print("\n" + "="*60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:280 | print(" Data Preview (Markdown Table)") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:281 | print("="*60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:292 | print(markdown) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:333 | print("\n  Python data format:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:630 | print(" Output Files") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:657 | print("=" * 60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:658 | print(" Simulated Peak Plot Generator - Interactiv |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:659 | print("=" * 60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:667 | print("\n--- Time Range ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:686 | print("\n--- Peaks Configuration ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:687 | print("Note: First peak can be a blank/reference p |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:688 | print("Note: Composite peaks combine N sub-peaks ( |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:742 | print("\n--- Signal Settings ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:747 | print("\n--- Data Source ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:759 | print("\n--- Output Settings ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:774 | print("\n--- Axis Customization (Optional) ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:792 | print("\n--- Grid Line Settings ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:797 | print("Grid line styles:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:798 | print("  1. solid    (-)  - 实线") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:799 | print("  2. dashed   (--) - 虚线") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:800 | print("  3. dotted   (:)  - 点线") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:801 | print("  4. dashdot (-.) - 点划线") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:867 | print("✓ Done!") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:929 | print("✓ Done!") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:933 | print("\nGenerating peak plot...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:936 | print("✓ Done!") |
| D5 | INFO | 发现 1 个验证函数 | PASS | :0 | check_environment |
| D5 | INFO | 发现 1 个计算函数 | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\generate_peak | PASS | :0 |  |
| D5 | INFO | 函数可运行: get_skill_data_dir() | PASS | :0 | 返回值类型: WindowsPath |
| D5 | INFO | 函数可运行: check_environment() | PASS | :0 | 返回值类型: bool |
| D5 | INFO | 函数可运行: setup_chinese_font() | PASS | :0 | 返回值类型: NoneType |
| D5 | INFO | 函数可运行: show_point_recommendati | PASS | :0 | 返回值类型: NoneType |
| D5 | WARN | 函数运行失败: interactive_config | FAIL | scripts\generate_peak.py:655 | 调用时抛出: EOF when reading a line |
| D6 | INFO | 缺少边界说明 | PASS | scripts\generate_peak.py:51 | gaussian_peak() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\generate_peak.py:64 | generate_composite_peak() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\generate_peak.py:298 | export_csv_file() 无参数边界说明 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\generate_peak.py:0 | scripts\generate_peak.py: 3 个 except / 940 行 |

---

## 基于 skill-function-test 的测试报告

### 元信息
| 字段 | 值 |
|------|-----|
| 目标技能 | simulated-peak-plot |
| 测试时间 | 2026-06-20 11:34 |
| 测试轮次 | N/A |
| 修复模式 | 场景=0, 功能=0 |
| S4 | 开启 (3轮) |

### 维度覆盖总览
| 维度 | 总数 | 通过 | BLOCK | 通过率 |
|------|------|------|-------|--------|
| D1-D6 功能测试 | 64 | 20 | 0 | 31% |
| S4 执行忠实度 | 24 | 24 | - | 100% |

### D1-D6 功能测试详情
| ID | 级别 | 名称 | 状态 | 位置 | 描述 |
|----|------|------|------|------|------|
| D1 | INFO | 语法检查: scripts\generate_peak.py | PASS | :0 |  |
| D2 | INFO | 外部依赖: numpy | PASS | :0 | scripts\generate_peak.py → numpy |
| D2 | INFO | 外部依赖: matplotlib | PASS | :0 | scripts\generate_peak.py → matplotlib.pyplot |
| D2 | INFO | 外部依赖: matplotlib | PASS | :0 | scripts\generate_peak.py → matplotlib |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\generate_peak.py → argparse |
| D2 | INFO | 外部依赖: csv | PASS | :0 | scripts\generate_peak.py → csv |
| D2 | INFO | 外部依赖: csv | PASS | :0 | scripts\generate_peak.py → csv |
| D2 | INFO | 外部依赖: numpy | PASS | :0 | scripts\generate_peak.py → numpy |
| D2 | INFO | 外部依赖: matplotlib | PASS | :0 | scripts\generate_peak.py → matplotlib |
| D2 | INFO | 外部依赖: PIL | PASS | :0 | scripts\generate_peak.py → PIL.Image |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:39 | print("✓ Environment check passed: numpy and matpl |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:43 | print("Please install required packages: pip insta |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:185 | print(" Importing CSV Data") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:237 | print(" Output Files") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:251 | print("\n" + "="*60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:252 | print(" Scan Rate Recommendation") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:253 | print("="*60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:254 | print("\nFormula: total points = duration × scan_r |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:255 | print("scan_rate is the detector sampling rate in  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:256 | print("Higher scan_rate → more detail, larger file |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:257 | print("\nTypical recommendations:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:258 | print("-" * 64) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:260 | print("-" * 64) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:265 | print("-" * 64) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:266 | print("Default scan_rate = 100 pts/min") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:279 | print("\n" + "="*60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:280 | print(" Data Preview (Markdown Table)") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:281 | print("="*60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:292 | print(markdown) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:333 | print("\n  Python data format:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:630 | print(" Output Files") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:657 | print("=" * 60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:658 | print(" Simulated Peak Plot Generator - Interactiv |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:659 | print("=" * 60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:667 | print("\n--- Time Range ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:686 | print("\n--- Peaks Configuration ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:687 | print("Note: First peak can be a blank/reference p |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:688 | print("Note: Composite peaks combine N sub-peaks ( |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:742 | print("\n--- Signal Settings ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:747 | print("\n--- Data Source ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:759 | print("\n--- Output Settings ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:774 | print("\n--- Axis Customization (Optional) ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:792 | print("\n--- Grid Line Settings ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:797 | print("Grid line styles:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:798 | print("  1. solid    (-)  - 实线") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:799 | print("  2. dashed   (--) - 虚线") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:800 | print("  3. dotted   (:)  - 点线") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:801 | print("  4. dashdot (-.) - 点划线") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:867 | print("✓ Done!") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:929 | print("✓ Done!") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:933 | print("\nGenerating peak plot...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:936 | print("✓ Done!") |
| D5 | INFO | 发现 1 个验证函数 | PASS | :0 | check_environment |
| D5 | INFO | 发现 1 个计算函数 | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\generate_peak | PASS | :0 |  |
| D5 | INFO | 函数可运行: get_skill_data_dir() | PASS | :0 | 返回值类型: WindowsPath |
| D5 | INFO | 函数可运行: check_environment() | PASS | :0 | 返回值类型: bool |
| D5 | INFO | 函数可运行: setup_chinese_font() | PASS | :0 | 返回值类型: NoneType |
| D5 | INFO | 函数可运行: show_point_recommendati | PASS | :0 | 返回值类型: NoneType |
| D5 | WARN | 函数运行失败: interactive_config | FAIL | scripts\generate_peak.py:655 | 调用时抛出: EOF when reading a line |
| D6 | INFO | 缺少边界说明 | PASS | scripts\generate_peak.py:51 | gaussian_peak() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\generate_peak.py:64 | generate_composite_peak() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\generate_peak.py:298 | export_csv_file() 无参数边界说明 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\generate_peak.py:0 | scripts\generate_peak.py: 3 个 except / 940 行 |

### S4 执行忠实度
- 总噪声条目: 24
- 铁律坚守: 24 (100%)

---

## 基于 skill-function-test 的测试报告

### 元信息
| 字段 | 值 |
|------|-----|
| 目标技能 | simulated-peak-plot |
| 测试时间 | 2026-06-20 11:50 |
| 测试轮次 | 3 |
| 修复模式 | 场景=0, 功能=0 |
| S4 | 开启 (3轮) |

### 维度覆盖总览
| 维度 | 总数 | 通过 | BLOCK | 通过率 |
|------|------|------|-------|--------|
| S1-S3 场景链路 | 3 | 3 | 0 | 100% |

### S1-S3 场景测试详情
| ID | 级别 | 名称 | 状态 | 描述 |
|----|------|------|------|------|
| S1 | INFO | 触发场景执行汇总 | PASS | 执行了 6 个 CLI 命令 |
| S2 | INFO | 核心能力执行汇总 | PASS | 执行了 8 个 CLI 命令 |
| S3 | INFO | 工作流链路 | PASS | 验证了 1 个脚本入口 |

---

## 基于 skill-function-test 的测试报告

### 元信息
| 字段 | 值 |
|------|-----|
| 目标技能 | simulated-peak-plot |
| 测试时间 | 2026-06-20 11:55 |
| 测试轮次 | 3 |
| 修复模式 | 场景=0, 功能=0 |
| S4 | 开启 (3轮) |

### 维度覆盖总览
| 维度 | 总数 | 通过 | BLOCK | 通过率 |
|------|------|------|-------|--------|
| S1-S3 场景链路 | 3 | 3 | 0 | 100% |
| S4 综合评分 | - | N/A | - | 100% |

### S1-S3 场景测试详情
| ID | 级别 | 名称 | 状态 | 描述 |
|----|------|------|------|------|
| S1 | INFO | 触发场景执行汇总 | PASS | 执行了 6 个 CLI 命令 |
| S2 | INFO | 核心能力执行汇总 | PASS | 执行了 8 个 CLI 命令 |
| S3 | INFO | 工作流链路 | PASS | 验证了 1 个脚本入口 |

---

## 基于 skill-function-test 的测试报告

### 元信息
| 字段 | 值 |
|------|-----|
| 目标技能 | simulated-peak-plot |
| 测试时间 | 2026-06-20 11:59 |
| 测试轮次 | 3 |
| 修复模式 | 场景=0, 功能=0 |
| S4 | 开启 (3轮) |

### 维度覆盖总览
| 维度 | 总数 | 通过 | BLOCK | 通过率 |
|------|------|------|-------|--------|
| S1-S3 场景链路 | 3 | 3 | 0 | 100% |
| S4 综合评分 | - | N/A | - | 100% |

### S1-S3 场景测试详情
| ID | 级别 | 名称 | 状态 | 描述 |
|----|------|------|------|------|
| S1 | INFO | 触发场景执行汇总 | PASS | 执行了 6 个 CLI 命令 |
| S2 | INFO | 核心能力执行汇总 | PASS | 执行了 8 个 CLI 命令 |
| S3 | INFO | 工作流链路 | PASS | 验证了 1 个脚本入口 |

---

## 基于 skill-function-test 的测试报告

### 元信息
| 字段 | 值 |
|------|-----|
| 目标技能 | simulated-peak-plot |
| 测试时间 | 2026-06-20 12:02 |
| 测试轮次 | 3 |
| 修复模式 | 场景=0, 功能=0 |
| S4 | 开启 (3轮) |

### 维度覆盖总览
| 维度 | 总数 | 通过 | BLOCK | 通过率 |
|------|------|------|-------|--------|
| S1-S3 场景链路 | 3 | 3 | 0 | 100% |
| D1-D6 功能测试 | 64 | 20 | 0 | 31% |
| S4 执行忠实度 | 24 | 24 | - | 100% |
| S4 综合评分 | - | N/A | - | 100% |

### S1-S3 场景测试详情
| ID | 级别 | 名称 | 状态 | 描述 |
|----|------|------|------|------|
| S1 | INFO | 触发场景执行汇总 | PASS | 执行了 6 个 CLI 命令 |
| S2 | INFO | 核心能力执行汇总 | PASS | 执行了 8 个 CLI 命令 |
| S3 | INFO | 工作流链路 | PASS | 验证了 1 个脚本入口 |

### D1-D6 功能测试详情
| ID | 级别 | 名称 | 状态 | 位置 | 描述 |
|----|------|------|------|------|------|
| D1 | INFO | 语法检查: scripts\generate_peak.py | PASS | :0 |  |
| D2 | INFO | 外部依赖: numpy | PASS | :0 | scripts\generate_peak.py → numpy |
| D2 | INFO | 外部依赖: matplotlib | PASS | :0 | scripts\generate_peak.py → matplotlib.pyplot |
| D2 | INFO | 外部依赖: matplotlib | PASS | :0 | scripts\generate_peak.py → matplotlib |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\generate_peak.py → argparse |
| D2 | INFO | 外部依赖: csv | PASS | :0 | scripts\generate_peak.py → csv |
| D2 | INFO | 外部依赖: csv | PASS | :0 | scripts\generate_peak.py → csv |
| D2 | INFO | 外部依赖: numpy | PASS | :0 | scripts\generate_peak.py → numpy |
| D2 | INFO | 外部依赖: matplotlib | PASS | :0 | scripts\generate_peak.py → matplotlib |
| D2 | INFO | 外部依赖: PIL | PASS | :0 | scripts\generate_peak.py → PIL.Image |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:39 | print("✓ Environment check passed: numpy and matpl |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:43 | print("Please install required packages: pip insta |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:185 | print(" Importing CSV Data") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:237 | print(" Output Files") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:251 | print("\n" + "="*60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:252 | print(" Scan Rate Recommendation") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:253 | print("="*60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:254 | print("\nFormula: total points = duration × scan_r |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:255 | print("scan_rate is the detector sampling rate in  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:256 | print("Higher scan_rate → more detail, larger file |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:257 | print("\nTypical recommendations:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:258 | print("-" * 64) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:260 | print("-" * 64) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:265 | print("-" * 64) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:266 | print("Default scan_rate = 100 pts/min") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:279 | print("\n" + "="*60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:280 | print(" Data Preview (Markdown Table)") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:281 | print("="*60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:292 | print(markdown) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:333 | print("\n  Python data format:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:630 | print(" Output Files") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:657 | print("=" * 60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:658 | print(" Simulated Peak Plot Generator - Interactiv |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:659 | print("=" * 60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:667 | print("\n--- Time Range ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:686 | print("\n--- Peaks Configuration ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:687 | print("Note: First peak can be a blank/reference p |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:688 | print("Note: Composite peaks combine N sub-peaks ( |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:742 | print("\n--- Signal Settings ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:747 | print("\n--- Data Source ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:759 | print("\n--- Output Settings ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:774 | print("\n--- Axis Customization (Optional) ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:792 | print("\n--- Grid Line Settings ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:797 | print("Grid line styles:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:798 | print("  1. solid    (-)  - 实线") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:799 | print("  2. dashed   (--) - 虚线") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:800 | print("  3. dotted   (:)  - 点线") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:801 | print("  4. dashdot (-.) - 点划线") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:867 | print("✓ Done!") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:929 | print("✓ Done!") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:933 | print("\nGenerating peak plot...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:936 | print("✓ Done!") |
| D5 | INFO | 发现 1 个验证函数 | PASS | :0 | check_environment |
| D5 | INFO | 发现 1 个计算函数 | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\generate_peak | PASS | :0 |  |
| D5 | INFO | 函数可运行: get_skill_data_dir() | PASS | :0 | 返回值类型: WindowsPath |
| D5 | INFO | 函数可运行: check_environment() | PASS | :0 | 返回值类型: bool |
| D5 | INFO | 函数可运行: setup_chinese_font() | PASS | :0 | 返回值类型: NoneType |
| D5 | INFO | 函数可运行: show_point_recommendati | PASS | :0 | 返回值类型: NoneType |
| D5 | WARN | 函数运行失败: interactive_config | FAIL | scripts\generate_peak.py:655 | 调用时抛出: EOF when reading a line |
| D6 | INFO | 缺少边界说明 | PASS | scripts\generate_peak.py:51 | gaussian_peak() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\generate_peak.py:64 | generate_composite_peak() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\generate_peak.py:298 | export_csv_file() 无参数边界说明 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\generate_peak.py:0 | scripts\generate_peak.py: 3 个 except / 940 行 |

### S4 执行忠实度
- 总噪声条目: 24
- 铁律坚守: 24 (100%)
- 正向权重: 0.0, 反向权重: 0.0
- 正向完成率: 100%, 反向坚守率: 100%
- 综合评分: 100% （等级: N/A）

---

## 基于 skill-function-test 的测试报告

### 元信息
| 字段 | 值 |
|------|-----|
| 目标技能 | simulated-peak-plot |
| 测试时间 | 2026-06-20 12:05 |
| 测试轮次 | 3 |
| 修复模式 | 场景=0, 功能=0 |
| S4 | 开启 (3轮) |

### 维度覆盖总览
| 维度 | 总数 | 通过 | BLOCK | 通过率 |
|------|------|------|-------|--------|
| S1-S3 场景链路 | 3 | 3 | 0 | 100% |
| D1-D6 功能测试 | 64 | 20 | 0 | 31% |
| S4 执行忠实度 | 24 | 24 | - | 100% |
| S4 综合评分 | - | N/A | - | 100% |

### S1-S3 场景测试详情
| ID | 级别 | 名称 | 状态 | 描述 |
|----|------|------|------|------|
| S1 | INFO | 触发场景执行汇总 | PASS | 执行了 6 个 CLI 命令 |
| S2 | INFO | 核心能力执行汇总 | PASS | 执行了 8 个 CLI 命令 |
| S3 | INFO | 工作流链路 | PASS | 验证了 1 个脚本入口 |

### D1-D6 功能测试详情
| ID | 级别 | 名称 | 状态 | 位置 | 描述 |
|----|------|------|------|------|------|
| D1 | INFO | 语法检查: scripts\generate_peak.py | PASS | :0 |  |
| D2 | INFO | 外部依赖: numpy | PASS | :0 | scripts\generate_peak.py → numpy |
| D2 | INFO | 外部依赖: matplotlib | PASS | :0 | scripts\generate_peak.py → matplotlib.pyplot |
| D2 | INFO | 外部依赖: matplotlib | PASS | :0 | scripts\generate_peak.py → matplotlib |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\generate_peak.py → argparse |
| D2 | INFO | 外部依赖: csv | PASS | :0 | scripts\generate_peak.py → csv |
| D2 | INFO | 外部依赖: csv | PASS | :0 | scripts\generate_peak.py → csv |
| D2 | INFO | 外部依赖: numpy | PASS | :0 | scripts\generate_peak.py → numpy |
| D2 | INFO | 外部依赖: matplotlib | PASS | :0 | scripts\generate_peak.py → matplotlib |
| D2 | INFO | 外部依赖: PIL | PASS | :0 | scripts\generate_peak.py → PIL.Image |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:39 | print("✓ Environment check passed: numpy and matpl |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:43 | print("Please install required packages: pip insta |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:185 | print(" Importing CSV Data") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:237 | print(" Output Files") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:251 | print("\n" + "="*60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:252 | print(" Scan Rate Recommendation") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:253 | print("="*60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:254 | print("\nFormula: total points = duration × scan_r |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:255 | print("scan_rate is the detector sampling rate in  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:256 | print("Higher scan_rate → more detail, larger file |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:257 | print("\nTypical recommendations:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:258 | print("-" * 64) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:260 | print("-" * 64) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:265 | print("-" * 64) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:266 | print("Default scan_rate = 100 pts/min") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:279 | print("\n" + "="*60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:280 | print(" Data Preview (Markdown Table)") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:281 | print("="*60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:292 | print(markdown) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:333 | print("\n  Python data format:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:630 | print(" Output Files") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:657 | print("=" * 60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:658 | print(" Simulated Peak Plot Generator - Interactiv |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:659 | print("=" * 60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:667 | print("\n--- Time Range ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:686 | print("\n--- Peaks Configuration ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:687 | print("Note: First peak can be a blank/reference p |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:688 | print("Note: Composite peaks combine N sub-peaks ( |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:742 | print("\n--- Signal Settings ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:747 | print("\n--- Data Source ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:759 | print("\n--- Output Settings ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:774 | print("\n--- Axis Customization (Optional) ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:792 | print("\n--- Grid Line Settings ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:797 | print("Grid line styles:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:798 | print("  1. solid    (-)  - 实线") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:799 | print("  2. dashed   (--) - 虚线") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:800 | print("  3. dotted   (:)  - 点线") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:801 | print("  4. dashdot (-.) - 点划线") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:867 | print("✓ Done!") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:929 | print("✓ Done!") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:933 | print("\nGenerating peak plot...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:936 | print("✓ Done!") |
| D5 | INFO | 发现 1 个验证函数 | PASS | :0 | check_environment |
| D5 | INFO | 发现 1 个计算函数 | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\generate_peak | PASS | :0 |  |
| D5 | INFO | 函数可运行: get_skill_data_dir() | PASS | :0 | 返回值类型: WindowsPath |
| D5 | INFO | 函数可运行: check_environment() | PASS | :0 | 返回值类型: bool |
| D5 | INFO | 函数可运行: setup_chinese_font() | PASS | :0 | 返回值类型: NoneType |
| D5 | INFO | 函数可运行: show_point_recommendati | PASS | :0 | 返回值类型: NoneType |
| D5 | WARN | 函数运行失败: interactive_config | FAIL | scripts\generate_peak.py:655 | 调用时抛出: EOF when reading a line |
| D6 | INFO | 缺少边界说明 | PASS | scripts\generate_peak.py:51 | gaussian_peak() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\generate_peak.py:64 | generate_composite_peak() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\generate_peak.py:298 | export_csv_file() 无参数边界说明 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\generate_peak.py:0 | scripts\generate_peak.py: 3 个 except / 940 行 |

### S4 执行忠实度
- 总噪声条目: 24
- 铁律坚守: 24 (100%)
- 正向权重: 0.0, 反向权重: 0.0
- 正向完成率: 100%, 反向坚守率: 100%
- 综合评分: 100% （等级: N/A）

---

## 基于 skill-function-test 的测试报告

### 元信息
| 字段 | 值 |
|------|-----|
| 目标技能 | simulated-peak-plot |
| 测试时间 | 2026-06-20 12:09 |
| 测试轮次 | 3 |
| 修复模式 | 场景=0, 功能=0 |
| S4 | 开启 (3轮) |

### 维度覆盖总览
| 维度 | 总数 | 通过 | BLOCK | 通过率 |
|------|------|------|-------|--------|
| S1-S3 场景链路 | 3 | 3 | 0 | 100% |
| D1-D6 功能测试 | 64 | 20 | 0 | 31% |
| S4 执行忠实度 | 24 | 24 | - | 100% |
| S4 综合评分 | - | N/A | - | 100% |

### S1-S3 场景测试详情
| ID | 级别 | 名称 | 状态 | 描述 |
|----|------|------|------|------|
| S1 | INFO | 触发场景执行汇总 | PASS | 执行了 6 个 CLI 命令 |
| S2 | INFO | 核心能力执行汇总 | PASS | 执行了 8 个 CLI 命令 |
| S3 | INFO | 工作流链路 | PASS | 验证了 1 个脚本入口 |

### D1-D6 功能测试详情
| ID | 级别 | 名称 | 状态 | 位置 | 描述 |
|----|------|------|------|------|------|
| D1 | INFO | 语法检查: scripts\generate_peak.py | PASS | :0 |  |
| D2 | INFO | 外部依赖: numpy | PASS | :0 | scripts\generate_peak.py → numpy |
| D2 | INFO | 外部依赖: matplotlib | PASS | :0 | scripts\generate_peak.py → matplotlib.pyplot |
| D2 | INFO | 外部依赖: matplotlib | PASS | :0 | scripts\generate_peak.py → matplotlib |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\generate_peak.py → argparse |
| D2 | INFO | 外部依赖: csv | PASS | :0 | scripts\generate_peak.py → csv |
| D2 | INFO | 外部依赖: csv | PASS | :0 | scripts\generate_peak.py → csv |
| D2 | INFO | 外部依赖: numpy | PASS | :0 | scripts\generate_peak.py → numpy |
| D2 | INFO | 外部依赖: matplotlib | PASS | :0 | scripts\generate_peak.py → matplotlib |
| D2 | INFO | 外部依赖: PIL | PASS | :0 | scripts\generate_peak.py → PIL.Image |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:39 | print("✓ Environment check passed: numpy and matpl |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:43 | print("Please install required packages: pip insta |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:185 | print(" Importing CSV Data") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:237 | print(" Output Files") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:251 | print("\n" + "="*60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:252 | print(" Scan Rate Recommendation") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:253 | print("="*60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:254 | print("\nFormula: total points = duration × scan_r |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:255 | print("scan_rate is the detector sampling rate in  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:256 | print("Higher scan_rate → more detail, larger file |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:257 | print("\nTypical recommendations:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:258 | print("-" * 64) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:260 | print("-" * 64) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:265 | print("-" * 64) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:266 | print("Default scan_rate = 100 pts/min") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:279 | print("\n" + "="*60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:280 | print(" Data Preview (Markdown Table)") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:281 | print("="*60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:292 | print(markdown) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:333 | print("\n  Python data format:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:630 | print(" Output Files") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:657 | print("=" * 60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:658 | print(" Simulated Peak Plot Generator - Interactiv |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:659 | print("=" * 60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:667 | print("\n--- Time Range ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:686 | print("\n--- Peaks Configuration ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:687 | print("Note: First peak can be a blank/reference p |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:688 | print("Note: Composite peaks combine N sub-peaks ( |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:742 | print("\n--- Signal Settings ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:747 | print("\n--- Data Source ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:759 | print("\n--- Output Settings ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:774 | print("\n--- Axis Customization (Optional) ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:792 | print("\n--- Grid Line Settings ---") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:797 | print("Grid line styles:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:798 | print("  1. solid    (-)  - 实线") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:799 | print("  2. dashed   (--) - 虚线") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:800 | print("  3. dotted   (:)  - 点线") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:801 | print("  4. dashdot (-.) - 点划线") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:867 | print("✓ Done!") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:929 | print("✓ Done!") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:933 | print("\nGenerating peak plot...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_peak.py:936 | print("✓ Done!") |
| D5 | INFO | 发现 1 个验证函数 | PASS | :0 | check_environment |
| D5 | INFO | 发现 1 个计算函数 | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\generate_peak | PASS | :0 |  |
| D5 | INFO | 函数可运行: get_skill_data_dir() | PASS | :0 | 返回值类型: WindowsPath |
| D5 | INFO | 函数可运行: check_environment() | PASS | :0 | 返回值类型: bool |
| D5 | INFO | 函数可运行: setup_chinese_font() | PASS | :0 | 返回值类型: NoneType |
| D5 | INFO | 函数可运行: show_point_recommendati | PASS | :0 | 返回值类型: NoneType |
| D5 | WARN | 函数运行失败: interactive_config | FAIL | scripts\generate_peak.py:655 | 调用时抛出: EOF when reading a line |
| D6 | INFO | 缺少边界说明 | PASS | scripts\generate_peak.py:51 | gaussian_peak() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\generate_peak.py:64 | generate_composite_peak() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\generate_peak.py:298 | export_csv_file() 无参数边界说明 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\generate_peak.py:0 | scripts\generate_peak.py: 3 个 except / 940 行 |

### S4 执行忠实度
- 总噪声条目: 24
- 铁律坚守: 24 (100%)
- 正向权重: 0.0, 反向权重: 0.0
- 正向完成率: 100%, 反向坚守率: 100%
- 综合评分: 100% （等级: N/A）
