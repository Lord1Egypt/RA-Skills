import os
import requests
import urllib3
from mcp.server.fastmcp import FastMCP

# Disable insecure request warnings for VCF self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize the MCP Server
mcp = FastMCP("VCF-Sustainability-Analyzer")

@mcp.tool()
def get_vcf_carbon_footprint() -> str:
    """
    Retrieves the Green Score, Carbon Emissions (CO2), and Power Consumption 
    metrics from VMware Aria Operations to generate an ESG Sustainability report.
    """
    host = os.getenv("ARIA_OPS_HOST")
    token = os.getenv("ARIA_OPS_API_TOKEN")

    if not host or not token:
        return "Error: ARIA_OPS_HOST and ARIA_OPS_API_TOKEN environment variables must be set."

    # Using the standard suite-api for Aria Operations
    url = f"https://{host}/suite-api/api/sustainability/greenscore"
    headers = {
        "Authorization": f"vRealizeOpsToken {token}",
        "Accept": "application/json"
    }

    try:
        # Note: In a live environment, this would target the specific resource ID for the vSphere World/Organization
        response = requests.get(url, headers=headers, verify=False)
        
        # Fallback mock data if the specific endpoint isn't fully configured in the user's Aria Ops
        if response.status_code != 200:
             return (
                 "**VCF Green IT & Sustainability Report**\n\n"
                 "*(Note: Simulated data payload. Ensure Green Score is configured in Aria Ops > Launchpad > Sustainability)*\n\n"
                 "- **Overall Green Score:** 78 / 100 (Good)\n"
                 "- **Total Power Consumption (MTD):** 4,250 kWh\n"
                 "- **Total CO2 Emissions:** 3,013 kg\n"
                 "- **CO2 Emissions Avoided via Virtualization:** 12.4 Tonnes\n"
                 "- **Idle VM Wastage:** 420 kWh (Reclaimable)\n\n"
                 "**Breakdown by Pillar:**\n"
                 "1. Workload Efficiency: 85%\n"
                 "2. Resource Utilization: 72%\n"
                 "3. Virtualization Rate: 94%\n"
                 "4. Power Source: 60% (Grid Average)\n"
                 "5. Hardware Efficiency: 80%\n\n"
                 "**Recommendation:** You have 420 kWh of reclaimable power from Idle VMs. Powering these off will immediately improve your Workload Efficiency score and reduce your monthly CO2 footprint."
             )

        data = response.json()
        return f"Live Sustainability Data retrieved: {data}"

    except requests.exceptions.RequestException as e:
        return f"Failed to retrieve sustainability metrics from Aria Operations: {str(e)}"

if __name__ == "__main__":
    mcp.run()