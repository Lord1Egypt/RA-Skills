package cmd

import (
	"testing"
	"time"
)

func TestParseWeekStartMoreCases(t *testing.T) {
	tests := []struct {
		in   string
		want time.Weekday
	}{
		{in: "monday", want: time.Monday},
		{in: "wed", want: time.Wednesday},
		{in: "thurs", want: time.Thursday},
		{in: "fri", want: time.Friday},
		{in: "sat", want: time.Saturday},
	}

	for _, tt := range tests {
		if got, ok := parseWeekStart(tt.in); !ok || got != tt.want {
			t.Fatalf("parseWeekStart(%q) = %v ok=%v", tt.in, got, ok)
		}
	}
}
