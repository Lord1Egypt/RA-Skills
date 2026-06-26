---
name: ios-marketing-capture-automation
description: Automate multi-locale marketing screenshot capture for SwiftUI iOS apps with in-app capture system, demo data seeding, and element rendering.
triggers:
  - capture marketing screenshots for my iOS app
  - generate locale screenshots across all languages
  - render my widgets as isolated PNGs
  - automate App Store screenshot capture
  - create marketing assets for SwiftUI app
  - screenshot my app in all locales
  - render iOS app components as images
  - automate iOS app store screenshots
---

# iOS Marketing Capture Automation

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

## What This Skill Does

This skill helps you automate marketing screenshot capture for SwiftUI iOS apps by building an in-app capture system that:

- Adds a `#if DEBUG`-gated capture system with zero production footprint
- Seeds deterministic demo data so screenshots look populated and polished
- Navigates to each screen programmatically via step-based coordinator
- Snapshots full window including status bar, safe area, and presented sheets
- Renders isolated elements (cards, widgets, charts) via `ImageRenderer` at 3x with transparency
- Loops every locale automatically — one build, N relaunches with `-AppleLanguages`
- Works with any SwiftUI navigation: `TabView`, `NavigationStack`, `NavigationSplitView`

## Installation

### Using npx skills (recommended)

```bash
npx skills add ParthJadhav/ios-marketing-capture
```

Global install (available across all projects):

```bash
npx skills add ParthJadhav/ios-marketing-capture -g
```

Agent-specific install:

```bash
npx skills add ParthJadhav/ios-marketing-capture -a claude-code
```

### Manual installation

```bash
git clone https://github.com/ParthJadhav/ios-marketing-capture ~/.claude/skills/ios-marketing-capture
```

## Requirements Checklist

Before starting, verify:

- ✅ Xcode 16+ (synchronized folder groups support)
- ✅ iOS 17+ deployment target (for `ImageRenderer`, `@Observable`)
- ✅ A simulator runtime matching target iOS version
- ✅ Python 3 (for JSON parsing in shell script)
- ✅ SwiftUI-based app with defined navigation structure

## Core Concepts

### In-App Capture (Not XCUITest)

This approach uses in-app capture instead of XCUITest/Fastlane because:

- **No test target needed** — many projects lack one, adding means fragile pbxproj edits
- **Direct access** — ViewModels, SwiftData, `ImageRenderer`, `UIWindow.drawHierarchy`
- **Faster** — `xcodebuild build` once, then `simctl launch` per locale
- **Element renders require it** — `ImageRenderer` must run inside app process

### Step-Based Coordinator

Each screenshot is a self-contained `CaptureStep`:

```swift
struct CaptureStep {
    let name: String                         // "01-home"
    let navigate: @MainActor () -> Void      // put app in right state
    let settle: Duration                     // wait for animations
    let cleanup: (@MainActor () -> Void)?    // tear down before next step
}
```

## Implementation Pattern

### 1. Gather Requirements

When user asks to capture screenshots, collect:

1. **Screens to capture** — exact tab names or navigation paths
2. **Elements to render** — cards, widgets, charts to isolate
3. **Locales** — explicit list or "all locales in xcstrings"
4. **Device** — simulator model (e.g. "iPhone 17")
5. **Appearance** — light, dark, or both
6. **Seed data requirements** — what demo data needs to populate

### 2. Generated File Structure

Create this structure:

```
YourApp/
├── Debug/
│   └── MarketingCapture.swift      # Capture system (DEBUG-only)
├── ContentView.swift               # Modified — DEBUG hook
scripts/
└── capture-marketing.sh            # Build + locale loop
```

Output lands in:

```
marketing/
    en/
        01-home.png
        02-detail.png
        elements/
            card-item.png
            widget-small.png
    de/
        01-home.png
        ...
```

### 3. Core Capture System Code

