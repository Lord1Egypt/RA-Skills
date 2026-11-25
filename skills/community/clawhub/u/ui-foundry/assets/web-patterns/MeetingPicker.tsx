import { Button, Calendar, DateField, DatePicker, Input, Label } from "@heroui/react";
import { getLocalTimeZone, parseDate, today } from "@internationalized/date";
import { useMemo, useRef, useState } from "react";

import { PlacePicker } from "./PlacePicker";
import type { MeetingDraft, Place, PlaceProvider } from "./types";

type SavedMeeting = MeetingDraft & { id: string };

type MeetingPickerProps = {
	provider: PlaceProvider;
	storageKey?: string;
	/** Called only after local persistence is attempted; callers may sync remotely. */
	onSave?(meeting: SavedMeeting): void | Promise<void>;
};

const emptyDraft: MeetingDraft = { title: "", date: "", place: null };

function validLocalDate(value: string) {
	if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
	try {
		return parseDate(value).toString() === value;
	} catch {
		return false;
	}
}

function isPlace(value: unknown): value is Place {
	if (!value || typeof value !== "object") return false;
	const place = value as Partial<Place>;
	return (
		typeof place.id === "string" &&
		typeof place.label === "string" &&
		typeof place.address === "string" &&
		(place.coordinateSystem === "GCJ-02" ||
			place.coordinateSystem === "WGS84" ||
			place.coordinateSystem === "BD-09" ||
			place.coordinateSystem === null) &&
		(place.source === "amap" || place.source === "manual" || place.source === "fixture")
	);
}

function restore(storageKey: string): SavedMeeting | null {
	try {
		const parsed: unknown = JSON.parse(window.localStorage.getItem(storageKey) ?? "null");
		if (!parsed || typeof parsed !== "object") return null;
		const item = parsed as Partial<SavedMeeting>;
		const date = item.date;
		if (
			typeof item.id !== "string" ||
			typeof item.title !== "string" ||
			typeof date !== "string" ||
			!validLocalDate(date) ||
			(item.place !== null && !isPlace(item.place))
		)
			return null;
		return { id: item.id, title: item.title, date, place: item.place ?? null };
	} catch {
		return null;
	}
}

function dateString(value: { year: number; month: number; day: number } | null) {
	if (!value) return "";
	return `${String(value.year).padStart(4, "0")}-${String(value.month).padStart(2, "0")}-${String(value.day).padStart(2, "0")}`;
}

/**
 * A small product workflow, not a component gallery. It uses a local YYYY-MM-DD
 * value so dates do not shift when a device changes timezone.
 */
