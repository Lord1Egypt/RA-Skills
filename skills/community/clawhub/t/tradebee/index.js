import blogCreate from "./blog-create/index.js";
import blogDelete from "./blog-delete/index.js";
import blogRead from "./blog-read/index.js";
import blogUpdate from "./blog-update/index.js";
import customPageCreate from "./custompage-create/index.js";
import customPageDelete from "./custompage-delete/index.js";
import customPageRead from "./custompage-read/index.js";
import customPageUpdate from "./custompage-update/index.js";
import blogGroupCreate from "./bloggroup-create/index.js";
import blogGroupDelete from "./bloggroup-delete/index.js";
import blogGroupRead from "./bloggroup-read/index.js";
import blogGroupUpdate from "./bloggroup-update/index.js";
import faqCreate from "./faq-create/index.js";
import faqDelete from "./faq-delete/index.js";
import faqRead from "./faq-read/index.js";
import faqUpdate from "./faq-update/index.js";
import faqGroupCreate from "./faqgroup-create/index.js";
import faqGroupDelete from "./faqgroup-delete/index.js";
import faqGroupRead from "./faqgroup-read/index.js";
import faqGroupUpdate from "./faqgroup-update/index.js";
import inquiryRead from "./inquiry-read/index.js";
import keywordsRank from "./keywords-rank/index.js";
import languagesGet from "./languages-get/index.js";
import productsCreate from "./products-create/index.js";
import productsDelete from "./products-delete/index.js";
import productsRead from "./products-read/index.js";
import productsUpdate from "./products-update/index.js";
import productsGroupCreate from "./productsgroup-create/index.js";
import productsGroupDelete from "./productsgroup-delete/index.js";
import productsGroupRead from "./productsgroup-read/index.js";
import productsGroupUpdate from "./productsgroup-update/index.js";
import ruleGet from "./rule-get/index.js";
import visitorRecent from "./visitor-recent/index.js";
import { isPlainObject } from "./validation.js";

const READ_ACTIONS = new Set([
    "blog-read",
    "bloggroup-read",
    "custompage-read",
    "faq-read",
    "faqgroup-read",
    "inquiry-read",
    "keywords-rank",
    "languages-get",
    "products-read",
    "productsgroup-read",
    "rule-get",
    "visitor-recent"
]);

const MUTATION_ACTIONS = new Set([
    "blog-create",
    "blog-delete",
    "blog-update",
    "bloggroup-create",
    "bloggroup-delete",
    "bloggroup-update",
    "custompage-create",
    "custompage-delete",
    "custompage-update",
    "faq-create",
    "faq-delete",
    "faq-update",
    "faqgroup-create",
    "faqgroup-delete",
    "faqgroup-update",
    "products-create",
    "products-delete",
    "products-update",
    "productsgroup-create",
    "productsgroup-delete",
    "productsgroup-update"
]);

