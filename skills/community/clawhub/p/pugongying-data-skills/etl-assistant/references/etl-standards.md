# ETL Pipeline开发标准与规范

## 目录

1. [ETL架构模式](#etl架构模式)
2. [命名规范](#命名规范)
3. [代码结构规范](#代码结构规范)
4. [数据质量检查点](#数据质量检查点)
5. [错误处理与重试机制](#错误处理与重试机制)
6. [监控与日志规范](#监控与日志规范)

---

## ETL架构模式

### 1. ETL vs ELT

| 特性 | ETL | ELT |
|------|-----|-----|
| **转换位置** | 在加载前进行 | 在目标库中进行 |
| **适用场景** | 传统数仓、复杂转换 | 云数仓、大数据量 |
| **性能** | 依赖ETL服务器 | 利用目标库计算能力 |
| **灵活性** | 较低 | 较高 |
| **成本** | ETL工具许可 | 存储和计算成本 |

**推荐**：云环境使用ELT，传统环境使用ETL。

### 2. 分层架构

```
┌─────────────────────────────────────────────────────────────┐
│                    ETL Pipeline 分层架构                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 1: Source (数据源层)                                  │
│  ├── 业务数据库 (MySQL/PostgreSQL/Oracle)                    │
│  ├── 日志文件 (JSON/CSV/Parquet)                            │
│  ├── API接口                                                 │
│  └── 消息队列 (Kafka/RabbitMQ)                              │
│                                                             │
│  Layer 2: Staging (暂存层)                                   │
│  ├── 原始数据保留 (与源一致)                                  │
│  ├── 轻量清洗 (格式转换、编码处理)                            │
│  └── 增量标识 (CDC/时间戳)                                   │
│                                                             │
│  Layer 3: Integration (整合层)                               │
│  ├── 数据清洗 (去重、缺失值处理)                              │
│  ├── 数据转换 (格式标准化、单位转换)                          │
│  ├── 数据验证 (质量检查、规则验证)                            │
│  └── 数据关联 (轻量Join)                                     │
│                                                             │
│  Layer 4: Warehouse (数仓层)                                 │
│  ├── 维度表 (SCD处理)                                        │
│  ├── 事实表 (代理键、度量计算)                                │
│  └── 汇总表 (预聚合)                                         │
│                                                             │
│  Layer 5: Mart (应用层)                                      │
│  ├── 主题域模型                                              │
│  ├── 报表数据                                                │
│  └── 数据服务                                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3. 增量抽取策略

| 策略 | 适用场景 | 优点 | 缺点 |
|------|----------|------|------|
| **时间戳** | 有update_time字段 | 简单高效 | 删除检测困难 |
| **自增ID** | 只有INSERT的表 | 实现简单 | 无法检测更新 |
| **CDC** | 支持CDC的数据库 | 完整捕获变更 | 配置复杂 |
| **全量比对** | 小表 | 数据一致性高 | 性能差 |
| **触发器** | 需要实时同步 | 实时性好 | 影响源库性能 |

**时间戳策略示例**：
```sql
-- 增量抽取SQL
SELECT * FROM source_table
WHERE updated_at > '{{ last_extract_time }}'
  AND updated_at <= '{{ current_extract_time }}';
```

### 4. Pipeline模式

#### 模式A：顺序执行
```
Extract → Transform → Load → Validate
```
适用：简单ETL，数据量小

#### 模式B：并行处理
```
         ┌─► Transform A ─┐
Extract ─┼─► Transform B ─┼─► Load
         └─► Transform C ─┘
```
适用：多表并行处理，无依赖关系

#### 模式C：分阶段处理
```
Stage 1: Extract to Staging
Stage 2: Staging to Integration
Stage 3: Integration to Warehouse
```
适用：复杂ETL，需要断点续传

---

## 命名规范

### Pipeline命名

```
{source}_{target}_{entity}_{load_type}

示例：
- mysql_dw_users_full        # MySQL到数仓用户表全量
- api_staging_orders_delta   # API到暂存层订单增量
- kafka_integration_events   # Kafka到整合层事件
```

### 任务命名

```
{action}_{entity}_{detail}

示例：
- extract_users_mysql
- transform_user_clean
- load_dim_user_scd2
- validate_user_count
```

### 变量命名

| 类型 | 前缀 | 示例 |
|------|------|------|
| 源连接 | `src_` | `src_mysql_host` |
| 目标连接 | `tgt_` | `tgt_dw_host` |
| 批处理ID | `batch_` | `batch_id` |
| 时间戳 | `ts_` | `ts_extract_start` |
| 计数 | `cnt_` | `cnt_source_rows` |
| 配置 | `cfg_` | `cfg_batch_size` |

---

## 代码结构规范

### Python ETL模板

```python
#!/usr/bin/env python3
"""
ETL Pipeline: {source}_{target}_{entity}
Description: {description}
Author: {author}
Created: {created_date}
"""

import logging
import sys
from datetime import datetime
from typing import Dict, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ETLPipeline:
    """ETL Pipeline 基类"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.batch_id = self._generate_batch_id()
        self.stats = {
            'extract_count': 0,
            'transform_count': 0,
            'load_count': 0,
            'error_count': 0,
            'start_time': None,
            'end_time': None
        }

    def _generate_batch_id(self) -> str:
        """生成批次ID"""
        return datetime.now().strftime('%Y%m%d_%H%M%S')

    def extract(self) -> Any:
        """数据抽取"""
        logger.info(f"[{self.batch_id}] Starting extraction...")
        self.stats['start_time'] = datetime.now()

        try:
            # 实现抽取逻辑
            data = self._do_extract()
            self.stats['extract_count'] = len(data)
            logger.info(f"[{self.batch_id}] Extracted {self.stats['extract_count']} rows")
            return data
        except Exception as e:
            logger.error(f"[{self.batch_id}] Extraction failed: {str(e)}")
            raise

    def _do_extract(self) -> Any:
        """具体抽取逻辑（子类实现）"""
        raise NotImplementedError

    def transform(self, data: Any) -> Any:
        """数据转换"""
        logger.info(f"[{self.batch_id}] Starting transformation...")

        try:
            # 数据清洗
            data = self._clean(data)
            # 数据验证
            data = self._validate(data)
            # 业务转换
            data = self._business_transform(data)

            self.stats['transform_count'] = len(data)
            logger.info(f"[{self.batch_id}] Transformed {self.stats['transform_count']} rows")
            return data
        except Exception as e:
            logger.error(f"[{self.batch_id}] Transformation failed: {str(e)}")
            raise

    def _clean(self, data: Any) -> Any:
        """数据清洗"""
        return data

    def _validate(self, data: Any) -> Any:
        """数据验证"""
        return data

    def _business_transform(self, data: Any) -> Any:
        """业务转换（子类实现）"""
        raise NotImplementedError

    def load(self, data: Any) -> None:
        """数据加载"""
        logger.info(f"[{self.batch_id}] Starting load...")

        try:
            self._do_load(data)
            self.stats['load_count'] = len(data)
            logger.info(f"[{self.batch_id}] Loaded {self.stats['load_count']} rows")
        except Exception as e:
            logger.error(f"[{self.batch_id}] Load failed: {str(e)}")
            raise

    def _do_load(self, data: Any) -> None:
        """具体加载逻辑（子类实现）"""
        raise NotImplementedError

    def run(self) -> Dict[str, Any]:
        """执行完整ETL流程"""
        try:
            # 1. 抽取
            data = self.extract()

            # 2. 转换
            data = self.transform(data)

            # 3. 加载
            self.load(data)

            self.stats['end_time'] = datetime.now()
            self.stats['status'] = 'SUCCESS'

            logger.info(f"[{self.batch_id}] ETL completed successfully")
            return self.stats

        except Exception as e:
            self.stats['end_time'] = datetime.now()
            self.stats['status'] = 'FAILED'
            self.stats['error'] = str(e)
            logger.error(f"[{self.batch_id}] ETL failed: {str(e)}")
            raise


class UserETL(ETLPipeline):
    """用户数据ETL示例"""

    def _do_extract(self) -> Any:
        """从MySQL抽取用户数据"""
        import pymysql

        connection = pymysql.connect(
            host=self.config['src_host'],
            user=self.config['src_user'],
            password=self.config['src_password'],
            database=self.config['src_database']
        )

        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT user_id, username, email, created_at, updated_at
                    FROM users
                    WHERE updated_at > %s
                """
                cursor.execute(sql, (self.config['last_extract_time'],))
                return cursor.fetchall()
        finally:
            connection.close()

    def _business_transform(self, data: Any) -> Any:
        """用户数据业务转换"""
        transformed = []
        for row in data:
            # 示例转换逻辑
            transformed.append({
                'user_id': row[0],
                'username': row[1].strip().lower(),
                'email': row[2].lower() if row[2] else None,
                'created_date': row[3].date() if row[3] else None,
                'etl_batch_id': self.batch_id
            })
        return transformed

    def _do_load(self, data: Any) -> None:
        """加载到数据仓库"""
        import psycopg2

        connection = psycopg2.connect(
            host=self.config['tgt_host'],
            user=self.config['tgt_user'],
            password=self.config['tgt_password'],
            database=self.config['tgt_database']
        )

        try:
            with connection.cursor() as cursor:
                # 使用COPY或UPSERT
                for row in data:
                    cursor.execute("""
                        INSERT INTO staging.users (user_id, username, email, created_date, etl_batch_id)
                        VALUES (%(user_id)s, %(username)s, %(email)s, %(created_date)s, %(etl_batch_id)s)
                        ON CONFLICT (user_id) DO UPDATE SET
                            username = EXCLUDED.username,
                            email = EXCLUDED.email,
                            updated_at = CURRENT_TIMESTAMP
                    """, row)
            connection.commit()
        finally:
            connection.close()


if __name__ == '__main__':
    config = {
        'src_host': 'localhost',
        'src_user': 'etl_user',
        'src_password': 'password',
        'src_database': 'source_db',
        'tgt_host': 'dw-host',
        'tgt_user': 'dw_user',
        'tgt_password': 'password',
        'tgt_database': 'data_warehouse',
        'last_extract_time': '2024-01-01 00:00:00'
    }

    pipeline = UserETL(config)
    stats = pipeline.run()
    print(f"ETL Stats: {stats}")
```

### Airflow DAG模板

```python
#!/usr/bin/env python3
"""
Airflow DAG: {dag_id}
Description: {description}
Schedule: {schedule}
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.sensors.external_task import ExternalTaskSensor

# 默认参数
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email': ['data-team@company.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=2),
}

# DAG定义
with DAG(
    dag_id='etl_mysql_dw_users',
    default_args=default_args,
    description='ETL pipeline for users from MySQL to Data Warehouse',
    schedule_interval='0 2 * * *',  # 每天凌晨2点
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['etl', 'users', 'daily'],
    max_active_runs=1,
) as dag:

    # 任务1: 检查依赖
    check_dependencies = ExternalTaskSensor(
        task_id='check_dependencies',
        external_dag_id='upstream_dag',
        external_task_id='upstream_task',
        timeout=3600,
        mode='reschedule',
    )

    # 任务2: 抽取数据
    def extract_data(**context):
        """抽取数据"""
        from etl.user_etl import UserETL

        config = {
            'execution_date': context['ds'],
            # 其他配置...
        }

        pipeline = UserETL(config)
        stats = pipeline.extract()

        # 推送XCom供下游使用
        context['task_instance'].xcom_push(key='extract_count', value=stats['extract_count'])
        return stats

    extract = PythonOperator(
        task_id='extract_users',
        python_callable=extract_data,
        provide_context=True,
    )

    # 任务3: 数据质量检查
    data_quality_check = PostgresOperator(
        task_id='data_quality_check',
        postgres_conn_id='dw_connection',
        sql="""
            -- 检查数据质量
            SELECT
                COUNT(*) as total_rows,
                COUNT(CASE WHEN user_id IS NULL THEN 1 END) as null_user_id,
                COUNT(CASE WHEN email IS NULL THEN 1 END) as null_email
            FROM staging.users
            WHERE etl_batch_id = '{{ ds_nodash }}';
        """,
    )

    # 任务4: 加载到目标表
    load_to_warehouse = PostgresOperator(
        task_id='load_to_warehouse',
        postgres_conn_id='dw_connection',
        sql="""
            -- SCD Type 2处理
            INSERT INTO warehouse.dim_users (
                user_id, username, email, user_level,
                valid_from, valid_to, is_current
            )
            SELECT
                s.user_id,
                s.username,
                s.email,
                s.user_level,
                CURRENT_DATE as valid_from,
                '9999-12-31'::date as valid_to,
                TRUE as is_current
            FROM staging.users s
            LEFT JOIN warehouse.dim_users d
                ON s.user_id = d.user_id AND d.is_current = TRUE
            WHERE s.etl_batch_id = '{{ ds_nodash }}'
              AND (d.user_sk IS NULL OR
                   (s.username != d.username OR s.user_level != d.user_level));

            -- 关闭旧版本
            UPDATE warehouse.dim_users
            SET valid_to = CURRENT_DATE - 1,
                is_current = FALSE
            WHERE user_id IN (
                SELECT user_id FROM staging.users
                WHERE etl_batch_id = '{{ ds_nodash }}'
            )
            AND is_current = TRUE
            AND valid_from < CURRENT_DATE;
        """,
    )

    # 任务5: 验证加载结果
    def validate_load(**context):
        """验证加载结果"""
        ti = context['task_instance']
        extract_count = ti.xcom_pull(task_ids='extract_users', key='extract_count')

        # 验证逻辑...
        print(f"Extracted: {extract_count}, Loaded successfully")
        return True

    validate = PythonOperator(
        task_id='validate_load',
        python_callable=validate_load,
        provide_context=True,
    )

    # 定义依赖关系
    check_dependencies >> extract >> data_quality_check >> load_to_warehouse >> validate
```

---

## 数据质量检查点

### 检查点位置

```
Extract ──► [检查点1: 源数据质量] ──► Transform ──► [检查点2: 转换后质量] ──► Load ──► [检查点3: 目标数据质量]
```

### 检查点1：源数据质量

```python
def check_source_quality(data):
    """源数据质量检查"""
    checks = {
        'row_count': len(data) > 0,
        'required_fields': all(
            field in data[0] for field in ['id', 'created_at']
        ),
        'no_duplicates': len(data) == len(set(d['id'] for d in data)),
        'data_freshness': max(d['updated_at'] for d in data) > datetime.now() - timedelta(days=1)
    }

    failed_checks = [k for k, v in checks.items() if not v]
    if failed_checks:
        raise QualityCheckError(f"Source quality checks failed: {failed_checks}")

    return True
```

### 检查点2：转换后质量

```python
def check_transform_quality(data):
    """转换后数据质量检查"""
    checks = {
        'no_null_ids': all(d.get('id') is not None for d in data),
        'valid_dates': all(
            isinstance(d.get('created_at'), datetime) for d in data
        ),
        'reasonable_counts': 0 < len(data) < 1000000,
    }

    return all(checks.values())
```

### 检查点3：目标数据质量

```sql
-- 加载后质量验证
WITH checks AS (
    SELECT
        COUNT(*) as total_rows,
        COUNT(CASE WHEN user_id IS NULL THEN 1 END) as null_id_count,
        COUNT(DISTINCT user_id) as unique_ids,
        MAX(loaded_at) as max_loaded_at
    FROM target_table
    WHERE batch_id = '{{ batch_id }}'
)
SELECT
    total_rows > 0 as has_data,
    null_id_count = 0 as no_null_ids,
    unique_ids = total_rows as all_unique,
    max_loaded_at > NOW() - INTERVAL '1 hour' as is_fresh
FROM checks;
```

---

## 错误处理与重试机制

### 错误分类

| 错误类型 | 处理方式 | 重试策略 |
|----------|----------|----------|
| 网络超时 | 自动重试 | 指数退避，最多3次 |
| 源数据错误 | 记录并跳过 | 不重试，告警通知 |
| 转换错误 | 记录错误行 | 不重试，人工介入 |
| 目标库错误 | 自动重试 | 固定间隔，最多5次 |
| 内存不足 | 分批处理 | 调整批次大小 |

### 重试装饰器

```python
import time
from functools import wraps
from typing import Callable

def retry(max_attempts=3, delay=5, backoff=2, exceptions=(Exception,)):
    """重试装饰器"""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            current_delay = delay

            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        raise

                    logger.warning(
                        f"Attempt {attempt} failed: {str(e)}. "
                        f"Retrying in {current_delay}s..."
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff
                    attempt += 1

            return None
        return wrapper
    return decorator


class DataExtractionError(Exception):
    """数据抽取错误"""
    pass


class DataTransformationError(Exception):
    """数据转换错误"""
    pass


class DataLoadError(Exception):
    """数据加载错误"""
    pass


class QualityCheckError(Exception):
    """数据质量检查错误"""
    pass
```

---

## 监控与日志规范

### 日志级别使用

| 级别 | 使用场景 | 示例 |
|------|----------|------|
| DEBUG | 详细信息 | 每行数据处理记录 |
| INFO | 正常流程 | 任务开始/结束 |
| WARNING | 警告信息 | 数据质量异常 |
| ERROR | 错误信息 | 任务失败 |
| CRITICAL | 严重错误 | 系统级错误 |

### 结构化日志

```python
import json
import logging

class StructuredLogFormatter(logging.Formatter):
    """结构化日志格式化"""

    def format(self, record):
        log_data = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'batch_id': getattr(record, 'batch_id', None),
            'pipeline': getattr(record, 'pipeline', None),
            'task': getattr(record, 'task', None),
            'duration_ms': getattr(record, 'duration_ms', None),
        }

        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


# 使用示例
logger.info(
    "ETL task completed",
    extra={
        'batch_id': '20240317_120000',
        'pipeline': 'user_etl',
        'task': 'extract',
        'duration_ms': 15000,
    }
)
```

### 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| etl_duration_seconds | ETL执行时间 | > 1小时 |
| etl_records_processed | 处理记录数 | 与预期偏差 > 20% |
| etl_error_count | 错误数 | > 0 |
| etl_retry_count | 重试次数 | > 3 |
| data_quality_score | 数据质量分 | < 95% |
| source_freshness_minutes | 源数据新鲜度 | > 30分钟 |

---

## 参考资料

- [Apache Airflow文档](https://airflow.apache.org/docs/)
- [dbt文档](https://docs.getdbt.com/)
- [The Data Warehouse ETL Toolkit]
- [Kimball dimensional modeling techniques]
