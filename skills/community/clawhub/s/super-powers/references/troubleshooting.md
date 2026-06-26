# Troubleshooting

## npm install fails

The helper script automatically retries with a temp npm cache. If npm still fails, check:
- network access
- npm permissions
- whether `node` and `npm` are installed

The package is installed locally under:

```text
.superpowers/npm
```

## Login fails

If the code was accepted but the package still says login failed, rerun:

```bash
node scripts/install_and_run.js
```

If it keeps failing, the package and backend may be out of sync.

## Stream does not appear

### `Room full`

The package reached signaling, but the selected room already has both sides attached.

### `Room not found`

The streamer is retrying a room that the host page has not opened yet, or the control link was opened under the wrong account or room.

### `fetch failed`

Check network access and whether the machine can reach the API.

## macOS runtime problems

### `Library not loaded: @rpath/WebRTC.framework/WebRTC`

The packaged Mac runtime is broken. Reinstall the npm package and retry.

```bash
node scripts/install_and_run.js --install-only
node scripts/install_and_run.js --start
```

### Permissions

If the streamer launches but no capture appears, check Screen Recording and Accessibility permissions in macOS settings.
