# Image rights audit (before launch)

Every image an app ships must have a known source and a right to use it. Do this as an audit before launch and again when images are added. Change nothing until the student has seen the list.

## 1. Inventory

List every image: files in `public/`, `src/**/assets`, images in the database or storage bucket that the app (not its users) put there, seed/demo data, OG images, screenshots in the store listing. For each, record:

| File | Where it is used | Source | Licence / proof | Shows a real person? |
|---|---|---|---|---|

Source is one of: **own** (the student made or photographed it), **stock** (Unsplash, Pexels, a paid library...), **generated** (an AI image tool; note which and its terms), **user upload** (covered by the terms of service), or **unknown**.

## 2. Fix unknown ones

- Treat **unknown as not allowed**. Replace it with licensed stock, a generated image, or the student's own.
- **Real people's faces come first**: a stranger's photo raises copyright and privacy/likeness rights (and in dating, social or review apps, impersonation). Replace with generated people or properly licensed stock with a model release.
- Logos and screenshots of other brands: only as allowed by that brand's guidelines.
- Do not trust "found on Google" or "free wallpaper" sites as a licence.

## 3. Keep a licence log

Commit the table as `IMAGE-SOURCES.md` (or `docs/image-sources.md`) in the app: one row per image with source URL, author, licence name and link, date downloaded. Add a row whenever an image is added. `verify` warns when an app ships images in `public/` without this log.
