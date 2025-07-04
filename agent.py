import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv

load_dotenv()

KEY=os.getenv("GEMINI_API_KEY")


llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")

class WaterIntakeAgent:
     def __init__(self):
          self.history=[]
          
     def analyse_intake(self,intake_ml):
               prompt=f"""
               you are a hydration assistant.The user has consumed {intake_ml} ml of water today.
               Provide a hydration status and suggest if they need to drink more water """
  
               message = HumanMessage(content=prompt)
               response = llm.invoke([message])

               return response.content
          
if __name__=="__main__":
     agent=WaterIntakeAgent()
     intake=1500
     feedback=agent.analyse_intake(intake)
     print(feedback)