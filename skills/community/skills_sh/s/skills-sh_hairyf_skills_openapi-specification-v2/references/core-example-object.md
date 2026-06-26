---
name: core-example-object
description: Example Object for response examples by MIME type in Swagger 2.0
---

# Example Object

Allows sharing **examples** for operation responses. Used inside the [Response Object](responses.md) in the `examples` field. Maps a MIME type (from the operation's `produces`) to an example response value.

## Structure

**Patterned fields only:** Each key MUST be one of the operation's `produces` values (either set on the operation or inherited from the root). The value SHOULD be an example of what that response looks like (any valid JSON/value for that MIME type).

## Example

```yaml
responses:
  "200":
    description: A pet
    schema:
      $ref: "#/definitions/Pet"
    examples:
      application/json:
        name: Puma
        type: Dog
        color: Black
        gender: Female
        breed: Mixed
      application/xml: "<Pet><name>Puma</name><type>Dog</type></Pet>"
```

If the operation produces only `application/json`, the Example Object would typically have just an `application/json` key.

## Key points

- Example keys MUST be in the operation's `produces` list (implicit or inherited).
- Value can be any structure that matches the response schema/MIME type (object, array, string for XML, etc.).
- Use for documentation and for tools that generate sample responses; not for validation.

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
