---
name: iso-42001-ai-governance
description: AI governance readiness and gap assessment using ISO/IEC 42001:2023. Evaluate AI management-system practices for risk management, accountability, transparency, security, and continuous improvement.
---

# ISO 42001 AI Governance Audit

This skill enables AI agents to perform a comprehensive **AI governance readiness and gap assessment** based on **ISO/IEC 42001:2023** - the international standard for Artificial Intelligence Management Systems (AIMS).

ISO 42001 provides a framework for responsible development, deployment, and use of AI systems, addressing risks, ethics, security, transparency, and regulatory compliance.

Use this skill to evaluate whether AI projects follow international best practices, manage risks effectively, and maintain ethical standards throughout the AI lifecycle.

**Certification boundary**: This skill can prepare evidence and identify gaps, but it is not a certification audit. Do not claim ISO/IEC 42001 conformance unless a qualified auditor or certification process verifies it.

Combine with security audits, code reviews, or ethical AI assessments for comprehensive AI system evaluation.

## When to Use This Skill

Invoke this skill when:
- Developing or integrating AI systems
- Ensuring AI governance and compliance
- Managing AI risks and ethical concerns
- Preparing for AI regulatory requirements (EU AI Act, etc.)
- Auditing existing AI implementations
- Establishing AI governance frameworks
- Responding to AI security or bias incidents
- Planning responsible AI deployment
- Documenting AI systems for stakeholders

## Inputs Required

When executing this audit, gather:

- **ai_system_description**: Detailed description (purpose, capabilities, data used, users affected, deployment context) [REQUIRED]
- **use_case**: Specific application (e.g., hiring tool, medical diagnosis, content moderation) [REQUIRED]
- **risk_category**: High-risk, limited-risk, or minimal-risk per EU AI Act classification [OPTIONAL but recommended]
- **existing_documentation**: Technical docs, data sheets, model cards, risk assessments [OPTIONAL]
- **stakeholders**: Who develops, deploys, uses, and is affected by the AI [OPTIONAL]
- **regulatory_context**: Applicable laws (GDPR, EU AI Act, industry regulations) [OPTIONAL]
- **impact_assessment_context**: Existing or needed AI impact assessments, especially for systems affecting individuals, groups, or society [OPTIONAL]

## ISO 42001 Framework Overview

ISO 42001 is structured around **10 key clauses** plus supporting annexes:

### Core Clauses

1. **Scope** - Define AIMS boundaries
2. **Normative References** - Related standards
3. **Terms and Definitions** - AI terminology
4. **Context of Organization** - Internal/external factors
5. **Leadership** - Management commitment and roles
6. **Planning** - Objectives and risk management
7. **Support** - Resources, competence, communication
8. **Operation** - AI system lifecycle management
9. **Performance Evaluation** - Monitoring and measurement
10. **Improvement** - Continual enhancement

### Key ISO 42001 Principles

#### 1. Risk-Based Approach
- Identify, assess, and mitigate AI-specific risks
- Consider technical, ethical, legal, and social risks
- Proportionate controls based on risk level

#### 2. Ethical AI
- Fairness and non-discrimination
- Transparency and explainability
- Human oversight and control
- Privacy and data protection
- Accountability

#### 3. Lifecycle Management
- Design → Development → Deployment → Monitoring → Decommissioning
- Continuous evaluation and improvement
- Documentation throughout

#### 4. Stakeholder Engagement
- Involve affected parties
- Clear communication about AI use
- Mechanisms for feedback and redress

### Related ISO AI Standards

Use ISO/IEC 42001 as the management-system anchor. When the request focuses on social, human, environmental, or lifecycle impact assessment, also reference **ISO/IEC 42005:2025** as a companion standard for AI system impact assessments. When the request focuses on risk methodology, consider ISO/IEC 23894 as supporting guidance.

---

## Audit Procedure

Work through seven steps, each mapped to ISO 42001 clauses. The full control-by-control
checklists — evaluation questions, scoring rubrics, example risks, and the seven AI
lifecycle stages — live in **[`references/audit-procedure.md`](references/audit-procedure.md)**.
Read the section for the step you are on rather than loading the whole file at once.

