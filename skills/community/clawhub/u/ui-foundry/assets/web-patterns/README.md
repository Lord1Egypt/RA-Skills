# Web interaction kit

Small runnable meeting-picker product flow for React 19, HeroUI 3 and Tailwind 4. It is a working starting point: local-date selection, keyboard-accessible place search, manual fallback, persistence and edit cancellation. It is not a component catalog or a live map.

```sh
npm ci
npm run verify
npm run dev
```

`demo.tsx` uses offline sample places without coordinates. For production, pass `createHTTPPlaceProvider()` to `MeetingPicker`; it calls the same-origin `POST /api/place-search` contract and forwards cancellation. A provider returns `Place[]` and must honor `AbortSignal` so stale results cannot replace a newer query.

`onSave` runs after browser storage is attempted. It may return a promise for remote sync. The UI reports a remote failure as a sync failure instead of claiming that it saved remotely. Calendar values are stored as local `YYYY-MM-DD` strings, never UTC timestamps.

No API key, map, or live search ships with this kit. Show a map only after the selected provider returns coordinates and coordinate system.
