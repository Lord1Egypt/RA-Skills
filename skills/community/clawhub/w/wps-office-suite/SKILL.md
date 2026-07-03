---
name: wps-office-suite
description: WPS Office 全家桶 - 四引擎（WPS/MS Office/LibreOffice/纯Python）智能识别用户已安装软件，纯Python模式支持排序/筛选/图表/公式/统计，含文档模板、最佳实践案例、反模式FAQ、环境自检、错误速查手册
version: 2.5.0
---


# WPS Office 全家桶 v2.5.0 ✅

> 🏗️ **四引擎智能识别**：自动检测用户电脑已安装的软件，按 WPS → MS Office → LibreOffice → 纯Python 顺序选择最合适的引擎
> ✨ **纯Python模式增强**：排序、筛选、图表、公式、统计 — 跨平台全部支持
> 📚 **文档模板 + 最佳实践**：3个即用模板 + 10个最佳实践案例 + 反模式FAQ
> 🛡️ **四道安全防线**：引擎自检 + 路径校验 + 错误中文化 + 数据零上传

---

## 🚀 分钟上手

### 1. 检查环境

```bash
python scripts/wps_test.py
```

### 2. 查看当前引擎

```bash
python scripts/wps_word.py engine-info
```

### 3. 创建文件

```bash
python scripts/wps_word.py create --title "测试文档"
python scripts/wps_excel.py create --name "预算表" --sheets "收入,支出"
python scripts/wps_ppt.py create --title "推广方案"
```

---

## 🔧 功能矩阵

| 功能 | WPS 模式 | MS Office 模式 | LibreOffice 模式 | 纯Python 模式 |
|------|----------|---------------|-----------------|----------|
| **创建 Word** | ✅ | ✅ | ✅（回退） | ✅ |
| **编辑 Word** | ✅ | ✅ | ❌ | ✅ |
| **格式设置（字体/对齐/颜色）** | ✅ | ✅ | ❌ | ✅ |
| **表格创建/编辑** | ✅ | ✅ | ❌ | ✅ |
| **图片插入** | ✅ | ❌ | ❌ | ✅ |
| **目录生成** | ✅ | ✅ | ❌ | ✅ |
| **Word → PDF/HTML/TXT** | ✅ | ✅ | ✅ | ✅（需LibreOffice） |
| **创建 Excel** | ✅ | ✅ | ✅（回退） | ✅ |
| **数据录入** | ✅ | ❌ | ❌ | ✅ |
| **公式计算** | ✅ | ❌ | ❌ | ✅ |
| **图表生成（柱/折/饼）** | ✅ | ❌ | ❌ | ✅ |
| **多列排序** | ✅ | ✅（回退） | ✅（回退） | ✅ |
| **多条件筛选（AND/OR）** | ✅ | ✅（回退） | ✅（回退） | ✅ |
| **数据汇总（SUM/AVG/MAX/MIN/COUNT）** | ✅ | ✅ | ✅ | ✅ |
| **创建 PPT** | ✅ | ✅ | ✅（回退） | ✅ |
| **添加幻灯片** | ✅ | ❌ | ❌ | ❌ |
| **插入内容** | ✅ | ❌ | ❌ | ❌ |
| **PPT 主题应用** | ✅ | ❌ | ❌ | ❌ |
| **PPT → PDF/PNG** | ✅ | ❌ | ✅ | ✅（需LibreOffice） |
| **环境自检** | ✅ | ✅ | ✅ | ✅ |
| **反馈入口** | ✅ | ✅ | ✅ | ✅ |

> 💡 **回退**：MS Office/LibreOffice 引擎不支持时，自动回退到纯Python实现

---

## 🏗️ 引擎智能选择 v2.5

自动检测用户电脑**实际已安装**的软件，无需手动配置：

```
检测流程：
  ① 尝试 WPS Office → ✅ WPS 模式（功能最全，推荐）
  ② 尝试 Microsoft Office → ✅ MS Office 模式（兼容）
  ③ 尝试 LibreOffice Headless → ✅ LibreOffice 模式（跨平台兜底）
  ④ 都没有 → ✅ 纯Python 模式（免安装，创建+编辑基础功能）
```

### 引擎检测原理

| 检测项 | 方法 | 适用平台 |
|--------|------|---------|
| WPS | COM 接口调用测试 | Windows |
| MS Word | COM 接口调用测试 | Windows |
| MS Excel | COM 接口调用测试 | Windows |
| MS PPT | COM 接口调用测试 | Windows |
| LibreOffice | `soffice` PATH 检测 + 注册表查询 | Windows / Linux / macOS |

