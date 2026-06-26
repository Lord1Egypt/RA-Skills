## Description: <br>
End-to-end builder for AI-based Subseasonal-to-Seasonal (S2S) forecasting systems that generates runnable PyTorch code for FuXi-style, FengWu-style, and AIFS-inspired models including CRPS-based probabilistic training. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manmeet3591](https://clawhub.ai/user/manmeet3591) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Climate AI researchers, Earth system ML engineers, research labs, and advanced ML developers use this skill to scaffold local PyTorch S2S forecasting models, training loops, CRPS losses, ERA5-style preprocessing, evaluation scripts, distributed training setups, and inference pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated training, preprocessing, inference, or multi-GPU code may be incorrect, expensive, or unsuitable for the user's local compute environment. <br>
Mitigation: Review generated code before running it, test on small samples first, and verify resource limits and distributed-training settings. <br>
Risk: Forecasting workflows may rely on licensed or restricted datasets such as ERA5. <br>
Mitigation: Confirm dataset access rights and license terms before using generated data pipelines. <br>


## Reference(s): <br>
- [S2S Forecasting Expert on ClawHub](https://clawhub.ai/manmeet3591/s2s-forecasting-expert) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with PyTorch code blocks, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated code runs locally and should be reviewed and adapted before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
