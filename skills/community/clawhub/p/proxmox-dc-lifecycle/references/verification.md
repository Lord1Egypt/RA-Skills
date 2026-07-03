# Verification — read-only health checks

These are the gates. Run them before and after every lifecycle step. All read-only; safe to run anytime. Execute via QGA against a healthy DC (the FSMO holder) unless noted.

## FSMO roles
```powershell
netdom query fsmo
```
Expect all 5 roles (Schema, Naming, PDC, RID, Infrastructure) on the holder you expect (the FSMO holder). The rebuild target holds **none** of them. If it holds any, transfer them to a healthy DC before demoting:
`Move-ADDirectoryServerOperationMasterRole -Identity <healthyDC> -OperationMasterRole <role> -Confirm:$false`

## Replication summary
```powershell
repadmin /replsummary
```
Expect the failure count = `0 / N` for every source and destination. Any non-zero failure count → stop and diagnose first. A removed DC simply drops out of this table; a promoted DC appears in both source and destination with a zero failure count.

Detailed per-partner failures:
```powershell
repadmin /showrepl * /csv | ConvertFrom-Csv |
  Where-Object { $_."Number of Failures" -ne "0" } |
  Select-Object "Source DSA","Destination DSA","Number of Failures","Last Failure Status"
```

## Who does AD think the DCs are
```powershell
Get-ADDomainController -Filter * | Select Name,IPv4Address,IsGlobalCatalog
# Authoritative DC marker = the nTDSDSA object:
$cfg=(Get-ADRootDSE).configurationNamingContext
Get-ADObject -SearchBase "CN=Sites,$cfg" -LDAPFilter "(objectClass=nTDSDSA)" |
  Select -ExpandProperty distinguishedName
```
**The presence/absence of the `nTDSDSA` object is the prime-directive gate.** Gone = AD no longer sees it as a DC = safe to rebuild the VM.

## dcdiag (deeper health)
```powershell
dcdiag /v   # filter to "passed test|failed test|error|warning" lines
```
Run on the FSMO holder and each surviving DC. Expect every test to pass **except possibly `DFSREvent`**: a `DFSREvent` warning that references a *just-removed* DC (errors 1722/1723/1753, or 9036 "Paused for backup") is benign — DFSR is retrying a partner that no longer exists, and it self-clears. A `DFSREvent` failure that references *surviving, healthy* DCs is worth investigating. Note `SystemLog` can also fail transiently right after a rebuild (errors logged during the install/reboot churn age out of its 60-minute window).

## SYSVOL / NETLOGON + DFSR state (per DC)
```powershell
Get-SmbShare | Where Name -in 'SYSVOL','NETLOGON' | Select Name,Path
Get-WmiObject -Namespace root\MicrosoftDFS -Class dfsrreplicatedfolderinfo |
  Select ReplicatedFolderName,State
```
DFSR `State` codes: 0 Uninitialized, 1 Initialized, 2 Initial Sync, 3 Auto Recovery, **4 Normal**, 5 In Error. A healthy DC shows both shares and `State = 4`. A freshly promoted DC may sit at `2` (initial sync) briefly — that's expected.

## Network identity (when templating a rebuild)
Read a sibling DC's config to mirror it:
```powershell
Get-NetIPConfiguration | ? IPv4Address | % {
  "$($_.InterfaceAlias) $($_.IPv4Address.IPAddress)/$($_.IPv4Address.PrefixLength) gw=$($_.IPv4DefaultGateway.NextHop) dns=$(($_.DNSServer|?{$_.AddressFamily-eq2}).ServerAddresses-join',')"
}
(Get-TimeZone).Id
```
