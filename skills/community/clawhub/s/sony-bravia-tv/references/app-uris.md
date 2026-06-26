# Sony Bravia — Known App URIs

These are pre-mapped in `tv_control.py`. For unlisted apps, the script falls back to `getApplicationList()` and matches by title.

| App | Key (for --app) | URI |
|-----|-----------------|-----|
| Netflix | `netflix` | `com.sony.dtv.com.netflix.ninja.com.netflix.ninja.MainActivity` |
| YouTube | `youtube` | `com.sony.dtv.com.google.android.youtube.tv.com.google.android.apps.youtube.tv.activity.ShellActivity` |
| Hotstar / Disney+ Hotstar | `hotstar` | `com.sony.dtv.in.startv.hotstar.in.startv.hotstar.MainActivity` |
| Prime Video | `prime` | `com.sony.dtv.com.amazon.avod.com.amazon.avod.MainActivity` |

## How to find URIs for other apps

Run:
```bash
uv run ~/openclaw-skills/sony-tv/scripts/tv_control.py --action list_apps
```

This calls `getApplicationList()` on the TV and prints all installed apps with their URIs. Add frequently used ones to the `KNOWN_APPS` dict in `tv_control.py`.
