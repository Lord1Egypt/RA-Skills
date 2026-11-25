---
name: tonight
description: Plan one night of telescope observing from a CSV of targets (name, ra, dec, optional priority), a site given as coordinates, and a date. It works out each target's observable window (airmass under 2), minimum airmass, best time and Moon separation, and returns a ranked plan with reasons for unobservable targets. Use when asked what is observable tonight, to plan an observing session, rank targets for a night, or find when a target is up from a site. Not for time conversion to BJD_TDB (use bjd), cross-matching catalogues (use epochmatch), or FITS night logs (use fitslog).
license: MIT
compatibility: Requires Python 3.10+ with Astropy and astroplan. Installing needs network access to GitHub; the tool itself runs fully offline (bundled IERS-B data, downloads disabled).
---

# tonight

## What this tool does

tonight builds a ranked observing plan for one night at one site. For
each target in a CSV it computes the window where airmass is under 2,
the minimum airmass and when it occurs, and the Moon separation at that
moment; targets that never get observable are listed separately with a
plain reason. It plans — it does not control a telescope.

## Install

```bash
pip install git+https://github.com/RakTikoo/tonight
```

This provides the `tonight` command.

## Run

```bash
tonight plan targets.csv --site "-31.2733,-70.7033,2300" --date 2026-12-15 --out plan.csv
```

- `targets.csv` has columns `name,ra,dec` plus an optional `priority`.
  RA/Dec may be plain degrees or sexagesimal (RA in hours, Dec in
  degrees).
- `--site` is `"lat,lon,height_m"` — degrees (south/west negative),
  height in metres. Coordinates only; site names are never looked up.
- `--date` is `YYYY-MM-DD` (default: today), anchored in UTC: the plan
  covers the first astronomical night (Sun 18° down) beginning after
  12:00 UTC that day.
- `--out` is optional; a summary is always printed.

## Reading the results

Exit code `0` means a plan was built. The printed summary gives the
night's span, the Moon illumination, then "Observe in this order" — each
target with its window in UTC, its length, best airmass and time, and
Moon separation — then an "Unobservable tonight" list with a reason per
target (for example "never rises above airmass 2 at this site"). A
target being unobservable is a result, not an error. Ranking is by
`priority` first (higher first), then longer observable window, then
lower minimum airmass; if a target has two separate windows in one
night, every window is reported, but the ranking uses the longest
single one. The `--out` CSV carries the same facts per target,
including `window_count` and `total_window_hours`.

All times are UTC, plus a local **solar** time derived from longitude.
tonight has no time-zone database: the local column is mean solar time
and can differ from clock time at the site by an hour or more. Use the
UTC values for anything that must be exact.

Exit code `2` means the request itself was wrong — an unreadable
targets file, unparseable coordinates, a malformed site. The error is
printed as one clean line and no plan was produced.

## Limits

- Planning-grade accuracy: airmass uses the plane-parallel approximation
  on a 5-minute grid; window edges are good to a few minutes, not a
  substitute for mount software at the telescope.
- IERS-B, not IERS-A: Earth-rotation finals need a download, so the
  bundled IERS-B predictions are used (difference well under a second).
- Moon positions come from Astropy's built-in ephemeris
  (arcminute-level), not the JPL tables.
- Ideal horizon: windows assume a flat horizon at altitude 0°, no
  weather, no twilight observing, no telescope limits.
- One night, one site, target list only — no multi-night trips, no
  site-name lookup, no equipment or exposure planning.
- Polar continuous night is reported, not planned: where the Sun stays
  over 18° down all day, the date is reported as a continuous night with
  all targets unobservable. Supported dates: years 1900–2100.
