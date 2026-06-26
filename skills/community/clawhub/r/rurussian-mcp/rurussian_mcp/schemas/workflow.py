from pydantic import Field

from .atomic import GenerateReadingPassageResponse
from .common import CEFRLevel, DrillItem, QuizItem, ReviewDifficulty, ReviewType, StrictSchema


class ExplainTextForLearnerRequest(StrictSchema):
    text: str = Field(min_length=1)
    level: CEFRLevel
    native_language: str = Field(min_length=1)


class GrammarPoint(StrictSchema):
    name: str
    explanation: str
    examples: list[str]


class DifficultWord(StrictSchema):
    word: str
    meaning: str
    cefr_level: CEFRLevel


class SentenceBreakdownItem(StrictSchema):
    sentence: str
    structure: str
    notes: str


class ExplainTextForLearnerResponse(StrictSchema):
    translation: str
    grammar_points: list[GrammarPoint]
    difficult_words: list[DifficultWord]
    sentence_breakdown: list[SentenceBreakdownItem]


class CreateDailyLessonRequest(StrictSchema):
    level: CEFRLevel
    focus: list[str] = Field(default_factory=list)
    duration_minutes: int = Field(default=15, ge=5, le=90)


class CreateDailyLessonResponse(StrictSchema):
    reading: GenerateReadingPassageResponse
    vocabulary: list[str]
    grammar_drill: list[DrillItem]
    quiz: list[QuizItem]


class CreateReviewSessionRequest(StrictSchema):
    known_words: list[str] = Field(default_factory=list)
    weak_points: list[str] = Field(default_factory=list)
    difficulty: ReviewDifficulty = ReviewDifficulty.adaptive


class ReviewItem(StrictSchema):
    type: ReviewType
    prompt: str
    answer: str


class CreateReviewSessionResponse(StrictSchema):
    review_items: list[ReviewItem]


class EvaluateUserAnswerRequest(StrictSchema):
    question: str = Field(min_length=1)
    user_answer: str = Field(min_length=1)
    expected_skill: str = Field(min_length=1)


class EvaluateUserAnswerResponse(StrictSchema):
    is_correct: bool
    mistake_type: str
    explanation: str
    score: float = Field(ge=0.0, le=1.0)


class SimulateConversationRequest(StrictSchema):
    scenario: str = Field(min_length=1)
    level: CEFRLevel


class DialogueTurn(StrictSchema):
    speaker: str
    text: str


class SimulateConversationResponse(StrictSchema):
    dialogue: list[DialogueTurn]
