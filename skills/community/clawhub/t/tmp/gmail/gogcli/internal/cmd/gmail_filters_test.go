package cmd

import "testing"

func TestFiltersCommandsExist(t *testing.T) {
	// Unit tests for the actual API calls live in integration; here we just ensure
	// the commands exist and are properly structured. (Compile-time coverage.)
	_ = GmailFiltersCmd{}
	_ = GmailFiltersListCmd{}
	_ = GmailFiltersGetCmd{}
	_ = GmailFiltersCreateCmd{}
	_ = GmailFiltersDeleteCmd{}
}
