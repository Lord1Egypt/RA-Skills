---
name: expo-image
description: Use expo-image for performant image loading, caching, placeholders (BlurHash/ThumbHash), and contentFit.
---

# expo-image

**expo-image** is a cross-platform image component with caching, placeholders, and smooth transitions. Prefer it over React Native's default `Image` when you need performance, disk/memory cache, or BlurHash/ThumbHash placeholders.

## Usage

```bash
npx expo install expo-image
```

```jsx
import { Image } from 'expo-image';

<Image
  source="https://example.com/photo.jpg"
  style={{ width: 200, height: 200 }}
  contentFit="cover"
  placeholder={{ blurhash: '|rF?hV%2WCj[ayj[a|j[az_NaeWBj@ayfRayfQfQM{M|azj[azf6fQfQfQIpWXofj[ayj[j[fQayWCoeoeaya}j[ayfQa{oLj?j[WVj[ayayj[fQoff7azay' }}
  transition={200}
/>
```

**Props:** `source` (URI or require), `contentFit` (`cover` | `contain` | `fill` | etc.), `contentPosition`, `placeholder` (blurhash string or `{ blurhash }` / thumbhash), `transition` (ms), `cachePolicy` (`memory` | `disk` | `memory-disk` | `none`).

## Key points

- **Caching:** Disk and memory caching are built in; use `cachePolicy` if you need to avoid cache (e.g. auth headers or one-time URLs).
- **Placeholders:** BlurHash or ThumbHash reduce layout shift; can be generated server-side and stored with image metadata.
- **Config plugin:** Optional. Use the `expo-image` plugin in app config to set options like `disableLibdav1d` (iOS) if another native lib conflicts with AVIF.
- **Formats:** Supports WebP, PNG, APNG, AVIF, HEIC (iOS), JPEG, GIF, SVG; platform support differs (e.g. HEIC not on web).

<!--
Source references:
- https://docs.expo.dev/versions/latest/sdk/image/
-->
