# Common Pitfalls and Solutions

> URMA API Version: 25.12.0
> **Important**: When encountering new issues, add them here to help future migrations.

---

## 1. Token Management

### Problem
URMA memory registration and remote access require security tokens. Incorrect token usage causes failures.

### Symptoms
```
Segment registration failed
Import remote segment failed
Access denied error
```

### Wrong
```c
// Missing token
urma_seg_cfg_t seg_cfg = { .token_value.token = 0, /* ... */ };

// Token policy mismatch
seg_cfg.token_value.token = 0;
seg_cfg.flag.bs.token_policy = URMA_TOKEN_PLAIN_TEXT;  // Conflict!
```

### Correct
```c
// Use non-zero token with security policy
urma_seg_cfg_t seg_cfg = {
    .token_value.token = 0xABCDEF,  // Must be non-zero!
    .flag.bs.token_policy = URMA_TOKEN_PLAIN_TEXT,
    // ...
};

// Or use URMA_TOKEN_NONE when token=0
seg_cfg.token_value.token = 0;
seg_cfg.flag.bs.token_policy = URMA_TOKEN_NONE;

// Or allocate token ID
urma_token_id_t *token_id = urma_alloc_token_id(ctx);
seg_cfg.token_id = token_id;
// Remember to release: urma_free_token_id(token_id);
```

### Token Policy Requirements

| Policy | Token Value Requirement |
|--------|------------------------|
| `URMA_TOKEN_NONE` | Can be 0 |
| `URMA_TOKEN_PLAIN_TEXT` | Must be non-zero |
| `URMA_TOKEN_SIGNED` | Must be non-zero |
| `URMA_TOKEN_ALL_ENCRYPTED` | Must be non-zero |

### Token Exchange
```c
// Exchange via TCP/Socket
write(sockfd, &local_token.token, sizeof(local_token.token));
read(sockfd, &remote_token.token, sizeof(remote_token.token));
// Both sides must use the same token
```

### Related
- `urma_register_seg()` - requires non-zero token when `token_policy != URMA_TOKEN_NONE`
- `urma_import_seg()` - requires token matching registered segment
- `urma_import_jetty()` - if JFR has token, jetty also needs token

### Token Mismatch

Local and remote using different tokens causes import failure. Common causes: not exchanging tokens, token policy mismatch.

```c
// Correct: exchange token via TCP/Socket
// Local side sends token
write(sockfd, &local_token.token, sizeof(local_token.token));

// Remote side receives token
read(sockfd, &remote_token.token, sizeof(remote_token.token));

// Both sides use the same token
urma_import_seg(ctx, &seg, &remote_token, 0, flag);
```

---

## 2. Cleanup Order

### Problem
Incorrect cleanup order causes resource leaks or crashes.

### Wrong
```c
urma_delete_jfc(jfc);      // JFC deleted before Jetty!
urma_delete_jetty(jetty);  // Crash!
```

### Correct
```c
urma_modify_jetty(jetty, &(urma_jetty_attr_t){ .mask = JETTY_STATE, .state = URMA_JETTY_STATE_ERROR });
urma_unbind_jetty(jetty);
urma_unimport_jetty(tjetty);
urma_delete_jetty(jetty);
urma_delete_jfr(jfr);
urma_delete_jfc(jfc);
urma_unregister_seg(tseg);
if (jfce) urma_delete_jfce(jfce);
urma_delete_context(ctx);
urma_uninit();
```

---

## 3. JFC Depth Insufficient

### Problem
JFC depth < JFR depth + JFS depth causes completion event loss and potential data loss.

### Symptoms
```
Completion event loss
Program hangs waiting for completion
Data incomplete
```

### Wrong
```c
// JFR depth = 64, JFS depth = 16
// Need JFC depth = 64 + 16 = 80
urma_jfc_cfg_t jfc_cfg = { .depth = 32 };  // Too small!
```

### Correct
```c
urma_jfc_cfg_t jfc_cfg = {
    .depth = jfr_depth + jfs_depth,  // Minimum: sum of depths
    .jfce = NULL,
    .user_ctx = 0
};

// Recommended: 2x safety margin
urma_jfc_cfg_t jfc_cfg = {
    .depth = (jfr_depth + jfs_depth) * 2,
    .jfce = NULL,
    .user_ctx = 0
};
```

### Depth Calculation Formula

