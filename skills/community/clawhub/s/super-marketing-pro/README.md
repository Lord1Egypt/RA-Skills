# Super Marketing Pro 🚀

> A full-stack B2B marketing execution skill for AI Agents, equivalent to a 10-person agency team.

**Super Marketing Pro** is a comprehensive, LLM-powered marketing skill designed for AI agents (like Manus and OpenClaw). It transforms your AI agent into a complete B2B marketing team capable of strategic planning, content generation, multi-platform repurposing, outbound email sequences, and data reporting.

## 🌟 Core Capabilities

This skill provides a 6-stage Super Workflow for marketing execution:

1. **Strategy First (`strategy_builder.py`)**: Generate Ideal Customer Profiles (ICP), buyer personas, and brand messaging pillars using LLM reasoning.
2. **Content Creation (`seo_analyzer.py`)**: Build LLM-powered Topic Cluster strategies and long-form pillar content.
3. **Multi-Platform Repurposing (`content_repurposer.py`)**: Transform a single long-form document into a complete matrix for LinkedIn, X (Twitter), TikTok/Douyin, and Xiaohongshu.
4. **Distribution (`hashtag_generator.py` & `content_calendar.py`)**: Generate platform-specific hashtag matrices and weekly/monthly publishing schedules.
5. **Conversion (`email_sequence_generator.py`)**: Create 5-stage high-converting cold email sequences (including breakup emails).
6. **Monitoring & Reporting (`competitor_monitor.py` & `data_reporter.py`)**: Generate batch competitor battle cards and multi-month cross-platform ROI reports.

## 📦 What's Included

- **9 Executable Scripts**: Fully functional Python scripts with built-in LLM integration (via `llm_utils.py` with exponential backoff).
- **9 Reference Documents**: A complete knowledge base covering ABM frameworks, funnel strategies, YouTube SEO, Douyin algorithms, and more.
- **Agent Instructions**: Clear `SKILL.md` and `AGENT.md` files optimized for AI agent consumption and execution.

## 🛠️ Installation & Usage

### For Manus Users
1. Copy the `SKILL.md` file to your `/home/ubuntu/skills/super-marketing-pro/` directory.
2. Ensure the `scripts/` and `references/` directories are placed alongside it.
3. Trigger the skill by asking Manus to: "Generate a marketing strategy", "Write a social media content matrix", or "Create a cold email sequence".

### For OpenClaw Users
This skill is fully compatible with OpenClaw. It includes the required `_meta.json` file.
1. Place the repository in your OpenClaw skills directory.
2. Ensure `openai` is installed (`pip install openai`).
3. Set your `OPENAI_API_KEY` environment variable.

## ⚙️ Requirements

- Python 3.11+
- `openai` >= 1.0.0 (See `requirements.txt`)
- An OpenAI-compatible API key (defaults to `gemini-3.0-flash`, configurable in `scripts/llm_utils.py`)

## 📝 License

MIT License
