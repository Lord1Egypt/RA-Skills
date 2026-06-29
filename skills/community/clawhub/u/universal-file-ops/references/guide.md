# universal-file-ops 使用指南

本指南详细说明 universal-file-ops 技能的使用方式、脚本接口和设计理念。

---

## 设计理念

1. **鲁棒性优先**：所有写操作前自动备份，支持回滚
2. **标准化 IO**：所有脚本输入输出均为 JSON，便于程序化调用和调试
3. **幂等性**：重复执行不产生副作用（读操作天然幂等，写操作在适当条件下幂等）
4. **可回溯**：所有操作记录日志，备份留存。

---

## 快速开始

### 方式一：直接调用脚本（LLM 推荐）

```bash
# 读取文件
python scripts/text_crud.py --action read --file hello.txt

# 创建文件（自动备份已有文件）
python scripts/text_crud.py --action create --file hello.txt --content "Hello World"

# 拷贝文件
python scripts/file_ops.py --action copy --src hello.txt --dst hello_copy.txt

# 删除文件（先备份）
python scripts/file_ops.py --action delete --file hello.txt
```

### 方式二：JSON 模式（程序化调用）

```bash
# 通过 stdin 传入 JSON
echo '{"action":"create","file":"test.txt","content":"Hello"}' | python scripts/text_crud.py

# 通过 --input 文件传入
echo '{"action":"copy","src":"a.txt","dst":"b.txt"}' > /tmp/req.json
python scripts/file_ops.py --input /tmp/req.json
```

### 方式三：通过 orchestrator 批量执行

```bash
# 1. 编写批量配置文件 batch.json
# 2. 执行
python scripts/orchestrator.py --batch batch.json
```

---

## 标准化 IO 接口

所有脚本遵循统一的输入输出规范。

### 输入（三种方式）

| 方式 | 适用场景 |
|------|----------|
| CLI 参数（`--action --file ...`） | LLM 直接调用，最简单 |
| stdin JSON | 管道传递，程序化调用 |
| `--input <file>` | JSON 配置从文件读取 |

### 输出（统一 JSON 到 stdout）

**成功时：**
```json
{
  "success": true,
  "action": "create",
  "file": "path/to/file.txt",
  "result": { "size": 11, "backup_file": "..." },
  "error": null,
  "rollback_id": "backup/20260525_...bak"
}
```

**失败时：**
```json
{
  "success": false,
  "action": null,
  "file": "path/to/file.txt",
  "result": null,
  "error": "文件不存在: ...",
  "rollback_id": null
}
```

### rollback_id 的使用

`rollback_id` 是备份文件的相对路径（相对于 `data/backup/`）。
用于出错时回滚：

```bash
python scripts/rollback.py --id "20260525_164457_file.txt_abcdef01.bak"
```

---

## 各脚本说明

### text_crud.py — 文本类文件增删查改

支持格式：`.txt`, `.py`, `.html`, `.md`, `.csv`, `.json`, `.yaml`, `.xml`, `.css`, `.js`, `.ts`

| action | 必填参数 | 可选参数 | 说明 |
|--------|------------|------------|------|
| `read` | `--file` | `--encoding`（默认 utf-8） | 读取文件内容 |
| `create` | `--file`, `--content` | `--overwrite`, `--no-backup` | 创建文件 |
| `update` | `--file`, `--content` | `--mode`（`replace`/`append`/`insert`）, `--line`, `--no-backup` | 更新文件 |
| `delete` | `--file` | `--no-backup` | 删除文件 |

### office_crud.py — Office 文件增删查改

支持格式：`.docx`, `.xlsx`

依赖（可选，缺失时报错引导安装）：
- `python-docx`（处理 .docx）：`pip install python-docx`
- `openpyxl`（处理 .xlsx）：`pip install openpyxl`

| action | 必填参数 | 说明 |
|--------|------------|------|
| `read` | `--file` | 读取 docx 全文 / xlsx 全部 sheet |
| `create` | `--file`, `--content`（docx 时） | 创建 Office 文件 |
| `update` | `--file`, `--content` | 更新 docx 全文覆盖 |
| `delete` | `--file` | 删除 Office 文件 |

### file_ops.py — 通用文件操作

| action | 必填参数 | 可选参数 | 说明 |
|--------|------------|------------|------|
| `copy` | `--src`, `--dst` | `--overwrite`, `--no-backup` | 拷贝文件或目录 |
| `move` | `--src`, `--dst` | `--overwrite`, `--no-backup` | 移动（跨文件系统自动降级为 拷贝+删除） |
| `rename` | `--file`, `--new-name` | `--overwrite`, `--no-backup` | 重命名（封装 move） |
| `delete` | `--file` | `--no-backup` | 删除文件或目录（不存在时幂等返回 success） |

### orchestrator.py — 统一调度器

