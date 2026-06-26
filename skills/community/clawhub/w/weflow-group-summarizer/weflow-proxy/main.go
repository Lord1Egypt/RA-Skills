package main

import (
	"fmt"
	"log"
	"net"
	"net/http"

	"weflow-proxy/proxy"
)

func main() {
	const (
		listenAddr  = "0.0.0.0:5032"
		upstreamURL = "http://127.0.0.1:5031"
	)

	handler := proxy.NewHandler(upstreamURL)

	fmt.Printf("weflow-proxy listening\n")
	if addrs := lanAddresses(); len(addrs) > 0 {
		for _, ip := range addrs {
			fmt.Printf("您可通过此地址访问 Weflow API: http://%s:%s\n", ip, "5032")
		}
	} else {
		fmt.Println("  warning: no LAN addresses detected")
	}
	if err := http.ListenAndServe(listenAddr, handler); err != nil {
		log.Fatal(err)
	}
}

func lanAddresses() []string {
	ifaces, err := net.Interfaces()
	if err != nil {
		return nil
	}
	var ips []string
	for _, iface := range ifaces {
		if iface.Flags&net.FlagUp == 0 || iface.Flags&net.FlagLoopback != 0 {
			continue
		}
		addrs, err := iface.Addrs()
		if err != nil {
			continue
		}
		for _, addr := range addrs {
			ipNet, ok := addr.(*net.IPNet)
			if !ok {
				continue
			}
			if ipNet.IP.To4() == nil {
				continue
			}
			ips = append(ips, ipNet.IP.String())
		}
	}
	return ips
}
