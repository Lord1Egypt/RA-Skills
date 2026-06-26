"""Zim CLI — Click-based command-line interface for travel search.

Entry point: ``python -m zim`` or ``zim`` (if installed via pip).

All subcommands output structured JSON to stdout for agent consumption.
"""

from __future__ import annotations

import json
import sys
from datetime import date, datetime

import click

from zim import __version__
from zim.approval import generate_approval_summary
from zim.core import Constraints, Policy, TravelPreferences
from zim.trip import plan_trip, plan_trip_with_scores


def _json_serializer(obj: object) -> str:
    """JSON serializer for objects not natively serializable."""
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def _output(data: object) -> None:
    """Print a Pydantic model or dict as formatted JSON."""
    if hasattr(data, "model_dump"):
        raw = data.model_dump()  # type: ignore[union-attr]
    elif isinstance(data, list):
        raw = [
            item.model_dump() if hasattr(item, "model_dump") else item
            for item in data
        ]
    else:
        raw = data
    click.echo(json.dumps(raw, indent=2, default=_json_serializer))


def _parse_date(value: str) -> date:
    """Parse a date string in YYYY-MM-DD format."""
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise click.BadParameter(f"Invalid date format: {value}. Use YYYY-MM-DD.")


# ---------------------------------------------------------------------------
# CLI Group
# ---------------------------------------------------------------------------

@click.group()
@click.version_option(__version__, prog_name="zim")
def cli() -> None:
    """Zim — Agent travel middleware.

    Search flights, hotels, and cars with policy awareness.
    All output is structured JSON for agent consumption.
    """
    pass


# ---------------------------------------------------------------------------
# Flights
# ---------------------------------------------------------------------------

@cli.command()
@click.argument("origin")
@click.argument("destination")
@click.argument("departure")
@click.option("--return-date", "-r", default=None, help="Return date (YYYY-MM-DD)")
@click.option("--currency", "-c", default="USD", help="Price currency")
@click.option("--limit", "-l", default=10, type=int, help="Max results")
@click.option("--cabin", default=None, help="Cabin class: economy/business/first")
@click.option("--direct-only", is_flag=True, help="Non-stop flights only")
@click.option("--max-price", type=float, default=None, help="Max flight price for policy")
@click.option("--policy/--no-policy", default=False, help="Apply saved policy")
def flights(
    origin: str,
    destination: str,
    departure: str,
    return_date: str | None,
    currency: str,
    limit: int,
    cabin: str | None,
    direct_only: bool,
    max_price: float | None,
    policy: bool,
) -> None:
    """Search flights between two airports.

    \b
    Example:
      zim flights LHR DXB 2026-04-15 -r 2026-04-20 --cabin business
    """
    from zim import flight_search, memory

    dep_date = _parse_date(departure)
    ret_date = _parse_date(return_date) if return_date else None

    pol = None
    if policy:
        pol = memory.load_policy()
    elif max_price is not None:
        pol = Policy(max_flight=max_price)

    constraints = None
    if cabin or direct_only:
        constraints = Constraints(
            cabin_class=cabin,
            direct_only=direct_only,
        )

    results = flight_search.search(
        origin=origin,
        destination=destination,
        departure=dep_date,
        return_date=ret_date,
        currency=currency,
        limit=limit,
        policy=pol,
        constraints=constraints,
    )

    _output(results)


# ---------------------------------------------------------------------------
# Hotels
# ---------------------------------------------------------------------------

@cli.command()
@click.argument("location")
@click.argument("checkin")
@click.argument("checkout")
@click.option("--currency", "-c", default="USD", help="Price currency")
@click.option("--adults", default=2, type=int, help="Number of adults")
@click.option("--stars-min", default=0, type=int, help="Minimum star rating")
@click.option("--policy/--no-policy", default=False, help="Apply saved policy")
def hotels(
    location: str,
    checkin: str,
    checkout: str,
    currency: str,
    adults: int,
    stars_min: int,
    policy: bool,
) -> None:
    """Search hotels in a location.

    \b
    Example:
      zim hotels Dubai 2026-04-15 2026-04-20 --stars-min 4
    """
    from zim import hotel_search, memory

    ci = _parse_date(checkin)
    co = _parse_date(checkout)

    pol = memory.load_policy() if policy else None

    results = hotel_search.search(
        location=location,
        checkin=ci,
        checkout=co,
        currency=currency,
        adults=adults,
        policy=pol,
        stars_min=stars_min,
    )

    _output(results)


