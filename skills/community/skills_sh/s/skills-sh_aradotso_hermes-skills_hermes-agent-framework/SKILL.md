---
name: hermes-agent-framework
description: Hermes Agent framework by Nous Research - self-improving AI agent with built-in learning loop, three-layer memory, and automatic skill evolution
triggers:
  - "help me set up Hermes Agent"
  - "how do I use the Hermes framework"
  - "create a Hermes agent with custom skills"
  - "configure Hermes memory system"
  - "build an AI agent with Hermes"
  - "how does Hermes learning loop work"
  - "integrate tools with Hermes Agent"
  - "customize Hermes agent behavior"
---

# Hermes Agent Framework

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

Hermes Agent is an open-source AI Agent framework by Nous Research that features a built-in self-improving learning loop, three-layer memory system (episodic, semantic, procedural), and automatic Skill creation and evolution. Unlike traditional agentic frameworks, Hermes continuously learns from interactions and builds up capabilities over time.

## Installation

### Prerequisites

- Python 3.9+
- API key for LLM provider (OpenAI, Anthropic, etc.)

### Basic Installation

```bash
# Clone the repository
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent

# Install dependencies
pip install -r requirements.txt

# Or install via pip (if published)
pip install hermes-agent
```

### Configuration

Create a `.env` file in the project root:

```bash
# LLM Provider Configuration
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Agent Configuration
HERMES_MODEL=gpt-4
HERMES_MEMORY_PATH=./memory
HERMES_SKILLS_PATH=./skills
```

## Core Concepts

### Three-Layer Memory System

1. **Episodic Memory**: Stores conversation history and interaction sequences
2. **Semantic Memory**: Long-term knowledge and facts extracted from experiences
3. **Procedural Memory**: Skills and learned procedures (how to do things)

### Learning Loop

Hermes operates in a continuous cycle:
1. **Perceive**: Receive user input and context
2. **Reflect**: Analyze what happened and extract learnings
3. **Learn**: Update memory systems and create/modify Skills
4. **Act**: Execute tasks using available tools and Skills

### Skills

Skills are reusable capabilities that Hermes creates and refines automatically. They're stored as structured modules in the procedural memory.

## Basic Usage

### Starting a Hermes Agent

```python
from hermes_agent import HermesAgent, Config

# Initialize configuration
config = Config(
    model="gpt-4",
    memory_path="./memory",
    skills_path="./skills",
    temperature=0.7
)

# Create agent instance
agent = HermesAgent(config)

# Start conversation
response = agent.chat("Help me analyze this CSV file and create visualizations")
print(response)
```

### With Custom System Prompt

```python
from hermes_agent import HermesAgent, Config

config = Config(
    model="claude-3-5-sonnet-20241022",
    system_prompt="""You are a specialized data analysis agent.
    Focus on statistical rigor and clear visualizations.
    Always explain your analytical choices."""
)

agent = HermesAgent(config)
```

### Enabling Memory Persistence

```python
from hermes_agent import HermesAgent, Config, MemoryConfig

memory_config = MemoryConfig(
    episodic_enabled=True,
    semantic_enabled=True,
    procedural_enabled=True,
    retention_days=90,
    auto_consolidate=True
)

config = Config(
    model="gpt-4",
    memory_config=memory_config
)

agent = HermesAgent(config)

# Memory is automatically saved and loaded
agent.chat("Remember that I prefer Python over JavaScript")
# Later sessions will recall this preference
```

## Working with Skills

### Creating a Custom Skill

```python
from hermes_agent import Skill, SkillParameter

# Define a custom skill
web_scraper_skill = Skill(
    name="web_scraper",
    description="Scrape and extract structured data from websites",
    parameters=[
        SkillParameter(name="url", type="string", required=True),
        SkillParameter(name="selectors", type="object", required=False)
    ],
    implementation="""
import requests
from bs4 import BeautifulSoup

def execute(url, selectors=None):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    if selectors:
        results = {}
        for key, selector in selectors.items():
            results[key] = soup.select(selector)
        return results
    
    return soup.get_text()
"""
)

# Register skill with agent
agent.register_skill(web_scraper_skill)
```

### Loading Skills from Directory

```python
from hermes_agent import HermesAgent, Config

config = Config(
    model="gpt-4",
    skills_path="./my_custom_skills"
)

agent = HermesAgent(config)

# Agent automatically loads all skills from directory
# Skills are available for use in conversations
```

### Skill Auto-Evolution

```python
from hermes_agent import HermesAgent, Config, LearningConfig

learning_config = LearningConfig(
    auto_create_skills=True,
    skill_refinement=True,
    min_usage_for_creation=3  # Create skill after pattern used 3+ times
)

config = Config(
    model="gpt-4",
    learning_config=learning_config
)

agent = HermesAgent(config)

# As agent performs repeated tasks, it automatically creates reusable skills
agent.chat("Convert this JSON to CSV format")
agent.chat("Convert this other JSON to CSV")
agent.chat("And convert this JSON to CSV too")

# After 3rd usage, Hermes creates a "json_to_csv" skill automatically
```

