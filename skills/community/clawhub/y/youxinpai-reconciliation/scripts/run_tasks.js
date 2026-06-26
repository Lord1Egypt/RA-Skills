const YOUXINPAI_TASKS = [
  "raw_auction_guafundaccountdetail_all_d",
  "raw_auction_auctionguafundbill_all_h",
  "raw_auction_guarantee_withdraw_apply_all_d",
  "ods_auction_refund_order_all_d",
  "raw_auction_payment_order2_all_d",
];

const YOUXINPAI_SELECTORS = {
  searchInput: 'input[placeholder="搜索任务名"]',
  switchInner: "span.ant-switch-inner",
  switch: '[role="switch"], button.ant-switch, .ant-switch',
  runIcon: "span.iconzanting2.iconfont",
  operationCell: "td:last-child",
  operationIcons:
    'td:last-child .iconfont, td:last-child [class*="icon"], td:last-child button, td:last-child a',
  confirmButton: "button.ant-btn.ant-btn-primary",
  tableRows: "table tbody tr, .ant-table-tbody > tr",
};

const YOUXINPAI_DELAYS = {
  searchUpdateMs: 500,
  dialogAppearMs: 2000,
  dialogDisappearMs: 2000,
  betweenClicksMs: 120,
  operationRevealMs: 150,
};

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function normalizeText(value) {
  return (value || "").replace(/\s+/g, " ").trim();
}

function normalizeMatchText(value) {
  return normalizeText(value).toLowerCase();
}

function isVisible(element) {
  if (!(element instanceof HTMLElement)) {
    return false;
  }

  const style = window.getComputedStyle(element);
  if (style.display === "none" || style.visibility === "hidden") {
    return false;
  }

  const rect = element.getBoundingClientRect();
  return rect.width > 0 && rect.height > 0;
}

function getInputValue(input) {
  return typeof input.value === "string" ? input.value : "";
}

function dispatchInputEvents(input) {
  input.dispatchEvent(new Event("input", { bubbles: true }));
  input.dispatchEvent(new Event("change", { bubbles: true }));
}

function setNativeValue(input, value) {
  const prototype = Object.getPrototypeOf(input);
  const descriptor =
    Object.getOwnPropertyDescriptor(prototype, "value") ||
    Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value");
  const previousValue = getInputValue(input);

  descriptor?.set?.call(input, value);
  if (input._valueTracker) {
    input._valueTracker.setValue(previousValue);
  }
  dispatchInputEvents(input);
}

function dispatchKeyboardEvent(input, type, key) {
  input.dispatchEvent(
    new KeyboardEvent(type, {
      key,
      code: key,
      keyCode: key === "Enter" ? 13 : undefined,
      which: key === "Enter" ? 13 : undefined,
      bubbles: true,
    })
  );
}

function triggerSearch(input, value) {
  input.focus();
  setNativeValue(input, "");
  setNativeValue(input, value);
  dispatchKeyboardEvent(input, "keydown", "Enter");
  dispatchKeyboardEvent(input, "keyup", "Enter");
}

function getSearchInputCandidates() {
  const nodes = Array.from(
    document.querySelectorAll('input, input[type="text"], input[type="search"]')
  );

  return nodes.filter((node) => {
    if (!(node instanceof HTMLInputElement)) {
      return false;
    }
    if (node.disabled || node.readOnly) {
      return false;
    }
    return isVisible(node);
  });
}

function scoreSearchInput(input) {
  const placeholder = normalizeText(input.getAttribute("placeholder"));
  const ariaLabel = normalizeText(input.getAttribute("aria-label"));
  const name = normalizeText(input.getAttribute("name"));
  const className = normalizeText(input.className);
  const wrapperText = normalizeText(input.closest("form, div, span")?.textContent);

  let score = 0;

  if (placeholder === "搜索任务名") {
    score += 100;
  } else if (placeholder.includes("搜索任务名")) {
    score += 80;
  } else if (placeholder.includes("搜索")) {
    score += 40;
  }

  if (ariaLabel.includes("搜索任务名")) {
    score += 50;
  }

  if (name.includes("search")) {
    score += 20;
  }

  if (className.includes("ant-input")) {
    score += 10;
  }

  if (wrapperText.includes("搜索任务名")) {
    score += 10;
  }

  return score;
}

function findSearchInput() {
  const exactMatch = document.querySelector(YOUXINPAI_SELECTORS.searchInput);
  if (exactMatch instanceof HTMLInputElement && !exactMatch.disabled && isVisible(exactMatch)) {
    return exactMatch;
  }

  const candidates = getSearchInputCandidates()
    .map((input) => ({ input, score: scoreSearchInput(input) }))
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score);

  return candidates[0]?.input || null;
}

