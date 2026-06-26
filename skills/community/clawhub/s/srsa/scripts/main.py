import argparse
import sys

from config import load_config
from fsrs_service import FsrsService
from storage import Storage


def _print_error(message: str) -> int:
    print(f"ERROR: {message}")
    return 1


def _format_progress(reviewed_today: int, remaining_due: int) -> str:
    total = reviewed_today + remaining_due
    return f"{reviewed_today}/{total}"


def _print_question(card: dict) -> None:
    print(f"CARD_ID: {card['id']}")
    print("QUESTION:")
    print(card["question"])


def _print_answer(card: dict) -> None:
    print(f"CARD_ID: {card['id']}")
    print("ANSWER:")
    print(card["answer"])


def handle_status(storage: Storage, fsrs_service: FsrsService) -> int:
    total_cards = storage.count_active_cards()
    reviewed_today = storage.count_reviewed_today()
    remaining_due = storage.count_due_cards_now()
    progress = _format_progress(reviewed_today, remaining_due)

    retrievability_values: list[float] = []
    for payload in storage.list_active_card_payloads():
        card = fsrs_service.deserialize_card(payload["card_json"])
        retrievability_values.append(fsrs_service.get_retrievability(card))

    average_retrievability = (
        sum(retrievability_values) / len(retrievability_values)
        if retrievability_values
        else 0.0
    )

    print(f"Total Cards: {total_cards}")
    print(f"Today's Review Progress: {progress}")
    print("Due Cards in the Next 7 Days:")
    for date_text, count in storage.due_counts_next_days(days=7):
        print(f"{date_text}: {count}")
    print(f"Average Retrievability: {average_retrievability:.2%}")
    return 0


def handle_card_new(
    args: argparse.Namespace, storage: Storage, fsrs_service: FsrsService
) -> int:
    new_card = fsrs_service.create_new_card()
    card_id = storage.create_card(
        question=args.question,
        answer=args.answer,
        card_json=fsrs_service.serialize_card(new_card),
        due_ts=fsrs_service.card_due_ts(new_card),
    )

    print(f"CARD_ID: {card_id} created.")
    return 0


def handle_card_override(
    args: argparse.Namespace, storage: Storage, fsrs_service: FsrsService
) -> int:
    existing = storage.get_card(args.card_id)
    if existing is None:
        return _print_error("CARD_ID does not exist or has been deleted.")

    reset_card = fsrs_service.create_new_card()
    updated = storage.override_card(
        card_id=args.card_id,
        question=args.question,
        answer=args.answer,
        card_json=fsrs_service.serialize_card(reset_card),
        due_ts=fsrs_service.card_due_ts(reset_card),
    )

    if not updated:
        return _print_error("Failed to override the card.")

    state = storage.get_review_state()
    if state["current_card_id"] == args.card_id and not state["rated"]:
        storage.set_review_state(None, False, True)

    print(f"CARD_ID: {args.card_id} overridden.")
    return 0


def handle_card_remove(args: argparse.Namespace, storage: Storage) -> int:
    removed = storage.soft_delete_card(args.card_id)
    if not removed:
        return _print_error("CARD_ID does not exist or has been deleted.")

    state = storage.get_review_state()
    if state["current_card_id"] == args.card_id:
        storage.set_review_state(None, False, True)

    print(f"CARD_ID: {args.card_id} removed.")
    return 0


def handle_review_get_question(storage: Storage) -> int:
    state = storage.get_review_state()

    if state["current_card_id"] is not None and not state["rated"]:
        current = storage.get_card(state["current_card_id"])
        if current is not None:
            print(
                "The current card has not been rated yet, please execute review rate [RATING] first."
            )
            _print_question(current)
            return 0

        storage.set_review_state(None, False, True)

    due_card = storage.get_next_due_card()
    if due_card is None:
        print("There are no due cards now.")
        return 0

    storage.set_review_state(due_card["id"], False, False)
    _print_question(due_card)
    return 0


def handle_review_get_answer(storage: Storage) -> int:
    state = storage.get_review_state()

    if state["current_card_id"] is None or state["rated"]:
        return _print_error(
            "There is no current card being reviewed, please execute review get-question first."
        )

    current = storage.get_card(state["current_card_id"])
    if current is None:
        storage.set_review_state(None, False, True)
        return _print_error(
            "The current card does not exist, please execute review get-question again."
        )

    storage.set_review_state(current["id"], True, False)
    _print_answer(current)
    return 0


