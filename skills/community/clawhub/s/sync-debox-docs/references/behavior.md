# Behavior Reference

## Current Documentation Definition

Current documentation means pages linked by the visible documentation sidebar on:

- Chinese: `https://docs.debox.pro/UserGuide`
- English: `https://docs.debox.pro/en/UserGuide`

The script does not use GitHub, `/sitemap.xml`, guessed URLs, or hidden routes.

## First And Later Runs

On the first run, no manifest exists, so all current pages and images are written locally.
Later runs compare content hashes with `manifest.json` and report additions, changes, and
removals.

When image understanding is selected for the first time, every current image is analyzed.
Later image-enabled runs compare `manifest.json` with `image-notes.json`, analyze only new or
changed images and images previously marked unreadable, reuse unchanged successful analysis,
and remove analysis for images no longer present.

When image understanding is not selected, images are still downloaded, but existing image
notes are not modified and the run must be reported as text-only analysis.

Image analysis is a separate best-effort stage after synchronization. It uses small batches,
preserves results after each completed batch, and retries each failed image once with a smaller
batch or individual inspection. A failed image-analysis stage does not invalidate a successful
document sync.

When the image tool cannot read synchronized image paths, the agent may copy only the selected
images to an accessible temporary directory. Records still refer to the synchronized originals,
which are never modified by image analysis.

An unreadable image record is retried on the next image-enabled run. If changed-image analysis
fails, its prior successful record is retained with its prior hash, causing another retry on the
next run. Incomplete image analysis must be reported as incomplete and cannot support a claim
that no image-text conflicts exist.

## Safety

The script refuses a non-empty output folder that has no DeBox sync marker. This prevents it
from treating an unrelated folder as its managed documentation folder.

The selected language is stored in the marker and manifest. Reusing the same folder with a
different language is refused.

Pages and images are downloaded into a temporary staging directory. Files are validated before
they replace managed local files. Existing files are preserved when synchronization is
incomplete. Stale files are deleted only after navigation, every page, and every image finish
successfully.

Every page records its original source URL. Broken links and images are listed in reports.
Every image manifest entry records which Markdown pages use it and its available alt text.

## Summary

The script synchronizes and reports deterministic facts. The agent is responsible for reading
all synchronized Markdown, optionally analyzing images, writing `image-notes.json`,
`image-notes.md`, and `summary.md`, and explaining the documentation to the user after every
successful run.
