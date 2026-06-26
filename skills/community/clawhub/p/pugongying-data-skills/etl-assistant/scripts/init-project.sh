#!/bin/bash
# ETL Pipeline项目初始化脚本
# 用法: bash init-project.sh <项目目录> <项目名称>
# 示例: bash init-project.sh ./etl-project "用户数据同步Pipeline"

set -e

PROJECT_DIR="$1"
PROJECT_NAME="${2:-ETL Pipeline Project}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

if [ -z "$PROJECT_DIR" ]; then
    echo "❌ 错误: 请指定项目目录"
    echo "用法: bash init-project.sh <项目目录> [项目名称]"
    echo "示例: bash init-project.sh ./my-etl-project "订单数据同步""
    exit 1
fi

# 创建目录结构
echo "🚀 创建ETL Pipeline项目: $PROJECT_NAME"
echo "📁 项目目录: $PROJECT_DIR"
mkdir -p "$PROJECT_DIR"/{pipelines/{generated,reviewed,production},dags,tests/{unit,integration,data_quality},docs,scripts,config,etl}

# 复制规范文件
cp "$SKILL_DIR/references/etl-standards.md" "$PROJECT_DIR/standards.md"

# 创建 PROJECT.md
cat > "$PROJECT_DIR/PROJECT.md" << 'EOF'
# PROJECT - ETL Pipeline项目中枢

## 项目信息

- **项目名称**: PROJECT_NAME_PLACEHOLDER
- **创建时间**: CREATE_TIME_PLACEHOLDER
- **技术栈**: Python + Airflow + BigQuery
- **调度工具**: Apache Airflow 2.x
- **开发环境**: Docker

## Pipeline清单

| Pipeline名 | 源系统 | 目标系统 | 调度频率 | 状态 | 负责人 |
|-----------|--------|----------|----------|------|--------|
| | | | | 🟡设计 | |
| | | | | 🟡设计 | |
| | | | | 🟡设计 | |

状态说明:
- 🟡 设计: 设计阶段
- 🟡 开发: 开发阶段
- 🟢 测试: 测试中
- 🟢 上线: 已上线
- 🔴 废弃: 已废弃

## 项目结构

```
.
├── PROJECT.md          # 项目中枢（本文件）
├── standards.md        # ETL开发规范
├── README.md           # 项目说明
├── requirements.txt    # Python依赖
├── config/
│   ├── dev.yml         # 开发环境配置
│   ├── staging.yml     # 测试环境配置
│   └── prod.yml        # 生产环境配置
├── pipelines/
│   ├── generated/      # 生成的Pipeline代码
│   ├── reviewed/       # 已审查的代码
│   └── production/     # 生产就绪代码
├── dags/               # Airflow DAG
├── etl/                # ETL模块
│   ├── __init__.py
│   ├── base.py         # 基础ETL类
│   └── utils.py        # 工具函数
├── tests/
│   ├── unit/           # 单元测试
│   ├── integration/    # 集成测试
│   └── data_quality/   # 数据质量测试
├── scripts/            # 部署脚本
└── docs/               # 文档
```

## 待办事项

### Pipeline设计
- [ ] 完成业务需求分析
- [ ] 确定源系统连接方式
- [ ] 设计ETL映射关系
- [ ] 确定调度策略

### Pipeline开发
- [ ] 生成ETL代码
- [ ] 代码审查
- [ ] 生成测试代码
- [ ] 测试执行

### 部署
- [ ] 开发环境部署
- [ ] 测试环境部署
- [ ] 生产环境部署
- [ ] 监控配置

## 快速链接

- [ETL开发规范](./standards.md)
- [pipelines/](./pipelines/) - Pipeline代码目录
- [dags/](./dags/) - Airflow DAG目录
- [tests/](./tests/) - 测试代码目录

## 使用流程

```bash
# 1. 进入项目目录
cd PROJECT_DIR_PLACEHOLDER

# 2. 启动 Claude Code
claude

# 3. 生成ETL代码
/etl-template 生成Python ETL脚本，源系统...目标系统...

# 4. 审查代码
/pipeline-review [ETL代码]

# 5. 生成测试
/data-test [ETL代码]

# 6. 运行测试
pytest tests/ -v
```

## 开发环境

