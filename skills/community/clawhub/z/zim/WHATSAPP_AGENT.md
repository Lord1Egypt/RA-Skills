# Zim WhatsApp Agent

## Overview
The Zim WhatsApp Agent allows users to search and book travel via natural language over WhatsApp.

## How It Works
1. User sends a message like "Find me a flight from Dubai to Copenhagen on May 1"
2. The intent parser extracts: type, origin, destination, dates, class, travelers
3. Zim searches flights/hotels/cars via Travelpayouts
4. Results are formatted for WhatsApp (bullet lists, no markdown tables)
5. User confirms a selection to proceed with booking

## Usage

```python
from zim.whatsapp_agent import ZimWhatsAppAgent

agent = ZimWhatsAppAgent()
response = agent.handle_message("Find flights DXB to CPH May 1", user_id="user123")
print(response)
```

## Example Conversations

**Flight search:**
> User: I need a business class flight from Dubai to London next Friday
> Agent: Found 3 flights DXB → LHR for May 16:
> • Emirates EK 29 — 7h 10m — $1,240
> • British Airways BA 108 — 7h 25m — $1,180
> • Qatar QR 16 — 8h 05m (via DOH) — $980
> Reply with 1, 2, or 3 to select.

**Hotel search:**
> User: Find me a hotel in Copenhagen for 3 nights from May 1
> Agent: Found 3 hotels in Copenhagen (May 1-4):
> • Hotel d'Angleterre ★★★★★ — $420/nt
> • Nimb Hotel ★★★★★ — $340/nt
> • Copenhagen Admiral Hotel ★★★★ — $180/nt
> Reply with 1, 2, or 3 to select.

## Integration with OpenClaw WhatsApp
Configure in your OpenClaw agent to route travel-related messages to the Zim WhatsApp agent handler.
