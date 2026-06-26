"""Zim FastAPI middleware API.

Exposes the Zim travel orchestration engine as an HTTP API for
agent-to-agent integration. Experience agents call these endpoints
to search, select, approve, and execute travel bookings.

Run with: uvicorn zim.api:app --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

import base64
import contextvars
import hashlib
import hmac
import logging
import os
import urllib.parse
import uuid
from datetime import date
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette.middleware.base import BaseHTTPMiddleware

from zim import __version__
from zim.fee_store import FeeStore
from zim.fees import DEFAULT_FEE_SCHEDULE, FeeSchedule, calculate_fee
from zim.policy_store import PolicyStore, StoredPolicy
from zim.request_state import (
    FulfillmentState,
    InvalidTransitionError,
    PaymentState,
    RequestState,
    TravelRequest,
)
from zim.request_store import RequestStore
from zim.tenant import Tenant, TenantSettings
from zim.tenant_store import TenantStore
from zim.traveler_store import Traveler, TravelerStore
from zim.trip_store import TripRecord, TripStore
from zim.webhook_store import WebhookEventStore

# ---------------------------------------------------------------------------
# Structured logging with request_id correlation
# ---------------------------------------------------------------------------

_request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default=""
)


class _RequestIdFilter(logging.Filter):
    """Inject the current request_id into every log record."""

    def filter(self, record: logging.LogRecord) -> bool:  # noqa: A003
        record.request_id = _request_id_var.get("")  # type: ignore[attr-defined]
        return True


_handler = logging.StreamHandler()
_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] [req=%(request_id)s] %(message)s"
    )
)
_handler.addFilter(_RequestIdFilter())

logger = logging.getLogger(__name__)
if not logger.handlers:
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)


# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Zim Travel Middleware",
    description="Agent-to-agent travel orchestration API",
    version=__version__,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_store = RequestStore(os.environ.get("ZIM_REQUESTS_DB", "/tmp/zim_requests.db"))
_trip_store = TripStore(os.environ.get("ZIM_TRIPS_DB", "/tmp/zim_trips.db"))
_webhook_store = WebhookEventStore(os.environ.get("ZIM_WEBHOOKS_DB", "/tmp/zim_webhooks.db"))
_tenant_store = TenantStore(os.environ.get("ZIM_TENANTS_DB", "/tmp/zim_tenants.db"))
_policy_store = PolicyStore(os.environ.get("ZIM_POLICIES_DB", "/tmp/zim_policies.db"))
_traveler_store = TravelerStore(os.environ.get("ZIM_TRAVELERS_DB", "/tmp/zim_travelers.db"))
_fee_store = FeeStore(os.environ.get("ZIM_FEES_DB", "/tmp/zim_fees.db"))

# WhatsApp agent (module-level singleton with SQLite-backed state)
from zim.state_store import SQLiteStateStore  # noqa: E402
from zim.whatsapp_agent import ZimWhatsAppAgent  # noqa: E402

_whatsapp_agent = ZimWhatsAppAgent(
    default_traveler_id=os.environ.get("ZIM_TRAVELER_ID", "default"),
    state_store=SQLiteStateStore(),
)

# LLM-powered agent (used when OPENROUTER_API_KEY is set)
_llm_agent = None
try:
    if os.environ.get("OPENROUTER_API_KEY"):
        from zim.llm_agent import LLMWhatsAppAgent  # noqa: E402
        _llm_agent = LLMWhatsAppAgent()
        logger.info("Using LLM-powered WhatsApp agent")
except Exception:
    logger.warning("Failed to init LLM agent, falling back to keyword agent")

# Paths that skip auth and are always public
_PUBLIC_PATHS = {"/v1/health"}
_PUBLIC_PREFIXES = ("/v1/webhooks/",)


# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------


class _LoggingMiddleware(BaseHTTPMiddleware):
    """Assign a request_id to each request and log start/end."""

    async def dispatch(self, request: Request, call_next: Any) -> Any:
        rid = request.headers.get("X-Request-ID") or uuid.uuid4().hex[:16]
        token = _request_id_var.set(rid)
        try:
            logger.info("→ %s %s", request.method, request.url.path)
            response = await call_next(request)
            logger.info("← %s %s %d", request.method, request.url.path, response.status_code)
            response.headers["X-Request-ID"] = rid
            return response
        finally:
            _request_id_var.reset(token)


class _AuthMiddleware(BaseHTTPMiddleware):
    """Enforce Bearer token auth on all /v1/ routes except health and webhooks.

    Admin routes (/v1/admin/*) are checked against ZIM_ADMIN_KEY, falling back
    to ZIM_API_KEY if ZIM_ADMIN_KEY is not set.
    """

    async def dispatch(self, request: Request, call_next: Any) -> Any:
        path = request.url.path

        # Skip auth for public paths
        if path in _PUBLIC_PATHS or any(path.startswith(p) for p in _PUBLIC_PREFIXES):
            return await call_next(request)

        is_admin_path = path.startswith("/v1/admin/") or path == "/v1/admin"
        if is_admin_path:
            required_key = os.environ.get("ZIM_ADMIN_KEY") or os.environ.get("ZIM_API_KEY", "")
        else:
            required_key = os.environ.get("ZIM_API_KEY", "")

        if required_key:
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return JSONResponse(
                    {"detail": "Missing Authorization header (Bearer token required)"},
                    status_code=401,
                )
            if auth_header[7:] != required_key:
                return JSONResponse({"detail": "Invalid API key"}, status_code=401)

        return await call_next(request)


# Middleware is applied in LIFO order — logging wraps auth
app.add_middleware(_AuthMiddleware)
app.add_middleware(_LoggingMiddleware)


# ---------------------------------------------------------------------------
# Request / response schemas
# ---------------------------------------------------------------------------


class StructuredIntent(BaseModel):
    origin: Optional[str] = None
    destination: Optional[str] = None
    departure_date: Optional[str] = None
    return_date: Optional[str] = None
    travelers: int = 1
    cabin_class: Optional[str] = None
    hotel_destination: Optional[str] = None
    check_in: Optional[str] = None
    check_out: Optional[str] = None
    car_location: Optional[str] = None


class CreateRequestBody(BaseModel):
    tenant_id: str = "default"
    traveler_id: str = "default"
    intent: Optional[StructuredIntent] = None
    raw_message: Optional[str] = None
    auto_search: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)


class SelectOptionsBody(BaseModel):
    flight_index: Optional[int] = None
    hotel_index: Optional[int] = None
    car_index: Optional[int] = None


class TravelerInfoBody(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    passport_number: Optional[str] = None
    passport_expiry: Optional[str] = None
    passport_country: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    frequent_flyer: dict[str, str] = Field(default_factory=dict)


class ApprovalBody(BaseModel):
    decision: str  # approved | rejected | needs_changes
    notes: Optional[str] = None


class FulfillmentUpdateBody(BaseModel):
    fulfillment_state: str  # link_sent | confirmed | partially_confirmed | failed
    details: dict[str, Any] = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    detail: str
    request_id: Optional[str] = None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_fee_schedule(tenant_id: str) -> FeeSchedule:
    """Return the FeeSchedule for a tenant, falling back to the default."""
    if tenant_id and tenant_id != "default":
        tenant = _tenant_store.get(tenant_id)
        if tenant and tenant.settings.fee_config:
            try:
                return FeeSchedule.model_validate(tenant.settings.fee_config)
            except Exception as exc:
                logger.warning(
                    "Invalid fee_config for tenant %s, using default: %s", tenant_id, exc
                )
    return DEFAULT_FEE_SCHEDULE


def _attach_fee_breakdown(req: TravelRequest) -> None:
    """Compute and store fee_breakdown in req.metadata for ready_to_execute requests.

    Called whenever a request transitions to READY_TO_EXECUTE so the breakdown
    is available in GET /v1/requests/{id} before the user hits execute.
    """
    itinerary = req.itinerary or {}
    flights = itinerary.get("flights", [])
    hotels = itinerary.get("hotels", [])
    cars = itinerary.get("cars", [])
    nights = itinerary.get("dates", {}).get("nights", 1) or 1

    # Calculate subtotal the same way build_line_items_from_itinerary does
    subtotal = 0.0
    if flights:
        subtotal += flights[0].get("price_usd", 0.0)
    if hotels:
        subtotal += hotels[0].get("nightly_rate_usd", 0.0) * nights
    if cars:
        subtotal += cars[0].get("price_usd_total", 0.0)

    schedule = _get_fee_schedule(req.tenant_id)
    breakdown = calculate_fee(subtotal, schedule)
    req.metadata["fee_breakdown"] = breakdown.model_dump(mode="json")


def _get_request_or_404(request_id: str) -> TravelRequest:
    req = _store.get(request_id)
    if req is None:
        raise HTTPException(status_code=404, detail=f"Request {request_id} not found")
    return req


def _run_search(req: TravelRequest) -> TravelRequest:
    """Execute search using existing trip planning pipeline."""
    from zim.core import Constraints, Policy, TravelPreferences
    from zim.intent_parser import parse_travel_intent
    from zim.memory import load_policy, load_preferences
    from zim.trip import plan_trip_with_scores

    intent = req.parsed_intent

    # Parse NL if we only have raw_message
    if not intent and req.raw_message:
        intent = parse_travel_intent(req.raw_message)
        req.parsed_intent = intent

    if not intent:
        req.state = RequestState.FAILED
        req.metadata["error"] = "No intent could be parsed"
        _store.update(req)
        raise HTTPException(status_code=422, detail="Could not parse travel intent")

    # Transition to searching
    req.transition_to(RequestState.SEARCHING)
    _store.update(req)

    # Load traveler prefs and policy — tenant policy overrides the file-based default
    preferences = load_preferences(req.traveler_id)
    policy = load_policy(req.traveler_id)

    # If a tenant policy was wired in, temporarily save it so plan_trip_with_scores uses it
    if "_tenant_policy" in req.metadata:
        from zim.core import Policy as _Policy
        from zim.memory import save_policy as _save_policy
        try:
            _tenant_pol = _Policy.model_validate(req.metadata["_tenant_policy"])
            _save_policy(_tenant_pol, req.traveler_id)
            policy = _tenant_pol
        except Exception as exc:
            logger.warning("Failed to apply tenant policy override for request %s: %s", req.id, exc)

    travel_type = intent.get("travel_type", "flight")
    origin = intent.get("origin", "")
    destination = intent.get("destination", "")
    departure_str = intent.get("departure_date")
    return_str = intent.get("return_date")
    cabin_class = intent.get("cabin_class")
    hotel_destination = intent.get("hotel_destination")
    check_in_str = intent.get("check_in")
    check_out_str = intent.get("check_out")
    car_location = intent.get("car_location")

    # Parse dates
    departure = date.fromisoformat(departure_str) if departure_str else None
    return_date = date.fromisoformat(return_str) if return_str else None
    check_in = date.fromisoformat(check_in_str) if check_in_str else None
    check_out = date.fromisoformat(check_out_str) if check_out_str else None

    # Resolve origin/destination based on travel type
    effective_origin = origin or "???"
    effective_destination = destination or hotel_destination or car_location or "???"
    effective_departure = departure or check_in or date.today()
    effective_return = return_date or check_out

    try:
        itinerary, ranked_flights, ranked_hotels, ranked_cars = plan_trip_with_scores(
            origin=effective_origin,
            destination=effective_destination,
            departure=effective_departure,
            return_date=effective_return,
            mode="personal",
            traveler_id=req.traveler_id,
        )
    except Exception as exc:
        logger.error("Search failed for request %s: %s", req.id, exc)
        req.state = RequestState.FAILED
        req.metadata["error"] = str(exc)
        _store.update(req)
        raise HTTPException(status_code=500, detail=f"Search failed: {exc}")

    # Store results
    req.itinerary = itinerary.model_dump() if hasattr(itinerary, "model_dump") else itinerary
    req.ranked_scores = {
        "flights": [
            {"score": sr.score, "rank_reason": sr.rank_reason}
            for sr in ranked_flights
        ],
        "hotels": [
            {"score": sr.score, "rank_reason": sr.rank_reason}
            for sr in ranked_hotels
        ],
        "cars": [
            {"score": sr.score, "rank_reason": sr.rank_reason}
            for sr in ranked_cars
        ],
    }

    req.transition_to(RequestState.OPTIONS_READY)
    _store.update(req)
    logger.info("Search complete for request %s — %d flights, %d hotels, %d cars",
                req.id, len(ranked_flights), len(ranked_hotels), len(ranked_cars))
    return req


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/v1/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


# ---------------------------------------------------------------------------
# Dedicated search endpoints — lightweight, no request lifecycle overhead
# ---------------------------------------------------------------------------


@app.get("/v1/search/flights")
def search_flights(
    origin: str = Query(..., description="IATA origin code (e.g. LHR)"),
    destination: str = Query(..., description="IATA destination code (e.g. DXB)"),
    departure_date: str = Query(..., description="Departure date (YYYY-MM-DD)"),
    return_date: Optional[str] = Query(None, description="Return date (YYYY-MM-DD)"),
    currency: str = Query("USD"),
    limit: int = Query(10, ge=1, le=50),
) -> list[dict[str, Any]]:
    """Search flights directly without creating a travel request.

    Calls the Travelpayouts prices_for_dates API with a month-level
    fallback and a deeplink-only fallback. Returns ranked FlightResult
    objects as JSON.
    """
    from zim.airports import normalize_airport
    from zim.flight_search import search as _search_flights

    try:
        dep = date.fromisoformat(departure_date)
    except ValueError:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail=f"Invalid departure_date: {departure_date!r}")

    ret: date | None = None
    if return_date:
        try:
            ret = date.fromisoformat(return_date)
        except ValueError:
            from fastapi import HTTPException
            raise HTTPException(status_code=422, detail=f"Invalid return_date: {return_date!r}")

    origin_iata = normalize_airport(origin)
    dest_iata = normalize_airport(destination)

    results = _search_flights(
        origin=origin_iata,
        destination=dest_iata,
        departure=dep,
        return_date=ret,
        currency=currency,
        limit=limit,
    )
    logger.info(
        "Direct flight search %s→%s %s: %d results",
        origin_iata, dest_iata, departure_date, len(results),
    )
    return [r.model_dump(mode="json") for r in results]


@app.get("/v1/search/hotels")
def search_hotels(
    location: str = Query(..., description="City or destination name"),
    checkin: str = Query(..., description="Check-in date (YYYY-MM-DD)"),
    checkout: str = Query(..., description="Check-out date (YYYY-MM-DD)"),
    adults: int = Query(2, ge=1, le=8),
    currency: str = Query("USD"),
    stars_min: int = Query(0, ge=0, le=5),
) -> list[dict[str, Any]]:
    """Search hotels directly without creating a travel request.

    Returns structured HotelResult objects with destination-tier
    estimated nightly rates and affiliate deeplinks. Prices are
    estimates; final prices are shown on the provider's site.
    """
    from zim.hotel_search import search as _search_hotels

    try:
        ci = date.fromisoformat(checkin)
        co = date.fromisoformat(checkout)
    except ValueError as exc:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail=f"Invalid date: {exc}")

    if co <= ci:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail="checkout must be after checkin")

    results = _search_hotels(
        location=location,
        checkin=ci,
        checkout=co,
        currency=currency,
        adults=adults,
        stars_min=stars_min,
    )
    logger.info("Direct hotel search %s %s–%s: %d results", location, checkin, checkout, len(results))
    return [r.model_dump(mode="json") for r in results]


@app.get("/v1/search/cars")
def search_cars(
    location: str = Query(..., description="Pickup city or airport"),
    pickup: str = Query(..., description="Pickup date (YYYY-MM-DD)"),
    dropoff: str = Query(..., description="Drop-off date (YYYY-MM-DD)"),
    car_class: Optional[str] = Query(None, description="Vehicle class (economy/compact/suv/luxury/van)"),
) -> list[dict[str, Any]]:
    """Search car rentals directly without creating a travel request.

    Returns structured CarResult objects with class-based estimated
    total prices and affiliate deeplinks. Prices are estimates; final
    prices are shown on the provider's site.
    """
    from zim.car_search import search as _search_cars

    try:
        pu = date.fromisoformat(pickup)
        do = date.fromisoformat(dropoff)
    except ValueError as exc:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail=f"Invalid date: {exc}")

    if do <= pu:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail="dropoff must be after pickup")

    results = _search_cars(location=location, pickup=pu, dropoff=do, car_class=car_class)
    logger.info("Direct car search %s %s–%s: %d results", location, pickup, dropoff, len(results))
    return [r.model_dump(mode="json") for r in results]


@app.post("/v1/requests", status_code=201)
def create_request(body: CreateRequestBody) -> dict[str, Any]:
    """Create a new travel request.

    Accepts structured intent OR a raw natural-language message.
    If auto_search is True (default), search runs immediately.
    """
    if not body.intent and not body.raw_message:
        raise HTTPException(
            status_code=422,
            detail="Provide either 'intent' (structured) or 'raw_message' (natural language)",
        )

    parsed_intent: dict[str, Any] = {}

    if body.raw_message:
        from zim.intent_parser import parse_travel_intent
        parsed_intent = parse_travel_intent(body.raw_message)
    elif body.intent:
        parsed_intent = body.intent.model_dump(exclude_none=True)
        # Map structured fields to the internal intent format
        if "departure_date" in parsed_intent:
            parsed_intent["travel_type"] = "flight"
        if "hotel_destination" in parsed_intent and not parsed_intent.get("origin"):
            parsed_intent["travel_type"] = "hotel"
        if "car_location" in parsed_intent and not parsed_intent.get("origin"):
            parsed_intent["travel_type"] = "car"
        if not parsed_intent.get("travel_type"):
            parsed_intent["travel_type"] = "flight"

    req = TravelRequest(
        tenant_id=body.tenant_id,
        traveler_id=body.traveler_id,
        raw_message=body.raw_message,
        parsed_intent=parsed_intent,
        metadata=body.metadata,
    )

    # Wire tenant's default policy into the request metadata
    if body.tenant_id and body.tenant_id != "default":
        tenant = _tenant_store.get(body.tenant_id)
        if tenant and tenant.settings.default_policy_id:
            sp = _policy_store.get(tenant.settings.default_policy_id)
            if sp and not sp.is_deleted:
                req.metadata["_tenant_policy"] = sp.policy.model_dump()
                logger.debug(
                    "Applied tenant policy %s to request %s",
                    sp.id, req.id,
                )

    # Wire stored traveler info and preferences
    if body.traveler_id and body.traveler_id != "default":
        stored_traveler = _traveler_store.get(body.traveler_id)
        if stored_traveler and not stored_traveler.is_deleted:
            # Pre-populate traveler info from the directory
            if stored_traveler.passport_info or stored_traveler.email:
                base_info: dict[str, Any] = {}
                if stored_traveler.passport_info:
                    base_info.update(stored_traveler.passport_info)
                if stored_traveler.email and not base_info.get("email"):
                    base_info["email"] = stored_traveler.email
                if stored_traveler.phone and not base_info.get("phone"):
                    base_info["phone"] = stored_traveler.phone
                if stored_traveler.frequent_flyer and not base_info.get("frequent_flyer"):
                    base_info["frequent_flyer"] = stored_traveler.frequent_flyer
                req.traveler_info = base_info
            # Save preferences so plan_trip_with_scores picks them up
            from zim.memory import save_preferences
            save_preferences(stored_traveler.preferences, body.traveler_id)
            logger.debug(
                "Auto-populated traveler info for request %s from directory traveler %s",
                req.id, stored_traveler.id,
            )

    _store.create(req)
    logger.info("Created request %s for tenant=%s traveler=%s",
                req.id, req.tenant_id, req.traveler_id)

    if body.auto_search:
        req = _run_search(req)

    return req.model_dump(mode="json")


@app.get("/v1/requests/{request_id}")
def get_request(request_id: str) -> dict[str, Any]:
    """Get the full state of a travel request."""
    req = _get_request_or_404(request_id)
    return req.model_dump(mode="json")


@app.get("/v1/requests")
def list_requests(
    tenant_id: Optional[str] = Query(None),
    traveler_id: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> list[dict[str, Any]]:
    """List travel requests with optional filters."""
    # Validate state filter if provided
    if state is not None:
        valid_states = {s.value for s in RequestState}
        if state not in valid_states:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid state '{state}'. Valid states: {sorted(valid_states)}",
            )

    results = _store.list_requests(
        tenant_id=tenant_id,
        traveler_id=traveler_id,
        state=state,
        limit=limit,
        offset=offset,
    )
    return [r.model_dump(mode="json") for r in results]


@app.post("/v1/requests/{request_id}/search")
def search_request(request_id: str) -> dict[str, Any]:
    """Trigger search on a request that was created with auto_search=False.

    Only valid when the request is in 'intent_received' state.
    """
    req = _get_request_or_404(request_id)

    if req.state != RequestState.INTENT_RECEIVED:
        raise HTTPException(
            status_code=409,
            detail=(
                f"Cannot search in state '{req.state.value}'. "
                "Must be 'intent_received'."
            ),
        )

    req = _run_search(req)
    return req.model_dump(mode="json")


@app.post("/v1/requests/{request_id}/select")
def select_options(request_id: str, body: SelectOptionsBody) -> dict[str, Any]:
    """Select specific options from the search results."""
    req = _get_request_or_404(request_id)

    if req.state != RequestState.OPTIONS_READY:
        raise HTTPException(
            status_code=409,
            detail=f"Cannot select options in state '{req.state.value}'. Must be 'options_ready'.",
        )

    selections: dict[str, int] = {}
    if body.flight_index is not None:
        if body.flight_index < 0:
            raise HTTPException(status_code=422, detail="flight_index must be >= 0")
        selections["flight_index"] = body.flight_index
    if body.hotel_index is not None:
        if body.hotel_index < 0:
            raise HTTPException(status_code=422, detail="hotel_index must be >= 0")
        selections["hotel_index"] = body.hotel_index
    if body.car_index is not None:
        if body.car_index < 0:
            raise HTTPException(status_code=422, detail="car_index must be >= 0")
        selections["car_index"] = body.car_index

    if not selections:
        raise HTTPException(
            status_code=422,
            detail="Must select at least one option (flight_index, hotel_index, or car_index)",
        )

    req.selected_options = selections
    req.transition_to(RequestState.OPTION_SELECTED)

    # Check if traveler info is needed
    from zim.traveler_info import TravelerInfo
    info = TravelerInfo(**(req.traveler_info or {}))
    missing = info.missing_required_fields(require_passport=False)

    if missing:
        req.transition_to(RequestState.AWAITING_INFO)
        req.metadata["missing_traveler_fields"] = missing
    else:
        req.traveler_info = info.model_dump()
        # Check if approval is needed
        itinerary_status = (req.itinerary or {}).get("status", "booking_ready")
        if itinerary_status == "approval_required":
            req.transition_to(RequestState.AWAITING_APPROVAL)
        else:
            req.transition_to(RequestState.READY_TO_EXECUTE)
            _attach_fee_breakdown(req)

    _store.update(req)
    return req.model_dump(mode="json")


@app.post("/v1/requests/{request_id}/traveler-info")
def submit_traveler_info(request_id: str, body: TravelerInfoBody) -> dict[str, Any]:
    """Submit traveler details for a request."""
    req = _get_request_or_404(request_id)

    if req.state not in (RequestState.AWAITING_INFO, RequestState.OPTION_SELECTED):
        raise HTTPException(
            status_code=409,
            detail=f"Cannot submit traveler info in state '{req.state.value}'.",
        )

    from zim.traveler_info import TravelerInfo

    # Merge with existing info
    existing = req.traveler_info or {}
    updates = body.model_dump(exclude_none=True)
    existing.update(updates)

    try:
        info = TravelerInfo(**existing)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    req.traveler_info = info.model_dump()
    missing = info.missing_required_fields(require_passport=False)

    if missing:
        req.metadata["missing_traveler_fields"] = missing
    else:
        req.metadata.pop("missing_traveler_fields", None)
        # Advance state
        if req.state == RequestState.AWAITING_INFO:
            itinerary_status = (req.itinerary or {}).get("status", "booking_ready")
            if itinerary_status == "approval_required":
                req.transition_to(RequestState.AWAITING_APPROVAL)
            else:
                req.transition_to(RequestState.READY_TO_EXECUTE)
                _attach_fee_breakdown(req)

    _store.update(req)
    return req.model_dump(mode="json")


@app.post("/v1/requests/{request_id}/approve")
def approve_request(request_id: str, body: ApprovalBody) -> dict[str, Any]:
    """Submit an approval decision."""
    req = _get_request_or_404(request_id)

    if req.state != RequestState.AWAITING_APPROVAL:
        raise HTTPException(
            status_code=409,
            detail=f"Cannot approve in state '{req.state.value}'. Must be 'awaiting_approval'.",
        )

    if body.decision not in ("approved", "rejected", "needs_changes"):
        raise HTTPException(status_code=422, detail="Decision must be: approved, rejected, needs_changes")

    req.approval_decision = body.decision
    req.approval_notes = body.notes
    req.approval_id = req.approval_id or uuid.uuid4().hex[:12]

    if body.decision == "approved":
        req.transition_to(RequestState.READY_TO_EXECUTE)
        _attach_fee_breakdown(req)
    elif body.decision == "rejected":
        req.transition_to(RequestState.CANCELLED)
    elif body.decision == "needs_changes":
        req.transition_to(RequestState.OPTIONS_READY)

    _store.update(req)
    logger.info("Request %s approval decision: %s", req.id, body.decision)
    return req.model_dump(mode="json")


@app.post("/v1/requests/{request_id}/execute")
def execute_request(request_id: str) -> dict[str, Any]:
    """Trigger booking execution — creates Stripe checkout and runs executor."""
    req = _get_request_or_404(request_id)

    if req.state != RequestState.READY_TO_EXECUTE:
        raise HTTPException(
            status_code=409,
            detail=f"Cannot execute in state '{req.state.value}'. Must be 'ready_to_execute'.",
        )

    req.transition_to(RequestState.EXECUTING)
    _store.update(req)

    itinerary = req.itinerary or {}
    flights = itinerary.get("flights", [])
    hotels = itinerary.get("hotels", [])
    cars = itinerary.get("cars", [])
    nights = itinerary.get("dates", {}).get("nights", 1) or 1

    # Build Stripe checkout — gracefully skip if Stripe is not configured
    from zim.payment import StripeConfig, build_line_items_from_itinerary, create_checkout_session

    fee_schedule = _get_fee_schedule(req.tenant_id)
    line_items, fee_breakdown = build_line_items_from_itinerary(
        flights, hotels, cars, nights, fee_schedule=fee_schedule
    )

    # Always store the fee breakdown in metadata (visible even if Stripe is skipped)
    req.metadata["fee_breakdown"] = fee_breakdown.model_dump(mode="json")

    # Record the fee in the ledger
    _fee_store.record_fee(
        booking_id=req.id,
        tenant_id=req.tenant_id,
        subtotal_usd=fee_breakdown.subtotal_usd,
        fee_amount_usd=fee_breakdown.fee_amount_usd,
        fee_type=fee_breakdown.fee_type,
    )

    if line_items:
        config = StripeConfig.from_env()
        if not config.is_configured:
            logger.info("Stripe not configured for request %s — skipping payment step", req.id)
            req.metadata["payment_note"] = "Stripe not configured — payment skipped"
        else:
            try:
                email = (req.traveler_info or {}).get("email")
                result = create_checkout_session(
                    booking_id=req.id,
                    line_items=line_items,
                    customer_email=email,
                    config=config,
                    metadata={"tenant_id": req.tenant_id, "traveler_id": req.traveler_id},
                )
                req.payment_session_id = result.session_id
                req.checkout_url = result.checkout_url
                req.payment_state = PaymentState.AUTHORIZED
                logger.info("Stripe checkout session created for request %s: %s", req.id, result.session_id)
            except Exception as exc:
                logger.warning("Stripe checkout failed for request %s: %s", req.id, exc)
                req.metadata["payment_error"] = str(exc)
                req.metadata["payment_note"] = "Stripe checkout failed — proceeding without payment"

    # Run booking executor regardless of payment state
    from zim.booking_executor import BookingExecutionRequest, get_executor
    from zim.booking_store import save_booking

    executor = get_executor()
    execution_results = []

    selected = req.selected_options
    traveler = req.traveler_info or {}

    if flights and selected.get("flight_index") is not None:
        idx = selected["flight_index"]
        if 0 <= idx < len(flights):
            f = flights[idx]
            exec_req = BookingExecutionRequest(
                booking_id=f"{req.id}-flight",
                category="flight",
                provider_name=f.get("airline", ""),
                provider_link=f.get("link", ""),
                traveler_first_name=traveler.get("first_name", ""),
                traveler_last_name=traveler.get("last_name", ""),
                traveler_email=traveler.get("email", ""),
                origin=f.get("origin", ""),
                destination=f.get("destination", ""),
                departure_date=f.get("depart_at"),
            )
            result = executor.execute(exec_req)
            execution_results.append(result.model_dump())

    if hotels and selected.get("hotel_index") is not None:
        idx = selected["hotel_index"]
        if 0 <= idx < len(hotels):
            h = hotels[idx]
            exec_req = BookingExecutionRequest(
                booking_id=f"{req.id}-hotel",
                category="hotel",
                provider_name=h.get("name", ""),
                provider_link=h.get("link", ""),
                traveler_first_name=traveler.get("first_name", ""),
                traveler_last_name=traveler.get("last_name", ""),
                traveler_email=traveler.get("email", ""),
                destination=h.get("location", ""),
            )
            result = executor.execute(exec_req)
            execution_results.append(result.model_dump())

    if cars and selected.get("car_index") is not None:
        idx = selected["car_index"]
        if 0 <= idx < len(cars):
            c = cars[idx]
            exec_req = BookingExecutionRequest(
                booking_id=f"{req.id}-car",
                category="car",
                provider_name=c.get("provider", ""),
                provider_link=c.get("link", ""),
                traveler_first_name=traveler.get("first_name", ""),
                traveler_last_name=traveler.get("last_name", ""),
                traveler_email=traveler.get("email", ""),
            )
            result = executor.execute(exec_req)
            execution_results.append(result.model_dump())

    req.execution_results = execution_results
    req.fulfillment_state = FulfillmentState.LINK_SENT

    # Save booking record
    booking_record = {
        "booking_id": req.id,
        "tenant_id": req.tenant_id,
        "traveler_id": req.traveler_id,
        "itinerary": itinerary,
        "selected_options": req.selected_options,
        "traveler_info": req.traveler_info,
        "execution_results": execution_results,
        "payment_session_id": req.payment_session_id,
        "checkout_url": req.checkout_url,
    }
    save_booking(booking_record)

    req.transition_to(RequestState.COMPLETED)
    _store.update(req)

    # Create TripRecord
    booking_links = [
        r.get("provider_raw_response", {}).get("booking_link", "")
        for r in execution_results
        if r.get("provider_raw_response", {}).get("booking_link")
    ]
    confirmation_numbers = [
        r.get("provider_confirmation_code", "")
        for r in execution_results
        if r.get("provider_confirmation_code")
    ]
    trip_record = TripRecord(
        request_id=req.id,
        traveler_id=req.traveler_id,
        tenant_id=req.tenant_id,
        destination=itinerary.get("destination", ""),
        dates=itinerary.get("dates", {}),
        total_cost=itinerary.get("total_price_usd", 0.0),
        booking_links=booking_links,
        confirmation_numbers=confirmation_numbers,
        fulfillment_details=req.fulfillment_details,
    )
    _trip_store.create(trip_record)

    logger.info("Request %s executed successfully (%d bookings)", req.id, len(execution_results))
    return req.model_dump(mode="json")


@app.post("/v1/requests/{request_id}/cancel")
def cancel_request(request_id: str) -> dict[str, Any]:
    """Cancel a travel request."""
    req = _get_request_or_404(request_id)

    try:
        req.transition_to(RequestState.CANCELLED)
    except InvalidTransitionError:
        raise HTTPException(
            status_code=409,
            detail=f"Cannot cancel request in terminal state '{req.state.value}'.",
        )

    _store.update(req)
    logger.info("Request %s cancelled", req.id)
    return req.model_dump(mode="json")


# ---------------------------------------------------------------------------
# Twilio signature validation helper
# ---------------------------------------------------------------------------


def _twilio_signature_valid(
    auth_token: str,
    url: str,
    post_data: dict[str, str],
    x_twilio_signature: str,
) -> bool:
    """Validate a Twilio webhook request signature (HMAC-SHA1).

    See https://www.twilio.com/docs/usage/webhooks/webhooks-security
    """
    params_str = "".join(f"{k}{v}" for k, v in sorted(post_data.items()))
    signed = (url + params_str).encode("utf-8")
    expected = hmac.new(auth_token.encode("utf-8"), signed, hashlib.sha1).digest()
    expected_b64 = base64.b64encode(expected).decode("utf-8")
    return hmac.compare_digest(expected_b64, x_twilio_signature)


# ---------------------------------------------------------------------------
# Stripe webhook
# ---------------------------------------------------------------------------


@app.post("/v1/webhooks/stripe", status_code=200)
async def stripe_webhook(request: Request) -> dict[str, Any]:
    """Handle Stripe webhook events.

    Verifies the Stripe-Signature header when STRIPE_WEBHOOK_SECRET is set.
    Handles:
      - checkout.session.completed → PaymentState.PAID
      - payment_intent.succeeded   → PaymentState.PAID
      - checkout.session.expired   → PaymentState.FAILED
      - payment_intent.payment_failed → PaymentState.FAILED
      - charge.refunded            → PaymentState.REFUNDED

    Idempotent — duplicate event IDs are no-ops.
    """
    import json as _json

    import stripe

    from zim.payment import StripeConfig

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")
    config = StripeConfig.from_env()

    if config.webhook_secret:
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, config.webhook_secret
            )
        except stripe.error.SignatureVerificationError:
            logger.warning("Stripe webhook signature verification failed")
            raise HTTPException(status_code=400, detail="Invalid Stripe signature")
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"Webhook parse error: {exc}")
    else:
        # Dev mode — no signature verification
        try:
            event = _json.loads(payload)
        except _json.JSONDecodeError as exc:
            raise HTTPException(status_code=400, detail=f"Invalid JSON payload: {exc}")

    event_type = event["type"] if isinstance(event, dict) else event.type
    event_id = event.get("id", "") if isinstance(event, dict) else getattr(event, "id", "")

    # Idempotency check — skip already-processed events
    if event_id and not _webhook_store.mark_processed(event_id, event_type):
        logger.info("Stripe event %s (%s) already processed — skipping", event_id, event_type)
        return {"received": True, "event_type": event_type, "duplicate": True}

    data_obj = (
        event.get("data", {}).get("object", {})
        if isinstance(event, dict)
        else event.data.object
    )

    # Map event types to payment state transitions
    _PAID_EVENTS = {"checkout.session.completed", "payment_intent.succeeded"}
    _FAILED_EVENTS = {"checkout.session.expired", "payment_intent.payment_failed"}
    _REFUNDED_EVENTS = {"charge.refunded"}

    booking_id: Optional[str] = None
    new_payment_state: Optional[PaymentState] = None

    if event_type in _PAID_EVENTS:
        new_payment_state = PaymentState.PAID
    elif event_type in _FAILED_EVENTS:
        new_payment_state = PaymentState.FAILED
    elif event_type in _REFUNDED_EVENTS:
        new_payment_state = PaymentState.REFUNDED

    if new_payment_state is not None:
        metadata = (
            data_obj.get("metadata", {})
            if isinstance(data_obj, dict)
            else getattr(data_obj, "metadata", {}) or {}
        )
        booking_id = metadata.get("booking_id") if isinstance(metadata, dict) else None

        if booking_id:
            req = _store.get(booking_id)
            if req:
                req.payment_state = new_payment_state
                _store.update(req)
                logger.info(
                    "Payment state → %s for request %s via %s",
                    new_payment_state.value, booking_id, event_type,
                )
            else:
                logger.warning(
                    "Stripe event %s references unknown booking_id %s",
                    event_type, booking_id,
                )
    else:
        logger.debug("Ignoring Stripe event type: %s", event_type)

    return {"received": True, "event_type": event_type, "booking_id": booking_id}


# ---------------------------------------------------------------------------
# Twilio WhatsApp webhook
# ---------------------------------------------------------------------------


@app.post("/v1/webhooks/twilio/whatsapp", status_code=200)
async def twilio_whatsapp_webhook(request: Request) -> Any:
    """Handle inbound WhatsApp messages from Twilio.

    Validates the X-Twilio-Signature header, passes the message to
    ZimWhatsAppAgent, sends the reply via the Twilio Messages API, and
    returns an empty TwiML response to acknowledge receipt.

    This path is public (no Bearer auth) — it is covered by _PUBLIC_PREFIXES.
    """
    from fastapi.responses import Response as _Response

    from zim.twilio_client import send_whatsapp_message

    # Parse URL-encoded form body without requiring python-multipart
    raw_body = await request.body()
    form: dict[str, str] = dict(urllib.parse.parse_qsl(raw_body.decode("utf-8")))

    body_text = form.get("Body", "").strip()
    from_number = form.get("From", "").strip()

    if not from_number:
        logger.warning("Twilio WhatsApp webhook received with no From field")
        raise HTTPException(status_code=400, detail="Missing From field")

    # Validate Twilio signature when credentials are present
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN", "")
    if auth_token:
        sig = request.headers.get("X-Twilio-Signature", "")
        url = str(request.url)
        if not _twilio_signature_valid(auth_token, url, form, sig):
            logger.warning(
                "Twilio signature verification failed (from=%s)",
                from_number[:12] + "..." if len(from_number) > 12 else from_number,
            )
            raise HTTPException(status_code=403, detail="Invalid Twilio signature")
    else:
        logger.warning(
            "TWILIO_AUTH_TOKEN not set — skipping signature verification (dev mode)"
        )

    safe_from = from_number[:12] + "..." if len(from_number) > 12 else from_number
    logger.info("Inbound WhatsApp from %s (%d chars)", safe_from, len(body_text))

    # Process message through the WhatsApp agent
    try:
        _agent = _llm_agent or _whatsapp_agent
        reply = _agent.handle_message(body_text, from_number)
    except Exception as exc:
        logger.error("WhatsApp agent error for %s: %s", safe_from, exc)
        reply = "Sorry, something went wrong. Please try again in a moment."

    # Send reply via Twilio Messages API (fire-and-forget style with error logging)
    try:
        send_whatsapp_message(to=from_number, body=reply)
    except Exception as exc:
        logger.error("Failed to send WhatsApp reply to %s: %s", safe_from, exc)

    # Return empty TwiML to acknowledge receipt
    empty_twiml = '<?xml version="1.0" encoding="UTF-8"?><Response></Response>'
    return _Response(content=empty_twiml, media_type="text/xml; charset=utf-8")


# ---------------------------------------------------------------------------
# Payment status
# ---------------------------------------------------------------------------


@app.get("/v1/requests/{request_id}/payment-status")
def get_payment_status(request_id: str) -> dict[str, Any]:
    """Return current payment state and Stripe session details."""
    req = _get_request_or_404(request_id)

    result: dict[str, Any] = {
        "request_id": req.id,
        "payment_state": req.payment_state.value,
        "payment_session_id": req.payment_session_id,
        "checkout_url": req.checkout_url,
    }

    # Optionally fetch live session status from Stripe
    if req.payment_session_id:
        from zim.payment import StripeConfig, retrieve_session_status
        config = StripeConfig.from_env()
        if config.is_configured:
            try:
                session_data = retrieve_session_status(req.payment_session_id, config)
                result["stripe_session"] = session_data
            except Exception as exc:
                logger.warning("Could not retrieve Stripe session %s: %s", req.payment_session_id, exc)
                result["stripe_session_error"] = str(exc)

    return result


# ---------------------------------------------------------------------------
# Fulfillment tracking
# ---------------------------------------------------------------------------


@app.post("/v1/requests/{request_id}/fulfillment")
def update_fulfillment(request_id: str, body: FulfillmentUpdateBody) -> dict[str, Any]:
    """Update the fulfillment state of a completed request.

    Used to record external confirmations (e.g. when a provider sends a PNR).
    """
    req = _get_request_or_404(request_id)

    valid_states = {s.value for s in FulfillmentState}
    if body.fulfillment_state not in valid_states:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid fulfillment_state '{body.fulfillment_state}'. Valid: {sorted(valid_states)}",
        )

    req.fulfillment_state = FulfillmentState(body.fulfillment_state)
    if body.details:
        req.fulfillment_details.update(body.details)
    req.updated_at = __import__("datetime").datetime.now(
        __import__("datetime").timezone.utc
    ).isoformat()
    _store.update(req)

    # Also update the linked TripRecord if it exists
    trip = _trip_store.get_by_request(request_id)
    if trip and body.details:
        _trip_store.update_fulfillment(trip.trip_id, body.details)

    logger.info(
        "Fulfillment state → %s for request %s", body.fulfillment_state, request_id
    )
    return req.model_dump(mode="json")


# ---------------------------------------------------------------------------
# Trip records
# ---------------------------------------------------------------------------


@app.get("/v1/trips")
def list_trips(
    tenant_id: Optional[str] = Query(None),
    traveler_id: Optional[str] = Query(None),
    created_after: Optional[str] = Query(None),
    created_before: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> list[dict[str, Any]]:
    """List completed trip records with optional filters."""
    trips = _trip_store.list_trips(
        tenant_id=tenant_id,
        traveler_id=traveler_id,
        created_after=created_after,
        created_before=created_before,
        limit=limit,
        offset=offset,
    )
    return [t.model_dump(mode="json") for t in trips]


@app.get("/v1/trips/{trip_id}")
def get_trip(trip_id: str) -> dict[str, Any]:
    """Get full details of a trip record."""
    trip = _trip_store.get(trip_id)
    if trip is None:
        raise HTTPException(status_code=404, detail=f"Trip {trip_id} not found")
    return trip.model_dump(mode="json")


# ---------------------------------------------------------------------------
# Retry / re-search
# ---------------------------------------------------------------------------


@app.post("/v1/requests/{request_id}/retry")
def retry_request(request_id: str) -> dict[str, Any]:
    """Re-search a request from options_ready or failed state.

    Resets the request back to intent_received and triggers a new search.
    Only allowed from 'options_ready' or 'failed' state.
    """
    req = _get_request_or_404(request_id)

    if req.state not in (RequestState.OPTIONS_READY, RequestState.FAILED):
        raise HTTPException(
            status_code=409,
            detail=(
                f"Cannot retry from state '{req.state.value}'. "
                "Must be 'options_ready' or 'failed'."
            ),
        )

    # Clear previous search results
    req.itinerary = None
    req.ranked_scores = {}
    req.selected_options = {}
    req.execution_results = []
    req.metadata.pop("error", None)

    req.transition_to(RequestState.INTENT_RECEIVED)
    _store.update(req)

    # Trigger a new search
    req = _run_search(req)
    logger.info("Request %s retried — new search triggered", request_id)
    return req.model_dump(mode="json")


# ---------------------------------------------------------------------------
# Admin: request / response schemas
# ---------------------------------------------------------------------------


class CreateTenantBody(BaseModel):
    name: str
    domain: str = ""
    settings: Optional[dict[str, Any]] = None


class UpdateTenantBody(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    settings: Optional[dict[str, Any]] = None


class CreatePolicyBody(BaseModel):
    tenant_id: str = "default"
    name: str
    is_default: bool = False
    policy: dict[str, Any] = Field(default_factory=dict)


class UpdatePolicyBody(BaseModel):
    name: Optional[str] = None
    is_default: Optional[bool] = None
    policy: Optional[dict[str, Any]] = None


class CreateTravelerBody(BaseModel):
    tenant_id: str = "default"
    name: str
    email: str
    phone: Optional[str] = None
    preferences: dict[str, Any] = Field(default_factory=dict)
    frequent_flyer: dict[str, str] = Field(default_factory=dict)
    passport_info: dict[str, Any] = Field(default_factory=dict)


class UpdateTravelerBody(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    preferences: Optional[dict[str, Any]] = None
    frequent_flyer: Optional[dict[str, str]] = None
    passport_info: Optional[dict[str, Any]] = None


# ---------------------------------------------------------------------------
# Admin: Tenant endpoints
# ---------------------------------------------------------------------------


@app.post("/v1/admin/tenants", status_code=201)
def admin_create_tenant(body: CreateTenantBody) -> dict[str, Any]:
    """Create a new tenant."""
    settings_data = body.settings or {}
    try:
        settings = TenantSettings.model_validate(settings_data)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Invalid settings: {exc}")

    tenant = Tenant(name=body.name, domain=body.domain, settings=settings)
    _tenant_store.create(tenant)
    logger.info("Created tenant %s (%s)", tenant.id, tenant.name)
    return tenant.model_dump(mode="json")


@app.get("/v1/admin/tenants")
def admin_list_tenants(
    include_deleted: bool = Query(False),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> list[dict[str, Any]]:
    """List tenants."""
    tenants = _tenant_store.list_tenants(
        include_deleted=include_deleted, limit=limit, offset=offset
    )
    return [t.model_dump(mode="json") for t in tenants]


@app.get("/v1/admin/tenants/{tenant_id}")
def admin_get_tenant(tenant_id: str) -> dict[str, Any]:
    """Get a tenant by id."""
    tenant = _tenant_store.get(tenant_id)
    if tenant is None or tenant.is_deleted:
        raise HTTPException(status_code=404, detail=f"Tenant {tenant_id} not found")
    return tenant.model_dump(mode="json")


@app.put("/v1/admin/tenants/{tenant_id}")
def admin_update_tenant(tenant_id: str, body: UpdateTenantBody) -> dict[str, Any]:
    """Update a tenant."""
    tenant = _tenant_store.get(tenant_id)
    if tenant is None or tenant.is_deleted:
        raise HTTPException(status_code=404, detail=f"Tenant {tenant_id} not found")

    if body.name is not None:
        tenant.name = body.name
    if body.domain is not None:
        tenant.domain = body.domain
    if body.settings is not None:
        try:
            tenant.settings = TenantSettings.model_validate(body.settings)
        except Exception as exc:
            raise HTTPException(status_code=422, detail=f"Invalid settings: {exc}")

    from datetime import UTC as _UTC, datetime as _dt
    tenant.updated_at = _dt.now(_UTC).isoformat()
    _tenant_store.update(tenant)
    logger.info("Updated tenant %s", tenant_id)
    return tenant.model_dump(mode="json")


@app.delete("/v1/admin/tenants/{tenant_id}", status_code=200)
def admin_delete_tenant(tenant_id: str) -> dict[str, Any]:
    """Soft-delete a tenant."""
    tenant = _tenant_store.get(tenant_id)
    if tenant is None or tenant.is_deleted:
        raise HTTPException(status_code=404, detail=f"Tenant {tenant_id} not found")
    _tenant_store.soft_delete(tenant_id)
    logger.info("Soft-deleted tenant %s", tenant_id)
    return {"deleted": True, "tenant_id": tenant_id}


# ---------------------------------------------------------------------------
# Admin: Policy endpoints
# ---------------------------------------------------------------------------


@app.post("/v1/admin/policies", status_code=201)
def admin_create_policy(body: CreatePolicyBody) -> dict[str, Any]:
    """Create a new policy."""
    from zim.core import Policy as _Policy
    try:
        pol = _Policy.model_validate(body.policy)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Invalid policy: {exc}")

    stored = StoredPolicy(
        tenant_id=body.tenant_id,
        name=body.name,
        is_default=body.is_default,
        policy=pol,
    )
    _policy_store.create(stored)
    logger.info("Created policy %s (%s) for tenant %s", stored.id, stored.name, stored.tenant_id)
    return stored.model_dump(mode="json")


@app.get("/v1/admin/policies")
def admin_list_policies(
    tenant_id: Optional[str] = Query(None),
    include_deleted: bool = Query(False),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> list[dict[str, Any]]:
    """List policies, optionally filtered by tenant."""
    policies = _policy_store.list_policies(
        tenant_id=tenant_id,
        include_deleted=include_deleted,
        limit=limit,
        offset=offset,
    )
    return [p.model_dump(mode="json") for p in policies]


@app.get("/v1/admin/policies/{policy_id}")
def admin_get_policy(policy_id: str) -> dict[str, Any]:
    """Get a policy by id."""
    policy = _policy_store.get(policy_id)
    if policy is None or policy.is_deleted:
        raise HTTPException(status_code=404, detail=f"Policy {policy_id} not found")
    return policy.model_dump(mode="json")


@app.put("/v1/admin/policies/{policy_id}")
def admin_update_policy(policy_id: str, body: UpdatePolicyBody) -> dict[str, Any]:
    """Update a policy."""
    stored = _policy_store.get(policy_id)
    if stored is None or stored.is_deleted:
        raise HTTPException(status_code=404, detail=f"Policy {policy_id} not found")

    if body.name is not None:
        stored.name = body.name
    if body.is_default is not None:
        stored.is_default = body.is_default
    if body.policy is not None:
        from zim.core import Policy as _Policy
        try:
            stored.policy = _Policy.model_validate(body.policy)
        except Exception as exc:
            raise HTTPException(status_code=422, detail=f"Invalid policy: {exc}")

    from datetime import UTC as _UTC, datetime as _dt
    stored.updated_at = _dt.now(_UTC).isoformat()
    _policy_store.update(stored)
    logger.info("Updated policy %s", policy_id)
    return stored.model_dump(mode="json")


@app.delete("/v1/admin/policies/{policy_id}", status_code=200)
def admin_delete_policy(policy_id: str) -> dict[str, Any]:
    """Soft-delete a policy."""
    policy = _policy_store.get(policy_id)
    if policy is None or policy.is_deleted:
        raise HTTPException(status_code=404, detail=f"Policy {policy_id} not found")
    _policy_store.soft_delete(policy_id)
    logger.info("Soft-deleted policy %s", policy_id)
    return {"deleted": True, "policy_id": policy_id}


# ---------------------------------------------------------------------------
# Admin: Traveler directory endpoints
# ---------------------------------------------------------------------------


@app.post("/v1/admin/travelers", status_code=201)
def admin_create_traveler(body: CreateTravelerBody) -> dict[str, Any]:
    """Add a traveler to the directory."""
    from zim.core import TravelPreferences as _TravelPreferences
    try:
        prefs = _TravelPreferences.model_validate(body.preferences)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Invalid preferences: {exc}")

    traveler = Traveler(
        tenant_id=body.tenant_id,
        name=body.name,
        email=body.email,
        phone=body.phone,
        preferences=prefs,
        frequent_flyer=body.frequent_flyer,
        passport_info=body.passport_info,
    )
    _traveler_store.create(traveler)
    logger.info("Created traveler %s (%s) for tenant %s", traveler.id, traveler.email, traveler.tenant_id)
    return traveler.model_dump(mode="json")


@app.get("/v1/admin/travelers")
def admin_list_travelers(
    tenant_id: Optional[str] = Query(None),
    include_deleted: bool = Query(False),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> list[dict[str, Any]]:
    """List travelers, optionally filtered by tenant."""
    travelers = _traveler_store.list_travelers(
        tenant_id=tenant_id,
        include_deleted=include_deleted,
        limit=limit,
        offset=offset,
    )
    return [t.model_dump(mode="json") for t in travelers]


@app.get("/v1/admin/travelers/{traveler_id}")
def admin_get_traveler(traveler_id: str) -> dict[str, Any]:
    """Get a traveler by id."""
    traveler = _traveler_store.get(traveler_id)
    if traveler is None or traveler.is_deleted:
        raise HTTPException(status_code=404, detail=f"Traveler {traveler_id} not found")
    return traveler.model_dump(mode="json")


@app.put("/v1/admin/travelers/{traveler_id}")
def admin_update_traveler(traveler_id: str, body: UpdateTravelerBody) -> dict[str, Any]:
    """Update a traveler record."""
    traveler = _traveler_store.get(traveler_id)
    if traveler is None or traveler.is_deleted:
        raise HTTPException(status_code=404, detail=f"Traveler {traveler_id} not found")

    if body.name is not None:
        traveler.name = body.name
    if body.email is not None:
        traveler.email = body.email
    if body.phone is not None:
        traveler.phone = body.phone
    if body.preferences is not None:
        from zim.core import TravelPreferences as _TravelPreferences
        try:
            traveler.preferences = _TravelPreferences.model_validate(body.preferences)
        except Exception as exc:
            raise HTTPException(status_code=422, detail=f"Invalid preferences: {exc}")
    if body.frequent_flyer is not None:
        traveler.frequent_flyer = body.frequent_flyer
    if body.passport_info is not None:
        traveler.passport_info = body.passport_info

    from datetime import UTC as _UTC, datetime as _dt
    traveler.updated_at = _dt.now(_UTC).isoformat()
    _traveler_store.update(traveler)
    logger.info("Updated traveler %s", traveler_id)
    return traveler.model_dump(mode="json")


# ---------------------------------------------------------------------------
# Admin: Fee revenue reporting
# ---------------------------------------------------------------------------


@app.get("/v1/admin/fees/summary")
def admin_fees_summary(
    tenant_id: Optional[str] = Query(None, description="Filter by tenant ID"),
    since: Optional[str] = Query(None, description="ISO-8601 lower bound on created_at"),
    until: Optional[str] = Query(None, description="ISO-8601 upper bound on created_at"),
) -> dict[str, Any]:
    """Return aggregate Zim service fee revenue statistics.

    Provides totals and per-fee-type breakdowns across all bookings,
    optionally filtered by tenant and/or date range.
    """
    summary = _fee_store.get_summary(tenant_id=tenant_id, since=since, until=until)
    logger.info(
        "Fee summary requested (tenant=%s): %d bookings, $%.2f collected",
        tenant_id or "all", summary["booking_count"], summary["total_fees_usd"],
    )
    return summary


@app.get("/v1/admin/fees")
def admin_list_fees(
    tenant_id: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> list[dict[str, Any]]:
    """List individual fee records, newest first."""
    return _fee_store.list_fees(tenant_id=tenant_id, limit=limit, offset=offset)


# ---------------------------------------------------------------------------
# Admin: Dashboard stats
# ---------------------------------------------------------------------------


@app.get("/v1/admin/stats")
def admin_stats(
    tenant_id: Optional[str] = Query(None),
) -> dict[str, Any]:
    """Return aggregate statistics for the admin dashboard."""
    import time as _time

    now = _time.time()
    since_7d = now - 7 * 86400
    since_30d = now - 30 * 86400

    req_stats = _store.get_stats(
        tenant_id=tenant_id,
        since_7d=since_7d,
        since_30d=since_30d,
    )
    trip_stats = _trip_store.get_stats(tenant_id=tenant_id)

    return {**req_stats, **trip_stats}


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
