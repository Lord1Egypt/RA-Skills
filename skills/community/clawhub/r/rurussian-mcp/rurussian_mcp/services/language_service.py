import re
from collections import Counter
from typing import Any

from rurussian_mcp.schemas.atomic import (
    MorphologyFeatures,
    ParseSentenceResponse,
    SyntaxEdge,
    SyntaxTree,
    TokenMorphology,
)
from rurussian_mcp.schemas.common import CEFRLevel, LexicalItem

try:  # pragma: no cover - exercised through runtime, not static analysis
    import pymorphy3

    _MORPH = pymorphy3.MorphAnalyzer()
except Exception:  # pragma: no cover - fallback path
    _MORPH = None


TOKEN_PATTERN = re.compile(r"[A-Za-zА-Яа-яЁё-]+|[^\w\s]", re.UNICODE)
SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[.!?])\s+")

POS_MAP = {
    "NOUN": "NOUN",
    "VERB": "VERB",
    "INFN": "VERB",
    "ADJF": "ADJ",
    "ADJS": "ADJ",
    "COMP": "ADJ",
    "PRTF": "PARTICIPLE",
    "PRTS": "PARTICIPLE",
    "GRND": "GERUND",
    "NUMR": "NUM",
    "ADVB": "ADV",
    "NPRO": "PRON",
    "PRED": "PREDICATIVE",
    "PREP": "ADP",
    "CONJ": "CCONJ",
    "PRCL": "PART",
    "INTJ": "INTJ",
}

CASE_MAP = {
    "nomn": "nominative",
    "gent": "genitive",
    "datv": "dative",
    "accs": "accusative",
    "ablt": "instrumental",
    "loct": "prepositional",
    "voct": "vocative",
}

NUMBER_MAP = {"sing": "singular", "plur": "plural"}
GENDER_MAP = {"masc": "masculine", "femn": "feminine", "neut": "neuter"}
TENSE_MAP = {"pres": "present", "past": "past", "futr": "future"}
PERSON_MAP = {"1per": "first", "2per": "second", "3per": "third"}
ASPECT_MAP = {"perf": "perfective", "impf": "imperfective"}
MOOD_MAP = {"indc": "indicative", "impr": "imperative"}

LEVEL_ORDER = {
    CEFRLevel.A1: 0.20,
    CEFRLevel.A2: 0.35,
    CEFRLevel.B1: 0.50,
    CEFRLevel.B2: 0.70,
    CEFRLevel.C1: 0.85,
}


