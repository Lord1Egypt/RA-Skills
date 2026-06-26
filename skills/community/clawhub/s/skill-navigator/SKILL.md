---
name: skill-dashboard-visualizer
description: Provides a highly visual and interactive dashboard for OpenClaw users to easily understand and recall the functionalities of installed skills, featuring a visual overview, capability map, and contextual prompting. Use this skill to generate a comprehensive visualization of all installed skills and their capabilities.
---

# Skill Dashboard Visualizer

This skill is designed to enhance the OpenClaw user experience by providing a clear, interactive, and visually appealing dashboard that summarizes the capabilities of all installed skills. It addresses the common pain point of users finding it difficult to remember and utilize the full potential of their diverse skill set.

## Core Features

This skill integrates three key functionalities to offer a holistic view and interaction model for managing skills:

1.  **Visual Dashboard (可视化看板)**:
    *   **Purpose**: To present a quick, at-a-glance overview of each installed skill.
    *   **Mechanism**: Automatically extracts metadata (name, description) from `SKILL.md` files. Each skill is represented as a card with an icon, category tags, and a concise summary of its core abilities. The design adheres to a **"blue tech style"** for a modern and professional aesthetic.

2.  **Capability Map (能力矩阵)**:
    *   **Purpose**: To illustrate the collective and individual strengths of installed skills across various domains.
    *   **Mechanism**: Utilizes a radar chart to visualize skill coverage in key capability areas such as Data Processing, Creative Writing, Technical Development, Logical Reasoning, and Communication. This helps users identify skill gaps or overlaps.

3.  **Contextual Prompting (智能联想提示)**:
    *   **Purpose**: To proactively suggest relevant skills based on user input, making skill discovery and activation seamless within OpenClaw or other Claw-like applications.
    *   **Mechanism**: Provides a retrieval mechanism for OpenClaw or current Claw-like applications to quickly match the most suitable installed skills when a user asks a question, prompting the user with options like: "您已安装的 [Skill名称] 具备处理此任务的能力，是否启用？"

## Usage Instructions

To generate the skill dashboard, follow these steps:

1.  **Scan Installed Skills**: Execute the `scan_skills.py` script to gather data on all skills present in the `/home/ubuntu/skills/` directory. This script parses each `SKILL.md` file to extract necessary metadata and performs a preliminary heuristic mapping of capabilities.

    ```bash
    python3 /home/ubuntu/skills/skill-dashboard-visualizer/scripts/scan_skills.py
    ```

    The output will be a JSON array containing information for each skill, including its name, description, and a calculated `capabilities` score across different dimensions.

2.  **Generate Dashboard Visualization**: Use the `dashboard_template.md` along with the data obtained from `scan_skills.py` to render the final dashboard. The template is designed to dynamically populate the visual dashboard, capability map (mermaid radar chart), and contextual prompting examples.

    The `dashboard_template.md` expects placeholders to be replaced with actual skill data. For the visual dashboard table, iterate through the scanned skill data. For the capability map, aggregate the capability scores from all skills to form a combined radar chart dataset. For contextual prompting, identify the top skills for each capability dimension.

    *Example of data integration for the template (conceptual):*

    ```python
    import json
    import os

    # Assume skills_data is obtained from scan_skills.py
    # skills_data = json.loads(shell_output_from_scan_skills)

    template_path = "/home/ubuntu/skills/skill-dashboard-visualizer/templates/dashboard_template.md"
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    # Populate Visual Dashboard table (simplified example)
    dashboard_table_rows = []
    for skill in skills_data:
        icon = "💡" # Placeholder, ideally based on skill type
        name = skill.get("name", "N/A")
        description = skill.get("description", "N/A")
        use_cases = "" # Derive from description or specific tags
        dashboard_table_rows.append(f"| {icon} | **{name}** | {description} | {use_cases} |")

    # Replace placeholder in template
    # template_content = template_content.replace("| {{icon}} | **{{name}}** | {{description}} | {{use_cases}} |", "\n".join(dashboard_table_rows))

    # Populate Capability Map (simplified aggregation)
    total_data = sum(s["capabilities"].get("Data", 0) for s in skills_data)
    total_creative = sum(s["capabilities"].get("Creative", 0) for s in skills_data)
    total_tech = sum(s["capabilities"].get("Technical", 0) for s in skills_data)
    total_logic = sum(s["capabilities"].get("Logic", 0) for s in skills_data)
    total_comm = sum(s["capabilities"].get("Communication", 0) for s in skills_data)

    # template_content = template_content.replace("data: [{{data_score}}, {{creative_score}}, {{tech_score}}, {{logic_score}}, {{comm_score}}]",
    #                                           f"data: [{total_data}, {total_creative}, {total_tech}, {total_logic}, {total_comm}]")

    # Further replacements for contextual prompting...

    # Final rendered_dashboard_md can then be displayed or saved.
    ```

## Bundled Resources

-   **`scripts/scan_skills.py`**: A Python script to scan the `/home/ubuntu/skills/` directory, parse `SKILL.md` files, extract metadata, and heuristically map skill capabilities.
-   **`templates/dashboard_template.md`**: A Markdown template for generating the visual dashboard, including placeholders for skill information, a Mermaid radar chart for capability mapping, and examples for contextual prompting.

## Design Considerations

-   **UI/UX**: The dashboard is designed with a "blue tech style" aesthetic, ensuring a clean, modern, and professional look that aligns with user preferences for web applications.
-   **Extensibility**: The `scan_skills.py` script can be easily extended to include more sophisticated parsing logic or integrate with a more robust capability taxonomy.
-   **Interactivity**: While the initial output is Markdown, the design is conducive to being rendered into an interactive web interface (e.g., using React components for cards and a charting library for the radar graph) for a richer user experience.
