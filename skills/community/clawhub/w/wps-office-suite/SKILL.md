---
name: wps-office-suite
description: WPS Office 全家桶 - 三引擎（WPS/MS Office/纯Python）自动适配，AI助手零学习成本，自然语言驱动，含目录生成、环境自检、错误速查手册
version: 2.1.0
---

# WPS Office 全家桶 v2.1 ✅

> 🏗️ **三引擎自动切换**：WPS → MS Office → 纯Python — **无 Office 也能用**
> 🤖 **AI助手零学习成本**：自然语言直接调用，傻瓜式教程
> 🛡️ **三道安全防线**：路径校验 + 引擎隔离 + 数据零上传
> 📚 **完全文档体系**：FAQ + 错误速查 + 用例库 + 环境自检

---

## 💬 在 AI 助手里这么说（零学习成本）

你和 AI 助手对话时，直接说需求就行：

| 你说 | AI 助手自动做 |
|------|-------------|
| 明天开周会，帮我做个汇报 PPT | 创建 PPT → 插入大纲 → 蓝色主题 → 导出PDF |
| 把这份 Word 转成 PDF，我要发邮件 | 格式转换 → 输出到原目录 |
| 打开我电脑上的合同.docx | 打开文档 |
| Excel 数据按金额从高到低排一下 | Excel 排序（多列） |
| 把表格里金额大于1000且城市是北京的多条件筛出来 | Excel 多条件筛选 |
| 做一个财务报表，分收入/支出/汇总三个 Sheet | Excel 创建多 Sheet |
| 帮我生成个目录，我文档标题太多了 | 目录生成 → 输出到文件 |
| 现在用的是什么引擎？能纯Python吗？ | 返回引擎信息 |
| 帮我测一下能不能用 | 环境自检一键排查 |
| ... | ... |

### 🧵 AI 助手对话示例

**场景 1：做汇报 PPT**

```
你：明天开周会，帮我做一个项目汇报 PPT，包含：背景、进展、问题、计划
AI：好的，我先创建 PPT，然后逐页插入内容...
    [执行一系列命令]
✅ PPT 已创建：项目汇报.pptx
   包含 5 页：封面、背景、进展、问题、计划
   使用了商务蓝色主题
   大小：245KB

你：把 PPT 转成 PDF
AI：正在转换...
✅ 已生成：项目汇报.pdf
```

**场景 2：处理 Excel**

```
你：打开 D:\数据\2026.xlsx，把销售额按从高到低排，找出前3名
AI：好的...
    [排序 + 筛选]
✅ 排序完成，前3名是：
    1. 华东区 - ¥1,250,000
    2. 华南区 - ¥980,000
    3. 华北区 - ¥850,000
```

**场景 3：无 Office 环境**

```
我：帮我用一个 Word 文档，标题是"会议纪要"
AI：⚠️ 未检测到 Office 软件，正在使用纯 Python 模式...
✅ 已创建：会议纪要.docx（纯Python模式）
   注意：纯Python模式下格式较简单
   建议安装 WPS Office 2019+ 获取完整功能
    pip install pywin32  # 安装后重启生效
```

---

## 🔰 Quick Start（1 分钟体验）

```bash
# 安装依赖（按需）
pip install pywin32                    # WPS/MS 模式（Windows，可选）
pip install python-docx openpyxl      # 纯Python模式（Word+Excel）
pip install python-pptx               # 纯Python模式（PPT）

# 创建文件（自动选引擎）
python scripts/wps_word.py create --title "测试文档"
python scripts/wps_excel.py create --name "预算表" --sheets "收入,支出"
python scripts/wps_ppt.py create --title "推广方案"

# 🆕 环境自检（一键测一下能不能用）
python scripts/wps_test.py

# 🆕 查看引擎信息
python scripts/wps_word.py engine-info
```

---

## 🏗️ 引擎自动选择

无需手动配置，自动检测：

```
检测流程：
  ① 尝试 WPS → ✅ WPS 模式（功能最全，推荐）
  ② 尝试 MS Office → ✅ Office 模式（兼容）
  ③ 都没有 → ✅ 纯 Python 模式（免安装，基础功能）
```