function rowContainsTaskName(row, taskName) {
  return normalizeMatchText(row.textContent).includes(normalizeMatchText(taskName));
}

function getVisibleTableRows() {
  const rows = [];
  const seen = new Set();

  for (const row of document.querySelectorAll(YOUXINPAI_SELECTORS.tableRows)) {
    if (!(row instanceof HTMLTableRowElement)) {
      continue;
    }
    if (!isVisible(row)) {
      continue;
    }
    if (!row.querySelector("td")) {
      continue;
    }
    if (seen.has(row)) {
      continue;
    }
    seen.add(row);
    rows.push(row);
  }

  return rows;
}

function getRowSwitch(row) {
  return row.querySelector(YOUXINPAI_SELECTORS.switch);
}

function isSwitchChecked(switchNode) {
  if (!(switchNode instanceof HTMLElement)) {
    return false;
  }

  const ariaChecked = switchNode.getAttribute("aria-checked");
  if (ariaChecked === "true") {
    return true;
  }
  if (ariaChecked === "false") {
    return false;
  }

  if (switchNode.classList.contains("ant-switch-checked")) {
    return true;
  }

  return normalizeText(switchNode.textContent).includes("开启");
}

function rowIsEnabled(row) {
  return isSwitchChecked(getRowSwitch(row));
}

function extractRowId(row) {
  for (const cell of row.querySelectorAll("td")) {
    const text = normalizeText(cell.textContent);
    if (/^\d{4,}$/.test(text)) {
      return text;
    }
  }

  const fallbackMatch = normalizeText(row.textContent).match(/\b\d{4,}\b/);
  return fallbackMatch ? fallbackMatch[0] : "";
}

function extractTaskName(row, taskName) {
  const exactText = normalizeMatchText(taskName);
  const textNodes = Array.from(row.querySelectorAll("a, span, div"))
    .map((node) => normalizeText(node.textContent))
    .filter(Boolean);

  const directMatch = textNodes.find((text) => normalizeMatchText(text).includes(exactText));
  if (directMatch) {
    return directMatch;
  }

  const underscoreCandidate = textNodes
    .filter((text) => text.includes("_"))
    .sort((a, b) => b.length - a.length)[0];

  if (underscoreCandidate) {
    return underscoreCandidate;
  }

  return normalizeText(row.textContent);
}

function extractRowInfo(row, taskName) {
  const switchNode = getRowSwitch(row);
  return {
    row,
    id: extractRowId(row),
    taskName: extractTaskName(row, taskName),
    enabled: isSwitchChecked(switchNode),
    switchText: normalizeText(switchNode?.textContent),
  };
}

function getOperationCell(row) {
  return row.querySelector(YOUXINPAI_SELECTORS.operationCell) || row.lastElementChild;
}

function isElementDisabled(element) {
  if (!(element instanceof HTMLElement)) {
    return true;
  }

  if (element.hasAttribute("disabled") || element.getAttribute("aria-disabled") === "true") {
    return true;
  }

  const className = element.className || "";
  return typeof className === "string" && className.includes("disabled");
}

function getOperationCandidates(row) {
  return Array.from(row.querySelectorAll(YOUXINPAI_SELECTORS.operationIcons)).filter(
    (node) => node instanceof HTMLElement && isVisible(node) && !isElementDisabled(node)
  );
}

function scoreRunCandidate(node) {
  const text = normalizeMatchText(node.textContent);
  const className = normalizeMatchText(node.className);
  const title = normalizeMatchText(node.getAttribute("title"));
  const ariaLabel = normalizeMatchText(node.getAttribute("aria-label"));

  let score = 0;

  if (className.includes("iconzanting2")) {
    score += 100;
  }
  if (text.includes("运行") || title.includes("运行") || ariaLabel.includes("运行")) {
    score += 60;
  }
  if (title.includes("暂停") || ariaLabel.includes("暂停")) {
    score -= 100;
  }
  if (className.includes("delete") || text.includes("删除")) {
    score -= 100;
  }

  return score;
}

function getRunIcon(row) {
  const directMatch = row.querySelector(YOUXINPAI_SELECTORS.runIcon);
  if (directMatch instanceof HTMLElement && isVisible(directMatch) && !isElementDisabled(directMatch)) {
    return directMatch;
  }

  const candidates = getOperationCandidates(row)
    .map((node) => ({ node, score: scoreRunCandidate(node) }))
    .sort((a, b) => b.score - a.score);

  if (candidates[0] && candidates[0].score > 0) {
    return candidates[0].node;
  }

  return getOperationCandidates(row)[0] || null;
}

function scrollElementIntoCenter(element) {
  if (!(element instanceof HTMLElement)) {
    return;
  }

  element.scrollIntoView({
    block: "center",
    inline: "center",
    behavior: "instant",
  });
}

