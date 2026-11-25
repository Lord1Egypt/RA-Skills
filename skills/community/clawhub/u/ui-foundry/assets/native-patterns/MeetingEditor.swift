// iOS 17+ reference. Copy into an app target; this file has no persistence or backend claim.
import MapKit
import SwiftUI

struct CivilDate: Equatable, Hashable, Sendable {
	let year: Int
	let month: Int
	let day: Int

	init?(year: Int, month: Int, day: Int) {
		var validationCalendar = Calendar(identifier: .gregorian)
		validationCalendar.timeZone = TimeZone(secondsFromGMT: 0) ?? .current
		guard let date = validationCalendar.date(from: DateComponents(year: year, month: month, day: day, hour: 12)) else {
			return nil
		}
		let normalized = validationCalendar.dateComponents([.year, .month, .day], from: date)
		guard normalized.year == year, normalized.month == month, normalized.day == day else {
			return nil
		}
		self.year = year
		self.month = month
		self.day = day
	}

	init(date: Date, displayCalendar: Calendar, timeZone: TimeZone) {
		let components = Self.gregorianCalendar(basedOn: displayCalendar, timeZone: timeZone)
			.dateComponents([.year, .month, .day], from: date)
		guard let year = components.year, let month = components.month, let day = components.day else {
			preconditionFailure("Could not derive Gregorian civil date")
		}
		self.year = year
		self.month = month
		self.day = day
	}

	func date(in displayCalendar: Calendar, timeZone: TimeZone) -> Date {
		guard let date = Self.gregorianCalendar(basedOn: displayCalendar, timeZone: timeZone)
			.date(from: DateComponents(year: year, month: month, day: day, hour: 12))
		else {
			preconditionFailure("CivilDate contains an invalid Gregorian calendar day")
		}
		return date
	}

	private static func gregorianCalendar(basedOn displayCalendar: Calendar, timeZone: TimeZone) -> Calendar {
		var calendar = Calendar(identifier: .gregorian)
		calendar.locale = displayCalendar.locale
		calendar.timeZone = timeZone
		return calendar
	}
}

struct MeetingDraft: Equatable {
	var title = ""
	var day = CivilDate(date: .now, displayCalendar: .current, timeZone: .current)
	var place: PlaceSelection?
}

/// A selected map result is a different data type from a manually written place.
/// Persist `providerID`/coordinates where provider terms allow it; preserve manual text as manual.
struct PlaceSelection: Identifiable, Equatable {
	enum Provenance: Equatable {
		case mapItem(providerID: String?)
		case manual
	}

	let id: UUID
	let name: String
	let subtitle: String?
	let provenance: Provenance
	let mapItem: MKMapItem?
	let latitude: Double?
	let longitude: Double?

	init(mapItem: MKMapItem) {
		id = UUID()
		name = mapItem.name ?? mapItem.placemark.name ?? "已选地点"
		subtitle = mapItem.placemark.title
		// `MKMapItem.identifier` starts in iOS 18. An iOS 17 client must treat
		// this as a resolved provider result, without inventing a stable provider ID.
		provenance = .mapItem(providerID: nil)
		self.mapItem = mapItem
		latitude = mapItem.placemark.coordinate.latitude
		longitude = mapItem.placemark.coordinate.longitude
	}

	init(manualName: String, details: String) {
		id = UUID()
		name = manualName
		subtitle = details.isEmpty ? nil : details
		provenance = .manual
		mapItem = nil
		latitude = nil
		longitude = nil
	}

	static func == (lhs: PlaceSelection, rhs: PlaceSelection) -> Bool {
		lhs.name == rhs.name
			&& lhs.subtitle == rhs.subtitle
			&& lhs.provenance == rhs.provenance
			&& lhs.latitude == rhs.latitude
			&& lhs.longitude == rhs.longitude
	}

	func matches(_ mapItem: MKMapItem) -> Bool {
		guard let latitude, let longitude else { return false }
		let coordinate = mapItem.placemark.coordinate
		return abs(latitude - coordinate.latitude) < 0.000_001
			&& abs(longitude - coordinate.longitude) < 0.000_001
			&& name == (mapItem.name ?? mapItem.placemark.name ?? "已选地点")
	}
}

