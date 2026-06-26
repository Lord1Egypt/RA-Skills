"""Deployment helper — legitimate use of risky APIs."""
import subprocess
import os

def deploy_to_server(server_ip, deploy_key_path):
    """Deploy code to remote server via SSH.

    This is a legitimate deployment tool — it NEEDS ssh key access
    and subprocess for scp/ssh commands. But it takes user-controlled
    input (server_ip) which could be abused.
    """
    # User-controlled input goes to subprocess — this IS risky
    subprocess.run(["ssh", "-i", deploy_key_path, f"deploy@{server_ip}", "deploy.sh"])
    subprocess.run(["scp", "-i", deploy_key_path, "dist.tar.gz", f"deploy@{server_ip}:/opt/app/"])

def read_deploy_config():
    """Read deployment configuration."""
    ssh_key = os.path.expanduser("~/.ssh/deploy_key")
    aws_region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    return {"key": ssh_key, "region": aws_region}
