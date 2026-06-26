package input

import (
	"errors"
	"io"
	"strings"
	"testing"
)

func TestReadLine(t *testing.T) {
	tests := []struct {
		name    string
		input   string
		want    string
		wantErr error
	}{
		{name: "with_newline", input: "hello\n", want: "hello"},
		{name: "without_newline", input: "hello", want: "hello"},
		{name: "with_crlf", input: "hello\r\n", want: "hello"},
		{name: "with_cr_only", input: "hello\r", want: "hello"},
		{name: "empty_eof", input: "", want: "", wantErr: io.EOF},
		{name: "only_newline", input: "\n", want: ""},
		{name: "only_crlf", input: "\r\n", want: ""},
		{name: "multiline_returns_first", input: "first\nsecond\n", want: "first"},
		{name: "url_without_newline", input: "http://localhost/?code=abc&state=xyz", want: "http://localhost/?code=abc&state=xyz"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := ReadLine(strings.NewReader(tt.input))
			if tt.wantErr == nil && err != nil {
				t.Fatalf("ReadLine() error = %v, want nil", err)
			}

			if tt.wantErr != nil && !errors.Is(err, tt.wantErr) {
				t.Fatalf("ReadLine() error = %v, want %v", err, tt.wantErr)
			}

			if got != tt.want {
				t.Fatalf("ReadLine() = %q, want %q", got, tt.want)
			}
		})
	}
}
