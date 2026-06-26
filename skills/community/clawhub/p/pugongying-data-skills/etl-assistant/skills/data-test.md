---
name: data-test
description: |
  ETL数据测试生成器 - 为Pipeline生成单元测试、集成测试、数据质量测试代码。
  当用户需要测试ETL逻辑、验证数据转换、编写自动化测试时触发。
  触发词：生成ETL测试、数据测试代码、Pipeline测试、ETL单元测试。
argument: { description: "ETL代码或测试需求描述", required: true }
agent: general-purpose
allowed-tools: [Read, Grep, Glob, Edit, Write, Bash]
---

# ETL数据测试生成器

为ETL Pipeline生成完整的测试套件，包括单元测试、集成测试和数据质量测试。

## 测试金字塔

```
         ┌─────────────┐
         │   E2E测试    │  ← 完整Pipeline验证
         │  (少量)      │
        ┌┴─────────────┴┐
        │   集成测试     │  ← 组件间交互
        │   (中等)       │
       ┌┴───────────────┴┐
       │    单元测试      │  ← 核心逻辑验证
       │    (大量)        │
       └──────────────────┘
```

## 测试类型

### 1. 单元测试

测试独立的数据转换函数。

### 2. 集成测试

测试数据源、转换、目标之间的交互。

### 3. 数据质量测试

验证数据的完整性、准确性、一致性。

## 输出格式

### 1. pytest单元测试模板

