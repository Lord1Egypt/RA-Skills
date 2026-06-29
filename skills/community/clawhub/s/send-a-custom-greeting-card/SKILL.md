---
name: send-a-custom-greeting-card
description: "Send a Custom Greeting Card: Mail custom folded greeting cards to any US address. Use when an agent needs send a custom greeting card, send a greeting card, holiday greeting card campaigns, customer appreciation and thank you cards, birthday and anniversary greetings, event invitation mailings, create proof, orientation through AgentPMT-hosted remote tool calls. Discovery terms: send a custom greeting card, send a greeting card, holiday greeting card campaigns."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/send-a-greeting-card
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/send-a-greeting-card"}}
---
# Send a Custom Greeting Card

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Mail custom folded greeting cards to any US address. You control all four panels: front cover (image), inside left, inside right (main message), and back — each panel can be text or image. Cards can be printed in horizontal or vertical orientation. Four font styles for text: handwritten (blue), elegant (charcoal), modern (near-black), classic (black). Printed on premium cardstock, folded, enveloped, and mailed via USPS First Class with tracking.

## Product Instructions
### Send a Custom Greeting Card

Mail custom folded greeting cards to any US address. Provide panel content (front cover image, inside text/images, back text/image) and the backend generates a print-ready PDF, prints it on premium 120# white uncoated cardstock, folds it, envelopes it, and mails it via USPS First Class.

#### Overview

This tool creates and mails physical folded greeting cards. There are two modes:

- **Card Builder Mode (recommended):** Provide individual panel content (front cover image, inside left/right text or images, back text or image) and the system assembles a print-ready 2-page PDF automatically.
- **Raw PDF Mode:** Provide your own pre-built 2-page PDF (must be exactly 2 pages, 5.5 x 8.5 inches flat).

The recommended workflow is: preview first, then send after user approval.

##### Panel Layout

```
PAGE 1 (outside)            PAGE 2 (inside)
+------------------+        +------------------+
|   BACK panel     |        |   INSIDE LEFT    |
|  (rotated 180)   |        |                  |
+------------------+        +------------------+
|   FRONT COVER    |        |   INSIDE RIGHT   |
|  (right-side up) |        |   (message area) |
+------------------+        +------------------+
```

- **Front cover** -- always an image (required in card builder mode). This is the card front when folded.
- **Inside left** -- text or image (optional). Visible when card is opened, left side.
- **Inside right** -- text or image (optional). The main message/greeting area.
- **Back** -- text or image (optional). Small branding, attribution, etc.

Each panel accepts text OR image (not both). Panels left empty render as blank white.

##### Physical Card Specs
- Flat sheet: 5.5 x 8.5 inches portrait (1650 x 2550 px at 300 DPI)
- Folded: 5.5 x 4.25 inches
- Paper: 120# White Uncoated premium cardstock
- Mailed in envelope with printed address via USPS First Class

#### Actions

##### render_preview

Generate a preview of the card without mailing. Returns the generated PDF (with signed URL) and preview images (front and inside JPGs with signed URLs) for the user to review before committing to send.

**Required parameters (card builder mode -- at least one panel content field):**
- `front_cover_image_url` (string) -- URL to front cover image (JPG/PNG). Required in card builder mode.
- OR `front_cover_image_file_id` (string) -- File ID of front cover image. Alternative to URL.

**Required parameters (raw PDF mode -- exactly one of):**
- `document_pdf_url` (string) -- Public URL to a print-ready 2-page PDF.
- `document_pdf_file_id` (string) -- File ID of a print-ready PDF in cloud storage.

**Optional parameters (card builder mode):**
- `orientation` (string, default: `"horizontal"`) -- Card orientation. `horizontal`: landscape panels, card folds along top edge. `vertical`: portrait panels, card folds along left edge.
- `font_style` (string, default: `"handwritten"`) -- Font style for text panels. Options: `handwritten` (Caveat, blue), `elegant` (Playfair Display, charcoal), `modern` (Montserrat, near-black), `classic` (Liberation Serif, black).
- `inside_left_text` (string) -- Text for inside left panel.
- `inside_left_image_url` (string) -- Image URL for inside left panel.
- `inside_left_image_file_id` (string) -- File ID for inside left image.
- `inside_right_text` (string) -- Text for inside right panel (main message area).
- `inside_right_image_url` (string) -- Image URL for inside right panel.
- `inside_right_image_file_id` (string) -- File ID for inside right image.
- `back_text` (string) -- Text for back of card.
- `back_image_url` (string) -- Image URL for back of card.
- `back_image_file_id` (string) -- File ID for back image.

###### Example: Preview with card builder

```json
{
  "action": "render_preview",
  "front_cover_image_url": "https://example.com/front.jpg",
  "inside_right_text": "Happy Birthday!\n\nWishing you all the best.",
  "font_style": "handwritten"
}
```

###### Example: Preview with raw PDF

