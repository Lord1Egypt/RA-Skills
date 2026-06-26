# Tool Output Audit Checklist

## Before moving to the next step
- Did the command actually finish?
- Did the output explicitly confirm the intended result?
- Did any warning or error change what should happen next?
- Are you inferring success from activity rather than evidence?
- Are you about to tell the user something the output did not prove?

## High-risk workflow types
- packaging and publishing
- deployments and restarts
- authentication and API calls
- file generation
- background process management
- destructive edits or deletes

## Rule of thumb
If you cannot quote the decisive line, you probably should not claim success yet.