```
Minimum JFC depth = JFR depth + JFS depth
Recommended JFC depth = (JFR depth + JFS depth) * 2
```

### Calculation Example

| Component | Depth |
|-----------|-------|
| JFR (receive queue) | 64 |
| JFS (send queue) | 16 |
| **Minimum JFC** | 80 |
| **Recommended JFC** | 160 |

### Related
- `urma_create_jfc()` - JFC creation
- `urma_create_jfr()` - JFR creation
- `urma_create_jetty()` - Jetty creation (contains JFS)

---

## 4. Polling Limit Exceeded

### Problem
Each call polls more than 16 completion records, causing errors.

### Symptoms
```
Polling returns error
Program exception
```

### Wrong
```c
urma_cr_t cr[32];
urma_poll_jfc(jfc, 32, cr);  // Wrong!
```

### Correct
```c
urma_cr_t cr[16];
urma_poll_jfc(jfc, 16, cr);  // Max 16 per call
```

### Limit
RDMA devices poll max **16 completion records** per call.

### Related
- `urma_poll_jfc()` - JFC polling

---

## 5. Missing urma_ack_jfc()

### Problem
Forgetting to call `urma_ack_jfc()` after `urma_wait_jfc()` causes **resource leaks and system instability**.

### Symptoms
```
Event channel exhaustion
System instability
Cannot receive events anymore
```

### Wrong
```c
urma_wait_jfc(jfce, 1, timeout, &ev_jfc);
urma_poll_jfc(jfc, 1, &cr);
// Missing urma_ack_jfc()!
```

### Correct
```c
urma_wait_jfc(jfce, 1, timeout, &ev_jfc);
urma_rearm_jfc(jfc, false);
urma_poll_jfc(jfc, 1, &cr);
uint32_t ack_cnt = 1;
urma_ack_jfc(&ev_jfc, &ack_cnt, 1);  // Must
```

### Event Mode Sequence

**Required sequence**: `wait → rearm → poll → ack`

Missing any step causes:
- Missing `rearm`: subsequent events won't trigger
- Missing `ack`: resource leak, system may hang
- Wrong `ev_jfc`: undefined behavior

See `patterns.md §3` for complete event mode code examples.

### Validation Rules
- `urma_wait_jfc()` - wait for event
- `urma_ack_jfc()` - acknowledge event (required)
- `urma_rearm_jfc()` - reload to receive next event

---

## 6. EID vs GID Format

### Problem
Verbs uses 8-byte GID. URMA uses 16-byte EID. Direct conversion fails.

### Wrong
```c
memcpy(eid->raw, gid->raw, 8);  // Only copied 8 bytes!
```

### Correct
```c
// Use conversion functions
wire_gid_to_gid(wgid_str, &eid);
gid_to_wire_gid(&eid, wgid_str);
```

---

## 7. Inline Send Size Not Checked

### Problem
Setting `inline_flag` without verifying message size fits device inline buffer.

### Symptoms
```
Data corruption
Send operation fails
Message silently truncated
```

### Wrong
```c
wr.flag.bs.inline_flag = 1;  // Always inline!
```

### Correct
```c
if (len <= jfs->jfs_cfg.max_inline_data) {
    wr.flag.bs.inline_flag = 1;
    // tseg can be NULL when inline
} else {
    wr.flag.bs.inline_flag = 0;
    sge.tseg = local_tseg;
}
```

### Size Guidelines
| Message Size | Inline? | Required max_inline_data |
|--------------|---------|--------------------------|
| < 64 bytes | Yes | Any |
| 64-256 bytes | Maybe | Check device capabilities |
| > 256 bytes | No | Not applicable |

### Related
- `urma_jfs_cfg_t.max_inline_data` - device inline limit
- `urma_jfs_wr_flag_t.bs.inline_flag` - inline enable flag

---

## 8. Remote Jetty Not Bound

### Problem
Attempting to send before Jetty is bound.

### Wrong
```c
// Send immediately after creation, without import/bind
urma_post_jetty_send_wr(jetty, &wr, &bad_wr);  // May fail!
```

### Correct
```c
// Always check remote_jetty is set before sending
if (jetty->remote_jetty == NULL) {
    // Not connected - wait or handle error
}
```

---

## 9. Address Exchange Format

### Problem
Using Verbs address exchange format (including LID) in URMA code.

