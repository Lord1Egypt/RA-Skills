"""wxgzh-mcp Skill entry point.

This skill provides WeChat Official Account management tools via MCP protocol.
"""
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server.fastmcp import FastMCP

# Import all tools
from .tools.token import mcp as token_mcp
from .tools.media import mcp as media_mcp
from .tools.draft import mcp as draft_mcp


def main():
    """Run the MCP skill server."""
    # Create main MCP server
    mcp = FastMCP("wxgzh-mcp")

    # Add all tools from sub-modules
    mcp.add_tool(token_mcp._tool_manager.tools)
    mcp.add_tool(media_mcp._tool_manager.tools)
    mcp.add_tool(draft_mcp._tool_manager.tools)

    # Run the server
    mcp.run()


if __name__ == "__main__":
    main()
