from pydantic import Field

from .common import ActivityType, StrictSchema


class LearningProfileResponse(StrictSchema):
    level: str
    known_vocab: list[str]
    weak_grammar: list[str]
    review_due: list[str]
    interest_topics: list[str]


class UpdateLearningProgressRequest(StrictSchema):
    activity: ActivityType
    score: float = Field(ge=0.0, le=1.0)
    mistakes: list[str] = Field(default_factory=list)


class UpdateLearningProgressResponse(StrictSchema):
    status: str


class NextBestLessonResponse(StrictSchema):
    recommended_focus: str
    reason: str
