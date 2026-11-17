import { weatherIcon } from "./weather-presentation.mjs";

const WEATHER_URL = new URL(
  "https://api.open-meteo.com/v1/forecast"
);

const TIMEZONE = "America/Los_Angeles";
const LOCATION = "Los Angeles, California";

const MAX_RESPONSE_BYTES = 128 * 1024;
const TIMEOUT_MS = 15000;

export const WEATHER_CODES = Object.freeze({
  0: "Clear sky",
  1: "Mainly clear",
  2: "Partly cloudy",
  3: "Overcast",
  45: "Fog",
  48: "Depositing rime fog",
  51: "Light drizzle",
  53: "Moderate drizzle",
  55: "Dense drizzle",
  56: "Light freezing drizzle",
  57: "Dense freezing drizzle",
  61: "Slight rain",
  63: "Moderate rain",
  65: "Heavy rain",
  66: "Light freezing rain",
  67: "Heavy freezing rain",
  71: "Slight snow",
  73: "Moderate snow",
  75: "Heavy snow",
  77: "Snow grains",
  80: "Slight rain showers",
  81: "Moderate rain showers",
  82: "Violent rain showers",
  85: "Slight snow showers",
  86: "Heavy snow showers",
  95: "Thunderstorm",
  96: "Thunderstorm with slight hail",
  97: "Heavy thunderstorm",
  99: "Thunderstorm with heavy hail",
});

WEATHER_URL.searchParams.set("latitude", "34.0522");
WEATHER_URL.searchParams.set("longitude", "-118.2437");

WEATHER_URL.searchParams.set(
  "current",
  [
    "temperature_2m",
    "apparent_temperature",
    "relative_humidity_2m",
    "weather_code",
    "wind_speed_10m",
  ].join(",")
);

WEATHER_URL.searchParams.set(
  "daily",
  [
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_probability_max",
    "weather_code",
  ].join(",")
);

WEATHER_URL.searchParams.set(
  "temperature_unit",
  "fahrenheit"
);

WEATHER_URL.searchParams.set(
  "wind_speed_unit",
  "mph"
);

WEATHER_URL.searchParams.set("timezone", TIMEZONE);
WEATHER_URL.searchParams.set("forecast_days", "2");

export const WEATHER_ENDPOINT = WEATHER_URL.toString();

function requiredNumber(value, field) {
  if (
    typeof value !== "number" ||
    !Number.isFinite(value)
  ) {
    throw new Error(`INVALID_${field}`);
  }

  return value;
}

function requiredString(value, field) {
  if (
    typeof value !== "string" ||
    !value.trim()
  ) {
    throw new Error(`INVALID_${field}`);
  }

  return value.trim();
}

function localDateKey(date, timezone = TIMEZONE) {
  if (
    !(date instanceof Date) ||
    !Number.isFinite(date.getTime())
  ) {
    throw new Error("INVALID_EVALUATION_TIME");
  }

  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone: timezone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).formatToParts(date);

  const get = (type) =>
    parts.find((part) => part.type === type)?.value;

  return `${get("year")}-${get("month")}-${get("day")}`;
}

function nextDateKey(dateKey) {
  const [year, month, day] =
    dateKey.split("-").map(Number);

  return new Date(
    Date.UTC(year, month - 1, day + 1)
  ).toISOString().slice(0, 10);
}

function conditionFromCode(code) {
  const numericCode = requiredNumber(
    code,
    "WEATHER_CODE"
  );

  return WEATHER_CODES[numericCode] ??
    "Unknown conditions";
}

function normalizeForecast(data, index) {
  const daily = data.daily;

  return {
    date: requiredString(
      daily.time?.[index],
      "FORECAST_DATE"
    ),

    highF: requiredNumber(
      daily.temperature_2m_max?.[index],
      "HIGH"
    ),

    lowF: requiredNumber(
      daily.temperature_2m_min?.[index],
      "LOW"
    ),

    precipitationProbability: requiredNumber(
      daily.precipitation_probability_max?.[index],
      "PRECIPITATION"
    ),

    condition: conditionFromCode(
      daily.weather_code?.[index]
    ),
    icon: weatherIcon(conditionFromCode(daily.weather_code?.[index])),
  };
}

export function normalizeWeather(
  data,
  now = new Date(),
  { location = LOCATION, timezone = TIMEZONE } = {},
) {
  if (
    !data ||
    typeof data !== "object" ||
    !data.current ||
    !data.daily ||
    !Array.isArray(data.daily.time) ||
    data.daily.time.length < 2
  ) {
    throw new Error("INVALID_WEATHER_RESPONSE");
  }

  if (data.timezone !== timezone) {
    throw new Error("INVALID_WEATHER_TIMEZONE");
  }

  const todayKey = localDateKey(now, timezone);
  const tomorrowKey = nextDateKey(todayKey);

  const today = normalizeForecast(data, 0);
  const tomorrow = normalizeForecast(data, 1);

  if (
    today.date !== todayKey ||
    tomorrow.date !== tomorrowKey
  ) {
    throw new Error("FORECAST_DATE_MISMATCH");
  }

  return {
    status: "ok",
    location,
    timezone,

    current: {
      temperatureF: requiredNumber(
        data.current.temperature_2m,
        "TEMPERATURE"
      ),

      feelsLikeF: requiredNumber(
        data.current.apparent_temperature,
        "FEELS_LIKE"
      ),

      condition: conditionFromCode(
        data.current.weather_code
      ),
      icon: weatherIcon(conditionFromCode(data.current.weather_code)),

      humidity: requiredNumber(
        data.current.relative_humidity_2m,
        "HUMIDITY"
      ),

      windMph: requiredNumber(
        data.current.wind_speed_10m,
        "WIND"
      ),
    },

    today,
    tomorrow,
  };
}

// Shared bounded JSON reader; never follows a provider's arbitrary links.
export async function readWeatherResponse(response) {
  if (!response.ok) {
    throw new Error("WEATHER_HTTP_ERROR");
  }

  const declaredLength =
    response.headers?.get?.("content-length");

  if (
    declaredLength !== null &&
    declaredLength !== undefined &&
    Number(declaredLength) > MAX_RESPONSE_BYTES
  ) {
    throw new Error("WEATHER_RESPONSE_TOO_LARGE");
  }

  let raw;
  const reader = response.body?.getReader?.();

  if (reader) {
    const chunks = [];
    let total = 0;

    try {
      while (true) {
        const { done, value } = await reader.read();

        if (done) break;

        total += value.byteLength;

        if (total > MAX_RESPONSE_BYTES) {
          await reader.cancel();
          throw new Error(
            "WEATHER_RESPONSE_TOO_LARGE"
          );
        }

        chunks.push(value);
      }
    } finally {
      reader.releaseLock();
    }

    raw = Buffer.concat(chunks).toString("utf8");
  } else {
    // Supports injected fetch mocks.
    raw = await response.text();

    if (
      Buffer.byteLength(raw, "utf8") >
      MAX_RESPONSE_BYTES
    ) {
      throw new Error("WEATHER_RESPONSE_TOO_LARGE");
    }
  }

  const data = JSON.parse(raw);

  return data;
}

export async function collectWeather({
  fetcher = fetch,
  now = () => new Date(),
} = {}) {
  try {
    const response = await fetcher(
      WEATHER_ENDPOINT,
      {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
        signal: AbortSignal.timeout(TIMEOUT_MS),
      }
    );

    const data = await readWeatherResponse(response);

    return normalizeWeather(data, now());
  } catch {
    return {
      status: "error",
      error: "WEATHER_UNAVAILABLE",
    };
  }
}
