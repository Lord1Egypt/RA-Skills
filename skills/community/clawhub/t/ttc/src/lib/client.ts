/**
 * TTC GTFS-RT Client.
 * Fetches and decodes protobuf feeds from bustime.ttc.ca.
 * No authentication required.
 */

import GtfsRealtimeBindings from "gtfs-realtime-bindings";
import type { VehiclePosition, TripUpdate, StopTimeUpdate, ServiceAlert } from "./types.js";

const BUSTIME_BASE = "https://bustime.ttc.ca/gtfsrt";
const ALERTS_BASE = "https://gtfsrt.ttc.ca";
const USER_AGENT = "ttc-cli (https://github.com/lucasygu/ttc-cli)";

// ─── Error ───────────────────────────────────────────────────────────────────

export class TtcApiError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public url?: string
  ) {
    super(message);
    this.name = "TtcApiError";
  }
}

// ─── Client ──────────────────────────────────────────────────────────────────

export class TtcClient {
  private async fetchFeed(url: string) {
    const res = await fetch(url, {
      headers: { "User-Agent": USER_AGENT },
    });

    if (!res.ok) {
      throw new TtcApiError(
        `Feed request failed: ${res.status} ${res.statusText}`,
        res.status,
        url
      );
    }

    const buffer = await res.arrayBuffer();
    return GtfsRealtimeBindings.transit_realtime.FeedMessage.decode(
      new Uint8Array(buffer)
    );
  }

  // ─── Vehicle Positions ───────────────────────────────────────────────────

  async getVehicles(routeId?: string): Promise<VehiclePosition[]> {
    const feed = await this.fetchFeed(`${BUSTIME_BASE}/vehicles`);
    const vehicles: VehiclePosition[] = [];

    for (const entity of feed.entity) {
      const v = entity.vehicle;
      if (!v?.position) continue;

      const vRouteId = v.trip?.routeId ?? "";
      if (routeId && vRouteId !== routeId) continue;

      vehicles.push({
        vehicleId: v.vehicle?.id ?? "",
        routeId: vRouteId,
        tripId: v.trip?.tripId ?? "",
        latitude: v.position.latitude ?? 0,
        longitude: v.position.longitude ?? 0,
        bearing: v.position.bearing ?? 0,
        speed: v.position.speed ?? 0,
        occupancyStatus: String(v.occupancyStatus ?? "NO_DATA"),
        stopId: v.stopId ?? "",
        currentStopSequence: v.currentStopSequence ?? 0,
        currentStatus: vehicleStopStatusToString(v.currentStatus),
        timestamp: Number(v.timestamp ?? 0),
      });
    }

    return vehicles;
  }

  // ─── Trip Updates (Predictions) ──────────────────────────────────────────

  async getTripUpdates(routeId?: string, stopId?: string): Promise<TripUpdate[]> {
    const feed = await this.fetchFeed(`${BUSTIME_BASE}/trips`);
    const updates: TripUpdate[] = [];

    for (const entity of feed.entity) {
      const tu = entity.tripUpdate;
      if (!tu?.trip) continue;

      const tuRouteId = tu.trip.routeId ?? "";
      if (routeId && tuRouteId !== routeId) continue;

      const stopTimeUpdates: StopTimeUpdate[] = [];
      for (const stu of tu.stopTimeUpdate ?? []) {
        if (stopId && stu.stopId !== stopId) continue;

        stopTimeUpdates.push({
          stopSequence: stu.stopSequence ?? 0,
          stopId: stu.stopId ?? "",
          arrivalTime: stu.arrival?.time ? Number(stu.arrival.time) : null,
          departureTime: stu.departure?.time ? Number(stu.departure.time) : null,
        });
      }

      if (stopId && stopTimeUpdates.length === 0) continue;

      updates.push({
        tripId: tu.trip.tripId ?? "",
        routeId: tuRouteId,
        vehicleId: tu.vehicle?.id ?? "",
        stopTimeUpdates,
        timestamp: Number(tu.timestamp ?? 0),
      });
    }

    return updates;
  }

  async getNextArrivals(stopId: string): Promise<TripUpdate[]> {
    return this.getTripUpdates(undefined, stopId);
  }

  // ─── Service Alerts ──────────────────────────────────────────────────────

  async getAlerts(routeId?: string): Promise<ServiceAlert[]> {
    const feed = await this.fetchFeed(`${BUSTIME_BASE}/alerts`);
    return this.parseAlerts(feed, routeId);
  }

  async getBroadAlerts(routeId?: string): Promise<ServiceAlert[]> {
    const feed = await this.fetchFeed(ALERTS_BASE);
    return this.parseAlerts(feed, routeId);
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  private parseAlerts(feed: any, routeId?: string): ServiceAlert[] {
    const alerts: ServiceAlert[] = [];

    for (const entity of feed.entity) {
      const a = entity.alert;
      if (!a) continue;

      const routeIds: string[] = [];
      for (const ie of a.informedEntity ?? []) {
        if (ie.routeId) routeIds.push(ie.routeId);
      }

      if (routeId && !routeIds.includes(routeId)) continue;

      alerts.push({
        id: entity.id,
        routeIds,
        headerText: extractTranslatedString(a.headerText),
        descriptionText: extractTranslatedString(a.descriptionText),
      });
    }

    return alerts;
  }
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

function vehicleStopStatusToString(status: number | null | undefined): string {
  const map: Record<number, string> = {
    0: "INCOMING_AT",
    1: "STOPPED_AT",
    2: "IN_TRANSIT_TO",
  };
  return map[status ?? 2] ?? "IN_TRANSIT_TO";
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function extractTranslatedString(ts: any): string {
  if (!ts?.translation) return "";
  for (const t of ts.translation) {
    if (t.language === "en" || !t.language) return t.text ?? "";
  }
  return ts.translation[0]?.text ?? "";
}
