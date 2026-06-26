from typing import Any

from mcp.server.fastmcp import FastMCP

from rurussian_mcp.schemas.memory import UpdateLearningProgressRequest
from rurussian_mcp.services import auth_service, memory_service


def _require_access() -> None:
    if not auth_service.has_access():
        raise ValueError("Authentication required. Call authenticate or complete the purchase flow first.")


def register_memory_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    async def get_learning_profile() -> dict[str, Any]:
        _require_access()
        response = memory_service.get_learning_profile()
        return response.model_dump()

    @mcp.tool()
    async def update_learning_progress(activity: str, score: float, mistakes: list[str]) -> dict[str, Any]:
        _require_access()
        request = UpdateLearningProgressRequest(activity=activity, score=score, mistakes=mistakes)
        response = memory_service.update_learning_progress(request)
        return response.model_dump()

    @mcp.tool()
    async def get_next_best_lesson() -> dict[str, Any]:
        _require_access()
        response = memory_service.get_next_best_lesson()
        return response.model_dump()
