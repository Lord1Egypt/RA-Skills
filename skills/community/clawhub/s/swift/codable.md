# Codable — Decoding Real-World JSON Without Guessing

`Codable` is strict by design: it fails loudly rather than producing a half-filled model. That is the right default and the reason every trap below is really "the server did something the type didn't allow".

## Read the Error Before Touching the Model

```swift
do { model = try JSONDecoder().decode(Payload.self, from: data) }
catch let error as DecodingError { print(error) }   // names the exact codingPath
```

- `DecodingError` has four cases and each names the culprit: `.keyNotFound(key, context)`, `.typeMismatch(type, context)`, `.valueNotFound(type, context)`, `.dataCorrupted(context)`. `context.codingPath` is the full path to the failing node — the single most useful string in the whole subsystem.
- `try?` and `try!` both destroy that information (SKILL.md Traps). Never debug a decode with either.
- "The data couldn't be read because it isn't in the correct format" is `.dataCorrupted` at the top level: usually an HTML error page or an empty body, not a model problem. Print the first 200 bytes.

## Defaults Are Not Applied

A property with a default value still throws `keyNotFound` when the key is absent — the synthesized `init(from:)` decodes every property and ignores initializer defaults. Three fixes, in order of preference:

1. Make the property optional (`var nickname: String?`) when absence is meaningful.
2. Write `init(from:)` and use `decodeIfPresent(_:forKey:) ?? default` for the few keys that need it.
3. Wrap with a property wrapper that supplies the default on decode — worth it only past a handful of properties (`metaprogramming.md`).

Related: writing `CodingKeys` by hand is all-or-nothing. Omitting a case excludes that property from **both** encoding and decoding, which silently drops data on the round trip.

## Key and Value Strategies

- `keyDecodingStrategy = .convertFromSnakeCase` handles `created_at` → `createdAt` for the whole payload. It mangles acronyms (`user_id` → `userId`, but `id_str` → `idStr`), so per-key `CodingKeys` still beats it for a small model.
- Mixing the strategy with explicit `CodingKeys` is a common source of "this one key never decodes": the strategy runs first, then your key string is matched against the converted name.
- `dateDecodingStrategy = .iso8601` uses the standard formatter **without** fractional seconds, so `2026-07-25T10:30:00.123Z` fails. For fractional-second timestamps use `.custom` with a formatter that has `.withFractionalSeconds`, or `.formatted(...)`.
- The default date strategy (`.deferredToDate`) is seconds since the 2001 reference date, not epoch. Decoding a Unix timestamp with the default silently produces dates 31 years off — use `.secondsSince1970` / `.millisecondsSince1970`.
- `dataDecodingStrategy` defaults to base64 for `Data`.
- `nonConformingFloatDecodingStrategy` is required if the payload can contain `NaN` or `Infinity`; JSON has no literal for them, so the default throws.

## Type Coercion the Decoder Won't Do

- `"123"` does not decode into `Int`, and `1`/`0` do not decode into `Bool`. Decode the wire type and convert in `init(from:)`.
- APIs that send a field as a string sometimes and a number other times need a small enum or a `try?`-cascade in a custom decoder. Model the ambiguity once, at the boundary — never spread `Any` through the app.
- JSON `null` decodes to `nil` for an optional property; a **missing** key also decodes to `nil` for an optional property. If the difference matters (PATCH semantics), you need a three-state wrapper, not an optional.
- Enum raw values must match exactly, case included: `"ACTIVE"` does not decode into `case active = "active"`. For forward compatibility give the enum an `unknown` case and a custom `init(from:)` that falls back to it — new server values then stop breaking old clients.

## Nesting, Flattening, and Polymorphism

- Flattening a nested object into a flat model: nested `CodingKeys` enums plus `nestedContainer(keyedBy:forKey:)` in a custom `init(from:)`.
- A response wrapper (`{"data": {...}, "meta": {...}}`) is better modeled as a generic `struct Envelope<T: Decodable>: Decodable` than as bespoke keys in every model.
- Heterogeneous arrays: decode a discriminator key first from the same container, switch on it, then decode the concrete type. Pattern:

```swift
let type = try container.decode(String.self, forKey: .type)
switch type {
case "text":  self = .text(try TextBlock(from: decoder))
case "image": self = .image(try ImageBlock(from: decoder))
default:      self = .unknown
}
```

- Arrays where one bad element should not fail the batch: decode into a wrapper that captures `Result` per element, using an `UnkeyedDecodingContainer` and `try?` around each item. Log the failures — silent skipping hides API drift for months.

## Encoding

- `outputFormatting = [.sortedKeys]` for anything compared, hashed, or committed to a file. Default key order is unspecified and changes.
- `.prettyPrinted` for fixtures and debugging only. The indentation inflates the payload — roughly 1.3-2x on typical documents, more as nesting deepens — and no client reads it.
- Encoding an optional that is nil omits the key. To emit an explicit `null`, encode the optional with `encode(_:forKey:)` on a container that was given the value explicitly, or model it with a three-state wrapper.
- `Encodable` synthesis includes computed properties never — only stored ones. A field that must appear on the wire but is derived needs a manual `encode(to:)`.

## Performance and Alternatives

- `JSONDecoder` allocates heavily; decoding thousands of small payloads per second is a real cost. Reuse one decoder instance (they are configuration objects, cheap to keep, safe when not mutated concurrently).
- For very large payloads, streaming or a leaner parser beats `Codable`; measure before adopting one, because the maintenance cost is real.
- `Codable` conformance on a type with 40 properties generates a lot of code — a known contributor to slow builds in model-heavy modules (`performance.md`).
- `PropertyListEncoder` shares the API for plists; `JSONSerialization` remains the escape hatch when the shape is genuinely dynamic, but convert to typed models at the boundary rather than passing dictionaries around.
