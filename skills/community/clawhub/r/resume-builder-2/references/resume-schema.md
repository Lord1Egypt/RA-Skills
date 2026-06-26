# Resume Schema

The renderer expects a JSON object with this structure.

```json
{
  "name": "Jane Doe",
  "title": "Senior Product Manager",
  "location": "Singapore",
  "phone": "+65 0000 0000",
  "email": "jane@example.com",
  "website": "https://janedoe.dev",
  "linkedin": "https://linkedin.com/in/janedoe",
  "summary": [
    "Lead product manager with 8 years of experience across B2B SaaS and fintech.",
    "Known for shipping high-impact workflow products and aligning engineering with business goals."
  ],
  "skills": [
    "Product Strategy",
    "Roadmapping",
    "SQL",
    "Experimentation"
  ],
  "experience": [
    {
      "company": "Acme Corp",
      "title": "Senior Product Manager",
      "location": "Remote",
      "start": "2022",
      "end": "Present",
      "bullets": [
        "Owned onboarding and activation product areas across web and mobile.",
        "Led a redesign that reduced time-to-value for new users."
      ]
    }
  ],
  "projects": [
    {
      "name": "Global Pricing Migration",
      "subtitle": "Internal strategic program",
      "bullets": [
        "Coordinated finance, engineering, and GTM teams across the rollout."
      ]
    }
  ],
  "education": [
    {
      "school": "Example University",
      "degree": "B.S. in Computer Science",
      "start": "2012",
      "end": "2016"
    }
  ],
  "certifications": [
    "PMP"
  ],
  "languages": [
    "English",
    "Mandarin"
  ]
}
```

Notes:

- `summary` should be 2 to 4 short bullets.
- `skills` should usually stay within 8 to 14 concise items.
- `experience` is the most important section.
- `projects`, `certifications`, and `languages` are optional.
- Use arrays of strings for bullet lists.