const ACTIONS = {
    "blog-create": {
        handler: blogCreate,
        buildArgs(args) {
            return {
                language: args.language,
                blog: args.blog,
                confirmation: args.confirmation
            };
        }
    },
    "blog-delete": {
        handler: blogDelete,
        buildArgs(args) {
            return {
                language: args.language,
                id_list: args.id_list,
                confirmation: args.confirmation
            };
        }
    },
    "blog-read": {
        handler: blogRead,
        buildArgs(args) {
            return {
                language: args.language,
                blog_id: args.blog_id,
                bloggroup_id: args.bloggroup_id,
                fields: args.fields,
                current_page: args.pagination?.current_page,
                page_size: args.pagination?.page_size
            };
        }
    },
    "blog-update": {
        handler: blogUpdate,
        buildArgs(args) {
            return {
                language: args.language,
                blog: args.blog,
                confirmation: args.confirmation
            };
        }
    },
    "custompage-create": {
        handler: customPageCreate,
        buildArgs(args) {
            return {
                language: args.language,
                custompage: args.custompage,
                confirmation: args.confirmation
            };
        }
    },
    "custompage-delete": {
        handler: customPageDelete,
        buildArgs(args) {
            return {
                language: args.language,
                id_list: args.id_list,
                confirmation: args.confirmation
            };
        }
    },
    "custompage-read": {
        handler: customPageRead,
        buildArgs(args) {
            return {
                language: args.language,
                custompage_id: args.custompage_id,
                fields: args.fields,
                current_page: args.pagination?.current_page,
                page_size: args.pagination?.page_size
            };
        }
    },
    "custompage-update": {
        handler: customPageUpdate,
        buildArgs(args) {
            return {
                language: args.language,
                custompage: args.custompage,
                confirmation: args.confirmation
            };
        }
    },
    "bloggroup-create": {
        handler: blogGroupCreate,
        buildArgs(args) {
            return {
                language: args.language,
                bloggroup: args.bloggroup,
                confirmation: args.confirmation
            };
        }
    },
    "bloggroup-delete": {
        handler: blogGroupDelete,
        buildArgs(args) {
            return {
                language: args.language,
                id_list: args.id_list,
                confirmation: args.confirmation
            };
        }
    },
    "bloggroup-read": {
        handler: blogGroupRead,
        buildArgs(args) {
            return {
                language: args.language,
                bloggroup_id: args.bloggroup_id,
                fields: args.fields,
                current_page: args.pagination?.current_page,
                page_size: args.pagination?.page_size
            };
        }
    },
    "bloggroup-update": {
        handler: blogGroupUpdate,
        buildArgs(args) {
            return {
                language: args.language,
                bloggroup: args.bloggroup,
                confirmation: args.confirmation
            };
        }
    },
    "faq-create": {
        handler: faqCreate,
        buildArgs(args) {
            return {
                language: args.language,
                faq: args.faq,
                confirmation: args.confirmation
            };
        }
    },
    "faq-delete": {
        handler: faqDelete,
        buildArgs(args) {
            return {
                language: args.language,
                id_list: args.id_list,
                confirmation: args.confirmation
            };
        }
    },
    "faq-read": {
        handler: faqRead,
        buildArgs(args) {
            return {
                language: args.language,
                faq_id: args.faq_id,
                faqgroup_id: args.faqgroup_id,
                fields: args.fields,
                current_page: args.pagination?.current_page,
                page_size: args.pagination?.page_size
            };
        }
    },
    "faq-update": {
        handler: faqUpdate,
        buildArgs(args) {
            return {
                language: args.language,
                faq: args.faq,
                confirmation: args.confirmation
            };
        }
    },
    "faqgroup-create": {
        handler: faqGroupCreate,
        buildArgs(args) {
            return {
                language: args.language,
                faqgroup: args.faqgroup,
                confirmation: args.confirmation
            };
        }
    },
    "faqgroup-delete": {
        handler: faqGroupDelete,
        buildArgs(args) {
            return {
                language: args.language,
                id_list: args.id_list,
                confirmation: args.confirmation
            };
        }
    },
    "faqgroup-read": {
        handler: faqGroupRead,
        buildArgs(args) {
            return {
                language: args.language,
                faqgroup_id: args.faqgroup_id,
                fields: args.fields,
                current_page: args.pagination?.current_page,
                page_size: args.pagination?.page_size
            };
        }
    },
    "faqgroup-update": {
        handler: faqGroupUpdate,
        buildArgs(args) {
            return {
                language: args.language,
                faqgroup: args.faqgroup,
                confirmation: args.confirmation
            };
        }
    },
    "inquiry-read": {
        handler: inquiryRead,
        buildArgs(args) {
            return {
                language: args.language,
                recent_days: args.recent_days,
                fields: args.fields,
                current_page: args.pagination?.current_page,
                page_size: args.pagination?.page_size
            };
        }
    },
    "keywords-rank": {
        handler: keywordsRank,
        buildArgs(args) {
            return {
                keywords: args.keywords,
                rank: args.rank,
                current_page: args.pagination?.current_page,
                page_size: args.pagination?.page_size
            };
        }
    },
    "languages-get": {
        handler: languagesGet,
        buildArgs(args) {
            return {};
        }
    },
    "products-create": {
        handler: productsCreate,
        buildArgs(args) {
            return {
                language: args.language,
                products: args.products,
                confirmation: args.confirmation
            };
        }
    },
    "products-delete": {
        handler: productsDelete,
        buildArgs(args) {
            return {
                language: args.language,
                id_list: args.id_list,
                confirmation: args.confirmation
            };
        }
    },
    "products-read": {
        handler: productsRead,
        buildArgs(args) {
            return {
                language: args.language,
                products_id: args.products_id,
                productsgroup_id: args.productsgroup_id,
                fields: args.fields,
                current_page: args.pagination?.current_page,
                page_size: args.pagination?.page_size
            };
        }
    },
    "products-update": {
        handler: productsUpdate,
        buildArgs(args) {
            return {
                language: args.language,
                products: args.products,
                confirmation: args.confirmation
            };
        }
    },
    "productsgroup-create": {
        handler: productsGroupCreate,
        buildArgs(args) {
            return {
                language: args.language,
                productsgroup: args.productsgroup,
                confirmation: args.confirmation
            };
        }
    },
    "productsgroup-delete": {
        handler: productsGroupDelete,
        buildArgs(args) {
            return {
                language: args.language,
                id_list: args.id_list,
                confirmation: args.confirmation
            };
        }
    },
    "productsgroup-read": {
        handler: productsGroupRead,
        buildArgs(args) {
            return {
                language: args.language,
                parent_productsgroup_id: args.parent_productsgroup_id,
                productsgroup_id: args.productsgroup_id,
                fields: args.fields
            };
        }
    },
    "productsgroup-update": {
        handler: productsGroupUpdate,
        buildArgs(args) {
            return {
                language: args.language,
                productsgroup: args.productsgroup,
                confirmation: args.confirmation
            };
        }
    },
    "rule-get": {
        handler: ruleGet,
        buildArgs(args) {
            return {
                language: args.language,
                scene: args.scene
            };
        }
    },
    "visitor-recent": {
        handler: visitorRecent,
        buildArgs(args) {
            return {
                ip: args.ip,
                current_page: args.pagination?.current_page,
                page_size: args.pagination?.page_size
            };
        }
    }
};

