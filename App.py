import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # reads GROQ_API_KEY from .env

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_roadmap(domain, level, time_to_learn):
    prompt = f"""
You are an expert curriculum designer and mentor.

Create a detailed, structured learning roadmap for the following:
- Domain/Field: {domain}
- Current skill level: {level}
- Time available to learn: {time_to_learn}

Requirements:
- Break the roadmap into weekly or phase-based milestones (adapt to the time given)
- For each phase, list: topics to learn, why they matter, and 1-2 recommended resource types (not fake links, just resource types e.g. "official docs", "YouTube course", "practice project")
- Include a small practical project idea at the end of each phase
- End with 2-3 tips specific to succeeding in {domain} at the {level} level
- Format the output in clean Markdown with headers and bullet points
"""

    response = client.chat.completions.create(
    model="openai/gpt-oss-120b",   # replace llama-3.3-70b-versatile
    messages=[
        {"role": "system", "content": "You are a helpful, precise learning roadmap generator."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    max_tokens=2048,
)

    return response.choices[0].message.content

import gradio as gr

def roadmap_ui(domain, level, time_to_learn):
    if not domain.strip():
        return "⚠️ Please enter a domain/field."
    return generate_roadmap(domain, level, time_to_learn)

with gr.Blocks(title="AI Learning Roadmap Generator") as demo:
    gr.Markdown("## 🧭 AI Learning Roadmap Generator")
    gr.Markdown("Enter a field, your current level, and how much time you have — get a personalized roadmap.")

    with gr.Row():
        domain_input = gr.Textbox(label="Domain / Field", placeholder="e.g. Web Development, Data Science, UI/UX")
        level_input = gr.Dropdown(choices=["Beginner", "Intermediate", "Advanced"], label="Skill Level", value="Beginner")
        time_input = gr.Textbox(label="Time to Learn", placeholder="e.g. 2 months, 6 weeks, 1 year")

    generate_btn = gr.Button("Generate Roadmap", variant="primary")
    output = gr.Markdown(label="Your Roadmap")

    generate_btn.click(fn=roadmap_ui, inputs=[domain_input, level_input, time_input], outputs=output)

if __name__ == "__main__":
    demo.launch()