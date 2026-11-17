# Stock Check (Step 8)

The ECS instance type is chosen from the live in-stock list in step 6, so `INSTANCE_TYPE` and
`ZONE_ID` are already confirmed — this step reuses them and **skips the ECS stock query**. When RDS
is needed, verify the RDS class is supported in the ECS-available zones and take the intersection for the final `ZONE_ID`.

---

## RDS Zone Verification (only when RDS is needed)

For the ECS-available zones, verify the selected RDS class is supported:

```bash
aliyun rds DescribeAvailableClasses \
  --RegionId "$REGION" --ZoneId "$ZONE_ID" \
  --Engine MySQL --EngineVersion 8.0 \
  --Category Basic --DBInstanceStorageType cloud_essd \
  --CommodityCode bards --OrderType BUY
```

If response contains `$DB_INSTANCE_CLASS` → that zone supports RDS. Take ECS ∩ RDS zone intersection.

---

## Decision Logic

| Result | Action |
|--------|--------|
| No RDS | Use the `ZONE_ID` from step 6, continue |
| RDS, intersection non-empty | Record a `ZONE_ID` from the intersection (use the first), continue |
| RDS, intersection empty | Offer user 2–3 alternatives (different RDS/ECS class, different region) with trade-offs |

---

## Alternative Suggestions

When the intersection is empty, Agent checks alternatives:
- Go back to step 6 and pick another in-stock ECS type
- Go back to step 5 and pick another RDS class
- Switch region (e.g. `ap-southeast-5`, `ap-northeast-1`) and rerun the affected steps

> Any of these changes the step-5/6 selection, so re-run step 7 to regenerate the template
> with the new choice before continuing to steps 8/9.
