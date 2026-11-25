---
name: subclip-map-explainer
description: Handle map requests by importing the built-in Remotion Cesium Map explainer or flat River sequence template and customizing verified geography. Route to subclip-hyperframes-map when both built-in styles are rejected or HyperFrames is explicitly requested.
---

# Subclip map explainer

Create an editable map beat inside the current Subclip project. Use Subclip's trusted map components and native layer tools; do not scaffold a Remotion project, install a package, run a framework renderer, or put provider credentials in source or props.

## Choose the map form

Discover the two styles with `list_motion_graphics_templates`, `query: "map"`. `map-explainer` is the Cesium globe; `river-sequence` is a flat vector map, not Cesium. For an unspecified map, default to the Cesium template. Choose the flat template for a river, watershed, or ordered flow. Import the selected template, then edit that returned item. Do not automatically create both maps or stop merely to ask which engine to use.

An exact `@` choice takes priority. If the creator dislikes the selected style, explain the other built-in option briefly. Once both are rejected, load `$subclip-hyperframes-map` and make the requested alternative. A transient render failure alone is not design rejection. Explicit HyperFrames requests can go directly to that skill.

- Use a Remotion layer with `CesiumRouteGlobe` from `@subclip/cesium` when the creator asks for a globe, a city-to-city journey, a world-scale route, an orbital view, or geography that visibly wraps around Earth. Its built-in camera starts on a source-region view, pulls back continuously, holds a stable world view while the route draws, and then closes on the destination region.
- Use the `river-sequence` Remotion template for a flat investigative river, watershed, or ordered geographic flow. It uses Subclip's packaged Natural Earth country topology through `world-atlas/countries-50m.json`, an ordered custom line, SVG country borders/fills, and a vector camera transform. It requires no provider key, network fetch, `staticFile()`, or MapTiler runtime.
- Use `$subclip-map-route` directly only for an explicitly selected legacy flat HTML route or an existing HTML map revision. It is not the default ahead of the two Remotion templates.
- True elevation-terrain and photorealistic city flyovers are unavailable until Subclip provides a managed provider and credential broker. Do not fake terrain with the ellipsoid globe.
- Use native Text and Elements for annotations outside the map component. Keep narration, footage, captions, TTS, music, and SFX in their native Subclip panels.

## Cesium globe workflow

1. Read `$subclip-remotion-layer`, then inspect the current project and concurrent layers.
2. Resolve every named place to verified decimal longitude and latitude. Preserve country/region qualifiers when two places share a name. Do not invent coordinates.
3. Import using `add_runtime_layer`, `kind: "remotion"`, `templateId: "map-explainer"`, and requested timing/geometry. Pass complete verified `origin` and `destination` objects shaped as `{longitude, latitude, label}`, and optional `accent` in props. The Mumbai/London defaults are example content, not a requirement for the user's video.
4. Customize the returned ID with `update_runtime_layer`, `mergeBindings: true`. The current template forwards the globe controls below, including custom points and waypoints. For an older imported version, read `get_runtime_layer` and refresh its source in place with `templateId: "map-explainer"`; this preserves its item ID, timing, layout, and existing props. Inspect custom source before replacement and adapt that source when it contains creator-approved changes. Imported templates are fully editable through source and props, not locked to their initial settings. Import only `CesiumRouteGlobe` from `@subclip/cesium`.
5. Keep map animation frame-derived with Remotion. The trusted component owns WebGL setup, Cesium asset loading, one continuous source/world/destination camera path, great-circle sampling, route visibility, tile settling, and export capture. Do not push the packaged Natural Earth surface into street-level zoom; it is intentionally a regional/world basemap.
6. Keep one intended Remotion item, using a full-canvas rectangle only when the map is the scene background. Preserve its imported ID; do not stack a customized copy over it.
7. Validate source and props before persistence. Inspect the route entrance, midpoint, destination arrival, and final hold in the live canvas.

