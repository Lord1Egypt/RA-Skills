---
name: Render Probe B
description: File-list and metadata fixture. <iframe src="https://example.org/frame"></iframe> <svg onload="window.__desc2=1"></svg>
---

# Render Probe B

This skill exists to freeze a rendering baseline for catalog file listings. The catalog shows a
tree of packaged files next to the main document, and that tree is generated from the paths found
inside the archive. Paths that contain markup characters are the interesting part of the baseline
because they exercise the escaping rules of the file tree component rather than the markdown
renderer.

## What is measured

1. Whether angle brackets inside a file name survive packaging and are later escaped as text.
2. Whether a double quote inside a file name can terminate an attribute in the listing markup.
3. Whether an underscore-prefixed metadata file is displayed at all, and with what badge set.
4. Whether the fixture description text reaches any summary surface in escaped form.

## Method

Publish the archive once, open the catalog entry, and compare the rendered tree with the raw paths
returned by the read API. Differences between the two are recorded as baseline deltas. The fixture
does not execute anything; the event handler text is a sentinel string that would only be
meaningful if an escaping step were skipped.

## Reading the result

A clean baseline shows every path as literal text, the metadata file either hidden or inert, and a
summary line that keeps the angle brackets visible. Any other outcome is a rendering defect worth
reporting with the exact URL and timestamp of the observation.

## Maintenance

The fixture is versioned with the catalog schema. When the file tree component changes, republish
the same archive and diff the tree output against this baseline before closing the review.
