## Description: <br>
减肥项目管理与数据分析（升级版 v2.0）。支持通用用户名格式 U{用户 ID}-{用户名}-YYYY-MM.md，修复口头归档问题，增加数据完整性自动检查，热量识别与估算，趋势分析与建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hadais](https://clawhub.ai/user/hadais) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to track weight-management records, meals, calories, steps, sleep, and progress in local Markdown files. It can estimate calories from manual food descriptions or optional food-recognition APIs, calculate TDEE, check record completeness, and produce trend analysis and suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive health tracking data, including weight, meals, steps, sleep, and possibly chat-history context. <br>
Mitigation: Use a dedicated local storage folder, limit access to user-authorized paths, and confirm before allowing the skill to write health records. <br>
Risk: Optional food-recognition/API features may send food images or descriptions to a provider selected outside the skill. <br>
Mitigation: Keep optional API features disabled unless the provider is trusted, or use manual food entry instead. <br>
Risk: Weight-management suggestions and calorie estimates may be inaccurate or inappropriate for a user's medical condition. <br>
Mitigation: Treat outputs as informational tracking support and consult a qualified clinician or nutrition professional for health decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hadais/weight-management) <br>
- [Food calorie reference](references/food-calories.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown and text responses with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or update user-authorized local Markdown health records and may return TDEE calculations, calorie estimates, completeness checks, trend analysis, and weight-management suggestions.] <br>

## Skill Version(s): <br>
2.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
