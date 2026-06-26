# SkillHub Manager Workflows

The following are standard operational workflows for managing skills in SkillHub compatible registries.

Before running any workflow below, ask the user for the SkillHub address they want to use. Do not assume a registry in advance.

After the user provides the address:
- if the user confirms the default hosted registry, use plain `npx clawhub ...`
- if the user provides a custom or self-hosted SkillHub address, prepend `CLAWHUB_REGISTRY=<url>` to every command below

Mandatory preflight interaction:
1. Ask for the SkillHub address.
2. Wait for the reply.
3. Repeat the address back in a confirmation message.
4. State the exact command style you will use next.
5. Only then execute the command.

## 1. Publishing a Skill (Submit / Upload)
When asked to submit or publish a skill package or directory to SkillHub, use the `publish` command.

1. Ensure the target skill codebase is prepared inside a local folder such as `./my-skill`.
2. Ask the user which SkillHub address to use and wait for the answer.
3. Repeat the address back and confirm the exact command style you will use.
4. Validate whether you already have a working token:
   ```bash
   npx clawhub whoami
   ```
5. If authentication is missing, log in with an API token:
   ```bash
   npx clawhub login --token <TOKEN>
   ```
6. Run the publishing command:
   ```bash
   # Usage: npx clawhub publish <path> --slug <slug> --name <Title> --version <SemVer>
   npx clawhub publish ./my-skill --slug my-skill --name "My Awesome Skill" --version 1.0.0
   ```
7. When targeting a custom or self-hosted registry, add the registry override:
   ```bash
   CLAWHUB_REGISTRY=https://your-registry.example npx clawhub publish ./my-skill --slug my-skill --name "My Awesome Skill" --version 1.0.0
   ```
8. Verify the result with:
   ```bash
   npx clawhub inspect my-skill
   ```

## 2. Previewing a Skill (Inspect)
When a user wants to preview or inspect a specific skill from the remote registry, use the `inspect` command to view its metadata.

```bash
npx clawhub inspect <skill-slug>
```

You can view recently updated skills via exploration:
```bash
npx clawhub explore --limit 10
```

## 3. Searching for a Skill
If a user asks what skills are available regarding a specific topic, use the `search` command.

```bash
npx clawhub search <query>
```

## 4. Practical Notes
- Always ask for the SkillHub address before login, search, inspect, explore, or publish.
- Always repeat the address back to the user before executing the first registry command.
- Use explicit `--slug`, `--name`, `--version`, and `--tags` values when publishing so the release is reproducible.
- Keep `README.md` and `SKILL.md` in sync before publishing.
- Prefer `npx clawhub whoami` before any publish attempt so you can fail fast on expired tokens.
- Use `CLAWHUB_REGISTRY` only after the user has provided a non-default registry.
