---
name: etl-template
description: |
  ETL代码模板生成器 - 生成Python/SQL/Airflow等ETL代码模板。
  当用户需要开发ETL Pipeline、数据抽取脚本、数据同步任务时触发。
  触发词：生成ETL代码、ETL模板、数据同步脚本、Pipeline代码、Airflow DAG。
argument: { description: "ETL需求描述（源系统、目标系统、转换逻辑等）", required: true }
agent: general-purpose
allowed-tools: [Read, Grep, Glob, Edit, Write, Bash]
---

# ETL代码模板生成器

根据数据源、目标系统和业务需求，生成标准化的ETL代码模板。

## 支持的技术栈

| 类型 | 技术选项 |
|------|----------|
| **抽取工具** | Python (pandas/sqlalchemy), Apache Spark, AWS Glue, Fivetran |
| **转换语言** | Python, SQL (dbt), Spark SQL |
| **加载目标** | PostgreSQL, MySQL, BigQuery, Snowflake, Redshift, Data Lake |
| **调度工具** | Apache Airflow, Prefect, Dagster, cron |
| **容器化** | Docker, Kubernetes |

## 输出格式

### 1. Python ETL脚本

```python
#!/usr/bin/env python3
"""
ETL Pipeline: {source}_to_{target}_{entity}
Schedule: {schedule}
Description: {description}
Generated: {timestamp}
"""

import logging
from datetime import datetime
from typing import Dict, Any, List
import pandas as pd
from sqlalchemy import create_engine

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class {PipelineName}ETL:
    """
    ETL Pipeline for {entity}

    Source: {source_type} ({source_connection})
    Target: {target_type} ({target_connection})
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.batch_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.stats = {
            'extracted': 0,
            'transformed': 0,
            'loaded': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None
        }

        # 初始化连接
        self.source_engine = self._create_source_engine()
        self.target_engine = self._create_target_engine()

    def _create_source_engine(self):
        """创建源数据库连接"""
        connection_string = (
            f"{self.config['source_driver']}://"
            f"{self.config['source_user']}:{self.config['source_password']}@"
            f"{self.config['source_host']}:{self.config['source_port']}/"
            f"{self.config['source_database']}"
        )
        return create_engine(connection_string)

    def _create_target_engine(self):
        """创建目标数据库连接"""
        connection_string = (
            f"{self.config['target_driver']}://"
            f"{self.config['target_user']}:{self.config['target_password']}@"
            f"{self.config['target_host']}:{self.config['target_port']}/"
            f"{self.config['target_database']}"
        )
        return create_engine(connection_string)

    def extract(self) -> pd.DataFrame:
        """
        从源系统抽取数据

        Strategy: {extract_strategy}
        """
        logger.info(f"[{self.batch_id}] Starting extraction from {self.config['source_table']}")
        self.stats['start_time'] = datetime.now()

        try:
            if self.config.get('extract_strategy') == 'incremental':
                # 增量抽取
                query = f"""
                    SELECT {', '.join(self.config['source_columns'])}
                    FROM {self.config['source_table']}
                    WHERE {self.config['incremental_column']} > '{self.config['last_extract_value']}'
                    AND {self.config['incremental_column']} <= '{self.config['current_extract_value']}'
                """
            else:
                # 全量抽取
                query = f"""
                    SELECT {', '.join(self.config['source_columns'])}
                    FROM {self.config['source_table']}
                """

            df = pd.read_sql(query, self.source_engine)
            self.stats['extracted'] = len(df)
            logger.info(f"[{self.batch_id}] Extracted {len(df)} rows")

            return df

        except Exception as e:
            logger.error(f"[{self.batch_id}] Extraction failed: {str(e)}")
            raise

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        数据转换

        Transformations:
        {transformations}
        """
        logger.info(f"[{self.batch_id}] Starting transformation")

        try:
            # 1. 数据清洗
            df = self._clean_data(df)

            # 2. 数据类型转换
            df = self._convert_types(df)

            # 3. 业务转换
            df = self._business_transform(df)

            # 4. 添加审计字段
            df['etl_batch_id'] = self.batch_id
            df['etl_extract_time'] = datetime.now()

            self.stats['transformed'] = len(df)
            logger.info(f"[{self.batch_id}] Transformed {len(df)} rows")

            return df

        except Exception as e:
            logger.error(f"[{self.batch_id}] Transformation failed: {str(e)}")
            raise

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """数据清洗"""
        # 去除空值
        df = df.dropna(subset=self.config.get('required_columns', []))

        # 去除重复
        df = df.drop_duplicates(subset=self.config.get('unique_key'))

        # 字符串trim
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.strip()

        return df

    def _convert_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """数据类型转换"""
        type_mapping = self.config.get('type_mapping', {})
        for col, dtype in type_mapping.items():
            if col in df.columns:
                df[col] = df[col].astype(dtype)
        return df

    def _business_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """业务转换逻辑"""
        # 自定义业务逻辑
        {business_logic}
        return df

    def load(self, df: pd.DataFrame) -> None:
        """
        加载到目标系统

        Strategy: {load_strategy}
        """
        logger.info(f"[{self.batch_id}] Starting load to {self.config['target_table']}")

        try:
            if self.config.get('load_strategy') == 'upsert':
                # UPSERT逻辑
                self._upsert_data(df)
            elif self.config.get('load_strategy') == 'append':
                # 追加模式
                df.to_sql(
                    self.config['target_table'],
                    self.target_engine,
                    if_exists='append',
                    index=False,
                    chunksize=1000
                )
            elif self.config.get('load_strategy') == 'replace':
                # 全量替换
                df.to_sql(
                    self.config['target_table'],
                    self.target_engine,
                    if_exists='replace',
                    index=False
                )

            self.stats['loaded'] = len(df)
            logger.info(f"[{self.batch_id}] Loaded {len(df)} rows")

        except Exception as e:
            logger.error(f"[{self.batch_id}] Load failed: {str(e)}")
            raise

    def _upsert_data(self, df: pd.DataFrame) -> None:
        """执行UPSERT操作"""
        # 临时表方式实现UPSERT
        temp_table = f"temp_{self.config['target_table']}_{self.batch_id}"

        try:
            # 创建临时表
            df.to_sql(temp_table, self.target_engine, if_exists='replace', index=False)

            # 执行MERGE/UPSERT
            merge_sql = f"""
                MERGE INTO {self.config['target_table']} AS target
                USING {temp_table} AS source
                ON target.{self.config['unique_key']} = source.{self.config['unique_key']}
                WHEN MATCHED THEN
                    UPDATE SET
                        {', '.join([f"{col} = source.{col}" for col in df.columns if col != self.config['unique_key']])}
                WHEN NOT MATCHED THEN
                    INSERT ({', '.join(df.columns)})
                    VALUES ({', '.join([f"source.{col}" for col in df.columns])})
            """

            with self.target_engine.connect() as conn:
                conn.execute(merge_sql)

        finally:
            # 清理临时表
            with self.target_engine.connect() as conn:
                conn.execute(f"DROP TABLE IF EXISTS {temp_table}")

    def validate(self) -> bool:
        """数据验证"""
        logger.info(f"[{self.batch_id}] Validating data load")

        # 行数检查
        result = pd.read_sql(
            f"SELECT COUNT(*) as cnt FROM {self.config['target_table']} WHERE etl_batch_id = '{self.batch_id}'",
            self.target_engine
        )

        loaded_count = result.iloc[0]['cnt']

        if loaded_count != self.stats['transformed']:
            raise ValueError(
                f"Validation failed: Expected {self.stats['transformed']} rows, "
                f"but found {loaded_count} rows in target"
            )

        logger.info(f"[{self.batch_id}] Validation passed")
        return True

    def run(self) -> Dict[str, Any]:
        """执行完整ETL流程"""
        try:
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
            logger.info(f"[{self.batch_id}] ETL completed in {duration}s")

            return self.stats

        except Exception as e:
            self.stats['end_time'] = datetime.now()
            self.stats['status'] = 'FAILED'
            self.stats['error'] = str(e)
            logger.error(f"[{self.batch_id}] ETL failed: {str(e)}")
            raise


if __name__ == '__main__':
    # 配置
    config = {
        # 源系统配置
        'source_driver': 'mysql+pymysql',
        'source_host': 'source-host',
        'source_port': 3306,
        'source_user': 'etl_user',
        'source_password': 'password',
        'source_database': 'source_db',
        'source_table': 'users',
        'source_columns': ['user_id', 'username', 'email', 'created_at'],

        # 目标系统配置
        'target_driver': 'postgresql+psycopg2',
        'target_host': 'target-host',
        'target_port': 5432,
        'target_user': 'dw_user',
        'target_password': 'password',
        'target_database': 'data_warehouse',
        'target_table': 'staging.users',

        # ETL配置
        'extract_strategy': 'incremental',  # or 'full'
        'incremental_column': 'updated_at',
        'last_extract_value': '2024-01-01 00:00:00',
        'current_extract_value': '2024-01-02 00:00:00',
        'load_strategy': 'upsert',  # or 'append', 'replace'
        'unique_key': 'user_id',
        'required_columns': ['user_id'],
        'type_mapping': {
            'user_id': 'int64',
            'created_at': 'datetime64[ns]'
        }
    }

    # 执行ETL
    etl = {PipelineName}ETL(config)
    stats = etl.run()
    print(f"ETL Stats: {stats}")
```