function listActions() {
    return Object.keys(ACTIONS).sort().join(", ");
}

function validateMutationConfirmation(action, args) {
    if (!MUTATION_ACTIONS.has(action)) {
        return null;
    }

    const confirmation = args.confirmation;
    if (!confirmation || typeof confirmation !== "object" || Array.isArray(confirmation)) {
        return {
            status: false,
            msg: `Missing required parameter: confirmation. Before using ${action}, require explicit user confirmation that includes the action, language, and target payload or IDs.`
        };
    }

    if (confirmation.approved !== true) {
        return {
            status: false,
            msg: `Explicit user confirmation is required before using ${action}. Set confirmation.approved=true only after showing the user the language and payload or IDs to be changed.`
        };
    }

    if (typeof confirmation.summary !== "string" || !confirmation.summary.trim()) {
        return {
            status: false,
            msg: `Missing required parameter: confirmation.summary. It must summarize the action, language, and target payload or IDs confirmed by the user.`
        };
    }

    return null;
}

function validateActionCategory(action) {
    if (READ_ACTIONS.has(action) || MUTATION_ACTIONS.has(action)) {
        return null;
    }

    return {
        status: false,
        msg: `Unsupported action category: ${action}.`
    };
}

export default async function TradebeeOpenApi(args = {}) {
    if (!isPlainObject(args)) {
        return {
            status: false,
            msg: "Invalid parameter: request.body. It must be a valid JSON object."
        };
    }

    const action = typeof args.action === "string" ? args.action.trim() : "";

    if (!action) {
        return {
            status: false,
            msg: `Missing required parameter: action. Supported actions: ${listActions()}.`
        };
    }

    const definition = ACTIONS[action];
    if (!definition) {
        return {
            status: false,
            msg: `Unsupported action: ${action}. Supported actions: ${listActions()}.`
        };
    }

    const actionCategoryError = validateActionCategory(action);
    if (actionCategoryError) {
        return actionCategoryError;
    }

    const confirmationError = validateMutationConfirmation(action, args);
    if (confirmationError) {
        return confirmationError;
    }

    return await definition.handler(definition.buildArgs(args));
}
