# Common Examples (.rsc)

Refer to the official manual for detailed syntax:
https://help.mikrotik.com/docs/spaces/ROS/pages/47579229/Scripting

## IP Address – idempotent add
```
# adds address to /interface only if it does not exist
:local iface "bridge";
:local addr "192.168.88.1/24";
:if ([:len [/ip address find where interface=$iface and address=$addr]] = 0) do={
    /ip address add interface=$iface address=$addr comment="defconf"
}
```

## Firewall Filter – single rule
```
# accepts DNS on forward chain if it does not exist
:local cm "allow-dns";
:if ([:len [/ip firewall filter find where chain=forward and protocol=udp and dst-port=53 and action=accept and comment=$cm]] = 0) do={
    /ip firewall filter add chain=forward protocol=udp dst-port=53 action=accept comment=$cm
}
```

## DHCP Client – add via lenient scheduler
```
/system script add name=add-dhcp owner=admin policy=read,write source="/ip dhcp-client add interface=ether2; :put \"Added DHCP\"";
/system scheduler add name=run-add-dhcp interval=10s on-event="/system script run add-dhcp" policy=read,write
```

## Single script per instance
```
:if ([/system script job print count-only as-value where script=[:jobname]] > 1) do={
  :error "script instance already running"
}
```

## Import with dry-run and error handling (≥ 7.16.x)
```
# Pass 1: parse-only. Reports every syntax error without touching config.
import test.rsc verbose=yes dry-run

# Pass 2a: import's own on-error parameter (added in 7.16.x).
# Catches parse-time failures of the import command itself.
:do { import test.rsc } on-error={ :put "Failure" }

# Pass 2b: general :onerror with the error message bound to a variable.
# Works on any command that raises, not just import.
:onerror e in={ import test.rsc } do={ :put "Failure - $e" }
```

## Retry with error handling
```
# Fetch a remote file with up to 3 retries, logging each failure.
:local url "https://example.com/config.rsc";
:local ok false;
:onerror e in={
    :retry command={
        /tool fetch url=$url dst-path="downloaded.rsc"
        :set ok true
    } delay=5 max=3
} do={
    :log error "fetch failed after retries: $e"
}
:if ($ok) do={
    :do { import downloaded.rsc } on-error={ :log error "import failed" }
}
```

## Remove by find (avoid fixed IDs)
```
# remove rule by comment — note the `where` filter; a bare [find] would match EVERY rule.
/ip firewall filter remove [find where comment="old-rule"]
```
