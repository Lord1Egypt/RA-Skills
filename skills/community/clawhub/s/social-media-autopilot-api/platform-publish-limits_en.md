# Platform publish limits: copy, media, and formats (reference)

This article summarizes the **text, media counts, file formats, and dimensions** enforced by SocialEcho when you publish through the **Publish API / publish flows** to each social network. Use it to prepare assets in advance for engineering and operations.

> **Notes**
>
> - Limits below reflect the rules embedded in the current product. **Official platform policies may change at any time.** If anything disagrees with the platform console or an error message from a failed publish, **follow the platform and the live in-product message.**
> - **Portrait / vertical** means recommended or required **vertical assets** (typically **width less than height**). See each section for details.

---

## Glossary

| Term | Meaning |
| --- | --- |
| Body length | Maximum length of the main text (including spaces, per system validation). |
| Title length | Character limit for the title; “no fixed cap” means no separate hard limit in this table (platform rules may still apply). |
| Media counts | How many images / GIFs / videos a single publish may include, and combined rules. |
| Mixed media rules | Whether multiple media types may be combined, and which combinations are forbidden. |
| Text-only | Whether a publish **without** any image, video, or GIF is allowed. |
| Category / placement ID required | Whether you must pick a platform-side category or placement (e.g. Pinterest board, Reddit community). |
| Portrait required | Whether vertical (portrait) creative is required (**width &lt; height**). |

---

## Facebook

### Regular feed (`post`, etc.)

| Field | Limit |
| --- | --- |
| Body length | Max **2200** characters |
| Title length | No fixed cap in this table |
| Minimum title / body | No fixed minimum |
| Media counts | Images up to **10**; GIFs up to **1**; videos up to **1**; total attachments uncapped |
| Mixed media | Image + GIF **not** allowed; image + video **not** allowed |
| Text-only | **Allowed** |
| Image formats | jpg / jpeg / png / gif |
| Video formats | mp4 / mov |
| Image file size | Static **8MB**; GIF **8MB** |
| Video file size | Max **1GB** |
| Video duration | **1s–20 minutes** |
| Video resolution | No fixed limit |
| Image resolution | No fixed limit |
| Frame rate | **23–60** fps |
| Aspect ratio (video/image) | No fixed limit |
| Comment length | No fixed cap in this table |
| Category / placement ID | **No** |
| Portrait required | **No** |

### Reels

| Field | Limit |
| --- | --- |
| Body length | Max **2200** characters |
| Title length | No fixed cap in this table |
| Minimum title / body | No fixed minimum |
| Media counts | **Video only, 1 file** (0 images, 0 GIFs, **1** media item total) |
| Mixed media | Image + GIF not allowed; image + video not allowed |
| Text-only | **Not** allowed (video required) |
| Image formats | N/A (video only) |
| Video formats | mp4 / mov |
| Video file size | Max **1GB** |
| Video duration | **3s–90s** |
| Video resolution | Width **≥ 540**, height **≥ 960** |
| Frame rate | **23–60** fps |
| Aspect ratio | No fixed limit |
| Comment length | No fixed cap in this table |
| Category / placement ID | **No** |
| Portrait required | **Yes** |

---

## X (formerly Twitter)

| Field | Limit |
| --- | --- |
| Body length | Max **280** characters |
| Title length | No fixed cap in this table |
| Minimum title / body | No fixed minimum |
| Media counts | Images up to **4**; GIFs up to **1**; videos up to **4**; **max 4 media items total** |
| Mixed media | Image + GIF **not** allowed; image + video **allowed** |
| Text-only | **Allowed** |
| Image formats | jpg / jpeg / png / gif |
| Video formats | mp4 / mov |
| Image file size | Static **5MB**; GIF **15MB** |
| Video file size | Max **512MB** |
| Video duration | **0.5s–140s** |
| Video resolution | Width **≥ 32**, height **≥ 32** |
| Image resolution | Width **4–8192**, height **4–8192** |
| Frame rate | **23–60** fps |
| Video aspect ratio | **0.333–3** |
| Image aspect ratio | No fixed limit |
| Comment length | No fixed cap in this table |
| Category / placement ID | **No** |
| Portrait required | **No** |

---

## Instagram

| Field | Limit |
| --- | --- |
| Body length | Max **2200** characters |
| Title length | No fixed cap in this table |
| Minimum title / body | No fixed minimum |
| Media counts | Images up to **10**; videos up to **1**; GIFs **0**; total uncapped |
| Mixed media | Image + GIF not allowed; image + video not allowed |
| Text-only | **Not** allowed (media required) |
| Image formats | jpg / jpeg / png |
| Video formats | mp4 |
| Image file size | Static **8MB**; GIF **8MB** per rules |
| Video file size | Max **300MB** |
| Video duration | **3s–15 minutes** |
| Video resolution | Width **1–1920**, height unrestricted |
| Image resolution | Width **320–1440**, height unrestricted |
| Frame rate | **23–60** fps |
| Video aspect ratio | **0.01–10** |
| Image aspect ratio | **0.8–1.91** |
| Comment length | No fixed cap in this table |
| Category / placement ID | **No** |
| Portrait required | **No** |

