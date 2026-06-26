# Tavily Web Search

## 说明

- 用 openclaw 搜索工具只能同时支持一个搜索引擎，如果需要多引擎搜索，还是要用Skills。
- 最好在 openclaw 的 TOOLS.md 加入类似 **"搜索时请调用tavily-search skill，不要用自带的web_search工具功能"** 的指示，否则 openclaw 可能消耗额外的token去尝试工具调用。
- 同时可以在 openclaw.json 中将 web_search 关闭。
```openclaw.json
  "tools": {
    "web": {
      "enabled": false
    }
  }
```

## 前置条件

### Tavily API Key

在 Tavily 官网
https://www.tavily.com/ -> Sign Up/Login

API Keys -> `+`

* 官方文档：https://docs.tavily.com/documentation/api-reference/endpoint/search