# ---------------------------------------------------------------------------
# Cars
# ---------------------------------------------------------------------------

@cli.command()
@click.argument("location")
@click.argument("pickup")
@click.argument("dropoff")
@click.option("--car-class", default=None, help="Vehicle class: economy/compact/suv/luxury")
@click.option("--policy/--no-policy", default=False, help="Apply saved policy")
def cars(
    location: str,
    pickup: str,
    dropoff: str,
    car_class: str | None,
    policy: bool,
) -> None:
    """Search car rentals at a location.

    \b
    Example:
      zim cars Dubai 2026-04-15 2026-04-20 --car-class suv
    """
    from zim import car_search, memory

    pu = _parse_date(pickup)
    do = _parse_date(dropoff)

    pol = memory.load_policy() if policy else None

    results = car_search.search(
        location=location,
        pickup=pu,
        dropoff=do,
        car_class=car_class,
        policy=pol,
    )

    _output(results)


# ---------------------------------------------------------------------------
# Trip (full itinerary assembly)
# ---------------------------------------------------------------------------

@cli.command()
@click.argument("origin")
@click.argument("destination")
@click.argument("departure")
@click.option("--return-date", "-r", default=None, help="Return date (YYYY-MM-DD)")
@click.option("--mode", default="personal", type=click.Choice(["business", "personal"]))
@click.option("--purpose", default=None, help="Trip purpose")
@click.option("--meeting-location", default=None, help="Meeting location/address for hotel ranking")
@click.option("--budget", type=float, default=None, help="Budget / approval threshold override")
@click.option("--traveler", default="default", help="Traveler profile ID")
@click.option("--human", is_flag=True, help="Output a human-readable trip summary")
@click.option("--approval", is_flag=True, help="Output a WhatsApp-ready approval summary")
def trip(
    origin: str,
    destination: str,
    departure: str,
    return_date: str | None,
    mode: str,
    purpose: str | None,
    meeting_location: str | None,
    budget: float | None,
    traveler: str,
    human: bool,
    approval: bool,
) -> None:
    """Plan a full trip itinerary (flights + hotels + cars).

    \b
    Example:
      zim trip London Dubai 2026-04-15 -r 2026-04-20 --mode business --meeting-location DIFC
    """
    dep_date = _parse_date(departure)
    ret_date = _parse_date(return_date) if return_date else None

    itinerary, flight_scores, hotel_scores, car_scores = plan_trip_with_scores(
        origin=origin,
        destination=destination,
        departure=dep_date,
        return_date=ret_date,
        mode=mode,
        purpose=purpose,
        meeting_location=meeting_location,
        budget=budget,
        traveler_id=traveler,
    )

    if approval:
        click.echo(generate_approval_summary(itinerary, flight_scores, hotel_scores, car_scores))
        return

    if human:
        lines: list[str] = []
        lines.append(f"Trip to {itinerary.destination} ({itinerary.mode})")
        lines.append(f"Dates: {itinerary.dates.get('departure')}" + (f" → {itinerary.dates.get('return')}" if itinerary.dates.get('return') else ""))
        lines.append(f"Status: {itinerary.status}")
        lines.append(f"Total: ${itinerary.total_price_usd:,.2f}")
        lines.append("")

        if itinerary.flights:
            flight = itinerary.flights[0]
            reason = flight_scores[0].rank_reason if flight_scores else ""
            lines.append("Flight:")
            lines.append(f"  {flight.airline or 'Unknown'} {flight.flight_number} | {flight.origin} → {flight.destination} | ${flight.price_usd:,.2f}")
            if reason:
                lines.append(f"  Why: {reason}")
            if flight.link:
                lines.append(f"  Link: {flight.link}")
            lines.append("")

        if itinerary.hotels:
            hotel = itinerary.hotels[0]
            reason = hotel_scores[0].rank_reason if hotel_scores else ""
            lines.append("Hotel:")
            lines.append(f"  {hotel.name} | ${hotel.nightly_rate_usd:,.2f}/night")
            if reason:
                lines.append(f"  Why: {reason}")
            if hotel.link:
                lines.append(f"  Link: {hotel.link}")
            lines.append("")

        if itinerary.cars:
            car = itinerary.cars[0]
            reason = car_scores[0].rank_reason if car_scores else ""
            lines.append("Car:")
            lines.append(f"  {car.provider} {car.vehicle_class} | ${car.price_usd_total:,.2f}")
            if reason:
                lines.append(f"  Why: {reason}")
            if car.link:
                lines.append(f"  Link: {car.link}")

        click.echo("\n".join(lines))
        return

    _output(itinerary)


