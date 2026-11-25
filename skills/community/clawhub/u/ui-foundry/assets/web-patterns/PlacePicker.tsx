import { ComboBox, Input, ListBox } from "@heroui/react";
import { useEffect, useId, useState } from "react";

import { usePlaceSearch } from "./usePlaceSearch";
import type { Place, PlaceProvider } from "./types";

type PlacePickerProps = {
	provider: PlaceProvider;
	value: Place | null;
	onChange(place: Place | null): void;
	label?: string;
};

/** HeroUI ComboBox handles focus, arrows, Enter and active-descendant semantics. */
export function PlacePicker({ provider, value, onChange, label = "地点" }: PlacePickerProps) {
	const inputId = useId();
	const [query, setQuery] = useState(value?.label ?? "");
	const [searchQuery, setSearchQuery] = useState("");
	const [composing, setComposing] = useState(false);
	const [manualOpen, setManualOpen] = useState(false);
	const [manualValue, setManualValue] = useState("");
	const search = usePlaceSearch(searchQuery, provider);

	useEffect(() => {
		if (value) {
			setQuery(value.label);
			setSearchQuery("");
		}
	}, [value]);

	function choose(place: Place) {
		// Commit key and label in one render. A later input-value update would
		// be interpreted by the combobox as typing and reopen its popup.
		setQuery(place.label);
		setSearchQuery("");
		onChange(place);
		setManualOpen(false);
	}

	function commitManual() {
		const label = manualValue.trim();
		if (!label) return;
		choose({
			id: `manual:${label.toLocaleLowerCase()}`,
			label,
			address: "手动填写",
			coordinateSystem: null,
			source: "manual",
		});
	}

	return (
		<div className="uf-place-picker">
			<p className="uf-field-label" id={`${inputId}-label`}>
				{label}
			</p>
			<ComboBox
				aria-labelledby={`${inputId}-label`}
				inputValue={query}
				items={value && !searchQuery.trim() ? [value] : search.results}
				allowsEmptyCollection
				menuTrigger="focus"
				selectedKey={value?.id ?? null}
				onInputChange={(next) => {
					setQuery(next);
					if (!composing) setSearchQuery(next);
					if (value && next !== value.label) onChange(null);
				}}
				onSelectionChange={(key) => {
					const place = search.results.find((item) => item.id === key);
					if (place) choose(place);
				}}
			>
				<ComboBox.InputGroup className="uf-combobox-input">
					<Input
						id={inputId}
						placeholder="搜索地点"
						onCompositionEnd={(event) => {
							setComposing(false);
							setSearchQuery(event.currentTarget.value);
						}}
						onCompositionStart={() => {
							setComposing(true);
							setSearchQuery("");
						}}
					/>
					<ComboBox.Trigger aria-label="显示地点建议" />
				</ComboBox.InputGroup>
				<ComboBox.Popover className="uf-combobox-popover">
					{search.status === "idle" && <p className="uf-result-note">输入名称或地址</p>}
					{search.status === "loading" && (
						<p aria-live="polite" className="uf-result-note">
							正在查找
						</p>
					)}
					{search.status === "error" && (
						<div className="uf-result-note" role="status">
							服务暂不可用{" "}
							<button type="button" onClick={search.retry}>
								重试
							</button>
						</div>
					)}
					{search.status === "empty" && <p className="uf-result-note">没有匹配地点</p>}
					<ListBox aria-label="地点结果">
						{(place: Place) => (
							<ListBox.Item id={place.id} textValue={place.label}>
								<span>{place.label}</span>
								<small>{place.address}</small>
							</ListBox.Item>
						)}
					</ListBox>
					<button
						className="uf-manual-link"
						type="button"
						onClick={() => {
							if (!manualOpen) setManualValue(query);
							setManualOpen((current) => !current);
						}}
					>
						手动填写
					</button>
					{manualOpen && (
						<div className="uf-manual-row">
							<input
								aria-label="手动地点"
								autoFocus
								value={manualValue}
								onChange={(event) => setManualValue(event.target.value)}
								onKeyDown={(event) => {
									if (
										event.key === "Enter" &&
										!event.nativeEvent.isComposing &&
										event.keyCode !== 229
									)
										commitManual();
								}}
							/>
							<button type="button" disabled={!manualValue.trim()} onClick={commitManual}>
								使用
							</button>
						</div>
					)}
				</ComboBox.Popover>
			</ComboBox>
			{value && (
				<p className="uf-selected-place" data-testid="selected-place">
					<span>{value.label}</span>
					{value.source === "manual" ? "手动地点" : value.address}
				</p>
			)}
		</div>
	);
}
