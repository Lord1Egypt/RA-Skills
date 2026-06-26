# TipKit Patterns Reference

Complete implementation patterns for TipKit including custom styles, event-based
rules, tip groups, testing strategies, onboarding flows, and SwiftUI previews.
Examples target iOS 17+ with Swift 6.3 conventions unless a section explicitly
calls out a newer availability requirement.

## Contents

- [Complete Tip with Rules and Events](#complete-tip-with-rules-and-events)
- [TipView and popoverTip Placement](#tipview-and-popovertip-placement)
- [Event-Based Rule with Donation Counting](#event-based-rule-with-donation-counting)
- [Custom TipViewStyle](#custom-tipviewstyle)
- [TipGroup Sequencing (iOS 18+)](#tipgroup-sequencing-ios-18)
- [Testing Strategies](#testing-strategies)
- [Tip with Action Buttons](#tip-with-action-buttons)
- [Integration with Onboarding Flow](#integration-with-onboarding-flow)
- [Reusable Tip Identifiers](#reusable-tip-identifiers)
- [CloudKit Sync (iOS 18+)](#cloudkit-sync-ios-18)
- [Full App Integration Example](#full-app-integration-example)

## Availability Notes

- TipKit core APIs are iOS 17+.
- `TipGroup`, `.cloudKitContainer(...)`, and `MaxDisplayDuration` are iOS 18+.
- `resetEligibility()` is iOS 26+.
- `Tips.resetDatastore()` must run before `Tips.configure(_:)`.

## Complete Tip with Rules and Events

A full-featured tip combining parameter-based and event-based rules. The tip
appears only after the user has logged in and opened the app at least three
times, ensuring they are familiar with the basics before seeing advanced
feature discovery.

```swift
import TipKit

struct AdvancedSearchTip: Tip {
    // Parameter rule: user must be logged in
    @Parameter
    static var isLoggedIn: Bool = false

    // Event rule: user must have performed searches
    static let searchPerformed = Tips.Event(id: "searchPerformed")

    var title: Text {
        Text("Try Advanced Search")
    }

    var message: Text? {
        Text("Filter results by date, category, and location for faster discovery.")
    }

    var image: Image? {
        Image(systemName: "magnifyingglass")
    }

    // All rules must pass before the tip becomes eligible
    var rules: [Rule] {
        #Rule(Self.$isLoggedIn) { $0 == true }
        #Rule(Self.searchPerformed) { $0.donations.count >= 3 }
    }

    var options: [any TipOption] {
        MaxDisplayCount(5)
    }
}
```

### Donating to Events

Place event donations at the point where the user action occurs. Each
donation increments the internal counter that rules evaluate against.

```swift
struct SearchView: View {
    @State private var query = ""

    var body: some View {
        SearchBar(text: $query, onSubmit: {
            performSearch(query)
            // Donate each time the user searches
            AdvancedSearchTip.searchPerformed.sendDonation()
        })
    }
}
```

### Setting Parameters

Set parameter values when the relevant app state changes. Parameters persist
across launches via the TipKit datastore.

```swift
func handleLoginSuccess() {
    AdvancedSearchTip.isLoggedIn = true
}
```

## TipView and popoverTip Placement

### Inline TipView in a List

Place a `TipView` as a list row for contextual inline discovery. The tip
appears as part of the list content and animates away when dismissed or
invalidated.

```swift
struct ItemListView: View {
    let filterTip = FilterTip()
    @State private var items: [Item] = []

    var body: some View {
        List {
            TipView(filterTip)

            ForEach(items) { item in
                ItemRow(item: item)
            }
        }
        .navigationTitle("Items")
        .toolbar {
            ToolbarItem(placement: .primaryAction) {
                Button {
                    showFilters()
                    filterTip.invalidate(reason: .actionPerformed)
                } label: {
                    Image(systemName: "line.3.horizontal.decrease.circle")
                }
                .popoverTip(filterTip, arrowEdge: .top)
            }
        }
    }
}
```

### Popover on Navigation Bar Button

Attach a popover tip to a toolbar button. The popover arrow points to the
button, drawing the user's attention to the exact control.

```swift
struct EditorView: View {
    let undoTip = UndoShortcutTip()

    var body: some View {
        TextEditor(text: $text)
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    Button("Undo", systemImage: "arrow.uturn.backward") {
                        undoLastAction()
                        undoTip.invalidate(reason: .actionPerformed)
                    }
                    .popoverTip(undoTip, arrowEdge: .top)
                }
            }
    }
}
```

### Popover on Tab Bar Item

Use `popoverTip` on a `Tab` label view inside a `TabView` to highlight a
new tab.

```swift
struct MainTabView: View {
    let newTabTip = NewFeatureTabTip()

    var body: some View {
        TabView {
            Tab("Home", systemImage: "house") {
                HomeView()
            }

            Tab("Discover", systemImage: "sparkles") {
                DiscoverView()
            }
            .popoverTip(newTabTip)
        }
    }
}
```

## Event-Based Rule with Donation Counting

Track how many times the user performs an action, then show a tip suggesting
a more efficient alternative. This pattern is effective for progressive
disclosure: let users learn the basic workflow first, then reveal shortcuts.

```swift
struct KeyboardShortcutTip: Tip {
    static let manualSaveEvent = Tips.Event(id: "manualSave")

    var title: Text {
        Text("Save Faster with Command-S")
    }

    var message: Text? {
        Text("Press Command-S instead of using the menu to save your work instantly.")
    }

    var image: Image? {
        Image(systemName: "keyboard")
    }

    var rules: [Rule] {
        // Show after user has manually saved 5 times via button
        #Rule(Self.manualSaveEvent) { $0.donations.count >= 5 }
    }
}

struct DocumentView: View {
    let shortcutTip = KeyboardShortcutTip()

    var body: some View {
        VStack {
            TipView(shortcutTip)
            DocumentEditor(document: $document)
        }
        .toolbar {
            ToolbarItem {
                Button("Save") {
                    saveDocument()
                    KeyboardShortcutTip.manualSaveEvent.sendDonation()
                }
            }
        }
    }
}
```

### Event Donations with Associated Values

Attach a `DonationValue` to event donations for richer rule evaluation.
Use `Codable`-conforming types to provide context about each donation.

```swift
struct DetailedTip: Tip {
    struct DonationInfo: Codable, Sendable {
        let category: String
        let timestamp: Date
    }

    static let itemViewed = Tips.Event<DonationInfo>(id: "itemViewed")

    var rules: [Rule] {
        #Rule(Self.itemViewed) {
            $0.donations.filter {
                $0.category == "premium"
            }.count >= 3
        }
    }

    var title: Text { Text("Unlock Premium Content") }
}

// Donate with associated value
DetailedTip.itemViewed.sendDonation(
    DetailedTip.DonationInfo(category: "premium", timestamp: .now)
)
```

## Custom TipViewStyle

Create a branded tip appearance that matches the app's design language.
The `Configuration` provides access to the tip's title, message, image,
and actions.

```swift
struct BrandedTipStyle: TipViewStyle {
    func makeBody(configuration: Configuration) -> some View {
        HStack(alignment: .top) {
            configuration.image?
                .font(.system(size: 24))
                .foregroundStyle(.white)
                .frame(width: 44, height: 44)
                .background(.blue.gradient, in: RoundedRectangle(cornerRadius: 10))

            VStack(alignment: .leading) {
                configuration.title?
                    .font(.headline)

                configuration.message?
                    .font(.subheadline)
                    .foregroundStyle(.secondary)

                if !configuration.actions.isEmpty {
                    HStack {
                        ForEach(configuration.actions) { action in
                            Button(action: action.handler) {
                                action.label()
                                    .font(.subheadline.bold())
                            }
                            .buttonStyle(.bordered)
                        }
                    }
                    .padding(.top)
                }
            }
        }
        .padding()
        .background(.regularMaterial, in: RoundedRectangle(cornerRadius: 16))
    }
}
```

### Applying the Custom Style

Apply the style to individual `TipView` instances or set it as the
environment default.

```swift
// Per view
TipView(myTip)
    .tipViewStyle(BrandedTipStyle())

// Environment-wide (apply to a parent container)
NavigationStack {
    ContentView()
}
.tipViewStyle(BrandedTipStyle())
```

### Minimal Compact Style

A stripped-down style for tips in tight layouts like toolbars or sidebars.

```swift
struct CompactTipStyle: TipViewStyle {
    func makeBody(configuration: Configuration) -> some View {
        HStack {
            configuration.image?
                .foregroundStyle(.tint)

            configuration.title?
                .font(.caption.bold())
        }
        .padding(.horizontal)
        .padding(.vertical)
        .background(.tint.opacity(0.1), in: Capsule())
    }
}
```

## TipGroup Sequencing (iOS 18+)

Use `TipGroup` to present related tips. `TipGroup` defaults to
`.firstAvailable`, which shows the first eligible tip in the group without
requiring a strict sequence. Pass `.ordered` only when each later tip must wait
until all previous tips have been invalidated.

For ordered coach-mark flows, only the current tip displays. When the user
dismisses or acts on it, invalidate that tip so the next tip in the group can
become current.

```swift
struct OnboardingTipA: Tip {
    var title: Text { Text("Welcome to the App") }
    var message: Text? { Text("Let's take a quick tour of the main features.") }
    var image: Image? { Image(systemName: "hand.wave") }
}

struct OnboardingTipB: Tip {
    var title: Text { Text("Browse Your Feed") }
    var message: Text? { Text("Swipe through curated content tailored for you.") }
    var image: Image? { Image(systemName: "rectangle.stack") }
}

struct OnboardingTipC: Tip {
    var title: Text { Text("Customize Your Profile") }
    var message: Text? { Text("Tap your avatar to set your name and preferences.") }
    var image: Image? { Image(systemName: "person.crop.circle") }
}

struct HomeView: View {
    @State private var tipGroup = TipGroup(.ordered) {
        OnboardingTipA()
        OnboardingTipB()
        OnboardingTipC()
    }

    var body: some View {
        VStack {
            if let currentTip = tipGroup.currentTip {
                TipView(currentTip) { action in
                    currentTip.invalidate(reason: .actionPerformed)
                }
            }

            FeedView()
        }
        .padding()
    }
}
```

### Tip Group with Popover

Attach the group's current tip as a popover that moves between controls
as tips advance.

```swift
struct ToolbarGroupView: View {
    @State private var group = TipGroup(.ordered) {
        SearchTip()
        FilterTip()
        SortTip()
    }

    var body: some View {
        HStack {
            Button("Search", systemImage: "magnifyingglass") { search() }
                .popoverTip(group.currentTip as? SearchTip)

            Button("Filter", systemImage: "line.3.horizontal.decrease") { filter() }
                .popoverTip(group.currentTip as? FilterTip)

            Button("Sort", systemImage: "arrow.up.arrow.down") { sort() }
                .popoverTip(group.currentTip as? SortTip)
        }
    }
}
```

## Testing Strategies

### Previewing Tips in SwiftUI Previews

Configure TipKit in the preview body so tips display in Xcode previews.
Use `showAllTipsForTesting()` to bypass rules. Reset the datastore before
configuration; `Tips.resetDatastore()` must not run after `Tips.configure()`.

```swift
#Preview {
    ContentView()
        .task {
            try? Tips.resetDatastore()
            Tips.showAllTipsForTesting()
            try? Tips.configure([.displayFrequency(.immediate)])
        }
}
```

### Previewing a Specific Tip

Show only one tip in a focused preview.

```swift
#Preview("Favorite Tip") {
    VStack {
        TipView(FavoriteTip())
        Spacer()
    }
    .padding()
    .task {
        try? Tips.resetDatastore()
        Tips.showTipsForTesting([FavoriteTip.self])
        try? Tips.configure([.displayFrequency(.immediate)])
    }
}
```

### Unit Testing Tip Rules

Verify that parameter and event rules correctly control tip eligibility.
Reset the datastore before each test to ensure a clean state.
TipKit configuration is process-level, so prefer isolated UI-test launches for
full lifecycle coverage. If using unit tests, reset before configuring.

```swift
import XCTest
import TipKit

final class TipRuleTests: XCTestCase {
    override func setUp() async throws {
        try Tips.resetDatastore()
        try Tips.configure([.displayFrequency(.immediate)])
    }

    func testAdvancedSearchTipRequiresLogin() async {
        let tip = AdvancedSearchTip()

        // Tip should not be eligible before login
        AdvancedSearchTip.isLoggedIn = false
        // Verify tip status

        // Tip should become eligible after login + enough events
        AdvancedSearchTip.isLoggedIn = true
        for _ in 0..<3 {
            AdvancedSearchTip.searchPerformed.sendDonation()
        }
        // Verify tip status
    }

    func testTipInvalidation() async {
        let tip = FavoriteTip()
        tip.invalidate(reason: .actionPerformed)
        // Tip should no longer be eligible after invalidation
    }
}
```

### UI Testing with Forced Tips

Pass launch arguments to control tip visibility in UI tests. This ensures
tests that verify tip UI always see the tip, regardless of rules.

```swift
// In UI test setUp
let app = XCUIApplication()
app.launchArguments += [
    "-com.apple.TipKit.ResetDatastore", "1",
    "-com.apple.TipKit.ShowAllTips", "1"
]
app.launch()
```

```swift
// Optional custom wrappers in App.init
init() {
    if ProcessInfo.processInfo.arguments.contains("--show-all-tips") {
        Tips.showAllTipsForTesting()
    }
    if ProcessInfo.processInfo.arguments.contains("--hide-all-tips") {
        Tips.hideAllTipsForTesting()
    }
    try? Tips.configure()
}
```

### UI Testing Without Tips

Suppress all tips in UI tests that are not about tip behavior, so tips
do not interfere with other test flows.

```swift
// In UI test setUp for non-tip tests
let app = XCUIApplication()
app.launchArguments += ["-com.apple.TipKit.HideAllTips", "1"]
app.launch()
```

## Tip with Action Buttons

Add action buttons that deep-link to a feature. Invalidate the tip when
the user taps the primary action.

```swift
struct NewEditorTip: Tip {
    var title: Text {
        Text("Try the New Editor")
    }

    var message: Text? {
        Text("A faster, more powerful editing experience awaits.")
    }

    var image: Image? {
        Image(systemName: "pencil.and.outline")
    }

    var actions: [Action] {
        Action(id: "open-editor", title: "Open Editor")
        Action(id: "later", title: "Maybe Later")
    }
}

struct HomeView: View {
    let editorTip = NewEditorTip()
    @State private var showEditor = false

    var body: some View {
        VStack {
            TipView(editorTip) { action in
                switch action.id {
                case "open-editor":
                    showEditor = true
                    editorTip.invalidate(reason: .actionPerformed)
                case "later":
                    editorTip.invalidate(reason: .tipClosed)
                default:
                    break
                }
            }

            MainContentView()
        }
        .sheet(isPresented: $showEditor) {
            EditorView()
        }
    }
}
```

## Integration with Onboarding Flow

Coordinate TipKit with a first-run onboarding flow. Invalidate welcome
tips after the user completes onboarding so they do not see redundant
information.

```swift
struct WelcomeTip: Tip {
    @Parameter
    static var hasCompletedOnboarding: Bool = false

    var title: Text { Text("Welcome to MyApp") }
    var message: Text? { Text("Swipe through to learn the basics.") }

    var rules: [Rule] {
        // Only show if onboarding was NOT completed (user skipped it)
        #Rule(Self.$hasCompletedOnboarding) { $0 == false }
    }
}

struct FeatureDiscoveryTip: Tip {
    @Parameter
    static var hasCompletedOnboarding: Bool = false

    var title: Text { Text("Discover Collections") }
    var message: Text? { Text("Organize your items into collections for easy access.") }

    var rules: [Rule] {
        // Only show after onboarding completes
        #Rule(Self.$hasCompletedOnboarding) { $0 == true }
    }
}

struct OnboardingView: View {
    @Binding var isPresented: Bool

    var body: some View {
        VStack {
            // Onboarding pages...

            Button("Get Started") {
                completeOnboarding()
            }
        }
    }

    func completeOnboarding() {
        // Invalidate welcome tips since onboarding covered the basics
        WelcomeTip.hasCompletedOnboarding = true
        FeatureDiscoveryTip.hasCompletedOnboarding = true

        // Explicitly invalidate any welcome-specific tips
        let welcomeTip = WelcomeTip()
        welcomeTip.invalidate(reason: .actionPerformed)

        isPresented = false
    }
}

struct ContentView: View {
    @AppStorage("hasCompletedOnboarding") private var hasCompletedOnboarding = false
    @State private var showOnboarding = false

    let welcomeTip = WelcomeTip()
    let discoveryTip = FeatureDiscoveryTip()

    var body: some View {
        NavigationStack {
            VStack {
                TipView(welcomeTip)

                CollectionGrid()
                    .popoverTip(discoveryTip)
            }
        }
        .sheet(isPresented: $showOnboarding) {
            OnboardingView(isPresented: $showOnboarding)
        }
        .onAppear {
            if !hasCompletedOnboarding {
                showOnboarding = true
            }
        }
    }
}
```

## Reusable Tip Identifiers

Override `id` when one reusable `Tip` type should create separate persisted
records for different content. The ID controls status, display count, rules,
and invalidation state.

```swift
struct NewCollectionTip: Tip {
    let collection: CollectionSummary

    var id: String {
        "NewCollectionTip-\(collection.id)"
    }

    var title: Text {
        Text("Explore \(collection.name)")
    }

    var message: Text? {
        Text("A new collection is ready for browsing.")
    }
}

struct CollectionListView: View {
    let latestCollection: CollectionSummary

    var body: some View {
        TipView(NewCollectionTip(collection: latestCollection))
        CollectionGrid()
    }
}
```

Use stable model identifiers. Do not use localized copy, array indexes, dates
that change every launch, or random values.

## CloudKit Sync (iOS 18+)

CloudKit sync shares TipKit status, rules, parameters, events, display counts,
and display duration across devices signed into the same iCloud account.

Project setup:

- Enable iCloud and CloudKit in Signing & Capabilities.
- Enable Background Modes > Remote notifications.
- Prefer a dedicated CloudKit container with a `.tips` suffix.

```swift
@main
struct SyncedTipsApp: App {
    init() {
        do {
            try Tips.configure([
                .cloudKitContainer(.named("iCloud.com.example.MyApp.tips")),
                .displayFrequency(.daily)
            ])
        } catch {
            assertionFailure("TipKit configuration failed: \(error)")
        }
    }

    var body: some Scene {
        WindowGroup { ContentView() }
    }
}
```

Use `.cloudKitContainer(.automatic)` only when the entitlement list is
deliberately arranged so TipKit can choose the intended container. When sharing
tip state across app-group members or devices, keep option settings consistent
for the same tip IDs.

## Full App Integration Example

A complete example showing TipKit configuration, multiple tips with rules,
event donations, and proper invalidation.

```swift
import SwiftUI
import TipKit

// MARK: - Tips

struct SearchTip: Tip {
    var title: Text { Text("Search Your Library") }
    var message: Text? { Text("Tap to find any item by name, tag, or date.") }
    var image: Image? { Image(systemName: "magnifyingglass") }
}

struct CollectionTip: Tip {
    static let itemAddedEvent = Tips.Event(id: "itemAdded")

    var title: Text { Text("Create a Collection") }
    var message: Text? { Text("Group related items together for quick access.") }
    var image: Image? { Image(systemName: "folder.badge.plus") }

    var rules: [Rule] {
        #Rule(Self.itemAddedEvent) { $0.donations.count >= 3 }
    }
}

struct ShareTip: Tip {
    @Parameter
    static var hasCreatedCollection: Bool = false

    var title: Text { Text("Share Your Collection") }
    var message: Text? { Text("Invite others to view or collaborate on your collection.") }
    var image: Image? { Image(systemName: "square.and.arrow.up") }

    var rules: [Rule] {
        #Rule(Self.$hasCreatedCollection) { $0 == true }
    }
}

// MARK: - App

@main
struct LibraryApp: App {
    init() {
        do {
            #if DEBUG
            if ProcessInfo.processInfo.arguments.contains("--reset-tips") {
                try Tips.resetDatastore()
            }
            if ProcessInfo.processInfo.arguments.contains("--show-all-tips") {
                Tips.showAllTipsForTesting()
            }
            if ProcessInfo.processInfo.arguments.contains("--hide-all-tips") {
                Tips.hideAllTipsForTesting()
            }
            #endif

            try Tips.configure([
                .displayFrequency(.daily),
                .datastoreLocation(.applicationDefault)
            ])
        } catch {
            assertionFailure("TipKit configuration failed: \(error)")
        }
    }

    var body: some Scene {
        WindowGroup { LibraryView() }
    }
}

// MARK: - Main View

struct LibraryView: View {
    let searchTip = SearchTip()
    let collectionTip = CollectionTip()
    let shareTip = ShareTip()

    @State private var items: [LibraryItem] = []

    var body: some View {
        NavigationStack {
            List {
                TipView(collectionTip)

                ForEach(items) { item in
                    Text(item.name)
                }
            }
            .navigationTitle("Library")
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    Button("Search", systemImage: "magnifyingglass") {
                        showSearch()
                        searchTip.invalidate(reason: .actionPerformed)
                    }
                    .popoverTip(searchTip)
                }

                ToolbarItem(placement: .secondaryAction) {
                    Button("Share", systemImage: "square.and.arrow.up") {
                        shareCollection()
                        shareTip.invalidate(reason: .actionPerformed)
                    }
                    .popoverTip(shareTip)
                }

                ToolbarItem(placement: .secondaryAction) {
                    Button("Add Item", systemImage: "plus") {
                        addItem()
                        CollectionTip.itemAddedEvent.sendDonation()
                    }
                }
            }
        }
    }

    func addItem() { /* ... */ }
    func showSearch() { /* ... */ }
    func shareCollection() { /* ... */ }
}
```
