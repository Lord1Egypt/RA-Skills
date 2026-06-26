from typing import Any

from rurussian_mcp.schemas.atomic import (
    ExampleItem,
    GenerateExamplesRequest,
    GenerateExamplesResponse,
    GenerateReadingPassageRequest,
    GenerateReadingPassageResponse,
)
from rurussian_mcp.schemas.common import CEFRLevel, DrillItem, DrillType, MistakeType, QuizItem, ReviewType
from rurussian_mcp.schemas.workflow import (
    CreateDailyLessonRequest,
    CreateDailyLessonResponse,
    CreateReviewSessionRequest,
    CreateReviewSessionResponse,
    DialogueTurn,
    DifficultWord,
    EvaluateUserAnswerRequest,
    EvaluateUserAnswerResponse,
    ExplainTextForLearnerRequest,
    ExplainTextForLearnerResponse,
    GrammarPoint,
    ReviewItem,
    SentenceBreakdownItem,
    SimulateConversationRequest,
    SimulateConversationResponse,
)
from rurussian_mcp.services.backend_client import backend_client
from rurussian_mcp.services.language_service import language_service
from rurussian_mcp.services.memory_service import memory_service


LENGTH_TO_SENTENCE_COUNT = {
    "short": 3,
    "medium": 5,
    "long": 7,
}


