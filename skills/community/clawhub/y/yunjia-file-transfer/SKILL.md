---
name: yunjia-file-transfer
description: 当用户请求文件时（如"把文件发给我"、"发个文件给我"、"把 xxx 发给我"），调用此 skill 将文件发送给用户。支持发送本地文件到当前聊天频道。
metadata: { "openclaw": { "emoji": "📦" } }
version: 1.1.0
last_updated: 2026-04-04
os_compatibility:
  - macOS
  - Linux (包括银河麒麟、统信UOS)
  - Windows
---

# 云加文件传输

## 🎯 **重点保证 Windows 系统支持**

**重要提示**：用户主要使用 Windows 系统，必须优先保证 Windows 上的正常使用！

### 🏆 **Windows 优先原则**
1. **Windows 是第一优先级** - 所有示例和说明都要考虑 Windows 兼容性
2. **用户使用 Windows** - 实际使用场景中 Windows 占比最高
3. **路径格式要正确** - Windows 使用反斜杠和驱动器字母

## 🌐 操作系统兼容性

✅ **完全支持**：
- **Windows** - **第一优先级**，用户主要使用 Windows
- **macOS** - 原生支持
- **Linux** - 包括银河麒麟、统信UOS等发行版

📝 **智能体注意事项**：
1. **Windows 优先**：首先考虑 Windows 兼容性，再考虑其他系统
2. **需要根据操作系统使用相应的文件查找命令**
3. **路径必须是操作系统对应的绝对路径格式**：
   - **Windows**: `C:\Users\用户名\文件.txt` 或 `C:/Users/用户名/文件.txt`
   - macOS: `/Users/用户名/文件.txt`
   - Linux: `/home/用户名/文件.txt`
4. **脚本会自动验证路径格式的合法性**
5. **重要**：不要硬编码 macOS 路径！智能体需要动态确定当前操作系统并生成正确的路径

## ⚠️ 重要警告

**调用技能后，你的回复必须是脚本的 stdout 输出，不要添加任何额外的文字、Markdown 代码块或说明！**

脚本已经输出了格式正确的 JSON，你只需要把这个 JSON **原封不动**地转发给用户。

## 🚫 常见错误