查看当前引擎：

```bash
python scripts/wps_word.py engine-info
# 输出: {"ok": true, "engine": "WPS", "ms_available": false, "pure_available": true}
```

---

## 📋 功能矩阵

| 功能 | WPS 模式 | MS Office 模式 | 纯 Python 模式 |
|------|----------|---------------|---------------|
| **创建 Word** | ✅ | ✅ | ✅ |
| **编辑 Word** | ✅ | ✅ | ✅ |
| **格式设置** | ✅ | ✅ | ⚠️（基础） |
| **目录生成** | ✅ | ✅ | ✅ |
| **Word → PDF** | ✅ | ✅ | ❌ |
| **创建 Excel** | ✅ | ✅ | ✅ |
| **数据录入** | ✅ | ⚠️ | ✅ |
| **公式计算** | ✅ | ❌ | ❌ |
| **图表生成** | ✅ | ❌ | ❌ |
| **多列排序** | ✅ | ❌ | ❌ |
| **多条件筛选** | ✅ | ❌ | ❌ |
| **创建 PPT** | ✅ | ✅ | ✅ |
| **添加幻灯片** | ✅ | ❌ | ❌ |
| **PPT → PDF** | ✅ | ❌ | ❌ |
| **环境自检** | ✅ | ✅ | ✅ |
| **反馈入口** | ✅ | ✅ | ✅ |

> 💡 **纯Python模式**适合：新建文件、简单内容、无 Office 环境
> 💡 **WPS模式**适合：功能最全、格式转换、复杂排版

---

## 🔧 命令速查

### Word

```bash
python scripts/wps_word.py create --title "report"
python scripts/wps_word.py edit --file "report.docx" --text "新增" --position end
python scripts/wps_word.py format --file "report.docx" --align center --size 12 --indent 2
python scripts/wps_word.py export --file "report.docx" --format pdf
python scripts/wps_word.py info --file "report.docx"
python scripts/wps_word.py engine-info
```

### Excel

```bash
python scripts/wps_excel.py create --name "Sales" --sheets "Q1,Q2,Q3"
python scripts/wps_excel.py input --file "Sales.xlsx" --sheet "Q1" --data '[["Product","Price"],["A",100]]'
python scripts/wps_excel.py formula --file "Sales.xlsx" --sheet "Q3" --cell "B3" --formula "=SUM(Q1!B:B)"
python scripts/wps_excel.py chart --file "Sales.xlsx" --sheet "Q1" --type bar --data "A1:B10"
python scripts/wps_excel.py sort --file "Sales.xlsx" --sheet "Q1" --sort-json '[{"column":"Price","ascending":false}]'
python scripts/wps_excel.py filter --file "Sales.xlsx" --sheet "Q1" --filter-json '[{"column":"Price","op":">","value":"50"}]'
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

### 🆕 目录生成

```bash
# 提取标题列表
python scripts/wps_toc.py extract --file "report.docx"

# 输出目录文件
python scripts/wps_toc.py generate --file "report.docx" --output "report_toc.txt"

# 在 Word 文档开头插入目录域（WPS 模式）
python scripts/wps_toc.py insert --file "report.docx"
```

### 🆕 环境自检

```bash
# 输出人类可读报告
python scripts/wps_test.py

# 输出 JSON 格式（可用于程序分析）
python scripts/wps_test.py --json
```

### 🆕 反馈入口

```bash
# 打开反馈页面（浏览器）
python scripts/wps_feedback.py page

