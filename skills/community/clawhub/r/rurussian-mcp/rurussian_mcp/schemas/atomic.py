from pydantic import Field

from .common import CEFRLevel, PassageLength, StrictSchema


class ParseSentenceRequest(StrictSchema):
    text: str = Field(min_length=1)


class MorphologyFeatures(StrictSchema):
    case: str = ""
    number: str = ""
    gender: str = ""
    tense: str = ""
    person: str = ""
    aspect: str = ""
    mood: str = ""


class TokenMorphology(StrictSchema):
    token: str
    features: MorphologyFeatures


class SyntaxEdge(StrictSchema):
    head_index: int
    dependent_index: int
    relation: str


class SyntaxTree(StrictSchema):
    root_index: int | None = None
    edges: list[SyntaxEdge] = Field(default_factory=list)


class ParseSentenceResponse(StrictSchema):
    tokens: list[str]
    lemmas: list[str]
    pos: list[str]
    morphology: list[TokenMorphology]
    syntax_tree: SyntaxTree


class GenerateExamplesRequest(StrictSchema):
    word: str = Field(min_length=1)
    level: CEFRLevel
    count: int = Field(default=5, ge=1, le=10)
    topic: str = ""


class ExampleItem(StrictSchema):
    sentence: str
    translation: str
    grammar_focus: str


class GenerateExamplesResponse(StrictSchema):
    examples: list[ExampleItem]


class GenerateReadingPassageRequest(StrictSchema):
    level: CEFRLevel
    topic: str = Field(min_length=1)
    length: PassageLength


class GenerateReadingPassageResponse(StrictSchema):
    title: str
    text: str
    sentences: list[str]
    estimated_difficulty: float = Field(ge=0.0, le=1.0)
