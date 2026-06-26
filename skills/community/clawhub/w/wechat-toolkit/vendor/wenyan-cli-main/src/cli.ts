#!/usr/bin/env node
import path from "node:path";
import { fileURLToPath } from "node:url";
import { Command } from "commander";
import pkg from "../package.json" with { type: "json" };
import {
    addTheme,
    ClientPublishOptions,
    listThemes,
    prepareRenderContext,
    removeTheme,
    renderAndPublish,
    renderAndPublishToServer,
    RenderOptions,
    ThemeOptions,
} from "@wenyan-md/core/wrapper";
import {
    countWechatDrafts,
    deleteWechatDraft,
    deleteWechatPublishedArticle,
    formatDraft,
    formatDraftCount,
    formatDraftList,
    formatPublishStatus,
    formatPublishedArticle,
    formatPublishedList,
    getWechatDraft,
    getWechatPublishStatus,
    getWechatPublishedArticle,
    isTerminalPublishStatus,
    listWechatDrafts,
    listWechatPublishedArticles,
    PublishStatusResponse,
    submitWechatDraftPublish,
} from "./wechat-admin.js";
import {
    countWechatDraftsViaServer,
    deleteWechatDraftViaServer,
    deleteWechatPublishedArticleViaServer,
    getWechatDraftViaServer,
    getWechatPublishStatusViaServer,
    getWechatPublishedArticleViaServer,
    listWechatDraftsViaServer,
    listWechatPublishedArticlesViaServer,
    submitWechatDraftPublishViaServer,
} from "./wechat-admin-client.js";
import { getInputContent } from "./utils.js";

interface RemoteCommandOptions {
    server?: string;
    apiKey?: string;
}

interface JsonCommandOptions {
    json?: boolean;
}

interface DraftGetCommandOptions extends RemoteCommandOptions, JsonCommandOptions {}

interface DraftDeleteCommandOptions extends RemoteCommandOptions, JsonCommandOptions {}

interface DraftCountCommandOptions extends RemoteCommandOptions, JsonCommandOptions {}

interface PaginationCommandOptions extends RemoteCommandOptions, JsonCommandOptions {
    offset: number;
    count: number;
    noContent?: boolean;
}

interface DraftPublishCommandOptions extends RemoteCommandOptions, JsonCommandOptions {
    wait?: boolean;
    timeout: number;
    interval: number;
}

interface PublishStatusCommandOptions extends RemoteCommandOptions, JsonCommandOptions {
    wait?: boolean;
    timeout: number;
    interval: number;
}

interface PublishedGetCommandOptions extends RemoteCommandOptions, JsonCommandOptions {}

interface PublishedDeleteCommandOptions extends RemoteCommandOptions, JsonCommandOptions {
    index: number;
}

