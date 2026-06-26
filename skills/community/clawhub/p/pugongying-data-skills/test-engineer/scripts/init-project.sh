#!/bin/bash
# 测试项目初始化脚本
# 创建标准化数据仓库测试项目结构

set -e

PROJECT_DIR=${1:-"./test-project"}
PROJECT_NAME=${2:-"数据仓库测试项目"}

echo "======================================"
echo "初始化测试项目: $PROJECT_NAME"
echo "项目目录: $PROJECT_DIR"
echo "======================================"

# 创建目录结构
mkdir -p "$PROJECT_DIR"/{unit,integration,performance,fixtures,reports}

# 创建 PROJECT.md
cat > "$PROJECT_DIR/PROJECT.md" << 'EOF'
# PROJECT_NAME

> 项目创建时间: $(date +%Y-%m-%d)
> 使用 Skill: test-engineer

---

## 测试清单

### 单元测试

| 测试对象 | 测试类型 | 状态 | 脚本 |
|----------|----------|------|------|
| dim_user | schema + not_null + unique | ⏳ 待开发 | test_dim_user.py |
| dim_product | schema + not_null + unique | ⏳ 待开发 | test_dim_product.py |
| fct_order_items | schema + relationship + custom | ⏳ 待开发 | test_fct_order_items.py |

### 集成测试

| 测试场景 | 描述 | 状态 | 脚本 |
|----------|------|------|------|
| ODS→DWD | 数据完整性验证 | ⏳ 待开发 | test_integration_ods_to_dwd.py |
| DWD→FCT | 转换逻辑验证 | ⏳ 待开发 | test_integration_dwd_to_fct.py |
| FCT→DWS | 汇总对账验证 | ⏳ 待开发 | test_integration_fct_to_dws.py |
| SCD2追踪 | 历史数据验证 | ⏳ 待开发 | test_integration_scd2.py |

### 性能测试

| 测试目标 | 基准要求 | 状态 | 脚本 |
|----------|----------|------|------|
| 销售日报查询 | P50<2s, P95<5s | ⏳ 待开发 | test_perf_daily_report.py |
| ETL执行时长 | <30分钟 | ⏳ 待开发 | test_perf_etl_pipeline.py |

---

## 进度追踪

- [ ] 阶段1: 单元测试开发
  - [ ] schema验证
  - [ ] 数据质量断言
  - [ ] 边界条件测试
- [ ] 阶段2: 集成测试开发
  - [ ] Pipeline测试
  - [ ] 对账验证
  - [ ] SCD2验证
- [ ] 阶段3: 性能测试开发
  - [ ] 查询性能
  - [ ] ETL性能
- [ ] 阶段4: 测试执行
  - [ ] 单元测试通过
  - [ ] 集成测试通过
  - [ ] 性能测试达标

---

## 快速开始

```bash
# 生成单元测试
/unit-test 表: dim_user

# 生成集成测试
/integration-test 场景: ODS到DWD数据完整性

# 生成性能测试
/performance-test 目标: 销售日报查询
```
EOF

sed -i "s/PROJECT_NAME/$PROJECT_NAME/g" "$PROJECT_DIR/PROJECT.md"

# 创建 conftest.py
cat > "$PROJECT_DIR/unit/conftest.py" << 'EOF'
"""
Pytest配置和共享Fixtures
"""
import pytest
import pandas as pd
from datetime import datetime, date

@pytest.fixture(scope="session")
def db_connection():
    """数据库连接Fixture"""
    # 实际项目中配置数据库连接
    import os
    connection_string = os.getenv("TEST_DB_CONNECTION", "default")
    yield connection_string

@pytest.fixture
def sample_date_range():
    """标准测试日期范围"""
    return {
        'start_date': date(2024, 1, 1),
        'end_date': date(2024, 1, 31)
    }

@pytest.fixture
def tolerance():
    """标准对账容差"""
    return {
        'row_count': 0.01,    # 1%
        'amount': 0.001       # 0.1%
    }
EOF

# 创建示例单元测试
cat > "$PROJECT_DIR/unit/test_example.py" << 'EOF'
"""
示例单元测试
展示标准测试模式
"""
import pytest
import pandas as pd

def test_schema_columns_should_exist(sample_table_data):
    """验证必需字段存在"""
    required_columns = ['order_id', 'user_id', 'paid_amount']
    for col in required_columns:
        assert col in sample_table_data.columns, f"Missing column: {col}"

def test_primary_key_should_be_unique(sample_table_data):
    """验证主键唯一性"""
    pk_col = 'order_id'
    duplicates = sample_table_data[pk_col].duplicated().sum()
    assert duplicates == 0, f"Found {duplicates} duplicate primary keys"

def test_amount_should_be_non_negative(sample_table_data):
    """验证金额非负"""
    amount_col = 'paid_amount'
    negative_count = (sample_table_data[amount_col] < 0).sum()
    assert negative_count == 0, f"Found {negative_count} negative amounts"

def test_status_should_be_valid_enum(sample_table_data):
    """验证状态枚举值"""
    valid_status = ['created', 'paid', 'shipped', 'completed', 'cancelled']
    invalid = sample_table_data[~sample_table_data['status'].isin(valid_status)]
    assert len(invalid) == 0, f"Found {len(invalid)} invalid status values"
