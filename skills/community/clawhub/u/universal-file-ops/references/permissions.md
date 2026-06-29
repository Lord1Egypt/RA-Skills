# 权限说明（universal-file-ops）

本技能的整体权限权重为 **MEDIUM**，原因如下：

---

## 权限权重说明

| 操作类型 | 权重占比 | 说明 |
|---------|---------|------|
| 文件读取（read） | 0% | 仅读取用户指定文件，无副作用 |
| 文件写入（create/update） | 10% | 会修改文件系统，但强制备份 |
| 文件删除（delete） | 20% | 破坏性操作，但强制备份可回滚 |
| 文件移动/重命名（move/rename） | 15% | 同删除+创建，强制备份 |
| 子进程调用（orchestrator） | 30% | `orchestrator.py` 用 `subprocess.run` 调用其他脚本 |
| 网络访问 | 0% | 无 |
| 凭证/Token 读取 | 0% | 无 |

**综合评估：MEDIUM**
- `orchestrator.py` 使用 `subprocess.run` 调用子脚本，存在代码执行风险（虽参数完全由 JSON 控制，无注入风险）
- 所有写操作强制备份，可回滚，降低了实际风险
- 无网络访问、无凭证读取，整体风险可控

---

## 各脚本权限说明

### text_crud.py

| 操作 | 风险等级 | 说明 |
|------|---------|------|
| read | LOW | 只读，无副作用 |
| create（overwrite=false） | LOW | 创建新文件，不覆盖 |
| create（overwrite=true） | MEDIUM | 覆盖已有文件，但强制备份 |
| update | MEDIUM | 修改已有文件，强制备份 |
| delete | MEDIUM | 删除文件，强制备份 |

### office_crud.py

依赖 `python-docx` / `openpyxl`，逻辑与 `text_crud.py` 类似，权限等级相同。

### file_ops.py

| 操作 | 风险等级 | 说明 |
|------|---------|------|
| copy（overwrite=false） | LOW | 拷贝文件，不覆盖 |
| copy（overwrite=true） | MEDIUM | 覆盖目标文件，强制备份 |
| move | MEDIUM | 移动文件，强制备份源和目标 |
| rename | MEDIUM | 封装 move，同级 |
| delete | MEDIUM | 删除文件/目录，强制备份 |

### orchestrator.py

| 操作 | 风险等级 | 说明 |
|------|---------|------|
| 串行执行 | MEDIUM | `subprocess.run` 调用子脚本 |
| 并行执行 | MEDIUM | 多线程，同样使用 `subprocess.run` |

**安全边界：**
- 子进程参数完全来自 JSON（`input=` 或 `--input`），无 shell 注入风险
- 调用的脚本路径硬编码在 `OP_MAP` 中，不可被用户控制
- 超时时间硬编码为 30 秒，防止子进程挂起

---

## 敏感信息访问声明

本技能 **不访问** 以下敏感位置：
- WorkBuddy 配置目录（仅读写用户指定路径）
- 系统目录（`/etc/`, `/Windows/`, 等）
- 凭证文件（`*.key`, `*.pem`, `.env`, 等）

`--no-backup` 参数会跳过备份，属于高风险选项，建议在非生产环境才使用。

---

## 关键位置写入声明

本技能 **不写入** 以下关键位置：
- WorkBuddy 配置目录
- 系统目录
- 启动脚本、登录脚本

写入位置仅限于：
1. 用户显式指定的文件路径
2. 备份目录（备份文件）
3. 操作日志目录（日志文件）

---

## 高风险操作授权

当前版本 **不支持** 运行时授权请求（所有操作直接执行）。

后续版本计划集成 `authorization_manager.py`（来自 `skill-standardization`），对以下操作进行授权确认：
- `delete`（删除文件/目录）
- `create --overwrite`（覆盖已有文件）
- `--no-backup`（跳过备份）

---

## 审计与回溯

所有操作记录在操作日志文件中。

格式：`[timestamp] OK|FAIL | action | file_path | rollback=... | detail`

备份文件记录在备份目录的 manifest.txt 中。

回滚操作：
```bash
python scripts/rollback.py --id "<rollback_id>"
```
