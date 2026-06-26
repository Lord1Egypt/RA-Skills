"""Remote Memory Client — connect to Agent Memory server over HTTP.

Used internally by Memory(server=...) for remote mode.
Can also be used directly for non-Python integrations.
"""

import json
import logging
from typing import Optional

from .utils import _validate_url

logger = logging.getLogger(__name__)

try:
    import urllib.request
    import urllib.error
    _HAS_URLLIB = True
except ImportError:
    _HAS_URLLIB = False


class MemoryClient:
    """HTTP client for Agent Memory server.

    Usage:
        client = MemoryClient("http://localhost:8000", api_key="<YOUR_API_KEY>")
        mid = client.save("Hello world")
        results = client.search("hello")
    """

    def __init__(self, base_url: str, api_key: Optional[str] = None, tenant_id: Optional[str] = None, timeout: int = 30):
        if not _HAS_URLLIB:
            raise ImportError("urllib is required for remote mode")

        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._tenant_id = tenant_id
        self._timeout = timeout

    def _request(self, method: str, path: str, data: Optional[dict] = None) -> dict:
        """Make HTTP request to the server."""
        url = f"{self._base_url}{path}"
        _validate_url(url)
        headers = {"Content-Type": "application/json"}

        if self._api_key:
            headers["X-API-Key"] = self._api_key

        body = None
        if data:
            body = json.dumps(data).encode("utf-8")

        req = urllib.request.Request(url, data=body, headers=headers, method=method)

        try:
            with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="replace")
            logger.error("HTTP %d: %s", e.code, error_body[:200])
            return {"error": f"HTTP {e.code}", "details": error_body[:200]}
        except Exception as e:
            logger.error("Request failed: %s", e)
            return {"error": str(e)}

    def save(self, content: str, **kwargs) -> str:
        """Save a memory remotely. Returns memory_id."""
        payload = {"content": content, **kwargs}
        if self._tenant_id:
            payload["tenant_id"] = self._tenant_id

        result = self._request("POST", "/api/v3/memories", payload)
        return result.get("memory_id", "")

    def search(self, query: str, limit: int = 10, **kwargs) -> list:
        """Search memories remotely. Returns list of dicts."""
        payload = {"query": query, "limit": limit, **kwargs}
        if self._tenant_id:
            payload["tenant_id"] = self._tenant_id

        result = self._request("POST", "/api/v3/recall", payload)

        # Normalize result
        if isinstance(result, dict):
            primary = result.get("primary", result.get("results", []))
            if isinstance(primary, list):
                return primary[:limit]
        if isinstance(result, list):
            return result[:limit]
        return []

    def update(self, memory_id: str, content: str, **kwargs) -> bool:
        """Update a memory remotely."""
        payload = {"content": content, **kwargs}
        result = self._request("PUT", f"/api/v3/memories/{memory_id}", payload)
        return "error" not in result

    def delete(self, memory_id: str, permanent: bool = False) -> bool:
        """Delete a memory remotely."""
        path = f"/api/v3/memories/{memory_id}"
        if permanent:
            path += "?permanent=true"
        result = self._request("DELETE", path)
        return "error" not in result

    def status(self) -> dict:
        """Check server health."""
        return self._request("GET", "/health")

    def bookmark(self, memory_id: str) -> bool:
        """Bookmark a memory for quick access."""
        result = self._request("POST", f"/api/v3/memories/{memory_id}/bookmark")
        return "error" not in result

    def unbookmark(self, memory_id: str) -> bool:
        """Remove bookmark from a memory."""
        result = self._request("DELETE", f"/api/v3/memories/{memory_id}/bookmark")
        return "error" not in result

    def bookmarks(self, limit: int = 50) -> list:
        """Get all bookmarked memories."""
        result = self._request("GET", f"/api/v3/memories/bookmarks?limit={limit}")
        if isinstance(result, dict):
            return result.get("items", result.get("bookmarks", []))
        return []

    def echo(self, context: str = "", limit: int = 3) -> list:
        """Get proactive memory recommendations remotely."""
        payload = {"context": context, "limit": limit}
        if self._tenant_id:
            payload["tenant_id"] = self._tenant_id
        result = self._request("POST", "/api/v3/echo", payload)
        if isinstance(result, dict):
            return result.get("echoes", result.get("items", []))
        return []

    def milestones(self) -> list:
        """View all achievement milestones (unlocked and locked)."""
        result = self._request("GET", "/api/v3/milestones")
        if isinstance(result, dict):
            return result.get("milestones", [])
        return []

    def share_card(self, card_type: str = "stats") -> str:
        """Generate a shareable HTML card."""
        result = self._request("GET", f"/api/v3/share-card?type={card_type}")
        if isinstance(result, dict):
            return result.get("html", "")
        return ""

    # Brand-name aliases (prefer remember/recall/forget over save/search/delete)

    def remember(self, content: str, **kwargs) -> str:
        """Alias-compatible: prefer remember() over save()."""
        return self.save(content, **kwargs)

    def recall(self, query: str, limit: int = 10, **kwargs) -> list:
        """Alias-compatible: prefer recall() over search()."""
        return self.search(query, limit=limit, **kwargs)

    def forget(self, memory_id: str, permanent: bool = False) -> bool:
        """Alias-compatible: prefer forget() over delete()."""
        return self.delete(memory_id, permanent=permanent)
