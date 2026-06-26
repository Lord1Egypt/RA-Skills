# 数据仓库测试规范

## 测试金字塔

```
                    ┌─────────┐
                    │  E2E测试 │  ← 端到端验证 (5%)
                   ┌┴─────────┴┐
                   │ 集成测试  │  ← Pipeline验证 (20%)
                  ┌┴───────────┴┐
                  │   单元测试   │  ← 模型验证 (35%)
                 ┌┴─────────────┴┐
                 │   数据质量     │  ← GE规则 (40%)
                 └───────────────┘
```

## 命名规范

### 文件命名
```
单元测试: test_{layer}_{table_name}.py
集成测试: test_integration_{scenario}.py
性能测试: test_perf_{target}.py
Fixture: conftest.py, fixtures/{name}.py

示例:
- test_fct_order_items.py
- test_integration_dwd_to_dws.py
- test_perf_daily_report_query.py
```

### 测试函数命名
```python
# 格式: test_{scenario}_{expected_behavior}
def test_primary_key_should_be_unique():
def test_paid_amount_calculation_should_be_correct():
def test_scd2_should_track_user_level_changes():
def test_gmv_reconciliation_should_match_within_tolerance():
```

## 断言规范

### 基础断言
```python
# 相等断言
assert actual == expected, f"Expected {expected}, got {actual}"

# 非空断言
assert value is not None, "Value should not be None"

# 范围断言
assert 0 <= value <= 100, f"Value {value} out of range [0, 100]"
```

### 数据断言
```python
# 行数匹配
def assert_row_count_match(source_count, target_count, tolerance=0.01):
    diff_rate = abs(source_count - target_count) / source_count
    assert diff_rate <= tolerance, \
        f"Row count mismatch: diff_rate={diff_rate:.2%} > tolerance={tolerance:.2%}"

# 金额对账
def assert_amount_reconciliation(source_amt, target_amt, tolerance=0.001):
    if source_amt == 0:
        assert target_amt == 0, f"Target amount should be 0 when source is 0"
    else:
        diff_rate = abs(source_amt - target_amt) / source_amt
        assert diff_rate <= tolerance, \
            f"Amount mismatch: source={source_amt}, target={target_amt}, diff={diff_rate:.4%}"

# 时间范围
def assert_date_range(df, date_col, expected_start, expected_end):
    actual_start = df[date_col].min()
    actual_end = df[date_col].max()
    assert actual_start >= expected_start, \
        f"Start date {actual_start} before expected {expected_start}"
    assert actual_end <= expected_end, \
        f"End date {actual_end} after expected {expected_end}"
```

## 测试数据规范

### Fixture设计
```python
# conftest.py
import pytest
import pandas as pd
from datetime import datetime, date

@pytest.fixture(scope="session")
def test_db_connection():
    """测试数据库连接"""
    conn = create_snowflake_connection(
        user="TEST_USER",
        database="TEST_DB",
        schema="TEST_SCHEMA"
    )
    yield conn
    conn.close()

@pytest.fixture
def sample_orders():
    """标准测试订单数据"""
    return pd.DataFrame({
        'order_id': [1, 2, 3, 4, 5],
        'user_id': [101, 102, 103, 104, 105],
        'total_amount': [100.0, 200.0, 300.0, 0.0, 500.0],
        'paid_amount': [90.0, 180.0, 270.0, 0.0, 450.0],
        'discount_amount': [10.0, 20.0, 30.0, 0.0, 50.0],
        'status': ['paid', 'completed', 'shipped', 'cancelled', 'created'],
        'created_at': pd.to_datetime(['2024-01-15'] * 5),
        'dt': ['2024-01-15'] * 5
    })

@pytest.fixture
def sample_dim_user():
    """标准测试用户维度数据"""
    return pd.DataFrame({
        'user_sk': [1, 2, 3, 4, 5],
        'user_nk': [101, 102, 103, 104, 105],
        'user_level': ['普通', 'VIP', '普通', 'SVIP', 'VIP'],
        'city': ['北京', '上海', '广州', '深圳', '杭州'],
        'effective_date': [date(2024, 1, 1)] * 5,
        'expiry_date': [date(9999, 12, 31)] * 5,
        'is_current': [True] * 5
    })
```

### 数据隔离
```python
# 每个测试前清理数据
@pytest.fixture(autouse=True)
def clean_test_data(test_db_connection):
    """自动清理测试数据"""
    yield
    # 测试后清理
    test_db_connection.execute("DELETE FROM TEST_SCHEMA.fct_order_items WHERE is_test = TRUE")
    test_db_connection.commit()
```

## 覆盖率标准

| 层级 | 覆盖要求 | 测量指标 |
|------|----------|----------|
| 数据质量 | 100% | GE规则执行率 |
| 单元测试 | ≥80% | 模型/字段覆盖率 |
| 集成测试 | ≥60% | Pipeline覆盖率 |
| E2E测试 | ≥40% | 核心场景覆盖率 |

## 性能基准

### 查询性能
| 查询类型 | P50 | P95 | P99 |
|----------|-----|-----|-----|
| 简单查询 | <1s | <2s | <3s |
| 聚合查询 | <2s | <5s | <10s |
| 复杂JOIN | <3s | <8s | <15s |
| 全表扫描 | <5s | <15s | <30s |

### ETL性能
| Pipeline | 目标时长 | 容忍上限 |
|----------|----------|----------|
| ODS→DWD | <15分钟 | <30分钟 |
| DWD→FCT | <10分钟 | <20分钟 |
| FCT→DWS | <20分钟 | <40分钟 |
| DWS→ADS | <5分钟 | <10分钟 |

## 测试环境规范

### 环境隔离
```
PROD    - 生产环境 (禁止测试)
STAGING - 预发布环境 (集成测试)
TEST    - 测试环境 (单元/性能测试)
DEV     - 开发环境 (开发调试)
```

### 数据规模
| 环境 | 数据量 | 说明 |
|------|--------|------|
| DEV | 1% | 抽样数据 |
| TEST | 10% | 最近一个月 |
| STAGING | 100% | 完整数据 |

## 测试报告规范

### 报告内容
```yaml
测试报告:
  基本信息:
    - 测试时间
    - 执行环境
    - 代码版本

  统计摘要:
    - 总用例数
    - 通过数/失败数/跳过数
    - 成功率
    - 执行时长

  详细结果:
    - 失败用例详情
    - 错误日志
    - 堆栈跟踪

  性能指标:
    - 查询耗时
    - 资源使用
    - 对比基准
```

### 失败分类
```
🔴 严重 (Blocker)
   - 数据丢失
   - 计算错误
   - 系统崩溃

🟠 高 (Critical)
   - 性能严重下降
   - 数据不一致 > 0.1%
   - 核心功能失败

🟡 中 (Major)
   - 边界条件失败
   - 非核心功能问题

🟢 低 (Minor)
   - 警告信息
   - 轻微性能波动
```

## CI/CD集成

### 测试阶段
```yaml
stages:
  - data_quality    # GE规则检查
  - unit_test       # 单元测试
  - integration_test # 集成测试 (每日)
  - performance_test # 性能测试 (发布前)
  - e2e_test        # 端到端测试 (发布前)
```

### 触发条件
```yaml
单元测试:
  - 每次代码提交
  - 模型变更时

集成测试:
  - 每日定时
  - ETL变更时

性能测试:
  - 每周定时
  - 发布前
```
