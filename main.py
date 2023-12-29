import openai
import streamlit as st
from llama_index import VectorStoreIndex, download_loader
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from streamlit_chat import message
import panel as pn
from panel.chat import ChatInterface

pn.extension("vega")

def myApp():
    # Download SimpleWebPageReader
    SimpleWebPageReader = download_loader("SimpleWebPageReader")

    # Set OpenAI API key
    openai.api_key = "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"  # Replace with your actual API key

    st.header("Chat with Web")

    # Input for the website URL
    website_url = st.text_input("Website URL", key="url")

    if website_url:
        try:
            # Initialize SimpleWebPageReader with the provided website URL
            loader = SimpleWebPageReader()
            documents = loader.load_data(urls=[website_url])

            # Create VectorStoreIndex from documents
            index = VectorStoreIndex.from_documents(documents)

            # Initialize LangChain OpenAI
            llm = OpenAI(openai_api_key="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", temperature=0, streaming = true)

            # Initialize ConversationBufferMemory
            memory = ConversationBufferMemory(memory_key="chat_history")

            # Initialize agent chain
            tools = [
                Tool(
                    name="Website Index",
                    func=lambda q: index.as_query_engine(),
                    description="Useful when you want to answer questions about the text on websites.",
                ),
            ]
            query_engine = index.as_query_engine()

            # Get user input for the query
            user_query = st.text_input("Your Question")

            if st.button("Ask"):
                # Query the LangChain agent with user input
                message(user_query, is_user=True)
                response = query_engine.query(user_query)

                # Display the response
                st.text("Response:")
                message(str(response))

        except Exception as e:
            st.error(f"An error occurred: {e}")
        ChatInterface(
            callback=even_or_odd,
            user="Asker",
            avatar="?",
            callback_user="Counter",
        )
        ChatMessage(
            "Want to hear some beat boxing?",
            user="Beat Boxer",
            avatar="🎶",
            height=250,
            sizing_mode="stretch_width",
            max_width=600,
            styles={"background": "#CBC3E3"},
        )

        def callback(contents, user, instance):
            callback_handler = pn.chat.langchain.PanelCallbackHandler(instance)
            return agent.run(contents, callbacks=[callback_handler])

        pn.chat.ChatInterface(callback=callback).servable()
if __name__ == "__main__":
    myApp()