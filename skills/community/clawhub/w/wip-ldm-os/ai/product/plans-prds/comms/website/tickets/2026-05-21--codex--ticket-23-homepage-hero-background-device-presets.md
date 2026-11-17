# Ticket 23: Homepage hero background desktop and mobile presets

**Date:** 2026-05-21
**Filed by:** Codex, with Parker
**Status:** open. Ready for implementation.
**Master:** `ai/product/plans-prds/comms/website/tickets/website-launch-masterticket.md`
**Surface:** `repos/wip-web/wip-computer-website/static/wip-websites-private/wip.computer/index.html`, `repos/wip-web/wip-computer-website/static/wip-websites-private/wip.computer/app.js`, and only if required `repos/wip-web/wip-computer-website/static/wip-websites-private/wip.computer/styles.css`

## Summary

The homepage hero background currently starts from a random Bucky image preset. Parker wants the first load to be intentional and device-specific, because the same coordinates do not frame correctly on desktop and mobile.

This ticket is only about preset selection. The existing Bucky coordinate system already worked and must remain the contract.

Do not change how coordinates render. Do not change the transform math, image scale, drift/parallax behavior, CSS canvas size, hero layout, or readout logic. All saved desktop coordinates must continue to render exactly as they did before this ticket.

Change the homepage Bucky preset selection from "random on load, slow random changes later" to:

1. Desktop first load always uses the approved desktop preset.
2. Mobile first load always uses the approved mobile preset.
3. After first load, keep the randomizer behavior, but make it cycle every 15 seconds.
4. Split the preset pool into two buckets: desktop presets and mobile presets.
5. Use the current existing preset sequence as the desktop bucket for now.
6. Seed the mobile bucket with the same current preset sequence as desktop for now, except the mobile first-load preset is the approved mobile coordinate. Parker will provide 5 to 10 true mobile coordinates later.

## Approved First-Load Presets

Use these exact starting presets from Parker's screenshots:

Desktop:

```js
{ img: 1, rot: 0, y: 0, dx: -90, dy: 294 }
```

Mobile:

```js
{ img: 1, rot: 0, y: 0, dx: -70, dy: 145 }
```

If the existing code stores image indexes as zero-based internally, adapt these carefully so the visible debug readout still shows `I1`.

## Desired Behavior

On desktop:

- First paint loads the desktop preset above.
- The visible debug/readout state, if enabled, reads `img I1`, `rot 0deg`, `y 0%`, `dx -90`, `dy 294`.
- After 15 seconds, the background fades to another preset from the desktop preset bucket.
- The desktop bucket starts with the current existing preset list.
- Existing desktop presets must not require recalibration. If an old desktop preset looked right before this ticket, it must still look right after this ticket.

On mobile:

- First paint loads the mobile preset above.
- The visible debug/readout state, if enabled, reads `img I1`, `rot 0deg`, `y 0%`, `dx -70`, `dy 145`.
- After 15 seconds, the background fades to another preset from the mobile preset bucket.
- For now, the mobile bucket uses the same current preset sequence as desktop after the first load. Do not invent new mobile coordinates and do not adapt desktop coordinates. Parker will provide a real mobile bucket later.

Across both:

- Preserve the existing Bucky background image set.
- Preserve the existing manual debug/readout interaction.
- Preserve the existing coordinate/render contract exactly: same `img`, `rot`, `y`, `dx`, and `dy` must produce the same visual placement as before this ticket.
- Preserve existing image scale, CSS sizing, drift/parallax behavior, transform math, and render timing except for the requested 15-second preset transition interval.
- Preserve the homepage layout, hero copy, CTA copy, footer, header, and scroll behavior.
- Do not touch login, demo, legal pages, live wall, auth, wallet, WebAuthn, QR login, image generation, Remote Control, relay, daemon, E2EE, API keys, or deploy scripts.

## Implementation Notes

- Add a device classifier for the hero background preset pool. Use the same practical breakpoint style as the footer passkey work unless the website already has a better homepage-specific breakpoint.
- Split the current `BUCKY_PRESETS` into desktop and mobile buckets.
- The split must be a selection-layer change only. Start from the old working Bucky system and add bucket selection around it.
- Choose the first preset deterministically from the active bucket.
- Subsequent transitions should choose from the active bucket and avoid immediately repeating the current preset when the bucket has more than one option.
- Change the automatic transition interval to 15 seconds.
- Fade between presets. If the current implementation already fades out then fades in, keep that mechanism and only adjust timing and bucket selection.
- Do not remove drift, do not change `160vmax`, do not change the image box, and do not compensate by editing coordinates. Those are not fixes for this ticket.
- If the first-load preset does not visually match the reference, investigate why the old coordinate contract changed. Do not solve it by creating a new coordinate system.

## Acceptance Criteria

- Desktop first load starts on `{ img: 1, rot: 0, y: 0, dx: -90, dy: 294 }`.
- Mobile first load starts on `{ img: 1, rot: 0, y: 0, dx: -70, dy: 145 }`.
- Desktop and mobile use separate preset buckets.
- The current desktop preset sequence is preserved as the desktop bucket.
- The mobile bucket exists and initially uses the same current preset sequence as desktop after the first-load mobile preset.
- The automatic background transition interval is 15 seconds.
- Transitions fade between presets rather than snapping.
- Manual debug/readout controls still work.
- Existing desktop coordinates render exactly as they did before this ticket.
- Same `img`, `rot`, `y`, `dx`, and `dy` values always produce the same visual placement under the old coordinate system.
- No hidden offset, scale, transform, CSS canvas, drift, or parallax change is introduced.
- No homepage copy changes.
- No CTA/header/footer changes.
- No non-homepage surfaces changed.
- Run `node --check wip.computer/app.js`.
- Run a focused desktop and mobile local verification of the first-load preset.
- Run a focused regression check proving the same preset produces the same rendered CSS transform/state as the old path.
- Run `git diff --check`.

## Out of Scope

- New mobile coordinate design beyond the one approved mobile preset.
- Any coordinate-system redesign.
- Any image scale, drift, parallax, transform, or CSS canvas-size change.
- Changing the hero headline or body copy.
- Changing the blue CTA.
- Changing the readout design.
- Changing the live wall visualization page.
- Changing the Kaleidoscope login/demo flow.
- Any deploy work.
