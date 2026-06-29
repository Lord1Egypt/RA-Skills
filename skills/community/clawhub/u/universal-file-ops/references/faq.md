# 常见问题（FAQ）

---

**Q: 如何确保重复执行不会破坏文件？**

A: 所有写操作（create overwrite、update、delete、move、copy overwrite）执行前会自动备份原文件到备份目录，且脚本支持幂等执行（重复执行结果一致）。如果出错，可用 `python scripts/rollback.py --id <rollback_id>` 回滚。读操作（read）天然幂等，多次执行无副作用。

---

**Q: 可以并行执行多个文件操作吗？**

A: 可以。`scripts/orchestrator.py` 支持并行模式（`--parallel`），适合相互无依赖的批量任务。但同一文件路径的操作会串行排队（通过任务队列保证），避免读写冲突。如果任务间有依赖关系（如任务 2 读任务 1 写的文件），应使用默认串行模式（`--parallel` 不指定）。

---

**Q: `text_crud.py` 和 `office_crud.py` 应该如何选择？**

A: 根据文件格式判断：
- `.txt`, `.py`, `.html`, `.md`, `.csv`, `.json`, `.yaml`, `.xml`, `.css`, `.js`, `.ts` → 使用 `text_crud.py`（按文本读写）
- `.docx` → 使用 `office_crud.py`（需要 `python-docx` 依赖）
- `.xlsx` → 使用 `office_crud.py`（需要 `openpyxl` 依赖）

如果依赖缺失，`office_crud.py` 会返回明确的错误提示，引导安装对应包。

---

**Q: 批量操作失败时，如何快速定位是哪个任务出错？**

A: 有两种方式：
1. **看 orchestrator 返回的 JSON 数组**——每项对应一个任务，按 `success` 字段判断是否成功，`error` 字段包含错误详情。
2. **查看操作日志**——所有操作记录在数据目录下的 logs/ops.log，按时间戳和状态（OK/FAIL）过滤。

建议：批量执行前加 `--dry-run` 先验证配置正确性，再实际执行。

---

**Q: 我想在自己的项目里用类似的文件操作逻辑，可以直接改 `scripts/` 里的脚本吗？**

A: 不建议直接改原始脚本。正确做法是：将 `scripts/` 下的原始脚本作为参考基线，创建一个新的适配副本（如 `my_text_crud.py`），在副本中更新。这样原始脚本保持只读，你可以随时回滚到基线版本，也方便后续合并本技能的更新。

---

**Q: `data/backup/` 目录下的备份文件会一直累积吗？需要手动清理吗？**

A: 当前版本不会自动清理备份文件。如果备份较多占用空间，可以：
1. 手动删除 `data/backup/` 下不再需要的 `.bak` 文件
2. 通过 `python scripts/rollback.py --list` 查看所有备份及其对应的原始文件，按需删除

后续版本计划加入备份保留策略（如保留最近 N 天）。

---

**Q: 为什么 `office_crud.py` 的 update 操作是全文覆盖，而不是局部更新？**

A: 当前版本的 `office_crud.py` 采用简化实现（docx 清空所有段落再重写），主要是为了避免复杂的格式保留逻辑。如果你需要局部更新 docx 内容，建议：
1. 先用 `office_crud.py --action read` 读取全文
2. 在 LLM 中处理文本（插入/替换/删除段落）
3. 再用 `--action create` 全覆盖写入

后续版本计划支持基于段落索引的局部更新。

---

**Q: 如何对 py 文件进行规范化和审查？**

A: 使用 `py_tools.py`：
1. **检查模式**（不更新文件）：`python scripts/py_tools.py normalize --file script.py`
2. **修复模式**（自动备份+修复）：`python scripts/py_tools.py normalize --file script.py --fix`
3. **代码审查**：`python scripts/py_tools.py review --file script.py`

建议在更新 py 文件前先运行 normalize（检查模式），确认无问题后再更新；更新后运行 review 确认无新引入问题。

---

**Q: 如何用 `py_tools.py` 生成测试？**

A: 使用 `gen-test` 子命令：
```bash
# 输出到 stdout
python scripts/py_tools.py gen-test --file script.py

# 直接写入测试文件
python scripts/py_tools.py gen-test --file script.py --output test_script.py
```

