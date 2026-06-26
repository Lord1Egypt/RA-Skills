# VLM-Based Schema Generation Workflow

Use this 4-step workflow when generating schemas via VLM (claude-opus-4-6) instead of the Upstage API endpoint. VLM mode produces more carefully designed schemas with detailed extraction rules, at the cost of additional latency and tokens.

---

## Step 1: Gather parameters

**IMPORTANT: Always ask the user for ALL parameters in a single message and wait for their response before proceeding to Step 2. Do NOT generate the schema without first receiving the user's answers.**

Start your message with: "**If you provide multiple files, all documents will be analyzed to generate a single unified schema.**"

Then ask the user for the following. If they say they don't know or want the default, use the default shown.

| Parameter | Ask | Default |
|---|---|---|
| **Input** | "Please provide the file path or folder path of the document(s) to generate a schema for." | — (required) |
| **Output path** | "Please provide the path to save the generated schema (file name or folder). If not specified, the result will be displayed only." | (none — display only) |
| **lang** | "Please select the language for the schema keys/descriptions: (1) key(en) desc(en) (2) key(ko) desc(ko) (3) key(en) desc(ko) (4) key(ko) desc(en). If not specified, it will be set automatically based on the document language." | Infer from document's primary language — Korean document: key(ko) desc(ko); English document: key(en) desc(en) |
| **max_property_count** | "Please specify the maximum number of keys in the schema." | `33` |

**Input resolution rules:**
- Decide autonomously how many files to examine and how many pages per file to read in order to generate the best possible schema. More varied samples generally yield a more robust schema.

---

## Step 2: Read the documents

Read pages as images using claude-opus-4.6 (VLM).

After reading, identify:
- The document type (e.g., invoice, insurance form, bank statement, receipt)
- The main sections, tables, and key fields
- What information is most important for business use

---

## Step 3: Generate the property list (internal working format)

Produce a JSON object that strictly matches this schema:

```json
{
  "property_list": [
    {
      "key_name": "field_name_in_snake_case",
      "type": "<one of the allowed types>",
      "description": "<precise extraction rule>",
      "subkey": null
    },
    {
      "key_name": "table_field",
      "type": "array_of_object",
      "description": "<description of the table>",
      "subkey": [
        {
          "key_name": "subfield_name",
          "type": "<string | number | integer | boolean>",
          "description": "<precise extraction rule>"
        }
      ]
    }
  ]
}
```

**Allowed `type` values** (enum — no other values permitted):

| Type | Use when | Value when blank |
|---|---|---|
| `string` | Text, dates, IDs, codes, names | `""` |
| `number` | Decimal numbers (amounts, rates) | `0` |
| `integer` | Whole numbers (counts, indices) | `0` |
| `boolean` | Checkboxes, yes/no flags | `false` |
| `array_of_string` | Repeated scalar text values | `[]` |
| `array_of_number` | Repeated decimal values | `[]` |
| `array_of_integer` | Repeated whole number values | `[]` |
| `array_of_boolean` | Repeated boolean values | `[]` |
| `array_of_object` | Tables and repeated record groups — requires `subkey` | `[]` |

**Structural rules:**
- Every entry must have all four keys: `key_name`, `type`, `description`, `subkey`.
- `subkey` must be `null` for every type **except** `array_of_object`.
- `subkey` item types are limited to: `string`, `number`, `integer`, `boolean` (no nested arrays).
- If `type` is `array_of_object` but subkeys cannot be identified, fall back to `array_of_string`.
- Total number of top-level entries must not exceed `max_property_count`.

---

## Step 4: Convert to final JSON schema

Convert the `property_list` using the following rules and produce the exact structure below:

**Conversion rules:**
- Scalar types (`string`, `number`, `integer`, `boolean`) → `"type": "<type>"`
- `array_of_string/number/integer/boolean` → `"type": "array"`, `"items": { "type": "<scalar>" }`
- `array_of_object` with subkeys → `"type": "array"`, `"items": { "type": "object", "properties": { <subkeys> } }`
- `array_of_object` without subkeys → fall back to `"type": "array"`, `"items": { "type": "string" }`

**Required output structure:**

```json
{
  "type": "json_schema",
  "json_schema": {
    "name": "document_schema",
    "schema": {
      "type": "object",
      "properties": {
        "scalar_field": {
          "type": "string",
          "description": "..."
        },
        "array_scalar_field": {
          "type": "array",
          "description": "...",
          "items": { "type": "string" }
        },
        "table_field": {
          "type": "array",
          "description": "...",
          "items": {
            "type": "object",
            "properties": {
              "subfield_name": {
                "type": "string",
                "description": "..."
              }
            }
          }
        }
      }
    }
  }
}
```

For schema design rules (key naming, descriptions, table handling), see `schema-design.md`.
