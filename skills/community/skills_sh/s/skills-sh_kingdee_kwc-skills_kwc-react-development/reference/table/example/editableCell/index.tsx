/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { useEffect, useState, useMemo, useRef } from 'react';
import { generateCustomSlot } from '@kdcloudjs/shoelace/dist/components/table/utils.js';
import SlTable from '@kdcloudjs/shoelace/dist/react/table/index.js';
import SlTextarea from '@kdcloudjs/shoelace/dist/react/textarea/index.js';
import SlInput from '@kdcloudjs/shoelace/dist/react/input/index.js';
import SlSelect from '@kdcloudjs/shoelace/dist/react/select/index.js';
import SlOption from '@kdcloudjs/shoelace/dist/react/option/index.js';
import SlRadioGroup from '@kdcloudjs/shoelace/dist/react/radio-group/index.js';
import SlRadio from '@kdcloudjs/shoelace/dist/react/radio/index.js';
import SlCheckbox from '@kdcloudjs/shoelace/dist/react/checkbox/index.js';
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';
import SlSwitch from '@kdcloudjs/shoelace/dist/react/switch/index.js';
import SlColorPicker from '@kdcloudjs/shoelace/dist/react/color-picker/index.js';
import SlAvatar from '@kdcloudjs/shoelace/dist/react/avatar/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';
import SlProgressBar from '@kdcloudjs/shoelace/dist/react/progress-bar/index.js';
import './index.less';

const editableDataSource = [
    {
        id: '1',
        name: 'Jane Doe',
        salary: '18000',
        address: '32 Park Road, London',
        gender: 'female',
        skills: ['react'],
        birthday: '1995-03-15',
        active: true,
        color: '#3b82f6',
        avatar: '',
        action: '',
        progress: '75'
    },
    {
        id: '2',
        name: 'Alisa Ross',
        salary: '24000',
        address: '35 Park Road, London',
        gender: 'male',
        skills: ['vue', 'react'],
        birthday: '1992-07-22',
        active: false,
        color: '#ef4444',
        avatar: '',
        action: '',
        progress: '40'
    },
    {
        id: '3',
        name: 'Kevin Sandra',
        salary: '20000',
        address: '31 Park Road, London',
        gender: 'female',
        skills: ['angular'],
        birthday: '1998-11-08',
        active: true,
        color: '#10b981',
        avatar: '',
        action: '',
        progress: '90'
    }
];

const editHeaderCell = () => ({ style: 'padding: 0 18px' });

const editableColumns = [
    { title: '头像', dataIndex: 'avatar', width: 80, slot: true },
    { title: '姓名', dataIndex: 'name', width: 160, slot: true, slHeaderCell: editHeaderCell },
    { title: '薪资', dataIndex: 'salary', width: 160, slot: true, slHeaderCell: editHeaderCell },
    { title: '地址', dataIndex: 'address', width: 240, slot: true, slHeaderCell: editHeaderCell },
    { title: '性别', dataIndex: 'gender', width: 220, slot: true },
    { title: '技能', dataIndex: 'skills', width: 300, slot: true },
    { title: '生日', dataIndex: 'birthday', width: 240, slot: true, slHeaderCell: editHeaderCell },
    { title: '状态', dataIndex: 'active', width: 80, slot: true },
    { title: '颜色', dataIndex: 'color', width: 80, slot: true },
    { title: '进度', dataIndex: 'progress', width: 300, slot: true },
    { title: '操作', dataIndex: 'action', width: 120, slot: true, fixed: 'right' }
];

const GENDER_OPTIONS = [
    { label: '男', value: 'male' },
    { label: '女', value: 'female' },
    { label: '其他', value: 'other' }
];

const SKILL_OPTIONS = [
    { label: 'React', value: 'react' },
    { label: 'Vue', value: 'vue' },
    { label: 'Angular', value: 'angular' }
];

