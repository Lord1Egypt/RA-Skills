# Recover: re-bind the EIP

Applies when diagnosis shows the EIP is `Available` (unbound from the instance), the port is
listening, and the security group already allows it. A frozen (overdue) EIP is not handled here —
only advise the user to renew.

## Get the EIP allocation ID

Prefer `outputs.eip_allocation_id` from the state file; when absent, look it up:

```bash
aliyun vpc DescribeEipAddresses --RegionId <region> --AssociatedInstanceId <ecs-id>
```

If already bound to the current instance, treat it as no-op. If an unbound EIP is found, record its
`AllocationId`.

## Confirmation gate

- Target: EIP `<eip-id>`, region `<region>`.
- Action: bind to ECS `<ecs-id>` (`AssociateEipAddress`).
- Interruption: public entry restored after binding.
- Version change: none.
- New cost: none (EIP already exists).
- Verify: `DescribeEipAddresses` shows `InUse`, then check `/healthz` and the home page.
- On failure: report and stop.

Decline → change nothing.

## Execute (one action)

```bash
aliyun vpc AssociateEipAddress --RegionId <region> --AllocationId <eip-id> --InstanceId <ecs-id>
```

Idempotent: if already bound to this instance, treat as success. Then verify and record the audit
(`workflow.md`).