> 📝 **说明**：LibreOffice 模式使用 Headless（无界面）调用，命令为 `soffice --headless --convert-to pdf`，支持 PDF/HTML/TXT 格式转换。

---

## 📂 文档模板（开箱即用）

Skill 内置 3 个常用文档模板，可直接复制使用：

| 模板 | 文件 | 用途 |
|------|------|------|
| 工作报告 | `templates/report_template.docx` | 周报/月报/汇报 |
| 月度预算 | `templates/budget_template.xlsx` | 收入支出汇总 |
| 商务PPT | `templates/business_ppt_template.pptx` | 项目汇报/方案 |

```bash
# 复制模板到当前目录
copy templates\report_template.docx 我的周报.docx
copy templates\budget_template.xlsx 家庭预算.xlsx
copy templates\business_ppt_template.pptx 项目汇报.pptx
```

---

## 💬 AI 助手对话示例

### 场景 1：零基础上手

```
你：帮我做个 Word 文档，标题"项目汇报"
AI：好的...
    python scripts/wps_word.py create --title "项目汇报"
✅ 已创建：项目汇报.docx
   当前引擎：WPS Office（功能最全）
```

### 场景 2：跨平台兼容（无WPS环境）

```
你：把 contract.docx 转成 PDF
AI：⚠️ 未检测到 WPS/MS Office，尝试 LibreOffice Headless...
    soffice --headless --convert-to pdf contract.docx
✅ 已生成：contract.pdf（LibreOffice模式）
```

### 场景 3：纯Python排序（跨平台）

```
你：把 sales.xlsx 按销售额从高到低排
AI：⚠️ 当前为纯Python模式，使用 openpyxl 排序...
    python scripts/wps_excel.py sort --file sales.xlsx --sheet Q1 --sorts '[{"column":"销售额","ascending":false}]'
✅ 排序完成（87 行）
```

### 场景 4：纯Python图表（跨平台）

```
你：给 sales.xlsx 生成柱状图
AI：⚠️ 当前为纯Python模式，使用 openpyxl 图表...
    python scripts/wps_excel.py chart --file sales.xlsx --sheet Q1 --type bar --data A1:B10
✅ 图表已生成（嵌入到 Excel 中）
```

### 场景 5：数据汇总统计

```
你：统计 sales.xlsx 销售额的总和、平均值、最大值
AI：好的...
    python scripts/wps_excel.py stats --file sales.xlsx --sheet Q1 --column B --type SUM
    ✅ 总和: ¥1,250,000
    python scripts/wps_excel.py stats --file sales.xlsx --sheet Q1 --column B --type AVG
    ✅ 平均值: ¥14,368
    python scripts/wps_excel.py stats --file sales.xlsx --sheet Q1 --column B --type MAX
    ✅ 最大值: ¥82,000
```

---

## 🏆 最佳实践（10 个案例）

### BP-1：大文件处理策略

```
问题：50MB 的 Word 文档操作很慢
策略：
  1. 先用纯Python模式读取内容：python scripts/wps_word.py info --file big.docx
  2. 定位到具体段落后再编辑
  3. 避免频繁保存（每次保存触发全量写入）
```

### BP-2：批量文件重命名

```
问题：20 个文件需要统一命名规范
策略：
  1. 用 document_manager.py 列出所有文件
  2. 批量重命名（加日期前缀）
  3. 用 format_converter.py 批量转换格式
```

### BP-3：数据报表自动化

```
问题：每周重复做相同格式的报表
策略：
  1. 创建模板文件（含公式和图表位置）
  2. 每周用 input 命令录入新数据
  3. 公式和图表自动更新
  4. 导出 PDF 分发
```

### BP-4：多 Sheet 数据汇总

```
问题：12 个月的数据在 12 个 Sheet，需要年度汇总
策略：
  1. 用 add-sheet 创建"年度汇总"Sheet
  2. 用公式跨 Sheet 引用：=SUM(1月:12月!B2)
  3. 用 stats 命令验证汇总结果
```

### BP-5：条件格式筛选导出

```
问题：从 1000 条记录中筛出"销售额>5000 且 地区=华东"
策略：
  python scripts/wps_excel.py filter --file data.xlsx --sheet Q1 \
    --conditions '[{"column":"销售额","op":">","value":"5000"},{"column":"地区","op":"=","value":"华东"}]' \
    --logic AND
  ✅ 筛出 12 条记录
```