### 错误做法：包装脚本输出
AI 在调用技能后，错误地包装了脚本的输出：
```
根据技能要求，我需要直接输出这个 JSON，不在外面加任何文字：

```json
{"filePaths":["/home/lifang/Downloads/测试文件.txt"],"text":"给您发过去了，查收一下。需要我把文件内容识别出来给您看吗？","mode":"sendFileToChat"}
```

### 错误做法：添加额外文本
```
给您发过去了，查收一下
{"filePaths":["..."],"text":"给您发过去了，查收一下","mode":"sendFileToChat"}
```

### 正确做法
1. **智能体查找文件路径**（使用上面提到的方法）
2. **智能体确定要对用户说的话**（自然口语化）
3. 调用脚本：`python3 "${SKILL_DIR}/scripts/assemble_send_instruction.py" --file "/找到的/具体/文件路径" --text "你想说的话"`
4. 脚本输出（stdout）：
   ```
   {
     "filePaths": ["/找到的/具体/文件路径"],
     "text": "你想说的话",
     "mode": "sendFileToChat"
   }
   ```
5. **直接把这个 stdout 输出作为你的回复**，不要添加任何东西

#### 完整示例（跨平台）：

**macOS/Linux 示例**：
**用户说**："把 test.txt 发给我"

**智能体操作**：
1. 查找文件：`find ~/Downloads -name "*test.txt*" -type f 2>/dev/null`
2. **找到绝对路径**：`/home/lifang/Downloads/test.txt` ✅
   - ❌ 错误：`~/Downloads/test.txt`
   - ❌ 错误：`test.txt`
   - ❌ 错误：`Downloads/test.txt`
3. 确定回复文本："给您发过去了，查收一下。需要我把文件内容识别出来给您看吗？"
4. 调用脚本：`python3 "${SKILL_DIR}/scripts/assemble_send_instruction.py" --file "/home/lifang/Downloads/test.txt" --text "给您发过去了，查收一下。需要我把文件内容识别出来给您看吗？"`
5. 脚本输出：
   ```
   {
     "filePaths": ["/home/lifang/Downloads/test.txt"],
     "text": "给您发过去了，查收一下。需要我把文件内容识别出来给您看吗？",
     "mode": "sendFileToChat"
   }
   ```
6. **智能体回复**（原样输出上面的 JSON）

**Windows 示例**：
**用户说**："把 report.docx 发给我"

**智能体操作**：
1. 查找文件：`Get-ChildItem -Path "$env:USERPROFILE\Downloads" -Filter "*report.docx*" -File`
2. **找到绝对路径**：`C:\Users\lifang\Downloads\report.docx` ✅
   - ✅ 也支持：`C:/Users/lifang/Downloads/report.docx`
   - ❌ 错误：`report.docx`
   - ❌ 错误：`Downloads\report.docx`
3. 确定回复文本："文件已发送，请查收"
4. 调用脚本：`python3 "${SKILL_DIR}/scripts/assemble_send_instruction.py" --file "C:\Users\lifang\Downloads\report.docx" --text "文件已发送，请查收"`
5. 脚本输出：
   ```
   {
     "filePaths": ["C:\\Users\\lifang\\Downloads\\report.docx"],
     "text": "文件已发送，请查收",
     "mode": "sendFileToChat"
   }
   ```
6. **智能体回复**（原样输出上面的 JSON）

#### 为什么必须用绝对路径？
- 脚本可能在不同目录下运行
- `~` 是 shell 扩展，Python 脚本可能无法正确解析
- 绝对路径确保文件能被准确找到和发送

#### 跨平台路径格式：
- **macOS/Linux/银河麒麟/UOS**：`/home/用户名/Downloads/文件.txt`
- **Windows**：`C:\Users\用户名\Downloads\文件.txt` 或 `C:/Users/用户名/Downloads/文件.txt`

#### 操作系统兼容性：
✅ **支持的系统**：
- macOS
- Linux（包括银河麒麟、统信UOS等发行版）
- Windows

⚠️ **注意事项**：
1. 智能体需要根据操作系统调整文件查找命令
2. Windows 上可能需要使用 PowerShell 命令查找文件
3. 不同系统的用户目录结构不同：
   - macOS: `/Users/用户名/`
   - Linux: `/home/用户名/`
   - Windows: `C:\Users\用户名\`

## 🖥️ **Windows 专用指南**

### Windows 环境特点
1. **路径分隔符**：反斜杠 `\`（也支持正斜杠 `/`）
2. **驱动器字母**：`C:`, `D:`, `E:` 等
3. **用户目录**：`C:\Users\用户名\`
4. **常用目录**：
   - 下载：`C:\Users\用户名\Downloads`
   - 文档：`C:\Users\用户名\Documents`
   - 桌面：`C:\Users\用户名\Desktop`

### Windows 文件查找命令
**PowerShell（推荐）**：
```powershell
# 查找 Downloads 目录下的文件
Get-ChildItem -Path "$env:USERPROFILE\Downloads" -Filter "*文件名*" -File

# 查找所有目录（递归）
Get-ChildItem -Path "$env:USERPROFILE" -Filter "*文件名*" -File -Recurse | Select-Object -First 10 FullName

# 查找特定扩展名的文件
Get-ChildItem -Path "$env:USERPROFILE\Documents" -Filter "*.docx" -File
```

**CMD 命令提示符**：
```cmd
dir /s /b "C:\Users\%USERNAME%\Downloads\*文件名*"
dir /s /b "C:\Users\%USERNAME%\Desktop\*.pdf"
```

### Windows 路径示例
**✅ 正确的 Windows 路径**：
- `C:\Users\张三\Downloads\报告.docx`
- `D:\工作文件\项目计划.xlsx`
- `C:/Users/李四/Documents/合同.pdf`（正斜杠也支持）

**❌ 错误的 Windows 路径**：
- `报告.docx`（相对路径）
- `Downloads\报告.docx`（相对路径）
- `~\Downloads\报告.docx`（需要展开）

## 🧠 智能体最佳实践

### 如何确定操作系统
在执行文件查找前，智能体应该先确定当前操作系统：

```bash
# 检查操作系统类型
uname -s  # Linux → Linux, macOS → Darwin

# 或者检查环境变量
echo $OSTYPE
```

### Windows 优先的智能体逻辑
**智能体应该优先检测 Windows 环境**：

```bash
# 方法1：检查是否在 Windows 环境中
if [ -n "$WINDIR" ] || [ -n "$OS" ] || [ "$(uname -o 2>/dev/null)" = "Msys" ] || [ "$(uname -s)" = "CYGWIN"* ] || [ "$(uname -s)" = "MINGW"* ]; then
    echo "检测到 Windows 环境"
    # Windows 路径逻辑
    # 注意：在 WSL/Cygwin 中，Windows 路径在 /mnt/c/ 下
fi

