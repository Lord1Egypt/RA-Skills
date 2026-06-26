# Advanced SQL Decision

适用于以下场景：

- QueryChain 表达困难
- 报表 SQL
- 数据库方言差异明显
- 复杂函数运算

## 优先顺序

1. 先确认是否真的不能用 `QueryChain`
2. 再考虑 SQL 模板
3. 再考虑动态 query / 动态 where
4. 最后才退到 XML / 原生 SQL

## SQL 模板适用场景

适合：

- 局部函数包装
- 特殊表达式
- 仍希望和框架字段、列对象结合

模板类型：

- 命令模板优先使用 `Methods.tpl(...)`
- 函数模板优先使用 `Methods.fTpl(...)`
- 条件模板优先使用 `Methods.cTpl(...)`

Agent 要点：

1. 当只是少量表达式复杂时，不要整条 SQL 都回退原生写法
2. 优先在原有 QueryChain 结构中用模板解决局部复杂度
3. 创建 SQL 模板时，优先通过 `Methods.tpl`、`Methods.fTpl`、`Methods.cTpl` 这些官方入口创建，不要自己手写模板对象

## 特殊字符注意

模板底层涉及 `MessageFormat` 风格占位，单引号要注意转义问题。

Agent 在生成模板时：

1. 尽量把固定值作为参数传入
2. 避免直接在模板里硬编码复杂字面量

## 原生 SQL / XML 何时合理

合理：

- 报表 SQL 结构极重
- 方言差异大
- 历史包袱明确要求保留
- xbatis 原生写法可读性明显更差

不合理：

- 简单 CRUD
- 标准列表页
- 常规联表
- 只因为开发者熟悉 XML
