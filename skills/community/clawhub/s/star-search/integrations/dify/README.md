# star-search LangChain & Dify 集成

## LangChain 安装

```bash
pip install langchain pydantic
```

## 使用

```python
from langchain.agents import load_tools
from star_search_langchain import StarSearchTool

tool = StarSearchTool()
result = tool.run("华为 mate 70 价格", mode="quick", top=3)
```

## Dify 集成

把 `dify_plugin/` 整个目录上传到 Dify Marketplace。

## 配置

环境变量：
- `STAR_SEARCH_BASE`：默认 `https://search.token-star.cn/v1`
- 自部署时改为你自己的 API endpoint。