# 打开邮件客户端，预先填好系统信息
python scripts/wps_feedback.py email
```

---

## 🚨 错误速查手册（遇到问题先看这里）

### E001: WPS 未安装或 COM 注册失败

**症状**: `RuntimeError: WPS 未安装或 COM 注册失败`

**原因**: 系统没装 WPS，或安装后没重启电脑

**解决**:
```bash
# 1. 安装 WPS Office 2019+ 或 WPS 365
# 2. 安装后必须重启电脑！
# 3. 重启后验证
python scripts/wps_test.py
```

### E002: python-docx 未安装

**症状**: `ModuleNotFoundError: No module named 'docx'`

**解决**:
```bash
pip install python-docx
pip install openpyxl      # Excel 也需要
pip install python-pptx   # PPT 也需要（纯Python模式）
```

### E003: 文件路径不存在

**症状**: `FileNotFoundError: 目录不存在：C:\Users\xxx\Desktop\中文`

**原因**: 中文路径 + 编码问题

**解决**:
```bash
# 方法1：把文件移到英文路径
D:\docs\report.docx

# 方法2：使用纯Python模式（自动处理编码）
python scripts/wps_word.py create --title "测试"

# 方法3：在命令行加引号
python scripts/wps_word.py edit --file "D:\中文路径\报告.docx" --text "xxx"
```

### E004: Word 转 PDF 失败

**症状**: `Word 不支持转 xxx，支持: ['pdf', 'txt', 'html']`

**原因**: 纯Python模式不支持格式转换

**解决**:
```bash
# 安装 WPS Office，自动切换为 WPS 模式
# 或只使用支持的操作（纯Python模式）
```

### E005: 筛选/排序报错 "需要 WPS 模式"

**症状**: `排序需要 WPS 模式，请安装 WPS Office`

**原因**: 排序和筛选只在 WPS 模式下可用

**解决**:
```bash
# 安装 WPS Office 2019+
# 安装后重启电脑
# 验证
python scripts/wps_test.py
```

### E006: WPS 卡住无响应

**症状**: 脚本运行中，WPS 一直没有反应

**原因**: WPS 偶尔会卡住（RPC 阻塞）

**解决**:
```bash
# 子进程超时保护会自动处理（等 60 秒后退出）
# 如果一直卡住，打开任务管理器 → 结束 WPS 进程 → 重新运行

# 如果反复出现，尝试：
# 1. 关闭 WPS 中不用的插件
# 2. 更新 WPS 到最新版
# 3. 安装 pywin32 后重新运行
pip install --upgrade pywin32
```

### E007: 权限不足

**症状**: `PermissionError: [Errno 13] Permission denied`

**解决**:
```bash
# Windows：右键命令提示符 → 以管理员身份运行
# macOS/Linux：命令前加 sudo
sudo python scripts/wps_word.py create --title "测试"
```

### E008: pywin32 导入失败

**症状**: `ImportError: DLL load failed`

**原因**: Python 和 pywin32 架构不匹配（32/64位）

**解决**:
```bash
# 卸载重装，确保版本匹配
pip uninstall pywin32
pip install pywin32
# 确保安装对应 Python 版本的 whl
```

### E009: Python 版本过低

**症状**: `SyntaxError` 或 `ModuleNotFoundError`

**解决**:
```bash
# 检查版本（需要 3.8+）
python --version

# 如果版本太低，安装新版本 Python
# 从 https://www.python.org/downloads/ 下载
# 或使用 conda/venv
```

### E010: 文档被占用

**症状**: `PermissionError` 或 `COMException: 文件被另一个程序占用`

**解决**:
```bash
# 1. 关闭正在使用该文件的程序（WPS/Word/Excel/PPT）
# 2. 查找锁定文件的进程
# Windows: 资源监视器 → CPU → 关联的句柄 → 搜索文件名
# 3. 重启电脑
# 4. 重新运行命令
```

### 📋 错误没有在上表里？

请使用反馈入口：

```bash
python scripts/wps_feedback.py email
```

这会自动打开邮件客户端，并在邮件正文中自动附加你的系统信息（Python版本、操作系统、引擎状态等），接反馈效率提升 10 倍。

---

## 🔮 用例库（20 个端到端场景）

### 场景 1：零基础上手

```
你：我用不会，帮我做个测试
AI：好的，先跑一下环境自检，看看...
    python scripts/wps_test.py
    ✅ WPS Office 已安装（11698）
    ✅ python-docx 已安装
    ✅ openpyxl 已安装
    ✅ 环境正常！
    现在我帮你创建一个测试文档：
    python scripts/wps_word.py create --title "测试文档"
    ✅ 已创建：C:\Users\用户\Desktop\测试文档.docx
