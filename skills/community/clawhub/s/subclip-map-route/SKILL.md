---
name: subclip-map-route
description: Revise existing Subclip flat HTML routes or build one when that legacy workflow is explicitly requested. General map requests start with subclip-map-explainer and its two built-in Remotion templates.
---

# Subclip map route

For a new map without an explicit legacy HTML choice, read `$subclip-map-explainer` and import the Cesium `map-explainer` or flat `river-sequence` template first. When the creator dislikes both styles, use `$subclip-hyperframes-map`. The HTML workflow below remains available for existing maps or an explicit choice; its geometry tool can also supply SVG paths for the HyperFrames alternative.

Build route maps from bundled geographic geometry. Do not search stock-media catalogs for ordinary world maps, download an external map, hand-draw continents, or fall back to a photographed map.

## Direct workflow

1. Resolve the origin and destination to verified decimal latitude/longitude. If only place names are supplied, use one authoritative lookup; preserve the country/region qualifiers and correct an obvious spelling only when the intended place is unambiguous.
2. Call `create_route_map_geometry` with both labels and coordinates. It returns:
   - a fixed, familiar Greenwich-centered Natural Earth map with the Americas on the left and Asia on the right;
   - one continuous route, coordinate-bound pins, destination shockwaves, and a seek-safe camera as ready Motion Graphics `html` and `css`;
   - calculated displayed-route distance, a rounded `metricLabel`, editorial Text timing, and camera-phase metadata;
   - `continuous: true` and `routeSubpathCount: 1` proof.
3. Add exactly one full-canvas Motion Graphics item with the returned HTML/CSS. Do not rewrite its map or route paths. When correcting an existing route scene, update that exact Motion Graphics item in place instead of adding a duplicate.
4. Keep coordinate-bound pins and shockwaves inside the returned Motion item so they inherit the same camera transform as the map and route. Do not recreate them as separate Elements that drift during zoom/pan.
5. Add place names and the metric as native Text only at the phases returned in `nativeTextPlan`: origin during the source close-up, metric during world reveal/route travel, and destination during the final close-up. When correcting an existing scene, update its existing labels instead of stacking replacements.
6. Use Media only when the creator supplies a specific styled/satellite map or asks to show real map imagery; bundled Natural Earth geometry is the default base.
7. Inspect the source close-up, full-world reveal, route midpoint, destination landing, and final hold. Verify familiar map orientation, label clearance, continuous camera velocity, and exact final focus.

## Continuous-route invariant

The displayed route must be one continuous visual stroke on the familiar standard world map.

- Do not rotate or recenter the full world to hide a seam. Keep the Greenwich-centered orientation: Americas left, Europe/Africa centered, Asia right.
- With `routeDirection: auto-visible` (the default), use the shortest great-circle route when it stays inside the standard map. When that route would split at an edge, use the tool's designed continuous interior arc; for Delhi→San Francisco this travels westward across the familiar map instead of moving Asia to the left.
- Use `routeDirection: longest` only when the creator explicitly requests the literal long great-circle route. A designed interior arc reports its own displayed distance and clearly identifies that basis; never label it as an airline itinerary.
- Require `continuous: true` and `routeSubpathCount: 1` before adding the Motion Graphics item.
- Never show two disconnected edge arcs, and never change the world orientation merely to make the shortest route continuous.

## Camera invariant

Map, route, and markers share one camera/world wrapper, following the same principle used by HyperFrames camera keyframes and Remotion map compositions. Do not animate the map separately from geographic markers.

The default eight-second pose ladder is:

1. Close on the source and hold long enough to establish it.
2. Ease out to the full standard world map.
3. Draw and follow the route with one uninterrupted world-to-destination transform segment—no intermediate waypoint poses.
4. Land the destination pin and triple shockwave while that same camera interval continues—no stop at landing.
5. Let the uninterrupted journey resolve into the destination close-up, then hold the final frame.

Use the returned HTML/CSS unchanged so the CSS timeline remains seek-safe in preview and export. Native Text is editorial overlay, not part of the geographic camera.

## Prepared camera corrections

`create_route_map_geometry` returns `cameraEditor.css`, marker comments, tuning inputs, and the complete `motionGraphic.css`. The default `continuous-journey-v2` camera deliberately has only these transform states: source hold, full-world reveal, destination close-up, final hold. Route draw completion, pin landing, and shockwaves are timed events inside the world-to-destination camera interval; they are not camera keyframes. It uses `translate3d`, no SVG blur, zero direction reversals, and no eased waypoint chain.

When revising an existing route:

1. Re-call `create_route_map_geometry` with `outputMode: camera-only` plus the same coordinates, route direction, scene duration, and route duration. Adjust only `cameraSourceScale`, `cameraDestinationScale`, or `cameraDestinationPushDuration`. The small response intentionally omits the unchanged world paths.
2. Update the same Motion item. Prefer the complete regenerated `motionGraphic.css`; if preserving unrelated creator CSS, replace only the block between `SUBCLIP_ROUTE_CAMERA_START` and `SUBCLIP_ROUTE_CAMERA_END` with `cameraEditor.css`. Do not rewrite the giant land/route paths or add another map item.
3. If the opening zoom is approved, keep its scale and timing unchanged. Tune close-up strength with `cameraDestinationScale`; tune how long the uninterrupted journey continues after pin landing with `cameraDestinationPushDuration`. Do not add camera poses.
4. A jerk in the route or landing means there is an extra transform stop, easing boundary, or direction reversal. Remove it. The `routeAndDestinationJourney` contract is `transformPoseCount: 2`, `directionReversals: 0`, and `transformBoundaryAtPinLanding: false` from full-world reveal through final destination framing.
5. Do not add CSS/SVG blur to disguise motion. It increases editor cost and does not repair velocity.

Still-frame inspection proves framing and positional continuity, not real-time playback frame rate. Check dense frames around each actual camera boundary—not the pin event—then describe playback smoothness as creator-preview-dependent unless the moving preview itself was observed.

Subclip's HTML-motion renderer must seek stable CSS `Animation` objects through the Web Animations timeline. It must not simulate time by overriding `animation-delay`, because that discards authored route/pin/shockwave delays and can force per-frame animation restarts. A route result with `authoredAnimationDelaysRequired: true` assumes this engine contract.
