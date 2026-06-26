import unittest
from datetime import datetime
from zoneinfo import ZoneInfo

from qbo_mileage.models import CalendarEvent
from qbo_mileage.trip_builder import TripBuilder


TZ = ZoneInfo("America/New_York")


def event(event_id, start_hour, end_hour, title, location, trip_type=None):
    return CalendarEvent(
        id=event_id,
        start=datetime(2026, 5, 5, start_hour, 0, tzinfo=TZ),
        end=datetime(2026, 5, 5, end_hour, 0, tzinfo=TZ),
        title=title,
        location=location,
        description=None,
        source="test",
        trip_type=trip_type,
    )


class TripBuilderTest(unittest.TestCase):
    def test_chain_break_returns_home_before_next_chain(self):
        builder = TripBuilder(
            home_base="Home",
            default_vehicle="Tesla M3",
            chain_threshold_hours=3,
        )
        legs, warnings = builder.build(
            [
                event("1", 9, 10, "Inspection: 123 Main", "123 Main St"),
                event("2", 10, 11, "Inspection: 456 Oak", "456 Oak Ave"),
                event("3", 16, 17, "Inspection: 789 Pine", "789 Pine Rd"),
            ]
        )

        self.assertEqual([], warnings)
        self.assertEqual(
            [
                ("Home", "123 Main St"),
                ("123 Main St", "456 Oak Ave"),
                ("456 Oak Ave", "Home"),
                ("Home", "789 Pine Rd"),
                ("789 Pine Rd", "Home"),
            ],
            [(leg.start_address, leg.end_address) for leg in legs],
        )

    def test_chain_legs_belong_to_destination_event(self):
        """Regression: intermediate chain legs must take their date, purpose,
        and BUSINESS/PERSONAL type from the event being driven TO, not the
        event being left. A personal stop between two inspections previously
        inverted the classification of both surrounding legs."""
        builder = TripBuilder(home_base="Home", default_vehicle="Tesla M3")
        legs, warnings = builder.build(
            [
                event("1", 9, 10, "Inspection: 123 Main", "123 Main St"),
                event("2", 10, 11, "Dentist", "456 Oak Ave", trip_type="Personal"),
                event("3", 12, 13, "Inspection: 789 Pine", "789 Pine Rd"),
            ]
        )

        self.assertEqual([], warnings)
        self.assertEqual(
            [
                ("Home", "123 Main St", "BUSINESS", "Inspection: 123 Main"),
                ("123 Main St", "456 Oak Ave", "PERSONAL", "Dentist"),
                ("456 Oak Ave", "789 Pine Rd", "BUSINESS", "Inspection: 789 Pine"),
                ("789 Pine Rd", "Home", "BUSINESS", "Inspection: 789 Pine"),
            ],
            [(leg.start_address, leg.end_address, leg.trip_type, leg.purpose) for leg in legs],
        )

    def test_chain_leg_dates_follow_destination_event(self):
        builder = TripBuilder(home_base="Home", default_vehicle="Tesla M3")
        legs, _ = builder.build(
            [
                event("1", 9, 10, "Inspection: 123 Main", "123 Main St"),
                event("2", 11, 12, "Inspection: 456 Oak", "456 Oak Ave"),
            ]
        )

        self.assertEqual(
            [9, 11, 11],
            [leg.date.hour for leg in legs],
        )

    def test_vehicle_and_personal_tags(self):
        builder = TripBuilder(home_base="Home", default_vehicle="Tesla M3")
        tagged = CalendarEvent(
            id="1",
            start=datetime(2026, 5, 5, 9, 0, tzinfo=TZ),
            end=datetime(2026, 5, 5, 10, 0, tzinfo=TZ),
            title="Errand [personal] [Vehicle: Truck]",
            location="Store",
            description=None,
            source="test",
        )

        legs, _ = builder.build([tagged])

        self.assertEqual("PERSONAL", legs[0].trip_type)
        self.assertEqual("Truck", legs[0].vehicle)
        self.assertEqual("Errand", legs[0].purpose)

    def test_description_start_end_override(self):
        builder = TripBuilder(home_base="Home", default_vehicle="Tesla M3")
        explicit = CalendarEvent(
            id="1",
            start=datetime(2026, 5, 5, 9, 0, tzinfo=TZ),
            end=datetime(2026, 5, 5, 10, 0, tzinfo=TZ),
            title="Inspection",
            location=None,
            description="Start: Office\nEnd: Site",
            source="test",
        )

        legs, warnings = builder.build([explicit])

        self.assertEqual([], warnings)
        self.assertEqual([("Office", "Site")], [(leg.start_address, leg.end_address) for leg in legs])

    def test_missing_location_does_not_count_as_valid_chain_event(self):
        builder = TripBuilder(
            home_base="Home",
            default_vehicle="Tesla M3",
            assume_round_trip_if_alone=False,
        )
        missing = event("missing", 8, 9, "No address", None)
        valid = event("valid", 10, 11, "Inspection", "Site")

        legs, warnings = builder.build([missing, valid])

        self.assertEqual([("Home", "Site")], [(leg.start_address, leg.end_address) for leg in legs])
        self.assertEqual(["missing_location"], [warning.code for warning in warnings])


if __name__ == "__main__":
    unittest.main()
