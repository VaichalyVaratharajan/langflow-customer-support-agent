import requests
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "0aeb782b-be53-4b98-a25a-65c2eafbdf08"
FLOW_ID = "698da4e3-5cc1-4462-bde6-043614ac1fac"
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
ENDPOINT = "customerTemplate" # The endpoint name of the flow


def run_flow(message: str) -> dict:

    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = None
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def main():
    st.title("Chat Interface")
    
    message = st.text_area("Message", placeholder="Ask something...")
    
    if st.button("Run Flow"):
        if not message.strip():
            st.error("Please enter a message")
            return
    
        try:
            with st.spinner("Running flow..."):
                response = run_flow(message)
            
            response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            st.markdown(response)
        except Exception as e:
            st.error(str(e))

if __name__ == "__main__":
    main()