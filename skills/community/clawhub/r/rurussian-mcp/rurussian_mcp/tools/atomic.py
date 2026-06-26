from typing import Any

from mcp.server.fastmcp import FastMCP

from rurussian_mcp.schemas.atomic import (
    GenerateExamplesRequest,
    GenerateReadingPassageRequest,
    ParseSentenceRequest,
)
from rurussian_mcp.services import auth_service, language_service, workflow_service


def _require_access() -> None:
    if not auth_service.has_access():
        raise ValueError("Authentication required. Call authenticate or complete the purchase flow first.")


def register_atomic_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    async def parse_sentence(text: str) -> dict[str, Any]:
        _require_access()
        request = ParseSentenceRequest(text=text)
        response = language_service.parse_sentence(request.text)
        return response.model_dump()

    @mcp.tool()
    async def generate_examples(word: str, level: str, count: int = 5, topic: str = "") -> dict[str, Any]:
        _require_access()
        request = GenerateExamplesRequest(word=word, level=level, count=count, topic=topic)
        response = await workflow_service.generate_examples(request)
        return response.model_dump()

    @mcp.tool()
    async def generate_reading_passage(level: str, topic: str, length: str) -> dict[str, Any]:
        _require_access()
        request = GenerateReadingPassageRequest(level=level, topic=topic, length=length)
        response = await workflow_service.generate_reading_passage(request)
        return response.model_dump()
