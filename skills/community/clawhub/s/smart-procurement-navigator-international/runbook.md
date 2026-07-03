# Smart Procurement Navigator Runbook

## 1. Pre-Deployment Preparation

1. Confirm that the deployment environment can run the intelligent agent platform.
2. Confirm that the collaboration platform is activated and configured.
3. Prepare demonstration procurement documents, technical specification texts, past response document templates, enterprise qualifications, and project case studies.
4. Confirm that the configuration in `agent.yaml` matches the actual environment.
5. Prepare evaluation model templates, response structure templates, and compliance review checklists.

## 2. Startup Checklist

```text
1. Start the intelligent agent
2. Load agent.yaml
3. Load procurement_skills.yaml
4. Connect to the collaboration platform
5. Execute Sample 1 from test_cases/p0_demo_cases.md
6. Verify that the evaluation model, response structure, and review report can be generated normally
7. Verify that logs are written correctly
```

## 3. Pre-Demonstration Checklist

- Collaboration platform account is logged in.
- Smart Procurement Navigator session window is pinned.
- Demonstration procurement documents are ready.
- Demonstration technical specifications or requirements documents are ready.
- Evaluation model and complete response chapter structure templates are loaded.
- Demonstration screen recording files play correctly.
- Output templates render correctly.

## 4. Troubleshooting

| Issue | Resolution |
| --- | --- |
| File parsing error | Switch to pre-generated parsing results |
| File size too large | Use excerpted demonstration files |
| Unstable output | Use fixed prompts and screen recording fallback |
| Risk items missing traceability references | Switch to manually annotated demonstration results |
| Reference file residual false positives | Supplement the knowledge base with reference project names, locations, models, and duration exclusion lists |
| Draft polishing over-correcting formal terminology | Add formal terminology to the whitelist and retain a manual review step |

## 5. Productionization To-Do List

- Integrate with procurement announcement sources or manual forwarding entry points.
- Organize the enterprise qualification database, case study library, and historical response document library.
- Establish evaluation criteria and rejection risk check rule sets.
- Establish standard templates for evaluation models, no-deviation indexes, and evidence chain catalogs.
- Establish rules for templated expression prohibited words, reference file residuals, and key data consistency checks.
- Enhance complete response chapter structure, chart placeholders, and chapter expansion capabilities.
- Integrate with collaboration platform to-do items to generate a bid response task collaboration board.
- Enhance bid response experience capture and material archiving processes.
- Adapt to the submission specifications of electronic bidding systems at various public resource trading centers.
- Establish a government procurement regulation update tracking mechanism.


## v2.0.0 New Operations Guide

### Bid Evaluation Method Deep Analysis
1. Identify the bid evaluation method used in the bidding documents
2. Determine the specific approach of the comprehensive scoring method (fixed score / interval scoring / ranking-based scoring)
3. Analyze the price score calculation formula (average price benchmark / lowest price benchmark / maximum price / ceiling price benchmark)
4. Identify price score anomaly scenarios (malicious low pricing / bid rigging / collusive bidding suspicion)
5. Develop a differentiated quotation strategy

### Electronic Bidding Checklist
- [ ] Confirm CA certificate validity
- [ ] Verify electronic trading platform compatibility
- [ ] Remote cross-location evaluation: Confirm primary/secondary venue arrangements
- [ ] Prepare electronic signatures
- [ ] Prepare encrypted bid documents
- [ ] Submit electronic guarantee / bid bond payment

### Bid Rejection Prevention Checklist
- [ ] Is the bid letter signed and stamped completely?
- [ ] Has the bid bond been paid in full and on time?
- [ ] Does the bid validity period comply?
- [ ] Do the technical specifications substantially comply (no major deviations)?
- [ ] Is the quotation within the maximum price / ceiling price?
- [ ] Is the consortium agreement complete (if applicable)?
- [ ] Is the SME declaration letter compliant (if applicable)?