export function createProgram(version: string = pkg.version): Command {
    const program = new Command();

    program
        .name("wenyan")
        .description("A CLI for WenYan Markdown Render.")
        .version(version, "-v, --version", "output the current version")
        .action(() => {
            program.outputHelp();
        });

    const addCommonOptions = (cmd: Command) => {
        return cmd
            .argument("[input-content]", "markdown content (string input)")
            .option("-f, --file <path>", "read markdown content from local file or web URL")
            .option("-t, --theme <theme-id>", "ID of the theme to use", "default")
            .option("-h, --highlight <highlight-theme-id>", "ID of the code highlight theme to use", "solarized-light")
            .option("-c, --custom-theme <path>", "path to custom theme CSS file")
            .option("--mac-style", "display codeblock with mac style", true)
            .option("--no-mac-style", "disable mac style")
            .option("--footnote", "convert link to footnote", true)
            .option("--no-footnote", "disable footnote");
    };

    const addRemoteCommandOptions = (cmd: Command) => {
        return cmd
            .option("--server <url>", "Server URL to operate through (e.g. https://api.yourdomain.com)")
            .option("--api-key <apiKey>", "API key for the remote server");
    };

    const addJsonOption = (cmd: Command) => cmd.option("--json", "output raw JSON");

    const addWaitOptions = (cmd: Command) => {
        return cmd
            .option("--wait", "wait until the publish job finishes")
            .option("--timeout <seconds>", "max seconds to wait when --wait is enabled", parsePositiveInteger, 120)
            .option("--interval <seconds>", "polling interval in seconds when --wait is enabled", parsePositiveInteger, 5);
    };

    const addPaginationOptions = (cmd: Command) => {
        return cmd
            .option("--offset <number>", "list offset (>= 0)", parseNonNegativeInteger, 0)
            .option("--count <number>", "page size (1-20)", parseListCount, 20)
            .option("--no-content", "only return summary metadata without article content");
    };

    const pubCmd = program
        .command("publish")
        .description("Render a markdown file to styled HTML and publish to wechat GZH");

    addCommonOptions(pubCmd)
        .option("--server <url>", "Server URL to publish through (e.g. https://api.yourdomain.com)")
        .option("--api-key <apiKey>", "API key for the remote server")
        .action(async (inputContent: string | undefined, options: ClientPublishOptions) => {
            await runCommandWrapper(async () => {
                if (options.server) {
                    options.clientVersion = version;
                    const mediaId = await renderAndPublishToServer(inputContent, options, getInputContent);
                    console.log(`发布成功，Media ID: ${mediaId}`);
                } else {
                    const mediaId = await renderAndPublish(inputContent, options, getInputContent);
                    console.log(`发布成功，Media ID: ${mediaId}`);
                }
            });
        });

    const renderCmd = program.command("render").description("Render a markdown file to styled HTML");

    addCommonOptions(renderCmd).action(async (inputContent: string | undefined, options: RenderOptions) => {
        await runCommandWrapper(async () => {
            const { gzhContent } = await prepareRenderContext(inputContent, options, getInputContent);
            console.log(gzhContent.content);
        });
    });

    program
        .command("theme")
        .description("Manage themes")
        .option("-l, --list", "List all available themes")
        .option("--add", "Add a new custom theme")
        .option("--name <name>", "Name of the new custom theme")
        .option("--path <path>", "Path to the new custom theme CSS file")
        .option("--rm <name>", "Name of the custom theme to remove")
        .action(async (options: ThemeOptions) => {
            await runCommandWrapper(async () => {
                const { list, add, name, path, rm } = options;
                if (list) {
                    const themes = await listThemes();
                    console.log("内置主题：");
                    themes
                        .filter((theme) => theme.isBuiltin)
                        .forEach((theme) => {
                            console.log(`- ${theme.id}: ${theme.description ?? ""}`);
                        });
                    const customThemes = themes.filter((theme) => !theme.isBuiltin);
                    if (customThemes.length > 0) {
                        console.log("\n自定义主题：");
                        customThemes.forEach((theme) => {
                            console.log(`- ${theme.id}: ${theme.description ?? ""}`);
                        });
                    }
                    return;
                }
                if (add) {
                    await addTheme(name, path);
                    console.log(`主题 "${name}" 已添加`);
                    return;
                }
                if (rm) {
                    await removeTheme(rm);
                    console.log(`主题 "${rm}" 已删除`);
                }
            });
        });

    const draftCmd = program.command("draft").description("Manage wechat drafts");

    addJsonOption(addRemoteCommandOptions(draftCmd.command("get").argument("<media-id>", "wechat draft media_id")))
        .description("Get a wechat draft by media_id")
        .action(async (mediaId: string, options: DraftGetCommandOptions) => {
            await runCommandWrapper(async () => {
                const result = await executeDraftGet(mediaId, options, version);
                printResult(options.json, result, formatDraft(result, mediaId));
            });
        });

    addPaginationOptions(addJsonOption(addRemoteCommandOptions(draftCmd.command("list"))))
        .description("List wechat drafts")
        .action(async (options: PaginationCommandOptions) => {
            await runCommandWrapper(async () => {
                const result = await executeDraftList(options, version);
                printResult(options.json, result, formatDraftList(result, options.offset));
            });
        });

    addJsonOption(addRemoteCommandOptions(draftCmd.command("count")))
        .description("Get total draft count")
        .action(async (options: DraftCountCommandOptions) => {
            await runCommandWrapper(async () => {
                const result = await executeDraftCount(options, version);
                printResult(options.json, result, formatDraftCount(result));
            });
        });

    addJsonOption(addRemoteCommandOptions(draftCmd.command("delete").argument("<media-id>", "wechat draft media_id")))
        .description("Delete a wechat draft by media_id")
        .action(async (mediaId: string, options: DraftDeleteCommandOptions) => {
            await runCommandWrapper(async () => {
                const result = await executeDraftDelete(mediaId, options, version);
                if (options.json) {
                    console.log(JSON.stringify(result, null, 2));
                    return;
                }
                console.log(`草稿删除成功，Media ID: ${mediaId}`);
            });
        });

    addWaitOptions(
        addJsonOption(addRemoteCommandOptions(draftCmd.command("publish").argument("<media-id>", "wechat draft media_id"))),
    )
        .description("Submit a wechat draft for formal publication")
        .action(async (mediaId: string, options: DraftPublishCommandOptions) => {
            await runCommandWrapper(async () => {
                const submitResult = await executeDraftPublish(mediaId, options, version);

                if (!options.wait) {
                    if (options.json) {
                        console.log(JSON.stringify(submitResult, null, 2));
                        return;
                    }

                    console.log(`正式发布任务已提交，Publish ID: ${submitResult.publish_id}`);
                    if (submitResult.msg_data_id) {
                        console.log(`消息数据 ID: ${submitResult.msg_data_id}`);
                    }
                    console.log("提示: 正式发布是异步任务，可使用 `wenyan publish-status <publish-id>` 查询结果。");
                    return;
                }

                const finalStatus = await waitForPublishStatus(
                    submitResult.publish_id,
                    (publishId) => executePublishStatus(publishId, options, version),
                    options,
                );

                if (options.json) {
                    console.log(JSON.stringify(finalStatus, null, 2));
                    return;
                }

                if (finalStatus.publish_status !== 0) {
                    throw new Error(`正式发布未成功。\n${formatPublishStatus(finalStatus)}`);
                }

                console.log(`正式发布完成。\n${formatPublishStatus(finalStatus)}`);
            });
        });

    const publishedCmd = program.command("published").description("Manage published wechat articles");

    addPaginationOptions(addJsonOption(addRemoteCommandOptions(publishedCmd.command("list"))))
        .description("List published wechat articles")
        .action(async (options: PaginationCommandOptions) => {
            await runCommandWrapper(async () => {
                const result = await executePublishedList(options, version);
                printResult(options.json, result, formatPublishedList(result, options.offset));
            });
        });

    addJsonOption(addRemoteCommandOptions(publishedCmd.command("get").argument("<article-id>", "wechat article_id")))
        .description("Get a published wechat article by article_id")
        .action(async (articleId: string, options: PublishedGetCommandOptions) => {
            await runCommandWrapper(async () => {
                const result = await executePublishedGet(articleId, options, version);
                printResult(options.json, result, formatPublishedArticle(result, articleId));
            });
        });

    addJsonOption(
        addRemoteCommandOptions(
            publishedCmd
                .command("delete")
                .argument("<article-id>", "wechat article_id")
                .option("--index <number>", "article index to delete; 0 means delete all", parseNonNegativeInteger, 0),
        ),
    )
        .description("Delete a published wechat article by article_id")
        .action(async (articleId: string, options: PublishedDeleteCommandOptions) => {
            await runCommandWrapper(async () => {
                const result = await executePublishedDelete(articleId, options, version);
                if (options.json) {
                    console.log(JSON.stringify(result, null, 2));
                    return;
                }
                if (options.index === 0) {
                    console.log(`已删除文章 ${articleId} 的全部已发布内容`);
                    return;
                }
                console.log(`已删除文章 ${articleId} 的第 ${options.index} 篇`);
            });
        });

    addWaitOptions(
        addJsonOption(
            addRemoteCommandOptions(program.command("publish-status").argument("<publish-id>", "wechat publish task id")),
        ),
    )
        .description("Query the status of a formal publish task")
        .action(async (publishId: string, options: PublishStatusCommandOptions) => {
            await runCommandWrapper(async () => {
                const status = options.wait
                    ? await waitForPublishStatus(
                          publishId,
                          (jobId) => executePublishStatus(jobId, options, version),
                          options,
                      )
                    : await executePublishStatus(publishId, options, version);

                if (options.json) {
                    console.log(JSON.stringify(status, null, 2));
                    return;
                }

                if (options.wait && status.publish_status !== 0) {
                    throw new Error(`正式发布未成功。\n${formatPublishStatus(status)}`);
                }

                console.log(formatPublishStatus(status));
            });
        });

    program
        .command("serve")
        .description("Start a server to provide HTTP API for rendering and publishing")
        .option("-p, --port <port>", "Port to listen on (default: 3000)", "3000")
        .option("--api-key <apiKey>", "API key for authentication")
        .action(async (options: { port?: string; apiKey?: string }) => {
            try {
                const { serveCommand } = await import("./commands/serve.js");
                const port = options.port ? parseInt(options.port, 10) : 3000;
                await serveCommand({ port, version, apiKey: options.apiKey });
            } catch (error: any) {
                console.error(error.message);
                process.exit(1);
            }
        });

    return program;
}

