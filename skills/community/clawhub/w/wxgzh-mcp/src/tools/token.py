"""Token management tools."""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("wxgzh-mcp")

from ..wechat_api import get_api


@mcp.tool()
def get_access_token(force_refresh: bool = False) -> dict:
    """Get WeChat Access Token.

    Access token is required for all other API calls.
    It is automatically cached and refreshed when expired.

    Args:
        force_refresh: Force refresh token even if current one is valid.

    Returns:
        dict: Contains access_token and expires_in seconds.
    """
    api = get_api()
    token = api.get_access_token(force_refresh=force_refresh)
    return {
        "access_token": token,
        "expires_in": 7200,
        "message": "Token retrieved successfully. Valid for 2 hours.",
    }