```python
#!/usr/bin/env python3
"""
ETL Pipeline测试: {pipeline_name}
Generated: {timestamp}
"""

import pytest
import pandas as pd
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

from etl.{pipeline_module} import {PipelineClass}


class Test{PipelineClass}:
    """{PipelineClass} 测试类"""

    @pytest.fixture
    def config(self):
        """测试配置"""
        return {
            'source_driver': 'sqlite',
            'source_host': ':memory:',
            'source_database': 'test.db',
            'target_driver': 'sqlite',
            'target_host': ':memory:',
            'target_database': 'test.db',
            'batch_size': 1000
        }

    @pytest.fixture
    def pipeline(self, config):
        """Pipeline实例"""
        return {PipelineClass}(config)

    @pytest.fixture
    def sample_data(self):
        """测试数据"""
        return pd.DataFrame({
            'user_id': [1, 2, 3],
            'username': ['Alice', 'Bob', 'Charlie'],
            'email': ['alice@test.com', 'bob@test.com', 'charlie@test.com'],
            'created_at': [datetime(2024, 1, 1), datetime(2024, 1, 2), datetime(2024, 1, 3)]
        })

    # ═══════════════════════════════════════════════════════════
    # 抽取测试
    # ═══════════════════════════════════════════════════════════

    def test_extract_returns_dataframe(self, pipeline):
        """测试抽取返回DataFrame"""
        # Mock数据库连接
        mock_engine = Mock()
        mock_df = pd.DataFrame({'col1': [1, 2]})

        with patch('pandas.read_sql', return_value=mock_df):
            result = pipeline.extract()

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2

    def test_extract_handles_empty_result(self, pipeline):
        """测试处理空结果"""
        mock_df = pd.DataFrame()

        with patch('pandas.read_sql', return_value=mock_df):
            result = pipeline.extract()

        assert len(result) == 0

    def test_extract_incremental_logic(self, pipeline):
        """测试增量抽取逻辑"""
        pipeline.config['extract_strategy'] = 'incremental'
        pipeline.config['incremental_column'] = 'updated_at'
        pipeline.config['last_extract_value'] = '2024-01-01'

        with patch('pandas.read_sql') as mock_read_sql:
            mock_read_sql.return_value = pd.DataFrame({'id': [1]})
            pipeline.extract()

            # 验证SQL包含WHERE条件
            called_query = mock_read_sql.call_args[0][0]
            assert 'WHERE' in called_query
            assert 'updated_at' in called_query

    # ═══════════════════════════════════════════════════════════
    # 转换测试
    # ═══════════════════════════════════════════════════════════

    def test_transform_cleans_data(self, pipeline, sample_data):
        """测试数据清洗"""
        # 添加脏数据
        dirty_data = sample_data.copy()
        dirty_data.loc[0, 'username'] = '  Alice  '  # 前后空格
        dirty_data.loc[1, 'username'] = None  # NULL值

        result = pipeline.transform(dirty_data)

        # 验证空格被去除
        assert result.loc[0, 'username'] == 'Alice'
        # 验证NULL行被移除
        assert 1 not in result.index

    def test_transform_converts_types(self, pipeline, sample_data):
        """测试类型转换"""
        pipeline.config['type_mapping'] = {
            'user_id': 'str',
            'created_at': 'datetime64[ns]'
        }

        result = pipeline.transform(sample_data)

        assert result['user_id'].dtype == 'object'
        assert pd.api.types.is_datetime64_any_dtype(result['created_at'])

    def test_transform_adds_audit_columns(self, pipeline, sample_data):
        """测试添加审计字段"""
        result = pipeline.transform(sample_data)

        assert 'etl_batch_id' in result.columns
        assert 'etl_extract_time' in result.columns
        assert all(result['etl_batch_id'] == pipeline.batch_id)

    def test_transform_handles_duplicates(self, pipeline, sample_data):
        """测试去重逻辑"""
        pipeline.config['unique_key'] = 'user_id'

        # 添加重复数据
        duplicate = sample_data.iloc[0:1].copy()
        data_with_dup = pd.concat([sample_data, duplicate], ignore_index=True)

        result = pipeline.transform(data_with_dup)

        assert len(result) == len(sample_data)
        assert result['user_id'].nunique() == len(result)

    # ═══════════════════════════════════════════════════════════
    # 加载测试
    # ═══════════════════════════════════════════════════════════

    def test_load_uses_upsert(self, pipeline, sample_data):
        """测试UPSERT加载策略"""
        pipeline.config['load_strategy'] = 'upsert'
        pipeline.config['unique_key'] = 'user_id'

        with patch.object(pipeline, '_upsert_data') as mock_upsert:
            pipeline.load(sample_data)
            mock_upsert.assert_called_once()

    def test_load_uses_append(self, pipeline, sample_data):
        """测试追加加载策略"""
        pipeline.config['load_strategy'] = 'append'

        with patch('pandas.DataFrame.to_sql') as mock_to_sql:
            pipeline.load(sample_data)
            mock_to_sql.assert_called_once()
            assert mock_to_sql.call_args[1]['if_exists'] == 'append'

    # ═══════════════════════════════════════════════════════════
    # 验证测试
    # ═══════════════════════════════════════════════════════════

    def test_validate_checks_row_count(self, pipeline):
        """测试行数验证"""
        pipeline.stats['transformed'] = 100

        with patch('pandas.read_sql', return_value=pd.DataFrame({'cnt': [100]})):
            result = pipeline.validate()
            assert result is True

    def test_validate_fails_on_count_mismatch(self, pipeline):
        """测试行数不匹配时失败"""
        pipeline.stats['transformed'] = 100

        with patch('pandas.read_sql', return_value=pd.DataFrame({'cnt': [90]})):
            with pytest.raises(ValueError, match='Validation failed'):
                pipeline.validate()

    # ═══════════════════════════════════════════════════════════
    # 端到端测试
    # ═══════════════════════════════════════════════════════════

    @patch('{PipelineClass}.extract')
    @patch('{PipelineClass}.transform')
    @patch('{PipelineClass}.load')
    @patch('{PipelineClass}.validate')
    def test_run_executes_full_pipeline(self, mock_validate, mock_load, mock_transform, mock_extract, pipeline):
        """测试完整Pipeline执行"""
        # Mock各阶段
        mock_extract.return_value = pd.DataFrame({'col': [1]})
        mock_transform.return_value = pd.DataFrame({'col': [1]})
        mock_validate.return_value = True

        result = pipeline.run()

        # 验证各阶段被调用
        mock_extract.assert_called_once()
        mock_transform.assert_called_once()
        mock_load.assert_called_once()
        mock_validate.assert_called_once()

        # 验证结果
        assert result['status'] == 'SUCCESS'

    def test_run_handles_errors(self, pipeline):
        """测试错误处理"""
        with patch.object(pipeline, 'extract', side_effect=Exception('Extract failed')):
            with pytest.raises(Exception, match='Extract failed'):
                pipeline.run()

            assert pipeline.stats['status'] == 'FAILED'
            assert 'error' in pipeline.stats


class TestHelperFunctions:
    """辅助函数测试"""

    def test_generate_batch_id(self, pipeline):
        """测试批次ID生成"""
        batch_id = pipeline._generate_batch_id()
        assert len(batch_id) == 15  # YYYYMMDD_HHMMSS
        assert '_' in batch_id

    def test_create_source_engine(self, pipeline):
        """测试源引擎创建"""
        with patch('sqlalchemy.create_engine') as mock_create:
            mock_create.return_value = Mock()
            engine = pipeline._create_source_engine()
            mock_create.assert_called_once()
            assert 'mysql' in mock_create.call_args[0][0] or 'sqlite' in mock_create.call_args[0][0]
```

