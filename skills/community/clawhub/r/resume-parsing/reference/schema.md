# JSON Resume schema + mapping rules

The full JSON Resume standard (13 sections + `meta`) that `resume.json` output
must conform to, plus the rules for mapping messy resume text onto it.

## Contents
- Mapping rules (read first)
- Section field reference
- Standard extensions (the `x_` namespaces)

## Mapping rules

1. **Never invent.** Only emit a field if the value is present in the resume
   text (or the `.extract.json` sidecar). Omit unknown fields and whole sections
   entirely — do not write empty strings or placeholders like `"N/A"`.
2. **Dates → ISO-8601.** Normalize every date to `YYYY`, `YYYY-MM`, or
   `YYYY-MM-DD`. Examples: `2020年3月` → `2020-03`; `Mar 2020` → `2020-03`;
   `2012–2016` → `startDate: "2012"`, `endDate: "2016"`. A current role has a
   `startDate` and **no** `endDate` (drop "至今"/"Present").
3. **Contacts come from the sidecar.** Take `email`, `phone`, `url`, and
   `basics.profiles` from `<stem>.extract.json` `contacts` — they are
   regex-extracted and more reliable than re-reading them from prose. Put the
   single best personal site/GitHub in `basics.url`; the rest go in `profiles`.
4. **Bilingual.** Keep values in the resume's own language (do not translate
   names, companies, or schools). Section keys stay English per the standard.
5. **Company vs position.** In `work`, `name` is the employer, `position` is the
   title. Bullet points describing impact go in `highlights` (array), the role's
   one-line scope in `summary`.
6. **Skills.** Group into a few `skills` entries by category when the resume
   implies categories (e.g. `{name:"后端", keywords:["Go","MySQL"]}`); otherwise
   one entry per named skill. `keywords` is an array of strings.
7. **Common CN-resume fields → use the standard extensions.** JSON Resume has no
   slot for birth date, gender, job objective, expected salary, etc. When the
   resume has them, put them in the fixed `x_` namespaces below — do NOT invent
   ad-hoc keys (always `birthDate`, never `birthday`/`sex`). `validate.py` checks
   these sub-field names.
8. **Traceability.** Always add an `x_parse` block recording the source file and
   any layout warnings from the sidecar.

## Section field reference

Only these fields are valid. `validate.py` flags anything else. `[]` = array of
strings unless noted; nested objects are spelled out.

- **basics**: `name`, `label` (headline/title), `image`, `email`, `phone`,
  `url`, `summary`,
  `location` = { `address`, `postalCode`, `city`, `countryCode`, `region` },
  `profiles` = [ { `network`, `username`, `url` } ]
- **work**: `name` (employer), `location`, `description` (of employer),
  `position`, `url`, `startDate`, `endDate`, `summary`, `highlights[]`
- **volunteer**: `organization`, `position`, `url`, `startDate`, `endDate`,
  `summary`, `highlights[]`
- **education**: `institution`, `url`, `area` (field of study), `studyType`
  (degree), `startDate`, `endDate`, `score` (GPA/rank, string), `courses[]`
- **awards**: `title`, `date`, `awarder`, `summary`
- **certificates**: `name`, `date`, `issuer`, `url`
- **publications**: `name`, `publisher`, `releaseDate`, `url`, `summary`
- **skills**: `name`, `level`, `keywords[]`
- **languages**: `language`, `fluency`
- **interests**: `name`, `keywords[]`
- **references**: `name`, `reference`
- **projects**: `name`, `description`, `entity`, `type`, `url`, `startDate`,
  `endDate`, `highlights[]`, `keywords[]`, `roles[]`
- **meta**: `canonical`, `version`, `lastModified` — standard use only; do NOT
  put parser data here.

Date fields (must be ISO): work/volunteer/education/projects `startDate` &
`endDate`; awards & certificates `date`; publications `releaseDate`.

## Standard extensions (the `x_` namespaces)

Top-level `additionalProperties` is `true`, and any key starting with `x_` is
accepted, so the document stays a valid JSON Resume that off-the-shelf tools can
still consume. To keep output consistent, put common fields the standard lacks
into these **three fixed namespaces** with these **exact** sub-field names.
`validate.py` warns on any unrecognized sub-field (a typo guard); add a genuinely
new field to `EXTENSIONS` in `validate.py` and to this list together.

### `x_personal` — personal info (常见于中文简历)
`birthDate` (ISO), `age`, `gender`, `maritalStatus` (婚姻状况), `nativePlace`
(籍贯), `residence` (现居地), `politicalStatus` (政治面貌), `ethnicity` (民族),
`photo` (URL/path). Emit only what's present.

```json
"x_personal": { "birthDate": "1989-10", "gender": "男" }
```

### `x_objective` — job objective (求职意向)
`positions[]` (期望职位), `industries[]` (期望行业), `domains[]` (领域),
`platforms[]` (平台), `expectedSalary` (string, e.g. "25-35K"), `locations[]`
(期望城市), `availability` (到岗时间), `employmentType` (全职/兼职/实习).

```json
"x_objective": { "positions": ["架构师","技术经理"], "domains": ["Web服务端"] }
```

### `x_parse` — parser traceability (always add)
`source` (filename), `pages`, `columns`, `warnings[]`, `confidence`
(`low`/`medium`/`high` by layout warnings and how cleanly it mapped), `tool`.

```json
"x_parse": { "source": "张伟_简历.pdf", "columns": 2,
  "warnings": ["Detected a multi-column layout; verify timeline"],
  "confidence": "medium" }
```
