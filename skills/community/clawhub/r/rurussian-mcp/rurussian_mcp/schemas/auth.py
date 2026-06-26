from pydantic import Field

from .common import PlanInfo, PurchaseContextSchema, StrictSchema


class AuthenticateRequest(StrictSchema):
    api_key: str = Field(min_length=1)
    user_agent: str = "ClawHub/1.0"


class AuthenticateResponse(StrictSchema):
    authenticated_for_session: bool
    auth_mode: str
    api_key_preview: str
    user_agent: str


class AuthenticationStatusResponse(StrictSchema):
    authenticated: bool
    authentication_method: str
    api_key_preview: str
    user_agent: str
    purchase_context: PurchaseContextSchema


class ListPricingPlansResponse(StrictSchema):
    currency: str
    plans: list[PlanInfo]
    recommended_bot_flow: list[str]


class PurchaseStatusResponse(StrictSchema):
    checkout_started: bool
    session_id: str
    payment_status: str
    paid_access_active: bool
    plan: str
    email: str


class CreateKeyPurchaseSessionRequest(StrictSchema):
    email: str = Field(min_length=1)
    plan: str = Field(min_length=1)
    success_url: str = ""
    cancel_url: str = ""


class CreateKeyPurchaseSessionResponse(StrictSchema):
    checkout_url: str
    session_id: str
    plan: str
    plan_details: PlanInfo
    next_step: str
    bot_payment_ready: bool


class ConfirmKeyPurchaseRequest(StrictSchema):
    session_id: str = Field(min_length=1)
    auto_authenticate: bool = True


class ConfirmKeyPurchaseResponse(StrictSchema):
    confirmed: bool
    payment_status: str
    authenticated_for_session: bool
    auth_mode: str
    api_key_preview: str = ""