| Step | Focus | ISO 42001 Clause | Est. |
|------|-------|------------------|------|
| 1. Context & Scope | AIMS boundaries, stakeholders, EU AI Act risk classification | 4 | 15 min |
| 2. Leadership & Governance | Management commitment, AI policy, roles & responsibilities | 5 | 20 min |
| 3. Planning & Risk Management | Risk categories, assessment process, AI objectives | 6 | 30 min |
| 4. Support & Resources | Resources, competence, awareness, communication, documentation | 7 | 20 min |
| 5. Operation (AI Lifecycle) | Design → data → development → validation → deployment → monitoring → decommissioning | 8 | 40 min |
| 6. Performance Evaluation | KPIs, internal audit, management review | 9 | 20 min |
| 7. Improvement | Nonconformity, corrective action, continual improvement (PDCA) | 10 | 15 min |

For each step: evaluate the documented controls, record evidence vs. gaps, assign a
clause score (0–10), and carry the findings into the report.

---

## Output Format

Assemble findings into the standard ISO 42001 audit report. The copy-ready template
and a clause-by-clause self-assessment checklist are in
**[`references/report-template.md`](references/report-template.md)**.

The report covers, in order:

1. **Executive Summary** — overall conformance, per-clause status table, risk classification, top 5 critical findings, positive highlights
2. **Detailed Findings** — clause-by-clause analysis with evidence, gaps, and recommendations
3. **Risk Assessment Summary** — critical/high risks with controls, owners, and deadlines
4. **Compliance Roadmap** — phased actions (0–3 / 3–6 / 6–12 months)
5. **Documentation Requirements** — missing artifacts to create
6. **Recommendations by Stakeholder** — leadership, AI teams, legal/compliance, operations
7. **Next Steps** — immediate through long-term
8. **Appendices** — checklist, risk register, glossary, references

---

## Best Practices

1. **Start with Risk Assessment**: Prioritize based on AI risk level
2. **Document Everything**: ISO 42001 requires extensive documentation
3. **Engage Stakeholders Early**: Include affected parties in governance
4. **Use Existing Frameworks**: Leverage NIST AI RMF, EU AI Act requirements
5. **Automate Monitoring**: Build MLOps with governance built-in
6. **Train Your Team**: ISO 42001 requires competent personnel
7. **Regular Audits**: Don't wait for problems—proactive reviews
8. **Learn from Incidents**: Every issue is improvement opportunity
9. **Balance Innovation and Safety**: Responsible AI doesn't mean no AI
10. **Seek Independent Review When Needed**: Third-party ISO 42001 certification can add credibility, but this skill only supports readiness and evidence preparation

---

## Regulatory Alignment

ISO 42001 aligns with major AI regulations:

**EU AI Act:**
- Risk classification framework
- High-risk AI obligations
- Transparency requirements
- Conformity assessment

**GDPR:**
- Data protection by design
- Privacy impact assessments
- Data subject rights
- Lawful processing

**NIST AI RMF:**
- Govern, Map, Measure, Manage functions
- Risk-based approach
- Trustworthy AI characteristics

**ISO/IEC 42005:2025:**
- AI system impact assessment
- Human, social, and environmental impacts across the lifecycle
- Transparent documentation of foreseeable impacts

**Sector-Specific:**
- Healthcare: FDA AI/ML guidance, MDR
- Finance: Model Risk Management (SR 11-7)
- Employment: EEOC AI guidance

---

## Common Pitfalls

1. **"We'll add governance later"** - Build it in from the start
2. **Treating ISO 42001 as one-time exercise** - It's continual
3. **Documentation without implementation** - Must be operational
4. **Ignoring low-risk AI** - Even minimal-risk needs baseline governance
5. **No stakeholder engagement** - Affected parties must be involved
6. **Insufficient resources** - Responsible AI requires investment
7. **Lack of monitoring** - Deploy-and-forget is non-compliant
8. **No incident response plan** - When AI fails, you need a plan
9. **Training as checkbox** - Teams must truly understand responsible AI
10. **Copying templates without customization** - Tailor to your context

---

## Version

1.0 - Initial release based on ISO/IEC 42001:2023

---

**Remember**: ISO 42001 is about building trustworthy AI systems through systematic risk management and governance. It's not a barrier to innovation—it's a framework for responsible innovation that protects both organizations and the people affected by AI.