# ---------------------------------------------------------------------------
# Preferences management
# ---------------------------------------------------------------------------

@cli.group()
def preferences() -> None:
    """Manage traveler preferences."""
    pass


@preferences.command("show")
@click.option("--traveler", default="default", help="Traveler profile ID")
def preferences_show(traveler: str) -> None:
    """Show current traveler preferences."""
    from zim import memory

    prefs = memory.load_preferences(traveler)
    _output(prefs)


@preferences.command("set")
@click.option("--seat", type=click.Choice(["window", "aisle", "any"]), default=None)
@click.option("--airlines", default=None, help="Comma-separated preferred airline IATA codes")
@click.option("--no-redeye/--allow-redeye", default=None, help="Avoid red-eye flights")
@click.option("--hotel-style", default=None, help="Hotel style: luxury/boutique/business/budget")
@click.option("--hotel-stars-min", type=int, default=None)
@click.option("--car-class", default=None, help="Car class: economy/compact/suv/luxury/van")
@click.option("--traveler", default="default", help="Traveler profile ID")
def preferences_set(
    seat: str | None,
    airlines: str | None,
    no_redeye: bool | None,
    hotel_style: str | None,
    hotel_stars_min: int | None,
    car_class: str | None,
    traveler: str,
) -> None:
    """Update traveler preferences (merges with existing)."""
    from zim import memory

    prefs = memory.load_preferences(traveler)

    if seat is not None:
        prefs.seat = seat
    if airlines is not None:
        prefs.airlines = [a.strip().upper() for a in airlines.split(",") if a.strip()]
    if no_redeye is not None:
        prefs.no_red_eye = no_redeye
    if hotel_style is not None:
        prefs.hotel_style = hotel_style
    if hotel_stars_min is not None:
        prefs.hotel_stars_min = hotel_stars_min
    if car_class is not None:
        prefs.car_class = car_class

    path = memory.save_preferences(prefs, traveler)
    click.echo(f"Preferences saved to {path}")
    _output(prefs)


@preferences.command("clear")
@click.option("--traveler", default="default", help="Traveler profile ID")
def preferences_clear(traveler: str) -> None:
    """Reset traveler preferences to defaults."""
    from zim import memory

    prefs = TravelPreferences()
    path = memory.save_preferences(prefs, traveler)
    click.echo(f"Preferences cleared at {path}")
    _output(prefs)


# ---------------------------------------------------------------------------
# Policy management
# ---------------------------------------------------------------------------

@cli.group()
def policy() -> None:
    """Manage travel policy."""
    pass


@policy.command("show")
@click.option("--traveler", default="default", help="Traveler profile ID")
def policy_show(traveler: str) -> None:
    """Show current travel policy."""
    from zim import memory

    pol = memory.load_policy(traveler)
    _output(pol)


@policy.command("set")
@click.option("--max-hotel", type=float, default=None, help="Max hotel nightly rate (USD)")
@click.option("--max-flight", type=float, default=None, help="Max flight price (USD)")
@click.option("--approval-threshold", type=float, default=None, help="Total trip approval threshold (USD)")
@click.option("--approved-airlines", default=None, help="Comma-separated approved airline codes")
@click.option("--direct-only/--allow-connections", default=None)
@click.option("--refundable/--non-refundable", default=None)
@click.option("--traveler", default="default", help="Traveler profile ID")
def policy_set(
    max_hotel: float | None,
    max_flight: float | None,
    approval_threshold: float | None,
    approved_airlines: str | None,
    direct_only: bool | None,
    refundable: bool | None,
    traveler: str,
) -> None:
    """Update travel policy (merges with existing)."""
    from zim import memory

    pol = memory.load_policy(traveler)

    if max_hotel is not None:
        pol.max_hotel_night = max_hotel
    if max_flight is not None:
        pol.max_flight = max_flight
    if approval_threshold is not None:
        pol.approval_threshold = approval_threshold
    if approved_airlines is not None:
        pol.approved_airlines = [a.strip().upper() for a in approved_airlines.split(",") if a.strip()]
    if direct_only is not None:
        pol.direct_only = direct_only
    if refundable is not None:
        pol.refundable_preferred = refundable

    path = memory.save_policy(pol, traveler)
    click.echo(f"Policy saved to {path}")
    _output(pol)


if __name__ == "__main__":
    cli()
