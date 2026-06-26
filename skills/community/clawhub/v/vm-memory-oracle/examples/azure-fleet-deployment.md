# Azure Fleet Deployment Guide

Deploy VM Memory Oracle across a fleet of 20+ Azure VMs using Terraform.

## Prerequisites

- Azure subscription with sufficient quota for your chosen VM SKU
- Terraform >= 1.5
- Azure CLI authenticated (`az login`)

## Terraform Configuration

### Separate Data Disk (Critical)

The memory data disk must be a **separate Azure managed disk** so it survives VM
redeployment. Set `deleteOption: Detach` on the VM's data disk attachment.

```hcl
resource "azurerm_managed_disk" "memory" {
  count                = var.fleet_size
  name                 = "openclaw-memory-disk-${count.index}"
  location             = azurerm_resource_group.main.location
  resource_group_name  = azurerm_resource_group.main.name
  storage_account_type = "Premium_LRS"
  disk_size_gb         = var.memory_disk_size_gb
  create_option        = "Empty"
}

resource "azurerm_virtual_machine_data_disk_attachment" "memory" {
  count              = var.fleet_size
  managed_disk_id    = azurerm_managed_disk.memory[count.index].id
  virtual_machine_id = azurerm_linux_virtual_machine.openclaw[count.index].id
  lun                = 0
  caching            = "ReadWrite"
}
```

### VM SKU Recommendations

| Workload | SKU | Monthly Cost | Notes |
|---|---|---|---|
| Standard (CPU embedding) | Standard_D4s_v5 | ~$140 | 4 vCPUs, 16 GB RAM |
| GPU-accelerated search | Standard_NC4as_T4_v3 | ~$380 | T4 GPU, 7ms search |
| Budget / low traffic | Standard_B4ms | ~$60 | Burstable, not for sustained loads |

### Cloud-Init Integration

Pass the provided `vm-cloud-init.yaml` as custom data:

```hcl
resource "azurerm_linux_virtual_machine" "openclaw" {
  count     = var.fleet_size
  name      = "openclaw-agent-${count.index}"
  size      = var.vm_sku
  custom_data = base64encode(file("${path.module}/cloud-init.yaml"))
  # ... other config ...
}
```

## Disk Sizing Guide

| Fleet Profile | Disk Size | Estimated Cost (Premium SSD) |
|---|---|---|
| Light (< 1K facts per VM) | 16 GB (P3) | ~$2/mo per disk |
| Medium (1K-5K facts) | 32 GB (P4) | ~$5/mo per disk |
| Heavy (5K-10K facts) | 64 GB (P10) | ~$10/mo per disk |

For a 20-VM fleet with 64 GB disks: ~$200/mo in disk costs.

## Backup Strategy

### Azure Disk Snapshots

Schedule automated snapshots after the nightly consolidation completes:

```hcl
# Snapshot policy: daily at 02:00 UTC (after 00:30 consolidation)
resource "azurerm_backup_policy_disk" "memory" {
  name     = "openclaw-memory-daily"
  vault_id = azurerm_data_protection_backup_vault.main.id

  backup_repeating_time_intervals = ["R/2026-01-01T02:00:00+00:00/P1D"]

  default_retention_rule {
    life_cycle {
      duration                 = "P7D"
      data_store_type          = "OperationalStore"
    }
  }
}
```

### Restore Procedure

```bash
# 1. Find the latest snapshot
az snapshot list --resource-group openclaw-fleet \
    --query "[?contains(name, 'openclaw-memory-disk-5')]" \
    --output table

# 2. Create a new disk from snapshot
az disk create --resource-group openclaw-fleet \
    --name openclaw-memory-disk-5-restored \
    --source <snapshot-name> \
    --sku Premium_LRS

# 3. Swap the disk (stop VM first)
az vm stop -g openclaw-fleet -n openclaw-agent-5
az vm disk detach -g openclaw-fleet --vm-name openclaw-agent-5 \
    --name openclaw-memory-disk-5
az vm disk attach -g openclaw-fleet --vm-name openclaw-agent-5 \
    --name openclaw-memory-disk-5-restored --lun 0
az vm start -g openclaw-fleet -n openclaw-agent-5
```

## Fleet-Wide Validation

After deployment, verify all VMs with:

```bash
# Run health check across fleet (using Ansible or az vm run-command)
for i in $(seq 0 19); do
  az vm run-command invoke \
    --resource-group openclaw-fleet \
    --name "openclaw-agent-${i}" \
    --command-id RunShellScript \
    --scripts "openclaw skill run vm-memory-oracle --action health-check && cat /data/memory/health.json"
done
```

Expected output per VM: `"status": "healthy"` with zero warnings.