```swift
#if DEBUG
import SwiftUI

struct CaptureStep {
    let name: String
    let navigate: @MainActor () -> Void
    let settle: Duration
    let cleanup: (@MainActor () -> Void)?
}

@Observable
final class MarketingCaptureCoordinator {
    var isCapturing = false
    var currentStep = 0
    
    private let steps: [CaptureStep]
    private let outputDir: URL
    private let elementsDir: URL
    
    init(steps: [CaptureStep], locale: String) {
        self.steps = steps
        
        let base = FileManager.default
            .urls(for: .documentDirectory, in: .userDomainMask)[0]
            .deletingLastPathComponent()
            .deletingLastPathComponent()
            .appendingPathComponent("marketing/\(locale)")
        
        self.outputDir = base
        self.elementsDir = base.appendingPathComponent("elements")
        
        try? FileManager.default.createDirectory(
            at: outputDir,
            withIntermediateDirectories: true
        )
        try? FileManager.default.createDirectory(
            at: elementsDir,
            withIntermediateDirectories: true
        )
    }
    
    @MainActor
    func startCapture() async {
        isCapturing = true
        currentStep = 0
        
        for step in steps {
            step.navigate()
            try? await Task.sleep(for: step.settle)
            captureWindow(name: step.name)
            step.cleanup?()
            currentStep += 1
        }
        
        isCapturing = false
        print("✅ Capture complete: \(outputDir.path)")
        exit(0)
    }
    
    private func captureWindow(name: String) {
        guard let window = UIApplication.shared
            .connectedScenes
            .compactMap({ $0 as? UIWindowScene })
            .first?.windows.first else { return }
        
        let renderer = UIGraphicsImageRenderer(bounds: window.bounds)
        let image = renderer.image { ctx in
            window.drawHierarchy(in: window.bounds, afterScreenUpdates: true)
        }
        
        let url = outputDir.appendingPathComponent("\(name).png")
        try? image.pngData()?.write(to: url)
    }
}

struct MarketingElementHarness {
    @MainActor
    static func renderElement<Content: View>(
        name: String,
        width: CGFloat,
        cornerRadius: CGFloat,
        background: Color,
        @ViewBuilder content: () -> Content
    ) {
        let renderer = ImageRenderer(content: content()
            .frame(width: width)
            .background(background)
            .clipShape(RoundedRectangle(cornerRadius: cornerRadius))
        )
        renderer.scale = 3.0
        
        guard let uiImage = renderer.uiImage else { return }
        
        let base = FileManager.default
            .urls(for: .documentDirectory, in: .userDomainMask)[0]
            .deletingLastPathComponent()
            .deletingLastPathComponent()
        
        let locale = Locale.current.language.languageCode?.identifier ?? "en"
        let elementsDir = base
            .appendingPathComponent("marketing/\(locale)/elements")
        
        try? FileManager.default.createDirectory(
            at: elementsDir,
            withIntermediateDirectories: true
        )
        
        let url = elementsDir.appendingPathComponent("\(name).png")
        try? uiImage.pngData()?.write(to: url)
    }
}
#endif
```

### 4. Navigation Pattern Examples

#### TabView Navigation

```swift
@Observable
final class AppCoordinator {
    var selectedTab = 0
    
    func setTab(_ index: Int) {
        selectedTab = index
    }
}

// In MarketingCapture.swift:
func makeSteps(coordinator: AppCoordinator) -> [CaptureStep] {
    [
        CaptureStep(
            name: "01-home",
            navigate: { coordinator.setTab(0) },
            settle: .seconds(0.5),
            cleanup: nil
        ),
        CaptureStep(
            name: "02-shelf",
            navigate: { coordinator.setTab(1) },
            settle: .seconds(0.5),
            cleanup: nil
        )
    ]
}
```

#### NavigationStack with Router

```swift
@Observable
final class Router {
    var path: [Route] = []
    
    func push(_ route: Route) {
        path.append(route)
    }
    
    func popToRoot() {
        path.removeAll()
    }
}

// Steps:
CaptureStep(
    name: "03-detail",
    navigate: {
        router.popToRoot()
        router.push(.coffeeDetail(coffee))
    },
    settle: .seconds(0.8),
    cleanup: { router.popToRoot() }
)
```

#### NavigationSplitView

