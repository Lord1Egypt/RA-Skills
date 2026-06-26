---
name: features-completion
description: Shell tab completion for pnpm (Bash, Zsh, Fish)
---

# Shell Completion

pnpm supports command-line tab completion for Bash, Zsh, Fish, and similar shells without extra plugins.

## Usage

### Bash

```bash
pnpm completion bash > ~/completion-for-pnpm.bash
echo 'source ~/completion-for-pnpm.bash' >> ~/.bashrc
```

### Fish

```bash
pnpm completion fish > ~/.config/fish/completions/pnpm.fish
```

### Zsh

Use the same pattern as Bash or source the completion script in `.zshrc`.

## Notes

- Completion for pnpm v9+ is incompatible with older versions. If you had `__tabtab` in dotfiles, remove it before using v9+ completion.
- Run `pnpm completion <shell>` to print the script; redirect to a file and source it in your shell config.

## Key Points

- Built-in: no plugin required.
- `pnpm completion bash | fish` outputs the completion script.
- Add to shell rc so completions load in new sessions.

<!--
Source references:
- https://pnpm.io/completion
- sources/pnpm/docs/completion.md
-->