def handle_review_rate(
    args: argparse.Namespace, storage: Storage, fsrs_service: FsrsService
) -> int:
    state = storage.get_review_state()

    if state["current_card_id"] is None or state["rated"]:
        return _print_error(
            "There is no current card being reviewed, please execute review get-question first."
        )

    if not state["answer_shown"]:
        return _print_error(
            "Please execute review get-answer to view the answer, then rate the card."
        )

    current = storage.get_card(state["current_card_id"])
    if current is None:
        storage.set_review_state(None, False, True)
        return _print_error(
            "The current card does not exist, please execute review get-question again."
        )

    card = fsrs_service.deserialize_card(current["card_json"])

    try:
        review_result = fsrs_service.review_card(card, args.rating)
    except ValueError as exc:
        return _print_error(str(exc))

    storage.update_card_schedule(
        card_id=current["id"],
        card_json=fsrs_service.serialize_card(review_result.updated_card),
        due_ts=fsrs_service.card_due_ts(review_result.updated_card),
    )
    storage.append_review_log(
        card_id=current["id"],
        rating=review_result.rating_name,
        review_datetime=fsrs_service.review_log_datetime_iso(review_result.review_log),
        review_log_json=fsrs_service.serialize_review_log(review_result.review_log),
        retrievability_before=review_result.retrievability_before,
        retrievability_after=review_result.retrievability_after,
    )
    storage.set_review_state(None, False, True)

    total_reviews, correct_reviews = storage.get_card_history_stats(current["id"])
    accuracy = (correct_reviews / total_reviews) if total_reviews else 0.0

    reviewed_today = storage.count_reviewed_today()
    remaining_due = storage.count_due_cards_now()

    print(f"CARD_ID: {current['id']}")
    print(f"RATING: {review_result.rating_name}")
    print(f"Historical Accuracy: {correct_reviews}/{total_reviews} ({accuracy:.2%})")
    print(f"Today's Review Progress: {_format_progress(reviewed_today, remaining_due)}")
    print(
        f"Retrievability Change: {review_result.retrievability_before:.2%} -> "
        f"{review_result.retrievability_after:.2%}"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SRSA CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status")

    card_parser = subparsers.add_parser("card")
    card_subparsers = card_parser.add_subparsers(dest="card_command", required=True)

    card_new = card_subparsers.add_parser("new")
    card_new.add_argument("-q", "--question", required=True)
    card_new.add_argument("-a", "--answer", required=True)

    card_override = card_subparsers.add_parser("override")
    card_override.add_argument("card_id", type=int)
    card_override.add_argument("-q", "--question", required=True)
    card_override.add_argument("-a", "--answer", required=True)

    card_rm = card_subparsers.add_parser("rm")
    card_rm.add_argument("card_id", type=int)

    review_parser = subparsers.add_parser("review")
    review_subparsers = review_parser.add_subparsers(
        dest="review_command", required=True
    )

    review_subparsers.add_parser("get-question")
    review_subparsers.add_parser("get-answer")

    review_rate = review_subparsers.add_parser("rate")
    review_rate.add_argument("rating")

    return parser


def dispatch(
    args: argparse.Namespace, storage: Storage, fsrs_service: FsrsService
) -> int:
    if args.command == "status":
        return handle_status(storage, fsrs_service)

    if args.command == "card":
        if args.card_command == "new":
            return handle_card_new(args, storage, fsrs_service)
        if args.card_command == "override":
            return handle_card_override(args, storage, fsrs_service)
        if args.card_command == "rm":
            return handle_card_remove(args, storage)

    if args.command == "review":
        if args.review_command == "get-question":
            return handle_review_get_question(storage)
        if args.review_command == "get-answer":
            return handle_review_get_answer(storage)
        if args.review_command == "rate":
            return handle_review_rate(args, storage, fsrs_service)

    return _print_error("Unknown command.")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    config = load_config()
    storage = Storage(config.database_path)
    fsrs_service = FsrsService(config)

    return dispatch(args, storage, fsrs_service)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (FileNotFoundError, ValueError) as exc:
        sys.exit(_print_error(str(exc)))
    except KeyboardInterrupt:
        sys.exit(_print_error("Interrupted."))
