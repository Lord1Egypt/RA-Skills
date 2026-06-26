---
name: swift-codable
description: "Implement Swift Codable models for JSON and property-list encoding and decoding with JSONDecoder, JSONEncoder, CodingKeys, and custom init(from:) or encode(to:). Use when parsing API responses, remapping keys, flattening nested JSON, handling date or data decoding strategies, decoding heterogeneous arrays, or integrating Codable with URLSession, SwiftData, or UserDefaults."
---

# Swift Codable

Encode and decode Swift types using `Codable` (`Encodable & Decodable`) with
`JSONEncoder`, `JSONDecoder`, and related APIs. Targets Swift 6.3 / iOS 26+.

## Contents

- [Basic Conformance](#basic-conformance)
- [Custom CodingKeys](#custom-codingkeys)
- [Custom Decoding and Encoding](#custom-decoding-and-encoding)
- [Nested and Flattened Containers](#nested-and-flattened-containers)
- [Heterogeneous Arrays](#heterogeneous-arrays)
- [Date Decoding Strategies](#date-decoding-strategies)
- [Data and Key Strategies](#data-and-key-strategies)
- [Lossy Array Decoding](#lossy-array-decoding)
- [Single Value Containers](#single-value-containers)
- [Default Values for Missing Keys](#default-values-for-missing-keys)
- [Encoder and Decoder Configuration](#encoder-and-decoder-configuration)
- [Codable with URLSession](#codable-with-urlsession)
- [Codable with SwiftData](#codable-with-swiftdata)
- [Codable with UserDefaults](#codable-with-userdefaults)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Basic Conformance

When all stored properties are themselves `Codable`, the compiler synthesizes
conformance automatically:

```swift
struct User: Codable {
    let id: Int
    let name: String
    let email: String
    let isVerified: Bool
}

let user = try JSONDecoder().decode(User.self, from: jsonData)
let encoded = try JSONEncoder().encode(user)
```

Prefer `Decodable` for read-only API responses and `Encodable` for write-only.
Use `Codable` only when both directions are required.

## Custom CodingKeys

Rename JSON keys without writing a custom decoder by declaring a `CodingKeys`
enum:

```swift
struct Product: Codable {
    let id: Int
    let displayName: String
    let imageURL: URL
    let priceInCents: Int

    enum CodingKeys: String, CodingKey {
        case id
        case displayName = "display_name"
        case imageURL = "image_url"
        case priceInCents = "price_in_cents"
    }
}
```

Every stored property must appear in the enum. Omitting a property from
`CodingKeys` excludes it from encoding/decoding -- provide a default value or
compute it separately.

## Custom Decoding and Encoding

Override `init(from:)` and `encode(to:)` for transformations the synthesized
conformance cannot handle:

```swift
struct Event: Codable {
    let name: String
    let timestamp: Date
    let tags: [String]

    enum CodingKeys: String, CodingKey {
        case name, timestamp, tags
    }

    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        name = try container.decode(String.self, forKey: .name)
        // Decode Unix timestamp as Double, convert to Date
        let epoch = try container.decode(Double.self, forKey: .timestamp)
        timestamp = Date(timeIntervalSince1970: epoch)
        // Default to empty array when key is missing
        tags = try container.decodeIfPresent([String].self, forKey: .tags) ?? []
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(name, forKey: .name)
        try container.encode(timestamp.timeIntervalSince1970, forKey: .timestamp)
        try container.encode(tags, forKey: .tags)
    }
}
```

## Nested and Flattened Containers

Use `nestedContainer(keyedBy:forKey:)` to navigate and flatten nested JSON:

```swift
// JSON: { "id": 1, "location": { "lat": 37.7749, "lng": -122.4194 } }
struct Place: Decodable {
    let id: Int
    let latitude: Double
    let longitude: Double

    enum CodingKeys: String, CodingKey { case id, location }
    enum LocationKeys: String, CodingKey { case lat, lng }

    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        id = try container.decode(Int.self, forKey: .id)
        let location = try container.nestedContainer(
            keyedBy: LocationKeys.self, forKey: .location)
        latitude = try location.decode(Double.self, forKey: .lat)
        longitude = try location.decode(Double.self, forKey: .lng)
    }
}
```

Chain multiple `nestedContainer` calls to flatten deeply nested structures.
Also use `nestedUnkeyedContainer(forKey:)` for nested arrays.

## Heterogeneous Arrays

Decode arrays of mixed types using a discriminator field:

```swift
// JSON: [{"type":"text","content":"Hello"},{"type":"image","url":"pic.jpg"}]
enum ContentBlock: Decodable {
    case text(String)
    case image(URL)

    enum CodingKeys: String, CodingKey { case type, content, url }

    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        let type = try container.decode(String.self, forKey: .type)
        switch type {
        case "text":
            let content = try container.decode(String.self, forKey: .content)
            self = .text(content)
        case "image":
            let url = try container.decode(URL.self, forKey: .url)
            self = .image(url)
        default:
            throw DecodingError.dataCorruptedError(
                forKey: .type, in: container,
                debugDescription: "Unknown type: \(type)")
        }
    }
}

let blocks = try JSONDecoder().decode([ContentBlock].self, from: jsonData)
```

## Date Decoding Strategies

Configure `JSONDecoder.dateDecodingStrategy` to match your API:

```swift
let decoder = JSONDecoder()

// ISO 8601 (e.g., "2024-03-15T10:30:00Z")
decoder.dateDecodingStrategy = .iso8601

// Unix timestamp in seconds (e.g., 1710499800)
decoder.dateDecodingStrategy = .secondsSince1970

// Custom DateFormatter
let formatter = DateFormatter()
formatter.dateFormat = "yyyy-MM-dd"
formatter.locale = Locale(identifier: "en_US_POSIX")
formatter.timeZone = TimeZone(secondsFromGMT: 0)
decoder.dateDecodingStrategy = .formatted(formatter)

// Custom closure for multiple formats
decoder.dateDecodingStrategy = .custom { decoder in
    let container = try decoder.singleValueContainer()
    let string = try container.decode(String.self)
    if let date = ISO8601DateFormatter().date(from: string) { return date }
    throw DecodingError.dataCorruptedError(
        in: container, debugDescription: "Cannot decode date: \(string)")
}
```

Set the matching strategy on `JSONEncoder`:
`encoder.dateEncodingStrategy = .iso8601`

## Data and Key Strategies

```swift
let decoder = JSONDecoder()
decoder.dataDecodingStrategy = .base64           // Base64-encoded Data fields
decoder.keyDecodingStrategy = .convertFromSnakeCase  // simple keys only; not URL/ID spelling
// {"user_name": "Alice"} maps to `var userName: String` -- no CodingKeys needed

let encoder = JSONEncoder()
encoder.dataEncodingStrategy = .base64
encoder.keyEncodingStrategy = .convertToSnakeCase
```

Use key strategies only for mechanical snake_case-to-camelCase mappings.
`convertFromSnakeCase` maps by spelling, not Swift acronym/initialism policy:
`image_url`, `base_uri`, and `user_id` match `imageUrl`, `baseUri`, and
`userId` only. If the Swift model uses `imageURL`, `baseURI`, or `userID`,
declare explicit `CodingKeys`; the strategy will not synthesize those names.

## Lossy Array Decoding

By default, one invalid element fails the entire array. Use a wrapper to skip
invalid elements:

```swift
struct LossyArray<Element: Decodable>: Decodable {
    let elements: [Element]

    init(from decoder: Decoder) throws {
        var container = try decoder.unkeyedContainer()
        var elements: [Element] = []
        while !container.isAtEnd {
            if let element = try? container.decode(Element.self) {
                elements.append(element)
            } else {
                _ = try? container.decode(AnyCodableValue.self) // advance past bad element
            }
        }
        self.elements = elements
    }
}
private struct AnyCodableValue: Decodable {}
```

## Single Value Containers

Wrap primitives for type safety using `singleValueContainer()`:

```swift
struct UserID: Codable, Hashable {
    let rawValue: String

    init(_ rawValue: String) { self.rawValue = rawValue }

    init(from decoder: Decoder) throws {
        let container = try decoder.singleValueContainer()
        rawValue = try container.decode(String.self)
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.singleValueContainer()
        try container.encode(rawValue)
    }
}
// JSON: "usr_abc123" decodes directly to UserID
```

## Default Values for Missing Keys

Stored property defaults such as `var theme = "system"` do not make synthesized
`Decodable` tolerate a missing nonoptional key; synthesis still fails unless the
property is optional or decoded manually. Use `decodeIfPresent` with
nil-coalescing when a missing or null key should fall back:

```swift
struct Settings: Decodable {
    let theme: String
    let fontSize: Int
    let notificationsEnabled: Bool

    enum CodingKeys: String, CodingKey {
        case theme, fontSize = "font_size"
        case notificationsEnabled = "notifications_enabled"
    }

    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        theme = try container.decodeIfPresent(String.self, forKey: .theme) ?? "system"
        fontSize = try container.decodeIfPresent(Int.self, forKey: .fontSize) ?? 16
        notificationsEnabled = try container.decodeIfPresent(
            Bool.self, forKey: .notificationsEnabled) ?? true
    }
}
```

## Encoder and Decoder Configuration

```swift
let encoder = JSONEncoder()
encoder.outputFormatting = [.prettyPrinted, .sortedKeys, .withoutEscapingSlashes]

let decoder = JSONDecoder()
// Non-conforming floats (NaN, Infinity are not valid JSON)
encoder.nonConformingFloatEncodingStrategy = .convertToString(
    positiveInfinity: "Infinity", negativeInfinity: "-Infinity", nan: "NaN")
decoder.nonConformingFloatDecodingStrategy = .convertFromString(
    positiveInfinity: "Infinity", negativeInfinity: "-Infinity", nan: "NaN")
```

### PropertyListEncoder / PropertyListDecoder

```swift
let plistEncoder = PropertyListEncoder()
plistEncoder.outputFormat = .xml  // or .binary
let data = try plistEncoder.encode(settings)
let decoded = try PropertyListDecoder().decode(Settings.self, from: data)
```

## Codable with URLSession

```swift
func fetchUser(id: Int) async throws -> User {
    let url = URL(string: "https://api.example.com/users/\(id)")!
    let (data, response) = try await URLSession.shared.data(from: url)
    guard let http = response as? HTTPURLResponse,
          (200...299).contains(http.statusCode) else {
        throw APIError.invalidResponse
    }
    let decoder = JSONDecoder()
    decoder.keyDecodingStrategy = .convertFromSnakeCase  // simple keys only; keep CodingKeys for URL/URI/ID
    decoder.dateDecodingStrategy = .iso8601
    return try decoder.decode(User.self, from: data)
}

// Generic API envelope. Configure a decoder inside this helper because
// fetchUser's decoder is out of scope.
struct APIResponse<T: Decodable>: Decodable {
    let data: T
    let meta: Meta?
    struct Meta: Decodable { let page: Int; let totalPages: Int }
}

func decodeUsersEnvelope(from data: Data) throws -> [User] {
    let decoder = JSONDecoder()
    decoder.keyDecodingStrategy = .convertFromSnakeCase  // simple keys only; keep CodingKeys for URL/URI/ID
    decoder.dateDecodingStrategy = .iso8601
    return try decoder.decode(APIResponse<[User]>.self, from: data).data
}
```

## Codable with SwiftData

SwiftData persists compatible noncomputed stored properties declared on `@Model`
types. Use `Codable` structs, enums, and other value types directly when that
value is part of the durable model schema:

```swift
struct Address: Codable {
    var street: String
    var city: String
    var zipCode: String
}

@Model class Contact {
    var name: String
    var address: Address?  // Codable value-type property stored by SwiftData
    init(name: String, address: Address? = nil) {
        self.name = name; self.address = address
    }
}
```

Do not recommend `@Attribute(.transformable)`, encoded `Data`, or encoded
`String` as a fallback in this Codable skill. Keep schema data as typed
SwiftData properties and defer unsupported persistence designs to the SwiftData skill.

## Codable with UserDefaults

`@AppStorage` is only for small UserDefaults-backed preferences. Store `Bool`,
numeric, `String`, or a `RawRepresentable` type with a primitive raw value. For
a small `Codable` preference payload, prefer `RawRepresentable` with JSON
`String` raw storage so `@AppStorage` binds the typed preference directly:

```swift
struct UserPreferences: Codable {
    var showOnboarding: Bool = true
    var accentColor: String = "blue"
}

extension UserPreferences: RawRepresentable {
    init?(rawValue: String) {
        guard let data = rawValue.data(using: .utf8),
              let decoded = try? JSONDecoder().decode(Self.self, from: data)
        else { return nil }
        self = decoded
    }
    var rawValue: String {
        guard let data = try? JSONEncoder().encode(self),
              let string = String(data: data, encoding: .utf8)
        else { return "{}" }
        return string
    }
}

struct SettingsView: View {
    @AppStorage("userPrefs") private var prefs = UserPreferences()
    var body: some View {
        Toggle("Show Onboarding", isOn: $prefs.showOnboarding)
    }
}
```

## Common Mistakes

**1. Not handling missing defaulted fields:**
```swift
// DON'T -- crashes if key is absent
let value = try container.decode(String.self, forKey: .bio)
// DO -- falls back when the key is absent or null
let value = try container.decodeIfPresent(String.self, forKey: .bio) ?? ""
```

**2. Failing entire array when one element is invalid:**
```swift
// DON'T -- one bad element kills the whole decode
let items = try container.decode([Item].self, forKey: .items)
// DO -- use LossyArray or decode elements individually
let items = try container.decode(LossyArray<Item>.self, forKey: .items).elements
```

**3. Date strategy mismatch:**
```swift
// DON'T -- default strategy expects Double, but API sends ISO string
let decoder = JSONDecoder()  // dateDecodingStrategy defaults to .deferredToDate
// DO -- set strategy to match your API format
decoder.dateDecodingStrategy = .iso8601
```

**4. Force-unwrapping decoded optionals:**
```swift
// DON'T
let user = try? decoder.decode(User.self, from: data)
print(user!.name)
// DO
guard let user = try? decoder.decode(User.self, from: data) else { return }
```

**5. Using Codable when only Decodable is needed:**
```swift
// DON'T -- unnecessarily constrains the type to also be Encodable
struct APIResponse: Codable { let id: Int; let message: String }
// DO -- use Decodable for read-only API responses
struct APIResponse: Decodable { let id: Int; let message: String }
```

**6. Manual CodingKeys for simple snake_case APIs:**
```swift
// DON'T -- verbose boilerplate for every model
enum CodingKeys: String, CodingKey {
    case userName = "user_name"
    case avatarUrl = "avatar_url"
}
// DO -- configure once on the decoder for simple cases
decoder.keyDecodingStrategy = .convertFromSnakeCase
// Keep CodingKeys for `imageURL`, `baseURI`, `userID`, and similar names.
```

## Review Checklist

- [ ] Types conform to `Decodable` only when encoding is not needed
- [ ] `decodeIfPresent` used with defaults for optional or missing keys
- [ ] `keyDecodingStrategy = .convertFromSnakeCase` used for simple snake_case APIs, with CodingKeys retained for acronym spellings
- [ ] `dateDecodingStrategy` matches the API date format
- [ ] Arrays of unreliable data use lossy decoding to skip invalid elements
- [ ] Custom `init(from:)` validates and transforms data instead of post-decode fixups
- [ ] `JSONEncoder.outputFormatting` includes `.sortedKeys` for deterministic test output
- [ ] Wrapper types (UserID, etc.) use `singleValueContainer` for clean JSON
- [ ] Generic `APIResponse<T>` wrapper used for consistent API envelope handling
- [ ] No force-unwrapping of decoded values
- [ ] Persistence boundary is explicit: SwiftData only for compatible noncomputed model properties, `@AppStorage`/UserDefaults only for small primitive or `RawRepresentable` preferences

## References

- [Codable](https://sosumi.ai/documentation/swift/codable/) -- protocol combining Encodable and Decodable
- [JSONDecoder](https://sosumi.ai/documentation/foundation/jsondecoder/) -- decodes JSON data into Codable types
- [JSONEncoder](https://sosumi.ai/documentation/foundation/jsonencoder/) -- encodes Codable types as JSON data
- [CodingKey](https://sosumi.ai/documentation/swift/codingkey/) -- protocol for encoding/decoding keys
- [JSONDecoder.KeyDecodingStrategy.convertFromSnakeCase](https://sosumi.ai/documentation/foundation/jsondecoder/keydecodingstrategy-swift.enum/convertfromsnakecase) -- snake-case conversion behavior and limitations
- [Encoding and Decoding Custom Types](https://sosumi.ai/documentation/foundation/encoding-and-decoding-custom-types/) -- Apple guide on custom Codable conformance
- [Using JSON with Custom Types](https://sosumi.ai/documentation/foundation/archives_and_serialization/using_json_with_custom_types/) -- Apple sample code for JSON patterns
- [Preserving your app's model data across launches](https://sosumi.ai/documentation/swiftdata/preserving-your-apps-model-data-across-launches) -- SwiftData model property compatibility
