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
- `personal.photo` is optional and hidden by default in all built-in themes. Provide a file path (relative to the HTML output location), an http(s) URL, or a data: base64 URI. Enable rendering in a custom theme via CSS (`.resume-photo { display: block; ... }`). Only include a photo when the target market expects one — many regions penalize photo resumes.
- Imported PDFs may initially produce rough entries or raw text. Normalize these into canonical fields before final export.

## Work File Convention

By default, save resume JSON to `resume.json` in the current working directory. If the user specifies a different location, use that instead. When importing from PDF, extract to the same location with a `.json` extension replacing `.pdf`.
