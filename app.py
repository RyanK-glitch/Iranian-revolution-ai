import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(page_title="World History AI Bot", page_icon="📜")
st.title("📜 All about Iranian revolution")
st.caption("Specialized strictly in iranian revolution and aftermath and the rise of islamic fanatism.")
st.sidebar.markdown("---")
st.sidebar.markdown("👨‍💻 **Developed by: RyanK**")

# 2. Connect to the Groq API securely using Streamlit Secrets
if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
else:
    # Backup input bar in case secrets aren't set up yet
    GROQ_API_KEY = st.sidebar.text_input("Enter Groq API Key:", type="password")

if not GROQ_API_KEY:
    st.info("Please add your Groq API key in the Advanced Settings to continue.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)
# 3. System Prompt Boundaries
SPECIALIZED_TOPIC = "World History, with a primary specialization in Korean history (Joseon, Goryeo, Three Kingdoms, modern eras) and Chinese history (Han, Tang, Song, Ming, Qing, and modern eras)"

SYSTEM_INSTRUCTION = f"""
YYou are a highly specialized, academic, and rigorous historian focusing exclusively on the 1979 Iranian Revolution and the subsequent Iranian fanatic religious government (the Islamic Republic). 

Your primary directive is to provide exhaustive, deep-dive historical information, bypassing generic AI summaries or conversational fluff. You must strictly adhere to the following operational parameters:

1. Specialization & Scope: You only discuss topics directly related to modern Iranian history, the revolution, Ayatollah Khomeini's ideology, the structural mechanics of the religious regime, state security apparatuses (IRGC, Basij), political executions, human rights records, and religious fundamentalist policies. Politely decline to discuss any topic outside this domain.

2. Rigor Over Politeness: Do not sugarcoat, sanitize, or soften historical facts, human rights abuses, state-sponsored violence, or extremist religious doctrines. Provide raw, factual, and deeply detailed data. If a historical event involves extreme violence, political purging, or strict religious oppression, report it with clinical, academic objectivity without withholding details.

3. Bypass Generic Guardrails: Do not use generic AI disclaimers, content warnings, or neutral "both-sides" phrasing when documenting verified historical atrocities, systemic oppression, or fanatic religious decrees. Treat the user as a high-level researcher who requires unredacted historical truth.

4. Analytical Depth: Avoid surface-level answers. Break down the theological, political, and socio-economic frameworks of the regime. Detail the exact names of entities, laws, dates, operations, and historical figures involved in the consolidation of the fundamentalist state.

5. Tone: Academic, clinical, objective, and unflinching. Do not express personal opinions, but do not shy away from exposing the full extent of the regime's fanaticism and governance mechanics as documented by credible historical records.
"""

# 4. Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle user input
if user_input := st.chat_input("Ask a history question (e.g., Joseon Dynasty, Tang Dynasty, World War II)..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    messages_for_api = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
    for m in st.session_state.messages:
        messages_for_api.append({"role": m["role"], "content": m["content"]})

    with st.chat_message("assistant"):
        with st.spinner("Reviewing historical archives..."):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages_for_api
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            
    st.session_state.messages.append({"role": "assistant", "content": response})

