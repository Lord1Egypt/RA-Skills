# Application Tracking

Read this reference only when the user explicitly asks to track or manage job
applications. Reactive Resume MCP can manage applications only when the current
client exposes the relevant tools; otherwise gather the facts without inventing
tool calls or claiming a record was changed.

- Use `list_applications` before changing an existing record.
- Use `create_application` for one opportunity or `import_applications` for
  spreadsheet/CSV rows.
- Use `update_application` for stages, archives, contacts, follow-ups, linked
  resumes, and job details; use `add_application_note` for timeline activity.
- Use document and Copilot operations only after the required linked resume and
  job description exist. Review generated cover letters and follow-ups before
  sending them.