EOF

# 创建示例集成测试
cat > "$PROJECT_DIR/integration/test_example.py" << 'EOF'
"""
示例集成测试
展示Pipeline测试模式
"""
import pytest

def test_ods_to_dwd_row_count_should_match(db_connection, sample_date_range):
    """验证ODS到DWD行数一致"""
    # 实际测试实现
    # source_count = query("SELECT COUNT(*) FROM ODS.ods_orders WHERE dt = ...")
    # target_count = query("SELECT COUNT(*) FROM DWD.dwd_orders WHERE dt = ...")
    # assert_row_count_match(source_count, target_count)
    pass

def test_dwd_to_dws_amount_reconciliation_should_pass(db_connection, tolerance):
    """验证DWD到DWS金额对账"""
    # 实际测试实现
    # source_amt = query("SELECT SUM(paid_amount) FROM DWD...")
    # target_amt = query("SELECT SUM(gmv) FROM DWS...")
    # assert_amount_reconciliation(source_amt, target_amt, tolerance['amount'])
    pass
EOF

# 创建示例性能测试
cat > "$PROJECT_DIR/performance/test_example.py" << 'EOF'
"""
示例性能测试
展示性能测试模式
"""
import pytest
import time

def test_daily_report_query_should_complete_within_sla(db_connection):
    """验证日报查询在SLA内完成"""
    query = """
    SELECT * FROM ADS.ads_daily_sales_report
    WHERE report_date >= '2024-01-01'
    """

    start = time.time()
    # execute_query(db_connection, query)
    duration = time.time() - start

    assert duration < 5.0, f"Query took {duration:.2f}s, exceeds SLA 5s"
EOF

# 创建测试工具模块
cat > "$PROJECT_DIR/fixtures/assertions.py" << 'EOF'
"""
测试断言工具库
"""

def assert_row_count_match(source_count, target_count, tolerance=0.01):
    """验证行数匹配（在容差范围内）"""
    if source_count == 0:
        assert target_count == 0, "Target should be empty when source is empty"
        return

    diff_rate = abs(source_count - target_count) / source_count
    assert diff_rate <= tolerance, \
        f"Row count mismatch: source={source_count}, target={target_count}, " \
        f"diff_rate={diff_rate:.2%} > tolerance={tolerance:.2%}"

def assert_amount_reconciliation(source_amt, target_amt, tolerance=0.001):
    """验证金额对账"""
    if source_amt == 0:
        assert target_amt == 0, f"Target amount should be 0 when source is 0, got {target_amt}"
        return

    diff_rate = abs(source_amt - target_amt) / source_amt
    assert diff_rate <= tolerance, \
        f"Amount mismatch: source={source_amt}, target={target_amt}, " \
        f"diff_rate={diff_rate:.4%} > tolerance={tolerance:.4%}"

def assert_date_range(df, date_col, expected_start, expected_end):
    """验证日期范围"""
    actual_start = df[date_col].min()
    actual_end = df[date_col].max()

    assert actual_start >= expected_start, \
        f"Start date {actual_start} before expected {expected_start}"
    assert actual_end <= expected_end, \
        f"End date {actual_end} after expected {expected_end}"
EOF

# 创建 requirements.txt
cat > "$PROJECT_DIR/requirements.txt" << 'EOF'
pytest>=7.0.0
pytest-cov>=4.0.0
pandas>=1.5.0
snowflake-connector-python>=3.0.0
pyyaml>=6.0
EOF

# 创建 README.md
cat > "$PROJECT_DIR/README.md" << 'EOF'
# PROJECT_NAME

数据仓库测试项目

## 目录结构

```
.
├── unit/           # 单元测试
├── integration/    # 集成测试
├── performance/    # 性能测试
├── fixtures/       # 测试工具和数据
├── reports/        # 测试报告
├── conftest.py     # Pytest配置
└── requirements.txt # 依赖
```

## 运行测试

```bash
# 安装依赖
pip install -r requirements.txt

# 运行所有测试
pytest

# 运行单元测试
pytest unit/

# 运行集成测试
pytest integration/

# 运行性能测试
pytest performance/

# 生成覆盖率报告
pytest --cov=src --cov-report=html
```

## 测试规范

- 单元测试: 验证单个模型/表
- 集成测试: 验证跨组件数据流
- 性能测试: 验证性能基准

## 使用 Skill

```bash
# 生成单元测试
/unit-test 表: dim_user

# 生成集成测试
/integration-test 场景: DWD到DWS对账

# 生成性能测试
/performance-test 目标: 销售日报查询
```
EOF

sed -i "s/PROJECT_NAME/$PROJECT_NAME/g" "$PROJECT_DIR/README.md"

# 创建 pytest.ini
cat > "$PROJECT_DIR/pytest.ini" << 'EOF'
[pytest]
testpaths = unit integration performance
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    performance: marks tests as performance tests
EOF

echo ""
echo "======================================"
echo "✅ 测试项目初始化完成"
echo "======================================"
echo ""
echo "项目结构:"
find "$PROJECT_DIR" -type f | head -20
echo ""
echo "下一步:"
echo "  1. cd $PROJECT_DIR"
echo "  2. pip install -r requirements.txt"
echo "  3. 使用 /unit-test 或 /integration-test 生成测试"