async function executeDraftGet(mediaId: string, options: DraftGetCommandOptions, version: string) {
    if (options.server) {
        return await getWechatDraftViaServer(mediaId, buildRemoteWechatOptions(options, version));
    }

    return await getWechatDraft(mediaId);
}

async function executeDraftList(options: PaginationCommandOptions, version: string) {
    const noContent = resolveNoContentOption(options);

    if (options.server) {
        return await listWechatDraftsViaServer({
            ...buildRemoteWechatOptions(options, version),
            offset: options.offset,
            count: options.count,
            noContent,
        });
    }

    return await listWechatDrafts({
        offset: options.offset,
        count: options.count,
        noContent,
    });
}

async function executeDraftCount(options: DraftCountCommandOptions, version: string) {
    if (options.server) {
        return await countWechatDraftsViaServer(buildRemoteWechatOptions(options, version));
    }

    return await countWechatDrafts();
}

async function executeDraftDelete(mediaId: string, options: DraftDeleteCommandOptions, version: string) {
    if (options.server) {
        return await deleteWechatDraftViaServer(mediaId, buildRemoteWechatOptions(options, version));
    }

    return await deleteWechatDraft(mediaId);
}

async function executeDraftPublish(mediaId: string, options: DraftPublishCommandOptions, version: string) {
    if (options.server) {
        return await submitWechatDraftPublishViaServer(mediaId, buildRemoteWechatOptions(options, version));
    }

    return await submitWechatDraftPublish(mediaId);
}

