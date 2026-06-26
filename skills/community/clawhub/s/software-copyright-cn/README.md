# software-copyright-cn

中国计算机软件著作权登记申请材料生成器（Claude Code Skill）

## 功能

自动化生成软著申请所需的全部材料：

- **信息采集**：通过对话逐步收集 18 项必填字段（软件名称、版本号、环境信息、功能描述、联系地址等）
- **程序鉴别材料**：从源代码目录自动生成 PDF，支持语法高亮（Pygments）、中文字体、前30+后30页分页
- **文档鉴别材料**：自动生成 60+ 页完整用户手册 PDF，包含概述、架构、功能说明、操作指南等 10 章 + 附录

## 安装

### 方式一：npx skills add（推荐）

使用 [skills](https://github.com/vercel-labs/skills) 一键安装：

```bash
# 安装到所有已检测到的 agent
npx skills add binbin/software-copyright-cn

# 指定安装到 Claude Code
npx skills add binbin/software-copyright-cn -a claude-code

# 全局安装
npx skills add binbin/software-copyright-cn -g
```

> `skills` 是 Vercel 开源的 agent skill 包管理器，支持 Claude Code、Cursor、Copilot、Windsurf 等主流 AI 编程工具。

### 方式二：手动安装 .skill 文件

下载 [software-copyright-cn.skill](./software-copyright-cn.skill) 文件，放入你的 skill 目录即可。

### 方式三：独立使用脚本

不依赖任何 AI agent，直接使用 Python 脚本：

```bash
pip install reportlab pygments
```

#### 生成程序鉴别材料

```bash
python scripts/generate_source_pdf.py <源代码目录> \
  --name "软件全称" --version "V1.0" \
  -o 程序鉴别材料.pdf
```

#### 生成文档鉴别材料

```bash
# 从 JSON 配置自动生成用户手册
python scripts/generate_doc_pdf.py --config software_info.json -o 文档鉴别材料.pdf

# 从已有文档转换
python scripts/generate_doc_pdf.py --input manual.txt \
  --name "软件名" --version "V1.0" --author "权利人" \
  -o 文档鉴别材料.pdf
```

## 特性

- 代码语法高亮（Pygments，支持 50+ 种语言）
- 中文字体自动检测（macOS / Linux / Windows 兼容）
- 多编码支持（UTF-8 / GBK / GB2312 / GB18030）
- 自动跳过 node_modules、.git、\_\_pycache\_\_ 等非源码目录
- 源代码不足 60 页时自动提交全部，超过 60 页时取前 30 + 后 30 页

## 文件结构

```
software-copyright-cn/
├── SKILL.md                       # Skill 主文件（5 阶段工作流）
├── references/
│   └── fields.md                  # 字段说明、验证规则与示例
├── scripts/
│   ├── generate_source_pdf.py     # 程序鉴别材料 PDF 生成器
│   └── generate_doc_pdf.py        # 文档鉴别材料 PDF 生成器
└── software-copyright-cn.skill    # 打包后的 Skill 文件
```

## 许可

MIT
