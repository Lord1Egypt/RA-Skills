markdown

\---

name: zpw-mianfei-web

description: 使用本地免费搜索引擎搜索网络

\---



\# 免费搜索技能



\## When to Run

\- 用户说“搜索”、“查一下”、“找找”



\## Workflow

1\. 提取搜索关键词

2\. 执行命令：

&#x20;  ```bash

&#x20;  curl -s 'http://192.168.199.100:8080/search?q={{query}}\&format=json'

