## Description: <br>
Xiao Chuang You is a Chinese-language lifestyle aesthetics assistant that routes requests across weather, pets, wellness, music, literature, fashion, handcrafts, photography, gardening, objects, seasonal customs, travel, and emotional support topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zcr3344](https://clawhub.ai/user/zcr3344) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for culturally styled lifestyle guidance, recommendations, and routing to specialized subskills for everyday topics such as weather-aware clothing, wellness routines, reading, music, crafts, gardening, travel, and mood support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill broadly activates on ordinary lifestyle and recommendation requests. <br>
Mitigation: Review the trigger scope before installation and disable or narrow activation if it conflicts with other assistant workflows. <br>
Risk: The skill may store user location, wellness, preference, and planning context in workspace memory files. <br>
Mitigation: Inspect memory behavior, avoid entering sensitive personal or medical data, and use the documented deletion workflow when memory should be cleared. <br>
Risk: The skill may query external weather or search services for time-sensitive answers. <br>
Mitigation: Share only the minimum location or query details needed, and verify important travel, price, event, or weather information against primary sources. <br>
Risk: Sleep, diet, acupressure, pet-care, and emotion guidance may be mistaken for professional advice. <br>
Mitigation: Treat those responses as general lifestyle guidance and seek qualified medical, veterinary, or mental health support for diagnosis, treatment, or urgent concerns. <br>
Risk: The skill declares a recurring monthly background memory-check task. <br>
Mitigation: Review scheduled jobs after installation and remove the cron task if background review is not desired. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zcr3344/xiao-chuang-you) <br>
- [Module Index](references/INDEX.md) <br>
- [Capability Matrix](references/capabilities.md) <br>
- [Conversation Flow](references/conversation-flow.md) <br>
- [Data Declaration](references/data-declaration.md) <br>
- [Response Style Guide](references/guidelines.md) <br>
- [Weather System](references/weather.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style conversational responses with recommendations, tables, links, and follow-up questions when appropriate] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local memory files and external weather or search results when the user asks for personalized or time-sensitive guidance.] <br>

## Skill Version(s): <br>
2.2.1 (source: server release evidence, changelog dated 2026-05-26) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
