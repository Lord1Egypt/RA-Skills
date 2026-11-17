## Description:

Submit ML training jobs to AWS SageMaker by packaging code, uploading to S3, launching managed CPU or GPU instances, polling status, estimating cost, and downloading artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zyyhhxx](https://clawhub.ai/user/zyyhhxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ML engineers use this skill to move training workloads from a local machine to AWS SageMaker when they need managed CPU or GPU compute. It helps prepare SageMaker-compatible training scripts, configure IAM and S3, submit jobs, monitor results, and retrieve artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Artifact download and extraction could overwrite local files or process unsafe archive members.

Mitigation: Use --no-download unless the job output is trusted, and do not extract artifacts from untrusted training code or shared S3 prefixes until paths and archive members are validated.

Risk: Broad source packaging could upload unintended private files.

Mitigation: Run dry-run from a tightly scoped source directory, avoid broad project roots, and use a dedicated S3 bucket with least-privilege temporary AWS credentials.

## Reference(s):

- [SageMaker Training Setup Guide](references/setup.md)
- [SageMaker Training Script Guide](references/training-scripts.md)
- [Project homepage](https://github.com/zyyhhxx/OpenClawSkill-sagemaker-training-job)
- [AWS SageMaker pricing](https://aws.amazon.com/sagemaker/pricing/)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands, JSON IAM policy examples, and Python script references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can submit AWS API calls through bundled Python scripts and may create local downloaded artifact files when download is enabled.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
