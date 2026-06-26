## Description: <br>
Configure and optimize Vite for development, production builds, and library bundling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill as Vite reference guidance for environment variables, CommonJS compatibility, dependency pre-bundling, path aliases, dev server proxies, static assets, build optimization, library mode, HMR, and SSR configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: VITE_-prefixed environment variables are bundled into client code and can expose values to users. <br>
Mitigation: Review environment variable names before applying guidance and keep secrets in non-client variables such as local server-only configuration. <br>
Risk: Suggested Vite configuration changes can alter production build behavior, dependency bundling, proxying, or SSR output. <br>
Mitigation: Review and test generated configuration changes before applying them to production builds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/vite) <br>
- [Publisher profile](https://clawhub.ai/user/ivangdavila) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown with inline TypeScript configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; requires Node for applicable Vite workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