```swift
@Observable
final class SplitCoordinator {
    var sidebarSelection: SidebarItem?
    var detailSelection: DetailItem?
}

// Steps:
CaptureStep(
    name: "04-settings",
    navigate: {
        coordinator.sidebarSelection = .settings
        coordinator.detailSelection = nil
    },
    settle: .seconds(0.6),
    cleanup: nil
)
```

### 5. Demo Data Seeding

```swift
#if DEBUG
@MainActor
func seedMarketingData(modelContext: ModelContext) {
    // Clear existing
    try? modelContext.delete(model: Coffee.self)
    
    // Seed deterministic data
    let coffees = [
        Coffee(
            name: "Morning Blend",
            roaster: "Blue Bottle",
            origin: "Ethiopia",
            notes: ["Blueberry", "Chocolate", "Citrus"],
            roastDate: Date().addingTimeInterval(-7 * 86400)
        ),
        Coffee(
            name: "Dark Horse",
            roaster: "Stumptown",
            origin: "Colombia",
            notes: ["Caramel", "Nuts", "Brown Sugar"],
            roastDate: Date().addingTimeInterval(-3 * 86400)
        )
    ]
    
    coffees.forEach { modelContext.insert($0) }
    try? modelContext.save()
}
#endif
```

### 6. Integrating with ContentView

```swift
struct ContentView: View {
    @Environment(\.modelContext) private var modelContext
    @State private var coordinator = AppCoordinator()
    
    #if DEBUG
    @State private var captureCoordinator: MarketingCaptureCoordinator?
    #endif
    
    var body: some View {
        TabView(selection: $coordinator.selectedTab) {
            HomeView()
                .tag(0)
                .tabItem { Label("Home", systemImage: "house") }
            
            ShelfView()
                .tag(1)
                .tabItem { Label("Shelf", systemImage: "books.vertical") }
        }
        #if DEBUG
        .task {
            if ProcessInfo.processInfo.environment["MARKETING_CAPTURE"] == "1" {
                seedMarketingData(modelContext: modelContext)
                
                let locale = Locale.current.language.languageCode?.identifier ?? "en"
                captureCoordinator = MarketingCaptureCoordinator(
                    steps: makeMarketingSteps(coordinator: coordinator),
                    locale: locale
                )
                
                try? await Task.sleep(for: .seconds(1))
                await captureCoordinator?.startCapture()
            }
        }
        #endif
    }
}
```

### 7. Element Rendering Examples

#### Widget Rendering

```swift
#if DEBUG
@MainActor
func renderWidgets() {
    let entry = PulseWidgetEntry(
        date: Date(),
        coffee: seedCoffee,
        recentBrew: seedBrew
    )
    
    // Small widget
    MarketingElementHarness.renderElement(
        name: "widget-pulse-small",
        width: 158,
        cornerRadius: 16,
        background: .white
    ) {
        PulseWidgetSmallView(entry: entry)
            .padding(16) // WidgetKit padding manually added
    }
    
    // Medium widget
    MarketingElementHarness.renderElement(
        name: "widget-pulse-medium",
        width: 338,
        cornerRadius: 16,
        background: .white
    ) {
        PulseWidgetMediumView(entry: entry)
            .padding(16)
    }
}
#endif
```

#### Card Rendering

```swift
#if DEBUG
@MainActor
func renderCards(coffees: [Coffee]) {
    for (index, coffee) in coffees.enumerated() {
        MarketingElementHarness.renderElement(
            name: "card-\(index + 1)",
            width: 380,
            cornerRadius: 20,
            background: Color(.systemBackground)
        ) {
            CoffeeCard(coffee: coffee)
                .padding(.horizontal, 16)
                .padding(.vertical, 12)
        }
    }
}
#endif
```

#### Chart Rendering

```swift
#if DEBUG
@MainActor
func renderCharts() {
    MarketingElementHarness.renderElement(
        name: "chart-cupping",
        width: 380,
        cornerRadius: 16,
        background: Color(.systemBackground)
    ) {
        CuppingRadarChart(scores: sampleScores)
            .frame(height: 300)
            .padding(20)
    }
}
#endif
```