## Route choice, visibility, and camera

- Call `plan_globe_route` with verified endpoint coordinates. The returned `props` can be passed to `add_runtime_layer` or merged into `update_runtime_layer`; its routePoints show the actual resolved journey before rendering.
- `routeMode: "direct"` uses great-circle legs. A northward arc on a long route may be geographically correct; it is not automatically a routing bug. If the creator requests an ocean/Pacific route or rejects the Arctic view, choose `pacific` and `cameraMode: "follow"` for an Asia-to-western-North-America journey. Choose `atlantic` when that ocean is requested and matches the geography. Do not secretly move the endpoint coordinates to change the arc.
- `waypoints` are ordered intermediate coordinates between origin and destination. Non-empty waypoints override preset corridors. Alternatively supply a complete `points` array, which takes priority over origin/destination. To return to endpoint-based routing, set `points: []`; to return to a preset, also clear old waypoints. Use only meaningful, verified named stops; generated ocean corridor points are editorial control points, not named destinations.
- Pacific/Atlantic corridors are illustrative geographic animations. Delhi is inland: an ocean-facing Delhi-to-San Francisco journey includes land departure/arrival. Do not label it an actual ship route, navigable itinerary, or flight plan without authoritative route data.
- `cameraMode: "follow"` keeps the moving route head in view while Earth rotates beneath it. `overview` holds a route-centered view during travel. Prefer follow when endpoints lie on opposite hemispheres or the creator asks to follow the journey; an overview cannot show both sides of Earth simultaneously.
- `cameraRange` and `closeRange` use meters and can be omitted for automatic aspect-aware framing. `cameraPitch` and `orbitDegrees` use degrees. `startHoldSeconds`, `endHoldSeconds`, `zoomOutSeconds`, and `zoomInSeconds` control the phase durations; oversized holds/zooms are proportionally capped to leave travel time. Adapt zoom to the square/portrait canvas and label clearance rather than copying landscape ranges.
- Appearance controls include `accent`, `background`, `routeWidth`, `arcHeight` (meters), `showLabels`, `showWaypointLabels`, `labelColor`, `labelSize`, and `labelOutlineColor`. Keep waypoint labels off for unlabeled corridor points and use contrasting outlines on light basemaps.
- Far-side markers and labels must be occluded by the globe. Inspect the source hold, ocean midpoint, destination approach, and final hold. A destination label projected over the source hemisphere is a visibility defect, not evidence of wrong longitude. Do not compensate by moving geographic coordinates or adding labels above the globe.
- Default route lines and the moving head to `arcHeight: 0`. The host adds only 1,000 meters of clearance against z-fighting and samples each geodesic leg densely. Never restore the old 650,000-meter template arc or add a hidden 80,000-meter baseline. A high arc can physically appear outside Earth's silhouette without a depth-test bug; use raised arcs only when the creator requests that style. For an existing imported map, merge `props: {arcHeight: 0}` into that same item, preserving every route point, camera setting, duration, and requested background. Refresh older template source if it hardcodes the elevation.
- For multi-stop journeys, use the complete ordered `points` array with `routeMode: "custom"` and `waypoints: []`. Keep repeated non-adjacent destinations when the requested journey returns to them. Do not route the complete itinerary as one origin-to-destination ocean preset or remove intermediate stops to simplify the camera. Enable `showWaypointLabels` for requested named stops, and inspect far-side route segments throughout the journey.
- If a desired control is absent, inspect and update the layer's TSX using `update_runtime_layer`; do not claim an imported template cannot be edited. The host Cesium renderer is still the boundary for GPU setup and depth testing. If capture returns loading/blank pixels, report that exact result and retry only after a concrete correction; saved state alone cannot establish what rendered.

## River sequence workflow

