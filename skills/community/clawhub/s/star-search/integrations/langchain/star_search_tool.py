"""
star-search LangChain Tool
让 LangChain / LlamaIndex / Dify agent 直接调用 star-search

用法:
    from star_search_langchain import StarSearchTool
    tool = StarSearchTool()
    result = tool.run("华为 mate 70 价格", mode="quick", top=3)

需要:
    pip install langchain pydantic
"""
import os
import json
from typing import Optional, Type
import urllib.request
import urllib.error

# 可选导入 - 不强制依赖 langchain
try:
    from langchain.tools import BaseTool
    from pydantic import BaseModel, Field
    LANGCHAIN_AVAILABLE = True
except ImportError:
    BaseTool = object
    BaseModel = object
    Field = lambda **kw: None
    LANGCHAIN_AVAILABLE = False


class StarSearchInput(BaseModel):
    """star-search 输入参数"""
    query: str = Field(description="搜索查询（中文/英文/混合）")
    mode: str = Field(default="deep", description="搜索模式: deep/quick/news/policy/stock/dev/global/auto")
    top: int = Field(default=8, ge=1, le=30, description="返回结果数")
    answer: bool = Field(default=True, description="是否生成 LLM 整理的答案")


class StarSearchTool(BaseTool):
    """star-search - 中文 + 英文 AI 搜索引擎
    
    16 个引擎混动（搜狗 / Bing CN / 知乎 / GitHub Issues 等），
    自动意图识别 + LLM 答案层。
    """
    
    name = "star_search"
    description = """中文 + 英文 AI 搜索引擎，输入查询关键词返回搜索结果 + AI 整理答案。
适用于: 查新闻、查资料、查公司、查股价、查技术问题、查学术资料。
参数: query (必填) / mode (deep|quick|news|policy|stock|dev|global|auto) / top (1-30) / answer (bool)
"""
    args_schema: Type[BaseModel] = StarSearchInput
    
    api_base: str = os.environ.get("STAR_SEARCH_BASE", "https://search.token-star.cn/v1")
    timeout: int = 30
    
    def _run(self, query: str, mode: str = "deep", top: int = 8, answer: bool = True) -> str:
        return json.dumps(
            self._call(query, mode, top, answer),
            ensure_ascii=False,
            indent=2
        )
    
    def _call(self, query, mode, top, answer):
        data = json.dumps({"query": query, "mode": mode, "top": top, "answer": answer}).encode()
        req = urllib.request.Request(
            f"{self.api_base}/search",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        try:
            resp = urllib.request.urlopen(req, timeout=self.timeout)
            return json.loads(resp.read())
        except Exception as e:
            return {"error": str(e)}
    
    async def _arun(self, *args, **kwargs):
        return self._run(*args, **kwargs)


# 单文件函数调用 - 不依赖 LangChain
def search(query: str, mode: str = "deep", top: int = 8, answer: bool = True) -> dict:
    """直接调用 star-search 搜索 API"""
    api_base = os.environ.get("STAR_SEARCH_BASE", "https://search.token-star.cn/v1")
    data = json.dumps({"query": query, "mode": mode, "top": top, "answer": answer}).encode()
    req = urllib.request.Request(
        f"{api_base}/search",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read())


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = search(sys.argv[1], mode="quick")
        print(json.dumps(result, ensure_ascii=False, indent=2)[:800])
    else:
        # Demo
        print("用法: python langchain_tool.py <query>")
        print("示例:")
        result = search("华为 mate 70", mode="quick")
        print(json.dumps(result, ensure_ascii=False, indent=2)[:500])