```bash
# 启动Airflow
docker-compose up -d

# 查看日志
docker-compose logs -f scheduler

# 运行测试
pytest tests/unit -v

# 运行特定Pipeline
python -m etl.orders_etl --date 2024-01-01
```
EOF

# 替换占位符
sed -i.bak "s/PROJECT_NAME_PLACEHOLDER/$PROJECT_NAME/g" "$PROJECT_DIR/PROJECT.md"
sed -i.bak "s/CREATE_TIME_PLACEHOLDER/$(date '+%Y-%m-%d')/g" "$PROJECT_DIR/PROJECT.md"
sed -i.bak "s|PROJECT_DIR_PLACEHOLDER|$PROJECT_DIR|g" "$PROJECT_DIR/PROJECT.md"
rm -f "$PROJECT_DIR/PROJECT.md.bak"

# 创建 README.md
cat > "$PROJECT_DIR/README.md" << EOF
# $PROJECT_NAME

ETL Pipeline项目，使用 Claude ETL Assistant Skill 管理。

## 项目结构

\`\`\`
.
├── PROJECT.md          # 项目中枢（Pipeline清单+进度+规范）
├── standards.md        # ETL开发规范
├── README.md           # 本文件
├── requirements.txt    # Python依赖
├── config/             # 配置文件
├── pipelines/          # Pipeline代码
├── dags/               # Airflow DAG
├── etl/                # ETL模块
├── tests/              # 测试代码
├── scripts/            # 部署脚本
└── docs/               # 文档
\`\`\`

## 快速开始

### 1. 模型设计

\`\`\`bash
cd $PROJECT_DIR
claude

# 生成ETL代码
/etl-template 生成Python ETL脚本，源系统...目标系统...
\`\`\`

### 2. 代码审查

\`\`\`bash
# 审查Pipeline代码
/pipeline-review [ETL代码]
\`\`\`

### 3. 生成测试

\`\`\`bash
# 生成测试代码
/data-test [ETL代码]

# 运行测试
pytest tests/ -v
\`\`\`

### 4. 部署DAG

\`\`\`bash
# 复制到Airflow DAG目录
cp dags/* \$AIRFLOW_HOME/dags/

# 测试DAG
airflow dags test my_dag 2024-01-01
\`\`\`

## 开发流程

1. **生成**: /etl-template → 输出ETL代码
2. **审查**: /pipeline-review → 输出审查报告
3. **测试**: /data-test → 输出测试代码
4. **验证**: pytest → 确保测试通过
5. **上线**: airflow → 部署到生产

## 规范

详见 [standards.md](./standards.md)

## 更新日志

### v1.0.0 ($(date '+%Y-%m-%d'))
- 项目初始化
EOF

# 创建 requirements.txt
cat > "$PROJECT_DIR/requirements.txt" << 'EOF'
# ETL Core
pandas>=2.0.0
numpy>=1.24.0
sqlalchemy>=2.0.0

# Database Drivers
psycopg2-binary>=2.9.0
pymysql>=1.1.0

# Cloud
google-cloud-bigquery>=3.0.0
boto3>=1.28.0

# Airflow
apache-airflow>=2.7.0
apache-airflow-providers-google>=10.0.0

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.0
great-expectations>=0.17.0

# Monitoring
prometheus-client>=0.17.0

# Utils
python-dotenv>=1.0.0
pydantic>=2.0.0
pyyaml>=6.0.0
EOF

# 创建基础ETL类
cat > "$PROJECT_DIR/etl/base.py" << 'EOF'
#!/usr/bin/env python3
"""
ETL Pipeline基类
"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, Optional

import pandas as pd

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class BaseETL(ABC):
    """ETL Pipeline基类"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.batch_id = self._generate_batch_id()
        self.stats = {
            'extracted': 0,
            'transformed': 0,
            'loaded': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None
        }

    def _generate_batch_id(self) -> str:
        """生成批次ID"""
        return datetime.now().strftime('%Y%m%d_%H%M%S')

    @abstractmethod
    def extract(self) -> pd.DataFrame:
        """数据抽取"""
        pass

    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """数据转换"""
        pass

    @abstractmethod
    def load(self, df: pd.DataFrame) -> None:
        """数据加载"""
        pass

    def validate(self) -> bool:
        """数据验证（可覆盖）"""
        self.logger.info(f"[{self.batch_id}] Validating data load")
        return True

    def run(self) -> Dict[str, Any]:
        """执行完整ETL流程"""
        try:
            self.stats['start_time'] = datetime.now()
            self.logger.info(f"[{self.batch_id}] Starting ETL pipeline")

            # 1. 抽取
            data = self.extract()

            # 2. 转换
            data = self.transform(data)

            # 3. 加载
            self.load(data)

            # 4. 验证
            self.validate()

            self.stats['end_time'] = datetime.now()
            self.stats['status'] = 'SUCCESS'

            duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
            self.logger.info(f"[{self.batch_id}] ETL completed in {duration}s")

            return self.stats

        except Exception as e:
            self.stats['end_time'] = datetime.now()
            self.stats['status'] = 'FAILED'
            self.stats['error'] = str(e)
            self.logger.error(f"[{self.batch_id}] ETL failed: {str(e)}")
            raise
EOF

# 创建 etl/__init__.py
cat > "$PROJECT_DIR/etl/__init__.py" << 'EOF'
"""
ETL模块
"""

from .base import BaseETL

__all__ = ['BaseETL']
EOF

# 创建 etl/utils.py
cat > "$PROJECT_DIR/etl/utils.py" << 'EOF'
#!/usr/bin/env python3
"""
ETL工具函数
"""

import os
from typing import Dict, Any
import yaml


def load_config(env: str = 'dev') -> Dict[str, Any]:
    """加载配置文件"""
    config_path = f'config/{env}.yml'

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def get_env_or_raise(key: str) -> str:
    """获取环境变量，不存在则报错"""
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Environment variable {key} not set")
    return value


def chunk_list(lst, chunk_size):
    """分批处理列表"""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]
EOF

# 创建示例配置文件
cat > "$PROJECT_DIR/config/dev.yml" << 'EOF'
# 开发环境配置

source:
  driver: mysql+pymysql
  host: localhost
  port: 3306
  database: source_db
  user: ${SOURCE_DB_USER}
  password: ${SOURCE_DB_PASSWORD}

target:
  project: my-project
  dataset: staging
  credentials: ${GOOGLE_APPLICATION_CREDENTIALS}

etl:
  batch_size: 10000
  retry_count: 3
  timeout_seconds: 3600
EOF

# 创建 .gitignore
cat > "$PROJECT_DIR/.gitignore" << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/

# IDEs
.idea/
.vscode/
*.swp
*.swo
*~

# Environment
.env
.env.local
.env.*.local

# Config with secrets
config/prod.yml
config/staging.yml

# Logs
logs/
*.log

# Airflow
airflow.db
airflow.cfg
unittests.cfg

# Test
.pytest_cache/
.coverage
htmlcov/

# Data
data/
*.csv
*.parquet
*.json

# OS
.DS_Store
Thumbs.db
EOF

# 创建测试示例
cat > "$PROJECT_DIR/tests/unit/.gitkeep" << 'EOF'
# Unit tests go here
# Example: test_orders_etl.py
EOF

cat > "$PROJECT_DIR/tests/integration/.gitkeep" << 'EOF'
# Integration tests go here
EOF

cat > "$PROJECT_DIR/tests/data_quality/.gitkeep" << 'EOF'
# Data quality tests go here
EOF

cat > "$PROJECT_DIR/pipelines/generated/.gitkeep" << 'EOF'
# Generated pipeline code goes here
EOF

cat > "$PROJECT_DIR/dags/.gitkeep" << 'EOF'
# Airflow DAGs go here
EOF

cat > "$PROJECT_DIR/docs/.gitkeep" << 'EOF'
# Documentation goes here
EOF

echo ""
echo "✅ 项目创建成功!"
echo ""
echo "📁 项目结构:"
tree -L 3 "$PROJECT_DIR" 2>/dev/null || find "$PROJECT_DIR" -maxdepth 3 -print | sed -e 's;[^/]*/;|____;g;s;____|; |;g'
echo ""
echo "📝 下一步:"
echo "   cd $PROJECT_DIR"
echo "   python -m venv venv"
echo "   source venv/bin/activate  # Windows: venv\Scripts\activate"
echo "   pip install -r requirements.txt"
echo "   claude"
echo "   /etl-template 开始你的第一个Pipeline"
echo ""
