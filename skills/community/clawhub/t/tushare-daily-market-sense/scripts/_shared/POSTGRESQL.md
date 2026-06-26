# CH Skills PostgreSQL 连接契约

本仓库所有需要数据库的 skill 默认使用同一套 PostgreSQL 连接入口：`shared/db_core.py`。不要在单个 skill 里重新发明连接配置、连接池或表存在性检查。

## 快速连接

在仓库根目录验证连接：

```bash
export ALPHA_DB_BACKEND=postgresql
export ALPHA_PG_URL="${ALPHA_PG_URL:-postgresql://alpha_user:alpha_pass@/alpha_data?host=/tmp}"
python3 shared/db_ping.py --alpha-schema
```

如果当前环境没有 Unix socket，改用 TCP：

```bash
export ALPHA_PG_URL="postgresql://alpha_user:alpha_pass@localhost:5432/alpha_data"
python3 shared/db_ping.py --alpha-schema
```

在同步后的 skill 包里验证连接：

```bash
python3 scripts/_shared/db_ping.py --alpha-schema
```

## 环境变量优先级

| 变量 | 作用 | 默认 |
|---|---|---|
| `ALPHA_DB_BACKEND` | `postgresql` 或 `sqlite` | `postgresql` |
| `ALPHA_PG_URL` | CH Skills 标准 PostgreSQL DSN，最高优先级 | 空 |
| `DATABASE_URL` | 通用 Agent / 调度器兼容 fallback | 空 |
| 内置 DSN | 未设置前两者时使用 Unix socket | `postgresql://alpha_user:alpha_pass@/alpha_data?host=/tmp` |
| `ALPHA_PG_CONNECT_TIMEOUT` | 连接超时秒数 | `5` |
| `ALPHA_PG_POOL_MAX` | 单进程连接池上限 | `8` |
| `ALPHA_SQLITE_DIR` | SQLite fallback 目录 | 当前目录 |

`ALPHA_PG_URL` 是唯一推荐写法；`DATABASE_URL` 只是为了兼容某些 Agent 沙箱或 scheduler 已经注入的环境。

## 新 skill 接入方式

脚本只依赖 `db_core`，不要直接依赖 `psycopg2.connect`：

```python
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
BUNDLED_SHARED = SCRIPT_DIR / "_shared"
DEV_SHARED = SCRIPT_DIR.parents[2] / "shared"
sys.path.insert(0, str(BUNDLED_SHARED if BUNDLED_SHARED.exists() else DEV_SHARED))

from db_core import get_connection, table_exists
```

若 skill 会被同步到各 Agent 目录，并且需要数据库，在 `skill-sync.yaml` 的 `shared.bundles` 中把它加入 `skills` 列表，让 `shared/` 被打包到 `scripts/_shared/`。

## 诊断顺序

1. 先跑 `python3 shared/db_ping.py --alpha-schema`，确认是连接问题、依赖问题还是 schema 问题。
2. 如果报 `psycopg2 is required`，安装 `psycopg2-binary`，或临时设置 `ALPHA_DB_BACKEND=sqlite`。
3. 如果 socket DSN 失败，换成 `localhost:5432` TCP DSN。
4. 如果连接成功但缺表，执行 `psql -d alpha_data -f init_alpha_data.sql` 初始化 schema。
5. 不要把 `.env`、真实口令或个人云数据库地址提交进仓库；文档和日志只能输出脱敏 DSN。
