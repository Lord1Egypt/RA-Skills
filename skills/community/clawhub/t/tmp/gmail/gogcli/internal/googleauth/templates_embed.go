package googleauth

import _ "embed"

//go:embed templates/accounts.html
var accountsTemplate string

//go:embed templates/success.html
var successTemplate string

//go:embed templates/error.html
var errorTemplate string

//go:embed templates/cancelled.html
var cancelledTemplate string
