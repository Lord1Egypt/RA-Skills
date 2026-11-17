# Diagnostic Model

Use the smallest fault domain that explains the evidence.

## Client-Specific Issues

Symptoms affect one device or one class of devices while other wired and wireless clients behave normally. Common evidence includes one client with weak signal, high retry rates, stale DHCP lease behavior, device sleep or roaming problems, bad local DNS cache, VPN interference, or heavy client traffic.

## RF/Wi-Fi Issues

Symptoms primarily affect wireless clients and often vary by location, band, AP, time of day, or roaming event. Common evidence includes low RSSI, poor SNR, high retries, crowded channels, DFS/channel-change events, band steering problems, or many clients on one AP while wired clients remain healthy.

## AP or Switching Issues

Symptoms affect clients behind one AP, switch, port, VLAN, or uplink. Common evidence includes an offline or degraded AP/switch, PoE instability, uplink speed downgrade, STP events, high port errors, one AP serving clients without usable upstream connectivity, or wired and wireless failures sharing the same path.

## DHCP/DNS Issues

Clients can associate or reach the gateway but cannot resolve names, obtain leases, renew leases, or consistently reach local services by name. Common evidence includes successful external IP ping with failed or slow DNS, lease exhaustion, DNS server timeout, split-horizon mismatch, or only newly joined clients failing.

## Gateway/WAN Issues

Multiple clients across wired and wireless networks are affected beyond the LAN. Common evidence includes reachable APs but failed gateway reachability, high packet loss to the gateway, failed external IP ping, high WAN latency, ISP outage signals, gateway CPU or memory pressure, or WAN failover events.

## External Service Issues

Local network, DNS, and general external reachability look healthy, but one service or destination is slow or unavailable. Common evidence includes failures limited to one provider, region, app, CDN, game, VPN, or website while unrelated external probes remain normal.
