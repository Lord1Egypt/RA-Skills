import { createRoot } from "react-dom/client";

import { MeetingPicker } from "./MeetingPicker";
import type { PlaceProvider } from "./types";
import "./styles.css";

const samples = [
	{
		id: "fixture:river",
		label: "河畔咖啡",
		address: "滨江区江南大道",
		coordinateSystem: null,
		source: "fixture" as const,
	},
	{
		id: "fixture:library",
		label: "城市图书馆",
		address: "西湖区文三路",
		coordinateSystem: null,
		source: "fixture" as const,
	},
];

/** Demonstration data only. Replace with createHTTPPlaceProvider() for a server adapter. */
const provider: PlaceProvider = {
	async search(query, signal) {
		await new Promise<void>((resolve, reject) => {
			const timer = window.setTimeout(resolve, 120);
			signal.addEventListener(
				"abort",
				() => {
					window.clearTimeout(timer);
					reject(new DOMException("Aborted", "AbortError"));
				},
				{ once: true },
			);
		});
		return samples.filter((place) => `${place.label}${place.address}`.includes(query));
	},
};

createRoot(document.getElementById("root")!).render(
	<main className="uf-demo-shell">
		<div className="uf-demo-content">
			<MeetingPicker provider={provider} />
			<p className="uf-demo-note">示例地点 · 仅保存在此设备</p>
		</div>
	</main>,
);
