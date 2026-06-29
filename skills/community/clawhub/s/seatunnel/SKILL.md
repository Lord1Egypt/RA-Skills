---
name: seatunnel
description: "Apache SeaTunnel 数据集成工具助手 - 当用户需要配置、调试或生成 SeaTunnel 数据同步作业时使用此技能。支持 100+ 连接器配置、CDC 设置、性能调优和故障排查。"
version: "2.3.13"
author: "WorkBuddy User"
tags: ["data-integration", "etl", "data-pipeline", "cdc", "real-time"]
agent_created: true
---

# Apache SeaTunnel Skill

你是一个 SeaTunnel 专家助手。帮助用户设计、配置、调试和优化 SeaTunnel 数据集成作业。

## 何时使用此技能

当用户提出以下类型的问题时，使用此技能：
- SeaTunnel 作业配置（HOCON 格式）
- 数据源到目标的数据同步
- CDC（变更数据捕获）配置
- 连接器使用和配置
- 性能调优
- 错误排查
- 最佳实践建议

## 核心概念

### SeaTunnel 是什么
Apache SeaTunnel 是一个**多模态、高性能、分布式数据集成工具**，支持：
- 100+ 连接器（MySQL, PostgreSQL, Kafka, Elasticsearch, HDFS 等）
- 多种同步模式：批处理（BATCH）、流式（STREAMING）、CDC
- 多引擎支持：Zeta Engine（轻量级）、Flink、Spark

### 作业配置结构（HOCON 格式）
```hocon
env {
  job.mode = "BATCH"  # 或 "STREAMING"
  job.name = "作业名称"
  parallelism = 4
}

source {
  # 数据源连接器
}

transform {
  # 可选：数据转换
}

sink {
  # 数据目标连接器
}
```

## 常见用例模板

### 1. MySQL 到 PostgreSQL（批处理）
```hocon
env {
  job.mode = "BATCH"
  job.name = "MySQL to PostgreSQL"
}

source {
  Jdbc {
    driver = "com.mysql.cj.jdbc.Driver"
    url = "jdbc:mysql://mysql-host:3306/mydb"
    user = "root"
    password = "password"
    query = "SELECT * FROM users"
  }
}

sink {
  Jdbc {
    driver = "org.postgresql.Driver"
    url = "jdbc:postgresql://pg-host:5432/mydb"
    user = "postgres"
    password = "password"
    table = "users"
    primary_keys = ["id"]
  }
}
```

### 2. MySQL CDC 到 Kafka（流式）
```hocon
env {
  job.mode = "STREAMING"
  job.name = "MySQL CDC to Kafka"
}

source {
  Mysql {
    server_id = 5400
    hostname = "mysql-host"
    port = 3306
    username = "root"
    password = "password"
    database = ["mydb"]
    table = ["users", "orders"]
    startup.mode = "initial"
  }
}

sink {
  Kafka {
    bootstrap.servers = "kafka-host:9092"
    topic = "mysql_cdc"
    format = "canal_json"
  }
}
```

### 3. Kafka 到 Elasticsearch（流式）
```hocon
env {
  job.mode = "STREAMING"
  job.name = "Kafka to Elasticsearch"
  parallelism = 2
}

source {
  Kafka {
    bootstrap.servers = "kafka-host:9092"
    topic = "events"
    format = "json"
    consumer.group = "seatunnel-group"
  }
}

sink {
  Elasticsearch {
    hosts = ["es-host:9200"]
    index = "events"
    username = "elastic"
    password = "password"
  }
}
```

## 连接器快速参考

### Source 连接器
- **关系型数据库**: Jdbc (MySQL, PostgreSQL, Oracle, SQL Server)
- **CDC**: Mysql, PostgreSQL, OceanBase
- **消息队列**: Kafka, Pulsar, RocketMQ
- **NoSQL**: MongoDB, Redis, HBase
- **数据湖**: Hive, Iceberg, Hudi, Paimon
- **搜索引擎**: Elasticsearch, OpenSearch

### Sink 连接器
- 与 Source 对应的写入连接器
- **Console**: 控制台输出（用于测试）

## 配置要点

### Source 通用配置
```hocon
source {
  ConnectorName {
    # 连接信息
    hostname = "host"
    port = 3306
    username = "user"
    password = "pass"
    
    # 数据范围
    database = "db_name"
    table = "table_name"
    
    # 性能调优
    fetch_size = 1000
    split_size = 10000
    
    # Schema 定义
    schema = {
      fields {
        id = "bigint"
        name = "string"
        age = "int"
      }
    }
  }
}
```

