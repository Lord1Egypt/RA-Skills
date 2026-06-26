# FSM Design in RSAD

The Finite State Machine (FSM) is the heart of FTM. Every transaction and transmission in FTM
has a lifecycle defined by an FSM. RSAD is where you model these FSMs, apply stereotypes, and
export them to SQL. This reference covers everything needed to design correct FTM FSMs.

---

## FSM Fundamentals

An FSM in FTM defines: given an object in STATE X, when EVENT Y arrives, execute ACTION Z and
transition to STATE W.

FTM selects the right FSM at runtime using:
- **Object type**: TRANSACTION / TRANSMISSION / BATCH
- **SUBTYPE**: Unique identifier for this interface (e.g., `SWIFT_OUTBOUND_TXN`)
- **OBJECT_SELECTION_TEMPLATE**: SQL WHERE predicate for dynamic selection

The FSM runs inside the Event Processing (EP) flow on ACE. When an event arrives on the MQ
event queue, EP reads the object's current state, queries `FSM_TRANSITION`, selects the matching
transition, and invokes the named ACE action subflow.

---

## DB2 FSM Tables

| Table | Purpose |
|---|---|
| `FSM` | Root: FSM name, object type, subtype, selection template |
| `FSM_STATE_REL` | All states belonging to an FSM |
| `FSM_TRANSITION` | Transition rules: (FSM, FromState, Event) → (Action, ToState) |
| `EVENT_TYPE` | Named events with logging/processing configuration |
| `OBJ_BASE` | Runtime: object's current `STATE`, `SUBTYPE`, `LAST_UPDATED_TS` |

---

## States

### State Types
- **Normal state**: Standard processing state (e.g., `INITIAL`, `VALIDATED`, `SENT`)
- **Alert state** (`PMP_Alert`): Object needs operator intervention; visible in OAC
- **Terminal state** (`PMP_Terminal`): Lifecycle ends here; no further transitions
- **OpsControl state** (`PMP_OpsControl`): Requires operator action; not surfaced as alert

### Naming Conventions
- Use ALL_CAPS with underscores: `WAITING_FOR_ACK`, `SEND_FAILED`
- Terminal states: `COMPLETED`, `CANCELLED`, `REJECTED`
- Alert states: `SEND_FAILED_ALERT`, `MAPPING_ERROR_ALERT`, `TIMEOUT_ALERT`

### Applying Stereotypes in RSAD
1. Draw state in the state machine diagram
2. Right-click state → Add Stereotype
3. Select `PMP_Alert`, `PMP_Terminal`, or `PMP_OpsControl`
4. For `PMP_Alert`: right-click state → Add Tagged Value → `Constraints`
   - Value is comma-separated list: `Cancel,Resubmit,Release`

---

## Transitions

Each transition has:
- **From State**: the current object state
- **Event Type**: the event that triggers this transition
- **Guard (Object Filter)**: optional SQL WHERE predicate on object data
- **Guard (Event Filter)**: optional ESQL boolean condition on event context
- **Action**: ACE subflow name to invoke (or blank for no-op transitions)
- **To State**: state to move the object to after action completes
- **Priority**: integer; lower = higher priority (used when multiple transitions match)

### Transition in RSAD
1. Draw arrow from source state to target state
2. Label arrow: `EventTypeName [Guard] / ActionSubflowName`
3. In transition properties:
   - Event: select from EVENT_TYPE list
   - Guard/Constraint: enter SQL or ESQL expression
   - Effect: enter ACE subflow name

### Transition Guards
```sql
-- Object Filter (SQL): restrict by object data
SUBTYPE = 'SWIFT_OUTBOUND_TXN' AND AMOUNT > 1000000

-- Event Filter (ESQL): inspect event context variables
$ContextNULL{BATCH}           -- true if event has no BATCH context
$Context{SP_NAME} = 'SWIFT'  -- true if event SP_NAME = SWIFT
```

---

## Events

### Standard Events (use these wherever possible)

| Event | Raised By | Meaning |
|---|---|---|
| `E_MpInMappingComplete` | PT Flow | Inbound mapping succeeded |
| `E_MpInMappingAborted` | PT Flow | Inbound mapping failed |
| `E_TransOutSent` | Action Subflow | Outbound transmission was sent |
| `E_TxnOutCreated` | Action Subflow | Outbound transaction created |
| `E_CorrelationSuccessful` | EP Flow | Response correlated to prior request |
| `E_CorrelationFailure` | EP Flow | Correlation failed |
| `E_Heartbeat` | ACE Timer (~60s) | Periodic tick for timeout checking |
| `E_HeartbeatStart` | ACE Startup | Broker startup event |
| `E_ActivityEvent` | Scheduler | Scheduled activity triggered |
| `E_ChildTxnArrived` | Action Subflow | Child transaction arrived (collating) |

### Custom Events
For interface-specific needs, define custom events in `EVENT_TYPE`:
- Name: `E_<Interface>_<Meaning>` (e.g., `E_SWIFT_AckReceived`)
- `EVENT_LOGGING`: Y / N — whether to log event instances
- `RENDER_AS_MESSAGE`: Y (async via MQ queue) / N (inline synchronous)
- `AGGREGATE_THRESHOLD`: max events to aggregate before processing

---

## Generic (Pre-built) FSMs

Always check if a generic FSM covers your use case before designing a custom one.
Generic FSMs are pre-built in FTM and just need SUBTYPE registration.

| Generic FSM | Use For |
|---|---|
| Generic Inbound Transmission FSM | Simple inbound: receive → map → complete |
| Generic Outbound Transmission FSM | Simple outbound: create → send → complete |
| Generic Outbound Transaction FSM | Standard outbound transaction lifecycle |
| Generic Inbound Acknowledgement Transaction FSM | Correlated ACK/NACK processing |