### 2. Airflow DAG模板

```python
#!/usr/bin/env python3
"""
Airflow DAG: {dag_id}
Description: {description}
Schedule: {schedule}
Owner: {owner}
Generated: {timestamp}
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.utils.task_group import TaskGroup

# 默认参数
default_args = {
    'owner': '{owner}',
    'depends_on_past': False,
    'email': ['data-team@company.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': {retries},
    'retry_delay': timedelta(minutes={retry_delay}),
    'execution_timeout': timedelta(hours={execution_timeout}),
}

# DAG定义
with DAG(
    dag_id='{dag_id}',
    default_args=default_args,
    description='{description}',
    schedule_interval='{schedule}',
    start_date=datetime({start_year}, {start_month}, {start_day}),
    catchup={catchup},
    tags={tags},
    max_active_runs={max_active_runs},
) as dag:

    # 任务1: 检查上游依赖
    {dependency_check}

    # 任务2: 数据抽取（使用TaskGroup组织相关任务）
    with TaskGroup("extract_group", tooltip="数据抽取任务组") as extract_group:

        def extract_{entity}(**context):
            """从{source}抽取{entity}数据"""
            from etl.{entity}_etl import {Entity}ETL

            execution_date = context['ds']

            config = {
                'execution_date': execution_date,
                'source_table': '{source_table}',
                'extract_strategy': '{extract_strategy}',
                # 其他配置...
            }

            etl = {Entity}ETL(config)
            stats = etl.extract()

            # 推送XCom
            context['task_instance'].xcom_push(
                key='extract_count',
                value=stats['extract_count']
            )

            return stats

        extract_task = PythonOperator(
            task_id='extract_{entity}',
            python_callable=extract_{entity},
            provide_context=True,
        )

    # 任务3: 数据质量检查
    quality_check = PostgresOperator(
        task_id='quality_check',
        postgres_conn_id='{target_connection_id}',
        sql="""
            -- 数据质量检查
            WITH quality_checks AS (
                SELECT
                    COUNT(*) as total_rows,
                    COUNT(CASE WHEN {unique_key} IS NULL THEN 1 END) as null_key_count,
                    COUNT(DISTINCT {unique_key}) as unique_keys,
                    MAX(etl_extract_time) as max_extract_time
                FROM {target_table}
                WHERE etl_batch_id = '{{{{ ds_nodash }}}}'
            )
            SELECT
                total_rows > 0 as has_data,
                null_key_count = 0 as no_null_keys,
                unique_keys = total_rows as all_unique
            FROM quality_checks;
        """,
    )

    # 任务4: 数据转换
    def transform_{entity}(**context):
        """数据转换"""
        from etl.{entity}_etl import {Entity}ETL

        ti = context['task_instance']

        config = {
            'execution_date': context['ds'],
            # 转换配置...
        }

        etl = {Entity}ETL(config)
        # 转换逻辑...

        return {'transformed': True}

    transform_task = PythonOperator(
        task_id='transform_{entity}',
        python_callable=transform_{entity},
        provide_context=True,
    )

    # 任务5: 加载到目标
    load_to_target = PostgresOperator(
        task_id='load_to_target',
        postgres_conn_id='{target_connection_id}',
        sql="""
            -- 从staging加载到warehouse
            -- 实现{load_strategy}逻辑

            {load_sql}
        """,
    )

    # 任务6: 验证加载结果
    def validate_load(**context):
        """验证加载结果"""
        import logging

        logger = logging.getLogger(__name__)
        ti = context['task_instance']

        # 获取上游任务的XCom
        extract_count = ti.xcom_pull(
            task_ids='extract_group.extract_{entity}',
            key='extract_count'
        )

        # 验证逻辑
        logger.info(f"Validation: Extracted {extract_count} rows")

        return {'validated': True}

    validate_task = PythonOperator(
        task_id='validate_load',
        python_callable=validate_load,
        provide_context=True,
    )

    # 定义任务依赖关系
    {dependency_check} >> extract_group >> quality_check >> transform_task >> load_to_target >> validate_task
```

