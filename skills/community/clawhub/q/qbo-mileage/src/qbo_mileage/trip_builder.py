from __future__ import annotations

import re
from datetime import datetime, timedelta

from .models import CalendarEvent, RunWarning, TripLeg

_TAG_PATTERN = re.compile(r"\[(?P<key>vehicle|type):\s*(?P<value>[^\]]+)\]", re.IGNORECASE)
_PERSONAL_PATTERN = re.compile(r"\[(personal|private)\]", re.IGNORECASE)
_BUSINESS_PATTERN = re.compile(r"\[(business|work)\]", re.IGNORECASE)
_START_PATTERN = re.compile(r"^\s*Start\s*:\s*(?P<value>.+?)\s*$", re.IGNORECASE | re.MULTILINE)
_END_PATTERN = re.compile(r"^\s*End\s*:\s*(?P<value>.+?)\s*$", re.IGNORECASE | re.MULTILINE)


class TripBuilder:
    def __init__(
        self,
        *,
        home_base: str,
        default_vehicle: str,
        chain_threshold_hours: float = 3,
        assume_round_trip_if_alone: bool = True,
        reset_chain_on_day_boundary: bool = True,
    ) -> None:
        self.home_base = home_base
        self.default_vehicle = default_vehicle
        self.chain_threshold = timedelta(hours=chain_threshold_hours)
        self.assume_round_trip_if_alone = assume_round_trip_if_alone
        self.reset_chain_on_day_boundary = reset_chain_on_day_boundary

    def build(self, events: list[CalendarEvent]) -> tuple[list[TripLeg], list[RunWarning]]:
        warnings: list[RunWarning] = []
        normalized = sorted(events, key=lambda event: event.start)
        explicit_legs: list[TripLeg] = []
        chain_events: list[CalendarEvent] = []

        for event in normalized:
            start_address, end_address = self._explicit_addresses(event)
            if start_address and end_address:
                explicit_legs.append(self._make_leg(event, start_address, end_address))
            else:
                chain_events.append(event)

        legs: list[TripLeg] = []
        previous: CalendarEvent | None = None
        previous_location: str | None = None
        valid_chain_events = 0

        for event in chain_events:
            current_location = self._event_location(event)
            if not current_location:
                warnings.append(
                    RunWarning(
                        code="missing_location",
                        message=f"Skipped event without a usable location: {event.title}",
                        event_id=event.id,
                        source=event.source,
                    )
                )
                continue

            if previous is None:
                legs.append(self._make_leg(event, self.home_base, current_location))
                previous = event
                previous_location = current_location
                valid_chain_events += 1
                continue

            if self._starts_new_chain(previous, event):
                if previous_location:
                    # The drive home belongs to the event being returned from.
                    legs.append(self._make_leg(previous, previous_location, self.home_base))
                legs.append(self._make_leg(event, self.home_base, current_location))
            else:
                if previous_location:
                    # The drive between stops belongs to the *destination* event:
                    # its date, purpose, vehicle, and BUSINESS/PERSONAL type must
                    # come from the event being driven to, not the one being left.
                    # Attributing it to `previous` inverted the tax classification
                    # whenever business and personal stops were mixed in one chain.
                    legs.append(self._make_leg(event, previous_location, current_location))
            previous = event
            previous_location = current_location
            valid_chain_events += 1

        if previous is not None and previous_location and (
            self.assume_round_trip_if_alone or valid_chain_events > 1
        ):
            legs.append(self._make_leg(previous, previous_location, self.home_base))

        all_legs = sorted(explicit_legs + legs, key=lambda leg: leg.date)
        filtered: list[TripLeg] = []
        for leg in all_legs:
            if self._same_address(leg.start_address, leg.end_address):
                warnings.append(
                    RunWarning(
                        code="same_start_end",
                        message=f"Skipped zero-distance leg for {leg.purpose}",
                        event_id=leg.source_event_id,
                        source=leg.source,
                    )
                )
                continue
            filtered.append(leg)
        return filtered, warnings

    def _starts_new_chain(self, previous: CalendarEvent, current: CalendarEvent) -> bool:
        if self.reset_chain_on_day_boundary and previous.start.date() != current.start.date():
            return True
        return current.start - previous.end > self.chain_threshold

    def _make_leg(self, event: CalendarEvent, start_address: str, end_address: str) -> TripLeg:
        return TripLeg(
            date=event.start,
            trip_type=self._trip_type(event),
            purpose=self._purpose(event),
            vehicle=self._vehicle(event),
            start_address=start_address,
            end_address=end_address,
            source_event_id=event.id,
            source=event.source,
        )

    def _vehicle(self, event: CalendarEvent) -> str:
        if event.vehicle:
            return event.vehicle
        for text in (event.title, event.description or ""):
            for match in _TAG_PATTERN.finditer(text):
                if match.group("key").lower() == "vehicle":
                    return match.group("value").strip()
        return self.default_vehicle

    def _trip_type(self, event: CalendarEvent) -> str:
        raw = (event.trip_type or "").strip()
        if raw:
            return "PERSONAL" if raw.lower().startswith("personal") else "BUSINESS"
        text = f"{event.title}\n{event.description or ''}"
        for match in _TAG_PATTERN.finditer(text):
            if match.group("key").lower() == "type":
                return "PERSONAL" if match.group("value").strip().lower().startswith("personal") else "BUSINESS"
        if _PERSONAL_PATTERN.search(text):
            return "PERSONAL"
        if _BUSINESS_PATTERN.search(text):
            return "BUSINESS"
        return "BUSINESS"

    def _purpose(self, event: CalendarEvent) -> str:
        text = _TAG_PATTERN.sub("", event.title)
        text = _PERSONAL_PATTERN.sub("", text)
        text = _BUSINESS_PATTERN.sub("", text)
        return " ".join(text.split()) or "Business trip"

    def _event_location(self, event: CalendarEvent) -> str | None:
        if event.location and event.location.strip():
            return event.location.strip()
        _, end_address = self._explicit_addresses(event)
        return end_address

    def _explicit_addresses(self, event: CalendarEvent) -> tuple[str | None, str | None]:
        start_address = event.metadata.get("start_address") or event.metadata.get("start")
        end_address = event.metadata.get("end_address") or event.metadata.get("end")
        description = event.description or ""
        start_match = _START_PATTERN.search(description)
        end_match = _END_PATTERN.search(description)
        if not start_address and start_match:
            start_address = start_match.group("value").strip()
        if not end_address and end_match:
            end_address = end_match.group("value").strip()
        return _clean_optional(start_address), _clean_optional(end_address)

    @staticmethod
    def _same_address(left: str, right: str) -> bool:
        return " ".join(left.lower().split()) == " ".join(right.lower().split())


def _clean_optional(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