### Wrong
```c
sprintf(msg, "%04x:%06x:%06x:%s", lid, qpn, psn, gid);  // Includes LID!
sprintf(msg, "%06x:%06x:%s", jpn, psn, eid_str);  // Includes PSN!
```

### Correct
```c
sprintf(msg, "%06x:%s", jpn, eid_str);  // jpn:eid only, no LID, no PSN!
```

### Related
- Complete address exchange code in `patterns.md §7`
- EID macros (EID_FMT, EID_ARGS) in `mapping.md`

---

## 10. Missing share_jfr Flag

### Problem
Omitting flag when creating Jetty with shared JFR.

### Symptoms
```
Cannot create Jetty with shared SRQ
```

### Wrong
```c
urma_jetty_cfg_t jetty_cfg = {0};
jetty_cfg.shared.jfr = srq;  // Missing flag!
```

### Correct
```c
urma_jetty_cfg_t jetty_cfg = {0};
jetty_cfg.flag.bs.share_jfr = 1;  // Key!
jetty_cfg.shared.jfr = srq;
```

### Important Notes
- `jetty_cfg.flag.bs.share_jfr` must be set to 1
- All Jetties share the same `urma_jfr_t` pointer
- Post receive requests to shared JFR, not individual Jetties

### Related APIs
- `urma_create_jfr()` - create SRQ equivalent
- `urma_delete_jfr()` - destroy SRQ
- `urma_post_jfr_wr()` - post to shared queue

---

## 11. Huge Page Memory Incorrect Release

### Problem
Using `free()` on memory allocated by `ub_hugemalloc()` causes corruption.

### Symptoms
```
Segmentation fault
Memory corruption
Double-free error
```

### Wrong
```c
void *buf = ub_hugemalloc(size, hugepage_size, NULL);
free(buf);  // Crash!
```

### Correct
```c
ub_hugefree(buf, size);
```

### Pattern
```c
typedef struct {
    void *buf;
    size_t len;
    int is_hugepage;
} buffer_t;

void safe_free(buffer_t *b) {
    if (b->is_hugepage) {
        ub_hugefree(b->buf, b->len);
    } else {
        free(b->buf);
    }
    free(b);
}
```

### Related
- `ub_hugemalloc()` - allocate huge page memory
- `ub_hugefree()` - free huge page memory

---

## 12. UB Device Memory Incorrect Release

### Problem
Using `free()` on UB transport device memory causes errors.

### Symptoms
```
Memory leak
Double-free corruption
Segmentation fault
```

### Wrong
```c
free(ctx->va);  // May be wrong for UB devices
```

### Correct
```c
if (ctx->urma_ctx->dev->type == URMA_TRANSPORT_UB) {
    munmap(ctx->va, MEM_SIZE);  // UB devices use munmap
} else {
    free(ctx->va);              // other devices use free
}
```

### Device Types
| Device Type | Allocation | Release |
|-------------|------------|---------|
| UB | `mmap()` | `munmap()` |
| Other | `malloc()/memalign()` | `free()` |

### Related
- `urma_context_t.dev->type` - device type field
- `URMA_TRANSPORT_UB` - UB transport type

---

## 13. Remote Jetty Missing tp_type

### Problem
Not setting `tp_type` in `urma_rjetty_t`.

### Wrong
```c
urma_rjetty_t rjetty = {
    .jetty_id = remote_id,
    .trans_mode = URMA_TM_RC,
    // tp_type missing!
};
```

### Correct
```c
urma_rjetty_t rjetty = {
    .jetty_id = remote_id,
    .trans_mode = URMA_TM_RC,
    .tp_type = URMA_RTP,  // Key!
    // ...
};
```

---

## 14. urma_init() Not Called Before URMA APIs

### Problem
Calling `urma_get_device_list()` and other URMA APIs before `urma_init()`.

### Wrong
```c
// urma_get_device_list called before urma_init!
urma_device_t **dev_list = urma_get_device_list(&num_devices);
urma_init(&init_attr);  // Too late!
```

### Correct
```c
// urma_init must be called first
urma_init(&init_attr);
urma_device_t **dev_list = urma_get_device_list(&num_devices);
```

**Key**: `urma_init()` must be called before any URMA API, including `urma_get_device_list()`.

---

## 15. Calling urma_init() Multiple Times

### Problem
Calling `urma_init()` multiple times.

### Wrong
```c
void create_resources() {
    urma_init(&init_attr);  // Called multiple times!
}
```

