import streamlit as st
from agente import stream_chat

st.set_page_config(
    page_title="Cleo",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Inter:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif;
    background-color: #111 !important;
    color: #f0ece4;
}

#MainMenu, footer, header, .stDeployButton,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

.block-container {
    max-width: 700px !important;
    padding: 0 1.5rem 7rem 1.5rem !important;
}

/* ── HEADER ── */
.cleo-header {
    text-align: center;
    padding: 3rem 0 2rem 0;
    border-bottom: 1px solid #222;
    margin-bottom: 2rem;
}
.cleo-title {
    font-family: 'Playfair Display', serif;
    font-size: 5rem;
    font-weight: 700;
    letter-spacing: -3px;
    color: #f0ece4;
    line-height: 1;
}
.cleo-title em {
    font-style: italic;
    color: #e8643a;
}
.cleo-subtitle {
    font-size: 0.78rem;
    color: #444;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    margin-top: 0.75rem;
}

/* ── MENSAGENS ── */
.message-user {
    display: flex;
    justify-content: flex-end;
    margin: 0.6rem 0;
}
.message-cleo {
    display: flex;
    justify-content: flex-start;
    align-items: flex-end;
    gap: 0.5rem;
    margin: 0.6rem 0;
}
.bubble-user {
    background: #e8643a;
    color: #fff;
    padding: 0.7rem 1rem;
    border-radius: 16px 16px 3px 16px;
    max-width: 72%;
    font-size: 0.92rem;
    line-height: 1.55;
    word-wrap: break-word;
}
.bubble-cleo {
    background: #1c1c1c;
    color: #f0ece4;
    padding: 0.7rem 1rem;
    border-radius: 16px 16px 16px 3px;
    max-width: 72%;
    font-size: 0.92rem;
    line-height: 1.65;
    border: 1px solid #2a2a2a;
    word-wrap: break-word;
}
.cleo-avatar {
    font-size: 1.1rem;
    flex-shrink: 0;
    margin-bottom: 2px;
}

/* ── INDICADOR DE DIGITANDO ── */
.typing-dots {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 0.2rem 0;
}
.typing-dots span {
    width: 7px;
    height: 7px;
    background: #555;
    border-radius: 50%;
    animation: bounce 1.2s infinite ease-in-out;
}
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce {
    0%, 80%, 100% { transform: translateY(0); opacity: 0.4; }
    40% { transform: translateY(-5px); opacity: 1; }
}

/* ── SUGESTÕES ── */
.suggestions-label {
    color: #444;
    font-size: 0.78rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
    text-align: center;
}
div[data-testid="column"] .stButton > button {
    background-color: #1c1c1c !important;
    color: #888 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 20px !important;
    font-size: 0.78rem !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0.4rem 0.8rem !important;
    width: 100% !important;
    white-space: normal !important;
    height: auto !important;
    line-height: 1.4 !important;
}
div[data-testid="column"] .stButton > button:hover {
    border-color: #e8643a !important;
    color: #e8643a !important;
}

/* ── BOTÃO LIMPAR ── */
.stButton > button {
    background-color: transparent !important;
    color: #444 !important;
    border: 1px solid #222 !important;
    border-radius: 8px !important;
    font-size: 0.78rem !important;
    font-family: 'Inter', sans-serif !important;
}
.stButton > button:hover {
    color: #888 !important;
    border-color: #333 !important;
}

/* ── CHAT INPUT — remove fundo azul e estilos nativos ── */
[data-testid="stBottom"] {
    background-color: #111 !important;
    border-top: 1px solid #1e1e1e !important;
    padding: 0.75rem 0 !important;
}
[data-testid="stBottom"] > div {
    background-color: #111 !important;
}
[data-testid="stChatInputContainer"] {
    background-color: #1c1c1c !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 14px !important;
    box-shadow: none !important;
}
[data-testid="stChatInputContainer"]:focus-within {
    border-color: #e8643a !important;
    box-shadow: 0 0 0 2px rgba(232,100,58,0.1) !important;
}
[data-testid="stChatInputContainer"] textarea {
    background-color: transparent !important;
    color: #f0ece4 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.92rem !important;
    caret-color: #e8643a !important;
}
[data-testid="stChatInputContainer"] textarea::placeholder {
    color: #444 !important;
}
[data-testid="stChatInputContainer"] button[kind="primaryFormSubmit"],
[data-testid="stChatInputContainer"] button {
    background-color: #e8643a !important;
    border-radius: 8px !important;
    border: none !important;
    color: white !important;
}
[data-testid="stChatInputContainer"] button:hover {
    background-color: #d0512a !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cleo-header">
    <div class="cleo-title">Cl<em>e</em>o</div>
    <div class="cleo-subtitle">filmes · séries · livros</div>
</div>
""", unsafe_allow_html=True)

# ── Estado ────────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Histórico ─────────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="message-user">
            <div class="bubble-user">{msg["content"]}</div>
        </div>""", unsafe_allow_html=True)
    else:
        content = msg["content"].replace("\n", "<br>")
        st.markdown(f"""
        <div class="message-cleo">
            <span class="cleo-avatar">🎬</span>
            <div class="bubble-cleo">{content}</div>
        </div>""", unsafe_allow_html=True)

# ── Sugestões rápidas ─────────────────────────────────────────────────────────
suggestions = [
    "Quero um filme pra hoje à noite",
    "Série que prende desde o primeiro ep",
    "Livro pra quem não tem paciência",
    "Algo de terror psicológico",
]

if not st.session_state.messages:
    st.markdown('<p class="suggestions-label">por onde começar</p>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, (col, s) in enumerate(zip(cols, suggestions)):
        with col:
            if st.button(s, key=f"sug_{i}"):
                st.session_state.messages.append({"role": "user", "content": s})
                response = ""
                for chunk in stream_chat(st.session_state.messages):
                    response += chunk
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

# ── Botão limpar ──────────────────────────────────────────────────────────────
if st.session_state.messages:
    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:
        if st.button("↺ limpar", key="clear"):
            st.session_state.messages = []
            st.rerun()

# ── Input fixo no rodapé ──────────────────────────────────────────────────────
user_input = st.chat_input("O que você quer assistir ou ler?")

if user_input and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})

    st.markdown(f"""
    <div class="message-user">
        <div class="bubble-user">{user_input.strip()}</div>
    </div>""", unsafe_allow_html=True)

    # Indicador de "pensando" antes do primeiro chunk
    placeholder = st.empty()
    placeholder.markdown("""
    <div class="message-cleo">
        <span class="cleo-avatar">🎬</span>
        <div class="bubble-cleo">
            <div class="typing-dots">
                <span></span><span></span><span></span>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    response = ""
    for chunk in stream_chat(st.session_state.messages):
        response += chunk
        placeholder.markdown(f"""
        <div class="message-cleo">
            <span class="cleo-avatar">🎬</span>
            <div class="bubble-cleo">{response.replace(chr(10), "<br>")}▌</div>
        </div>""", unsafe_allow_html=True)

    placeholder.markdown(f"""
    <div class="message-cleo">
        <span class="cleo-avatar">🎬</span>
        <div class="bubble-cleo">{response.replace(chr(10), "<br>")}</div>
    </div>""", unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": response})
