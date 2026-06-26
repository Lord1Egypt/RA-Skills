# FTM Patterns and RSAD Artifacts

Each of the 15 FTM patterns requires a specific set of RSAD design artifacts. This reference maps
every pattern to the diagrams, FSMs, and configuration it needs.

---

## Pattern Selection Guide

| # | Pattern | Trigger |
|---|---|---|
| 9.1 | Outbound Message/File | Send a message/file to an external system |
| 9.2 | Routing + ODM | Dynamic routing; message goes to one of N targets |
| 9.3 | Inbound Acknowledgement | Correlate response/ACK/NACK to a prior request |
| 9.4 | Store and Release | Hold transactions until a gateway opens (cut-off window) |
| 9.5 | Transformation/Mapping | Convert format between external systems |
| 9.6 | Debulking | Split inbound batch into individual transactions |
| 9.7 | Bulking | Aggregate multiple transactions into an outbound batch |
| 9.8 | Scheduler-driven Store/Release | Release held transactions at a scheduled cut-off time |
| 9.9 | External Services | Invoke an external service (sync or async) from FTM |
| 9.10 | Hosting Services | FTM exposes a service for external systems to call |
| 9.11 | Collating Information | Wait for N related messages before processing |
| 9.12 | Scheduled Activity | Trigger an activity at a configured schedule |
| 9.13 | Scheduled Expectation | Raise an alert if an expected event doesn't arrive in time |
| 9.14 | Heartbeat Monitoring | Send/receive periodic pings to check SP availability |
| 9.15 | Error Handling + Alerts | Operator-facing notification and resolution flow |

---

## Required RSAD Artifacts per Pattern

Every FTM interface produces these 7 standard artifacts. The table below shows what each
contains, specialized per pattern.

### Pattern 9.1 — Outbound Message/File

| Artifact | Content |
|---|---|
| Use Case Diagram | Actors: Originating System, FTM, Target SP. Use cases: Submit Payment, Deliver Payment, Handle Delivery Failure |
| Functional Sequence | PT → Mapper → DB2 INSERT Txn/Trans → E_MpInMappingComplete → EP → ActRoute → E_TxnOutCreated → ACE Outbound |
| Object Lifecycle (FSM) | INITIAL → (E_MpInMappingComplete) → VALIDATED → (E_TxnOutCreated) → SENT → COMPLETED |
| Alert States | MAPPING_ERROR_ALERT (Cancel, Resubmit), SEND_FAILED_ALERT (Cancel, Resubmit) |
| SP/Channel Config | Outbound channel; output queue; mapper reference |
| SQL Export | FSM + transitions + SP + Channel |

---

### Pattern 9.2 — Routing + ODM

Additional RSAD elements:
- Sequence diagram must show ODM service invocation (ActRouteViaODM action)
- FSM adds ROUTING state between VALIDATED and SENT
- Activity diagram recommended for routing logic (ODM ruleset name + parameters)
- SP config includes `ODM_RULESET_NAME` channel attribute

```
INITIAL → VALIDATED → ROUTING → SENT → COMPLETED
ROUTING → ROUTING_FAILED_ALERT (Cancel, Resubmit)
```

---

### Pattern 9.3 — Inbound Acknowledgement

Additional RSAD elements:
- Separate Transmission FSM for inbound ACK
- Transaction FSM adds WAITING_FOR_ACK state after SENT
- Correlation key documented in sequence diagram (how ACK is linked to original request)
- Events: `E_CorrelationSuccessful`, `E_CorrelationFailure`

```
Transaction FSM:
  SENT → (E_CorrelationSuccessful) → ACKNOWLEDGED → COMPLETED
  SENT → (E_CorrelationFailure) → CORRELATION_FAILED_ALERT (Cancel, Resubmit)
  SENT → (E_Heartbeat [timeout < NOW()]) → TIMEOUT_ALERT (Cancel, Continue)

Transmission FSM (ACK):
  RECEIVED → (E_MpInMappingComplete) → CORRELATED → COMPLETED
```

---

### Pattern 9.4 — Store and Release

Additional RSAD elements:
- Transaction FSM has HELD state (gateway closed)
- Release trigger modeled in sequence diagram (manual operator release or scheduled)
- PMP_OpsControl stereotype on HELD state (operator can release)
- Channel config: `STORE_AND_RELEASE=Y`, gateway schedule reference

```
INITIAL → VALIDATED → HELD «PMP_OpsControl»
HELD → (Release / ActSendToSP) → SENT → COMPLETED
HELD → (Cancel / ActCancel) → CANCELLED «PMP_Terminal»
```

---

### Pattern 9.5 — Transformation/Mapping

Additional RSAD elements:
- Mapping design artifacts are central (see `mapping-design.md`)
- Two channels: inbound channel (format A) + outbound channel (format B)
- Two mappers: MapIn<FormatA> + MapOut<FormatB>
- Sequence diagram shows double-transform: raw → ISF → raw-output

---

### Pattern 9.6 — Debulking

Additional RSAD elements:
- Batch object lifecycle (Transmission FSM for batch)
- Transaction FSM for each debulked child transaction
- Sequence diagram shows: PT Flow inserts 1 Transmission + N Transactions; raises N events
- Batch FSM: RECEIVED → (all children complete) → COMPLETED
- Child count tracking in class diagram

```
Batch Transmission FSM:
  RECEIVED → PROCESSING → (E_AllChildrenComplete) → COMPLETED
  PROCESSING → (E_Heartbeat [timeout]) → BATCH_TIMEOUT_ALERT (Cancel, Continue)

Child Transaction FSM: standard outbound pattern (9.1)
```