### Correct
```c
// Call once at program start
urma_init(&init_attr);
// ... all operations ...
// Call once at program exit
urma_uninit();
```

---

## 16. Memory Alignment

### Problem
Unaligned memory causes performance issues or failures.

### Solution
```c
// Use aligned memory allocation
#include <stdlib.h>

// Page alignment
long page_size = sysconf(_SC_PAGESIZE);
void *buf = memalign(page_size, size);

// Or cache line alignment for best performance
void *buf;
posix_memalign(&buf, 64, size);  // 64-byte cache line
```

---

## 17. Event Channel Usage

### Problem
Mixing polling mode and event mode.

### Solution
```c
// Polling mode - no event channel
urma_jfc_cfg_t jfc_cfg = {
    .jfce = NULL,  // no event
    // ...
};

// Event-driven mode
urma_jfce_t *jfce = urma_create_jfce(ctx);
urma_jfc_cfg_t jfc_cfg = {
    .jfce = jfce,  // use event
    // ...
};
```

---

## 18. Work Request Flags

### Problem
Missing flags causes operations not to complete or not generate completion records.

### Solution
```c
// Request completion notification
wr.flag.bs.complete_enable = 1;

// Request remote event
wr.flag.bs.solicited_enable = 1;

// Fence (for read/atomic operations)
wr.flag.bs.fence = 1;

// Inline data (no sge copy)
wr.flag.bs.inline_flag = 1;
```

---

## 19. EID Index Handling

### Problem
Using wrong EID index when creating context.

### Solution
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

---

## 20. Jetty Creation Missing JFR

### Problem
`jfr_cfg` is deprecated; all transport modes (RC/RM/UM) must explicitly create JFR first then share.

### Symptoms
```
Cannot create Jetty
Invalid configuration
```

### Wrong
```c
// Wrong 1: using deprecated jfr_cfg
urma_jetty_cfg_t jetty_cfg = {
    .jfr_cfg = &jfr_cfg,  // deprecated!
    .jfs_cfg = { ... }
};

// Wrong 2: shared not set
urma_jetty_cfg_t jetty_cfg = {
    .jfs_cfg = { ... }
    // missing shared field!
};
```

### Correct
```c
// 1. Create JFR first (required for all modes)
urma_jfr_cfg_t jfr_cfg = {
    .depth = 64,
    .trans_mode = URMA_TM_UM,  // must match Jetty's trans_mode
    .jfc = jfc,
    .flag.bs.token_policy = URMA_TOKEN_NONE,
    .flag.bs.order_type = URMA_DEF_ORDER
};
urma_jfr_t *jfr = urma_create_jfr(ctx, &jfr_cfg);

// 2. Create Jetty and share JFR
urma_jetty_cfg_t jetty_cfg = {
    .flag.bs.share_jfr = URMA_SHARE_JFR,  // must set!
    .jfs_cfg = {
        .depth = 1,
        .trans_mode = URMA_TM_UM,  // must match JFR's trans_mode
        .jfc = jfc,
        .flag.bs.order_type = URMA_DEF_ORDER
    },
    .shared = {
        .jfr = jfr,   // point to created JFR
        .jfc = jfc    // optional: replace jfc
    }
};
urma_jetty_t *jetty = urma_create_jetty(ctx, &jetty_cfg);
```

### Required Checklist (All Modes)
- [ ] Call urma_create_jfr() to create receive queue
- [ ] Set jetty_cfg.flag.bs.share_jfr = URMA_SHARE_JFR
- [ ] Set jetty_cfg.shared.jfr = JFR created above
- [ ] JFR.trans_mode == Jetty.jfs_cfg.trans_mode
- [ ] JFR.flag.bs.order_type == Jetty.jfs_cfg.flag.bs.order_type
- [ ] Call urma_import_jetty() to get remote Jetty (required for all modes!)
- [ ] Set wr.tjetty = imported target Jetty before sending

### Related APIs
- `urma_create_jfr()` - create receive queue
- `urma_create_jetty()` - create send queue with shared JFR
- `URMA_SHARE_JFR` - flag to enable JFR sharing
- `urma_delete_jfr()` - destroy JFR
- `urma_import_jetty()` - import remote Jetty (required for all modes!)
- `urma_unimport_jetty()` - release imported Jetty

---

## 21. Send Work Request Missing tjetty

### Problem
Send work requests for all transport modes (RC/RM/UM) must set tjetty field to imported remote Jetty.

