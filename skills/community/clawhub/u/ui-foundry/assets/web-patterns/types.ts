/** A selection produced by a place provider. Coordinates are optional by design. */
export type Place = {
	id: string;
	label: string;
	address: string;
	latitude?: number;
	longitude?: number;
	coordinateSystem: "GCJ-02" | "WGS84" | "BD-09" | null;
	source: "amap" | "manual" | "fixture";
};

/**
 * Keep network and vendor concerns outside the UI. Implementations must honour
 * AbortSignal so a stale response cannot replace a newer query.
 */
export type PlaceProvider = {
	search(query: string, signal: AbortSignal): Promise<Place[]>;
};

export type MeetingDraft = {
	title: string;
	date: string; // Local calendar date: YYYY-MM-DD. Never serialize a Date as UTC.
	place: Place | null;
};