### 8. Build and Launch Script

```bash
#!/bin/bash
# scripts/capture-marketing.sh

set -e

APP_NAME="YourApp"
SCHEME="YourApp"
DEVICE="iPhone 17"
IOS_VERSION="18.2"

LOCALES=("en" "de" "es" "fr" "ja")

SIMULATOR_ID=$(xcrun simctl list devices available | \
    grep "$DEVICE ($IOS_VERSION)" | head -1 | \
    grep -o '\[.*\]' | tr -d '[]')

if [ -z "$SIMULATOR_ID" ]; then
    echo "❌ Simulator '$DEVICE ($IOS_VERSION)' not found"
    exit 1
fi

echo "📱 Using simulator: $SIMULATOR_ID"

# Boot simulator
xcrun simctl boot "$SIMULATOR_ID" 2>/dev/null || true
sleep 2

# Build once
echo "🔨 Building..."
xcodebuild \
    -scheme "$SCHEME" \
    -destination "id=$SIMULATOR_ID" \
    -configuration Debug \
    -derivedDataPath ./build \
    build

APP_PATH=$(find ./build -name "${APP_NAME}.app" | head -1)
BUNDLE_ID=$(defaults read "$APP_PATH/Info.plist" CFBundleIdentifier)

echo "📦 Bundle ID: $BUNDLE_ID"

# Install once
xcrun simctl install "$SIMULATOR_ID" "$APP_PATH"

# Per-locale capture
for LOCALE in "${LOCALES[@]}"; do
    echo ""
    echo "📸 Capturing $LOCALE..."
    
    xcrun simctl launch \
        --terminate-running-process \
        "$SIMULATOR_ID" \
        "$BUNDLE_ID" \
        -AppleLanguages "($LOCALE)" \
        -MARKETING_CAPTURE 1
    
    sleep 8
done

# Copy to project
CONTAINER=$(xcrun simctl get_app_container "$SIMULATOR_ID" "$BUNDLE_ID" data)
cp -R "$CONTAINER/Documents/../../tmp/marketing" ./marketing/

echo ""
echo "✅ All locales captured → ./marketing/"
```

## Critical Gotchas (Baked Into Skill)

### 1. Live Activities Persist Across Launches

**Problem:** Next locale crashes on stale SwiftData references.

**Solution:** End all Live Activities in cleanup:

```swift
for activity in Activity<PulseAttributes>.activities {
    await activity.end(nil, dismissalPolicy: .immediate)
}
```

### 2. Re-Seeding Per Locale

**Problem:** CloudKit sync churn causes crashes.

**Solution:** Seed once at launch, not per step.

### 3. ViewModels Setup Before Seed

**Problem:** VMs hold stale empty snapshots.

**Solution:** Seed data → wait 1s → instantiate VMs → capture.

### 4. Setting Trigger Binding to nil

**Problem:** Doesn't dismiss `fullScreenCover` — captures wrong sheet.

**Solution:** Use dedicated dismiss closure:

```swift
.fullScreenCover(isPresented: $showTimer) {
    TimerView(onDismiss: { showTimer = false })
}
```

### 5. NavigationPath Can't Be Popped Externally

**Problem:** Pushing over existing path captures wrong stack.

**Solution:** Always `popToRoot()` before `push()` in navigate block.

### 6. `membershipExceptions` Is an INCLUSION List

**Problem:** Widget target membership goes backwards — widget renders fail.

**Solution:** Set `membershipExceptions` for DEBUG files to exclude widget target:

```swift
// In pbxproj or via Xcode:
// MarketingCapture.swift → Target Membership → Widget ❌
```

### 7. `ImageRenderer` + `ProgressView`

**Problem:** Renders as prohibited symbol without explicit style.

**Solution:** Force `.circular` style:

```swift
ProgressView()
    .progressViewStyle(.circular)
```

### 8. `.containerBackground` Outside WidgetKit

**Problem:** No-op — widget renders have no background.

**Solution:** Manually add background in render harness:

