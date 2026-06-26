# Creating or Editing an Agent

**Trigger**: User wants to start, scaffold, create a new agent, get started with Terminal Use, OR modify/update/edit an existing agent (add skills, change behavior, update dependencies, configure options).

**Recommended reading**:
- Terminal use docs for building agents: https://docs.terminaluse.com/introduction/building-agents.md
- Reference for Claude Agent SDK: https://platform.claude.com/docs/en/agent-sdk/python

## Creating a New Agent

**Default rule:** use `tu init` for new agent creation unless the user explicitly instructs otherwise.

1. (Optional) `tu namespaces ls`
    - List namespaces user has access to

2. `tu init -ns <namespace> --name <agent name> --description <description>`
   - Ask user for agent name upfront and come up with description
   - Creates hello world Claude Agent SDK example

3. Modify the agent as needed based on user's requirements. You must read the Claude Agent SDK docs if you're making changes to the agent.

4. Ask: "Want to deploy this agent?" → if yes, see [./deploy.md](./deploy.md)

## Editing an Existing Agent

1. Locate the agent directory (must contain `config.yaml`):
   ```bash
   ls <agent-dir>/config.yaml || echo "Not an agent directory"
   ```

2. Read the existing agent code to understand current state:
   - `config.yaml` — agent name, build config, deployment settings
   - `src/agent.py` — agent logic, ClaudeAgentOptions, tools
   - `Dockerfile` — build steps, system deps, file copies
   - `pyproject.toml` — Python dependencies

3. Make the requested changes (see sections below for common modifications).

4. Ask: "Want to deploy the updated agent?" → if yes, see [./deploy.md](./deploy.md)


## Adding Dependencies

```bash
# Python packages
uv add requests

# System deps — edit Dockerfile
RUN apt-get update && apt-get install -y ffmpeg
```

⚠️ Never modify `ENTRYPOINT` or `CMD` in Dockerfile.

## Custom Skills Integration

When the user specifies a custom skills directory for their agent, configure the agent to include those skills:

1. **Copy the skills folder into the agent directory**:
   ```bash
   cp -r <user-specified-skills-path> <agent-dir>/skills
   ```

2. **Edit Dockerfile** to copy skills into the image (paths relative to docker root from config):
   ```dockerfile
   # Copy skills folder for baked mount
   COPY <path-to-agent>/skills <agent-dir-in-image>/skills
   ```
   Example: `COPY examples/devrel_agent/skills /app/examples/devrel_agent/skills`

3. **Edit config.yaml** to mount skills in the sandbox:
   ```yaml
   # Sandbox Configuration
   sandbox:
     mounts:
       - source: skills                  # Path in image (relative to agent WORKDIR)
         target: /root/.claude/skills    # Path in sandbox
         readonly: true
   ```

4. Update ClaudeAgentOptions in agent.py to load the skills:
    ```python
    options = ClaudeAgentOptions(
        setting_sources=["user"],  # "user" load skills from ~/.claude/skills
        allowed_tools=["Skill"]  # Enable Skill tool
    )
    ```
