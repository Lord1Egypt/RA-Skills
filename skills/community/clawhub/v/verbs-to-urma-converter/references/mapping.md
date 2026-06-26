# URMA API Mapping Reference

> URMA API Version: 25.12.0
> **Important**: This document covers the latest URMA API. Always verify against the source repository at https://atomgit.com/openeuler/umdk

## URMA Source Repository

| Resource | URL | Description |
|----------|-----|-------------|
| **Main Repository** | https://atomgit.com/openeuler/umdk | Official URMA/UMDK source |
| URMA Headers | `lib/urma/include/` | Core API header files |
| URMA API | `include/urma_api.h` | Public API definitions |
| URMA Types | `include/urma_types.h` | Type definitions |
| URMA Samples | `tools/urma_perftest/` | Performance test examples |

### Header File Locations

| Header File | Content |
|-------------|---------|
| `urma_api.h` | Function signatures, resource lifecycle |
| `urma_types.h` | Structs, enums, macros |
| `urma_opcode.h` | Constants: URMA_ACCESS_*, URMA_TOKEN_*, URMA_OPC_* |

```bash
find /usr -name "urma_api.h" -o -name "urma_opcode.h" 2>/dev/null
# Common location: /usr/include/ub/umdk/urma/
```

---

## No URMA Equivalent (Delete Directly)

The following Verbs APIs have no URMA equivalents; during migration, **delete directly** rather than replace:

| Verbs API | Deletion Reason | Notes When Deleting |
|-----------|-----------------|-------------------|
| `ibv_alloc_pd()` | PD is implicit in URMA, managed by context | Delete call and its returned `ibv_pd*` variable; context originally obtained through PD changes to direct use of `urma_context_t*` |
| `ibv_dealloc_pd()` | Same as above | Delete this call in cleanup flow |
| `ibv_query_gid()` | EID is determined when `urma_create_context()` | Use `urma_get_eid_list()` to get EID |
| `ibv_query_pkey()` | URMA has no partition key concept | Delete related logic directly |
| `port_attr->lid` | URMA removed LID; only uses EID | All code referencing LID (address exchange, routing judgment) changes to use EID |
| `ibv_modify_qp(IBV_QPS_INIT)` | URMA Jetty is in INIT state upon creation | Delete this modify_qp call; related port/GID initialization logic need not migrate |
| `ibv_modify_qp(IBV_QPS_RESET)` | URMA uses delete+create instead of reset | Delete this call; if reset needed, do delete then create |

**⚠️ Do not try to find "equivalents" for these APIs** — the semantics they represent either don't exist in URMA or are handled implicitly by other mechanisms. When encountering unmapped APIs not listed in table, read `urma_api.h` to confirm, then decide to delete or replace.

---

## API Function Mapping

### Initialization/Uninitialization

| Verbs API | URMA API | Description |
|-----------|----------|-------------|
| *(implicit)* | `urma_init()` | Initialize URMA library - must be called before any URMA API |
| *(implicit)* | `urma_uninit()` | Uninitialize URMA library - call once at exit |

### Initialization and Devices

| Verbs API | URMA API | Description |
|-----------|----------|-------------|
| `ibv_get_device_list()` | `urma_get_device_list(&num_devices)` | **num_devices pointer is required, cannot be NULL** |
| `ibv_free_device_list()` | `urma_free_device_list()` | Free device list |
| `ibv_open_device()` | `urma_create_context()` | Get device context |
| `ibv_close_device()` | `urma_delete_context()` | Close device context |
| `ibv_query_device()` | `urma_query_device()` | Query device capabilities |
| `ibv_query_port()` | *(in urma_query_device())* | Port info included in device attributes |
| `ibv_get_device_name(dev)` | `dev->name` | Direct member access, not a function |

### Port Query

URMA has no standalone port query function. Use `urma_query_device()`:

```c
// Get device attributes including port info
urma_device_attr_t dev_attr = {0};
status = urma_query_device(ctx->context->dev, &dev_attr);
if (status != URMA_SUCCESS) {
    fprintf(stderr, "Failed to get device info\n");
    return 1;
}
// Port 1 attributes:
urma_port_attr_t port_attr = dev_attr.port_attr[0];
```

### Memory Registration

