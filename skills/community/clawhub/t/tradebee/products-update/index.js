import { appendPreviewNotice, callTradebeeApi, extractFirstRecord, firstPositiveInteger, getApiKeyOrError, getHtmlLengthWithoutImages, hasOwn, isPlainObject, saveBackupToFile, validateAttributes, validateHtmlWithoutH1, validateImages, validateLanguage, validateSeo, validateTags, withDefinedProperties } from "../validation.js";

function buildRestorePayload(snapshot = {}) {
    return withDefinedProperties(
        {
            products_id: firstPositiveInteger(snapshot.products_id),
            productsgroup_id: firstPositiveInteger(snapshot.productsgroup_id, snapshot.group?.productsgroup_id, snapshot.group?.id),
            product_name: snapshot.product_name,
            model: snapshot.model,
            attributes: snapshot.attributes,
            tags: snapshot.tags,
            brief_description: snapshot.brief_description,
            description: snapshot.description,
            seo: snapshot.seo
        },
        [
            "products_id",
            "productsgroup_id",
            "product_name",
            "model",
            "attributes",
            "tags",
            "brief_description",
            "description",
            "seo"
        ]
    );
}

export default async function ProductsUpdate(args = {}) {
    if (!args || typeof args !== "object" || Array.isArray(args)) {
        return {
            status: false,
            msg: "Invalid parameter: request.body. It must be a valid JSON object."
        };
    }

    const { apiKey: API_KEY, error: apiKeyError } = getApiKeyOrError(args);
    if (apiKeyError) return apiKeyError;

    if (!args.confirmation || typeof args.confirmation !== "object" || Array.isArray(args.confirmation)) {
        return {
            status: false,
            msg: "Missing required parameter: confirmation. Before updating a product, require explicit user confirmation that includes the language, target product ID, and payload."
        };
    }

    if (args.confirmation.approved !== true) {
        return {
            status: false,
            msg: "Explicit user confirmation is required before updating a product. Set confirmation.approved=true only after showing the user the language, target product ID, and payload to be changed."
        };
    }

    if (typeof args.confirmation.summary !== "string" || !args.confirmation.summary.trim()) {
        return {
            status: false,
            msg: "Missing required parameter: confirmation.summary. It must summarize the language, target product ID, and payload confirmed by the user."
        };
    }

    const languageError = validateLanguage(args.language);
    if (languageError) {
        return {
            status: false,
            msg: languageError
        };
    }

    if (!isPlainObject(args.products)) {
        return {
            status: false,
            msg: "Missing required parameter: products."
        };
    }

    const productsId = Number(args.products.products_id ?? 0);
    if (!Number.isInteger(productsId) || productsId <= 0) {
        return {
            status: false,
            msg: "Invalid parameter: products.products_id. The product does not exist, does not belong to this account, or does not belong to the selected language. Use products-read with the same language to get the correct products_id first."
        };
    }

    if (hasOwn(args.products, "productsgroup_id")) {
        const productGroupId = Number(args.products.productsgroup_id);
        if (!Number.isInteger(productGroupId) || productGroupId <= 0) {
            return {
                status: false,
                msg: "Invalid parameter: products.productsgroup_id. Omit this field to keep the current group unchanged. If provided, it must be a positive leaf group ID selected from productsgroup-read where is_leaf=true. Parent group IDs and 0 are not allowed."
            };
        }
    }

    if (hasOwn(args.products, "product_name")
        && (typeof args.products.product_name !== "string" || args.products.product_name.length > 300)) {
        return {
            status: false,
            msg: "Invalid parameter: products.product_name. If provided for products-update, it must contain 1 to 300 characters. Omit this field to keep the current name unchanged."
        };
    }

    if (hasOwn(args.products, "model")
        && (typeof args.products.model !== "string" || args.products.model.length > 50)) {
        return {
            status: false,
            msg: "Invalid parameter: products.model. If provided for products-update, it must be 50 characters or fewer. Omit this field to keep the current model unchanged."
        };
    }

    if (hasOwn(args.products, "upload_images")) {
        const imagesError = validateImages(args.products.upload_images, { required: false });
        if (imagesError) {
            return {
                status: false,
                msg: imagesError
            };
        }
    }

    if (hasOwn(args.products, "attributes")) {
        const attributesError = validateAttributes(args.products.attributes);
        if (attributesError) {
            return {
                status: false,
                msg: attributesError
            };
        }
    }

    if (hasOwn(args.products, "tags")) {
        const tagsError = validateTags(args.products.tags, "products.tags", {
            required: false,
            minItems: 0,
            maxItems: 6,
            minTagLength: 3,
            maxTagLength: 50,
            unique: true
        });
        if (tagsError) {
            return {
                status: false,
                msg: "Invalid parameter: products.tags. If provided, supply 0 to 6 unique tags. Each tag must be 3 to 50 characters."
            };
        }
    }

    if (hasOwn(args.products, "brief_description")
        && (typeof args.products.brief_description !== "string" || args.products.brief_description.length > 127)) {
        return {
            status: false,
            msg: "Invalid parameter: products.brief_description. If provided for products-update, it must contain 1 to 127 plain-text characters. Omit this field to keep the current brief description unchanged."
        };
    }

    if (hasOwn(args.products, "description")
        && (typeof args.products.description !== "string" || getHtmlLengthWithoutImages(args.products.description) > 100000)) {
        return {
            status: false,
            msg: "Invalid parameter: products.description. If provided for products-update, it must contain 1 to 100000 HTML characters after removing <img> tags. Omit this field to keep the current detailed description unchanged."
        };
    }

    if (hasOwn(args.products, "description")) {
        const descriptionStructureError = validateHtmlWithoutH1(args.products.description, "products.description", {
            actionLabel: "products-update",
            maxImageCount: 50
        });
        if (descriptionStructureError) {
            return {
                status: false,
                msg: descriptionStructureError
            };
        }
    }

    if (hasOwn(args.products, "seo")) {
        const seoError = validateSeo(args.products.seo, "products", { mode: "update", actionLabel: "products-update" });
        if (seoError) {
            return {
                status: false,
                msg: seoError
            };
        }
    }

    const body = {
        language: args.language,
        products: args.products
    };

    try {
        const backupResponse = await callTradebeeApi(
            "https://platform.tradew.com/openapis/products/read",
            API_KEY,
            {
                language: args.language,
                products_id: productsId,
                productsgroup_id: 0,
                fields: [
                    "products_id",
                    "group",
                    "product_name",
                    "model",
                    "images",
                    "tags",
                    "attributes",
                    "brief_description",
                    "description",
                    "seo",
                    "update_time"
                ],
                pagination: {
                    current_page: 1,
                    page_size: 10
                }
            }
        );

        const backupSnapshot = extractFirstRecord(backupResponse, ["products", "list", "items", "rows"]);
        if (!backupResponse?.status || !backupSnapshot) {
            return {
                status: false,
                msg: "Backup capture failed before products-update. Read the current product with the same language and products_id first, then retry."
            };
        }

        const restorePayload = {
            language: args.language,
            products: buildRestorePayload(backupSnapshot)
        };

        const backupFile = await saveBackupToFile({
            action: "products-update",
            language: args.language,
            entityId: productsId,
            rawReadResponse: backupResponse,
            snapshot: backupSnapshot,
            requestedPayload: body,
            restoreAction: "products-update",
            restorePayload,
            restoreLimitations: [
                "upload_images cannot be auto-restored because the read API does not return original image base64 data."
            ],
            confirmationSummary: args.confirmation.summary
        });

        const result = await callTradebeeApi(
            "https://platform.tradew.com/openapis/products/update",
            API_KEY,
            body
        );

        if (!isPlainObject(result)) {
            return result;
        }

        return appendPreviewNotice({
            ...result,
            backup: {
                captured: true,
                action: "products-update",
                language: args.language,
                entity_id: productsId,
                storage: {
                    type: "file",
                    ...backupFile
                },
                snapshot_source: "read_api_response",
                raw_read_response: backupResponse,
                snapshot: backupSnapshot,
                restore_action: "products-update",
                restore_payload: restorePayload,
                restore_limitations: [
                    "upload_images cannot be auto-restored because the read API does not return original image base64 data."
                ]
            }
        });
    } catch (error) {
        return {
            status: false,
            msg: "Request failed."
        };
    }
}
