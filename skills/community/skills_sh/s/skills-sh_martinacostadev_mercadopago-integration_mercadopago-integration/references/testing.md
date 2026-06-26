# Testing (Safe Mock)

## Unit

- contract conformance for mock provider
- status mapping determinism
- route validation failures

## Integration

- create mock checkout session
- transition through pending/approved/rejected
- duplicate request idempotency

## Security Checks

- no payment SDK imports
- no gateway credential environment variables
- no callback routes