| Verbs API | URMA API | Description |
|-----------|----------|-------------|
| `ibv_alloc_pd()` | *(implicit)* | No explicit PD in URMA |
| `ibv_dealloc_pd()` | *(implicit)* | Handled by context destruction |
| `ibv_reg_mr()` | `urma_register_seg()` | Register memory segment |
| `ibv_dereg_mr()` | `urma_unregister_seg()` | Unregister memory segment |
| `ibv_reg_dm_mr()` | *(use DM directly)* | Device memory support |
| `ibv_advise_mr()` | *(see URMA flags)* | ODP/prefetch via flags |

### Completion Queues

| Verbs API | URMA API | Description |
|-----------|----------|-------------|
| `ibv_create_cq()` | `urma_create_jfc()` | Create completion queue |
| `ibv_destroy_cq()` | `urma_delete_jfc()` | Destroy completion queue |
| `ibv_poll_cq()` | `urma_poll_jfc()` | Poll completion events, max 16 per call |
| `ibv_req_notify_cq()` | `urma_rearm_jfc()` | Request notification |

#### JFC Limits and Recommendations

**Polling limit**: RDMA devices poll max **16 completion records** per call.

**Depth recommendation**:
```
JFC depth >= sum of associated Jetty queue depths / CR generation interval + number of associated Jetties
```

**Key constraint**: JFC depth must be >= JFR depth + JFS depth, otherwise completion events may be lost.

### Event Channels (Completion Channels)

| Verbs API | URMA API | Description |
|-----------|----------|-------------|
| `ibv_create_comp_channel()` | `urma_create_jfce()` | Create event channel |
| `ibv_destroy_comp_channel()` | `urma_delete_jfce()` | Destroy event channel |
| `ibv_get_cq_event()` | `urma_wait_jfc()` | Wait for completion event (blocking) |
| `ibv_ack_cq_events()` | `urma_ack_jfc()` | **Must call after `urma_wait_jfc()`** |

**Complete event mode sequence:**
```c
// 1. Create JFCE (event channel)
urma_jfce_t *jfce = urma_create_jfce(ctx);

// 2. Create JFC bound to JFCE
urma_jfc_cfg_t jfc_cfg = {
    .depth = 128,
    .jfce = jfce,  // bound to event channel
    .user_ctx = 0
};
urma_jfc_t *jfc = urma_create_jfc(ctx, &jfc_cfg);

// 3. Initial load (before first wait)
urma_rearm_jfc(jfc, false);

// 4. Wait for event (blocking)
urma_jfc_t *ev_jfc = NULL;
int cnt = urma_wait_jfc(jfce, 1, timeout_ms, &ev_jfc);

// 5. Reload to receive next event (can be before or after poll/ack)
urma_rearm_jfc(jfc, false);

// 6. Poll completion events
urma_cr_t cr;
urma_poll_jfc(jfc, 1, &cr);

// 7. Acknowledge - must call!
uint32_t ack_cnt = 1;
urma_ack_jfc(&ev_jfc, &ack_cnt, 1);
```

**⚠️ Key**: `urma_ack_jfc()` must be called after every `urma_wait_jfc()`. Omitting causes resource leaks.

**Note**: `rearm` and `ack` order can be flexible, but `ack` must be called after `wait`.

### Async Event Handling

| Verbs API | URMA API | Description |
|-----------|----------|-------------|
| `ibv_get_async_event()` | `urma_get_async_event()` | Get async events |
| `ibv_ack_async_event()` | `urma_ack_async_event()` | Acknowledge async events |

### Queue Pairs / Jetties (Lifecycle)

| Verbs Operation | URMA Operation | Description |
|-----------------|----------------|-------------|
| `ibv_create_qp()` | `urma_create_jfr()` → `urma_create_jetty()` | **All modes (RC/RM/UM)**: create JFR first, then Jetty with `jetty_cfg.flag.bs.share_jfr = URMA_SHARE_JFR` and `jetty_cfg.shared.jfr = jfr` |
| `ibv_modify_qp(RTR)` | `urma_import_jetty()` | **All modes** need import |
| `ibv_modify_qp(RTS)` | `urma_bind_jetty()` | **RC mode only** |
| `ibv_destroy_qp()` | **RC**: `urma_unbind_jetty()` → `urma_unimport_jetty()` → `urma_delete_jetty()` → `urma_delete_jfr()` | Must call in order |
| | **RM/UM**: `urma_unimport_jetty()` → `urma_delete_jetty()` → `urma_delete_jfr()` | Must call in order |
| `ibv_query_qp()` | `urma_query_jetty()` | Query QP state |