To use a generic FSM:
1. Do not model a custom FSM in RSAD
2. Register the new SUBTYPE in `VALUE` table pointing to the generic FSM
3. Configure `OBJECT_SELECTION_TEMPLATE` in `FSM` table to select objects of this SUBTYPE

---

## FSM Design Patterns by Object Type

### Transaction FSM (most common)
```
[Initial] →(E_MpInMappingComplete / ActValidate)→ [Validated]
[Validated] →(E_TxnOutCreated / ActSendToSP)→ [Sent]
[Sent] →(E_CorrelationSuccessful / ActComplete)→ [Completed] «PMP_Terminal»
[Sent] →(E_CorrelationFailure / ActRaiseAlert)→ [SendFailed_Alert] «PMP_Alert» Constraints: Cancel,Resubmit
[SendFailed_Alert] →(Cancel / ActCancel)→ [Cancelled] «PMP_Terminal»
[SendFailed_Alert] →(Resubmit / ActSendToSP)→ [Sent]
[Initial] →(E_MpInMappingAborted / ActRaiseAlert)→ [MappingError_Alert] «PMP_Alert» Constraints: Cancel,Resubmit
[MappingError_Alert] →(Cancel / ActCancel)→ [Cancelled] «PMP_Terminal»
```

### Transmission FSM (inbound)
```
[Received] →(E_MpInMappingComplete)→ [Processed] «PMP_Terminal»
[Received] →(E_MpInMappingAborted / ActRaiseAlert)→ [MapError_Alert] «PMP_Alert» Constraints: Cancel,Resubmit
[MapError_Alert] →(Cancel)→ [Cancelled] «PMP_Terminal»
[MapError_Alert] →(Resubmit / ActRetryMapper)→ [Received]
```

### Heartbeat/Timeout pattern
```
[Sent] →(E_Heartbeat [timeout < NOW()] / ActTimeout)→ [Timeout_Alert] «PMP_Alert» Constraints: Cancel,Continue
```
Object Filter on Heartbeat transition: `TIMEOUT < CURRENT TIMESTAMP`

---

## FSM Design Checklist

Before exporting from RSAD:

- [ ] FSM name is unique and follows convention: `<ObjectType>FSM_<Interface>`
- [ ] SUBTYPE is unique; registered in `VALUE` table
- [ ] OBJECT_SELECTION_TEMPLATE is correct SQL (test against DB2)
- [ ] Every processing state has at least one outgoing transition
- [ ] Every path terminates at a `PMP_Terminal` state
- [ ] Every error path has a `PMP_Alert` state
- [ ] Every `PMP_Alert` state has Constraints tagged value (Cancel/Resubmit/Release)
- [ ] Heartbeat transitions use Object Filter on `timeout` field
- [ ] Generic FSMs used where applicable (no redundant custom modeling)
- [ ] Action names match ACE subflow naming convention: `Act<PascalCase>`
- [ ] Transition priorities set correctly (no ambiguous transitions at same priority)
- [ ] Custom events defined in EVENT_TYPE with correct RENDER_AS_MESSAGE setting

---

## Exported SQL Example

```sql
-- FSM root
INSERT INTO FSM (FSM_NAME, OBJECT_TYPE, OBJECT_CLASS, SUBTYPE, OBJECT_SELECTION_TEMPLATE, DESCRIPTION)
VALUES ('TxnFSM_SWIFT_OUT', 'TRANSACTION', 'PAYMENT', 'SWIFT_OUTBOUND_TXN',
        'SUBTYPE = ''SWIFT_OUTBOUND_TXN''', 'SWIFT MT103 Outbound Transaction FSM');

-- States
INSERT INTO FSM_STATE_REL (FSM_NAME, STATE_NAME, STATE_TYPE, DESCRIPTION)
VALUES ('TxnFSM_SWIFT_OUT', 'INITIAL', 'NORMAL', 'Transaction received, awaiting validation');

INSERT INTO FSM_STATE_REL (FSM_NAME, STATE_NAME, STATE_TYPE, DESCRIPTION)
VALUES ('TxnFSM_SWIFT_OUT', 'COMPLETED', 'TERMINAL', 'Transaction successfully processed');

INSERT INTO FSM_STATE_REL (FSM_NAME, STATE_NAME, STATE_TYPE, STEREOTYPE, CONSTRAINTS, DESCRIPTION)
VALUES ('TxnFSM_SWIFT_OUT', 'SEND_FAILED_ALERT', 'ALERT', 'PMP_Alert', 'Cancel,Resubmit',
        'Outbound send failed — operator action required');

-- Transitions
INSERT INTO FSM_TRANSITION (FSM_NAME, FROM_STATE, EVENT_TYPE, ACTION_SUBFLOW, TO_STATE,
                            TRANSITION_PRIORITY, OBJECT_FILTER, EVENT_FILTER)
VALUES ('TxnFSM_SWIFT_OUT', 'INITIAL', 'E_MpInMappingComplete', 'ActValidateAndRoute',
        'VALIDATED', 1, NULL, NULL);

INSERT INTO FSM_TRANSITION (FSM_NAME, FROM_STATE, EVENT_TYPE, ACTION_SUBFLOW, TO_STATE,
                            TRANSITION_PRIORITY, OBJECT_FILTER, EVENT_FILTER)
VALUES ('TxnFSM_SWIFT_OUT', 'INITIAL', 'E_MpInMappingAborted', 'ActRaiseMappingAlert',
        'MAPPING_ERROR_ALERT', 1, NULL, NULL);
```
