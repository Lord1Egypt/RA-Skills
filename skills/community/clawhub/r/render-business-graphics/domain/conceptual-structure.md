# 概念结构领域

## 适用范围

SmartArt 用于有限数量的概念点，重点是表达视觉关系，而不是表达任意图论连接。每个模板有固定项目数量和页面方向，必须查询对应 catalog id 的精确契约。

## 模板意图

- `process`：有序阶段；默认横向，也可纵向。
- `vertical-detail`：纵向条目，每项需要较长说明。
- `cycle`：循环、闭环、PDCA。
- `radial`：一个中心概念和周边维度。
- `petal-radial`：恰好六个维度的分类体系，使用横版。
- `pyramid`：分层、等级、保障体系。
- `relationship`：围绕中心的多方协同关系。
- `comparison`：两个方案按多个标准对比。
- `key-points`：有限数量的关键保障或重点。

普通模板使用项目数组；`comparison` 使用 `columns + rows` 对象。`center` 只用于 cycle、radial、petal-radial、relationship。

## 文字规则

SmartArt 标题建议 14 个字符以内，解释放 `note`，建议 36 个字符以内。每个项目只表达一个概念，不要在一个项目中叠加多个职责。