---

## LinkedIn

| Field | Limit |
| --- | --- |
| Body length | Max **3000** characters |
| Title length | No fixed cap in this table |
| Minimum title / body | No fixed minimum |
| Media counts | Images up to **20**; GIFs up to **20**; images+GIFs combined up to **20**; videos up to **1**; total uncapped |
| Mixed media | Image + GIF **allowed**; image + video **not** allowed |
| Text-only | **Allowed** |
| Image formats | jpg / png / gif |
| Video formats | mp4 |
| Image file size | Static **5MB**; GIF **8MB** |
| Video file size | Max **500MB** |
| Video duration | **3s–10 minutes** |
| Video resolution | Width **1–4096**, height **1–2304** |
| Image resolution | No fixed limit |
| Frame rate | **10–60** fps |
| Video aspect ratio | **0.416–2.4** |
| Image aspect ratio | No fixed limit |
| Comment length | No fixed cap in this table |
| Category / placement ID | **No** |
| Portrait required | **No** |

---

## TikTok

| Field | Limit |
| --- | --- |
| Body length | Max **4000** characters |
| Title length | No fixed cap in this table |
| Minimum title / body | No fixed minimum |
| Media counts | Videos up to **1**; images up to **35**; GIFs **0**; total uncapped |
| Mixed media | Image + GIF not allowed; image + video not allowed |
| Text-only | **Not** allowed (media required) |
| Image formats | jpg / jpeg / webp |
| Video formats | mp4 / mov |
| Image file size | Static **20MB**; **GIF not supported** |
| Video file size | Max **1GB** |
| Video duration | **3s–10 minutes** |
| Video resolution | Width **≥ 360**, height **≥ 360** |
| Image resolution | No fixed limit |
| Frame rate | **23–60** fps |
| Aspect ratio (video/image) | No fixed limit |
| Comment length | Max **150** characters |
| Category / placement ID | **No** |
| Portrait required | **No** |

---

## YouTube

### Regular long-form video (`video`)

| Field | Limit |
| --- | --- |
| Body length | Max **5000** characters |
| Title length | **1–100** characters |
| Minimum body | **At least 1** character |
| Media counts | **Video only, 1 file** (0 images, 0 GIFs) |
| Mixed media | Image + GIF not allowed; image + video not allowed |
| Text-only | **Not** allowed (video required) |
| Video formats | mp4 / mov |
| Video file size | Max **2GB** |
| Video duration | **1s–12 hours** |
| Video resolution | No fixed limit |
| Frame rate | No fixed limit |
| Aspect ratio | No fixed limit |
| Comment length | No fixed cap in this table |
| Category / placement ID | **No** |
| Portrait required | **No** |

### Shorts

| Field | Limit |
| --- | --- |
| Body length | Max **5000** characters |
| Title length | **1–100** characters |
| Minimum body | **At least 1** character |
| Media counts | Video only, **1** file |
| Mixed media | Same as long-form |
| Text-only | **Not** allowed (video required) |
| Video formats | mp4 / mov |
| Video file size | Max **2GB** |
| Video duration | **1s–60s** |
| Video resolution | Width **≥ 480**, height **≥ 480** |
| Frame rate | No fixed limit |
| Aspect ratio | No fixed limit |
| Comment length | No fixed cap in this table |
| Category / placement ID | **No** |
| Portrait required | **Yes** |

---

## Pinterest

| Field | Limit |
| --- | --- |
| Body length | Max **500** characters |
| Title length | Max **100** characters |
| Minimum title / body | No fixed minimum |
| Media counts | Images up to **1**; GIFs up to **1**; videos up to **1**; use one type per publish (mutually exclusive) |
| Mixed media | Image + GIF not allowed; image + video not allowed |
| Text-only | **Not** allowed (media required) |
| Image formats | jpg / jpeg / png |
| Video formats | mp4 |
| Image file size | Static **20MB**; GIF no fixed cap in this table |
| Video file size | Max **2GB** |
| Video duration | **4s–15 minutes** |
| Video resolution | No fixed limit |
| Image resolution | Width **≥ 200**, height **≥ 300** |
| Frame rate | No fixed limit |
| Aspect ratio | No fixed limit |
| Comment length | No fixed cap in this table |
| Category / placement ID | **Yes** (e.g. board selection) |
| Portrait required | **No** |

---

## Document meta

- **Source**: Internal rules doc *Platform limits*, edited for help center use.
- **Use**: Help center, integration guides, and creative/production checklists.
- **Maintenance**: Update this file when product rules change, and re-validate against the live publish pipeline.
