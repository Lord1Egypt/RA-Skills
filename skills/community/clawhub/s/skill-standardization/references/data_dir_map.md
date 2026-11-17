# skill-standardization 数据目录路径引用对照表

## 设计原则

1. **安装目录**（`skills/<name>/` 或 `skills/installed/<name>/`）—— 由平台/智能体管理，代码不干涉
2. **数据目录**（`skills/.standardization/<name>/`）—— 固定结构，平台更新技能时不被清除
3. **通用路径计算**（不依赖 `..`，适用于任何安装结构）：
   ```python
   SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
   SKILL_DIR   = os.path.dirname(SCRIPT_DIR)          # → .../<name>/
   SKILLS_ROOT = os.path.dirname(SKILL_DIR)         # → .../skills/ 或 .../skills/installed/
   SKILL_NAME   = os.path.basename(SKILL_DIR)         # → <name>
   DATA_DIR     = os.path.join(SKILLS_ROOT, ".standardization", SKILL_NAME)
   ```

---

## 数据目录子目录分类（`.standardization/<name>/` 下）

| 分类 | 路径 | 用途 | 生命周期 |
|---|---|---|---|
| 持久化业务数据 | `data/` | 配置快照、进度文件、用户偏好 | 永久 |
| 临时文件 | `temp/` | 会话级中间产物、`.tmp` 文件 | 会话级（操作完即清） |
| 操作备份 | `backup/` | `safe_io.py` 写操作备份、回滚用 | 保留最新 10 个 |
| 缓存 | `cache/` | API 响应缓存、计算中间结果 | 可重建，可随时清空 |
| 输出产物 | `output/` | 技能生成的报告、导出文件、用户可见产物 | 永久 |
| 状态文件 | `state/` | 进度锁、PID 文件、运行标志 | 运行时 |

> **不需要** `misc/` 或 `other/` 分类。无法分类的文件应在 `data/` 下按功能建子目录。

---

## 本技能自身文件引用对照表

| 文件 | 行号 | 引用路径/变量 | 用途 | 自定义时改哪里 |
|---|---|---|---|---|
| `scripts/safe_io.py` | 25 | `SKILL_ROOT = os.path.dirname(...)` | 安装目录根 | 由平台决定，不改 |
| `scripts/safe_io.py` | 26 | `SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))` | 脚本所在目录 | 不改 |
| `scripts/safe_io.py` | 27 | `SKILL_DIR = os.path.dirname(SCRIPT_DIR)` | 技能安装目录 | 不改 |
| `scripts/safe_io.py` | 28 | `SKILLS_ROOT = os.path.dirname(SKILL_DIR)` | 安装根目录（通用） | 不改 |
| `scripts/safe_io.py` | 29 | `SKILL_NAME = os.path.basename(SKILL_DIR)` | 技能名（通用） | 不改 |
| `scripts/safe_io.py` | 30 | `DATA_DIR = os.path.join(SKILLS_ROOT, ".standardization", SKILL_NAME)` | **数据目录根（通用）** | **改此处即改全技能数据路径** |
| `scripts/safe_io.py` | 31 | `BACKUP_DIR = os.path.join(DATA_DIR, "backup")` | 备份目录 | 随 `DATA_DIR` 自动变化 |
| `scripts/safe_io.py` | 32 | `OPS_LOG = os.path.join(DATA_DIR, "logs", "ops.log")` | 日志文件路径 | 随 `DATA_DIR` 自动变化 |
| `SKILL.md` frontmatter | 12 | `data_dir: ../.standardization/skill-standardization/` | 声明数据目录 | 改此处声明 + 所有 `.py` 中的 `DATA_DIR` 计算逻辑 |

---

## 自定义数据目录路径的正确方式

**场景**：用户想把数据存到别的位置（如 `D:/skill-data/`）。

**步骤**：
1. 更新 `SKILL.md` frontmatter 的 `data_dir:` 字段
2. 更新各 `.py` 文件中的 `DATA_DIR` 计算逻辑，改为从 `fm["data_dir"]` 读取

**推荐**：未来版本从 `SKILL.md` frontmatter 动态读取 `data_dir:`，不再硬编码计算逻辑。
