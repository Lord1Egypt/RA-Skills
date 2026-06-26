import json
from dataclasses import dataclass
from datetime import timezone

from fsrs import Card, Rating, ReviewLog, Scheduler

from config import AppConfig


@dataclass(frozen=True)
class ReviewResult:
    updated_card: Card
    review_log: ReviewLog
    rating_name: str
    retrievability_before: float
    retrievability_after: float


class FsrsService:
    def __init__(self, config: AppConfig) -> None:
        self.scheduler = Scheduler(
            desired_retention=config.desired_retention,
            enable_fuzzing=config.enable_fuzzing,
            maximum_interval=config.maximum_interval,
        )

    def create_new_card(self) -> Card:
        return Card()

    def serialize_card(self, card: Card) -> str:
        return json.dumps(card.to_json(), ensure_ascii=False)

    def deserialize_card(self, payload: str) -> Card:
        return Card.from_json(json.loads(payload))

    def serialize_review_log(self, review_log: ReviewLog) -> str:
        return json.dumps(review_log.to_json(), ensure_ascii=False)

    def review_log_datetime_iso(self, review_log: ReviewLog) -> str:
        review_datetime = review_log.review_datetime
        if review_datetime.tzinfo is None:
            review_datetime = review_datetime.replace(tzinfo=timezone.utc)
        else:
            review_datetime = review_datetime.astimezone(timezone.utc)
        return review_datetime.isoformat()

    def card_due_ts(self, card: Card) -> float:
        due = card.due
        if due.tzinfo is None:
            due = due.replace(tzinfo=timezone.utc)
        else:
            due = due.astimezone(timezone.utc)
        return due.timestamp()

    def get_retrievability(self, card: Card) -> float:
        return self.scheduler.get_card_retrievability(card)

    def _normalize_rating_name(self, raw_rating: str) -> Rating:
        normalized = raw_rating.strip().lower()
        mapping = {
            "again": Rating.Again,
            "hard": Rating.Hard,
            "good": Rating.Good,
            "easy": Rating.Easy,
        }
        if normalized not in mapping:
            raise ValueError("RATING must be one of: again, hard, good, easy")
        return mapping[normalized]

    def review_card(self, card: Card, raw_rating: str) -> ReviewResult:
        rating_enum = self._normalize_rating_name(raw_rating)

        retrievability_before = self.get_retrievability(card)
        updated_card, review_log = self.scheduler.review_card(card, rating_enum)
        retrievability_after = self.get_retrievability(updated_card)

        return ReviewResult(
            updated_card=updated_card,
            review_log=review_log,
            rating_name=raw_rating,
            retrievability_before=retrievability_before,
            retrievability_after=retrievability_after,
        )
