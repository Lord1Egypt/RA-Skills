# URMA Code Patterns and Best Practices

> URMA API Version: 25.12.0

## System Header File Locations

| Installation Method | Include Path |
|---------------------|--------------|
| System install | `#include <ub/umdk/urma/urma_api.h>` |
| Custom install | Check `find /usr -name "urma_api.h"` |

---

## 1. Initialization Flow

### Golden Rule
**Each process must call `urma_init()` once, and `urma_uninit()` once at exit.**

### Correct Pattern

```c
// At program start (e.g., beginning of main())
urma_init_attr_t init_attr = {
    .token = 0,
    .uasid = 0
};
if (urma_init(&init_attr) != URMA_SUCCESS) {
    fprintf(stderr, "URMA init failed\n");
    return 1;
}

// ... your URMA operations ...

// At program exit (e.g., end of main())
urma_uninit();
```

### Resource Creation Order (All modes: RC/RM/UM)

```
urma_init()           ← Must be called first! (before any URMA API)
    ↓
urma_get_device_list() / urma_get_device_by_name()
    ↓
urma_create_context(device, eid_index)
    ↓
urma_create_jfce(context)        [Optional - for event-driven mode]
    ↓
urma_create_jfc(context, &jfc_cfg)
    ↓
urma_register_seg(context, &seg_cfg)
    ↓
urma_create_jfr(context, &jfr_cfg)  [Required - shared JFR]
    ↓
urma_create_jetty(context, &jetty_cfg)  [Pass shared JFR + set share_jfr]
    ↓
urma_import_jetty(context, &rjetty)    [Required for all modes]
    ↓
urma_bind_jetty(jetty, tjetty)          [RC mode only]
```

### Key Difference: GID Index vs EID Index Timing

Verbs and URMA have major differences in timing for specifying GID/EID index:

| Feature | Verbs (RDMA) | URMA |
|---------|--------------|------|
| When to specify index | In `ibv_modify_qp()` as `sgid_index` parameter | In `urma_create_context()` as `eid_index` parameter |
| When to set | After QP creation, before connection (modify_qp) | When opening device (context creation) |
| How to get local GID | Via `ibv_query_gid(ctx, port, gid_idx, &gid)` | Directly via `ctx->eid` |
| Scope | Each QP can use different gid_index | Entire context shares same EID |

**Verbs code pattern**:
```c
// 1. Create QP (gid not specified here)
struct ibv_qp_init_attr init_attr = { .qp_type = IBV_QPT_RC, ... };
struct ibv_qp *qp = ibv_create_qp(pd, &init_attr);

// 2. Modify QP to INIT state
struct ibv_qp_attr attr = { .qp_state = IBV_QPS_INIT, ... };
ibv_modify_qp(qp, &attr, IBV_QP_STATE);

// 3. Modify QP to RTR state - specify gid_index here
attr.ah_attr.grh.sgid_index = gid_idx;  // specified here
attr.ah_attr.grh.dgid = remote_gid;
ibv_modify_qp(qp, &attr, IBV_QP_AV);

// 4. Get local gid (can query anytime)
ibv_query_gid(context, port, gid_idx, &local_gid);
```

**URMA code pattern**:
```c
// 1. Must specify eid_index when creating context (local EID determined here)
urma_context_t *ctx = urma_create_context(device, eid_idx);  // specified here

// 2. Get local EID (directly from context)
urma_eid_t local_eid = ctx->eid;

// 3. At connection, only need to provide remote_eid
urma_rjetty_t rjetty = {
    .jetty_id = {
        .eid = remote_eid,  // remote EID
        .id = remote_jpn
    },
    .tp_type = URMA_RTP
};
urma_target_jetty_t *tjetty = urma_import_jetty(ctx, &rjetty, NULL);
urma_bind_jetty(jetty, tjetty);
```

**Migration notes**:
- **Must determine eid_idx early**: In URMA, must decide which EID index to use before creating context
- **Entire context shares one EID**: Unlike Verbs, all Jetties in URMA share the same EID
- **Cannot change dynamically**: URMA does not support dynamic gid_index change like Verbs' modify_qp

> Complete resource creation code example see §4 "Combined Jetty Creation".

---

## 2. Memory Registration

### URMA Version

```c
// PD is implicit - no need to allocate

// Register memory segment
urma_seg_cfg_t seg_cfg = {
    .va = (uint64_t)buf,
    .len = size,
    .token_id = NULL,
    .token_value.token = 0xABCDEF,  // security token (must be non-zero!)
    .flag.bs.token_policy = URMA_TOKEN_NONE,
    .flag.bs.cacheable = URMA_NON_CACHEABLE,
    .flag.bs.access = URMA_ACCESS_LOCAL_ONLY,  // must set!
    .flag.bs.token_id_valid = 0,
    .flag.bs.reserved = 0,
    .user_ctx = 0,
    .iova = 0
};
urma_target_seg_t *tseg = urma_register_seg(ctx, &seg_cfg);

// Unregister
urma_unregister_seg(tseg);
```

**Key points**:
- PD is implicit, no need for `ibv_alloc_pd()`
- `sge.tseg` is a pointer to `urma_target_seg_t`, not an integer key
- When `token_policy` requires it, token must be non-zero

### ⚠️ Key: Access flags must be set

`.bs.access` field **must** be explicitly set, otherwise runtime error:
```
urma_check_seg_cfg[2769]|Local only access is not allowed to config with other accesses
```

**Access flag semantics**:
- `URMA_ACCESS_LOCAL_ONLY`: Local access only, no remote access
- When not using `LOCAL_ONLY`: local has full access by default, remote access controlled by READ/WRITE/ATOMIC