---

### Connection Establishment Decision Tree

URMA's operations corresponding to Verbs' `ibv_modify_qp()` depend on transport mode. This decision tree helps quickly determine correct flow:

```
When ibv_modify_qp(RTR) appears → determine trans_mode:
   ├─ RC (IBV_QPT_RC / URMA_TM_RC)
   │    → urma_import_jetty()  // import remote Jetty
   │    → urma_bind_jetty()    // establish reliable connection (RC only)
   │
   ├─ RM (URMA_TM_RM)
   │    → urma_import_jetty()  // import remote Jetty (no bind)
   │
   └─ UM (IBV_QPT_UD / URMA_TM_UM)
        → urma_import_jetty()  // import remote Jetty (no bind)

When ibv_modify_qp(RTS) appears → determine trans_mode:
   ├─ RC → already done by bind_jetty(), no additional action needed
   ├─ RM → not applicable (no connection state transition)
   └─ UM → not applicable

When ibv_modify_qp(INIT) appears → delete directly (Jetty is in INIT state upon creation)
When ibv_modify_qp(RESET) appears → replace with delete + create (if reset needed)
```

**Address exchange format decision**:
```
Verbs exchange content:  lid + gid + qpn + psn
                      ↓
URMA exchange content:  eid + jpn
                      ↓
Specific packing:       rjetty.jetty_id.eid  (16-byte EID)
                        rjetty.jetty_id.uasid (UASID)
                        rjetty.jetty_id.id    (JPN)
                        rjetty.tp_type        (URMA_RTP or URMA_UTP)
                        rjetty.trans_mode     (URMA_TM_RC/RM/UM)
```

**Cleanup order decision**:
```
Program exit → determine transport mode used:
   ├─ RC mode:  unbind_jetty → unimport_jetty → delete_jetty → delete_jfr → delete_jfc → uninit
   ├─ RM mode:  unimport_jetty → delete_jetty → delete_jfr → delete_jfc → uninit
   └─ UM mode:  unimport_jetty → delete_jetty → delete_jfr → delete_jfc → uninit
                                                                           ↑
                                                              call urma_uninit() last!
```

---

### Shared Receive Queues (SRQ)

| Verbs API | URMA API | Description |
|-----------|----------|-------------|
| `ibv_srq` | `urma_jfr_t` | Shared receive queue |
| `ibv_create_srq()` | `urma_create_jfr()` | Create SRQ |
| `ibv_destroy_srq()` | `urma_delete_jfr()` | Destroy SRQ |
| `ibv_post_srq_recv()` | `urma_post_jfr_wr()` | Post receive requests to SRQ |
| `ibv_modify_srq()` | `urma_modify_jfr()` | Modify JFR attributes |
| `ibv_query_srq()` | `urma_query_jfr()` | Query JFR attributes |
| QP using shared SRQ | `jetty_cfg.flag.bs.share_jfr = URMA_SHARE_JFR` + `jetty_cfg.shared.jfr = srq` | Multiple Jetties share same JFR |

**Note**: When using `URMA_TOKEN_PLAIN_TEXT` (or higher security level), JFR also needs a valid token, which must be exchanged with remote.

### Work Requests

| Verbs API | URMA API | Description |
|-----------|----------|-------------|
| `ibv_post_send()` | `urma_post_jfs_wr()` | Post send requests (JFS) |
| `ibv_post_send()` | `urma_post_jetty_send_wr()` | Post send requests (Jetty) |
| `ibv_post_recv()` | `urma_post_jfr_wr()` | Post receive requests (JFR) |
| `ibv_post_recv()` | `urma_post_jetty_recv_wr()` | Post receive requests (Jetty) |

### High-Level Operations

| Verbs | URMA High-Level API | Description |
|-------|---------------------|-------------|
| Manual send/recv | `urma_send()` | Simplified send |
| Manual send/recv | `urma_recv()` | Simplified receive |
| RDMA Write | `urma_write()` | Direct RDMA write |
| RDMA Read | `urma_read()` | Direct RDMA read |
| Atomic | `urma_cas()`, `urma_faa()` | Compare-and-swap, fetch-and-add |