async function executePublishedList(options: PaginationCommandOptions, version: string) {
    const noContent = resolveNoContentOption(options);

    if (options.server) {
        return await listWechatPublishedArticlesViaServer({
            ...buildRemoteWechatOptions(options, version),
            offset: options.offset,
            count: options.count,
            noContent,
        });
    }

    return await listWechatPublishedArticles({
        offset: options.offset,
        count: options.count,
        noContent,
    });
}

async function executePublishedGet(articleId: string, options: PublishedGetCommandOptions, version: string) {
    if (options.server) {
        return await getWechatPublishedArticleViaServer(articleId, buildRemoteWechatOptions(options, version));
    }

    return await getWechatPublishedArticle(articleId);
}

async function executePublishedDelete(articleId: string, options: PublishedDeleteCommandOptions, version: string) {
    if (options.server) {
        return await deleteWechatPublishedArticleViaServer(articleId, options.index, buildRemoteWechatOptions(options, version));
    }

    return await deleteWechatPublishedArticle(articleId, options.index);
}

async function executePublishStatus(publishId: string, options: PublishStatusCommandOptions, version: string) {
    if (options.server) {
        return await getWechatPublishStatusViaServer(publishId, buildRemoteWechatOptions(options, version));
    }

    return await getWechatPublishStatus(publishId);
}

function buildRemoteWechatOptions(options: RemoteCommandOptions, version: string) {
    return {
        server: options.server,
        apiKey: options.apiKey,
        clientVersion: version,
    };
}

async function waitForPublishStatus(
    publishId: string,
    getStatus: (publishId: string) => Promise<PublishStatusResponse>,
    options: { timeout: number; interval: number },
) {
    const timeoutMs = options.timeout * 1000;
    const intervalMs = options.interval * 1000;
    const startedAt = Date.now();

    while (true) {
        const status = await getStatus(publishId);
        if (isTerminalPublishStatus(status.publish_status)) {
            return status;
        }

        if (Date.now() - startedAt >= timeoutMs) {
            throw new Error(`等待正式发布结果超时（${options.timeout} 秒），请稍后再次执行 publish-status 查询`);
        }

        await new Promise((resolve) => setTimeout(resolve, intervalMs));
    }
}

function resolveNoContentOption(options: PaginationCommandOptions & { content?: boolean }) {
    if (typeof options.noContent === "boolean") {
        return options.noContent;
    }

    if (options.content === false) {
        return true;
    }

    return undefined;
}

function printResult(json: boolean | undefined, data: unknown, formattedText: string) {
    if (json) {
        console.log(JSON.stringify(data, null, 2));
        return;
    }

    console.log(formattedText);
}

function parsePositiveInteger(value: string) {
    const parsed = Number.parseInt(value, 10);
    if (!Number.isInteger(parsed) || parsed <= 0) {
        throw new Error(`Expected a positive integer, received "${value}"`);
    }
    return parsed;
}

function parseNonNegativeInteger(value: string) {
    const parsed = Number.parseInt(value, 10);
    if (!Number.isInteger(parsed) || parsed < 0) {
        throw new Error(`Expected a non-negative integer, received "${value}"`);
    }
    return parsed;
}

function parseListCount(value: string) {
    const parsed = parsePositiveInteger(value);
    if (parsed > 20) {
        throw new Error(`Expected an integer between 1 and 20, received "${value}"`);
    }
    return parsed;
}

async function runCommandWrapper(action: () => Promise<void>) {
    try {
        await action();
    } catch (error) {
        if (error instanceof Error) {
            console.error(error.message);
        } else {
            console.error("An unexpected error occurred:", error);
        }
        process.exit(1);
    }
}

function isDirectInvocation() {
    const currentFile = fileURLToPath(import.meta.url);
    const entryFile = process.argv[1] ? path.resolve(process.argv[1]) : "";
    return entryFile === currentFile;
}

if (isDirectInvocation()) {
    const program = createProgram();
    program.parse(process.argv);
}
