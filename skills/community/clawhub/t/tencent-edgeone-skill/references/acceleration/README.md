# EdgeOne Site Acceleration Reference

> **Telemetry note:** You are now in module **`acceleration`**. Every `tccli` call you make from this entry must carry `--request-client "tencent-edgeone-skill/1.1.0 module/acceleration"`.

Configuration and operational guidance for site onboarding, domain management, cache purge/prefetch, and HTTPS certificates.

## Files in This Directory

| File | Risk Level | Trigger Scenarios (User says...) |
|---|---|---|
| `zone-onboarding.md` | Medium-High | "Onboard example.com to EO" "Create a new site" "Apply for free certificate after onboarding" |
| `cache-purge.md` | Medium | "Purge all cache under /static/" "Prefetch these URLs" "Check purge task status" |
| `cert-manager.md` | Medium | "Renew certificate that's expiring soon" "Bind new certificate to these domains" "Check certificate status" |