---

## Enum Mapping

### MTU

| Verbs | URMA |
|-------|------|
| `IBV_MTU_256` | `URMA_MTU_256` |
| `IBV_MTU_512` | `URMA_MTU_512` |
| `IBV_MTU_1024` | `URMA_MTU_1024` |
| `IBV_MTU_2048` | `URMA_MTU_2048` |
| `IBV_MTU_4096` | `URMA_MTU_4096` |
| - | `URMA_MTU_8192` |

### Access Flags

#### Registration Flags (urma_reg_seg_flag_t)

| Verbs | URMA | Value | Description |
|-------|------|-------|-------------|
| `IBV_ACCESS_LOCAL_WRITE` | `URMA_ACCESS_LOCAL_ONLY` | 0x1 | Local access only (mutually exclusive with other flags) |
| `IBV_ACCESS_REMOTE_READ` | `URMA_ACCESS_READ` | 0x2 | Read permission |
| `IBV_ACCESS_REMOTE_WRITE` | `URMA_ACCESS_WRITE` | 0x4 | Write permission (requires READ) |
| `IBV_ACCESS_REMOTE_ATOMIC` | `URMA_ACCESS_ATOMIC` | 0x8 | Atomic operations (requires READ+WRITE) |
| `IBV_ACCESS_ON_DEMAND` | *(not supported)* | - | ODP handled differently |
| `IBV_ACCESS_ZERO_BASED` | *(not needed in URMA)* | - | |

**Dependencies**: WRITE depends on READ; ATOMIC depends on READ+WRITE.

### QP States

| Verbs | URMA | Description |
|-------|------|-------------|
| `IBV_QPS_RESET` | *(upon creation)* | Initial state |
| `IBV_QPS_INIT` | *(upon creation)* | Initialized |
| `IBV_QPS_RTR` | `urma_import_jetty()` | Ready to receive |
| `IBV_QPS_RTS` | `urma_bind_jetty()` | Ready to send |
| `IBV_QPS_ERR` | *(error state)* | Error |

### QP Types

| Verbs | URMA | Description |
|-------|------|-------------|
| `IBV_QPT_RC` | `URMA_TM_RC` | Reliable connection |
| `IBV_QPT_UD` | `URMA_TM_UM` | Unreliable datagram |
| - | `URMA_TM_RM` | Reliable message (connectionless) |

**Key: All transport modes require explicit JFR creation and import_jetty**

| Verbs | URMA | Resource Creation Difference |
|-------|------|------------------------------|
| QP internally contains send/receive queues | **Jetty does not create JFR by default**, must be explicitly created and shared |

**Required steps (all modes)**:
```
1. urma_create_jfr()     // create receive queue (JFR)
2. urma_create_jetty()   // create send queue (JFS)
   └── set jetty_cfg.flag.bs.share_jfr = URMA_SHARE_JFR
   └── set jetty_cfg.shared.jfr = JFR from step 1
3. urma_import_jetty()   // import remote Jetty (required for all modes!)
   └── set wr.tjetty = imported_target_jetty  // must be set in send WR
```

**RC mode additional steps**:
```
4. urma_bind_jetty()      // bind connection (RC only)
```

**RM mode**:
```
4. urma_import_jetty()    // (advise deprecated)
```

**UM mode**:
```
4. urma_import_jetty()    // (no bind)
```

### Work Request Operation Codes

| Verbs | URMA | Description |
|-------|------|-------------|
| `IBV_WR_SEND` | `URMA_OPC_SEND` | |
| `IBV_WR_SEND_WITH_IMM` | `URMA_OPC_SEND_IMM` | Immediate data in `send.imm_data` |
| `IBV_WR_RDMA_WRITE` | `URMA_OPC_WRITE` | |
| `IBV_WR_RDMA_WRITE_WITH_IMM` | `URMA_OPC_WRITE_IMM` | Immediate data in `rw.notify_data` (not `imm_data`!) |
| `IBV_WR_RDMA_READ` | `URMA_OPC_READ` | |
| `IBV_WR_ATOMIC_CMP_AND_SWP` | `URMA_OPC_CAS` | |
| `IBV_WR_ATOMIC_FETCH_AND_ADD` | `URMA_OPC_FADD` | Note: FAA → FADD |

