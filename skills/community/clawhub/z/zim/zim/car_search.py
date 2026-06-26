"""Car rental search module for Zim.

Builds structured CarResult objects with affiliate deeplinks to
Rentalcars, Kayak, Discover Cars, Economy Bookings, and Kiwi Cars.

Travelpayouts does not have a dedicated car rental API, and neither do
Booking.com or SerpApi in a structured way. Results therefore use
deeplinks with class-based estimated daily rates so that ranking,
policy checks, and total price calculation function correctly.
Prices are estimates — final prices appear on the provider's site.
"""

from __future__ import annotations

import logging
from datetime import date
from urllib.parse import quote

from zim.core import CarResult, Policy, apply_policy_to_car
from zim.providers.travelpayouts import _get_marker

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Estimated daily rental rates (USD) by vehicle class
# ---------------------------------------------------------------------------

_CLASS_DAILY_RATE: dict[str, float] = {
    "economy": 35.0,
    "compact": 45.0,
    "intermediate": 52.0,
    "standard": 58.0,
    "fullsize": 65.0,
    "suv": 75.0,
    "luxury": 95.0,
    "van": 85.0,
    "minivan": 85.0,
    "any": 50.0,
}

_DEFAULT_DAILY_RATE = 50.0


def _estimate_total(car_class: str | None, pickup: date, dropoff: date) -> float:
    """Return an estimated rental total (USD) for the given class and period."""
    days = max((dropoff - pickup).days, 1)
    daily = _CLASS_DAILY_RATE.get((car_class or "any").lower(), _DEFAULT_DAILY_RATE)
    return round(daily * days, 2)


# ---------------------------------------------------------------------------
# Deeplink builders
# ---------------------------------------------------------------------------

def _build_rentalcars_link(
    location: str,
    pickup: date,
    dropoff: date,
) -> str:
    """Build Rentalcars affiliate search deeplink."""
    marker = _get_marker()
    encoded = quote(location)
    return (
        f"https://www.rentalcars.com/search"
        f"?location={encoded}"
        f"&puDay={pickup.day}&puMonth={pickup.month}&puYear={pickup.year}"
        f"&doDay={dropoff.day}&doMonth={dropoff.month}&doYear={dropoff.year}"
        f"&driversAge=30"
        f"&affiliateCode={marker}"
    )


def _build_kayak_link(
    location: str,
    pickup: date,
    dropoff: date,
) -> str:
    """Build Kayak car search deeplink."""
    encoded = quote(location)
    return (
        f"https://www.kayak.com/cars/{encoded}"
        f"/{pickup.isoformat()}/{dropoff.isoformat()}"
        f"?sort=price_a"
    )


def _build_discover_cars_link(
    location: str,
    pickup: date,
    dropoff: date,
) -> str:
    """Build Discover Cars affiliate search deeplink."""
    marker = _get_marker()
    encoded = quote(location)
    return (
        f"https://www.discovercars.com/search"
        f"?location={encoded}"
        f"&pick_up_date={pickup.isoformat()}"
        f"&drop_off_date={dropoff.isoformat()}"
        f"&marker={marker}"
    )


def _build_economy_bookings_link(
    location: str,
    pickup: date,
    dropoff: date,
) -> str:
    """Build Economy Bookings search deeplink."""
    encoded = quote(location)
    return (
        f"https://www.economybookings.com/search"
        f"?location={encoded}"
        f"&pick_up={pickup.isoformat()}"
        f"&drop_off={dropoff.isoformat()}"
    )


def _build_kiwi_cars_link(
    location: str,
    pickup: date,
    dropoff: date,
) -> str:
    """Build Kiwi.com car rental search deeplink."""
    encoded = quote(location)
    return (
        f"https://www.kiwi.com/en/cars/{encoded}"
        f"?pickup={pickup.isoformat()}&dropoff={dropoff.isoformat()}"
    )


# ---------------------------------------------------------------------------
# Public search entrypoint
# ---------------------------------------------------------------------------

def search(
    location: str,
    pickup: date,
    dropoff: date,
    car_class: str | None = None,
    policy: Policy | None = None,
) -> list[CarResult]:
    """Search car rentals and return structured results with affiliate deeplinks.

    Returns five provider options (Rentalcars, Kayak, Discover Cars,
    Economy Bookings, Kiwi Cars) with class-based estimated total prices
    so that ranking and total price calculation function correctly.
    Prices are estimates — final prices appear on each provider's site.

    Args:
        location: Pickup city or airport name.
        pickup: Pickup date.
        dropoff: Drop-off date.
        car_class: Optional vehicle class filter.
        policy: Optional travel policy for annotations.

    Returns:
        List of CarResult objects with estimated prices and affiliate links.
    """
    vehicle = car_class or "any"
    days = max((dropoff - pickup).days, 1)
    base_total = _estimate_total(car_class, pickup, dropoff)
    logger.debug(
        "Car search %s (%s): %d days, base est. $%.0f total",
        location, vehicle, days, base_total,
    )

    results: list[CarResult] = [
        # Rentalcars — strong free-cancellation policy, standard rate
        CarResult(
            provider="Rentalcars",
            vehicle_class=vehicle,
            pickup_location=location,
            link=_build_rentalcars_link(location, pickup, dropoff),
            free_cancellation=True,
            price_usd_total=base_total,
        ),
        # Kayak — meta-search, slight discount
        CarResult(
            provider="Kayak",
            vehicle_class=vehicle,
            pickup_location=location,
            link=_build_kayak_link(location, pickup, dropoff),
            free_cancellation=False,
            price_usd_total=round(base_total * 0.92, 2),
        ),
        # Discover Cars — free cancellation, slight discount
        CarResult(
            provider="Discover Cars",
            vehicle_class=vehicle,
            pickup_location=location,
            link=_build_discover_cars_link(location, pickup, dropoff),
            free_cancellation=True,
            price_usd_total=round(base_total * 0.95, 2),
        ),
        # Economy Bookings — budget tier, no free cancel
        CarResult(
            provider="Economy Bookings",
            vehicle_class=vehicle,
            pickup_location=location,
            link=_build_economy_bookings_link(location, pickup, dropoff),
            free_cancellation=False,
            price_usd_total=round(base_total * 0.85, 2),
        ),
        # Kiwi Cars — bundled travel option via Kiwi.com
        CarResult(
            provider="Kiwi Cars",
            vehicle_class=vehicle,
            pickup_location=location,
            link=_build_kiwi_cars_link(location, pickup, dropoff),
            free_cancellation=False,
            price_usd_total=round(base_total * 0.90, 2),
        ),
    ]

    # Apply policy annotations
    if policy:
        results = [apply_policy_to_car(r, policy) for r in results]

    return results
