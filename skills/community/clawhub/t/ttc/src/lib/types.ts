/**
 * TTC CLI type definitions.
 * Covers both static GTFS data (bundled JSON) and real-time GTFS-RT entities.
 */

// ─── Static GTFS (bundled in data/*.json) ────────────────────────────────────

export interface GtfsStop {
  stop_id: string;
  stop_code: string;
  stop_name: string;
  stop_lat: number;
  stop_lon: number;
  /** Pre-computed normalized name for fuzzy matching */
  normalized?: string;
}

export interface GtfsRoute {
  route_id: string;
  route_short_name: string;
  route_long_name: string;
  route_type: number; // 0=streetcar/LRT, 3=bus
}

export interface GtfsTrip {
  trip_id: string;
  route_id: string;
  direction_id: number;
  trip_headsign: string;
}

export interface GtfsManifest {
  bundled: string;
  source: string;
  stop_count: number;
  route_count: number;
  trip_count: number;
}

// ─── GTFS-RT (real-time from protobuf feeds) ─────────────────────────────────

export interface VehiclePosition {
  vehicleId: string;
  routeId: string;
  tripId: string;
  latitude: number;
  longitude: number;
  bearing: number;
  speed: number;
  occupancyStatus: string;
  stopId: string;
  currentStopSequence: number;
  currentStatus: string;
  timestamp: number;
}

export interface StopTimeUpdate {
  stopSequence: number;
  stopId: string;
  arrivalTime: number | null;
  departureTime: number | null;
}

export interface TripUpdate {
  tripId: string;
  routeId: string;
  vehicleId: string;
  stopTimeUpdates: StopTimeUpdate[];
  timestamp: number;
}

export interface ServiceAlert {
  id: string;
  routeIds: string[];
  headerText: string;
  descriptionText: string;
}

export interface StopSearchResult {
  stop: GtfsStop;
  score: number;
}
