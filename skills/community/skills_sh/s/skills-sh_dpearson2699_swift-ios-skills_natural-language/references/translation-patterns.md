# NaturalLanguage + Translation Extended Patterns

Overflow reference for the `natural-language` skill. Contains advanced patterns
that exceed the main skill file's scope.

## Contents

- [Custom NLModel Integration](#custom-nlmodel-integration)
- [Contextual Embeddings](#contextual-embeddings)
- [Gazetteers for Domain Vocabulary](#gazetteers-for-domain-vocabulary)
- [NLTagger with Multiple Schemes](#nltagger-with-multiple-schemes)
- [Translation with Replacement Action](#translation-with-replacement-action)
- [Translation Session Strategies](#translation-session-strategies)
- [SwiftUI Integration Patterns](#swiftui-integration-patterns)
- [Lemmatization](#lemmatization)

## Custom NLModel Integration

Load a Create ML text classifier or word tagger into `NLTagger` via `NLModel`.

```swift
import NaturalLanguage
import CoreML

func setupCustomTagger() throws -> NLTagger {
    let mlModel = try MLModel(contentsOf: modelURL)
    let nlModel = try NLModel(mlModel: mlModel)

    let tagger = NLTagger(tagSchemes: [.nameType])
    tagger.setModels([nlModel], forTagScheme: .nameType)
    return tagger
}

// Direct prediction without a tagger
func classifyText(_ text: String) throws -> String? {
    let mlModel = try MLModel(contentsOf: modelURL)
    let nlModel = try NLModel(mlModel: mlModel)
    return nlModel.predictedLabel(for: text)
}

// Predictions with confidence scores
func classifyWithConfidence(_ text: String) throws -> [String: Double] {
    let mlModel = try MLModel(contentsOf: modelURL)
    let nlModel = try NLModel(mlModel: mlModel)
    return nlModel.predictedLabelHypotheses(for: text, maximumCount: 5)
}
```

## Contextual Embeddings

`NLContextualEmbedding` produces context-aware vectors where the same word
gets different vectors based on surrounding text.

```swift
import NaturalLanguage

func contextualVectors(for text: String) throws -> [([Double], Range<String.Index>)] {
    guard let embedding = NLContextualEmbedding(language: .english) else {
        return []
    }

    // Check and load assets
    guard embedding.hasAvailableAssets else {
        embedding.requestAssets { result, error in
            // Handle download
        }
        return []
    }

    try embedding.load()
    defer { embedding.unload() }

    let result = try embedding.embeddingResult(for: text, language: .english)
    var vectors: [([Double], Range<String.Index>)] = []

    result.enumerateTokenVectors(in: text.startIndex..<text.endIndex) { vector, range in
        vectors.append((vector, range))
        return true
    }
    return vectors
}
```

### Finding Available Contextual Embeddings

```swift
let embeddings = NLContextualEmbedding.contextualEmbeddings(forValues: [
    .languages: [NLLanguage.english.rawValue]
])

for embedding in embeddings {
    print("Model: \(embedding.modelIdentifier)")
    print("Dimension: \(embedding.dimension)")
    print("Max length: \(embedding.maximumSequenceLength)")
}
```

## Gazetteers for Domain Vocabulary

Override or supplement tagger results with custom term-to-label mappings.

```swift
func setupGazetteer() throws -> NLTagger {
    let dictionary: [String: [String]] = [
        "PRODUCT": ["iPhone", "MacBook Pro", "Apple Watch"],
        "FEATURE": ["Dynamic Island", "ProMotion", "MagSafe"]
    ]

    let gazetteer = try NLGazetteer(dictionary: dictionary, language: .english)
    let tagger = NLTagger(tagSchemes: [.nameType])
    tagger.setGazetteers([gazetteer], for: .nameType)
    return tagger
}

// Persist a gazetteer to disk
func saveGazetteer(_ dictionary: [String: [String]], to url: URL) throws {
    try NLGazetteer.write(dictionary, language: .english, to: url)
}
```

## NLTagger with Multiple Schemes

Request multiple tag schemes in a single tagger for efficient processing.

```swift
func analyzeText(_ text: String) {
    let tagger = NLTagger(tagSchemes: [.lexicalClass, .nameType, .lemma])
    tagger.string = text

    let range = text.startIndex..<text.endIndex
    let options: NLTagger.Options = [.omitWhitespace, .omitPunctuation, .joinNames]

    tagger.enumerateTags(in: range, unit: .word, scheme: .nameTypeOrLexicalClass,
                         options: options) { tag, tokenRange in
        let word = String(text[tokenRange])
        let (lemmaTag, _) = tagger.tag(at: tokenRange.lowerBound,
                                        unit: .word, scheme: .lemma)
        let lemma = lemmaTag?.rawValue ?? word
        print("\(word) -> tag: \(tag?.rawValue ?? "?"), lemma: \(lemma)")
        return true
    }
}
```

## Translation with Replacement Action

Replace the source text in-place after translation using the replacement action.

```swift
import SwiftUI
import Translation

struct EditableTranslationView: View {
    @State private var text = "Hello, how are you?"
    @State private var showTranslation = false

    var body: some View {
        TextEditor(text: $text)
            .toolbar {
                Button("Translate") { showTranslation = true }
            }
            .translationPresentation(
                isPresented: $showTranslation,
                text: text,
                replacementAction: { translated in
                    text = translated
                }
            )
    }
}
```

## Translation Session Strategies

Control whether translations prioritize quality or speed. Strategy selection
requires iOS 26.4+ / macOS 26.4+. Translation content is processed on device;
`.highFidelity` uses Apple Intelligence models when available, and
`.lowLatency` uses traditional models.

```swift
import Translation

// High fidelity: more fluent translations when Apple Intelligence is available
let highQualityConfig = TranslationSession.Configuration(
    source: Locale.Language(identifier: "en"),
    target: Locale.Language(identifier: "ja"),
    preferredStrategy: .highFidelity
)

// Low latency: faster traditional translation models
let fastConfig = TranslationSession.Configuration(
    source: Locale.Language(identifier: "en"),
    target: Locale.Language(identifier: "ja"),
    preferredStrategy: .lowLatency
)
```

### Preparing a Translation Session

Pre-download models before translating to avoid UI delays.

```swift
.translationTask(configuration) { session in
    do {
        try await session.prepareTranslation()
        // Models are now ready, translate without delay
        let response = try await session.translate(sourceText)
        await MainActor.run {
            translatedText = response.targetText
        }
    } catch {
        // Handle download refusal, cancellation, or unsupported language pairs.
    }
}
```

For non-UI translation, initialize `TranslationSession(installedSource:target:)`
only after the source and target languages are installed; this initializer
throws when the required languages are unavailable.

## SwiftUI Integration Patterns

### Language Analysis View

```swift
import SwiftUI
import NaturalLanguage

@Observable
@MainActor
final class TextAnalyzer {
    var tokens: [String] = []
    var detectedLanguage: String = ""
    var sentimentLabel: String = ""

    func analyze(_ text: String) {
        guard !text.isEmpty else { return }

        // Tokenize
        let tokenizer = NLTokenizer(unit: .word)
        tokenizer.string = text
        tokens = tokenizer.tokens(for: text.startIndex..<text.endIndex)
            .map { String(text[$0]) }

        // Language
        detectedLanguage = NLLanguageRecognizer.dominantLanguage(for: text)?
            .rawValue ?? "Unknown"

        // Sentiment
        let tagger = NLTagger(tagSchemes: [.sentimentScore])
        tagger.string = text
        let (tag, _) = tagger.tag(at: text.startIndex, unit: .paragraph,
                                   scheme: .sentimentScore)
        if let score = tag.flatMap({ Double($0.rawValue) }) {
            sentimentLabel = score > 0.1 ? "Positive" :
                             score < -0.1 ? "Negative" : "Neutral"
        }
    }
}

struct TextAnalysisView: View {
    @State private var text = ""
    @State private var analyzer = TextAnalyzer()

    var body: some View {
        Form {
            TextField("Enter text", text: $text)
                .onChange(of: text) { _, newValue in
                    analyzer.analyze(newValue)
                }
            Section("Results") {
                LabeledContent("Language", value: analyzer.detectedLanguage)
                LabeledContent("Sentiment", value: analyzer.sentimentLabel)
                LabeledContent("Words", value: "\(analyzer.tokens.count)")
            }
        }
    }
}
```

### Requesting NLTagger Assets

Some tag schemes require downloadable assets. Request them before tagging.

```swift
NLTagger.requestAssets(for: .japanese, tagScheme: .nameType) { result, error in
    switch result {
    case .available:
        // Assets loaded, safe to tag Japanese text
        break
    case .notAvailable:
        // Assets not available for this language/scheme
        break
    case .error:
        print("Asset request error: \(error?.localizedDescription ?? "")")
    @unknown default:
        break
    }
}
```

## Lemmatization

Get the base form of words for indexing or search normalization.

```swift
func lemmatize(_ text: String) -> [String] {
    let tagger = NLTagger(tagSchemes: [.lemma])
    tagger.string = text

    var lemmas: [String] = []
    tagger.enumerateTags(
        in: text.startIndex..<text.endIndex,
        unit: .word,
        scheme: .lemma,
        options: [.omitPunctuation, .omitWhitespace]
    ) { tag, range in
        lemmas.append(tag?.rawValue ?? String(text[range]))
        return true
    }
    return lemmas
}
// "The cats were running quickly" -> ["the", "cat", "be", "run", "quickly"]
```
