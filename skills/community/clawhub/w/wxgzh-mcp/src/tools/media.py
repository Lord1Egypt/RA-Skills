"""Media upload tools."""
from typing import Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("wxgzh-mcp")

from ..wechat_api import get_api


@mcp.tool()
def upload_thumb(thumb_path: str) -> dict:
    """Upload cover/thumbnail image to WeChat Official Account.

    The returned media_id must be used when creating a draft.

    Args:
        thumb_path: Local path to the thumb image file (JPG/PNG, max 2MB).

    Returns:
        dict: Contains media_id of uploaded thumb cover image.
    """
    api = get_api()
    media_id = api.upload_thumb(thumb_path)
    return {
        "media_id": media_id,
        "message": "Thumb uploaded successfully. Use this media_id in create_draft.",
    }


@mcp.tool()
def upload_image(image_path: str) -> dict:
    """Upload image to WeChat Official Account (for article content).

    This is used for images embedded in article body, not cover images.

    Args:
        image_path: Local path to the image file (JPG/PNG, max 2MB).

    Returns:
        dict: Contains media_id and url of uploaded image.
    """
    api = get_api()
    result = api.upload_image(image_path)
    return {
        "media_id": result.get("media_id"),
        "url": result.get("url"),
        "message": "Image uploaded successfully.",
    }


@mcp.tool()
def list_materials(type: str = "image", offset: int = 0, count: int = 20) -> dict:
    """List permanent materials (images, videos, etc.).

    Args:
        type: Material type: "image", "video", "voice", "news"
        offset: Offset for pagination
        count: Number of items to return (max 20)

    Returns:
        dict: List of materials with media_id, name, url, etc.
    """
    api = get_api()
    items = api.batch_get_material(type=type, offset=offset, count=count)
    return {
        "items": items,
        "total": len(items),
    }
