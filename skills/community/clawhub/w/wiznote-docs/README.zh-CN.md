# wiznote

让 WizNote 成为 Claude 驱动开发中的文档主源。

[English](./README.md) | 简体中文

`wiznote` 是一个可公开发布、去隐私化的 Claude skill 与 Python 辅助工具集，适合希望同时获得私有部署、仓库镜像和 Claude 友好工作流的开发者。

它特别适合个人开发者或小团队的 vibe coding：计划、设计、笔记和实现上下文可以持续贴近代码，而不需要引入笨重的文档管理平台。

## 为什么开发者会想用它

- **默认适合私有化** —— 可以直接连接你自己部署的 WizNote，而不是把文档迁到公共 SaaS 平台
- **适合 Claude 工作流** —— 可与 Claude Code 配合使用，也容易延展到桌面端、Web 端、IDE 场景下的仓库型工作流
- **跨端连续性更好** —— 在一个端写或同步文档后，换到另一个端仍然围绕同一套文档主源继续工作
- **适合个人或小团队 vibe coding** —— 文档、设计、计划、实现过程可以始终贴近代码库
- **自带仓库镜像能力** —— 既保留 WizNote 作为主源，又保留 `docs/wiznote-mirror/...` 下的 Markdown 镜像

它来源于一个私有内部工作流，但已经移除了所有用户相关路径、私有服务地址、账号密码以及组织专用的目录映射。

## 包含内容

- `SKILL.md` —— Claude Code skill 定义
- `wiznote_cli.py` —— 登录、列出、下载、新建、更新笔记的辅助方法
- `wiznote_helper.py` —— 分类路径校验、镜像路径生成、HTML body 提取等辅助方法
- `tests/` —— 面向公开版行为的 pytest 测试

## 功能特性

- 通过显式参数或环境变量登录 WizNote
- 在可配置的分类根路径下列出笔记
- 下载笔记 HTML
- 用 HTML 创建新笔记
- 更新已有笔记
- 将笔记安全镜像到 `docs/wiznote-mirror/...`
- 校验分类路径，确保同步范围不会超出你指定的根目录
- 镜像文件名支持 Unicode/中文标题

## 环境要求

- 建议 Python 3.11+
- 可访问的 WizNote 服务
- 视你的工作流而定的可选依赖：
  - `markdown`：用于 Markdown → HTML 转换
  - `pytest`：用于运行内置测试

## 安装方式

### 方式 1：作为 Claude Code skill 使用

将当前目录复制到 Claude 的 skills 目录：

```bash
mkdir -p ~/.claude/skills
cp -R ./wiznote ~/.claude/skills/wiznote
```

### 方式 2：直接放在你的仓库里

你也可以直接把 `wiznote/` 保留在自己的仓库中，然后在脚本里直接导入这些 Python 文件。

## 配置说明

先设置环境变量：

```bash
export WIZNOTE_BASE_URL="https://notes.example.com"
export WIZNOTE_USER="you@example.com"
export WIZNOTE_PASSWORD="your-password"
```

另外，你的脚本中还需要两个运行时参数：

- `category_root` —— 你希望同步到的 WizNote 顶层分类，例如 `/team/docs/`
- `repo_root` —— 本地仓库根目录，用于生成镜像文件路径

## 快速开始

### 1. 导入辅助文件

```python
from pathlib import Path
import sys

SKILL_DIR = Path("/path/to/wiznote")
sys.path.insert(0, str(SKILL_DIR))

import wiznote_cli as cli
import wiznote_helper as helper
```

### 2. 加载凭据并登录

```python
creds = cli.load_credentials()
login = cli.login(creds)
```

或者直接显式传入：

```python
creds = cli.load_credentials(
    base_url="https://notes.example.com",
    user="you@example.com",
    password="your-password",
)
login = cli.login(creds)
```

### 3. 指定分类根路径和目标分类

```python
category_root = helper.normalize_category_root("/team/docs/")
category = helper.resolve_category(category_root, "plans/")
```

### 4. 列出笔记

```python
payload = cli.fetch_note_list(
    base_url=login.kb_server,
    kb_guid=login.kb_guid,
    token=login.token,
    category=category,
)
```

### 5. 创建笔记

```python
html = "<h1>Project Design</h1><p>...</p>"

result = cli.create_note(
    base_url=login.kb_server,
    kb_guid=login.kb_guid,
    token=login.token,
    title="Project Design",
    category=category,
    html=html,
)
```

### 6. 生成安全的本地镜像路径

```python
mirror_path = helper.mirror_output_path(
    repo_root=Path("/path/to/repo"),
    category_root=category_root,
    category=category,
    title="Project Design",
)
```

## 推荐同步流程

1. 配置凭据
2. 规范化分类根路径
3. 登录一次并复用 session
4. 解析出最终目标分类
5. 写入前先列出现有笔记
6. 将 Markdown 转成 HTML
7. 先写 WizNote，再刷新本地镜像
8. 最后重新列出分类确认写入结果

## Markdown 转 HTML

`create_note(...)` 和 `save_note(...)` 接收的是 HTML，不是原始 Markdown。

示例：

```bash
python3 -m pip install markdown
```

```python
import markdown

html = markdown.markdown(text, extensions=["extra", "fenced_code", "tables", "sane_lists"])
```

## 运行测试

```bash
python3 -m pip install pytest
pytest wiznote/tests
```

## 隐私与开源发布说明

这个公开版刻意避免包含以下信息：

- 本地用户目录
- 私有服务地址
- 用户名或密码
- 组织内部固定项目目录映射

如果你继续 fork 或改造它，公开发布前也要确保没有把自己的私有基础设施信息带进去。

## 目录结构

```text
wiznote/
├── README.md
├── README.zh-CN.md
├── SKILL.md
├── wiznote_cli.py
├── wiznote_helper.py
└── tests/
    ├── conftest.py
    ├── test_cli.py
    └── test_helper.py
```

## License

MIT。见 [`LICENSE`](./LICENSE)。
