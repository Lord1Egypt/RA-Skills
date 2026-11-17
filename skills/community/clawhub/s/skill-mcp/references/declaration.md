# The `mcp-host:` declaration block

Optional. Inside SKILL.md's YAML frontmatter, which is already YAML.

```yaml
mcp-host:
  version: 1            # required; an unknown MAJOR is refused wholesale
  run:                  # the scripts that MAY be run, exactly
    - script: scripts/report.js   # relative to this skill's directory
      interpreter: node           # from the host's closed set; never inferred
      env: [SOME_TOKEN]           # variables this script ASKS for
      timeout: 15                 # seconds; clamped to a 300s ceiling
  env:                  # fields proposed for the REGISTRATION's environment
    - name: SOME_TOKEN
      secret: true
      description: What it is and where to get one.
  egress: [api.example.com]   # hosts this skill reaches; a proposal
```

Two things about it that are easy to get wrong.

**`run[].env` and the top-level `env` are different things.** The first names
the variables ONE SCRIPT is handed. The second proposes fields for the
registration's own environment — what the MCP process gets, which an owner
fills in with a value. A variable can be in the second and not the first: it
reaches the server and no script sees it.

**A declaration narrows; it never grants.** The same author wrote the scripts
and the block that names them, so nothing here is an authorization. When this
server runs under mcp-host, what makes a script runnable — and what makes a
variable reach it — is the registration owner accepting it. This block can only
ever reduce what that grant covers.

## What a script is handed

The fixed host set (`PATH`, `HOME`, `LANG`, `TZ`, `TMPDIR`), `MCP_DATA_DIR`
when the host set one, and exactly the names on this script's own `env` list
that the owner granted. Nothing else — not the server's own environment, and
not a variable a neighbouring skill declared.

The skill's own directory is the working directory, and when hosted it is
**read-only**: a script that needs to write uses `MCP_DATA_DIR` or `TMPDIR`.
