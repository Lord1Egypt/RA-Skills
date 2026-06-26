from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class StrictSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CEFRLevel(str, Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"


class PassageLength(str, Enum):
    short = "short"
    medium = "medium"
    long = "long"


class DrillType(str, Enum):
    fill_blank = "fill_blank"
    translation = "translation"
    mcq = "mcq"


class ReviewType(str, Enum):
    vocab = "vocab"
    grammar = "grammar"


class ReviewDifficulty(str, Enum):
    adaptive = "adaptive"


class MistakeType(str, Enum):
    none = "none"
    case_error = "case_error"
    tense_error = "tense_error"


class ActivityType(str, Enum):
    quiz = "quiz"
    conversation = "conversation"
    reading = "reading"


class PurchaseContextSchema(StrictSchema):
    email: str = ""
    plan: str = ""
    checkout_url: str = ""
    session_id: str = ""
    payment_status: str = ""


class ErrorPayload(StrictSchema):
    code: str
    message: str
    retryable: bool = False


class ToolErrorResponse(StrictSchema):
    error: ErrorPayload


class PlanInfo(StrictSchema):
    plan: str
    display_name: str
    price_usd: float
    duration_days: int
    marketing_copy: str


class LexicalItem(StrictSchema):
    word: str
    lemma: str
    pos: str
    difficulty_score: float = Field(ge=0.0, le=1.0)


class DrillItem(StrictSchema):
    question: str
    answer: str
    type: DrillType


class QuizItem(StrictSchema):
    question: str
    options: list[str]
    correct: str
