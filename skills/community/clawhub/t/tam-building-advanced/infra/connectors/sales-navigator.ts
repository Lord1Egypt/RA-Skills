import { defineConnector } from "@cargo-ai/cdk";

// Sales Navigator: the census. LinkedIn's own filters, and every row comes
// back with the LinkedIn company id, the key the whole TAM is merged on.
// Cookieless: no seat, no cookie, never `identityIds`.
export const salesNavigator = defineConnector("sales_navigator", {
  integration: "salesNavigator",
  default: true,
});
