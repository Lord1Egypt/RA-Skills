from mcp.server.fastmcp import FastMCP

from rurussian_mcp.tools import register_all_tools


mcp = FastMCP(
    "rurussian-mcp",
    dependencies=["mcp>=1.0.0", "httpx", "pydantic", "pymorphy3"],
)

register_all_tools(mcp)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