```json
{
  "action": "render_preview",
  "document_pdf_url": "https://example.com/my-card.pdf"
}
```

##### create_proof

Upload the card to the print service and create the print job without mailing. This creates the job in the print system for final review. Requires a recipient address.

**Required parameters:**
- Card content: same as `render_preview` (card builder fields or raw PDF).
- `recipient_address` (object) -- Recipient mailing address (US only). Required fields within: `address1`, `city`, `state` (two-letter code), `postal_code`. Must also include `name` or `organization` (or both).

**Optional parameters:**
- All card builder options from `render_preview` (`orientation`, `font_style`, panel content fields).

###### Example: Create proof

```json
{
  "action": "create_proof",
  "front_cover_image_file_id": "FILE_ID",
  "inside_right_text": "Thank you for your business!",
  "font_style": "elegant",
  "recipient_address": {
    "name": "Jane Doe",
    "address1": "123 Main St",
    "city": "Austin",
    "state": "TX",
    "postal_code": "78701"
  }
}
```

##### send

Generate the card PDF, print it, and mail it to the recipient. Returns the order ID, document PDF (with signed URL), and preview images.

**Required parameters:**
- Card content: same as `render_preview` (card builder fields or raw PDF).
- `recipient_address` (object) -- Recipient mailing address (US only). Required fields within: `address1`, `city`, `state` (two-letter code), `postal_code`. Must also include `name` or `organization` (or both). Optional: `address2`, `country` (defaults to "US").

**Optional parameters:**
- All card builder options from `render_preview` (`orientation`, `font_style`, panel content fields).

###### Example: Send a greeting card (card builder)

```json
{
  "action": "send",
  "front_cover_image_file_id": "FILE_ID",
  "inside_right_text": "Happy Birthday!\n\nWishing you all the best.",
  "back_text": "Made with love",
  "font_style": "elegant",
  "orientation": "horizontal",
  "recipient_address": {
    "name": "Jane Doe",
    "address1": "123 Main St",
    "city": "Austin",
    "state": "TX",
    "postal_code": "78701"
  }
}
```

###### Example: Send with all panels filled

```json
{
  "action": "send",
  "front_cover_image_url": "https://example.com/holiday-photo.jpg",
  "inside_left_image_url": "https://example.com/family-photo.jpg",
  "inside_right_text": "Season's Greetings!\n\nWishing you warmth and joy this holiday season.",
  "back_text": "From the Smith Family, 2026",
  "font_style": "classic",
  "recipient_address": {
    "name": "The Johnson Family",
    "address1": "789 Pine Rd",
    "city": "Denver",
    "state": "CO",
    "postal_code": "80202"
  }
}
```

##### get_order_status

Check the status of a previously sent or proofed card order. Automatically includes USPS tracking information when available.

**Required parameters:**
- `order_id` (string) -- Order ID returned from a previous `send` or `create_proof` call.

###### Example: Check order status

```json
{
  "action": "get_order_status",
  "order_id": "ORDER_ID"
}
```

##### get_tracking

Get USPS tracking details for a previously sent card order.

**Required parameters:**
- `order_id` (string) -- Order ID returned from a previous `send` call.

**Optional parameters:**
- `tracking_type` (string) -- Tracking barcode type. Options: `IMB` (Intelligent Mail Barcode, default), `IMPB` (Intelligent Mail Package Barcode).

###### Example: Get tracking

```json
{
  "action": "get_tracking",
  "order_id": "ORDER_ID"
}
```

###### Example: Get package tracking

```json
{
  "action": "get_tracking",
  "order_id": "ORDER_ID",
  "tracking_type": "IMPB"
}
```

##### list_orders

List past greeting card orders for the current budget, sorted by most recent first.

**Optional parameters:**
- `limit` (integer, default: 10, min: 1, max: 50) -- Number of orders to return.

###### Example: List recent orders

```json
{
  "action": "list_orders",
  "limit": 10
}
```

#### Workflows

##### Preview then send (recommended)
1. Call `render_preview` with the card content to generate a proof.
2. The response includes `document_file` (full PDF with signed URL) and `preview_images` (front and inside JPGs with signed URLs). Show these to the user for review.
3. Once the user approves, call `send` with the same card content plus `recipient_address`.

##### Create proof then approve
1. Call `create_proof` with card content and recipient address to create a print job without mailing.
2. Review the proof in the print system.
3. Use the order ID to check status with `get_order_status`.

##### Check delivery status
1. After sending, save the `order_id` from the response.
2. Call `get_order_status` with that `order_id` to check printing and mailing status.
3. Use `get_tracking` for detailed USPS tracking information.

#### Notes