```swift
WidgetView(entry: entry)
    .background(Color.white)
```

### 9. iPhone 8 Plus Gone on iOS 18+

**Problem:** Legacy 6.5" simulator unavailable.

**Solution:** Use iPhone 17 Pro Max or latest available large device.

### 10. Locale Launch Argument Format

**Problem:** Locale ignored if parens missing.

**Solution:** Always use `"($LOCALE)"` format:

```bash
-AppleLanguages "(de)"  # ✅
-AppleLanguages "de"    # ❌
```

### 11. SwiftUI Animations in ImageRenderer

**Problem:** Captures frame 0, not animated state.

**Solution:** Render non-animated state or use explicit `.animation(nil)`.

## Common Workflows

### Capturing Timer Mid-Countdown

```swift
CaptureStep(
    name: "05-timer-active",
    navigate: {
        router.popToRoot()
        coordinator.startTimer(seconds: 180)
        // Timer view subscribes to coordinator.activeTimer
    },
    settle: .seconds(1.5), // Let timer animate in
    cleanup: {
        coordinator.stopTimer()
        router.popToRoot()
    }
)
```

### Capturing Presented Sheet

```swift
@State private var showSheet = false

// Step:
CaptureStep(
    name: "06-add-coffee",
    navigate: {
        showSheet = true
    },
    settle: .seconds(0.8),
    cleanup: {
        showSheet = false
    }
)

// View:
.sheet(isPresented: $showSheet) {
    AddCoffeeView()
}
```

### Rendering All Widgets

```swift
#if DEBUG
@MainActor
func renderAllWidgets() {
    let entries = [
        ("pulse-small", PulseWidgetSmallView.self, 158),
        ("pulse-medium", PulseWidgetMediumView.self, 338),
        ("pulse-large", PulseWidgetLargeView.self, 338)
    ]
    
    for (name, viewType, width) in entries {
        MarketingElementHarness.renderElement(
            name: "widget-\(name)",
            width: width,
            cornerRadius: 16,
            background: .white
        ) {
            viewType.init(entry: sampleEntry)
                .padding(16)
        }
    }
}
#endif
```

## Troubleshooting

### Capture exits immediately

**Check:** `MARKETING_CAPTURE=1` env var is set in launch args.

```bash
xcrun simctl launch ... -MARKETING_CAPTURE 1
```

### Locale not applied

**Check:** Parens in `-AppleLanguages`:

```bash
-AppleLanguages "(de)"  # ✅ Correct
```

### Widget renders blank

**Check:** Manual padding added (WidgetKit adds 16pt automatically):

```swift
WidgetView(entry: entry)
    .padding(16)  // Add this
```

### Screenshot captures wrong screen

**Check:** Settle duration long enough for animations:

```swift
settle: .seconds(0.8)  // Increase if needed
```

### SwiftData crash on second locale

**Check:** Live Activities ended in cleanup:

```swift
cleanup: {
    Task {
        for activity in Activity<Attrs>.activities {
            await activity.end(nil, dismissalPolicy: .immediate)
        }
    }
}
```

### Element renders with wrong size

**Check:** Frame width explicitly set:

```swift
content()
    .frame(width: 380)  // Must be explicit
```

## Configuration Reference

### Capture Step Properties

| Property | Type | Purpose |
|----------|------|---------|
| `name` | `String` | Filename without extension (e.g. "01-home") |
| `navigate` | `@MainActor () -> Void` | Put app in correct state |
| `settle` | `Duration` | Wait time for animations |
| `cleanup` | `(@MainActor () -> Void)?` | Tear down before next step |

### Script Variables

| Variable | Example | Purpose |
|----------|---------|---------|
| `APP_NAME` | `"YourApp"` | App target name |
| `SCHEME` | `"YourApp"` | Xcode scheme |
| `DEVICE` | `"iPhone 17"` | Simulator model |
| `IOS_VERSION` | `"18.2"` | iOS runtime |
| `LOCALES` | `("en" "de" "es")` | Locale codes |

### Environment Variables

Set in launch args or script:

```bash
MARKETING_CAPTURE=1        # Enable capture mode
```

