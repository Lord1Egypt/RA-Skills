## Description: <br>
Weekly Meal Planner generates a seven-day breakfast, lunch, and dinner plan plus a shopping list from people count, budget, and taste preference inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to produce a weekly meal plan, estimated shopping list, and budget summary for households based on family size, budget, and preferred taste profile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the script creates or overwrites menu_plan.json in the directory where it is run, which may expose household budget or preference details in shared or sensitive folders. <br>
Mitigation: Run the skill from a private working directory and review or remove menu_plan.json after use if the plan contains sensitive household details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/weekly-meal-planner) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands] <br>
**Output Format:** [Terminal text plus a local menu_plan.json file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or overwrites menu_plan.json in the current working directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports v1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
