import type { Campus, ZhuhaiStationKey } from "./routes.js";
import type { ApiSchedule, NormalizedSchedule, ScheduleStatus } from "./types.js";

export function normalizeSchedule(
  raw: ApiSchedule,
  startCampus: Campus,
  toCampus: Campus,
  zhuhaiStation: ZhuhaiStationKey,
): NormalizedSchedule {
  const firstEnd = raw.endStations[0];
  return {
    startCampus,
    toCampus,
    zhuhaiStation,
    lineTime: raw.startTime,
    boardingTime: raw.startStation.departureTime || raw.startTime,
    arrivalTime: firstEnd?.departureTime || "",
    fromStation: raw.startStation.station,
    toStation: firstEnd?.station || "",
    price: raw.price,
    remain: raw.stockAmount ?? raw.carSeat ?? null,
    direct: detectDirect(raw),
    status: getStatus(raw),
    raw,
  };
}

function detectDirect(raw: ApiSchedule): boolean | null {
  if (Array.isArray(raw.lineTagsList)) {
    return raw.lineTagsList.some((tag) => tag.desc === "直达");
  }
  if (typeof raw.lineTags === "string" && raw.lineTags.includes("直达")) return true;
  if (raw.lineTags === "") return false;
  return null;
}

function getStatus(raw: ApiSchedule): ScheduleStatus {
  if (raw.expired !== 0) return "expired";
  if (raw.soldOut || raw.stockAmount === 0) return "sold-out";
  return "available";
}
