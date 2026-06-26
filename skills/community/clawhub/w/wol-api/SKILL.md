---
name: wol-api
description: "Use this skill when the user wants to interact with the Wake-up On LAN (WOL) API — Catering features: listing products/menu, placing an order, or checking order history and account balance. Event registration features: Checking event registration status, registering for events. Trigger phrases: 'wake up on lan', 'catering api', 'place order', 'check my orders', 'what\'s on the menu', 'show balance', 'wol api', 'order food', 'wol registration'."
metadata: {"openclaw": {"requires": {"bins": ["curl"], "env": ["WOL_API_TOKEN"]}, "primaryEnv": "WOL_API_TOKEN", "envVars": [{"name": "WOL_BASE_URL", "required" : false}, {"name": "WOL_API_TOKEN", "required" : true}], "emoji": "⛺️", "os": ["darwin", "linux"]}}
---

# WOL API

Interact with the Wake-up On LAN website via its REST API using `curl`. There are 2 major features: A catering system, and event registration system.

## Step 1 — Resolve credentials

Run these two shell commands to check for environment variables:

```bash
echo "${WOL_API_TOKEN}"
echo "${WOL_BASE_URL}"
```

- If `WOL_API_TOKEN` is empty, ask the user:
  > "Please paste your API token, or configure the WOL_API_TOKEN environment variable. You can generate one at `/user/api-tokens` on the WOL site."
- If `WOL_BASE_URL` is empty, asume https://wollan.nl as the base url.

Store the resolved values as `TOKEN` and `BASE_URL` for use in the commands below.

## Step 2 — Dispatch on user intent

Look at `$ARGUMENTS` and/or the user's message to determine which action to take.

---

### Catering: List products / show the menu

**Trigger:** `$ARGUMENTS` contains `products`, or the user asks what is available / what's on the menu.

```bash
curl -s \
  -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/api/v1/catering/products"
```

Present the result grouped by category. For each product show:
- Name
- Price formatted as `€X.XX` (response values are in euro cents — divide by 100)
- Stock status (`inStock` / out of stock)
- Product ID (the user needs this to place an order)

---

### Catering: Place an order

**Trigger:** `$ARGUMENTS` contains `order`, or the user says they want to order something.

Parse items from `$ARGUMENTS` in the format `productId:quantity,...` (e.g. `order 3:2,5:1` means product 3 qty 2, product 5 qty 1). If no items are provided in `$ARGUMENTS`, ask the user which products and quantities they want (show the menu first if needed).
Assume a quantity of 1 if the user provides a product or list of products without quantities. 

Build the JSON body and POST:

```bash
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"items": [{"productId": PRODUCT_ID, "quantity": QUANTITY}]}' \
  "$BASE_URL/api/v1/catering/orders"
```

On **201 Created**: show a confirmation with the order ID, items, and total cost (sum of `quantity × productPrice` for all items, formatted as `€X.XX`).

---

### Catering: View order history and account balance

**Trigger:** `$ARGUMENTS` contains `history`, is empty, or the user asks about their orders / balance.

```bash
curl -s \
  -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/api/v1/catering/orders"
```

Present the account summary as a table:

|                       | Amount  |
|-----------------------|---------|
| Total spent           | `€X.XX` |
| Total paid            | `€X.XX` |
| Balance (owed)        | `€X.XX` |
| Pending (in progress) | `€X.XX` |

Then list each order with its ID, date, status, and items. Only show the detailed order list if the user asks for it.  

**Order status meanings:**
- `accepted` — received, being prepared
- `waiting` — queued behind other orders
- `ready` — ready for pick-up
- `complete` — picked up / done
- `cancelled` / `rejected` — not fulfilled

### Event registration: Check event status

**Trigger:** `$ARGUMENTS` contains `eventstatus`, or user asks if the WOL registrations are open or not

```bash
curl -s \
  -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/api/v1/events/zijn-de-inschrijvingen-al-open-of-nie"
```

Returns: open: true|false, with eventId if true.

### Event registration: Register for event

**Trigger:** `$ARGUMENTS` contains `register`, or user asks to register for the next WOL event.
Use "Check event status" to check if registrations are open or not, and if so, use that eventId to register the user with the following call:

```bash
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "$BASE_URL/api/v1/events/{eventId}/register"
```
The result is a simple success:true

### Event registration: Check user registration status for an event

**Trigger:** `$ARGUMENTS` contains `registration-status`, or user asks to check his payment status for his registration for the next WOL event.
Use "Check event status" to check if registrations are open or not, and if so, use that eventId to check the users' registration status with the following call:

```bash
curl -s \
  -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/api/v1/events/{eventId}/registration-status"
```


---

## Error handling

| HTTP status                 | Meaning                                                        | Action                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|-----------------------------|----------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `401 Unauthorized`          | Token invalid or expired                                       | Ask the user to generate a new token at `/user/api-tokens` and set `WOL_API_TOKEN`                                                                                                                                                                                                                                                                                                                                                           |
| `403 Forbidden`             | Not registered / not paid for the active event,                | User needs to register for the active event and pay on the WOL site                                                                                                                                                                                                                                                                                                                                                                          |
| `422 Unprocessable Entity`  | Validation error. Check the error message for more details.    | Check the error message: if it mentions "disabled by crew", inform the user that ordering is temporarily paused and they should try again later; If out of stock: Inform the user that the product is out of stock and suggest an alternative product from the same category if available. If other message: Show the error message from the response; suggest running the `products` command to check availability (for catering endpoints) |
| `503 Service Unavailable`   | No active catering event configured                            | Inform the user the catering system has no active event; contact the site admin                                                                                                                                                                                                                                                                                                                                                              |
| `500 Internal server error` | Something is wrong with the service, nothing the user can fix. | Inform the user that there is a problem with the service, this is nothing the user can fix; contact the site admin                                                                                                                                                                                                                                                                                                                           |

---

## Notes

- All monetary values in API responses are in **euro cents**. Always divide by 100 before displaying (`250` → `€2.50`).
- The `curl -s` flag suppresses progress output. Pipe through `| python3 -m json.tool` or similar if you want to inspect raw JSON.
- Tokens are managed at `/user/api-tokens` (web UI, requires login). Each token can have a name and optional expiry date.
