## Description: <br>
Route any query by intent across code, analysis, creative, realtime, and general requests, returning a DeepSeek V4 Flash recommendation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[certainlogicai](https://clawhub.ai/user/certainlogicai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to classify a prompt by intent and receive a low-cost model recommendation before deciding how to answer or route the request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake the recommendation for a live model router or cache-backed execution path. <br>
Mitigation: Treat the output as a local classification and routing recommendation only; wire any model calls or caching separately and verify their behavior. <br>
Risk: Realtime, sensitive, high-stakes, or ambiguous queries may need fresher data or stronger review than a static keyword classifier can provide. <br>
Mitigation: Use additional judgment, retrieval, verification, or escalation before acting on these recommendations in high-impact contexts. <br>


## Reference(s): <br>
- [Smart Router Intents on ClawHub](https://clawhub.ai/certainlogicai/smart-router-intents) <br>
- [Publisher profile](https://clawhub.ai/user/certainlogicai) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, guidance] <br>
**Output Format:** [JSON object with intent, tier, model, cost, latency, and reasoning fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local deterministic classifier; does not call models, fetch live data, persist data, or mutate user resources.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