**Important**: Field difference for immediate data operations:
- `URMA_OPC_SEND_IMM`: uses `wr.send.imm_data`
- `URMA_OPC_WRITE_IMM`: uses `wr.rw.notify_data` (different field!)

### Completion Status Values

| Verbs | URMA | Description |
|-------|------|-------------|
| `IBV_WC_SUCCESS` | `URMA_CR_SUCCESS` | Success |
| `IBV_WC_LOC_LEN_ERR` | `URMA_CR_LOC_LEN_ERR` | Local data too long |
| `IBV_WC_LOC_QP_OP_ERR` | `URMA_CR_LOC_OPERATION_ERR` | Local operation error |
| `IBV_WC_LOC_ACCESS_ERR` | `URMA_CR_LOC_ACCESS_ERR` | Local access error |
| `IBV_WC_REM_RESP_ERR` | `URMA_CR_REM_RESP_LEN_ERR` | Remote response length error |
| `IBV_WC_REM_OP_ERR` | `URMA_CR_REM_OPERATION_ERR` | Remote operation error |
| `IBV_WC_RNR_RETRY_CNT_EXC` | `URMA_CR_RNR_RETRY_CNT_EXC_ERR` | RNR retry exceeded |
| `IBV_WC_WR_FLUSH_ERR` | `URMA_CR_WR_FLUSH_ERR` | WR flushed |

### Error Codes

| URMA Error | Value | Description |
|------------|-------|-------------|
| `URMA_SUCCESS` | 0 | Success |
| `URMA_EAGAIN` | -11 | Resource temporarily unavailable |
| `URMA_ENOMEM` | -12 | Memory allocation failed |
| `URMA_ENOPERM` | -1 | Operation not permitted |
| `URMA_ETIMEOUT` | -110 | Operation timeout |
| `URMA_EINVAL` | -22 | Invalid parameter |
| `URMA_EEXIST` | -17 | Already exists |
| `URMA_EINPROGRESS` | -115 | Operation in progress |
| `URMA_FAIL` | 0x1000 | General failure |

**Return value checking**: URMA function return value semantics are not unified; judge by category:

| Category | Success Condition | Example Functions |
|----------|-------------------|-------------------|
| Resource management | Returns 0 for success, non-zero for error | `urma_init`, `urma_register_seg`, `urma_create_jfc`, `urma_create_jetty`, `urma_import_jetty`, `urma_bind_jetty` |
| Polling/wait | Returns >0 for success (returns count), 0 or negative for failure/no data | `urma_poll_jfc`, `urma_wait_jfc` |
| Pointer return | Returns non-NULL for success, NULL for failure | `urma_create_context`, `urma_create_jfce` |

**⚠️ Common error**: checking `urma_poll_jfc()` or `urma_wait_jfc()` return values with `!= 0` — this incorrectly treats error codes as success. Correct approach: `> 0` means completion events available.

### Transport Type (TP Type)

| TP Type | URMA Value | Description |
|---------|------------|-------------|
| Reliable transport | `URMA_RTP` | Default reliable transport protocol |
| Connection-oriented transport | `URMA_CTP` | Connection-oriented transport |
| Unreliable transport | `URMA_UTP` | Unreliable transport, highest performance |

**Note**: TP type determines connection behavior.

### Completion Record Operation Codes

| Verbs | URMA | Description |
|-------|------|-------------|
| `IBV_WC_SEND` | `URMA_CR_OPC_SEND` | Send operation completed |
| `IBV_WC_RDMA_WRITE` | `URMA_CR_OPC_WRITE` | RDMA write completed |
| `IBV_WC_RDMA_READ` | `URMA_CR_OPC_READ` | RDMA read completed |
| `IBV_WC_RECV` | `URMA_CR_OPC_RECV` | Receive completed |
| `IBV_WC_RECV_RDMA_WITH_IMM` | `URMA_CR_OPC_WRITE_WITH_IMM` | Write with immediate data |

**Note**: `URMA_CR_OPC_WRITE_WITH_IMM` commonly used for RDMA operations with immediate data notification.

### Token Policies

