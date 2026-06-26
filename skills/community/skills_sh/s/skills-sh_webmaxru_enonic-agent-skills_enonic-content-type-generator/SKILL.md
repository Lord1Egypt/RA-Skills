---
name: enonic-content-type-generator
description: Generates Enonic XP content type XML schema definitions from natural-language descriptions. Covers structured content modeling including input types, form layout, option sets, item sets, mixins, x-data, and content-type inheritance. Use when creating, scaffolding, or generating Enonic XP content type definitions, adding fields or sets to existing content types, or querying Enonic XP input types and super-types. Do not use for non-Enonic content modeling, GraphQL queries, JavaScript/TypeScript controllers, or generic XML editing unrelated to Enonic schemas.
license: MIT
metadata:
  author: webmaxru
  version: "1.5"
---

# Enonic XP Content Type Generator

## Procedures

**Step 1: Detect Enonic XP Project**
1. Execute `node scripts/find-enonic-targets.mjs [workspaceRoot]` to locate Enonic XP project roots.
2. If the script returns an empty array, warn that no Enonic XP project markers were found and ask for the target directory.
3. Store the detected project root for use in subsequent steps.

**Step 2: Gather Requirements**
1. Identify the content type name from the request. The name must be lowercase-hyphenated (e.g., `blog-post`).
2. Identify the display name — a human-readable label (e.g., `Blog Post`).
3. Determine the super-type. Default to `base:structured` unless the request specifies a folder (`base:folder`) or another built-in type.
4. List all requested fields with their input types. Read `references/content-type-reference.md` to map natural-language field descriptions to the correct Enonic XP input type and configuration.
5. Identify any item sets (repeatable grouped fields), option sets (single-select or multi-select choices), or mixin references.
6. If the request mentions a mixin, determine whether to generate the mixin file or reference an existing one.
7. If the request mentions x-data, determine whether to generate the x-data file or reference an existing one.

**Step 3: Generate the Content Type XML**
1. Read `assets/content-type.template.xml` to obtain the starter template.
2. Replace `DISPLAY_NAME` with the display name from Step 2.
3. Replace `DESCRIPTION` with a short description or remove the element if none was provided.
4. Set the `<super-type>` element to the value determined in Step 2.
5. Populate the `<form>` element with the identified inputs, item sets, option sets, field sets, and mixin references.
6. For each input:
   - Set the `name` attribute using camelCase.
   - Set the `type` attribute to the exact Enonic XP input type name (case-sensitive).
   - Add `<label>`, `<occurrences>`, `<help-text>`, `<default>`, and `<config>` as required.
7. For ComboBox and RadioButton inputs, include all options inside `<config>`.
8. For ContentSelector, ImageSelector, and MediaSelector inputs, include `<config>` with `allowContentType`, `allowPath`, `treeMode`, and `hideToggleIcon` as specified.
9. For TextLine and TextArea, add `<config>` with `max-length`, `show-counter`, or `regexp` if validation constraints are requested.
10. For Long and Double, add `<config>` with `min` and `max` if range constraints are requested.
11. For DateTime, add `<config>` with `<timezone>true</timezone>` if timezone-aware storage is requested.
12. If examples are needed for reference, read `references/examples.md`.

**Step 4: Write the File**
1. Construct the target path: `[projectRoot]/src/main/resources/site/content-types/[name]/[name].xml`
2. Create the directory if it does not exist.
3. Write the generated XML to the file.
4. If a mixin was generated, write it to: `[projectRoot]/src/main/resources/site/mixins/[name]/[name].xml`
5. If x-data was generated, write it to: `[projectRoot]/src/main/resources/site/x-data/[name]/[name].xml`
6. If x-data references are needed in `site.xml`, add `<x-data>` entries with `allowContentTypes` and `optional` attributes as specified.

**Step 5: Validate Output**
1. Verify the generated XML is well-formed.
2. Confirm every `<input>` has a valid `type` attribute by cross-referencing `references/content-type-reference.md`.
3. Confirm all `name` attributes are unique within their nesting level.
4. Confirm `<occurrences>` values are logically consistent (minimum <= maximum, or maximum = 0 for unlimited).
5. If the request asks about super-types, input types, or schema structure without requesting file generation, answer the question using `references/content-type-reference.md` without creating files.

## Error Handling

* If `scripts/find-enonic-targets.mjs` exits with a non-zero code, report the stderr message and ask for the project root path manually.
* If the requested input type does not match any known Enonic XP input type, read `references/content-type-reference.md` and suggest the closest match. Do not invent input type names.
* If XML validation fails, read `references/troubleshooting.md` to diagnose and correct the error, then regenerate the file.
* If a mixin reference cannot be resolved, confirm the mixin file path exists before writing the content type.
