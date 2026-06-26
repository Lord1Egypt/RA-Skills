let currentTranscript = "";
let currentVideoId = "";

// --- SECURE API KEY STORAGE ---
let secureApiKey = "";
let secureOpenAiKey = "";

document.getElementById('apiKey').addEventListener('change', function() {
    if (this.value && this.value !== "••••••••••••••••") {
        secureApiKey = this.value; 
        this.value = "••••••••••••••••"; 
        this.disabled = true; 
        log("🔐 Gemini API Key secured in memory and removed from DOM.");
    }
});

document.getElementById('openaiApiKey').addEventListener('change', function() {
    if (this.value && this.value !== "••••••••••••••••") {
        secureOpenAiKey = this.value; 
        this.value = "••••••••••••••••"; 
        this.disabled = true; 
        log("🔐 OpenAI API Key secured in memory and removed from DOM.");
    }
});

// --- AUTO-RESIZE TEXTAREA HELPER ---
function autoResizeEditor() {
    const editor = document.getElementById('script-editor');
    editor.style.height = 'auto'; 
    editor.style.height = editor.scrollHeight + 'px';
}

document.getElementById('script-editor').addEventListener('input', function() {
    document.getElementById('btn-download-script').disabled = this.value.trim().length === 0;
    autoResizeEditor(); 
});

function generateNumericId(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = ((hash << 5) - hash) + str.charCodeAt(i);
        hash |= 0; 
    }
    return Math.abs(hash).toString() + Date.now().toString();
}

const log = (msg) => {
    const container = document.getElementById('log-container');
    const messages = document.getElementById('log-messages');
    container.style.display = 'block';
    
    const msgDiv = document.createElement('div');
    msgDiv.textContent = `> ${msg}`;
    messages.appendChild(msgDiv);
    
    container.scrollTop = container.scrollHeight;
};

const setApiLoading = (isLoading) => {
    const spinnerDiv = document.getElementById('log-active-spinner');
    const container = document.getElementById('log-container');
    
    if (isLoading) {
        container.style.display = 'block';
        spinnerDiv.style.display = 'block';
        container.appendChild(spinnerDiv); 
        container.scrollTop = container.scrollHeight;
    } else {
        spinnerDiv.style.display = 'none';
    }
};

// --- RESET UI & DELETE ---
document.getElementById('btn-clear').addEventListener('click', async () => {
    if (currentVideoId) {
        await fetch('/api/delete-folder', { 
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: currentVideoId })
        });
    }

    currentTranscript = "";
    currentVideoId = "";

    secureApiKey = "";
    const keyInput = document.getElementById('apiKey');
    keyInput.value = "";
    keyInput.disabled = false;

    secureOpenAiKey = "";
    const openaiKeyInput = document.getElementById('openaiApiKey');
    openaiKeyInput.value = "";
    openaiKeyInput.disabled = false;

    document.getElementById('url').value = "";
    document.getElementById('script-editor').value = "";
    document.getElementById('script-editor').style.height = 'auto';
    document.getElementById('yt-preview').innerText = "";
    document.getElementById('search-results').innerHTML = "";
    
    document.getElementById('log-messages').innerHTML = "";
    document.getElementById('log-container').style.display = 'none';
    setApiLoading(false);

    document.getElementById('editor-container').style.display = 'none';
    document.getElementById('search-container').style.display = 'none';
    document.getElementById('result-container').style.display = 'none';
    document.getElementById('btn-download-txt').style.display = 'none';
    
    document.getElementById('btn-download-script').disabled = true;
    document.getElementById('btn-generate-audio').disabled = true;
    document.getElementById('file-preview-modal').style.display = 'none';
    
    document.getElementById('audio-player').pause();
    document.getElementById('audio-player').innerHTML = ""; 
    document.getElementById('audio-player').removeAttribute('src');
    document.getElementById('audio-player').load(); 
    
    log("Studio reset for new video. Server wiped. API Keys cleared.");
});

// --- FILE PREVIEW VIEWER LOGIC ---
document.querySelectorAll('.file-preview-link').forEach(link => {
    link.addEventListener('click', async (e) => {
        e.preventDefault(); 
        if (!currentVideoId) return;

        const fileName = e.target.getAttribute('data-file');
        const title = e.target.getAttribute('data-title');
        
        try {
            const response = await fetch(`/downloads/${currentVideoId}/${fileName}?t=${Date.now()}`);
            if (!response.ok) throw new Error(`Could not load ${fileName}. It may not be generated yet.`);
            
            const rawText = await response.text();
            
            document.getElementById('preview-title').innerText = `👀 Viewing: ${title} (${fileName})`;
            // Changed from textContent to value for the textarea
            document.getElementById('preview-content').value = rawText;
            document.getElementById('file-preview-modal').style.display = 'block';
            
            document.getElementById('file-preview-modal').scrollIntoView({ behavior: 'smooth' });

        } catch (err) {
            log(`❌ Error viewing file: ${err.message}`);
        }
    });
});

