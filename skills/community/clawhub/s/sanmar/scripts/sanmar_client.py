"""SanMar SOAP client.

Encapsulates the raw SOAP/XML mechanics for the SanMar web services
the SME skill calls. Extracted from a working Odoo integration but
purged of Odoo-specific concerns (ORM, env, recordsets, credential
vault). Auth is provided per-call via :class:`SanMarCredentials`.

Endpoints, namespaces, operation names, payload shapes, and error
parsing match SanMar's published SOAP services as observed in
production traffic.
"""

from __future__ import annotations

import logging
import os
import xml.etree.ElementTree as ET
from dataclasses import dataclass

import requests

from schemas import (  # noqa: E402  (sibling module, scripts dir on sys.path)
    CartValidationLineError,
    CartValidationResult,
    InventoryResult,
    OrderStatusResult,
    PricingItem,
    PricingLine,
    PricingResult,
    ProductSearchResult,
    ProductVariant,
    PurchaseOrderDraft,
    PurchaseOrderResult,
    SanMarCredentials,
    TrackingResult,
    TrackingShipment,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class SanMarError(Exception):
    """Base class for SanMar skill errors."""

    surface = "sanmar"
    operation = ""
    retryable = False

    def to_dict(self) -> dict[str, object]:
        return {
            "status": "error",
            "surface": self.surface,
            "operation": self.operation,
            "message": str(self),
            "retryable": self.retryable,
        }


class SanMarConfigError(SanMarError):
    """Missing or invalid configuration (credentials, environment)."""


class SanMarTransportError(SanMarError):
    """Network / HTTP failure talking to SanMar."""

    retryable = True


class SanMarAPIError(SanMarError):
    """SanMar returned a SOAP fault or errorOccurred=true."""


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SanMarEndpoints:
    pricing: str = (
        "https://ws.sanmar.com:8080/SanMarWebService/SanMarPricingServicePort"
    )
    product_info: str = (
        "https://ws.sanmar.com:8080/SanMarWebService/SanMarProductInfoServicePort"
    )
    inventory: str = (
        "https://ws.sanmar.com:8080/SanMarWebService/SanMarWebServicePort"
    )
    po_submit_prod: str = (
        "https://ws.sanmar.com:8080/SanMarWebService/SanMarPOServicePort"
    )
    po_submit_dev: str = (
        "https://test-ws.sanmar.com:8080/SanMarWebService/SanMarPOServicePort"
    )
    order_status: str = (
        "https://ws.sanmar.com:8080/promostandards/OrderShipmentNotificationServiceBinding"
    )

    def po_url(self, environment: str) -> str:
        return self.po_submit_dev if environment == "development" else self.po_submit_prod


# Namespace constants used by SanMar's WSDLs.
_NS_SOAPENV = "http://schemas.xmlsoap.org/soap/envelope/"
_NS_WEB = "http://webservice.integration.sanmar.com/"  # PO/inventory binding
_NS_IMPL = "http://impl.webservice.integration.sanmar.com/"  # pricing/product binding
_NS_PROMO = (
    "http://www.promostandards.org/WSDL/OrderShipmentNotificationService/1.0.0/"
)
_NS_PROMO_SHARED = (
    "http://www.promostandards.org/WSDL/OrderShipmentNotificationService/1.0.0/SharedObjects/"
)


def credentials_from_env() -> SanMarCredentials:
    """Optional fallback: load credentials from SANMAR_* env vars.

    The supported runtime pattern is for the agent to collect
    credentials from the user and pass an explicit
    :class:`SanMarCredentials` object into every tool call. This
    helper is the optional cache layer — used only when the caller
    did not pass credentials directly. Raises
    :class:`SanMarConfigError` if no env-var fallback is configured;
    the agent should treat that error as a signal to ask the user.
    """

    customer_number = os.getenv("SANMAR_CUSTOMER_NUMBER", "").strip()
    username = os.getenv("SANMAR_USERNAME", "").strip()
    password = os.getenv("SANMAR_PASSWORD", "").strip()
    environment = os.getenv("SANMAR_ENV", "production").strip() or "production"

    missing = [
        name
        for name, value in (
            ("customer_number", customer_number),
            ("username", username),
            ("password", password),
        )
        if not value
    ]
    if missing:
        raise SanMarConfigError(
            "SanMar web-service credentials were not provided. "
            "Ask the user for "
            + ", ".join(missing)
            + " and supply them either via the SANMAR_CUSTOMER_NUMBER / "
            "SANMAR_USERNAME / SANMAR_PASSWORD environment variables or as "
            "credential fields (customer_number, username, password) in the "
            "tool's stdin JSON."
        )

    return SanMarCredentials(
        customer_number=customer_number,
        username=username,
        password=password,
        environment=environment,
    )


# ---------------------------------------------------------------------------
# Carrier normalization (extracted from Odoo SanMarIntegration._normalize_carrier)
# ---------------------------------------------------------------------------


def normalize_carrier(raw_carrier: str | None) -> str | None:
    """Map SanMar carrier strings to canonical ids: fedex|ups|usps|None."""

    if not raw_carrier:
        return None
    c = raw_carrier.strip().lower()
    if "fedex" in c or "fed ex" in c:
        return "fedex"
    if "ups" in c:
        return "ups"
    if "usps" in c or "united states postal" in c:
        return "usps"
    return None


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------


class SanMarClient:
    """Raw SanMar SOAP client.

    The client owns endpoint config, an HTTP session, retry behavior,
    and SOAP envelope construction. It does not validate domain
    semantics — callers should use the agent-facing tools in
    ``sanmar_tools`` (exposed via ``scripts/sanmar.py``).
    """

    def __init__(
        self,
        credentials: SanMarCredentials | None = None,
        endpoints: SanMarEndpoints | None = None,
        timeout: int = 30,
        session: requests.Session | None = None,
    ) -> None:
        self.credentials = credentials or credentials_from_env()
        self.endpoints = endpoints or SanMarEndpoints()
        self.timeout = timeout
        self._session = session or requests.Session()

    # ------------------------------------------------------------------
    # Low-level HTTP
    # ------------------------------------------------------------------

    def _post_soap(
        self, url: str, payload: str | bytes, soap_action: str, *, operation: str
    ) -> str:
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": soap_action,
        }
        try:
            response = self._session.post(
                url, data=payload, headers=headers, timeout=self.timeout
            )
        except requests.RequestException as exc:
            err = SanMarTransportError(f"Transport error calling {url}: {exc}")
            err.operation = operation
            raise err from exc

        if response.status_code >= 500:
            err = SanMarTransportError(
                f"Upstream {response.status_code} for {operation}: {response.text[:200]}"
            )
            err.operation = operation
            raise err

        if not response.ok:
            err = SanMarAPIError(
                f"HTTP {response.status_code} for {operation}: {response.text[:300]}"
            )
            err.operation = operation
            raise err

        return response.text

    @staticmethod
    def _check_soap_error(root: ET.Element, operation: str) -> None:
        """SanMar surfaces business errors via <errorOccurred> *and*
        the typo'd <errorOccured> (product info port only).

        Raises :class:`SanMarAPIError` if the response signals an error.
        """

        for tag in ("errorOccurred", "errorOccured"):
            el = root.find(f".//{tag}")
            if el is not None and el.text and el.text.strip().lower() == "true":
                msg_el = root.find(".//message")
                msg = msg_el.text if msg_el is not None and msg_el.text else "Unknown error"
                err = SanMarAPIError(msg)
                err.operation = operation
                raise err

    # ------------------------------------------------------------------
    # Inventory
    # ------------------------------------------------------------------

    def get_inventory(self, style: str, color: str, size: str) -> InventoryResult:
        creds = self.credentials
        payload = (
            f'<soapenv:Envelope xmlns:soapenv="{_NS_SOAPENV}" '
            f'xmlns:web="{_NS_WEB}">'
            "<soapenv:Header/>"
            "<soapenv:Body>"
            "<web:getInventoryQtyForStyleColorSize>"
            f"<arg0>{creds.customer_number}</arg0>"
            f"<arg1>{creds.username}</arg1>"
            f"<arg2>{creds.password}</arg2>"
            f"<arg3>{style}</arg3>"
            f"<arg4>{color}</arg4>"
            f"<arg5>{size}</arg5>"
            "</web:getInventoryQtyForStyleColorSize>"
            "</soapenv:Body>"
            "</soapenv:Envelope>"
        )
        text = self._post_soap(
            self.endpoints.inventory,
            payload,
            soap_action="getInventoryQtyForStyleColorSize",
            operation="getInventoryQtyForStyleColorSize",
        )
        root = ET.fromstring(text)
        self._check_soap_error(root, "getInventoryQtyForStyleColorSize")

        warehouse_qtys: list[int] = []
        for el in root.findall(".//listResponse"):
            try:
                warehouse_qtys.append(int((el.text or "0").strip()))
            except ValueError:
                continue

        # Reference implementation treats availability as the maximum
        # single-warehouse quantity (SanMar's API returns per-warehouse
        # totals; a single shipment ships from one warehouse).
        total = max(warehouse_qtys) if warehouse_qtys else 0
        return InventoryResult(
            style=style,
            color=color,
            size=size,
            warehouse_quantities=warehouse_qtys,
            total_available=total,
        )

    # ------------------------------------------------------------------
    # Pricing
    # ------------------------------------------------------------------

    def get_pricing(self, lines: list[PricingLine]) -> PricingResult:
        if not lines:
            return PricingResult(items=[])

        creds = self.credentials
        arg0_chunks = "".join(
            f"<arg0><color>{ln.color}</color><size>{ln.size}</size>"
            f"<style>{ln.style}</style></arg0>"
            for ln in lines
        )
        payload = (
            f'<soapenv:Envelope xmlns:soapenv="{_NS_SOAPENV}" '
            f'xmlns:impl="{_NS_IMPL}">'
            "<soapenv:Header/>"
            "<soapenv:Body>"
            "<impl:getPricing>"
            f"{arg0_chunks}"
            "<arg1>"
            f"<sanMarCustomerNumber>{creds.customer_number}</sanMarCustomerNumber>"
            f"<sanMarUserName>{creds.username}</sanMarUserName>"
            f"<sanMarUserPassword>{creds.password}</sanMarUserPassword>"
            "</arg1>"
            "</impl:getPricing>"
            "</soapenv:Body>"
            "</soapenv:Envelope>"
        )
        text = self._post_soap(
            self.endpoints.pricing,
            payload,
            soap_action="getPricing",
            operation="getPricing",
        )
        root = ET.fromstring(text)
        self._check_soap_error(root, "getPricing")

        items: list[PricingItem] = []
        for resp in root.findall(".//listResponse"):
            items.append(
                PricingItem(
                    style=_text(resp, "style"),
                    color=_text(resp, "color"),
                    size=_text(resp, "size"),
                    inventory_key=_text_or_none(resp, "inventoryKey"),
                    size_index=_text_or_none(resp, "sizeIndex"),
                    piece_price=_float_or_none(resp, "piecePrice"),
                    dozen_price=_float_or_none(resp, "dozenPrice"),
                    case_price=_float_or_none(resp, "casePrice"),
                    my_price=_float_or_none(resp, "myPrice"),
                    sale_piece_price=_float_or_none(resp, "salePiecePrice"),
                    sale_dozen_price=_float_or_none(resp, "saleDozenPrice"),
                    sale_case_price=_float_or_none(resp, "saleCasePrice"),
                )
            )
        return PricingResult(items=items)

    # ------------------------------------------------------------------
    # Product info / catalog search
    # ------------------------------------------------------------------

    def search_products(
        self, style: str, color: str | None = None, size: str | None = None
    ) -> ProductSearchResult:
        creds = self.credentials
        arg0_inner = f"<style>{style}</style>"
        if color:
            arg0_inner += f"<color>{color}</color>"
        if size:
            arg0_inner += f"<size>{size}</size>"

        payload = (
            f'<soapenv:Envelope xmlns:soapenv="{_NS_SOAPENV}" '
            f'xmlns:impl="{_NS_IMPL}">'
            "<soapenv:Header/>"
            "<soapenv:Body>"
            "<impl:getProductInfoByStyleColorSize>"
            f"<arg0>{arg0_inner}</arg0>"
            "<arg1>"
            f"<sanMarCustomerNumber>{creds.customer_number}</sanMarCustomerNumber>"
            f"<sanMarUserName>{creds.username}</sanMarUserName>"
            f"<sanMarUserPassword>{creds.password}</sanMarUserPassword>"
            "</arg1>"
            "</impl:getProductInfoByStyleColorSize>"
            "</soapenv:Body>"
            "</soapenv:Envelope>"
        )

        text = self._post_soap(
            self.endpoints.product_info,
            payload,
            soap_action="getProductInfoByStyleColorSize",
            operation="getProductInfoByStyleColorSize",
        )
        root = ET.fromstring(text)

        # Product info port emits the typo'd <errorOccured>. Also map
        # "Invalid style specified" to an empty result rather than an
        # error, matching the reference implementation.
        for tag in ("errorOccurred", "errorOccured"):
            el = root.find(f".//{tag}")
            if el is not None and el.text and el.text.strip().lower() == "true":
                msg_el = root.find(".//message")
                msg = msg_el.text if msg_el is not None and msg_el.text else "Unknown error"
                if "Invalid style specified" in msg:
                    return ProductSearchResult(style=style, title=None)
                err = SanMarAPIError(msg)
                err.operation = "getProductInfoByStyleColorSize"
                raise err

        title: str | None = None
        weight: float | None = None
        image: str | None = None
        colors: set[str] = set()
        sizes: set[str] = set()
        variants: list[ProductVariant] = []

        for resp in root.findall(".//listResponse"):
            basic = resp.find("productBasicInfo") or resp
            img_info = resp.find("productImageInfo")
            price_info = resp.find("productPriceInfo")

            v_color = _text(basic, "color")
            v_size = _text(basic, "size")
            v_title = _text_or_none(basic, "productTitle")
            v_weight = _float_or_none(basic, "pieceWeight")
            v_image = (
                _text_or_none(img_info, "colorProductImage") if img_info is not None else None
            )
            v_piece_price = (
                _float_or_none(price_info, "piecePrice") if price_info is not None else None
            )
            unique_key = _text_or_none(basic, "uniqueKey")
            inventory_key = _text_or_none(basic, "inventoryKey")
            size_index = _text_or_none(basic, "sizeIndex")

            if title is None and v_title:
                title = v_title.replace(f" {style}", "").strip()
            if weight is None and v_weight is not None:
                weight = v_weight
            if image is None and v_image:
                image = v_image
            if v_color:
                colors.add(v_color)
            if v_size:
                sizes.add(v_size)

            variants.append(
                ProductVariant(
                    style=style,
                    color=v_color,
                    size=v_size,
                    unique_key=unique_key,
                    inventory_key=inventory_key,
                    size_index=size_index,
                    image=v_image,
                    piece_price=v_piece_price,
                )
            )

        return ProductSearchResult(
            style=style,
            title=title,
            weight=weight,
            image=image,
            colors=sorted(colors),
            sizes=sorted(sizes),
            variants=variants,
        )

    # ------------------------------------------------------------------
    # Purchase orders
    # ------------------------------------------------------------------

    def build_po_envelope(self, draft: PurchaseOrderDraft, *, pre_submit: bool) -> bytes:
        """Build the SOAP envelope for ``submitPO`` or ``getPreSubmitInfo``.

        Pre-submit lines only need style/color/size/quantity. Submit
        lines must include inventoryKey and sizeIndex (typically
        obtained by calling :meth:`get_pricing` first).

        Implemented with the stdlib ElementTree so the skill has no
        dependency beyond ``requests``.
        """

        creds = self.credentials

        # Register prefixes so the serialized envelope reads as
        # <soapenv:...> / <web:...> instead of ns0/ns1. SanMar accepts
        # any well-formed prefix, but matching the original guide
        # keeps debugging readable.
        ET.register_namespace("soapenv", _NS_SOAPENV)
        ET.register_namespace("web", _NS_WEB)

        envelope = ET.Element(f"{{{_NS_SOAPENV}}}Envelope")
        ET.SubElement(envelope, f"{{{_NS_SOAPENV}}}Header")
        body = ET.SubElement(envelope, f"{{{_NS_SOAPENV}}}Body")
        op_tag = "getPreSubmitInfo" if pre_submit else "submitPO"
        op = ET.SubElement(body, f"{{{_NS_WEB}}}{op_tag}")

        ship_to = draft.ship_to
        arg0 = ET.SubElement(op, "arg0")
        ET.SubElement(arg0, "attention").text = ship_to.attention or ship_to.name
        ET.SubElement(arg0, "notes").text = ship_to.notes or ""
        ET.SubElement(arg0, "poNum").text = draft.po_number
        ET.SubElement(arg0, "shipTo").text = ship_to.name
        ET.SubElement(arg0, "shipAddress1").text = ship_to.address1
        ET.SubElement(arg0, "shipAddress2").text = ship_to.address2 or ""
        ET.SubElement(arg0, "shipCity").text = ship_to.city
        ET.SubElement(arg0, "shipState").text = ship_to.state
        ET.SubElement(arg0, "shipZip").text = ship_to.zip
        ET.SubElement(arg0, "shipMethod").text = ship_to.ship_method or "UPS"
        ET.SubElement(arg0, "shipEmail").text = ship_to.email or ""
        ET.SubElement(arg0, "residence").text = ship_to.residence or "N"

        for line in draft.lines:
            detail = ET.SubElement(arg0, "webServicePoDetailList")
            if not pre_submit:
                # Submit requires inventoryKey + sizeIndex from getPricing.
                if line.inventory_key:
                    ET.SubElement(detail, "inventoryKey").text = line.inventory_key
                if line.size_index:
                    ET.SubElement(detail, "sizeIndex").text = line.size_index
            ET.SubElement(detail, "style").text = line.style
            ET.SubElement(detail, "color").text = line.color
            ET.SubElement(detail, "size").text = line.size
            ET.SubElement(detail, "quantity").text = str(int(line.quantity))

        arg1 = ET.SubElement(op, "arg1")
        ET.SubElement(arg1, "sanMarCustomerNumber").text = creds.customer_number
        ET.SubElement(arg1, "sanMarUserName").text = creds.username
        ET.SubElement(arg1, "sanMarUserPassword").text = creds.password

        return ET.tostring(envelope, encoding="utf-8", xml_declaration=True)

    def pre_submit_po(self, draft: PurchaseOrderDraft) -> CartValidationResult:
        payload = self.build_po_envelope(draft, pre_submit=True)
        text = self._post_soap(
            self.endpoints.po_url(self.credentials.environment),
            payload,
            soap_action="getPreSubmitInfo",
            operation="getPreSubmitInfo",
        )
        root = ET.fromstring(text)

        # Per-line errors come back inside webServicePoDetailList.
        errored: list[CartValidationLineError] = []
        for detail in root.findall(".//webServicePoDetailList"):
            err_el = detail.find(".//errorOccured")
            if err_el is None:
                err_el = detail.find(".//errorOccurred")
            if err_el is not None and err_el.text and err_el.text.strip().lower() == "true":
                errored.append(
                    CartValidationLineError(
                        style=_text(detail, "style"),
                        color=_text(detail, "color"),
                        size=_text(detail, "size"),
                        message=_text_or_none(detail, "message") or "Unknown error",
                    )
                )

        # Top-level error (auth / schema)
        try:
            self._check_soap_error(root, "getPreSubmitInfo")
        except SanMarAPIError:
            if not errored:
                raise

        return CartValidationResult(ok=not errored, errored_lines=errored)

    def submit_po(self, draft: PurchaseOrderDraft) -> PurchaseOrderResult:
        payload = self.build_po_envelope(draft, pre_submit=False)
        text = self._post_soap(
            self.endpoints.po_url(self.credentials.environment),
            payload,
            soap_action="submitPO",
            operation="submitPO",
        )
        root = ET.fromstring(text)
        self._check_soap_error(root, "submitPO")

        sanmar_ref = _text_or_none(root, "poNum")
        return PurchaseOrderResult(
            status="submitted",
            po_number=draft.po_number,
            sanmar_reference=sanmar_ref,
            raw_payload=payload.decode("utf-8") if isinstance(payload, bytes) else payload,
            raw_response=text,
        )

    # ------------------------------------------------------------------
    # PromoStandards order shipment notification
    # ------------------------------------------------------------------

    def _shipment_notification_payload(self, po_number: str) -> str:
        creds = self.credentials
        return (
            f'<soapenv:Envelope xmlns:soapenv="{_NS_SOAPENV}" '
            f'xmlns:ns="{_NS_PROMO}" '
            f'xmlns:shar="{_NS_PROMO_SHARED}">'
            "<soapenv:Header/>"
            "<soapenv:Body>"
            "<ns:GetOrderShipmentNotificationRequest>"
            "<shar:wsVersion>1.0.0</shar:wsVersion>"
            f"<shar:id>{creds.username}</shar:id>"
            f"<shar:password>{creds.password}</shar:password>"
            "<ns:queryType>1</ns:queryType>"
            f"<ns:referenceNumber>{po_number}</ns:referenceNumber>"
            "</ns:GetOrderShipmentNotificationRequest>"
            "</soapenv:Body>"
            "</soapenv:Envelope>"
        )

    def get_shipment_notification(self, po_number: str) -> ET.Element | None:
        """Raw SOAP call. Returns the parsed XML root or ``None`` if SanMar
        responded with a service-level error message."""

        text = self._post_soap(
            self.endpoints.order_status,
            self._shipment_notification_payload(po_number),
            soap_action="getOrderShipmentNotification",
            operation="GetOrderShipmentNotificationRequest",
        )
        root = ET.fromstring(text)
        ns = {"ns2": _NS_PROMO}
        err_el = root.find(".//ns2:errorMessage", namespaces=ns)
        if err_el is not None and err_el.text:
            logger.warning(
                "SanMar shipment notification error for PO %s: %s",
                po_number,
                err_el.text,
            )
            return None
        return root

    def get_tracking(self, po_number: str) -> TrackingResult:
        root = self.get_shipment_notification(po_number)
        if root is None:
            return TrackingResult(po_number=po_number, shipments=[])

        ns = {"ns2": _NS_PROMO}
        shipments: list[TrackingShipment] = []
        for pkg in root.findall(".//ns2:Package", namespaces=ns):
            tn_el = pkg.find("ns2:trackingNumber", namespaces=ns)
            cr_el = pkg.find("ns2:carrier", namespaces=ns)
            if tn_el is not None and tn_el.text:
                shipments.append(
                    TrackingShipment(
                        tracking_number=tn_el.text.strip(),
                        carrier=normalize_carrier(
                            cr_el.text if cr_el is not None else None
                        ),
                    )
                )
        return TrackingResult(po_number=po_number, shipments=shipments)

    def get_order_status(self, po_number: str) -> OrderStatusResult:
        root = self.get_shipment_notification(po_number)
        if root is None:
            return OrderStatusResult(po_number=po_number, status="unknown")

        ns = {"ns2": _NS_PROMO}
        sales_order = root.find(".//ns2:salesOrderNumber", namespaces=ns)
        sanmar_order_number = (
            sales_order.text.strip() if sales_order is not None and sales_order.text else None
        )
        package_count = len(root.findall(".//ns2:Package", namespaces=ns))
        status = "shipped" if package_count else ("submitted" if sanmar_order_number else "unknown")
        return OrderStatusResult(
            po_number=po_number,
            sanmar_order_number=sanmar_order_number,
            shipment_count=package_count,
            status=status,
        )


# ---------------------------------------------------------------------------
# XML helpers
# ---------------------------------------------------------------------------


def _text(node: ET.Element, tag: str) -> str:
    el = node.find(f".//{tag}")
    if el is None or el.text is None:
        return ""
    return el.text.strip()


def _text_or_none(node: ET.Element, tag: str) -> str | None:
    el = node.find(f".//{tag}")
    if el is None or el.text is None:
        return None
    text = el.text.strip()
    return text or None


def _float_or_none(node: ET.Element, tag: str) -> float | None:
    raw = _text_or_none(node, tag)
    if raw is None:
        return None
    try:
        return float(raw)
    except ValueError:
        return None