### Symptoms
```
Send operation fails
Operation timeout
No data sent
```

### Wrong
```c
// Missing tjetty - send will fail
urma_jfs_wr_t wr = {
    .opcode = URMA_OPC_SEND,
    .flag.bs.complete_enable = 1,
    // .tjetty not set!
    .send = { .src = { .sge = &sge, .num_sge = 1 } }
};
urma_post_jetty_send_wr(jetty, &wr, &bad_wr);
```

### Correct
```c
// 1. Import remote Jetty (required for all modes!)
urma_rjetty_t rjetty = {
    .jetty_id = { .eid = remote_eid, .uasid = 0, .id = remote_jpn },
    .trans_mode = URMA_TM_UM,
    .type = URMA_JETTY,
    .tp_type = URMA_UTP,  // UM mode uses UTP
    .flag.bs.order_type = URMA_DEF_ORDER
};
urma_target_jetty_t *tjetty = urma_import_jetty(ctx, &rjetty, &token);

// 2. Set tjetty in send WR
urma_jfs_wr_t wr = {
    .opcode = URMA_OPC_SEND,
    .flag.bs.complete_enable = 1,
    .tjetty = tjetty,  // Key - must set!
    .send = { .src = { .sge = &sge, .num_sge = 1 } }
};
urma_post_jetty_send_wr(jetty, &wr, &bad_wr);
```

### tp_type by Transport Mode
| Mode | tp_type | Description |
|------|---------|-------------|
| RC | `URMA_RTP` | Reliable transport protocol |
| RM | `URMA_RTP` | Reliable transport protocol |
| UM | `URMA_UTP` | Unreliable transport protocol |

> **Checklist**: After address exchange, call import_jetty(), store tjetty pointer, set wr.tjetty before each send, set tp_type by mode, call unimport_jetty() during cleanup.

### Related APIs
- `urma_import_jetty()` - import remote Jetty
- `urma_unimport_jetty()` - release imported Jetty
- `urma_post_jetty_send_wr()` - send after setting tjetty

---

## 22. RDMA Operations Missing urma_import_seg()

### Problem
In RDMA read/write/atomic operations, remote memory segment's `tseg` field must be obtained via `urma_import_seg()`. Setting `tseg = NULL` causes runtime failure.

### Symptoms
```
RDMA read/write operation fails
Segmentation fault during RDMA operation
Invalid parameter error
```

### Wrong
```c
// ❌ tseg set to NULL - runtime will fail!
urma_sge_t dst_sge = {
    .addr = remote_va,
    .len = length,
    .tseg = NULL  // Wrong!
};

urma_jfs_wr_t wr = {
    .opcode = URMA_OPC_WRITE,
    .rw = { .dst = { .sge = &dst_sge, .num_sge = 1 }, ... }
};
```

### Correct
```c
// Step 1: Import remote segment during connection phase
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

// Step 2: Use imported tseg in RDMA operation
urma_sge_t dst_sge = {
    .addr = remote_va,
    .len = length,
    .tseg = import_tseg  // Correct!
};
```

### Difference from Verbs

| Verbs | URMA |
|-------|------|
| `sge.lkey` is local integer key | `sge.tseg` is pointer to `urma_target_seg_t` |
| Use `rkey` directly for remote access | Must call `urma_import_seg()` first to get `tseg` |

### Complete Lifecycle

```
1. Exchange phase:    exchange remote segment info (seg.ubva.va, seg.len, etc.)
2. Connection phase:  urma_import_seg() imports remote memory segment
3. Operation phase:   use import_tseg for RDMA read/write/atomic operations
4. Cleanup phase:    urma_unimport_seg() releases reference
```

### Cleanup Order

Must unimport remote segment before unregistering local segment:

```c
// Correct cleanup order
urma_unimport_seg(import_tseg);     // First: unimport remote segment
urma_unregister_seg(local_tseg);    // Then: unregister local segment
```

> **Checklist**: import_seg() during connection, store import_tseg, use import_tseg in RDMA operations (WRITE sets dst_sge.tseg, READ sets src_sge.tseg), unimport_seg before unregister_seg during cleanup.

### Related APIs
- `urma_import_seg()` - import remote memory segment
- `urma_unimport_seg()` - release imported segment
- `urma_post_jetty_send_wr()` - post RDMA read/write with correct tseg

---

## 23. Segment Exchange Incomplete