### BP-6：PPT 批量生成

```
问题：为 10 个客户生成个性化 PPT
策略：
  1. 创建模板 PPT（含占位符）
  2. 用脚本批量替换占位符
  3. 每个客户一个 add-slide + insert
```

### BP-7：Word 报告自动生成

```
问题：每周生成格式固定的周报
策略：
  1. 复制模板：copy templates\report_template.docx 本周周报.docx
  2. 用 edit 命令追加内容
  3. 用 format 命令设置标题格式
  4. 用 export 生成 PDF
```

### BP-8：Excel 数据透视替代

```
问题：没有 WPS，需要数据透视表功能
策略：
  1. 用 stats 命令做 SUM/AVG/COUNT 汇总
  2. 用 filter 做多维筛选
  3. 用 chart 生成可视化图表
  4. 组合使用完成透视分析
```

### BP-9：跨平台文档转换

```
问题：Linux 服务器上需要把 Word 转 PDF
策略：
  1. 安装 LibreOffice：sudo apt install libreoffice
  2. 引擎自动检测为 LIBREOFFICE
  3. 直接 export --format pdf
```

### BP-10：定时自动化

```
问题：每天凌晨自动生成报表
策略：
  1. 编写自动化脚本（调用 wps_excel.py + wps_word.py）
  2. 使用 WorkBuddy automation 定时执行
  3. 输出到指定目录
```

---

## 🚫 反模式 FAQ（避免这些坑）

### ❌ 反模式 1：频繁创建/销毁 Worker

```
错误做法：
  for i in range(100):
      subprocess.call(["python", "wps_word.py", "create", ...])  # 每次启动新进程

正确做法：
  # 使用 wps_worker.py 的 stdin/stdout 协议，保持进程常驻
  # 或在一次操作中完成多个任务
```

### ❌ 反模式 2：忽略引擎差异

```
错误做法：
  # 在 Linux 上尝试调用 WPS COM 接口
  python scripts/wps_word.py create --title "test"  # 失败！

正确做法：
  # 先检查引擎
  python scripts/wps_word.py engine-info
  # 根据引擎选择合适操作
```

### ❌ 反模式 3：大文件一次性加载

```
错误做法：
  # 50MB 文件直接读取全部内容到内存
  data = ws.UsedRange.Value  # 内存爆炸！

正确做法：
  # 分批处理，每次读取 1000 行
  for r in range(1, 1001):
      row = ws.Cells(r, 1).Value
```

### ❌ 反模式 4：不检查返回值

```
错误做法：
  subprocess.call(["python", "wps_word.py", "create", ...])
  # 直接假设成功，继续下一步

正确做法：
  result = subprocess.check_output(...)
  data = json.loads(result)
  if not data.get("ok"):
      print(f"错误: {data.get('error')}")
      # 查看错误码，按 E001-E015 解决
```

### ❌ 反模式 5：中文路径不转义

```
错误做法：
  python scripts/wps_word.py edit --file D:\中文\报告.docx --text "xxx"

正确做法：
  # 方法1：加引号
  python scripts/wps_word.py edit --file "D:\中文\报告.docx" --text "xxx"
  # 方法2：改用英文路径
  python scripts/wps_word.py edit --file D:\docs\report.docx --text "xxx"
```

### ❌ 反模式 6：同时操作同一文件

```
错误做法：
  # 两个进程同时写入同一文件
  Process 1: wps_word.py edit --file doc.docx --text "A"
  Process 2: wps_word.py edit --file doc.docx --text "B"

正确做法：
  # 串行操作，等上一个完成后再开始下一个
```

### ❌ 反模式 7：不释放 COM 对象

```
错误做法：
  wps = win32com.client.Dispatch("WPS.Application")
  doc = wps.Documents.Open("file.docx")
  # 忘记调用 wps.Quit() → 进程残留！

正确做法：
  # 使用 wps_worker.py 的 release_wps() 自动释放
  # 或在 finally 块中调用 wps.Quit()
```

### ❌ 反模式 8：忽略超时

```
错误做法：
  subprocess.call(["python", "wps_worker.py"])  # 可能永远挂起

正确做法：
  proc = subprocess.Popen(...)
  stdout, stderr = proc.communicate(timeout=120)  # 设置超时
```

---