### 2. 数据质量测试模板

```python
#!/usr/bin/env python3
"""
数据质量测试: {table_name}
Generated: {timestamp}
"""

import pytest
import pandas as pd
from great_expectations.dataset import PandasDataset
from sqlalchemy import create_engine


class TestDataQuality{TableName}:
    """{table_name} 数据质量测试"""

    @pytest.fixture(scope='class')
    def engine(self):
        """数据库连接"""
        return create_engine('{connection_string}')

    @pytest.fixture
    def df(self, engine):
        """加载数据"""
        return pd.read_sql("SELECT * FROM {table_name}", engine)

    @pytest.fixture
    def ge_df(self, df):
        """Great Expectations数据集"""
        return PandasDataset(df)

    # ═══════════════════════════════════════════════════════════
    # 完整性测试
    # ═══════════════════════════════════════════════════════════

    def test_no_empty_table(self, df):
        """测试表不为空"""
        assert len(df) > 0, f"表 {table_name} 为空"

    @pytest.mark.parametrize("column", {required_columns})
    def test_required_columns_not_null(self, ge_df, column):
        """测试必填字段不为空"""
        result = ge_df.expect_column_values_to_not_be_null(column)
        assert result['success'], f"字段 {column} 存在NULL值"

    def test_unique_key_constraint(self, ge_df):
        """测试主键唯一性"""
        result = ge_df.expect_column_values_to_be_unique('{unique_key}')
        assert result['success'], f"主键 {unique_key} 存在重复值"

    # ═══════════════════════════════════════════════════════════
    # 准确性测试
    # ═══════════════════════════════════════════════════════════

    def test_date_range_valid(self, ge_df):
        """测试日期范围有效"""
        result = ge_df.expect_column_values_to_be_between(
            '{date_column}',
            min_value='{min_date}',
            max_value='{max_date}'
        )
        assert result['success']

    @pytest.mark.parametrize("column,expected_type", [
        {type_checks}
    ])
    def test_column_types(self, ge_df, column, expected_type):
        """测试数据类型正确"""
        result = ge_df.expect_column_values_to_be_of_type(column, expected_type)
        assert result['success'], f"字段 {column} 类型不匹配"

    def test_enum_values_valid(self, ge_df):
        """测试枚举值有效"""
        result = ge_df.expect_column_values_to_be_in_set(
            '{enum_column}',
            {enum_values}
        )
        assert result['success']

    # ═══════════════════════════════════════════════════════════
    # 一致性测试
    # ═══════════════════════════════════════════════════════════

    def test_foreign_key_integrity(self, engine):
        """测试外键完整性"""
        orphan_count = pd.read_sql("""
            SELECT COUNT(*) as cnt
            FROM {table_name} t
            LEFT JOIN {parent_table} p ON t.{fk_column} = p.{pk_column}
            WHERE p.{pk_column} IS NULL
        """, engine).iloc[0]['cnt']

        assert orphan_count == 0, f"发现 {orphan_count} 条孤儿记录"

    def test_calculated_fields_accuracy(self, engine):
        """测试计算字段准确性"""
        invalid = pd.read_sql("""
            SELECT COUNT(*) as cnt
            FROM {table_name}
            WHERE {calculated_field} != {expected_calculation}
        """, engine).iloc[0]['cnt']

        assert invalid == 0, f"发现 {invalid} 条计算字段不准确的记录"

    # ═══════════════════════════════════════════════════════════
    # 时效性测试
    # ═══════════════════════════════════════════════════════════

    def test_data_freshness(self, engine):
        """测试数据新鲜度"""
        max_date = pd.read_sql("""
            SELECT MAX({etl_timestamp}) as max_ts
            FROM {table_name}
        """, engine).iloc[0]['max_ts']

        age_hours = (pd.Timestamp.now() - pd.Timestamp(max_date)).total_seconds() / 3600
        assert age_hours < {max_data_age_hours}, f"数据已过期 {age_hours:.1f} 小时"

    # ═══════════════════════════════════════════════════════════
    # 自定义业务规则测试
    # ═══════════════════════════════════════════════════════════

    {custom_tests}
```

