package cmd

import "strings"

func isConsumerAccount(account string) bool {
	account = strings.TrimSpace(strings.ToLower(account))
	at := strings.LastIndex(account, "@")
	if at == -1 {
		return false
	}
	domain := account[at+1:]
	switch domain {
	case "gmail.com", "googlemail.com":
		return true
	default:
		return false
	}
}
