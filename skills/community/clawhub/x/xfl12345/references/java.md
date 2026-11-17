---
name: java
description: Java 编码规范。编写任何 Java 源码时都应触发。
---

# Java

## Coding Practices

### 通用约定

- 除非有 className 冲突，业务代码和 Javadoc 都禁止使用全限定名，一律 `import`
- 如果项目使用了 lombok 则所有 java record 带 lombok `@Builder`
- record 组件的说明放 record 的 javadoc 里用 `@param 组件名 说明`，不要在组件行写 `/** */`（IDE 报「dangling javadoc」）或 `//` 注释

### References

Java 细则入口。按场景触发对应主题细则：

| 场景 | skill | 何时触发 |
|---|---|---|
| 判空 / 取默认值 / 安全取属性 / Map 查询 | [java-null.md](./java-null.md) | 任何 Java null 处理——Objects/Optional，禁裸三元 |
| 字符串判空 | [java-string-utils.md](./java-string-utils.md) | **仅当项目已装 commons-lang3**——StringUtils 替换裸双目 |
| 多分支 switch | [java-switch-yield.md](./java-switch-yield.md) | Java 3+ 常量分支——增强 switch / yield（通用的「3+ 用 switch」见 [SKILL.md](../SKILL.md)） |
| 集合加工 / 数据流水线 | [java-stream.md](./java-stream.md) | 集合遍历加工、filter/map/collect、并行流、Stream 相关 API——Stream 该用 / 禁用 / 高频误用与性能红线 |
