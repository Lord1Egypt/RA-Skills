import { Command } from "commander";
import {
  buy,
  details,
  orders,
  register,
  search,
  setAddress,
  setEmail,
  setName,
  setPhone,
  settingsPageLink,
  settingsSummary,
  stripePublishableKey
} from "./api.js";
import { pretty, money, printSection } from "./format.js";
import { readConfig, writeConfig } from "./config.js";
import { tokenizeCard } from "./stripe.js";

function amount(value: { amount: number } | null | undefined) {
  return value?.amount ?? null;
}

export async function runCli(argv: string[]) {
  const program = new Command();
  program.name("selva").description("Selva shopping CLI").version("0.1.0");

  program
    .command("register")
    .description("Register and store a new API key")
    .action(async () => {
      const response = await register();
      const existing = await readConfig();

      await writeConfig({
        ...existing,
        apiKey: response.api_key
      });

      console.log(`Registered. API key saved to ~/selva/config.json`);
      console.log(response.message);
    });

  program
    .command("search")
    .description("Search products")
    .argument("<query>", "Search query")
    .option("--raw", "Include full raw provider payloads")
    .action(async (query: string, options: { raw?: boolean }) => {
      const response = await search(query, { includeRaw: options.raw === true });

      if (response.notice) {
        console.log(response.notice);
      }

      printSection("Search Results");
      if (response.pricing_note) {
        console.log(`(${response.pricing_note})`);
      }
      if (!response.products.length) {
        console.log("No products found.");
      }

      for (const [index, item] of response.products.entries()) {
        console.log(`${index + 1}. ${item.selva_id}`);
        console.log(`   ${item.title}`);
        console.log(`   source: ${item.provider} | price: ${money(amount(item.price))}`);
        console.log(`   rating: ${item.rating ?? "n/a"} | reviews: ${item.review_count ?? "n/a"}`);
        const searchMeta = [`delivery: ${item.delivery_estimate ?? "n/a"}`];
        if (item.availability_status !== "unknown") {
          searchMeta.unshift(`availability: ${item.availability_status}`);
        }
        console.log(`   ${searchMeta.join(" | ")}`);
        console.log(`   image: ${item.image_url ?? "n/a"}`);
        console.log(`   url: ${item.url ?? "n/a"}`);
      }

      if (response.errors.length) {
        printSection("Provider Errors");
        for (const error of response.errors) {
          console.log(`${error.provider}: ${error.message}`);
        }
      }

      if (response.raw_providers) {
        printSection("Raw Provider Responses");
        console.log(pretty(response.raw_providers));
      }
    });

  program
    .command("details")
    .description("Get product details")
    .argument("<selva_id>", "Selva product id")
    .action(async (selvaId: string) => {
      const response = await details(selvaId);

      printSection("Product Details");
      if (response.pricing_note) {
        console.log(`(${response.pricing_note})`);
      }
      const p = response.product;
      console.log(`selva_id: ${p.selva_id}`);
      console.log(`title: ${p.title}`);
      console.log(`provider: ${p.provider}`);
      console.log(`price: ${money(amount(p.price))} ${p.price?.currency ?? "USD"}`);
      if (p.price_range?.min || p.price_range?.max) {
        console.log(
          `price_range: min=${money(amount(p.price_range?.min))} max=${money(amount(p.price_range?.max))}`
        );
      }
      console.log(`rating: ${p.rating ?? "n/a"} | reviews: ${p.review_count ?? "n/a"}`);
      const detailMeta = [`delivery: ${p.delivery_estimate ?? "n/a"}`, `prime: ${p.prime_eligible ?? "n/a"}`];
      if (p.availability_status !== "unknown") {
        detailMeta.unshift(`availability: ${p.availability_status} (${p.stock_status_text ?? "n/a"})`);
      }
      console.log(detailMeta.join(" | "));
      console.log(`url: ${p.url}`);
      console.log(`image: ${p.image_url ?? "n/a"}`);
      if (p.images?.length) {
        console.log(`images: ${p.images.join(", ")}`);
      }
      if (p.brand) {
        console.log(`brand: ${p.brand}`);
      }
      if (p.merchant) {
        console.log(`merchant: ${p.merchant.name ?? "n/a"} (${p.merchant.url ?? "n/a"})`);
      }
      if (p.description) {
        console.log(`description: ${p.description}`);
      }
      if (p.item_specifications?.length) {
        printSection("Item Specifications");
        for (const line of p.item_specifications.slice(0, 12)) {
          console.log(`- ${line}`);
        }
      }
      if (p.user_reviews?.length) {
        printSection("User Reviews");
        for (const review of p.user_reviews.slice(0, 5)) {
          const heading = `${review.rating != null ? `${review.rating}/5` : "n/a"}${review.author ? ` by ${review.author}` : ""}${review.title ? ` - ${review.title}` : ""}`;
          console.log(`- ${heading}`);
          console.log(`  ${review.text}`);
        }
      }
      if (p.features?.length) {
        console.log(`features: ${p.features.join(" | ")}`);
      }
      if (p.badges?.length) {
        console.log(`badges: ${p.badges.join(", ")}`);
      }
      if (p.attributes && Object.keys(p.attributes).length) {
        printSection("Detail Attributes");
        for (const [key, values] of Object.entries(p.attributes)) {
          console.log(`${key}: ${values.join(", ")}`);
        }
      }
      printSection("Detail Variants");
      if (!p.variants?.length) {
        console.log("none");
      } else {
        for (const variant of p.variants.slice(0, 12)) {
          console.log(
            `- ${variant.variant_id} | ${variant.title ?? "n/a"} | ${money(amount(variant.price))} ${variant.price?.currency ?? "USD"} | ${variant.availability_status}`
          );
          if (variant.options && Object.keys(variant.options).length) {
            console.log(
              `  options: ${Object.entries(variant.options)
                .map(([k, v]) => `${k}=${v}`)
                .join(", ")}`
            );
          }
          if (variant.checkout_url) {
            console.log(`  checkout: ${variant.checkout_url}`);
          }
        }
        if (p.variants.length > 12) {
          console.log(`...and ${p.variants.length - 12} more`);
        }
      }
    });

  program
    .command("buy")
    .description("Buy a product")
    .argument("<selva_id>", "Selva product id")
    .requiredOption("--method <method>", "Payment method: card|saved")
    .option("--number <card_number>", "Card number for --method card")
    .option("--exp <exp>", "Card expiry MM/YY for --method card")
    .option("--cvv <cvv>", "Card CVV for --method card")
    .action(
      async (
        selvaId: string,
        options: { method: string; number?: string; exp?: string; cvv?: string }
      ) => {
        const method = options.method === "saved" ? "saved" : options.method === "card" ? "card" : null;
        if (!method) {
          throw new Error("--method must be either 'card' or 'saved'.");
        }

        let paymentToken: string | undefined;
        if (method === "card") {
          if (!options.number || !options.exp || !options.cvv) {
            throw new Error("For --method card, provide --number, --exp, and --cvv.");
          }

          const stripeConfig = await stripePublishableKey();
          const publishableKey = stripeConfig.stripe_publishable_key;
          if (!publishableKey) {
            throw new Error("Card tokenization requires STRIPE_PUBLISHABLE_KEY on the API.");
          }

          const tokenized = await tokenizeCard({
            publishableKey,
            number: options.number,
            exp: options.exp,
            cvv: options.cvv
          });

          paymentToken = tokenized.token;
        }

        const response = await buy({
          selva_id: selvaId,
          method,
          payment_token: paymentToken
        });

        printSection("Buy Response");
        const body = response as Record<string, unknown>;
        const orderId = typeof body.order_id === "string" ? body.order_id : null;
        const status = typeof body.status === "string" ? body.status : null;
        const message = typeof body.message === "string" ? body.message : null;
        const emailWarning = typeof body.email_warning === "string" ? body.email_warning : null;

        if (orderId) {
          console.log(`order_id: ${orderId}`);
        }
        if (status) {
          console.log(`status: ${status}`);
        }
        if (message) {
          console.log(`message: ${message}`);
        }
        if (emailWarning) {
          console.log(`email_warning: ${emailWarning}`);
        }

        const product = body.product;
        if (product && typeof product === "object") {
          const p = product as Record<string, unknown>;
          const priceRecord =
            p.price && typeof p.price === "object"
              ? (p.price as { amount?: unknown })
              : null;
          const priceAmount =
            typeof priceRecord?.amount === "number" ? priceRecord.amount : null;
          const availability =
            typeof p.availability_status === "string" ? p.availability_status : null;

          printSection("Product");
          console.log(`${typeof p.selva_id === "string" ? p.selva_id : "n/a"}`);
          console.log(`${typeof p.title === "string" ? p.title : "n/a"}`);
          console.log(
            `source: ${typeof p.provider === "string" ? p.provider : "n/a"} | price: ${money(priceAmount)}`
          );
          console.log(
            `rating: ${typeof p.rating === "number" ? p.rating : "n/a"} | reviews: ${
              typeof p.review_count === "number" ? p.review_count : "n/a"
            }`
          );
          const productMeta = [
            `delivery: ${typeof p.delivery_estimate === "string" ? p.delivery_estimate : "n/a"}`
          ];
          if (availability && availability !== "unknown") {
            productMeta.unshift(`availability: ${availability}`);
          }
          console.log(productMeta.join(" | "));
          console.log(`image: ${typeof p.image_url === "string" ? p.image_url : "n/a"}`);
          console.log(`url: ${typeof p.url === "string" ? p.url : "n/a"}`);
        }

        if (!orderId && !status && (!product || typeof product !== "object")) {
          console.log(pretty(response));
        }
      }
    );

  program
    .command("orders")
    .description("List orders")
    .action(async () => {
      const response = await orders();
      printSection("Orders");
      if (!response.orders.length) {
        console.log("No orders yet.");
        return;
      }

      for (const order of response.orders) {
        console.log(`${order.id}`);
        console.log(`   selva_id: ${order.selva_id}`);
        console.log(`   status: ${order.status} | method: ${order.payment_method}`);
        console.log(
          `   subtotal: ${order.subtotal_amount ? `$${order.subtotal_amount}` : "n/a"} | tax: ${order.tax_amount ? `$${order.tax_amount}` : "$0.00"} | shipping: ${order.shipping_amount ? `$${order.shipping_amount}` : "$0.00"} | total: ${order.total_amount ? `$${order.total_amount}` : "n/a"} ${order.currency}`
        );
        if (order.failure_reason) {
          console.log(`   failure_reason: ${order.failure_reason}`);
        }
        console.log(`   created_at: ${order.created_at}`);
      }
    });

  const settings = program.command("settings").description("Manage and view settings");

  settings.action(async () => {
    const response = await settingsSummary();
    const card = response.settings.card;
    const address = response.settings.address;
    const addressParts = address
      ? [
          address.street,
          address.line2 ?? null,
          address.city,
          address.state,
          `${address.zip} ${address.country}`
        ].filter((value): value is string => Boolean(value && value.trim()))
      : [];
    console.log(`name: ${response.settings.name ?? "unset"}`);
    console.log(`phone: ${response.settings.phone ?? "unset"}`);
    console.log(`address: ${addressParts.length ? addressParts.join(", ") : "unset"}`);
    console.log(
      `threshold_limit: ${
        response.settings.approval_enabled
          ? `$${response.settings.approval_threshold_amount ?? "n/a"} ${response.settings.approval_threshold_currency ?? "USD"}`
          : "unset"
      }`
    );
    console.log(`zip_code: ${response.settings.zip_code ?? "unset"}`);
    console.log(`payment_method: ${card ? `${card.issuer ?? "card"} **** ${card.last4 ?? "????"}` : "not linked"}`);
    console.log(`email: ${response.settings.email ?? "unset"}`);
  });

  settings
    .command("page")
    .description("Generate a settings page URL")
    .action(async () => {
      const response = await settingsPageLink();
      console.log(response.url);
    });

  settings
    .command("set-address")
    .requiredOption("--street <street>", "Street address")
    .option("--line2 <line2>", "Address line 2 (optional)")
    .requiredOption("--city <city>", "City")
    .requiredOption("--state <state>", "State")
    .requiredOption("--zip <zip>", "ZIP code")
    .requiredOption("--country <country>", "Country code")
    .action(
      async (options: {
        street: string;
        line2?: string;
        city: string;
        state: string;
        zip: string;
        country: string;
      }) => {
        await setAddress(options);
        console.log("Address updated.");
      }
    );

  settings
    .command("set-email")
    .requiredOption("--email <email>", "Notification email")
    .action(async (options: { email: string }) => {
      await setEmail(options.email);
      console.log("Email updated.");
    });

  settings
    .command("set-name")
    .requiredOption("--name <name>", "Full name")
    .action(async (options: { name: string }) => {
      await setName(options.name);
      console.log("Name updated.");
    });

  settings
    .command("set-phone")
    .requiredOption("--phone <phone>", "Phone number")
    .action(async (options: { phone: string }) => {
      await setPhone(options.phone);
      console.log("Phone updated.");
    });

  await program.parseAsync(argv);
}
