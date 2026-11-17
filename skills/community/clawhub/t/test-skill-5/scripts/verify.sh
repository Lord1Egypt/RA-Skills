#!/usr/bin/env sh
set -eu

skill_dir=${1:-.}

for required_file in \
  SKILL.md \
  agents/openai.yaml \
  assets/expected-output.txt \
  references/fixture-contract.md \
  scripts/verify.sh; do
  if [ ! -f "$skill_dir/$required_file" ]; then
    printf 'Missing required fixture file: %s\n' "$required_file" >&2
    exit 1
  fi
done

IFS= read -r first_line < "$skill_dir/SKILL.md"
if [ "$first_line" != '---' ]; then
  printf 'SKILL.md must begin with YAML frontmatter.\n' >&2
  exit 1
fi

printf 'OpenClaw test skill fixture is valid.\n'