document.getElementById('btn-close-preview').addEventListener('click', () => {
    document.getElementById('file-preview-modal').style.display = 'none';
    // Changed from textContent to value for the textarea
    document.getElementById('preview-content').value = "";
});

document.getElementById('btn-copy-preview').addEventListener('click', async () => {
    // Changed from textContent to value for the textarea
    const textToCopy = document.getElementById('preview-content').value;
    const copyBtn = document.getElementById('btn-copy-preview');
    
    try {
        copyBtn.innerHTML = '<span class="spinner"></span> Copying...';
        await navigator.clipboard.writeText(textToCopy);
        
        copyBtn.innerHTML = "✅ Copied!";
        copyBtn.style.backgroundColor = "#27ae60"; 
        
        setTimeout(() => {
            copyBtn.innerHTML = "📋 Copy";
            copyBtn.style.backgroundColor = "#2ecc71"; 
        }, 2000);
    } catch (err) {
        alert("Failed to copy to clipboard.");
        console.error(err);
        copyBtn.innerHTML = "📋 Copy";
    }
});

// --- DOWNLOAD FILES ---
document.getElementById('btn-download-txt').addEventListener('click', () => {
    if (!currentTranscript) return;
    const blob = new Blob([currentTranscript], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'youtube-transcript.txt';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
});

document.getElementById('btn-download-script').addEventListener('click', () => {
    const scriptContent = document.getElementById('script-editor').value;
    if (!scriptContent) return alert("The script editor is empty! Generate or write a script first.");
    const blob = new Blob([scriptContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'podcast-script.txt';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
    log("✅ Podcast script downloaded.");
});

document.getElementById('btn-download-zip').addEventListener('click', () => {
    if (!currentVideoId) return alert("No active video session found.");
    log("📦 Compressing files into a zip archive...");
    window.location.href = `/api/download-zip?id=${currentVideoId}`;
});

// --- STEP 1: TRANSCRIBE ---
document.getElementById('btn-transcribe').addEventListener('click', async () => {
    const url = document.getElementById('url').value;
    const lang = document.getElementById('transcriptLang').value;
    if (!url) return alert("Enter a YouTube URL");
    
    currentVideoId = generateNumericId(url); 
    
    log(`Fetching ${lang ? lang.toUpperCase() : 'Default'} transcript and creating folder securely...`);
    setApiLoading(true);
    
    try {
        const res = await fetch('/api/transcribe', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url, id: currentVideoId, lang: lang })
        });
        const data = await res.json();
        if (data.fullText) {
            currentTranscript = data.fullText;
            document.getElementById('yt-preview').innerText = "Transcript Ready.";
            document.getElementById('editor-container').style.display = 'block';
            document.getElementById('search-container').style.display = 'block';
            document.getElementById('btn-download-txt').style.display = 'inline-block';
            log(`Secure storage created for video context.`);
        } else log("❌ " + data.error);
    } catch (err) { 
        log("Error: " + err.message); 
    } finally {
        setApiLoading(false);
    }
});

// --- SEARCH ---
document.getElementById('btn-search').addEventListener('click', async () => {
    const query = document.getElementById('search-query').value;
    if (!query || !secureApiKey) return alert("Gemini API Key and Query required."); 
    
    log("Searching VTT via Gemini...");
    setApiLoading(true);
    
    try {
        const res = await fetch('/api/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'x-api-key': secureApiKey }, 
            body: JSON.stringify({ id: currentVideoId, query: query })
        });
        const data = await res.json();
        if (data.results) {
            document.getElementById('search-results').innerHTML = data.results.map(r => `
                <div class="search-item">
                    <strong>"${r.text}"</strong><br>
                    <a href="https://youtube.com/watch?v=${currentVideoId}&t=${r.seconds}s" target="_blank">Jump to ${r.timestamp} ➔</a>
                </div>
            `).join('');
        } else log("❌ " + data.error);
    } catch (err) { 
        log("Error: " + err.message); 
    } finally {
        setApiLoading(false);
    }
});

// --- STEP 2: DRAFT ---
document.getElementById('btn-draft').addEventListener('click', async () => {
    const host1 = document.getElementById('host1').value || 'Alex';
    const host2 = document.getElementById('host2').value || 'Sam';
    const targetLanguage = document.getElementById('targetLanguage').value || 'English';

    if (!secureApiKey) return alert("Gemini API Key required.");

    log(`Generating ${targetLanguage} script draft for ${host1} & ${host2}...`);
    setApiLoading(true);
    
    try {
        const res = await fetch('/api/draft-script', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'x-api-key': secureApiKey },
            body: JSON.stringify({ id: currentVideoId, host1, host2, targetLanguage })
        });
        const data = await res.json();
        if (data.script) {
            document.getElementById('script-editor').value = data.script;
            document.getElementById('btn-generate-audio').disabled = false;
            document.getElementById('btn-download-script').disabled = false; 
            
            autoResizeEditor(); 
            log("Draft ready for editing.");
        } else log("❌ " + data.error);
    } catch (err) { 
        log("Error: " + err.message); 
    } finally {
        setApiLoading(false);
    }
});

