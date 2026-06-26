---
name: vcf-loginsight-sddc-errors
description: Extract recent critical SDDC Manager and vCenter error logs from Aria Operations for Logs to assist with VCF troubleshooting.
version: 1.0.1
homepage: https://github.com/kasture-rohit/vcf-openclaw-skills
metadata:
  openclaw:
    requires:
      env:
        - LOGINSIGHT_HOST
        - LOGINSIGHT_API_TOKEN
      bins:
        - curl
        - jq
    primaryEnv: LOGINSIGHT_API_TOKEN
    emoji: ""
---

# Query VCF Critical Errors

When the user asks to find recent errors, investigate failures, or troubleshoot SDDC Manager workflows, follow these steps:

1. **Verify Credentials:** Ensure `LOGINSIGHT_HOST` and `LOGINSIGHT_API_TOKEN` are available in the environment.
2. **Query Recent Errors:** Use the `exec` tool to run the following command. This queries the Log Insight API for recent log entries containing the keyword "error" specifically originating from SDDC Manager or related VCF components:
   ```bash
   curl -s -k -X GET "https://$LOGINSIGHT_HOST/api/v1/events?keyword=error&limit=10" \
     -H "Authorization: Bearer $LOGINSIGHT_API_TOKEN" \
     -H "Accept: application/json" | jq '.events[]? | {timestamp, source, text}'
   ```
3. **Format and Analyze Output:** * Parse the returned JSON payload.
   * Present the logs to the user in a clean, readable format (e.g., bulleted list or table) showing the Timestamp, Source, and the exact Error Text.
   * Provide a brief, logical assessment of what might be failing in the VCF environment based on the context of the error messages. If no errors are found, let the user know the recent workflows appear clean.