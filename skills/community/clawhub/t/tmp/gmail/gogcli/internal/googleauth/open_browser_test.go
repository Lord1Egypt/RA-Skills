package googleauth

import "testing"

func TestOpenBrowserCommand(t *testing.T) {
	name, args := openBrowserCommand("https://example.com", "darwin")
	if name != "open" || len(args) != 1 || args[0] != "https://example.com" {
		t.Fatalf("darwin: %q %#v", name, args)
	}

	name, args = openBrowserCommand("https://example.com", "windows")
	if name != "rundll32" || len(args) != 2 || args[1] != "https://example.com" {
		t.Fatalf("windows: %q %#v", name, args)
	}

	name, args = openBrowserCommand("https://example.com", "linux")
	if name != "xdg-open" || len(args) != 1 || args[0] != "https://example.com" {
		t.Fatalf("linux: %q %#v", name, args)
	}
}

func TestOpenBrowser_UsesStartCommand(t *testing.T) {
	orig := startCommand

	t.Cleanup(func() { startCommand = orig })

	var gotName string
	var gotArgs []string
	startCommand = func(name string, args ...string) error {
		gotName = name

		gotArgs = append([]string(nil), args...)

		return nil
	}

	if err := openBrowser("https://example.com"); err != nil {
		t.Fatalf("openBrowser: %v", err)
	}

	if gotName == "" || len(gotArgs) == 0 {
		t.Fatalf("expected startCommand to be called")
	}

	if gotArgs[len(gotArgs)-1] != "https://example.com" {
		t.Fatalf("unexpected args: %q %#v", gotName, gotArgs)
	}
}
