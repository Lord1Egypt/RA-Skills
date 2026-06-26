# Mapping Design in RSAD

Mapping is the conversion between external message formats and ISF (Internal Standard Format).
The mapping technology decision is made during RSAD design and documented before ACE implementation.

---

## ISF Overview

ISF (Internal Standard Format) is FTM's canonical XML format. All messages inside FTM are in ISF.

- **Namespace**: `http://www.ibm.com/xmlns/prod/ftm/isf/v3`
- **Schema**: `ISF_V3.xsd` — part of the FTM toolkit, included in ACE library projects
- **Root element**: `ISFDocument`
- **Key child elements**:
  - `Header` — message metadata (type, version, correlation IDs)
  - `Body` — payment content (CreditTransfer, DirectDebit, etc.)
  - `Party` — debtor, creditor, agents
  - `Amount` — instructed amount with currency attribute
  - `RemittanceInformation` — optional remittance data

ISF is stored in DB2 `TRANSACTION_BASE.ISF_BLOB` column as a CLOB.

---

## Mapping Strategies

### Pass-Through (no mapping)
- Used when the external format IS ISF, or when no field transformation is needed
- PT Flow passes message through without invoking a mapper
- Rare in practice — most external systems use native formats (SWIFT MT, ISO 20022, etc.)

### Shallow Mapping
- 1:1 field mapping from external format to ISF fields
- No structural transformation; just field renaming/reordering
- Implemented easily in ESQL
- Example: map SWIFT MT103 field 32A (value date + currency + amount) → ISF InstructedAmount

### Deep Mapping
- Structural transformation required (1:N, N:1, conditional logic, loops)
- Typical for batch debulking, format normalization, multi-part messages
- May require Java or WTX for complex cases
- Example: ISO 20022 pain.001 (multi-transaction batch) → multiple ISF CreditTransfer elements

---

## Mapping Technology Selection

| Technology | Strengths | Use When |
|---|---|---|
| **ESQL** | Native ACE language; fast; full ISF/MQ tree access; easy to debug | Default choice for most FTM mappers |
| **Java** | OO design; external library use; recursion; unit testable | Complex business logic; non-XML parsing; external API calls |
| **XSLT** | Declarative; stylesheet-based; no ACE-specific knowledge needed | Pure XML-to-XML structural transforms |
| **WTX/ITX** | IBM Transform Extender; handles EDI, positional, binary formats; batch | Legacy EDI (SWIFT FIN, ACH NACHA), binary/positional formats, very large transforms |

**Decision guide:**
1. Is the source format XML? → Consider ESQL or XSLT
2. Is it flat/positional/binary? → WTX/ITX
3. Simple field mapping? → ESQL
4. Need external library or complex OO logic? → Java
5. Team skill set? → Default to ESQL unless there's a reason not to

---

## Metadata Modeling

FTM's ISF uses `xsd:any` elements in certain places to allow custom metadata. This must be
modeled in RSAD before implementation so the ACE developer knows what fields to set.

### xsd:any Pattern in ISF
```xml
<ISFDocument xmlns="http://www.ibm.com/xmlns/prod/ftm/isf/v3">
  <Header>
    <MessageType>CreditTransfer</MessageType>
    <CorrelationId>TXN-001</CorrelationId>
  </Header>
  <Body>
    <CreditTransfer>
      <InstructedAmount Currency="USD">1000.00</InstructedAmount>
      <Debtor>...</Debtor>
      <Creditor>...</Creditor>
      <!-- xsd:any extension point for channel-specific metadata -->
      <ChannelSpecific>
        <BankReference>REF123</BankReference>
      </ChannelSpecific>
    </CreditTransfer>
  </Body>
</ISFDocument>
```

In RSAD class diagrams, model the `xsd:any` content as a class with attributes, then reference
it from the ISF extension point in the sequence diagram.

---

## ESQL Mapping Patterns

When ESQL is selected, the ACE developer will implement the mapper subflow. The RSAD design
should document which fields map where.

### Standard ESQL mapper structure
```esql
-- Output ISF location (always this path for inbound mapper)
DECLARE ISF_NS NAMESPACE 'http://www.ibm.com/xmlns/prod/ftm/isf/v3';
DECLARE rISF REFERENCE TO OutputLocalEnvironment.PMP.ISF.XMLNSC.{ISF_NS}ISFDocument;

-- Set currency as XML attribute
SET rISF.{ISF_NS}Body.{ISF_NS}CreditTransfer.{ISF_NS}InstructedAmount
    .(XMLNSC.Attribute)Currency = InputRoot.XMLNSC.MT103.Field32A.Currency;

-- Set xsi:type for polymorphic party role
DECLARE XSI_NS NAMESPACE 'http://www.w3.org/2001/XMLSchema-instance';
SET rISF.{ISF_NS}Body.{ISF_NS}CreditTransfer.{ISF_NS}DebtorParty
    .(XMLNSC.Attribute){XSI_NS}:type = 'isf:DebtorRole';

-- Delete empty optional element to prevent ISF validation errors
IF NOT EXISTS(rISF.{ISF_NS}Body.{ISF_NS}CreditTransfer.{ISF_NS}RemittanceInformation.*[]) THEN
    DELETE FIELD rISF.{ISF_NS}Body.{ISF_NS}CreditTransfer.{ISF_NS}RemittanceInformation;
END IF;
```

---

## Mapper Subflow Naming Convention

Document these names in RSAD (in the Channel class model and sequence diagrams):

| Direction | Convention | Example |
|---|---|---|
| Inbound (to ISF) | `MapIn<Format>` | `MapInSwiftMT103`, `MapInPacs008` |
| Outbound (from ISF) | `MapOut<Format>` | `MapOutSwiftMT103`, `MapOutPacs008` |
| Two-way | `Map<Format>` | `MapSwiftMT103` |

The mapper name in the Channel model must exactly match the ACE subflow name deployed in the
integration server. Any mismatch causes the PT Flow to fail with a mapper-not-found error.

---

## Mapping Design Artifact

The RSAD design for mapping should produce:

1. **Mapping Strategy document** (in Confluence / attached to JIRA):
   - Source format and schema reference
   - Target format (ISF version)
   - Technology choice (ESQL / Java / XSLT / WTX)
   - Field-level mapping table

2. **Field mapping table** (minimum required in RSAD design):

| Source Field | Source Path | Target ISF Element | Transformation |
|---|---|---|---|
| Value Date | MT103/Field32A/Date | Header/ValueDate | Format: YYMMDD → YYYY-MM-DD |
| Currency | MT103/Field32A/Currency | InstructedAmount/@Currency | Direct copy |
| Amount | MT103/Field32A/Amount | InstructedAmount/text() | Decimal normalization |
| Sender BIC | MT103/Field51A/BIC | DebtorAgent/FinancialInstitution/BIC | Direct copy |

3. **Sequence diagram annotation**: Mark the mapper invocation in the functional sequence
   diagram with the mapper subflow name and technology.

---

## WTX/ITX Mapping Design

When WTX (IBM Transformation Extender / IBM App Connect Professional) is used:

- The RSAD design should reference the WTX map name and version
- Document input/output schema files (`.dpa` for WTX, or XSD)
- The ACE flow invokes WTX via a Mapping node or Java call
- Include WTX map files in the same repository as ACE projects
- Test maps standalone in WTX Design Studio before ACE integration

WTX is typically used for:
- SWIFT FIN (MT) message parsing (tag-value format)
- ACH NACHA (fixed-position format)
- EDIFACT or X12 EDI
- ISO 8583 (card payment binary format)
