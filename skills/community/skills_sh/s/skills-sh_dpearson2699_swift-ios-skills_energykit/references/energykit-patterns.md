# EnergyKit Extended Patterns

Overflow reference for the `energykit` skill. Contains advanced patterns
that exceed the main skill file's scope.

## Contents

- [Full App Architecture](#full-app-architecture)
- [EV Charging Session Manager](#ev-charging-session-manager)
- [HVAC Control Manager](#hvac-control-manager)
- [SwiftUI Energy Dashboard](#swiftui-energy-dashboard)
- [Insight Data Visualization](#insight-data-visualization)
- [Error Handling Strategies](#error-handling-strategies)
- [Venue Discovery Flow](#venue-discovery-flow)

## Full App Architecture

An `@Observable` manager that ties together guidance, venues, and load events.

```swift
import EnergyKit
import SwiftUI

@Observable
@MainActor
final class EnergyManager {
    var venues: [EnergyVenue] = []
    var selectedVenue: EnergyVenue?
    var currentGuidance: ElectricityGuidance?
    var guidanceValues: [ElectricityGuidance.Value] = []
    var isLoading = false
    var errorMessage: String?

    private var guidanceTask: Task<Void, Never>?

    func loadVenues() async {
        isLoading = true
        errorMessage = nil

        do {
            venues = try await EnergyVenue.venues()
            selectedVenue = venues.first
            if let venue = selectedVenue {
                startObservingGuidance(for: venue.id)
            }
        } catch let error as EnergyKitError {
            errorMessage = handleError(error)
        } catch {
            errorMessage = error.localizedDescription
        }

        isLoading = false
    }

    func startObservingGuidance(for venueID: UUID) {
        guidanceTask?.cancel()
        guidanceTask = Task { [weak self] in
            let query = ElectricityGuidance.Query(suggestedAction: .shift)
            let service = ElectricityGuidance.sharedService

            do {
                for try await guidance in service.guidance(using: query, at: venueID) {
                    self?.currentGuidance = guidance
                    self?.guidanceValues = guidance.values
                }
            } catch {
                self?.errorMessage = error.localizedDescription
            }
        }
    }

    func stopObserving() {
        guidanceTask?.cancel()
        guidanceTask = nil
    }

    var bestWindow: ElectricityGuidance.Value? {
        guidanceValues.min(by: { $0.rating < $1.rating })
    }

    var hasRatePlan: Bool {
        currentGuidance?.options.contains(.locationHasRatePlan) ?? false
    }

    var usesRatePlan: Bool {
        currentGuidance?.options.contains(.guidanceIncorporatesRatePlan) ?? false
    }

    // EnergyKitError cases
    private func handleError(_ error: EnergyKitError) -> String {
        switch error {
        case .unsupportedRegion:
            return "Energy guidance is not available in your region."
        case .guidanceUnavailable:
            return "Grid guidance data is currently unavailable."
        case .venueUnavailable:
            return "No energy venue found. Set up your home in the Home app."
        case .permissionDenied:
            return "Permission to access energy data was denied."
        case .serviceUnavailable:
            return "The energy service is temporarily unavailable."
        case .rateLimitExceeded:
            return "Too many requests. Please try again later."
        case .invalidLoadEvent:
            return "The load event data was invalid."
        case .inProgress:
            return "A request is already in progress."
        case .locationServicesDenied:
            return "Location services are required for energy guidance."
        @unknown default:
            return "An unknown error occurred."
        }
    }
}
```

## EV Charging Session Manager

Manage the full lifecycle of an EV charging session with guidance tracking.
Use only a `guidanceToken` returned by EnergyKit for the venue and device that
requested guidance. Do not synthesize placeholder tokens.

```swift
import EnergyKit

@Observable
@MainActor
final class EVChargingManager {
    var isCharging = false
    var currentSessionID: UUID?
    var stateOfCharge: Int = 0
    var currentPower: Double = 0  // kW
    var totalEnergy: Double = 0   // kWh

    private let deviceID: String
    private var venue: EnergyVenue?
    private var guidanceToken: UUID?
    private var pendingEvents: [ElectricVehicleLoadEvent] = []

    init(deviceID: String) {
        self.deviceID = deviceID
    }

    func setVenue(_ venue: EnergyVenue) {
        self.venue = venue
    }

    func setGuidanceToken(_ token: UUID) {
        self.guidanceToken = token
    }

    func startCharging(stateOfCharge: Int) async throws {
        guard let venue else { throw EVError.noVenue }

        let sessionID = UUID()
        currentSessionID = sessionID
        self.stateOfCharge = stateOfCharge
        isCharging = true

        let event = try makeEvent(
            sessionState: .begin,
            stateOfCharge: stateOfCharge,
            power: 0,
            energy: 0
        )
        pendingEvents = [event]
    }

    func updateCharging(
        stateOfCharge: Int,
        power: Double,
        energy: Double
    ) async throws {
        guard let venue, isCharging else { return }

        self.stateOfCharge = stateOfCharge
        self.currentPower = power
        self.totalEnergy = energy

        let event = try makeEvent(
            sessionState: .active,
            stateOfCharge: stateOfCharge,
            power: power,
            energy: energy
        )
        pendingEvents.append(event)

        if pendingEvents.count >= 4 {
            try await flushPendingEvents()
        }
    }

    func stopCharging() async throws {
        guard let venue, isCharging else { return }

        let event = try makeEvent(
            sessionState: .end,
            stateOfCharge: stateOfCharge,
            power: 0,
            energy: totalEnergy
        )
        pendingEvents.append(event)
        try await flushPendingEvents()

        isCharging = false
        currentSessionID = nil
    }

    func flushPendingEvents() async throws {
        guard let venue, !pendingEvents.isEmpty else { return }

        let events = pendingEvents
        pendingEvents.removeAll()
        try await venue.submitEvents(events)
    }

    private func makeEvent(
        sessionState: ElectricVehicleLoadEvent.Session.State,
        stateOfCharge: Int,
        power: Double,
        energy: Double
    ) throws -> ElectricVehicleLoadEvent {
        guard let guidanceToken else { throw EVError.missingGuidanceToken }
        guard let currentSessionID else { throw EVError.noActiveSession }

        let guidanceState = ElectricVehicleLoadEvent.Session.GuidanceState(
            wasFollowingGuidance: true,
            guidanceToken: guidanceToken
        )

        let session = ElectricVehicleLoadEvent.Session(
            id: currentSessionID,
            state: sessionState,
            guidanceState: guidanceState
        )

        let measurement = ElectricVehicleLoadEvent.ElectricalMeasurement(
            stateOfCharge: stateOfCharge,
            direction: .imported,
            power: Measurement(value: power, unit: .kilowatts),
            energy: Measurement(value: energy, unit: .kilowattHours)
        )

        return ElectricVehicleLoadEvent(
            timestamp: Date(),
            measurement: measurement,
            session: session,
            deviceID: deviceID
        )
    }

    enum EVError: Error {
        case noVenue
        case missingGuidanceToken
        case noActiveSession
    }
}
```

## HVAC Control Manager

Track HVAC load events with guidance compliance.
Submit events when the heating or cooling stage changes, and use the real
guidance token that was in effect for that venue.
Treat heat stage 1 -> heat stage 2, heat -> cooling, cooling -> idle, and
equipment stop as distinct load events instead of one summarized session row.
For devices that emit frequent stage/runtime samples, buffer events and submit
periodically or at the end of a session, while still recording significant state
changes as they occur.

```swift
import EnergyKit

@Observable
@MainActor
final class HVACManager {
    var isRunning = false
    var currentStage: Int = 0
    var sessionID: UUID?

    private let deviceID: String
    private var venue: EnergyVenue?
    private var guidanceToken: UUID?

    init(deviceID: String) {
        self.deviceID = deviceID
    }

    func configure(venue: EnergyVenue, guidanceToken: UUID) {
        self.venue = venue
        self.guidanceToken = guidanceToken
    }

    func start(stage: Int) async throws {
        guard let venue else { return }
        sessionID = UUID()
        currentStage = stage
        isRunning = true

        let event = try makeEvent(state: .begin, stage: stage)
        try await venue.submitEvents([event])
    }

    func updateStage(_ stage: Int) async throws {
        guard let venue, isRunning else { return }
        currentStage = stage

        let event = try makeEvent(state: .active, stage: stage)
        try await venue.submitEvents([event])
    }

    func stop() async throws {
        guard let venue, isRunning else { return }

        let event = try makeEvent(state: .end, stage: 0)
        try await venue.submitEvents([event])

        isRunning = false
        sessionID = nil
    }

    private func makeEvent(
        state: ElectricHVACLoadEvent.Session.State,
        stage: Int
    ) throws -> ElectricHVACLoadEvent {
        guard let guidanceToken else { throw HVACError.missingGuidanceToken }
        guard let sessionID else { throw HVACError.noActiveSession }

        let guidanceState = ElectricHVACLoadEvent.Session.GuidanceState(
            wasFollowingGuidance: true,
            guidanceToken: guidanceToken
        )

        let session = ElectricHVACLoadEvent.Session(
            id: sessionID,
            state: state,
            guidanceState: guidanceState
        )

        let measurement = ElectricHVACLoadEvent.ElectricalMeasurement(stage: stage)

        return ElectricHVACLoadEvent(
            timestamp: Date(),
            measurement: measurement,
            session: session,
            deviceID: deviceID
        )
    }

    enum HVACError: Error {
        case missingGuidanceToken
        case noActiveSession
    }
}
```

## SwiftUI Energy Dashboard

A complete dashboard view showing guidance and insights.

```swift
import SwiftUI
import EnergyKit

struct EnergyDashboardView: View {
    @Environment(EnergyManager.self) private var energyManager

    var body: some View {
        NavigationStack {
            Group {
                if energyManager.isLoading {
                    ProgressView("Loading energy data...")
                } else if let error = energyManager.errorMessage {
                    ContentUnavailableView(
                        "Energy Guidance Unavailable",
                        systemImage: "bolt.slash",
                        description: Text(error)
                    )
                } else {
                    dashboardContent
                }
            }
            .navigationTitle("Energy")
            .task {
                await energyManager.loadVenues()
            }
        }
    }

    private var dashboardContent: some View {
        List {
            if let venue = energyManager.selectedVenue {
                Section("Venue") {
                    LabeledContent("Name", value: venue.name)
                }
            }

            if let best = energyManager.bestWindow {
                Section("Best Time") {
                    VStack(alignment: .leading) {
                        Text("Optimal usage window")
                            .font(.headline)
                        Text(best.interval.start, style: .time)
                        + Text(" - ")
                        + Text(best.interval.end, style: .time)
                        Text("Rating: \(best.rating, specifier: "%.2f")")
                            .foregroundStyle(.secondary)
                    }
                }
            }

            if !energyManager.guidanceValues.isEmpty {
                Section("Timeline") {
                    ForEach(energyManager.guidanceValues, id: \.interval.start) { value in
                        HStack {
                            VStack(alignment: .leading) {
                                Text(value.interval.start, style: .time)
                                Text(value.interval.end, style: .time)
                                    .font(.caption)
                                    .foregroundStyle(.secondary)
                            }
                            Spacer()
                            guidanceRatingView(value.rating)
                        }
                    }
                }
            }

            if energyManager.hasRatePlan {
                Section("Rate Plan") {
                    Label(
                        energyManager.usesRatePlan
                            ? "Guidance incorporates your rate plan"
                            : "Rate plan available but not yet incorporated",
                        systemImage: "dollarsign.circle"
                    )
                }
            }
        }
    }

    private func guidanceRatingView(_ rating: Double) -> some View {
        let color: Color = rating <= 0.3 ? .green : rating <= 0.6 ? .yellow : .red
        let label = rating <= 0.3 ? "Good" : rating <= 0.6 ? "Fair" : "Avoid"

        return Text(label)
            .font(.caption)
            .fontWeight(.medium)
            .padding(.horizontal)
            .padding(.vertical)
            .background(color.opacity(0.15))
            .foregroundStyle(color)
            .clipShape(Capsule())
    }
}
```

## Insight Data Visualization

Prepare insight records for chart display.
`dataByGridCleanliness` is iOS/iPadOS 26.1+, so keep the chart model optional
and guard access when supporting 26.0.

```swift
struct InsightDataPoint: Identifiable {
    let id = UUID()
    let date: Date
    let energy: Double  // kWh
    let cleanerEnergy: Double?
    let lessCleanEnergy: Double?
}

func processInsightRecords(
    _ records: [ElectricityInsightRecord<Measurement<UnitEnergy>>]
) -> [InsightDataPoint] {
    records.compactMap { record in
        guard let total = record.totalEnergy else { return nil }

        let cleanliness: (cleaner: Double?, lessClean: Double?)
        if #available(iOS 26.1, iPadOS 26.1, *) {
            cleanliness = (
                record.dataByGridCleanliness?.cleaner?
                    .converted(to: .kilowattHours).value,
                record.dataByGridCleanliness?.lessClean?
                    .converted(to: .kilowattHours).value
            )
        } else {
            cleanliness = (nil, nil)
        }

        return InsightDataPoint(
            date: record.range.start,
            energy: total.converted(to: .kilowattHours).value,
            cleanerEnergy: cleanliness.cleaner,
            lessCleanEnergy: cleanliness.lessClean
        )
    }
}
```

## Error Handling Strategies

Comprehensive error handling with retry logic.

```swift
@Observable
@MainActor
final class ResilientEnergyService {
    private let maxRetries = 3

    func fetchGuidanceWithRetry(venueID: UUID) async throws -> ElectricityGuidance? {
        let query = ElectricityGuidance.Query(suggestedAction: .shift)
        let service = ElectricityGuidance.sharedService

        for attempt in 0..<maxRetries {
            do {
                for try await guidance in service.guidance(using: query, at: venueID) {
                    return guidance
                }
            } catch let error as EnergyKitError {
                switch error {
                case .serviceUnavailable, .rateLimitExceeded:
                    if attempt < maxRetries - 1 {
                        try await Task.sleep(for: .seconds(pow(2.0, Double(attempt + 1))))
                    }
                case .unsupportedRegion, .permissionDenied, .venueUnavailable:
                    throw error  // Do not retry permanent failures
                default:
                    throw error
                }
            }
        }

        return nil
    }
}
```

## Venue Discovery Flow

Guide users through venue setup if none exist.

```swift
import SwiftUI
import EnergyKit

struct VenueSetupView: View {
    @State private var venues: [EnergyVenue] = []
    @State private var isLoading = true
    @State private var showSetupGuide = false

    var body: some View {
        Group {
            if isLoading {
                ProgressView()
            } else if venues.isEmpty {
                ContentUnavailableView {
                    Label("No Energy Venues", systemImage: "house")
                } description: {
                    Text("Set up your home in the Home app to use energy guidance.")
                } actions: {
                    Button("Learn More") { showSetupGuide = true }
                        .buttonStyle(.borderedProminent)
                }
            } else {
                List(venues, id: \.id) { venue in
                    NavigationLink(value: venue.id) {
                        Label(venue.name, systemImage: "house.fill")
                    }
                }
            }
        }
        .task {
            do {
                venues = try await EnergyVenue.venues()
            } catch {
                venues = []
            }
            isLoading = false
        }
    }
}
```