1. Resolve the exact named river or route and obtain one verified, ordered source-to-mouth or start-to-end coordinate line. Simplify only after preserving the meaningful bends and country crossings.
2. Import `river-sequence` through `add_runtime_layer` with `kind: "remotion"` and requested timing. Editable props are `river` (ordered `[longitude, latitude]` pairs), `accent`, and `background`. Focus-country IDs, entry stops, label anchors, and projection are source-defined for the sample region. For another river/region, retrieve this exact template with source included, adapt those constants as well as coordinates, validate, and update the same imported item. Changing only `river` cannot move the sample labels or recenter its projection.
3. Use only `d3-geo`, `topojson-client`, and `world-atlas/countries-50m.json`. Keep the base map and camera as vector SVG so pan/zoom remains sharp and deterministic without a live tile provider.
   World-atlas feature IDs are not guaranteed unique (for example, `036` can occur more than once). When rendering topology features with React, use a composite key such as `${feature.id ?? "unknown"}-${index}` rather than the raw provider ID.
4. Keep route reveal and camera progress separate. The camera may lead or follow the draw, but every phase must remain continuous; never switch projections or reset the map transform mid-shot.
5. Trigger each country border, fill, and label from the verified point where the ordered line enters it. Preserve complete country geometry from the packaged topology and keep labels in the relevant story region.
6. Validate and visually inspect the source, each crossing, the route head, the destination, and the final hold. Record the line's source and effective date in the director brief.

The included Yarlung–Brahmaputra example is a simplified editorial path derived from the referenced sample geometry. It demonstrates sequencing, not authoritative hydrology. Verify or replace it before using it to support a factual claim.

## Authoring boundary

```tsx
import {CesiumRouteGlobe} from '@subclip/cesium';

<CesiumRouteGlobe
  points={[
    {longitude: 72.8777, latitude: 19.076, label: 'MUMBAI'},
    {longitude: -0.1276, latitude: 51.5072, label: 'LONDON'},
  ]}
  accent="#26c9d5"
  arcHeight={0}
  orbitDegrees={8}
/>
```

Never import `cesium`, call `fetch`, set `CESIUM_BASE_URL`, load a tile URL, or add `apiKey`, `token`, authorization, cookie, signed URL, or environment-variable fields. The built-in view uses Apache-2.0 CesiumJS with a token-free packaged Natural Earth surface. Subclip omits the Cesium ion logo because no ion service is used and omits a Natural Earth credit because its public-domain terms make attribution optional. Any future provider-backed surface must preserve that provider's required credits. The built-in view does not promise street-level imagery, photorealistic buildings, or elevation terrain.

## Visual and editorial rules

- Let geography establish before copy explains it. Reveal labels after the corresponding point or route is readable.
- Use sparse, verified waypoints. Intermediate points should express a meaningful route, not approximate a curve with dozens of hand-authored samples.
- Keep labels legible in both landscape and portrait layouts; recompose rather than center-cropping.
- If a future trusted component adds provider data with required attribution, keep those provider credits readable and unobstructed.
- For disputed, historical, proposed, or custom geography, record the source and effective date in the project brief and use verified data rather than the base layer as evidence.

After successful verification, update the project director brief with the places, coordinate source, route meaning, engine, and any provider/data limitations.

## Loading and frame verification

`view_current_frame` mounts a separate composition; the visible player already having a globe does not prove that capture's globe is ready. A blank white frame or `LOADING GLOBE` is not visual verification and does not prove the saved route is missing.

The host must use render-scoped `useDelayRender()` and `useRemotionEnvironment()`, wait for initialization, commit the ready tree, then settle the requested camera frame before capture continues. The previous global readiness calls could let capture return the loading placeholder prematurely. These host synchronization issues cannot be repaired by moving coordinates, replacing the template repeatedly, adding another map, or asking for a map-provider key.

After a concrete source/runtime correction, request the same timestamp once more. If it still fails, report the exact error or returned placeholder and preserve the edit. Do not claim the render is fixed from a successful mutation response. Read `subclip-remotion-layer` resource `references/globe-rendering.md` for the host readiness and occlusion contract.