struct MeetingEditor: View {
	@Environment(\.calendar) private var calendar
	@Environment(\.timeZone) private var timeZone
	@Environment(\.dismiss) private var dismiss
	@State private var draft: MeetingDraft
	@State private var presentsPlacePicker = false
	private let onSave: (MeetingDraft) -> Void

	init(initialDraft: MeetingDraft, onSave: @escaping (MeetingDraft) -> Void) {
		_draft = State(initialValue: initialDraft)
		self.onSave = onSave
	}

	private var dateBinding: Binding<Date> {
		Binding(
			get: { draft.day.date(in: calendar, timeZone: timeZone) },
			set: { draft.day = CivilDate(date: $0, displayCalendar: calendar, timeZone: timeZone) },
		)
	}

	var body: some View {
		Form {
			Section("会议") {
				TextField("标题", text: $draft.title)
				DatePicker("日期", selection: dateBinding, displayedComponents: .date)
					.accessibilityHint("只选择日期，不选择具体时刻")
			}

			Section("地点") {
				Button {
					presentsPlacePicker = true
				} label: {
					LabeledContent("地点") {
						Text(draft.place?.name ?? "选择地点")
							.foregroundStyle(draft.place == nil ? .secondary : .primary)
					}
				}
				.buttonStyle(.plain)

				if let mapItem = draft.place?.mapItem {
					ResolvedPlaceMapPreview(item: mapItem)
						.frame(height: 160)
						.clipShape(.rect(cornerRadius: 12))
				}
			}
		}
		.navigationTitle("新建会议")
		.toolbar {
			ToolbarItem(placement: .cancellationAction) {
				Button("取消") { dismiss() }
			}
			ToolbarItem(placement: .confirmationAction) {
				Button("保存") {
					onSave(draft)
					dismiss()
				}
			}
		}
		.sheet(isPresented: $presentsPlacePicker) {
			PlacePicker(initialSelection: draft.place) { selection in
				draft.place = selection
			}
		}
	}
}

private struct PlacePicker: View {
	let initialSelection: PlaceSelection?
	let onCommit: (PlaceSelection) -> Void

	@Environment(\.dismiss) private var dismiss
	@Environment(\.accessibilityReduceMotion) private var reduceMotion
	@State private var query = ""
	@State private var phase: SearchPhase = .idle
	@State private var results: [MKMapItem] = []
	@State private var candidate: PlaceSelection?
	@State private var showsManualEntry = false
	@State private var manualName = ""
	@State private var manualDetails = ""
	@State private var retryID = 0

	init(initialSelection: PlaceSelection?, onCommit: @escaping (PlaceSelection) -> Void) {
		self.initialSelection = initialSelection
		self.onCommit = onCommit
		_candidate = State(initialValue: initialSelection)
	}