# 方法2：检查常见 Windows 环境变量
if [ -n "$USERPROFILE" ]; then
    echo "Windows 用户目录: $USERPROFILE"
fi
```

### 动态生成用户目录路径（Windows 优先）
```bash
# 示例：智能体逻辑（Windows 优先）
USERNAME=$(whoami)

# 首先检查 Windows 环境
if [ -n "$USERPROFILE" ]; then
    # Windows 环境（PowerShell、CMD、WSL）
    USER_HOME="$USERPROFILE"
    DOWNLOADS_DIR="$USER_HOME/Downloads"
    # 注意：在 WSL 中可能需要转换为 /mnt/c/Users/...
elif [ "$(uname -s)" = "Darwin" ]; then
    # macOS
    USER_HOME="/Users/$USERNAME"
    DOWNLOADS_DIR="$USER_HOME/Downloads"
elif [ "$(uname -s)" = "Linux" ]; then
    # Linux (银河麒麟、统信UOS等)
    USER_HOME="/home/$USERNAME"
    DOWNLOADS_DIR="$USER_HOME/Downloads"
else
    # 其他系统
    USER_HOME="$HOME"
    DOWNLOADS_DIR="$USER_HOME/Downloads"
fi

echo "用户目录: $USER_HOME"
echo "下载目录: $DOWNLOADS_DIR"
```

### 👔 用户使用注意事项

**智能体服务用户时的特别注意事项**：

1. **称呼要恰当**：
   - 使用合适的称呼
   - 语气要友好但不随意
   - 回复要简洁明了，用户时间宝贵

2. **文件查找优先级**：
   - 首先检查用户常用目录：`Downloads`、`Documents`、`Desktop`
   - 考虑用户可能使用的命名习惯：中文名、带日期、带版本号
   - 优先查找最近修改的文件

3. **常见用户文件类型**：
   - 财务报表：`.xlsx`, `.xls`
   - 合同文档：`.docx`, `.pdf`
   - 项目计划：`.pptx`, `.pdf`
   - 会议纪要：`.docx`, `.md`

4. **错误处理要友好**：
   - 如果找不到文件，要提供清晰的下一步建议
   - 可以询问更具体的文件名或位置
   - 避免技术术语，用用户能理解的语言

### Windows 文件查找最佳实践
**智能体应该根据环境使用正确的命令**：

1. **纯 Windows（PowerShell/CMD）**：
   ```powershell
   # 查找文件并获取绝对路径
   $files = Get-ChildItem -Path "$env:USERPROFILE\Downloads" -Filter "*报告*" -File
   foreach ($file in $files) {
       Write-Output $file.FullName
   }
   ```

2. **WSL（Windows Subsystem for Linux）**：
   ```bash
   # WSL 中 Windows 路径在 /mnt/ 下
   find /mnt/c/Users/$USERNAME/Downloads -name "*报告*" -type f 2>/dev/null
   ```

3. **跨平台兼容查找**：
   ```bash
   # 智能体可以先尝试通用查找
   if command -v find &> /dev/null; then
       # Unix-like 系统
       find ~/Downloads -name "*文件*" -type f 2>/dev/null
   elif command -v Get-ChildItem &> /dev/null; then
       # PowerShell 环境
       Get-ChildItem -Path "$env:USERPROFILE\Downloads" -Filter "*文件*" -File
   else
       # 其他环境
       echo "无法确定合适的文件查找命令"
   fi
   ```

## 触发条件

用户说以下任何一条时激活：
- 把文件发给我
- 发个文件给我
- 给我发个文件
- 发送文件
- 上传文件
- 分享文件
- 把 xxx 发给我（xxx 是文件名）
- 传个文件
- 文件发一下

## 工作流程

### 1. AI 获取文件路径

AI 根据用户说的文件名，找到文件的完整路径。

**关键：智能体必须主动查找文件，不能等待用户提供完整路径！**

#### 查找方法（按操作系统）：

**🎯 Windows（用户主要使用）**：
1. **使用 PowerShell 搜索（推荐）**：
   ```powershell
   # 搜索 Downloads 目录
   Get-ChildItem -Path "$env:USERPROFILE\Downloads" -Filter "*文件名*" -File | Select-Object -First 5 FullName
   
   # 搜索 Documents 目录
   Get-ChildItem -Path "$env:USERPROFILE\Documents" -Filter "*文件名*" -File | Select-Object -First 5 FullName
   
   # 递归搜索整个用户目录
   Get-ChildItem -Path "$env:USERPROFILE" -Filter "*文件名*" -File -Recurse | Select-Object -First 10 FullName
   ```

2. **使用 CMD 命令提示符**：
   ```cmd
   dir /s /b "C:\Users\%USERNAME%\Downloads\*文件名*"
   dir /s /b "C:\Users\%USERNAME%\Documents\*文件名*"
   ```

3. **检查常见 Windows 目录**：
   - `C:\Users\用户名\Downloads\`
   - `C:\Users\用户名\Documents\`
   - `C:\Users\用户名\Desktop\`
   - `D:\工作文件\`（如果有 D 盘）
   - 当前工作目录

**macOS/Linux（银河麒麟、统信UOS等）**：
1. **使用 `find` 命令搜索**：
   ```bash
   find ~/Downloads -name "*文件名*" -type f 2>/dev/null | head -5
   find ~/Documents -name "*文件名*" -type f 2>/dev/null | head -5
   ```

2. **使用 `locate` 命令（如果可用）**：
   ```bash
   locate "文件名" | grep -E '\.(xlsx|xls|doc|docx|pdf|txt|jpg|png|zip)$' | head -5
   ```

3. **检查常见目录**：
   - `~/Downloads/`
   - `~/Documents/`
   - `~/Desktop/`
   - `~/`
   - 当前工作目录

**Windows**：
1. **使用 PowerShell 查找**：
   ```powershell
   Get-ChildItem -Path "$env:USERPROFILE\Downloads" -Filter "*文件名*" -File | Select-Object -First 5 FullName
   Get-ChildItem -Path "$env:USERPROFILE\Documents" -Filter "*文件名*" -File | Select-Object -First 5 FullName
   ```

2. **使用 cmd 命令**：
   ```cmd
   dir "%USERPROFILE%\Downloads\*文件名*" /b /s 2>nul | head -5
   dir "%USERPROFILE%\Documents\*文件名*" /b /s 2>nul | head -5
   ```

3. **检查常见目录**：
   - `%USERPROFILE%\Downloads\`
   - `%USERPROFILE%\Documents\`
   - `%USERPROFILE%\Desktop\`
   - 当前工作目录

4. **如果用户提到特定位置**：
   - "桌面上的文件" → `~/Desktop/文件名`
   - "下载的文件" → `~/Downloads/文件名`
   - "文档里的" → `~/Documents/文件名`

#### 文件路径示例：
- 用户说："把 test.txt 发给我"
- 智能体查找：`find ~/Downloads -name "*test.txt*" -type f`
- 找到路径：`/Users/lifang/Downloads/test.txt`

- 用户说："发个 Excel 文件"
- 智能体需要询问："您说的是哪个 Excel 文件？"

#### 重要规则：
- **必须找到具体文件路径**，不能只写"文件名"
- **必须使用绝对路径**，如 `/Users/lifang/Downloads/文件.xlsx`，不能使用相对路径或 `~/Downloads/文件.xlsx`
- 如果找不到，询问用户："没找到这个文件，您能告诉我文件的具体位置吗？"
- 路径必须是**绝对路径**，如 `/Users/lifang/Downloads/文件.xlsx`

### 2. AI 像正常人一样回复用户

智能体应像人与人聊天一样回复用户，**不要用机械、生硬的语气**。根据不同的场景选择合适的表达方式：

文件发送成功时（自然口语化）：
- "给您发过去了，查收一下"
- "ok，发给你了"
- "文件已经发到群里了"
- "搞定！文件已发"
- "好了，过去了"

如果文件较大：
- "这个文件有点大，稍微等等哈"
- "正在上传，稍等"

如果文件是文档类型（如 Excel、PDF、Word、txt 等），**必须**询问用户是否需要把内容识别出来展示，例如：
- "需要我把文件内容识别出来给您看吗？"
- "要不要我把里面的内容读出来？"
- "需要我提取文件内容吗？"

把你想对用户说的话通过 `--text` 参数传入。

### 3. AI 调用 skill

```bash
python3 "${SKILL_DIR}/scripts/assemble_send_instruction.py" --file "文件完整路径" --text "你想对用户说的话"
```

### 4. Skill 返回 JSON

skill 脚本会输出纯 JSON 到 stdout，例如：
```json
{
  "filePaths": ["/path/to/file.xlsx"],
  "text": "你想对用户说的话",
  "mode": "sendFileToChat"
}
```

### 5. **关键：直接输出脚本的 stdout 内容，不要做任何修改！**

你的回复**必须**是脚本输出的**原始内容**，不要添加任何额外的文字、Markdown 代码块或说明。

**重要**：脚本已经输出了格式正确的 JSON，你只需要把这个 JSON 原样转发给用户。

错误示例（不要这样做）：
```
根据技能要求，我需要直接输出这个 JSON，不在外面加任何文字：

