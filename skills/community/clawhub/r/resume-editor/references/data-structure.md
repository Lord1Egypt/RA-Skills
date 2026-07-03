# Resume Data Structure

Resume data is maintained in structured JSON format. The `personal.name` field is required; all other fields are optional.

The canonical machine-readable schema is in `references/resume-schema.json`. Keep working files aligned to that schema before export.

```json
{
  "personal": {
    "name": "Full Name",
    "email": "email@example.com",
    "phone": "+86 138-0000-0000",
    "location": "City, Country",
    "linkedin": "https://linkedin.com/in/...",
    "github": "https://github.com/...",
    "photo": "photo.jpg"
  },
  "summary": "Professional summary...",
  "education": [
    {
      "institution": "University Name",
      "degree": "Bachelor/Master/PhD in Field",
      "period": "2020-2024",
      "location": "City, Country",
      "gpa": "3.8/4.0",
      "honors": ["Dean's List", "Scholarship"]
    }
  ],
  "experience": [
    {
      "company": "Company Name",
      "position": "Job Title",
      "period": "2022-Present",
      "location": "City, Country",
      "description": "High-level description of role and responsibilities.",
      "achievements": ["Quantified achievement with metrics"]
    }
  ],
  "projects": [
    {
      "name": "Project Name",
      "role": "Role (e.g., Lead Developer)",
      "period": "2023",
      "technologies": ["Python", "React", "AWS"],
      "description": "Brief overview...",
      "achievements": ["Launched product with 10k+ users"]
    }
  ],
  "skills": {
    "programming": ["Python", "JavaScript", "Go"],
    "frameworks": ["React", "Django", "Spring Boot"],
    "tools": ["Git", "Docker", "Kubernetes"],
    "languages": ["Chinese (Native)", "English (Fluent)"]
  }
}
```

## Notes

- Store spoken languages under `skills.languages`, not `personal.languages`.
- `personal.linkedin` and `personal.github` should be full `https://` profile URLs.
- `personal.photo` is optional and hidden by default in all built-in themes. Provide a relative path, absolute local file path, `file://` URL, `https://` URL, or a `data:` URI. Plain `http://` photo URLs are rejected. Enable rendering in a custom theme via CSS (`.resume-photo { display: block; ... }`). Only include a photo when the target market expects one — many regions penalize photo resumes.
- Imported PDFs may initially produce rough entries or raw text. Normalize these into canonical fields before final export.

## Rich Text (Emphasis)

Body fields accept a small, safe Markdown subset for emphasis. Apply it when you (the agent) author content, and the user can also apply it visually via the editable HTML toolbar.

Supported syntax:

| Syntax | Effect |
|---|---|
| `**text**` | bold |
| `*text*` | italic |
| `_text_` | underline |
| `==text\|#rrggbb==` or `==text\|namedcolor==` | colored run |

Examples:

- `"Achieved **30%** growth with *custom* analytics."` → bold "30%", italic "custom".
- `"Shipped ==critical|#c0392b== fix ahead of schedule."` → "critical" in red.

**Fields that support rich text:**

- `summary`
- `experience[].description`, `experience[].responsibilities[]`, `experience[].achievements[]`
- `education[].honors[]` (each honor item)
- `projects[].description`, `projects[].achievements[]`

**Fields that render plain** (kept plain to preserve tight layouts and a professional look):

- `personal.*` (name, contact fields)
- `experience[].company`, `position`, `period`, `location`
- `education[].institution`, `degree`, `period`, `location`, `gpa`
- `projects[].name`, `role`, `period`, `technologies`
- `skills.*` (all categories and items)

**Safety:** the renderer escapes HTML special characters first and then applies a strict whitelist of `<strong>` / `<em>` / `<u>` / `<span style="color:...">`. Color specs must match `#rrggbb` (3–8 hex digits) or a fixed set of CSS named colors; anything else is left as literal text. Use emphasis sparingly — a resume should still read as a professional document, not a highlight reel.

## Work File Convention

By default, save resume JSON to `resume.json` in the current working directory. If the user specifies a different location, use that instead. When importing from PDF, extract to the same location with a `.json` extension replacing `.pdf`.