export function MeetingPicker({
	provider,
	storageKey = "ui-foundry:meeting-picker",
	onSave,
}: MeetingPickerProps) {
	const [saved, setSaved] = useState<SavedMeeting | null>(() => restore(storageKey));
	const [draft, setDraft] = useState<MeetingDraft>(() => restore(storageKey) ?? emptyDraft);
	const [notice, setNotice] = useState("");
	const [editing, setEditing] = useState(() => restore(storageKey) === null);
	const [saving, setSaving] = useState(false);
	const saveAttempt = useRef(0);
	const saveInFlight = useRef(false);
	const isReady =
		draft.title.trim().length > 0 && validLocalDate(draft.date) && Boolean(draft.place);
	const dateValue = useMemo(
		() => (validLocalDate(draft.date) ? parseDate(draft.date) : null),
		[draft.date],
	);

	function update<K extends keyof MeetingDraft>(key: K, value: MeetingDraft[K]) {
		if (saveInFlight.current) return;
		setDraft((current) => ({ ...current, [key]: value }));
		setNotice("");
	}

	async function save() {
		if (!isReady || saveInFlight.current) return;
		saveInFlight.current = true;
		const attempt = ++saveAttempt.current;
		setSaving(true);
		const next = { ...draft, title: draft.title.trim(), id: saved?.id ?? crypto.randomUUID() };
		let stored = true;
		try {
			window.localStorage.setItem(storageKey, JSON.stringify(next));
		} catch {
			stored = false;
		}
		setSaved(next);
		setDraft(next);
		try {
			await onSave?.(next);
			if (attempt !== saveAttempt.current) return;
			setEditing(false);
			setNotice(stored ? "已保存" : "已保留在当前页面，设备存储不可用");
		} catch {
			if (attempt !== saveAttempt.current) return;
			setNotice(stored ? "已本地保存，远程同步失败" : "已保留在当前页面，远程同步失败");
		} finally {
			if (attempt === saveAttempt.current) {
				saveInFlight.current = false;
				setSaving(false);
			}
		}
	}

	function cancelEdits() {
		if (!saved || saveInFlight.current) return;
		saveAttempt.current += 1;
		setDraft(saved);
		setEditing(false);
		setNotice("已恢复已保存安排");
	}

	const currentDate = today(getLocalTimeZone());
	const tomorrowDate = currentDate.add({ days: 1 });
	const setDate = (value: { toString(): string }) => update("date", value.toString());

	if (saved && !editing) {
		return (
			<section
				aria-labelledby="meeting-picker-title"
				className="uf-meeting-picker uf-meeting-summary"
			>
				<div className="uf-meeting-heading">
					<div>
						<p className="uf-kicker">已安排</p>
						<h1 id="meeting-picker-title">{saved.title}</h1>
					</div>
					<button className="uf-undo" type="button" onClick={() => setEditing(true)}>
						编辑
					</button>
				</div>
				<div className="uf-saved-card" data-testid="saved-meeting">
					<strong>{saved.date}</strong>
					<span>
						{saved.place?.label} · {saved.place?.address}
					</span>
				</div>
				<p aria-live="polite" className="uf-status" data-testid="meeting-status">
					{notice}
				</p>
			</section>
		);
	}

	return (
		<section aria-labelledby="meeting-picker-title" className="uf-meeting-picker">
			<div className="uf-meeting-heading">
				<div>
					<p className="uf-kicker">新安排</p>
					<h1 id="meeting-picker-title">约个时间</h1>
				</div>
				{saved && (
					<button
						aria-label="取消未保存更改"
						className="uf-undo"
						type="button"
						disabled={saving}
						onClick={cancelEdits}
					>
						取消
					</button>
				)}
			</div>

			<fieldset className="uf-meeting-flow" disabled={saving}>
				<div className="uf-title-row">
					<Label htmlFor="meeting-title">事项</Label>
					<Input
						id="meeting-title"
						placeholder="例如：和陈晨喝咖啡"
						value={draft.title}
						onChange={(event) => update("title", event.currentTarget.value)}
					/>
				</div>

				<DatePicker
					aria-label="日期"
					value={dateValue}
					onChange={(value) => update("date", dateString(value))}
				>
					<Label>日期</Label>
					<DateField.Group>
						<DateField.Input>
							{(segment) => <DateField.Segment segment={segment} />}
						</DateField.Input>
						<DateField.Suffix>
							<DatePicker.Trigger aria-label="打开日期选择">
								<DatePicker.TriggerIndicator />
							</DatePicker.Trigger>
						</DateField.Suffix>
					</DateField.Group>
					<DatePicker.Popover>
						<Calendar>
							<Calendar.Header>
								<Calendar.NavButton slot="previous">‹</Calendar.NavButton>
								<Calendar.Heading />
								<Calendar.NavButton slot="next">›</Calendar.NavButton>
							</Calendar.Header>
							<Calendar.Grid>
								<Calendar.GridHeader>
									{(day) => <Calendar.HeaderCell>{day}</Calendar.HeaderCell>}
								</Calendar.GridHeader>
								<Calendar.GridBody>{(date) => <Calendar.Cell date={date} />}</Calendar.GridBody>
							</Calendar.Grid>
						</Calendar>
					</DatePicker.Popover>
				</DatePicker>
				<div aria-label="快速选择日期" className="uf-date-shortcuts">
					<button type="button" onClick={() => setDate(currentDate)}>
						今天
					</button>
					<button type="button" onClick={() => setDate(tomorrowDate)}>
						明天
					</button>
				</div>

				<PlacePicker
					label="见面地点"
					provider={provider}
					value={draft.place}
					onChange={(place: Place | null) => update("place", place)}
				/>
			</fieldset>

			<div className="uf-meeting-actions">
				<Button data-testid="save-meeting" isDisabled={!isReady || saving} onPress={save}>
					{saving ? "保存中" : "保存安排"}
				</Button>
				<p aria-live="polite" className="uf-status" data-testid="meeting-status">
					{notice}
				</p>
			</div>
		</section>
	);
}
