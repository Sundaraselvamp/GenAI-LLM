import streamlit as st 
from dotenv import load_dotenv
load_dotenv()
import os 
import google.generativeai as genai 


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


prompt=""" you are a receipe generator and cook assistant. you will be taking the user's query and generating a receipe based on their preferences.
    User Query:{user_query}
    Receipe:
    Title:
    Ingredients:
    Instructions:
    """
## Getting the user's query from streamlit interface
def get_user_query():
    query=st.text_input("Ask me a Question about Cooking")
    return query

## Getting the receipe based on user's query from gemini pro
def generate_gemini_receipe(user_query):
    ## Prepare the prompt with the user's query
    prepared_prompt=prompt.format(user_query=user_query)

    ## send the prompt to gemini api 
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prepared_prompt)

        ## extract the receipe from the response
    receipe=response.text

        # parse the receipe into title,ingredients, instrucrions
    receipe_title=receipe.split('\n')[1]
    receipe_ingredients=receipe.split('\n')[3:-2]
    receipe_instructions=receipe.split('\n')[-2:]

        # return the receipe as dict
    return {
        "title":receipe_title,
        "ingredients":receipe_ingredients,
        "instructions":receipe_instructions
        }

def main():
    ## get uesr query
    user_query=get_user_query()

    ## generate the receipe from the user's query
    if user_query:
        receipe=generate_gemini_receipe(user_query)

        ## display the receipe in streamlit interface
        st.header(receipe["title"])
        
        st.subheader("Ingredients:")
        for ingredient in receipe["ingredients"]:
            st.write(f'-{ingredient}')
        
        st.subheader("Instructions:")
        for instruction in receipe["instructions"]:
            st.write(f'{instruction}')

if __name__ == "__main__":
    main()

