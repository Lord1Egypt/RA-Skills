// Presentation only: select an icon from the reported condition, never infer
// weather from temperature or precipitation probability.
export function weatherIcon(condition) {
  const text = typeof condition === "string" ? condition.toLowerCase() : "";
  if (/thunderstorm/.test(text)) return "⛈️";
  if (/snow|snow grains/.test(text)) return "❄️";
  if (/fog/.test(text)) return "🌫️";
  if (/drizzle/.test(text)) return "🌦️";
  if (/rain|showers/.test(text)) return "🌧️";
  if (/partly cloudy/.test(text)) return "⛅";
  if (/overcast|cloudy/.test(text)) return "☁️";
  if (/mainly clear/.test(text)) return "🌤️";
  if (/clear sky|^clear$/.test(text)) return "☀️";
  return "🌡️";
}