生成的测试是 **pytest 风格框架**，包含目标文件的所有公开函数和类的实例化测试。需人工补充断言逻辑（生成脚本无法推断预期行为）。

---

**Q: `py_tools.py oo-ify` 会自动重构我的代码吗？**

A: **不会**。`oo-ify` 只输出建议和示例，**不更新原文件**。你需要根据建议手动重构（或借助其他工具/LLM 辅助重构）。这样设计是为了安全——自动 OO 化可能改变代码语义。

---

**Q: 临时脚本和正式工具的区别是什么？何时豁免 600 行 OO 化限制？**

A: 根据 `references/py_standards.md` 第 7.5 节：

| 类型 | 定义 | 600 行 OO 化限制 |
|------|------|---------------------|
| **临时脚本** | 一次性任务、临时数据处理、临时测试 | **豁免**（不需要 OO 化） |
| **正式工具** | skill 脚本、长期维护的工具类脚本 | **必须 OO 化** |

**判断标准：**
- 文件路径在 `skills/` 下 → 正式工具
- 文件头部有 `# 临时脚本` 注释 → 临时脚本
- 文件有 shebang 且放在系统路径 → 正式工具
- 文件在 `/tmp`、`/temp`、用户临时目录 → 临时脚本
- 默认保守判断为**正式工具**

---

**Q: 如何用 `python_env.py` 安装指定版本的 Python？**

A: `python_env.py` 本身不安装 Python（需要系统管理员权限），但它可以：
1. **检测已安装版本**：`python scripts/python_env.py detect`
2. **创建 venv（使用指定版本）**：`python scripts/python_env.py setup --python-version 3.11`
3. **切换 venv 的 Python 版本**：`python scripts/python_env.py switch --python-version 3.11`

如果需要安装新的 Python 版本，请：
- Windows：从 https://www.python.org/downloads/ 下载安装
- Linux：使用 `apt install python3.11` 或 `pyenv`
- macOS：使用 `brew install python@3.11` 或 `pyenv`

---

**Q: 如何用 `python_env.py` 干净重装 Python 环境？**

A: 使用 `clean-reinstall` 子命令：

```bash
# 删除当前 venv 并重新创建（默认 Python 3.11）
python scripts/python_env.py clean-reinstall

# 指定 Python 版本并安装常用包
python scripts/python_env.py clean-reinstall --python-version 3.11 --install-common
```

**行为：**
1. 删除当前 venv（如果存在）
2. 使用指定 Python 版本重建 venv
3. 如果 `requirements.txt` 存在，自动重新安装所有包

---

**Q: `python_env.py` 和 `venv` 有什么区别？**

A: `python_env.py` 是 **venv 的管理工具**，提供比原生 `venv` 更完整的 CLI 接口：

| 功能 | 原生 venv | python_env.py |
|------|-----------|----------------|
| 创建 venv | `python -m venv` | `python python_env.py setup` |
| 安装包 | 手动 `pip install` | `python python_env.py install --packages ...` |
| 更新包 | 手动 `pip install -U` | `python python_env.py update` |
| 列出包 | `pip list` | `python python_env.py list` |
| 切换 Python 版本 | 不支持 | `python python_env.py switch --python-version 3.11` |
| 干净重装 | 手动删除+重建 | `python python_env.py clean-reinstall` |
| 检测已安装版本 | 不支持 | `python python_env.py detect` |
| 自动更新 requirements.txt | 不支持 | 支持 |

**推荐使用 `python_env.py`**，因为它提供标准化的 JSON IO，更适合 LLM 调用和自动化流程。

---

**Q: universal-file-ops 有哪些能力边界限制？**

A: 本技能的能力边界如下：

| 类别 | 限制 |
|------|------|
| 文件大小 | 文本文件单次读写不超过 50MB |
| 并行任务 | 最多同时 10 个并行任务 |
| Python 版本 | 仅支持 Python 3.8+ |
| 文件类型 | 仅支持文本文件和 Office 文件（.docx/.xlsx） |
| 网络访问 | pip 安装时需要网络连接；其他操作不需要网络 |


---
