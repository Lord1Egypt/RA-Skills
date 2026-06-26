---
name: parameters-collection-format
description: collectionFormat for array parameters and items in Swagger 2.0
---

# collectionFormat

Determines how **array** values are serialized for parameters (and for [Items Object](core-items-object.md) in parameters/headers). Used when `type` is `"array"` and `in` is not `"body"`.

## Values and where they apply

| Value   | Serialization        | Example     | Where allowed |
|---------|----------------------|-------------|----------------|
| csv     | Comma separated      | `foo,bar`   | Parameter (query, path, header, formData), Items, Header. Default. |
| ssv     | Space separated      | `foo bar`   | Parameter, Items, Header. |
| tsv     | Tab separated        | `foo\tbar`  | Parameter, Items, Header. |
| pipes   | Pipe separated       | `foo\|bar`  | Parameter, Items, Header. |
| multi   | Multiple instances   | `foo=bar&foo=baz` | **Parameter only**, and only when `in` is `"query"` or `"formData"`. |

- **multi:** Corresponds to multiple parameter instances (e.g. repeated query key), not multiple values in one instance. Valid only for parameters `in: "query"` or `in: "formData"`.
- **Items Object:** No `multi`; only csv, ssv, tsv, pipes (default csv).
- **Header Object:** No `multi`; only csv, ssv, tsv, pipes (default csv).

## Examples

**Query array (multi):**
```yaml
name: id
in: query
type: array
items:
  type: string
collectionFormat: multi
# Serialized as ?id=1&id=2&id=3
```

**Query array (csv, default):**
```yaml
name: tags
in: query
type: array
items:
  type: string
collectionFormat: csv
# Serialized as ?tags=foo,bar,baz
```

**Path parameter array (csv):**
```yaml
name: id
in: path
required: true
type: array
items:
  type: string
collectionFormat: csv
# Path segment: foo,bar,baz
```

## Key points

- Default is `csv` when not specified.
- Use `multi` only for query or formData parameters when the client sends multiple instances of the same parameter name.
- Headers and Items do not support `multi`.

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