```json
{"filePaths":["..."],"text":"给您发过去了，查收一下","mode":"sendFileToChat"}
```
```

错误示例（不要这样做）：
```
给您发过去了，查收一下
{"filePaths":["..."],"text":"给您发过去了，查收一下","mode":"sendFileToChat"}
```

正确示例（应该这样做）：
```
{"filePaths":["/path/to/file.xlsx"],"text":"给您发过去了，查收一下","mode":"sendFileToChat"}
```

**简单规则**：调用脚本后，把脚本的 stdout 输出**原封不动**地作为你的回复。

## 示例

**用户说**：把文件 定制app物料.xlsx 发给我

**AI 做的**：
1. 找到文件路径：`/Users/lifang/Downloads/定制app物料.xlsx`
2. 调用 skill：`python3 "${SKILL_DIR}/scripts/assemble_send_instruction.py" --file "/Users/lifang/Downloads/定制app物料.xlsx" --text "给您发过去了，查收一下"`
3. **脚本输出**（stdout）：
   ```
   {
     "filePaths": ["/Users/lifang/Downloads/定制app物料.xlsx"],
     "text": "给您发过去了，查收一下",
     "mode": "sendFileToChat"
   }
   ```
4. **AI 回复**：把脚本的 stdout 输出**原封不动**地作为回复

**最终回复应该是**（注意：这是脚本输出的原始内容，不是 AI 包装过的）：
```
{
  "filePaths": ["/Users/lifang/Downloads/定制app物料.xlsx"],
  "text": "给您发过去了，查收一下。需要我把文件内容识别出来给您看吗？",
  "mode": "sendFileToChat"
}
```

**重要提醒**：脚本输出的 JSON 可能有多行缩进，也可能没有缩进。无论哪种格式，都要**原样转发**，不要修改格式。

## 规则

1. 文件路径必须是绝对路径
2. 不要读取文件内容，只组装 JSON
3. 支持多个文件：多个 --file 参数
4. 输出 JSON 用于插件解析

## 🧪 测试验证

### 测试命令（跨平台示例）

**macOS**：
```bash
python3 ~/.openclaw/skills/yunjia-file-transfer/scripts/assemble_send_instruction.py --file "/Users/lifang/Downloads/测试文件.txt" --text "测试macOS调用方式"
```

**Linux（银河麒麟/UOS）**：
```bash
python3 ~/.openclaw/skills/yunjia-file-transfer/scripts/assemble_send_instruction.py --file "/home/lifang/Downloads/测试文件.txt" --text "测试Linux调用方式"
```

**Windows**：
```bash
python3 ~/.openclaw/skills/yunjia-file-transfer/scripts/assemble_send_instruction.py --file "C:\Users\lifang\Downloads\测试文件.txt" --text "测试Windows调用方式"
```

### 期望输出（Linux示例）
```
{
  "filePaths": [
    "/home/lifang/Downloads/测试文件.txt"
  ],
  "text": "测试Linux调用方式",
  "mode": "sendFileToChat"
}
```

### 🧪 Windows 路径验证测试结果
脚本已经过专门的 Windows 兼容性测试：

**✅ 支持的 Windows 路径格式**：
- 标准 Windows 路径: `C:\Users\用户\Downloads\2024年财报.xlsx`
- 中文路径: `D:\工作文件\项目计划\里程碑报告.docx`
- 带空格的路径: `C:\Users\用户\My Documents\年度总结报告 2024.docx`
- 正斜杠路径: `C:/Users/用户/Documents/合同范本.docx`
- 长路径: `C:\Users\...\document_v1.2.3_final_review.docx`
- 混合路径: `C:/Users/mixed\path/test.txt`

**❌ 不支持的路径格式**：
- 相对路径: `报告.docx`, `Downloads\报告.docx`
- 用户目录简写: `~\Downloads\报告.docx`（需要展开）
- **网络路径**: `\\server\share\部门文件\预算表.xlsx`（当前版本不支持）

**📊 用户使用场景测试通过**：
- 用户要查看财报 ✅
- 用户需要合同文件 ✅  
- 用户要项目计划 ✅

**📘 详细指南**：
更多用户使用场景和话术，请参考：[WINDOWS_GUIDE.md](./WINDOWS_GUIDE.md)

**重要**：这个输出应该原封不动地作为 AI 的回复，不要添加任何包装或额外文本。