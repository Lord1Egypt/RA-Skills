# X-ray 分析规则

先读取 `xray-data.json`，所有分析必须基于扫描得到的一手数据。

## project.total_files
用于判断项目规模。

## project.total_directories
用于判断项目的目录规模和组织程度。

## project.languages
用于判断项目主要使用的开发语言。

## project.files
用于了解项目文件结构，并选择值得进一步阅读的关键文件。

## stack.technology_stack
用于判断已经识别出的技术栈。

## 分析原则

在 `xray-data.json` 的基础上，再读取 README、配置文件和关键源码，
进一步判断：

- 这个项目是什么
- 项目类型
- 整体架构
- 关键模块
- 项目复杂度
- 适合哪些方向的人学习
- 推荐阅读顺序

所有结论必须优先依据 `xray-data.json` 和实际源码。

`references` 只负责说明“如何解释扫描数据”，不能覆盖或虚构项目的一手事实。

如果证据不足，明确标记为“不确定”，不要猜测。