"""Traveler information capture and validation for booking execution.

Collects the PII required by airlines and hotels to issue tickets and
confirm reservations: legal name, date of birth, passport, contact info.
"""

from __future__ import annotations

import re
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class TravelerInfo(BaseModel):
    """Information required to execute a booking with a travel provider.

    All fields are optional initially — the booking state machine moves
    to ``needs_traveler_info`` when required fields are missing and to
    ``ready_for_payment`` once validation passes.
    """

    # Legal identity
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None  # M / F / X — IATA standard

    # Passport / travel document
    passport_number: Optional[str] = None
    passport_expiry: Optional[date] = None
    passport_country: Optional[str] = None  # ISO-3166-1 alpha-2

    # Contact
    email: Optional[str] = None
    phone: Optional[str] = None

    # Loyalty / frequent flyer
    frequent_flyer: dict[str, str] = Field(
        default_factory=dict,
        description="Airline IATA code → FF number mapping",
    )

    # -------------------------------------------------------------------
    # Validators
    # -------------------------------------------------------------------

    @field_validator("gender")
    @classmethod
    def _validate_gender(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.upper().strip()
        if v not in ("M", "F", "X"):
            raise ValueError(f"Gender must be M, F, or X — got '{v}'")
        return v

    @field_validator("email")
    @classmethod
    def _validate_email(cls, v: str | None) -> str | None:
        if v is None:
            return None
        # Lightweight check — not RFC-5321 exhaustive
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", v):
            raise ValueError(f"Invalid email address: {v}")
        return v.lower().strip()

    @field_validator("passport_country")
    @classmethod
    def _validate_country(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.upper().strip()
        if len(v) != 2 or not v.isalpha():
            raise ValueError(f"Country must be ISO-3166-1 alpha-2 — got '{v}'")
        return v

    # -------------------------------------------------------------------
    # Completeness checks
    # -------------------------------------------------------------------

    def missing_required_fields(self, require_passport: bool = True) -> list[str]:
        """Return a list of field names that are required but still empty.

        Args:
            require_passport: Whether passport fields are required
                (international flights need them; domestic may not).
        """
        missing: list[str] = []

        if not self.first_name:
            missing.append("first_name")
        if not self.last_name:
            missing.append("last_name")
        if not self.date_of_birth:
            missing.append("date_of_birth")
        if not self.email:
            missing.append("email")
        if not self.phone:
            missing.append("phone")

        if require_passport:
            if not self.passport_number:
                missing.append("passport_number")
            if not self.passport_expiry:
                missing.append("passport_expiry")
            if not self.passport_country:
                missing.append("passport_country")

        return missing

    def is_complete(self, require_passport: bool = True) -> bool:
        """Return True if all required fields are populated."""
        return len(self.missing_required_fields(require_passport)) == 0

    def validate_passport_expiry(self, departure: date, min_months: int = 6) -> str | None:
        """Check that passport is valid for at least ``min_months`` after departure.

        Returns an error message string, or None if valid.
        """
        if not self.passport_expiry:
            return "Passport expiry date is required"

        from dateutil.relativedelta import relativedelta

        required_expiry = departure + relativedelta(months=min_months)
        if self.passport_expiry < required_expiry:
            return (
                f"Passport expires {self.passport_expiry.isoformat()} — "
                f"must be valid until at least {required_expiry.isoformat()} "
                f"({min_months} months after departure)"
            )
        return None
