# x402 Seller Minimal Example

This is a minimal FastAPI seller example for x402.

It protects one paid endpoint, `/weather`, with a fixed USDC price on Base Sepolia by default.

## Files

- `app.py` - runnable FastAPI server with x402 middleware
- `requirements.txt` - minimal Python dependencies
- `.env-example` - environment variables used by the example

## Setup

1. Copy the environment template:

```bash
cp .env.example .env
```

2. Fill in your receiving address:

```bash
	X402_PAY_TO=0xYourWalletAddress
	# Optional: change this only if you are using another EVM network
	X402_NETWORK=eip155:84532
```

3. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

4. Run the server:

```bash
uvicorn app:app --reload --port 8000
```

## Test the paywall

Without payment, the endpoint should return `402 Payment Required`:

```bash
curl -i http://localhost:8000/weather
```

To test as a buyer, use the x402 client skill or any x402-capable client configured for Base Sepolia.

## Notes

- This example is EVM-only because it uses `ExactEvmServerScheme`.
- The example uses the testnet facilitator at `https://x402.org/facilitator`.
- To accept real payments, switch to the CDP facilitator and a mainnet EVM network ID.