**Choose by operation type**:
- `send/recv` (bidirectional): use `URMA_ACCESS_LOCAL_ONLY`
- `RDMA read/write` (unidirectional): use `URMA_ACCESS_READ | URMA_ACCESS_WRITE` (don't use LOCAL_ONLY)
- `Atomic operations`: add `URMA_ACCESS_ATOMIC` on above basis

### ⚠️ Key: Access flags are mutually exclusive

 **`URMA_ACCESS_LOCAL_ONLY` cannot be combined with other access flags:**
```c
// ❌ Wrong - causes runtime error
.flag.bs.access = URMA_ACCESS_LOCAL_ONLY | URMA_ACCESS_READ;

// ✅ Correct - choose one category
.flag.bs.access = URMA_ACCESS_READ | URMA_ACCESS_WRITE;  // for RDMA
.flag.bs.access = URMA_ACCESS_READ | URMA_ACCESS_WRITE | URMA_ACCESS_ATOMIC;  // for RDMA + atomic
.flag.bs.access = URMA_ACCESS_LOCAL_ONLY;  // for send/recv only
```

**From Verbs migration:**
| Verbs Flags | URMA Flags |
|-------------|------------|
| `IBV_ACCESS_LOCAL_WRITE` only | `URMA_ACCESS_LOCAL_ONLY` |
| `IBV_ACCESS_REMOTE_READ | IBV_ACCESS_REMOTE_WRITE` | `URMA_ACCESS_READ | URMA_ACCESS_WRITE` |
| `... | IBV_ACCESS_REMOTE_ATOMIC` | `... | URMA_ACCESS_ATOMIC` |

### urma_reg_seg_flag_t Bit Field Layout

```c
// Wrong - .value sets all bits, including token_policy
urma_reg_seg_flag_t flag = { .value = URMA_ACCESS_LOCAL_ONLY };
// Result: token_policy=1 (URMA_TOKEN_PLAIN_TEXT), not 0 (URMA_TOKEN_NONE)!

// Correct - .bs.xxx sets single field
urma_reg_seg_flag_t flag = {
    .bs.token_policy = URMA_TOKEN_NONE,
    .bs.cacheable = URMA_NON_CACHEABLE,
    .bs.access = URMA_ACCESS_READ | URMA_ACCESS_WRITE,
    .bs.token_id_valid = 0,
    .bs.reserved = 0
};
```

### Common Configurations

```c
// Local access only (development)
urma_reg_seg_flag_t flag = {
    .bs.token_policy = URMA_TOKEN_NONE,
    .bs.cacheable = URMA_NON_CACHEABLE,
    .bs.access = URMA_ACCESS_LOCAL_ONLY,
    .bs.token_id_valid = 0,
    .bs.reserved = 0
};

// Full remote access (production)
urma_reg_seg_flag_t flag = {
    .bs.token_policy = URMA_TOKEN_PLAIN_TEXT,
    .bs.cacheable = URMA_NON_CACHEABLE,
    .bs.access = URMA_ACCESS_READ | URMA_ACCESS_WRITE | URMA_ACCESS_ATOMIC,
    .bs.token_id_valid = 0,
    .bs.reserved = 0
};
```

---

## 3. Completion Queues

### Polling Mode

```c
// Create completion queue (polling mode - no JFCE)
urma_jfc_cfg_t jfc_cfg = {
    .depth = depth,
    .flag.value = 0,
    .jfce = NULL,  // NULL = polling mode
    .user_ctx = 0
};
urma_jfc_t *jfc = urma_create_jfc(ctx, &jfc_cfg);

// Poll completion events
urma_cr_t cr[16];
int ne = urma_poll_jfc(jfc, 16, cr);

// Cleanup
urma_delete_jfc(jfc);
```

**Key points**:
- Each `urma_poll_jfc()` call handles max 16 completion records
- JFC depth must be >= JFR depth + JFS depth

### Event-Driven Mode

```c
// Create JFCE
urma_jfce_t *jfce = urma_create_jfce(ctx);

// Create JFC bound to JFCE
urma_jfc_cfg_t jfc_cfg = {
    .depth = 128,
    .jfce = jfce,
    .user_ctx = 0
};
urma_jfc_t *jfc = urma_create_jfc(ctx, &jfc_cfg);

urma_rearm_jfc(jfc, false);  // initial load

urma_jfc_t *ev_jfc = NULL;
int cnt = urma_wait_jfc(jfce, 1, timeout_ms, &ev_jfc);

urma_rearm_jfc(jfc, false);  // reload

urma_cr_t cr;
urma_poll_jfc(jfc, 1, &cr);

// Parameters: (jfc_array, event_count_array, jfc_array_count)
// - jfc_array: array of JFC pointers to acknowledge
// - event_count_array: array of event counts for each JFC
// - jfc_array_count: number of JFC pointers in array (not event count!)
uint32_t ack_cnt = 1;  // event count to acknowledge
urma_ack_jfc(&ev_jfc, &ack_cnt, 1);  // must: 1 = 1 JFC in array
```

**Event mode sequence**:
```
wait -> rearm -> poll -> ack
```

**Key**: `urma_ack_jfc()` must be called after every `urma_wait_jfc()`.

### Mode Comparison

| Feature | Polling Mode | Event Mode |
|---------|--------------|------------|
| Latency | Very low (μs) | Low (10-100μs) |
| CPU usage | High | Low |
| Requires JFCE | No | Yes |
| Call sequence | `poll → use` | `wait → rearm → poll → ack` |
| Use case | High frequency, low latency | Multiplexing, power saving |

### JFCE Interrupt-Driven Thread Mode

```c
typedef struct {
    urma_context_t *ctx;
    urma_jfce_t *jfce;
    urma_jfc_t *jfc;
    int running;
} event_handler_t;

int event_handler_init(event_handler_t *eh, urma_context_t *ctx) {
    eh->ctx = ctx;
    eh->running = 1;

    eh->jfce = urma_create_jfce(ctx);
    if (!eh->jfce) return -1;

    urma_jfc_cfg_t jfc_cfg = {
        .depth = 128,
        .jfce = eh->jfce,
        .user_ctx = 0
    };
    eh->jfc = urma_create_jfc(ctx, &jfc_cfg);
    if (!eh->jfc) {
        urma_delete_jfce(eh->jfce);
        return -1;
    }

    urma_rearm_jfc(eh->jfc, false);
    return 0;
}

void *event_handler_thread(void *arg) {
    event_handler_t *eh = (event_handler_t *)arg;

    while (eh->running) {
        urma_jfc_t *ev_jfc = NULL;
        int cnt = urma_wait_jfc(eh->jfce, 1, 1000, &ev_jfc);
        if (cnt <= 0) continue;
        if (ev_jfc != eh->jfc) continue;

        urma_cr_t cr;
        while (urma_poll_jfc(eh->jfc, 1, &cr) > 0) {
            if (cr.status == URMA_CR_SUCCESS) {
                // Handle success
            }
        }

        uint32_t ack_cnt = 1;
        urma_ack_jfc(&ev_jfc, &ack_cnt, 1);
        urma_rearm_jfc(eh->jfc, false);
    }

    return NULL;
}

void event_handler_cleanup(event_handler_t *eh) {
    eh->running = 0;
    urma_delete_jfc(eh->jfc);
    urma_delete_jfce(eh->jfce);
}
```

---

## 4. Jetty Connection Flow

### By Transport Mode

URMA uses different connection APIs based on transport mode. See mapping.md for API mapping.

#### RC Mode (Reliable Connection) - Single Jetty

RC mode uses `urma_import_jetty()` + `urma_bind_jetty()`:

```c
// Step 1: Import remote Jetty
urma_rjetty_t rjetty = {
    .jetty_id = { .eid = remote_eid, .uasid = 0, .id = remote_jpn },
    .trans_mode = URMA_TM_RC,
    .policy = URMA_JETTY_GRP_POLICY_RR,
    .type = URMA_JETTY,
    .tp_type = URMA_RTP,  // Key: must set!
    .flag = { .bs.order_type = URMA_DEF_ORDER, .bs.share_tp = 0 }
};
urma_token_t token = { .token = 0xACFE };
urma_target_jetty_t *tjetty = urma_import_jetty(ctx, &rjetty, &token);

// Step 2: Bind local Jetty to remote (RC only!)
urma_bind_jetty(jetty, tjetty);
```

**Key points**:
- Only RC mode uses `urma_bind_jetty()`. Documented in urma_api.h: "Only supported by jetty under URMA_TM_RC"
- Must save `tjetty` pointer for cleanup (see §8)

#### RM Mode (Reliable Message) - Shared JFR

RM mode uses `urma_import_jetty()` (advise deprecated):

```c
// Step 1: Import remote Jetty
urma_rjetty_t rjetty = {
    .jetty_id = { .eid = remote_eid, .uasid = 0, .id = remote_jpn },
    .trans_mode = URMA_TM_RM,
    .policy = URMA_JETTY_GRP_POLICY_RR,
    .type = URMA_JETTY,
    .tp_type = URMA_RTP,
    .flag = {
        .bs.order_type = URMA_DEF_ORDER,
        .bs.share_tp = 0
    }
};
urma_token_t token = { .token = 0xACFE };
urma_target_jetty_t *tjetty = urma_import_jetty(ctx, &rjetty, &token);
```

**Key points**:
- RM mode uses import_jetty only (no advise)
- Must set tp_type = URMA_RTP
- Must save tjetty pointer for cleanup (see §8)

#### UM Mode (Unreliable Message) - Shared JFR

UM mode uses `urma_import_jetty()` (no bind):

```c
// Step 1: Import remote Jetty
urma_rjetty_t rjetty = {
    .jetty_id = { .eid = remote_eid, .uasid = 0, .id = remote_jpn },
    .trans_mode = URMA_TM_UM,
    .policy = URMA_JETTY_GRP_POLICY_RR,
    .type = URMA_JETTY,
    .tp_type = URMA_UTP,  // UM mode uses UTP!
    .flag.bs.order_type = URMA_DEF_ORDER,
    .flag.bs.share_tp = 0
};
urma_token_t token = { .token = 0 };
urma_target_jetty_t *tjetty = urma_import_jetty(ctx, &rjetty, &token);

// Step 2: Set tjetty in send WR
urma_jfs_wr_t wr = {
    .opcode = URMA_OPC_SEND,
    .flag.bs.complete_enable = 1,
    .tjetty = tjetty,  // Key - must set!
    .send.src.sge = &sge,
    .send.src.num_sge = 1
};
urma_post_jetty_send_wr(jetty, &wr, &bad_wr);
```

**Key points**:
- UM mode needs import_jetty (different from earlier docs)
- UM mode uses tp_type = URMA_UTP
- Must set wr.tjetty before sending
- No bind/advise, but still needs import
- Simpler but less reliable (may drop packets)

### Connection Summary

> **Important**: All modes (RC/RM/UM) use shared JFR. Creation flow: create JFR first, then create Jetty passing and setting share_jfr.

| Mode | Transport | Connection API | Cleanup Order |
|------|-----------|----------------|---------------|
| RC | URMA_TM_RC | `urma_import_jetty()` + `urma_bind_jetty()` | unbind → unimport → delete jetty → delete jfr |
| RM | URMA_TM_RM | `urma_import_jetty()` (advise deprecated) | unimport → delete jetty → delete jfr |
| UM | URMA_TM_UM | `urma_import_jetty()` (no bind) | unimport → delete jetty → delete jfr |

Note: All modes need import_jetty; only RC mode needs bind_jetty.

See §8 for complete cleanup code examples.

### Combined Jetty Creation

```c
// 1. Create JFR first (shared by all modes)
urma_jfr_cfg_t jfr_cfg = {
    .depth = 256,
    .trans_mode = URMA_TM_RC,  // must match Jetty's trans_mode
    .max_sge = 1,
    .jfc = jfc,
    .token_value = token,
    .flag = {
        .bs.token_policy = URMA_TOKEN_NONE,
        .bs.tag_matching = URMA_NO_TAG_MATCHING,
        .bs.order_type = URMA_DEF_ORDER
    }
};
urma_jfr_t *jfr = urma_create_jfr(ctx, &jfr_cfg);

// 2. Create Jetty with shared JFR
urma_jetty_cfg_t jetty_cfg = {
    .id = 0,  // auto-assign

    // Key: must set share_jfr flag
    .flag = {
        .bs.share_jfr = URMA_SHARE_JFR
    },

    // Send side (JFS)
    .jfs_cfg = {
        .depth = 16,
        .trans_mode = URMA_TM_RC,  // must match JFR's trans_mode
        .priority = 0,
        .max_sge = 1,
        .rnr_retry = URMA_TYPICAL_RNR_RETRY,
        .err_timeout = URMA_TYPICAL_ERR_TIMEOUT,
        .jfc = jfc,
        .flag = {
            .bs.order_type = URMA_DEF_ORDER  // must match JFR
        },
        .user_ctx = 0
    },

    // Receive side (shared JFR)
    .shared = {
        .jfr = jfr,  // pass shared JFR
        .jfc = jfc
    },

    .user_ctx = 0
};

urma_jetty_t *jetty = urma_create_jetty(ctx, &jetty_cfg);
```

**Key point**: `order_type` in JFS (`jfs_cfg.flag.bs.order_type`) must explicitly match JFR and rjetty, otherwise runtime error.

---

## 5. Send/Recv Operations

### Send Operation

```c
// Prepare local buffer
urma_sge_t sge = {
    .addr = (uint64_t)buf,
    .len = size,
    .tseg = local_tseg
};
urma_sg_t src_sg = { .sge = &sge, .num_sge = 1 };

urma_send_wr_t send_wr = {
    .src = src_sg,
    .target_hint = 0,
    .imm_data = 0,
    .tseg = NULL
};

urma_jfs_wr_t wr = {0};
wr.opcode = URMA_OPC_SEND;
wr.flag.bs.complete_enable = 1;
wr.flag.bs.solicited_enable = 1;
wr.user_ctx = wr_id;
wr.tjetty = t_jetty;
wr.send = send_wr;

urma_jfs_wr_t *bad_wr = NULL;
urma_post_jetty_send_wr(jetty, &wr, &bad_wr);
```

### Send with Immediate Data

```c
urma_send_wr_t send_wr = {
    .src = src_sg,
    .imm_data = IMM_DATA  // immediate data in send.imm_data
};

urma_jfs_wr_t wr = {
    .opcode = URMA_OPC_SEND_IMM,
    .flag.bs.complete_enable = 1,
    .tjetty = t_jetty,
    .user_ctx = wr_id,
    .send = send_wr
};
urma_post_jetty_send_wr(jetty, &wr, &bad_wr);
```

### Recv Operation

```c
// Prepare receive buffer
urma_sge_t sge = {
    .addr = (uint64_t)buf,
    .len = size,
    .tseg = local_tseg
};
urma_sg_t src_sg = { .sge = &sge, .num_sge = 1 };

urma_jfr_wr_t wr = {0};
wr.src = src_sg;
wr.user_ctx = wr_id;
wr.next = NULL;

urma_jfr_wr_t *bad_wr = NULL;
urma_post_jetty_recv_wr(jetty, &wr, &bad_wr);
```

**Key points**:
- Always initialize work requests with `{0}` before setting fields
- `wr.send.src.sge` nested in `urma_send_wr_t.src`
- `wr.src.sge` for receive nested in `urma_jfr_wr_t.src`
- `SEND_IMM` uses `send.imm_data` (different from `WRITE_IMM` using `rw.notify_data`)

---

## 6. RDMA Read/Write Operations

### RDMA Operation src/dst Semantics

**Important**: URMA uses different src/dst semantics for READ and WRITE operations:

| Operation | src | dst | Data Flow |
|-----------|-----|-----|-----------|
| WRITE | **local** address | **remote** address | local → remote |
| WRITE_IMM | **local** address | **remote** address | local → remote |
| READ | **remote** address | **local** address | remote → local |

**Struct definition**:
```c
typedef struct urma_rw_wr {
    urma_sg_t src;  // local va for write, remote va for read
    urma_sg_t dst;  // remote va for write, local va for read
    uint8_t target_hint;
    uint64_t notify_data;  // for WRITE_IMM
} urma_rw_wr_t;
```

### Import Remote Segments (Required for RDMA Operations)

Before RDMA read/write/atomic operations, must import remote memory segments:

```c
// During connection phase, import remote segments
urma_import_seg_flag_t seg_flag = {
    .bs.cacheable = URMA_NON_CACHEABLE,
    .bs.access = URMA_ACCESS_READ | URMA_ACCESS_WRITE | URMA_ACCESS_ATOMIC,
    .bs.mapping = URMA_SEG_NOMAP,
    .bs.reserved = 0
};

urma_target_seg_t *import_tseg = urma_import_seg(
    ctx->urma_ctx,
    &remote_seg,      // from address exchange
    &token,           // matching token
    0,
    seg_flag
);
if (import_tseg == NULL) {
    fprintf(stderr, "Failed to import segment\n");
    return -1;
}
```

### Write Operation

```c
// Prepare local and remote sge
urma_sge_t local_sge = {
    .addr = (uint64_t)local_buf,
    .len = MSG_SIZE,
    .tseg = local_tseg
};
urma_sge_t remote_sge = {
    .addr = remote_va,
    .len = MSG_SIZE,
    .tseg = import_tseg  // must use imported segment!
};

urma_sg_t src_sg = { .sge = &local_sge, .num_sge = 1 };
urma_sg_t dst_sg = { .sge = &remote_sge, .num_sge = 1 };

// WRITE: src=local, dst=remote
urma_rw_wr_t rw = { .src = src_sg, .dst = dst_sg };
urma_jfs_wr_t wr = {
    .opcode = URMA_OPC_WRITE,
    .flag.bs.complete_enable = 1,
    .tjetty = t_jetty,
    .user_ctx = wr_id,
    .rw = rw
};
urma_jfs_wr_t *bad_wr = NULL;
urma_post_jetty_send_wr(jetty, &wr, &bad_wr);
```

### Write with Immediate Data

```c
// Prepare local and remote sge (same as WRITE)
urma_sge_t local_sge = {
    .addr = (uint64_t)local_buf,
    .len = MSG_SIZE,
    .tseg = local_tseg
};
urma_sge_t remote_sge = {
    .addr = remote_va,
    .len = MSG_SIZE,
    .tseg = import_tseg
};

urma_sg_t src_sg = { .sge = &local_sge, .num_sge = 1 };
urma_sg_t dst_sg = { .sge = &remote_sge, .num_sge = 1 };

// WRITE_IMM uses rw.notify_data (not imm_data!)
urma_rw_wr_t rw = {
    .src = src_sg,
    .dst = dst_sg,
    .notify_data = IMM_DATA
};
urma_jfs_wr_t wr = {
    .opcode = URMA_OPC_WRITE_IMM,
    .flag.bs.complete_enable = 1,
    .tjetty = t_jetty,
    .user_ctx = wr_id,
    .rw = rw
};
urma_post_jetty_send_wr(jetty, &wr, &bad_wr);
```

### Read Operation

```c
// Prepare local and remote sge
urma_sge_t local_sge = {
    .addr = (uint64_t)local_buf,
    .len = MSG_SIZE,
    .tseg = local_tseg
};
urma_sge_t remote_sge = {
    .addr = remote_va,
    .len = MSG_SIZE,
    .tseg = import_tseg
};

// READ: src=remote, dst=local (opposite of WRITE)
urma_sg_t src_sg = { .sge = &remote_sge, .num_sge = 1 };  // READ source is remote
urma_sg_t dst_sg = { .sge = &local_sge, .num_sge = 1 };   // READ destination is local

urma_rw_wr_t rw = { .src = src_sg, .dst = dst_sg };
urma_jfs_wr_t wr = {
    .opcode = URMA_OPC_READ,
    .flag.bs.complete_enable = 1,
    .tjetty = t_jetty,
    .user_ctx = wr_id,
    .rw = rw
};
urma_post_jetty_send_wr(jetty, &wr, &bad_wr);
```

### Complete RDMA Operation Lifecycle

```c
// 1. Exchange phase: exchange remote segment info
typedef struct {
    urma_seg_t seg;           // remote segment info
    urma_jetty_id_t jetty_id; // remote Jetty ID
} exchange_info_t;

// 2. Connection phase: import remote segments
urma_target_seg_t *import_seg[test_ctx->num_seg];
for (int i = 0; i < test_ctx->num_seg; i++) {
    import_seg[i] = urma_import_seg(ctx, &remote[i].seg, &token, 0, seg_flag);
}

// 3. Operation phase: use import_seg for RDMA
urma_sge_t remote_sge = {
    .addr = remote_va,
    .len = length,
    .tseg = import_seg[id]  // use imported segment
};

// 4. Cleanup phase: unimport before unregister
for (int i = 0; i < test_ctx->num_seg; i++) {
    urma_unimport_seg(import_seg[i]);
}
urma_unregister_seg(local_tseg);
```

> **Migration tip**: URMA provides high-level wrappers (`urma_write`/`urma_read`/`urma_send`/`urma_recv`), but during migration prefer low-level APIs (`urma_post_jetty_send_wr` etc.) for precise WR field control.

### Immediate Data Field Comparison

| Operation | Field | Location |
|-----------|-------|----------|
| `URMA_OPC_SEND_IMM` | `imm_data` | `wr.send.imm_data` |
| `URMA_OPC_WRITE_IMM` | `notify_data` | `wr.rw.notify_data` |

**Note**: SEND_IMM and WRITE_IMM use different fields to store immediate data.

---

## 7. Address Exchange

### URMA Version

```c
// EID to wire format string
char eid_str[URMA_EID_STR_LEN + 1];
eid_to_wire_gid(&my_dest.eid, eid_str);

// Send: jpn:eid (no PSN)
snprintf(msg, sizeof(msg), "%06x:%s", my_dest.jpn, eid_str);

// Receive
sscanf(msg, "%hx:%s", &rem_dest->jpn, eid_str);
wire_gid_to_eid(eid_str, &rem_dest->eid);
```

**Key points**:
- URMA has no LID - only uses EID (16 bytes)
- URMA has no PSN - managed by kernel, no user-space exchange needed
- Format: `jpn:eid`

---

## 8. Cleanup Order

### Cleanup by Transport Mode

Cleanup order depends on transport mode used during connection.

#### RC Mode (Jetty + import + bind)

RC mode uses `urma_import_jetty()` + `urma_bind_jetty()` for connection:

```c
// 1. Unbind (RC mode only)
urma_unbind_jetty(local_jetty);

// 2. Unimport (release remote Jetty reference)
urma_unimport_jetty(target_jetty);

// 3. Delete local Jetty
urma_delete_jetty(local_jetty);

// 4. Delete shared JFR (after all Jetties destroyed)
urma_delete_jfr(shared_jfr);
```

**Important**: Must save `tjetty` pointer during connection phase for cleanup:
```c
// During connection (pp_connect_ctx):
ctx->tjetty[i] = urma_import_jetty(ctx->context, &rjetty, &token);
urma_bind_jetty(ctx->jetty[i], ctx->tjetty[i]);

// During cleanup:
urma_unbind_jetty(ctx->jetty[i]);
urma_unimport_jetty(ctx->tjetty[i]);
urma_delete_jetty(ctx->jetty[i]);
```

#### RM Mode (Jetty + import)

RM mode uses `urma_import_jetty()` for connection (advise deprecated):

```c
// 1. Unimport (release remote Jetty reference)
urma_unimport_jetty(target_jetty);

// 2. Delete local Jetty
urma_delete_jetty(local_jetty);

// 3. Delete shared JFR (after all Jetties destroyed)
urma_delete_jfr(shared_jfr);
```

#### UM Mode (Jetty + import)

UM mode uses `urma_import_jetty()` for connection (no bind):

```c
// 1. Unimport (release remote Jetty reference)
urma_unimport_jetty(target_jetty);

// 2. Delete local Jetty
urma_delete_jetty(local_jetty);

// 3. Delete shared JFR (after all Jetties destroyed)
urma_delete_jfr(shared_jfr);
```

### Complete Cleanup Sequence

> **Important**: All modes (RC/RM/UM) use shared JFR. Cleanup order: delete all Jetties first, then delete shared JFR.

```c
// 1. Modify Jetty to error state (recommended)
urma_jetty_attr_t attr = { .mask = JETTY_STATE, .state = URMA_JETTY_STATE_ERROR };
urma_modify_jetty(jetty, &attr);

// 2. (RC mode) Unbind - must be before unimport
urma_unbind_jetty(jetty);

// 3. Unimport remote Jetty - release remote Jetty reference
urma_unimport_jetty(tjetty);

// 4. Unimport remote segments - must be before unregister local segments
//    (for remote segments imported during RDMA read/write operations)
urma_unimport_seg(import_tseg);

// 5. Delete local Jetty
urma_delete_jetty(jetty);

// 6. Delete shared JFR (after all Jetties destroyed)
urma_delete_jfr(shared_jfr);

// 7. Delete JFC
urma_delete_jfc(jfc);

// 8. Unregister local memory segments
urma_unregister_seg(tseg);

// 9. Delete event channel
if (jfce) urma_delete_jfce(jfce);

// 10. Delete context
urma_delete_context(ctx);

// 11. Free device list
urma_free_device_list(dev_list);

// 12. Uninitialize URMA
urma_uninit();
```

**Key points**: Order must be:
1. Unbind (RC) - **must be first**
2. Unimport Jetty - **must be after unbind**
3. Unimport segments - **must be before unregister local segments**
4. Delete Jetty/JFR - **must be after all unimports**
5. Delete JFC - **after Jetty/JFR deleted**
6. Unregister segments - **after all resources using them deleted**
7. Delete context/uninit - **last**

Skipping unbind/unimport before delete causes resource leaks.

---

## 9. Inline Send Optimization

```c
int post_send_inline(urma_jetty_t *jetty, urma_target_jetty_t *tjetty,
                     urma_target_seg_t *local_tseg,
                     uint8_t *buf, uint32_t len, uint64_t wr_id) {
    urma_sge_t sge = {0};
    urma_jfs_wr_t wr = {0};
    urma_jfs_wr_t *bad_wr = NULL;

    sge.addr = (uint64_t)buf;
    sge.len = len;

    wr.opcode = URMA_OPC_SEND;
    wr.flag.value = 0;
    wr.flag.bs.complete_enable = 1;
    wr.tjetty = tjetty;
    wr.user_ctx = wr_id;
    wr.send.src.sge = &sge;
    wr.send.src.num_sge = 1;

    // Check if message fits in inline buffer
    if (len <= jetty->jetty_cfg->jfs_cfg.max_inline_data) {
        wr.flag.bs.inline_flag = 1;  // enable inline mode
        // tseg can be NULL when inline
    } else {
        sge.tseg = local_tseg;  // use registered memory
    }

    return urma_post_jetty_send_wr(jfs, &wr, &bad_wr);
}
```

**Use case guidelines**:
| Message Size | Recommendation |
|--------------|----------------|
| < 64 bytes | Always inline |
| 64-256 bytes | Inline if max_inline_data supports |
| > 256 bytes | Use registered memory |

---

## 10. Chained WR Batch Sending

```c
#define BATCH_SIZE 32

typedef struct {
    urma_jfs_t *jfs;
    urma_jfc_t *jfc;
    urma_target_seg_t *local_tseg;
} batch_sender_t;

int batch_send(batch_sender_t *sender, uint8_t **bufs, uint32_t *lens, int count) {
    urma_jfs_wr_t wrs[BATCH_SIZE];
    urma_jfs_wr_t *bad_wr;
    int sent = 0;

    for (int i = 0; i < count && i < BATCH_SIZE; i++) {
        memset(&wrs[i], 0, sizeof(wrs[i]));

        wrs[i].opcode = URMA_OPC_SEND;
        wrs[i].flag.bs.complete_enable = 1;
        wrs[i].user_ctx = (uint64_t)i;

        // Small messages use inline
        if (lens[i] <= sender->jfs->jfs_cfg.max_inline_data) {
            wrs[i].flag.bs.inline_flag = 1;
        }

        wrs[i].send.src.sge = &(urma_sge_t){
            .addr = (uint64_t)bufs[i],
            .len = lens[i],
            .tseg = sender->local_tseg
        };
        wrs[i].send.src.num_sge = 1;

        // Link WRs
        if (i > 0) {
            wrs[i-1].next = &wrs[i];
        }
    }

    // Post batch
    if (urma_post_jetty_send_wr(sender->jfs, &wrs[0], &bad_wr) != URMA_SUCCESS) {
        return -1;
    }

    return count;
}
```

---

## 11. RM vs RC Mode Settings

### RM Mode (Separate JFS + JFR)

```c
// Create separate JFS for sending
urma_jfs_cfg_t jfs_cfg = {
    .depth = 16,
    .trans_mode = URMA_TM_RM,
    .priority = 0,
    .max_sge = 1,
    .jfc = jfc
};
urma_jfs_t *jfs = urma_create_jfs(ctx, &jfs_cfg);

// Create separate JFR for receiving
urma_jfr_cfg_t jfr_cfg = {
    .depth = 16,
    .trans_mode = URMA_TM_RM,
    .jfc = jfc
};
urma_jfr_t *jfr = urma_create_jfr(ctx, &jfr_cfg);

// Import remote JFR (no bind needed)
urma_rjfr_t rjfr = {
    .jfr_id = remote_jfr_id,
    .trans_mode = URMA_TM_RM,
    .flag.value = 0,
    .tp_type = URMA_RTP
};
urma_target_jfr_t *tjfr = urma_import_jfr(ctx, &rjfr, &token);
```

### RC Mode (Single Jetty)

```c
urma_jetty_cfg_t jetty_cfg = {
    .id = 0,
    .jfs_cfg = { .depth = 16, .trans_mode = URMA_TM_RC, .jfc = jfc },
    .shared.jfc = jfc
};
urma_jetty_t *jetty = urma_create_jetty(ctx, &jetty_cfg);

// RC mode needs import + bind
urma_rjetty_t rjetty = {
    .jetty_id = remote_jetty_id,
    .trans_mode = URMA_TM_RC,
    .policy = URMA_JETTY_GRP_POLICY_RR,
    .type = URMA_JETTY,
    .flag.value = 0,
    .tp_type = URMA_RTP
};
urma_target_jetty_t *tjetty = urma_import_jetty(ctx, &rjetty, &token);
urma_bind_jetty(jetty, tjetty);  // RC mode needs bind
```

### Selection Guide

| Scenario | Recommended Mode |
|----------|------------------|
| Bidirectional communication | Separate mode (RM) |
| Simple request-response | Unified mode (RC) |
| Need multi-path support | Separate mode (RM) |
| Lower resource usage | Unified mode (RC) |

---

## 12. Token Management

### Token Lifecycle

```
Register:  local_seg = urma_register_seg(ctx, &seg_cfg)  // token = 0x1234
     ↓
Exchange:  send token to remote via TCP/Socket
     ↓
Import:    remote_seg = urma_import_seg(ctx, &seg, &token, ...)  // must match!
     ↓
Access:    RDMA read/write operations
```

### Token Generation

```c
#include <openssl/rand.h>

urma_token_t generate_token(void) {
    urma_token_t token;
    int ret = RAND_priv_bytes((unsigned char *)&token.token, sizeof(token.token));
    if (ret != 1) {
        token.token = 0xABCDEF;  // fallback to fixed token
    }
    return token;
}
```

### Token Exchange

```c
// Send local token
write(sockfd, &local_token.token, sizeof(local_token.token));

// Receive remote token
urma_token_t remote_token;
read(sockfd, &remote_token.token, sizeof(remote_token.token));

// Use remote token for import
urma_target_seg_t *dst_tseg = urma_import_seg(ctx, &seg, &remote_token, 0, flag);
```

### Token Matching Rules

| Local Policy | Remote Policy | Token Required |
|--------------|---------------|----------------|
| `URMA_TOKEN_NONE` | `URMA_TOKEN_NONE` | No |
| `URMA_TOKEN_PLAIN_TEXT` | `URMA_TOKEN_PLAIN_TEXT` | Yes (must match) |
| `URMA_TOKEN_NONE` | `URMA_TOKEN_PLAIN_TEXT` | Yes (remote requires) |

---

## 13. Port Status Check

```c
int check_urma_device_state(char *dev_name) {
    urma_device_t *urma_dev = urma_get_device_by_name(dev_name);
    if (urma_dev == NULL) {
        fprintf(stderr, "Device %s not found\n", dev_name);
        return -1;
    }

    urma_device_attr_t dev_attr;
    if (urma_query_device(urma_dev, &dev_attr) != URMA_SUCCESS) {
        fprintf(stderr, "Failed to query device %s\n", dev_name);
        return -1;
    }

    for (uint32_t port_idx = 0; port_idx < dev_attr.port_cnt; port_idx++) {
        if (dev_attr.port_attr[port_idx].state == URMA_PORT_ACTIVE) {
            return port_idx + 1;  // return port number starting from 1
        }
    }

    fprintf(stderr, "No active port found on device %s\n", dev_name);
    return -1;
}
```

---

## 14. EID Index Handling

```c
uint32_t get_urma_eid_index(urma_device_t *urma_dev, urma_eid_t *eid) {
    uint32_t eid_cnt;
    urma_eid_info_t *eid_list = urma_get_eid_list(urma_dev, &eid_cnt);
    if (eid_list == NULL) {
        return UINT32_MAX;
    }

    // If eid is NULL, return first available index
    for (uint32_t i = 0; i < eid_cnt; i++) {
        if (eid == NULL || memcmp(eid->raw, eid_list[i].eid.raw, 16) == 0) {
            uint32_t index = eid_list[i].eid_index;
            urma_free_eid_list(eid_list);
            return index;
        }
    }

    urma_free_eid_list(eid_list);
    return UINT32_MAX;
}
```

### Usage Example

```c
urma_device_t *dev = urma_get_device_by_name("ubcore0");
uint32_t eid_index = get_urma_eid_index(dev, NULL);  // get first EID
urma_context_t *ctx = urma_create_context(dev, eid_index);
```

---

## 15. Huge Page Support

```c
#include <ub/ub_hugepage.h>

#define HUGE_PAGE_2MB 2
#define HUGE_PAGE_1GB 1024

urma_target_seg_t *register_with_hugepage(urma_context_t *ctx,
                                           size_t len, int hugepage_size) {
    // Allocate huge page memory
    void *buf = ub_hugemalloc(len, hugepage_size, NULL);
    if (!buf) return NULL;
    memset(buf, 0, len);

    // Register with URMA
    urma_seg_cfg_t seg_cfg = {
        .va = (uint64_t)buf,
        .len = len,
        .token_id = NULL,
        .token_value.token = 0,
        .flag.bs.token_policy = URMA_TOKEN_NONE,
        .flag.bs.cacheable = URMA_NON_CACHEABLE,
        .flag.bs.access = URMA_ACCESS_LOCAL_ONLY,
        .flag.bs.token_id_valid = 0,
        .flag.bs.reserved = 0,
        .user_ctx = 0,
        .iova = 0
    };

    urma_target_seg_t *tseg = urma_register_seg(ctx, &seg_cfg);
    if (!tseg) {
        ub_hugefree(buf, len);
        return NULL;
    }

    return tseg;
}

void unregister_with_hugepage(urma_target_seg_t *tseg, void *buf, size_t len) {
    urma_unregister_seg(tseg);
    ub_hugefree(buf, len);
}
```

**Key points**:
- Use `ub_hugemalloc()` to allocate
- Use `ub_hugefree()` to release (not `free()`)
- Register with `urma_register_seg()` after allocation

---

## 16. JFC Depth Constraints

### Key Constraint

```
JFC depth must be >= JFR depth + JFS depth
```

### Depth Recommendation

```
JFC depth >= sum of associated Jetty queue depths / CR generation interval + number of associated Jetties
```

### Example

```c
// Given: JFR depth = 64, JFS depth = 16
urma_jfc_cfg_t jfc_cfg = {
    .depth = 64 + 16,  // must be >= JFR + JFS depth
    .jfce = NULL,
    .user_ctx = 0
};
urma_jfc_t *jfc = urma_create_jfc(ctx, &jfc_cfg);
```

---

## 17. Buffer Layout Best Practices

### Recommended Layout

```
Buffer layout (for RDMA operations):
[0, MSG_SIZE-1]              : local send buffer / RDMA source
[MSG_SIZE, 2*MSG_SIZE-1]     : local receive buffer
[2*MSG_SIZE, MEM_SIZE-1]     : receive pool (for pre-posting receives)
```

### Example

```c
#define MSG_SIZE 4096
#define MEM_SIZE 0x100000  // 1MB
#define RECV_POOL_START (2 * MSG_SIZE)

void *buf = memalign(PAGE_SIZE, MEM_SIZE);

// Send from offset 0
urma_sge_t send_sge = {
    .addr = (uint64_t)buf,
    .len = MSG_SIZE,
    .tseg = local_tseg
};

// Pre-post receives from receive pool
for (int i = 0; i < BATCH_SIZE; i++) {
    uint64_t offset = RECV_POOL_START + i * MSG_SIZE;
    urma_sge_t recv_sge = {
        .addr = (uint64_t)buf + offset,
        .len = MSG_SIZE,
        .tseg = local_tseg
    };
    // ... post recv with recv_sge ...
}
```

---

## 18. Error Handling Migration

### Verbs Error Handling Pattern

Verbs error handling is based on two conventions:
- Functions returning pointers (`ibv_open_device`, `ibv_create_cq`, etc.): NULL means failure, `errno` set for cause
- Functions returning integers (`ibv_poll_cq`, `ibv_post_send`, etc.): 0 or negative means failure

```c
// Verbs pointer return - check NULL
struct ibv_cq *cq = ibv_create_cq(ctx, 128, NULL, NULL, 0);
if (!cq) {
    perror("ibv_create_cq");
    exit(1);
}

// Verbs integer return - check negative
int ne = ibv_poll_cq(cq, 1, &wc);
if (ne < 0) {
    fprintf(stderr, "poll CQ failed\n");
}
```

### URMA Error Handling Pattern

URMA return value semantics are not unified; must distinguish by category (see mapping.md error code chapter):

```c
// 1. Resource management - returns 0 for success
int status = urma_init(&init_attr);
if (status != URMA_SUCCESS) {   // URMA_SUCCESS == 0
    fprintf(stderr, "urma_init failed: %d\n", status);
    return 1;
}

status = urma_register_seg(ctx, &seg_cfg, &local_seg);
if (status != URMA_SUCCESS) {
    fprintf(stderr, "urma_register_seg failed: %d\n", status);
    return 1;
}

status = urma_create_jfc(ctx, &jfc_cfg, &jfc);
if (status != URMA_SUCCESS) {
    fprintf(stderr, "urma_create_jfc failed: %d\n", status);
    return 1;
}

// 2. Polling/wait - returns >0 for success (returns count)
int cnt = urma_poll_jfc(jfc, 16, crs);
if (cnt > 0) {
    // Success, cnt is completion record count
    for (int i = 0; i < cnt; i++) {
        process_cr(&crs[i]);
    }
} else if (cnt == 0) {
    // No completion events (not an error)
} else {
    // cnt < 0 means error
    fprintf(stderr, "urma_poll_jfc failed: %d\n", cnt);
}

urma_jfc_t *ev_jfc = NULL;
cnt = urma_wait_jfc(jfce, 1, timeout_ms, &ev_jfc);
if (cnt > 0) {
    // Success, received event
    urma_ack_jfc(&ev_jfc, &(uint32_t){1}, 1);  // must call!
} else if (cnt == 0) {
    // Timeout, no events
} else {
    // Error
    fprintf(stderr, "urma_wait_jfc failed: %d\n", cnt);
}

// 3. Pointer return - returns non-NULL for success
urma_context_t *ctx = urma_create_context(dev);
if (!ctx) {
    fprintf(stderr, "urma_create_context failed\n");
    return 1;
}

urma_jfce_t *jfce = urma_create_jfce(ctx);
if (!jfce) {
    fprintf(stderr, "urma_create_jfce failed\n");
    goto cleanup_context;
}
```

### Key Differences

- **Verbs uses `errno` / `perror()`** → **URMA uses return values directly**: URMA functions don't set `errno`; error info obtained via return values
- **`ibv_poll_cq()` returns 0 for no events** → **`urma_poll_jfc()` also returns 0 for no events**, but must distinguish "0=no events" from "<0=error"; cannot use `<= 0` uniformly
- **Verbs `ibv_wc.status` check** → **URMA `cr.status` check**: same semantics, different enum names (see mapping.md completion status mapping)
- **Common migration error**: checking `urma_poll_jfc()` return value with `if (cnt)` or `if (cnt != 0)` — this treats error codes as success. Correct: `if (cnt > 0)`

---

## 19. Device Type Handling

UB devices differ from other devices in memory management:

```c
// Choose memory release method based on device type
if (ctx->urma_ctx->dev->type == URMA_TRANSPORT_UB) {
    munmap(ctx->va, MEM_SIZE);  // UB devices use munmap
} else {
    free(ctx->va);              // other devices use free
}
```

---

## Adding New Examples

When creating new migration patterns:

1. Determine pattern category
2. Provide both Verbs and URMA versions
3. Include key differences in comments
4. Reference `mapping.md` for API names

Format:
```markdown
## Category Name

### URMA Version
```c
// URMA code
```

### Key Differences
- Point 1
- Point 2
```