/** Timezone helpers: derive local calendar date + minutes-since-midnight for an
 *  instant, in a given IANA zone, without pulling in a date library. */

const cache = new Map<string, Intl.DateTimeFormat>();

function fmt(timezone: string): Intl.DateTimeFormat {
  let f = cache.get(timezone);
  if (!f) {
    f = new Intl.DateTimeFormat("en-CA", {
      timeZone: timezone,
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      hour12: false,
    });
    cache.set(timezone, f);
  }
  return f;
}

export interface LocalParts {
  /** YYYY-MM-DD in the target zone. */
  date: string;
  /** Minutes since local midnight in the target zone. */
  minutes: number;
}

export function localParts(iso: string, timezone: string): LocalParts {
  const parts = fmt(timezone).formatToParts(new Date(iso));
  const get = (t: string) => parts.find((p) => p.type === t)?.value ?? "00";
  const hh = Number(get("hour")) % 24; // en-CA may emit "24" at midnight
  const mm = Number(get("minute"));
  return {
    date: `${get("year")}-${get("month")}-${get("day")}`,
    minutes: hh * 60 + mm,
  };
}

/** Parse "HH:MM" into minutes since midnight. */
export function hhmmToMinutes(hhmm: string): number {
  const [h, m] = hhmm.split(":").map(Number);
  return (h ?? 0) * 60 + (m ?? 0);
}
