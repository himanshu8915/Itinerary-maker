from dotenv import load_dotenv
import os
import groq

load_dotenv()

class AIAssistant:
    def __init__(self):
        self.client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama3-70b-8192"

    def chat(self, message, itinerary):
        prompt = f"""
        You are a travel assistant helping modify this itinerary:
        
        **Current Itinerary**:
        {itinerary}

        **User Request**:
        {message}

        **Rules**:
        1. If modifying, return COMPLETE updated itinerary in markdown
        2. Preserve all original formatting and special requests
        3. For discussions, respond conversationally
        4. Never use JSON/code blocks
        """
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            temperature=0.5
        )
        return response.choices[0].message.content