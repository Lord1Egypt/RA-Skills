## Description: <br>
Provides benchmark testing, A/B testing, performance regression detection, and simulation environment testing for agent evaluation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent evaluators use this skill to benchmark agent behavior, compare prompt or implementation variants with A/B tests, detect performance regressions over time, and run simulated scenarios before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scenario files and local paths may be influenced by untrusted prompts or inputs. <br>
Mitigation: Use trusted scenario files and avoid allowing untrusted prompts to choose local paths. <br>
Risk: Benchmark or A/B callbacks could repeatedly act on real agents, services, or accounts. <br>
Mitigation: Point callbacks at mocks, test agents, or test accounts unless repeated production actions are intentional. <br>
Risk: Evaluation results may be mistaken for production readiness without human review. <br>
Mitigation: Install and run the suite in development or test projects, then review benchmark, regression, and simulation results before deployment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/yuyonghao-agent-eval-suite) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/yuyonghao-123) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with JavaScript and shell examples; evaluation APIs return structured result objects and reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce benchmark summaries, A/B test outcomes, regression findings, simulation results, and Markdown or HTML reports.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