```

### 场景 2：写一份报告

```
你：帮我写一份销售周报，标题"2026年6月第4周销售周报"
AI：好的...
    python scripts/wps_word.py create --title "2026年6月第4周销售周报"
    python scripts/wps_word.py edit --file "周报.docx" --text "一、本周销售概况..." --position end
    python scripts/wps_word.py edit --file "周报.docx" --text "二、重点客户..." --position end
    python scripts/wps_word.py edit --file "周报.docx" --text "三、下周计划..." --position end
    python scripts/wps_word.py format --file "周报.docx" --align center --size 14
    python scripts/wps_word.py export --file "周报.docx" --format pdf
    ✅ 完成！周报.docx 和 周报.pdf 已生成到桌面
```

### 场景 3：制作预算表

```
你：帮我做个家庭月度预算表，分收入/支出/汇总
AI：好的...
    python scripts/wps_excel.py create --name "家庭预算2026" --sheets "收入,支出,汇总"
    python scripts/wps_excel.py input --file "家庭预算2026.xlsx" --sheet "收入" \
      --data '[["来源","金额"],["工资",15000],["兼职",3000],["理财",500]]'
    python scripts/wps_excel.py input --file "家庭预算2026.xlsx" --sheet "支出" \
      --data '[["类目","金额"],["房租",4000],["餐饮",2000],["交通",500],["购物",1000]]'
    python scripts/wps_excel.py formula --file "家庭预算2026.xlsx" --sheet "汇总" \
      --cell "B2" --formula "=SUM(收入!B:B)"
    python scripts/wps_excel.py formula --file "家庭预算2026.xlsx" --sheet "汇总" \
      --cell "B3" --formula "=SUM(支出!B:B)"
    python scripts/wps_excel.py chart --file "家庭预算2026.xlsx" --sheet "支出" \
      --type pie --data "A1:B5"
    ✅ 完成！包含：收入/支出/汇总三个 Sheet + 饼图
```

### 场景 4：商务 PPT

```
你：帮我在5分钟内做个商务汇报PPT，大蓝色调
AI：好的...
    python scripts/wps_ppt.py create --title "2026年Q2汇报"
    python scripts/wps_ppt.py theme --file "2026年Q2汇报.pptx" --name business_blue
    python scripts/wps_ppt.py add-slide --file "2026年Q2汇报.pptx" --title "一、业绩概览"
    python scripts/wps_ppt.py insert --file "2026年Q2汇报.pptx" --slide 2 \
      --content "• 收入同比增长 35%\n• 客户数突破 1000\n• 满意度 92%"
    python scripts/wps_ppt.py add-slide --file "2026年Q2汇报.pptx" --title "二、下季度计划"
    python scripts/wps_ppt.py insert --file "2026年Q2汇报.pptx" --slide 3 \
      --content "• 开拓海外市场\n• 新增两条产品线\n• 优化客服体系"
    python scripts/wps_ppt.py export --file "2026年Q2汇报.pptx" --format pdf
    ✅ 完成！包含封面+2个内容页，大蓝色调，已生成PDF
```

### 场景 5：多条件数据分析

```
你：筛选"销售额大于5000"且"地区为华东"的记录
AI：好的...
    python scripts/wps_excel.py filter --file "sales.xlsx" --sheet "Q2" \
      --filter-json '[{"column":"销售额","op":">","value":"5000"},{"column":"地区","op":"=","value":"华东"}]'
    ✅ 筛出 12 条记录：
    A公司 ¥8,200 华东
    B公司 ¥6,100 华东
    ...
```

### 场景 6：多列排序

```
你：按销售额降序、利润升序排列
AI：好的...
    python scripts/wps_excel.py sort --file "sales.xlsx" --sheet "Q2" \
      --sort-json '[{"column":"销售额","ascending":false},{"column":"利润","ascending":true}]'
    ✅ 排序完成（87 行）