- **US addresses only.** International mailing is not supported.
- **Recipient must include `name` or `organization`** (or both) in the address.
- **Card builder mode and raw PDF mode are mutually exclusive.** Use one or the other; providing both returns an error.
- **Each panel is text OR image, not both.** Providing both text and image for the same panel returns an error.
- **Front cover image is required** in card builder mode. It must be a direct link to a JPG or PNG image.
- **For each image panel,** provide either the URL or file ID, not both.
- **Raw PDF must be exactly 2 pages.** Page 1 is the outside (front cover + back), page 2 is the inside (left + right panels).
- **Font auto-sizing:** Text is automatically sized to fit within the panel (72px max, 18px min).
- **Preview files expire after 7 days.** The signed URLs for document PDFs and preview images are temporary.
- **Text supports newlines.** Use `\n` in text fields for line breaks.
- **Images are cover-cropped** to fill the panel exactly (no margins, no distortion).

## When To Use
- Use this skill for `Send a Custom Greeting Card` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: send a custom greeting card, send a greeting card, holiday greeting card campaigns, customer appreciation and thank you cards, birthday and anniversary greetings, event invitation mailings, create proof, orientation.
- Supported action names: `create_proof`, `get_order_status`, `get_tracking`, `list_orders`, `render_preview`, `send`.

## Use Cases
- Holiday greeting card campaigns
- Customer appreciation and thank-you cards
- Birthday and anniversary greetings
- Event invitation mailings
- Nonprofit donor outreach cards
- Real estate follow-up mailers
- Employee recognition cards
- Brand loyalty and retention mailings
- Condolence and sympathy cards
- Welcome and onboarding cards

## Related Product Skills
- File Storage - Over 10MB: ../file-storage-over-10mb (ClawHub: `file-storage-over-10mb`, page: https://clawhub.ai/agentpmt/file-storage-over-10mb; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-storage-over-10mb`)
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)
- File Storage - 10MB or less: ../file-storage-10mb-or-less (ClawHub: `file-storage-10mb-or-less`, page: https://clawhub.ai/agentpmt/file-storage-10mb-or-less; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-storage-10mb-or-less`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `6`.
x402 availability: not enabled for this product.

- `create_proof` (action slug: `create-proof`): Upload the card to Click2Mail and create the print job without mailing. Used for final review before committing to send. Price: `400` credits. Parameters: `back_image_file_id`, `back_image_url`, `back_text`, `document_pdf_file_id`, `document_pdf_url`, `font_style`, `front_cover_image_file_id`, `front_cover_image_url`, plus 8 more.
- `get_order_status` (action slug: `get-order-status`): Check the status of a previously sent or proofed card order. Automatically includes USPS tracking information when available. Price: `400` credits. Parameters: `order_id`.
- `get_tracking` (action slug: `get-tracking`): Get USPS tracking details for a previously sent card order. Price: `400` credits. Parameters: `order_id`, `tracking_type`.
- `list_orders` (action slug: `list-orders`): List past greeting card orders for the current budget, sorted by most recent first. Price: `400` credits. Parameters: `limit`.
- `render_preview` (action slug: `render-preview`): Generate a preview of the greeting card without mailing. Returns the generated PDF and preview images with signed URLs for review before sending. Price: `400` credits. Parameters: `back_image_file_id`, `back_image_url`, `back_text`, `document_pdf_file_id`, `document_pdf_url`, `font_style`, `front_cover_image_file_id`, `front_cover_image_url`, plus 7 more.
- `send` (action slug: `send`): Generate the card PDF, print it on premium cardstock, fold it, envelope it, and mail it via USPS First Class to the recipient address. Price: `400` credits. Parameters: `back_image_file_id`, `back_image_url`, `back_text`, `document_pdf_file_id`, `document_pdf_url`, `font_style`, `front_cover_image_file_id`, `front_cover_image_url`, plus 8 more.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "send-a-greeting-card"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "send-a-greeting-card"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "send-a-greeting-card"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "send-a-greeting-card"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "send-a-greeting-card"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "send-a-greeting-card"
  }
}
```

## Call This Tool
Product slug: `send-a-greeting-card`

Marketplace page: https://www.agentpmt.com/marketplace/send-a-greeting-card

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Send-a-Custom-Greeting-Card",
    "arguments": {
      "action": "create_proof",
      "back_image_file_id": "example back image file id",
      "back_image_url": "https://example.com",
      "back_text": "example back text",
      "document_pdf_file_id": "example document pdf file id",
      "document_pdf_url": "https://example.com",
      "font_style": "handwritten",
      "front_cover_image_file_id": "example front cover image file id",
      "front_cover_image_url": "https://example.com"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "send-a-greeting-card",
  "parameters": {
    "action": "create_proof",
    "back_image_file_id": "example back image file id",
    "back_image_url": "https://example.com",
    "back_text": "example back text",
    "document_pdf_file_id": "example document pdf file id",
    "document_pdf_url": "https://example.com",
    "font_style": "handwritten",
    "front_cover_image_file_id": "example front cover image file id",
    "front_cover_image_url": "https://example.com"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `create_proof` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/send-a-greeting-card
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
