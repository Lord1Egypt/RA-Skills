# RelevanceKit Patterns

Extended patterns and reference material for RelevanceKit widget relevance
on watchOS 26+. See the main `SKILL.md` for an overview and quick-start
guidance.

## Contents

- [Complete Relevant Widget Example](#complete-relevant-widget-example)
- [Boundary Routing Cheat Sheet](#boundary-routing-cheat-sheet)
- [Complete Timeline Provider Relevance Example](#complete-timeline-provider-relevance-example)
- [RelevanceEntry Patterns](#relevanceentry-patterns)
- [Permission Handling](#permission-handling)
- [All RelevantContext Factories](#all-relevantcontext-factories)
- [Grouping Strategies](#grouping-strategies)
- [Associating Timeline and Relevant Widgets](#associating-timeline-and-relevant-widgets)
- [Preview Recipes](#preview-recipes)
- [Combining Multiple Clue Types](#combining-multiple-clue-types)
- [Point-of-Interest Categories](#point-of-interest-categories)
- [Updating Relevance Outside the Timeline](#updating-relevance-outside-the-timeline)
- [Testing Tips](#testing-tips)

---

## Boundary Routing Cheat Sheet

Relevant widget plumbing lives in WidgetKit, but it belongs in this skill only
when it exposes watchOS Smart Stack relevance clues.

- Keep `RelevantContext`, `WidgetRelevance`, `WidgetRelevanceAttribute`,
  provider `relevance()`, `RelevantIntentManager`, and relevant-widget
  handoffs in RelevanceKit scope.
- Route general widget timelines, rendering, families, reload budgets, APNs
  widget push updates, Live Activities, and widget Controls to WidgetKit.
- Route `HKWorkoutSession`, `HKLiveWorkoutBuilder`, `HKWorkoutRoute`, HealthKit
  queries, activity-ring data, sleep analysis data, and authorization flows to
  HealthKit.
- Route `MKLocalSearch`, `MKLocalSearchCompleter`, `MKDirections`,
  `CLGeocoder`, `CLLocationManager`, regions, geofencing, and place lookup to
  MapKit/CoreLocation. Use their outputs only as inputs to
  `RelevantContext.location(...)`.

---

## Complete Relevant Widget Example

A full watchOS-only widget using `RelevanceConfiguration` and
`RelevanceEntriesProvider`. This widget shows upcoming meetings and only
appears in the Smart Stack when a meeting is approaching.

```swift
import WidgetKit
import SwiftUI
import RelevanceKit
import AppIntents

// MARK: - Entry

@available(watchOS 26.0, *)
struct MeetingRelevanceEntry: RelevanceEntry {
    let title: String
    let time: Date
    let location: String?
    let isPlaceholder: Bool

    static let placeholder = MeetingRelevanceEntry(
        title: "Meeting",
        time: .now,
        location: nil,
        isPlaceholder: true
    )

    static let preview = MeetingRelevanceEntry(
        title: "Design Review",
        time: .now.addingTimeInterval(1800),
        location: "Room 3",
        isPlaceholder: false
    )
}

// MARK: - Configuration Intent

struct MeetingWidgetIntent: WidgetConfigurationIntent {
    static var title: LocalizedStringResource = "Meeting"
    static var description: IntentDescription = "Shows an upcoming meeting."

    @Parameter(title: "Meeting ID")
    var meetingID: String

    init() {}
    init(meetingID: String) {
        self.meetingID = meetingID
    }
}

// MARK: - Provider

@available(watchOS 26.0, *)
struct MeetingRelevanceProvider: RelevanceEntriesProvider {
    typealias Configuration = MeetingWidgetIntent
    typealias Entry = MeetingRelevanceEntry

    func relevance() async -> WidgetRelevance<MeetingWidgetIntent> {
        let meetings = await MeetingStore.shared.upcomingMeetings()

        let attributes = meetings.map { meeting in
            // Show the widget 15 minutes before through the meeting end
            let context = RelevantContext.date(
                from: meeting.startDate.addingTimeInterval(-900),
                to: meeting.endDate
            )
            return WidgetRelevanceAttribute(
                configuration: MeetingWidgetIntent(meetingID: meeting.id),
                context: context
            )
        }
        return WidgetRelevance(attributes)
    }

    func entry(
        configuration: MeetingWidgetIntent,
        context: Context
    ) async throws -> MeetingRelevanceEntry {
        if context.isPreview {
            return .preview
        }

        guard let meeting = await MeetingStore.shared
            .meeting(id: configuration.meetingID)
        else {
            return .placeholder
        }

        return MeetingRelevanceEntry(
            title: meeting.title,
            time: meeting.startDate,
            location: meeting.location,
            isPlaceholder: false
        )
    }

    func placeholder(context: Context) -> MeetingRelevanceEntry {
        .placeholder
    }
}

// MARK: - Widget

@available(watchOS 26.0, *)
struct MeetingRelevantWidget: Widget {
    let kind = "com.example.meeting-relevant"

    var body: some WidgetConfiguration {
        RelevanceConfiguration(
            kind: kind,
            provider: MeetingRelevanceProvider()
        ) { entry in
            MeetingWidgetView(entry: entry)
        }
        .configurationDisplayName("Meetings")
        .description("Shows upcoming meetings when relevant")
        .associatedKind("com.example.meeting-timeline")
    }
}

// MARK: - View

@available(watchOS 26.0, *)
struct MeetingWidgetView: View {
    let entry: MeetingRelevanceEntry

    var body: some View {
        VStack(alignment: .leading) {
            if entry.isPlaceholder {
                Text("Meeting")
                    .redacted(reason: .placeholder)
            } else {
                Text(entry.title)
                    .font(.headline)
                Text(entry.time, style: .time)
                    .font(.caption)
                if let location = entry.location {
                    Text(location)
                        .font(.caption2)
                        .foregroundStyle(.secondary)
                }
            }
        }
    }
}
```

---

## Complete Timeline Provider Relevance Example

Cross-platform timeline provider that adds watchOS relevance via `relevance()`
and `RelevantIntentManager`.

```swift
import WidgetKit
import SwiftUI
import RelevanceKit
import AppIntents

struct TaskEntry: TimelineEntry {
    let date: Date
    let task: TaskItem
}

struct TaskWidgetIntent: WidgetConfigurationIntent {
    static var title: LocalizedStringResource = "Task"
    static var description: IntentDescription = "Shows a task."

    @Parameter(title: "Task ID")
    var taskID: String

    init() {}
    init(taskID: String) {
        self.taskID = taskID
    }
}

struct TaskTimelineProvider: AppIntentTimelineProvider {
    typealias Entry = TaskEntry
    typealias Intent = TaskWidgetIntent

    func placeholder(in context: Context) -> TaskEntry {
        TaskEntry(date: .now, task: .placeholder)
    }

    func snapshot(for configuration: TaskWidgetIntent,
                  in context: Context) async -> TaskEntry {
        let task = await TaskStore.shared.task(id: configuration.taskID)
            ?? .placeholder
        return TaskEntry(date: .now, task: task)
    }

    func timeline(for configuration: TaskWidgetIntent,
                  in context: Context) async -> Timeline<TaskEntry> {
        let task = await TaskStore.shared.task(id: configuration.taskID)
            ?? .placeholder
        let entry = TaskEntry(date: .now, task: task)

        // Update relevant intents alongside timeline refresh
        await updateTaskRelevantIntents()

        return Timeline(entries: [entry], policy: .after(
            Date.now.addingTimeInterval(3600)
        ))
    }

    func recommendations() -> [AppIntentRecommendation<TaskWidgetIntent>] {
        []  // Configurable widget
    }

    // watchOS relevance -- provides contextual clues
    func relevance() async -> WidgetRelevance<TaskWidgetIntent> {
        let tasks = await TaskStore.shared.dueSoonTasks()

        let attributes = tasks.map { task in
            WidgetRelevanceAttribute(
                configuration: TaskWidgetIntent(taskID: task.id),
                context: RelevantContext.date(task.dueDate, kind: .scheduled)
            )
        }
        return WidgetRelevance(attributes)
    }

    private func updateTaskRelevantIntents() async {
        let tasks = await TaskStore.shared.dueSoonTasks()

        let intents = tasks.map { task in
            RelevantIntent(
                TaskWidgetIntent(taskID: task.id),
                widgetKind: "com.example.task-widget",
                relevance: RelevantContext.date(task.dueDate, kind: .scheduled)
            )
        }

        try? await RelevantIntentManager.shared
            .updateRelevantIntents(intents)
    }
}
```

---

## RelevanceEntry Patterns

`RelevanceEntry` conforms to `Sendable`. Keep entries lightweight -- they carry
only the data needed to render the view. Types that conform to `RelevanceEntry`
are watchOS 26.0+.

### Minimal Entry

```swift
@available(watchOS 26.0, *)
struct SimpleRelevanceEntry: RelevanceEntry {
    let value: String
}
```

### Entry with Placeholder Support

```swift
@available(watchOS 26.0, *)
struct WeatherRelevanceEntry: RelevanceEntry {
    let temperature: String
    let condition: String
    let isPlaceholder: Bool

    static let placeholder = WeatherRelevanceEntry(
        temperature: "--",
        condition: "Clear",
        isPlaceholder: true
    )
}
```

### Entry with Optional Data

```swift
@available(watchOS 26.0, *)
struct FlightRelevanceEntry: RelevanceEntry {
    let flightNumber: String?
    let departureTime: Date?
    let gate: String?

    var isLoading: Bool { flightNumber == nil }

    static let loading = FlightRelevanceEntry(
        flightNumber: nil,
        departureTime: nil,
        gate: nil
    )
}
```

---

## Permission Handling

Location, fitness, and sleep clues require target-specific setup. Keep location
authorization in the containing app, then declare widget location usage in the
extension. For HealthKit-based fitness and sleep clues, enable HealthKit and
request the exact read types in the app and widget extension target that
provides relevance.

### Location Setup

Add `NSWidgetWantsLocation` to the widget extension's Info.plist:

```xml
<key>NSWidgetWantsLocation</key>
<true/>
```

Add the appropriate location purpose strings to the containing app's Info.plist,
and have the app request location authorization before the widget relies on
location clues:

```xml
<key>NSLocationWhenInUseUsageDescription</key>
<string>Shows relevant widgets based on your location.</string>
```

In widget code, check whether the person extended app location authorization to
the widget:

```swift
let manager = CLLocationManager()
let canUseLocationInWidget = manager.isAuthorizedForWidgetUpdates
```

### HealthKit Permissions for Fitness/Sleep

Request only the HealthKit data types required by the clue in the target that
evaluates those clues. `sleep(_:)` requires `sleepAnalysis`; `.workoutActive`
requires `HKWorkoutType`; and
`.activityRingsIncomplete` requires `appleExerciseTime`, `appleMoveTime`, and
`appleStandTime`.

```swift
import HealthKit

func requestSleepPermission() async {
    let store = HKHealthStore()
    let sleepType = HKCategoryType(.sleepAnalysis)
    try? await store.requestAuthorization(toShare: [], read: [sleepType])
}

func requestFitnessRelevancePermission() async {
    let store = HKHealthStore()
    let workoutType = HKObjectType.workoutType()
    let ringTypes: Set<HKObjectType> = [
        HKQuantityType(.appleExerciseTime),
        HKQuantityType(.appleMoveTime),
        HKQuantityType(.appleStandTime),
    ]
    try? await store.requestAuthorization(
        toShare: [],
        read: ringTypes.union([workoutType])
    )
}
```

### Graceful Degradation

Always handle the case where permissions are denied. The widget should still
function -- it just won't appear via relevance clues that require the missing
permission.

```swift
func relevance() async -> WidgetRelevance<MyIntent> {
    var attributes: [WidgetRelevanceAttribute<MyIntent>] = []

    // Time-based clues always work (no permission needed)
    for event in events {
        attributes.append(
            WidgetRelevanceAttribute(
                configuration: MyIntent(eventID: event.id),
                context: .date(event.date, kind: .scheduled)
            )
        )
    }

    // Location clues require widget location approval -- add if available
    if CLLocationManager().isAuthorizedForWidgetUpdates {
        attributes.append(
            WidgetRelevanceAttribute(
                configuration: MyIntent(mode: .nearby),
                context: .location(inferred: .work)
            )
        )
    }

    return WidgetRelevance(attributes)
}
```

---

## All RelevantContext Factories

### Time Clues

```swift
// At a specific date
RelevantContext.date(someDate)

// At a date with a kind hint
RelevantContext.date(someDate, kind: .scheduled)
RelevantContext.date(someDate, kind: .informational)
RelevantContext.date(someDate, kind: .default)

// Between two dates
RelevantContext.date(from: startDate, to: endDate)

// Using DateInterval
RelevantContext.date(interval: dateInterval, kind: .scheduled)

// Using ClosedRange<Date>
RelevantContext.date(range: startDate...endDate, kind: .default)
```

### Location Clues

`location(category:)` is available on Apple platform SDKs 26.0+ and returns an
optional; RelevanceKit clues still affect Smart Stack behavior only on watchOS.

```swift
// Inferred locations (from the person's routine)
RelevantContext.location(inferred: .home)
RelevantContext.location(inferred: .work)
RelevantContext.location(inferred: .school)
RelevantContext.location(inferred: .commute)

// Specific geographic region
RelevantContext.location(CLCircularRegion(...))

// Point-of-interest category (returns optional)
RelevantContext.location(category: .cafe)       // MKPointOfInterestCategory
RelevantContext.location(category: .airport)
RelevantContext.location(category: .beach)
```

### Fitness Clues

```swift
RelevantContext.fitness(.activityRingsIncomplete)
RelevantContext.fitness(.workoutActive)
```

### Sleep Clues

```swift
RelevantContext.sleep(.bedtime)
RelevantContext.sleep(.wakeup)
```

### Hardware Clues

```swift
RelevantContext.hardware(headphones: .connected)
```

---

## Grouping Strategies

`WidgetRelevanceGroup` controls how the system deduplicates and organizes
widgets from the same app in the Smart Stack.

### Default Grouping

By default, the system groups widgets per-app. This means only one widget
from the app may appear at a time.

```swift
WidgetRelevanceAttribute(
    configuration: intent,
    group: .automatic
)
```

### Ungrouped

Opt out of default grouping. Each widget card can appear independently,
useful when multiple cards should be visible simultaneously.

```swift
WidgetRelevanceAttribute(
    configuration: intent,
    group: .ungrouped
)
```

### Named Groups

Place related widgets in a named group. Only one widget from each group
appears at a time, but widgets in different groups can coexist.

```swift
// These two share a group -- only one shows
WidgetRelevanceAttribute(
    configuration: weatherCurrent,
    group: .named("weather")
)
WidgetRelevanceAttribute(
    configuration: weatherForecast,
    group: .named("weather")
)

// This one is in a different group -- can show alongside weather
WidgetRelevanceAttribute(
    configuration: calendarIntent,
    group: .named("calendar")
)
```

---

## Associating Timeline and Relevant Widgets

When an app offers both a timeline-based widget and a relevance-based widget
showing overlapping information, use `.associatedKind(_:)` to prevent
duplicate cards.

```swift
@available(watchOS 26, *)
struct EventRelevantWidget: Widget {
    var body: some WidgetConfiguration {
        RelevanceConfiguration(
            kind: "com.example.event-relevant",
            provider: EventRelevanceProvider()
        ) { entry in
            EventView(entry: entry)
        }
        // When relevant cards are suggested, they replace the timeline widget
        .associatedKind("com.example.event-timeline")
    }
}

struct EventTimelineWidget: Widget {
    var body: some WidgetConfiguration {
        AppIntentConfiguration(
            kind: "com.example.event-timeline",
            provider: EventTimelineProvider()
        ) { entry in
            EventView(entry: entry)
        }
    }
}
```

When the system has relevant cards to show, it replaces the pinned timeline
widget card with the relevant widget cards. When no relevant cards match,
the timeline widget remains visible.

---

## Preview Recipes

### Preview with Sample Entries

Useful during view development to test layout across display sizes.

```swift
#Preview("Meeting Cards", widget: MeetingRelevantWidget.self,
         relevanceEntries: {
    [
        MeetingRelevanceEntry(
            title: "Standup",
            time: .now.addingTimeInterval(600),
            location: "Zoom",
            isPlaceholder: false
        ),
        MeetingRelevanceEntry(
            title: "Long Planning Session Title",
            time: .now.addingTimeInterval(3600),
            location: "Conference Room B",
            isPlaceholder: false
        ),
    ]
})
```

### Preview with Relevance Configurations

Useful for testing that the provider creates correct entries from configurations.

```swift
#Preview("Relevance", widget: MeetingRelevantWidget.self, relevance: {
    WidgetRelevance([
        WidgetRelevanceAttribute(
            configuration: MeetingWidgetIntent(meetingID: "standup"),
            context: .date(Date(), kind: .scheduled)
        ),
        WidgetRelevanceAttribute(
            configuration: MeetingWidgetIntent(meetingID: "planning"),
            context: .date(
                Date().addingTimeInterval(3600),
                kind: .scheduled
            )
        ),
    ])
})
```

### Preview with the Full Provider

End-to-end preview using the actual provider. Supply test data through
a preview-specific data source.

```swift
#Preview("Full Provider", widget: MeetingRelevantWidget.self,
         relevanceProvider: MeetingRelevanceProvider())
```

---

## Combining Multiple Clue Types

A single widget can be relevant under diverse conditions. Mix clue types
to cover different scenarios.

```swift
func relevance() async -> WidgetRelevance<PodcastIntent> {
    var attributes: [WidgetRelevanceAttribute<PodcastIntent>] = []

    // Show during commute (likely listening time)
    attributes.append(
        WidgetRelevanceAttribute(
            configuration: PodcastIntent(mode: .recentEpisode),
            context: .location(inferred: .commute)
        )
    )

    // Show when headphones are connected
    attributes.append(
        WidgetRelevanceAttribute(
            configuration: PodcastIntent(mode: .nowPlaying),
            context: .hardware(headphones: .connected)
        )
    )

    // Show during workout (many people listen while exercising)
    attributes.append(
        WidgetRelevanceAttribute(
            configuration: PodcastIntent(mode: .workout),
            context: .fitness(.workoutActive)
        )
    )

    // Show around bedtime (sleep podcast)
    if hasSleepPodcast {
        attributes.append(
            WidgetRelevanceAttribute(
                configuration: PodcastIntent(mode: .sleep),
                context: .sleep(.bedtime)
            )
        )
    }

    return WidgetRelevance(attributes)
}
```

---

## Point-of-Interest Categories

`RelevantContext.location(category:)` accepts `MKPointOfInterestCategory`
values. The method returns `RelevantContext?` -- not all categories are
supported by the system. It is available in Apple platform SDKs 26.0+; always
handle the `nil` case and remember that RelevanceKit effects are watchOS-only.

```swift
import MapKit

func locationRelevanceForCategory(
    _ category: MKPointOfInterestCategory,
    intent: MyIntent
) -> WidgetRelevanceAttribute<MyIntent>? {
    guard let context = RelevantContext.location(category: category) else {
        return nil
    }
    return WidgetRelevanceAttribute(configuration: intent, context: context)
}

// Usage
let categories: [MKPointOfInterestCategory] = [.cafe, .restaurant, .grocery]
let attributes = categories.compactMap { category in
    locationRelevanceForCategory(category, intent: FoodIntent())
}
```

---

## Updating Relevance Outside the Timeline

When using the timeline provider path, relevance data can become stale
between timeline refreshes. Update `RelevantIntentManager` whenever
underlying data changes.

```swift
// In the main app, after data changes
func onEventsUpdated(_ events: [Event]) async {
    let intents = events.map { event in
        RelevantIntent(
            EventWidgetIntent(eventID: event.id),
            widgetKind: "com.example.events",
            relevance: RelevantContext.date(
                from: event.start,
                to: event.end
            )
        )
    }
    try? await RelevantIntentManager.shared.updateRelevantIntents(intents)

    // Also reload the timeline
    WidgetCenter.shared.reloadTimelines(ofKind: "com.example.events")
}
```

---

## Testing Tips

1. **Enable Developer Mode.** On the Apple Watch, go to Settings > Developer
   and enable WidgetKit Developer Mode. This bypasses rotation limits so
   relevant widgets appear immediately.

2. **Use Xcode Previews.** The three preview variants (entries, relevance,
   provider) let you verify appearance without deploying to a device.

3. **Verify permissions.** Test with location/health permissions both granted
   and denied. Widgets should degrade gracefully, not crash.

4. **Test with `context.isPreview`.** The preview branch in `entry()` is
   called when the widget appears in system settings and the widget gallery.
   Return representative data that helps the user understand what the widget
   shows.

5. **Check placeholder.** The placeholder entry appears while the widget loads
   data. Use `.redacted(reason: .placeholder)` or a loading indicator.

6. **Inspect on device.** The Simulator does not fully replicate Smart Stack
   behavior. Test on a real Apple Watch for accurate relevance triggering.

7. **Audit for duplicates.** If both a timeline widget and a relevant widget
   exist for the same data, verify that `.associatedKind(_:)` is set and
   working correctly.
