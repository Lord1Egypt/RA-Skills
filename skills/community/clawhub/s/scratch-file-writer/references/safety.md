# Safety Reference for File Writer

## Sanitization Patterns
- Reject regex: ^/|\.\./ (absolutes/parents)
- Allowed extensions: txt|md|log|json|py (case-insensitive check)

## Backup Logic
- Check existence with 'read'.
- Loop to find unique .bak.N: Try .bak, .bak.1, etc., until 'read' fails (non-existent).
- Write copy to that path using 'write'.

## Confirmation Messages
- Overwrite: "File exists in scratch. Backup and overwrite? Yes/No."
- Append: "Append to existing file? Yes/No."
- Mkdir: "Subdir missing. Run `mkdir -p [path]`? Or confirm I exec it."

Load when validating or confirming actions.
