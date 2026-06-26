# WhatsApp Cloud API - Interactive Messages Reference

> **Author:** Bello Sanchez
> **API Version:** v21.0
> **Last Updated:** 2026-02-09

---

## Overview

Interactive messages allow businesses to present structured choices to users — buttons, lists, CTAs, and product catalogs. They are sent through the same messages endpoint with `type` set to `"interactive"`. This document covers all interactive message types, their constraints, and the corresponding webhook payloads when users interact with them.

---

## Endpoint

```
POST https://graph.facebook.com/v21.0/{phone-number-id}/messages
```

| Header          | Value                    |
|-----------------|--------------------------|
| `Authorization` | `Bearer {access-token}`  |
| `Content-Type`  | `application/json`       |

Every interactive message request body **must** include:

```json
{
  "messaging_product": "whatsapp",
  "to": "+18091234567",
  "type": "interactive",
  "interactive": { ... }
}
```

---

## Interactive Types Summary

| Type            | Description                              | Max Items         |
|-----------------|------------------------------------------|--------------------|
| `button`        | Reply buttons displayed inline           | 3 buttons          |
| `list`          | Scrollable list with sections and rows   | 10 sections, 10 rows per section |
| `cta_url`       | Call-to-action URL button                | 1 URL              |
| `product`       | Single product from a catalog            | 1 product          |
| `product_list`  | Multi-product list from a catalog        | 10 sections, 30 products total |

---

## Reply Buttons

Displays up to 3 inline buttons beneath a message body. Ideal for quick yes/no choices, confirmations, or simple branching.

### Constraints

| Field              | Limit                |
|--------------------|----------------------|
| Number of buttons  | Max 3                |
| Button title       | Max 20 characters    |
| Button ID          | Max 256 characters   |
| Body text          | Max 1024 characters  |
| Header text        | Max 60 characters    |
| Footer text        | Max 60 characters    |

### Request Body

```json
{
  "messaging_product": "whatsapp",
  "to": "+18091234567",
  "type": "interactive",
  "interactive": {
    "type": "button",
    "header": {
      "type": "text",
      "text": "Appointment Confirmation"
    },
    "body": {
      "text": "Your appointment is scheduled for March 15 at 2:00 PM. Would you like to confirm?"
    },
    "footer": {
      "text": "Reply to manage your booking"
    },
    "action": {
      "buttons": [
        {
          "type": "reply",
          "reply": {
            "id": "btn_confirm",
            "title": "Confirm"
          }
        },
        {
          "type": "reply",
          "reply": {
            "id": "btn_reschedule",
            "title": "Reschedule"
          }
        },
        {
          "type": "reply",
          "reply": {
            "id": "btn_cancel",
            "title": "Cancel"
          }
        }
      ]
    }
  }
}
```

### Optional Header Types

The `header` field supports multiple content types:

| Type       | Fields Required                |
|------------|--------------------------------|
| `text`     | `text` (string)                |
| `image`    | `link` or `id`                 |
| `video`    | `link` or `id`                 |
| `document` | `link` or `id`, `filename`     |

### Webhook Response (Button Click)

When the user taps a reply button, the webhook delivers:

```json
{
  "type": "interactive",
  "interactive": {
    "type": "button_reply",
    "button_reply": {
      "id": "btn_confirm",
      "title": "Confirm"
    }
  }
}
```

---

## List Messages

Displays a scrollable list of options organized into sections. Ideal for menus, catalogs, or any selection with more than 3 options.

### Constraints

| Field                | Limit                |
|----------------------|----------------------|
| Number of sections   | Max 10               |
| Rows per section     | Max 10               |
| Total rows           | Max 10 (across all sections) |
| Button text          | Max 20 characters    |
| Section title        | Max 24 characters    |
| Row title            | Max 24 characters    |
| Row description      | Max 72 characters    |
| Row ID               | Max 200 characters   |
| Body text            | Max 1024 characters  |
| Header text          | Max 60 characters    |
| Footer text          | Max 60 characters    |

### Request Body

```json
{
  "messaging_product": "whatsapp",
  "to": "+18091234567",
  "type": "interactive",
  "interactive": {
    "type": "list",
    "header": {
      "type": "text",
      "text": "Our Services"
    },
    "body": {
      "text": "Browse our available services and select one to learn more."
    },
    "footer": {
      "text": "Tap the button below to view options"
    },
    "action": {
      "button": "View Services",
      "sections": [
        {
          "title": "Consulting",
          "rows": [
            {
              "id": "svc_strategy",
              "title": "Strategy Session",
              "description": "1-hour business strategy consultation"
            },
            {
              "id": "svc_audit",
              "title": "Technical Audit",
              "description": "Full-stack architecture review"
            }
          ]
        },
        {
          "title": "Development",
          "rows": [
            {
              "id": "svc_mvp",
              "title": "MVP Build",
              "description": "Rapid prototype in 4 weeks"
            },
            {
              "id": "svc_custom",
              "title": "Custom Project",
              "description": "Tailored software development"
            }
          ]
        }
      ]
    }
  }
}
```

