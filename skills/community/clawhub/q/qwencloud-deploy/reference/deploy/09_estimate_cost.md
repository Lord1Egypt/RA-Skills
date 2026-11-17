# Template Validation + Cost Estimation (Step 9)

Agent directly executes CLI commands for template validation and cost estimation.

> **Where `$TEMPLATE_URL` comes from**: upload the template generated in step 7 to OSS, i.e.
> `python3 scripts/upload_artifacts.py --template-file <generated-template.yaml> ...`,
> which prints a signed URL; export it as `TEMPLATE_URL` before running the commands below.
> Validation and estimation only inspect resource structure and price, using placeholder
> UserData — artifacts are not involved (they are uploaded in step 10). (ROS must use
> `--TemplateURL`; `--TemplateBody` is blocked by WAF.)

---

## Template Validation

```bash
aliyun ros ValidateTemplate --RegionId "$REGION" --TemplateURL "$TEMPLATE_URL"
```

Non-zero exit → read `Code` + `Message`, fix template, retry.

---

## Cost Estimation

> Pricing requires a `Password` param but never provisions it. Inject a throwaway
> value via env var so no secret-shaped literal lands in shell history:
> `export PRICING_PWD="$(openssl rand -base64 12)!aA1"`.

```bash
aliyun ros GetTemplateEstimateCost \
  --RegionId "$REGION" \
  --TemplateURL "$TEMPLATE_URL" \
  --Parameters.1.ParameterKey AppName        --Parameters.1.ParameterValue "$APP_NAME" \
  --Parameters.2.ParameterKey InstanceType   --Parameters.2.ParameterValue "$INSTANCE_TYPE" \
  --Parameters.3.ParameterKey Password       --Parameters.3.ParameterValue "$PRICING_PWD" \
  --Parameters.4.ParameterKey SystemDiskSize --Parameters.4.ParameterValue "40" \
  --Parameters.5.ParameterKey AppPort    --Parameters.5.ParameterValue "8080" \
  --Parameters.6.ParameterKey ZoneId         --Parameters.6.ParameterValue "$ZONE_ID" \
  --Parameters.7.ParameterKey UserDataScript --Parameters.7.ParameterValue "#!/bin/bash"
```

> With RDS: omit UserDataScript, add RDS parameters instead:
> `DbInstanceClass` (= step-5 `DB_INSTANCE_CLASS`), `DbInstanceStorage` (GiB), `DbName`,
> `DbAccount`, `DbPassword`. `DbInstanceClass`/`DbInstanceStorage` must match the user's
> step-5 selection so the quote reflects the actual RDS class.

---

## Parse Results

Returns `Resources.<LogicalId>.Result.Order.OriginalAmount` (each resource's **hourly** amount).
Sum all to get total hourly price. Currency: always **USD**.

---

## Confirmation Display

AskUserQuestion summary should show:
- Hourly price (USD)
- Full list of billable resources to be created
- Note: does not include network traffic, snapshots, OSS storage, or other dynamic costs
