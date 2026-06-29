# Send a Custom Greeting Card Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `send-a-greeting-card`

x402 availability: not enabled for this product.

## `create_proof`

Action slug: `create-proof`

Price: `400` credits

Upload the card to Click2Mail and create the print job without mailing. Used for final review before committing to send.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `back_image_file_id` | `string` | no | File ID for back image. |
| `back_image_url` | `string` | no | Image URL for back of card. |
| `back_text` | `string` | no | Text for back of card. |
| `document_pdf_file_id` | `string` | no | File ID of a print-ready PDF (raw PDF mode). |
| `document_pdf_url` | `string` | no | Public URL to a print-ready 2-page PDF (raw PDF mode). |
| `font_style` | `string` | no | Font style for text panels. |
| `front_cover_image_file_id` | `string` | no | File ID of front cover image. |
| `front_cover_image_url` | `string` | no | URL to front cover image (JPG/PNG). |
| `inside_left_image_file_id` | `string` | no | File ID for inside left image. |
| `inside_left_image_url` | `string` | no | Image URL for inside left panel. |
| `inside_left_text` | `string` | no | Text for inside left panel. |
| `inside_right_image_file_id` | `string` | no | File ID for inside right image. |
| `inside_right_image_url` | `string` | no | Image URL for inside right panel. |
| `inside_right_text` | `string` | no | Text for inside right panel — the main message area. |
| `orientation` | `string` | no | Card orientation. horizontal: landscape panels. vertical: portrait panels. |
| `recipient_address` | `object` | yes | Recipient mailing address (US only). Must include name or organization. |

Sample parameters:

```json
{
  "back_image_file_id": "example back image file id",
  "back_image_url": "https://example.com",
  "back_text": "example back text",
  "document_pdf_file_id": "example document pdf file id",
  "document_pdf_url": "https://example.com",
  "font_style": "handwritten",
  "front_cover_image_file_id": "example front cover image file id",
  "front_cover_image_url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "back_image_file_id": {
    "description": "File ID for back image.",
    "required": false,
    "type": "string"
  },
  "back_image_url": {
    "description": "Image URL for back of card.",
    "required": false,
    "type": "string"
  },
  "back_text": {
    "description": "Text for back of card.",
    "required": false,
    "type": "string"
  },
  "document_pdf_file_id": {
    "description": "File ID of a print-ready PDF (raw PDF mode).",
    "required": false,
    "type": "string"
  },
  "document_pdf_url": {
    "description": "Public URL to a print-ready 2-page PDF (raw PDF mode).",
    "required": false,
    "type": "string"
  },
  "font_style": {
    "default": "handwritten",
    "description": "Font style for text panels.",
    "enum": [
      "handwritten",
      "elegant",
      "modern",
      "classic"
    ],
    "required": false,
    "type": "string"
  },
  "front_cover_image_file_id": {
    "description": "File ID of front cover image.",
    "required": false,
    "type": "string"
  },
  "front_cover_image_url": {
    "description": "URL to front cover image (JPG/PNG).",
    "required": false,
    "type": "string"
  },
  "inside_left_image_file_id": {
    "description": "File ID for inside left image.",
    "required": false,
    "type": "string"
  },
  "inside_left_image_url": {
    "description": "Image URL for inside left panel.",
    "required": false,
    "type": "string"
  },
  "inside_left_text": {
    "description": "Text for inside left panel.",
    "required": false,
    "type": "string"
  },
  "inside_right_image_file_id": {
    "description": "File ID for inside right image.",
    "required": false,
    "type": "string"
  },
  "inside_right_image_url": {
    "description": "Image URL for inside right panel.",
    "required": false,
    "type": "string"
  },
  "inside_right_text": {
    "description": "Text for inside right panel — the main message area.",
    "required": false,
    "type": "string"
  },
  "orientation": {
    "default": "horizontal",
    "description": "Card orientation. horizontal: landscape panels. vertical: portrait panels.",
    "enum": [
      "horizontal",
      "vertical"
    ],
    "required": false,
    "type": "string"
  },
  "recipient_address": {
    "description": "Recipient mailing address (US only). Must include name or organization.",
    "properties": {
      "address1": {
        "description": "Street address line 1.",
        "required": true,
        "type": "string"
      },
      "address2": {
        "description": "Street address line 2.",
        "required": false,
        "type": "string"
      },
      "city": {
        "description": "City.",
        "required": true,
        "type": "string"
      },
      "name": {
        "description": "Recipient full name.",
        "required": false,
        "type": "string"
      },
      "organization": {
        "description": "Organization name (can be used instead of or with name).",
        "required": false,
        "type": "string"
      },
      "postal_code": {
        "description": "ZIP code.",
        "required": true,
        "type": "string"
      },
      "state": {
        "description": "Two-letter state code.",
        "required": true,
        "type": "string"
      }
    },
    "required": true,
    "type": "object"
  }
}
```