```

### 场景 7：自动目录

```
你：帮我给这份报告生成目录
AI：好的...
    python scripts/wps_toc.py insert --file "报告.docx"
    ✅ 目录已插入到文档开头！共识别 8 个标题
    提示：右键目录域可更新页码
```

### 场景 8：PNG 生成饼图

```
你：把各省销售额做成饼图
AI：好的...
    python scripts/wps_excel.py chart --file "各省销售.xlsx" --sheet "汇总" \
      --type pie --data "A1:B31"
    ✅ 饼图已生成！各省占比一目了然
```

### 场景 9：环境自检排查

```
你：帮我测一下这个能不能用
AI：好的，正在运行环境自检...
    python scripts/wps_test.py
    ==================================================
    WPS Office 全家桶 - 环境自检报告
    ==================================================
      Python 版本: ✅ Python 版本满足（3.13.12）
      操作系统: ✅ Windows 10
      路径安全: ✅ 桌面路径可访问
      写入权限: ✅ 桌面写入权限正常
      pywin32（COM）: ✅ pywin32 已安装
      python-docx: ✅ python-docx 已安装
      openpyxl: ✅ openpyxl 已安装
      python-pptx: ✅ python-pptx 已安装
      WPS Office: ✅ WPS Office 已安装（11.1.0.14309）
    --------------------------------------------------
    总结: ✅ 所有检查通过，可以正常使用
    ==================================================
```

### 场景 10：大文件操作

```
你：打开 50MB 的 report.docx，编辑第10页
AI：⚠️ 文件较大，WPS 操作可能较慢
    建议：
    1. 多条件查找替换：Ctrl+H 批量处理
    2. 特定页面定位：使用书签或分节符
    3. 如果是多次操作，先转为纯文本处理
    ⚠️ 是否需要继续？
```

### 场景 11：文件被占用

```
你：报错说文件被占用
AI：好的，检查一下...
    任务管理器 → CPU → 关联的句柄 → 搜索 "report.docx"
    发现 WINWORD.EXE 正在使用该文件
    解决：
    1. 按上面的方法结束 WINWORD 进程
    2. 或先关闭 Word/WPS 窗口
    3. 再重新运行命令
```

### 场景 12：字体效果差异

```
你：Python 创建的 WPS 打开效果有差异
AI：这是因为纯Python模式使用默认字体
    建议：
    1. 先用纯Python创建文件
    2. 再用 WPS 打开重新设置字体/格式
    3. 或者直接使用 WPS 模式创建
    python scripts/wps_word.py create --title "WPS模式文档"
```

### 场景 13：导出 PPT  PDF 打印

```
你：PPT 转 PDF 打印时字体变了
AI：这是常见现象，原因和解决方法：
    1. 字体未嵌入：WPS 导出时需勾选"嵌入字体"
    2. 替换字体：PDF 用系统默认字体替代
    3. 建议：转换后再手动打开 PDF 检查效果
    python scripts/wps_ppt.py export --file "Pitch.pptx" --format pdf
    ✅ 导出完成，请在 Adobe PDF 中打开查看打印效果
```

### 场景 14：透视表

```
你：生一份销售数据的透视表
AI：当前版本不直接支持透视表创建
    但可以通过以下方式：
    1. 先在 Excel 中手动创建一次透视表
    2. 或用 Python 数据汇总：
    import pandas as pd
    df = pd.read_excel("sales.xlsx")
    pivot = df.pivot_table(values="销售额", index="地区", columns="季度", aggfunc="sum")
    pivot.to_excel("pivot_result.xlsx")
    ✅ 数据透视结果已保存
```

### 场景 15：批量20个 Word 转 PDF

```
你：把 D:\Reports\ 下所有 Word 转成 PDF
AI：好的...
    python scripts/format_converter.py batch --input-dir "D:\Reports" --input-format docx --output-format pdf
    ✅ 转换完成：18/20 个文件成功，2 个失败（中文路径，建议重命名）
