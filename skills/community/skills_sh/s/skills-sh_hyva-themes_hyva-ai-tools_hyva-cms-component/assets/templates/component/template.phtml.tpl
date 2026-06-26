<?php
declare(strict_types=1);

use Hyva\CmsLiveviewEditor\Block\Element;
use Hyva\Theme\Model\ViewModelRegistry;
use Magento\Framework\Escaper;

/** @var Element $block */
/** @var Escaper $escaper */
/** @var ViewModelRegistry $viewModels */

// Content fields
{{CONTENT_FIELDS}}

// Design fields
$textAlign = $block->getData('text_align') ?: 'text-left';
$textColor = $block->getData('text_color') ?: '';
$backgroundColor = $block->getData('background_color') ?: 'transparent';

// Advanced fields
$classes = $block->getData('classes') ?: '';
$blockId = $block->getData('block_id') ?: '';
?>
<div <?= /** @noEscape */ $block->getEditorAttrs() ?>
     <?php if ($blockId): ?>id="<?= $escaper->escapeHtmlAttr($blockId) ?>"<?php endif; ?>
     class="<?= $escaper->escapeHtmlAttr($textAlign) ?> <?= $escaper->escapeHtmlAttr($classes) ?>"
     style="background-color: <?= $escaper->escapeHtmlAttr($backgroundColor) ?>; <?php if ($textColor): ?>color: <?= $escaper->escapeHtmlAttr($textColor) ?>;<?php endif; ?>">

{{TEMPLATE_BODY}}

</div>
