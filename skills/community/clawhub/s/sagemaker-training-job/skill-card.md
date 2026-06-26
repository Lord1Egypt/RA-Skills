## Description: <br>
Submit ML training jobs to AWS SageMaker by packaging code, uploading it to S3, launching GPU or CPU training instances, polling job status, and downloading artifacts for common ML frameworks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zyyhhxx](https://clawhub.ai/user/zyyhhxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ML engineers use this skill to move training workloads from a local environment to AWS SageMaker, including source packaging, job submission, status polling, artifact download, cost checks, and smoke testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper scripts can create billable SageMaker training jobs and use AWS credentials. <br>
Mitigation: Use a dedicated AWS profile or short-lived role, least-privilege IAM policies, scoped iam:PassRole, a dedicated S3 bucket, and review --dry-run output before submitting. <br>
Risk: Broad source directories can upload unintended local files to S3 as part of the training package. <br>
Mitigation: Set --source-dir to a narrow project directory, review the packaged file list during dry run, and keep secrets outside the source tree. <br>
Risk: Downloaded model archives are automatically extracted when model.tar.gz is present. <br>
Mitigation: Use a dedicated output directory and avoid downloading or auto-extracting untrusted model archives unless the behavior is disabled or patched. <br>


## Reference(s): <br>
- [SageMaker Training - Setup Guide](references/setup.md) <br>
- [SageMaker Training Script Guide](references/training-scripts.md) <br>
- [Project homepage](https://github.com/zyyhhxx/OpenClawSkill-sagemaker-training-job) <br>
- [AWS SageMaker pricing](https://aws.amazon.com/sagemaker/pricing/) <br>
- [ClawHub skill page](https://clawhub.ai/zyyhhxx/sagemaker-training-job) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash, JSON, IAM policy examples, and Python helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May submit AWS API requests and create local downloaded artifact files when the helper scripts are run.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