### 3. dbt模型ETL

```sql
-- {model_name}.sql
{{{{
  config(
    materialized='{materialized}',
    {incremental_config}
    unique_key='{unique_key}',
    partition_by={{
      field: '{partition_field}',
      data_type: 'date',
      granularity: '{partition_granularity}'
    }},
    tags=['{entity}', '{load_type}']
  )
}}}}

WITH source AS (
    SELECT *
    FROM {{{{ source('{source_schema}', '{source_table}') }}}}
    {{
    % if is_incremental() %

    WHERE updated_at > (SELECT MAX(updated_at) FROM {{{{ this }}}})

    {{% endif %}}
  }}
),

cleaned AS (
    SELECT
        {unique_key},
        {source_columns},

        -- 数据清洗
        TRIM(username) AS username,
        LOWER(email) AS email,

        -- 审计字段
        CURRENT_TIMESTAMP AS loaded_at,
        '{{{{ invocation_id }}}}' AS dbt_batch_id

    FROM source
    WHERE {unique_key} IS NOT NULL
),

final AS (
    SELECT *
    FROM cleaned
    {{
    % if is_incremental() %}

    -- 增量加载时排除已存在记录
    WHERE {unique_key} NOT IN (
        SELECT {unique_key} FROM {{{{ this }}}}
    )

    {{% endif %}}
}}

SELECT * FROM final
```

## 生成参数

用户提供以下信息以获得最佳模板：

| 参数 | 说明 | 示例 |
|------|------|------|
| source_type | 源系统类型 | MySQL, PostgreSQL, API, Kafka |
| target_type | 目标系统类型 | PostgreSQL, BigQuery, Snowflake |
| entity | 同步实体 | users, orders, products |
| load_type | 加载类型 | full, incremental, upsert |
| schedule | 调度频率 | 0 2 * * *, hourly, daily |
| orchestrator | 调度工具 | Airflow, Prefect, cron |

## 当前生成需求

$ARGUMENTS

---

**生成模板时**：
1. 确认数据源和目标系统的技术栈
2. 确定抽取策略（全量/增量/CDC）
3. 选择合适的技术方案
4. 生成完整的、可运行的代码模板
5. 包含错误处理、日志记录、监控埋点
6. 提供部署和运行指南