| 参数 | 说明 |
|------|------|
| `--list` | 列出所有可用操作 |
| `--op <name>` | 单操作模式（从 stdin 传 JSON） |
| `--batch <file>` | 批量执行（JSON 配置文件） |
| `--parallel` | 并行执行（默认串行） |
| `--no-stop` | 失败不中止（继续后续任务） |
| `--dry-run` | 仅打印计划，不实际执行 |

### rollback.py — 容灾回滚

| 参数 | 说明 |
|------|------|
| `--id <backup_file>` | 回滚单个备份 |
| `--ids <id1,id2>` | 批量回滚 |
| `--restore-to <path>` | 显式指定恢复路径（覆盖 manifest） |
| `--list` | 列出所有可用备份 |
| `--dry-run` | 预览模式 |

---

### py_tools.py — Python 代码工具链

提供四个子命令：`normalize`、`review`、`oo-ify`、`gen-test`。
所有子命令遵循标准化 JSON IO（同其他脚本一致）。

| 子命令 | 必填参数 | 可选参数 | 说明 |
|---------|------------|------------|------|
| `normalize` | `--file` | `--fix`（修复模式） | 检查/修复 py 文件常见问题 |
| `review` | `--file` | — | 代码审查（语法/风格/bug/行数） |
| `oo-ify` | `--file` | — | >600 行文件给出 OO 化建议（不更新文件） |
| `gen-test` | `--file` | `--output`（输出路径） | 生成 pytest 测试框架 |

#### normalize — 规范化

检查项（对应 `references/py_standards.md`）：

| # | 检查项 | `--fix` 可修复 |
|---|--------|----------------|
| 1 | UTF-8 BOM | ✅ 删除 |
| 2 | 编码声明缺失/非 utf-8 | ✅ 插入/修正 |
| 3 | Tab 缩进 | ✅ 替换为 4 空格 |
| 4 | 行尾空白 | ✅ 去除 |
| 5 | 文件末尾无换行 | ✅ 追加 `\n` |
| 6 | CRLF 换行符 | ✅ 替换为 `\n` |
| 7 | 代码区中文符号 `（），；：！？""【】` | ✅ 替换为英文半角 |
| 8 | 行长度 >120 | ❌ 需人工处理 |

**使用建议：**
- 先运行**检查模式**（`--fix` 不指定）查看问题清单
- 确认后运行**修复模式**（`--fix`），会自动备份原文件
- 修复后运行 `review` 确认无新引入问题

#### review — 代码审查

执行以下检查：
1. **语法检查** — `ast.parse`，失败直接返回 error
2. **docstring 检查** — 公共函数/类缺少 docstring → warning
3. **行数检查** — >600 行 → info（并建议 OO 化）
4. **未使用 import** — 简化启发式检查
5. **函数过长** — >50 行 → info

**使用建议：**
- 每次更新 py 文件后运行 `review` 确认无新引入问题
- `suggest_oo: true` 时，运行 `py_tools.py oo-ify` 查看具体建议

#### oo-ify — OO 化建议

仅当文件 >600 行时输出建议（**不更新原文件**）：
- 按函数名前缀分组，建议封装为类
- 全局变量 ≥3 个，建议提升为类属性
- >1000 行，建议按功能拆分为多个模块

**输出：** JSON 包含 `suggestions` 数组，每项有 `type`、`description`、`example`。

#### gen-test — 生成测试

分析目标文件的公开函数和类，生成 pytest 测试框架（模板代码）。
- 自动推导函数参数示例值（基于参数名启发式）
- 可选 `--output` 直接写入测试文件
- 私有函数（前缀 `_`）自动跳过

**使用建议：**
- 生成后需人工补充断言逻辑（生成的是框架/模板）
- 建议将生成的测试文件保存为 `test_<module>.py`

---

### python_env.py — Python 环境管理

提供 8 个子命令：`setup` / `install` / `uninstall` / `update` / `list` / `switch` / `remove` / `clean-reinstall` / `detect`。

所有子命令遵循标准化 JSON IO（同其他脚本一致）。

| 子命令 | 必填参数 | 可选参数 | 说明 |
|---------|------------|------------|------|
| `setup` | — | `--venv`、`--python-version`、`--install-common` | 创建 venv（默认 Python 3.11） |
| `install` | `--packages` | `--venv` | 安装包（自动更新 requirements.txt） |
| `uninstall` | `--packages` | `--venv` | 卸载包 |
| `update` | — | `--packages`、`--venv` | 更新包（不指定包名则更新所有过期包） |
| `list` | — | `--venv`、`--format` | 列出已安装包（json / table） |
| `switch` | `--python-version` | `--venv` | 切换 Python 版本（重建 venv，保留 requirements.txt） |
| `remove` | — | `--venv` | 删除 venv |
| `clean-reinstall` | — | `--venv`、`--python-version`、`--install-common` | 干净重装（删除并重建 venv） |
| `detect` | — | — | 检测已安装的 Python 版本 |

