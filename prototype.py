import gradio as gr
import requests
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

# Constants for calling the Azure OpenAI service
openai_api_type = "azure"
gpt_endpoint = "https://TODO.openai.azure.com/"            # Your endpoint will look something like this: https://YOUR_AOAI_RESOURCE_NAME.openai.azure.com/
gpt_api_key = "TODO"                                       # Your key will look something like this: 00000000000000000000000000000000
gpt_deployment_name="gpt-35-turbo"

# Create instance to call GPT model
gpt = AzureChatOpenAI(
    openai_api_base=gpt_endpoint,
    openai_api_version="2023-03-15-preview",
    deployment_name=gpt_deployment_name,
    openai_api_key=gpt_api_key,
    openai_api_type = openai_api_type,
)

def call_gpt_model(rag_from_bing, message):
    system_template="You are a professional, helpful assistant to provide resources to combat childhood hunger.  \n"
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    user_prompt=PromptTemplate(
        template="## Context \n {rag_from_bing} \n" +
                "## Instructions \n Using the above context, answer the question below.\n" +
                "## Question \n {message} \n",
        input_variables=["rag_from_bing", "message"],
    )
    human_message_prompt = HumanMessagePromptTemplate(prompt=user_prompt)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    # Get formatted messages for the chat completion
    messages = chat_prompt.format_prompt(rag_from_bing={rag_from_bing}, message={message}).to_messages()
    print("Messages")
    print(messages)

    # Call the model
    output = gpt(messages)
    print("Output")
    print(output)
    return output.content


def chat(message, history):

    # Get information from trusted sources
    # TODO
    # TODO - do we need logic here to see if we have sufficient trusted source data, or whether we even need to call Bing?  

    # Call Bing to get context
    # TODO - Bing logic here - set rag_from_bing variable to Bing response rather than the hardcoded below.  
    rag_from_bing = "To determine your eligibility for WIC in Michigan, you can use the online prescreening tool available at the Michigan Department of Health and Human Services website. The tool will ask you a series of questions related to your household size, income, and other factors to determine if you may be eligible for WIC benefits. You can access the tool here: https://www.michigan.gov/mdhhs/0,5885,7-339-71551_2945_42592---,00.html"

    # Call GPT model with context from Bing
    model_response =call_gpt_model(rag_from_bing, message)
    return model_response

# Get location 
# Gets the ip address of the request (user)
def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

# Fetches the location of the user based on the ip address
def get_location():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data
print(get_location())

chatbot = gr.Chatbot(bubble_full_width = False)
chat_interface = gr.ChatInterface(fn=chat, 
#                 title="Title here", 
#                 description="Description here", 
                 chatbot=chatbot)

chat_interface.launch()