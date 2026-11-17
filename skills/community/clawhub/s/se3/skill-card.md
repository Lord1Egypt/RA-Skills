## Description:

SE(3) rigid body transformation library for 3D rotation and translation operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyendt](https://clawhub.ai/user/wangyendt)

### License/Terms of Use:


## Use Case:

Developers and robotics engineers use this skill as reference guidance for working with SE(3) poses, camera transformations, SLAM systems, and 3D rigid body motion operations in pywayne.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill references the pywayne package and related SE(3) functions that must exist in the user's environment.

Mitigation: Install only if you use or trust the referenced pywayne package and verify package availability before relying on generated code.

Risk: Incorrect pose conventions, frame direction, or angle units can produce misleading robotics, camera, or SLAM results.

Mitigation: Review generated transformations against the documented radians, 6D vector, and right-multiply conventions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangyendt/skills/se3)
- [Publisher profile](https://clawhub.ai/user/wangyendt)

## Skill Output:

**Output Type(s):** [guidance, code]

**Output Format:** [Markdown with Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides function names, input and output conventions, and usage patterns for SE(3) rigid body transformations.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
