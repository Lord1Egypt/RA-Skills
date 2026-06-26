from typing import Any

from mcp.server.fastmcp import FastMCP

from rurussian_mcp.schemas.workflow import (
    CreateDailyLessonRequest,
    CreateReviewSessionRequest,
    EvaluateUserAnswerRequest,
    ExplainTextForLearnerRequest,
    SimulateConversationRequest,
)
from rurussian_mcp.services import auth_service, workflow_service


def _require_access() -> None:
    if not auth_service.has_access():
        raise ValueError("Authentication required. Call authenticate or complete the purchase flow first.")


def register_workflow_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    async def explain_text_for_learner(text: str, level: str, native_language: str) -> dict[str, Any]:
        _require_access()
        request = ExplainTextForLearnerRequest(text=text, level=level, native_language=native_language)
        response = await workflow_service.explain_text_for_learner(request)
        return response.model_dump()

    @mcp.tool()
    async def create_daily_lesson(level: str, focus: list[str], duration_minutes: int = 15) -> dict[str, Any]:
        _require_access()
        request = CreateDailyLessonRequest(
            level=level,
            focus=focus,
            duration_minutes=duration_minutes,
        )
        response = await workflow_service.create_daily_lesson(request)
        return response.model_dump()

    @mcp.tool()
    async def create_review_session(
        known_words: list[str],
        weak_points: list[str],
        difficulty: str = "adaptive",
    ) -> dict[str, Any]:
        _require_access()
        request = CreateReviewSessionRequest(
            known_words=known_words,
            weak_points=weak_points,
            difficulty=difficulty,
        )
        response = await workflow_service.create_review_session(request)
        return response.model_dump()

    @mcp.tool()
    async def evaluate_user_answer(question: str, user_answer: str, expected_skill: str) -> dict[str, Any]:
        _require_access()
        request = EvaluateUserAnswerRequest(
            question=question,
            user_answer=user_answer,
            expected_skill=expected_skill,
        )
        response = await workflow_service.evaluate_user_answer(request)
        return response.model_dump()

    @mcp.tool()
    async def simulate_conversation(scenario: str, level: str) -> dict[str, Any]:
        _require_access()
        request = SimulateConversationRequest(scenario=scenario, level=level)
        response = await workflow_service.simulate_conversation(request)
        return response.model_dump()