## Tool Integration

### Registering External Tools

```python
from hermes_agent import HermesAgent, Tool

def search_api(query: str) -> dict:
    """Search using external API"""
    import os
    import requests
    
    api_key = os.getenv("SEARCH_API_KEY")
    response = requests.get(
        "https://api.example.com/search",
        params={"q": query, "key": api_key}
    )
    return response.json()

# Register as tool
search_tool = Tool(
    name="web_search",
    description="Search the web for current information",
    function=search_api,
    parameters={
        "query": {"type": "string", "description": "Search query"}
    }
)

agent = HermesAgent(config)
agent.register_tool(search_tool)
```

### Built-in Tool Categories

```python
from hermes_agent import HermesAgent, Config, ToolConfig

tool_config = ToolConfig(
    enable_file_operations=True,
    enable_web_browsing=True,
    enable_code_execution=True,
    enable_shell_commands=False,  # Disabled by default for security
    allowed_domains=["*.example.com", "api.trusted.com"]
)

config = Config(
    model="gpt-4",
    tool_config=tool_config
)

agent = HermesAgent(config)
```

## Multi-Agent Orchestration

### Creating Agent Teams

```python
from hermes_agent import HermesAgent, AgentTeam, Config

# Create specialized agents
researcher = HermesAgent(Config(
    model="gpt-4",
    system_prompt="You are a research specialist. Focus on gathering and analyzing information."
))

coder = HermesAgent(Config(
    model="claude-3-5-sonnet-20241022",
    system_prompt="You are a coding specialist. Write clean, efficient code."
))

writer = HermesAgent(Config(
    model="gpt-4",
    system_prompt="You are a technical writer. Create clear documentation."
))

# Create team
team = AgentTeam(
    agents=[researcher, coder, writer],
    coordinator=HermesAgent(Config(
        model="gpt-4",
        system_prompt="Coordinate agent activities and synthesize results."
    ))
)

# Execute team task
result = team.execute(
    "Research best practices for API design, implement a sample API, and document it"
)
```

### Agent Communication

```python
from hermes_agent import HermesAgent, AgentChannel

# Create communication channel
channel = AgentChannel()

agent_a = HermesAgent(config)
agent_b = HermesAgent(config)

# Connect agents to channel
agent_a.connect(channel)
agent_b.connect(channel)

# Agents can now share context and learnings
agent_a.chat("Learn about Python async patterns")
# agent_b automatically has access to what agent_a learned
agent_b.chat("Use async patterns to build a web scraper")
```

## Advanced Configuration

### Feedback Loop Customization

```python
from hermes_agent import HermesAgent, Config, FeedbackConfig

feedback_config = FeedbackConfig(
    enable_self_critique=True,
    reflection_frequency="after_task",  # or "periodic", "never"
    quality_threshold=0.8,
    auto_correction=True
)

config = Config(
    model="gpt-4",
    feedback_config=feedback_config
)

agent = HermesAgent(config)
```

### Constraints and Safety

```python
from hermes_agent import HermesAgent, Config, ConstraintConfig

constraints = ConstraintConfig(
    max_iterations=10,
    timeout_seconds=300,
    max_tool_calls_per_turn=5,
    blocked_operations=["rm -rf", "DROP TABLE"],
    require_approval_for=["file_delete", "api_payment"]
)

config = Config(
    model="gpt-4",
    constraint_config=constraints
)

agent = HermesAgent(config)
```

### Memory Management

```python
from hermes_agent import HermesAgent, Config

config = Config(model="gpt-4")
agent = HermesAgent(config)

# Inspect memory
episodic = agent.memory.get_episodic(last_n=10)
semantic = agent.memory.get_semantic(topic="python programming")
skills = agent.memory.get_skills()

# Clear specific memory types
agent.memory.clear_episodic()  # Clear conversation history
agent.memory.clear_semantic(topic="outdated_info")

# Export/Import memory
agent.memory.export("backup.json")
agent.memory.import_from("backup.json")
```

## Real-World Examples

### Personal Knowledge Assistant

```python
from hermes_agent import HermesAgent, Config, MemoryConfig, ToolConfig

memory_config = MemoryConfig(
    episodic_enabled=True,
    semantic_enabled=True,
    retention_days=365,
    auto_consolidate=True
)

tool_config = ToolConfig(
    enable_file_operations=True,
    enable_web_browsing=True
)

config = Config(
    model="gpt-4",
    memory_config=memory_config,
    tool_config=tool_config,
    system_prompt="""You are a personal knowledge assistant.
    Learn from all our interactions and help me recall information,
    make connections, and build on past conversations."""
)

agent = HermesAgent(config)

# Over time, agent builds up knowledge about user preferences, projects, etc.
agent.chat("I'm working on a new Python project for data analysis")
# Days later...
agent.chat("What was that project I mentioned last week?")
```