## Post-Processing

Use [app-store-screenshots](https://github.com/ParthJadhav/app-store-screenshots) to composite captured PNGs into Apple-style marketing pages with device mockups, headlines, and gradients.

```bash
npx skills add ParthJadhav/app-store-screenshots
```

Then prompt:

```
Composite my marketing screenshots into App Store pages with device frames
```

## When to Use This Skill

✅ **Use when:**
- Capturing marketing screenshots for App Store
- Rendering isolated components (cards, widgets, charts)
- Multi-locale asset generation
- SwiftUI-based iOS app with defined navigation
- Need full control over demo data and app state

❌ **Don't use when:**
- UIKit-based app (requires different capture approach)
- XCUITest infrastructure already working well
- Single locale, manual capture sufficient
- App uses web views or external content (can't seed)

## Example: Complete Coffee App Capture

```swift
#if DEBUG
@MainActor
func makeMarketingSteps(
    coordinator: AppCoordinator,
    router: Router,
    viewModel: HomeViewModel
) -> [CaptureStep] {
    let coffees = viewModel.coffees
    
    return [
        // Tab 1: Home
        CaptureStep(
            name: "01-home",
            navigate: { coordinator.setTab(0) },
            settle: .seconds(0.5),
            cleanup: nil
        ),
        
        // Tab 2: Shelf
        CaptureStep(
            name: "02-shelf",
            navigate: { coordinator.setTab(1) },
            settle: .seconds(0.5),
            cleanup: nil
        ),
        
        // Detail: First coffee
        CaptureStep(
            name: "03-detail",
            navigate: {
                coordinator.setTab(0)
                router.popToRoot()
                router.push(.coffeeDetail(coffees[0]))
            },
            settle: .seconds(0.8),
            cleanup: { router.popToRoot() }
        ),
        
        // Timer: Active brew
        CaptureStep(
            name: "04-timer",
            navigate: {
                coordinator.setTab(0)
                router.popToRoot()
                coordinator.startTimer(seconds: 180)
            },
            settle: .seconds(1.2),
            cleanup: {
                coordinator.stopTimer()
                router.popToRoot()
            }
        ),
        
        // Settings
        CaptureStep(
            name: "05-settings",
            navigate: { coordinator.setTab(2) },
            settle: .seconds(0.5),
            cleanup: nil
        ),
        
        // Elements: Cards
        CaptureStep(
            name: "elements",
            navigate: {
                for (index, coffee) in coffees.enumerated() {
                    MarketingElementHarness.renderElement(
                        name: "card-\(index + 1)",
                        width: 380,
                        cornerRadius: 20,
                        background: Color(.systemBackground)
                    ) {
                        CoffeeCard(coffee: coffee)
                            .padding(.horizontal, 16)
                            .padding(.vertical, 12)
                    }
                }
                
                renderAllWidgets()
            },
            settle: .seconds(0.1),
            cleanup: nil
        )
    ]
}
#endif
```

Run:

```bash
chmod +x scripts/capture-marketing.sh
./scripts/capture-marketing.sh
```

Output:

```
marketing/
    en/
        01-home.png
        02-shelf.png
        03-detail.png
        04-timer.png
        05-settings.png
        elements/
            card-1.png
            card-2.png
            widget-pulse-small.png
            widget-pulse-medium.png
    de/
        [same structure]
    es/
        [same structure]
    fr/
        [same structure]
    ja/
        [same structure]
```

## Summary

This skill automates iOS marketing screenshot capture by:

1. **Gathering requirements** — screens, elements, locales, device, appearance
2. **Generating capture system** — DEBUG-gated coordinator + steps
3. **Seeding demo data** — deterministic, locale-agnostic
4. **Navigating programmatically** — TabView, NavigationStack, or SplitView
5. **Capturing window** — `drawHierarchy` for full screenshots
6. **Rendering elements** — `ImageRenderer` for isolated components
7. **Looping locales** — `simctl launch` with `-AppleLanguages`

The result: one build, N launches, complete multi-locale marketing assets ready for App Store or further compositing.
