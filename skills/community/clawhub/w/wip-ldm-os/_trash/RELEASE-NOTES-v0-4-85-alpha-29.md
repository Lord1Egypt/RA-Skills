LDM OS install prompts now carry the same track-aware install pattern as downstream products. The install document teaches agents to check npm dist-tags, explain stable/current, beta, and alpha availability in plain English, and map the selected track to the right dry-run and install commands without hard-coding `@latest`.

This alpha also adds a README prompt regression test so the human-facing prompt stays short while detailed track-selection logic remains in `SKILL.md`.
