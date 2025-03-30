from dotenv import load_dotenv
import os
import groq

load_dotenv()

class AItineraryGenerator:
    def __init__(self):
        self.client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama3-70b-8192"

    def generate(self, destination, days, budget, currency, style, companions, requests=""):
        prompt = f"""
        Create a detailed {days}-day itinerary for {destination} with:
        - **Budget**: {currency} {budget:,}
        - **Style**: {style}
        - **Companions**: {companions}
        - **Special Requests**: {requests if requests else "None"}

        **Format Rules**:
        1. Start with "## {destination} Itinerary ({days} days)"
        2. Use Day 1/Day 2 headings with time slots
        3. Include costs in {currency}
        4. Bold important items (**Hotel**, **Flight**)
        5. Keep special requests visible
        """
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            temperature=0.3
        )
        return response.choices[0].message.content