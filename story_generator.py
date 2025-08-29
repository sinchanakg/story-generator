import streamlit as st
from transformers import pipeline, set_seed

# Load the text generation model
@st.cache_resource
def load_model():
    generator = pipeline("text-generation", model="distilgpt2")
    set_seed(42)
    return generator

generator = load_model()

# Length map
length_map = {
    "Short": 100,
    "Medium": 200,
    "Long": 300
}

# Streamlit UI
st.title("AI Story Generator")
st.write("Generate a story based on your topic, tone, and preferred length.")

topic = st.text_input("Enter a topic (e.g., dragons, friendship, time travel):")
tone = st.selectbox("Choose a tone:", ["Fantasy", "Horror", "Sci-fi", "Funny", "Mystery", "Adventure"])
length_choice = st.radio("Select story length:", ["Short", "Medium", "Long"])
num_stories = st.slider("How many stories do you want?", 1, 3, 1)
save_file = st.checkbox("Save story to a file")

if st.button("Generate Story"):
    if topic.strip() == "":
        st.warning("Please enter a topic.")
    else:
        max_len = length_map.get(length_choice, 150)
        stories = []

        for i in range(num_stories):
            prompt = f"Write a {tone.lower()} story about {topic}. Once upon a time,"
            result = generator(prompt, max_length=max_len, num_return_sequences=1)
            story = result[0]['generated_text']
            stories.append(story)
            st.markdown(f"### Story {i+1}")
            st.write(story)

        if save_file:
            filename = f"story_{topic.replace(' ', '_')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                for idx, story in enumerate(stories):
                    f.write(f"--- Story {idx + 1} ---\n{story}\n\n")
            st.success(f"Stories saved to {filename}")