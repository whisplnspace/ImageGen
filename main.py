import streamlit as st
import requests
from PIL import Image

# DeepAI API key
api_key = "fd5ecd3c-4d3a-43c9-8dd7-f37506ece0fc"
url = "https://api.deepai.org/api/text2img"

# Streamlit UI styling
st.set_page_config(page_title="AI Image Generator", page_icon=":art:", layout="wide")
st.markdown("""
    <style>
    body {
        background-color: #f0f4f8;
        font-family: 'Arial', sans-serif;
    }
    .title {
        color: #4b89dc;
        font-size: 2.5rem;
        text-align: center;
        font-weight: bold;
        margin-bottom: 30px;
    }
    .description {
        color: #8e8e8e;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 30px;
    }
    .prompt-input {
        font-size: 1.5rem;
        padding: 10px;
        width: 80%;
        margin: 20px auto;
        border-radius: 10px;
        border: 2px solid #ddd;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    }
    .generate-btn {
        background-color: #4b89dc;
        color: white;
        font-size: 1.2rem;
        padding: 10px 20px;
        border-radius: 10px;
        width: 50%;
        margin: 20px auto;
        cursor: pointer;
        border: none;
    }
    .generate-btn:hover {
        background-color: #3d6fa7;
    }
    .image-display {
        text-align: center;
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit Header and Description
st.markdown('<h1 class="title">🎨 AI Image Generator</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="description">Generate stunning images from text descriptions using DeepAI’s Text2Image API. Enter a description and see the magic happen!</p>',
    unsafe_allow_html=True)

# Input for user prompt
user_prompt = st.text_input("Enter your image prompt:", "A futuristic city skyline at sunset with flying cars",
                            key="prompt", placeholder="E.g., A cat flying through space")

# Button to generate image
generate_button = st.button("Generate Image", key="generate", help="Click to generate image from the text prompt",
                            use_container_width=True)


# Function to call the API and get image
def generate_image_from_text(prompt):
    response = requests.post(
        url,
        data={'text': prompt},
        headers={'api-key': api_key}
    )

    if response.status_code == 200:
        image_url = response.json().get('output_url')
        return image_url
    else:
        st.error(f"Error generating image: {response.status_code} - {response.text}")
        return None


# If the user presses the "Generate Image" button
if generate_button and user_prompt:
    with st.spinner("Generating image... Please wait!"):
        image_url = generate_image_from_text(user_prompt)

        if image_url:
            # Display the generated image
            st.markdown('<div class="image-display"><h3>Generated Image:</h3></div>', unsafe_allow_html=True)
            image_response = requests.get(image_url)
            img = Image.open(image_response.raw)
            st.image(img, caption=user_prompt, use_column_width=True)

            # Download link for the image
            st.markdown(f"[Download the Image]( {image_url} )", unsafe_allow_html=True)

# Footer information
st.sidebar.header("About")
st.sidebar.info("""
    This web app uses DeepAI's Text2Image API to generate images based on your textual descriptions. 
    Simply enter a description, and watch the AI bring it to life!
""")