### Sink 通用配置
```hocon
sink {
  ConnectorName {
    # 连接信息
    hostname = "host"
    port = 3306
    username = "user"
    password = "pass"
    
    # 目标设置
    database = "db_name"
    table = "table_name"
    primary_keys = ["id"]
    
    # 性能调优
    batch_size = 500
    max_retries = 3
  }
}
```

### 环境变量
```bash
export JAVA_HOME=/path/to/java
export JVM_OPTS="-Xms1G -Xmx4G"
export SEATUNNEL_HOME=/path/to/seatunnel
```

### 运行作业
```bash
# 本地模式（Zeta Engine）
seatunnel.sh -c config/job.conf -e zeta

# Spark 引擎
seatunnel.sh -c config/job.conf -e spark

# Flink 引擎
seatunnel.sh -c config/job.conf -e flink

# 详细日志
seatunnel.sh -c config/job.conf -e zeta -l DEBUG
```

## 故障排除

### 问题1: ClassNotFoundException (JDBC 驱动)
**原因**: 驱动 JAR 不在 classpath
**解决**:
```bash
# 下载驱动并放到 lib 目录
cp mysql-connector-java-8.0.33.jar $SEATUNNEL_HOME/lib/
```

### 问题2: OutOfMemoryError
**原因**: JVM 堆内存不足
**解决**:
```bash
export JVM_OPTS="-Xms2G -Xmx8G"
```

### 问题3: CDC 时 "Table not found"
**原因**: MySQL 未启用 binlog
**解决**:
```sql
-- 检查 binlog 状态
SHOW VARIABLES LIKE 'log_bin';

-- 启用 binlog (my.cnf)
[mysqld]
log_bin = mysql-bin
binlog_format = ROW
server_id = 1
```

### 问题4: 作业性能慢
**解决**: 调整以下参数
```hocon
env {
  parallelism = 8  # 增加并行度
}

source {
  Jdbc {
    fetch_size = 5000      # 增加 fetch 大小
    split_size = 100000     # 增加分片大小
  }
}

sink {
  Jdbc {
    batch_size = 2000      # 增加批量写入大小
  }
}
```

## 性能调优建议

### 批处理作业
- `parallelism`: 根据集群 CPU 核心数设置（通常 2-4 倍核心数）
- `fetch_size`: 1000-5000（根据记录大小调整）
- `batch_size`: 500-2000（根据目标数据库承受能力）
- `split_size`: 100000+（大表并行读取）

### 流式作业
- `checkpoint.interval`: 30000-60000 ms（平衡延迟和容错）
- Kafka `max_poll_records`: 500-1000
- 监控反压（backpressure）

## 最佳实践

1. **总是定义 schema**: 明确指定字段类型，避免自动推断错误
2. **使用 primary_keys**: 确保幂等写入
3. **配置重试**: 网络抖动时自动恢复
4. **监控日志**: `tail -f logs/seatunnel.log`
5. **测试先用 FakeSource**: 验证配置正确性
6. **分批迁移**: 大表先同步少量数据测试

## 测试配置

使用 FakeSource 快速测试配置：
```hocon
env {
  job.mode = "BATCH"
}

source {
  FakeSource {
    row.num = 100
    schema = {
      fields {
        id = "bigint"
        name = "string"
        age = "int"
      }
    }
  }
}

sink {
  Console {
    format = "json"
  }
}
```

## 响应格式

当用户询问 SeaTunnel 相关问题时：

1. **理解需求**: 确认源系统、目标系统、同步模式（批处理/流式/CDC）
2. **提供配置**: 给出完整的 HOCON 配置示例
3. **解释要点**: 说明关键配置项的含义
4. **提醒注意事项**: 驱动、权限、网络等前置条件
5. **性能建议**: 根据数据量给出调优参数

## 资源链接

- [官方文档](https://seatunnel.apache.org/docs/)
- [连接器列表](https://seatunnel.apache.org/docs/2.3.12/connector-v2/overview)
- [GitHub](https://github.com/apache/seatunnel)
- [下载](https://seatunnel.apache.org/download)
- [社区 Slack](https://the-asf.slack.com/archives/C01CB5186TL)

## 注意事项

- SeaTunnel 2.x 使用 HOCON 配置格式（类似 JSON 但更灵活）
- 连接器驱动需要手动下载并放到 `lib/` 目录
- CDC 模式需要源数据库开启 binlog（MySQL）或 replication slot（PostgreSQL）
- 生产环境建议使用 Zeta Engine（轻量级，无需外部集群）