| Policy | Value | Token Required | Security Level | Use Case |
|--------|-------|----------------|----------------|----------|
| `URMA_TOKEN_NONE` | 0 | Can be 0 | No authentication | Development/testing |
| `URMA_TOKEN_PLAIN_TEXT` | 1 | Must be non-zero | Plaintext token | Production (recommended) |
| `URMA_TOKEN_SIGNED` | 2 | Must be non-zero | Signed authentication | High security |
| `URMA_TOKEN_ALL_ENCRYPTED` | 3 | Must be non-zero | Full encryption | Maximum security |

### Transport Modes

| Mode | Value | Description | Use Case |
|------|-------|-------------|----------|
| `URMA_TM_RM` | 0x1 | Reliable message | Bidirectional, connectionless |
| `URMA_TM_RC` | 0x2 | Reliable connection | Unidirectional, connection-oriented |
| `URMA_TM_UM` | 0x4 | Unreliable message | High performance, may drop packets |

---

## Data Structure Mapping

**Must use designated initializer syntax during migration; never define then assign:**
  ```c
  // ❌ Wrong - uninitialized local variable, field values undefined
  urma_seg_cfg_t seg_cfg;
  seg_cfg.va = (uint64_t)buf;
  // ✅ Correct - use designated initializer, unspecified fields auto-zero
  urma_seg_cfg_t seg_cfg = {
      .va = (uint64_t)buf,
      .len = size
  };
  ```
  Reason: URMA structs have many fields; omitting fields causes undefined behavior.

### Core Objects

| Verbs Type | URMA Type | Description |
|------------|-----------|-------------|
| `ibv_context` | `urma_context_t` | Device context handle |
| `ibv_pd` | *(implicit)* | PD implicitly managed in URMA |
| `ibv_mr` | `urma_target_seg_t` | Memory region obtained via `urma_register_seg()` |
| `ibv_cq` | `urma_jfc_t` | Completion queue |
| `ibv_comp_channel` | `urma_jfce_t` | Completion event channel |
| `ibv_qp` | `urma_jetty_t` | Queue pair (send/receive combined) |
| `ibv_qp` | `urma_jfs_t` + `urma_jfr_t` | Queue pair (send/receive separated) |
| `ibv_srq` | `urma_jfr_t` | Shared receive queue - can be shared by multiple Jetties |
| `ibv_device` | `urma_device_t` | Network device |
| `ibv_port_attr` | `urma_port_attr_t` | Port attributes |
| `ibv_sge` | `urma_sge_t` | Scatter-gather entry |
| `ibv_send_wr` | `urma_jfs_wr_t` | Send work request |
| `ibv_recv_wr` | `urma_jfr_wr_t` | Receive work request |

### Address Types

| Verbs | URMA | Format |
|-------|------|--------|
| `lid` | *(removed)* | URMA uses EID instead of LID |
| `union ibv_gid` | `urma_eid_t` | 16-byte endpoint ID |
| `qpn` | `jpn` | Jetty pair number |
| `psn` | *(removed)* | PSN managed internally by URMA kernel |

### Address Exchange Format

| Verbs Format | URMA Format | Example |
|--------------|-------------|---------|
| `lid:qpn:psn:gid` | `jpn:eid` | Verbs: `0001:010203:abcdef:...` |
| | | URMA: `010203:0000000000000000000000000000000000000000000000000000000000000000` |

**Note**:
- URMA completely removed LID - uses only EID (16 bytes)
- URMA removed PSN - managed internally by kernel, no user-space exchange needed

---

## Struct Field Mapping

> **Important**: This section maps Verbs struct fields to URMA struct fields.
> If mapping not found here, read system URMA header files to verify.

### Completion Records (ibv_wc → urma_cr_t)

| Verbs Field | URMA Field | Description |
|-------------|------------|-------------|
| `wc.qp_num` | `cr.local_id` | **Not** `cr.jetty_id.id` |
| `wc.wr_id` | `cr.user_ctx` | User context |
| `wc.status` | `cr.status` | Completion status |
| `wc.opcode` | `cr.opcode` | Operation code |
| `wc.byte_len` | `cr.completion_len` | Transfer byte count |
| `wc.imm_data` | `cr.imm_data` | Immediate data |

#### Completion Record (urma_cr_t) Detailed Fields

