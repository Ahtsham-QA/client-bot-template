"""
Starter Client Chatbot Template
--------------------------------
A simple, adaptable Streamlit + Claude API chatbot you can reuse for
different small-business clients. Swap in their FAQ/knowledge base
and branding to spin up a new demo fast.

SETUP:
1. pip install streamlit anthropic
2. Set your API key as an environment variable:
   export ANTHROPIC_API_KEY="your-key-here"
3. Run: streamlit run client_chatbot_template.py

CUSTOMIZING FOR A NEW CLIENT:
- Edit BUSINESS_NAME, BUSINESS_KNOWLEDGE, and SYSTEM_PROMPT below.
- That's it for a basic FAQ bot. For larger knowledge bases, see the
  "SCALING UP" notes at the bottom of this file.
"""

import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from anthropic import Anthropic

# ============================================================
# 1. CLIENT-SPECIFIC CONFIG — edit this section per client
# ============================================================

BUSINESS_NAME = "Demo Dental Clinic"

# Paste the client's FAQ, hours, services, policies, etc. here.
# For a small business, this can just be plain text — Claude will
# use it as context to answer questions accurately.
BUSINESS_KNOWLEDGE = """
Business: Demo Dental Clinic (placeholder — replace with real client info)
Hours: Mon-Fri 8am-5pm, Sat 9am-1pm, Closed Sundays
Services: General checkups, cleanings, whitening, Invisalign, emergency dental care
Location: 12300 Main St, Springfield
Insurance: Accepts most major PPO plans; ask staff for details on your specific plan
New patients: $50 off first cleaning, mention code NEWPATIENT
Emergencies: Call the office directly at (111) 000-0000 for same-day emergency slots
"""

SYSTEM_PROMPT = f"""You are a helpful assistant for {BUSINESS_NAME}.
Answer customer questions using ONLY the information below. If you don't
know the answer, politely tell the customer to call the office directly.
Keep answers short, friendly, and professional.

BUSINESS INFORMATION:
{BUSINESS_KNOWLEDGE}
"""

# ============================================================
# 2. APP SETUP
# ============================================================

st.set_page_config(page_title=f"{BUSINESS_NAME} Assistant", page_icon="💬")
st.title(f"💬 {BUSINESS_NAME} Assistant")
st.caption("Ask me about hours, services, pricing, or booking.")

# Initialize Claude client
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# ============================================================
# 3. DISPLAY CHAT HISTORY
# ============================================================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ============================================================
# 4. HANDLE NEW USER INPUT
# ============================================================

user_input = st.chat_input("Type your question here...")

if user_input:
    # Show user message immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Build message history for the API call (last 10 turns to keep it light)
    api_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages[-10:]
    ]

    # Call Claude API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.messages.create(
                    model="claude-sonnet-4-5",  # swap model as needed
                    max_tokens=500,
                    system=SYSTEM_PROMPT,
                    messages=api_messages,
                )
                answer = response.content[0].text
            except Exception as e:
                answer = f"Sorry, something went wrong: {e}"

            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

# ============================================================
# SCALING UP (for later, once you have paying clients)
# ============================================================
# - Bigger knowledge base: instead of pasting everything into
#   SYSTEM_PROMPT, chunk the client's docs, embed them (e.g. using
#   a vector DB like Chroma or Pinecone), and retrieve only the
#   relevant chunks per question (RAG pattern).
# - Logging: save conversations to a Google Sheet, Airtable, or DB
#   so the client can review what customers are asking.
# - Handoff: add a button like "Talk to a human" that emails/Slacks
#   the business owner with the chat transcript.
# - Branding: swap st.set_page_config icon/title, add client logo
#   with st.image(), adjust colors via a custom Streamlit theme
#   (.streamlit/config.toml).
# - Deployment: Streamlit Community Cloud (free, good for demos),
#   or Render/Railway ($5-10/mo) for a client's live production bot.