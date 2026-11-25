import { useEffect, useRef, useState } from "react";

import type { Place, PlaceProvider } from "./types";

export type PlaceSearchState = {
	status: "idle" | "loading" | "ready" | "empty" | "error";
	results: Place[];
	error: Error | null;
	retry(): void;
};

/** Debounced, abortable search. A sequence number also guards providers that ignore aborts. */
export function usePlaceSearch(
	query: string,
	provider: PlaceProvider,
	delay = 180,
): PlaceSearchState {
	const [attempt, setAttempt] = useState(0);
	const [state, setState] = useState<Omit<PlaceSearchState, "retry"> & { query: string }>({
		query: "",
		status: "idle",
		results: [],
		error: null,
	});
	const request = useRef(0);

	useEffect(() => {
		const value = query.trim();
		if (!value) {
			setState({ query: value, status: "idle", results: [], error: null });
			return;
		}

		const controller = new AbortController();
		const sequence = ++request.current;
		// Never leave an old result list actionable while debounce is pending.
		setState({ query: value, status: "loading", results: [], error: null });
		const timer = window.setTimeout(async () => {
			try {
				const results = await provider.search(value, controller.signal);
				if (sequence !== request.current || controller.signal.aborted) return;
				setState({
					query: value,
					status: results.length ? "ready" : "empty",
					results,
					error: null,
				});
			} catch (reason) {
				if (sequence !== request.current || controller.signal.aborted) return;
				setState({
					query: value,
					status: "error",
					results: [],
					error: reason instanceof Error ? reason : new Error("Place search failed"),
				});
			}
		}, delay);

		return () => {
			window.clearTimeout(timer);
			controller.abort();
		};
	}, [attempt, delay, provider, query]);

	// Mask stale results during render, before the effect for a new query runs.
	const current =
		state.query === query.trim()
			? state
			: {
					status: query.trim() ? ("loading" as const) : ("idle" as const),
					results: [],
					error: null,
				};
	return { ...current, retry: () => setAttempt((value) => value + 1) };
}
