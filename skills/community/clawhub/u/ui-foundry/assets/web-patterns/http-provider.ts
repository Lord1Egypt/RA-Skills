import type { Place, PlaceProvider } from "./types";

type HTTPPlaceProviderOptions = { endpoint?: string; city?: string; limit?: number };

/**
 * Same-origin adapter for assets/place-service/route-handler.mjs.
 * It sends no request until a user searches and forwards AbortSignal unchanged.
 */
export function createHTTPPlaceProvider({
	endpoint = "/api/place-search",
	city,
	limit = 8,
}: HTTPPlaceProviderOptions = {}): PlaceProvider {
	return {
		async search(query: string, signal: AbortSignal): Promise<Place[]> {
			const response = await fetch(endpoint, {
				method: "POST",
				headers: { "content-type": "application/json" },
				body: JSON.stringify({ query, city, limit }),
				signal,
			});
			const payload: unknown = await response.json().catch(() => null);
			if (
				!response.ok ||
				!payload ||
				typeof payload !== "object" ||
				!("places" in payload) ||
				!Array.isArray(payload.places)
			) {
				const message =
					payload &&
					typeof payload === "object" &&
					"error" in payload &&
					typeof payload.error === "string"
						? payload.error
						: "Place search failed";
				throw new Error(message);
			}
			return payload.places as Place[];
		},
	};
}
