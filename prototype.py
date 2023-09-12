import gradio as gr
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import bingsearch

# Constants for calling the Azure OpenAI service
openai_api_type = "azure"
gpt_endpoint = ""            # Your endpoint will look something like this: https://YOUR_AOAI_RESOURCE_NAME.openai.azure.com/
gpt_api_key = ""                  # Your key will look something like this: 00000000000000000000000000000000
gpt_deployment_name="gpt-35-turbo-16k"
bing_endpoint = "https://api.bing.microsoft.com/v7.0/search"
bing_api_key = ""

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

    # Get location and pass it to Bing call below
    # TODO

    # Get information from trusted sources
    # TODO
    # TODO - do we need logic here to see if we have sufficient trusted source data, or whether we even need to call Bing?  

    # Call Bing to get context
    query =  "Determine eligibility for SNAP - Supplemental Nutrition Assistance Program(Food Stamps), WIC- Women, Infants and Children, SFSP and SSO (summer food services for kids)"
    bing_response = bingsearch.call_search_api(query, bing_endpoint, bing_api_key)
    # rag_from_bing = "To determine your eligibility for WIC in Michigan, you can use the online prescreening tool available at the Michigan Department of Health and Human Services website. The tool will ask you a series of questions related to your household size, income, and other factors to determine if you may be eligible for WIC benefits. You can access the tool here: https://www.michigan.gov/mdhhs/0,5885,7-339-71551_2945_42592---,00.html"
    rag_from_bing = bing_response;
    # Call GPT model with context from Bing
    model_response =call_gpt_model(rag_from_bing, message)
    return model_response


chatbot = gr.Chatbot(bubble_full_width = False)
chat_interface = gr.ChatInterface(fn=chat, 
#                 title="Title here", 
#                 description="Description here", 
                 chatbot=chatbot)

chat_interface.launch()