### Development Automation Agent

```python
from hermes_agent import HermesAgent, Config, ToolConfig, LearningConfig

tool_config = ToolConfig(
    enable_code_execution=True,
    enable_file_operations=True,
    enable_shell_commands=True
)

learning_config = LearningConfig(
    auto_create_skills=True,
    skill_refinement=True
)

config = Config(
    model="claude-3-5-sonnet-20241022",
    tool_config=tool_config,
    learning_config=learning_config,
    system_prompt="You are a development automation specialist."
)

agent = HermesAgent(config)

# Agent learns common development patterns and creates skills
agent.chat("Set up a new FastAPI project with PostgreSQL")
agent.chat("Add authentication with JWT")
agent.chat("Create CRUD endpoints for a User model")
# Agent creates reusable skills for these common patterns
```

### Content Creation Pipeline

```python
from hermes_agent import HermesAgent, AgentTeam, Config

researcher = HermesAgent(Config(
    model="gpt-4",
    system_prompt="Research topics and gather information.",
    tool_config=ToolConfig(enable_web_browsing=True)
))

writer = HermesAgent(Config(
    model="claude-3-5-sonnet-20241022",
    system_prompt="Create engaging, well-structured content."
))

editor = HermesAgent(Config(
    model="gpt-4",
    system_prompt="Review and refine content for clarity and quality."
))

team = AgentTeam(agents=[researcher, writer, editor])

# Automated content pipeline
result = team.execute(
    "Create a comprehensive blog post about Hermes Agent framework"
)
```

## CLI Usage

If Hermes provides a command-line interface:

```bash
# Start interactive session
hermes chat

# With specific model
hermes chat --model gpt-4

# Load skills from directory
hermes chat --skills ./my_skills

# Enable debug mode
hermes chat --debug

# One-off command
hermes exec "analyze this CSV: data.csv"

# Manage memory
hermes memory export backup.json
hermes memory import backup.json
hermes memory clear --episodic

# List learned skills
hermes skills list

# Export a skill
hermes skills export web_scraper > web_scraper.py
```

## Troubleshooting

### Memory Not Persisting

```python
# Ensure memory path is writable
import os
from hermes_agent import HermesAgent, Config

memory_path = "./hermes_memory"
os.makedirs(memory_path, exist_ok=True)

config = Config(
    model="gpt-4",
    memory_path=memory_path,
    auto_save=True  # Enable automatic saving
)

agent = HermesAgent(config)
```

### Skills Not Loading

```python
# Verify skills directory structure
from hermes_agent import HermesAgent, Config

config = Config(
    model="gpt-4",
    skills_path="./skills",
    debug=True  # Enable debug logging
)

agent = HermesAgent(config)

# Check loaded skills
print(agent.list_skills())
```

### High Token Usage

```python
from hermes_agent import HermesAgent, Config, MemoryConfig

# Optimize memory retrieval
memory_config = MemoryConfig(
    max_episodic_context=5,  # Limit conversation history
    semantic_relevance_threshold=0.7,  # Only retrieve relevant memories
    consolidation_frequency="daily"  # Compress old memories
)

config = Config(
    model="gpt-4",
    memory_config=memory_config,
    max_tokens=2000  # Limit response length
)

agent = HermesAgent(config)
```

### Tool Execution Failures

```python
from hermes_agent import HermesAgent, Config, ToolConfig

tool_config = ToolConfig(
    timeout_seconds=30,
    retry_attempts=3,
    error_handling="graceful",  # vs "strict"
    log_tool_calls=True
)

config = Config(
    model="gpt-4",
    tool_config=tool_config
)

agent = HermesAgent(config)
```

### Rate Limiting Issues

```python
from hermes_agent import HermesAgent, Config

config = Config(
    model="gpt-4",
    rate_limit_rpm=20,  # Requests per minute
    backoff_strategy="exponential",
    retry_on_rate_limit=True
)

agent = HermesAgent(config)
```

## Best Practices

1. **Start Simple**: Begin with basic configuration and add complexity as needed
2. **Enable Memory**: Hermes's strength is learning over time - enable all memory systems
3. **Curate Skills**: Review auto-created skills periodically and refine them
4. **Set Constraints**: Always configure safety constraints for production use
5. **Monitor Token Usage**: Use memory consolidation to manage costs
6. **Version Skills**: Export and version control important skills
7. **Use Teams Wisely**: Specialized agents work better than one generalist for complex tasks
8. **Provide Feedback**: The more feedback in the loop, the better Hermes learns

## Resources

- Official Documentation: https://hermes-agent.nousresearch.com/docs/
- GitHub Repository: https://github.com/NousResearch/hermes-agent
- Orange Book Guide: https://github.com/alchaincyf/hermes-agent-orange-book
- Community Discord: Check repository for link
- Nous Research: https://nousresearch.com/
