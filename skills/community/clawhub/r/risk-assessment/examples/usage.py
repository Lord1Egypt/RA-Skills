"""
Example: Using the Risk Assessment skill with the Anthropic API.

This demonstrates how to use a standalone skill as a system prompt
with optional framework appendix injection.
"""
import anthropic
import json
from pathlib import Path


def load_skill(skill_path: str, framework_path: str | None = None) -> str:
    """Load a skill file and optionally append a framework appendix."""
    skill_text = Path(skill_path).read_text()
    if framework_path:
        framework_text = Path(framework_path).read_text()
        skill_text += "\n\n" + framework_text
    return skill_text


def run_risk_assessment(context: str, framework: str | None = None) -> dict:
    """Run a risk assessment on the given context."""
    client = anthropic.Anthropic()

    # Load skill with optional framework
    skill_dir = Path(__file__).parent.parent
    framework_path = None
    if framework:
        framework_path = str(skill_dir.parent.parent / "frameworks" / f"{framework}.md")

    system_prompt = load_skill(
        str(skill_dir / "SKILL.md"),
        framework_path,
    )

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        temperature=0.1,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": f"Perform a comprehensive risk assessment based on the following context:\n\n{context}",
        }],
    )

    # Extract JSON from response
    response_text = message.content[0].text
    # Find JSON block in response
    if "```json" in response_text:
        json_start = response_text.index("```json") + 7
        json_end = response_text.index("```", json_start)
        return json.loads(response_text[json_start:json_end])
    return json.loads(response_text)


if __name__ == "__main__":
    context = """
    Our organization is a mid-size healthcare provider with 500 employees.
    Key systems include:
    - EHR system accessed via web portal (username/password only, no MFA)
    - Patient billing system on an on-premise server running Windows Server 2019
    - Email system is Microsoft 365 with basic security defaults
    - Backup tapes stored in an unlocked closet at the main office
    - No formal incident response plan documented
    - Annual security training for clinical staff only
    """

    result = run_risk_assessment(context, framework="nist-csf-2.0-controls")
    print(json.dumps(result, indent=2))