## ⚠️ 能力边界说明

| 限制项 | 说明 | 解决方案 |
|--------|------|---------|
| **文件大小** | WPS/Excel 模式建议 < 50MB | 大文件先分片处理（拆分 Sheet/Section） |
| **复杂度** | 透视表/VBA/ActiveX 不支持 | 使用 pandas 或手动处理 |
| **网络文件** | 不支持 HTTP/URL 下载 | 先手动下载到本地，再调用 Skill |
| **并发限制** | 同一时间只能操作同一引擎的一个实例 | 等待上次操作完成后再发起 |
| **中文名文件路径** | 建议改用英文路径 | 路径中避免中文和特殊字符 |
| **实时协作** | 不支持多人同时编辑同一文件 | 通过手动分发和合并 |
| **跨平台** | 添加幻灯片/主题/插入内容 仅 WPS | 使用纯Python创建+LibreOffice转换 |

---

## 🚨 错误速查手册 v2.5（15个错误ID）

### E001-E010：用户可自助解决

| ID | 错误 | 解决 |
|----|------|------|
| E001 | WPS 未安装或 COM 注册失败 | 安装 WPS 后重启电脑 |
| E002 | python-docx 未安装 | `pip install python-docx openpyxl python-pptx` |
| E003 | 文件路径不存在或无法访问 | 改用英文路径或以管理员运行 |
| E004 | 格式转换失败（纯Python不支持） | 安装 WPS 或 LibreOffice |
| E005 | 排序/筛选/图表需要 WPS 模式 | 安装 WPS 或改用纯Python模式（v2.5已支持） |
| E006 | WPS/LibreOffice 卡住无响应 | 任务管理器结束进程；更新到最新版 |
| E007 | 权限不足 | 或以管理员运行；检查文件只读属性 |
| E008 | pywin32 导入失败 |  `pip uninstall pywin32 && pip install pywin32` |
| E009 | Python 版本过低 | 升级到 Python 3.8+ |
| E010 | 当前引擎不支持此功能 | 安装 WPS 或改用 info 查看能力矩阵 |

### E011-E015：需要进一步排查

| ID | 错误 | 解决 |
|----|------|------|
| E011 | LibreOffice 未安装 | 下载 LibreOffice 并添加到 PATH |
| E012 | LibreOffice 转换失败 | 检查源文件是否损坏；避免中文路径 |
| E013 | 文件不存在 | 确认路径正确；未被删除或移动 |
| E014 | 未知运行时错误 | 运行环境自检 `wps_test.py`；联系反馈 |
| E015 | 不支持的操作或格式 | 输出格式改为 pdf/txt/html |

---

## 📋 命令速查

### Word

```bash
python scripts/wps_word.py create --title "report" --body "正文内容"
python scripts/wps_word.py edit --file "report.docx" --text "新增内容" --position end
python scripts/wps_word.py format --file "report.docx" --font "微软雅黑" --size 14 --align center --bold
python scripts/wps_word.py export --file "report.docx" --format pdf
python scripts/wps_word.py info --file "report.docx"
python scripts/wps_word.py engine-info
```

### Excel

```bash
python scripts/wps_excel.py create --name "Sales" --sheets "Q1,Q2,Q3"
python scripts/wps_excel.py input --file "Sales.xlsx" --sheet "Q1" --data '[["A",100],["B",200]]'
python scripts/wps_excel.py formula --file "Sales.xlsx" --sheet "Q1" --cell "C1" --formula "=SUM(A1:B1)"
python scripts/wps_excel.py chart --file "Sales.xlsx" --sheet "Q1" --type bar --data "A1:B10" --title "销售趋势"
python scripts/wps_excel.py sort --file "Sales.xlsx" --sheet "Q1" --sorts '[{"column":"Price","ascending":false}]'
python scripts/wps_excel.py filter --file "Sales.xlsx" --sheet "Q1" --conditions '[{"column":"Price","op":">","value":"50"}]' --logic AND
python scripts/wps_excel.py add-sheet --file "Sales.xlsx" --sheet "Q4" --headers '["Product","Price"]' --data '[["X",300]]'
python scripts/wps_excel.py stats --file "Sales.xlsx" --sheet "Q1" --column "B" --type SUM
python scripts/wps_excel.py info --file "Sales.xlsx"
python scripts/wps_excel.py engine-info
```

### PPT

