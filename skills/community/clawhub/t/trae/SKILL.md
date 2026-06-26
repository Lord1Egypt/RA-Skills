### Skill Name: TRAE IDE & Workflow Architect

### Skill Description

This skill equips an Agent with deep expertise in the TRAE IDE ecosystem, specifically focusing on its unique "Skills" architecture, AI-driven coding capabilities, and workflow automation. The Agent will move beyond basic usage to explain how to architect custom Skills (packaging instructions, scripts, and resources), manage the distinction between Rules and Skills, and leverage the IDE's agentic features to maximize development velocity. It serves as a guide for transforming TRAE from a text editor into a personalized, automated development partner.

### Core Instruction Set

#### 1. The "Skills" Architecture

Explain the modular nature of TRAE's intelligence, which relies on "Skills" rather than just static prompts.

- **Definition:** A Skill is a context-triggered instruction set. It allows users to package specific workflows (instructions + resources) into reusable modules.
- **File Structure:**
    - **SKILL.md (Mandatory):** The core "brain" containing metadata (name, description) and the specific system instructions for the AI.
    - **Resources (Optional):** Scripts (`.py`, `.sh`), templates, or reference documents that the Skill can execute or reference.
    - **Location:** Skills are typically stored in the `.trae/skills/` directory within a project or globally.
- **Trigger Mechanism:** Skills can be invoked manually via natural language (e.g., "Use the [Skill Name] to...") or automatically when the AI detects a context match.

#### 2. Strategic Distinctions: Rules vs. Skills vs. Context

Clarify the specific use cases for TRAE's different configuration layers to optimize Token usage and AI focus.

- **Rules (Global/Project):**
    - **Function:** Persistent preferences and constraints (e.g., "Always use TypeScript," "No console logs").
    - **Loading:** Loaded into the context window constantly.
    - **Best For:** Coding styles, linting preferences, and broad behavioral guidelines.
- **Skills (Modular):**
    - **Function:** Specific, complex workflows (e.g., "Generate Unit Tests," "Refactor Legacy Code").
    - **Loading:** **On-demand (Lazy Loading).** They only consume context when triggered.
    - **Best For:** Reusable tasks, complex multi-step operations, and specialized domain knowledge.
- **Context (Passive):**
    - **Function:** Reference materials (documentation, codebases).
    - **Best For:** Providing the AI with the "knowledge base" it needs to answer questions.

#### 3. Creating and Deploying Custom Skills

Guide users through the lifecycle of building a custom Skill.

- **Natural Language Creation:** Instruct users that they can simply ask TRAE to "Create a skill for X," and the IDE will generate the folder structure and `SKILL.md` automatically.
- **Manual Authoring:**
    - **Metadata:** Define clear `name` and `description` fields to help the AI recognize when to use the skill.
    - **Instructions:** Write precise, step-by-step directives in the `SKILL.md` file.
- **Import/Export:** Explain how to share Skills by zipping the skill folder or importing them from community repositories (like GitHub).

#### 4. Agentic Capabilities & Workflow

Leverage TRAE's ability to act as an autonomous agent.

- **Sub-Agents:** Explain how TRAE can delegate tasks to specialized sub-agents (e.g., a "Code Reviewer" agent or a "UI Designer" agent) that utilize specific Skills.
- **Automation:** Describe how to chain Skills together. For example, using a "Data Cleaner" skill followed by a "Visualization" skill in a data science workflow.
- **MCP (Model Context Protocol):** Mention TRAE's compatibility with MCP, allowing it to connect to external data sources and tools seamlessly.

#### 5. Ecosystem & Community Resources

Highlight the collaborative aspect of the TRAE ecosystem.

- **Marketplace/Repositories:** Point users towards community-driven collections (like `awesome-trae-skills` or Anthropic's skill repositories) to avoid reinventing the wheel.
- **Common Use Cases:**
    - **Frontend Design:** Generating high-quality UI code based on design principles.
    - **DevOps:** Automating Dockerfile creation or CI/CD pipelines.
    - **Documentation:** Auto-generating docs from code comments.

### Troubleshooting & Common Pitfalls

#### "Skill Not Found" or Not Triggering

- **Diagnosis:** The `SKILL.md` file might be missing, misnamed, or located outside the `.trae/skills/` directory.
- **Fix:** Verify the file path and ensure the metadata (name/description) clearly matches the user's prompt intent.

#### Context Window Overload

- **Symptom:** The AI becomes slow or confused because too many Rules are active.
- **Fix:** Move complex, specific instructions out of "Rules" and into a "Skill." This keeps the baseline context light and only loads the heavy instructions when necessary.

#### Skill Logic Errors

- **Symptom:** The Skill executes but produces incorrect code.
- **Fix:** Treat the `SKILL.md` like code—debug it. Refine the instructions within the markdown file and re-test.

### Skill Extension Suggestions

#### Python/Scripting Integration

Expand the skill to teach users how to embed Python scripts within a Skill folder. This allows the AI to not just *write* code, but *execute* it (e.g., a Skill that runs a Python script to format data before answering).

#### Enterprise Governance

Instruct on how to create "Organization-wide" Skills that enforce company-specific security protocols, coding standards, or API usage patterns across all developer environments.

#### Multi-Agent Collaboration

Guide users on setting up complex workflows where one Skill acts as a "Manager" that delegates tasks to other specialized Skills, simulating a full software team within the IDE.