| URMA Field | Description |
|------------|-------------|
| `cr.local_id` | Local Jetty/JFS/JFR ID |
| `cr.remote_id` | Remote Jetty ID (valid only for receive CR) |
| `cr.user_ctx` | User context (wr_id) |
| `cr.completion_len` | Transfer byte count |
| `cr.imm_data` | Immediate data (send/write with imm) |
| `cr.opcode` | Operation code (valid only for receive CR) |
| `cr.tpn` | TP or TPG number |

### Queue Pairs (ibv_qp → urma_jetty_t)

| Verbs Field | URMA Field | Description |
|-------------|------------|-------------|
| `qp->qp_num` | `jetty->jetty_id.id` | **Not** `jetty->id` |
| `qp->state` | `jetty->jetty_cfg` | Obtained via jetty config |
| `qp->qp_type` | `jetty->jetty_cfg.jfs_cfg.trans_mode` | Transport mode |

### Port Attributes (ibv_port_attr → urma_port_attr_t)

| Verbs Field | URMA Field | Description |
|-------------|------------|-------------|
| `port_attr->lid` | *(removed)* | **Does not exist** in URMA; use EID |
| `port_attr->gid` | `eid_info->eid` | Obtained via `urma_get_eid_list()` |
| `port_attr->mtu` | `port_attr->active_mtu` | Active MTU |

### Device Attributes (ibv_device_attr → urma_device_attr_t)

| Verbs Field | URMA Field | Description |
|-------------|------------|-------------|
| `dev_attr->phys_port_cnt` | `dev_attr->port_cnt` | Port count |
| `dev_attr->gid_tbl_len` | `dev_attr->dev_cap.max_eid_cnt` | Max EID count |

### Remote Jetty (urma_rjetty_t)

| Required Fields | Description |
|-----------------|-------------|
| `rjetty.jetty_id` | Remote jetty ID (EID, uasid, id) |
| `rjetty.trans_mode` | Transport mode (URMA_TM_RC/RM/UM) |
| `rjetty.policy` | Policy (URMA_JETTY_GRP_POLICY_RR) |
| `rjetty.type` | Type (URMA_JETTY) |
| `rjetty.flag` | Import flags |
| `rjetty.tp_type` | **Key**: must set (URMA_RTP) |

### Scatter-Gather Entries (ibv_sge → urma_sge_t)

| Verbs Field | URMA Field | Description |
|-------------|------------|-------------|
| `sge.addr` | `sge.addr` | Buffer address |
| `sge.length` | `sge.len` | **Not** `length` |
| `sge.lkey` | `sge.tseg` | **Not** integer; use `urma_target_seg_t*` from `urma_register_seg()` or `urma_import_seg()` |

**Important**: In RDMA read/write/atomic operations, remote memory segment's `tseg` must be obtained via `urma_import_seg()`, not `urma_register_seg()`. See pitfalls.md §23.

### Send Work Requests (ibv_send_wr → urma_jfs_wr_t)

| Verbs Field | URMA Field | Description |
|-------------|------------|-------------|
| `wr.wr_id` | `wr.user_ctx` | Work request ID |
| `wr.opcode` | `wr.opcode` | Operation code |
| `wr.send_flags` | `wr.flag.value` or `wr.flag.bs.*` | Use bit fields to set flags |
| `wr.sg_list` | `wr.send.src.sge` | **Not** `wr.sge` - nested in `send.src` union |
| `wr.num_sge` | `wr.send.src.num_sge` | **Not** `wr.num_sge` - nested in `urma_sg_t` |
| `wr.next` | `wr.next` | Linked list |

**Send flags**:

| Verbs Flag | URMA Bit Field | Description |
|------------|----------------|-------------|
| `IBV_SEND_SIGNALED` | `flag.bs.complete_enable = 1` | Generate completion event |
| `IBV_SEND_INLINE` | `flag.bs.inline_flag = 1` | Inline data |
| `IBV_SEND_FENCE` | `flag.bs.fence = 1` | Fence |
| `IBV_SEND_SOLICITED` | `flag.bs.solicited_enable = 1` | Request event |

### Receive Work Requests (ibv_recv_wr → urma_jfr_wr_t)

| Verbs Field | URMA Field | Description |
|-------------|------------|-------------|
| `wr.wr_id` | `wr.user_ctx` | Work request ID |
| `wr.sg_list` | `wr.src.sge` | **Not** `wr.sge` - nested in `src` |
| `wr.num_sge` | `wr.src.num_sge` | **Not** `wr.num_sge` - nested in `urma_sg_t` |
| `wr.next` | `wr.next` | Linked list |

