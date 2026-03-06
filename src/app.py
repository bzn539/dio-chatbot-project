import streamlit as st
from agente import stream_chat

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Cleo",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS customizado ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0e0e0e;
    color: #f0ece4;
}

.stApp {
    background-color: #0e0e0e;
}

/* Header */
.cleo-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem 0;
    border-bottom: 1px solid #2a2a2a;
    margin-bottom: 2rem;
}

.cleo-title {
    font-family: 'DM Serif Display', serif;
    font-size: 3rem;
    letter-spacing: -1px;
    color: #f0ece4;
    margin: 0;
    line-height: 1;
}

.cleo-title span {
    color: #e8643a;
}

.cleo-subtitle {
    font-size: 0.85rem;
    color: #666;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.5rem;
}

/* Chat messages */
.message-user {
    display: flex;
    justify-content: flex-end;
    margin: 0.75rem 0;
}

.message-cleo {
    display: flex;
    justify-content: flex-start;
    margin: 0.75rem 0;
}

.bubble-user {
    background: #e8643a;
    color: #fff;
    padding: 0.75rem 1.1rem;
    border-radius: 18px 18px 4px 18px;
    max-width: 75%;
    font-size: 0.95rem;
    line-height: 1.5;
}

.bubble-cleo {
    background: #1a1a1a;
    color: #f0ece4;
    padding: 0.75rem 1.1rem;
    border-radius: 18px 18px 18px 4px;
    max-width: 75%;
    font-size: 0.95rem;
    line-height: 1.6;
    border: 1px solid #2a2a2a;
}

.avatar {
    font-size: 1.2rem;
    margin-right: 0.5rem;
    align-self: flex-end;
}

/* Sugestões rápidas */
.quick-chips {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-bottom: 1.5rem;
}

/* Input */
.stTextInput > div > div > input {
    background-color: #1a1a1a !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 12px !important;
    color: #f0ece4 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
}

.stTextInput > div > div > input:focus {
    border-color: #e8643a !important;
    box-shadow: 0 0 0 2px rgba(232, 100, 58, 0.15) !important;
}

.stTextInput > div > div > input::placeholder {
    color: #555 !important;
}

/* Botão enviar */
.stButton > button {
    background-color: #e8643a !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    padding: 0.6rem 1.4rem !important;
    transition: background 0.2s ease !important;
}

.stButton > button:hover {
    background-color: #d0512a !important;
}

/* Botões de sugestão */
.suggestion-btn > button {
    background-color: #1a1a1a !important;
    color: #aaa !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 20px !important;
    font-size: 0.8rem !important;
    padding: 0.3rem 0.9rem !important;
}

.suggestion-btn > button:hover {
    border-color: #e8643a !important;
    color: #e8643a !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0e0e0e; }
::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 4px; }

/* Remove streamlit defaults */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 720px; }
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cleo-header">
    <p class="cleo-title">Cle<span>o</span></p>
    <p class="cleo-subtitle">filmes · séries · livros</p>
</div>
""", unsafe_allow_html=True)

# ── Estado da sessão ────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "input_key" not in st.session_state:
    st.session_state.input_key = 0

# ── Renderizar histórico ────────────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="message-user">
            <div class="bubble-user">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="message-cleo">
            <span class="avatar">🎬</span>
            <div class="bubble-cleo">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Sugestões rápidas (só mostra se não tem histórico) ──────────────────────
suggestions = [
    "Quero um filme pra hoje à noite 🌙",
    "Série que prende desde o primeiro ep",
    "Livro pra ler na praia",
    "Algo de terror psicológico",
]

if not st.session_state.messages:
    st.markdown("""
    <p style="color:#555; font-size:0.85rem; margin-bottom:0.5rem;">Algumas ideias pra começar:</p>
    """, unsafe_allow_html=True)
    
    cols = st.columns(len(suggestions))
    for i, (col, suggestion) in enumerate(zip(cols, suggestions)):
        with col:
            with st.container():
                st.markdown('<div class="suggestion-btn">', unsafe_allow_html=True)
                if st.button(suggestion, key=f"suggest_{i}"):
                    st.session_state.messages.append({"role": "user", "content": suggestion})
                    response = ""
                    for chunk in stream_chat(st.session_state.messages):
                        response += chunk
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# ── Input do usuário ────────────────────────────────────────────────────────
st.markdown("<div style='height: 1.5rem'></div>", unsafe_allow_html=True)

col_input, col_btn = st.columns([5, 1])

with col_input:
    user_input = st.text_input(
        label="",
        placeholder="O que você quer assistir ou ler?",
        key=f"input_{st.session_state.input_key}",
        label_visibility="collapsed",
    )

with col_btn:
    send = st.button("→", use_container_width=True)

# ── Processar envio ─────────────────────────────────────────────────────────
if (send or user_input) and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})

    # Renderiza mensagem do usuário imediatamente
    st.markdown(f"""
    <div class="message-user">
        <div class="bubble-user">{user_input.strip()}</div>
    </div>
    """, unsafe_allow_html=True)

    # Stream da resposta
    with st.empty():
        response = ""
        placeholder = st.markdown("""
        <div class="message-cleo">
            <span class="avatar">🎬</span>
            <div class="bubble-cleo">...</div>
        </div>
        """, unsafe_allow_html=True)
        
        for chunk in stream_chat(st.session_state.messages):
            response += chunk
            st.markdown(f"""
            <div class="message-cleo">
                <span class="avatar">🎬</span>
                <div class="bubble-cleo">{response}▌</div>
            </div>
            """, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.input_key += 1
    st.rerun()

# ── Botão limpar conversa ───────────────────────────────────────────────────
if st.session_state.messages:
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    if st.button("↺ limpar conversa", key="clear"):
        st.session_state.messages = []
        st.session_state.input_key += 1
        st.rerun()
