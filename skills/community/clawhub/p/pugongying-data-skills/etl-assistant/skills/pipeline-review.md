---
name: pipeline-review
description: |
  ETL Pipeline代码审查器 - 审查Python ETL脚本、Airflow DAG、数据Pipeline代码。
  当用户需要审查ETL代码质量、发现潜在问题、优化Pipeline性能时触发。
  触发词：审查ETL代码、Pipeline审查、ETL代码评审、Airflow DAG审查。
argument: { description: "ETL代码内容（Python脚本、Airflow DAG、SQL等）", required: true }
agent: Explore
allowed-tools: [Read, Grep, Glob]
---

# ETL Pipeline代码审查器

对ETL Pipeline代码进行全面审查，识别性能问题、可靠性风险、安全漏洞和可维护性问题。

## 审查维度

### 🔴 性能问题

| 检查项 | 风险等级 | 说明 |
|--------|----------|------|
| 内存泄漏 | 高 | 大数据集全量加载到内存 |
| 重复查询 | 高 | 循环中执行数据库查询 |
| 缺少索引 | 高 | 大表JOIN缺少索引 |
| 全表扫描 | 中 | 没有WHERE条件的SELECT |
| 大事务 | 中 | 单事务处理过多数据 |
| 连接池耗尽 | 高 | 未正确释放连接 |

### 🟡 可靠性问题

| 检查项 | 风险等级 | 说明 |
|--------|----------|------|
| 无错误处理 | 高 | 缺少try-except块 |
| 幂等性缺失 | 高 | 重跑会产生重复数据 |
| 无超时控制 | 中 | 网络请求无超时设置 |
| 无重试机制 | 中 | 临时失败无法自动恢复 |
| 硬编码配置 | 中 | 敏感信息直接写死在代码中 |

### 🟠 数据质量问题

| 检查项 | 风险等级 | 说明 |
|--------|----------|------|
| 无数据验证 | 高 | 缺少行数/值域检查 |
| 类型转换风险 | 中 | 强制类型转换可能失败 |
| NULL处理不当 | 中 | 未处理NULL值 |
| 时区问题 | 中 | 时间字段缺少时区处理 |

### 🟢 可维护性问题

| 检查项 | 风险等级 | 说明 |
|--------|----------|------|
| 缺少日志 | 低 | 关键步骤无日志记录 |
| 无注释 | 低 | 复杂逻辑无说明 |
| 命名不规范 | 低 | 变量/函数命名不清晰 |
| 代码重复 | 低 | 重复代码块未抽象 |

## Python ETL代码审查清单

```python
# ✅ 推荐的代码结构
class DataPipeline:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.batch_id = self._generate_batch_id()
        self.logger = self._setup_logger()
        self.stats = {}

    def extract(self) -> Iterator[pd.DataFrame]:
        """分批抽取，避免内存问题"""
        for chunk in pd.read_sql(query, engine, chunksize=10000):
            yield chunk

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """数据转换，包含验证"""
        df = self._clean(df)
        df = self._validate(df)
        return df

    def load(self, df: pd.DataFrame) -> None:
        """批量加载，带UPSERT"""
        df.to_sql(table, engine, if_exists='append', chunksize=1000)

    def run(self) -> Dict[str, Any]:
        """主流程，带错误处理"""
        try:
            for chunk in self.extract():
                transformed = self.transform(chunk)
                self.load(transformed)
            return {'status': 'SUCCESS', 'stats': self.stats}
        except Exception as e:
            self.logger.error(f"Pipeline failed: {e}")
            raise
```

### 常见反模式

```python
# ❌ 反模式1: 内存问题
df = pd.read_sql("SELECT * FROM huge_table", engine)  # 加载全表

# ✅ 正确做法
for chunk in pd.read_sql(query, engine, chunksize=10000):
    process(chunk)

# ❌ 反模式2: 连接泄漏
conn = create_connection()
result = conn.execute(query)  # 连接未关闭

# ✅ 正确做法
with create_connection() as conn:
    result = conn.execute(query)

# ❌ 反模式3: 无错误处理
data = extract()
transformed = transform(data)
load(transformed)

# ✅ 正确做法
try:
    data = extract()
    transformed = transform(data)
    load(transformed)
except DataExtractionError as e:
    logger.error(f"Extract failed: {e}")
    raise
except DataTransformationError as e:
    logger.error(f"Transform failed: {e}")
    raise

# ❌ 反模式4: 硬编码
DB_PASSWORD = "mysecret123"

# ✅ 正确做法
DB_PASSWORD = os.getenv("DB_PASSWORD")
if not DB_PASSWORD:
    raise ValueError("DB_PASSWORD environment variable not set")

# ❌ 反模式5: SQL注入风险
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ 正确做法
query = "SELECT * FROM users WHERE id = %(user_id)s"
conn.execute(query, {"user_id": user_id})

# ❌ 反模式6: 非幂等
INSERT INTO target SELECT * FROM source

# ✅ 正确做法（UPSERT）
INSERT INTO target
SELECT * FROM source
ON CONFLICT (id) DO UPDATE SET ...
```

