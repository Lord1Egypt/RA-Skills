#!/usr/bin/env python3
"""
System management abstraction for Ubuntu and CentOS 8.
Provides command matrix for packages, services, networking.
"""

from dataclasses import dataclass
from typing import Optional
import subprocess

@dataclass
class SystemCommand:
    ubuntu: str
    centos: str
    description: str

class SystemManager:
    """
    Ubuntu vs CentOS 8 command matrix.
    """
    
    COMMANDS = {
        "install": SystemCommand(
            ubuntu="apt-get install -y {package}",
            centos="dnf install -y {package}",
            description="Install a package"
        ),
        "remove": SystemCommand(
            ubuntu="apt-get remove -y {package}",
            centos="dnf remove -y {package}",
            description="Remove a package"
        ),
        "update": SystemCommand(
            ubuntu="apt-get update && apt-get upgrade -y",
            centos="dnf update -y",
            description="Update all packages"
        ),
        "search": SystemCommand(
            ubuntu="apt-cache search {package}",
            centos="dnf search {package}",
            description="Search for package"
        ),
        "service_start": SystemCommand(
            ubuntu="systemctl start {service}",
            centos="systemctl start {service}",
            description="Start a service"
        ),
        "service_stop": SystemCommand(
            ubuntu="systemctl stop {service}",
            centos="systemctl stop {service}",
            description="Stop a service"
        ),
        "service_enable": SystemCommand(
            ubuntu="systemctl enable {service}",
            centos="systemctl enable {service}",
            description="Enable service at boot"
        ),
        "service_status": SystemCommand(
            ubuntu="systemctl status {service}",
            centos="systemctl status {service}",
            description="Check service status"
        ),
        "firewall_allow": SystemCommand(
            ubuntu="ufw allow {port}/{proto}",
            centos="firewall-cmd --add-port={port}/{proto} --permanent && firewall-cmd --reload",
            description="Open firewall port"
        ),
        "firewall_status": SystemCommand(
            ubuntu="ufw status",
            centos="firewall-cmd --list-all",
            description="Check firewall status"
        ),
        "add_user": SystemCommand(
            ubuntu="adduser --disabled-password --gecos '' {username}",
            centos="adduser {username}",
            description="Add system user"
        ),
        "add_to_sudo": SystemCommand(
            ubuntu="usermod -aG sudo {username}",
            centos="usermod -aG wheel {username}",
            description="Add user to sudoers"
        ),
    }
    
    # Package name mappings (same software, different package names)
    PACKAGE_MAP = {
        "apache": {"ubuntu": "apache2", "centos": "httpd"},
        "mysql": {"ubuntu": "mysql-server", "centos": "mysql-server"},
        "php": {"ubuntu": "php", "centos": "php"},
        "nodejs": {"ubuntu": "nodejs", "centos": "nodejs"},
        "nginx": {"ubuntu": "nginx", "centos": "nginx"},
    }
    
    def __init__(self, os_type: str):
        self.os = os_type.lower()
        if self.os not in ["ubuntu", "centos"]:
            raise ValueError(f"Unsupported OS: {os_type}")
    
    def get_command(self, action: str, **kwargs) -> str:
        """Get the command for an action."""
        cmd_template = self.COMMANDS.get(action)
        if not cmd_template:
            raise ValueError(f"Unknown action: {action}")
        
        # Get OS-specific command
        if self.os == "ubuntu":
            cmd = cmd_template.ubuntu
        else:
            cmd = cmd_template.centos
        
        # Format with arguments
        return cmd.format(**kwargs)
    
    def get_package_name(self, software: str) -> str:
        """Get correct package name for OS."""
        mapping = self.PACKAGE_MAP.get(software.lower(), {})
        return mapping.get(self.os, software)
    
    def detect_os(self) -> Optional[str]:
        """Auto-detect OS type."""
        try:
            with open("/etc/os-release") as f:
                content = f.read().lower()
                if "ubuntu" in content or "debian" in content:
                    return "ubuntu"
                elif "centos" in content or "rhel" in content or "fedora" in content:
                    return "centos"
        except FileNotFoundError:
            pass
        return None
    
    def generate_script(self, actions: list[dict]) -> str:
        """Generate a shell script for multiple actions."""
        lines = ["#!/bin/bash", "set -e", ""]
        
        for action in actions:
            cmd_name = action.pop("action")
            lines.append(f"# {self.COMMANDS[cmd_name].description}")
            lines.append(self.get_command(cmd_name, **action))
            lines.append("")
        
        return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="System management for Ubuntu/CentOS")
    parser.add_argument("--os", choices=["ubuntu", "centos"], required=True)
    parser.add_argument("--action", required=True, help="Action to perform")
    parser.add_argument("--package", help="Package name")
    parser.add_argument("--service", help="Service name")
    parser.add_argument("--port", help="Port number")
    parser.add_argument("--proto", default="tcp", help="Protocol (tcp/udp)")
    parser.add_argument("--username", help="Username")
    parser.add_argument("--generate", action="store_true", help="Generate script instead of execute")
    args = parser.parse_args()
    
    manager = SystemManager(args.os)
    
    # Build kwargs from args
    kwargs = {}
    if args.package:
        kwargs["package"] = manager.get_package_name(args.package)
    if args.service:
        kwargs["service"] = args.service
    if args.port:
        kwargs["port"] = args.port
        kwargs["proto"] = args.proto
    if args.username:
        kwargs["username"] = args.username
    
    cmd = manager.get_command(args.action, **kwargs)
    
    if args.generate:
        print(cmd)
    else:
        print(f"Executing: {cmd}")
        # subprocess.run(cmd, shell=True)  # Uncomment to actually execute


if __name__ == "__main__":
    main()
