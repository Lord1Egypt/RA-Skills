---
name: vcf-loginsight-health
description: Check the health, uptime, and node status of Aria Operations for Logs (Log Insight) in a VCF environment.
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

# VCF Log Insight Health Check

When the user asks to check the health of the Log Insight or Aria Operations for Logs cluster, follow these steps:

1.  **Verify Credentials:** Ensure `LOGINSIGHT_HOST` and `LOGINSIGHT_API_TOKEN` are available in the environment.
2. **Fetch Cluster Health:** Use the `exec` tool to run the following command to check the cluster status:
   ```bash
   curl -s -k -X GET "https://$LOGINSIGHT_HOST/api/v1/health" \
     -H "Authorization: Bearer $LOGINSIGHT_API_TOKEN" \
     -H "Accept: application/json" | jq '.'
   ```
3. **Fetch Node Status:** Use the `exec` tool to run the following command to check individual node uptime and status:
   ```bash
   curl -s -k -X GET "https://$LOGINSIGHT_HOST/api/v1/cluster/nodes" \
     -H "Authorization: Bearer $LOGINSIGHT_API_TOKEN" \
     -H "Accept: application/json" | jq '.nodes[] | {id, ip, status, uptime}'
   ```
4. **Report to User:** Summarize the JSON output into a clean, readable table detailing the overall health and the status of each node. Point out any errors or disconnected nodes explicitly.