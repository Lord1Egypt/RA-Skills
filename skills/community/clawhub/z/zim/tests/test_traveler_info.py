"""Tests for zim.traveler_info — traveler information capture and validation."""

from datetime import date

import pytest

from zim.traveler_info import TravelerInfo


class TestTravelerInfoConstruction:
    def test_empty_defaults(self) -> None:
        ti = TravelerInfo()
        assert ti.first_name is None
        assert ti.last_name is None
        assert ti.email is None
        assert ti.frequent_flyer == {}

    def test_full_construction(self) -> None:
        ti = TravelerInfo(
            first_name="Robin",
            last_name="Zieme",
            date_of_birth=date(1990, 5, 15),
            gender="M",
            passport_number="AB1234567",
            passport_expiry=date(2030, 12, 31),
            passport_country="DE",
            email="robin@example.com",
            phone="+971544042230",
            frequent_flyer={"EK": "FF12345"},
        )
        assert ti.first_name == "Robin"
        assert ti.gender == "M"
        assert ti.passport_country == "DE"
        assert ti.email == "robin@example.com"


class TestTravelerInfoValidation:
    def test_gender_normalized_to_upper(self) -> None:
        ti = TravelerInfo(gender="f")
        assert ti.gender == "F"

    def test_invalid_gender_raises(self) -> None:
        with pytest.raises(ValueError, match="Gender must be M, F, or X"):
            TravelerInfo(gender="Z")

    def test_email_validated(self) -> None:
        ti = TravelerInfo(email="Robin@Example.COM")
        assert ti.email == "robin@example.com"

    def test_invalid_email_raises(self) -> None:
        with pytest.raises(ValueError, match="Invalid email"):
            TravelerInfo(email="not-an-email")

    def test_country_code_validated(self) -> None:
        ti = TravelerInfo(passport_country="de")
        assert ti.passport_country == "DE"

    def test_invalid_country_raises(self) -> None:
        with pytest.raises(ValueError, match="ISO-3166-1 alpha-2"):
            TravelerInfo(passport_country="DEU")


class TestMissingFields:
    def test_empty_traveler_missing_all(self) -> None:
        ti = TravelerInfo()
        missing = ti.missing_required_fields(require_passport=True)
        assert "first_name" in missing
        assert "last_name" in missing
        assert "date_of_birth" in missing
        assert "email" in missing
        assert "phone" in missing
        assert "passport_number" in missing
        assert "passport_expiry" in missing
        assert "passport_country" in missing

    def test_no_passport_required(self) -> None:
        ti = TravelerInfo(
            first_name="Robin",
            last_name="Zieme",
            date_of_birth=date(1990, 1, 1),
            email="r@example.com",
            phone="+1234",
        )
        missing = ti.missing_required_fields(require_passport=False)
        assert missing == []

    def test_is_complete(self) -> None:
        ti = TravelerInfo(
            first_name="Robin",
            last_name="Zieme",
            date_of_birth=date(1990, 1, 1),
            email="r@example.com",
            phone="+1234",
            passport_number="AB123",
            passport_expiry=date(2030, 1, 1),
            passport_country="DE",
        )
        assert ti.is_complete(require_passport=True) is True
        assert ti.missing_required_fields() == []


class TestPassportExpiry:
    def test_valid_passport(self) -> None:
        ti = TravelerInfo(passport_expiry=date(2030, 12, 31))
        result = ti.validate_passport_expiry(departure=date(2026, 6, 1))
        assert result is None  # valid

    def test_expired_passport(self) -> None:
        ti = TravelerInfo(passport_expiry=date(2026, 8, 1))
        result = ti.validate_passport_expiry(departure=date(2026, 6, 1))
        assert result is not None
        assert "must be valid until" in result

    def test_no_expiry(self) -> None:
        ti = TravelerInfo()
        result = ti.validate_passport_expiry(departure=date(2026, 6, 1))
        assert result is not None
        assert "required" in result