class LanguageService:
    def tokenize(self, text: str) -> list[str]:
        return TOKEN_PATTERN.findall(text)

    def split_sentences(self, text: str) -> list[str]:
        chunks = [chunk.strip() for chunk in SENTENCE_SPLIT_PATTERN.split(text.strip()) if chunk.strip()]
        return chunks or ([text.strip()] if text.strip() else [])

    def parse_sentence(self, text: str) -> ParseSentenceResponse:
        tokens = self.tokenize(text)
        lemmas: list[str] = []
        pos_tags: list[str] = []
        morphology: list[TokenMorphology] = []

        root_index: int | None = None
        edges: list[SyntaxEdge] = []
        last_content_index: int | None = None
        noun_stack: list[int] = []

        for index, token in enumerate(tokens):
            token_data = self._parse_token(token)
            lemmas.append(token_data["lemma"])
            pos_tags.append(token_data["pos"])
            morphology.append(
                TokenMorphology(
                    token=token,
                    features=MorphologyFeatures(**token_data["features"]),
                )
            )

            pos = token_data["pos"]
            if root_index is None and pos == "VERB":
                root_index = index
            if pos in {"NOUN", "PRON"}:
                noun_stack.append(index)
            if pos == "ADJ" and noun_stack:
                edges.append(SyntaxEdge(head_index=noun_stack[-1], dependent_index=index, relation="amod"))
            elif pos == "ADP" and noun_stack:
                edges.append(SyntaxEdge(head_index=noun_stack[-1], dependent_index=index, relation="case"))
            elif pos not in {"PUNCT", "CCONJ"} and last_content_index is not None:
                relation = "dep"
                if pos == "ADV":
                    relation = "advmod"
                elif pos in {"NOUN", "PRON"}:
                    relation = "obj" if root_index is not None else "dep"
                edges.append(SyntaxEdge(head_index=last_content_index, dependent_index=index, relation=relation))

            if pos not in {"PUNCT", "CCONJ"}:
                last_content_index = index

        if root_index is None:
            root_index = 0 if tokens else None

        return ParseSentenceResponse(
            tokens=tokens,
            lemmas=lemmas,
            pos=pos_tags,
            morphology=morphology,
            syntax_tree=SyntaxTree(root_index=root_index, edges=edges),
        )

    def extract_lexical_items(self, text: str) -> list[LexicalItem]:
        parsed = self.parse_sentence(text)
        items: list[LexicalItem] = []
        seen: set[tuple[str, str]] = set()
        for token, lemma, pos in zip(parsed.tokens, parsed.lemmas, parsed.pos):
            if pos in {"PUNCT", "CCONJ", "PART", "ADP"}:
                continue
            key = (token.lower(), lemma.lower())
            if key in seen:
                continue
            seen.add(key)
            items.append(
                LexicalItem(
                    word=token,
                    lemma=lemma,
                    pos=pos,
                    difficulty_score=self.word_difficulty(token, pos),
                )
            )
        items.sort(key=lambda item: item.difficulty_score, reverse=True)
        return items

    def extract_vocabulary(self, text: str, limit: int = 8) -> list[str]:
        items = self.extract_lexical_items(text)
        return [item.word for item in items[:limit]]

    def estimate_difficulty(self, text: str) -> float:
        items = self.extract_lexical_items(text)
        if not items:
            return 0.0
        base = sum(item.difficulty_score for item in items) / len(items)
        sentence_bonus = min(len(self.split_sentences(text)) / 10.0, 0.15)
        return round(min(base + sentence_bonus, 1.0), 2)

    def assign_cefr_level(self, word: str, pos: str = "") -> CEFRLevel:
        score = self.word_difficulty(word, pos)
        if score < 0.30:
            return CEFRLevel.A1
        if score < 0.45:
            return CEFRLevel.A2
        if score < 0.60:
            return CEFRLevel.B1
        if score < 0.78:
            return CEFRLevel.B2
        return CEFRLevel.C1

    def rank_words_for_level(self, words: list[str], level: CEFRLevel) -> list[str]:
        target = LEVEL_ORDER[level]
        scored = []
        for word in words:
            score = self.word_difficulty(word)
            scored.append((abs(score - target), score, word))
        scored.sort(key=lambda item: (item[0], item[1]))
        return [word for _, _, word in scored]

    def identify_focus_points(self, text: str) -> list[str]:
        parsed = self.parse_sentence(text)
        points: Counter[str] = Counter()
        for token_info, pos in zip(parsed.morphology, parsed.pos):
            features = token_info.features
            if pos == "VERB" and features.aspect:
                points[f"verb aspect: {features.aspect}"] += 1
            if pos in {"NOUN", "PRON", "ADJ"} and features.case:
                points[f"case usage: {features.case}"] += 1
            if pos == "ADP":
                points["prepositions"] += 1
        if not points:
            return ["basic sentence structure"]
        return [item for item, _ in points.most_common(4)]

    def build_sentence_structure_label(self, sentence: str) -> str:
        parsed = self.parse_sentence(sentence)
        has_verb = "VERB" in parsed.pos
        has_subject = any(pos in {"NOUN", "PRON"} for pos in parsed.pos[:2])
        has_object = parsed.pos.count("NOUN") + parsed.pos.count("PRON") > 1
        if has_subject and has_verb and has_object:
            return "subject + predicate + object"
        if has_subject and has_verb:
            return "subject + predicate"
        if has_verb:
            return "predicate-centered clause"
        return "nominal phrase"

    def make_title(self, topic: str, level: CEFRLevel) -> str:
        title_topic = " ".join(part.capitalize() for part in topic.split())
        return f"{title_topic} ({level.value})"

    def word_difficulty(self, word: str, pos: str = "") -> float:
        normalized = word.strip().lower()
        if not normalized:
            return 0.0
        length_score = min(len(normalized) / 12.0, 1.0) * 0.45
        uppercase_penalty = 0.10 if any(ch.isupper() for ch in word) else 0.0
        hyphen_penalty = 0.08 if "-" in normalized else 0.0
        pos_bonus = 0.0
        if pos in {"PARTICIPLE", "GERUND"}:
            pos_bonus = 0.30
        elif pos in {"VERB", "ADJ"}:
            pos_bonus = 0.15
        rare_chars_bonus = 0.12 if any(ch in normalized for ch in {"щ", "ё"}) else 0.0
        return round(min(length_score + uppercase_penalty + hyphen_penalty + pos_bonus + rare_chars_bonus, 1.0), 2)

    def _parse_token(self, token: str) -> dict[str, Any]:
        if not re.search(r"[A-Za-zА-Яа-яЁё]", token):
            return {
                "lemma": token,
                "pos": "PUNCT",
                "features": {
                    "case": "",
                    "number": "",
                    "gender": "",
                    "tense": "",
                    "person": "",
                    "aspect": "",
                    "mood": "",
                },
            }

        if _MORPH is None:
            return {
                "lemma": token.lower(),
                "pos": "X",
                "features": {
                    "case": "",
                    "number": "",
                    "gender": "",
                    "tense": "",
                    "person": "",
                    "aspect": "",
                    "mood": "",
                },
            }

        parsed = _MORPH.parse(token)[0]
        tag = parsed.tag
        return {
            "lemma": parsed.normal_form,
            "pos": POS_MAP.get(str(tag.POS), str(tag.POS) if tag.POS else "X"),
            "features": {
                "case": CASE_MAP.get(str(tag.case), ""),
                "number": NUMBER_MAP.get(str(tag.number), ""),
                "gender": GENDER_MAP.get(str(tag.gender), ""),
                "tense": TENSE_MAP.get(str(tag.tense), ""),
                "person": PERSON_MAP.get(str(tag.person), ""),
                "aspect": ASPECT_MAP.get(str(tag.aspect), ""),
                "mood": MOOD_MAP.get(str(tag.mood), ""),
            },
        }


language_service = LanguageService()