### Problem
When exchanging segment info for RDMA operations, copying individual fields instead of entire `urma_seg_t` struct causes missing fields like `token_id`, which `urma_import_seg()` needs.

### Symptoms
```
urma_import_seg() fails
Invalid token_id error
RDMA read/write operation fails
```

### Wrong
```c
// ❌ Incomplete - only copied some fields
remote->seg.ubva.eid = ctx->eid;
remote->seg.ubva.uasid = ctx->uasid;
remote->seg.ubva.va = local_tseg->seg.ubva.va;
remote->seg.len = local_tseg->seg.len;
remote->seg.attr.value = flag.value;
// Missing: token_id and other fields!
```

### Correct
```c
// ✅ Correct - copy entire struct
remote->seg = local_tseg->seg;
```

### Required Fields in urma_seg_t

| Field | Purpose | Required for Import |
|-------|---------|---------------------|
| `ubva.eid` | Endpoint ID | Yes |
| `ubva.uasid` | User address space ID | Yes |
| `ubva.va` | Virtual address | Yes |
| `len` | Segment length | Yes |
| `attr` | Segment attributes | Yes |
| `token_id` | Token ID | Yes (if token_id_valid) |

### Complete Exchange Example

```c
// Local side: register segment
urma_target_seg_t *local_tseg = urma_register_seg(ctx, &seg_cfg);

// Pack for exchange (complete struct copy)
exchange_msg.seg = local_tseg->seg;

// Remote side: receive and import
urma_target_seg_t *import_tseg = urma_import_seg(ctx, &exchange_msg.seg, &token, 0, flag);
```

### Related
- `urma_register_seg()` - returns `urma_seg_t` containing all fields
- `urma_import_seg()` - requires complete `urma_seg_t`
- `urma_seg_cfg_t.token_id` - required when `attr.bs.token_id_valid = 1`

---

## 24. WRITE_IMM Wrong imm_data Field

### Problem
`URMA_OPC_WRITE_IMM` and `URMA_OPC_SEND_IMM` store immediate data in different fields. Using wrong field causes immediate data to be ignored or corrupted.

### Symptoms
```
Remote did not receive immediate data
Immediate data is garbage
WRITE_WITH_IMM completion event missing imm_data
```

### Wrong
```c
// ❌ Wrong: WRITE_IMM used wrong field
if (opcode == URMA_OPC_WRITE_IMM || opcode == URMA_OPC_SEND_IMM) {
    wr.send.imm_data = IMM_DATA;  // Wrong for WRITE_IMM!
}
```

### Correct
```c
// ✅ Correct: different opcodes use different fields
if (opcode == URMA_OPC_SEND_IMM) {
    wr.send.imm_data = IMM_DATA;      // SEND_IMM: uses send.imm_data
} else if (opcode == URMA_OPC_WRITE_IMM) {
    wr.rw.notify_data = IMM_DATA;     // WRITE_IMM: uses rw.notify_data
}
```

### Field Mapping by Opcode

| Opcode | Struct | Field | Description |
|--------|--------|-------|-------------|
| `URMA_OPC_SEND` | `urma_send_wr_t` | - | No immediate data |
| `URMA_OPC_SEND_IMM` | `urma_send_wr_t` | `imm_data` | Immediate data |
| `URMA_OPC_WRITE` | `urma_rw_wr_t` | - | No immediate data |
| `URMA_OPC_WRITE_IMM` | `urma_rw_wr_t` | `notify_data` | Immediate data (not imm_data!) |

### Struct Definitions

```c
// For SEND operations
typedef struct urma_send_wr {
    urma_sg_t src;
    uint8_t target_hint;
    uint64_t imm_data;       // SEND_IMM uses this field
    urma_target_seg_t *tseg;
} urma_send_wr_t;

// For RDMA write/read operations
typedef struct urma_rw_wr {
    urma_sg_t src;
    urma_sg_t dst;
    uint8_t target_hint;
    uint64_t notify_data;    // WRITE_IMM uses this field (not imm_data!)
} urma_rw_wr_t;
```

### Receiver Side

Receiver gets immediate data via completion record's `cr.imm_data` in both cases:

```c
urma_cr_t cr;
urma_poll_jfc(jfc, 1, &cr);

if (cr.opcode == URMA_CR_OPC_WRITE_WITH_IMM) {
    printf("Received imm_data: %lu\n", cr.imm_data);  // from notify_data
} else if (cr.flag.bs.s_r == 1 && cr.opcode == URMA_CR_OPC_SEND) {
    // SEND with immediate data
    printf("Received imm_data: %lu\n", cr.imm_data);  // from imm_data
}
```

### Related
- `urma_send_wr_t.imm_data` - for SEND_IMM
- `urma_rw_wr_t.notify_data` - for WRITE_IMM
- `urma_cr_t.imm_data` - immediate data in completion record

---

## 25. Access Flag Combination Errors

### Problem
`URMA_ACCESS_LOCAL_ONLY` is mutually exclusive with remote access flags. Combining them causes runtime errors.

### Symptoms
```
Local only access is not allowed to config with other accesses
Segment registration fails
RDMA operations access errors
```

### Wrong
```c
// ❌ LOCAL_ONLY conflicts with remote access flags
.flag.bs.access = URMA_ACCESS_LOCAL_ONLY | URMA_ACCESS_READ | URMA_ACCESS_WRITE;

// ❌ Missing ATOMIC when using CAS/FADD operations
.flag.bs.access = URMA_ACCESS_READ | URMA_ACCESS_WRITE;
// but code uses URMA_OPC_CAS or URMA_OPC_FADD
```

### Correct
```c
// ✅ RDMA read/write only
.flag.bs.access = URMA_ACCESS_READ | URMA_ACCESS_WRITE;

// ✅ RDMA + atomic operations
.flag.bs.access = URMA_ACCESS_READ | URMA_ACCESS_WRITE | URMA_ACCESS_ATOMIC;

// ✅ send/recv only (no RDMA)
.flag.bs.access = URMA_ACCESS_LOCAL_ONLY;
```

### Access Flag Semantics

| Flag | Meaning | Compatible Flags |
|------|---------|------------------|
| `URMA_ACCESS_LOCAL_ONLY` | Local access only | None (mutually exclusive) |
| `URMA_ACCESS_READ` | Remote read | WRITE, ATOMIC |
| `URMA_ACCESS_WRITE` | Remote write | READ, ATOMIC |
| `URMA_ACCESS_ATOMIC` | Remote atomic operations | READ, WRITE |

### Required Checklist
- [ ] If `LOCAL_ONLY` is set, no other access flags should be set
- [ ] If code uses `URMA_OPC_CAS` or `URMA_OPC_FADD`, must include `URMA_ACCESS_ATOMIC`
- [ ] Compare with access flags in original Verbs code during migration

### Related
- `urma_register_seg()` - segment registration with access flags
- `urma_import_seg()` - remote segment import
- `URMA_OPC_CAS`, `URMA_OPC_FADD` - atomic operations

---

## 26. Parameters Exceeding Device Capabilities

### Problem
URMA has device-specific limits that must be checked. Parameters exceeding device capabilities cause runtime errors.

### Symptoms
```
jetty cfg out of range, jfs_depth:8192, max_jfs_depth: 8192, ...
jfs_rsge:13, max_jfs_rsge: 1, ...
```

### Wrong
```c
// ❌ max_rsge set to max_send_sge, but device only supports 1 remote sge
.max_sge = 13,
.max_rsge = 13,  // Wrong! Device max_jfs_rsge = 1

// ❌ Set without checking device capabilities
.depth = user_value,  // may exceed max_jfs_depth
```

### Correct
```c
// ✅ Use device capability limits
urma_jfs_cfg_t jfs_cfg = {
    .depth = ctx->dev_attr.dev_cap.max_jfs_depth,
    .max_sge = (uint8_t)ctx->dev_attr.dev_cap.max_jfs_sge,
    .max_rsge = (uint8_t)ctx->dev_attr.dev_cap.max_jfs_rsge,  // use max_jfs_rsge!
    .max_inline_data = ctx->dev_attr.dev_cap.max_jfs_inline_len,
};

urma_jfr_cfg_t jfr_cfg = {
    .depth = ctx->dev_attr.dev_cap.max_jfr_depth,
    .max_sge = (uint8_t)ctx->dev_attr.dev_cap.max_jfr_sge,
};
```

### URMA-Specific Device Capabilities (No Verbs Equivalent)

