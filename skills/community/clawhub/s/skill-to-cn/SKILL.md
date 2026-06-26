---
name: skill-to-cn
description: 将任意技能汉化为中文版本。当用户要求"汉化技能"、"翻译技能"、"把XX技能翻译成中文"、"创建技能的中文版"时触发。输入原始技能路径（如 ~/.claude/skills/X/），输出汉化后的技能目录（~/.claude/skills/X-cn/）。
---

# 技能汉化器

将任意 Claude Code 技能翻译为中文版本。

## 核心职责

**重要**：本技能的完整工作流程包含两个阶段：
1. **脚本阶段**：运行翻译脚本，生成标记 `[待翻译]` 的骨架文件
2. **模型阶段**：Claude 必须读取骨架文件，完成所有 `[待翻译]` 内容的实际翻译

最终输出的必须是**已完成翻译的中文技能**，而非标记状态的中间产物。

## 工作流程

汉化技能涉及以下步骤：

1. 确认源技能路径（默认 ~/.claude/skills/<技能名>/）
2. 读取并分析源技能结构
3. 运行翻译脚本，生成目标目录骨架
4. **Claude 读取并翻译所有标记内容**
5. 输出完整翻译后的技能文件
6. 验证汉化结果

## 执行汉化

### 第一步：运行脚本生成骨架

运行汉化脚本生成带标记的骨架文件：

```bash
python3 ~/.claude/skills/skill-to-cn/scripts/translate_skill.py <源技能名>
```

示例：
```bash
# 汉化 pdf-editor 技能
python3 ~/.claude/skills/skill-to-cn/scripts/translate_skill.py pdf-editor

# 指定完整路径
python3 ~/.claude/skills/skill-to-cn/scripts/translate_skill.py /path/to/skill --output /custom/output
```

脚本会创建目标目录并标记所有需要翻译的内容。

### 第二步：Claude 完成翻译

**这是关键步骤，必须由 Claude 执行：**

1. 读取生成的目标目录中的所有文件
2. 找到所有 `[待翻译]` 标记的内容
3. 将标记内容翻译为中文，并**移除 `[待翻译]` 标记**
4. 将翻译后的内容写回文件

翻译时遵循以下原则：
- 保留代码块、命令、文件路径不翻译
- 保留 Markdown 格式标记
- 技术术语可保留英文或使用通用译名
- 专有名词（API 名称、库名、命令名等）保持原文
- 确保翻译后的内容流畅自然

**产出物语言设定**：在汉化过程中，需要在 SKILL.md 中明确指定输出语言为中文（除非原文另有要求）。这确保汉化后的技能执行时，其产出物默认使用中文：
- 文档和说明使用中文
- 代码注释使用中文
- 程序输出和提示信息使用中文
- 专有名词保持原文

### 第三步：验证输出

确认所有文件已完成翻译，无残留的 `[待翻译]` 标记。

## 手动汉化指南

如需手动汉化，遵循以下规则：

### YAML 元数据翻译

```yaml
# 原文
---
name: pdf-editor
description: Professional PDF editing toolkit for merging, splitting, and rotating PDFs. Use when user asks to "merge PDFs", "split PDF", or "rotate PDF".
---

# 译文
---
name: pdf-editor-cn
description: 专业 PDF 编辑工具包，支持合并、拆分和旋转 PDF。当用户要求"合并 PDF"、"拆分 PDF"、"旋转 PDF"时使用。
---
```

### 正文翻译原则

1. **保留代码块**：代码示例和命令不翻译
2. **保留文件路径**：路径、URL、技术术语保持原样
3. **翻译描述性文本**：说明、指导、步骤描述等
4. **保留格式标记**：Markdown 语法不变
5. **技术术语处理**：
   - 常见术语保留英文或使用通用译名
   - 首次出现可标注英文原文
6. **专有名词保留**：文档中的专有名词（如 API 名称、库名、命令名等）保持原文不翻译

### 产出物语言要求

**核心原则**：汉化后的技能执行时，其产出物应以中文为默认语言。

具体规则如下：