#### setup — 创建 venv

```bash
# 默认 Python 3.11
python scripts/python_env.py setup

# 指定 Python 版本
python scripts/python_env.py setup --python-version 3.11

# 创建 venv 并安装常用包
python scripts/python_env.py setup --install-common

# 指定 venv 路径
python scripts/python_env.py setup --venv /path/to/venv
```

**默认偏好版本：** Python 3.11（稳定版，兼容性最好）。

**常用包（`--install-common`）：** `requests`、`pyyaml`、`python-dotenv`、`pytest`。

#### install / uninstall / update — 包管理

```bash
# 安装包
python scripts/python_env.py install --packages requests pyyaml

# 卸载包
python scripts/python_env.py uninstall --packages requests

# 更新指定包
python scripts/python_env.py update --packages requests

# 更新所有过期包
python scripts/python_env.py update
```

**注意：** 所有包操作自动更新 `requirements.txt`。

#### list — 列出已安装包

```bash
# JSON 格式（默认）
python scripts/python_env.py list

# 表格格式
python scripts/python_env.py list --format table
```

#### switch — 切换 Python 版本

```bash
# 切换到 Python 3.11（会重建 venv）
python scripts/python_env.py switch --python-version 3.11
```

**行为：**
1. 备份当前 venv（重命名为 `<venv>_backup_<timestamp>`）
2. 用指定 Python 版本重建 venv
3. 如果 `requirements.txt` 存在，自动重新安装所有包

#### clean-reinstall — 干净重装

```bash
# 删除 venv 并重新创建（默认 Python 3.11）
python scripts/python_env.py clean-reinstall

# 指定 Python 版本并安装常用包
python scripts/python_env.py clean-reinstall --python-version 3.11 --install-common
```

#### detect — 检测已安装版本

```bash
python scripts/python_env.py detect
```

**输出示例：**
```json
{
  "status": "success",
  "installed_versions": [
    {"version": "3.11.8", "executable": "C:\\Python311\\python.exe", "source": "filesystem"},
    {"version": "3.13.12", "executable": "C:\\Users\\sm001\\AppData\\Local\\Programs\\Python\\Python313\\python.exe", "source": "py_launcher"}
  ],
  "preferred_version": {"version": "3.11.8", "executable": "...", "source": "filesystem"},
  "default_prefer": "3.11",
  "code": 0
}
```

#### LLM 使用建议

1. **任务需要 Python 环境时** → 先运行 `python_env.py detect` 确认可用版本
2. **需要安装依赖时** → 运行 `python_env.py setup --install-common` 创建干净环境
3. **安装项目依赖时** → 运行 `python_env.py install --packages <包列表>`
4. **Python 版本不匹配时** → 运行 `python_env.py switch --python-version <版本>`
5. **环境损坏时** → 运行 `python_env.py clean-reinstall` 干净重装

---

## 批量配置格式（batch.json）

```json
{
  "tasks": [
    {
      "op": "text_crud",
      "args": {"action": "create", "file": "a.txt", "content": "Hello"}
    },
    {
      "op": "file_ops",
      "args": {"action": "copy", "src": "a.txt", "dst": "b.txt"}
    },
    {
      "op": "text_crud",
      "args": {"action": "read", "file": "b.txt"}
    }
  ],
  "parallel": false,
  "stop_on_error": true
}
```

**字段说明：**
- `tasks`：任务数组，每项包含 `op`（操作脚本名）和 `args`（传给脚本的 JSON 参数）
- `parallel`：`true` 时并行执行（线程池），`false` 时串行
- `stop_on_error`：`true` 时任意任务失败立即中止后续任务

---

## 容灾与回溯机制

### 自动备份

所有破坏性操作（create overwrite、update、delete、move、copy overwrite）执行前，自动将目标文件备份至备份目录：

备份文件名格式：`<时间戳>_<原文件名>_<SHA256前8位>.bak`

### 回滚

1. 从操作结果的 `rollback_id` 字段获取备份文件名
2. 执行回滚：

```bash
python scripts/rollback.py --id "<rollback_id>"
```

3. 批量回滚（orchestrator 失败时会打印提示）：

```bash
python scripts/rollback.py --ids "id1.bak,id2.bak"
```

### 操作日志

所有操作记录在：

格式：`[timestamp] OK|FAIL | action | file_path | rollback=... | detail`

---

## LLM 使用建议

1. **优先直接调用脚本**（方式一），最简单直观
2. **需要编排多步骤时使用 orchestrator**（方式三）
3. **不要更新 `scripts/` 下的原始脚本**——如需适配，创建副本并注明来源
4. **检查返回的 `success` 字段**——失败时有 `error` 字段说明原因
5. **重要操作前可手动备份**——虽然脚本自动备份，但重要数据双重保护更安全
