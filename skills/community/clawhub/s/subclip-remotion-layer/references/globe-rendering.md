# Globe route visibility and frame capture

## Surface geometry

The default is `arcHeight: 0` in the Cesium component, Motion Graphics template, and `plan_globe_route`. The renderer adds 1 km of clearance to avoid z-fighting. Extra elevation is opt-in; a high arc can remain visible beyond the limb because that part of the route really is above the horizon. Do not diagnose that as an incorrect coordinate or fix it with an overlay mask.

Each geodesic leg is sampled at intervals no greater than 25 km, including every waypoint, so straight GPU segments follow the curved surface without cutting through it. Route reveal uses cumulative route distance and shares its exact endpoint and altitude with the moving marker. Pins and labels keep depth testing enabled; the host also checks ellipsoid line of sight for markers. Preserve occlusion during preview, seeking, and export.

For an old saved map, `update_runtime_layer` with `mergeBindings: true` and `props: {arcHeight: 0}` changes only the elevation. Read its source before refreshing `templateId: "map-explainer"`: a customized source may hardcode its own height and should be adapted in place. Do not change approved routes, timing, colors, camera movement, or a requested white background merely to correct visibility.

## Independent render readiness

The live player and `renderStillOnWeb` use different render contexts. Global `delayRender`/`continueRender` manipulate window state, while the web renderer waits on a per-render scope. The host component must use `useDelayRender()` and `useRemotionEnvironment()` so capture sees initialization, asset loading, errors, and frame-settling handles.

The initialization handle stays pending until React commits the ready tree. That render allocates the requested frame's handle before initialization is released; camera updates and local tile settling clear the frame handle afterward. This prevents a gap in which capture sees no blockers but the DOM still contains `LOADING GLOBE`. Initialization and frame errors cancel the correct scoped render. Cleanup releases only its own task's handles, and stale asynchronous work must not release a newer scene's handle or cancel another render.

Tile settling is bounded by elapsed time, not a fast count of zero-delay timer ticks. Current settling has a 15-second budget, and readiness labels expire before the outer 30-second still-capture budget. A timeout is reported as a concrete failure, never treated as a verified white/blank frame.

## Agent checks

Inspect the source hold, one or more route midpoints, far-side transitions, and the arrival hold. Include repeated destinations and intermediate named stops when validating a multi-leg journey. A still establishes pixels at that time, not real-time playback performance.

If capture shows a loader or blank canvas while the player shows a globe, report that discrepancy and inspect the readiness path. Do not keep replacing map source or alter geography solely because capture is failing. Preserve successful edits, retry after a concrete correction, and leave verification pending if no rendered image is obtained.

Reference: [Remotion scoped render readiness](https://www.remotion.dev/docs/use-delay-render).
