package main

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestMainUpdatesReadme(t *testing.T) {
	orig, _ := os.Getwd()

	dir := t.TempDir()
	if err := os.Chdir(dir); err != nil {
		t.Fatalf("chdir: %v", err)
	}

	t.Cleanup(func() { _ = os.Chdir(orig) })

	readme := filepath.Join(dir, "README.md")
	if err := os.WriteFile(readme, []byte("# Test\n"+startMarker+"\n"+endMarker+"\n"), 0o600); err != nil {
		t.Fatalf("write README: %v", err)
	}

	main()

	updated, err := os.ReadFile(readme)
	if err != nil {
		t.Fatalf("read README: %v", err)
	}

	text := string(updated)
	if !strings.Contains(text, startMarker) || !strings.Contains(text, endMarker) {
		t.Fatalf("missing markers: %q", text)
	}

	if !strings.Contains(text, "|") {
		t.Fatalf("expected markdown table: %q", text)
	}
}