```bash
python scripts/wps_ppt.py create --title "Pitch"
python scripts/wps_ppt.py add-slide --file "Pitch.pptx" --title "Intro"
python scripts/wps_ppt.py insert --file "Pitch.pptx" --slide 2 --content "Key points"
python scripts/wps_ppt.py theme --file "Pitch.pptx" --name business_blue
python scripts/wps_ppt.py export --file "Pitch.pptx" --format pdf
python scripts/wps_ppt.py info --file "Pitch.pptx"
python scripts/wps_ppt.py engine-info
```

### 🆕 格式设置（纯Python模式）

```bash
# Word 格式设置
python scripts/wps_word.py format --file "report.docx" --font "微软雅黑" --size 14 --align center --bold --first-indent 0.74

# Excel 添加 Sheet
python scripts/wps_excel.py add-sheet --file "Sales.xlsx" --sheet "Q4" --headers '["A","B","C"]'

# Word 添加表格
python scripts/wps_word.py add-table --file "report.docx" --headers "姓名,年龄,城市" --data '[["张三",25,"北京"],["李四",30,"上海"]]'

# Word 插入图片
python scripts/wps_word.py insert-image --file "report.docx" --image "logo.png" --width 10 --caption "公司LOGO"
```

### 🆕 环境自检

```bash
python scripts/wps_test.py              # 人类可读报告
python scripts/wps_test.py --json       # JSON 格式（程序分析）
```

### 🆕 反馈入口

```bash
python scripts/wps_feedback.py page     # 打开反馈页面（浏览器）
python scripts/wps_feedback.py email    # 打开邮件客户端（自动附带系统信息）
```

---

## 📊 版本兼容矩阵

| Python | WPS Office | LibreOffice | Windows | macOS | Linux | 状态 |
|--------|-----------|-------------|---------|-------|-------|------|
| 3.8+ | 2019+ | - | ✅ | ⚠️ | ❌ | 基础 |
| 3.8+ | 365 | - | ✅ | ✅ | ❌ | 最佳 |
| 3.8+ | - | 7.0+ | ✅ | ✅ | ✅ | 跨平台推荐 |
| 3.8+ | - | - | ✅ | ✅ | ✅ | 纯Python |

> ⚠️ = 部分功能受限，❌ = 对应引擎不可用（如 WPS 在 Linux 上不支持）

---

## ⚠️ 安全须知

**✅ 四道防线保障安全**：
1. **引擎自检**：启动时自动检测可用引擎，崩溃自动重启
2. **路径校验**：`safe_path()` 全面校验，拒绝非法路径和特殊字符
3. **错误中文化**：所有错误 ID 提供详细中文说明和操作步骤
4. **数据零上传**：所有处理在本地完成，不上传任何内容到互联网

**📝 注意事项**：
- 批量操作时，桌面会创建 `WPS_Backup` 文件夹保存副本
- macOS 上 WPS 不支持所有功能
- 纯 Python 模式下格式设置有限，复杂排版建议安装 WPS
- 所有文件操作在本地进行，不会联网
- LibreOffice Headless 模式下不支持实时预览

---

## 📝 版本记录

| 版本 | 日期 | 本次更新 |
|------|------|---------|
| **v2.5.0** | 2026-07-03 | ✨ 纯Python模式增强：排序/筛选/图表/公式/统计全部支持；📂 新增文档模板目录（报告/预算/PPT）；🏆 新增10个最佳实践案例；🚫 新增反模式FAQ（8个常见错误）；📋 能力边界说明更新；🔧 Excel CLI 增加 formula/chart/add-sheet/stats 子命令；🔄 纯Python模式回退机制（MS Office/LibreOffice不支持时自动回退） |
| v2.2.0 | 2026-06-30 | 🏗️ 四引擎智能识别（WPS/MS Office/LibreOffice/纯Python）；🆕 LibreOffice Headless 跨平台兜底；✨ 纯Python格式设置/表格/图片插入；📋 错误ID系统（E001-E015）；📐 能力边界说明；🔧 中文化提示 |
| v2.1.0 | 2026-06-28 | 🆕 目录生成（TOC）；🆕 环境自检（test）；🆕 反馈入口；📚 错误速查手册（10个FAQ）；🎬 用例库（20个端到端场景） |
| v2.0.0 | 2026-06-28 | 🏗️ 三引擎自动切换；🤖 AI助手零学习成本；🛡️ 三道安全防线 |
| v1.0.0 | 2026-06-28 | 初始版本，三大组件 + 格式转换 |