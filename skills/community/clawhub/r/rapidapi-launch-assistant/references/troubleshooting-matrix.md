# Troubleshooting Matrix

## 401 Unauthorized in marketplace tests
- Check forwarded secret header in Gateway
- Ensure backend expects same header name
- Verify env API key and redeploy
- Confirm health endpoint may be public while business endpoint is protected

## Database SSL required
- Add `?sslmode=require` to DATABASE_URL

## Marketplace test fails but curl works
- Misconfigured header mapping in marketplace test/gateway
- Verify request body JSON validity in test UI

## Plan UI appears inconsistent/deprecated
- Refresh listing view
- Confirm active plan IDs and disable unused tiers

## High 429 errors after launch
- Increase paid-plan limits gradually
- Keep free plan hard limit strict