const EditCell = (props: any) => {
    const ref = useRef<any>(null);
    const { slotName, cellInfo, colKey, editing, handleCellValueChange } = props;

    useEffect(() => {
        if (!ref.current) {return;}
        const ele = ref.current as any;
        if (ele.focus) {setTimeout(() => ele.focus());}
        if (ele.show) {setTimeout(() => ele.show());}
    }, [editing]);

    const renderEditCell = () => {
        switch (colKey) {
            case 'name':
                return <SlInput ref={ref} value={cellInfo} onSlChange={(e: any) => handleCellValueChange(e.target.value)} />;
            case 'salary':
                return (
                    <SlSelect hoist defaultValue={cellInfo} onSlChange={(e: any) => handleCellValueChange(e.target.value)} ref={ref}>
                        <SlOption value="12000">12000</SlOption>
                        <SlOption value="15000">15000</SlOption>
                        <SlOption value="18000">18000</SlOption>
                        <SlOption value="20000">20000</SlOption>
                        <SlOption value="24000">24000</SlOption>
                    </SlSelect>
                );
            case 'address':
                return <SlTextarea value={cellInfo} onSlChange={(e: any) => handleCellValueChange(e.target.value)} ref={ref} />;
            case 'birthday':
                return <SlDatepicker hoist ref={ref} style={{ width: '100%' }} value={cellInfo} onSlChange={(e: any) => handleCellValueChange(e.target.value)} />;
            default:
                return <SlInput ref={ref} value={cellInfo} onSlChange={(e: any) => handleCellValueChange(e.target.value)} />;
        }
    };

    const renderLockCell = () => {
        switch (colKey) {
            case 'salary':
                return (
                    <div className="table-editClass">
                        <div className="select-cell">
                            <div>{cellInfo}</div>
                            <sl-icon library="system" name="chevron-down" className="icon"></sl-icon>
                        </div>
                    </div>
                );
            default:
                return <div className="table-editClass"><div>{cellInfo}</div></div>;
        }
    };

    // 始终可交互的控件（不需要编辑态切换）
    const alwaysInteractive = ['gender', 'skills', 'active', 'color', 'avatar', 'action', 'progress'];
    if (alwaysInteractive.includes(colKey)) {
        switch (colKey) {
            case 'gender':
                return (
                    <div slot={slotName} className="table-custom-cell">
                        <SlRadioGroup className="cell-radio-group" value={cellInfo} onSlChange={(e: any) => handleCellValueChange(e.target.value)}>
                            {GENDER_OPTIONS.map((opt) => (
                                <SlRadio key={opt.value} value={opt.value}>{opt.label}</SlRadio>
                            ))}
                        </SlRadioGroup>
                    </div>
                );
            case 'skills': {
                const current: string[] = Array.isArray(cellInfo) ? cellInfo : [];
                return (
                    <div slot={slotName} className="table-custom-cell">
                        <div className="checkbox-group">
                            {SKILL_OPTIONS.map((opt) => (
                                <SlCheckbox
                                    key={opt.value}
                                    checked={current.includes(opt.value)}
                                    onSlChange={(e: any) => {
                                        const {checked} = e.target;
                                        const next = checked ? [...current, opt.value] : current.filter((v: string) => v !== opt.value);
                                        handleCellValueChange(next);
                                    }}
                                >
                                    {opt.label}
                                </SlCheckbox>
                            ))}
                        </div>
                    </div>
                );
            }
            case 'active':
                return (
                    <div slot={slotName} className="table-custom-cell">
                        <SlSwitch checked={!!cellInfo} onSlChange={(e: any) => handleCellValueChange(e.target.checked)} />
                    </div>
                );
            case 'color':
                return (
                    <div slot={slotName} className="table-custom-cell">
                        <SlColorPicker value={cellInfo} size="small" hoist onSlChange={(e: any) => handleCellValueChange(e.target.value)} />
                    </div>
                );
            case 'avatar':
                return (
                    <div slot={slotName} className="table-custom-cell">
                        <SlAvatar initials={props.rowInfo?.name?.charAt(0) || '?'} style={{ '--size': '32px' } as React.CSSProperties} />
                    </div>
                );
            case 'action':
                return (
                    <div slot={slotName} className="table-custom-cell">
                        <SlButton size="small" variant="primary" onClick={() => alert(`编辑 ${props.rowInfo?.name}`)}>操作</SlButton>
                    </div>
                );
            case 'progress':
                return (
                    <div slot={slotName} className="table-custom-cell">
                        <SlProgressBar value={Number(cellInfo) || 0} style={{ '--height': '12px' } as React.CSSProperties}>{cellInfo}%</SlProgressBar>
                    </div>
                );
        }
    }

    return (
        <div slot={slotName} className="table-custom-cell">
            {editing ? renderEditCell() : renderLockCell()}
        </div>
    );
};

export default () => {
    const [dataSource, setDataSource] = useState(editableDataSource);
    const [editKey, setEditKey] = useState('');

    const handleOnCell = (_record: any, index: number, colKey: string) => ({
        onclick: (e: Event) => {
            e?.stopPropagation();
            setEditKey(`${colKey}-${index}`);
        }
    });

    const columns = useMemo(
        () =>
            editableColumns.map((col) => ({
                ...col,
                slCell: col.slot ? (record: any, rowIndex: number) => handleOnCell(record, rowIndex, col.dataIndex) : undefined
            })),
        []
    );

    const handleCellValueChange = (value: any, index: number, colKey: string) => {
        const newData = [...dataSource];
        newData[index] = { ...newData[index], [colKey]: value };
        setDataSource(newData);
    };

    const handleGetCustomSlot = useMemo(
        () =>
            generateCustomSlot(
                'id',
                dataSource,
                columns
                    .filter((f) => f.slot)
                    .map((col) => ({
                        type: 'customCell' as const,
                        columnId: col.dataIndex,
                        callback: (props: any) => {
                            const editing = editKey === `${col.dataIndex}-${props.rowIndex}`;
                            return (
                                <EditCell
                                    key={props.slotName}
                                    handleCellValueChange={(value: any) => handleCellValueChange(value, props.rowIndex, col.dataIndex)}
                                    colKey={col.dataIndex}
                                    editing={editing}
                                    {...props}
                                />
                            );
                        }
                    }))
            ),
        [dataSource, columns, editKey]
    );

    useEffect(() => {
        const reset = () => setEditKey('');
        document.addEventListener('click', reset);
        return () => document.removeEventListener('click', reset);
    }, []);

    return (
        <div className="custom-cell-table">
            <SlTable rowKey="id" columns={columns} dataSource={dataSource} enableColumnResizing>
                {handleGetCustomSlot}
            </SlTable>
        </div>
    );
};
