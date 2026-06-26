from typing import Any

from mcp.server.fastmcp import FastMCP

from rurussian_mcp.config import PLAN_CATALOG
from rurussian_mcp.schemas.auth import (
    AuthenticateRequest,
    AuthenticateResponse,
    AuthenticationStatusResponse,
    ConfirmKeyPurchaseRequest,
    ConfirmKeyPurchaseResponse,
    CreateKeyPurchaseSessionRequest,
    CreateKeyPurchaseSessionResponse,
    ListPricingPlansResponse,
    PurchaseStatusResponse,
)
from rurussian_mcp.schemas.common import PlanInfo
from rurussian_mcp.services import auth_service, backend_client


def register_auth_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    def authenticate(api_key: str, user_agent: str = "ClawHub/1.0") -> dict[str, Any]:
        request = AuthenticateRequest(api_key=api_key, user_agent=user_agent)
        auth_service.authenticate(request.api_key, request.user_agent)
        response = AuthenticateResponse(
            authenticated_for_session=True,
            auth_mode="api_key",
            api_key_preview=auth_service.get_api_key_preview(),
            user_agent=request.user_agent,
        )
        return response.model_dump()

    @mcp.tool()
    def authentication_status() -> dict[str, Any]:
        response = AuthenticationStatusResponse(**auth_service.status())
        return response.model_dump()

    @mcp.tool()
    def list_pricing_plans() -> dict[str, Any]:
        response = ListPricingPlansResponse(
            currency="USD",
            plans=[PlanInfo(plan=plan_id, **plan_data) for plan_id, plan_data in PLAN_CATALOG.items()],
            recommended_bot_flow=[
                "Choose a plan.",
                "Call create_key_purchase_session with the buyer email.",
                "Open the checkout_url in a payment-capable browser flow.",
                "After checkout completes, pass session_id to confirm_key_purchase.",
            ],
        )
        return response.model_dump()

    @mcp.tool()
    def purchase_status() -> dict[str, Any]:
        context = auth_service.purchase_context
        response = PurchaseStatusResponse(
            checkout_started=bool(context.checkout_url),
            session_id=context.session_id,
            payment_status=context.payment_status,
            paid_access_active=auth_service.paid_access,
            plan=context.plan,
            email=context.email,
        )
        return response.model_dump()

    @mcp.tool()
    async def create_key_purchase_session(
        email: str,
        plan: str,
        success_url: str = "",
        cancel_url: str = "",
    ) -> dict[str, Any]:
        request = CreateKeyPurchaseSessionRequest(
            email=email,
            plan=plan,
            success_url=success_url,
            cancel_url=cancel_url,
        )
        if request.plan not in PLAN_CATALOG:
            raise ValueError(f"Unsupported plan '{request.plan}'.")

        result = await backend_client.create_purchase_session(request.model_dump())
        auth_service.set_purchase_context(
            email=request.email,
            plan=request.plan,
            checkout_url=result["checkout_url"],
            session_id=result["session_id"],
            payment_status="checkout_created",
        )

        response = CreateKeyPurchaseSessionResponse(
            checkout_url=result["checkout_url"],
            session_id=result["session_id"],
            plan=request.plan,
            plan_details=PlanInfo(plan=request.plan, **PLAN_CATALOG[request.plan]),
            next_step="Open checkout_url, complete payment, then call confirm_key_purchase.",
            bot_payment_ready=True,
        )
        return response.model_dump()

    @mcp.tool()
    async def confirm_key_purchase(session_id: str, auto_authenticate: bool = True) -> dict[str, Any]:
        request = ConfirmKeyPurchaseRequest(session_id=session_id, auto_authenticate=auto_authenticate)
        result = await backend_client.confirm_purchase(request.session_id)
        auth_service.set_purchase_context(
            session_id=request.session_id,
            payment_status=result["payment_status"],
        )

        if result["confirmed"] and request.auto_authenticate:
            api_key = result.get("api_key") or ""
            if api_key:
                auth_service.authenticate(api_key, auth_service.user_agent)
            else:
                auth_service.set_paid_access(True)

        response = ConfirmKeyPurchaseResponse(
            confirmed=result["confirmed"],
            payment_status=result["payment_status"],
            authenticated_for_session=bool(result["confirmed"] and request.auto_authenticate),
            auth_mode="api_key" if result.get("api_key") and request.auto_authenticate else "paid_checkout" if result["confirmed"] and request.auto_authenticate else "none",
            api_key_preview=auth_service.get_api_key_preview(),
        )
        return response.model_dump()