```

### 场景 16：即时反馈

```
你：你做的这个有很大问题！
AI：抱歉给您不好的体验。请告诉我具体什么问题：
    1. 功能报错 → 请运行 `python scripts/wps_test.py` 并放大报错信息
    2. 功能建议 → 欢迎提出，我会优先安排
    3. 卡住了/崩溃 → 请打开任务管理器查看是否有 WPS 进程未退出

    也可直接使用反馈入口：
    python scripts/wps_feedback.py email
    （会自动附带系统信息，高效排查）
```

### 场景 17：找不到文件

```
你：我桌面上的文件在哪？
AI：文件在：
    C:\Users\Administrator\Desktop\
    或
    C:\Users\你的用户名\Desktop\

    如果想确认，运行：
    python scripts/document_manager.py recent --limit 10
    ✅ 最近 10 个文档：
    1. 测试文档.docx (2026-06-28 14:25:33)
    2. 销售数据.xlsx (2026-06-28 14:15:12)
    ...
```

### 场景 18：安装字体

```
你：如何用特殊的字体？
AI：需要两层安装：
    系统级：字体文件右键 → 为所有用户安装
    WPS级：打开 WPS → 工具 → 字体 → 嵌入字体到文件
    Python级：WPS 模式下在 format 时指定字体名：
    python scripts/wps_word.py format --file "report.docx" --font "微软雅黑"
```

### 场景 19：PPT 内容过多

```
你：PPT 内容溢出/遮挡
AI：常见解决方法：
    1. 拆分幻灯片：一个主题拆成2页
    2. 缩小字体：在 format 中把 size 从 14 改为 12
    3. 调整文本框位置：手动拖动到合适位置
    4. 或让 AI 重新生成时控制内容密度
```

### 场景 20：跨平台兼容

```
我写一个文档在 Windows，到 macOS 打开有问题
AI：建议使用通用格式保存：
    1. 保存为兼容格式：.docx（不是 .doc）
    2. PDF 打印时嵌入字体
    3. 纯 Python 模式跨平台兼容最好
    python scripts/wps_word.py export --file "report.docx" --format pdf
    ✅ PDF 在任何设备打开都能保持一致
```

---

## 📊 版本兼容矩阵

| Python | WPS Office | Windows | macOS | Linux | 状态 |
|--------|-----------|---------|-------|-------|------|
| 3.8+ | 2019+ | ✅ | ⚠️ | ❌ | 推荐 |
| 3.8+ | 365 | ✅ | ✅ | ❌ | 最佳 |
| 3.8+ | - | ✅ | ✅ | ✅ | 纯Python |

> ⚠️ = 部分功能受限（纯Python模式），❌ = 未测试

---

## ⚠️ 安全须知

**✅ 三道防线保障安全**：
1. **路径安全**：`safe_path()` 全面校验，拒绝非法路径
2. **引擎隔离**：子进程模式隔离 WPS崩溃，主进程不受影响
3. **数据零上传**：所有处理本地完成，不上传任何内容到互联网

**⚠️ 注意事项**：
- 批量操作时，桌面会创建 `WPS_Backup` 文件夹保存副本
- 纯Python模式的格式支持有限
- macOS 上 WPS 支持不支持所有功能
- 所有文件操作在本地进行，不会联网

---

## 📝 版本记录

| 版本 | 日期 | 本次更新 |
|------|------|---------|
| **v2.1.0** | 2026-06-28 | 🆕 目录生成（TOC）；🆕 环境自检（test）；🆕 反馈入口；📚 错误速查手册（10个FAQ+编号）；🎬 用例库（20个端到端场景）；📊 版本兼容矩阵；📖 AI助手完全指南（对话示例+状态追踪） |
| v2.0.0 | 2026-06-28 | 🏗️ 三引擎自动切换；🤖 AI助手零学习成本；🛡️ 三道安全防线；📊 多列排序+多条件筛选 |
| v1.2.0 | 2026-06-28 | 子进程隔离架构 / 多列排序 / 多条件筛选 |
| v1.0.0 | 2026-06-28 | 初始版本，三大组件 + 格式转换 |
