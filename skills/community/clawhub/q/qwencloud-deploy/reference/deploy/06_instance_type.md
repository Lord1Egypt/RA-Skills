# Instance Type Selection (Step 6)

Topology is fixed: single ECS + EIP + VPC + SG. The instance type is chosen from the list of
types that are **actually in stock in the current region**.

---

## Fetch in-stock instance types

First query the pay-as-you-go types actually in stock in the region:

```bash
aliyun ecs DescribeAvailableResource \
  --RegionId "$REGION" \
  --DestinationResource InstanceType \
  --InstanceChargeType PostPaid
```

From `AvailableZones.AvailableZone[]`, collect `SupportedResources.SupportedResource[].Value`
(the instance type ID) where `StatusCategory` is `WithStock`, and record its `ZoneId`
(a type may be in stock in multiple zones).

Then fill in vCPU / memory for each type:

```bash
aliyun ecs DescribeInstanceTypes --RegionId "$REGION"
```

Join on `InstanceTypeId`; take `CpuCoreCount` (vCPU) and `MemorySize` (GiB).

---

## Denoise filter

Present only regular types suitable for a lightweight single node; drop the noise:

- **Keep**: general / compute / memory / shared & burstable families
  (`ecs.g*` / `ecs.c*` / `ecs.r*` / `ecs.e*` / `ecs.u*` / `ecs.t*` / `ecs.s*`, etc.).
- **Drop**: GPU / FPGA (`ecs.gn*`, `ecs.vgn*`, `ecs.f*`), bare metal (`ecs.ebm*`, `.metal`),
  oversized types with vCPU > 16 or memory > 32 GiB, and non-x86 special architectures.
- Dedupe, sort ascending by vCPU then memory, and list every type individually.

If the filtered list is empty (no regular type in stock in this region), give the
alternatives from "Step 8 · Alternatives" (switch region / type).

---

## Present and select (AskUserQuestion)

List the filtered, sorted types one per line, each showing `type ID · vCPU/memory`, and let the
user pick one. Price is not shown here (step 9's live quote is authoritative), avoiding drift-prone estimates.

---

## Output

- `INSTANCE_TYPE`: user-selected ECS instance type ID
- `ZONE_ID`: an availability zone where that type is in stock (pick one if several)

---

## Notes

- Every presented type comes from the live in-stock result, so the user's choice is already stock-verified; step 8 reuses it and skips the ECS stock query.
- Actual price is confirmed in step 9 (cost estimation).
