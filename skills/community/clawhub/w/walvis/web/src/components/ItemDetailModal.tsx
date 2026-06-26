import { useEffect, useState, useRef, useCallback } from 'react';
import { createPortal } from 'react-dom';
import type { BookmarkItem } from '../lib/types';

interface Props {
  item: BookmarkItem;
  onClose: () => void;
  isLocalMode?: boolean;
  spaceId?: string;
  onItemChanged?: (updated: BookmarkItem) => void;
  onItemDeleted?: (id: string) => void;
}

export function ItemDetailModal({ item: initialItem, onClose, isLocalMode, spaceId, onItemChanged, onItemDeleted }: Props) {
  const [item, setItem] = useState(initialItem);
  const didMutate = useRef(false);

  // Tag editing
  const [newTag, setNewTag] = useState('');
  const [hoveredTag, setHoveredTag] = useState<string | null>(null);
  const tagInputRef = useRef<HTMLInputElement | null>(null);

  // Notes editing
  const [notes, setNotes] = useState(item.notes || '');
  const [notesSaving, setNotesSaving] = useState(false);
  const notesDirty = notes !== (item.notes || '');

  // Title editing
  const [editingTitle, setEditingTitle] = useState(false);
  const [titleValue, setTitleValue] = useState(item.title);
  const [titleHovered, setTitleHovered] = useState(false);
  const titleInputRef = useRef<HTMLInputElement | null>(null);

  // Delete confirm
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  // Toast
  const [toast, setToast] = useState<string | null>(null);
  const toastTimeout = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Sync parent on close if any edits were made
  const handleClose = useCallback(() => {
    if (didMutate.current && onItemChanged) onItemChanged(item);
    onClose();
  }, [onClose, onItemChanged, item]);

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        if (editingTitle) {
          setEditingTitle(false);
          setTitleValue(item.title);
        } else if (showDeleteConfirm) {
          setShowDeleteConfirm(false);
        } else {
          handleClose();
        }
      }
    };
    document.addEventListener('keydown', handleEscape);
    document.body.classList.add('modal-open');
    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.classList.remove('modal-open');
    };
  }, [handleClose, editingTitle, showDeleteConfirm, item.title]);

  useEffect(() => {
    if (editingTitle && titleInputRef.current) {
      titleInputRef.current.focus();
      titleInputRef.current.select();
    }
  }, [editingTitle]);

  const showToast = useCallback((msg: string) => {
    setToast(msg);
    if (toastTimeout.current) clearTimeout(toastTimeout.current);
    toastTimeout.current = setTimeout(() => setToast(null), 2000);
  }, []);

  // --- API helpers ---

  const removeTag = async (tag: string) => {
    if (!isLocalMode || !spaceId) return;
    const newTags = item.tags.filter(t => t !== tag);
    try {
      const res = await fetch(`/api/local/spaces/${spaceId}/items/${item.id}/tags`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tags: newTags }),
      });
      if (res.ok) {
        setItem(prev => ({ ...prev, tags: newTags }));
        didMutate.current = true;
      }
    } catch { /* ignore */ }
  };

  const addTag = async () => {
    if (!isLocalMode || !spaceId) return;
    const tag = newTag.trim().toLowerCase();
    if (!tag || item.tags.includes(tag)) {
      setNewTag('');
      return;
    }
    const newTags = [...item.tags, tag];
    try {
      const res = await fetch(`/api/local/spaces/${spaceId}/items/${item.id}/tags`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tags: newTags }),
      });
      if (res.ok) {
        setItem(prev => ({ ...prev, tags: newTags }));
        setNewTag('');
        didMutate.current = true;
      }
    } catch { /* ignore */ }
  };

  const saveNotes = async () => {
    if (!isLocalMode || !spaceId) return;
    setNotesSaving(true);
    try {
      const res = await fetch(`/api/local/spaces/${spaceId}/items/${item.id}/note`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ notes }),
      });
      if (res.ok) {
        setItem(prev => ({ ...prev, notes }));
        didMutate.current = true;
        showToast('Notes saved');
      }
    } catch { /* ignore */ }
    setNotesSaving(false);
  };

  const saveTitle = async () => {
    if (!isLocalMode || !spaceId) return;
    const trimmed = titleValue.trim();
    if (!trimmed || trimmed === item.title) {
      setEditingTitle(false);
      setTitleValue(item.title);
      return;
    }
    try {
      const res = await fetch(`/api/local/spaces/${spaceId}/items/${item.id}/title`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: trimmed }),
      });
      if (res.ok) {
        setItem(prev => ({ ...prev, title: trimmed }));
        didMutate.current = true;
      }
    } catch { /* ignore */ }
    setEditingTitle(false);
  };

  const handleDelete = async () => {
    if (!isLocalMode || !spaceId) return;
    try {
      const res = await fetch(`/api/local/spaces/${spaceId}/items/${item.id}`, {
        method: 'DELETE',
      });
      if (res.ok) {
        if (onItemDeleted) onItemDeleted(item.id);
        onClose();
      }
    } catch { /* ignore */ }
  };

  const handleCopy = () => {
    const text = item.url || item.content || item.title;
    navigator.clipboard.writeText(text).then(() => {
      showToast('Copied to clipboard');
    }).catch(() => {
      showToast('Failed to copy');
    });
  };

  const modalRoot = document.getElementById('modal-root');
  if (!modalRoot) return null;

  return createPortal(
    <div
      onClick={handleClose}
      style={{
        position: 'fixed',
        inset: 0,
        background: 'rgba(8, 14, 27, 0.9)',
        backdropFilter: 'blur(8px)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
        padding: 40,
        animation: 'modal-fade 0.3s ease forwards',
      }}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          width: '100%',
          maxWidth: 1200,
          maxHeight: '90vh',
          background: 'var(--deep)',
          border: '1px solid var(--rim)',
          borderRadius: 12,
          overflow: 'hidden',
          display: 'flex',
          boxShadow: '0 20px 60px rgba(0, 0, 0, 0.5)',
          position: 'relative',
        }}
      >
        {/* Left: Content preview (60%) */}
        <div style={{
          flex: '0 0 60%',
          background: 'var(--abyss)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: 40,
          overflow: 'auto',
        }}>
          {item.type === 'link' && item.screenshot ? (
            <img src={item.screenshot} alt={item.title} style={{ maxWidth: '100%', borderRadius: 8 }} />
          ) : item.type === 'image' ? (
            <img src={item.url || item.content} alt={item.title} style={{ maxWidth: '100%', borderRadius: 8 }} />
          ) : (
            <div style={{
              width: '100%',
              fontSize: 14,
              lineHeight: 1.8,
              color: 'var(--text)',
              whiteSpace: 'pre-wrap',
              fontFamily: 'var(--font-data)',
            }}>
              {item.content}
            </div>
          )}
        </div>

        {/* Right: Metadata (40%) */}
        <div style={{
          flex: '0 0 40%',
          padding: 32,
          display: 'flex',
          flexDirection: 'column',
          gap: 24,
          overflow: 'auto',
        }}>
          {/* Close button */}
          <button
            onClick={handleClose}
            style={{
              alignSelf: 'flex-end',
              background: 'none',
              border: 'none',
              fontSize: 24,
              color: 'var(--text-muted)',
              cursor: 'pointer',
              padding: 0,
              lineHeight: 1,
              transition: 'color 0.2s',
            }}
            onMouseEnter={(e) => e.currentTarget.style.color = '#fff'}
            onMouseLeave={(e) => e.currentTarget.style.color = 'var(--text-muted)'}
          >
            ×
          </button>

          {/* Title - inline editable */}
          <div
            onMouseEnter={() => setTitleHovered(true)}
            onMouseLeave={() => setTitleHovered(false)}
            style={{ position: 'relative' }}
          >
            {editingTitle ? (
              <input
                ref={titleInputRef}
                value={titleValue}
                onChange={(e) => setTitleValue(e.target.value)}
                onBlur={saveTitle}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') saveTitle();
                  if (e.key === 'Escape') {
                    setEditingTitle(false);
                    setTitleValue(item.title);
                  }
                }}
                style={{
                  width: '100%',
                  fontFamily: 'var(--font-display)',
                  fontSize: 20,
                  fontWeight: 700,
                  color: '#fff',
                  lineHeight: 1.3,
                  background: 'var(--layer)',
                  border: '1px solid var(--walrus-mint-dim)',
                  borderRadius: 6,
                  padding: '6px 10px',
                  outline: 'none',
                }}
              />
            ) : (
              <h2
                style={{
                  fontFamily: 'var(--font-display)',
                  fontSize: 20,
                  fontWeight: 700,
                  color: '#fff',
                  lineHeight: 1.3,
                  margin: 0,
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: 8,
                }}
              >
                <span style={{ flex: 1 }}>{item.title}</span>
                {isLocalMode && titleHovered && (
                  <button
                    onClick={() => setEditingTitle(true)}
                    style={{
                      background: 'none',
                      border: 'none',
                      padding: 2,
                      cursor: 'pointer',
                      color: 'var(--walrus-mint)',
                      fontSize: 14,
                      lineHeight: 1,
                      flexShrink: 0,
                      opacity: 0.7,
                      transition: 'opacity 0.2s',
                    }}
                    onMouseEnter={(e) => e.currentTarget.style.opacity = '1'}
                    onMouseLeave={(e) => e.currentTarget.style.opacity = '0.7'}
                    title="Edit title"
                  >
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
                    </svg>
                  </button>
                )}
              </h2>
            )}
          </div>

          {/* Summary */}
          <p style={{
            fontSize: 13,
            lineHeight: 1.6,
            color: 'var(--text-muted)',
            margin: 0,
          }}>
            {item.summary}
          </p>

          {/* URL */}
          {item.url && (
            <div>
              <div style={{ fontSize: 10, color: 'var(--text-dim)', marginBottom: 4, letterSpacing: '0.1em', textTransform: 'uppercase' }}>URL</div>
              <a href={item.url} target="_blank" rel="noopener noreferrer" style={{
                fontSize: 12,
                color: 'var(--walrus-mint)',
                wordBreak: 'break-all',
              }}>
                {item.url}
              </a>
            </div>
          )}

          {/* Tags - inline editable */}
          <div>
            <div style={{ fontSize: 10, color: 'var(--text-dim)', marginBottom: 8, letterSpacing: '0.1em', textTransform: 'uppercase' }}>
              Tags
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, alignItems: 'center' }}>
              {item.tags.map(tag => (
                <span
                  key={tag}
                  onMouseEnter={() => isLocalMode && setHoveredTag(tag)}
                  onMouseLeave={() => setHoveredTag(null)}
                  style={{
                    fontSize: 11,
                    padding: '4px 10px',
                    background: 'var(--walrus-mint-faint)',
                    border: '1px solid var(--walrus-mint-dim)',
                    borderRadius: 4,
                    color: 'var(--walrus-mint)',
                    letterSpacing: '0.05em',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: 6,
                    transition: 'all 0.15s',
                    ...(hoveredTag === tag ? { borderColor: 'var(--danger)', background: 'rgba(255,107,107,0.08)' } : {}),
                  }}
                >
                  #{tag}
                  {isLocalMode && hoveredTag === tag && (
                    <button
                      onClick={() => removeTag(tag)}
                      style={{
                        background: 'none',
                        border: 'none',
                        padding: 0,
                        cursor: 'pointer',
                        color: 'var(--danger)',
                        fontSize: 13,
                        lineHeight: 1,
                        display: 'flex',
                        alignItems: 'center',
                      }}
                      title="Remove tag"
                    >
                      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                        <line x1="18" y1="6" x2="6" y2="18" />
                        <line x1="6" y1="6" x2="18" y2="18" />
                      </svg>
                    </button>
                  )}
                </span>
              ))}
              {isLocalMode && (
                <span style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: 2,
                }}>
                  <input
                    ref={tagInputRef}
                    value={newTag}
                    onChange={(e) => setNewTag(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') addTag();
                    }}
                    placeholder="add…"
                    style={{
                      width: 60,
                      fontSize: 11,
                      padding: '4px 8px',
                      background: 'transparent',
                      border: '1px solid var(--rim)',
                      borderRadius: 4,
                      color: 'var(--walrus-mint)',
                      outline: 'none',
                      letterSpacing: '0.05em',
                      transition: 'border-color 0.2s',
                    }}
                    onFocus={(e) => e.currentTarget.style.borderColor = 'var(--walrus-mint-dim)'}
                    onBlur={(e) => e.currentTarget.style.borderColor = 'var(--rim)'}
                  />
                  <button
                    onClick={addTag}
                    style={{
                      background: 'none',
                      border: '1px solid var(--rim)',
                      borderRadius: 4,
                      padding: '4px 6px',
                      cursor: 'pointer',
                      color: 'var(--walrus-mint)',
                      fontSize: 13,
                      lineHeight: 1,
                      display: 'flex',
                      alignItems: 'center',
                      transition: 'all 0.15s',
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.borderColor = 'var(--walrus-mint)';
                      e.currentTarget.style.background = 'var(--walrus-mint-faint)';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.borderColor = 'var(--rim)';
                      e.currentTarget.style.background = 'none';
                    }}
                    title="Add tag"
                  >
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                      <line x1="12" y1="5" x2="12" y2="19" />
                      <line x1="5" y1="12" x2="19" y2="12" />
                    </svg>
                  </button>
                </span>
              )}
            </div>
          </div>

          {/* Notes - inline textarea */}
          <div>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: 8,
              marginBottom: 8,
            }}>
              <div style={{ fontSize: 10, color: 'var(--text-dim)', letterSpacing: '0.1em', textTransform: 'uppercase' }}>Notes</div>
              {isLocalMode && notesDirty && (
                <button
                  onClick={saveNotes}
                  disabled={notesSaving}
                  style={{
                    background: 'var(--walrus-mint-faint)',
                    border: '1px solid var(--walrus-mint-dim)',
                    borderRadius: 4,
                    padding: '2px 10px',
                    fontSize: 10,
                    color: 'var(--walrus-mint)',
                    cursor: notesSaving ? 'wait' : 'pointer',
                    letterSpacing: '0.05em',
                    transition: 'all 0.2s',
                    opacity: notesSaving ? 0.5 : 1,
                  }}
                  onMouseEnter={(e) => {
                    if (!notesSaving) {
                      e.currentTarget.style.borderColor = 'var(--walrus-mint)';
                      e.currentTarget.style.background = 'var(--walrus-mint-glow)';
                    }
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.borderColor = 'var(--walrus-mint-dim)';
                    e.currentTarget.style.background = 'var(--walrus-mint-faint)';
                  }}
                >
                  {notesSaving ? 'Saving…' : 'Save'}
                </button>
              )}
            </div>
            {isLocalMode ? (
              <textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="Add a note…"
                rows={3}
                style={{
                  width: '100%',
                  fontSize: 12,
                  lineHeight: 1.6,
                  color: 'var(--text)',
                  background: 'var(--layer)',
                  border: '1px solid var(--rim)',
                  borderRadius: 6,
                  padding: '10px 12px',
                  outline: 'none',
                  resize: 'vertical',
                  fontFamily: 'var(--font-data)',
                  transition: 'border-color 0.2s',
                }}
                onFocus={(e) => e.currentTarget.style.borderColor = 'var(--walrus-mint-dim)'}
                onBlur={(e) => e.currentTarget.style.borderColor = 'var(--rim)'}
              />
            ) : (
              <div style={{
                fontSize: 12,
                color: item.notes ? 'var(--text)' : 'var(--text-dim)',
                fontStyle: item.notes ? 'normal' : 'italic',
                lineHeight: 1.6,
              }}>
                {item.notes || 'No notes'}
              </div>
            )}
          </div>

          {/* Metadata */}
          <div style={{
            marginTop: 'auto',
            paddingTop: 24,
            borderTop: '1px solid var(--rim)',
            display: 'flex',
            flexDirection: 'column',
            gap: 8,
            fontSize: 11,
            color: 'var(--text-dim)',
          }}>
            <div><span style={{ color: 'var(--text-muted)' }}>Source:</span> {item.source}</div>
            <div><span style={{ color: 'var(--text-muted)' }}>Created:</span> {new Date(item.createdAt).toLocaleString()}</div>
            {item.updatedAt && (
              <div><span style={{ color: 'var(--text-muted)' }}>Updated:</span> {new Date(item.updatedAt).toLocaleString()}</div>
            )}
            <div><span style={{ color: 'var(--text-muted)' }}>Analyzed by:</span> {item.analyzedBy}</div>
          </div>

          {/* Bottom action bar: Delete + Copy */}
          {isLocalMode && (
            <div style={{
              display: 'flex',
              justifyContent: 'flex-end',
              gap: 8,
              paddingTop: 8,
            }}>
              <button
                onClick={handleCopy}
                style={{
                  background: 'none',
                  border: '1px solid var(--rim)',
                  borderRadius: 6,
                  padding: '6px 14px',
                  fontSize: 11,
                  color: 'var(--text-muted)',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 6,
                  letterSpacing: '0.05em',
                  transition: 'all 0.2s',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.borderColor = 'var(--walrus-mint-dim)';
                  e.currentTarget.style.color = 'var(--walrus-mint)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.borderColor = 'var(--rim)';
                  e.currentTarget.style.color = 'var(--text-muted)';
                }}
              >
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
                  <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
                </svg>
                Copy
              </button>

              {showDeleteConfirm ? (
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 6,
                }}>
                  <span style={{ fontSize: 11, color: 'var(--danger)' }}>Delete?</span>
                  <button
                    onClick={handleDelete}
                    style={{
                      background: 'rgba(255,107,107,0.12)',
                      border: '1px solid var(--danger)',
                      borderRadius: 6,
                      padding: '6px 12px',
                      fontSize: 11,
                      color: 'var(--danger)',
                      cursor: 'pointer',
                      letterSpacing: '0.05em',
                      transition: 'all 0.2s',
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.background = 'rgba(255,107,107,0.25)';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.background = 'rgba(255,107,107,0.12)';
                    }}
                  >
                    Yes
                  </button>
                  <button
                    onClick={() => setShowDeleteConfirm(false)}
                    style={{
                      background: 'none',
                      border: '1px solid var(--rim)',
                      borderRadius: 6,
                      padding: '6px 12px',
                      fontSize: 11,
                      color: 'var(--text-muted)',
                      cursor: 'pointer',
                      letterSpacing: '0.05em',
                      transition: 'all 0.2s',
                    }}
                  >
                    No
                  </button>
                </div>
              ) : (
                <button
                  onClick={() => setShowDeleteConfirm(true)}
                  style={{
                    background: 'none',
                    border: '1px solid var(--rim)',
                    borderRadius: 6,
                    padding: '6px 14px',
                    fontSize: 11,
                    color: 'var(--text-muted)',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: 6,
                    letterSpacing: '0.05em',
                    transition: 'all 0.2s',
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.borderColor = 'var(--danger)';
                    e.currentTarget.style.color = 'var(--danger)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.borderColor = 'var(--rim)';
                    e.currentTarget.style.color = 'var(--text-muted)';
                  }}
                >
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="3 6 5 6 21 6" />
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                  </svg>
                  Delete
                </button>
              )}
            </div>
          )}
        </div>

        {/* Toast notification */}
        {toast && (
          <div style={{
            position: 'absolute',
            bottom: 20,
            left: '50%',
            transform: 'translateX(-50%)',
            background: 'var(--layer)',
            border: '1px solid var(--walrus-mint-dim)',
            borderRadius: 8,
            padding: '8px 20px',
            fontSize: 12,
            color: 'var(--walrus-mint)',
            boxShadow: '0 4px 20px rgba(0,0,0,0.4)',
            animation: 'modal-fade 0.2s ease forwards',
            zIndex: 10,
            pointerEvents: 'none',
          }}>
            {toast}
          </div>
        )}
      </div>
    </div>,
    modalRoot
  );
}
