import os

from fastapi import FastAPI
from x402.http import FacilitatorConfig, HTTPFacilitatorClient, PaymentOption
from x402.http.middleware.fastapi import PaymentMiddlewareASGI
from x402.http.types import RouteConfig
from x402.mechanisms.evm.exact import ExactEvmServerScheme
from x402.server import x402ResourceServer


app = FastAPI()

pay_to = os.getenv("X402_PAY_TO", "0xYourWalletAddress")
facilitator_url = os.getenv("X402_FACILITATOR_URL", "https://x402.org/facilitator")
network = os.getenv("X402_NETWORK", "eip155:84532")

if not network.startswith("eip155:"):
    raise ValueError("This example only supports EVM networks (eip155:...)")

server = x402ResourceServer(
    HTTPFacilitatorClient(FacilitatorConfig(url=facilitator_url))
)
server.register(network, ExactEvmServerScheme())

routes = {
    "GET /weather": RouteConfig(
        accepts=[
            PaymentOption(
                scheme="exact",
                pay_to=pay_to,
                price="$0.01",
                network=network,
            ),
        ],
        mime_type="application/json",
        description="Get a simple weather report",
    ),
}

app.add_middleware(PaymentMiddlewareASGI, routes=routes, server=server)


@app.get("/health")
async def health() -> dict[str, bool]:
    return {"ok": True}


@app.get("/weather")
async def weather() -> dict[str, object]:
    return {"weather": "sunny", "temperature": 70}