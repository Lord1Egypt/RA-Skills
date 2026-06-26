## Description: <br>
Statically analyze C struct member offsets through code reading to calculate memory layouts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LittleEnough](https://clawhub.ai/user/LittleEnough) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers, reverse engineers, debuggers, and security researchers use this skill to inspect C header files, resolve type sizes and alignment rules, and calculate struct member offsets without running code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires inspecting local C/C++ source headers, which may contain proprietary or sensitive implementation details. <br>
Mitigation: Use it only in workspaces where the agent is permitted to read the target headers and related source files. <br>
Risk: Manual struct offset calculations can be wrong when platform width, packing pragmas, unions, or conditional compilation are missed. <br>
Mitigation: Confirm target platform assumptions, compiler packing behavior, and relevant preprocessor conditions before relying on an offset table. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/LittleEnough/struct-offset-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with grep-style search commands and struct offset tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs typically include type-size reasoning, padding notes, platform assumptions, and hexadecimal member-offset tables.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
