# CarPlay Extended Patterns

Overflow reference for the `carplay` skill. Contains advanced patterns that
exceed the main skill file's scope.

## Contents

- [Dashboard Scene for Navigation Apps](#dashboard-scene-for-navigation-apps)
- [Instrument Cluster Scene](#instrument-cluster-scene)
- [Full Navigation Session Lifecycle](#full-navigation-session-lifecycle)
- [Lane Guidance](#lane-guidance)
- [Navigation Alerts](#navigation-alerts)
- [Map Panning Delegate](#map-panning-delegate)
- [Advanced List Patterns](#advanced-list-patterns)
- [Audio App: Full Scene Delegate](#audio-app-full-scene-delegate)
- [Communication App Patterns](#communication-app-patterns)
- [Quick Food Ordering Flow](#quick-food-ordering-flow)
- [Session Configuration and Vehicle Limits](#session-configuration-and-vehicle-limits)
- [Handling Multiple Scenes](#handling-multiple-scenes)

## Dashboard Scene for Navigation Apps

Navigation apps can present maps, upcoming maneuvers, and shortcut buttons
in the CarPlay Dashboard. Add `CPSupportsDashboardNavigationScene` and a
dashboard scene configuration to Info.plist alongside the main scene.

```plist
<key>UIApplicationSceneManifest</key>
<dict>
    <key>CPSupportsDashboardNavigationScene</key>
    <true/>
    <key>UISceneConfigurations</key>
    <dict>
        <key>CPTemplateApplicationDashboardSceneSessionRoleApplication</key>
        <array>
            <dict>
                <key>UISceneClassName</key>
                <string>CPTemplateApplicationDashboardScene</string>
                <key>UISceneConfigurationName</key>
                <string>CarPlayDashboardConfiguration</string>
                <key>UISceneDelegateClassName</key>
                <string>$(PRODUCT_MODULE_NAME).DashboardSceneDelegate</string>
            </dict>
        </array>
    </dict>
</dict>
```

### Dashboard Scene Delegate

```swift
import CarPlay

final class DashboardSceneDelegate: UIResponder,
    CPTemplateApplicationDashboardSceneDelegate {

    var dashboardWindow: UIWindow?
    var dashboardController: CPDashboardController?

    func templateApplicationDashboardScene(
        _ scene: CPTemplateApplicationDashboardScene,
        didConnect dashboardController: CPDashboardController,
        to window: UIWindow
    ) {
        self.dashboardController = dashboardController
        self.dashboardWindow = window
        window.rootViewController = DashboardMapViewController()

        dashboardController.shortcutButtons = [
            CPDashboardButton(
                titleVariants: ["Home"], subtitleVariants: ["25 min"],
                image: UIImage(systemName: "house.fill")!) { _ in },
            CPDashboardButton(
                titleVariants: ["Work"], subtitleVariants: ["35 min"],
                image: UIImage(systemName: "building.2.fill")!) { _ in }
        ]
    }

    func templateApplicationDashboardScene(
        _ scene: CPTemplateApplicationDashboardScene,
        didDisconnect dashboardController: CPDashboardController,
        from window: UIWindow
    ) {
        self.dashboardController = nil
        self.dashboardWindow = nil
    }
}
```

## Instrument Cluster Scene

Navigation apps can display turn-by-turn guidance in the vehicle's
instrument cluster using `CPTemplateApplicationInstrumentClusterScene`.

```swift
final class InstrumentClusterDelegate: UIResponder,
    CPTemplateApplicationInstrumentClusterSceneDelegate {

    var instrumentClusterController: CPInstrumentClusterController?

    func templateApplicationInstrumentClusterScene(
        _ scene: CPTemplateApplicationInstrumentClusterScene,
        didConnect instrumentClusterController: CPInstrumentClusterController
    ) {
        self.instrumentClusterController = instrumentClusterController
        instrumentClusterController.delegate = self
    }
}

extension InstrumentClusterDelegate: CPInstrumentClusterControllerDelegate {
    func instrumentClusterControllerDidConnect(
        _ controller: CPInstrumentClusterController) { }

    func instrumentClusterController(
        _ controller: CPInstrumentClusterController,
        didChangeCompassSetting setting: CPInstrumentClusterSetting) { }

    func instrumentClusterController(
        _ controller: CPInstrumentClusterController,
        didChangeSpeedLimitSetting setting: CPInstrumentClusterSetting) { }
}
```

## Full Navigation Session Lifecycle

A complete navigation session flow from trip creation through completion.

```swift
import CarPlay
import MapKit

final class NavigationManager: @unchecked Sendable {
    var navigationSession: CPNavigationSession?
    var mapTemplate: CPMapTemplate?

    func createTrip(to destination: CLLocationCoordinate2D,
                    name: String) -> CPTrip {
        let origin = MKMapItem.forCurrentLocation()
        let destItem = MKMapItem(placemark: MKPlacemark(coordinate: destination))
        destItem.name = name

        return CPTrip(origin: origin, destination: destItem, routeChoices: [
            CPRouteChoice(summaryVariants: ["Fastest"],
                          additionalInformationVariants: ["Via Highway"],
                          selectionSummaryVariants: ["25 min"]),
            CPRouteChoice(summaryVariants: ["Shortest"],
                          additionalInformationVariants: ["Local Roads"],
                          selectionSummaryVariants: ["30 min"])
        ])
    }

    func startNavigation(for trip: CPTrip, routeChoice: CPRouteChoice) {
        guard let mapTemplate else { return }
        let session = mapTemplate.startNavigationSession(for: trip)
        navigationSession = session
        session.pauseTrip(for: .loading, description: "Calculating route...")

        Task {
            let maneuvers = await calculateManeuvers()
            session.upcomingManeuvers = maneuvers
            if let first = maneuvers.first {
                session.updateEstimates(
                    CPTravelEstimates(
                        distanceRemaining: Measurement(value: 12.5, unit: .miles),
                        timeRemaining: 1500),
                    for: first)
            }
        }
    }

    func updateManeuver(instruction: String, symbolName: String,
                        distanceMiles: Double, timeSeconds: TimeInterval) {
        guard let session = navigationSession else { return }
        let maneuver = CPManeuver()
        maneuver.instructionVariants = [instruction]
        maneuver.symbolImage = UIImage(systemName: symbolName)
        session.upcomingManeuvers = [maneuver]
        session.updateEstimates(
            CPTravelEstimates(
                distanceRemaining: Measurement(value: distanceMiles, unit: .miles),
                timeRemaining: timeSeconds),
            for: maneuver)
    }

    func updateCurrentRoad(_ roadName: String) {
        navigationSession?.currentRoadNameVariants = [roadName]
    }

    func reroute() {
        navigationSession?.pauseTrip(for: .rerouting, description: "Rerouting...")
        Task {
            let maneuvers = await calculateManeuvers()
            navigationSession?.upcomingManeuvers = maneuvers
        }
    }

    func finishNavigation() {
        navigationSession?.finishTrip()
        navigationSession = nil
        mapTemplate?.hideTripPreviews()
    }

    func cancelNavigation() {
        navigationSession?.cancelTrip()
        navigationSession = nil
    }

    private func calculateManeuvers() async -> [CPManeuver] {
        let turn = CPManeuver()
        turn.instructionVariants = ["Turn right onto Main St", "Right on Main"]
        turn.symbolImage = UIImage(systemName: "arrow.turn.up.right")

        let arrive = CPManeuver()
        arrive.instructionVariants = ["Arrive at destination", "Arrive"]
        arrive.symbolImage = UIImage(systemName: "mappin.circle.fill")

        return [turn, arrive]
    }
}
```

## Lane Guidance

Provide lane guidance during active navigation to display lane arrows.

```swift
func provideLaneGuidance(for session: CPNavigationSession) {
    let guidance = CPLaneGuidance()
    guidance.instructionVariants = ["Use left two lanes"]

    let left = CPLane(); left.status = .preferred
    let middle = CPLane(); middle.status = .good
    let right = CPLane(); right.status = .notGood
    guidance.lanes = [left, middle, right]

    session.add([guidance])
    session.currentLaneGuidance = guidance
}
```

## Navigation Alerts

Display time-sensitive alerts on the map template for incidents or closures.

```swift
func showNavigationAlert(on mapTemplate: CPMapTemplate) {
    let alert = CPNavigationAlert(
        titleVariants: ["Road Closure Ahead", "Road Closed"],
        subtitleVariants: ["Main St closed at 5th Ave"],
        image: UIImage(systemName: "exclamationmark.triangle.fill"),
        primaryAction: CPAlertAction(title: "Reroute", style: .default) { _ in
            mapTemplate.dismissNavigationAlert(animated: true, completion: nil)
        },
        secondaryAction: CPAlertAction(title: "Dismiss", style: .cancel) { _ in
            mapTemplate.dismissNavigationAlert(animated: true, completion: nil)
        },
        duration: 10.0)

    mapTemplate.present(navigationAlert: alert, animated: true)
}
```

## Map Panning Delegate

Handle user-initiated map panning via touchscreen or rotary controller.

```swift
extension CarPlaySceneDelegate: CPMapTemplateDelegate {
    func mapTemplateDidShowPanningInterface(_ mapTemplate: CPMapTemplate) {
        // User entered panning mode
    }

    func mapTemplateDidDismissPanningInterface(_ mapTemplate: CPMapTemplate) {
        // User exited panning mode
    }

    func mapTemplate(_ mapTemplate: CPMapTemplate,
                     panWith direction: CPMapTemplate.PanDirection) {
        switch direction {
        case .up:    mapViewController.panUp()
        case .down:  mapViewController.panDown()
        case .left:  mapViewController.panLeft()
        case .right: mapViewController.panRight()
        @unknown default: break
        }
    }
}
```

## Advanced List Patterns

### Header Grid Buttons

```swift
let listTemplate = CPListTemplate(
    title: "Browse",
    sections: [CPListSection(items: items)],
    assistantCellConfiguration: nil,
    headerGridButtons: [
        CPGridButton(titleVariants: ["Favorites"],
                     image: UIImage(systemName: "heart.fill")!) { _ in },
        CPGridButton(titleVariants: ["Recents"],
                     image: UIImage(systemName: "clock.fill")!) { _ in }
    ])
```

### Dynamic Updates

Use transactional APIs to update list content without rebuilding templates.

```swift
template.updateSections([
    CPListSection(items: newItems, header: "Results", sectionIndexTitle: nil)
])
```

### Empty State and Loading Spinner

```swift
listTemplate.emptyViewTitleVariants = ["No Results Found"]
listTemplate.emptyViewSubtitleVariants = ["Try a different search"]
listTemplate.showsSpinnerWhileEmpty = true

// After loading:
listTemplate.showsSpinnerWhileEmpty = false
listTemplate.updateSections([CPListSection(items: loadedItems)])
```

### Tab Badge Updates

```swift
var templates = tabBar.templates
templates[0].showsTabBadge = true
tabBar.updateTemplates(templates)
```

## Audio App: Full Scene Delegate

```swift
import CarPlay
import MediaPlayer

final class AudioCarPlaySceneDelegate: UIResponder,
    CPTemplateApplicationSceneDelegate, CPNowPlayingTemplateObserver {

    var interfaceController: CPInterfaceController?

    func templateApplicationScene(
        _ scene: CPTemplateApplicationScene,
        didConnect interfaceController: CPInterfaceController
    ) {
        self.interfaceController = interfaceController
        configureNowPlaying()
        interfaceController.setRootTemplate(buildRootTemplate(),
                                            animated: true, completion: nil)
    }

    func templateApplicationScene(
        _ scene: CPTemplateApplicationScene,
        didDisconnectInterfaceController ic: CPInterfaceController
    ) { self.interfaceController = nil }

    private func buildRootTemplate() -> CPTabBarTemplate {
        let items = MusicLibrary.shared.playlists.map { playlist in
            let item = CPListItem(text: playlist.name,
                                  detailText: "\(playlist.count) songs",
                                  image: playlist.artwork)
            item.handler = { [weak self] _, completion in
                MusicLibrary.shared.play(playlist)
                self?.interfaceController?.pushTemplate(
                    CPNowPlayingTemplate.shared, animated: true,
                    completion: nil)
                completion()
            }
            return item
        }
        let tab = CPListTemplate(title: "Library",
                                 sections: [CPListSection(items: items)])
        tab.tabImage = UIImage(systemName: "music.note.list")
        return CPTabBarTemplate(templates: [tab])
    }

    private func configureNowPlaying() {
        let np = CPNowPlayingTemplate.shared
        np.isAlbumArtistButtonEnabled = true
        np.isUpNextButtonEnabled = true
        np.updateNowPlayingButtons([
            CPNowPlayingShuffleButton { _ in MusicLibrary.shared.toggleShuffle() },
            CPNowPlayingRepeatButton { _ in MusicLibrary.shared.toggleRepeat() }
        ])
        np.add(self)
    }

    func nowPlayingTemplateUpNextButtonTapped(_ t: CPNowPlayingTemplate) {
        let items = MusicLibrary.shared.upNext.map {
            CPListItem(text: $0.title, detailText: $0.artist)
        }
        interfaceController?.pushTemplate(
            CPListTemplate(title: "Up Next",
                           sections: [CPListSection(items: items)]),
            animated: true, completion: nil)
    }

    func nowPlayingTemplateAlbumArtistButtonTapped(_ t: CPNowPlayingTemplate) { }
}
```

## Communication App Patterns

### Contact Template

```swift
let contact = CPContact(
    name: PersonNameComponents(givenName: "Jane", familyName: "Doe"),
    image: UIImage(systemName: "person.circle.fill")!)

contact.actions = [
    CPButton(image: UIImage(systemName: "phone.fill")!) { _ in },
    CPButton(image: UIImage(systemName: "message.fill")!) { _ in }
]

let contactTemplate = CPContactTemplate(contact: contact)
interfaceController?.pushTemplate(contactTemplate, animated: true,
                                  completion: nil)
```

### Assistant Cell for Calls

```swift
let config = CPAssistantCellConfiguration(
    position: .top, visibility: .always, assistantAction: .startCall)
let messageList = CPListTemplate(
    title: "Messages",
    sections: [CPListSection(items: messageItems)],
    assistantCellConfiguration: config)
```

## Quick Food Ordering Flow

Food ordering apps must not exceed two levels of list hierarchy.

```swift
// Step 1: POI template showing nearby restaurants
func showRestaurants(interfaceController: CPInterfaceController) {
    let pois = fetchNearbyRestaurants().map { r -> CPPointOfInterest in
        let poi = CPPointOfInterest(
            location: r.mapItem, title: r.name, subtitle: r.cuisine,
            summary: r.rating, detailTitle: r.name,
            detailSubtitle: r.priceRange,
            detailSummary: "Open until \(r.closingTime)",
            pinImage: UIImage(systemName: "fork.knife"))
        poi.primaryButton = CPTextButton(title: "Order",
                                         textStyle: .confirm) { _ in
            self.showMenu(for: r, interfaceController: interfaceController)
        }
        return poi
    }
    let template = CPPointOfInterestTemplate(
        title: "Restaurants", pointsOfInterest: pois, selectedIndex: 0)
    template.pointOfInterestDelegate = self
    interfaceController.pushTemplate(template, animated: true, completion: nil)
}

// Step 2: Menu list
func showMenu(for restaurant: Restaurant,
              interfaceController: CPInterfaceController) {
    let items = restaurant.menuItems.map { item in
        let li = CPListItem(text: item.name, detailText: item.formattedPrice)
        li.handler = { _, completion in
            self.addToOrder(item)
            self.showOrderSummary(interfaceController: interfaceController)
            completion()
        }
        return li
    }
    interfaceController.pushTemplate(
        CPListTemplate(title: restaurant.name,
                       sections: [CPListSection(items: items)]),
        animated: true, completion: nil)
}

// Step 3: Order confirmation via CPInformationTemplate
func showOrderSummary(interfaceController: CPInterfaceController) {
    let info = CPInformationTemplate(
        title: "Order Summary", layout: .leading,
        items: currentOrder.items.map {
            CPInformationItem(title: $0.name, detail: $0.formattedPrice)
        },
        actions: [
            CPTextButton(title: "Place Order", textStyle: .confirm) { _ in
                self.placeOrder() },
            CPTextButton(title: "Cancel", textStyle: .cancel) { _ in
                interfaceController.popToRootTemplate(animated: true,
                                                      completion: nil) }
        ])
    interfaceController.pushTemplate(info, animated: true, completion: nil)
}
```

## Session Configuration and Vehicle Limits

Query `CPSessionConfiguration` to adapt content to vehicle constraints.

```swift
func configureForVehicle(sessionConfig: CPSessionConfiguration) {
    let limits = sessionConfig.limitedUserInterfaces
    if limits.contains(.keyboard) {
        // Vehicle is limiting keyboard display -- adapt text entry/search.
    }

    // Always respect template maximums
    let maxItems = CPListTemplate.maximumItemCount
    let maxSections = CPListTemplate.maximumSectionCount
}
```

## Handling Multiple Scenes

An app can have both a phone scene and a CarPlay scene active at the same
time. Share state via an `@Observable` singleton or similar pattern.

```swift
@Observable
final class AppState {
    static let shared = AppState()
    var currentPlaylist: Playlist?
    var isPlaying = false
}

// Both PhoneSceneDelegate and CarPlaySceneDelegate read/write AppState.shared.
// CPTemplate subclasses are @MainActor -- ensure template mutations happen
// on the main actor when updating from background threads.
```
