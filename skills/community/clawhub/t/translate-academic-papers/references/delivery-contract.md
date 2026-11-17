# Final delivery contract

This contract separates resumable working drafts from files that may be shown
to the user as completed translations.

## Required artifacts

- One Chinese-only DOCX named `<Chinese title>_Image2全文中文版.docx`.
- One paragraph-aligned DOCX named `<Chinese title>_Image2逐段中英对照版.docx`.
- A `translations.jsonl` cache whose effective last row for every body source ID
  has `status: "ai_verified"` and retains the matching English source text.
- An `image2_manifest.json` containing one accepted record for every translated
  figure, including original and translated paths/hashes, `generator: "Image2"`,
  a label-by-label audit with `result: "pass"`, residual-English result, and
  clipping result. A nonempty audit object whose result is `fail` is a failure.

## Structural invariants

- The bilingual body is emitted as atomic English/Chinese pairs from the same
  source ID. Adjacent English blocks may not be merged before Chinese output.
- Its figures alternate exact pairs: untouched English original, then the exact
  same Chinese Image2 file embedded in the Chinese-only edition.
- Both files contain native WPS `w:hyperlink w:anchor="ref_N"` links and matching
  ASCII bookmarks. The usual WPS activation gesture is Ctrl+click.
- DOI text links to the official `https://doi.org/<doi>` target.
- English reference entries remain English in both editions.

## Figure acceptance

Image2 must edit the original crop rather than invent a replacement chart. The
accepted image preserves data marks, numeric values, scales, colors, panels,
geometry, uncertainty and significance marks. Every semantic English label is
replaced at its original location. Reject residual semantic English, added
translation keys, missing labels, clipped text, cropped color bars, changed
numbers, changed plot geometry, or a result that only translates the caption.

## Final command gate

Run `scripts/validate_delivery.py` after citation linking and DOCX assembly. A
non-zero result means the invocation is incomplete, regardless of whether both
DOCX files exist or open successfully.