### Webhook Response (List Selection)

When the user selects a list row, the webhook delivers:

```json
{
  "type": "interactive",
  "interactive": {
    "type": "list_reply",
    "list_reply": {
      "id": "svc_strategy",
      "title": "Strategy Session",
      "description": "1-hour business strategy consultation"
    }
  }
}
```

---

## CTA URL Button

Displays a single call-to-action button that opens a URL when tapped. Useful for directing users to external pages, forms, or web applications.

### Constraints

| Field          | Limit                |
|----------------|----------------------|
| Display text   | Max 20 characters    |
| URL            | Must be a valid HTTPS URL |
| Body text      | Max 1024 characters  |
| Header text    | Max 60 characters    |
| Footer text    | Max 60 characters    |

### Request Body

```json
{
  "messaging_product": "whatsapp",
  "to": "+18091234567",
  "type": "interactive",
  "interactive": {
    "type": "cta_url",
    "header": {
      "type": "text",
      "text": "Your Order is Ready"
    },
    "body": {
      "text": "Track your order status and estimated delivery time on our portal."
    },
    "footer": {
      "text": "Order #12345"
    },
    "action": {
      "name": "cta_url",
      "parameters": {
        "display_text": "Track Order",
        "url": "https://example.com/orders/12345"
      }
    }
  }
}
```

> **Note:** CTA URL buttons do not generate a webhook callback. The user is redirected to the URL directly.

---

## Single Product Message

Displays a single product from a linked product catalog. Requires a Facebook Commerce catalog connected to the WhatsApp Business Account.

### Request Body

```json
{
  "messaging_product": "whatsapp",
  "to": "+18091234567",
  "type": "interactive",
  "interactive": {
    "type": "product",
    "body": {
      "text": "Check out this item we think you'll love."
    },
    "footer": {
      "text": "Free shipping on orders over $50"
    },
    "action": {
      "catalog_id": "CATALOG_ID",
      "product_retailer_id": "SKU-12345"
    }
  }
}
```

### Required Fields

| Field                  | Type   | Description                                      |
|------------------------|--------|--------------------------------------------------|
| `catalog_id`           | string | The Facebook Commerce catalog ID.                |
| `product_retailer_id`  | string | The product SKU / retailer ID from the catalog.  |

---

## Multi-Product Message

Displays multiple products organized into sections from a linked catalog. Users can browse and select products directly within the conversation.

### Constraints

| Field                    | Limit                          |
|--------------------------|--------------------------------|
| Sections                 | Max 10                         |
| Products per section     | Max 30                         |
| Total products           | Max 30 across all sections     |
| Section title            | Max 24 characters              |
| Header text              | Required, max 60 characters    |
| Body text                | Max 1024 characters            |

### Request Body

```json
{
  "messaging_product": "whatsapp",
  "to": "+18091234567",
  "type": "interactive",
  "interactive": {
    "type": "product_list",
    "header": {
      "type": "text",
      "text": "Featured Products"
    },
    "body": {
      "text": "Browse our top picks for this week."
    },
    "footer": {
      "text": "Prices may vary"
    },
    "action": {
      "catalog_id": "CATALOG_ID",
      "sections": [
        {
          "title": "Electronics",
          "product_items": [
            { "product_retailer_id": "SKU-001" },
            { "product_retailer_id": "SKU-002" }
          ]
        },
        {
          "title": "Accessories",
          "product_items": [
            { "product_retailer_id": "SKU-010" },
            { "product_retailer_id": "SKU-011" }
          ]
        }
      ]
    }
  }
}
```

---

## Webhook Payloads for Interactive Messages

All interactive webhook responses are nested under the `messages[].interactive` field in the webhook payload.

### Button Reply

```json
{
  "type": "interactive",
  "interactive": {
    "type": "button_reply",
    "button_reply": {
      "id": "btn_confirm",
      "title": "Confirm"
    }
  }
}
```

### List Reply

```json
{
  "type": "interactive",
  "interactive": {
    "type": "list_reply",
    "list_reply": {
      "id": "svc_strategy",
      "title": "Strategy Session",
      "description": "1-hour business strategy consultation"
    }
  }
}
```

### Product Inquiry (from Single or Multi-Product)

When a user interacts with a product message, the webhook may include an `order` object or a `product_inquiry` depending on the user's action. Consult the Conversations reference for the full webhook structure.

---

## Best Practices

1. **Use reply buttons for 2-3 options.** They have the highest engagement rate of any interactive type.
2. **Use lists for 4-10 options.** They keep the conversation clean and avoid long text menus.
3. **Keep button and row titles short.** Users scan quickly; concise labels perform better.
4. **Use unique, descriptive IDs.** The `id` field is what your application receives in the webhook — make it meaningful for routing logic (e.g., `btn_confirm_appt`, not `btn_1`).
5. **Always include body text.** While some fields are optional, body text provides essential context for the user's decision.
6. **Test on actual devices.** Interactive rendering varies slightly between iOS and Android WhatsApp clients.
