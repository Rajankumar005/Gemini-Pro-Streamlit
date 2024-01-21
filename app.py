import streamlit as st
from PIL import Image
import google.generativeai as genai
import streamlit as st

# Define the CSS styles
css = """
/* Neomorphic Styles */
:root {
  --background-color: #e0e0e0;
  --primary-color: #c98bdb;
  --secondary-color: #5591f5;
  --text-color: black;
  --shadow-color: #d3d3d3;
  --highlight-color: #ffffff;
  --border-radius: 10px;
}

body {
  background-color: var(--background-color);
  font-family: Arial, sans-serif;
}

.neumorphic {
  background-color: var(--background-color);
  border-radius: var(--border-radius);
  box-shadow: 5px 5px 10px var(--shadow-color),
              -5px -5px 10px var(--highlight-color);
}

.neumorphic:hover {
  box-shadow: 20px 20px 20px var(--shadow-color),
              -10px -10px 20px var(--highlight-color);
}

.neumorphic-button {
  background-color: var(--primary-color);
  color: var(--text-color);
  border: none;
  border-radius: var(--border-radius);
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

.neumorphic-button:hover {
  background-color: var(--secondary-color);
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 100px);
  overflow-y: auto;
}

.chat-message {
  display: flex;
  align-items: center;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: var(--border-radius);
}

.chat-message-user {
  background-color: var(--primary-color);
  color: var(--text-color);
  margin-right: auto;
}

.chat-message-assistant {
  background-color: var(--secondary-color);
  color: var(--text-color);
  margin-left: auto;
}

.chat-input {
  width: 100%;
  padding: 10px;
  border-radius: var(--border-radius);
  margin-top: 10px;
}
"""


st.set_page_config(page_title="Gemini Pro with Streamlit",page_icon="♊")

st.write("Welcome to the Gemini Pro Dashboard. You can proceed by providing your Google API Key")

ms = st.session_state
if "themes" not in ms: 
  ms.themes = {"current_theme": "light",
                    "refreshed": True,

                    "light": {"theme.base": "dark",
                             
                              "button_face": "🌜"},

                    "dark":  {"theme.base": "light",
                             
                              "button_face": "🌞"},
                    }


def ChangeTheme():
  previous_theme = ms.themes["current_theme"]
  tdict = ms.themes["light"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]
  for vkey, vval in tdict.items(): 
    if vkey.startswith("theme"): st._config.set_option(vkey, vval)

  ms.themes["refreshed"] = False
  if previous_theme == "dark": ms.themes["current_theme"] = "light"
  elif previous_theme == "light": ms.themes["current_theme"] = "dark"


btn_face = ms.themes["light"]["button_face"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]["button_face"]

with st.expander("Provide Your Google API Key"):
     google_api_key = st.text_input("Google API Key", key="google_api_key", type="password")

if not google_api_key:#
    st.info(" *** Enter Your Own Google Token Key ***")
    st.stop()

genai.configure(api_key=google_api_key)
st.button(btn_face, on_click=ChangeTheme)

if ms.themes["refreshed"] == False:
  ms.themes["refreshed"] = True
  st.rerun()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
st.title("Gemini Pro How can I help you today?")

with st.sidebar:
    option = st.selectbox('Choose Your Model',('gemini-pro', 'gemini-pro-vision'))

    if 'model' not in st.session_state or st.session_state.model != option:
        st.session_state.chat = genai.GenerativeModel(option).start_chat(history=[])
        st.session_state.model = option

    #st.write("Adjust Your Parameter Here:")
    # temperature = st.number_input("Temperature", min_value=0.0, max_value= 1.0, value =0.5, step =0.01)
    # max_token = st.number_input("Maximum Output Token", min_value=0, value =100)
    #gen_config = genai.types.GenerationConfig(max_output_tokens=max_token,temperature=temperature)

    st.divider()

    upload_image = st.file_uploader("Upload Your Image Here", accept_multiple_files=False, type = ['jpg', 'png'])

    if upload_image:
        image = Image.open(upload_image)
    st.divider()

    if st.button("Clear Chat History"):
        st.session_state.messages.clear()
        st.session_state["messages"] = [{"role": "assistant", "content": "Hi there. Can I help you?"}]

    st.divider()
    st.markdown("""<span ><font size=1>Connect With Me</font></span>""",unsafe_allow_html=True)
    "[Linkedin](https://www.linkedin.com/in/rajan-kumar-4a5383154/)"
    "[GitHub](https://github.com/Rajankumar005?tab=repositories)"

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi there. Can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if upload_image:
    if option == "gemini-pro":
        st.info("Please Switch to the Gemini Pro Vision")
        st.stop()
    if prompt := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            response=st.session_state.chat.send_message([prompt,image],stream=True)
            response.resolve()
            msg=response.text

            st.session_state.chat = genai.GenerativeModel(option).start_chat(history=[])
            st.session_state.messages.append({"role": "assistant", "content": msg})

            st.image(image,width=300)
            st.chat_message("assistant").write(msg)

else:
    if prompt := st.chat_input():

            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)

            response=st.session_state.chat.send_message(prompt,stream=True)
            response.resolve()
            msg=response.text
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant").write(msg)
