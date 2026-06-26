# soc-deploy-misp

Deploy MISP threat intelligence platform on any Docker-ready Linux host. Handles MariaDB memory tuning automatically, generates API keys via cake CLI.

## Platform Agnostic

This skill deploys the application. It doesn't create infrastructure. Pair with:
- `hyperv-create-vm` for Hyper-V VMs
- `proxmox-create-vm` for Proxmox containers/VMs
- Or any existing Linux host with Docker

## Key Fix: MariaDB OOM

The #1 deployment failure on small hosts. Default InnoDB buffer pool is 2GB, which kills MariaDB on 4GB VMs. This skill auto-calculates the correct `INNODB_BUFFER_POOL_SIZE` based on available RAM.

## What Gets Automated

- Official misp-docker clone and configuration
- MariaDB memory tuning
- Docker Compose deployment
- Admin provisioning
- API key generation via cake CLI
- MCP connection info output

## Requirements

- SSH access to a Linux host with Docker + Compose v2
- At least 3GB RAM free

## Tags

soc, misp, threat-intelligence, security, docker, automation, ioc
