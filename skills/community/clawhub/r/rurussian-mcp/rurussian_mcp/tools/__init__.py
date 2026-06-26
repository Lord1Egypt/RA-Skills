from mcp.server.fastmcp import FastMCP

from .atomic import register_atomic_tools
from .auth import register_auth_tools
from .memory import register_memory_tools
from .workflow import register_workflow_tools


def register_all_tools(mcp: FastMCP) -> None:
    register_auth_tools(mcp)
    register_atomic_tools(mcp)
    register_workflow_tools(mcp)
    register_memory_tools(mcp)


__all__ = ["register_all_tools"]