function revealOperationArea(row) {
  scrollElementIntoCenter(row);
  const operationCell = getOperationCell(row);
  scrollElementIntoCenter(operationCell);

  let current = row.parentElement;
  while (current && current !== document.body) {
    if (current.scrollWidth > current.clientWidth + 20) {
      current.scrollLeft = current.scrollWidth;
    }
    current = current.parentElement;
  }
}

function getConfirmButton() {
  return Array.from(document.querySelectorAll(YOUXINPAI_SELECTORS.confirmButton)).find(
    (button) => normalizeText(button.textContent).includes("确定")
  );
}

async function waitFor(condition, timeoutMs, intervalMs = 100) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    const value = condition();
    if (value) {
      return value;
    }
    await sleep(intervalMs);
  }
  return null;
}

function getCandidateRows(taskName) {
  return getVisibleTableRows()
    .filter((row) => rowContainsTaskName(row, taskName))
    .map((row) => extractRowInfo(row, taskName));
}

async function searchTask(taskName) {
  const input = await waitFor(() => findSearchInput(), 3000);
  if (!input) {
    throw new Error("未找到“搜索任务名”输入框");
  }

  triggerSearch(input, taskName);

  await sleep(YOUXINPAI_DELAYS.searchUpdateMs);
  return getCandidateRows(taskName);
}

async function clickRunAndConfirm(row) {
  revealOperationArea(row);
  await sleep(YOUXINPAI_DELAYS.operationRevealMs);

  const runIcon = getRunIcon(row);
  if (!runIcon) {
    return { success: false, reason: "未找到运行按钮" };
  }

  runIcon.click();

  const confirmButton = await waitFor(
    () => getConfirmButton(),
    YOUXINPAI_DELAYS.dialogAppearMs
  );

  if (!confirmButton) {
    return { success: false, reason: "未出现确认弹窗" };
  }

  confirmButton.click();

  const dialogClosed = await waitFor(
    () => !getConfirmButton(),
    YOUXINPAI_DELAYS.dialogDisappearMs
  );

  if (!dialogClosed) {
    return { success: false, reason: "点击确定后弹窗未关闭" };
  }

  await sleep(YOUXINPAI_DELAYS.betweenClicksMs);
  return { success: true };
}

async function processTask(taskName) {
  const result = {
    taskName,
    found: false,
    triggered: 0,
    attempted: 0,
    failed: 0,
    success: false,
    reason: "",
    matchedRows: [],
    enabledTasks: [],
    executionDetails: [],
  };

  const rowInfos = await searchTask(taskName);
  result.matchedRows = rowInfos.map((item) => ({
    id: item.id,
    taskName: item.taskName,
    enabled: item.enabled,
    switchText: item.switchText,
  }));
  result.enabledTasks = rowInfos
    .filter((item) => item.enabled)
    .map((item) => ({
      id: item.id,
      taskName: item.taskName,
    }));

  if (!rowInfos.length) {
    result.reason = "未找到任务";
    return result;
  }

  result.found = true;

  for (const rowInfo of rowInfos) {
    if (!rowInfo.enabled) {
      continue;
    }

    result.attempted += 1;
    const clickResult = await clickRunAndConfirm(rowInfo.row);
    result.executionDetails.push({
      id: rowInfo.id,
      taskName: rowInfo.taskName,
      success: clickResult.success,
      reason: clickResult.reason || "",
    });
    if (!clickResult.success) {
      result.failed += 1;
      result.reason = clickResult.reason;
      continue;
    }
    result.triggered += 1;
  }

  result.success = result.found && result.failed === 0;
  if (!result.attempted) {
    result.reason = "已找到任务，但没有可运行实例";
  } else if (result.failed > 0 && !result.reason) {
    result.reason = "部分任务执行失败";
  }
  return result;
}

async function runYouxinpaiTasks(taskNames = YOUXINPAI_TASKS) {
  const summary = [];
  for (const taskName of taskNames) {
    const taskResult = await processTask(taskName);
    summary.push(taskResult);
  }
  return summary;
}

async function inspectYouxinpaiTasks(taskNames = YOUXINPAI_TASKS) {
  const summary = [];
  for (const taskName of taskNames) {
    const rowInfos = await searchTask(taskName);
    summary.push({
      taskName,
      matchedRows: rowInfos.map((item) => ({
        id: item.id,
        taskName: item.taskName,
        enabled: item.enabled,
        switchText: item.switchText,
      })),
      enabledTasks: rowInfos
        .filter((item) => item.enabled)
        .map((item) => ({
          id: item.id,
          taskName: item.taskName,
        })),
    });
  }
  return summary;
}

window.runYouxinpaiTasks = runYouxinpaiTasks;
window.inspectYouxinpaiTasks = inspectYouxinpaiTasks;

