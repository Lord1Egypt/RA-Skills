# Reference Documentation

This directory contains links to reference documentation for the HL7 IHE PAM Parser skill.

## IHE PAM Documentation

**IHE Patient Administration Management (PAM) 2.10 - French Profile**  
URL: https://github.com/Interop-Sante/ihe.iti.pam.fr  
Description: Official French IHE PAM specification repository containing:
- ADT message event codes (A01-A60)
- Mandatory segment definitions (MSH, EVN, PID, PV1, PV2)
- Field requirements and constraints
- Implementation guides for French healthcare context

**IHE Patient Administration Management (PAM) Profile - International**  
URL: https://profiles.ihe.net/ITI/TF/Volume1/ch-14.html  
Description: International IHE PAM profile specification (English version).

**IHE ITI Technical Framework Volume 2**  
URL: https://profiles.ihe.net/ITI/TF/Volume2/  
Description: Complete IHE ITI Technical Framework covering transactions and content modules.

## HL7 v2.5 Specification

**HL7 Version 2.5 Standard**  
URL: http://www.hl7.eu/HL7v2x/v25/std25/ch02.html  
Description: Official HL7 v2.5 specification covering:
- Message structure and syntax
- Encoding rules and delimiters
- Message control and processing

**HL7 v2.5 Segment Definitions**  
URL: http://www.hl7.eu/HL7v2x/v25/std25/ch03.html  
Description: Complete segment definitions for HL7 v2.5:
- MSH (Message Header)
- EVN (Event Type)
- PID (Patient Identification)
- PV1 (Patient Visit)
- PV2 (Patient Visit - Additional Info)
- And many more...

**HL7 v2.5 Data Types**  
URL: http://www.hl7.eu/HL7v2x/v25/std25/ch02a.html  
Description: Data type definitions used in HL7 v2.5 messages.

**HL7 v2.x Table Values**  
URL: http://www.hl7.eu/HL7v2x/v25/std25/ch02c.html  
Description: Code tables and valid values for HL7 fields.

## Implementation Libraries

**simple-hl7 (Node.js)**  
URL: https://github.com/Bugs5382/node-hl7-client  
Description: Node.js HL7 v2.x client and parser library.

**HAPI HL7 (Java)**  
URL: https://hapifhir.github.io/hapi-hl7v2/  
Description: Java API for HL7 v2.x parsing and generation.

**python-hl7 (Python)**  
URL: https://github.com/johnpaulett/python-hl7  
Description: Python library for parsing HL7 v2.x messages.

## Testing and Validation

**HL7 Soup**  
URL: https://hl7soup.com/  
Description: Online HL7 message validator and parser.

**7Edit**  
URL: http://7edit.com/  
Description: Free HL7 message editor and validation tool.

## Related Internal Documentation

- [HL7 PAM Parser User Guide](../../docs/hl7-pam-parser.md)
- [HPK Parser](../hpk-parser/SKILL.md) - Parse HPK messages (often mapped to HL7)

## Quick Links

| Resource | Type | URL |
|----------|------|-----|
| IHE PAM 2.10 (FR) | Specification | https://github.com/Interop-Sante/ihe.iti.pam.fr |
| IHE PAM Profile (EN) | Specification | https://profiles.ihe.net/ITI/TF/Volume1/ch-14.html |
| HL7 v2.5 Standard | Specification | http://www.hl7.eu/HL7v2x/v25/std25/ch02.html |
| HL7 Segments | Reference | http://www.hl7.eu/HL7v2x/v25/std25/ch03.html |
| HL7 Data Types | Reference | http://www.hl7.eu/HL7v2x/v25/std25/ch02a.html |
| simple-hl7 | Library (Node.js) | https://github.com/Bugs5382/node-hl7-client |
| HAPI HL7 | Library (Java) | https://hapifhir.github.io/hapi-hl7v2/ |
| HL7 Soup | Validator | https://hl7soup.com/ |
| User Guide | Internal | ../../docs/hl7-pam-parser.md |

## Notes

- HL7 v2.5 is widely used in healthcare interoperability
- IHE PAM 2.10 is the French national profile for patient administration
- For complete field definitions, consult the HL7 v2.5 specification
- For French healthcare context, refer to IHE PAM 2.10 (French profile)
- This skill focuses on ADT (Admit, Discharge, Transfer) messages which are the most common PAM messages
