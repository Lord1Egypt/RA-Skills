# FTM Design Workflow in RSAD

This reference covers the step-by-step process for designing a new FTM interface using RSAD,
from receiving a JIRA ticket through to handing off design artifacts for ACE implementation.

---

## Step 1: Understand the Requirement

Before opening RSAD, answer these questions from the JIRA ticket and Confluence:

1. **What payment type?** (SWIFT MT103, ISO 20022 pacs.008, ACH, CHAPS, etc.)
2. **Which FTM pattern?** (See `patterns-artifacts.md` — select from 9.1–9.15)
3. **Inbound or outbound?** Or both (bilateral)?
4. **What external system?** (New SP? Or modify existing SP?)
5. **What transport?** (MQ, HTTP, FILE)
6. **What mapper technology?** (ESQL / Java / XSLT / WTX — see `mapping-design.md`)
7. **New FSM or extend existing?** (Use generic FSMs if possible)
8. **Error handling requirements?** (What alert states are needed?)

---

## Step 2: Identify or Create the Service Participant

A **Service Participant (SP)** represents either:
- An external financial institution or system (bank, clearinghouse, gateway)
- An internal FTM service (e.g., a separate payment rail)

### New SP checklist:
- [ ] Name: `<INSTITUTION_CODE>_<RAIL>` (e.g., `SWIFT_MT103`, `FPS_OUTBOUND`)
- [ ] Type: BANK / CLEARINGHOUSE / INTERNAL
- [ ] Role: maps to ISO 20022 party role (e.g., `DEBTOR_AGENT`, `CREDITOR_AGENT`)
- [ ] Status: ACTIVE (set INACTIVE until go-live)
- [ ] Channels: one per direction per format

### SP configuration in RSAD class diagram:
```
Class: ServiceParticipant
  «stereotype: FTM_SP»
  + sp_name: String = "SWIFT_OUTBOUND"
  + sp_type: String = "BANK"
  + role: String = "CREDITOR_AGENT"
  + active: Boolean = true

Class: Channel
  «stereotype: FTM_Channel»
  + channel_name: String = "SWIFT_MT103_OUT"
  + direction: String = "OUTBOUND"
  + format: String = "SWIFT_MT103"
  + mapper_subflow: String = "MapOutSwiftMT103"
  + output_queue: String = "FTM.SWIFT.OUT"
  + transport: String = "MQ"
```

---

## Step 3: Draw the Use Case Diagram

Purpose: establish WHO does WHAT at the highest functional level.

Template for a new interface:
```
Actors: [External System], [FTM Operator], [Receiving System]
Use Cases (inside FTM boundary):
  - Receive [Payment Type] Message
  - Validate and Map to ISF
  - Route Transaction
  - Deliver to [Receiving System]
  - Handle Processing Error        «include»
  - Notify Operator of Alert       «include»
```

Rules:
- Every external actor has at least one primary use case
- Include error handling as a shared use case via `«include»`
- Do not model implementation details here — keep it functional

---

## Step 4: Draw the Functional Sequence Diagram

This is the primary design artifact reviewed by architects and business analysts.

**Lifelines to include:**
1. External System (sending)
2. PT Flow (Physical Transmission — entry point ACE flow)
3. Inbound Mapper (ACE subflow)
4. DB2 (FTM database)
5. MQ Event Queue
6. EP Flow (Event Processing — orchestration ACE flow)
7. Action Subflow (ACE subflow executing FSM action)
8. External System (receiving, if outbound)

**Mandatory message sequence (Pattern 9.1 Outbound as example):**
```
1. ExternalSystem → PTFlow: Inbound raw message
2. PTFlow → Mapper: invoke mapper subflow
3. Mapper → PTFlow: return ISF document
4. PTFlow → DB2: INSERT Transmission (state=RECEIVED)
5. PTFlow → DB2: INSERT Transaction (state=INITIAL)
6. PTFlow → MQEventQueue: PUT E_MpInMappingComplete
7. MQEventQueue → EPFlow: GET event
8. EPFlow → DB2: SELECT FSM transitions for state=INITIAL, event=E_MpInMappingComplete
9. EPFlow → ActionSubflow: Execute ValidateAndRoute action
10. ActionSubflow → DB2: UPDATE Transaction state=VALIDATED
11. ActionSubflow → MQOutbound: PUT outbound message
12. ActionSubflow → MQEventQueue: PUT E_TxnOutCreated
```

**Error path (always include):**
```
3a. Mapper fails → PTFlow raises E_MpInMappingAborted
4a. EPFlow transitions Transaction to PMP_Alert state
5a. OAC shows alert to operator
```

---

## Step 5: Design the FSM(s)

See `fsm-design.md` for the full FSM reference. Summary of what to decide here:

- **Object type**: Transaction FSM? Transmission FSM? Both?
- **SUBTYPE**: Unique identifier for this interface's FSM (registered in `VALUE` table)
- **OBJECT_SELECTION_TEMPLATE**: SQL WHERE clause selecting objects for this FSM
- **States**: Map each processing stage to a named state
- **Events**: Use standard events where possible (see standard events table in `fsm-design.md`)
- **Actions**: Name of ACE subflow to execute (follows naming convention: `Act<Name>`)
- **Stereotypes**: Apply `PMP_Alert`, `PMP_Terminal` correctly

---

## Step 6: Select Mapping Technology

The mapping decision is made during design and documented in RSAD before ACE implementation.

| Technology | Use When |
|---|---|
| **ESQL** | Simple to moderate transforms; ISF field-by-field mapping; standard choice |
| **Java** | Complex logic, external library calls, recursive parsing |
| **XSLT** | XML-to-XML structural transforms; stylesheet-based |
| **WTX/ITX** | Very large/complex transforms; legacy integration; batch file processing |

See `mapping-design.md` for full guidance.

---

## Step 7: Export SQL Configuration

After modeling SP, Channel, and FSM in RSAD:

1. **Right-click model** → IBM FTM → Export Configuration
2. Review each generated SQL file:

```sql
-- sp_config.sql
INSERT INTO SERVICE_PARTICIPANT_BASE
  (SP_NAME, SP_TYPE, ROLE, STATUS, ...)
VALUES
  ('SWIFT_OUTBOUND', 'BANK', 'CREDITOR_AGENT', 'INACTIVE', ...);

-- channel_config.sql
INSERT INTO CHANNEL_BASE
  (CHANNEL_NAME, SP_NAME, DIRECTION, FORMAT, MAPPER, OUTPUT_QUEUE, ...)
VALUES
  ('SWIFT_MT103_OUT', 'SWIFT_OUTBOUND', 'OUT', 'SWIFT_MT103', 'MapOutSwiftMT103', 'FTM.SWIFT.OUT', ...);

-- fsm_config.sql
INSERT INTO FSM (FSM_NAME, OBJECT_TYPE, SUBTYPE, OBJECT_SELECTION_TEMPLATE)
VALUES ('TxnFSM_SWIFT_OUT', 'TRANSACTION', 'SWIFT_OUTBOUND_TXN', 'SUBTYPE = ''SWIFT_OUTBOUND_TXN''');

INSERT INTO FSM_STATE_REL (FSM_NAME, STATE_NAME, STATE_TYPE)
VALUES ('TxnFSM_SWIFT_OUT', 'INITIAL', 'NORMAL');
-- ... more states

INSERT INTO FSM_TRANSITION (FSM_NAME, FROM_STATE, EVENT_TYPE, ACTION, TO_STATE, TRANSITION_PRIORITY)
VALUES ('TxnFSM_SWIFT_OUT', 'INITIAL', 'E_MpInMappingComplete', 'ActValidateAndRoute', 'VALIDATED', 1);
-- ... more transitions
```

3. Register new SUBTYPE in VALUE table:
```sql
INSERT INTO VALUE (NAME, VALUE, DESCRIPTION)
VALUES ('ROLE_FOR_TXN_TYPE', 'SWIFT_OUTBOUND_TXN:CREDITOR_AGENT', 'SWIFT outbound transaction type');
```

---

## Step 8: Hand Off to ACE Development

Package and hand off these artifacts for ACE implementation:

| Artifact | Consumed By |
|---|---|
| Functional sequence diagram | ACE developer (flow structure reference) |
| FSM state machine diagram | ACE developer (action subflow list, event names) |
| SQL config scripts | DB2 DBA (import to FTM database) |
| Mapper technology decision | ACE developer (ESQL/Java/WTX implementation) |
| SP/Channel config | ACE developer (queue names, mapper subflow names) |

The ACE developer should not need to make any architectural decisions — RSAD design artifacts
contain all the information needed to implement without ambiguity.

---

## Modifying an Existing Interface

When a JIRA ticket modifies an existing interface (not creating new):

1. Open RSAD and locate the existing SP/FSM model
2. Identify what changed: new state? new event? channel attribute update?
3. Make minimal changes — don't redesign if only one transition changes
4. Re-export only the affected SQL (FSM transitions, channel record, etc.)
5. Apply the delta SQL to DB2 (UPDATE or INSERT the changed rows)
6. Update the sequence diagram if the message flow changed
7. Commit all changed `.emx`/`.uml` files + SQL delta to version control

---

## Design Review Checklist

Before handing off RSAD artifacts for implementation:

- [ ] Use case diagram reviewed with business analyst
- [ ] Functional sequence diagram reviewed with architect
- [ ] FSM covers all paths: happy path, error path, timeout path
- [ ] Every FSM path ends in a terminal state
- [ ] Every error path has a `PMP_Alert` state with Constraints
- [ ] SP and channel names follow naming conventions
- [ ] SQL scripts generated and reviewed (no orphaned FK references)
- [ ] Mapping technology decision documented
- [ ] Artifacts committed to version control
