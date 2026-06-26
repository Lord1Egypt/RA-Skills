import json
import os
from datetime import datetime, timezone
from typing import Any

from rurussian_mcp.config import DEFAULT_LEARNER_EMAIL, DEFAULT_LEARNER_ID, MEMORY_STORE_PATH
from rurussian_mcp.schemas.memory import (
    LearningProfileResponse,
    NextBestLessonResponse,
    UpdateLearningProgressRequest,
    UpdateLearningProgressResponse,
)
from rurussian_mcp.services.auth_service import auth_service


DEFAULT_PROFILE: dict[str, Any] = {
    "level": "A1",
    "known_vocab": [],
    "weak_grammar": [],
    "review_due": [],
    "interest_topics": [],
    "activity_log": [],
    "last_activity_at": "",
}


class MemoryService:
    def __init__(self, store_path: str = MEMORY_STORE_PATH) -> None:
        self.store_path = store_path

    def get_learning_profile(self) -> LearningProfileResponse:
        profile = self._get_profile()
        return LearningProfileResponse(
            level=profile["level"],
            known_vocab=profile["known_vocab"],
            weak_grammar=profile["weak_grammar"],
            review_due=profile["review_due"],
            interest_topics=profile["interest_topics"],
        )

    def update_learning_progress(
        self,
        request: UpdateLearningProgressRequest,
    ) -> UpdateLearningProgressResponse:
        store = self._load_store()
        learner_id = self._resolve_learner_id()
        profile = store["learners"].setdefault(learner_id, self._make_default_profile())

        timestamp = datetime.now(timezone.utc).isoformat()
        profile["activity_log"].append(
            {
                "activity": request.activity.value,
                "score": request.score,
                "mistakes": request.mistakes,
                "timestamp": timestamp,
            }
        )
        profile["activity_log"] = profile["activity_log"][-50:]
        profile["last_activity_at"] = timestamp

        if request.score >= 0.85:
            if profile["review_due"]:
                profile["review_due"] = profile["review_due"][1:]
        else:
            for mistake in request.mistakes:
                if mistake not in profile["weak_grammar"]:
                    profile["weak_grammar"].append(mistake)
                if mistake not in profile["review_due"]:
                    profile["review_due"].append(mistake)

        if request.activity.value == "reading" and request.score >= 0.75:
            profile["level"] = self._promote_level(profile["level"])

        self._save_store(store)
        return UpdateLearningProgressResponse(status="updated")

    def get_next_best_lesson(self) -> NextBestLessonResponse:
        profile = self._get_profile()
        if profile["review_due"]:
            item = profile["review_due"][0]
            return NextBestLessonResponse(
                recommended_focus=item,
                reason="Pending spaced-review items should be revisited before new material.",
            )
        if profile["weak_grammar"]:
            item = profile["weak_grammar"][0]
            return NextBestLessonResponse(
                recommended_focus=item,
                reason="Recent activities show repeated errors in this grammar area.",
            )
        if profile["interest_topics"]:
            topic = profile["interest_topics"][0]
            return NextBestLessonResponse(
                recommended_focus=topic,
                reason="No urgent review is due, so the next lesson follows the learner's interests.",
            )
        return NextBestLessonResponse(
            recommended_focus="everyday conversation",
            reason="The profile has no urgent gaps yet, so a general high-frequency lesson is the best next step.",
        )

    def enrich_profile_from_content(self, *, vocabulary: list[str] | None = None, topics: list[str] | None = None) -> None:
        store = self._load_store()
        learner_id = self._resolve_learner_id()
        profile = store["learners"].setdefault(learner_id, self._make_default_profile())

        for word in vocabulary or []:
            if word not in profile["known_vocab"]:
                profile["known_vocab"].append(word)

        for topic in topics or []:
            if topic and topic not in profile["interest_topics"]:
                profile["interest_topics"].append(topic)

        self._save_store(store)

    def get_active_learner_email(self) -> str:
        purchase_email = auth_service.purchase_context.email
        return purchase_email or DEFAULT_LEARNER_EMAIL

    def _get_profile(self) -> dict[str, Any]:
        store = self._load_store()
        learner_id = self._resolve_learner_id()
        return store["learners"].setdefault(learner_id, self._make_default_profile())

    def _load_store(self) -> dict[str, Any]:
        if not os.path.exists(self.store_path):
            return {"learners": {}}
        with open(self.store_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        if "learners" not in data or not isinstance(data["learners"], dict):
            data["learners"] = {}
        return data

    def _save_store(self, store: dict[str, Any]) -> None:
        os.makedirs(os.path.dirname(self.store_path), exist_ok=True)
        with open(self.store_path, "w", encoding="utf-8") as handle:
            json.dump(store, handle, ensure_ascii=False, indent=2)

    def _resolve_learner_id(self) -> str:
        return auth_service.purchase_context.email or DEFAULT_LEARNER_EMAIL or DEFAULT_LEARNER_ID

    @staticmethod
    def _promote_level(level: str) -> str:
        order = ["A1", "A2", "B1", "B2", "C1"]
        if level not in order:
            return "A1"
        index = order.index(level)
        return order[min(index + 1, len(order) - 1)]

    @staticmethod
    def _make_default_profile() -> dict[str, Any]:
        return json.loads(json.dumps(DEFAULT_PROFILE))


memory_service = MemoryService()