## Airflow DAG审查清单

### DAG结构审查

```python
# ✅ 推荐的DAG结构
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

# 默认参数
default_args = {
    'owner': 'data-team',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=2),  # 超时控制
    'email_on_failure': True,
}

with DAG(
    dag_id='etl_example',
    default_args=default_args,
    schedule_interval='0 2 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,  # 防止历史重跑
    max_active_runs=1,  # 限制并发
    tags=['etl', 'daily'],
) as dag:

    # 使用TaskGroup组织相关任务
    with TaskGroup("extract_group") as extract_group:
        extract_a = PythonOperator(task_id='extract_a', python_callable=extract_a)
        extract_b = PythonOperator(task_id='extract_b', python_callable=extract_b)

    # 依赖关系清晰
    extract_group >> transform >> load >> validate
```

### 常见DAG问题

```python
# ❌ 问题1: 动态DAG生成导致性能问题
for i in range(1000):
    with DAG(f'dag_{i}', ...)  # 过多DAG

# ❌ 问题2: 顶层代码执行
data = load_data()  # DAG解析时执行

def my_task():
    return data

# ✅ 正确做法
def my_task():
    data = load_data()  # 任务执行时才加载
    return data

# ❌ 问题3: 缺少重试和超时
task = PythonOperator(
    task_id='my_task',
    python_callable=my_func,
    # 没有retries和execution_timeout
)

# ❌ 问题4: XCom滥用（大数据）
def extract():
    df = pd.read_sql(query, engine)
    return df.to_json()  # 大DataFrame放入XCom

# ✅ 正确做法
def extract():
    df = pd.read_sql(query, engine)
    df.to_parquet('/tmp/data.parquet')  # 写入文件
    return '/tmp/data.parquet'  # 只返回路径
```

## 输出格式

### 审查报告结构

```markdown
# ETL Pipeline代码审查报告

## 基本信息

- **审查对象**: {pipeline_name}
- **代码类型**: Python ETL / Airflow DAG / SQL
- **审查时间**: {timestamp}
- **风险等级**: 🔴 高风险 / 🟡 中风险 / 🟢 低风险

## 问题汇总

| 序号 | 问题类型 | 风险等级 | 位置 | 问题描述 |
|------|----------|----------|------|----------|
| 1 | 性能 | 🔴 | extract() | 全表加载可能导致内存溢出 |
| 2 | 可靠性 | 🔴 | load() | 缺少幂等性处理，重跑会重复 |
| 3 | 安全 | 🟡 | __init__ | 硬编码数据库密码 |

## 详细问题分析

### 问题1: 内存泄漏风险 [🔴 高风险]

**位置**: `extract()` 方法第23行

**问题代码**:
```python
df = pd.read_sql("SELECT * FROM orders", engine)
```

**风险说明**:
- 如果orders表数据量达到百万级，将消耗大量内存
- 可能导致OOM Killer终止进程

**修复建议**:
```python
# 分批读取
for chunk in pd.read_sql(query, engine, chunksize=10000):
    yield chunk
```

### 问题2: 缺少幂等性处理 [🔴 高风险]

**位置**: `load()` 方法第45行

**问题代码**:
```python
df.to_sql('target_table', engine, if_exists='append')
```

**风险说明**:
- DAG失败后重跑会产生重复数据
- 数据一致性无法保证

**修复建议**:
```python
# 使用UPSERT模式
from sqlalchemy.dialects.postgresql import insert

# 或使用临时表+MERGE
temp_table = f"temp_{batch_id}"
df.to_sql(temp_table, engine, if_exists='replace')
# 执行MERGE语句
```

## 优化建议

### 性能优化

1. **使用批量操作**: 将单条INSERT改为批量
2. **添加索引**: 在JOIN条件和WHERE字段上添加索引
3. **并行处理**: 使用多线程/多进程处理独立任务

### 可靠性优化

1. **添加重试机制**: 对网络请求添加指数退避重试
2. **数据验证**: 在关键步骤添加行数检查
3. **监控埋点**: 发送指标到Prometheus/StatsD

## 评分

| 维度 | 得分 | 权重 | 加权得分 |
|------|------|------|----------|
| 性能 | 65 | 30% | 19.5 |
| 可靠性 | 50 | 30% | 15.0 |
| 安全性 | 70 | 20% | 14.0 |
| 可维护性 | 80 | 20% | 16.0 |
| **总分** | - | 100% | **64.5** |

## 修复优先级

1. 🔴 **立即修复**: 内存泄漏、非幂等处理
2. 🟡 **本周修复**: 硬编码配置、缺少超时
3. 🟢 **下次迭代**: 日志完善、注释补充
```

## 当前审查需求

$ARGUMENTS

---

**审查流程**：
1. 分析代码结构和设计模式
2. 识别性能瓶颈和风险点
3. 检查错误处理和可靠性
4. 评估安全性和可维护性
5. 生成详细审查报告和修复建议