### urma_reg_seg_flag_t Bit Field Layout

```c
typedef union urma_reg_seg_flag {
    struct {
        uint32_t token_policy   : 3;  // bits 0-2
        uint32_t cacheable      : 1;  // bit 3
        uint32_t dsva           : 1;  // bit 4
        uint32_t access         : 6;  // bits 5-10
        uint32_t non_pin        : 1;  // bit 11
        uint32_t user_iova      : 1;  // bit 12
        uint32_t token_id_valid : 1;  // bit 13
        uint32_t reserved       : 18; // bits 14-31
    } bs;
    uint32_t value;
} urma_reg_seg_flag_t;
```

### Common Field Mapping Errors

| Wrong Usage | Correct Usage | Error Reason |
|-------------|---------------|--------------|
| `cr.jetty_id.id` | `cr.remote_id.id` | `urma_cr_t` has no `jetty_id` member |
| `jetty->id` | `jetty->jetty_id.id` | `urma_jetty_t` has no `id` member |
| `port_attr->lid` | use EID | URMA removed LID |
| `rjetty` (missing tp_type) | `rjetty.tp_type = URMA_RTP` | tp_type must be set |
| `sge.length` | `sge.len` | Field name is `len`, not `length` |
| `sge.lkey` | `sge.tseg` | Use pointer type, not integer key |
| `wr.sg_list` | `wr.send.src.sge` / `wr.src.sge` | Nested in union/struct |
| `wr.num_sge` | `wr.send.src.num_sge` / `wr.src.num_sge` | Nested in `urma_sg_t` |
| `seg_cfg.addr` | `seg_cfg.va` | Field name is `va`, not `addr` |
| `flag = URMA_ACCESS_LOCAL_ONLY` | `flag.bs.access = URMA_ACCESS_LOCAL_ONLY` | Access via bit field |
| `.value = URMA_ACCESS_LOCAL_ONLY` | `.bs.token_policy = URMA_TOKEN_NONE, .bs.access = ...` | `.value` sets all bits |

### URMA-Specific Parameters (No Verbs Equivalent)

The following parameters exist in URMA but have no Verbs equivalents; must be set correctly based on device capabilities.

| URMA Parameter | Device Capability Field | Typical Value | Description |
|----------------|-------------------------|---------------|-------------|
| `jfs_cfg.max_rsge` | `dev_cap.max_jfs_rsge` | Usually 1 | Max remote SGE count (no Verbs equivalent) |
| `jfs_cfg.max_sge` | `dev_cap.max_jfs_sge` | 13+ | Max local SGE for send |
| `jfr_cfg.max_sge` | `dev_cap.max_jfr_sge` | 4+ | Max local SGE for receive |
| `jfs_cfg.depth` | `dev_cap.max_jfs_depth` | 8192 | JFS queue depth |
| `jfr_cfg.depth` | `dev_cap.max_jfr_depth` | 32768 | JFR queue depth |
| `jfs_cfg.max_inline_data` | `dev_cap.max_jfs_inline_len` | 208 | Max inline data |
| `jfc_cfg.depth` | `dev_cap.max_jfc_depth` | 65536 | JFC depth |

**⚠️ Key**: User-defined constants must be compared with device capability values; use the smaller one.

```c
// ✅ Correct - use device capabilities
urma_jfs_cfg_t jfs_cfg = {
    .max_sge = min(13, (uint8_t)ctx->dev_attr.dev_cap.max_jfs_sge),
    .max_rsge = ming(12, (uint8_t)ctx->dev_attr.dev_cap.max_jfs_rsge),  // not max_sge!
};

// ❌ Wrong - use arbitrary values
urma_jfs_cfg_t jfs_cfg = {
    .max_sge = 13,
    .max_rsge = 13,  // Wrong! Device may only support 1
};
```

---

## Adding New Mappings

When discovering new API mappings during migration:

1. Determine category (data structures, API functions, enums, etc.)
2. Add entry in appropriate table
3. Include: Verbs API, URMA API, and brief description

Format:
```markdown
| Verbs API | URMA API | Description |
|-----------|----------|-------------|
| `ibv_xxx()` | `urma_xxx()` | Description |
```