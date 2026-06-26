---
name: web-search-engine
description: Retrieve search results from web search engines.
---

# 说明
- 使用node脚本进行搜索
- search.js文件在当前skill目录下
- 返回json序列化数组,顺序对应参数2（搜索引擎名称）
- 参数优先使用引号，特别是搜索关键词包含空格
- 可同时搜索多个搜索引擎,多选使用逗号分割
- 用法：`node search.js "参数1:搜索的关键词(必填参数)" "参数2:搜索引擎名称(可选参数,多选使用逗号分割)"`

# 搜索引擎名称
- `baidu_web_pc`:百度网页搜索PC
- `so_web_pc`:360网页搜索 PC
- `bing_web_pc`:bing网页搜索 PC (默认)
- `sogou_web_pc`:sogou网页搜索 PC

# 优势
- 节省token使用
- 可同时搜索多个搜索引擎
- 轻量
