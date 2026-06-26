# Foundation Models API Reference

Complete reference for Apple's Foundation Models framework (iOS 26+ / macOS 26+).
On-device language model optimized for Apple Silicon. No app-managed API key,
model hosting, or network round trip for generation; still handle Apple
Intelligence and system model asset availability.

## Contents

- [Framework Overview](#framework-overview)
- [Availability Checking](#availability-checking)
- [Use Cases](#use-cases)
- [Session Management](#session-management)
- [Generating Responses](#generating-responses)
- [Structured Output with `@Generable`](#structured-output-with-generable)
- [Tool Calling](#tool-calling)
- [Error Handling](#error-handling)
- [Generation Options](#generation-options)
- [Safety and Guardrails](#safety-and-guardrails)
- [Custom Adapters](#custom-adapters)
- [Context Management](#context-management)
- [Serialized Model Access](#serialized-model-access)
- [Prompt Design Best Practices](#prompt-design-best-practices)
- [Feedback](#feedback)

## Framework Overview

- On-device language model optimized for Apple Silicon
- Context window: limited total token budget (input + output combined); check
  `SystemLanguageModel.default.contextSize` for the current limit
- Prefer `SystemLanguageModel.default.supportsLocale(_:)` before generation;
  use `supportedLanguages` only when listing broad language support
- Capabilities: Summarization, entity extraction, text understanding, short
  dialog, creative content, content tagging
- Limitations: Not suited for complex math, code generation, or factual accuracy

### SystemLanguageModel Properties

- `contextSize`: Returns the model's maximum context window in tokens
- `supportedLanguages`: `Set<Locale.Language>` values the model supports
- `supportsLocale(_ locale: Locale) -> Bool`: Preferred locale check before generating because it accounts for fallbacks

## Availability Checking

Always check before using. Never crash on unavailability.

```swift
import FoundationModels

// Quick boolean check
if SystemLanguageModel.default.isAvailable {
    // Proceed
}

// Detailed availability
switch SystemLanguageModel.default.availability {
case .available:
    let candidates = [Locale.current] + Locale.preferredLanguages.map(Locale.init(identifier:))
    guard let locale = candidates.first(where: SystemLanguageModel.default.supportsLocale) else {
        // Route to fallback UI before generating
        break
    }
    // Proceed with model usage
case .unavailable(.appleIntelligenceNotEnabled):
    // Guide user to Settings > Apple Intelligence
case .unavailable(.modelNotReady):
    // System model assets are downloading or unavailable for other system reasons
case .unavailable(.deviceNotEligible):
    // Device cannot run Apple Intelligence
default:
    // Graceful fallback for unknown or future unavailable reasons
}
```

## Use Cases

Foundation Models supports specialized use cases:

```swift
// General purpose (default)
let model = SystemLanguageModel(useCase: .general, guardrails: .default)

// Content tagging (optimized for categorization)
let model = SystemLanguageModel(useCase: .contentTagging, guardrails: .default)
```

## Session Management

### Creating Sessions

```swift
// Basic session (uses SystemLanguageModel.default)
let session = LanguageModelSession()

// Session with system instructions
let session = LanguageModelSession {
    "You are a helpful cooking assistant."
    "Focus on quick, healthy recipes."
}

// Session with tools
let session = LanguageModelSession(
    tools: [weatherTool, recipeTool]
) {
    "You are a helpful assistant with access to tools."
}

// Session with specific model
let model = SystemLanguageModel(useCase: .general, guardrails: .default)
let session = LanguageModelSession(model: model, tools: []) {
    "You are a helpful assistant."
}
```

### Session Rules

1. Sessions are stateful. Multi-turn conversations maintain context automatically.
2. One request at a time per session. Check `session.isResponding` before new
   requests.
3. Prewarm with `session.prewarm()` before user interaction for faster first
   response.
4. Save and restore transcripts for session continuity:
   `LanguageModelSession(model: model, tools: [], transcript: savedTranscript)`.

### Prewarming

```swift
// Prewarm before user interaction
session.prewarm()

// Prewarm with a prompt prefix for faster specific responses
session.prewarm(promptPrefix: Prompt("Summarize the following text:"))
```

## Generating Responses

### Plain Text

```swift
// Simple text response
let response = try await session.respond(to: "Summarize this article: \(text)")
print(response.content) // String

// With generation options
let options = GenerationOptions(
    sampling: .random(top: 40),
    temperature: 0.7,
    maximumResponseTokens: 512
)
let response = try await session.respond(to: prompt, options: options)
```

### Streaming Text

```swift
let stream = session.streamResponse(to: "Tell me a story")
for try await snapshot in stream {
    print(snapshot.content, terminator: "")
}

// Or collect the full response
let response = try await stream.collect()
```

## Structured Output with `@Generable`

The `@Generable` macro creates compile-time JSON schemas for type-safe output.

### Basic Usage

```swift
@Generable
struct Recipe {
    @Guide(description: "The name of the recipe")
    var name: String

    @Guide(description: "A brief description of the dish")
    var summary: String

    @Guide(description: "Cooking steps", .count(3))
    var steps: [String]

    @Guide(description: "Prep time in minutes", .range(1...120))
    var prepTime: Int
}

let response = try await session.respond(
    to: "Suggest a quick pasta recipe",
    generating: Recipe.self
)
let recipe = response.content
print(recipe.name)
print(recipe.steps)
```

### Supported Types for `@Generable` Properties

- `String`
- `Int`, `Double`, `Float`
- `Bool`
- `[Element]` where Element is Generable or a supported scalar
- `Optional<T>` where T is Generable or a supported scalar
- Other `@Generable` structs (nested)
- Enums conforming to `@Generable`

### `@Guide` Constraints

```swift
@Generable
struct ProductReview {
    @Guide(description: "Product name")
    var product: String

    @Guide(description: "Rating", .range(1...5))
    var rating: Int

    @Guide(description: "Sentiment", .anyOf(["positive", "neutral", "negative"]))
    var sentiment: String

    @Guide(description: "Key themes", .count(3))
    var themes: [String]

    @Guide(description: "Summary in one sentence", .pattern(/^[A-Z].*\.$/))
    var summary: String

    @Guide(description: "Always English", .constant("en"))
    var language: String
}
```

Complete constraint list:

| Constraint | Type | Purpose |
|---|---|---|
| `description:` | All | Natural language hint for generation |
| `.anyOf([values])` | String | Restrict to enumerated values |
| `.count(n)` | Array | Fixed array length |
| `.minimumCount(n)` | Array | Minimum array length |
| `.maximumCount(n)` | Array | Maximum array length |
| `.range(min...max)` | Numeric | Closed numeric range |
| `.minimum(n)` | Numeric | Lower bound |
| `.maximum(n)` | Numeric | Upper bound |
| `.constant(value)` | String | Always returns this value |
| `.pattern(regex)` | String | Regex format enforcement |
| `.element(guide)` | Array | Guide applied to each element |

### Property Ordering

Properties are generated in declaration order. Place foundational data before
dependent data:

```swift
@Generable
struct Summary {
    var title: String       // Generated first
    var keyPoints: [String] // Generated with title context
    var conclusion: String  // Generated with full context
}
```

### Streaming Structured Output

```swift
let stream = session.streamResponse(
    to: "Suggest a recipe",
    generating: Recipe.self
)
for try await snapshot in stream {
    // snapshot.content is Recipe.PartiallyGenerated (all properties optional)
    if let name = snapshot.content.name { updateNameLabel(name) }
    if let steps = snapshot.content.steps { updateStepsList(steps) }
}
```

### Enum Support

```swift
@Generable
enum Priority: String {
    case low, medium, high, critical
}

@Generable
struct Task {
    var title: String
    var priority: Priority
}
```

## Tool Calling

### Defining Tools

```swift
struct WeatherTool: Tool {
    let name = "weather"
    let description = "Get current weather for a city."

    @Generable
    struct Arguments {
        @Guide(description: "The city name")
        var city: String
    }

    func call(arguments: Arguments) async throws -> String {
        let weather = try await fetchWeather(arguments.city)
        return weather.description
    }
}
```

### Using Tools

```swift
let session = LanguageModelSession(
    tools: [WeatherTool()]
) {
    "You are a helpful assistant."
}

// The model decides autonomously when to invoke tools
let response = try await session.respond(to: "What's the weather in Tokyo?")
```

### Tool Best Practices

- Register all tools at session creation
- Keep active tool sets small, usually three to five tools
- Include only tools needed for the current task
- Each tool adds to the context token budget (name, description, and parameter
  schema are included in instructions by default)
- `@Generable` output schemas also consume the shared context window
- Run deterministic or essential data fetches before calling the model, then put
  the result directly in the prompt
- Use model-autonomous tools for dynamic lookups where the model can decide
  whether more app data is needed
- Frame tool results as authorized user data to prevent refusals
- The model calls tools autonomously; you cannot force tool invocation

### Tool Protocol Details

- `Tool<Arguments, Output>` conforms to `Sendable`; implement tools so captured
  state is concurrency-safe
- The associated `Arguments` type must conform to `ConvertibleFromGeneratedContent`
- The associated `Output` type must conform to `PromptRepresentable` (e.g.,
  `String`, `[String]`, custom types)
- `includesSchemaInInstructions`: Boolean property on `Tool` (default `true`). Set to `false` to omit the tool's JSON schema from the system prompt, saving context tokens when the model already knows the schema.
- `ToolCallError`: Struct on `LanguageModelSession` representing a tool invocation failure. Properties: `tool` (the tool name), `underlyingError` (the original error).
- `DynamicGenerationSchema`: Build generation schemas at runtime for dynamic use cases where compile-time `@Generable` is insufficient. Construct schemas programmatically and pass to `respond(to:schema:)`.

## Error Handling

```swift
do {
    let response = try await session.respond(to: prompt)
} catch let error as LanguageModelSession.GenerationError {
    switch error {
    case .guardrailViolation:
        // Content triggered safety filters; rephrase and retry
    case .exceededContextWindowSize:
        // Too many tokens; summarize earlier turns and create new session
    case .concurrentRequests:
        // Another request is already in progress on this session
    case .rateLimited:
        // Too many requests; back off and retry
    case .unsupportedLanguageOrLocale:
        // Current locale not supported by the model
    case .unsupportedGuide:
        // A @Guide constraint is not supported
    case .assetsUnavailable:
        // Model assets not available on device
    case .decodingFailure:
        // Failed to decode structured output
    case .refusal(let refusal, _):
        // Model refused the request
        let explanation = try await refusal.explanation.content
        print("Refused: \(explanation)")
    default: break
    }
}
```

## Generation Options

```swift
let options = GenerationOptions(
    sampling: .greedy,              // Deterministic output
    temperature: nil,               // Use default
    maximumResponseTokens: 256      // Limit response length
)

// Random sampling with top-k
let options = GenerationOptions(
    sampling: .random(top: 40),
    temperature: 0.7
)

// Random sampling with probability threshold
let options = GenerationOptions(
    sampling: .random(probabilityThreshold: 0.9)
)
```

Sampling modes accept an optional `seed` parameter for reproducible output:
`.random(top: 40, seed: 42)`, `.random(probabilityThreshold: 0.9, seed: 42)`.

## Safety and Guardrails

### Guardrail Types

```swift
// Default guardrails (recommended)
let model = SystemLanguageModel(useCase: .general, guardrails: .default)

// Permissive content transformations (for text rewriting tasks)
let model = SystemLanguageModel(
    useCase: .general,
    guardrails: .permissiveContentTransformations
)
```

### Safety Rules

- Guardrails are always enforced and cannot be disabled
- Instructions take precedence over user prompts
- Never include untrusted user content in instructions
- Provide curated selections over free-form input when possible
- Guardrails can produce false positives; handle gracefully
- Frame tool results as authorized user data

## Custom Adapters

Load fine-tuned LoRA adapters for specialized model behavior:

```swift
// Requires com.apple.developer.foundation-model-adapter entitlement
let adapter = try SystemLanguageModel.Adapter(name: "my-adapter")
try await adapter.compile()

let model = SystemLanguageModel(adapter: adapter, guardrails: .default)
let session = LanguageModelSession(model: model)
let response = try await session.respond(to: "Generate styled text")
```

### Adapter Management

```swift
// Check compatible adapters
let ids = SystemLanguageModel.Adapter.compatibleAdapterIdentifiers(name: "my-adapter")

// Remove obsolete adapters
try SystemLanguageModel.Adapter.removeObsoleteAdapters()
```

## Context Management

When conversations grow long:

1. Monitor token usage against `SystemLanguageModel.default.contextSize`
2. Use `SystemLanguageModel.default.tokenCount(for:)` to estimate usage
3. Summarize earlier turns into new session instructions
4. Create fresh sessions with summary context rather than overflowing

```swift
if transcript.estimatedTokenCount > 3000 {
    let summary = try await summarizeSession(session)
    session = LanguageModelSession {
        "Previous conversation summary: \(summary)"
        "Continue helping the user."
    }
}
```

## Serialized Model Access

When multiple parts of an app need the model:

```swift
actor FoundationModelCoordinator {
    private var session: LanguageModelSession?

    func respond(to prompt: String) async throws -> String {
        if session == nil {
            session = LanguageModelSession()
        }
        guard let activeSession = session else {
            throw FoundationModelError.sessionUnavailable
        }
        let response = try await activeSession.respond(to: prompt)
        return response.content
    }
}
```

Serialize all Foundation Model access through a single coordinator to prevent
Neural Engine contention.

## Prompt Design Best Practices

1. **Be concise.** The context window covers both input and output tokens.
   Check `SystemLanguageModel.default.contextSize` for the current limit.
2. **Use bracketed placeholders** in instructions: `[descriptive example]`.
3. **Use "DO NOT" in all caps** for behavioral prohibitions.
4. **Provide up to 5 few-shot examples** for consistent output.
5. **Use length qualifiers:** "in a few words", "in three sentences".
6. **Estimate token usage** with `SystemLanguageModel.default.tokenCount(for:)`
   to avoid exceeding the context window.

## Feedback

Log feedback for model improvement:

```swift
let data = session.logFeedbackAttachment(
    sentiment: .negative,
    issues: [
        LanguageModelFeedback.Issue(
            category: .didNotFollowInstructions,
            explanation: "Ignored the word count constraint"
        )
    ],
    desiredOutput: nil
)
```

Issue categories: `.didNotFollowInstructions`, `.incorrect`,
`.stereotypeOrBias`, `.suggestiveOrSexual`, `.tooVerbose`,
`.triggeredGuardrailUnexpectedly`, `.unhelpful`, `.vulgarOrOffensive`.