## `get_order_status`

Action slug: `get-order-status`

Price: `400` credits

Check the status of a previously sent or proofed card order. Automatically includes USPS tracking information when available.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `order_id` | `string` | yes | Order ID returned from a previous send or create_proof call. |

Sample parameters:

```json
{
  "order_id": "example order id"
}
```

Generated JSON parameter schema:

```json
{
  "order_id": {
    "description": "Order ID returned from a previous send or create_proof call.",
    "required": true,
    "type": "string"
  }
}
```

## `get_tracking`

Action slug: `get-tracking`

Price: `400` credits

Get USPS tracking details for a previously sent card order.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `order_id` | `string` | yes | Order ID returned from a previous send call. |
| `tracking_type` | `string` | no | Tracking type. Default: IMB. |

Sample parameters:

```json
{
  "order_id": "example order id",
  "tracking_type": "IMB"
}
```

Generated JSON parameter schema:

```json
{
  "order_id": {
    "description": "Order ID returned from a previous send call.",
    "required": true,
    "type": "string"
  },
  "tracking_type": {
    "description": "Tracking type. Default: IMB.",
    "enum": [
      "IMB",
      "IMPB"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `list_orders`

Action slug: `list-orders`

Price: `400` credits

List past greeting card orders for the current budget, sorted by most recent first.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `limit` | `integer` | no | Number of orders to return. |

Sample parameters:

```json
{
  "limit": 10
}
```

Generated JSON parameter schema:

```json
{
  "limit": {
    "default": 10,
    "description": "Number of orders to return.",
    "maximum": 50,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```

## `render_preview`

Action slug: `render-preview`

Price: `400` credits

Generate a preview of the greeting card without mailing. Returns the generated PDF and preview images with signed URLs for review before sending.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `back_image_file_id` | `string` | no | File ID for back image. |
| `back_image_url` | `string` | no | Image URL for back of card. |
| `back_text` | `string` | no | Text for back of card (small branding, attribution, etc.). |
| `document_pdf_file_id` | `string` | no | File ID of a print-ready PDF in cloud storage (raw PDF mode). |
| `document_pdf_url` | `string` | no | Public URL to a print-ready 2-page PDF (raw PDF mode, mutually exclusive with card builder fields). |
| `font_style` | `string` | no | Font style for text panels. handwritten = blue pen-on-paper, elegant = charcoal formal, modern = clean contemporary, classic = traditional black. |
| `front_cover_image_file_id` | `string` | no | File ID of front cover image. Alternative to URL for card builder mode. |
| `front_cover_image_url` | `string` | no | URL to front cover image (JPG/PNG). Required for card builder mode. |
| `inside_left_image_file_id` | `string` | no | File ID for inside left image. |
| `inside_left_image_url` | `string` | no | Image URL for inside left panel. Provide text OR image for each panel, not both. |
| `inside_left_text` | `string` | no | Text for inside left panel (visible when card is opened, left side). |
| `inside_right_image_file_id` | `string` | no | File ID for inside right image. |
| `inside_right_image_url` | `string` | no | Image URL for inside right panel. |
| `inside_right_text` | `string` | no | Text for inside right panel — the main message area. Provide text OR image, not both. |
| `orientation` | `string` | no | Card orientation. horizontal: landscape panels, card folds along top edge. vertical: portrait panels, card folds along left edge. |

Sample parameters:

```json
{
  "back_image_file_id": "example back image file id",
  "back_image_url": "https://example.com",
  "back_text": "example back text",
  "document_pdf_file_id": "example document pdf file id",
  "document_pdf_url": "https://example.com",
  "font_style": "handwritten",
  "front_cover_image_file_id": "example front cover image file id",
  "front_cover_image_url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "back_image_file_id": {
    "description": "File ID for back image.",
    "required": false,
    "type": "string"
  },
  "back_image_url": {
    "description": "Image URL for back of card.",
    "required": false,
    "type": "string"
  },
  "back_text": {
    "description": "Text for back of card (small branding, attribution, etc.).",
    "required": false,
    "type": "string"
  },
  "document_pdf_file_id": {
    "description": "File ID of a print-ready PDF in cloud storage (raw PDF mode).",
    "required": false,
    "type": "string"
  },
  "document_pdf_url": {
    "description": "Public URL to a print-ready 2-page PDF (raw PDF mode, mutually exclusive with card builder fields).",
    "required": false,
    "type": "string"
  },
  "font_style": {
    "default": "handwritten",
    "description": "Font style for text panels. handwritten = blue pen-on-paper, elegant = charcoal formal, modern = clean contemporary, classic = traditional black.",
    "enum": [
      "handwritten",
      "elegant",
      "modern",
      "classic"
    ],
    "required": false,
    "type": "string"
  },
  "front_cover_image_file_id": {
    "description": "File ID of front cover image. Alternative to URL for card builder mode.",
    "required": false,
    "type": "string"
  },
  "front_cover_image_url": {
    "description": "URL to front cover image (JPG/PNG). Required for card builder mode.",
    "required": false,
    "type": "string"
  },
  "inside_left_image_file_id": {
    "description": "File ID for inside left image.",
    "required": false,
    "type": "string"
  },
  "inside_left_image_url": {
    "description": "Image URL for inside left panel. Provide text OR image for each panel, not both.",
    "required": false,
    "type": "string"
  },
  "inside_left_text": {
    "description": "Text for inside left panel (visible when card is opened, left side).",
    "required": false,
    "type": "string"
  },
  "inside_right_image_file_id": {
    "description": "File ID for inside right image.",
    "required": false,
    "type": "string"
  },
  "inside_right_image_url": {
    "description": "Image URL for inside right panel.",
    "required": false,
    "type": "string"
  },
  "inside_right_text": {
    "description": "Text for inside right panel — the main message area. Provide text OR image, not both.",
    "required": false,
    "type": "string"
  },
  "orientation": {
    "default": "horizontal",
    "description": "Card orientation. horizontal: landscape panels, card folds along top edge. vertical: portrait panels, card folds along left edge.",
    "enum": [
      "horizontal",
      "vertical"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `send`

Action slug: `send`

Price: `400` credits

Generate the card PDF, print it on premium cardstock, fold it, envelope it, and mail it via USPS First Class to the recipient address.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `back_image_file_id` | `string` | no | File ID for back image. |
| `back_image_url` | `string` | no | Image URL for back of card. |
| `back_text` | `string` | no | Text for back of card. |
| `document_pdf_file_id` | `string` | no | File ID of a print-ready PDF (raw PDF mode). |
| `document_pdf_url` | `string` | no | Public URL to a print-ready 2-page PDF (raw PDF mode). |
| `font_style` | `string` | no | Font style for text panels. |
| `front_cover_image_file_id` | `string` | no | File ID of front cover image. |
| `front_cover_image_url` | `string` | no | URL to front cover image (JPG/PNG). |
| `inside_left_image_file_id` | `string` | no | File ID for inside left image. |
| `inside_left_image_url` | `string` | no | Image URL for inside left panel. |
| `inside_left_text` | `string` | no | Text for inside left panel. |
| `inside_right_image_file_id` | `string` | no | File ID for inside right image. |
| `inside_right_image_url` | `string` | no | Image URL for inside right panel. |
| `inside_right_text` | `string` | no | Text for inside right panel — the main message area. |
| `orientation` | `string` | no | Card orientation. horizontal: landscape panels. vertical: portrait panels. |
| `recipient_address` | `object` | yes | Recipient mailing address (US only). Must include name or organization. |

Sample parameters:

```json
{
  "back_image_file_id": "example back image file id",
  "back_image_url": "https://example.com",
  "back_text": "example back text",
  "document_pdf_file_id": "example document pdf file id",
  "document_pdf_url": "https://example.com",
  "font_style": "handwritten",
  "front_cover_image_file_id": "example front cover image file id",
  "front_cover_image_url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "back_image_file_id": {
    "description": "File ID for back image.",
    "required": false,
    "type": "string"
  },
  "back_image_url": {
    "description": "Image URL for back of card.",
    "required": false,
    "type": "string"
  },
  "back_text": {
    "description": "Text for back of card.",
    "required": false,
    "type": "string"
  },
  "document_pdf_file_id": {
    "description": "File ID of a print-ready PDF (raw PDF mode).",
    "required": false,
    "type": "string"
  },
  "document_pdf_url": {
    "description": "Public URL to a print-ready 2-page PDF (raw PDF mode).",
    "required": false,
    "type": "string"
  },
  "font_style": {
    "default": "handwritten",
    "description": "Font style for text panels.",
    "enum": [
      "handwritten",
      "elegant",
      "modern",
      "classic"
    ],
    "required": false,
    "type": "string"
  },
  "front_cover_image_file_id": {
    "description": "File ID of front cover image.",
    "required": false,
    "type": "string"
  },
  "front_cover_image_url": {
    "description": "URL to front cover image (JPG/PNG).",
    "required": false,
    "type": "string"
  },
  "inside_left_image_file_id": {
    "description": "File ID for inside left image.",
    "required": false,
    "type": "string"
  },
  "inside_left_image_url": {
    "description": "Image URL for inside left panel.",
    "required": false,
    "type": "string"
  },
  "inside_left_text": {
    "description": "Text for inside left panel.",
    "required": false,
    "type": "string"
  },
  "inside_right_image_file_id": {
    "description": "File ID for inside right image.",
    "required": false,
    "type": "string"
  },
  "inside_right_image_url": {
    "description": "Image URL for inside right panel.",
    "required": false,
    "type": "string"
  },
  "inside_right_text": {
    "description": "Text for inside right panel — the main message area.",
    "required": false,
    "type": "string"
  },
  "orientation": {
    "default": "horizontal",
    "description": "Card orientation. horizontal: landscape panels. vertical: portrait panels.",
    "enum": [
      "horizontal",
      "vertical"
    ],
    "required": false,
    "type": "string"
  },
  "recipient_address": {
    "description": "Recipient mailing address (US only). Must include name or organization.",
    "properties": {
      "address1": {
        "description": "Street address line 1.",
        "required": true,
        "type": "string"
      },
      "address2": {
        "description": "Street address line 2.",
        "required": false,
        "type": "string"
      },
      "city": {
        "description": "City.",
        "required": true,
        "type": "string"
      },
      "name": {
        "description": "Recipient full name.",
        "required": false,
        "type": "string"
      },
      "organization": {
        "description": "Organization name (can be used instead of or with name).",
        "required": false,
        "type": "string"
      },
      "postal_code": {
        "description": "ZIP code.",
        "required": true,
        "type": "string"
      },
      "state": {
        "description": "Two-letter state code.",
        "required": true,
        "type": "string"
      }
    },
    "required": true,
    "type": "object"
  }
}
```
