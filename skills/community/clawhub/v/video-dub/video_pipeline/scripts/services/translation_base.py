from abc import ABC, abstractmethod


class Translator(ABC):
    @abstractmethod
    def translate_sentences(self, sentences: list[str]) -> list[str]:
        """Translate a list of sentences while preserving order."""

    def restore_english_sentences(self, sentences: list[str]) -> list[list[str]]:
        """Optionally restore punctuation / sentence boundaries before translation."""
        return [[sentence] for sentence in sentences]
