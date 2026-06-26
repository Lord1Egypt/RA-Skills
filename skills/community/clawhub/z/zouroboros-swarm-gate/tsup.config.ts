import { defineConfig } from "tsup";

export default defineConfig({
  entry: {
    index: "src/index.ts",
    cli: "src/cli.ts",
  },
  format: ["esm", "cjs"],
  dts: { entry: "src/index.ts" },
  clean: true,
  target: "node22",
  splitting: false,
  banner: ({ format }) => {
    if (format === "esm") return {};
    return {};
  },
});
