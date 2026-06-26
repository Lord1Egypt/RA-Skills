"""Draft management tools."""
from typing import Optional, List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("wxgzh-mcp")

from ..wechat_api import get_api


@mcp.tool()
def create_draft(
    title: str,
    content: str,
    thumb_media_id: str,
    author: str = None,
    digest: str = None,
) -> dict:
    """Create a draft article in WeChat Official Account.

    After creating a draft, you can publish it manually from WeChat backend,
    or use publish_draft if you have a certified account.

    Args:
        title: Article title (max 64 characters).
        content: Article content in HTML format.
        thumb_media_id: Cover image media_id (from upload_thumb).
        author: Author name (max 8 characters).
        digest: Article summary/digest (max 54 characters).

    Returns:
        dict: Contains media_id of created draft.
    """
    api = get_api()
    result = api.add_draft(
        title=title,
        content=content,
        author=author,
        thumb_media_id=thumb_media_id,
        digest=digest,
    )
    return {
        "media_id": result.get("media_id"),
        "message": "Draft created successfully. Check WeChat backend to publish.",
    }


@mcp.tool()
def list_drafts(offset: int = 0, count: int = 20) -> dict:
    """List all drafts from WeChat Official Account.

    Args:
        offset: Offset for pagination.
        count: Number of items to return (max 20).

    Returns:
        dict: List of draft items with media_id, update_time, etc.
    """
    api = get_api()
    result = api.get_draft_list(offset=offset, count=count)

    drafts = []
    for item in result.get("item", []):
        drafts.append({
            "media_id": item.get("media_id"),
            "update_time": item.get("update_time"),
            "content": item.get("content", {}).get("news_item", []),
        })

    return {
        "drafts": drafts,
        "total": result.get("total_count", 0),
        "offset": offset,
        "count": count,
    }


@mcp.tool()
def get_draft(media_id: str) -> dict:
    """Get single draft detail by media_id.

    Args:
        media_id: The draft media_id.

    Returns:
        dict: Draft content including title, author, content, etc.
    """
    api = get_api()
    result = api.get_draft(media_id)
    return {
        "media_id": media_id,
        "content": result.get("content", {}).get("news_item", []),
        "message": "Draft retrieved successfully.",
    }


@mcp.tool()
def delete_draft(media_id: str) -> dict:
    """Delete a draft by media_id.

    Args:
        media_id: The draft media_id to delete.

    Returns:
        dict: Success status.
    """
    api = get_api()
    api.delete_draft(media_id)
    return {
        "media_id": media_id,
        "message": "Draft deleted successfully.",
    }


@mcp.tool()
def publish_draft(media_id: str) -> dict:
    """Publish/submit a draft for review.

    Note: This only works for certified service accounts.
    Personal subscription accounts cannot use this API.

    Args:
        media_id: The draft media_id to publish.

    Returns:
        dict: Publish result with msg_id and status.
    """
    api = get_api()
    result = api.publish_draft(media_id)
    return {
        "media_id": media_id,
        "msg_id": result.get("msg_id"),
        "errmsg": result.get("errmsg"),
        "message": "Draft published successfully" if result.get("errcode") == 0 else "Publish failed",
    }
