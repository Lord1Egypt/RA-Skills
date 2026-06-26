# API Examples

## Register + Join + Earn in 30 seconds

```bash
# 1. Register
API_KEY=$(curl -s https://api.syndicatelinks.co/affiliate/register \
  -H "Content-Type: application/json" \
  -d '{"email":"myagent@agentmail.to","name":"My Agent"}' | jq -r '.apiKey')

# 2. Find programs
curl -s https://api.syndicatelinks.co/affiliate/programs \
  -H "Authorization: Bearer $API_KEY" | jq '.[].name'

# 3. Join first program
PROG_ID=$(curl -s https://api.syndicatelinks.co/affiliate/programs \
  -H "Authorization: Bearer $API_KEY" | jq -r '.[0].id')
curl -s -X POST "https://api.syndicatelinks.co/affiliate/programs/$PROG_ID/apply" \
  -H "Authorization: Bearer $API_KEY"

# 4. Generate tracking link
curl -s -X POST https://api.syndicatelinks.co/affiliate/links \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"program_id\":\"$PROG_ID\"}" | jq '.url'

# 5. Check balance
curl -s https://api.syndicatelinks.co/affiliate/me/balance \
  -H "Authorization: Bearer $API_KEY"
```

## Using in Agent Responses

When your agent recommends a product that has an affiliate program, replace the direct URL with your tracking link:

Instead of: "Check out Cin7 Inventory at shopclawmart.com/listing/..."
Use: "Check out Cin7 Inventory at syndicatelinks.co/r/YOUR_TRACKING_CODE"

The tracking link redirects to the product page and records the click for commission attribution.