| 场景 | 处理方式 |
|------|---------|
| 原文未指定语言 | 产出物使用中文 |
| 原文要求英文输出 | 保持英文（尊重原文要求） |
| 原文要求其他语言 | 保持该语言（尊重原文要求） |
| 文档中的专有名词 | 保持原文不翻译 |
| 代码注释 | 翻译为中文 |
| 代码输出/提示信息 | 翻译为中文 |
| 代码变量名/函数名 | 保持原文 |

**实施方法**：在汉化 SKILL.md 时，应在技能说明中添加以下内容（如适用）：

```markdown
## 输出语言

本技能的输出内容默认使用中文。除非用户明确要求其他语言，否则：
- 文档和说明使用中文
- 代码注释使用中文
- 程序输出和提示信息使用中文
- 专有名词（API 名称、库名等）保持原文
```

### 文件处理

| 文件类型 | 处理方式 |
|---------|---------|
| SKILL.md | 翻译元数据和正文，添加"输出语言"说明（指定中文为默认） |
| README.md | 翻译为 README-cn.md（仅当目标目录不存在 README-cn.md 时） |
| scripts/* (任意语言) | 翻译注释和输出内容为中文，保留代码逻辑和变量名 |
| scripts/* (二进制文件) | 直接复制，不翻译 |
| references/*.md | 翻译全部内容，专有名词保持原文 |
| references/* (二进制文件) | 直接复制，不翻译 |
| assets/* | 直接复制（图片、模板等） |
| 根目录其他文件 | 直接复制（如 LICENSE.txt 等） |

### 二进制文件检测

脚本会自动检测以下类型的二进制文件并直接复制：

- **图片**：.png, .jpg, .gif, .ico, .webp, .svg 等
- **音频**：.mp3, .wav, .ogg, .flac 等
- **视频**：.mp4, .avi, .mkv, .mov 等
- **压缩包**：.zip, .tar, .gz, .rar, .7z 等
- **可执行文件**：.exe, .dll, .so, .dylib 等
- **字体**：.ttf, .otf, .woff, .woff2 等
- **PDF 和文档**：.pdf, .doc, .docx, .xls, .xlsx 等
- **其他**：.bin, .dat, .pyc, .jar 等

此外，脚本还会通过检测文件内容中的空字节（\x00）来识别未知的二进制文件格式。

### 支持的代码语言

脚本文件支持以下语言的注释翻译：

| 注释风格 | 支持的语言 |
|---------|-----------|
| `#` 单行注释 | Python, Shell, Ruby, YAML, TOML, R, Perl 等 |
| `//` 和 `/* */` | JavaScript, TypeScript, Java, C, C++, Go, Rust, Swift, Kotlin, Scala, C#, PHP 等 |
| `<!-- -->` | HTML, XML, Vue, Svelte 等 |
| `/* */` | CSS, SCSS, LESS 等 |

## 输出结构

汉化后的技能目录：

```
~/.claude/skills/<技能名>-cn/
├── SKILL.md          # 已翻译
├── README-cn.md      # README.md 的中文翻译（如源目录存在 README.md）
├── scripts/          # 注释已翻译
├── references/       # 已翻译（如存在）
├── assets/           # 原样复制（如存在）
└── <其他文件>        # 原样复制（如 LICENSE.txt）
```

## 完整汉化示例

假设用户要求汉化 `pdf-editor` 技能：

**用户**：请汉化 pdf-editor 技能

**Claude 执行流程**：

```
1. 运行脚本：
   python3 ~/.claude/skills/skill-to-cn/scripts/translate_skill.py pdf-editor

2. 脚本输出骨架文件，内容类似：
   ---
   name: pdf-editor-cn
   description: [待翻译] Professional PDF editing toolkit...
   ---
   [待翻译] # PDF Editor
   [待翻译] A professional toolkit for PDF operations.

3. Claude 读取骨架文件，翻译并写入最终内容：
   ---
   name: pdf-editor-cn
   description: 专业 PDF 编辑工具包，支持合并、拆分和旋转 PDF...
   ---
   # PDF 编辑器
   专业 PDF 操作工具包。

4. 确认所有文件已翻译完成，无 [待翻译] 残留
```

**最终输出**：完整可用的中文版技能，用户可直接使用。