// --- STEP 3: AUDIO (POLLING ARCHITECTURE) ---
document.getElementById('btn-generate-audio').addEventListener('click', async function() {
    const script = document.getElementById('script-editor').value;
    const host1 = document.getElementById('host1').value || 'Alex';
    const host2 = document.getElementById('host2').value || 'Sam';
    
    if (!secureApiKey) return alert("Gemini API Key required for context.");
    if (!secureOpenAiKey) return alert("OpenAI API Key required for audio generation.");
    if (!script) return alert("Script is empty.");
    
    this.disabled = true; 
    log("Starting background task... This may take several minutes.");
    setApiLoading(true); 

    try {
        const response = await fetch('/api/synthesize', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json', 
                'x-api-key': secureApiKey,
                'x-openai-key': secureOpenAiKey 
            },
            body: JSON.stringify({ id: currentVideoId, script: script, host1: host1, host2: host2 })
        });

        const initData = await response.json();
        if (!initData.success) throw new Error(initData.error || "Failed to start job.");

        let lastMsg = "";
        const pollInterval = setInterval(async () => {
            try {
                const statusRes = await fetch(`/api/status?id=${currentVideoId}`);
                const data = await statusRes.json();

                if (data.status === 'not_found' || data.status === 'error') {
                    clearInterval(pollInterval);
                    setApiLoading(false); 
                    log(`❌ ${data.status === 'error' ? 'Server Error: ' + data.message : 'Job disappeared.'}`);
                    document.getElementById('btn-generate-audio').disabled = false;
                } 
                else if (data.status === 'done') {
                    clearInterval(pollInterval);
                    setApiLoading(false); 
                    handleSynthesisSuccess(data.file); 
                } 
                else if (data.status === 'processing' || data.status === 'queued') {
                    if (data.message && data.message !== lastMsg) {
                        log(data.message);
                        lastMsg = data.message;
                    }
                }
            } catch (pollErr) {
                console.warn("Polling hiccup:", pollErr);
            }
        }, 2000); 

    } catch (err) {
        log("❌ Failed to initiate task: " + err.message);
        console.error(err);
        setApiLoading(false); 
        this.disabled = false;
    }
});

function handleSynthesisSuccess(file) {
    const vttFile = file.replace('.m4a', '.vtt'); 
    const audioPlayer = document.getElementById('audio-player');
    const liveCaptions = document.getElementById('live-captions');

    audioPlayer.innerHTML = ''; 
    audioPlayer.removeAttribute('src'); 
    liveCaptions.innerHTML = '<em>Press play to see captions...</em>';
    
    const timestamp = Date.now();
    
    const sourceNode = document.createElement('source');
    sourceNode.src = `/downloads/${currentVideoId}/${file}?t=${timestamp}`;
    sourceNode.type = 'audio/mp4'; 
    audioPlayer.appendChild(sourceNode);
    
    const vttBtn = document.getElementById('download-podcast-vtt');
    vttBtn.href = `/downloads/${currentVideoId}/${vttFile}`;
    vttBtn.download = `podcast_${currentVideoId}.vtt`;

    const track = document.createElement('track');
    track.kind = 'captions';
    track.label = 'English';
    track.srclang = 'en';
    track.src = `/downloads/${currentVideoId}/${vttFile}?t=${timestamp}`;
    track.default = true;
    audioPlayer.appendChild(track);

    audioPlayer.load();

    track.addEventListener('load', function() {
        const textTrack = audioPlayer.textTracks[0];
        textTrack.mode = 'hidden'; 
        textTrack.oncuechange = function(e) {
            const cues = e.target.activeCues;
            if (cues && cues.length > 0) {
                let rawText = cues[0].text;
                let formattedText = rawText.replace(/<v ([^>]+)>/g, '<strong style="color: #ffffff;">$1:</strong> ');
                formattedText = formattedText.replace(/<\/v>/g, '');
                formattedText = formattedText.replace(/\n/g, '<br>');
                liveCaptions.innerHTML = `<span>${formattedText}</span>`;
            } else {
                liveCaptions.innerHTML = '<span style="color:#bdc3c7;">...</span>';
            }
        };
    });

    document.getElementById('result-container').style.display = 'block';
    document.getElementById('btn-generate-audio').disabled = false;
    log("✅ Final M4A and VTT ready!");
}

// --- AUTOMATIC CLEANUP ON TAB CLOSE ---
window.addEventListener('beforeunload', () => {
    if (currentVideoId) {
        fetch('/api/delete-folder', {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: currentVideoId }),
            keepalive: true 
        }).catch(err => console.error("Tab-close cleanup failed:", err));
    }
});