---

### Pattern 9.7 — Bulking

Additional RSAD elements:
- Batch object lifecycle (outbound batch)
- Sequence diagram: N individual transactions → ACT_Bulk action → 1 outbound batch
- Batch FSM: transitions driven by trigger (count/timer/manual)
- `OBJ_OBJ_REL` relationship modeled in class diagram (transactions belong to batch)

```
Batch Transmission FSM:
  OPEN → (E_ActivityEvent [count >= threshold]) → CLOSING → SENT → COMPLETED
  OPEN → (E_Heartbeat [cutoff time]) → CLOSING → ...
```

---

### Pattern 9.8 — Scheduler-driven Store/Release

Additional RSAD elements:
- Scheduler Task object lifecycle (FSM for SchedulerTask)
- Transaction FSM has HELD state (as in 9.4)
- Sequence diagram shows: Scheduler fires E_ActivityEvent → ActReleaseBatch → releases held transactions
- Scheduler config: cron expression or fixed interval in `SCHEDULER_TASK_BASE`

---

### Pattern 9.9 — External Services

Additional RSAD elements:
- Sequence diagram shows synchronous or async service call
  - Sync: ActCallService → service response → continue in same action
  - Async: ActCallService → WAITING_FOR_RESPONSE state → E_ServiceResponse → continue
- Component diagram shows external service endpoint (SOAP/REST)
- Channel config: `SERVICE_URL`, `TIMEOUT_SECONDS` attributes

---

### Pattern 9.10 — Hosting Services

Additional RSAD elements:
- FTM exposes a service endpoint (modeled as actor/component in use case diagram)
- Sequence diagram: External caller → FTM (HTTP/MQ input) → processing → synchronous response
- No outbound SP needed — response goes back to caller on same connection
- Channel config: `INPUT_QUEUE` or `HTTP_ENDPOINT`

---

### Pattern 9.11 — Collating Information

Additional RSAD elements:
- Collation object lifecycle (special FSM tracking N expected messages)
- Event: `E_ChildTxnArrived` raised when each component arrives
- Object Filter on transition: `CHILD_COUNT >= EXPECTED_COUNT`
- Sequence diagram: N inbound → FTM holds each → ActCollate when all arrived → single ISF

```
Collation Transaction FSM:
  COLLECTING → (E_ChildTxnArrived [childCount >= expected] / ActProcess) → PROCESSING
  COLLECTING → (E_Heartbeat [timeout] / ActAlert) → TIMEOUT_ALERT (Cancel, Continue)
```

---

### Pattern 9.12 — Scheduled Activity

Additional RSAD elements:
- Scheduler Task FSM (SCHEDULED → RUNNING → COMPLETED)
- Sequence diagram: E_ActivityEvent → ActPerformScheduledWork → result
- Scheduler config in class diagram: interval/cron expression, target action

---

### Pattern 9.13 — Scheduled Expectation

Additional RSAD elements:
- Expectation deadline modeled as `timeout` on the waiting state
- Heartbeat transition: `E_Heartbeat [timeout < NOW()] → EXPECTATION_FAILED_ALERT`
- Sequence diagram shows both paths: expectation met (happy) and deadline missed (alert)

```
WAITING_FOR_MESSAGE → (E_MessageArrived) → PROCESSING → COMPLETED
WAITING_FOR_MESSAGE → (E_Heartbeat [timeout < NOW()]) → DEADLINE_MISSED_ALERT (Cancel, Continue)
```

---

### Pattern 9.14 — Heartbeat Monitoring

Additional RSAD elements:
- Dedicated Heartbeat Transaction FSM
- Sequence diagram: FTM sends ping → waits → receives pong OR timeout alert
- Events: `E_HeartbeatStart`, `E_Heartbeat`
- SP config: heartbeat interval, expected response queue

---

### Pattern 9.15 — Error Handling + Alerts

This pattern is present in ALL interfaces (not standalone). Every interface in RSAD must include:
- `PMP_Alert` states on every error path
- Constraints tagged values: at minimum `Cancel`; add `Resubmit` if retry is safe
- OAC will surface these alerts to operators
- Sequence diagram includes alert resolution flows (Cancel path, Resubmit path)

When designing standalone error/retry infrastructure:
- Model a dedicated Alert Monitor FSM with escalation states
- Include timeout escalation: `E_Heartbeat [unresolved > N hours] → ESCALATED_ALERT`

---

## Standard RSAD Design Package (per interface)

Commit to version control in the design repository:

```
design/<InterfaceName>/
├── diagrams/
│   ├── use-case.emx              # Use case diagram
│   ├── sequence-functional.emx   # Functional sequence
│   ├── sequence-technical.emx    # Technical service interaction
│   ├── fsm-transaction.emx       # Transaction FSM
│   ├── fsm-transmission.emx      # Transmission FSM (if applicable)
│   └── deployment.emx            # Deployment topology
├── config/
│   ├── sp_config.sql             # SERVICE_PARTICIPANT_BASE inserts
│   ├── channel_config.sql        # CHANNEL_BASE inserts
│   ├── fsm_config.sql            # FSM + FSM_STATE_REL + FSM_TRANSITION inserts
│   ├── event_type_config.sql     # EVENT_TYPE inserts
│   └── value_config.sql          # VALUE table inserts (SUBTYPE registration)
└── mapping/
    └── field-mapping-<format>.md  # Field-level mapping table
```
