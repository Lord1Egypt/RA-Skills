# pypdf PDF Recovery Procedures

## Understanding PDF Form Architecture

A fillable PDF stores form data in two parallel structures:

1. **AcroForm /Fields** — a tree in the document catalog (`/Root → /AcroForm → /Fields`). This is what `get_form_text_fields()` and `get_fields()` read from.
2. **Page /Annots** — an array on each page containing the visual widget annotations. Each annotation has `/T` (field name), `/V` (value), `/FT` (field type), and `/Rect` (position).

Normally these reference the same objects. Corruption can break the linkage.

## Diagnosing Corruption

### Symptom: `get_form_text_fields()` returns empty but the PDF looks fine in a viewer

```python
reader = PdfReader("corrupted.pdf")

# Check 1: Are AcroForm /Fields empty?
catalog = reader.trailer["/Root"]
acroform = catalog.get("/AcroForm")
if acroform:
    af = acroform.get_object()
    fields = af.get("/Fields", [])
    print(f"AcroForm /Fields count: {len(fields)}")  # If 0 = broken field tree

# Check 2: Do page annotations still have values?
page = reader.pages[0]
annots = page.get("/Annots")
if annots:
    for annot_ref in annots:
        annot = annot_ref.get_object()
        t = str(annot.get("/T", ""))
        v = annot.get("/V", "")
        if v:
            print(f"Annotation {t} has value: {v}")  # Values survive here
```

If Check 1 shows 0 fields but Check 2 shows values, the field tree is broken but data is recoverable.

## Recovery: Rebuild Field Tree from Annotations

```python
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, TextStringObject, ArrayObject

reader = PdfReader("corrupted.pdf")
writer = PdfWriter()
writer.append(reader)

# Optional: update specific field values during recovery
target_updates = {"f1_17": "338"}  # example: fix a value while rebuilding

# Step 1: Update annotation values on writer pages
for page_idx in range(len(writer.pages)):
    page = writer.pages[page_idx]
    annots = page.get("/Annots")
    if not annots:
        continue
    for annot_ref in annots:
        annot = annot_ref.get_object()
        t = str(annot.get("/T", ""))
        for key, val in target_updates.items():
            if key in t:
                annot[NameObject("/V")] = TextStringObject(val)

# Step 2: Collect all annotation references across all pages
all_field_refs = []
for page_idx in range(len(writer.pages)):
    page = writer.pages[page_idx]
    annots = page.get("/Annots")
    if annots:
        for annot_ref in annots:
            all_field_refs.append(annot_ref)

# Step 3: Rebuild AcroForm /Fields
catalog = writer._root_object
acroform = catalog.get("/AcroForm")
if acroform:
    af_obj = acroform.get_object() if hasattr(acroform, 'get_object') else acroform
    af_obj[NameObject("/Fields")] = ArrayObject(all_field_refs)

# Step 4: Write to DIFFERENT path, then copy
output_path = "/tmp/recovered.pdf"
with open(output_path, "wb") as f:
    writer.write(f)

# Step 5: Verify
reader2 = PdfReader(output_path)
fields = reader2.get_form_text_fields()
print(f"Recovered {len(fields)} text fields")
all_f = reader2.get_fields()
print(f"Recovered {len(all_f)} total fields (incl. checkboxes)")
```

## Root Cause: Writing to Same File Path

The most common cause of field tree corruption is writing pypdf output to the same file being read:

```python
# This WILL corrupt the file
reader = PdfReader("form.pdf")
writer = PdfWriter()
writer.append(reader)
# ... modifications ...
with open("form.pdf", "wb") as f:  # SAME PATH as reader input
    writer.write(f)
```

What happens: `PdfReader` uses lazy reading. When `writer.write()` opens the same file for writing, it truncates the file while the reader still has references into it. The page annotations (already in memory) survive, but the AcroForm catalog gets corrupted during the partial read/write overlap.

**Prevention**: Always write to a temp file first:
```python
import shutil
with open("/tmp/form_temp.pdf", "wb") as f:
    writer.write(f)
shutil.copy("/tmp/form_temp.pdf", "form.pdf")
```

## Other pypdf Gotchas

### `auto_regenerate=True` (the default) clears appearance streams
Always pass `auto_regenerate=False` to `update_page_form_field_values()`. The default `True` removes `/AP` (appearance) entries, which makes some PDF viewers show blank fields even though `/V` has a value.

### "No fields to update on this page" warning
This is normal and harmless. It just means the field names you passed don't exist on that particular page. Since we iterate all pages, this fires for pages that don't contain the target fields.

### Field names include full path
IRS PDFs use hierarchical field names like `topmostSubform[0].Page1[0].f1_42[0]`. When using `update_page_form_field_values()`, you need the FULL path, not just `f1_42`. Extract the full name from `get_form_text_fields()` or from annotations.

### Checkbox values
IRS checkboxes use `/Off` for unchecked and a number like `/1`, `/2`, `/Yes` for checked. The specific "on" value varies by form. Check the existing value in the annotation before trying to set it.