### 3. Airflow DAG测试模板

```python
#!/usr/bin/env python3
"""
Airflow DAG测试: {dag_id}
Generated: {timestamp}
"""

import pytest
from datetime import datetime
from airflow.models import DagBag, TaskInstance
from airflow.utils.state import State


class Test{dag_id}:
    """{dag_id} DAG测试"""

    @pytest.fixture(scope='class')
    def dagbag(self):
        """加载DAG"""
        return DagBag(dag_folder='dags/', include_examples=False)

    @pytest.fixture
    def dag(self, dagbag):
        """获取特定DAG"""
        return dagbag.get_dag(dag_id='{dag_id}')

    # ═══════════════════════════════════════════════════════════
    # DAG结构测试
    # ═══════════════════════════════════════════════════════════

    def test_dag_loaded(self, dagbag):
        """测试DAG成功加载"""
        assert dagbag.import_errors == {}
        assert '{dag_id}' in dagbag.dags

    def test_dag_has_correct_tags(self, dag):
        """测试DAG标签正确"""
        assert dag.tags == {expected_tags}

    def test_dag_has_description(self, dag):
        """测试DAG有描述"""
        assert dag.description is not None
        assert len(dag.description) > 0

    def test_dag_schedule_interval(self, dag):
        """测试调度间隔正确"""
        assert str(dag.schedule_interval) == '{expected_schedule}'

    # ═══════════════════════════════════════════════════════════
    # 任务测试
    # ═══════════════════════════════════════════════════════════

    def test_task_count(self, dag):
        """测试任务数量"""
        assert len(dag.tasks) == {expected_task_count}

    @pytest.mark.parametrize("task_id", {task_list})
    def test_task_exists(self, dag, task_id):
        """测试任务存在"""
        assert dag.has_task(task_id)

    def test_dependencies_correct(self, dag):
        """测试依赖关系正确"""
        {dependency_tests}

    # ═══════════════════════════════════════════════════════════
    # 任务执行测试
    # ═══════════════════════════════════════════════════════════

    def test_extract_task_logic(self, dag):
        """测试抽取任务逻辑"""
        task = dag.get_task('extract_{entity}')

        # 创建TaskInstance
        ti = TaskInstance(task, execution_date=datetime(2024, 1, 1))

        # 执行任务
        with pytest.mock.patch('etl.{entity}_etl.{Entity}ETL') as mock_etl:
            mock_instance = mock_etl.return_value
            mock_instance.extract.return_value = {'extract_count': 100}

            result = task.execute(context={'ti': ti, 'ds': '2024-01-01'})

            assert result['extract_count'] == 100

    def test_validate_task_fails_on_error(self, dag):
        """测试验证任务在错误时失败"""
        task = dag.get_task('validate_load')
        ti = TaskInstance(task, execution_date=datetime(2024, 1, 1))

        # 模拟验证失败
        with pytest.raises(Exception):
            task.execute(context={'ti': ti, 'ds': '2024-01-01'})
```

## 测试生成参数

| 参数 | 说明 | 示例 |
|------|------|------|
| test_type | 测试类型 | unit, integration, e2e |
| coverage_level | 覆盖级别 | basic, standard, comprehensive |
| mocking_strategy | Mock策略 | full, partial, none |
| test_framework | 测试框架 | pytest, unittest |

## 当前生成需求

$ARGUMENTS

---

**生成测试时**：
1. 分析被测代码结构
2. 识别关键逻辑和边界条件
3. 设计测试用例（正常/异常/边界）
4. 生成Mock和Fixture
5. 提供测试执行指南
