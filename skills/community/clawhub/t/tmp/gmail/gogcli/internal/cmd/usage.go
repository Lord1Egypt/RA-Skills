package cmd

import (
	"errors"
	"fmt"
)

func usage(msg string) error {
	return &ExitError{Code: 2, Err: errors.New(msg)}
}

func usagef(format string, args ...any) error {
	return &ExitError{Code: 2, Err: fmt.Errorf(format, args...)}
}