| URMA Field | Device Capability | Description |
|------------|-------------------|-------------|
| `max_rsge` | `max_jfs_rsge` | Max remote SGE count (no Verbs equivalent) |
| `max_sge` (JFS) | `max_jfs_sge` | Max local SGE count for send |
| `max_sge` (JFR) | `max_jfr_sge` | Max local SGE count for receive |
| `depth` (JFS) | `max_jfs_depth` | JFS queue depth |
| `depth` (JFR) | `max_jfr_depth` | JFR queue depth |
| `max_inline_data` | `max_jfs_inline_len` | Max inline data length |

### Required Checklist
- [ ] All `depth`, `max_sge`, `max_rsge`, `max_inline_data` values must be ≤ device capabilities
- [ ] `max_rsge` is URMA-specific; use `dev_cap.max_jfs_rsge` (usually = 1)
- [ ] Compare with `urma_device_cap_t` fields, not user-defined constants
- [ ] Read original URMA samples to understand correct parameter sources

### Related
- `urma_query_device()` - query device capabilities
- `urma_device_cap_t` - device capability struct
- `urma_create_jetty()`, `urma_create_jfr()`, `urma_create_jfc()` - resource creation

---

## 27. Return Count Function Check Logic Errors

### Problem
Some URMA functions return counts (positive for success) rather than 0 for success. Checking `ret != 0` or `ret == 0` causes logic errors.

### Affected Functions

| Function | Return Value | Meaning |
|----------|-------------|---------|
| `urma_poll_jfc()` | `> 0` | Success, completion record count |
| `urma_poll_jfc()` | `0` | No completion records available |
| `urma_poll_jfc()` | `< 0` | Error |
| `urma_wait_jfc()` | `> 0` | Success, event count |
| `urma_wait_jfc()` | `0` | Timeout (if timeout specified) |
| `urma_wait_jfc()` | `< 0` | Error |

### Symptoms
```
Success treated as failure
Test exits unexpectedly
Event loop terminates early
```

### Wrong
```c
// ❌ Wrong: ret=1 (success) triggered error handling
ret = urma_wait_jfc(jfce, 1, timeout, &ev_jfc);
if (ret != 0) {
    // This block executes on success!
    return -1;
}

// ❌ Wrong: ret=5 (5 completion records) triggered error handling
ret = urma_poll_jfc(jfc, 16, cr);
if (ret != 0) {
    // This block executes on success!
    return -1;
}
```

### Correct
```c
// ✅ Correct: check <= 0 for failure/timeout
int cnt = urma_wait_jfc(jfce, 1, timeout, &ev_jfc);
if (cnt <= 0) {
    // Handle timeout or error
    continue;
}

// ✅ Correct: use > 0 while loop
int ne;
while ((ne = urma_poll_jfc(jfc, 16, cr)) > 0) {
    // Process ne completion records
    for (int i = 0; i < ne; i++) {
        // Process cr[i]
    }
}

// ✅ Correct: only < 0 is error (0 = no completion records is normal)
ret = urma_poll_jfc(jfc, 1, &cr);
if (ret < 0) {
    // Error handling
} else if (ret > 0) {
    // Process completion records
}
```

### Comparison with Verbs

| Verbs Function | Return Value Semantics | URMA Equivalent | URMA Return Value Semantics |
|----------------|------------------------|-----------------|----------------------------|
| `ibv_poll_cq()` | Returns count (> 0 success) | `urma_poll_jfc()` | Same: returns count |
| `ibv_get_cq_event()` | 0 is success | `urma_wait_jfc()` | Returns count (> 0 success) |

**Key difference**: Verbs' `ibv_get_cq_event()` returns 0 on success, while URMA's `urma_wait_jfc()` returns event count.

### Required Checklist
- [ ] All `urma_poll_jfc()` calls use `> 0` or `<= 0` to check return values, not `== 0` or `!= 0`
- [ ] All `urma_wait_jfc()` calls use `> 0` or `<= 0` to check return values, not `== 0` or `!= 0`
- [ ] Verify that success path is taken when return value > 0

### Related
- `urma_poll_jfc()` - poll completion events
- `urma_wait_jfc()` - wait for events
- `urma_ack_jfc()` - must call after wait

---

## Adding New Pitfalls

When encountering new issues:

1. Determine category
2. Describe symptoms
3. Provide solution
4. Include code examples if applicable

Format:
```markdown
## Category Name

### Problem
Problem description.

### Symptoms
Observed error messages or behaviors.

### Solution
Fix method.

### Code Example
```c
// Correct way
```

### Related APIs
- `api_name()`
```