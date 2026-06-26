# Vela Notes

## Confirmed environment

- Build with `aiot-toolkit` / `npx aiot build`
- Minimum required project files include:
  - `src/app.ux`
  - `src/config-watch.json`
  - `src/manifest.json`
  - page `.ux` files
- Missing `src/app.ux` or `src/config-watch.json` can trigger app-file-missing style errors

## Screen/device notes

- Xiaomi Band 10 is not round; it is a **212x520 跑道屏**
- Design for vertical space and narrow width
- Large buttons and scrollable lists are usually safer than dense dashboard layouts
- Foreground apps are more reliable than background-heavy concepts

## UI guidance

- Prefer dark background + high contrast text for wearable readability
- Home page should not cram too many options in one static block
- Use scrollable list/card layouts when there are multiple entries
- Keep one primary action per screen when possible

## Text/button caveat

- Device rendering may fail for symbolic buttons such as:
  - `↺`
  - `⏸`
  - `▶`
  - `⏭`
- Use plain text labels instead

## Practical lessons from prior work

- A single-page app with `currentView` switching is often fast to build and stable
- But when the menu gets crowded, switch to a scrollable `list`
- Browser/Figma reference lookup is more reliable through the browser tool than scraping attempts

## Sending builds

After successful build, the output package is typically under:
- `dist/<package>.debug.<version>.rpk`
