# SafeShrink 密小件 / SafeShrink Document Optimizer

> **密小件** 帮您让文档变得更轻、更安全、更 AI 友好。
>
> 它一键完成三件事：
> - **压缩** 文档体积，去除冗余 — **减小 30%-85%**
> - **脱敏** 敏感信息（手机号、证件号、银行卡、金额）— 分享前保护隐私
> - **转换** 为 .ssd 格式 — **AI Token 减少约 70%**
>
> 所有处理 **完全离线** — 数据不会离开您的电脑。无需安装，下载 zip 包，解压后双击 EXE 运行。
>
> ---
>
> **SafeShrink** helps you make documents **lighter, safer, and more AI-friendly**.
>
> It does three things in one click:
> - **Compress** document size, removing redundancy — **30%-85% smaller**
> - **Sanitize** sensitive info (phone numbers, IDs, bank cards, amounts) — privacy protected before sharing
> - **Convert** to .ssd format — **~70% fewer AI tokens**
>
> All processing is **fully offline** — your data never leaves your computer. No installation needed, just download the zip, extract, and double-click the EXE.

---


**版本：v1.2.4** | [GitHub](https://github.com/JinwaTech/safeshrink) · [下载 zip](https://github.com/JinwaTech/safeshrink/releases/latest)

---

## ✨ 核心功能 / Core Features

| 功能 / Feature | 说明 / Description | 效果 / Effect |
|------|------|------|
| 🗜️ **文档减肥 / Document Slimming** | 压缩文档体积，去除冗余内容 / Compress document size, remove redundancy | 体积减少 / Size reduced **30%-70%** |
| 🔒 **智能脱敏 / Smart Sanitization** | 自动识别并脱敏敏感信息 / Auto-detect and mask sensitive info | 支持 26+ 种中英文敏感类型 / 26+ CN/EN sensitive types supported |
| 📝 **SSD 转换 / SSD Conversion** | Office/PDF → .ssd 格式 / Office/PDF → .ssd format | Token 消耗降低 / Token reduced **~70%** |
| 📦 **批量处理 / Batch Processing** | 文件夹一键批量处理 / One-click folder batch processing | 多线程并行，智能跳过 / Multi-threaded, smart skip |
| 🖼️ **OCR 识别 / OCR Recognition** | 扫描件 PDF / 图片自动 OCR / Auto OCR for scanned PDFs/images | 输出可搜索文本 / Searchable text output |

---

## 🖼️ 功能展示 / Features

### 主界面 / Main Interface

![主界面](https://raw.githubusercontent.com/JinwaTech/safeshrink/main/docs/screenshot/01-main-interface.png)

### 单文件减肥 / Single-File Slimming

![单文件减肥](https://raw.githubusercontent.com/JinwaTech/safeshrink/main/docs/screenshot/02-single-file-slim-standard.png)

### 批量处理报告 / Batch Processing Report

![批量处理](https://raw.githubusercontent.com/JinwaTech/safeshrink/main/docs/screenshot/03-batch-slim-report.png)

### 脱敏前后对比 / Sanitization Compare

![脱敏对比](https://raw.githubusercontent.com/JinwaTech/safeshrink/main/docs/screenshot/04-sanitize-compare.png)

### PDF 转 SSD / PDF to SSD

![PDF转SSD](https://raw.githubusercontent.com/JinwaTech/safeshrink/main/docs/screenshot/05-pdf-to-ssd.png)

### 结果对比对话框 / Result Compare Dialog

![结果对比](https://raw.githubusercontent.com/JinwaTech/safeshrink/main/docs/screenshot/06-result-compare-dialog.png)

### 设置面板 / Settings Panel

![设置面板](https://raw.githubusercontent.com/JinwaTech/safeshrink/main/docs/screenshot/07-settings-panel.png)

### CLI 命令行 / Command Line Interface

![CLI](https://raw.githubusercontent.com/JinwaTech/safeshrink/main/docs/screenshot/08-cli-version.png)

---

## 💰 使用效果 / Usage Results

### 📉 Token 节省对比 / Token Savings

> 基于方案F实测（原文字符×3 vs SSD Markdown token 估算），真实测试数据
> Based on Scheme F actual testing (original chars ×3 vs SSD Markdown token estimate)

| 文档类型 / Document Type | 原始 Token / Original | 转换后 Token / After SSD | 节省 / Saved |
|----------|-----------|-------------|------|
| DOCX → SSD（实测）/ DOCX → SSD (tested) | 5,520 | 1,784 | **67%** |
| 合同.docx (5页) / Contract.docx (5 pages) | ~4,000 | ~1,200 | **~70%** |
| 报告.pptx (20页) / Report.pptx (20 pages) | ~10,000 | ~3,000 | **~70%** |
| 手册.pdf (50页) / Manual.pdf (50 pages) | ~18,000 | ~5,400 | **~70%** |
| 含图片文档 / Image-heavy docs | ~15,000 | ~4,500 | **~70%** |
| 激进压缩 / Aggressive | ~5,520 | ~800 | **~85%** |

**节省原理 / Why so high:**
- Office 文件内部 XML 标签占大量 token（字体、样式、段落属性等），SSD 直接输出 Markdown 结构，XML 开销全部消除 / Office files have heavy XML overhead (fonts, styles, paragraph props); SSD outputs clean Markdown, eliminating all XML bloat
- 隐藏内容（批注、修订、宏）全部清除，不占 token / Hidden content (comments, revisions, macros) removed, zero token cost
- 图片 Base64 可替换为文字描述，大幅降低 token / Images can be replaced with text descriptions, drastically reducing token usage

*按 GPT-4o 价格 ¥0.10/1K tokens 计算 / Calculated at GPT-4o price ¥0.10/1K tokens*

### 📄 转换效果示例 / Conversion Examples

**SSD 转换效果 / SSD Conversion:**
```
📄 合同.docx  →  📄 合同.ssd
- 文字：完整保留 / Text: fully preserved
- 表格：转为 .ssd 表格格式 / Tables: converted to .ssd table format
- 图片：自动 Base64 内嵌（可选压缩）/ Images: auto Base64 embedded (optional compression)
- 格式：去除冗余样式，LLM 更易读 / Formatting: redundant styles removed, LLM-friendly
```

**智能脱敏效果 / Smart Sanitization:**
```
原文 / Original:
联系人：张三，电话：13812345678，报价：500万元
Contact: Zhang San, Phone: 13812345678, Quote: 5 million CNY

脱敏后 / Sanitized:
联系人：张*，电话：138****5678，报价：***
Contact: Z*, Phone: 138****5678, Quote: ***
```

| 类型 / Type | 示例 / Example | 脱敏结果 / Result |
|------|------|----------|
| 手机号 / Phone | `13812345678` | `138****5678` |
| 邮箱 / Email | `test@example.com` | `te***@example.com` |
| 身份证 / ID Card | `110101199001011234` | `110***********1234` |
| 银行卡 / Bank Card | `6222021234567890123` | `622202******0123` |
| IP地址 / IP Address | `192.168.1.1` | `***.***.***.***` |
| 金额 / Amount | `500万元` / `5 million CNY`、`87.81亿元` / `8.78 billion CNY` | `***` |
| 自定义 / Custom | 任意关键词 / Any keyword | 手动配置 / Manual config |

---

## 📖 使用场景 / Use Cases

### 💼 企业合规 / Enterprise Compliance
批量处理合同，脱敏敏感信息后再分享给外部团队
Batch process contracts, sanitize sensitive info before sharing externally

```
📂 /客户资料/
   ├─ 合同A.docx     →  合同A_脱敏.ssd
   ├─ 合同B.pdf      →  合同B_脱敏.ssd
   └─ 报价单.xlsx    →  报价单_脱敏.ssd
```

### 📚 知识库建设 / Knowledge Base
将 Office 文档转为 .ssd 格式，降低 AI 知识库成本
Convert Office docs to .ssd format, reducing AI knowledge base costs

```
📂 /产品文档/
   ├─ 演示文稿.pptx   →  演示文稿.ssd（嵌入图片）
   └─ 技术文档.docx   →  技术文档.ssd（嵌入图片）
```

### 🖼️ 扫描件 OCR / Scanned PDF OCR
对扫描件 PDF 进行 OCR，输出可搜索文本
OCR scanned PDFs, output searchable text

```
📄 扫描合同.pdf  →  📄 扫描合同.ssd（文字可搜索）
```

---

## 🚀 快速开始 / Quick Start

### 方式一：下载 zip 包（推荐）/ Option 1: Download zip (Recommended)

前往 [GitHub Releases](https://github.com/JinwaTech/safeshrink/releases/latest) 下载 `SafeShrink-v1.2.4.zip`，解压后双击 `SafeShrink.exe` 运行，无需安装。

> ⚠️ **系统要求 / System Requirements**：Windows 8 或更高版本 / Windows 8 or later。不支持 Windows 7（缺少必要的系统 API）。
> ⚠️ **System Requirements**: Windows 8 or later. Windows 7 is not supported (missing required system APIs).

### 方式二：SkillHub 安装 / Option 2: Install via SkillHub

```bash
# 安装 SafeShrink Skill / Install SafeShrink Skill
skillhub install safeshrink
```

### 方式三：源码运行 / Option 3: Run from Source

```bash
# 克隆仓库 / Clone repo
git clone https://github.com/JinwaTech/safeshrink.git
cd safeshrink
# 安装依赖 / Install deps
pip install -r requirements.txt
# 启动 GUI / Launch GUI
python start_gui.py
```

---

## 📋 更新日志 / Changelog

### v1.2.4（2026-06-05）

**New Features：**
- **26 种英文脱敏规则 / 26 English Sanitization Patterns**：对标 Microsoft Presidio（MIT License），新增 US Phone、SSN、Tax ID、Passport、MAC Address、Employee ID 等 26 种英文敏感信息识别，覆盖个人身份、金融、网络、证件四大类 / Aligned with Microsoft Presidio (MIT License); added 26 English patterns covering Personal Identity, Financial, Network, and Document categories
- **GUI 英文选项 / GUI English Options**：设置页和批量页新增 26 个英文脱敏 checkbox，中/英文模式自动切换显示 / Settings and Batch tabs add 26 English checkboxes, auto-toggled by language mode

**Bug Fixes：**
- **设置页标签不翻译 / Settings Labels Not Translating**：从英文切回中文时，13 个标签仍显示英文。根因：_label_map 反向映射键不匹配，改为 _orig_zh + get_translation 动态映射 / Labels stayed English when switching back to Chinese; fixed with dynamic bidirectional mapping
- **导航栏不切换 / Navbar Not Switching**：pply_language 的 else 分支读实例属性而非类属性。修复：items = MainWindow.NAV_ITEMS / Navbar read instance attribute instead of class attribute
- **"减肠"错别字 / "减肠" Typo**：history_tab 筛选下拉框和 translations.py 中 "减肥" 误写为 "减肠" / Filter dropdown and translations.py had typo "减肠" instead of "减肥"
- **CJK 字体渲染 / CJK Font Rendering**：CSS font-family Segoe UI 优先导致中文字符错误渲染，改为 Microsoft YaHei 优先 / CSS font-family order caused incorrect CJK rendering

**Build Optimization：**
- **spec 恢复 collect_submodules**：EXE 从 30MB 降至 18.4MB，dist 从 252MB 降至 182MB / Restored collect_submodules in spec, EXE 30MB→18.4MB
- **.pyd 全部重编译**：8 个模块用最新代码重编译 / Recompiled all 8 .pyd modules
- **format_to_ssd.py 编码修复**：UTF-16 LE → UTF-8 / Converted from UTF-16 LE to UTF-8
- **Python 版本迁移**：构建环境从 3.14 迁回 3.13.13 / Migrated build from Python 3.14 back to 3.13.13
### v1.2.3（2026-06-02）

#### 新增 / New Features

- **GUI 全面英文支持 / Full GUI English Support**：全部界面元素支持中英双语切换，启动时自动检测系统语言 / All UI elements support Chinese/English switching, auto-detect system language on startup

#### 修复 / Bug Fixes

- **QSpinBox 高度压缩 / QSpinBox Height Compression**：QSpinBox 最小高度未设置，布局系统将其高度压缩 30% 导致数值显示截断 / QSpinBox minimum height unset, layout system compressed height by 30% causing value display truncation
- **关闭对话框硬编码中文 / Close Dialog Hardcoded Chinese**：退出确认对话框 3 处硬编码中文，已用 `_()` 包裹支持英文 / 3 exit confirmation dialog strings hardcoded in Chinese, wrapped with `_()` for English support
- **Settings Tab hasattr 双前缀 / Settings Tab hasattr Double Prefix**：`hasattr(self, 'self.xxx')` 导致属性检查永远返回 False / `hasattr(self, 'self.xxx')` caused attribute check to always return False
- **i18n 启动不生效 / i18n Not Working on Startup**：启动时未调用语言切换，导致界面始终显示中文 / Language switch not called on startup, UI always showed Chinese

#### 改进 / Improvements

- **版本号统一 / Version Unified**：CLI `--version`、GUI 状态栏、文件标记三处版本号统一为 v1.2.3 / Version number unified across CLI, GUI footer, and file status marker

---

### v1.2.2（2026-05-28）

#### 新增 / New Features

- **结构化安全脱敏 / Structured Sanitization**：JSON/XML/YAML/CSV/HTML 等结构化文件支持安全脱敏，递归遍历只替换 string value，不破坏 key 和数据结构 / Structured files (JSON/XML/YAML/CSV/HTML) support safe sanitization — recursive traversal replaces only string values, preserving keys and structure
- **XLS 旧格式支持 / XLS Legacy Support**：通过 xlrd 支持 .xls（OLE2 格式）的预览、压缩跳过和脱敏处理 / .xls (OLE2) format supported via xlrd for preview, compression skip, and sanitization
- **CLI 英文输出 / CLI English Output**：CLI 根据系统 locale 自动切换中英文输出 / CLI auto-switches output language based on system locale
- **英文脱敏规则 / English Sanitization Rules**：新增 US Phone、UK Phone、SSN、Credit Card 等英文敏感信息识别 / Added US Phone, UK Phone, SSN, Credit Card detection patterns
- **XLS 写入支持 / XLS Write Support**：通过 xlwt 支持 .xls（OLE2 格式）文件写入和保存 / .xls (OLE2) write and save support via xlwt

#### 修复 / Bug Fixes

- **XLS 预览乱码 / XLS Preview Garbled**：OLE2 二进制文件被当 UTF-8 读取导致显示乱码，现用 xlrd 正确读取 / OLE2 binary files were read as UTF-8 causing garbled display; now correctly read with xlrd
- **XLS 压缩损坏 / XLS Compression Corruption**：标准/激进压缩对结构化数据执行文本压缩导致损坏，结构化格式统一跳过压缩 / Standard/aggressive compression on structured data caused corruption; structured formats now skip compression
- **XLS SSD 转换丢失内容 / XLS SSD Conversion Data Loss**：数字值被错误当作 shared string 索引查表，修复为正确区分属性值和字符串值 / Numeric values were incorrectly treated as shared string indices; now properly distinguished
- **批量脱敏 CSV/XLSX 无效 / Batch Sanitize CSV/XLSX Ineffective**：CSV 未加入原生脱敏列表，dummy SanitizeTab 实例缺少属性导致 fallback / CSV missing from native sanitize list; dummy SanitizeTab instance missing attributes
- **批量脱敏跳过逻辑 / Batch Sanitize Skip Logic**：`_减肥` 文件被同等跳过，无法二次脱敏；修复后 `_减肥` 可再脱敏，`_脱敏` 可再减肥 / `_减肥` files were skipped during sanitization; now `_减肥` can be re-sanitized, `_脱敏` can be re-slimmed
- **GUI 单文件 CSV/JSON 压缩 / GUI Single-File CSV/JSON Compression**：slim_tab 独立流程未跳过结构化格式，导致 CSV/JSON 被错误压缩 / slim_tab's independent flow didn't skip structured formats
- **Qt platform plugin 初始化失败 / Qt Platform Plugin Init Failure**：添加 qt.conf 解决 VCRUNTIME140.dll 多版本冲突 / Added qt.conf resolving VCRUNTIME140.dll version conflicts

#### 改进 / Improvements

- **PyInstaller 打包优化 / PyInstaller Packaging Optimization**：18 个模块编译为 .pyd，1079 文件/168MB（旧版 1552 文件/186MB）/ 18 modules compiled to .pyd, 1079 files/168MB (was 1552/186MB)

---

### v1.2.1（2026-05-24）

- **源码保护 / Source Code Protection**: 11 个核心模块编译为 Cython .pyd（safe_shrink、batch_processor、slim_tab 等） / 11 core modules compiled to Cython .pyd
- **源码保护 / Source Code Protection**: GitHub 历史版本（v1.0.0~v1.2.0）已删除，仅保留 v1.2.1 Release / GitHub history versions (v1.0.0~v1.2.0) removed, only v1.2.1 Release retained
- **修复 / Fix**: 单文档脱敏 `[Errno 22] Invalid argument` — `load_file_content()` 未设置 `self._current_file_path` / Single-document sanitization error
- **修复 / Fix**: Cython 循环依赖 — `safe_shrink.py` 自引用导入导致编译失败 / Cython circular import
- **新增 / New**: CLI 命令体系（slim/batch-slim/convert/compress-image/batch-convert/batch-compress-image）/ CLI command system
- **新增 / New**: `result_compare_dialog.py` 结果对比对话框 / Result comparison dialog
- **构建 / Build**: EXE 20.67MB，Python 3.13 + PySide6 + Cython .pyd

### v1.2.0（2026-05-23）

- **修复 / Fix**: 批量减肥 `_减肥` 后缀缺失 / Batch slimming `_减肥` suffix missing
- **修复 / Fix**: PPTX/XLSX 标准压缩报错 / PPTX/XLSX standard compression error
- **修复 / Fix**: 模式切换状态残留 / Mode switch state leakage
- **修复 / Fix**: SSD 命名泄漏 / SSD naming leakage
- **修复 / Fix**: sanitize 逐项目验证 / Sanitize item-by-item verification
- **修复 / Fix**: markitdown EXE 打包 / markitdown EXE packaging

### v1.1.8（2026-05-12）

- **修复 / Fix**: 批量处理双弹窗 / Batch processing double popup
- **修复 / Fix**: 批量处理卡死 / Batch processing freeze
- **修复 / Fix**: 进程残留 / Process residue
- **UI 修复 / UI Fix**: "扫描为Markdown" → "扫描为SSD"（5处）/ "Scan to Markdown" → "Scan to SSD"

### v1.1.7（2026-05-10）

- **新增 / New**: 单文件 PDF OCR / Single-file PDF OCR
- **新增 / New**: 批量 PDF OCR / Batch PDF OCR
- **新增 / New**: `is_scanned_pdf()` 智能检测扫描件 / Scanned PDF detection

### v1.1.6（2026-05-09）

- **修复 / Fix**: 尺寸限制区域布局 / Size limit area layout
- **新增 / New**: QSpinBox:disabled 样式 / QSpinBox:disabled style

### v1.1.5（2026-05-09）

- **修复 / Fix**: 选"扫描为SSD"后跳回"文件减肥"页面 / Jump back to slimming page after selecting SSD
- **新增 / New**: build.py 自动同步 EXE 到桌面 / build.py auto-sync EXE to desktop

### v1.1.4（2026-05-09）

- **新增 / New**: 图片模式 OCR — Tesseract v5.4.0 集成 / Image mode OCR with Tesseract v5.4.0
- **新增 / New**: `img_format_combo` 两选项 / Two image format options
- **修复 / Fix**: 隐藏 Tesseract 黑窗口 / Hide Tesseract console window

### v1.1.3（2026-05-08）

- **新增 / New**: 批量处理 Tab — 多线程并行 / Batch processing Tab
- **修复 / Fix**: SSD 转换默认 `embed_images=False` / SSD default `embed_images=False`


## ⚠️ 重要提示 / Important Notices

### 前置依赖 / Prerequisites

> 运行 SafeShrink 前，请确保已安装 **Visual C++ Redistributable**。如果启动时提示"找不到 VCRUNTIME140_1.dll"或"MSVCP140.dll 丢失"，请下载并安装：
>
> - 🔗 [VC++ Redistributable (x64)](https://aka.ms/vs/17/release/vc_redist.x64.exe)
> - 🔗 [VC++ Redistributable (x86)](https://aka.ms/vs/17/release/vc_redist.x86.exe)
>
> ⚠️ **重要 / Important：** SafeShrink 的 `_internal` 文件夹已包含所有第三方依赖，但仍需要您电脑安装 VC++ 运行时。这是因为 DLL 文件本身依赖微软的系统库，这部分无法打包进 EXE。
>
> ---
>
> Before running SafeShrink, please ensure **Visual C++ Redistributable** is installed. If you see an error like "VCRUNTIME140_1.dll not found" or "MSVCP140.dll missing", please download and install:
>
> - 🔗 [VC++ Redistributable (x64)](https://aka.ms/vs/17/release/vc_redist.x64.exe)
> - 🔗 [VC++ Redistributable (x86)](https://aka.ms/vs/17/release/vc_redist.x86.exe)
>
> ⚠️ **Important:** SafeShrink's `_internal` folder contains all third-party dependencies, but your system still needs the VC++ runtime. DLL files depend on Microsoft's system libraries, which cannot be packaged into the EXE.

### 杀毒软件提示 / Antivirus Notice

> ⚠️ **如果 SafeShrink 被杀毒软件拦截，这是误报。**
>
> SafeShrink 是**纯本地**的文件预处理工具，**不联网、不连接任何服务端、不上传任何数据**，不存在数据泄露风险。它**不会修改系统文件、不会安装驱动、不会驻留后台**，不会对电脑造成任何损害。
>
> 被拦截的原因是：SafeShrink 使用 PyInstaller 打包成独立 EXE，这类"单文件可执行程序"在杀毒软件中属于低信誉类别，容易被误判。
>
> **⚠️ 特别提醒 / Special Notice：** 杀毒软件可能会逐个扫描 `_internal` 文件夹中的数百个 DLL 文件，**隔离其中任何一个关键 DLL 都会导致 EXE 启动失败或功能异常**。
>
> **解决方法 / Solution：** 将 SafeShrink 整个文件夹（包括 `_internal`）加入杀毒软件白名单/排除项。如有疑虑，可用 [VirusTotal](https://www.virustotal.com) 上传检测验证。
>
> ---
>
> ⚠️ **If SafeShrink is blocked by your antivirus, it is a false positive.**
>
> SafeShrink is a **fully offline** file preprocessing tool — **no internet, no server connection, no data upload**. Zero risk of data leakage. It **does not modify system files, install drivers, or run in the background**.
>
> **Special Notice:** Antivirus software may scan hundreds of DLL files in the `_internal` folder one by one. **Isolating any critical DLL will cause the EXE to fail to start or malfunction.**
>
> **Solution:** Add the entire SafeShrink folder (including `_internal`) to your antivirus whitelist/exclusions. For verification, upload to [VirusTotal](https://www.virustotal.com).

### 常见问题 / FAQ

| 问题 / Problem | 原因 / Cause | 解决方法 / Solution |
|------|------|------|
| **双击 EXE 没反应 / EXE does nothing** | 杀毒软件静默隔离了 `_internal` 中的某个 DLL / Antivirus silently isolated a DLL in `_internal` | 检查杀毒软件隔离区，恢复所有 SafeShrink 相关文件，并将整个文件夹加入白名单 / Check quarantine, restore all SafeShrink files, add folder to whitelist |
| **提示"找不到 xxx.dll" / "xxx.dll not found"** | VC++ 运行时未安装 / VC++ runtime not installed | 安装 [VC++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe) / Install VC++ Redistributable |
| **提示"api-ms-win-core-*.dll 丢失" / "api-ms-win-core-*.dll missing"** | Windows 版本过低 / Windows version too old | SafeShrink 需要 Windows 8 或更高版本 / Requires Windows 8 or later |
| **"转换结果为空" / "Conversion result is empty"** | `_internal` 中的某个依赖 DLL 被杀毒软件隔离 / A dependency DLL in `_internal` was isolated | 检查杀毒软件隔离区，恢复文件并加入白名单 / Check quarantine, restore files and add to whitelist |
| **批量处理中途崩溃 / Batch processing crashes** | 杀毒软件在处理过程中隔离了关键 DLL / Antivirus isolated a critical DLL during processing | 将 SafeShrink 文件夹加入白名单后重试 / Add folder to whitelist and retry |

---

## 📋 支持格式 / Supported Formats

| 类型 / Type | 格式 / Formats | 减肥 / Slim | 脱敏 / Sanitize | SSD |
|------|------|:----:|:----:|:--------:|
| **Office** | .docx, .xlsx, .xls, .pptx | ✅ | ✅ | ✅ |
| **PDF** | .pdf | ✅ | ✅ | ✅ |
| **网页 / Web** | .html, .htm | ✅ | ✅ | ✅ |
| **文本 / Text** | .txt, .ssd, .json, .csv | ✅ | ✅ | — |
| **结构化 / Structured** | .json, .xml, .yaml, .csv, .html | — | ✅ | — |
| **图片 / Image** | .jpg, .png, .gif, .webp | ✅ | — | — |
| **代码 / Code** | .js, .py, .ts, .css, .sql | ✅ | ✅ | ✅ |

---

## 🛡️ 产品准则 / Product Principles

| 准则 / Principle | 说明 / Description |
|------|------|
| 🔒 **完全离线 / Fully Offline** | 无需联网，数据不出本地 / No internet needed, data stays local |
| 🚫 **零删除 / Zero Deletion** | 保留原文件，输出到新文件夹 / Keep originals, output to new folder |
| 📁 **可回溯 / Traceable** | 处理报告记录所有操作 / Processing report records all operations |
| ⚡ **高效并行 / Efficient Parallel** | 多线程批量处理 / Multi-threaded batch processing |

---

## 📊 性能指标 / Performance Metrics

| 指标 / Metric | 数值 / Value |
|------|------|
| 处理速度 / Processing Speed | ~50 页/秒（文档减肥）/ ~50 pages/sec (slimming) |
| 批量并行 / Batch Parallel | 多线程默认，智能调度 / Multi-threaded by default, smart scheduling |
| 内存占用 / Memory Usage | < 200MB（常规文档）/ < 200MB (typical docs) |
| 支持单文件 / Max Single File | 最大 500MB / Up to 500MB |
| OCR 支持 / OCR Support | 扫描件 PDF + 图片 / Scanned PDFs + images |

---

## 📁 文件说明 / File Index

| 文件 / File | 说明 / Description |
|------|------|
| `README.md` | 用户指南 / User Guide |
| `SKILL.md` | Skill 插件文档 / Skill Plugin Documentation |
| `main_window_v2.py` | 主窗口 UI 源码 / Main Window UI Source |
| `settings_tab.py` | 设置面板源码 / Settings Panel Source |
| `history_manager.py` | 历史记录管理器 / History Manager |
| `history_tab.py` | 历史记录面板 / History Panel |
| `theme_manager.py` | 主题管理器 / Theme Manager |
| `translations.py` | 多语言翻译 / Translations |
| `result_compare_dialog.py` | 结果对比对话框 / Result Compare Dialog |
| `assets/` | 图标与资源文件 / Icons & Resources |
| `requirements.txt` | Python 依赖列表 / Python Dependencies |
| `.gitignore` | Git 忽略规则 / Git Ignore Rules |
| `LICENSES_THIRD_PARTY.txt` | 第三方许可证 / Third-Party Licenses |

---

## 🤝 贡献与支持 / Contributing

- 🐛 [提交 Issue](https://github.com/JinwaTech/safeshrink/issues) / [Submit Issue](https://github.com/JinwaTech/safeshrink/issues)
- 💡 [功能建议](https://github.com/JinwaTech/safeshrink/discussions) / [Feature Request](https://github.com/JinwaTech/safeshrink/discussions)
- ⭐ [Star 支持](https://github.com/JinwaTech/safeshrink) / [Star on GitHub](https://github.com/JinwaTech/safeshrink)

---

## 📄 License / 许可证

**专有软件许可证（Proprietary License）**
**Proprietary License — All Rights Reserved**

© 2026 杭州金蛙信息科技有限公司 版权所有
© 2026 JinwaTech Co., Ltd. All Rights Reserved.

- 本软件为专有软件，受知识产权保护 / Proprietary software, protected by intellectual property rights
- 禁止逆向工程、反编译或修改本软件 / Reverse engineering, decompiling, or modifying prohibited
- 禁止分发、转让或出租本软件 / Distribution, transfer, or rental prohibited
- 详细信息请参阅 LICENSES_THIRD_PARTY.txt / See LICENSES_THIRD_PARTY.txt for details

---

<div align="center">

**SafeShrink 密小件 — 让文档更轻、更安全、更 AI 友好**
**SafeShrink — Lighter Docs, Safer Data, More AI-Friendly**

[GitHub](https://github.com/JinwaTech/safeshrink) · [下载 zip](https://github.com/JinwaTech/safeshrink/releases/latest) · [问题反馈](https://github.com/JinwaTech/safeshrink/issues)

</div>

---

## 反馈与联系我们 / Feedback & Contact

- 📧 邮箱 / Email: lssclty@jinwakeji.cn（全球用户 / Global）
- 📞 电话 / Phone: +86-186-6700-8029（国内用户 / China）
- 💼 企业微信 / WeChat Work: [扫码添加 / Scan QR code](https://github.com/JinwaTech/safeshrink/releases/download/v1.2.4/qr_wechat_work.png)
- 🚀 飞书 / Lark: [扫码添加 / Scan QR code](https://github.com/JinwaTech/safeshrink/releases/download/v1.2.4/qr_lark.png)



