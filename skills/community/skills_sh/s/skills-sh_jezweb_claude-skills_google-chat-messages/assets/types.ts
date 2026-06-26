// Google Chat cardsV2 TypeScript types for webhook messages
// Reference: https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces.messages

export interface WebhookMessage {
  text?: string;
  cardsV2?: CardWithId[];
  thread?: Thread;
}

export interface Thread {
  threadKey?: string;
}

export interface CardWithId {
  cardId: string;
  card: Card;
}

export interface Card {
  header?: CardHeader;
  sections: CardSection[];
}

export interface CardHeader {
  title: string;
  subtitle?: string;
  imageUrl?: string;
  imageType?: 'SQUARE' | 'CIRCLE';
}

export interface CardSection {
  header?: string;
  widgets: Widget[];
  collapsible?: boolean;
  uncollapsibleWidgetsCount?: number;
}

export interface Widget {
  textParagraph?: { text: string };
  image?: { imageUrl: string; altText?: string };
  decoratedText?: DecoratedText;
  buttonList?: { buttons: Button[] };
  divider?: Record<string, never>;
}

export interface DecoratedText {
  topLabel?: string;
  text: string;
  bottomLabel?: string;
  startIcon?: Icon;
  endIcon?: Icon;
  wrapText?: boolean;
  onClick?: OnClick;
  button?: Button;
}

export interface Icon {
  knownIcon?: string;
  iconUrl?: string;
  altText?: string;
}

export interface Button {
  text: string;
  icon?: Icon;
  color?: { red?: number; green?: number; blue?: number; alpha?: number };
  onClick: OnClick;
  disabled?: boolean;
  altText?: string;
}

export interface OnClick {
  openLink?: { url: string };
  action?: {
    function?: string;
    parameters?: { key: string; value: string }[];
  };
}
