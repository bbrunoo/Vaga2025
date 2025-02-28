import os
from langchain_core.prompts import ChatPromptTemplate 
from langchain_groq import ChatGroq
import json

#The API key was created in a virtual environment on the machine.
api_key = os.getenv("GROQ_API_KEY")

#Configuring the Groq call
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0.0,
    max_retries=2,
    api_key=api_key,
    max_tokens=None,
    timeout=None
)

#Function that checks if the question is related to mathematics
def verify_question(question):
    acceptable = r"[0-9\+\-\=\*\/]"
    return any(caracter in acceptable for caracter in question)


# Loop to ask questions until they are related to mathematics.
while True:
    question_input = input("Write your question (or type 'exit' to quit): ")
    
    #Breaking the call if typed exit
    if question_input == "exit":
        print("Exiting...")
        break
    
    #Create the JSON for the question
    question_json={
        "category":"math",
        "question":question_input
    }

    #Get the question asked by the user
    question_str = json.dumps(question_input)
    
    #Verify and send the question to the AI
    if verify_question(question_input):
        prompt = ChatPromptTemplate.from_template(
            "Based on the category {category}, answer the follow question: {question}"
        )
        
        #Format the question into JSON
        formatted_prompt = prompt.format(**question_json)
        
        #Generate the AI response
        response = llm.invoke(formatted_prompt)
        
        print("AI anwser", response)
    else:
        #If it is not related to mathematics, the verification will end and return to the loop.
        print("Write something related to mathematic")    
