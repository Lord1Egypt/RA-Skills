# WeatherKit Extended Patterns

Overflow reference for the `weatherkit` skill. Contains advanced patterns that exceed the main skill file's scope.

## Contents

- [WeatherKit SwiftUI Integration](#weatherkit-swiftui-integration)
- [Charts Integration](#charts-integration)
- [Historical Weather Statistics](#historical-weather-statistics)
- [Weather Changes and Historical Comparisons](#weather-changes-and-historical-comparisons)
- [Weather Condition Mapping](#weather-condition-mapping)
- [Caching Strategy](#caching-strategy)
- [Location-Based Weather](#location-based-weather)
- [References](#references)

## WeatherKit SwiftUI Integration

SwiftUI views may trigger loads from `.task` or `.refreshable`, but the
`@Observable` model should decide whether a network request is needed. Use
`loadWeatherIfNeeded` for automatic view lifecycle loads and a separate refresh
path for explicit user refresh.

### Weather Manager with `@Observable`

```swift
import WeatherKit
import CoreLocation

@Observable
@MainActor
final class WeatherManager {
    private let service = WeatherService.shared

    var current: CurrentWeather?
    var hourlyForecast: Forecast<HourWeather>?
    var dailyForecast: Forecast<DayWeather>?
    var alerts: [WeatherAlert]?
    var attribution: WeatherAttribution?
    var isLoading = false
    var error: Error?

    func loadWeatherIfNeeded(for location: CLLocation) async {
        guard current == nil else { return }
        await refreshWeather(for: location)
    }

    func refreshWeather(for location: CLLocation) async {
        isLoading = true
        error = nil

        do {
            let (current, hourly, daily, alerts) = try await service.weather(
                for: location,
                including: .current, .hourly, .daily, .alerts
            )
            self.current = current
            self.hourlyForecast = hourly
            self.dailyForecast = daily
            self.alerts = alerts
            self.attribution = try await service.attribution
        } catch {
            self.error = error
        }

        isLoading = false
    }
}
```

### Weather Dashboard View

```swift
import SwiftUI
import WeatherKit

struct WeatherDashboardView: View {
    @Environment(WeatherManager.self) private var manager
    let location: CLLocation

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack {
                    if manager.isLoading {
                        ProgressView("Loading weather...")
                    } else if let current = manager.current {
                        currentConditionsCard(current)
                    }

                    if let hourly = manager.hourlyForecast {
                        hourlyForecastSection(hourly)
                    }

                    if let daily = manager.dailyForecast {
                        dailyForecastSection(daily)
                    }

                    if let alerts = manager.alerts, !alerts.isEmpty {
                        alertsSection(alerts)
                    }

                    if let attribution = manager.attribution {
                        WeatherAttributionView(attribution: attribution)
                    }
                }
                .padding()
            }
            .navigationTitle("Weather")
            .task {
                await manager.loadWeatherIfNeeded(for: location)
            }
            .refreshable {
                await manager.refreshWeather(for: location)
            }
        }
    }

    private func currentConditionsCard(_ current: CurrentWeather) -> some View {
        VStack {
            Image(systemName: current.symbolName)
                .font(.system(size: 60))
                .symbolRenderingMode(.multicolor)

            Text(current.temperature.formatted())
                .font(.system(size: 48, weight: .thin))

            Text(current.condition.description)
                .font(.title3)
                .foregroundStyle(.secondary)

            HStack {
                Label(
                    "Humidity \(current.humidity.formatted(.percent))",
                    systemImage: "humidity"
                )
                Label(
                    "Wind \(current.wind.speed.formatted())",
                    systemImage: "wind"
                )
                Label(
                    "UV \(current.uvIndex.value)",
                    systemImage: "sun.max"
                )
            }
            .font(.caption)
        }
        .padding()
    }

    private func hourlyForecastSection(_ forecast: Forecast<HourWeather>) -> some View {
        VStack(alignment: .leading) {
            Text("Hourly Forecast")
                .font(.headline)

            ScrollView(.horizontal, showsIndicators: false) {
                HStack {
                    ForEach(Array(forecast.prefix(12)), id: \.date) { hour in
                        VStack {
                            Text(hour.date, format: .dateTime.hour())
                                .font(.caption)
                            Image(systemName: hour.symbolName)
                                .symbolRenderingMode(.multicolor)
                            Text(hour.temperature.formatted())
                                .font(.subheadline)
                        }
                    }
                }
            }
        }
    }

    private func dailyForecastSection(_ forecast: Forecast<DayWeather>) -> some View {
        VStack(alignment: .leading) {
            Text("10-Day Forecast")
                .font(.headline)

            ForEach(Array(forecast), id: \.date) { day in
                HStack {
                    Text(day.date, format: .dateTime.weekday(.abbreviated))
                        .frame(width: 40, alignment: .leading)

                    Image(systemName: day.symbolName)
                        .symbolRenderingMode(.multicolor)
                        .frame(width: 30)

                    Text(day.lowTemperature.formatted())
                        .foregroundStyle(.secondary)
                        .frame(width: 50, alignment: .trailing)

                    temperatureBar(low: day.lowTemperature, high: day.highTemperature)

                    Text(day.highTemperature.formatted())
                        .frame(width: 50)
                }
                .font(.subheadline)
            }
        }
    }

    private func temperatureBar(
        low: Measurement<UnitTemperature>,
        high: Measurement<UnitTemperature>
    ) -> some View {
        Capsule()
            .fill(.linearGradient(
                colors: [.blue, .orange],
                startPoint: .leading,
                endPoint: .trailing
            ))
            .frame(height: 4)
            .containerRelativeFrame(.horizontal) { length, _ in
                length * 0.3
            }
    }

    private func alertsSection(_ alerts: [WeatherAlert]) -> some View {
        VStack(alignment: .leading) {
            Text("Weather Alerts")
                .font(.headline)

            ForEach(alerts, id: \.detailsURL) { alert in
                HStack {
                    Image(systemName: "exclamationmark.triangle.fill")
                        .foregroundStyle(alert.severity == .extreme ? .red : .orange)
                    VStack(alignment: .leading) {
                        Text(alert.summary)
                            .font(.subheadline)
                        Text(alert.region ?? "Affected area unavailable")
                            .font(.caption)
                            .foregroundStyle(.secondary)

                        Link("Details", destination: alert.detailsURL)
                            .font(.caption2)
                    }
                }
                .padding()
                .background(.yellow.opacity(0.1))
                .clipShape(.rect(cornerRadius: 8))
            }
        }
    }
}
```

When alert or minute support is uncertain, fetch `WeatherAvailability` and use
only `alertAvailability` or `minuteAvailability`; it is not a broad matrix for
current, hourly, or daily forecast support.

### Attribution View

```swift
struct WeatherAttributionView: View {
    let attribution: WeatherAttribution
    @Environment(\.colorScheme) private var colorScheme

    var body: some View {
        VStack {
            AsyncImage(url: markURL) { image in
                image
                    .resizable()
                    .scaledToFit()
                    .frame(height: 12)
            } placeholder: {
                Text(attribution.serviceName)
                    .font(.caption2)
            }

            Link(destination: attribution.legalPageURL) {
                Text("Data Sources")
                    .font(.caption2)
                    .foregroundStyle(.secondary)
            }
        }
        .padding(.vertical)
    }

    private var markURL: URL {
        colorScheme == .dark
            ? attribution.combinedMarkDarkURL
            : attribution.combinedMarkLightURL
    }
}
```

## Charts Integration

### Hourly Temperature Chart

```swift
import SwiftUI
import Charts
import WeatherKit

struct HourlyTemperatureChart: View {
    let forecast: Forecast<HourWeather>

    var body: some View {
        Chart(Array(forecast.prefix(24)), id: \.date) { hour in
            LineMark(
                x: .value("Hour", hour.date),
                y: .value("Temperature", hour.temperature.converted(to: .celsius).value)
            )
            .interpolationMethod(.catmullRom)
            .foregroundStyle(.orange)

            AreaMark(
                x: .value("Hour", hour.date),
                y: .value("Temperature", hour.temperature.converted(to: .celsius).value)
            )
            .interpolationMethod(.catmullRom)
            .foregroundStyle(.orange.opacity(0.1))
        }
        .chartYAxisLabel("Temperature (C)")
        .chartXAxis {
            AxisMarks(values: .stride(by: .hour, count: 3)) { _ in
                AxisGridLine()
                AxisValueLabel(format: .dateTime.hour())
            }
        }
        .frame(height: 200)
    }
}
```

### Daily Precipitation Chart

```swift
struct DailyPrecipitationChart: View {
    let forecast: Forecast<DayWeather>

    var body: some View {
        Chart(Array(forecast), id: \.date) { day in
            BarMark(
                x: .value("Day", day.date, unit: .day),
                y: .value("Chance", day.precipitationChance)
            )
            .foregroundStyle(.blue.gradient)
        }
        .chartYScale(domain: 0...1)
        .chartYAxis {
            AxisMarks(format: .percent)
        }
        .chartXAxis {
            AxisMarks(values: .stride(by: .day)) { _ in
                AxisGridLine()
                AxisValueLabel(format: .dateTime.weekday(.abbreviated))
            }
        }
        .frame(height: 150)
    }
}
```

## Historical Weather Statistics

WeatherKit provides iOS 18+ historical statistics through variadic APIs. The
tuple return order matches the `including:` query order.
Use statistics properties such as `averagePrecipitationProbability`; do not use
forecast-only `DayWeather.precipitationChance` in statistics examples.

### Daily Statistics

```swift
@available(iOS 18.0, *)
func fetchDailyStats(
    for location: CLLocation,
    dateRange: DateInterval
) async throws -> [(day: Int, averageHigh: Measurement<UnitTemperature>, averagePrecipitation: Measurement<UnitLength>)] {
    let (dailyPrecipitation, dailyTemperature) = try await WeatherService.shared.dailyStatistics(
        for: location,
        forDaysIn: dateRange,
        including: .precipitation, .temperature
    )
    // Tuple order follows the variadic query order above.

    return zip(dailyPrecipitation, dailyTemperature).map { precipitation, temperature in
        (
            day: temperature.day,
            averageHigh: temperature.averageHighTemperature,
            averagePrecipitation: precipitation.averagePrecipitationAmount
        )
    }
}
```

### Monthly Statistics

```swift
@available(iOS 18.0, *)
func fetchMonthlyStats(
    for location: CLLocation
) async throws -> [(month: Int, averageLow: Measurement<UnitTemperature>, averagePrecipitation: Measurement<UnitLength>)] {
    let (monthlyPrecipitation, monthlyTemperature) = try await WeatherService.shared.monthlyStatistics(
        for: location,
        including: .precipitation, .temperature
    )
    // Tuple order follows the variadic query order above.

    return zip(monthlyPrecipitation, monthlyTemperature).map { precipitation, temperature in
        (
            month: temperature.month,
            averageLow: temperature.averageLowTemperature,
            averagePrecipitation: precipitation.averagePrecipitationAmount
        )
    }
}
```

## Weather Changes and Historical Comparisons

Use the optional iOS 18+ context queries to summarize why forecast data matters
for a user. `.changes` reports upcoming significant changes; `.historicalComparisons`
compares current conditions to historical averages and returns comparisons ordered
by significance.

For "unusual tomorrow" features, combine `.changes` with the tomorrow daily
date-range forecast and `.historicalComparisons`.

```swift
@available(iOS 18.0, *)
func contextHighlights(for location: CLLocation) async throws -> [String] {
    let (changes, comparisons) = try await WeatherService.shared.weather(
        for: location,
        including: .changes, .historicalComparisons
    )

    var highlights: [String] = []

    for change in changes?.changes ?? [] {
        switch change.highTemperature {
        case .increase:
            highlights.append("High temperature is expected to rise.")
        case .decrease:
            highlights.append("High temperature is expected to fall.")
        case .steady:
            break
        @unknown default:
            break
        }
    }

    for comparison in comparisons?.comparisons ?? [] {
        switch comparison {
        case .highTemperature(let trend):
            highlights.append("High temperature is \(trend.deviation).")
        case .lowTemperature(let trend):
            highlights.append("Low temperature is \(trend.deviation).")
        case .precipitationAmount(let trend):
            highlights.append("Precipitation is \(trend.deviation).")
        case .snowfallAmount(let trend):
            highlights.append("Snowfall is \(trend.deviation).")
        @unknown default:
            break
        }
    }

    return highlights
}
```

## Weather Condition Mapping

### Mapping Conditions to Colors

```swift
extension WeatherCondition {
    var themeColor: Color {
        switch self {
        case .clear, .mostlyClear:
            return .yellow
        case .partlyCloudy, .mostlyCloudy, .cloudy:
            return .gray
        case .rain, .heavyRain, .drizzle:
            return .blue
        case .snow, .heavySnow, .flurries, .sleet, .freezingRain,
             .freezingDrizzle, .wintryMix, .blizzard:
            return .cyan
        case .thunderstorms, .strongStorms, .tropicalStorm, .hurricane:
            return .purple
        case .foggy, .haze, .smoky:
            return .gray.opacity(0.6)
        case .breezy, .windy:
            return .teal
        case .hot:
            return .red
        case .frigid, .blowingDust:
            return .indigo
        @unknown default:
            return .primary
        }
    }
}
```

### Mapping Severity to Priority

```swift
extension WeatherSeverity {
    var displayPriority: Int {
        switch self {
        case .extreme:
            return 4
        case .severe:
            return 3
        case .moderate:
            return 2
        case .minor:
            return 1
        case .unknown:
            return 0
        @unknown default:
            return 0
        }
    }
}
```

## Caching Strategy

### Actor-Based Weather Cache

```swift
actor WeatherCache {
    struct CacheEntry {
        let weather: CurrentWeather
        let hourly: Forecast<HourWeather>
        let daily: Forecast<DayWeather>
        let expiresAt: Date
    }

    private var cache: [String: CacheEntry] = [:]

    func get(for key: String) -> CacheEntry? {
        guard let entry = cache[key], Date.now < entry.expiresAt else {
            cache[key] = nil
            return nil
        }
        return entry
    }

    func set(_ entry: CacheEntry, for key: String) {
        cache[key] = entry
    }

    /// Generate a cache key from a location (rounded to ~1km precision)
    static func key(for location: CLLocation) -> String {
        let lat = (location.coordinate.latitude * 100).rounded() / 100
        let lon = (location.coordinate.longitude * 100).rounded() / 100
        return "\(lat),\(lon)"
    }
}
```

### Using the Cache

```swift
@Observable
@MainActor
final class CachedWeatherManager {
    private let service = WeatherService.shared
    private let cache = WeatherCache()

    var current: CurrentWeather?

    func fetchWeather(for location: CLLocation) async throws {
        let key = WeatherCache.key(for: location)

        if let cached = await cache.get(for: key) {
            current = cached.weather
            return
        }

        let (current, hourly, daily) = try await service.weather(
            for: location,
            including: .current, .hourly, .daily
        )

        let entry = WeatherCache.CacheEntry(
            weather: current,
            hourly: hourly,
            daily: daily,
            expiresAt: min(
                current.metadata.expirationDate,
                hourly.metadata.expirationDate,
                daily.metadata.expirationDate
            )
        )
        await cache.set(entry, for: key)
        self.current = current
    }
}
```

## Location-Based Weather

### Combining CoreLocation with WeatherKit

```swift
import CoreLocation
import WeatherKit

@Observable
@MainActor
final class LocationWeatherManager: NSObject, CLLocationManagerDelegate {
    private let locationManager = CLLocationManager()
    private let weatherService = WeatherService.shared

    var current: CurrentWeather?
    var locationError: Error?

    override init() {
        super.init()
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyKilometer
    }

    func requestWeather() {
        locationManager.requestWhenInUseAuthorization()
        locationManager.requestLocation()
    }

    nonisolated func locationManager(
        _ manager: CLLocationManager,
        didUpdateLocations locations: [CLLocation]
    ) {
        guard let location = locations.last else { return }
        Task { @MainActor in
            do {
                current = try await weatherService.weather(
                    for: location,
                    including: .current
                )
            } catch {
                locationError = error
            }
        }
    }

    nonisolated func locationManager(
        _ manager: CLLocationManager,
        didFailWithError error: Error
    ) {
        Task { @MainActor in
            locationError = error
        }
    }
}
```

## References

- [WeatherKit](https://sosumi.ai/documentation/weatherkit)
- [WeatherAlert.detailsURL](https://sosumi.ai/documentation/weatherkit/weatheralert/detailsurl)
- [WeatherAlert.region](https://sosumi.ai/documentation/weatherkit/weatheralert/region)
- [WeatherMetadata.expirationDate](https://sosumi.ai/documentation/weatherkit/weathermetadata/expirationdate)
- [dailyStatistics(for:forDaysIn:including:)](https://sosumi.ai/documentation/weatherkit/weatherservice/dailystatistics(for:fordaysin:including:))
- [monthlyStatistics(for:including:)](https://sosumi.ai/documentation/weatherkit/weatherservice/monthlystatistics(for:including:))
- [WeatherQuery.changes](https://sosumi.ai/documentation/weatherkit/weatherquery/changes)
- [WeatherQuery.historicalComparisons](https://sosumi.ai/documentation/weatherkit/weatherquery/historicalcomparisons)
- [WeatherKit updates](https://sosumi.ai/documentation/updates/weatherkit)