	var body: some View {
		NavigationStack {
			List {
				if let candidate {
					Section("已选") {
						PlaceRow(selection: candidate, selected: true)
					}
				}

				Section("结果") {
					searchContent
				}

				Section {
					Button("手动填写地点", systemImage: "pencil") {
						manualName = query
						showsManualEntry.toggle()
					}
					if showsManualEntry {
						TextField("地点名称", text: $manualName)
						TextField("地址（可选）", text: $manualDetails)
						Button("使用此地点") {
							candidate = PlaceSelection(manualName: manualName, details: manualDetails)
							showsManualEntry = false
						}
						.disabled(manualName.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
					}
				}
			}
			.navigationTitle("选择地点")
			.searchable(text: $query, prompt: "搜索地点或地址")
			.task(id: SearchRequest(query: query, retryID: retryID)) { await search(query) }
			.onChange(of: query) { _, _ in
				candidate = nil
				showsManualEntry = false
			}
			.toolbar {
				ToolbarItem(placement: .cancellationAction) {
					Button("取消") { dismiss() }
				}
				ToolbarItem(placement: .confirmationAction) {
					Button("完成") {
						guard let candidate else { return }
						onCommit(candidate)
						dismiss()
					}
					.disabled(candidate == nil)
				}
			}
		}
	}

	@ViewBuilder
	private var searchContent: some View {
		switch phase {
		case .idle:
			ContentUnavailableView("搜索地点", systemImage: "magnifyingglass", description: Text("输入名称或地址"))
		case .loading:
			HStack { Spacer(); ProgressView(); Spacer() }
		case .empty:
			ContentUnavailableView.search(text: query)
		case .failed(let message):
			ContentUnavailableView {
				Label("暂时无法搜索", systemImage: "wifi.exclamationmark")
			} description: {
				Text(message)
			} actions: {
				Button("重试") { retryID += 1 }
			}
		case .results:
			ForEach(results, id: \.self) { item in
				Button {
					candidate = PlaceSelection(mapItem: item)
				} label: {
					PlaceRow(selection: PlaceSelection(mapItem: item), selected: candidate?.matches(item) ?? false)
				}
				.buttonStyle(.plain)
			}
		}
	}

	@MainActor
	private func search(_ input: String) async {
		let trimmed = input.trimmingCharacters(in: .whitespacesAndNewlines)
		guard !trimmed.isEmpty else {
			phase = .idle
			results = []
			return
		}

		let requestedQuery = trimmed
		phase = .loading
		do {
			try await Task.sleep(for: .milliseconds(280))
			try Task.checkCancellation()
			let request = MKLocalSearch.Request()
			request.naturalLanguageQuery = requestedQuery
			let localSearch = MKLocalSearch(request: request)
			let response = try await withTaskCancellationHandler {
				try await localSearch.start()
			} onCancel: {
				localSearch.cancel()
			}
			try Task.checkCancellation()
			guard query.trimmingCharacters(in: .whitespacesAndNewlines) == requestedQuery else { return }
			results = response.mapItems
			phase = results.isEmpty ? .empty : .results
		} catch is CancellationError {
			return
		} catch {
			guard query.trimmingCharacters(in: .whitespacesAndNewlines) == requestedQuery, !Task.isCancelled else { return }
			results = []
			phase = .failed("请稍后重试，或手动填写地点。")
		}
	}
}

private enum SearchPhase: Equatable {
	case idle
	case loading
	case results
	case empty
	case failed(String)
}

private struct SearchRequest: Hashable {
	let query: String
	let retryID: Int
}

private struct PlaceRow: View {
	let selection: PlaceSelection
	let selected: Bool
	@Environment(\.accessibilityReduceMotion) private var reduceMotion

	var body: some View {
		HStack(spacing: 12) {
			Image(systemName: selection.mapItem == nil ? "mappin.slash" : "mappin.circle.fill")
				.foregroundStyle(selection.mapItem == nil ? Color.secondary : Color.accentColor)
			VStack(alignment: .leading, spacing: 2) {
				Text(selection.name).foregroundStyle(.primary)
				if let subtitle = selection.subtitle, subtitle != selection.name {
					Text(subtitle).font(.footnote).foregroundStyle(.secondary).lineLimit(1)
				}
			}
			Spacer()
			if selected {
				Image(systemName: "checkmark.circle.fill").foregroundStyle(.tint)
			}
		}
		.contentShape(.rect)
		.animation(reduceMotion ? nil : .snappy(duration: 0.22), value: selected)
	}
}

private struct ResolvedPlaceMapPreview: View {
	let item: MKMapItem

	private var region: MKCoordinateRegion {
		MKCoordinateRegion(center: item.placemark.coordinate, latitudinalMeters: 900, longitudinalMeters: 900)
	}

	var body: some View {
		Map(initialPosition: .region(region)) {
			Marker(item.name ?? "地点", coordinate: item.placemark.coordinate)
		}
		.id("\(item.placemark.coordinate.latitude),\(item.placemark.coordinate.longitude)")
		.allowsHitTesting(false)
		.accessibilityLabel("已解析地点地图预览")
	}
}

#Preview {
	NavigationStack { MeetingEditor(initialDraft: MeetingDraft(), onSave: { _ in }) }
}