class WorkflowService:
    async def generate_examples(self, request: GenerateExamplesRequest) -> GenerateExamplesResponse:
        forms = []
        for index in range(request.count):
            forms.append(
                {
                    "id": f"example_{index}",
                    "form_name": f"{request.level.value} usage example {index + 1}",
                    "word": request.word,
                    "definition": request.topic or f"daily life topic for {request.level.value}",
                }
            )

        response_items: list[ExampleItem] = []
        try:
            results = await backend_client.generate_sentences(
                request.word,
                forms,
                cache_only=False,
                wait_seconds=0,
                poll_interval_ms=500,
            )
            for form in forms:
                item = results.get(form["id"], {}) if isinstance(results, dict) else {}
                sentence = item.get("sentence")
                translation = item.get("translation")
                if not isinstance(sentence, str) or not sentence:
                    continue
                response_items.append(
                    ExampleItem(
                        sentence=sentence,
                        translation=translation or "",
                        grammar_focus=self._pick_grammar_focus(sentence),
                    )
                )
        except Exception:
            response_items = []

        if not response_items:
            response_items = self._fallback_examples(request)

        return GenerateExamplesResponse(examples=response_items[: request.count])

    async def generate_reading_passage(
        self,
        request: GenerateReadingPassageRequest,
    ) -> GenerateReadingPassageResponse:
        learner_email = memory_service.get_active_learner_email()
        text = ""

        if learner_email:
            try:
                backend_payload = {
                    "user_email": learner_email,
                    "mode": "custom",
                    "selected_words": [
                        {
                            "word": request.topic,
                            "context": f"{request.level.value} reading passage about {request.topic}",
                        }
                    ],
                }
                backend_result = await backend_client.generate_zakuska(backend_payload)
                text = (
                    backend_result.get("paragraph")
                    or backend_result.get("text")
                    or backend_result.get("content")
                    or ""
                )
            except Exception:
                text = ""

        if not text:
            sentences = self._fallback_passage_sentences(request.topic, request.level, request.length.value)
            text = " ".join(sentences)

        sentences = language_service.split_sentences(text)
        max_sentences = LENGTH_TO_SENTENCE_COUNT[request.length.value]
        trimmed_sentences = sentences[:max_sentences]
        passage_text = " ".join(trimmed_sentences)

        return GenerateReadingPassageResponse(
            title=language_service.make_title(request.topic, request.level),
            text=passage_text,
            sentences=trimmed_sentences,
            estimated_difficulty=language_service.estimate_difficulty(passage_text),
        )

    async def explain_text_for_learner(
        self,
        request: ExplainTextForLearnerRequest,
    ) -> ExplainTextForLearnerResponse:
        translation = ""
        try:
            translation_payload = await backend_client.translate_text(
                request.text,
                source_lang="Russian",
                target_lang=request.native_language,
            )
            translation = (
                translation_payload.get("translation")
                or translation_payload.get("translated_text")
                or translation_payload.get("text")
                or ""
            )
        except Exception:
            translation = ""

        sentences = language_service.split_sentences(request.text)
        grammar_points: list[GrammarPoint] = []
        sentence_breakdown: list[SentenceBreakdownItem] = []
        seen_points: set[str] = set()

        for sentence in sentences:
            focus_points = language_service.identify_focus_points(sentence)
            for focus in focus_points:
                if focus in seen_points:
                    continue
                seen_points.add(focus)
                grammar_points.append(
                    GrammarPoint(
                        name=focus,
                        explanation=self._explain_focus_point(focus, request.level),
                        examples=[sentence],
                    )
                )
            sentence_breakdown.append(
                SentenceBreakdownItem(
                    sentence=sentence,
                    structure=language_service.build_sentence_structure_label(sentence),
                    notes=", ".join(focus_points[:2]) if focus_points else "basic sentence pattern",
                )
            )

        difficult_words = await self._build_difficult_words(request.text)

        if not translation:
            translation = request.text

        return ExplainTextForLearnerResponse(
            translation=translation,
            grammar_points=grammar_points[:5],
            difficult_words=difficult_words,
            sentence_breakdown=sentence_breakdown,
        )

    async def create_daily_lesson(
        self,
        request: CreateDailyLessonRequest,
    ) -> CreateDailyLessonResponse:
        primary_focus = request.focus[0] if request.focus else "everyday life"
        reading = await self.generate_reading_passage(
            GenerateReadingPassageRequest(
                level=request.level,
                topic=primary_focus,
                length=self._lesson_length_from_duration(request.duration_minutes),
            )
        )

        vocabulary = language_service.extract_vocabulary(reading.text, limit=8)
        ranked_vocab = language_service.rank_words_for_level(vocabulary, request.level)
        grammar_drill = self._build_grammar_drills(primary_focus, reading.text, ranked_vocab)
        quiz = self._build_quiz(reading, ranked_vocab)

        memory_service.enrich_profile_from_content(vocabulary=ranked_vocab[:5], topics=request.focus)

        return CreateDailyLessonResponse(
            reading=reading,
            vocabulary=ranked_vocab,
            grammar_drill=grammar_drill,
            quiz=quiz,
        )

    async def create_review_session(
        self,
        request: CreateReviewSessionRequest,
    ) -> CreateReviewSessionResponse:
        review_items: list[ReviewItem] = []
        for word in request.known_words[:5]:
            review_items.append(
                ReviewItem(
                    type=ReviewType.vocab,
                    prompt=f"Use the word '{word}' in a simple Russian sentence.",
                    answer=f"Sentence should include '{word}' naturally and correctly.",
                )
            )

        for weak_point in request.weak_points[:5]:
            review_items.append(
                ReviewItem(
                    type=ReviewType.grammar,
                    prompt=f"Explain or produce one example of: {weak_point}.",
                    answer=f"Correct response should demonstrate accurate use of {weak_point}.",
                )
            )

        return CreateReviewSessionResponse(review_items=review_items)

    async def evaluate_user_answer(
        self,
        request: EvaluateUserAnswerRequest,
    ) -> EvaluateUserAnswerResponse:
        user_answer = self._normalize_text(request.user_answer)
        expected = self._normalize_text(request.question)

        if user_answer == expected:
            return EvaluateUserAnswerResponse(
                is_correct=True,
                mistake_type=MistakeType.none.value,
                explanation="The answer matches the expected target exactly.",
                score=1.0,
            )

        user_parse = language_service.parse_sentence(request.user_answer)
        expected_parse = language_service.parse_sentence(request.question)

        user_lemmas = [lemma for lemma in user_parse.lemmas if lemma.isalpha()]
        expected_lemmas = [lemma for lemma in expected_parse.lemmas if lemma.isalpha()]
        shared_lemmas = set(user_lemmas) & set(expected_lemmas)

        mistake_type = MistakeType.tense_error
        explanation = "The answer is related to the target but uses different grammatical forms."
        score = 0.45

        if user_lemmas == expected_lemmas:
            case_changed = any(
                u.features.case != e.features.case
                for u, e in zip(user_parse.morphology, expected_parse.morphology)
                if u.features.case or e.features.case
            )
            if case_changed:
                mistake_type = MistakeType.case_error
                explanation = "The answer keeps the core meaning but changes noun or adjective case marking."
                score = 0.7
            else:
                mistake_type = MistakeType.tense_error
                explanation = "The answer keeps the same lemmas but shifts tense, aspect, or verbal inflection."
                score = 0.65
        elif shared_lemmas:
            score = 0.55
            explanation = "The answer overlaps with the expected meaning, but key lexical items or structures differ."
        else:
            mistake_type = MistakeType.tense_error
            explanation = "The answer does not align closely enough with the requested skill target."
            score = 0.2

        return EvaluateUserAnswerResponse(
            is_correct=score >= 0.85,
            mistake_type=mistake_type.value,
            explanation=explanation,
            score=round(score, 2),
        )

    async def simulate_conversation(
        self,
        request: SimulateConversationRequest,
    ) -> SimulateConversationResponse:
        scenario = request.scenario.strip()
        starter = self._conversation_starter(request.level, scenario)
        follow_up = self._conversation_follow_up(request.level, scenario)

        dialogue = [
            DialogueTurn(speaker="tutor", text=starter),
            DialogueTurn(speaker="user", text=self._user_turn(request.level, scenario)),
            DialogueTurn(speaker="tutor", text=follow_up),
            DialogueTurn(speaker="user", text=self._user_response(request.level, scenario)),
        ]
        return SimulateConversationResponse(dialogue=dialogue)

    async def _build_difficult_words(self, text: str) -> list[DifficultWord]:
        lexical_items = language_service.extract_lexical_items(text)[:5]
        difficult_words: list[DifficultWord] = []
        for item in lexical_items:
            meaning = item.lemma
            try:
                word_data = await backend_client.get_word_data(item.lemma)
                meaning = self._extract_word_meaning(word_data) or item.lemma
            except Exception:
                meaning = item.lemma
            difficult_words.append(
                DifficultWord(
                    word=item.word,
                    meaning=meaning,
                    cefr_level=language_service.assign_cefr_level(item.word, item.pos),
                )
            )
        return difficult_words

    def _fallback_examples(self, request: GenerateExamplesRequest) -> list[ExampleItem]:
        templates = [
            f"Это {request.word}.",
            f"Я часто использую слово {request.word} в разговоре.",
            f"Сегодня тема урока связана с {request.word}.",
            f"Мы обсуждаем {request.word}, потому что это полезная тема.",
            f"Преподаватель объясняет, как правильно употреблять {request.word}.",
        ]
        examples: list[ExampleItem] = []
        for sentence in templates[: request.count]:
            examples.append(
                ExampleItem(
                    sentence=sentence,
                    translation=sentence,
                    grammar_focus=self._pick_grammar_focus(sentence),
                )
            )
        return examples

    def _fallback_passage_sentences(self, topic: str, level: CEFRLevel, length: str) -> list[str]:
        count = LENGTH_TO_SENTENCE_COUNT[length]
        sentences = [
            f"Сегодня мы говорим о теме '{topic}'.",
            f"Это важная тема для ученика уровня {level.value}.",
            "Герой текста читает, слушает и повторяет новые слова каждый день.",
            "Потом он обсуждает материал с преподавателем и делает короткие упражнения.",
            "Такой подход помогает лучше понимать русский язык в обычной жизни.",
            "Иногда он возвращается к трудным словам и повторяет их в новых предложениях.",
            "В конце занятия он замечает, что говорить стало немного легче.",
        ]
        return sentences[:count]

    @staticmethod
    def _extract_word_meaning(word_data: dict[str, Any]) -> str:
        definitions = word_data.get("definitions")
        if not isinstance(definitions, list):
            return ""
        for definition in definitions:
            for item in definition.get("items", []):
                if item.get("type") == "definition":
                    return item.get("text", "")
        return ""

    @staticmethod
    def _lesson_length_from_duration(duration_minutes: int) -> str:
        if duration_minutes <= 10:
            return "short"
        if duration_minutes <= 20:
            return "medium"
        return "long"

    @staticmethod
    def _normalize_text(text: str) -> str:
        return " ".join(text.lower().split())

    @staticmethod
    def _pick_grammar_focus(sentence: str) -> str:
        return language_service.identify_focus_points(sentence)[0]

    @staticmethod
    def _explain_focus_point(focus: str, level: CEFRLevel) -> str:
        return f"This text highlights {focus}, explained at a {level.value} learner-friendly level."

    @staticmethod
    def _build_grammar_drills(focus: str, text: str, vocabulary: list[str]) -> list[DrillItem]:
        target_word = vocabulary[0] if vocabulary else "слово"
        return [
            DrillItem(
                question=f"Fill the blank with a correct form related to '{focus}': Я ___ русский каждый день.",
                answer="учу",
                type=DrillType.fill_blank,
            ),
            DrillItem(
                question=f"Translate into Russian using '{target_word}' when possible: 'This topic is important.'",
                answer=f"Эта тема важна. ({target_word})",
                type=DrillType.translation,
            ),
            DrillItem(
                question=f"Choose the best grammar label for this lesson focus: {focus}.",
                answer=focus,
                type=DrillType.mcq,
            ),
        ]

    @staticmethod
    def _build_quiz(reading: GenerateReadingPassageResponse, vocabulary: list[str]) -> list[QuizItem]:
        first_word = vocabulary[0] if vocabulary else "урок"
        return [
            QuizItem(
                question="What is the main topic of the reading?",
                options=[reading.title, "Weather", "Travel", "Food"],
                correct=reading.title,
            ),
            QuizItem(
                question="Which item appears in the lesson vocabulary?",
                options=[first_word, "bonjour", "hola", "ciao"],
                correct=first_word,
            ),
            QuizItem(
                question="How many sentences are in the reading block?",
                options=["1", str(len(reading.sentences)), "10", "12"],
                correct=str(len(reading.sentences)),
            ),
        ]

    @staticmethod
    def _conversation_starter(level: CEFRLevel, scenario: str) -> str:
        if level in {CEFRLevel.A1, CEFRLevel.A2}:
            return f"Здравствуйте. Давайте разыграем ситуацию: {scenario}. Как вы начнёте разговор?"
        return f"Представим ситуацию '{scenario}'. Начните диалог естественной репликой на русском."

    @staticmethod
    def _user_turn(level: CEFRLevel, scenario: str) -> str:
        if level in {CEFRLevel.A1, CEFRLevel.A2}:
            return f"Здравствуйте. Мне нужна помощь в ситуации: {scenario}."
        return f"Добрый день. Я хотел бы обсудить ситуацию '{scenario}' и уточнить детали."

    @staticmethod
    def _conversation_follow_up(level: CEFRLevel, scenario: str) -> str:
        if level in {CEFRLevel.A1, CEFRLevel.A2}:
            return "Хорошо. Скажите это немного подробнее и используйте одну вежливую просьбу."
        return f"Отлично. Теперь добавьте уточняющий вопрос, чтобы продвинуть разговор о теме '{scenario}'."

    @staticmethod
    def _user_response(level: CEFRLevel, scenario: str) -> str:
        if level in {CEFRLevel.A1, CEFRLevel.A2}:
            return f"Пожалуйста, помогите мне с темой '{scenario}'."
        return f"Не могли бы вы подробнее объяснить, как лучше действовать в ситуации '{scenario}'?"


workflow_service = WorkflowService()
