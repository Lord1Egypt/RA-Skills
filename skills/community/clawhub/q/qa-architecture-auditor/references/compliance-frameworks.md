# Compliance Frameworks Reference

This document outlines how the QA Architecture Auditor's output aligns with common compliance frameworks.

## IT General Controls (ITGC)

**Focus**: Change management, access control, testing, security scanning, deployment controls.

**Report Alignment**:
- The **ITGC Compliance** section directly lists controls relevant to the codebase.
- Change Management: All code changes must undergo peer review and testing (implied by testing requirements).
- Access Control: Role-based access to repository and production systems is recommended.
- Testing Requirements: Unit tests, integration tests, security scanning are mandated.
- Security Scanning: SAST/DAST and SCA are recommended.
- Deployment Controls: Automated deployments with rollback and approval gates.
- Configuration Management: Infrastructure as code recommended.
- Incident Response: Defined procedures for security incidents.

**Evidence**: The report provides a complete control set that can be used for audit readiness.

## SOC 2 (Service Organization Control 2)

**Focus**: Security, availability, processing integrity, confidentiality, privacy.

**Report Alignment**:
- **Security**: Security testing section covers OWASP Top 10, vulnerability scanning, penetration testing.
- **Availability**: Performance testing recommendations (load, stress, endurance) help ensure availability.
- **Processing Integrity**: API testing, database integrity testing, and functional tests ensure correct processing.
- **Confidentiality**: Cryptography usage review, access control testing, and data protection test cases.
- **Privacy**: Input validation, data handling, and security testing cover privacy aspects.

**Usage**: Map controls and test cases to SOC 2 Trust Services Criteria.

## ISO 27001

**Focus**: Information Security Management System (ISMS), risk assessment, controls.

**Report Alignment**:
- **Risk Assessment**: The risk assessment section identifies high-risk modules and provides a scoring model.
- **Annex A Controls**: Testing strategies cover access control, cryptography, operations security, communications security, system acquisition, development, and maintenance.
- **Asset Management**: Inventory of dependencies and modules.
- **Access Control**: Authentication and authorization testing.
- **Incident Management**: Security testing includes vulnerability scanning and penetration testing.

**Usage**: Integrate the report findings into the ISMS risk treatment plan.

## HIPAA (Health Insurance Portability and Accountability Act)

**Focus**: Protected Health Information (PHI) privacy and security.

**Report Alignment**:
- **Access Controls**: Strict authentication and authorization testing; role-based access.
- **Audit Controls**: Logging and monitoring recommendations (implicit in ITGC).
- **Integrity**: Database integrity testing and data validation.
- **Transmission Security**: Network operations testing and encryption verification.
- **Unique User Identification**: Authentication module testing.

**Usage**: Ensure that all modules handling PHI are subject to rigorous security and access testing.

## GDPR (General Data Protection Regulation)

**Focus**: Personal data protection, privacy by design, data subject rights.

**Report Alignment**:
- **Data Minimization**: Input validation and data handling tests.
- **Security of Processing**: Security testing, encryption, and vulnerability assessment.
- **Data Subject Rights**: Functional testing for data export, deletion, and correction workflows.
- **Breach Notification**: Incident response planning and logging.
- **International Transfers**: Localization and data residency considerations (if applicable).

**Usage**: Validate that applications processing personal data meet GDPR requirements through targeted testing.

---

## How to Use This Document

- Use the risk assessment and security surface mapping to prioritize testing efforts for compliance.
- For each framework, map the recommended test cases to the control objectives.
- Document evidence of test execution to satisfy auditors.
- Regularly re-run the QA Architecture Auditor to maintain compliance posture.
