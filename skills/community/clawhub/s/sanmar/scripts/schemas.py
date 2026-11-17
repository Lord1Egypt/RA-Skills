"""Typed request/response models for the SanMar skill.

These dataclasses are intentionally plain — no Odoo, no pydantic, no
agent-core dependencies — so the skill can run in any Python 3.11+
process. Conversion to/from JSON uses ``dataclasses.asdict`` and the
plain ``dict`` constructor.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SanMarCredentials:
    """SOAP-body credentials shared across SanMar service ports."""

    customer_number: str
    username: str
    password: str
    environment: str = "production"  # or "development"

    def to_payload_fields(self) -> dict[str, str]:
        return {
            "sanMarCustomerNumber": self.customer_number,
            "sanMarUserName": self.username,
            "sanMarUserPassword": self.password,
        }


# ---------------------------------------------------------------------------
# Catalog / pricing / inventory request lines
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class StyleColorSize:
    """Canonical SanMar product key."""

    style: str
    color: str | None = None
    size: str | None = None


@dataclass(frozen=True)
class PricingLine:
    """Input line for getPricing."""

    style: str
    color: str
    size: str


@dataclass
class PricingItem:
    """Single response row from getPricing."""

    style: str
    color: str
    size: str
    inventory_key: str | None = None
    size_index: str | None = None
    piece_price: float | None = None
    dozen_price: float | None = None
    case_price: float | None = None
    my_price: float | None = None
    sale_piece_price: float | None = None
    sale_dozen_price: float | None = None
    sale_case_price: float | None = None


@dataclass
class PricingResult:
    items: list[PricingItem] = field(default_factory=list)
    surface: str = "sanmar_webservice"
    operation: str = "getPricing"


@dataclass
class InventoryResult:
    style: str
    color: str
    size: str
    warehouse_quantities: list[int] = field(default_factory=list)
    total_available: int = 0
    surface: str = "sanmar_webservice"
    operation: str = "getInventoryQtyForStyleColorSize"


@dataclass
class ProductVariant:
    style: str
    color: str
    size: str
    unique_key: str | None = None
    inventory_key: str | None = None
    size_index: str | None = None
    image: str | None = None
    piece_price: float | None = None


@dataclass
class ProductSearchResult:
    style: str
    title: str | None = None
    weight: float | None = None
    image: str | None = None
    colors: list[str] = field(default_factory=list)
    sizes: list[str] = field(default_factory=list)
    variants: list[ProductVariant] = field(default_factory=list)
    surface: str = "sanmar_webservice"
    operation: str = "getProductInfoByStyleColorSize"


# ---------------------------------------------------------------------------
# Purchase orders
# ---------------------------------------------------------------------------


@dataclass
class ShipTo:
    """Destination address for a SanMar PO.

    Mirrors the field set the SanMar PO SOAP envelope expects.
    """

    name: str
    address1: str
    city: str
    state: str
    zip: str
    address2: str = ""
    email: str = ""
    ship_method: str = "UPS"  # SanMar accepts UPS, FedEx, etc.
    residence: str = "N"  # "Y" or "N"
    attention: str = ""
    notes: str = ""


@dataclass
class PurchaseOrderLine:
    """Single line on a SanMar PO.

    ``inventory_key`` and ``size_index`` are required at *submit* time
    and are typically populated by calling ``sanmar_get_pricing`` first.
    They are optional on the draft because pre-submit only needs
    style/color/size/quantity.
    """

    style: str
    color: str
    size: str
    quantity: int
    inventory_key: str | None = None
    size_index: str | None = None


@dataclass
class PurchaseOrderDraft:
    po_number: str
    ship_to: ShipTo
    lines: list[PurchaseOrderLine]


@dataclass
class CartValidationLineError:
    style: str
    color: str
    size: str
    message: str


@dataclass
class CartValidationResult:
    ok: bool
    errored_lines: list[CartValidationLineError] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    surface: str = "sanmar_webservice"
    operation: str = "getPreSubmitInfo"


@dataclass
class PurchaseOrderResult:
    status: str  # "submitted", "dry_run", "error"
    po_number: str
    sanmar_reference: str | None = None
    raw_payload: str | None = None
    raw_response: str | None = None
    surface: str = "sanmar_webservice"
    operation: str = "submitPO"


# ---------------------------------------------------------------------------
# Order status / tracking
# ---------------------------------------------------------------------------


@dataclass
class TrackingShipment:
    tracking_number: str
    carrier: str | None = None  # normalized: fedex|ups|usps|None


@dataclass
class TrackingResult:
    po_number: str
    shipments: list[TrackingShipment] = field(default_factory=list)
    surface: str = "sanmar_promostandards"
    operation: str = "GetOrderShipmentNotificationRequest"


@dataclass
class OrderStatusResult:
    po_number: str
    sanmar_order_number: str | None = None
    shipment_count: int = 0
    status: str = "unknown"  # "submitted" | "shipped" | "unknown"
    surface: str = "sanmar_promostandards"
    operation: str = "GetOrderShipmentNotificationRequest"


@dataclass
class CancelResult:
    status: str  # "not_implemented" for now
    message: str
    po_number: str
    surface: str = "sanmar_webservice"
    operation: str = "cancelPO"


# ---------------------------------------------------------------------------
# PDF purchase-order parsing
# ---------------------------------------------------------------------------


@dataclass
class ParsedPOLine:
    """One line item extracted from a PDF purchase order.

    Fields are best-effort: parsing pipelines should populate every
    field they can confidently identify. ``raw`` retains the source
    text the line was extracted from so the caller can show context
    when asking the user to approve the parse.
    """

    style: str
    color: str
    size: str
    quantity: int
    unit_price: float | None = None
    description: str | None = None
    raw: str | None = None


@dataclass
class ParsedShipTo:
    name: str = ""
    address1: str = ""
    address2: str = ""
    city: str = ""
    state: str = ""
    zip: str = ""
    email: str = ""


@dataclass
class ParsedPurchaseOrder:
    """Best-effort structured PO extracted from a PDF.

    The agent must show this back to the user for approval before
    handing it to :func:`sanmar_create_purchase_order`. ``warnings``
    flags fields that could not be confidently extracted.
    """

    po_number: str | None = None
    order_date: str | None = None
    ship_to: ParsedShipTo = field(default_factory=ParsedShipTo)
    ship_method: str | None = None
    lines: list[ParsedPOLine] = field(default_factory=list)
    notes: str = ""
    warnings: list[str] = field(default_factory=list)
    raw_text: str = ""
    surface: str = "sanmar_pdf_parser"
    operation: str = "parse_po_pdf"


# ---------------------------------------------------------------------------
# Mainframe color resolution (FTP SDL)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SanMarFTPCredentials:
    """SFTP credentials for the SanMar FTP server.

    SanMar issues these separately from web-service credentials. The
    server is ``ftp.sanmar.com:2200`` over SFTP (SSH), and the username
    is your SanMar customer number.
    """

    username: str
    password: str
    host: str = "ftp.sanmar.com"
    port: int = 2200


@dataclass
class MainframeColorMatch:
    style: str
    requested_color: str
    size: str | None
    mainframe_color: str
    color_name: str
    inventory_key: str | None = None
    size_index: str | None = None
    unique_key: str | None = None


@dataclass
class MainframeColorResolution:
    """Result of resolving a marketing color name to a mainframe color."""

    status: str  # "matched" | "ambiguous" | "not_found"
    style: str
    requested_color: str
    size: str | None = None
    matches: list[MainframeColorMatch] = field(default_factory=list)
    source_file: str = "SanMarPDD/SanMar_SDL_N.csv"
    as_of: str | None = None  # ISO timestamp of cached file mtime
    surface: str = "sanmar_ftp"
    operation: str = "lookup_mainframe_color"


# ---------------------------------------------------------------------------
# JSON helpers
# ---------------------------------------------------------------------------


def to_dict(obj: Any) -> Any:
    """Convert dataclass trees to plain JSON-serializable dicts."""

    if hasattr(obj, "__dataclass_fields__"):
        return asdict(obj)
    if isinstance(obj, list):
        return [to_dict(x) for x in obj]
    if isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    return obj
