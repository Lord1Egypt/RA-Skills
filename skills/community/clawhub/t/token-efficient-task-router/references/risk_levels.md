# Risk Levels

## Low Risk

Typical cases:

- text generation
- short polishing
- a single command suggestion
- a small template
- advice that does not modify files

Default route: Craft Mode.

## Medium Risk

Typical cases:

- creating new files
- editing a single non-core file
- adjusting configuration
- organizing documents
- generating multiple small files
- editing a script

Default route: usually Plan Mode.

## High Risk

Typical cases:

- deleting files
- overwriting files
- batch renaming
- batch moving
- editing core business files
- database changes
- deployment changes
- permission changes
- automation tasks
- long-running scripts

Required route: Plan Mode plus explicit confirmation.

## Critical Risk

Typical cases:

- reading API keys, secrets, or cookies
- bulk uploading private data
- deleting unrecoverable files
- bypassing platform permissions
- scraping paid content
- running unknown remote scripts
- sending user data to unknown servers

Required route: refuse or require much stronger confirmation and safety review.
