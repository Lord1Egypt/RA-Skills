# TypeBox Error Transformation with @wthek

Guide for implementing `@wthek/typebox-transformer`.

---

## Installation

```bash
npm install @wthek/typebox-transformer @sinclair/typebox http-error-kit http-response-status-code
```

---

## 1. Throwing Pattern (`KitTypeBoxTransformer`)

Transforms any TypeBox validation error into a `KitHttpError` and throws it. If the error is not a TypeBox error, it is re-thrown unchanged:

```typescript
import { Type } from "@sinclair/typebox";
import { Value } from "@sinclair/typebox/value";
import { KitTypeBoxTransformer } from "@wthek/typebox-transformer";

const UserSchema = Type.Object({
  name: Type.String(),
  age: Type.Number({ minimum: 18 }),
});

try {
  Value.Assert(UserSchema, { name: "Himanshu", age: 14 });
} catch (err: unknown) {
  KitTypeBoxTransformer(err); // Throws KitHttpError with status 400 and issues
}
```

---

## 2. Non-Throwing Pattern (`fromTypeBoxError`)

Converts a TypeBox validation error into a `KitHttpError` instance or returns `null` if the error is not a recognized TypeBox error:

```typescript
import { Type } from "@sinclair/typebox";
import { Value } from "@sinclair/typebox/value";
import { fromTypeBoxError } from "@wthek/typebox-transformer";

const errors = [...Value.Errors(UserSchema, payload)];
const kitError = fromTypeBoxError(errors);

if (kitError) {
  // Pass to framework error handler or send response
  return res.status(kitError.statusCode).json(kitError.toJSON());
}
```

---

## 3. Supported Input Shapes

`fromTypeBoxError` and `KitTypeBoxTransformer` seamlessly accept:
- `TypeBoxError` instances (including `AssertError` from `Value.Assert`)
- `ValueError[]` arrays (e.g. `[...Value.Errors(schema, data)]`)
- `ValueErrorIterator` iterators directly (e.g. `Value.Errors(schema, data)`)
- Single `ValueError` objects
- Objects with an `.errors` property containing `ValueError[]`

---

## 4. Configuration Options

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `message` | `string` | `"TypeBox Validation Failed"` | Custom error message for the transformed error. |
| `statusCode` | `number` | `400` | Custom HTTP status code to assign to the validation error. |
