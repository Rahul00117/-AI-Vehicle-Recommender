import gradio as gr
from openai import OpenAI

# ✅ Gemini API Setup
gemini_key = "AIzaSyBDJ3nvuCbvNA0e3nuri2Fjt7V5Xfis4Zs"
model = OpenAI(api_key=gemini_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai")

# 🔮 Gemini LLM Call with Strong Prompt for Images
def my_google_llm(myprompt):
    try:
        response = model.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a vehicle expert AI assistant.\n"
                        "Suggest 2–3 vehicles with the following info:\n"
                        "- Model Name\n- Brand\n- Fuel\n- Transmission\n- Seating Capacity\n- Price (INR)\n"
                        "- Reason for recommendation\n"
                        "- Show a real vehicle image using Markdown format: ![Alt](https://...jpg/png)\n"
                        "Only use image links from trusted sources such as:\n"
                        "- https://upload.wikimedia.org\n"
                        "- https://www.autocarindia.com\n"
                        "- https://www.carwale.com\n"
                        "- https://www.bikewale.com\n"
                        "Avoid Google Drive, Pinterest, Unsplash, or private links. Ensure image is accessible via browser."
                    )
                },
                {"role": "user", "content": myprompt}
            ]
        )
        result = response.choices[0].message.content
        print(result)
        print("🔍 Gemini Output:\n", result)  # 🔧 For Debugging Image Links
        return result
    except Exception as e:
        return f"❌ Error: {str(e)}"

# 🏍️ 2-Wheeler Recommender
def recommend_2wheeler(fuel, budget, brand, usage, look, extra):
    prompt = f"""
    I need 2–3 **2-wheeler** recommendations for a user with these preferences:
    - Fuel Type: {fuel}
    - Budget: ₹{budget}
    - Brand: {brand}
    - Usage: {usage}
    - Style: {look}
    - Extra: {extra or 'None'}
    
    Include:
    - Model Name
    - Brand
    - Fuel
    - Transmission
    - Seating (max 2)
    - Price (INR)
    - Reason for recommendation
    - Show real image using Markdown format: ![Alt](ImageURL)
    Ensure image is from Wikimedia, Autocar India, or BikeWale.
    """
    return my_google_llm(prompt)

# 🚗 4-Wheeler Recommender
def recommend_4wheeler(fuel, budget, brand, seating, usage, transmission, look, extra):
    prompt = f"""
    I need 2–3 **4-wheeler** recommendations for a user with these preferences:
    - Fuel: {fuel}
    - Budget: ₹{budget}
    - Brand: {brand}
    - Seating: {seating}
    - Usage: {usage}
    - Transmission: {transmission}
    - Style: {look}
    - Extra: {extra or 'None'}
    
    Include:
    - Model Name
    - Brand
    - Fuel
    - Transmission
    - Seating
    - Price (INR)
    - Reason
    - Image in Markdown: ![Alt](ImageURL)
    Use image links only from Wikimedia, CarWale, or trusted public sources.
    """
    return my_google_llm(prompt)

# 🖥️ Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 🚘 Gemini AI Vehicle Recommender System (With Real Images)")

    with gr.Tab("🏍️ 2-Wheeler Recommendation"):
        with gr.Row():
            fuel_2 = gr.Radio(["Petrol", "Electric"], label="Fuel Type")
            budget_2 = gr.Slider(20000, 250000, step=1000, label="Budget (₹)", value=70000)
        brand_2 = gr.Dropdown(["Any", "Hero", "Honda", "TVS", "Bajaj", "Yamaha", "Ola", "Ather"], label="Brand")
        usage_2 = gr.Dropdown(["Daily Commute", "Touring", "Sport", "Delivery"], label="Usage")
        look_2 = gr.Textbox(label="Look & Style (e.g. Sporty, Retro)")
        extra_2 = gr.Textbox(label="Other Preferences")
        out_2 = gr.Markdown()
        btn_2 = gr.Button("Get 2-Wheeler Suggestions")
        btn_2.click(recommend_2wheeler, [fuel_2, budget_2, brand_2, usage_2, look_2, extra_2], out_2)

    with gr.Tab("🚗 4-Wheeler Recommendation"):
        with gr.Row():
            fuel_4 = gr.Radio(["Petrol", "Diesel", "Electric", "Hybrid"], label="Fuel Type")
            budget_4 = gr.Slider(300000, 2000000, step=10000, label="Budget (₹)", value=600000)
        with gr.Row():
            brand_4 = gr.Dropdown(["Any", "Maruti", "Tata", "Hyundai", "Honda", "Kia", "Toyota", "MG", "Mahindra"], label="Brand")
            seating_4 = gr.Slider(4, 9, step=1, label="Seating Capacity")
            transmission_4 = gr.Radio(["Manual", "Automatic", "CVT", "Any"], label="Transmission")
        usage_4 = gr.Dropdown(["City", "Family", "Long Drive", "Commercial", "Luxury"], label="Usage Purpose")
        look_4 = gr.Textbox(label="Look & Style (e.g. Sleek, Bold)")
        extra_4 = gr.Textbox(label="Other Preferences")
        out_4 = gr.Markdown()
        btn_4 = gr.Button("Get 4-Wheeler Suggestions")
        btn_4.click(recommend_4wheeler, [fuel_4, budget_4, brand_4, seating_4, usage_4, transmission_4, look_4, extra_4], out_4)

# 🔁 Launch
demo.launch(show_api=False, show_error=False)
