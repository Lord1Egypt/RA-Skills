---
name: zotero-local-import
description: 通过 Zotero 本地连接器（127.0.0.1），在 Windows/macOS/Linux 上使用命令行将本地 PDF 文件导入 Zotero。用户需要导入单个文件、批量导入文件夹、导入到已有分类、列出分类或校验最近导入的附件时使用。需要在 Zotero 桌面端设置中允许本机应用与 Zotero 通信，并由用户提供连接端口。使用时用户需要向agent提供pdf文件绝对路径或pdf文件所处文件夹绝对路径。仅在 Windows 平台测试通过。
---

# Zotero Local Import Skill（Windows / macOS / Linux）

使用本技能前，先确认 Zotero 桌面端已开启并完成以下设置：

1. 打开 **Zotero → 设置 → 高级**
2. 勾选：**允许此计算机中的其他应用程序与 Zotero 通讯**
3. 记下该接口端口（默认常见为 `23119`）并告诉 Agent，用于脚本参数 `--port`

> 该技能只支持“导入到已存在分类”。**不会创建分类**。
> 若不指定 `--collection`，默认导入到 **我的文库**。

## 脚本位置

- `scripts/zotero_tool.py`

## 功能清单

1. 导入单个 PDF
2. 导入整个文件夹 PDF（可递归）
3. 导入到指定的“已存在分类”
4. 列出 Zotero 本地分类
5. 检查最近导入附件（读取 `zotero.sqlite`，只读）

## Agent 执行前置（傻瓜模式）

agent 必须支持以下任一输入形态并自动完成导入：
1. 一个文件夹路径
2. 一个 PDF 路径
3. 多个 PDF 路径
4. 某文件夹下的几个 PDF（用户只说某文件夹的文件名也可以，如 `x.pdf, y.pdf, z.pdf`）

同时收集：
- Zotero 本地通讯端口（用户在 Zotero 高级设置里看到的端口）
- 可选分类名（不提供则默认导入“我的文库”）

固定流程：先跑 `doctor --auto-install-deps`，通过后再执行导入。

自然语言解析（路径、文件名、端口、分类）必须由 agent 完成；脚本只接受结构化参数并执行导入。

## 命令用法

在仓库根目录执行（或使用绝对路径调用脚本）：

```bash
python skills/zotero-local-import-zh/scripts/zotero_tool.py --help
```

### 0) 先自动检测运行环境（必跑）

```bash
python skills/zotero-local-import-zh/scripts/zotero_tool.py doctor \
  --port <用户提供的Zotero端口> \
  --auto-install-deps
```

会检测并自动处理：
- Python 是否可用
- `requests` 是否已安装（缺失时自动 `pip install`）
- `http://127.0.0.1:<port>/connector/ping` 是否可达
- 平台 URL 打开器是否可用（Windows: `os.startfile` / macOS: `open` / Linux: `xdg-open`）

如果自动安装失败，agent 应回显错误并提示用户手动执行：

```bash
python -m pip install requests>=2.31.0
```

### NL) 自然语言输入规范（由 agent 解析，不由脚本解析）

用户可以说：
- 帮我导入 `xxx文件夹` 中的 `x.pdf,y.pdf,z.pdf`，端口 `xxxx`，分类 `xxxx`
- 帮我导入这个 PDF：`<绝对路径>`，端口 `xxxx`

agent 必须先把自然语言解析成结构化参数，再调用脚本 `import`：
- 文件夹场景：`--dir` + 可选 `--pick`
- 单/多 PDF 场景：`--pdf`（可重复）
- 端口：`--port`
- 分类：`--collection`（可选，不传则默认我的文库）

### A) 导入单个 PDF（路径必须由用户提供）

```bash
python skills/zotero-local-import-zh/scripts/zotero_tool.py import \
  --pdf "<用户实际PDF绝对路径>" \
  --port <用户提供的Zotero端口>
```

### A2) 导入多个 PDF（重复传 `--pdf`）

```bash
python skills/zotero-local-import-zh/scripts/zotero_tool.py import \
  --pdf "<PDF路径1>" \
  --pdf "<PDF路径2>" \
  --pdf "<PDF路径3>" \
  --port <用户提供的Zotero端口>
```

### B) 批量导入文件夹（不递归，路径由用户提供）

```bash
python skills/zotero-local-import-zh/scripts/zotero_tool.py import \
  --dir "<用户实际文件夹绝对路径>" \
  --port <用户提供的Zotero端口>
```

### C) 批量导入文件夹（递归，路径由用户提供）

```bash
python skills/zotero-local-import-zh/scripts/zotero_tool.py import \
  --dir "<用户实际文件夹绝对路径>" \
  --recursive \
  --port <用户提供的Zotero端口>
```

### D) 导入到指定分类（分类必须已存在）

```bash
python skills/zotero-local-import-zh/scripts/zotero_tool.py import \
  --dir "<用户实际文件夹绝对路径>" \
  --recursive \
  --collection "<用户指定分类名>" \
  --port <用户提供的Zotero端口>
```

### D2) 导入某文件夹下的指定几个 PDF（用户说文件名列表）

```bash
python skills/zotero-local-import-zh/scripts/zotero_tool.py import \
  --dir "<用户实际文件夹绝对路径>" \
  --pick "x.pdf,y.pdf,z.pdf" \
  --collection "<用户指定分类名>" \
  --port <用户提供的Zotero端口>
```

也可重复传参：

```bash
python skills/zotero-local-import-zh/scripts/zotero_tool.py import \
  --dir "<用户实际文件夹绝对路径>" \
  --pick "x.pdf" \
  --pick "y.pdf" \
  --pick "z.pdf" \
  --port <用户提供的Zotero端口>
```

### E) 列出本地分类

```bash
python skills/zotero-local-import-zh/scripts/zotero_tool.py list-collections --port <用户提供的Zotero端口>
```

### F) 检查最近导入附件

```bash
python skills/zotero-local-import-zh/scripts/zotero_tool.py check --limit 10
```

## 关键参数

- `--port`：Zotero 本地通讯端口（由用户告知；脚本默认读取环境变量 `ZOTERO_PORT`，若未设置则回退 23119）
- `--timeout`：HTTP 超时秒数（默认 90）
- `--collection`：目标分类名（已存在）
- `--db`：`zotero.sqlite` 路径（check 命令可覆盖）

## 平台补充

- Windows：默认可用（脚本已启用 UTF-8 输出增强）
- macOS：需系统可调用 `open`
- Linux：需安装并可调用 `xdg-open`

## 失败处理

- `error=collection not found`：分类不存在，要求用户先在 Zotero 中手工创建分类，因为自动创造分类会有意想不到的问题
- 连接失败：检查 Zotero 是否打开、是否勾选“允许此计算机中的其他应用程序与 Zotero 通讯”、端口是否正确
- 导入失败：先对单个 PDF 复测，再跑目录批量
