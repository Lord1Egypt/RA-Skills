# 拟在建项目业务流程

## 接口组

- `searchNZJProjectApi`：拟在建项目搜索；
- `getNZJProjectDetail`：拟在建项目详情；
- `getNZJProjectFileList`：拟在建项目附件列表。

## 调用链

```text
自然语言或结构化条件
  -> 拟在建项目搜索
  -> id + publishTime
  -> 拟在建项目详情
  -> 拟在建附件列表（需要时）
```

拟在建项目使用独立模型，不要直接套用招中标项目的官方结构化字段。搜索结果中的 ID 和发布时间仍要成对保存。
