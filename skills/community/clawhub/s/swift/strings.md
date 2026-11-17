# Strings — Unicode, Indices, Substrings, Regex

Swift's `String` is a collection of **extended grapheme clusters** stored as UTF-8, not an array of bytes and not an array of code points. Every trap below follows from that one design choice, and it is the right one — the traps are the price of never producing a broken emoji.

## Counting and Comparing

- `count` is O(n): it walks the string counting grapheme clusters. Caching it in a loop condition is not premature optimization.
- Four different "lengths" of `"é"` written as `e` + combining accent: `count` 1, `unicodeScalars.count` 2, `utf8.count` 3, `utf16.count` 2. When an API demands a length, ask which one — NSRange and most C APIs mean UTF-16 and UTF-8 respectively.
- Comparison is canonical-equivalence based: precomposed `"é"` `==` decomposed `"é"` is **true** even though their bytes differ. Byte-identical comparison needs `a.utf8.elementsEqual(b.utf8)`.
- An emoji flag, a family emoji, and a skin-toned emoji are each `count == 1`. Truncating "safely" by grapheme cluster is why `String.prefix(n)` never splits one in half; truncating by `utf8` will.
- Case-insensitive user-facing comparison uses `localizedCaseInsensitiveCompare` / `localizedStandardContains`. `lowercased()` is locale-independent and gets Turkish dotless-i wrong; `localizedLowercase` respects the locale.
- Sorting user-visible lists uses `localizedStandardCompare` (Finder-style, digit-aware): plain `<` puts "Item 10" before "Item 9".

## Indices

- `String.Index` is an opaque position, not an integer, because the byte offset of the n-th character is not computable in O(1).
- An index from one string is invalid in another, even when the contents match — using it is undefined behavior, not a compile error.
- Indices are invalidated by mutation. Collect ranges first, then apply changes from the end backwards.
- Convert once when you must interoperate: `let ns = str as NSString` for NSRange work, or `String.Index(utf16Offset:in:)`. Converting per call inside a loop turns O(n) into O(n²).
- The idiomatic slice is `str[str.index(str.startIndex, offsetBy: k)...]`, and its cost is O(k) — if you are doing this in a loop, iterate with `indices` or `enumerated()` instead.

## Substrings

- `dropFirst`, `prefix`, `split`, and `[range]` all return `Substring`, which **shares the parent's storage**. Keeping one keeps the whole original string alive (SKILL.md Traps).
- Rule: `Substring` for the duration of a parse, `String(sub)` the moment a value is stored, returned across an API boundary, or put into a collection.
- `Substring` and `String` are different types but interchangeable in most generic code (`StringProtocol`). Writing APIs against `some StringProtocol` avoids forcing a copy on callers — but do not store a `StringProtocol` value.

## Splitting and Trimming

- `split(separator:)` (stdlib) drops empty subsequences by default; `components(separatedBy:)` (Foundation) keeps them. Parsing CSV with `split` silently collapses `a,,b` into two fields — pass `omittingEmptySubsequences: false`.
- `split(separator:maxSplits:)` stops early: the standard way to parse `key=value` where the value may contain `=`.
- `trimmingCharacters(in: .whitespacesAndNewlines)` is Foundation; `.whitespaces` alone leaves `\n` behind, which is the usual "my trimmed string still has a newline".
- Joining beats `+=` in a loop: `parts.joined(separator: ",")` allocates once (`performance.md`).

## Regex

- Literals `/\d+/` and the `Regex` type (`swift >=5.7`) are typed: captures come out as a tuple, and `RegexBuilder` gives named, strongly-typed captures for anything longer than a line.
- `firstMatch(of:)`, `wholeMatch(of:)`, `prefixMatch(of:)`, `replacing(_:with:)`, `split(separator:)` all accept a `Regex` — no NSRegularExpression bridging.
- On Apple platforms the `Regex` runtime is availability-gated to the OS versions that shipped it, so a project with an older `deployment_floor` still needs `NSRegularExpression`. Check before adopting.
- `/.../` literals conflict with a bare `/` operator in rare expressions; the compiler will tell you, and `Regex("…")` is the escape.
- Regex is the wrong tool for structured formats. For JSON use `Codable`; for dates use `Date.ParseStrategy`; for anything recursive write a parser.

## Formatting and Localization

- `String(localized:)` plus String Catalogs is the current path on Apple platforms; the key is the source string, so editing English text silently orphans translations unless you set an explicit key.
- Plurals need a plural rule in the catalog, never `count == 1 ? "item" : "items"` — most languages have more than two forms.
- Numbers, dates, and measurements go through `formatted()` / `FormatStyle`: `value.formatted(.currency(code: "EUR"))` picks the user's separators and symbol placement. Hand-rolled `String(format: "%.2f")` produces a period in locales that use a comma.
- `String(format:)` is Foundation and unchecked: a mismatched specifier reads garbage memory. Interpolation is safe and usually shorter.
- Interpolating an optional prints `Optional("x")`.

## Performance Notes

- Small strings up to 15 UTF-8 bytes are stored inline in the `String` value on 64-bit — no allocation, no ARC. Beyond that a heap buffer is allocated and shared by copy-on-write.
- Appending in a loop is amortized O(1) with geometric growth; `reserveCapacity` still helps when the final size is known.
- Bridging to `NSString` is lazy in one direction and copying in the other; a hot loop that crosses the bridge per iteration will show up in the profiler as `_bridgeToObjectiveC` (`interop.md`).
- For byte-level work (hashing, protocol framing) operate on `str.utf8` directly rather than converting to `[UInt8]`.
