# ByteHouse CDW notes

这份文档承接历史 `flink-template-bytehouse-cdw` 中的“参数说明/误区说明”，供 `flink-sql/assets/bytehouse-cdw.md` 的模板配套参考。

## 连接方式与鉴权

历史模板默认采用“IAM 用户 + Gateway 连接”口径：

- IAM 用户：来自火山引擎 IAM，通常也可访问控制台
- 数据库用户：ByteHouse 内部数据库级用户，只用于连接驱动/工具

若使用数据库用户，请按官方文档补齐所需连接信息。

## 依赖准备

使用 Flink SQL 方式时，需要安装与 Flink 版本匹配的 ByteHouse CDW SQL connector jar。

历史说明中的 Maven 信息：

- `groupId`: `com.bytedance.bytehouse`
- `artifactId`: `flink-sql-connector-bytehouse-cdw_${scala.version}`
- `version`: `${flink-sql-connector-bytehouse-cdw.version}`
- repository: `https://artifact.bytedance.com/repository/releases`

说明：`${scala.version}` 需与 Flink 发行版的 Scala 版本匹配。

## 常用参数说明

- `connector`: 必须使用 `bytehouse-cdw`
- `jdbc.enable-gateway-connection`: 是否启用 gateway 连接
- `bytehouse.gateway.region`: gateway 区域标识
- `bytehouse.gateway.host`: gateway 域名
- `bytehouse.gateway.port`: gateway 端口
- `bytehouse.gateway.api-token`: API key / token
- `bytehouse.gateway.virtual-warehouse`: 计算组 ID
- `database`: ByteHouse 数据库名
- `table-name`: ByteHouse 表名

## 常见误区

- 不要写成 `connector = bytehouse`
- 不要直接用 `url = jdbc:bytehouse://...` 直连 JDBC 口径替代 gateway 参数集
- 不要臆造 `scan.partition.*` 之类读取并行参数作为 CDW connector 的必选项

## 参考

- 官方文档链接汇总：`references/connectors.md`

